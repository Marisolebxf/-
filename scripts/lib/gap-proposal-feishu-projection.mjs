#!/usr/bin/env node
/**
 * Outbound projection for registry-gap-proposals → Feishu Bitable.
 * Creates/updates draft rows for tasks not yet in task-registry.yaml.
 */

import { loadDotEnv } from './feishu-bitable-config.mjs';
import { syncOneTask, loadBitableConfig } from './board-task-status.mjs';
import {
  buildVirtualTaskFromProposal,
  loadGapProposals,
  saveGapProposals,
  upsertProposalFeishuMeta,
} from './registry-gap-suggest.mjs';

function gateForProposal(proposal) {
  if (proposal.status === 'accepted') return 'gap_accepted';
  if (proposal.status === 'rejected') return 'gap_rejected';
  return 'gap_proposed';
}

function triggerForProposal(proposal) {
  return `[${proposal.kind}] ${proposal.reason}`;
}

export async function projectGapProposalToFeishu(proposal, opts = {}) {
  const dryRun = !!opts.dryRun;
  const cfg = loadBitableConfig();
  const task = buildVirtualTaskFromProposal(proposal);
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
  upsertProposalFeishuMeta(proposal.id, meta, false);
  return { ...r, proposalId: proposal.id, taskId: task.id };
}

export async function projectGapProposalsToFeishu(opts = {}) {
  loadDotEnv();
  const status = opts.status || 'proposed';
  const doc = loadGapProposals();
  const items = (doc.proposals || []).filter((p) => !status || p.status === status);
  const results = [];
  for (const p of items) {
    try {
      const r = await projectGapProposalToFeishu(p, opts);
      results.push(r);
    } catch (e) {
      results.push({ ok: false, proposalId: p.id, error: e.message });
    }
  }
  return { count: items.length, results };
}

export async function refreshAcceptedGapFeishu(opts = {}) {
  loadDotEnv();
  const doc = loadGapProposals();
  const items = (doc.proposals || []).filter(
    (p) => ['accepted', 'rejected'].includes(p.status) && p.feishu_record_id,
  );
  const results = [];
  for (const p of items) {
    const r = await projectGapProposalToFeishu(p, opts);
    results.push(r);
  }
  return { count: items.length, results };
}
