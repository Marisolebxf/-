#!/usr/bin/node
/**
 * Feishu webhook: gap_proposal_accept / gap_proposal_reject (Tier C).
 * Resolves both registry-gap-proposals and story-impl-proposals.
 * accept → merge suggested_yaml into task-registry + mark accepted + refresh 派单门控.
 */

import { fetchBitableRecord, feishuTenantToken } from './feishu-open-api.mjs';
import { projectGapProposalToFeishu } from './gap-proposal-feishu-projection.mjs';
import { projectStoryImplProposalToFeishu } from './story-impl-feishu-projection.mjs';
import {
  acceptGapProposalWithMerge,
  resolveGapProposal,
  reviewGapProposals,
} from './registry-gap-suggest.mjs';
import {
  acceptStoryImplWithMerge,
  resolveStoryImplProposal,
  reviewStoryImplProposals,
} from './story-impl-suggest.mjs';
import { resolveApprovedBy } from './dispatch-webhook-confirm.mjs';
import { validateConfirmApprover } from '../coordinator-dispatch.mjs';

/**
 * @returns {{ source: 'registry_gap'|'story_impl', proposal: object } | null}
 */
export function resolveCreateProposal(ref = {}) {
  const gap = resolveGapProposal(ref);
  if (gap) return { source: 'registry_gap', proposal: gap };
  const story = resolveStoryImplProposal(ref);
  if (story) return { source: 'story_impl', proposal: story };
  return null;
}

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

  const resolved = resolveCreateProposal({
    recordId: intent.recordId,
    taskId: intent.taskId || row?.task_id,
    proposalId: intent.proposalId || intent.rawBody?.proposal_id,
  });
  if (!resolved) {
    throw new Error(
      'gap_proposal_accept: proposal not found in registry-gap or story-impl (record_id / task_id)',
    );
  }
  const { source, proposal } = resolved;

  if (proposal.status === 'accepted') {
    return {
      action: 'noop',
      source,
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
    (source === 'story_impl' ? 'story_impl gap_proposal_accept webhook' : 'gap_proposal_accept webhook');

  let mergeResult;
  let reviewResult;
  let dgEnsure;
  if (source === 'story_impl') {
    ({ mergeResult, reviewResult, dgEnsure } = acceptStoryImplWithMerge(proposal, {
      dryRun: opts.dryRun,
      approvedBy,
      note,
      allowMissingDeps: true,
    }));
  } else {
    ({ mergeResult, reviewResult, dgEnsure } = acceptGapProposalWithMerge(proposal, {
      dryRun: opts.dryRun,
      approvedBy,
      note,
    }));
  }

  if (!opts.dryRun && reviewResult.updated.length) {
    const updated = reviewResult.updated[0];
    try {
      if (source === 'story_impl') {
        await projectStoryImplProposalToFeishu(updated, { dryRun: false });
      } else {
        await projectGapProposalToFeishu(updated, { dryRun: false });
      }
    } catch (e) {
      mergeResult.feishuProjectionError = e.message;
    }
  }

  // 自动创建的门3 → 投影飞书，派单门控「待确认」，确认人淮政玮
  if (!opts.dryRun && dgEnsure?.created?.length) {
    try {
      const { projectAutoCreatedDgToFeishu } = await import('./ensure-dg-gate3-feishu.mjs');
      mergeResult.dgFeishu = await projectAutoCreatedDgToFeishu(dgEnsure.created, {
        dryRun: false,
      });
    } catch (e) {
      mergeResult.dgFeishuError = e.message;
    }
  }

  return {
    action: 'gap_proposal_accept',
    source,
    proposalId: proposal.id,
    taskId: proposal.suggested_task_id,
    merge: mergeResult,
    dgEnsure,
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

  const resolved = resolveCreateProposal({
    recordId: intent.recordId,
    taskId: intent.taskId || row?.task_id,
    proposalId: intent.proposalId || intent.rawBody?.proposal_id,
  });
  if (!resolved) {
    throw new Error('gap_proposal_reject: proposal not found');
  }
  const { source, proposal } = resolved;

  if (proposal.status === 'rejected') {
    return {
      action: 'noop',
      source,
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
    (source === 'story_impl' ? 'story_impl gap_proposal_reject webhook' : 'gap_proposal_reject webhook');

  let updated;
  if (source === 'story_impl') {
    ({ updated } = reviewStoryImplProposals({
      action: 'reject',
      ids: [proposal.id],
      approvedBy,
      note,
      dryRun: opts.dryRun,
    }));
  } else {
    ({ updated } = reviewGapProposals({
      action: 'reject',
      ids: [proposal.id],
      approvedBy,
      note,
      dryRun: opts.dryRun,
    }));
  }

  if (!opts.dryRun && updated.length) {
    try {
      if (source === 'story_impl') {
        await projectStoryImplProposalToFeishu(updated[0], { dryRun: false });
      } else {
        await projectGapProposalToFeishu(updated[0], { dryRun: false });
      }
    } catch {
      // soft-fail
    }
  }

  return {
    action: 'gap_proposal_reject',
    source,
    proposalId: proposal.id,
    taskId: proposal.suggested_task_id,
    reviewed: updated.length,
    approved_by: approvedBy,
  };
}
