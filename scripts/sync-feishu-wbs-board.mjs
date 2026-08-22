#!/usr/bin/env node
/**
 * sync-feishu-wbs-board.mjs —— 飞书「指标算法WBS」出站同步
 * ---------------------------------------------------------------------------
 * 配置：agent-delivery/feishu/feishu-wbs-board.yaml
 * 真源：给人说明 §5 WBS + §8.0 点名 ID；状态 join task-registry.yaml
 * 不 MCP 建单；不投影全文 / xlsx / 611 行任务看板。
 * 用法：node scripts/sync-feishu-wbs-board.mjs [--dry-run]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';
import { readRegistryText, findTaskBlocks, parseTaskBlock } from './lib/task-registry-lib.mjs';
import { loadWbsWorkpacks } from './lib/wbs-workpack-items.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-wbs-board.yaml');
const SOURCE_PATH = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'agent-handoffs',
  '算法库联调-ALGO-LIB',
  '给人说明-指标与算法工作类型与流程梳理.md',
);

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STATUS_ZH = {
  backlog: '待排期',
  ready: '待认领',
  claimed: '已认领',
  in_progress: '进行中',
  integration: '联调中',
  pending_test: '待测试',
  testing: '测试中',
  ready_to_sign: '待签收',
  done: '已完成',
  blocked: '阻塞',
  'needs-revision': '需返工',
  review: '评审中',
};

const KIND = ['工作包', '维内步骤', '任务叶', '未建单', '废作'];
const TRACK = ['8/25硬路径', '不挡8/25', '勿再派'];
const PHASES = [
  'WBS-0 治理与会合',
  'WBS-1 合同盘点',
  'WBS-2 产品定义',
  'WBS-3 语义与血缘',
  'WBS-4 实现分流',
  'WBS-5 算法库合规',
  'WBS-6 联调硬化',
  '勿再派',
];

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

function loadRegistryIndex() {
  const text = readRegistryText();
  const lines = text.split(/\r?\n/);
  const byId = new Map();
  for (const { start, end } of findTaskBlocks(lines)) {
    const t = parseTaskBlock(lines.slice(start, end));
    if (t.id) byId.set(t.id, t);
  }
  return byId;
}

function statusOf(item, task) {
  if (item.kind === '未建单' && !item.taskId) return '未建单';
  if (!item.taskId) return '—';
  if (!task) return 'registry无此ID';
  return STATUS_ZH[task.status] || task.status || '—';
}

function noteDeadline(note) {
  const m = String(note || '').match(/截止\s*(\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : '';
}

function deadlineYmd(item, task) {
  return item.deadline || task?.deadline || noteDeadline(task?.note) || '';
}

/** 飞书日期列：当天 23:59:59 +08，表示「这一天结束前必须完成」。 */
function deadlineMs(ymd) {
  if (!ymd) return null;
  const ms = Date.parse(`${ymd}T23:59:59+08:00`);
  return Number.isFinite(ms) ? ms : null;
}

function buildRows() {
  const today = new Date().toISOString().slice(0, 10);
  const registry = loadRegistryIndex();
  const items = loadWbsWorkpacks(SOURCE_PATH, [...registry.keys()]);
  return items.map((it) => {
    const task = it.taskId ? registry.get(it.taskId) : null;
    const ymd = deadlineYmd(it, task);
    return {
      rowId: it.rowId,
      fieldsZh: {
        wbs: it.wbs,
        phase: it.phase,
        title: it.title,
        kind: KIND.includes(it.kind) ? it.kind : '工作包',
        track: TRACK.includes(it.track) ? it.track : '不挡8/25',
        owner: it.owner,
        task_id: it.taskId || '',
        deadline: deadlineMs(ymd),
        status: statusOf(it, task),
        epic: task?.epic || '',
        supervised_by: task?.supervised_by || '',
        claimed_by: task?.claimed_by || '',
        task_type: task?.task_type || '',
        note: it.note || '',
        synced_at: today,
      },
    };
  });
}

function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}
function dateField(name) {
  return { field_name: name, type: 5, property: { date_formatter: 'yyyy/MM/dd' } };
}

function fieldDefs(fn, rows) {
  const statuses = [...new Set(['未建单', '—', 'registry无此ID', ...Object.values(STATUS_ZH), ...rows.map((r) => r.fieldsZh.status)])];
  const epics = [...new Set(rows.map((r) => r.fieldsZh.epic).filter(Boolean))].sort();
  return [
    textField(fn.row_id),
    textField(fn.wbs),
    selectField(fn.phase, PHASES),
    textField(fn.title),
    selectField(fn.kind, KIND),
    selectField(fn.track, TRACK),
    textField(fn.owner),
    textField(fn.task_id),
    dateField(fn.deadline),
    selectField(fn.status, statuses.length ? statuses : ['—']),
    selectField(fn.epic, epics.length ? epics : ['（空）']),
    textField(fn.supervised_by),
    textField(fn.claimed_by),
    textField(fn.task_type),
    textField(fn.note),
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
      if (!fn[key]) continue;
      if (key === 'deadline') {
        if (value == null) continue;
        fields[fn[key]] = value;
        continue;
      }
      fields[fn[key]] = value ?? '';
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

function assertCore(rows) {
  const byId = new Map(rows.map((r) => [r.rowId, r]));
  const a1 = byId.get('WBS-1.1');
  if (!a1) throw new Error('WBS 解析失败：缺少 WBS-1.1');
  if (a1.fieldsZh.task_id !== 'ALGO-LIB-METRIC-DEPS-L01') {
    throw new Error(`WBS-1.1 应对 ALGO-LIB-METRIC-DEPS-L01，实际 ${a1.fieldsZh.task_id}`);
  }
  if (a1.fieldsZh.track !== '8/25硬路径') throw new Error('WBS-1.1 路径应为 8/25硬路径');
  const a1Day = new Date(a1.fieldsZh.deadline).toLocaleDateString('en-CA', { timeZone: 'Asia/Shanghai' });
  if (a1Day !== '2026-08-25') throw new Error(`WBS-1.1 截止日期应为 2026-08-25，实际 ${a1Day}`);
  const step = byId.get('WBS-1.1.1');
  const stepDay = step ? new Date(step.fieldsZh.deadline).toLocaleDateString('en-CA', { timeZone: 'Asia/Shanghai' }) : '';
  if (stepDay !== '2026-08-23') throw new Error(`WBS-1.1.1 截止日期应为 2026-08-23，实际 ${stepDay}`);
  const scrap = rows.filter((r) => r.fieldsZh.kind === '废作');
  if (scrap.length < 4) throw new Error(`废作行不足 4，实际 ${scrap.length}`);
  const opens = rows.filter((r) => r.rowId.startsWith('WBS-2.2/') && r.fieldsZh.kind === '任务叶');
  if (opens.some((r) => r.fieldsZh.task_id.includes('READINESS'))) {
    throw new Error('OPEN 叶误含 READINESS');
  }
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  const rows = buildRows();
  assertCore(rows);
  const byKind = {};
  const byTrack = {};
  for (const r of rows) {
    byKind[r.fieldsZh.kind] = (byKind[r.fieldsZh.kind] || 0) + 1;
    byTrack[r.fieldsZh.track] = (byTrack[r.fieldsZh.track] || 0) + 1;
  }
  console.log(`[source] WBS 行 ${rows.length} 条 kind=${JSON.stringify(byKind)} track=${JSON.stringify(byTrack)}`);
  if (DRY_RUN) {
    const hard = rows.find((r) => r.rowId === 'WBS-1.1');
    const open = rows.find((r) => r.fieldsZh.task_id.endsWith('-METRIC-OPEN-L01'));
    const pending = rows.find((r) => r.fieldsZh.kind === '未建单' && r.rowId.includes('pending'));
    if (hard) console.log(`[sample] ${hard.rowId} deadline=${hard.fieldsZh.deadline} → ${JSON.stringify(hard.fieldsZh)}`);
    if (open) console.log(`[sample-open] ${open.rowId} → ${JSON.stringify(open.fieldsZh)}`);
    if (pending) console.log(`[sample-pending] ${pending.rowId} → ${JSON.stringify(pending.fieldsZh)}`);
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
