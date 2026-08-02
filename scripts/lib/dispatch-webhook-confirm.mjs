#!/usr/bin/node
/**
 * Feishu webhook: action=dispatch_confirm → coordinator confirm pipeline.
 */

import fs from 'node:fs';
import path from 'node:path';
import { loadBitableConfig, ORCH_ROOT } from './feishu-bitable-config.mjs';
import { fetchBitableRecord, feishuTenantToken } from './feishu-open-api.mjs';
import { resolveTaskByRecordId } from './feishu-bitable-inbound.mjs';
import { loadAllTasks } from './task-registry-lib.mjs';
import { projectRejectedTaskToFeishu } from './dispatch-feishu-projection.mjs';
import {
  confirmPending,
  loadPending,
  rejectPendingForTask,
  validateConfirmApprover,
} from '../coordinator-dispatch.mjs';

const USER_MAP_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-user-map.yaml');

function loadOpenIdToRegistry() {
  const map = {};
  if (!fs.existsSync(USER_MAP_PATH)) return map;
  const raw = fs.readFileSync(USER_MAP_PATH, 'utf8');
  const blocks = raw.split(/(?=\n\s*- name:)/);
  for (const b of blocks) {
    const openId = (b.match(/feishu_open_id:\s*(\S+)/) || [])[1]?.trim();
    const reg = (b.match(/registry_name:\s*(\S+)/) || [])[1]?.trim();
    if (openId && reg) map[openId] = reg;
  }
  return map;
}

function normalizeHumanPrefix(value) {
  const v = (value || '').trim();
  if (!v) return '';
  if (v.startsWith('human:')) return v;
  if (v.startsWith('@')) return `human:${v.slice(1)}`;
  return `human:${v}`;
}

export function resolveApprovedBy(body, row) {
  const direct =
    body.approved_by ||
    body.approvedBy ||
    body.confirmed_by ||
    body.confirmedBy ||
    '';
  if (direct) return normalizeHumanPrefix(direct);

  const openId = body.operator_open_id || body.operatorOpenId || body.open_id || '';
  if (openId) {
    const reg = loadOpenIdToRegistry()[openId];
    if (reg) return normalizeHumanPrefix(reg);
  }

  if (row?.dispatch_confirm_by) {
    return normalizeHumanPrefix(row.dispatch_confirm_by);
  }
  return '';
}

function findPendingEntryForTask(taskId) {
  const state = loadPending();
  return state.pending.find((e) => e.targets.includes(taskId)) || null;
}

function assertNotGapProposalRow(cfg, row, actionName) {
  if (!row?.dispatch_gate_label) return;
  const m = cfg.dispatchGateMap || {};
  const labels = [m.gap_proposed, m.gap_accepted, m.gap_rejected].filter(Boolean);
  if (!labels.includes(row.dispatch_gate_label)) return;
  const hint =
    row.dispatch_gate_label === (m.gap_accepted || '建单已采纳')
      ? 'gap_proposal_accept'
      : row.dispatch_gate_label === (m.gap_rejected || '建单已驳回')
        ? 'gap_proposal_reject'
        : 'gap_proposal_accept / gap_proposal_reject';
  throw new Error(
    `${actionName}: 此行是建单建议（${row.dispatch_gate_label}），请用 action=${hint}，不要用 ${actionName}`,
  );
}

export async function handleDispatchConfirmIntent(cfg, intent, opts = {}) {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required for dispatch_confirm');
  }

  let taskId = intent.taskId;
  let row = null;

  if (intent.recordId) {
    const token = await feishuTenantToken(appId, appSecret);
    row = await fetchBitableRecord(
      cfg,
      token,
      intent.recordId,
      intent.appToken || cfg.appToken,
      intent.tableId || cfg.tableId,
    );
    if (!taskId) taskId = row.task_id;
  }

  if (!taskId && intent.recordId) {
    const byRec = resolveTaskByRecordId(intent.recordId);
    if (byRec) taskId = byRec.id;
  }
  if (!taskId) throw new Error('dispatch_confirm: missing task_id');

  assertNotGapProposalRow(cfg, row, 'dispatch_confirm');

  const { byId: registryById } = loadAllTasks();
  if (!registryById.has(taskId)) {
    throw new Error(
      `dispatch_confirm: ${taskId} 不在 task-registry；若是建单建议请用 action=gap_proposal_accept`,
    );
  }

  const confirmedLabel = cfg.dispatchGateMap?.confirmed || '已确认';
  if (row?.dispatch_gate_label && row.dispatch_gate_label !== confirmedLabel) {
    throw new Error(
      `dispatch_confirm: 派单门控须为「${confirmedLabel}」，当前为「${row.dispatch_gate_label || '(空)'}」`,
    );
  }

  const approvedByRaw = resolveApprovedBy(intent.rawBody || {}, row);
  if (!approvedByRaw) {
    throw new Error(
      'dispatch_confirm: 缺少 approved_by（请在飞书自动化 body 加 approved_by 或 operator_open_id）',
    );
  }
  const approvedBy = validateConfirmApprover(approvedByRaw);

  const pendingEntry = findPendingEntryForTask(taskId);
  if (!pendingEntry) {
    const task = registryById.get(taskId);
    if (
      task?.status === 'ready' &&
      (task.design_refs || []).some(
        (r) => typeof r === 'string' && (r.includes('派单包') || r.includes('派单条')),
      )
    ) {
      return {
        action: 'noop',
        taskId,
        reason: 'already confirmed',
        approved_by: approvedBy,
      };
    }
    throw new Error(`dispatch_confirm: ${taskId} 不在 pending 队列`);
  }

  const result = confirmPending({
    ids: [taskId],
    all: false,
    dryRun: opts.dryRun,
    approvedBy,
  });

  return {
    action: 'dispatch_confirm',
    taskId,
    applied: result.applied,
    approved_by: result.approved_by,
  };
}

export async function handleDispatchRejectIntent(cfg, intent, opts = {}) {
  let taskId = intent.taskId;
  if (!taskId && intent.recordId) {
    const byRec = resolveTaskByRecordId(intent.recordId);
    if (byRec) taskId = byRec.id;
  }
  if (!taskId) throw new Error('dispatch_reject: missing task_id');

  const approvedByRaw = resolveApprovedBy(intent.rawBody || {}, null);
  if (approvedByRaw) validateConfirmApprover(approvedByRaw);

  const removed = rejectPendingForTask(taskId, opts.dryRun);
  if (!opts.dryRun) projectRejectedTaskToFeishu(taskId, false);

  return { action: 'dispatch_reject', taskId, removed };
}
