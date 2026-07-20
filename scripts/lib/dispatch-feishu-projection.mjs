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
