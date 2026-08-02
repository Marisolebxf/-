#!/usr/bin/env node
/**
 * task-registry.yaml parse / mutate helpers (coordinator dispatch + ready engine).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const REGISTRY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'task-registry.yaml');

export function readRegistryText() {
  return fs.readFileSync(REGISTRY_PATH, 'utf8');
}

export function writeRegistryText(text) {
  const out = text.endsWith('\n') ? text : `${text}\n`;
  fs.writeFileSync(REGISTRY_PATH, out, 'utf8');
}

/** Asia/Shanghai wall clock as ISO 8601 with +08:00 (task-registry convention). */
export function nowIsoPlus8(date = new Date()) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
  const parts = Object.fromEntries(fmt.formatToParts(date).map((p) => [p.type, p.value]));
  const hour = parts.hour === '24' ? '00' : parts.hour;
  return `${parts.year}-${parts.month}-${parts.day}T${hour}:${parts.minute}:${parts.second}+08:00`;
}

/** Bump task.update_time to now (or explicit ISO). Call on every registry task mutation. */
export function touchUpdateTime(blockLines, when = null) {
  upsertField(blockLines, 'update_time', when || nowIsoPlus8());
}

export function findTaskBlocks(lines) {
  const blocks = [];
  let inTasks = false;
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (/^tasks:\s*$/.test(lines[i])) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    if (/^\s+- id:\s*/.test(lines[i])) {
      if (start >= 0) blocks.push({ start, end: i });
      start = i;
    }
  }
  if (start >= 0) blocks.push({ start, end: lines.length });
  return blocks;
}

export function findTaskBlock(lines, taskId) {
  const esc = taskId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  for (let i = 0; i < lines.length; i++) {
    if (new RegExp(`^\\s+- id:\\s*${esc}\\s*$`).test(lines[i])) {
      let end = lines.length;
      for (let j = i + 1; j < lines.length; j++) {
        if (/^\s+- id:\s*/.test(lines[j])) {
          end = j;
          break;
        }
      }
      return { start: i, end };
    }
  }
  return null;
}

export function parseInlineList(value) {
  const v = (value || '').trim();
  const m = v.match(/^\[(.*)\]$/);
  if (!m) return v ? [v] : [];
  const inner = m[1].trim();
  if (!inner) return [];
  return inner.split(/,\s*/).map((s) => s.trim().replace(/^["']|["']$/g, ''));
}

/** End index (exclusive) of a YAML mapping entry starting at idx, including |/> body or orphaned deeper lines. */
export function fieldValueEnd(blockLines, idx) {
  const m = blockLines[idx]?.match(/^(\s+)\S/);
  if (!m) return idx + 1;
  const indent = m[1];
  let end = idx + 1;
  while (end < blockLines.length) {
    const line = blockLines[end];
    if (line.trim() === '') {
      const next = blockLines[end + 1];
      if (next && next.startsWith(`${indent} `)) {
        end += 1;
        continue;
      }
      break;
    }
    // deeper indent → continuation / list / nested (or inbound-orphan after quoted scalar)
    if (line.startsWith(`${indent} `)) {
      end += 1;
      continue;
    }
    break;
  }
  return end;
}

export function getScalar(blockLines, key) {
  const re = new RegExp(`^(\\s+)${key}:\\s*(.*)$`);
  for (let i = 0; i < blockLines.length; i++) {
    const m = blockLines[i].match(re);
    if (!m) continue;
    const rest = (m[2] || '').trim();
    if (rest === '|' || rest === '>' || rest.startsWith('|') || rest.startsWith('>')) {
      const end = fieldValueEnd(blockLines, i);
      const body = [];
      for (let j = i + 1; j < end; j++) {
        const raw = blockLines[j];
        if (raw.trim() === '') {
          body.push('');
          continue;
        }
        body.push(raw.replace(new RegExp(`^${m[1]}  `), '').replace(new RegExp(`^${m[1]} `), ''));
      }
      while (body.length && body[body.length - 1] === '') body.pop();
      return body.join('\n').trim();
    }
    return rest.replace(/^["']|["']$/g, '').replace(/\s+#.*$/, '').trim();
  }
  return '';
}

function formatFieldLines(indent, key, value) {
  if (typeof value === 'number') return [`${indent}${key}: ${value}`];
  const s = String(value);
  if (s.includes('\n') || s.length > 160) {
    const lines = s.replace(/\r\n/g, '\n').split('\n');
    return [`${indent}${key}: |`, ...lines.map((l) => `${indent}  ${l}`)];
  }
  return [`${indent}${key}: "${s.replace(/"/g, '\\"')}"`];
}

export function getListField(blockLines, key) {
  for (let i = 0; i < blockLines.length; i++) {
    const m = blockLines[i].match(new RegExp(`^\\s+${key}:\\s*(.*)$`));
    if (!m) continue;
    const rest = m[1].trim();
    if (rest.startsWith('[')) return parseInlineList(rest);
    const items = [];
    if (rest && rest !== '[]') items.push(rest.replace(/^["']|["']$/g, ''));
    for (let j = i + 1; j < blockLines.length; j++) {
      const li = blockLines[j].match(/^\s+-\s+(.+)$/);
      if (!li) break;
      items.push(li[1].trim().replace(/^["']|["']$/g, ''));
    }
    return items;
  }
  return [];
}

export function parseTaskBlock(blockLines) {
  const id =
    getScalar(blockLines, 'id') ||
    (blockLines[0].match(/id:\s*(.+)/) || [])[1]?.trim().replace(/^["']|["']$/g, '');
  return {
    id,
    title: getScalar(blockLines, 'title'),
    status: getScalar(blockLines, 'status'),
    agent: getScalar(blockLines, 'agent'),
    epic: getScalar(blockLines, 'epic'),
    sprint_id: getScalar(blockLines, 'sprint_id'),
    supervised_by: getScalar(blockLines, 'supervised_by'),
    claimed_by: getScalar(blockLines, 'claimed_by'),
    claim_type: getScalar(blockLines, 'claim_type'),
    claimed_at: getScalar(blockLines, 'claimed_at'),
    lock_until: getScalar(blockLines, 'lock_until'),
    update_time: getScalar(blockLines, 'update_time'),
    completed_at: getScalar(blockLines, 'completed_at'),
    last_seen_at: getScalar(blockLines, 'last_seen_at'),
    subcoord: getScalar(blockLines, 'subcoord'),
    graph_role: getScalar(blockLines, 'graph_role'),
    ods_dependency_phase: getScalar(blockLines, 'ods_dependency_phase'),
    convoy: getScalar(blockLines, 'convoy'),
    repo: getScalar(blockLines, 'repo'),
    touched_files: getListField(blockLines, 'touched_files'),
    priority: getScalar(blockLines, 'priority'),
    blocked_by: getScalar(blockLines, 'blocked_by'),
    delivery_phase: getScalar(blockLines, 'delivery_phase'),
    task_type: getScalar(blockLines, 'task_type'),
    effort_points: getScalar(blockLines, 'effort_points'),
    difficulty: getScalar(blockLines, 'difficulty'),
    estimated_tokens: getScalar(blockLines, 'estimated_tokens'),
    record_id: getScalar(blockLines, 'feishu_bitable_record_id'),
    depends_on: getListField(blockLines, 'depends_on'),
    collaborators: getListField(blockLines, 'collaborators'),
    definition_of_done: getListField(blockLines, 'definition_of_done'),
    design_refs: getListField(blockLines, 'design_refs'),
    dispatch_confirmed_by: getScalar(blockLines, 'dispatch_confirmed_by'),
    review_phase: getScalar(blockLines, 'review_phase'),
    verified_at: getScalar(blockLines, 'verified_at'),
    verified_by: getScalar(blockLines, 'verified_by'),
    note: getScalar(blockLines, 'note'),
  };
}

export function loadAllTasks() {
  const lines = readRegistryText().split(/\r?\n/);
  const blocks = findTaskBlocks(lines);
  const byId = new Map();
  for (const { start, end } of blocks) {
    const blockLines = lines.slice(start, end);
    const task = parseTaskBlock(blockLines);
    if (task.id) {
      task._loc = { start, end };
      byId.set(task.id, task);
    }
  }
  return { lines, byId };
}

export function upsertField(blockLines, key, value) {
  const re = new RegExp(`^(\\s+)${key}:\\s*`);
  const baseIndent = blockLines[0]?.match(/^(\s+)/)?.[1] || '  ';
  const indent = /^\s+- id:/.test(blockLines[0]) ? `${baseIndent}  ` : baseIndent;
  const formatted = formatFieldLines(indent, key, value);

  for (let i = 0; i < blockLines.length; i++) {
    if (!re.test(blockLines[i])) continue;
    const end = fieldValueEnd(blockLines, i);
    // Keep existing field indent if present (may differ from computed indent)
    const existingIndent = blockLines[i].match(/^(\s+)/)?.[1] || indent;
    const lines = formatFieldLines(existingIndent, key, value);
    blockLines.splice(i, end - i, ...lines);
    return;
  }
  blockLines.splice(1, 0, ...formatted);
}

export function upsertListItem(blockLines, key, item) {
  const items = getListField(blockLines, key);
  if (items.includes(item)) return;
  items.push(item);
  const re = new RegExp(`^\\s+${key}:\\s*`);
  let idx = -1;
  for (let i = 0; i < blockLines.length; i++) {
    if (re.test(blockLines[i])) {
      idx = i;
      break;
    }
  }
  // Task blocks start with `  - id:`; field indent is two more spaces than that list marker line.
  const baseIndent = blockLines[0]?.match(/^(\s+)/)?.[1] || '  ';
  const indent = /^\s+- id:/.test(blockLines[0]) ? `${baseIndent}  ` : baseIndent;
  const listIndent = `${indent}  `;
  if (idx < 0) {
    blockLines.splice(1, 0, `${indent}${key}:`, `${listIndent}- ${item}`);
    return;
  }
  let end = idx + 1;
  while (end < blockLines.length && /^\s+-\s+/.test(blockLines[end])) end++;
  blockLines.splice(end, 0, `${listIndent}- ${item}`);
}

export function applyBlockUpdate(lines, loc, blockLines) {
  return [...lines.slice(0, loc.start), ...blockLines, ...lines.slice(loc.end)];
}

/**
 * Patch task fields. Always refreshes update_time unless:
 *   - opts.touchUpdateTime === false, or
 *   - patch already sets update_time (explicit / backfill).
 */
export function updateTaskFields(taskId, patch, dryRun = false, opts = {}) {
  const text = readRegistryText();
  const lines = text.split(/\r?\n/);
  const loc = findTaskBlock(lines, taskId);
  if (!loc) throw new Error(`Task not found: ${taskId}`);
  const block = lines.slice(loc.start, loc.end);
  const before = parseTaskBlock(block);
  const explicitUpdateTime =
    patch && Object.prototype.hasOwnProperty.call(patch, 'update_time');
  for (const [k, v] of Object.entries(patch || {})) {
    if (v === undefined || v === null) continue;
    upsertField(block, k, v);
  }
  if (opts.touchUpdateTime !== false && !explicitUpdateTime) {
    touchUpdateTime(block);
  }
  const after = parseTaskBlock(block);
  if (dryRun) return { before, after, changed: false };
  const newLines = applyBlockUpdate(lines, loc, block);
  writeRegistryText(newLines.join('\n'));
  return { before, after, changed: true };
}

export function isDoneStatus(status) {
  return status === 'done' || status === 'completed';
}

// ── Status Machine v4 (task_type-driven paths) ────────────────────
//
// All tasks: backlog → ready → claimed → in_progress → ... → done
//
// After in_progress, the path depends on task_type:
//
//   feature:    in_progress →[AV-0]→ integration →[AV-1]→ pending_test →[QA]→ testing →[QA]→ ready_to_sign →[签收]→ done
//   definition: in_progress →[AV-0]→ integration(会签) →[AV-1]→ ready_to_sign →[签收]→ done
//   tech_task:  in_progress →[AV-0]→ ready_to_sign →[签收]→ done
//   spike:      in_progress →[AV-0]→ ready_to_sign →[签收]→ done
//   bugfix:     in_progress →[AV-0]→ pending_test →[QA]→ testing →[QA]→ ready_to_sign →[签收]→ done
//   chore:      in_progress →[AV-0]→ done
//
// AV-0 target (in_progress → ?) by task_type:
//   feature/definition → integration
//   tech_task/spike     → ready_to_sign
//   bugfix              → pending_test
//   chore               → done
//
// AV-1 target (integration → ?) by task_type:
//   feature    → pending_test
//   definition → ready_to_sign
//
// Gates:
//   pending_test → testing : claimed_by=qa-agent OR supervised_by=human:黄敬洲
//   ready_to_sign → done   : signer = human:淮政玮 (chore 类型豁免)
//
// `review` is a LEGACY umbrella status (deprecated).
export const VALID_STATUSES = new Set([
  'backlog', 'ready', 'claimed', 'in_progress', 'integration',
  'pending_test', 'testing', 'ready_to_sign',
  'done', 'blocked', 'needs-revision',
  // legacy (deprecated, kept for backward compat during migration)
  'review',
]);

export const TERMINAL_STATUSES = new Set(['done', 'completed']);

// ── Task Types ────────────────────────────────────────────────────
export const TASK_TYPES = new Set([
  'feature',      // 用户故事级功能：用户可感知的操作，走完整路径（联调+QA测试）
  'definition',   // PDR/USM/Wireframe：走会签路径，跳过测试
  'tech_task',    // 技术任务：接口规约/ETL/算法框架，跳过联调+测试
  'spike',        // 探针：调研/分析/选型，跳过联调+测试
  'bugfix',       // 修缺陷：跳过联调，但走QA测试
  'chore',        // 杂项：看板/文档/配置，直接done
]);

// AV-0 target status by task_type (in_progress → ?)
export const AV0_TARGET = {
  feature: 'integration',
  definition: 'integration',
  tech_task: 'ready_to_sign',
  spike: 'ready_to_sign',
  bugfix: 'pending_test',
  chore: 'done',
};

// AV-1 target status by task_type (integration → ?)
export const AV1_TARGET = {
  feature: 'pending_test',
  definition: 'ready_to_sign',
};

// Sign-off gate: who can transition ready_to_sign → done
export const SIGN_OFF_BY = 'human:淮政玮';

// chore type skips sign-off gate
export const SIGN_OFF_EXEMPT_TYPES = new Set(['chore']);

// QA gate: who can claim pending_test → testing
export const QA_GATE_AGENTS = new Set(['qa-agent']);
export const QA_GATE_SUPERVISORS = new Set(['human:黄敬洲']);

// DEPRECATED — kept for backward compat. Will be removed after migration.
export const REVIEW_PHASES = new Set([
  'pending_test', 'pending_sign', 'pending_business', 'blocked_by_dep',
]);

/**
 * Check if the transition is allowed by gate rules.
 * Returns { ok: true } or { ok: false, reason: '...' }.
 */
export function checkTransitionGate(fromStatus, toStatus, task, actor) {
  const taskType = task?.task_type || 'feature'; // default feature
  // pending_test → testing: QA gate
  if (fromStatus === 'pending_test' && toStatus === 'testing') {
    const actorAgent = actor?.agent || task?.claimed_by || '';
    const actorSupervisor = actor?.supervised_by || task?.supervised_by || '';
    const isQaAgent = QA_GATE_AGENTS.has(actorAgent) || actorAgent === 'qa-agent';
    const isQaSupervisor = QA_GATE_SUPERVISORS.has(actorSupervisor);
    if (!isQaAgent && !isQaSupervisor) {
      return { ok: false, reason: `pending_test → testing 需要 qa-agent 认领或监管人 human:黄敬洲（当前 agent=${actorAgent}, supervised_by=${actorSupervisor}）` };
    }
  }
  // ready_to_sign → done: sign-off gate (chore exempt)
  if (fromStatus === 'ready_to_sign' && toStatus === 'done') {
    if (!SIGN_OFF_EXEMPT_TYPES.has(taskType)) {
      const actorHuman = actor?.human || '';
      if (actorHuman && actorHuman !== SIGN_OFF_BY) {
        return { ok: false, reason: `ready_to_sign → done 需要淮政玮签收（当前操作人=${actorHuman}，task_type=${taskType}）` };
      }
    }
  }
  return { ok: true };
}

export function depsSatisfied(task, doneIds) {
  const deps = (task.depends_on || []).filter(Boolean);
  if (deps.length === 0) return true;
  return deps.every((d) => doneIds.has(d));
}

export function buildDoneIdSet(byId) {
  const done = new Set();
  for (const t of byId.values()) {
    if (isDoneStatus(t.status)) done.add(t.id);
  }
  return done;
}

export function modulePrefixFromTaskId(taskId, suffix) {
  if (!taskId.endsWith(suffix)) return null;
  return taskId.slice(0, -suffix.length);
}
