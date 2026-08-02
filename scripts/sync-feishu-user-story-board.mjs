#!/usr/bin/env node
/**
 * sync-feishu-user-story-board.mjs —— 飞书「用户故事库」看板出站同步
 * ---------------------------------------------------------------------------
 * 真源：agent-delivery/user-story-library.yaml（extract-user-stories 生成 + check-story-coverage 回填）
 * 行为：自动建表/建列 → 按「故事ID」upsert；飞书只读投影，不回写。
 * 「实现任务」= 单向关联(type=18) → 任务看板记录；点击打开任务详情侧栏（显示主列 Task ID）。
 * 用法：node scripts/sync-feishu-user-story-board.mjs [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0，提示待手跑/投影机）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv, loadBitableConfig } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';
import { STORY_STATUS_ZH, STORY_STATUS_ORDER } from './lib/story-progress.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-user-story-board.yaml');
const LIBRARY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'user-story-library.yaml');
const REGISTRY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'task-registry.yaml');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const LINK_FIELD_TYPE = 18; // 单向关联 SingleLink
const STATUS_OPTIONS = STORY_STATUS_ORDER.map((k) => STORY_STATUS_ZH[k]);
/* ── 配置 ── */
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
  const handoffLink = {
    enabled: true,
    writeMode: 'plain',
    gitlabBase: '',
    gitlabGroup: '',
    repo: '',
    branch: '',
    pathPrefix: '',
  };
  const hlBlock = raw.match(/^handoff_link:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  const HL_KEYS = {
    gitlab_base: 'gitlabBase',
    gitlab_group: 'gitlabGroup',
    repo: 'repo',
    branch: 'branch',
    path_prefix: 'pathPrefix',
  };
  if (hlBlock) {
    for (const line of hlBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"?([^"\r\n#]+)"?\s*(?:#.*)?$/);
      if (!m) continue;
      if (m[1] === 'enabled') handoffLink.enabled = m[2].trim() === 'true';
      else if (m[1] === 'write_mode') handoffLink.writeMode = m[2].trim();
      else if (HL_KEYS[m[1]]) handoffLink[HL_KEYS[m[1]]] = m[2].trim();
    }
  }

  const taskCfg = loadBitableConfig();
  const taskBoard = { tableId: taskCfg.tableId, taskIdField: taskCfg.fieldTaskId || 'Task ID' };
  const tbBlock = raw.match(/^task_board:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  if (tbBlock) {
    for (const line of tbBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"([^"]+)"/);
      if (!m) continue;
      if (m[1] === 'table_id') taskBoard.tableId = m[2];
      if (m[1] === 'task_id_field') taskBoard.taskIdField = m[2];
    }
  }

  // bitable.table_id 在 yaml 里出现两次时 get() 会命中第一个（故事表）；显式取 bitable 块下的
  const storyTableId =
    (raw.match(/^bitable:\s*\r?\n(?:[ \t]+.+\r?\n)*?[ \t]+table_id:\s*"([^"]*)"/m) || [])[1] ||
    get('table_id');

  return {
    raw,
    appToken: get('app_token') || taskCfg.appToken,
    tableName: get('table_name'),
    tableId: storyTableId,
    fieldNames,
    handoffLink,
    taskBoard,
  };
}

function backfillTableId(tableId) {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  if (!/^\s+table_id:\s*""/m.test(raw)) return;
  fs.writeFileSync(CONFIG_PATH, raw.replace(/^(\s+table_id:\s*)""/m, `$1"${tableId}"`), 'utf8');
  console.log(`[config] table_id 已回填：${tableId}`);
}

/* ── 真源解析 ── */
function parseStories(text) {
  const stories = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"([^"]+)"/);
    if (idm) {
      current = {
        id: idm[1],
        title: '',
        text: '',
        module: '',
        source: '',
        roles: [],
        status: 'defined',
        implementation_tasks: [],
      };
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

/** registry id → feishu_bitable_record_id（同步脚本可读 registry；飞书侧缺 record 时再扫任务表） */
function parseRegistryRecordIds() {
  const map = new Map();
  if (!fs.existsSync(REGISTRY_PATH)) return map;
  const raw = fs.readFileSync(REGISTRY_PATH, 'utf8');
  let cur = null;
  for (const line of raw.split(/\r?\n/)) {
    const idm = line.match(/^  - id:\s*(.+)/);
    if (idm) {
      cur = idm[1].trim().replace(/^["']|["']$/g, '');
      continue;
    }
    if (!cur) continue;
    const rm = line.match(/^\s+feishu_bitable_record_id:\s*(.+)/);
    if (rm) {
      const rid = rm[1].trim().replace(/^["']|["']$/g, '');
      if (rid) map.set(cur, rid);
    }
  }
  return map;
}

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
  const stories = parseStories(fs.readFileSync(LIBRARY_PATH, 'utf8'));
  const today = new Date().toISOString().slice(0, 10);
  return stories.map((s) => ({
    storyId: s.id,
    taskIds: s.implementation_tasks,
    fieldsZh: {
      title: s.title || s.id,
      text: s.text || '',
      module: s.module || '—',
      roles: s.roles.length ? s.roles.join('、') : '',
      source: sourceUrl(s.source, cfg),
      status: STORY_STATUS_ZH[s.status] ?? s.status,
      synced_at: today,
    },
  }));
}

/* ── 字段定义 ── */
function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}
function linkField(name, taskTableId) {
  return {
    field_name: name,
    type: LINK_FIELD_TYPE,
    property: { multiple: true, table_id: taskTableId },
  };
}

function fieldDefs(cfg, rows) {
  const fn = cfg.fieldNames;
  const moduleOptions = [...new Set(rows.map((r) => r.fieldsZh.module))].sort();
  return [
    textField(fn.story_id),
    textField(fn.title),
    textField(fn.text),
    selectField(fn.module, moduleOptions),
    textField(fn.roles),
    textField(fn.source),
    selectField(fn.status, STATUS_OPTIONS),
    linkField(fn.implementation_tasks, cfg.taskBoard.tableId),
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
    console.log(`[dry-run] 将创建数据表「${cfg.tableName}」（${fieldDefs(cfg, rows).length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: cfg.tableName, default_view_name: '全量总览', fields: fieldDefs(cfg, rows) },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error('建表失败：无 table_id 返回');
  console.log(`[table] 已创建「${cfg.tableName}」table_id=${tableId}`);
  backfillTableId(tableId);
  return tableId;
}

/** 保证「实现任务」为单向关联；若现存为文本列则删后重建 */
async function ensureFields(cfg, token, tableId, rows) {
  const data = await feishuApi(
    'GET',
    `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`,
    token,
  );
  const items = data.data?.items || [];
  const byName = new Map(items.map((f) => [f.field_name, f]));
  const linkName = cfg.fieldNames.implementation_tasks;
  const existingLink = byName.get(linkName);

  if (existingLink && existingLink.type !== LINK_FIELD_TYPE) {
    console.log(
      `[field] 「${linkName}」当前 type=${existingLink.type}，将迁移为单向关联 → ${cfg.taskBoard.tableId}`,
    );
    if (!DRY_RUN) {
      await feishuApi(
        'DELETE',
        `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields/${existingLink.field_id}`,
        token,
      );
      byName.delete(linkName);
      await sleep(300);
    }
  } else if (
    existingLink &&
    existingLink.type === LINK_FIELD_TYPE &&
    existingLink.property?.table_id &&
    existingLink.property.table_id !== cfg.taskBoard.tableId
  ) {
    console.warn(
      `[WARN] 「${linkName}」已关联到 ${existingLink.property.table_id}，期望 ${cfg.taskBoard.tableId}；请人工核对`,
    );
  }

  for (const def of fieldDefs(cfg, rows)) {
    if (byName.has(def.field_name)) continue;
    if (DRY_RUN) {
      console.log(`[dry-run] 将补建列「${def.field_name}」type=${def.type}`);
      continue;
    }
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields`, token, def);
    console.log(`[field] 已补建列「${def.field_name}」type=${def.type}`);
    await sleep(200);
  }

  await ensureStatusSelectOptions(cfg, token, tableId, byName);
}

/** 补齐「实现状态」单选七态选项（保留已有选项 ID，追加缺失项） */
async function ensureStatusSelectOptions(cfg, token, tableId, byName) {
  const statusName = cfg.fieldNames.status;
  const field = byName.get(statusName);
  if (!field || field.type !== 3) return;
  const existing = field.property?.options || [];
  const existingNames = new Set(existing.map((o) => o.name));
  const missing = STATUS_OPTIONS.filter((n) => !existingNames.has(n));
  if (!missing.length) return;
  if (DRY_RUN) {
    console.log(`[dry-run] 将为「${statusName}」追加选项: ${missing.join(', ')}`);
    return;
  }
  const options = [
    ...existing.map((o) => ({ id: o.id, name: o.name, color: o.color })),
    ...missing.map((name) => ({ name })),
  ];
  await feishuApi(
    'PUT',
    `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields/${field.field_id}`,
    token,
    { field_name: statusName, type: 3, property: { options } },
  );
  console.log(`[field] 「${statusName}」已追加选项: ${missing.join(', ')}`);
  await sleep(200);
}

async function buildTaskIdToRecordMap(cfg, token) {
  const map = parseRegistryRecordIds();
  const needed = new Set();
  // 仅当 registry 缺 record_id 时才扫任务表
  const stories = parseStories(fs.readFileSync(LIBRARY_PATH, 'utf8'));
  for (const s of stories) {
    for (const tid of s.implementation_tasks) {
      if (!map.has(tid)) needed.add(tid);
    }
  }
  if (!needed.size) {
    console.log(`[link] 任务 record_id 映射：registry=${map.size}，无需扫任务表`);
    return map;
  }
  console.log(`[link] registry 缺 ${needed.size} 个 record_id，扫描任务看板补齐…`);
  const taskRows = await listAllBitableRecords(
    { appToken: cfg.appToken, tableId: cfg.taskBoard.tableId },
    token,
  );
  const field = cfg.taskBoard.taskIdField;
  let filled = 0;
  for (const rec of taskRows) {
    const tid = bitableFieldToString(rec.fields?.[field]).trim();
    if (!tid) continue;
    if (!map.has(tid)) {
      map.set(tid, rec.record_id);
      if (needed.has(tid)) filled += 1;
    }
  }
  console.log(`[link] 任务表扫描完成：补齐 ${filled}/${needed.size}，映射总计 ${map.size}`);
  return map;
}

function resolveLinkIds(taskIds, taskMap, missing) {
  const recIds = [];
  for (const tid of taskIds) {
    const rid = taskMap.get(tid);
    if (rid) recIds.push(rid);
    else missing.push(tid);
  }
  return recIds;
}

async function upsertRows(cfg, token, tableId, rows, taskMap) {
  const fn = cfg.fieldNames;
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byStoryId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.story_id]).trim();
    if (id) byStoryId.set(id, rec.record_id);
  }

  const missing = [];
  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = { [fn.story_id]: row.storyId };
    for (const [key, value] of Object.entries(row.fieldsZh)) {
      if (fn[key]) fields[fn[key]] = value ?? '';
    }
    fields[fn.implementation_tasks] = resolveLinkIds(row.taskIds || [], taskMap, missing);
    const recordId = byStoryId.get(row.storyId);
    if (recordId) toUpdate.push({ record_id: recordId, fields });
    else toCreate.push({ fields });
  }

  if (missing.length) {
    const uniq = [...new Set(missing)];
    console.warn(
      `[WARN] ${uniq.length} 个任务无飞书 record_id，跳过关联：${uniq.slice(0, 12).join(', ')}${uniq.length > 12 ? '…' : ''}`,
    );
  }

  console.log(`[plan] 共 ${rows.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}`);
  if (DRY_RUN) {
    const sample = rows.find((r) => r.taskIds?.length);
    if (sample) {
      console.log(
        `[sample] ${sample.storyId} tasks=${sample.taskIds.join(',')} → recs=${JSON.stringify(
          resolveLinkIds(sample.taskIds, taskMap, []),
        )}`,
      );
    }
    return;
  }

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
  console.log('[done] 看板已同步（实现任务=可点击关联）');
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  if (!cfg.taskBoard.tableId) throw new Error('task_board.table_id 未配置');
  const rows = buildRows(cfg);
  const bySt = {};
  for (const r of rows) {
    const st = r.fieldsZh.status || '—';
    bySt[st] = (bySt[st] || 0) + 1;
  }
  const dist = Object.entries(bySt)
    .map(([k, n]) => `${k}=${n}`)
    .join(', ');
  console.log(`[source] 用户故事 ${rows.length} 条（${dist}）`);
  if (!rows.length) throw new Error(`未解析到任何故事，请检查 ${LIBRARY_PATH}`);

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn(
      '[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步，请在配好 .env 的机器（如投影机）重跑本脚本',
    );
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token, rows);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId, rows);
  const taskMap = await buildTaskIdToRecordMap(cfg, token);
  await upsertRows(cfg, token, tableId, rows, taskMap);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
