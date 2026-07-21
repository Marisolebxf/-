#!/usr/bin/env node
/**
 * Suggest missing task-registry leaves (proposals only — never auto-merge).
 *
 *   node scripts/suggest-registry-tasks.mjs scan [--module ENT-MOD-SEARCH] [--phase all|definition|implementation]
 *   node scripts/suggest-registry-tasks.mjs scan --json
 *   node scripts/suggest-registry-tasks.mjs write [--module ...] [--dry-run]
 *   node scripts/suggest-registry-tasks.mjs list [--status proposed|accepted|rejected]
 *   node scripts/suggest-registry-tasks.mjs yaml [--module ENT-MOD-RISK]
 */

import { loadRules } from './coordinator-dispatch.mjs';
import {
  scanRegistryGaps,
  appendGapProposals,
  loadGapProposals,
  loadGapTemplates,
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
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/suggest-registry-tasks.mjs scan [--module ENT-MOD-SEARCH] [--phase all|definition|implementation]
  node scripts/suggest-registry-tasks.mjs write [--module ...] [--dry-run]
  node scripts/suggest-registry-tasks.mjs list [--status proposed]
  node scripts/suggest-registry-tasks.mjs yaml [--module ENT-MOD-RISK]

Proposals file: agent-delivery/registry-gap-proposals.yaml
Templates: agent-delivery/registry-gap-templates.yaml
Guide: agent-delivery/task-creation-guide.md §13`);
}

function runScan(opts) {
  const rules = loadRules();
  const gaps = scanRegistryGaps({
    modulePrefix: opts.module,
    phase: opts.phase,
    includeBrokenDeps: !opts.noBroken,
    includeUnlockTargets: !opts.noUnlock,
    confirmTriggers: rules.confirmTriggers,
    templates: loadGapTemplates(),
  });

  if (opts.json) {
    console.log(JSON.stringify({ count: gaps.length, gaps }, null, 2));
    return gaps;
  }

  if (!gaps.length) {
    console.log('No registry gaps found.');
    return gaps;
  }

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
  return gaps;
}

function runWrite(opts) {
  const gaps = runScan({ ...opts, json: false });
  if (!gaps.length) return;
  const { added, total } = appendGapProposals(gaps, { dryRun: opts.dryRun });
  if (opts.dryRun) {
    console.log(`[dry-run] would append ${added.length} proposal(s)`);
  } else {
    console.log(`Appended ${added.length} proposal(s) → registry-gap-proposals.yaml (total ${total})`);
  }
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
    console.log(`${p.status}\t${p.suggested_task_id}\t${p.kind}\t${p.reason}`);
  }
}

function runYaml(opts) {
  const gaps = scanRegistryGaps({
    modulePrefix: opts.module,
    phase: opts.phase,
    includeBrokenDeps: false,
    includeUnlockTargets: true,
    confirmTriggers: loadRules().confirmTriggers,
    templates: loadGapTemplates(),
  }).filter((g) => g.suggested_yaml);

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
