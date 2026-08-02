#!/usr/bin/env node
/**
 * Gate-1 PDR → story library ingest + story-impl proposals (one shot).
 *
 *   node scripts/pdr-gate1-story-pipeline.mjs --module E1-企业查询
 *   node scripts/pdr-gate1-story-pipeline.mjs --module SEARCH --dry-run
 *
 * Steps:
 *   1) extract-user-stories --module --write (skipped if --dry-run)
 *   2) suggest-story-impl-tasks write --module
 *
 * Does NOT touch task-registry; does NOT mark ready.
 */
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

function parseCli(argv) {
  const out = {
    module: '',
    dryRun: false,
    help: false,
    skipExtract: false,
    skipPropose: false,
    all: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--module' || a === '-m') out.module = argv[++i] || '';
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--skip-extract') out.skipExtract = true;
    else if (a === '--skip-propose') out.skipPropose = true;
    else if (a === '--all') out.all = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/pdr-gate1-story-pipeline.mjs --module NAME [--dry-run] [--all]
  node scripts/pdr-gate1-story-pipeline.mjs --module NAME --skip-extract
  node scripts/pdr-gate1-story-pipeline.mjs --module NAME --skip-propose`);
}

function runNode(script, args) {
  const r = spawnSync(process.execPath, [path.join(ORCH_ROOT, 'scripts', script), ...args], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
    stdio: 'inherit',
  });
  if (r.status !== 0) {
    throw new Error(`${script} exited ${r.status}`);
  }
}

function main() {
  const opts = parseCli(process.argv.slice(2));
  if (opts.help || !opts.module) {
    usage();
    process.exit(opts.help ? 0 : 2);
  }

  console.log(`=== PDR Gate-1 story pipeline · module=${opts.module} dryRun=${opts.dryRun} ===\n`);

  if (!opts.skipExtract) {
    console.log('--- 1/2 extract-user-stories ---');
    const args = ['--module', opts.module];
    if (!opts.dryRun) args.push('--write');
    runNode('extract-user-stories.mjs', args);
  }

  if (!opts.skipPropose) {
    console.log('\n--- 2/2 suggest-story-impl-tasks ---');
    const args = ['write', '--module', opts.module];
    if (opts.dryRun) args.push('--dry-run');
    if (opts.all) args.push('--all');
    runNode('suggest-story-impl-tasks.mjs', args);
  }

  console.log(`
=== Done ===
Next (human):
  1. Review agent-delivery/user-story-library.yaml (module stories)
  2. Review agent-delivery/story-impl-proposals.yaml
  3. PM paste suggested_yaml into task-registry (status=backlog) if accepted
  4. After DG-G3: scan/confirm → ready（勿在门1后标 ready）
`);
}

main();
