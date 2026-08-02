#!/usr/bin/env node
/**
 * Suggest missing task-registry leaves (proposals only — never auto-merge).
 *
 *   node scripts/suggest-registry-tasks.mjs scan [--module ENT-MOD-SEARCH] [--phase all|definition|implementation]
 *   node scripts/suggest-registry-tasks.mjs scan --json
 *   node scripts/suggest-registry-tasks.mjs write [--module ...] [--dry-run] [--project-feishu]
 *   node scripts/suggest-registry-tasks.mjs list [--status proposed|accepted|rejected]
 *   node scripts/suggest-registry-tasks.mjs yaml [--module ENT-MOD-RISK]
 *   node scripts/suggest-registry-tasks.mjs accept --ids ID [--approved-by human:真名] [--note ...]
 *   node scripts/suggest-registry-tasks.mjs reject --ids ID --approved-by human:真名 [--note ...]
 *   node scripts/suggest-registry-tasks.mjs merge --ids ID [--approved-by human:真名] [--note ...] [--dry-run]
 */

import { loadRules, validateConfirmApprover } from './coordinator-dispatch.mjs';
import { projectGapProposalToFeishu, projectGapProposalsToFeishu } from './lib/gap-proposal-feishu-projection.mjs';
import {
  scanRegistryGaps,
  appendGapProposals,
  loadGapProposals,
  loadGapTemplates,
  printGapSummary,
  reviewGapProposals,
  acceptGapProposalWithMerge,
  resolveGapProposal,
} from './lib/registry-gap-suggest.mjs';

function parseCli(argv) {
  const out = {
    cmd: 'scan',
    module: '',
    phase: 'all',
    status: 'proposed',
    json: false,
    dryRun: false,
    noUnlock: false,
    noBroken: false,
    noSummary: false,
    projectFeishu: false,
    all: false,
    ids: [],
    approvedBy: '',
    note: '',
    help: false,
  };
  if (!argv.length) return out;
  out.cmd = argv[0];
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--module' || a === '--prefix') out.module = argv[++i];
    else if (a === '--phase') out.phase = argv[++i];
    else if (a === '--status') out.status = argv[++i];
    else if (a === '--json') out.json = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--no-unlock') out.noUnlock = true;
    else if (a === '--no-broken') out.noBroken = true;
    else if (a === '--no-summary') out.noSummary = true;
    else if (a === '--project-feishu') out.projectFeishu = true;
    else if (a === '--all') out.all = true;
    else if (a === '--ids') out.ids = argv[++i].split(',').map((s) => s.trim()).filter(Boolean);
    else if (a === '--approved-by') out.approvedBy = argv[++i];
    else if (a === '--note') out.note = argv[++i];
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/suggest-registry-tasks.mjs scan [--module ENT-MOD-SEARCH] [--phase all|definition|implementation]
  node scripts/suggest-registry-tasks.mjs write [--module ...] [--dry-run] [--project-feishu]
  node scripts/suggest-registry-tasks.mjs list [--status proposed|accepted|rejected]
  node scripts/suggest-registry-tasks.mjs yaml [--module ENT-MOD-RISK]
  node scripts/suggest-registry-tasks.mjs accept --ids ID1,ID2 --approved-by human:真名 [--note ...]
  node scripts/suggest-registry-tasks.mjs merge --ids ID1 --approved-by human:真名 [--note ...] [--dry-run]
  node scripts/suggest-registry-tasks.mjs reject --all --approved-by human:真名 [--note ...]
  node scripts/suggest-registry-tasks.mjs project-feishu [--status proposed] [--dry-run]

Proposals file: agent-delivery/registry-gap-proposals.yaml
Templates: agent-delivery/registry-gap-templates.yaml
Guide: agent-delivery/task-creation-guide.md §13–§14`);
}

function scanGaps(opts) {
  const rules = loadRules();
  return scanRegistryGaps({
    modulePrefix: opts.module,
    phase: opts.phase,
    includeBrokenDeps: !opts.noBroken,
    includeUnlockTargets: !opts.noUnlock,
    confirmTriggers: rules.confirmTriggers,
    templates: loadGapTemplates(),
  });
}

function runScan(opts) {
  const gaps = scanGaps(opts);

  if (opts.json) {
    console.log(JSON.stringify({ count: gaps.length, gaps }, null, 2));
    if (!opts.noSummary) printGapSummary(gaps);
    return gaps;
  }

  if (!gaps.length) {
    console.log('No registry gaps found.');
  } else {
    console.log(`Found ${gaps.length} gap(s):\n`);
    for (const g of gaps) {
      console.log(`[${g.kind}] ${g.suggested_task_id}`);
      console.log(`  reason: ${g.reason}`);
      if (g.depends_on?.length) console.log(`  depends_on: ${g.depends_on.join(', ')}`);
      if (g.suggested_yaml) {
        console.log('  suggested_yaml:');
        for (const ln of g.suggested_yaml.split('\n')) console.log(`    ${ln}`);
      }
      console.log('');
    }
  }

  if (!opts.noSummary) printGapSummary(gaps);
  return gaps;
}

async function runWrite(opts) {
  const gaps = runScan({ ...opts, json: false, noSummary: true });
  if (!gaps.length) return;
  const { added, total } = appendGapProposals(gaps, { dryRun: opts.dryRun });
  if (opts.dryRun) {
    console.log(`[dry-run] would append ${added.length} proposal(s)`);
  } else {
    console.log(`Appended ${added.length} proposal(s) → registry-gap-proposals.yaml (total ${total})`);
  }
  if (opts.projectFeishu && added.length) {
    const r = await projectGapProposalsToFeishu({
      status: 'proposed',
      dryRun: opts.dryRun,
    });
    console.log(`project-feishu: ${r.count} row(s), ok=${r.results.filter((x) => x.ok).length}`);
  }
  if (!opts.noSummary) printGapSummary(gaps);
}

function runList(opts) {
  const doc = loadGapProposals();
  const items = (doc.proposals || []).filter((p) => !opts.status || p.status === opts.status);
  if (opts.json) {
    console.log(JSON.stringify({ count: items.length, proposals: items }, null, 2));
    return;
  }
  if (!items.length) {
    console.log('No proposals.');
    return;
  }
  for (const p of items) {
    console.log(
      `${p.status}\t${p.suggested_task_id}\t${p.kind}\t${p.id}\t${p.reason}`,
    );
  }
}

function runYaml(opts) {
  const gaps = scanGaps(opts).filter((g) => g.suggested_yaml);

  if (!gaps.length) {
    console.log('# No YAML suggestions');
    return;
  }
  console.log('# Paste into task-registry.yaml tasks: (PM review required)\n');
  for (const g of gaps) {
    console.log(`# ${g.reason}`);
    console.log(g.suggested_yaml);
    console.log('');
  }
}

async function runMergeAccept(opts) {
  if (!opts.approvedBy) {
    console.error('merge 必须带 --approved-by human:真名（PM 或监管人）');
    usage();
    process.exit(2);
  }
  if (!opts.ids.length) {
    console.error('merge 必须带 --ids（一条或多条 proposal id）');
    process.exit(2);
  }
  const approver = validateConfirmApprover(opts.approvedBy);
  for (const id of opts.ids) {
    const proposal = resolveGapProposal({ proposalId: id });
    if (!proposal) {
      console.error(`proposal not found: ${id}`);
      continue;
    }
    if (proposal.status !== 'proposed') {
      console.error(`skip ${id}: status=${proposal.status}`);
      continue;
    }
    const { mergeResult, reviewResult, dgEnsure } = acceptGapProposalWithMerge(proposal, {
      dryRun: opts.dryRun,
      approvedBy: approver,
      note: opts.note || 'merge CLI (Tier C local)',
    });
    console.log(
      `merge ${proposal.id} → ${proposal.suggested_task_id}: merge=${mergeResult.action}, accept=${reviewResult.updated.length}` +
        (dgEnsure?.created?.length ? ` | auto_dg=${dgEnsure.created.join(',')}` : ''),
    );
    if (dgEnsure?.ensured?.length) {
      for (const e of dgEnsure.ensured) {
        console.log(`  dg ${e.dgId}: ${e.action}${e.status ? ` (${e.status})` : ''}`);
      }
    }
    if (!opts.dryRun && dgEnsure?.created?.length) {
      try {
        const { projectAutoCreatedDgToFeishu } = await import('./lib/ensure-dg-gate3-feishu.mjs');
        await projectAutoCreatedDgToFeishu(dgEnsure.created, { dryRun: false });
      } catch (e) {
        console.warn(`  dg feishu soft-fail: ${e.message}`);
      }
    }
    if (!opts.dryRun && reviewResult.updated.length) {
      try {
        await projectGapProposalToFeishu(reviewResult.updated[0], { dryRun: false });
      } catch (e) {
        console.warn(`  project-feishu soft-fail: ${e.message}`);
      }
    }
  }
}

async function runReview(action, opts) {
  if (!opts.approvedBy) {
    console.error(`${action} 必须带 --approved-by human:真名（PM 或监管人）`);
    usage();
    process.exit(2);
  }
  if (!opts.all && !opts.ids.length) {
    console.error(`Use --all or --ids for ${action}`);
    process.exit(2);
  }
  const approver = validateConfirmApprover(opts.approvedBy);
  const { updated } = reviewGapProposals({
    action,
    ids: opts.ids,
    all: opts.all,
    approvedBy: approver,
    note: opts.note,
    dryRun: opts.dryRun,
  });
  console.log(`${action}: ${updated.length} proposal(s) by ${approver}`);
  for (const p of updated) {
    console.log(`  ${p.id} → ${p.status} (${p.suggested_task_id})`);
    if (p.registry_merged) console.log(`    registry merged: ${p.registry_task_id}`);
  }
  if (!opts.dryRun) {
    let projected = 0;
    for (const p of updated) {
      try {
        const r = await projectGapProposalToFeishu(p, { dryRun: false });
        if (r.ok) projected++;
      } catch (e) {
        console.warn(`  project-feishu soft-fail ${p.id}: ${e.message}`);
      }
    }
    console.log(`project-feishu: ${projected}/${updated.length} row(s) updated`);
  }
}

async function runProjectFeishu(opts) {
  const r = await projectGapProposalsToFeishu({
    status: opts.status,
    dryRun: opts.dryRun,
  });
  console.log(
    `project-feishu (${opts.status}): ${r.count} proposal(s), ok=${r.results.filter((x) => x.ok).length}`,
  );
  for (const x of r.results) {
    if (!x.ok && x.error) console.log(`  FAIL ${x.proposalId}: ${x.error}`);
    else if (x.dryRun) console.log(`  [DRY] ${x.taskId}`);
    else if (x.recordId) console.log(`  OK ${x.taskId} → ${x.recordId}`);
  }
}

async function main() {
  const opts = parseCli(process.argv.slice(2));
  if (opts.help) {
    usage();
    process.exit(0);
  }
  switch (opts.cmd) {
    case 'scan':
      runScan(opts);
      break;
    case 'write':
      await runWrite(opts);
      break;
    case 'list':
      runList(opts);
      break;
    case 'yaml':
      runYaml(opts);
      break;
    case 'accept':
      await runReview('accept', opts);
      break;
    case 'merge':
      await runMergeAccept(opts);
      break;
    case 'reject':
      await runReview('reject', opts);
      break;
    case 'project-feishu':
      await runProjectFeishu(opts);
      break;
    default:
      usage();
      process.exit(2);
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
