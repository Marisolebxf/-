#!/usr/bin/env node
/**
 * Cross-platform task status updater + optional Feishu Bitable outbound (soft-fail).
 *
 * Usage:
 *   node scripts/lib/board-task-status.mjs --task-id ID --status review [--sync-board]
 *   node scripts/lib/board-task-status.mjs --task-id ID --heartbeat [--sync-board]
 *   node scripts/lib/board-task-status.mjs --watch-outbound [--sprint-id 2026-W28]
 *
 * Defaults: --sync-board ON; use --no-sync to skip. Missing FEISHU_* ? YAML still written, warn.
 * No WSL required. Node 18+.
 */

import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { touchUpdateTime, VALID_STATUSES as LIB_VALID_STATUSES } from './task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..', '..');
const REGISTRY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'task-registry.yaml');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-bitable.yaml');
const SCRUM_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'scrum-sprint.yaml');
const USER_MAP_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-user-map.yaml');
const LOG_DIR = path.join(ORCH_ROOT, 'agent-delivery', '_tmp');
const LOG_PATH = path.join(LOG_DIR, 'board-sync-watch.log');

// VALID_STATUSES imported from task-registry-lib.mjs (single source of truth)
const VALID_STATUSES = LIB_VALID_STATUSES;

const DEFAULT_STATUS_MAP = {
  backlog: '\u5f85\u6392\u671f',
  ready: '\u5f85\u8ba4\u9886',
  claimed: '\u5df2\u8ba4\u9886',
  in_progress: '\u8fdb\u884c\u4e2d',
  integration: '\u8054\u8c03\u4e2d',
  pending_test: '\u5f85\u6d4b\u8bd5',
  testing: '\u6d4b\u8bd5\u4e2d',
  ready_to_sign: '\u5f85\u7b7e\u6536',
  done: '\u5df2\u5b8c\u6210',
  blocked: '\u963b\u585e',
  'needs-revision': '\u8bc4\u5ba1\u4e2d',
};

function loadDotEnv(orchRoot) {
  const envFile = path.join(orchRoot, '.env');
  if (!fs.existsSync(envFile)) return;
  const text = fs.readFileSync(envFile, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const m = t.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    if (
      (v.startsWith('"') && v.endsWith('"')) ||
      (v.startsWith("'") && v.endsWith("'"))
    ) {
      v = v.slice(1, -1);
    }
    if (process.env[m[1]] === undefined) process.env[m[1]] = v;
  }
}

function parseArgs(argv) {
  const out = {
    taskId: '',
    status: '',
    claimedBy: '',
    supervisedBy: '',
    blockedBy: '',
    evidence: '',
    heartbeat: false,
    syncBoard: true,
    dryRun: false,
    watchOutbound: false,
    skipKanbanFields: false,
    dispatchOnly: false,
    dispatchGate: '',
    dispatchConfirmBy: '',
    dispatchTrigger: '',
    sprintId: '',
    allSprints: false,
    onlyTaskIds: [],
    lockHours: 2,
    help: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    switch (a) {
      case '--task-id':
      case '-t':
        out.taskId = next();
        break;
      case '--status':
      case '-s':
        out.status = next();
        break;
      case '--claimed-by':
        out.claimedBy = next();
        break;
      case '--supervised-by':
        out.supervisedBy = next();
        break;
      case '--blocked-by':
        out.blockedBy = next();
        break;
      case '--evidence':
        out.evidence = next();
        break;
      case '--heartbeat':
        out.heartbeat = true;
        break;
      case '--sync-board':
        out.syncBoard = true;
        break;
      case '--no-sync':
        out.syncBoard = false;
        break;
      case '--dry-run':
        out.dryRun = true;
        break;
      case '--watch-outbound':
        out.watchOutbound = true;
        break;
      case '--skip-kanban-fields':
        out.skipKanbanFields = true;
        break;
      case '--only-task-ids': {
        const raw = next() || '';
        out.onlyTaskIds = raw
          .split(/[,;\s]+/)
          .map((s) => s.trim())
          .filter(Boolean);
        break;
      }
      case '--dispatch-only':
        out.dispatchOnly = true;
        out.syncBoard = true;
        break;
      case '--dispatch-gate':
        out.dispatchGate = next();
        break;
      case '--dispatch-confirm-by':
        out.dispatchConfirmBy = next();
        break;
      case '--dispatch-trigger':
        out.dispatchTrigger = next();
        break;
      case '--sprint-id':
        out.sprintId = next();
        break;
      case '--all-sprints':
        out.allSprints = true;
        break;
      case '--lock-hours':
        out.lockHours = Number(next()) || 2;
        break;
      case '--help':
      case '-h':
        out.help = true;
        break;
      default:
        if (a.startsWith('-')) throw new Error(`Unknown arg: ${a}`);
    }
  }
  return out;
}

function usage() {
  console.log(`board-task-status.mjs — update task-registry + optional Feishu sync

  node scripts/lib/board-task-status.mjs --task-id ID --status review
  node scripts/lib/board-task-status.mjs --task-id ID --heartbeat --sync-board
  node scripts/lib/board-task-status.mjs --watch-outbound [--sprint-id 2026-W28]
  node scripts/lib/board-task-status.mjs --watch-outbound --all-sprints
  node scripts/lib/board-task-status.mjs --watch-outbound --only-task-ids ID1,ID2

  --skip-kanban-fields   watch 模式：不覆盖飞书状态/认领/Sprint（Cron 默认）
  --all-sprints          投影全部 Sprint（含历史 done）
  --only-task-ids        仅投影所列任务（跨 Sprint；配合全量看板字段写出）
  --no-sync              skip Feishu (YAML only)
  --dry-run              print plan, no write
  Default: --sync-board on; soft-fail if FEISHU_* missing`);
}

function yamlQuote(v) {
  const s = String(v);
  if (/[:#{}[\],&*?|>!%@`]/.test(s) || /\s/.test(s) || s === '') {
    return JSON.stringify(s);
  }
  return s;
}

function findTaskBlock(lines, taskId) {
  let inTasks = false;
  let start = -1;
  let end = -1;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^tasks:\s*$/.test(line)) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    const idMatch = line.match(/^\s+- id:\s*(.+)\s*$/);
    if (idMatch) {
      const id = idMatch[1].trim().replace(/^["']|["']$/g, '');
      if (start >= 0) {
        end = i;
        break;
      }
      if (id === taskId) start = i;
    }
  }
  if (start >= 0 && end < 0) end = lines.length;
  if (start < 0) return null;
  return { start, end };
}

function getField(blockLines, key) {
  const re = new RegExp(`^(\\s+)${key}:\\s*(.+?)\\s*$`);
  for (const line of blockLines) {
    const m = line.match(re);
    if (m) return m[2].replace(/^["']|["']$/g, '');
  }
  return '';
}

/** Extract YAML `|` / `>` block or plain scalar for a key. */
function getMultilineField(blockLines, key) {
  const startRe = new RegExp(`^(\\s+)${key}:\\s*(.*)\\s*$`);
  for (let i = 0; i < blockLines.length; i++) {
    const m = blockLines[i].match(startRe);
    if (!m) continue;
    const indent = m[1].length;
    const rest = m[2].trim();
    if (rest === '|' || rest === '>') {
      const body = [];
      for (let j = i + 1; j < blockLines.length; j++) {
        const line = blockLines[j];
        if (/^\s*$/.test(line)) {
          body.push('');
          continue;
        }
        const lead = (line.match(/^(\s*)/) || ['', ''])[1].length;
        if (lead <= indent) break;
        body.push(line.slice(indent + 2).replace(/\s+$/, ''));
      }
      return body.join('\n').trim();
    }
    if (rest === '') return '';
    return rest.replace(/^["']|["']$/g, '');
  }
  return '';
}

/** Extract YAML list under a key as "- a\\n- b". */
function getListField(blockLines, key) {
  const startRe = new RegExp(`^(\\s+)${key}:\\s*$`);
  for (let i = 0; i < blockLines.length; i++) {
    const m = blockLines[i].match(startRe);
    if (!m) continue;
    const indent = m[1].length;
    const items = [];
    for (let j = i + 1; j < blockLines.length; j++) {
      const line = blockLines[j];
      if (/^\s*$/.test(line)) continue;
      const lead = (line.match(/^(\s*)/) || ['', ''])[1].length;
      if (lead <= indent) break;
      const im = line.match(/^\s+-\s+(.+)$/);
      if (im) items.push(`- ${im[1].trim()}`);
      else break;
    }
    return items.join('\n');
  }
  return '';
}

function upsertField(blockLines, key, value) {
  const indent = '    ';
  const re = new RegExp(`^(\\s+)${key}:\\s*.*$`);
  const rendered = `${indent}${key}: ${yamlQuote(value)}`;
  for (let i = 0; i < blockLines.length; i++) {
    if (re.test(blockLines[i])) {
      blockLines[i] = rendered;
      return;
    }
  }
  blockLines.splice(1, 0, rendered);
}

function warnTransition(from, to) {
  if (!from || !to || from === to) return;
  if (from === 'done') console.warn(`[WARN] transition done ? ${to} (unusual)`);
  if (from === 'backlog' && to === 'in_progress') {
    console.warn(`[WARN] skipped claimed: backlog ? in_progress`);
  }
}

function readCurrentSprint() {
  if (!fs.existsSync(SCRUM_PATH)) return '';
  const raw = fs.readFileSync(SCRUM_PATH, 'utf8');
  const m = raw.match(/^\s*current_sprint:\s*"?([^"\r\n]+)"?/m);
  return m ? m[1].trim() : '';
}

function parseSimpleYamlMap(raw, sectionKey) {
  const map = {};
  const re = new RegExp(
    `^${sectionKey}:\\s*\\r?\\n((?:[ \\t].+\\r?\\n)+)`,
    'm',
  );
  const m = raw.match(re);
  if (!m) return map;
  for (const line of m[1].split(/\r?\n/)) {
    const km = line.match(/^\s+([A-Za-z0-9_-]+):\s*"?(.*?)"?\s*$/);
    if (km) map[km[1]] = km[2];
  }
  return map;
}

function loadBitableConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const get = (key) => {
    const m = raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm'));
    return m ? m[1] : '';
  };
  const statusMap = { ...DEFAULT_STATUS_MAP, ...parseSimpleYamlMap(raw, 'status_map') };
  const epicExact = parseSimpleYamlMap(raw, 'epic_module_map');
  const epicPrefix = parseSimpleYamlMap(raw, 'epic_module_prefix');
  const taskModuleMap = parseSimpleYamlMap(raw, 'task_module_map');
  const taskModulePrefix = parseSimpleYamlMap(raw, 'task_module_prefix');
  let epicDefault = '\u5176\u4ed6';
  const ed = raw.match(/^\s*epic_module_default:\s*"([^"]*)"/m);
  if (ed) epicDefault = ed[1];
  return {
    appToken: get('app_token'),
    tableId: get('table_id'),
    fieldTaskId: get('task_id') || 'Task ID',
    fieldTitle: get('title') || '\u6807\u9898',
    fieldUserStory: get('user_story') || '\u7528\u6237\u6545\u4e8b',
    fieldStatus: get('status') || '\u72b6\u6001',
    fieldAgent: get('agent') || 'Agent',
    fieldEpic: get('epic') || 'Epic',
    fieldSprint: get('sprint_id') || 'Sprint',
    fieldSupervised: get('supervised_by') || '\u76d1\u7ba1\u4eba',
    fieldClaimed: get('claimed_by') || '\u8ba4\u9886',
    fieldPriority: get('priority') || '\u4f18\u5148\u7ea7',
    fieldHandoff: get('handoff') || 'Handoff',
    fieldModule: get('module') || '\u529f\u80fd\u6a21\u5757',
    fieldNote: get('note') || '\u5907\u6ce8',
    fieldDefinitionOfDone:
      get('definition_of_done') || '\u9a8c\u6536\u6807\u51c6',
    fieldEffortPoints: get('effort_points') || '\u8d21\u732e\u5206',
    fieldDifficulty: get('difficulty') || '\u96be\u5ea6',
    fieldDeliveryPhase: get('delivery_phase') || '\u4ea4\u4ed8\u9636\u6bb5',
    fieldUpdateTime: get('update_time') || '\u66f4\u65b0\u65f6\u95f4',
    fieldDispatchGate: get('dispatch_gate') || '\u6d3e\u5355\u95e8\u63a7',
    fieldDispatchConfirmBy: get('dispatch_confirm_by') || '\u786e\u8ba4\u4eba',
    fieldDispatchTrigger: get('dispatch_trigger') || '\u89e3\u9501\u8bf4\u660e',
    fieldReviewPhase: get('review_phase') || '\u8bc4\u5ba1\u9636\u6bb5',
    fieldTaskType: get('task_type') || '\u4efb\u52a1\u7c7b\u578b',
    dispatchGateMap: {
      none: '\u2014',
      pending: '\u5f85\u786e\u8ba4',
      confirmed: '\u5df2\u786e\u8ba4',
      rejected: '\u5df2\u9a73\u56de',
      ...parseSimpleYamlMap(raw, 'dispatch_gate_map'),
    },
    statusMap,
    deliveryPhaseMap: {
      definition: '\u5b9a\u4e49',
      implementation: '\u5b9e\u73b0',
      crosscut: '\u6a2a\u5207',
      ...parseSimpleYamlMap(raw, 'delivery_phase_map'),
    },
    reviewPhaseMap: {
      pending_test: '\u5f85\u6d4b\u8bd5',
      pending_sign: '\u5f85\u7b7e\u6536',
      pending_business: '\u5f85\u4e1a\u52a1\u786e\u8ba4',
      blocked_by_dep: '\u88ab\u4f9d\u8d56\u963b\u585e',
      ...parseSimpleYamlMap(raw, 'review_phase_map'),
    },
    taskTypeMap: {
      feature: '\u529f\u80fd',
      definition: '\u5b9a\u4e49',
      tech_task: '\u6280\u672f\u4efb\u52a1',
      spike: '\u63a2\u9488',
      bugfix: '\u4fee\u7f3a\u9677',
      chore: '\u6742\u9879',
      ...parseSimpleYamlMap(raw, 'task_type_map'),
    },
    deliveryPhaseClassify: parseDeliveryPhaseClassify(raw),
    epicExact,
    epicPrefix,
    epicDefault,
    taskModuleMap,
    taskModulePrefix,
    rateLimitMs: 200,
    gitlabBase: 'https://gitlab.htmisoft.net',
    gitlabGroup: 'gkx-lumen',
    repo: 'gkx-orchestration',
    branch: 'dev',
    pathPrefix: 'agent-delivery',
  };
}

function resolveModule(epic, cfg, taskId = '') {
  if (taskId && cfg.taskModuleMap && cfg.taskModuleMap[taskId]) {
    return cfg.taskModuleMap[taskId];
  }
  if (epic) {
    if (cfg.epicExact[epic]) return cfg.epicExact[epic];
    let bestEpicPrefix = '';
    for (const pfx of Object.keys(cfg.epicPrefix)) {
      if (epic.startsWith(pfx) && pfx.length > bestEpicPrefix.length) {
        bestEpicPrefix = pfx;
      }
    }
    if (bestEpicPrefix) return cfg.epicPrefix[bestEpicPrefix];
  }
  let bestTaskPrefix = '';
  for (const pfx of Object.keys(cfg.taskModulePrefix || {})) {
    if (taskId.startsWith(pfx) && pfx.length > bestTaskPrefix.length) {
      bestTaskPrefix = pfx;
    }
  }
  return bestTaskPrefix
    ? cfg.taskModulePrefix[bestTaskPrefix]
    : cfg.epicDefault;
}

function parseDeliveryPhaseClassify(raw) {
  const block = raw.match(/delivery_phase_classify:\s*\r?\n((?:  .+\r?\n)+)/);
  const out = {
    default: 'crosscut',
    crosscutEpicPrefixes: ['E-PLATFORM-', 'E-PERM-'],
    crosscutIdRegex:
      '(ORCH-|PLATFORM-|PERM-|E-PLATFORM-|E-PERM-)',
    definitionIdRegex:
      '(PACK-L0|METRIC-OPEN|UX-L0|V1-HIFI|V1-FINAL|PDR-G1|G2-SIGNOFF|V2-LUMEN|V2-DEMO|DG-G3|-PDR-|HIFI-|WIREFRAME|USM-|TRACE-)',
    implementationIdRegex:
      '(IMPL-|JAVA-|FE-WIRE|FE-PERM|-API-|ALGO-ALIGN|QA-ACCEPT|DATA-PATH|DATA-IMPL|ENT-JAVA-|ENT-ARCH-API|ENT-DATA-|ENT-ALGO-)',
  };
  if (!block) return out;
  const b = block[1];
  const d = b.match(/^\s+default:\s*(\w+)/m);
  if (d) out.default = d[1];
  const cx = b.match(/^\s+crosscut_id_regex:\s*"(.*)"/m);
  if (cx) out.crosscutIdRegex = cx[1];
  const df = b.match(/^\s+definition_id_regex:\s*"(.*)"/m);
  if (df) out.definitionIdRegex = df[1];
  const im = b.match(/^\s+implementation_id_regex:\s*"(.*)"/m);
  if (im) out.implementationIdRegex = im[1];
  const pf = b.match(/^\s+crosscut_epic_prefixes:\s*\[(.*?)\]/m);
  if (pf) {
    out.crosscutEpicPrefixes = pf[1]
      .split(',')
      .map((s) => s.trim().replace(/^["']|["']$/g, ''))
      .filter(Boolean);
  }
  return out;
}

function resolveDeliveryPhaseKey(task, cfg) {
  const allowed = new Set(['definition', 'implementation', 'crosscut']);
  const explicit = (task.delivery_phase || '').trim();
  if (allowed.has(explicit)) return explicit;
  const id = task.id || '';
  const epic = task.epic || '';
  const cls = cfg.deliveryPhaseClassify || {};
  for (const pfx of cls.crosscutEpicPrefixes || []) {
    if (pfx && epic.startsWith(pfx)) return 'crosscut';
  }
  try {
    if (cls.crosscutIdRegex && new RegExp(cls.crosscutIdRegex).test(id)) {
      return 'crosscut';
    }
    if (cls.definitionIdRegex && new RegExp(cls.definitionIdRegex).test(id)) {
      return 'definition';
    }
    if (
      cls.implementationIdRegex &&
      new RegExp(cls.implementationIdRegex).test(id)
    ) {
      return 'implementation';
    }
  } catch {
    /* ignore bad regex in config */
  }
  const def = cls.default || 'crosscut';
  return allowed.has(def) ? def : 'crosscut';
}

function resolveDeliveryPhaseLabel(task, cfg) {
  const key = resolveDeliveryPhaseKey(task, cfg);
  return (
    (cfg.deliveryPhaseMap && cfg.deliveryPhaseMap[key]) ||
    ({ definition: '定义', implementation: '实现', crosscut: '横切' }[key] ||
      '横切')
  );
}

function humanDisplay(name) {
  if (!name) return '';
  const n = name.replace(/^human:/, '').trim();
  return n ? `@${n}` : '';
}

function loadOpenIdMap() {
  const map = {};
  if (!fs.existsSync(USER_MAP_PATH)) return map;
  const raw = fs.readFileSync(USER_MAP_PATH, 'utf8');
  const blocks = raw.split(/(?=\n\s*- name:)/);
  for (const b of blocks) {
    const name = (b.match(/name:\s*(.+)/) || [])[1]?.trim();
    const openId = (b.match(/feishu_open_id:\s*(\S+)/) || [])[1]?.trim();
    const reg = (b.match(/registry_name:\s*(\S+)/) || [])[1]?.trim();
    if (name && openId) {
      map[name] = openId;
      map[`human:${name}`] = openId;
    }
    if (reg && openId) map[reg] = openId;
  }
  return map;
}

function handoffUrl(evidence, cfg) {
  if (!evidence) return '';
  let p = evidence.replace(/\\/g, '/').trim();
  if (/^https?:\/\//.test(p)) return p;
  if (!p.startsWith(cfg.pathPrefix)) p = `${cfg.pathPrefix}/${p}`;
  const encoded = p
    .split('/')
    .map((s) => encodeURIComponent(s))
    .join('/');
  return `${cfg.gitlabBase}/${cfg.gitlabGroup}/${cfg.repo}/-/blob/${cfg.branch}/${encoded}?ref_type=heads`;
}

async function feishuToken(appId, appSecret) {
  const resp = await fetch(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
    },
  );
  const data = await resp.json();
  if (data.code !== 0 || !data.tenant_access_token) {
    throw new Error(`tenant_access_token failed: ${JSON.stringify(data)}`);
  }
  return data.tenant_access_token;
}

async function feishuApi(method, apiPath, token, body) {
  const resp = await fetch(`https://open.feishu.cn/open-apis${apiPath}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await resp.json();
  if (data.code !== 0) {
    throw new Error(`Feishu ${method} ${apiPath}: code=${data.code} msg=${data.msg}`);
  }
  return data;
}

async function searchRecord(cfg, token, taskId) {
  const data = await feishuApi(
    'POST',
    `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/records/search`,
    token,
    {
      filter: {
        conjunction: 'and',
        conditions: [
          {
            field_name: cfg.fieldTaskId,
            operator: 'is',
            value: [taskId],
          },
        ],
      },
      page_size: 5,
    },
  );
  const items = data.data?.items || [];
  return items[0]?.record_id || '';
}

function buildFields(task, cfg, openIdMap, opts = {}) {
  const skipKanban = opts.skipKanbanFields && task.record_id;
  const statusLabel = cfg.statusMap[task.status] || task.status;
  const fields = {};
  if (!skipKanban) {
    fields[cfg.fieldTaskId] = task.id;
    fields[cfg.fieldTitle] = task.title || task.id;
    fields[cfg.fieldStatus] = statusLabel;
  } else {
    fields[cfg.fieldTaskId] = task.id;
  }
  if (task.agent) fields[cfg.fieldAgent] = task.agent;
  if (task.epic) fields[cfg.fieldEpic] = task.epic;
  const moduleLabel = resolveModule(task.epic, cfg, task.id);
  if (moduleLabel) fields[cfg.fieldModule] = moduleLabel;
  if (!skipKanban && task.sprint_id) fields[cfg.fieldSprint] = task.sprint_id;
  if (!skipKanban && task.priority) fields[cfg.fieldPriority] = task.priority;
  if (task.supervised_by) {
    fields[cfg.fieldSupervised] = humanDisplay(task.supervised_by);
  }
  if (!skipKanban) {
    if (task.claimed_by) {
      const oid =
        openIdMap[task.claimed_by] ||
        openIdMap[task.claimed_by.replace(/^human:/, '')];
      if (oid) fields[cfg.fieldClaimed] = [{ id: oid }];
      else if (String(task.claimed_by).startsWith('agent:')) {
        // agent 认领：人员列无法映射时留空（避免脏数据）
        fields[cfg.fieldClaimed] = null;
      }
    } else if (task.record_id) {
      // lease 回收 / ready：清空飞书「认领」，避免 inbound 把旧认领写回 registry
      fields[cfg.fieldClaimed] = null;
    }
  }
  if (task.evidence) {
    fields[cfg.fieldHandoff] = handoffUrl(task.evidence, cfg);
  }
  if (task.note && cfg.fieldNote) {
    fields[cfg.fieldNote] = String(task.note);
  }
  if (task.definition_of_done && cfg.fieldDefinitionOfDone) {
    fields[cfg.fieldDefinitionOfDone] = String(task.definition_of_done);
  }
  if (task.user_story && cfg.fieldUserStory) {
    fields[cfg.fieldUserStory] = String(task.user_story);
  }
  if (task.effort_points && cfg.fieldEffortPoints) {
    const ep = Number(String(task.effort_points).replace(/_/g, ''));
    if (Number.isFinite(ep)) fields[cfg.fieldEffortPoints] = ep;
  }
  if (task.difficulty && cfg.fieldDifficulty) {
    fields[cfg.fieldDifficulty] = String(task.difficulty);
  }
  if (cfg.fieldDeliveryPhase) {
    fields[cfg.fieldDeliveryPhase] = resolveDeliveryPhaseLabel(task, cfg);
  }
  if (cfg.fieldTaskType && task.task_type) {
    fields[cfg.fieldTaskType] = cfg.taskTypeMap[task.task_type] || task.task_type;
  }
  // review_phase 列已废弃（pending_test/testing 升级为独立 status）。
  // 飞书列保留但不再回填，避免历史数据丢失。
  if (task.update_time && cfg.fieldUpdateTime) {
    const ms = Date.parse(task.update_time);
    if (Number.isFinite(ms)) fields[cfg.fieldUpdateTime] = ms;
  }
  if (opts.dispatchGate && cfg.fieldDispatchGate) {
    const label = cfg.dispatchGateMap?.[opts.dispatchGate] || opts.dispatchGate;
    fields[cfg.fieldDispatchGate] = label;
  }
  if (opts.dispatchConfirmBy && cfg.fieldDispatchConfirmBy) {
    fields[cfg.fieldDispatchConfirmBy] = humanDisplay(opts.dispatchConfirmBy);
  }
  if (opts.dispatchTrigger && cfg.fieldDispatchTrigger) {
    fields[cfg.fieldDispatchTrigger] = String(opts.dispatchTrigger);
  }
  return fields;
}

function parseTaskSnapshot(blockLines) {
  const get = (k) => getField(blockLines, k);
  return {
    id:
      get('id') ||
      (blockLines[0].match(/id:\s*(.+)/) || [])[1]
        ?.trim()
        .replace(/^["']|["']$/g, ''),
    title: get('title'),
    user_story: get('user_story'),
    status: get('status'),
    agent: get('agent'),
    epic: get('epic'),
    sprint_id: get('sprint_id'),
    supervised_by: get('supervised_by'),
    claimed_by: get('claimed_by'),
    priority: get('priority'),
    evidence: get('evidence'),
    note: getMultilineField(blockLines, 'note'),
    definition_of_done: getListField(blockLines, 'definition_of_done'),
    effort_points: get('effort_points'),
    difficulty: get('difficulty'),
    delivery_phase: get('delivery_phase'),
    update_time: get('update_time'),
    record_id: get('feishu_bitable_record_id'),
    blocked_by: get('blocked_by'),
    review_phase: get('review_phase'),
    task_type: get('task_type'),
  };
}

async function ensureTextColumns(cfg, token, dryRun) {
  const wanted = [
    { name: cfg.fieldUserStory, type: 1 },
    { name: cfg.fieldNote, type: 1 },
    { name: cfg.fieldDefinitionOfDone, type: 1 },
    { name: cfg.fieldEffortPoints, type: 2 },
    { name: cfg.fieldDifficulty, type: 1 },
    { name: cfg.fieldDeliveryPhase, type: 1 },
    {
      name: cfg.fieldUpdateTime,
      type: 5,
      property: { date_formatter: 'yyyy/MM/dd HH:mm' },
    },
    { name: cfg.fieldDispatchGate, type: 1 },
    { name: cfg.fieldDispatchConfirmBy, type: 1 },
    { name: cfg.fieldDispatchTrigger, type: 1 },
    {
      name: cfg.fieldTaskType,
      type: 3,
      property: {
        options: Object.entries(cfg.taskTypeMap).map(([_, label]) => ({ name: label })),
      },
    },
    // review_phase 列已废弃，不再自动创建
  ].filter((c) => c.name);
  if (!wanted.length) return;
  const listed = await feishuApi(
    'GET',
    `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/fields`,
    token,
  );
  const existing = new Set(
    (listed.data?.items || []).map((f) => f.field_name).filter(Boolean),
  );
  for (const col of wanted) {
    if (existing.has(col.name)) continue;
    const typeLabel =
      col.type === 2 ? 'number' : col.type === 3 ? 'single-select'
      : col.type === 5 ? 'datetime' : 'text';
    if (dryRun) {
      console.log(`[DRY] would create ${typeLabel} column: ${col.name}`);
      continue;
    }
    try {
      const body = { field_name: col.name, type: col.type };
      if (col.property) body.property = col.property;
      await feishuApi(
        'POST',
        `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/fields`,
        token,
        body,
      );
      console.log(`  CREATE column [${col.name}] (${typeLabel})`);
      existing.add(col.name);
    } catch (e) {
      console.warn(
        `[WARN] create column [${col.name}] failed: ${e.message}. Create manually.`,
      );
    }
  }
}

async function syncOneTask(task, cfg, dryRun, syncOpts = {}) {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn(
      '[WARN] FEISHU_APP_ID/SECRET missing ? YAML updated; board not synced (projector will catch up)',
    );
    return { ok: false, soft: true, reason: 'missing_credentials' };
  }
  if (!cfg.appToken || !cfg.tableId) {
    console.warn('[WARN] feishu-bitable.yaml missing app_token/table_id ? skip board sync');
    return { ok: false, soft: true, reason: 'missing_config' };
  }

  const token = await feishuToken(appId, appSecret);
  await ensureTextColumns(cfg, token, dryRun);
  const openIdMap = loadOpenIdMap();
  const dispatchOpts = {
    skipKanbanFields: syncOpts.skipKanbanFields,
    dispatchGate: syncOpts.dispatchGate,
    dispatchConfirmBy: syncOpts.dispatchConfirmBy,
    dispatchTrigger: syncOpts.dispatchTrigger,
  };
  const fields = buildFields(task, cfg, openIdMap, dispatchOpts);
  let recordId = task.record_id;
  if (!recordId) recordId = await searchRecord(cfg, token, task.id);

  if (dryRun) {
    console.log(
      `[DRY] board ${recordId ? 'UPDATE ' + recordId : 'CREATE'} | ${task.status} | ${fields[cfg.fieldModule] || cfg.epicDefault} | ${task.id}`,
    );
    return { ok: true, dryRun: true, recordId };
  }

  if (recordId) {
    try {
      await feishuApi(
        'PUT',
        `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/records/${recordId}`,
        token,
        { fields },
      );
      console.log(`  BOARD UPDATE ${recordId} | ${task.id}`);
      return { ok: true, recordId };
    } catch (e) {
      if (!String(e.message).includes('RecordIdNotFound')) throw e;
      console.warn(
        `[WARN] stale record_id ${recordId} for ${task.id}; resolving by Task ID`,
      );
      recordId = await searchRecord(cfg, token, task.id);
      if (recordId) {
        await feishuApi(
          'PUT',
          `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/records/${recordId}`,
          token,
          { fields },
        );
        console.log(`  BOARD UPDATE ${recordId} | ${task.id}`);
        return { ok: true, recordId };
      }
    }
  }
  const created = await feishuApi(
    'POST',
    `/bitable/v1/apps/${cfg.appToken}/tables/${cfg.tableId}/records`,
    token,
    { fields },
  );
  recordId = created.data?.record?.record_id || '';
  console.log(`  BOARD CREATE ${recordId} | ${task.id}`);
  return { ok: true, recordId };
}

function updateRegistry(opts) {
  const text = fs.readFileSync(REGISTRY_PATH, 'utf8');
  const lines = text.split(/\r?\n/);
  const loc = findTaskBlock(lines, opts.taskId);
  if (!loc) throw new Error(`Task not found in registry: ${opts.taskId}`);

  const block = lines.slice(loc.start, loc.end);
  const before = parseTaskSnapshot(block);
  const oldStatus = before.status;

  if (opts.status) {
    if (!VALID_STATUSES.has(opts.status)) {
      throw new Error(`Invalid status: ${opts.status}`);
    }
    warnTransition(oldStatus, opts.status);
    upsertField(block, 'status', opts.status);
  }
  if (opts.claimedBy) upsertField(block, 'claimed_by', opts.claimedBy);
  if (opts.supervisedBy) upsertField(block, 'supervised_by', opts.supervisedBy);
  if (opts.blockedBy) upsertField(block, 'blocked_by', opts.blockedBy);
  if (opts.evidence) upsertField(block, 'evidence', opts.evidence);

  if (opts.heartbeat || opts.status === 'claimed' || opts.status === 'in_progress') {
    const until = new Date(Date.now() + opts.lockHours * 3600 * 1000).toISOString();
    upsertField(block, 'lock_until', until);
    upsertField(block, 'last_seen_at', new Date().toISOString());
  }

  // Any registry mutation bumps update_time (Feishu sortable clock)
  touchUpdateTime(block);

  const after = parseTaskSnapshot(block);

  if (opts.dryRun) {
    console.log(
      `[DRY] registry ${opts.taskId}: ${oldStatus || '?'} ? ${after.status || oldStatus}`,
    );
    return { before, after, changed: false };
  }

  const newLines = [...lines.slice(0, loc.start), ...block, ...lines.slice(loc.end)];
  const out = newLines.join('\n');
  fs.writeFileSync(REGISTRY_PATH, out.endsWith('\n') ? out : `${out}\n`, 'utf8');
  console.log(
    `REGISTRY ${opts.taskId}: ${oldStatus || '?'} ? ${after.status || oldStatus || '(heartbeat)'}`,
  );
  return { before, after, changed: true };
}

function listSprintTasks(sprintId) {
  const text = fs.readFileSync(REGISTRY_PATH, 'utf8');
  const lines = text.split(/\r?\n/);
  const tasks = [];
  let inTasks = false;
  let cur = null;
  let curLines = null;
  const flush = (end) => {
    if (!cur || !curLines) return;
    const snap = parseTaskSnapshot(curLines);
    Object.assign(cur, snap, { start: cur.start, end });
    if (!sprintId || cur.sprint_id === sprintId) tasks.push(cur);
  };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^tasks:\s*$/.test(line)) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    const idMatch = line.match(/^\s+- id:\s*(.+)\s*$/);
    if (idMatch) {
      flush(i);
      cur = {
        id: idMatch[1].trim().replace(/^["']|["']$/g, ''),
        start: i,
        end: -1,
      };
      curLines = [line];
    } else if (cur) {
      curLines.push(line);
    }
  }
  flush(lines.length);
  return tasks;
}

function appendLog(msg) {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(LOG_PATH, `[${new Date().toISOString()}] ${msg}\n`, 'utf8');
  } catch {
    /* ignore */
  }
}

async function watchOutbound(sprintId, dryRun, syncOpts = {}) {
  const only = Array.isArray(syncOpts.onlyTaskIds) ? syncOpts.onlyTaskIds : [];
  // --only-task-ids / --all-sprints：跨 Sprint；否则默认 current_sprint
  let sid = '';
  if (only.length || syncOpts.allSprints) sid = '';
  else sid = sprintId || readCurrentSprint();
  const cfg = loadBitableConfig();
  // Project all valid kanban-visible statuses (excludes internal-only 'needs-revision').
  const KANBAN_STATUSES = [...VALID_STATUSES].filter((s) => s !== 'needs-revision');
  let tasks = listSprintTasks(sid).filter((t) =>
    only.length && syncOpts.skipKanbanFields
      ? VALID_STATUSES.has(t.status)
      : KANBAN_STATUSES.includes(t.status),
  );
  if (only.length) {
    const want = new Set(only);
    tasks = tasks.filter((t) => want.has(t.id));
    const missing = only.filter((id) => !tasks.some((t) => t.id === id));
    if (missing.length) {
      console.warn(`[WARN] only-task-ids not found in filter: ${missing.join(', ')}`);
    }
  }
  const skipHint = syncOpts.skipKanbanFields ? ' skipKanban=ON' : '';
  const onlyHint = only.length ? ` only=${only.length}` : '';
  console.log(
    `Watch outbound: ${tasks.length} task(s) sprint=${sid || '(all)'} dryRun=${dryRun}${skipHint}${onlyHint}`,
  );
  appendLog(
    `watch-outbound start sprint=${sid} count=${tasks.length}${skipHint}${onlyHint}`,
  );
  let ok = 0;
  let fail = 0;
  for (const t of tasks) {
    try {
      const r = await syncOneTask(t, cfg, dryRun, syncOpts);
      if (r.ok || r.soft) ok++;
      else fail++;
      // CREATE 后回写 feishu_bitable_record_id（新任务本无该字段）
      if (
        !dryRun &&
        r.ok &&
        r.recordId &&
        !t.record_id &&
        r.recordId !== t.record_id
      ) {
        try {
          const text = fs.readFileSync(REGISTRY_PATH, 'utf8');
          const lines = text.split(/\r?\n/);
          const loc = findTaskBlock(lines, t.id);
          if (loc) {
            const block = lines.slice(loc.start, loc.end);
            upsertField(block, 'feishu_bitable_record_id', r.recordId);
            touchUpdateTime(block);
            const newLines = [
              ...lines.slice(0, loc.start),
              ...block,
              ...lines.slice(loc.end),
            ];
            const out = newLines.join('\n');
            fs.writeFileSync(
              REGISTRY_PATH,
              out.endsWith('\n') ? out : `${out}\n`,
              'utf8',
            );
            t.record_id = r.recordId;
            console.log(`  REGISTRY record_id ← ${r.recordId} | ${t.id}`);
          }
        } catch (e) {
          console.warn(
            `[WARN] backfill record_id ${t.id}: ${e.message}`,
          );
        }
      }
      await new Promise((r) => setTimeout(r, cfg.rateLimitMs));
    } catch (e) {
      fail++;
      console.warn(`[WARN] sync ${t.id}: ${e.message}`);
      appendLog(`ERROR ${t.id}: ${e.message}`);
    }
  }
  appendLog(`watch-outbound done ok=${ok} fail=${fail}`);
  console.log(`Done. ok=${ok} fail=${fail}`);
  return fail === 0 ? 0 : 1;
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    usage();
    process.exit(0);
  }

  if (opts.watchOutbound) {
    const code = await watchOutbound(opts.sprintId, opts.dryRun, {
      skipKanbanFields: opts.skipKanbanFields,
      onlyTaskIds: opts.onlyTaskIds,
      allSprints: opts.allSprints,
    });
    process.exit(code);
  }

  if (opts.dispatchOnly) {
    if (!opts.taskId) {
      console.error('dispatch-only requires --task-id');
      process.exit(2);
    }
    const text = fs.readFileSync(REGISTRY_PATH, 'utf8');
    const lines = text.split(/\r?\n/);
    const loc = findTaskBlock(lines, opts.taskId);
    if (!loc) throw new Error(`Task not found in registry: ${opts.taskId}`);
    const task = parseTaskSnapshot(lines.slice(loc.start, loc.end));
    try {
      const cfg = loadBitableConfig();
      await syncOneTask(task, cfg, opts.dryRun, {
        skipKanbanFields: true,
        dispatchGate: opts.dispatchGate,
        dispatchConfirmBy: opts.dispatchConfirmBy,
        dispatchTrigger: opts.dispatchTrigger,
      });
    } catch (e) {
      console.warn(`[WARN] dispatch-only sync soft-fail: ${e.message}`);
    }
    return;
  }

  if (!opts.taskId) {
    usage();
    process.exit(2);
  }
  if (!opts.status && !opts.heartbeat) {
    console.error('Require --status or --heartbeat');
    process.exit(2);
  }

  const result = updateRegistry(opts);
  const task = result.after;

  if (opts.syncBoard) {
    try {
      const cfg = loadBitableConfig();
      const syncResult = await syncOneTask(task, cfg, opts.dryRun, {
        dispatchGate: opts.dispatchGate,
        dispatchConfirmBy: opts.dispatchConfirmBy,
        dispatchTrigger: opts.dispatchTrigger,
      });
      if (
        syncResult.ok &&
        syncResult.recordId &&
        !opts.dryRun &&
        syncResult.recordId !== result.before.record_id
      ) {
        const text = fs.readFileSync(REGISTRY_PATH, 'utf8');
        const lines = text.split(/\r?\n/);
        const loc = findTaskBlock(lines, opts.taskId);
        if (loc) {
          const block = lines.slice(loc.start, loc.end);
          upsertField(block, 'feishu_bitable_record_id', syncResult.recordId);
          touchUpdateTime(block);
          const newLines = [...lines.slice(0, loc.start), ...block, ...lines.slice(loc.end)];
          const out = newLines.join('\n');
          fs.writeFileSync(REGISTRY_PATH, out.endsWith('\n') ? out : `${out}\n`, 'utf8');
        }
      }
    } catch (e) {
      console.warn(`[WARN] board sync soft-fail: ${e.message}`);
      console.warn('        YAML is updated; projector / next watch will retry.');
      appendLog(`soft-fail ${opts.taskId}: ${e.message}`);
    }
  } else {
    console.log('Board sync skipped (--no-sync)');
  }

  if (opts.status === 'done' && !opts.dryRun) {
    try {
      const dispatchScript = path.join(ORCH_ROOT, 'scripts', 'coordinator-dispatch.mjs');
      if (fs.existsSync(dispatchScript)) {
        const r = spawnSync(
          process.execPath,
          [dispatchScript, 'scan', '--cause-task', opts.taskId],
          { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env },
        );
        if (r.stdout) console.log(r.stdout.trim());
        if (r.status !== 0 && r.stderr) {
          console.warn(`[WARN] coordinator-dispatch scan: ${r.stderr.trim()}`);
        }
      }
    } catch (e) {
      console.warn(`[WARN] coordinator-dispatch scan soft-fail: ${e.message}`);
    }
  }
}

const __boardMain =
  process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (__boardMain) {
  main().catch((e) => {
    console.error(e.message || e);
    process.exit(1);
  });
}

export { syncOneTask, loadBitableConfig };
