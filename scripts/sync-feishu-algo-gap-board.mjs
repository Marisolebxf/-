#!/usr/bin/env node
/**
 * sync-feishu-algo-gap-board.mjs —— 飞书「页面指标差集」看板出站同步（A2）
 * ---------------------------------------------------------------------------
 * 配置：agent-delivery/feishu/feishu-algo-gap-board.yaml
 * 真源：metrics/request/{专题系统,展示系统}/pages/*.yaml items[]
 * 不读 _work / 索引 yaml / semantic_debt。
 * 用法：node scripts/sync-feishu-algo-gap-board.mjs [--dry-run]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';
import { loadA2GapItems } from './lib/a2-gap-items.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-algo-gap-board.yaml');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const VERDICT = ['missing', 'mapped', 'third_party', 'other_system', 'n/a_ops'];
const DISPOSE = ['①STAT', '②已有模型', '③新MODEL', '④DEMO', '未分拣'];
const DISPOSE_MAP = {
  stat: '①STAT',
  '①STAT': '①STAT',
  mapped_model: '②已有模型',
  '②已有模型': '②已有模型',
  new_model: '③新MODEL',
  '③新MODEL': '③新MODEL',
  demo: '④DEMO',
  '④DEMO': '④DEMO',
};

function loadBoardConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const get = (key) => (raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  const fieldNames = {};
  const fnBlock = raw.match(/^field_names:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  if (fnBlock) {
    for (const line of fnBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z0-9_]+):\s*"([^"]+)"/);
      if (m) fieldNames[m[1]] = m[2];
    }
  }
  return { appToken: get('app_token'), tableName: get('table_name'), tableId: get('table_id'), fieldNames };
}

function backfillTableId(tableId) {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  if (!/^\s+table_id:\s*""/m.test(raw)) return;
  fs.writeFileSync(CONFIG_PATH, raw.replace(/^(\s+table_id:\s*)""/m, `$1"${tableId}"`), 'utf8');
  console.log(`[config] table_id 已回填：${tableId}`);
}

function disposeOf(raw) {
  if (!raw) return '未分拣';
  return DISPOSE_MAP[raw] || (DISPOSE.includes(raw) ? raw : '未分拣');
}

function buildRows() {
  const today = new Date().toISOString().slice(0, 10);
  return loadA2GapItems(ORCH_ROOT).map((it) => ({
    rowId: it.rowId,
    fieldsZh: {
      system: it.system,
      module: it.module,
      page: it.page,
      main: it.main,
      sub: it.sub,
      meaning: it.meaning,
      basis_type: it.basisType,
      call_system: it.callSystem,
      call_module: it.callModule,
      verdict: VERDICT.includes(it.verdict) ? it.verdict : it.verdict,
      a1_req: it.a1Req,
      a1_leaf: it.a1Leaf,
      metric_id: it.metricId,
      gap_note: it.gapNote,
      dispose: disposeOf(it.dispose),
      synced_at: today,
    },
  }));
}

function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn, rows) {
  const modules = [...new Set(rows.map((r) => r.fieldsZh.module).filter(Boolean))].sort();
  const basis = [...new Set(rows.map((r) => r.fieldsZh.basis_type).filter(Boolean))].sort();
  const callSys = [...new Set(rows.map((r) => r.fieldsZh.call_system).filter(Boolean))].sort();
  const verdicts = [...new Set([...VERDICT, ...rows.map((r) => r.fieldsZh.verdict).filter(Boolean)])];
  return [
    textField(fn.row_id),
    selectField(fn.system, ['专题', '展示']),
    selectField(fn.module, modules.length ? modules : ['（空）']),
    textField(fn.page),
    textField(fn.main),
    textField(fn.sub),
    textField(fn.meaning),
    selectField(fn.basis_type, basis.length ? basis : ['需确认']),
    selectField(fn.call_system, callSys.length ? callSys : ['（空）']),
    textField(fn.call_module),
    selectField(fn.verdict, verdicts),
    textField(fn.a1_req),
    textField(fn.a1_leaf),
    textField(fn.metric_id),
    textField(fn.gap_note),
    selectField(fn.dispose, DISPOSE),
    textField(fn.synced_at),
  ].filter((d) => d.field_name);
}

async function ensureTable(cfg, token, rows) {
  if (cfg.tableId) return cfg.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === cfg.tableName);
  if (hit) {
    backfillTableId(hit.table_id);
    return hit.table_id;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] 将创建数据表「${cfg.tableName}」（${fieldDefs(cfg.fieldNames, rows).length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: cfg.tableName, default_view_name: '全量总览', fields: fieldDefs(cfg.fieldNames, rows) },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error('建表失败：无 table_id 返回');
  console.log(`[table] 已创建「${cfg.tableName}」table_id=${tableId}`);
  backfillTableId(tableId);
  return tableId;
}

async function ensureFields(cfg, token, tableId, rows) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of fieldDefs(cfg.fieldNames, rows)) {
    if (existing.has(def.field_name)) continue;
    if (DRY_RUN) {
      console.log(`[dry-run] 将补建列「${def.field_name}」`);
      continue;
    }
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields`, token, def);
    console.log(`[field] 已补建列「${def.field_name}」`);
    await sleep(200);
  }
}

async function upsertRows(cfg, token, tableId, rows) {
  const fn = cfg.fieldNames;
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.row_id]).trim();
    if (id) byId.set(id, rec.record_id);
  }
  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = { [fn.row_id]: row.rowId };
    for (const [key, value] of Object.entries(row.fieldsZh)) {
      if (fn[key]) fields[fn[key]] = value ?? '';
    }
    const recordId = byId.get(row.rowId);
    if (recordId) toUpdate.push({ record_id: recordId, fields });
    else toCreate.push({ fields });
  }
  console.log(`[plan] 共 ${rows.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}`);
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
  console.log('[done] 看板已同步');
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  const rows = buildRows();
  const byV = {};
  const bySys = {};
  for (const r of rows) {
    byV[r.fieldsZh.verdict] = (byV[r.fieldsZh.verdict] || 0) + 1;
    bySys[r.fieldsZh.system] = (bySys[r.fieldsZh.system] || 0) + 1;
  }
  console.log(`[source] A2 行 ${rows.length} 条 system=${JSON.stringify(bySys)} verdict=${JSON.stringify(byV)}`);
  if (!rows.length) throw new Error('未解析到 A2 items[]，请检查 metrics/request/{专题系统,展示系统}/pages/*.yaml');
  if (DRY_RUN) {
    const miss = rows.find((r) => r.fieldsZh.verdict === 'missing');
    const mapped = rows.find((r) => r.fieldsZh.verdict === 'mapped');
    if (mapped) console.log(`[sample] ${mapped.rowId} → ${JSON.stringify(mapped.fieldsZh)}`);
    if (miss) console.log(`[sample-missing] ${miss.rowId} → ${JSON.stringify(miss.fieldsZh)}`);
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token, rows);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId, rows);
  await upsertRows(cfg, token, tableId, rows);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
