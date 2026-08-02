#!/usr/bin/env node
/**
 * Suggest story-driven implementation leaves after Gate-1 PDR.
 * Feishu Tier C: 派单门控「待审建单」→「建单已采纳」= merge registry backlog.
 *
 *   node scripts/suggest-story-impl-tasks.mjs scan [--module NAME] [--all]
 *   node scripts/suggest-story-impl-tasks.mjs write [--module ...] [--dry-run] [--all] [--project-feishu]
 *   node scripts/suggest-story-impl-tasks.mjs list [--status proposed]
 *   node scripts/suggest-story-impl-tasks.mjs yaml [--module ...] [--all]
 *   node scripts/suggest-story-impl-tasks.mjs project-feishu [--status proposed] [--dry-run]
 *   node scripts/suggest-story-impl-tasks.mjs accept --ids ID --approved-by human:真名
 *   node scripts/suggest-story-impl-tasks.mjs reject --ids ID --approved-by human:真名
 *   node scripts/suggest-story-impl-tasks.mjs merge --ids ID --approved-by human:真名 [--dry-run]
 *
 * NEVER marks ready; ready still requires gate3 + confirm.
 */
import { validateConfirmApprover } from './coordinator-dispatch.mjs';
import {
  projectStoryImplProposalToFeishu,
  projectStoryImplProposalsToFeishu,
} from './lib/story-impl-feishu-projection.mjs';
import {
  scanStoryImplGaps,
  appendStoryImplProposals,
  loadStoryImplProposals,
  printStoryImplSummary,
  reviewStoryImplProposals,
  acceptStoryImplWithMerge,
  resolveStoryImplProposal,
  STORY_IMPL_PROPOSALS_PATH,
} from './lib/story-impl-suggest.mjs';

function parseCli(argv) {
  const out = {
    cmd: 'scan',
    module: '',
    status: 'proposed',
    json: false,
    dryRun: false,
    all: false,
    projectFeishu: false,
    ids: [],
    approvedBy: '',
    note: '',
    help: false,
  };
  if (!argv.length) return out;
  out.cmd = argv[0];
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--module' || a === '-m') out.module = argv[++i] || '';
    else if (a === '--status') out.status = argv[++i] || '';
    else if (a === '--json') out.json = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--all') out.all = true;
    else if (a === '--project-feishu') out.projectFeishu = true;
    else if (a === '--ids') out.ids = (argv[++i] || '').split(',').map((s) => s.trim()).filter(Boolean);
    else if (a === '--approved-by') out.approvedBy = argv[++i] || '';
    else if (a === '--note') out.note = argv[++i] || '';
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/suggest-story-impl-tasks.mjs scan [--module NAME] [--all]
  node scripts/suggest-story-impl-tasks.mjs write [--module NAME] [--dry-run] [--all] [--project-feishu]
  node scripts/suggest-story-impl-tasks.mjs list [--status proposed]
  node scripts/suggest-story-impl-tasks.mjs yaml [--module NAME] [--all]
  node scripts/suggest-story-impl-tasks.mjs project-feishu [--status proposed] [--dry-run]
  node scripts/suggest-story-impl-tasks.mjs accept --ids ID --approved-by human:真名 [--note ...]
  node scripts/suggest-story-impl-tasks.mjs reject --ids ID --approved-by human:真名 [--note ...]
  node scripts/suggest-story-impl-tasks.mjs merge --ids ID --approved-by human:真名 [--dry-run]

  --all            含已有 implementation_tasks 的故事
  --project-feishu write 后投影飞书「待审建单」

Feishu flow:
  待审建单 → 建单已采纳 (Webhook gap_proposal_accept) → registry backlog
  → 门3 后 待确认 → 已确认 → ready

Proposals: agent-delivery/story-impl-proposals.yaml
Guide: agent-delivery/task-creation-guide.md §16`);
}

function runScan(opts) {
  const gaps = scanStoryImplGaps({ moduleFilter: opts.module, includeCovered: opts.all });
  if (opts.json) {
    console.log(JSON.stringify({ count: gaps.length, gaps }, null, 2));
    return gaps;
  }
  if (!gaps.length) {
    console.log('No story-impl gaps (all stories covered or no matching module).');
    return gaps;
  }
  console.log(`Found ${gaps.length} proposal(s):\n`);
  for (const g of gaps) {
    console.log(`[${g.kind}] ${g.suggested_task_id}`);
    console.log(`  module: ${g.module}`);
    console.log(`  reason: ${g.reason}`);
    if (g.user_story) console.log(`  user_story: ${g.user_story}`);
    if (g.themes?.length) {
      console.log(
        `  themes: ${g.themes.map((t) => `${t.id}[${(t.stories || []).join(',')}]`).join(' | ')}`,
      );
    }
    if (g.suggested_yaml) {
      console.log('  suggested_yaml:');
      for (const ln of g.suggested_yaml.split('\n')) console.log(`    ${ln}`);
    }
    console.log('');
  }
  printStoryImplSummary(gaps);
  return gaps;
}

async function runWrite(opts) {
  const gaps = runScan({ ...opts, json: false });
  if (!gaps.length) return;
  const { added, total } = appendStoryImplProposals(gaps, { dryRun: opts.dryRun });
  if (opts.dryRun) {
    console.log(`\n[dry-run] would append/refresh ${added.length} proposal(s) (total ${total})`);
  } else {
    console.log(`\nAppended ${added.length} new proposal(s) → ${STORY_IMPL_PROPOSALS_PATH} (total ${total})`);
  }
  if (opts.projectFeishu) {
    const r = await projectStoryImplProposalsToFeishu({
      status: 'proposed',
      dryRun: opts.dryRun,
    });
    console.log(
      `project-feishu: ${r.count} row(s), ok=${r.results.filter((x) => x.ok && !x.skipped).length}, skipped=${r.results.filter((x) => x.skipped).length}`,
    );
  }
}

function runList(opts) {
  const doc = loadStoryImplProposals();
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
    const gate = p.skip_create ? 'n/a' : p.status === 'proposed' ? '待审建单' : p.status;
    console.log(
      `${p.status}\t${gate}\t${p.suggested_task_id}\t${p.kind}\t${p.id}\t${p.module}`,
    );
  }
}

function runYaml(opts) {
  const gaps = scanStoryImplGaps({
    moduleFilter: opts.module,
    includeCovered: opts.all,
  }).filter((g) => g.suggested_yaml);
  if (!gaps.length) {
    console.log('# No YAML suggestions');
    return;
  }
  console.log('# Paste into task-registry.yaml tasks: (or use merge / 飞书建单已采纳)\n');
  for (const g of gaps) {
    console.log(`# ${g.reason}`);
    console.log(g.suggested_yaml);
    console.log('');
  }
}

async function runProjectFeishu(opts) {
  const r = await projectStoryImplProposalsToFeishu({
    status: opts.status,
    dryRun: opts.dryRun,
  });
  console.log(
    `project-feishu (${opts.status}): ${r.count} proposal(s), ok=${r.results.filter((x) => x.ok && !x.skipped).length}`,
  );
  for (const x of r.results) {
    if (x.skipped) console.log(`  SKIP ${x.proposalId}: ${x.reason}`);
    else if (!x.ok && x.error) console.log(`  FAIL ${x.proposalId}: ${x.error}`);
    else if (x.dryRun) console.log(`  [DRY] ${x.taskId}`);
    else if (x.recordId) console.log(`  OK ${x.taskId} → ${x.recordId}`);
    else console.log(`  OK ${x.taskId || x.proposalId}`);
  }
}

async function runReview(action, opts) {
  if (!opts.approvedBy) {
    console.error(`${action} 必须带 --approved-by human:真名`);
    usage();
    process.exit(2);
  }
  if (!opts.ids.length && !opts.all) {
    console.error(`Use --ids or --all for ${action}`);
    process.exit(2);
  }
  const approver = validateConfirmApprover(opts.approvedBy);
  const { updated } = reviewStoryImplProposals({
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
    if (!opts.dryRun) {
      try {
        await projectStoryImplProposalToFeishu(p, { dryRun: false });
      } catch (e) {
        console.warn(`  project-feishu soft-fail: ${e.message}`);
      }
    }
  }
}

async function runMerge(opts) {
  if (!opts.approvedBy) {
    console.error('merge 必须带 --approved-by human:真名');
    usage();
    process.exit(2);
  }
  if (!opts.ids.length) {
    console.error('merge 必须带 --ids');
    process.exit(2);
  }
  const approver = validateConfirmApprover(opts.approvedBy);
  for (const id of opts.ids) {
    const proposal = resolveStoryImplProposal({ proposalId: id, taskId: id });
    if (!proposal) {
      console.error(`proposal not found: ${id}`);
      continue;
    }
    if (proposal.status !== 'proposed') {
      console.error(`skip ${id}: status=${proposal.status}`);
      continue;
    }
    const { mergeResult, reviewResult } = acceptStoryImplWithMerge(proposal, {
      dryRun: opts.dryRun,
      approvedBy: approver,
      note: opts.note || 'merge CLI (story-impl Tier C local)',
      allowMissingDeps: true,
    });
    console.log(
      `merge ${proposal.id} → ${proposal.suggested_task_id}: merge=${mergeResult.action}, accept=${reviewResult.updated.length}` +
        (mergeResult.missingDeps?.length ? ` (deps_pending=${mergeResult.missingDeps.join(',')})` : '') +
        (mergeResult.dgEnsure?.created?.length
          ? ` | auto_dg=${mergeResult.dgEnsure.created.join(',')}`
          : ''),
    );
    if (mergeResult.dgEnsure?.ensured?.length) {
      for (const e of mergeResult.dgEnsure.ensured) {
        console.log(`  dg ${e.dgId}: ${e.action}${e.status ? ` (${e.status})` : ''}`);
      }
    }
    if (!opts.dryRun && mergeResult.dgEnsure?.created?.length) {
      try {
        const { projectAutoCreatedDgToFeishu } = await import('./lib/ensure-dg-gate3-feishu.mjs');
        const r = await projectAutoCreatedDgToFeishu(mergeResult.dgEnsure.created, {
          dryRun: false,
        });
        console.log(
          `  dg feishu: ok=${r.results.filter((x) => x.ok).length}/${r.count}`,
        );
      } catch (e) {
        console.warn(`  dg feishu soft-fail: ${e.message}`);
      }
    }
    if (!opts.dryRun && reviewResult.updated.length) {
      try {
        await projectStoryImplProposalToFeishu(reviewResult.updated[0], { dryRun: false });
      } catch (e) {
        console.warn(`  project-feishu soft-fail: ${e.message}`);
      }
    }
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
    case 'project-feishu':
      await runProjectFeishu(opts);
      break;
    case 'accept':
      await runReview('accept', opts);
      break;
    case 'reject':
      await runReview('reject', opts);
      break;
    case 'merge':
      await runMerge(opts);
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
