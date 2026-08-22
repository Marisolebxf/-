#!/usr/bin/env node
/**
 * sync-feishu-algo-leaf-board.mjs —— 飞书「算法库叶子」看板出站同步（A1）
 * ---------------------------------------------------------------------------
 * 配置：agent-delivery/feishu/feishu-algo-leaf-board.yaml
 * 真源：metrics/algo-results/*-requirements.yaml + *-metrics.yaml
 * 用法：node scripts/sync-feishu-algo-leaf-board.mjs [--dry-run]
 * yaml 未交：建表/补列 + 0 行（不清已有行）。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-algo-leaf-board.yaml');
const ALGO_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'algo-results');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const COVERAGE_ZH = { full: '完整', partial: '部分', missing: '缺失', third_party: '第三方', unassessed: '未评估' };
const ODS_ZH = { full: '齐备', partial: '部分', none: '无源', pending_ods: '待ODS', 'n/a': '不适用', unassessed: '未评估' };
const ODS_RANK = { none: 5, pending_ods: 4, partial: 3, full: 2, 'n/a': 1, unassessed: 0 };
const DIM_OWNER = {
  企业: '徐滕强',
  综合: '徐滕强',
  产业链: '李伟',
  产业服务: '侯佳伟',
  政策: '淮政玮',
  技术链: '未点名',
  科研机构: '未点名',
  人才: '未点名',
};
const DIM_OPTIONS = ['产业链', '技术链', '企业', '科研机构', '人才', '政策', '产业服务', '综合'];
const LAYER_OPTIONS = ['基础指标', '图谱', '深度分析', '综合分析', '图谱API'];

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

function fieldOf(block, key) {
  const m = block.match(new RegExp(`^\\s+${key}:\\s*(.+)$`, 'm'));
  if (!m) return '';
  let v = m[1].trim();
  if (!v || v === 'null' || v === '~') return '';
  if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1).replace(/\\"/g, '"');
  if (v.length > 1 && v.startsWith("'") && v.endsWith("'")) return v.slice(1, -1);
  const hash = v.indexOf(' #');
  if (hash >= 0) v = v.slice(0, hash).trim();
  return v;
}

function splitBlocks(raw, idKey) {
  const re = new RegExp(`^ {2}- ${idKey}:`);
  const blocks = [];
  let current = null;
  for (const line of raw.split(/\r?\n/)) {
    if (re.test(line)) {
      if (current) blocks.push(current);
      current = [line];
    } else if (current) {
      if (/^ {2}- /.test(line) || (/^\S/.test(line) && line.trim() !== '')) {
        blocks.push(current);
        current = null;
        if (re.test(line)) current = [line];
      } else {
        current.push(line);
      }
    }
  }
  if (current) blocks.push(current);
  return blocks.map((lines) => lines.join('\n'));
}

function worstOds(statuses) {
  let best = 'unassessed';
  let rank = -1;
  for (const s of statuses) {
    const k = ODS_RANK[s] >= 0 ? s : 'unassessed';
    if ((ODS_RANK[k] || 0) > rank) {
      rank = ODS_RANK[k] || 0;
      best = k;
    }
  }
  return best;
}

function parseMetricsTable() {
  const byId = new Map();
  if (!fs.existsSync(ALGO_DIR)) return byId;
  for (const name of fs.readdirSync(ALGO_DIR).filter((f) => /-metrics\.yaml$/.test(f))) {
    const raw = fs.readFileSync(path.join(ALGO_DIR, name), 'utf8');
    for (const block of splitBlocks(raw, 'metric_id')) {
      const id = fieldOf(block, '- metric_id') || fieldOf(block, 'metric_id');
      if (!id) continue;
      const type = (block.match(/^\s+type:\s*(\w+)/m) || [])[1] || '';
      const rollup = (block.match(/dependency_rollup:[\s\S]*?ods_mapping_status:\s*(\w+)/) || [])[1] || '';
      const inputStatuses = [...block.matchAll(/^\s+ods_mapping_status:\s*(\w+)/gm)].map((m) => m[1]);
      const ods = rollup || worstOds(inputStatuses);
      byId.set(id, { type, ods: ods || 'unassessed' });
    }
  }
  return byId;
}

function parseRequirements() {
  const rows = [];
  if (!fs.existsSync(ALGO_DIR)) return rows;
  const files = fs.readdirSync(ALGO_DIR).filter((f) => /-requirements\.yaml$/.test(f));
  const metrics = parseMetricsTable();
  for (const name of files) {
    const raw = fs.readFileSync(path.join(ALGO_DIR, name), 'utf8');
    for (const block of splitBlocks(raw, 'requirement_id')) {
      const id = fieldOf(block, '- requirement_id') || fieldOf(block, 'requirement_id');
      if (!id) continue;
      const metricIds = [...block.matchAll(/^\s+- metric_id:\s*(\S+)/gm)].map((m) => m[1].replace(/["']/g, ''));
      const types = [...new Set(metricIds.map((mid) => metrics.get(mid)?.type).filter(Boolean))];
      const ods = worstOds(metricIds.map((mid) => metrics.get(mid)?.ods).filter(Boolean));
      const cov = fieldOf(block, 'coverage_status') || 'unassessed';
      const dim = fieldOf(block, 'dimension');
      rows.push({
        requirementId: id,
        fieldsZh: {
          dimension: dim,
          layer: fieldOf(block, 'layer'),
          title: fieldOf(block, 'requirement_title'),
          coverage: COVERAGE_ZH[cov] || COVERAGE_ZH.unassessed,
          ods_worst: ODS_ZH[ods] || ODS_ZH.unassessed,
          metric_ids: metricIds.join(', '),
          algo_types: types.join(', '),
          topic_owner: DIM_OWNER[dim] || '未点名',
          coverage_note: fieldOf(block, 'coverage_note'),
          srs_path: fieldOf(block, 'srs_path'),
          synced_at: new Date().toISOString().slice(0, 10),
        },
      });
    }
  }
  rows.sort((a, b) => (a.fieldsZh.dimension + a.requirementId).localeCompare(b.fieldsZh.dimension + b.requirementId, 'zh-Hans-CN'));
  return rows;
}

function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn) {
  return [
    textField(fn.requirement_id),
    selectField(fn.dimension, DIM_OPTIONS),
    selectField(fn.layer, LAYER_OPTIONS),
    textField(fn.title),
    selectField(fn.coverage, Object.values(COVERAGE_ZH)),
    selectField(fn.ods_worst, Object.values(ODS_ZH)),
    textField(fn.metric_ids),
    textField(fn.algo_types),
    selectField(fn.topic_owner, ['徐滕强', '李伟', '侯佳伟', '淮政玮', '未点名', '—']),
    textField(fn.coverage_note),
    textField(fn.srs_path),
    textField(fn.synced_at),
  ].filter((d) => d.field_name);
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

async function upsertRows(cfg, token, tableId, rows) {
  const fn = cfg.fieldNames;
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.requirement_id]).trim();
    if (id) byId.set(id, rec.record_id);
  }
  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = { [fn.requirement_id]: row.requirementId };
    for (const [key, value] of Object.entries(row.fieldsZh)) {
      if (fn[key]) fields[fn[key]] = value ?? '';
    }
    const recordId = byId.get(row.requirementId);
    if (recordId) toUpdate.push({ record_id: recordId, fields });
    else toCreate.push({ fields });
  }
  console.log(`[plan] 共 ${rows.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}`);
  if (DRY_RUN || !rows.length) return;
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
  const rows = parseRequirements();
  console.log(`[source] A1 叶子 ${rows.length} 条（期望 97；未交 yaml 则为 0）`);
  if (DRY_RUN && rows[0]) console.log(`[sample] ${rows[0].requirementId} → ${JSON.stringify(rows[0].fieldsZh)}`);

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId);
  await upsertRows(cfg, token, tableId, rows);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
