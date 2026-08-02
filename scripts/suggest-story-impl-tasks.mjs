#!/usr/bin/env node
/**
 * Suggest story-driven implementation leaves after Gate-1 PDR (proposals only).
 *
 *   node scripts/suggest-story-impl-tasks.mjs scan [--module E1-企业查询|SEARCH]
 *   node scripts/suggest-story-impl-tasks.mjs write [--module ...] [--dry-run]
 *   node scripts/suggest-story-impl-tasks.mjs list [--status proposed]
 *   node scripts/suggest-story-impl-tasks.mjs yaml [--module ...]
 *
 * Outputs: agent-delivery/story-impl-proposals.yaml
 * NEVER writes task-registry.yaml.
 */
import {
  scanStoryImplGaps,
  appendStoryImplProposals,
  loadStoryImplProposals,
  printStoryImplSummary,
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
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/suggest-story-impl-tasks.mjs scan [--module NAME] [--all]
  node scripts/suggest-story-impl-tasks.mjs write [--module NAME] [--dry-run] [--all]
  node scripts/suggest-story-impl-tasks.mjs list [--status proposed]
  node scripts/suggest-story-impl-tasks.mjs yaml [--module NAME] [--all]

  --all   含已有 implementation_tasks 的故事（默认只扫未覆盖）

Proposals: agent-delivery/story-impl-proposals.yaml
Templates: agent-delivery/story-impl-templates.yaml
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
      console.log(`  themes: ${g.themes.map((t) => `${t.id}[${(t.stories || []).join(',')}]`).join(' | ')}`);
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

function runWrite(opts) {
  const gaps = runScan({ ...opts, json: false });
  if (!gaps.length) return;
  const { added, total } = appendStoryImplProposals(gaps, { dryRun: opts.dryRun });
  if (opts.dryRun) {
    console.log(`\n[dry-run] would append ${added.length} proposal(s)`);
  } else {
    console.log(`\nAppended ${added.length} new proposal(s) → ${STORY_IMPL_PROPOSALS_PATH} (total ${total})`);
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
    console.log(`${p.status}\t${p.suggested_task_id}\t${p.kind}\t${p.id}\t${p.module}`);
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
  console.log('# Paste into task-registry.yaml tasks: (PM review required; status=backlog)\n');
  for (const g of gaps) {
    console.log(`# ${g.reason}`);
    console.log(g.suggested_yaml);
    console.log('');
  }
}

function main() {
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
      runWrite(opts);
      break;
    case 'list':
      runList(opts);
      break;
    case 'yaml':
      runYaml(opts);
      break;
    default:
      usage();
      process.exit(2);
  }
}

main();
