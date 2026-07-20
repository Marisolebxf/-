#!/usr/bin/env node
/**
 * Coordinator auto-dispatch: scan triggers → pending confirm → ready + 派单包
 * Gate3 DG-G3 done → propose impl-gate3-unlock pending → confirm → ready
 *
 *   node scripts/coordinator-dispatch.mjs scan [--cause-task ID] [--dry-run]
 *   node scripts/coordinator-dispatch.mjs list
 *   node scripts/coordinator-dispatch.mjs confirm --all [--dry-run]
 *   node scripts/coordinator-dispatch.mjs confirm --ids ID1,ID2 [--dry-run]
 *   node scripts/coordinator-dispatch.mjs ready-engine [--dry-run]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import {
  buildDispatchTriggerText,
  projectConfirmedTaskToFeishu,
  projectPendingTargetsToFeishu,
  projectRejectedTaskToFeishu,
  resolveDispatchConfirmBy,
} from './lib/dispatch-feishu-projection.mjs';
import {
  ORCH_ROOT,
  REGISTRY_PATH,
  loadAllTasks,
  findTaskBlock,
  readRegistryText,
  writeRegistryText,
  parseTaskBlock,
  upsertField,
  upsertListItem,
  applyBlockUpdate,
  updateTaskFields,
  isDoneStatus,
  depsSatisfied,
  buildDoneIdSet,
} from './lib/task-registry-lib.mjs';

const RULES_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'dispatch-rules.yaml');
const PENDING_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'pending-dispatch.yaml');
const ROSTER_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'team-roster.yaml');
const DISPATCH_QUEUE_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'dispatch-queue.yaml');
const LOG_PATH = path.join(ORCH_ROOT, 'agent-delivery', '_tmp', 'coordinator-dispatch.log');

function normalizeHumanPrefix(value) {
  const v = (value || '').trim();
  if (!v) return '';
  if (v.startsWith('human:')) return v;
  return `human:${v}`;
}

function loadConfirmApprovers() {
  if (!fs.existsSync(ROSTER_PATH)) {
    throw new Error(`team-roster not found: ${ROSTER_PATH}`);
  }
  const raw = fs.readFileSync(ROSTER_PATH, 'utf8');
  const approvers = new Map();

  const memberBlocks = raw.split(/\n\s+- registry_name:/).slice(1);
  for (const block of memberBlocks) {
    const body = `registry_name:${block}`;
    const reg = body.match(/^registry_name:\s*(.+)$/m)?.[1]?.trim();
    if (!reg) continue;
    const team = body.match(/^\s+team:\s*(\S+)/m)?.[1]?.trim() || '';
    const role = body.match(/^\s+role:\s*(\S+)/m)?.[1]?.trim() || '';
    const canSup = /can_supervise_agent:\s*true/.test(body);
    const isPm = team === 'pm' || role === 'project_owner';
    if (canSup || isPm) {
      approvers.set(reg, { name: reg.replace(/^human:/, ''), team, role, canSupervise: canSup, isPm });
    }
  }

  const gates = raw.match(/review_gates:\s*\r?\n([\s\S]*?)(?:\n\S|$)/);
  if (gates) {
    for (const m of gates[1].matchAll(/^\s+\w+:\s*(human:\S+)/gm)) {
      approvers.set(m[1].trim(), { name: m[1].replace(/^human:/, ''), team: 'review_gate', role: '', canSupervise: true, isPm: false });
    }
  }
  const maint = raw.match(/^maintainer:\s*(human:\S+)/m);
  if (maint) {
    approvers.set(maint[1].trim(), { name: maint[1].replace(/^human:/, ''), team: 'pm', role: 'maintainer', canSupervise: true, isPm: true });
  }

  return approvers;
}

export function validateConfirmApprover(approvedBy) {
  const reg = normalizeHumanPrefix(approvedBy);
  if (!reg || !/^human:.+/.test(reg)) {
    throw new Error('confirm 必须带 --approved-by human:真名（或 --approved-by 真名）');
  }
  const approvers = loadConfirmApprovers();
  if (!approvers.has(reg)) {
    const allowed = [...approvers.values()]
      .map((a) => a.name)
      .filter((v, i, arr) => arr.indexOf(v) === i)
      .sort()
      .join('、');
    throw new Error(
      `[REJECT] ${reg} 无权 confirm。须 PM 或 can_supervise_agent 监管人。当前可确认：${allowed}`,
    );
  }
  return reg;
}

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
    fs.appendFileSync(LOG_PATH, `${line}\n`, 'utf8');
  } catch {
    /* ignore */
  }
}

const KNOWN_CAUSE_SUFFIXES = [
  'PACK-L01',
  'UX-L01',
  'METRIC-OPEN-L01',
  'V1-HIFI-R1',
  'V1-HIFI',
  'PDR-G1-RECLOSE',
  'V1-FINAL',
];

export function loadRules() {
  const raw = fs.readFileSync(RULES_PATH, 'utf8');
  const agentSupervisors = {};
  const asBlock = raw.match(/agent_supervisors:\s*\r?\n((?:  .+\r?\n)+)/);
  if (asBlock) {
    for (const m of asBlock[1].matchAll(/^\s+([\w-]+):\s*(.+)$/gm)) {
      agentSupervisors[m[1]] = m[2].trim();
    }
  }
  const packageDirs = { default: 'agent-handoffs' };
  const pdBlock = raw.match(/package_dirs:\s*\r?\n((?:  .+\r?\n)+)/);
  if (pdBlock) {
    for (const m of pdBlock[1].matchAll(/^\s+([\w-]+):\s*(.+)$/gm)) {
      packageDirs[m[1]] = m[2].trim();
    }
  }

  const confirmTriggers = [];
  const ctSection = raw.match(/confirm_triggers:\s*\r?\n([\s\S]*?)(?:\n# ──|\ngate3_confirm_trigger:|\nconfirm_policy:)/);
  if (ctSection) {
    const chunks = ctSection[1].split(/\n\s+- id:/).filter((c) => c.trim());
    for (const chunk of chunks) {
      const body = chunk.startsWith('id:') ? chunk : `id:${chunk}`;
      const id = body.match(/^id:\s*(\S+)/)?.[1];
      if (!id) continue;
      const suffixM = body.match(/task_done_suffix:\s*(\S+)/);
      const unlockSuffixes = [];
      const suffixLines = body.match(/unlock_suffixes:\s*\r?\n((?:\s+-.+\r?\n)+)/);
      if (suffixLines) {
        for (const m of suffixLines[1].matchAll(/^\s+-\s+(\S+)/gm)) {
          unlockSuffixes.push(m[1]);
        }
      }
      const reqStatus = [];
      const rs = body.match(/require_status:\s*\[(.*?)\]/);
      if (rs) {
        reqStatus.push(...rs[1].split(',').map((s) => s.trim()));
      }
      const phase = body.match(/delivery_phase:\s*(\w+)/)?.[1] || '';
      confirmTriggers.push({
        id,
        taskDoneSuffix: suffixM?.[1] || '',
        unlockSuffixes,
        requireStatus: reqStatus.length ? reqStatus : ['backlog'],
        deliveryPhase: phase,
      });
    }
  }

  const gate3 = { enabled: true, id: 'impl-gate3-unlock', triggerSuffixes: ['DG-G3'] };
  const g3Block = raw.match(/gate3_confirm_trigger:\s*\r?\n([\s\S]*?)(?:\nready_engine:|\n$)/);
  if (g3Block && /enabled:\s*false/.test(g3Block[1])) gate3.enabled = false;
  const g3Id = g3Block?.[1].match(/^\s+id:\s*(\S+)/m)?.[1];
  if (g3Id) gate3.id = g3Id;
  const g3s = g3Block?.[1].match(/trigger_suffixes:\s*\r?\n((?:\s+-.+\r?\n)+)/);
  if (g3s) {
    gate3.triggerSuffixes = [...g3s[1].matchAll(/^\s+-\s+(\S+)/gm)].map((m) => m[1]);
  }

  const excludeDeliveryPhases = [];
  const reBlock = raw.match(/ready_engine:\s*\r?\n([\s\S]*?)(?:\n\S|$)/);
  const ex = reBlock?.[1].match(/exclude_delivery_phases:\s*\r?\n((?:\s+-.+\r?\n)+)/);
  if (ex) {
    for (const m of ex[1].matchAll(/^\s+-\s+(\w+)/gm)) excludeDeliveryPhases.push(m[1]);
  }

  return { agentSupervisors, packageDirs, confirmTriggers, gate3, excludeDeliveryPhases, raw };
}

export function loadPending() {
  if (!fs.existsSync(PENDING_PATH)) {
    return { pending: [], confirmed: [] };
  }
  const raw = fs.readFileSync(PENDING_PATH, 'utf8');
  const pending = [];
  if (/pending:\s*\[\]/.test(raw)) {
    return { pending, confirmed: [] };
  }
  const pendingBlock = raw.match(/pending:\s*\r?\n([\s\S]*?)(?:\nconfirmed:|$)/);
  if (pendingBlock) {
    const chunks = pendingBlock[1].split(/\n\s+- id:/).filter((c) => c.trim());
    for (const chunk of chunks) {
      const body = chunk.startsWith('id:') ? chunk : `id:${chunk}`;
      const id = body.match(/^id:\s*(\S+)/)?.[1];
      const cause = body.match(/cause_task:\s*(\S+)/)?.[1];
      const trigger = body.match(/trigger:\s*(\S+)/)?.[1];
      const targets = [];
      const tb = body.match(/targets:\s*\r?\n((?:\s+-.+\r?\n)+)/);
      if (tb) {
        for (const m of tb[1].matchAll(/^\s+-\s+(\S+)/gm)) targets.push(m[1]);
      }
      if (id && targets.length) pending.push({ id, cause_task: cause, trigger, targets });
    }
  }
  return { pending, confirmed: [] };
}

function savePending(state) {
  const lines = [
    '# coordinator 待确认派单队列',
    'version: 1',
    `updated: "${new Date().toISOString().slice(0, 10)}"`,
    '',
  ];
  if (!state.pending.length) {
    lines.push('pending: []');
  } else {
    lines.push('pending:');
    for (const p of state.pending) {
      lines.push(`  - id: ${p.id}`);
      lines.push(`    created_at: "${p.created_at || new Date().toISOString()}"`);
      lines.push(`    trigger: ${p.trigger}`);
      lines.push(`    cause_task: ${p.cause_task}`);
      lines.push('    targets:');
      for (const t of p.targets) lines.push(`      - ${t}`);
    }
  }
  lines.push('', 'confirmed:');
  if (!state.confirmed?.length) {
    lines.push('  []');
  } else {
    for (const c of state.confirmed.slice(-20)) {
      lines.push(`  - id: ${c.id}`);
      lines.push(`    confirmed_at: "${c.confirmed_at}"`);
      lines.push(`    approved_by: ${c.approved_by}`);
      lines.push(`    trigger: ${c.trigger}`);
      lines.push(`    cause_task: ${c.cause_task}`);
      lines.push('    applied_tasks:');
      for (const t of c.applied_tasks || c.targets || []) {
        lines.push(`      - ${t}`);
      }
    }
  }
  lines.push('');
  fs.writeFileSync(PENDING_PATH, lines.join('\n'), 'utf8');
}

function isHalted() {
  if (!fs.existsSync(DISPATCH_QUEUE_PATH)) return false;
  const raw = fs.readFileSync(DISPATCH_QUEUE_PATH, 'utf8');
  return /coordinator_halt:\s*\r?\n[\s\S]*?active:\s*true/.test(raw);
}

function matchesSuffix(taskId, suffix) {
  return taskId.endsWith(suffix);
}

function modulePrefixFromCause(causeTaskId) {
  for (const suf of KNOWN_CAUSE_SUFFIXES) {
    if (causeTaskId.endsWith(suf)) return causeTaskId.slice(0, -suf.length);
  }
  return null;
}

function resolveUnlockTaskIds(causeTaskId, suffixes, byId) {
  const modulePrefix = modulePrefixFromCause(causeTaskId);
  if (!modulePrefix) return [];
  const ids = [];
  for (const suf of suffixes) {
    const tid = `${modulePrefix}${suf}`;
    if (byId.has(tid)) ids.push(tid);
  }
  return ids;
}

function moduleSlugFromDgTask(taskId) {
  const m = taskId.match(/^ENT-MOD-(.+?)-DG-G3$/);
  return m ? m[1] : null;
}

function implTaskMatchesModule(taskId, moduleSlug, dgTaskId) {
  if ((taskId.match(/-DG-G3$/) || taskId.match(/-DG$/)) && taskId !== dgTaskId) return false;
  if (taskId.includes(`ENT-MOD-${moduleSlug}-`)) return true;
  if (taskId.includes(`ENT-${moduleSlug}-`)) return true;
  if (taskId.includes(`-${moduleSlug}-`) || taskId.endsWith(`-${moduleSlug}`)) return true;
  return false;
}

function extraGateForPdrRecClose(triggerId, causeTaskId, targetId, byId, doneIds) {
  if (!targetId.endsWith('PDR-G1-RECLOSE')) return true;
  const prefix = targetId.replace(/PDR-G1-RECLOSE$/, '');
  const mo = `${prefix}METRIC-OPEN-L01`;
  const v1 = `${prefix}V1-HIFI`;
  const v1r1 = `${prefix}V1-HIFI-R1`;
  const moDone = doneIds.has(mo);
  const v1Done = doneIds.has(v1) || doneIds.has(v1r1);
  if (triggerId.includes('mo-v1') || causeTaskId.endsWith('METRIC-OPEN-L01')) {
    return v1Done;
  }
  if (causeTaskId.endsWith('V1-HIFI') || causeTaskId.endsWith('V1-HIFI-R1')) {
    return moDone;
  }
  return moDone && v1Done;
}

function runReadyEngine(dryRun) {
  const rules = loadRules();
  if (!rules.raw.includes('ready_engine:') || /ready_engine:[\s\S]*enabled:\s*false/.test(rules.raw)) {
    return { changes: [] };
  }
  const { lines, byId } = loadAllTasks();
  const doneIds = buildDoneIdSet(byId);
  const changes = [];
  let newLines = lines;

  const excludePhases = rules.excludeDeliveryPhases || [];

  for (const task of byId.values()) {
    if (!['backlog', 'pending'].includes(task.status)) continue;
    if (task.delivery_phase && excludePhases.includes(task.delivery_phase)) continue;
    if (task.blocked_by) {
      if (task.status !== 'blocked') {
        changes.push({ id: task.id, old: task.status, new: 'blocked' });
        if (!dryRun) {
          const loc = findTaskBlock(newLines, task.id);
          const block = newLines.slice(loc.start, loc.end);
          upsertField(block, 'status', 'blocked');
          newLines = applyBlockUpdate(newLines, loc, block);
        }
      }
      continue;
    }
    if (!depsSatisfied(task, doneIds)) continue;
    if (task.status === 'ready') continue;
    changes.push({ id: task.id, old: task.status, new: 'ready' });
    if (!dryRun) {
      const loc = findTaskBlock(newLines, task.id);
      const block = newLines.slice(loc.start, loc.end);
      upsertField(block, 'status', 'ready');
      const note = `${new Date().toISOString().slice(0, 10)} auto-ready-engine`;
      upsertField(block, 'note', note);
      newLines = applyBlockUpdate(newLines, loc, block);
    }
  }

  if (!dryRun && changes.length) {
    writeRegistryText(newLines.join('\n'));
  }
  return { changes };
}

function resolveGate3UnlockTargets(causeTask, byId, doneIds) {
  const rules = loadRules();
  if (!rules.gate3.enabled) return [];
  const causeTaskId = causeTask.id;
  const matched = rules.gate3.triggerSuffixes.some((s) => causeTaskId.endsWith(s));
  if (!matched) return [];

  const moduleSlug = moduleSlugFromDgTask(causeTaskId);
  const effectiveDone = new Set(doneIds);
  effectiveDone.add(causeTaskId);
  const targets = [];

  for (const task of byId.values()) {
    if (task.delivery_phase !== 'implementation') continue;
    if (task.status !== 'backlog') continue;
    if (task.epic && causeTask.epic && task.epic !== causeTask.epic) continue;
    if (task.claimed_by) continue;

    const depHasDg = (task.depends_on || []).includes(causeTaskId);
    const slugMatch = moduleSlug && implTaskMatchesModule(task.id, moduleSlug, causeTaskId);
    if (!depHasDg && !slugMatch) continue;
    if (!depsSatisfied(task, effectiveDone)) continue;
    targets.push(task.id);
  }
  return targets;
}

function scanTriggers(causeTaskId, dryRun) {
  if (isHalted()) {
    log('HALT active — skip scan');
    return { pending: [], ready: [] };
  }

  const readyResult = runReadyEngine(dryRun);
  log(`ready-engine: ${readyResult.changes.length} change(s)`);

  const rules = loadRules();
  const { byId } = loadAllTasks();
  const doneIds = buildDoneIdSet(byId);
  const pendingState = loadPending();
  const newPending = [];

  const causes = causeTaskId
    ? [byId.get(causeTaskId)].filter(Boolean)
    : [...byId.values()].filter((t) => isDoneStatus(t.status));

  for (const cause of causes) {
    if (!isDoneStatus(cause.status)) continue;

    const gate3Targets = resolveGate3UnlockTargets(cause, byId, doneIds);
    if (gate3Targets.length) {
      const triggerId = rules.gate3.id || 'impl-gate3-unlock';
      const exists = pendingState.pending.some(
        (p) => p.trigger === triggerId && p.cause_task === cause.id,
      );
      if (exists) {
        log(`pending already exists for trigger=${triggerId} cause=${cause.id}`);
      } else {
        const pendId = `${triggerId}-${cause.id}-${gate3Targets.join('_')}`.slice(0, 80);
        const entry = {
          id: pendId,
          created_at: new Date().toISOString(),
          trigger: triggerId,
          cause_task: cause.id,
          targets: gate3Targets,
        };
        newPending.push(entry);
        log(`propose gate3 confirm: ${gate3Targets.join(', ')} (cause=${cause.id})`);
      }
    }

    for (const trigger of rules.confirmTriggers) {
      if (!trigger.taskDoneSuffix || !matchesSuffix(cause.id, trigger.taskDoneSuffix)) continue;
      const targets = resolveUnlockTaskIds(cause.id, trigger.unlockSuffixes, byId);
      const validTargets = targets.filter((tid) => {
        const t = byId.get(tid);
        if (!t) return false;
        if (!trigger.requireStatus.includes(t.status)) return false;
        if (trigger.deliveryPhase && t.delivery_phase !== trigger.deliveryPhase) return false;
        if (!extraGateForPdrRecClose(trigger.id, cause.id, tid, byId, doneIds)) return false;
        if (t.status === 'ready' || t.claimed_by) return false;
        return true;
      });
      if (!validTargets.length) continue;

      const pendId = `${trigger.id}-${cause.id}-${validTargets.join('_')}`.slice(0, 80);
      const exists = pendingState.pending.some(
        (p) => p.trigger === trigger.id && p.cause_task === cause.id,
      );
      if (exists) {
        log(`pending already exists for trigger=${trigger.id} cause=${cause.id}`);
        continue;
      }

      const entry = {
        id: pendId,
        created_at: new Date().toISOString(),
        trigger: trigger.id,
        cause_task: cause.id,
        targets: validTargets,
      };
      newPending.push(entry);
      log(`propose confirm: ${validTargets.join(', ')} (cause=${cause.id})`);
    }
  }

  if (!dryRun && newPending.length) {
    pendingState.pending.push(...newPending);
    savePending(pendingState);
    projectPendingTargetsToFeishu(newPending, rules, byId, false);
  } else if (dryRun && newPending.length) {
    projectPendingTargetsToFeishu(newPending, rules, byId, true);
  }

  return { pending: newPending, ready: readyResult.changes };
}

function packagePath(task, rules) {
  const dir =
    rules.packageDirs[task.epic] || rules.packageDirs.default || 'agent-handoffs';
  return path.join(ORCH_ROOT, dir, `${task.id}-派单包.md`);
}

function generateDispatchPackage(task, rules, causeTask) {
  const pkgPath = packagePath(task, rules);
  if (fs.existsSync(pkgPath)) return pkgPath;

  const sup = task.supervised_by || rules.agentSupervisors[task.agent] || 'human:郭万迎';
  const relPath = path.relative(ORCH_ROOT, pkgPath).replace(/\\/g, '/');
  const dod = (task.definition_of_done || [])
    .map((d, i) => `${i + 1}. ${d}`)
    .join('\n');
  const today = new Date().toISOString().slice(0, 10);
  const collab =
    task.collaborators?.length > 0
      ? `\n- **协作**：${task.collaborators.map((c) => `\`${c}\``).join('、')}`
      : '';

  const content = `# 派单包：${task.id}

- **派单方**：coordinator（auto-dispatch）
- **时间**：${today}
- **执行 Agent**：\`${task.agent}\`${collab}
- **监管人**：${sup}
- **Sprint**：${task.sprint_id || '（Planning 时填写）'}
- **上游**：\`${causeTask || '—'}\` ✅

## 1. 目标

${task.title || task.id}

## 2. Definition of Done

${dod || '（见 task-registry definition_of_done）'}

## 3. 认领话术

\`\`\`text
/goal ${task.id}
监管：${sup}
\`\`\`
`;

  fs.mkdirSync(path.dirname(pkgPath), { recursive: true });
  fs.writeFileSync(pkgPath, content, 'utf8');
  log(`created package: ${relPath}`);
  return relPath;
}

function syncFeishuTask(taskId, dryRun, dispatchOverlay = {}) {
  if (dryRun) return;
  const script = path.join(ORCH_ROOT, 'scripts', 'lib', 'board-task-status.mjs');
  const args = [script, '--task-id', taskId, '--status', 'ready'];
  if (dispatchOverlay.gate) args.push('--dispatch-gate', dispatchOverlay.gate);
  if (dispatchOverlay.confirmBy) args.push('--dispatch-confirm-by', dispatchOverlay.confirmBy);
  if (dispatchOverlay.trigger) args.push('--dispatch-trigger', dispatchOverlay.trigger);
  const r = spawnSync(process.execPath, args, {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
    env: process.env,
  });
  if (r.status !== 0) {
    log(`WARN feishu sync skipped for ${taskId}: ${r.stderr || r.stdout}`);
  }
}

export function rejectPendingForTask(taskId, dryRun) {
  const state = loadPending();
  const before = state.pending.length;
  state.pending = state.pending.filter((e) => !e.targets.includes(taskId));
  if (!dryRun && state.pending.length !== before) {
    savePending(state);
    projectRejectedTaskToFeishu(taskId, false);
  }
  return before - state.pending.length;
}

export function confirmPending(opts) {
  const { ids, all, dryRun, approvedBy } = opts;
  const approver = validateConfirmApprover(approvedBy);
  log(`confirm approved_by=${approver}`);

  const rules = loadRules();
  const state = loadPending();
  let entries = state.pending;
  if (!all && ids?.length) {
    entries = entries.filter((e) => e.targets.some((t) => ids.includes(t)) || ids.includes(e.id));
  }
  if (!entries.length) {
    log('nothing to confirm');
    return { applied: [], approved_by: approver };
  }

  const applied = [];
  const remaining = [...state.pending];
  const confirmedAt = new Date().toISOString();

  for (const entry of entries) {
    for (const taskId of entry.targets) {
      const { byId } = loadAllTasks();
      const task = byId.get(taskId);
      if (!task) continue;
      if (task.status === 'ready' && task.design_refs?.some((r) => r.includes('派单包'))) {
        log(`skip ${taskId}: already ready with package`);
        continue;
      }

      const sup = task.supervised_by || rules.agentSupervisors[task.agent];
      const patch = { status: 'ready' };
      if (sup) patch.supervised_by = sup;
      const noteLine = `${confirmedAt.slice(0, 10)} coordinator confirm approved_by=${approver} trigger=${entry.trigger}`;
      if (!dryRun) {
        updateTaskFields(taskId, patch, false);
        const pkgRel = generateDispatchPackage(
          { ...task, supervised_by: sup || task.supervised_by },
          rules,
          entry.cause_task,
        );
        const text = readRegistryText();
        const lines = text.split(/\r?\n/);
        const loc = findTaskBlock(lines, taskId);
        if (loc) {
          const block = lines.slice(loc.start, loc.end);
          upsertListItem(block, 'design_refs', pkgRel.replace(/\\/g, '/'));
          upsertField(block, 'note', noteLine);
          upsertField(block, 'dispatch_confirmed_by', approver);
          writeRegistryText(applyBlockUpdate(lines, loc, block).join('\n'));
        }
        const triggerText = buildDispatchTriggerText(entry);
        const confirmBy = resolveDispatchConfirmBy(
          { ...task, supervised_by: sup || task.supervised_by },
          rules,
          entry,
        );
        syncFeishuTask(taskId, false, {
          gate: 'confirmed',
          confirmBy,
          trigger: triggerText,
        });
      } else {
        log(`[DRY] confirm ${taskId} → ready + package (approved_by=${approver})`);
      }
      applied.push(taskId);
    }
    const idx = remaining.findIndex((p) => p.id === entry.id);
    if (idx >= 0) remaining.splice(idx, 1);
    if (!dryRun) {
      state.confirmed = state.confirmed || [];
      state.confirmed.push({
        ...entry,
        confirmed_at: confirmedAt,
        approved_by: approver,
        applied_tasks: entry.targets.filter((t) => applied.includes(t)),
      });
    }
  }

  if (!dryRun) {
    state.pending = remaining;
    savePending(state);
  }
  log(`confirm applied: ${applied.join(', ') || '(none)'} by ${approver}`);
  return { applied, approved_by: approver };
}

function parseCli(argv) {
  const out = {
    cmd: '',
    causeTask: '',
    dryRun: false,
    all: false,
    ids: [],
    approvedBy: '',
    help: false,
  };
  if (!argv.length) {
    out.help = true;
    return out;
  }
  out.cmd = argv[0];
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dry-run') out.dryRun = true;
    else if (a === '--all') out.all = true;
    else if (a === '--cause-task') out.causeTask = argv[++i];
    else if (a === '--ids') out.ids = argv[++i].split(',').map((s) => s.trim()).filter(Boolean);
    else if (a === '--approved-by') out.approvedBy = argv[++i];
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/coordinator-dispatch.mjs scan [--cause-task ID] [--dry-run]
  node scripts/coordinator-dispatch.mjs ready-engine [--dry-run]
  node scripts/coordinator-dispatch.mjs list
  node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:真名 [--dry-run]
  node scripts/coordinator-dispatch.mjs confirm --ids TASK1,TASK2 --approved-by 郭万迎 [--dry-run]

confirm 必填 --approved-by：须 team-roster 中 PM 或 can_supervise_agent=true 的监管人真名。`);
}

async function main() {
  const opts = parseCli(process.argv.slice(2));
  if (opts.help || !opts.cmd) {
    usage();
    process.exit(opts.help ? 0 : 2);
  }

  switch (opts.cmd) {
    case 'scan':
      scanTriggers(opts.causeTask, opts.dryRun);
      break;
    case 'ready-engine': {
      const r = runReadyEngine(opts.dryRun);
      console.log(`ready-engine: ${r.changes.length} change(s)`);
      r.changes.forEach((c) => console.log(`  ${c.id}: ${c.old} → ${c.new}`));
      break;
    }
    case 'list': {
      const st = loadPending();
      if (!st.pending.length) {
        console.log('No pending dispatch proposals.');
        break;
      }
      for (const p of st.pending) {
        console.log(`\n[${p.id}] trigger=${p.trigger} cause=${p.cause_task}`);
        p.targets.forEach((t) => console.log(`  → ${t}`));
      }
      console.log('\nConfirm（须 PM/监管人真名）：');
      console.log('  node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:郭万迎');
      break;
    }
    case 'confirm':
      if (!opts.approvedBy) {
        console.error('confirm 必须带 --approved-by human:真名（PM 或监管人）');
        usage();
        process.exit(2);
      }
      if (!opts.all && !opts.ids.length) {
        console.error('Use --all or --ids');
        process.exit(2);
      }
      confirmPending(opts);
      break;
    default:
      usage();
      process.exit(2);
  }
}

const __dispatchMain = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (__dispatchMain) {
  main().catch((e) => {
    console.error(e.message || e);
    process.exit(1);
  });
}
