#!/usr/bin/env node
/**
 * sync-feishu-decision-board.mjs —— 飞书「甲方决策清单」看板出站同步
 * ---------------------------------------------------------------------------
 * 任务：ORCH-DECISION-BOARD-L01 · 配置：agent-delivery/feishu-decision-board.yaml
 * 真源：agent-delivery/客户决策清单跟踪表.md（§2 决策项注册表，markdown 表格）
 * 行为：解析各 §2.x 小节表格的 Q 项 → 自动建表/建列 → 按「决策ID」upsert；
 *       飞书只读投影，不回写。列名以表格 header 行为准（兼容「甲方决策」vs「PDR Δ」等差异）。
 * 用法：node scripts/sync-feishu-decision-board.mjs [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0）。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-decision-board.yaml');
const SOURCE_PATH = path.join(ORCH_ROOT, 'agent-delivery', '客户决策清单跟踪表.md');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STATUS_MAP = { '🔴': '阻塞', '🟡': '临时默认', '🟢': '已确认', '⚪': '已撤销' };
const STATUS_DEFAULT = '未标注';

/* ── 配置读取 ── */
function loadBoardConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const get = (key) => (raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  const fieldNames = {};
  const fnBlock = raw.match(/^field_names:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  if (fnBlock) {
    for (const line of fnBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"([^"]+)"/);
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

/* ── markdown 真源解析 ── */
/** 表头列名 → 内部字段 key（按包含关系归一化；兼容各小节列名差异） */
function classifyHeader(name) {
  const n = name.trim();
  if (n === 'ID') return 'decision_id';
  if (n.includes('标题')) return 'title';
  if (n.includes('来源')) return 'source';
  if (n.includes('影响')) return 'impact';
  if (n.includes('临时默认')) return 'team_default';
  if (n.includes('状态')) return 'status';
  if (n.toLowerCase().includes('deadline')) return 'deadline';
  if (n.includes('甲方决策')) return 'decision';
  if (n.includes('PDR')) return 'pdr_delta';
  if (n.includes('落地')) return 'landing';
  return null;
}

function splitTableRow(line) {
  // | a | b | c | → ['a','b','c']（首尾空段丢弃）
  const cells = line.split('|').map((c) => c.trim());
  return cells.slice(1, cells.length - 1);
}

function stripMd(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    // 只剥独立的 _占位斜体_（如 _PM 待填_），不动 dwd_zh_project 这类标识符内下划线
    .replace(/(^|\s)_([^_]+)_(?=\s|$)/g, '$1$2')
    .trim();
}

function parseDecisionItems() {
  const raw = fs.readFileSync(SOURCE_PATH, 'utf8');
  const lines = raw.split(/\r?\n/);
  const items = [];
  let batch = '';           // 当前 §2.x 小节标题
  let headerKeys = null;    // 当前表格的列 key 序列（null = 不在目标表格中）

  for (const line of lines) {
    const h = line.match(/^###\s+(2\.\w+)\s+(.+)$/);
    if (h) {
      batch = `${h[1]} ${stripMd(h[2])}`;
      headerKeys = null;
      continue;
    }
    if (!line.trim().startsWith('|')) {
      headerKeys = null;
      continue;
    }
    const cells = splitTableRow(line);
    if (!cells.length) continue;
    if (/^:?-{3,}/.test(cells[0])) continue; // 分隔行
    if (cells[0] === 'ID') {
      // 只吸收「首列 = ID」的注册表（跳过速查表/待办表等）
      headerKeys = cells.map(classifyHeader);
      continue;
    }
    if (!headerKeys) continue;
    if (!/^Q[\w-]*\d/.test(cells[0])) continue; // 只收 Q 项行

    const item = { batch };
    headerKeys.forEach((key, i) => {
      if (key && cells[i] !== undefined) item[key] = stripMd(cells[i]);
    });
    if (!item.decision_id || item.title === '—' || !item.title) continue; // 跳过占位行
    // 状态符号 → 选项文字
    const sym = Object.keys(STATUS_MAP).find((s) => (item.status || '').includes(s));
    item.status = sym ? STATUS_MAP[sym] : STATUS_DEFAULT;
    items.push(item);
  }
  return items;
}

/* ── Bitable 建表/建列/upsert ── */
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn, items) {
  const batchOptions = [...new Set(items.map((i) => i.batch))];
  return [
    textField(fn.decision_id),
    textField(fn.title),
    selectField(fn.status, [...Object.values(STATUS_MAP), STATUS_DEFAULT]),
    selectField(fn.batch, batchOptions),
    textField(fn.deadline),
    textField(fn.impact),
    textField(fn.team_default),
    textField(fn.decision),
    textField(fn.pdr_delta),
    textField(fn.landing),
    textField(fn.source),
    textField(fn.synced_at),
  ];
}

async function ensureTable(cfg, token, items) {
  if (cfg.tableId) return cfg.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === cfg.tableName);
  if (hit) {
    backfillTableId(hit.table_id);
    return hit.table_id;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] 将创建数据表「${cfg.tableName}」（${fieldDefs(cfg.fieldNames, items).length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: cfg.tableName, default_view_name: '全量总览', fields: fieldDefs(cfg.fieldNames, items) },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error('建表失败：无 table_id 返回');
  console.log(`[table] 已创建「${cfg.tableName}」table_id=${tableId}`);
  backfillTableId(tableId);
  return tableId;
}

async function ensureFields(cfg, token, tableId, items) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of fieldDefs(cfg.fieldNames, items)) {
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

async function upsertRows(cfg, token, tableId, items) {
  const fn = cfg.fieldNames;
  const today = new Date().toISOString().slice(0, 10);
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.decision_id]).trim();
    if (id) byId.set(id, rec.record_id);
  }

  const toCreate = [];
  const toUpdate = [];
  for (const item of items) {
    const fields = {
      [fn.decision_id]: item.decision_id,
      [fn.title]: item.title || '',
      [fn.batch]: item.batch,
      [fn.source]: item.source || '',
      [fn.impact]: item.impact || '',
      [fn.team_default]: item.team_default || '',
      [fn.status]: item.status,
      [fn.deadline]: item.deadline || '',
      [fn.decision]: item.decision || '',
      [fn.pdr_delta]: item.pdr_delta || '',
      [fn.landing]: item.landing || '',
      [fn.synced_at]: today,
    };
    const recordId = byId.get(item.decision_id);
    if (recordId) toUpdate.push({ record_id: recordId, fields });
    else toCreate.push({ fields });
  }

  console.log(`[plan] 共 ${items.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}`);
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

/* ── main ── */
async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  const items = parseDecisionItems();
  const byStatus = {};
  for (const i of items) byStatus[i.status] = (byStatus[i.status] || 0) + 1;
  console.log(`[source] 决策项 ${items.length} 条（${Object.entries(byStatus).map(([k, v]) => `${k} ${v}`).join(' / ')}）`);
  if (!items.length) throw new Error('未解析到任何决策项，请检查 客户决策清单跟踪表.md §2 表格格式');
  if (DRY_RUN) {
    for (const id of ['Q001', 'Q041', 'Q053', 'Q-OPS-02']) {
      const it = items.find((i) => i.decision_id === id);
      if (it) console.log(`[sample] ${id} → ${JSON.stringify(it)}`);
    }
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步，请在配好 .env 的机器重跑本脚本');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token, items);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId, items);
  await upsertRows(cfg, token, tableId, items);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
