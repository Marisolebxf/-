#!/usr/bin/env node
/**
 * sync-feishu-daily-snapshot.mjs —— 当日进展 → 飞书「GKX 当日进展」出站
 * ---------------------------------------------------------------------------
 * 真源：agent-delivery/工程过程/当日进展/YYYY-MM-DD.md
 * 配置：agent-delivery/feishu/feishu-daily-snapshot-board.yaml
 * 用法：node scripts/sync-feishu-daily-snapshot.mjs [--date YYYY-MM-DD] [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0）。
 * 纪律：只出站；同日按「行键」upsert，删掉当日快照里已不存在的行。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-daily-snapshot-board.yaml');
const SOURCE_DIR = path.join(ORCH_ROOT, 'agent-delivery', '工程过程', '当日进展');

const DRY_RUN = process.argv.includes('--dry-run');
const dateArg = (() => {
  const i = process.argv.indexOf('--date');
  return i >= 0 ? process.argv[i + 1] : '';
})();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const WBS_DIM = {
  '02': '对接三要素',
  '03': '专题系统集成',
  '04': '门户系统集成',
  '05': '展示系统集成',
  '06': 'GDF数据治理集成',
  '07': '图数据库集成',
};

function loadBoardConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const get = (key) => (raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  // 必须从 field_names 段取列名，避免命中 bitable.daily / bitable.summary
  const parseFieldBlock = (section) => {
    const fnSection = raw.match(/^field_names:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m)?.[1] || '';
    const re = new RegExp(`^ {2}${section}:\\s*\\r?\\n((?: {4}.+\\r?\\n)+)`, 'm');
    const block = fnSection.match(re)?.[1] || '';
    const out = {};
    for (const line of block.split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"([^"]+)"/);
      if (m) out[m[1]] = m[2];
    }
    return out;
  };
  const statusOptions = [];
  const so = raw.match(/^status_options:\s*\r?\n((?:\s+-\s+".+"\r?\n)+)/m);
  if (so) {
    for (const line of so[1].split(/\r?\n/)) {
      const m = line.match(/^\s+-\s+"([^"]+)"/);
      if (m) statusOptions.push(m[1]);
    }
  }
  const dailyFields = parseFieldBlock('daily');
  const summaryFields = parseFieldBlock('summary');
  if (!dailyFields.row_key || !dailyFields.status) {
    throw new Error('feishu-daily-snapshot-board.yaml#field_names.daily 解析失败（缺 行键/完成状态）');
  }
  return {
    appToken: get('app_token'),
    daily: { tableName: get('table_name') || '当日八列', tableId: '' },
    summary: { tableName: '维度汇总', tableId: '' },
    fieldNames: { daily: dailyFields, summary: summaryFields },
    statusOptions,
    raw,
  };
}

function refineTableIds(cfg) {
  const raw = cfg.raw;
  const dailyBlock = raw.match(/^ {2}daily:\s*\r?\n((?: {4}.+\r?\n)+)/m)?.[1] || '';
  const summaryBlock = raw.match(/^ {2}summary:\s*\r?\n((?: {4}.+\r?\n)+)/m)?.[1] || '';
  const pick = (block, key) => (block.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  const pickName = (block) => pick(block, 'table_name');
  cfg.daily.tableName = pickName(dailyBlock) || cfg.daily.tableName;
  cfg.daily.tableId = pick(dailyBlock, 'table_id');
  cfg.summary.tableName = pickName(summaryBlock) || '维度汇总';
  cfg.summary.tableId = pick(summaryBlock, 'table_id');
  return cfg;
}

function backfillYaml(pathKey, tableId) {
  // pathKey: daily | summary
  let raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const re = new RegExp(`( {2}${pathKey}:\\s*\\r?\\n(?: {4}.+\\r?\\n)*? {4}table_id:\\s*)""`);
  if (!re.test(raw)) return;
  raw = raw.replace(re, `$1"${tableId}"`);
  fs.writeFileSync(CONFIG_PATH, raw, 'utf8');
  console.log(`[config] ${pathKey}.table_id 已回填：${tableId}`);
}

function resolveDate() {
  if (dateArg) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dateArg)) throw new Error(`--date 格式应为 YYYY-MM-DD，收到 ${dateArg}`);
    return dateArg;
  }
  const files = fs
    .readdirSync(SOURCE_DIR)
    .filter((f) => /^\d{4}-\d{2}-\d{2}\.md$/.test(f))
    .sort();
  if (!files.length) throw new Error(`当日进展目录没有 YYYY-MM-DD.md：${SOURCE_DIR}`);
  return files[files.length - 1].replace(/\.md$/, '');
}

function splitTableRow(line) {
  const cells = line.split('|').map((c) => c.trim());
  return cells.slice(1, cells.length - 1);
}

function stripMd(text) {
  return String(text || '')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .trim();
}

function dimensionFromTask(task) {
  const m = String(task).match(/WBS-(\d{2})/);
  if (!m) return '';
  return WBS_DIM[m[1]] || '';
}

function rowKey(date, task, owner) {
  const wbs = String(task).match(/WBS-[\w.-]+/);
  if (wbs) return `${date}|${wbs[0]}`;
  return `${date}|${owner}|${task}`.slice(0, 200);
}

function dateToMs(yyyyMmDd) {
  return Date.parse(`${yyyyMmDd}T00:00:00+08:00`);
}

/** 解析当日进展 md → { dailyRows, summaryRows } */
function parseSnapshotMd(date) {
  const file = path.join(SOURCE_DIR, `${date}.md`);
  if (!fs.existsSync(file)) throw new Error(`找不到快照文件：${file}`);
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  const dailyRows = [];
  const summaryRows = [];
  let mode = null; // daily | summary | null
  let header = null;

  for (const line of lines) {
    if (line.startsWith('## 设计、开发、整体、阻塞行数')) {
      mode = null;
      header = null;
      continue;
    }
    if (line.startsWith('## ')) {
      // 负责人分节；下一张八列表即 daily
      mode = 'daily_wait';
      header = null;
      continue;
    }
    if (!line.trim().startsWith('|')) {
      if (mode === 'summary_body') mode = null;
      continue;
    }
    const cells = splitTableRow(line);
    if (!cells.length) continue;
    if (/^:?-{3,}/.test(cells[0])) continue;

    if (cells[0] === '负责人' && cells.includes('任务内容')) {
      mode = 'daily';
      header = cells;
      continue;
    }
    if (cells[0] === '范围' && cells.includes('整体')) {
      mode = 'summary';
      header = cells;
      continue;
    }
    if (mode === 'daily' && header) {
      const owner = stripMd(cells[0]);
      const task = stripMd(cells[1]);
      if (!owner || !task) continue;
      dailyRows.push({
        row_key: rowKey(date, task, owner),
        snapshot_date: date,
        owner,
        task,
        due: stripMd(cells[2]),
        status: stripMd(cells[3]),
        today_task: stripMd(cells[4]),
        today_progress: stripMd(cells[5]),
        test: stripMd(cells[6]),
        note: stripMd(cells[7]),
        dimension: dimensionFromTask(task),
      });
      continue;
    }
    if (mode === 'summary' && header) {
      const scope = stripMd(cells[0]);
      if (!scope) continue;
      const num = (v) => {
        const t = stripMd(v);
        if (!t || t === '—' || t === '-') return null;
        const n = Number(t);
        return Number.isFinite(n) ? n : null;
      };
      summaryRows.push({
        row_key: `${date}|${scope}`,
        snapshot_date: date,
        scope,
        design: num(cells[1]),
        develop: num(cells[2]),
        overall: num(cells[3]),
        blocked: num(cells[4]) ?? 0,
      });
    }
  }
  return { dailyRows, summaryRows, file };
}

function textField(name) {
  return { field_name: name, type: 1 };
}
function numberField(name) {
  return { field_name: name, type: 2, property: { formatter: '0' } };
}
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function dateField(name) {
  return { field_name: name, type: 5, property: { date_formatter: 'yyyy/MM/dd', auto_fill: false } };
}

function dailyFieldDefs(fn, statusOptions) {
  return [
    textField(fn.row_key),
    dateField(fn.snapshot_date),
    textField(fn.owner),
    textField(fn.task),
    textField(fn.due),
    selectField(fn.status, statusOptions),
    textField(fn.today_task),
    textField(fn.today_progress),
    textField(fn.test),
    textField(fn.note),
    textField(fn.dimension),
  ];
}

function summaryFieldDefs(fn) {
  return [
    textField(fn.row_key),
    dateField(fn.snapshot_date),
    textField(fn.scope),
    numberField(fn.design),
    numberField(fn.develop),
    numberField(fn.overall),
    numberField(fn.blocked),
  ];
}

async function ensureTable(cfg, token, which, fieldDefs) {
  const slot = cfg[which];
  if (slot.tableId) return slot.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === slot.tableName);
  if (hit) {
    backfillYaml(which, hit.table_id);
    slot.tableId = hit.table_id;
    return hit.table_id;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] 将创建数据表「${slot.tableName}」（${fieldDefs.length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: slot.tableName, default_view_name: '全量总览', fields: fieldDefs },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error(`建表失败：${slot.tableName}`);
  console.log(`[table] 已创建「${slot.tableName}」table_id=${tableId}`);
  backfillYaml(which, tableId);
  slot.tableId = tableId;
  return tableId;
}

async function ensureFields(cfg, token, tableId, defs) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of defs) {
    if (existing.has(def.field_name)) continue;
    if (DRY_RUN) {
      console.log(`[dry-run] 将补建列「${def.field_name}」@ ${tableId}`);
      continue;
    }
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields`, token, def);
    console.log(`[field] 已补建列「${def.field_name}」`);
    await sleep(200);
  }
}

function dailyFieldsPayload(fn, row) {
  return {
    [fn.row_key]: row.row_key,
    [fn.snapshot_date]: dateToMs(row.snapshot_date),
    [fn.owner]: row.owner,
    [fn.task]: row.task,
    [fn.due]: row.due || '',
    [fn.status]: row.status || '',
    [fn.today_task]: row.today_task || '',
    [fn.today_progress]: row.today_progress || '',
    [fn.test]: row.test || '',
    [fn.note]: row.note || '',
    [fn.dimension]: row.dimension || '',
  };
}

function summaryFieldsPayload(fn, row) {
  const fields = {
    [fn.row_key]: row.row_key,
    [fn.snapshot_date]: dateToMs(row.snapshot_date),
    [fn.scope]: row.scope,
    [fn.blocked]: row.blocked ?? 0,
  };
  if (row.design !== null) fields[fn.design] = row.design;
  if (row.develop !== null) fields[fn.develop] = row.develop;
  if (row.overall !== null) fields[fn.overall] = row.overall;
  return fields;
}

async function upsertAndPrune(cfg, token, tableId, fn, rows, buildFields, date) {
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byKey = new Map();
  const sameDayExtras = [];
  for (const rec of existing) {
    const key = bitableFieldToString(rec.fields?.[fn.row_key]).trim();
    const dateCell = rec.fields?.[fn.snapshot_date];
    let recDate = '';
    if (typeof dateCell === 'number') {
      recDate = new Date(dateCell + 8 * 3600_000).toISOString().slice(0, 10);
    } else {
      recDate = bitableFieldToString(dateCell).slice(0, 10);
    }
    if (key) byKey.set(key, rec.record_id);
    // 无行键但日期匹配，或行键属于本日却不在本次集合：清理
    if (recDate === date || (key && key.startsWith(`${date}|`))) {
      sameDayExtras.push({ record_id: rec.record_id, key });
    }
  }

  const wanted = new Set(rows.map((r) => r.row_key));
  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = buildFields(fn, row);
    const rid = byKey.get(row.row_key);
    if (rid) toUpdate.push({ record_id: rid, fields });
    else toCreate.push({ fields });
  }
  const toDelete = sameDayExtras
    .filter((x) => !x.key || !wanted.has(x.key))
    .map((x) => x.record_id)
    .filter((id, i, arr) => arr.indexOf(id) === i);

  console.log(
    `[plan] ${tableId} 共 ${rows.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}，删除当日多余 ${toDelete.length}`,
  );
  if (DRY_RUN) return;

  for (let i = 0; i < toCreate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_create`, token, {
      records: toCreate.slice(i, i + 100),
    });
    await sleep(200);
  }
  for (let i = 0; i < toUpdate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_update`, token, {
      records: toUpdate.slice(i, i + 100),
    });
    await sleep(200);
  }
  for (let i = 0; i < toDelete.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_delete`, token, {
      records: toDelete.slice(i, i + 100),
    });
    await sleep(200);
  }
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = refineTableIds(loadBoardConfig());
  if (!cfg.appToken) throw new Error('feishu-daily-snapshot-board.yaml 缺少 app_token');

  const date = resolveDate();
  const { dailyRows, summaryRows, file } = parseSnapshotMd(date);
  console.log(`[source] ${file}`);
  console.log(`[source] ${date} 八列 ${dailyRows.length} 行，维度汇总 ${summaryRows.length} 行`);
  if (!dailyRows.length) throw new Error('未解析到八列行，请检查 md 表头是否为「负责人|任务内容|…」');
  if (DRY_RUN) {
    console.log(`[sample] ${JSON.stringify(dailyRows[0])}`);
    if (summaryRows[0]) console.log(`[sample] ${JSON.stringify(summaryRows[0])}`);
    console.log('[dry-run] 仅解析，不请求飞书。去掉 --dry-run 才会写入');
    return;
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：飞书未同步。请把新企业应用凭证写入 .env 后重跑');
    return;
  }

  const token = await feishuTenantToken(appId, appSecret);
  const dailyDefs = dailyFieldDefs(cfg.fieldNames.daily, cfg.statusOptions);
  const summaryDefs = summaryFieldDefs(cfg.fieldNames.summary);

  const dailyTableId = await ensureTable(cfg, token, 'daily', dailyDefs);
  if (dailyTableId) {
    await ensureFields(cfg, token, dailyTableId, dailyDefs);
    await upsertAndPrune(cfg, token, dailyTableId, cfg.fieldNames.daily, dailyRows, dailyFieldsPayload, date);
  }

  const summaryTableId = await ensureTable(cfg, token, 'summary', summaryDefs);
  if (summaryTableId) {
    await ensureFields(cfg, token, summaryTableId, summaryDefs);
    await upsertAndPrune(cfg, token, summaryTableId, cfg.fieldNames.summary, summaryRows, summaryFieldsPayload, date);
  }

  if (!DRY_RUN) console.log('[done] 当日进展已投影到飞书');
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
