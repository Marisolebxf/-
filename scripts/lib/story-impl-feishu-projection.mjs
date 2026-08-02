#!/usr/bin/env node
/**
 * Outbound projection for story-impl-proposals → Feishu Bitable.
 * Reuses 派单门控「待审建单 / 建单已采纳 / 建单已驳回」（与 registry-gap 同构）。
 * Only projects story_impl_leaf with skip_create=false.
 */

import { loadDotEnv } from './feishu-bitable-config.mjs';
import { syncOneTask, loadBitableConfig } from './board-task-status.mjs';
import {
  buildVirtualTaskFromStoryProposal,
  loadStoryImplProposals,
  upsertStoryImplFeishuMeta,
} from './story-impl-suggest.mjs';

function gateForProposal(proposal) {
  if (proposal.status === 'accepted') return 'gap_accepted';
  if (proposal.status === 'rejected') return 'gap_rejected';
  return 'gap_proposed';
}

function triggerForProposal(proposal) {
  const us = proposal.user_story ? ` user_story=${proposal.user_story}` : '';
  return `[故事拆单] ${proposal.module || ''}${us} · ${proposal.reason || proposal.kind}`;
}

export function isProjectableStoryImpl(proposal) {
  return (
    !!proposal &&
    proposal.kind === 'story_impl_leaf' &&
    !proposal.skip_create &&
    !!proposal.suggested_yaml?.trim()
  );
}

export async function projectStoryImplProposalToFeishu(proposal, opts = {}) {
  const dryRun = !!opts.dryRun;
  if (!isProjectableStoryImpl(proposal)) {
    return {
      ok: true,
      skipped: true,
      proposalId: proposal?.id,
      reason: 'not projectable (theme/skip_create)',
    };
  }

  const cfg = loadBitableConfig();
  const task = buildVirtualTaskFromStoryProposal(proposal);
  const gate = gateForProposal(proposal);
  const r = await syncOneTask(task, cfg, dryRun, {
    dispatchGate: gate,
    dispatchConfirmBy: proposal.reviewed_by || 'human:郭万迎',
    dispatchTrigger: triggerForProposal(proposal),
  });
  if (!r.ok || dryRun) return { ...r, proposalId: proposal.id, taskId: task.id };

  const meta = {
    feishu_projected_at: new Date().toISOString(),
  };
  if (r.recordId) meta.feishu_record_id = r.recordId;
  upsertStoryImplFeishuMeta(proposal.id, meta, false);
  return { ...r, proposalId: proposal.id, taskId: task.id };
}

export async function projectStoryImplProposalsToFeishu(opts = {}) {
  loadDotEnv();
  const status = opts.status || 'proposed';
  const doc = loadStoryImplProposals();
  const items = (doc.proposals || []).filter(
    (p) => (!status || p.status === status) && isProjectableStoryImpl(p),
  );
  const results = [];
  for (const p of items) {
    try {
      const r = await projectStoryImplProposalToFeishu(p, opts);
      results.push(r);
    } catch (e) {
      results.push({ ok: false, proposalId: p.id, error: e.message });
    }
  }
  return { count: items.length, results };
}
