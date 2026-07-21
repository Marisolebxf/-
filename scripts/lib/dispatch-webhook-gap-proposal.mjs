#!/usr/bin/node
/**
 * Feishu webhook: gap_proposal_accept / gap_proposal_reject (Tier C).
 * accept → merge suggested_yaml into task-registry + reviewGapProposals + git push + scan.
 */

import { fetchBitableRecord, feishuTenantToken } from './feishu-open-api.mjs';
import { projectGapProposalToFeishu } from './gap-proposal-feishu-projection.mjs';
import {
  acceptGapProposalWithMerge,
  resolveGapProposal,
  reviewGapProposals,
} from './registry-gap-suggest.mjs';
import { resolveApprovedBy } from './dispatch-webhook-confirm.mjs';
import { validateConfirmApprover } from '../coordinator-dispatch.mjs';

export async function handleGapProposalAcceptIntent(cfg, intent, opts = {}) {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required for gap_proposal_accept');
  }

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
  }

  const acceptedLabel = cfg.dispatchGateMap?.gap_accepted || '建单已采纳';
  if (row?.dispatch_gate_label && row.dispatch_gate_label !== acceptedLabel) {
    throw new Error(
      `gap_proposal_accept: 派单门控须为「${acceptedLabel}」，当前为「${row.dispatch_gate_label || '(空)'}」`,
    );
  }

  const proposal = resolveGapProposal({
    recordId: intent.recordId,
    taskId: intent.taskId || row?.task_id,
    proposalId: intent.proposalId || intent.rawBody?.proposal_id,
  });
  if (!proposal) {
    throw new Error('gap_proposal_accept: proposal not found (record_id / task_id)');
  }

  if (proposal.status === 'accepted') {
    return {
      action: 'noop',
      proposalId: proposal.id,
      taskId: proposal.suggested_task_id,
      reason: proposal.registry_merged ? 'already accepted and merged' : 'already accepted',
    };
  }
  if (proposal.status !== 'proposed') {
    throw new Error(`gap_proposal_accept: proposal status is ${proposal.status}, expected proposed`);
  }

  const approvedByRaw = resolveApprovedBy(intent.rawBody || {}, row);
  if (!approvedByRaw) {
    throw new Error(
      'gap_proposal_accept: 缺少 approved_by（请在飞书自动化 body 加 approved_by 或 operator_open_id）',
    );
  }
  const approvedBy = validateConfirmApprover(approvedByRaw);
  const note =
    intent.note ||
    intent.rawBody?.note ||
    intent.rawBody?.review_note ||
    'gap_proposal_accept webhook';

  const { mergeResult, reviewResult } = acceptGapProposalWithMerge(proposal, {
    dryRun: opts.dryRun,
    approvedBy,
    note,
  });

  if (!opts.dryRun && reviewResult.updated.length) {
    const updated = reviewResult.updated[0];
    try {
      await projectGapProposalToFeishu(updated, { dryRun: false });
    } catch (e) {
      // registry merge succeeded; feishu projection is soft-fail
      mergeResult.feishuProjectionError = e.message;
    }
  }

  return {
    action: 'gap_proposal_accept',
    proposalId: proposal.id,
    taskId: proposal.suggested_task_id,
    merge: mergeResult,
    reviewed: reviewResult.updated.length,
    approved_by: approvedBy,
  };
}

export async function handleGapProposalRejectIntent(cfg, intent, opts = {}) {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required for gap_proposal_reject');
  }

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
  }

  const rejectedLabel = cfg.dispatchGateMap?.gap_rejected || '建单已驳回';
  if (row?.dispatch_gate_label && row.dispatch_gate_label !== rejectedLabel) {
    throw new Error(
      `gap_proposal_reject: 派单门控须为「${rejectedLabel}」，当前为「${row.dispatch_gate_label || '(空)'}」`,
    );
  }

  const proposal = resolveGapProposal({
    recordId: intent.recordId,
    taskId: intent.taskId || row?.task_id,
    proposalId: intent.proposalId || intent.rawBody?.proposal_id,
  });
  if (!proposal) {
    throw new Error('gap_proposal_reject: proposal not found');
  }

  if (proposal.status === 'rejected') {
    return {
      action: 'noop',
      proposalId: proposal.id,
      taskId: proposal.suggested_task_id,
      reason: 'already rejected',
    };
  }
  if (proposal.status !== 'proposed') {
    throw new Error(`gap_proposal_reject: proposal status is ${proposal.status}, expected proposed`);
  }

  const approvedByRaw = resolveApprovedBy(intent.rawBody || {}, row);
  if (!approvedByRaw) {
    throw new Error('gap_proposal_reject: 缺少 approved_by');
  }
  const approvedBy = validateConfirmApprover(approvedByRaw);
  const note =
    intent.note ||
    intent.rawBody?.note ||
    intent.rawBody?.review_note ||
    'gap_proposal_reject webhook';

  const { updated } = reviewGapProposals({
    action: 'reject',
    ids: [proposal.id],
    approvedBy,
    note,
    dryRun: opts.dryRun,
  });

  if (!opts.dryRun && updated.length) {
    try {
      await projectGapProposalToFeishu(updated[0], { dryRun: false });
    } catch (e) {
      // soft-fail
    }
  }

  return {
    action: 'gap_proposal_reject',
    proposalId: proposal.id,
    taskId: proposal.suggested_task_id,
    reviewed: updated.length,
    approved_by: approvedBy,
  };
}
