#!/usr/bin/env node
/**
 * sync-feishu-bug.mjs —— 缺陷台账 → 飞书「GKX 当日进展 / 缺陷」出站
 * ---------------------------------------------------------------------------
 * 真源：qa/bug-registry.yaml + qa/bugs 正文。截图不进 git，只在本次用 --image 上传。
 * 配置：agent-delivery/feishu/feishu-daily-snapshot-board.yaml#bitable.bugs
 * 用法：node scripts/sync-feishu-bug.mjs [--id BUG-...] [--image path] [--dry-run] [--self-check]
 * 纪律：按 BUG编号 upsert。不删除已有编号行。空首列的占位行会删掉。
 *       文本更新不覆盖截图列。--image 追加。无 --image 且列里已有附件时不重传。
 *       无凭证时软失败（退出码 0）。
 */

import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-daily-snapshot-board.yaml');
const REGISTRY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'qa', 'bug-registry.yaml');
const BUGS_ROOT = path.join(ORCH_ROOT, 'agent-delivery', 'qa', 'bugs');

const DRY_RUN = process.argv.includes('--dry-run');
const SELF_CHECK = process.argv.includes('--self-check');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const CONCLUSIONS = ['产品缺陷', '数据缺口', '环境不可用', '用例与现网不一致'];
const STATUS_LABEL = {
  open: '待处理',
  fixed: '已修复',
  verified: '已复验',
  closed: '已关闭',
  deferred: '暂缓',
};
const IMAGE_EXT = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp']);

function argValue(flag) {
  const i = process.argv.indexOf(flag);
  return i >= 0 ? process.argv[i + 1] || '' : '';
}
function argValues(flag) {
  const out = [];
  for (let i = 0; i < process.argv.length; i++) {
    if (process.argv[i] === flag && process.argv[i + 1]) out.push(process.argv[i + 1]);
  }
  return out;
}

const onlyId = argValue('--id');
const extraImages = argValues('--image');

function loadBugConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const appToken = (raw.match(/^\s+app_token:\s*"([^"]*)"/m) || [])[1] || '';
  const bugsBlock = raw.match(/^ {2}bugs:\s*\r?\n((?: {4}.+\r?\n)+)/m)?.[1] || '';
  const pick = (block, key) => (block.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  const fnSection = raw.match(/^field_names:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m)?.[1] || '';
  const fnBlock = fnSection.match(/^ {2}bugs:\s*\r?\n((?: {4}.+\r?\n)+)/m)?.[1] || '';
  const fields = {};
  for (const line of fnBlock.split(/\r?\n/)) {
    const m = line.match(/^\s+([a-z_]+):\s*"([^"]+)"/);
    if (m) fields[m[1]] = m[2];
  }
  if (!appToken || !fields.id || !fields.screenshot) {
    throw new Error('feishu-daily-snapshot-board.yaml 缺少 app_token 或 field_names.bugs');
  }
  return {
    appToken,
    tableName: pick(bugsBlock, 'table_name') || '缺陷',
    tableId: pick(bugsBlock, 'table_id'),
    fields,
  };
}

function backfillTableId(tableId) {
  let raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const re = /( {2}bugs:\s*\r?\n {4}table_name:\s*"[^"]*"\r?\n {4}table_id:\s*)""/;
  if (!re.test(raw)) return;
  raw = raw.replace(re, `$1"${tableId}"`);
  fs.writeFileSync(CONFIG_PATH, raw, 'utf8');
  console.log(`[config] bugs.table_id 已回填：${tableId}`);
}

function parseRegistry(text) {
  const bugs = [];
  let cur = null;
  for (const line of text.split(/\r?\n/)) {
    const id = line.match(/^ {2}- id:\s*(\S+)\s*$/);
    if (id) {
      if (cur) bugs.push(cur);
      cur = { id: id[1] };
      continue;
    }
    if (!cur) continue;
    const kv = line.match(/^ {4}([a-z_]+):\s*(.*)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    if (v === 'null' || v === '~') v = '';
    else v = v.replace(/^["']|["']$/g, '');
    cur[kv[1]] = v;
  }
  if (cur) bugs.push(cur);
  return bugs;
}

function dateFromId(id) {
  const m = String(id).match(/-(\d{4})(\d{2})(\d{2})-\d{3}$/);
  return m ? `${m[1]}-${m[2]}-${m[3]}` : '';
}

function clip(text) {
  const t = String(text || '').trim();
  // ponytail: 飞书文本列按 10000 字截断；全文仍在 bugs md
  if (t.length <= 10000) return t;
  return `${t.slice(0, 10000)}\n…`;
}

export function parseBugMarkdown(text) {
  const parts = String(text).split(/^(?=#{1,2} BUG-\S+)/m);
  const out = [];
  for (const part of parts) {
    const head = part.match(/^#{1,2} (BUG-\S+) · (.+)$/m);
    if (!head) continue;
    const meta = {};
    for (const line of part.split(/\r?\n/)) {
      const cell = line.match(/^\| ([^|]+) \| ([^|]*) \|$/);
      if (!cell) continue;
      const key = cell[1].trim();
      if (key === '项' || key.startsWith('---')) continue;
      meta[key] = cell[2].trim();
    }
    const section = (name) => {
      const m = part.match(new RegExp(`### ${name}\\s*\\r?\\n([\\s\\S]*?)(?=\\n### |\\n## |$)`));
      return m ? m[1].trim() : '';
    };
    const shotLine = (section('证据').match(/^- 截图：\s*(.+)$/m) || [])[1] || '';
    out.push({
      id: head[1],
      title: head[2].trim(),
      conclusion: meta['结论'] || '',
      module: meta['模块'] || '',
      entry: meta['入口'] || '',
      env: meta['环境'] || '',
      foundDate: /^\d{4}-\d{2}-\d{2}$/.test(meta['发现日期'] || '') ? meta['发现日期'] : '',
      sourceCase: meta['关联用例'] || '',
      expected: section('预期'),
      actual: section('实际'),
      shotLine,
    });
  }
  return out;
}

function walkMd(dir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ent.name.startsWith('_') || ent.name === 'README.md') continue;
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walkMd(p, acc);
    else if (ent.name.endsWith('.md')) acc.push(p);
  }
  return acc;
}

function assetImages(bugId) {
  const hits = [];
  const walk = (dir) => {
    if (!fs.existsSync(dir)) return;
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(p);
      else if (path.basename(dir) === bugId && IMAGE_EXT.has(path.extname(ent.name).toLowerCase())) hits.push(p);
    }
  };
  walk(BUGS_ROOT);
  return hits;
}

function loadBugs() {
  const registry = parseRegistry(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  const md = new Map();
  const files = walkMd(BUGS_ROOT).sort((a, b) => {
    const rank = (p) => (p.includes(`${path.sep}items${path.sep}`) ? 1 : 0);
    return rank(a) - rank(b);
  });
  for (const file of files) {
    for (const bug of parseBugMarkdown(fs.readFileSync(file, 'utf8'))) md.set(bug.id, bug);
  }
  return registry
    .filter((r) => !onlyId || r.id === onlyId)
    .map((r) => {
      const extra = md.get(r.id) || {};
      const images = assetImages(r.id);
      return {
        id: r.id,
        title: r.title || extra.title || r.id,
        conclusion: CONCLUSIONS.includes(extra.conclusion) ? extra.conclusion : '',
        module: extra.module || '',
        entry: extra.entry || '',
        env: extra.env || '',
        expected: clip(extra.expected),
        actual: clip(extra.actual),
        status: STATUS_LABEL[r.status] || '',
        sourceCase: extra.sourceCase || r.source_case || '',
        foundDate: extra.foundDate || dateFromId(r.id),
        images,
      };
    });
}

function textField(name) {
  return { field_name: name, type: 1 };
}
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function dateField(name) {
  return { field_name: name, type: 5, property: { date_formatter: 'yyyy/MM/dd', auto_fill: false } };
}
function attachmentField(name) {
  return { field_name: name, type: 17 };
}

function fieldDefs(fn) {
  return [
    textField(fn.title),
    selectField(fn.conclusion, CONCLUSIONS),
    textField(fn.module),
    textField(fn.entry),
    textField(fn.env),
    textField(fn.expected),
    textField(fn.actual),
    selectField(fn.status, Object.values(STATUS_LABEL)),
    attachmentField(fn.screenshot),
    textField(fn.source_case),
    dateField(fn.found_date),
  ];
}

function dateToMs(yyyyMmDd) {
  const ms = Date.parse(`${yyyyMmDd}T00:00:00+08:00`);
  return Number.isNaN(ms) ? 0 : ms;
}

function payload(fn, row) {
  const fields = { [fn.id]: row.id, [fn.title]: row.title };
  const text = [
    [fn.module, row.module],
    [fn.entry, row.entry],
    [fn.env, row.env],
    [fn.expected, row.expected],
    [fn.actual, row.actual],
    [fn.source_case, row.sourceCase],
  ];
  for (const [key, value] of text) if (value) fields[key] = value;
  if (row.conclusion) fields[fn.conclusion] = row.conclusion;
  if (row.status) fields[fn.status] = row.status;
  const ms = dateToMs(row.foundDate);
  if (ms) fields[fn.found_date] = ms;
  return fields;
}

async function ensureTable(cfg, token) {
  if (cfg.tableId) return cfg.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === cfg.tableName);
  if (!hit) {
    const names = (list.data?.items || []).map((t) => t.name).join('、');
    throw new Error(`多维表格里没有「${cfg.tableName}」。现有：${names}`);
  }
  backfillTableId(hit.table_id);
  return hit.table_id;
}

async function ensurePrimary(cfg, token, tableId) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const items = data.data?.items || [];
  if (items.some((f) => f.field_name === cfg.fields.id)) return;
  const primary = items.find((f) => f.is_primary) || items.find((f) => f.field_name === '文本');
  if (!primary) throw new Error('缺陷表没有首列，无法改名为 BUG编号');
  if (DRY_RUN) {
    console.log(`[dry-run] 将把首列「${primary.field_name}」改名为「${cfg.fields.id}」`);
    return;
  }
  await feishuApi('PUT', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields/${primary.field_id}`, token, {
    field_name: cfg.fields.id,
    type: primary.type || 1,
  });
  console.log(`[field] 首列「${primary.field_name}」已改名为「${cfg.fields.id}」`);
}

async function ensureFields(cfg, token, tableId) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of fieldDefs(cfg.fields)) {
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

async function uploadFile(token, appToken, filePath) {
  const buf = fs.readFileSync(filePath);
  const name = path.basename(filePath);
  const form = new FormData();
  form.append('file_name', name);
  form.append('parent_type', 'bitable_file');
  form.append('parent_node', appToken);
  form.append('size', String(buf.length));
  form.append('extra', JSON.stringify({ drive_route_token: appToken }));
  form.append('file', new Blob([buf]), name);
  const resp = await fetch('https://open.feishu.cn/open-apis/drive/v1/medias/upload_all', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const data = await resp.json();
  if (data.code !== 0 || !data.data?.file_token) {
    throw new Error(`上传截图失败 ${name}: code=${data.code} msg=${data.msg}`);
  }
  return data.data.file_token;
}

function existingTokens(value) {
  if (!Array.isArray(value)) return [];
  return value.map((item) => item?.file_token).filter(Boolean);
}

async function deleteEmptyRows(cfg, token, tableId, records) {
  const empty = records
    .filter((rec) => !bitableFieldToString(rec.fields?.[cfg.fields.id]).trim())
    .map((rec) => rec.record_id);
  if (!empty.length) return 0;
  if (DRY_RUN) {
    console.log(`[dry-run] 将删除空首列占位行 ${empty.length} 条`);
    return empty.length;
  }
  await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_delete`, token, {
    records: empty,
  });
  console.log(`[prune] 已删除空首列占位行 ${empty.length} 条`);
  return empty.length;
}

async function upsertOne(cfg, token, tableId, row, byId) {
  const fn = cfg.fields;
  const fields = payload(fn, row);
  const hit = byId.get(row.id);
  let recordId = hit?.record_id || '';
  if (DRY_RUN) {
    console.log(`[dry-run] ${recordId ? '更新' : '新增'} ${row.id} 截图 ${row.images.length + extraImages.length} 张`);
    return;
  }
  if (recordId) {
    await feishuApi('PUT', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/${recordId}`, token, { fields });
  } else {
    const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records`, token, { fields });
    recordId = created.data?.record?.record_id || '';
    if (!recordId) throw new Error(`写入失败：${row.id}`);
  }
  console.log(`[row] ${row.id} 已写 ${Object.keys(fields).join('、')}`);
  const localImages = extraImages.length && (!onlyId || onlyId === row.id) ? extraImages : row.images;
  const already = existingTokens(hit?.fields?.[fn.screenshot]);
  const toUpload = extraImages.length && (!onlyId || onlyId === row.id) ? localImages : already.length ? [] : localImages;
  if (!toUpload.length || !recordId) return;
  const tokens = extraImages.length ? already.slice() : [];
  for (const file of toUpload) {
    if (!fs.existsSync(file)) throw new Error(`截图不存在：${file}`);
    tokens.push(await uploadFile(token, cfg.appToken, file));
    await sleep(200);
  }
  await feishuApi('PUT', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/${recordId}`, token, {
    fields: { [fn.screenshot]: tokens.map((file_token) => ({ file_token })) },
  });
  console.log(`[image] ${row.id} 附件 ${tokens.length} 个`);
}

function selfCheck() {
  const sample = `# BUG-ZNFWJQ-KJZTFWXT-20261030-001 · 清单为空

| 项 | 值 |
|----|----|
| 编号 | BUG-ZNFWJQ-KJZTFWXT-20261030-001 |
| 结论 | 产品缺陷 |
| 模块 | 企业分析 / 查询 |
| 入口 | /enterprise/x |
| 环境 | https://example.test/ |
| 发现日期 | 2026-10-30 |
| 关联用例 | 无 |

### 预期

应该看到清单。

### 实际

清单为空。

### 证据

- 截图：无
`;
  const rows = parseBugMarkdown(sample);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].id, 'BUG-ZNFWJQ-KJZTFWXT-20261030-001');
  assert.equal(rows[0].module, '企业分析 / 查询');
  assert.equal(rows[0].expected, '应该看到清单。');
  assert.equal(rows[0].actual, '清单为空。');
  assert.equal(dateFromId(rows[0].id), '2026-10-30');
  const reg = parseRegistry('bugs:\n  - id: BUG-A\n    title: 甲\n    source_case: null\n    status: fixed\n');
  assert.equal(reg.length, 1);
  assert.equal(reg[0].status, 'fixed');
  assert.equal(reg[0].source_case, '');
  assert.equal(STATUS_LABEL.fixed, '已修复');
  console.log('[self-check] ok');
}

async function main() {
  if (SELF_CHECK) {
    selfCheck();
    return;
  }
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBugConfig();
  const rows = loadBugs();
  if (extraImages.length && !onlyId) throw new Error('--image 必须和 --id 一起用');
  if (onlyId && !rows.length) throw new Error(`台账里没有 ${onlyId}`);
  console.log(`[source] ${rows.length} 条${onlyId ? `（仅 ${onlyId}）` : ''}`);
  if (DRY_RUN && !process.env.FEISHU_APP_ID) {
    console.log(`[sample] ${rows[0] ? rows[0].id : '(空)'} ${rows[0]?.title || ''}`);
    console.log('[dry-run] 未读凭证，只解析了台账');
    return;
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：飞书未同步');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token);
  console.log(`[table] ${cfg.tableName} ${tableId}`);
  await ensurePrimary(cfg, token, tableId);
  await ensureFields(cfg, token, tableId);
  if (DRY_RUN) {
    console.log('[dry-run] 列已核对，不写记录');
    return;
  }

  const records = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token, cfg.appToken, tableId);
  await deleteEmptyRows(cfg, token, tableId, records);
  const byId = new Map();
  for (const rec of records) {
    const id = bitableFieldToString(rec.fields?.[cfg.fields.id]).trim();
    if (id) byId.set(id, rec);
  }
  let created = 0;
  let updated = 0;
  for (const row of rows) {
    const existed = byId.has(row.id);
    await upsertOne(cfg, token, tableId, row, byId);
    if (existed) updated += 1;
    else created += 1;
    await sleep(200);
  }
  console.log(`[done] 新增 ${created}，更新 ${updated}。https://zhipu-ai.feishu.cn/base/${cfg.appToken}?table=${tableId}`);
}

const isDirect = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isDirect) {
  main().catch((err) => {
    console.error(`[ERROR] ${err.message}`);
    process.exitCode = 1;
  });
}
