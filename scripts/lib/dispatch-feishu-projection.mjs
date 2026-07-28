#!/usr/bin/node
/**
 * Project dispatch gate fields to Feishu Bitable (outbound only; not inbound sync).
 */

import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { ORCH_ROOT } from './feishu-bitable-config.mjs';

const BOARD_SCRIPT = path.join(ORCH_ROOT, 'scripts', 'lib', 'board-task-status.mjs');

export function resolveDispatchConfirmBy(task, rules, entry) {
  const trigger = entry?.trigger || '';
  if (trigger === 'mayor-loop-dispatch' || trigger.startsWith('mayor-loop')) {
    return 'human:淮政玮';
  }
  if (trigger === 'impl-gate3-unlock' || trigger.startsWith('impl-gate3')) {
    return 'human:郭万迎';
  }
  return task.supervised_by || rules.agentSupervisors?.[task.agent] || 'human:郭万迎';
}

export function buildDispatchTriggerText(entry) {
  if (!entry) return '';
  return `${entry.trigger} ← ${entry.cause_task}`;
}

function syncDispatchFields(taskId, gateKey, confirmBy, triggerText, dryRun) {
  const args = [
    BOARD_SCRIPT,
    '--task-id',
    taskId,
    '--dispatch-only',
    '--dispatch-gate',
    gateKey,
  ];
  if (confirmBy) {
    args.push('--dispatch-confirm-by', confirmBy);
  }
  if (triggerText) {
    args.push('--dispatch-trigger', triggerText);
  }
  if (dryRun) args.push('--dry-run');

  const r = spawnSync(process.execPath, args, {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
    env: process.env,
  });
  if (r.status !== 0) {
    return { ok: false, error: r.stderr || r.stdout || 'board sync failed' };
  }
  return { ok: true };
}

export function projectPendingTargetsToFeishu(entries, rules, byId, dryRun) {
  const results = [];
  for (const entry of entries) {
    for (const taskId of entry.targets) {
      const task = byId.get(taskId);
      if (!task) continue;
      const confirmBy = resolveDispatchConfirmBy(task, rules, entry);
      const triggerText = buildDispatchTriggerText(entry);
      const r = syncDispatchFields(taskId, 'pending', confirmBy, triggerText, dryRun);
      results.push({ taskId, gate: 'pending', ...r });
    }
  }
  return results;
}

export function projectConfirmedTaskToFeishu(taskId, confirmBy, triggerText, dryRun) {
  return syncDispatchFields(taskId, 'confirmed', confirmBy, triggerText, dryRun);
}

export function projectRejectedTaskToFeishu(taskId, dryRun) {
  return syncDispatchFields(taskId, 'rejected', '', '', dryRun);
}

export function buildPendingTargetMap(pendingEntries) {
  const map = new Map();
  for (const entry of pendingEntries || []) {
    for (const taskId of entry.targets || []) {
      map.set(taskId, entry);
    }
  }
  return map;
}

function parseNoteDispatchMeta(note) {
  const text = note || '';
  const trigger = text.match(/trigger=(\S+)/)?.[1] || '';
  const cause = text.match(/cause_task=(\S+)/)?.[1] || '';
  const approvedRaw = text.match(/approved_by=(\S+)/)?.[1] || '';
  const approvedBy = approvedRaw
    ? approvedRaw.startsWith('human:')
      ? approvedRaw
      : `human:${approvedRaw}`
    : '';
  if (trigger && cause) return { triggerText: `${trigger} ← ${cause}`, approvedBy };
  if (trigger) return { triggerText: trigger, approvedBy };
  return { triggerText: '', approvedBy };
}

export function inferConfirmedTriggerText(task, rules) {
  const fromNote = parseNoteDispatchMeta(task.note);
  if (fromNote.triggerText) return fromNote.triggerText;

  const causes = task.depends_on || [];
  const cause =
    causes.find((d) => /PACK-L01|UX-L01|METRIC-OPEN-L01|PDR-G1|V1-HIFI|DG-G3/.test(d)) ||
    causes[0] ||
    '';

  for (const trigger of rules.confirmTriggers || []) {
    if (!trigger.taskDoneSuffix || !cause.endsWith(trigger.taskDoneSuffix)) continue;
    if ((trigger.unlockSuffixes || []).some((suf) => task.id.endsWith(suf))) {
      return `${trigger.id} ← ${cause}`;
    }
  }

  if (cause.endsWith('DG-G3') && rules.gate3?.enabled !== false) {
    return `${rules.gate3?.id || 'impl-gate3-unlock'} ← ${cause}`;
  }

  return cause ? `dispatch ← ${cause}` : '';
}

export function resolveDispatchProjectionForTask(task, pendingEntry, rules) {
  if (pendingEntry) {
    return {
      gate: 'pending',
      confirmBy: resolveDispatchConfirmBy(task, rules, pendingEntry),
      trigger: buildDispatchTriggerText(pendingEntry),
    };
  }

  const noteMeta = parseNoteDispatchMeta(task.note);
  const coordinatorDispatched =
    !!task.dispatch_confirmed_by ||
    /coordinator confirm/.test(task.note || '') ||
    /coordinator 派单 → ready/.test(task.note || '');

  if (
    coordinatorDispatched &&
    ['ready', 'claimed', 'in_progress', 'review', 'done', 'blocked'].includes(task.status)
  ) {
    return {
      gate: 'confirmed',
      confirmBy:
        task.dispatch_confirmed_by ||
        noteMeta.approvedBy ||
        task.supervised_by ||
        rules.agentSupervisors?.[task.agent] ||
        'human:郭万迎',
      trigger: inferConfirmedTriggerText(task, rules),
    };
  }

  return { gate: 'none', confirmBy: '', trigger: '' };
}

export function projectDispatchProjection(taskId, projection, dryRun) {
  return syncDispatchFields(
    taskId,
    projection.gate,
    projection.confirmBy,
    projection.trigger,
    dryRun,
  );
}

export async function backfillAllDispatchFields(opts = {}) {
  const { tasks, rules, pendingMap, dryRun = false, rateLimitMs = 200, onProgress } = opts;
  const summary = { none: 0, pending: 0, confirmed: 0, ok: 0, fail: 0, skipped: 0 };
  const failures = [];

  for (const task of tasks) {
    if (!task.id) continue;
    if (!task.record_id && !opts.syncWithoutRecordId) {
      summary.skipped++;
      continue;
    }

    const pendingEntry = pendingMap.get(task.id);
    const projection = resolveDispatchProjectionForTask(task, pendingEntry, rules);
    summary[projection.gate] = (summary[projection.gate] || 0) + 1;

    const r = projectDispatchProjection(task.id, projection, dryRun);
    if (r.ok) summary.ok++;
    else {
      summary.fail++;
      failures.push({ taskId: task.id, error: r.error, gate: projection.gate });
    }

    if (onProgress) onProgress({ taskId: task.id, projection, ...r });
    if (rateLimitMs && !dryRun) {
      await new Promise((resolve) => setTimeout(resolve, rateLimitMs));
    }
  }

  return { summary, failures };
}
