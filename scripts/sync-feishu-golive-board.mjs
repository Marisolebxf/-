#!/usr/bin/env node
/**
 * sync-feishu-golive-board.mjs —— 飞书「上线前必办清单」看板出站同步
 * ---------------------------------------------------------------------------
 * 任务：ORCH-GOLIVE-BOARD-L01 · 配置：agent-delivery/feishu/feishu-golive-board.yaml
 * 真源：agent-delivery/golive-checklist.yaml（items 列表）
 * 行为：自动建表/建列 → 按「事项ID」upsert；飞书只读投影，不回写。
 * 用法：node scripts/sync-feishu-golive-board.mjs [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0）。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-golive-board.yaml');
const SOURCE_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'golive-checklist.yaml');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const STATUS_ZH = { open: '待办', in_progress: '进行中', done: '已完成', waived: '豁免' };
const CATEGORY_OPTIONS = ['签核', '口径闭合', '数据', '联调切换', '核验走查'];
const GATE_OPTIONS = ['上线前', 'Wave1 前', '联调前'];

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

/* ── 真源解析（items 列表，规整缩进 + 双引号值） ── */
function fieldOf(block, key) {
  const m = block.match(new RegExp(`^\\s+${key}:\\s*(.+)$`, 'm'));
  if (!m) return '';
  let v = m[1].trim();
  if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1).replace(/\\"/g, '"');
  const hash = v.indexOf(' #');
  if (hash >= 0) v = v.slice(0, hash).trim();
  return v;
}

function parseChecklistItems() {
  const raw = fs.readFileSync(SOURCE_PATH, 'utf8');
  const itemsSection = raw.split(/^items:\s*$/m)[1];
  if (!itemsSection) throw new Error('golive-checklist.yaml 缺少 items: 段');
  const blocks = itemsSection.split(/\r?\n(?=  - id: )/).filter((b) => /- id:\s*GL-/.test(b));
  return blocks.map((b) => ({
    id: fieldOf(b, '- id') || fieldOf(b, 'id'),
    title: fieldOf(b, 'title'),
    category: fieldOf(b, 'category'),
    gate: fieldOf(b, 'gate'),
    owner: fieldOf(b, 'owner'),
    depends: fieldOf(b, 'depends'),
    source: fieldOf(b, 'source'),
    status: STATUS_ZH[fieldOf(b, 'status')] || '待办',
    note: fieldOf(b, 'note'),
  }));
}

/* ── Bitable 建表/建列/upsert ── */
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn) {
  return [
    textField(fn.item_id),
    textField(fn.title),
    selectField(fn.category, CATEGORY_OPTIONS),
    selectField(fn.gate, GATE_OPTIONS),
    textField(fn.owner),
    textField(fn.depends),
    selectField(fn.status, Object.values(STATUS_ZH)),
    textField(fn.source),
    textField(fn.note),
    textField(fn.synced_at),
  ];
}

async function ensureTable(cfg, token) {
  if (cfg.tableId) return cfg.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === cfg.tableName);
  if (hit) {
    backfillTableId(hit.table_id);
    return hit.table_id;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] 将创建数据表「${cfg.tableName}」（${fieldDefs(cfg.fieldNames).length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: cfg.tableName, default_view_name: '全量总览', fields: fieldDefs(cfg.fieldNames) },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error('建表失败：无 table_id 返回');
  console.log(`[table] 已创建「${cfg.tableName}」table_id=${tableId}`);
  backfillTableId(tableId);
  return tableId;
}

async function ensureFields(cfg, token, tableId) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of fieldDefs(cfg.fieldNames)) {
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
    const id = bitableFieldToString(rec.fields?.[fn.item_id]).trim();
    if (id) byId.set(id, rec.record_id);
  }

  const toCreate = [];
  const toUpdate = [];
  for (const item of items) {
    const fields = {
      [fn.item_id]: item.id,
      [fn.title]: item.title,
      [fn.category]: item.category,
      [fn.gate]: item.gate,
      [fn.owner]: item.owner,
      [fn.depends]: item.depends,
      [fn.status]: item.status,
      [fn.source]: item.source,
      [fn.note]: item.note,
      [fn.synced_at]: today,
    };
    const recordId = byId.get(item.id);
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
  const items = parseChecklistItems();
  console.log(`[source] 上线前必办 ${items.length} 条（${items.filter((i) => i.status === '待办').length} 待办）`);
  if (!items.length) throw new Error('未解析到任何 GL 项，请检查 golive-checklist.yaml');
  if (DRY_RUN) {
    for (const id of ['GL-01', 'GL-07', 'GL-12']) {
      const it = items.find((i) => i.id === id);
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
  const tableId = await ensureTable(cfg, token);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId);
  await upsertRows(cfg, token, tableId, items);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
