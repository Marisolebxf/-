#!/usr/bin/env node
/**
 * task-mcp-server.mjs — MCP Server for task-registry.yaml
 *
 * Exposes tools for querying, creating, claiming, and updating tasks
 * without AI reading the YAML file directly.
 *
 * Protocol: MCP stdio (JSON-RPC 2.0)
 * Usage: Configure in .cursor/mcp.json:
 *   {
 *     "mcpServers": {
 *       "task-registry": {
 *         "type": "stdio",
 *         "command": "node",
 *         "args": ["scripts/task-mcp-server.mjs"]
 *       }
 *     }
 *   }
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  REGISTRY_PATH,
  readRegistryText,
  findTaskBlock,
  findTaskBlocks,
  parseTaskBlock,
  createTask,
  updateTaskFields,
  loadAllTasks,
  getScalar,
  getListField,
  isDoneStatus,
  VALID_STATUSES,
  checkTransitionGate,
  SIGN_OFF_BY,
  TASK_TYPES,
} from './lib/task-registry-lib.mjs';
import { runReview, runAutoVerify } from './review-check.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

// ── File Lock (mkdir-based, atomic on all platforms) ──────────────

const LOCK_PATH = REGISTRY_PATH + '.lock';
const LOCK_RETRY_MS = 100;
const LOCK_TIMEOUT_MS = 5000;

function acquireLock() {
  const deadline = Date.now() + LOCK_TIMEOUT_MS;
  while (Date.now() < deadline) {
    try {
      fs.mkdirSync(LOCK_PATH);
      return;
    } catch {
      // Another process holds the lock; wait and retry
      const ms = Math.min(LOCK_RETRY_MS, deadline - Date.now());
      if (ms <= 0) break;
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
    }
  }
  throw new Error(`File lock timeout: ${LOCK_PATH}`);
}

function releaseLock() {
  try {
    fs.rmdirSync(LOCK_PATH);
  } catch {
    // Best effort
  }
}

// ── Epic Name Mapping (for fuzzy module search) ───────────────────

const EPIC_NAME_MAP = buildEpicNameMap();

function buildEpicNameMap() {
  // Extracted from task-registry.yaml by_epic section + known epic IDs
  const map = {};
  try {
    const text = readRegistryText();
    // Parse the by_epic section
    const m = text.match(/by_epic:\s*\r?\n([\s\S]*?)(?:\n\S|\s{2,}[a-z]|$)/);
    if (m) {
      for (const line of m[1].split('\n')) {
        const kv = line.match(/^\s{4}(\S+):/);
        if (kv) map[kv[1]] = kv[1];
      }
    }
  } catch {
    // Fallback: use known epic codes
  }
  // Known Chinese name mappings (extend as needed)
  const NAME_MAP = {
    'E-INNOV-M1':       '创新监测',
    'E-PLATFORM-P0':    '平台基建',
    'E-PLATFORM-P1':    '平台基建',
    'E-E7-POLICY-M1':   '政策要素',
    'E-ENT-PROTOTYPE':  '企业原型',
    'E-ENT-SCRUM-PDR':  '企业Scrum',
    'E-TECH-NEWS-IE-M1':'科技资讯',
    'E-TECH-NEWS-ENTITY': '科技资讯实体',
    'E-PERM':           '权限改造',
    'E-PROD-UXUE-COMP': '通用交互组件',
  };
  for (const [k, v] of Object.entries(NAME_MAP)) {
    if (map[k]) map[k] = v;
  }
  return map;
}

function taskMatchesModule(task, keyword) {
  if (!keyword) return true;
  const kw = keyword.toLowerCase();
  // Match epic name
  const epicName = EPIC_NAME_MAP[task.epic] || task.epic || '';
  if (epicName.toLowerCase().includes(kw)) return true;
  // Match task title
  if ((task.title || '').toLowerCase().includes(kw)) return true;
  // Match task id
  if ((task.id || '').toLowerCase().includes(kw)) return true;
  return false;
}

// ── Task field helpers ────────────────────────────────────────────

const SUMMARY_FIELDS = ['id', 'title', 'status', 'agent', 'epic', 'priority', 'sprint_id'];
const EXTRA_FIELDS = [
  'supervised_by', 'claimed_by', 'blocked_by', 'repo', 'delivery_phase',
  'subcoord', 'lock_until', 'update_time', 'estimated_tokens', 'note',
  'difficulty', 'effort_points', 'depends_on', 'definition_of_done',
  'user_story', 'task_type', 'graph_role', 'ods_dependency_phase',
  'collaborators', 'touched_files', 'design_refs',
];

function pickFields(task, mode) {
  const out = {};
  const fields = mode === 'full' ? [...SUMMARY_FIELDS, ...EXTRA_FIELDS] : SUMMARY_FIELDS;
  for (const f of fields) {
    const v = task[f];
    if (v !== undefined && v !== null && v !== '' &&
        !(Array.isArray(v) && v.length === 0)) {
      out[f] = v;
    }
  }
  return out;
}

// ── MCP Protocol Implementation ───────────────────────────────────

const MCPServer = {
  name: 'task-registry-mcp',
  version: '1.1.0',
};

function jsonRpcError(id, code, message) {
  return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
}

function jsonRpcResult(id, result) {
  return JSON.stringify({ jsonrpc: '2.0', id, result });
}

function jsonRpcNotification(method, params) {
  return JSON.stringify({ jsonrpc: '2.0', method, params });
}

// ── Tool Handlers ─────────────────────────────────────────────────

const TOOLS = {};

// ──── 1. task-query ────

TOOLS['task-query'] = {
  description: '查询任务列表，支持按模块名模糊搜索、按状态/Agent/Epic 筛选',
  inputSchema: {
    type: 'object',
    properties: {
      module:    { type: 'string',  description: '模块名模糊搜索（如"企业"匹配所有企业相关任务）' },
      status:    { type: 'string',  description: '按状态筛选（backlog/ready/claimed/in_progress/testing/ready_to_sign/review/done/blocked/needs-revision）' },
      agent:     { type: 'string',  description: '按 Agent 角色筛选（如 api-agent/frontend-agent）' },
      epic:      { type: 'string',  description: '按 Epic 精确匹配（如 E-ENT-PROTOTYPE）' },
      sprint:    { type: 'string',  description: '按 Sprint ID 筛选' },
      limit:     { type: 'number',  description: '最大返回条数（默认 20）', default: 20 },
      fields:    { type: 'string',  description: '返回字段模式: summary（默认，精简）| full（完整）', enum: ['summary', 'full'] },
    },
  },
  async handler(args) {
    const { module, status, agent, epic, sprint, limit = 20, fields = 'summary' } = args || {};
    const { byId } = loadAllTasks();
    let results = [];

    for (const task of byId.values()) {
      if (module && !taskMatchesModule(task, module)) continue;
      if (status && task.status !== status) continue;
      if (agent && task.agent !== agent) continue;
      if (epic && task.epic !== epic) continue;
      if (sprint && task.sprint_id !== sprint) continue;
      results.push(pickFields(task, fields));
    }

    // Sort by epic + priority for consistent ordering
    results.sort((a, b) => {
      const ep = (a.epic || '').localeCompare(b.epic || '');
      if (ep !== 0) return ep;
      const pa = a.priority ? Number(a.priority) : 999;
      const pb = b.priority ? Number(b.priority) : 999;
      return pa - pb;
    });

    if (limit > 0) results = results.slice(0, limit);

    const total = byId.size;
    const matched = byId.size; // Recalculate
    let matchedCount = 0;
    for (const _ of byId.values()) {
      if (module && !taskMatchesModule(_, module)) continue;
      if (status && _.status !== status) continue;
      if (agent && _.agent !== agent) continue;
      if (epic && _.epic !== epic) continue;
      if (sprint && _.sprint_id !== sprint) continue;
      matchedCount++;
    }

    const text = JSON.stringify({
      total_in_registry: total,
      matched: matchedCount,
      returned: results.length,
      tasks: results,
    }, null, 2);

    return { content: [{ type: 'text', text }] };
  },
};

// ──── 2. task-get ────

TOOLS['task-get'] = {
  description: '按 ID 查询单个任务的完整信息',
  inputSchema: {
    type: 'object',
    properties: {
      id: { type: 'string', description: '任务 ID（如 E-INNOV-M1-L03）' },
    },
    required: ['id'],
  },
  async handler(args) {
    const { id } = args || {};
    const { byId } = loadAllTasks();
    const task = byId.get(id);
    if (!task) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Task not found: ${id}` }, null, 2) }] };
    }
    return { content: [{ type: 'text', text: JSON.stringify(pickFields(task, 'full'), null, 2) }] };
  },
};

// ──── 3. task-create ────

TOOLS['task-create'] = {
  description: '创建新任务；校验必填字段、重复 ID、依赖与 ready 门禁',
  inputSchema: {
    type: 'object',
    properties: {
      id:                   { type: 'string', description: '全局唯一任务 ID' },
      title:                { type: 'string', description: '任务标题' },
      status:               { type: 'string', description: '初始状态（默认 backlog）', enum: ['backlog', 'ready'], default: 'backlog' },
      agent:                { type: 'string', description: '执行 Agent 角色（如 data-agent）' },
      epic:                 { type: 'string', description: '所属 Epic' },
      priority:             { type: 'string', description: '优先级（如 P0/P1）' },
      sprint_id:            { type: 'string', description: 'Sprint ID（可选）' },
      repo:                 { type: 'string', description: '交付仓或编排资产名' },
      delivery_phase:       { type: 'string', description: '交付阶段', enum: ['definition', 'implementation', 'crosscut'] },
      task_type:            { type: 'string', description: '任务类型', enum: [...TASK_TYPES] },
      subcoord:             { type: 'string', description: '子协调域（可选）' },
      graph_role:           { type: 'string', description: 'Graph Engineering 角色（可选）' },
      ods_dependency_phase: { type: 'string', description: 'ODS 依赖阶段（可选）' },
      effort_points:        { type: 'string', description: '贡献分', enum: ['1', '2', '3', '5', '8', '13'] },
      difficulty:           { type: 'string', description: '难度', enum: ['S', 'M', 'L', 'XL'] },
      estimated_tokens:     { type: 'number', description: '预计 token 消耗' },
      user_story:           { type: 'string', description: '用户故事库 ID 引用（可选）' },
      depends_on:           { type: 'array', description: '前置任务 ID 列表', items: { type: 'string' } },
      collaborators:        { type: 'array', description: '协作 Agent 列表（可选）', items: { type: 'string' } },
      touched_files:        { type: 'array', description: '预计触碰文件列表（可选）', items: { type: 'string' } },
      design_refs:          { type: 'array', description: '设计/规约引用（可选）', items: { type: 'string' } },
      definition_of_done:   { type: 'array', description: '可验收 DoD，至少一项', minItems: 1, items: { type: 'string' } },
      note:                 { type: 'string', description: '建单背景或约束（可选）' },
    },
    required: [
      'id', 'title', 'agent', 'epic', 'repo', 'delivery_phase', 'task_type',
      'effort_points', 'difficulty', 'estimated_tokens', 'definition_of_done',
    ],
  },
  async handler(args) {
    const task = { ...(args || {}), status: args?.status || 'backlog' };
    const requiredStrings = ['id', 'title', 'agent', 'epic', 'repo', 'delivery_phase', 'task_type', 'difficulty'];
    const missing = requiredStrings.filter((key) => !String(task[key] || '').trim());
    if (missing.length > 0) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Missing required fields: ${missing.join(', ')}` }, null, 2) }] };
    }
    if (!/^[A-Z0-9][A-Z0-9._-]*$/.test(task.id)) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'Invalid task id: use uppercase letters, digits, dot, underscore, or hyphen' }, null, 2) }] };
    }
    if (!['backlog', 'ready'].includes(task.status)) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'Initial status must be backlog or ready' }, null, 2) }] };
    }
    if (!TASK_TYPES.has(task.task_type)) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Invalid task_type: ${task.task_type}` }, null, 2) }] };
    }
    if (!['1', '2', '3', '5', '8', '13'].includes(String(task.effort_points))) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'effort_points must be one of 1/2/3/5/8/13' }, null, 2) }] };
    }
    if (!Number.isFinite(task.estimated_tokens) || task.estimated_tokens < 0) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'estimated_tokens must be a non-negative number' }, null, 2) }] };
    }
    if (!Array.isArray(task.definition_of_done) || task.definition_of_done.length === 0) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'definition_of_done must contain at least one item' }, null, 2) }] };
    }

    acquireLock();
    try {
      const { byId } = loadAllTasks();
      if (byId.has(task.id)) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: `Task already exists: ${task.id}` }, null, 2) }] };
      }
      const dependencies = Array.isArray(task.depends_on) ? task.depends_on : [];
      const missingDeps = dependencies.filter((id) => !byId.has(id));
      if (missingDeps.length > 0) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: 'Dependencies not found', missing_dependencies: missingDeps }, null, 2) }] };
      }
      if (task.status === 'ready') {
        const unfinished = dependencies.filter((id) => !isDoneStatus(byId.get(id)?.status));
        if (unfinished.length > 0) {
          return { content: [{ type: 'text', text: JSON.stringify({ error: 'READY_GATE_DENIED', unfinished_dependencies: unfinished }, null, 2) }] };
        }
      }

      const result = createTask(task);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            id: result.task.id,
            title: result.task.title,
            status: result.task.status,
            created: result.changed,
          }, null, 2),
        }],
      };
    } finally {
      releaseLock();
    }
  },
};

// ──── 4. task-summary ────

TOOLS['task-summary'] = {
  description: '任务概览：按状态/Epic/Agent 聚合统计，不返回具体任务',
  inputSchema: {
    type: 'object',
    properties: {
      module: { type: 'string', description: '可选：仅统计某模块（如"企业"）' },
    },
  },
  async handler(args) {
    const { module } = args || {};
    const { byId } = loadAllTasks();

    const byStatus = {};
    const byEpic = {};
    const byAgent = {};
    let total = 0;

    for (const task of byId.values()) {
      if (module && !taskMatchesModule(task, module)) continue;
      total++;

      byStatus[task.status || 'unknown'] = (byStatus[task.status || 'unknown'] || 0) + 1;
      byEpic[task.epic || 'unknown'] = (byEpic[task.epic || 'unknown'] || 0) + 1;
      byAgent[task.agent || 'unknown'] = (byAgent[task.agent || 'unknown'] || 0) + 1;
    }

    // Build ready list (for coordinator) + pending_test list (for QA)
    const readyTasks = [];
    const pendingTestTasks = [];
    for (const task of byId.values()) {
      if (module && !taskMatchesModule(task, module)) continue;
      if (task.status === 'ready' && !task.claimed_by) {
        readyTasks.push({ id: task.id, title: task.title, agent: task.agent, epic: task.epic });
      }
      if (task.status === 'pending_test') {
        pendingTestTasks.push({ id: task.id, title: task.title, agent: task.agent, supervised_by: task.supervised_by, delivery_phase: task.delivery_phase });
      }
    }

    const text = JSON.stringify({
      total,
      filter_module: module || null,
      by_status: byStatus,
      by_epic: byEpic,
      by_agent: byAgent,
      ready_to_claim: readyTasks.length,
      ready_list: readyTasks.slice(0, 30),
      pending_test_count: pendingTestTasks.length,
      pending_test_list: pendingTestTasks.slice(0, 30),
    }, null, 2);

    return { content: [{ type: 'text', text }] };
  },
};

// ──── 4. task-update-status ────
// VALID_STATUSES is imported from task-registry-lib.mjs (single source of truth).

TOOLS['task-update-status'] = {
  description: '更新任务状态（backlog→ready→claimed→in_progress→pending_test→testing→ready_to_sign→done）',
  inputSchema: {
    type: 'object',
    properties: {
      id:     { type: 'string', description: '任务 ID' },
      status: { type: 'string', description: '新状态', enum: [...VALID_STATUSES] },
      note:   { type: 'string', description: '备注（可选，会追加到 note 字段）' },
      actor:  { type: 'string', description: '操作人（如 human:淮政玮 / agent:qa-agent），用于闸门校验' },
    },
    required: ['id', 'status'],
  },
  async handler(args) {
    const { id, status, note, actor } = args || {};
    if (!VALID_STATUSES.has(status)) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Invalid status: ${status}. Valid: ${[...VALID_STATUSES].join(', ')}` }, null, 2) }] };
    }

    // 读取当前任务，用于闸门校验
    const { byId } = loadAllTasks();
    const task = byId.get(id);
    if (!task) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: `Task not found: ${id}` }, null, 2) }] };
    }

    // 解析 actor
    const actorInfo = actor ? { human: actor, agent: actor, supervised_by: task.supervised_by } : { supervised_by: task.supervised_by };

    // 闸门校验
    const gate = checkTransitionGate(task.status, status, task, actorInfo);
    if (!gate.ok) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'GATE_DENIED', reason: gate.reason, from: task.status, to: status }, null, 2) }] };
    }

    const patch = { status };
    if (note) patch.note = note;

    acquireLock();
    try {
      const result = updateTaskFields(id, patch);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ id, old_status: result.before.status, new_status: result.after.status, changed: result.changed }, null, 2),
        }],
      };
    } finally {
      releaseLock();
    }
  },
};

// ──── 5. task-claim ────

TOOLS['task-claim'] = {
  description: '认领任务（设置 claimed_by + supervised_by + lock_until）',
  inputSchema: {
    type: 'object',
    properties: {
      id:            { type: 'string', description: '任务 ID' },
      claimed_by:    { type: 'string', description: '认领人（如 human:侯佳伟）' },
      supervised_by: { type: 'string', description: '监管人（如 human:郭万迎）' },
      lock_hours:    { type: 'number', description: '锁定小时数（默认 4）', default: 4 },
    },
    required: ['id', 'claimed_by'],
  },
  async handler(args) {
    const { id, claimed_by, supervised_by, lock_hours = 4 } = args || {};
    const now = new Date();
    const lockUntil = new Date(now.getTime() + lock_hours * 3600 * 1000).toISOString();

    const patch = {
      claimed_by,
      lock_until: lockUntil,
      last_seen_at: now.toISOString(),
      claimed_at: now.toISOString(),
    };
    if (supervised_by) patch.supervised_by = supervised_by;
    // If currently backlog/ready, move to claimed
    const { byId } = loadAllTasks();
    const task = byId.get(id);
    if (task && (task.status === 'backlog' || task.status === 'ready')) {
      patch.status = 'claimed';
    }

    acquireLock();
    try {
      const result = updateTaskFields(id, patch);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            id,
            claimed_by,
            supervised_by: supervised_by || result.before.supervised_by || null,
            lock_until: lockUntil,
            status: patch.status || result.before.status,
          }, null, 2),
        }],
      };
    } finally {
      releaseLock();
    }
  },
};

// ──── 6. task-set-blocked ────

TOOLS['task-set-blocked'] = {
  description: '将任务设为阻塞状态，记录阻塞原因',
  inputSchema: {
    type: 'object',
    properties: {
      id:         { type: 'string', description: '任务 ID' },
      blocked_by: { type: 'string', description: '阻塞原因（如 依赖 E-INNOV-M1-L02 未完成 / 等待甲方确认）' },
    },
    required: ['id', 'blocked_by'],
  },
  async handler(args) {
    const { id, blocked_by } = args || {};
    acquireLock();
    try {
      const result = updateTaskFields(id, { status: 'blocked', blocked_by });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ id, blocked_by, old_status: result.before.status }, null, 2),
        }],
      };
    } finally {
      releaseLock();
    }
  },
};

// ──── 7. task-update-fields ────

TOOLS['task-update-fields'] = {
  description: '更新任务的附加字段（证据、绩效、成本等），不改状态',
  inputSchema: {
    type: 'object',
    properties: {
      id:             { type: 'string', description: '任务 ID' },
      evidence:       { type: 'string', description: 'handoff 证据路径（如 agent-handoffs/XXX.md）' },
      effort_points:  { type: 'string', description: '贡献分（1/2/3/5/8/13）' },
      difficulty:     { type: 'string', description: '难度（S/M/L/XL）' },
      actual_tokens:  { type: 'number', description: '实际消耗 token 数' },
      model_used:     { type: 'string', description: '使用的模型（如 claude-sonnet-4.5）' },
      actual_cost:    { type: 'number', description: '实际成本（美元）' },
      cost_warn:      { type: 'string', description: '成本预警（green/yellow/orange/red）' },
      note:           { type: 'string', description: '备注' },
      user_story:     { type: 'string', description: '用户故事库 ID 引用（逗号分隔多个，如 US-E1-SCH-04；禁止写全文）' },
      sprint_id:      { type: 'string', description: 'Sprint ID（如 2026-W32）；与 scrum-sprint.yaml committed 对齐时使用' },
    },
    required: ['id'],
  },
  async handler(args) {
    const { id, ...rest } = args || {};
    const patch = {};
    const ALLOWED = new Set([
      'evidence', 'effort_points', 'difficulty', 'actual_tokens', 'model_used',
      'actual_cost', 'cost_warn', 'note', 'user_story', 'sprint_id',
    ]);
    for (const [k, v] of Object.entries(rest)) {
      if (!ALLOWED.has(k)) continue;
      if (v !== undefined && v !== null && v !== '') {
        patch[k] = v;
      }
    }
    if (Object.keys(patch).length === 0) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'No fields to update' }, null, 2) }] };
    }

    acquireLock();
    try {
      const result = updateTaskFields(id, patch);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            id,
            updated_fields: Object.keys(patch),
            old_status: result.before.status,
          }, null, 2),
        }],
      };
    } finally {
      releaseLock();
    }
  },
};

// ──── 8. task-review ────
// runAutoVerify 按当前状态自动选择验收规则 (AV-0/AV-1)

TOOLS['task-review'] = {
  description: '自动验收：按当前状态检查能否推进到下一阶段（in_progress→integration; integration→pending_test/ready_to_sign）',
  inputSchema: {
    type: 'object',
    properties: {
      id: { type: 'string', description: '任务 ID' },
    },
    required: ['id'],
  },
  async handler(args) {
    const { id } = args || {};
    const av = runAutoVerify(id);
    if (av.error) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: av.error }, null, 2) }] };
    }
    return { content: [{ type: 'text', text: JSON.stringify(av, null, 2) }] };
  },
};

// ──── 9. task-review-batch ────

TOOLS['task-review-batch'] = {
  description: '批量自动验收所有 in_progress/integration 状态的任务。auto_fix=true 时通过后自动推进到目标状态',
  inputSchema: {
    type: 'object',
    properties: {
      auto_fix: { type: 'boolean', description: '通过后自动推进状态（默认 false，仅出报告）', default: false },
      module:   { type: 'string', description: '可选：仅检查某模块（如"企业"）' },
      target_status: { type: 'string', description: '可选：仅检查目标状态匹配的任务（如 pending_test）', enum: ['integration', 'pending_test', 'ready_to_sign'] },
    },
  },
  async handler(args) {
    const { auto_fix = false, module, target_status } = args || {};
    const { byId } = loadAllTasks();

    const REVIEWABLE = new Set(['in_progress', 'integration']);
    const results = [];
    for (const task of byId.values()) {
      if (!REVIEWABLE.has(task.status)) continue;
      if (module && !taskMatchesModule(task, module)) continue;

      const av = runAutoVerify(task.id);
      if (target_status && av.target_status !== target_status) continue;

      if (av.passed && auto_fix && av.target_status) {
        const now = new Date().toISOString().slice(0, 10);
        acquireLock();
        try {
          updateTaskFields(task.id, {
            status: av.target_status,
            verified_at: now,
            verified_by: 'agent:coordinator',
            note: `auto-verify ${av.av} ${now}: ${av.reason}`,
          });
          av.auto_marked = av.target_status;
        } catch (e) {
          av.auto_marked = `failed: ${e.message}`;
        } finally {
          releaseLock();
        }
      }
      results.push({
        task_id: av.task_id,
        title: av.title,
        status: av.status,
        av: av.av,
        target_status: av.target_status,
        passed: av.passed,
        reason: av.reason,
        auto_marked: av.auto_marked || null,
      });
    }

    const passed = results.filter(r => r.passed).length;
    const failed = results.filter(r => !r.passed).length;

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          total: results.length,
          passed,
          failed,
          auto_fix_applied: auto_fix,
          target_status,
          results,
        }, null, 2),
      }],
    };
  },
};

// ── MCP Protocol Handler ──────────────────────────────────────────

function handleRequest(id, method, params) {
  switch (method) {
    case 'initialize':
      return jsonRpcResult(id, {
        protocolVersion: '2024-11-05',
        capabilities: {
          tools: {},
        },
        serverInfo: {
          name: MCPServer.name,
          version: MCPServer.version,
        },
      });

    case 'notifications/initialized':
      return null; // No response needed

    case 'tools/list': {
      const tools = Object.entries(TOOLS).map(([name, def]) => ({
        name,
        description: def.description,
        inputSchema: def.inputSchema,
      }));
      return jsonRpcResult(id, { tools });
    }

    case 'tools/call': {
      const { name, arguments: args } = params || {};
      const tool = TOOLS[name];
      if (!tool) {
        return jsonRpcError(id, -32601, `Tool not found: ${name}`);
      }
      // Execute handler, catch errors
      const result = tool.handler(args);
      if (result && typeof result.then === 'function') {
        result
          .then((res) => {
            process.stdout.write(jsonRpcResult(id, res) + '\n');
          })
          .catch((err) => {
            process.stderr.write(`Error in tool ${name}: ${err.stack || err.message}\n`);
            process.stdout.write(jsonRpcError(id, -32603, err.message || 'Internal error') + '\n');
          });
        return null; // Response will be sent async
      }
      return jsonRpcResult(id, result);
    }

    default:
      return jsonRpcError(id, -32601, `Method not found: ${method}`);
  }
}

// ── Main Loop ─────────────────────────────────────────────────────

let buffer = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop() || ''; // Keep incomplete line in buffer

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    let msg;
    try {
      msg = JSON.parse(trimmed);
    } catch {
      process.stderr.write(`Invalid JSON-RPC: ${trimmed.slice(0, 200)}\n`);
      continue;
    }

    const { id, method, params } = msg;
    try {
      const response = handleRequest(id, method, params);
      if (response) {
        process.stdout.write(response + '\n');
      }
    } catch (err) {
      process.stderr.write(`Handler error: ${err.stack || err.message}\n`);
      if (id !== undefined && id !== null) {
        process.stdout.write(jsonRpcError(id, -32603, err.message || 'Internal error') + '\n');
      }
    }
  }
});

process.stdin.on('end', () => {
  process.exit(0);
});

process.on('uncaughtException', (err) => {
  process.stderr.write(`Uncaught: ${err.stack || err.message}\n`);
  process.exit(1);
});

// Notify that the server is ready
process.stderr.write(`MCP server "${MCPServer.name}" v${MCPServer.version} started\n`);