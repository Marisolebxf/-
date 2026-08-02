#!/usr/bin/env node
/**
 * sync-feishu-user-story-board.mjs —— 飞书「用户故事库」看板出站同步
 * ---------------------------------------------------------------------------
 * 真源：agent-delivery/user-story-library.yaml（extract-user-stories 生成 + check-story-coverage 回填）
 * 行为：自动建表/建列 → 按「故事ID」upsert；飞书只读投影，不回写。
 * 用法：node scripts/sync-feishu-user-story-board.mjs [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0，提示待手跑/投影机）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-user-story-board.yaml');
const LIBRARY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'user-story-library.yaml');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ── 状态显示映射（与 feishu-user-story-board.yaml#display_maps 保持一致） ── */
const STATUS_ZH = { defined: '已定义', implemented: '已实现' };

/* ── 配置读取（app_token / table_name / table_id / 列名 / handoff_link） ── */
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
  const hlBlock = raw.match(/^handoff_link:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  const handoffLink = { enabled: true, writeMode: 'plain', gitlabBase: '', gitlabGroup: '', repo: '', branch: '', pathPrefix: '' };
  const HL_KEYS = { gitlab_base: 'gitlabBase', gitlab_group: 'gitlabGroup', repo: 'repo', branch: 'branch', path_prefix: 'pathPrefix' };
  if (hlBlock) {
    for (const line of hlBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"?([^"\r\n#]+)"?\s*(?:#.*)?$/);
      if (!m) continue;
      if (m[1] === 'enabled') handoffLink.enabled = m[2].trim() === 'true';
      else if (m[1] === 'write_mode') handoffLink.writeMode = m[2].trim();
      else if (HL_KEYS[m[1]]) handoffLink[HL_KEYS[m[1]]] = m[2].trim();
    }
  }
  return { raw, appToken: get('app_token'), tableName: get('table_name'), tableId: get('table_id'), fieldNames, handoffLink };
}

function backfillTableId(tableId) {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  if (!/^\s+table_id:\s*""/m.test(raw)) return;
  fs.writeFileSync(CONFIG_PATH, raw.replace(/^(\s+table_id:\s*)""/m, `$1"${tableId}"`), 'utf8');
  console.log(`[config] table_id 已回填：${tableId}`);
}

/* ── 真源解析（user-story-library.yaml 为脚本生成的规整格式） ── */
function parseStories(text) {
  const stories = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"([^"]+)"/);
    if (idm) {
      current = { id: idm[1], title: '', text: '', module: '', source: '', roles: [], status: 'defined', implementation_tasks: [] };
      stories.push(current);
      continue;
    }
    if (!current) continue;
    const km = line.match(/^\s{4}([a-z_]+):\s*"((?:[^"\\]|\\.)*)"/);
    if (km) {
      current[km[1]] = km[2];
      continue;
    }
    const rm = line.match(/^\s{4}roles:\s*\[(.*)\]\s*$/);
    if (rm) {
      const inner = rm[1].trim();
      current.roles = inner
        ? inner.split(/,\s*/).map((s) => s.replace(/^"|"$/g, '')).filter(Boolean)
        : [];
      continue;
    }
    const lm = line.match(/^\s{4}implementation_tasks:\s*\[(.*)\]\s*$/);
    if (lm) {
      const inner = lm[1].trim();
      current.implementation_tasks = inner
        ? inner.split(/,\s*/).map((s) => s.replace(/^"|"$/g, '')).filter(Boolean)
        : [];
    }
  }
  return stories;
}

/* ── 行构建 ── */
// 库 source 相对路径 → GitLab blob 直链（约定同 feishu-bitable.yaml#handoff_link）
function sourceUrl(src, cfg) {
  if (!src) return '';
  if (/^https?:\/\//i.test(src)) return src;
  if (!cfg.handoffLink.enabled) return src;
  let p = src.replace(/\\/g, '/').trim();
  if (cfg.handoffLink.pathPrefix && !p.startsWith(cfg.handoffLink.pathPrefix)) {
    p = `${cfg.handoffLink.pathPrefix}/${p}`;
  }
  const encoded = p
    .split('/')
    .map((s) => encodeURIComponent(s))
    .join('/');
  return `${cfg.handoffLink.gitlabBase}/${cfg.handoffLink.gitlabGroup}/${cfg.handoffLink.repo}/-/blob/${cfg.handoffLink.branch}/${encoded}?ref_type=heads`;
}

function buildRows(cfg) {
  const text = fs.readFileSync(LIBRARY_PATH, 'utf8');
  const stories = parseStories(text);
  const today = new Date().toISOString().slice(0, 10);
  return stories.map((s) => ({
    storyId: s.id,
    fieldsZh: {
      title: s.title || s.id,
      text: s.text || '',
      module: s.module || '—',
      roles: s.roles.length ? s.roles.join('、') : '',
      source: sourceUrl(s.source, cfg),
      status: STATUS_ZH[s.status] ?? s.status,
      implementation_tasks: s.implementation_tasks.length ? s.implementation_tasks.join(', ') : '',
      synced_at: today,
    },
  }));
}

/* ── Bitable 建表/建列/upsert ── */
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn, rows) {
  const moduleOptions = [...new Set(rows.map((r) => r.fieldsZh.module))].sort();
  return [
    textField(fn.story_id),
    textField(fn.title),
    textField(fn.text),
    selectField(fn.module, moduleOptions),
    textField(fn.roles),
    textField(fn.source),
    selectField(fn.status, Object.values(STATUS_ZH)),
    textField(fn.implementation_tasks),
    textField(fn.synced_at),
  ];
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
  const byStoryId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.story_id]).trim();
    if (id) byStoryId.set(id, rec.record_id);
  }

  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = { [fn.story_id]: row.storyId };
    for (const [key, value] of Object.entries(row.fieldsZh)) {
      if (fn[key]) fields[fn[key]] = value ?? '';
    }
    const recordId = byStoryId.get(row.storyId);
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

/* ── main ── */
async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  const rows = buildRows(cfg);
  console.log(`[source] 用户故事 ${rows.length} 条（已实现 ${rows.filter((r) => r.fieldsZh.status === '已实现').length} 条）`);
  if (!rows.length) throw new Error(`未解析到任何故事，请检查 ${LIBRARY_PATH}`);
  if (DRY_RUN) {
    for (const id of ['US-E1-SCH-01', 'US-ENT-EVAL-OBJ']) {
      const row = rows.find((r) => r.storyId === id);
      if (row) console.log(`[sample] ${id} → ${JSON.stringify(row.fieldsZh, null, 0)}`);
    }
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步，请在配好 .env 的机器（如投影机）重跑本脚本');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token, rows);
  if (!tableId) return; // dry-run 且表未建
  await ensureFields(cfg, token, tableId, rows);
  await upsertRows(cfg, token, tableId, rows);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
