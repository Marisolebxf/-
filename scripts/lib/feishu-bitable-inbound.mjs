#!/usr/bin/env node
/**
 * Bitable → task-registry inbound (shared by pull sync + webhook handler).
 */

import fs from 'node:fs';
import path from 'node:path';
import {
  feishuTenantToken,
  listAllBitableRecords,
  readBitableRowFromFields,
} from './feishu-open-api.mjs';
import {
  ORCH_ROOT,
  applyBlockUpdate,
  findTaskBlock,
  isDoneStatus,
  loadAllTasks,
  readRegistryText,
  upsertField,
  fieldValueEnd,
  getScalar,
  writeRegistryText,
} from './task-registry-lib.mjs';

const STATUS_TRANSITIONS = {
  backlog: ['ready', 'blocked'],
  ready: ['claimed', 'blocked', 'backlog'],
  claimed: ['in_progress', 'ready', 'blocked'],
  in_progress: ['review', 'blocked'],
  review: ['done', 'in_progress', 'blocked'],
  blocked: ['backlog', 'ready'],
  done: [],
};

export function isValidStatusTransition(from, to) {
  if (!from || !to || from === to) return true;
  const allowed = STATUS_TRANSITIONS[from];
  if (!allowed) return true;
  return allowed.includes(to);
}

export function buildInboundChanges(row, task, cfg, opts = {}) {
  const validateMode = opts.validateTransitions || cfg.inbound?.validateTransitions || 'warn';
  const allowed = new Set(cfg.inbound?.allowedFields || ['status', 'claimed_by', 'sprint_id', 'title', 'priority']);
  const changes = {};
  const warnings = [];
  const rejects = [];

  if (allowed.has('status') && row.status_label) {
    const newSt = cfg.statusReverse[row.status_label];
    if (!newSt) {
      warnings.push(`unknown status label '${row.status_label}'`);
    } else if (newSt !== task.status) {
      const ok = isValidStatusTransition(task.status, newSt);
      if (!ok && validateMode === 'strict') {
        rejects.push(`illegal status ${task.status}->${newSt}`);
      } else {
        if (!ok && validateMode === 'warn') {
          warnings.push(`transition ${task.status}->${newSt}`);
        }
        changes.status = newSt;
      }
    }
  }

  if (allowed.has('claimed_by') && row.claimed_by) {
    const v = row.claimed_by;
    if (v && v !== task.claimed_by) changes.claimed_by = v;
  }

  if (allowed.has('sprint_id') && row.sprint_id && row.sprint_id !== task.sprint_id) {
    changes.sprint_id = row.sprint_id;
  }

  if (allowed.has('title') && row.title && row.title !== task.title) {
    changes.title = row.title;
  }

  if (allowed.has('priority')) {
    const regPri = (task.priority || '').trim();
    const bitPri = (row.priority || '').trim();
    if (bitPri !== regPri) {
      if (bitPri) changes.priority = bitPri;
      else changes.__remove_priority = true;
    }
  }

  if (row.record_id && task.record_id !== row.record_id) {
    changes.feishu_bitable_record_id = row.record_id;
  }

  return { changes, warnings, rejects };
}

function removeField(blockLines, key) {
  const re = new RegExp(`^\\s+${key}:\\s*`);
  for (let i = 0; i < blockLines.length; i++) {
    if (re.test(blockLines[i])) {
      const end = fieldValueEnd(blockLines, i);
      blockLines.splice(i, end - i);
      return true;
    }
  }
  return false;
}

export function applyInboundChanges(taskId, changes, opts = {}) {
  const { dryRun = false, source = 'feishu_bitable_webhook' } = opts;
  if (!changes || Object.keys(changes).length === 0) {
    return { applied: false, taskId, fields: [] };
  }

  const text = readRegistryText();
  const lines = text.split(/\r?\n/);
  const loc = findTaskBlock(lines, taskId);
  if (!loc) throw new Error(`Task not found: ${taskId}`);

  const block = lines.slice(loc.start, loc.end);
  const appliedFields = [];

  for (const [key, value] of Object.entries(changes)) {
    if (key === '__remove_priority') {
      if (!dryRun) removeField(block, 'priority');
      appliedFields.push('priority=(cleared)');
      continue;
    }
    if (!dryRun) upsertField(block, key, value);
    appliedFields.push(`${key}=${value}`);
  }

  if (!dryRun) {
    const today = new Date().toISOString().slice(0, 10);
    const audit = `${today} inbound ${source}: ${appliedFields.join(', ')}`;
    const prev = getScalar(block, 'note');
    const merged =
      prev && !prev.includes(audit)
        ? `${audit}\n${prev}`
        : prev || audit;
    upsertField(block, 'note', merged);
    writeRegistryText(applyBlockUpdate(lines, loc, block).join('\n'));
  }

  const statusBecameDone = changes.status && isDoneStatus(changes.status);
  return { applied: true, taskId, fields: appliedFields, statusBecameDone, newStatus: changes.status };
}

export function resolveTaskByRecordId(recordId) {
  const { byId } = loadAllTasks();
  for (const task of byId.values()) {
    if (task.record_id === recordId) return task;
  }
  return null;
}

export function appendInboundProposal(cfg, row, statusRegistry = 'backlog') {
  const rel = cfg.inbound.proposalsFile.replace(/\//g, path.sep);
  const full = path.join(ORCH_ROOT, rel);
  const dir = path.dirname(full);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  if (!fs.existsSync(full)) {
    fs.writeFileSync(
      full,
      `# Bitable 新增行提案队列\nversion: 1\nupdated: "${new Date().toISOString().slice(0, 10)}"\nproposals: []\n`,
      'utf8',
    );
  }
  const tid = row.task_id?.trim() || `PROPOSE-${row.record_id}`;
  const entry = `  - record_id: "${row.record_id}"\n    task_id: "${tid}"\n    title: "${(row.title || '').replace(/"/g, '\\"')}"\n    status: "${statusRegistry}"\n    sprint_id: "${row.sprint_id || ''}"\n    claimed_by: "${row.claimed_by || ''}"\n    captured_at: "${new Date().toISOString()}"\n    source: feishu_bitable_webhook\n`;
  let raw = fs.readFileSync(full, 'utf8');
  if (/proposals:\s*\[\]/.test(raw)) {
    raw = raw.replace(/proposals:\s*\[\]/, `proposals:\n${entry}`);
  } else {
    raw = `${raw.trimEnd()}\n${entry}`;
  }
  fs.writeFileSync(full, raw.endsWith('\n') ? raw : `${raw}\n`, 'utf8');
  return tid;
}

export function processInboundRow(row, cfg, opts = {}) {
  const validateMode = opts.validateTransitions || cfg.webhook?.validateTransitions || cfg.inbound.validateTransitions;
  const taskId = (row.task_id || '').trim();
  const pattern = new RegExp(cfg.inbound.taskIdPattern);

  if (!taskId) {
    if (cfg.inbound.newTasks === 'queue') {
      if (!opts.dryRun) appendInboundProposal(cfg, row);
      return { action: 'queued', reason: 'empty task_id' };
    }
    return { action: 'skipped', reason: 'empty task_id' };
  }

  if (!pattern.test(taskId)) {
    return { action: 'skipped', reason: 'invalid task_id format', taskId };
  }

  const { byId } = loadAllTasks();
  const task = byId.get(taskId);
  if (!task) {
    if (cfg.inbound.newTasks === 'queue') {
      const st = row.status_label && cfg.statusReverse[row.status_label]
        ? cfg.statusReverse[row.status_label]
        : 'backlog';
      if (!opts.dryRun) appendInboundProposal(cfg, row, st);
      return { action: 'queued', reason: 'unknown task', taskId };
    }
    return { action: 'skipped', reason: 'unknown task', taskId };
  }

  const { changes, warnings, rejects } = buildInboundChanges(row, task, cfg, {
    validateTransitions: validateMode,
  });

  if (rejects.length) {
    return { action: 'rejected', taskId, rejects, warnings };
  }
  if (Object.keys(changes).length === 0) {
    return { action: 'noop', taskId, warnings };
  }

  const applyResult = applyInboundChanges(taskId, changes, {
    dryRun: opts.dryRun,
    source: opts.source || 'feishu_bitable_webhook',
  });

  return { action: 'updated', taskId, ...applyResult, warnings };
}

/** Full-table inbound pull (Cron / fallback when Webhook missed events). */
export async function runInboundPullAll(cfg, opts = {}) {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required for inbound pull');
  }
  if (!cfg.inbound.enabled) {
    return { action: 'skipped', reason: 'inbound disabled' };
  }

  const token = await feishuTenantToken(appId, appSecret);
  const records = await listAllBitableRecords(cfg, token);
  const stats = { total: records.length, updated: 0, noop: 0, skipped: 0, queued: 0, rejected: 0 };

  for (const rec of records) {
    const row = readBitableRowFromFields(rec.fields, cfg);
    if (!row) {
      stats.skipped++;
      continue;
    }
    row.record_id = rec.record_id || '';
    const result = processInboundRow(row, cfg, {
      dryRun: opts.dryRun,
      validateTransitions: opts.validateTransitions || cfg.inbound.validateTransitions,
      source: 'feishu_bitable_cron_inbound',
    });
    if (result.action === 'updated') stats.updated++;
    else if (result.action === 'noop') stats.noop++;
    else if (result.action === 'queued') stats.queued++;
    else if (result.action === 'rejected') stats.rejected++;
    else stats.skipped++;
  }
  return stats;
}
