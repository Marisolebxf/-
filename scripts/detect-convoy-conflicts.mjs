#!/usr/bin/env node
/**
 * detect-convoy-conflicts.mjs
 * 扫描 task-registry 活跃任务的 Convoy / touched_files 冲突。
 *
 * 用法：
 *   node scripts/detect-convoy-conflicts.mjs
 *   node scripts/detect-convoy-conflicts.mjs --task ENT-FE-SEARCH-REGION-FILTER
 *   node scripts/detect-convoy-conflicts.mjs --json
 *   node scripts/detect-convoy-conflicts.mjs --strict   # soft_warn 也 exit 1
 *
 * 真源：dispatch-queue.yaml#convoy_groups · graph_engineering_policy · 手册 §14.3 / §十六
 */

import {
  loadTasksWithTouchedFiles,
  detectConflicts,
  canClaim,
} from './lib/convoy-lib.mjs';

function parseArgs(argv) {
  const out = { task: null, json: false, strict: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--task') out.task = argv[++i];
    else if (a === '--json') out.json = true;
    else if (a === '--strict') out.strict = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/detect-convoy-conflicts.mjs [--task ID] [--json] [--strict]`);
    process.exit(0);
  }

  const { byId, convoyGroups } = loadTasksWithTouchedFiles();

  let result;
  if (opts.task) {
    const gate = canClaim(opts.task, byId, convoyGroups);
    result = {
      mode: 'claim_gate',
      task: opts.task,
      ok: gate.ok,
      conflicts: gate.conflicts,
      soft_warns: gate.soft_warns,
    };
  } else {
    const det = detectConflicts(byId, convoyGroups);
    result = {
      mode: 'scan_active',
      active_count: det.active_count,
      ok: det.conflicts.length === 0,
      conflicts: det.conflicts,
      soft_warns: det.soft_warns,
      convoy_groups: Object.keys(convoyGroups),
    };
  }

  if (opts.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log('=== detect-convoy-conflicts ===');
    console.log(`模式: ${result.mode}  hard=${result.conflicts.length}  soft=${result.soft_warns.length}`);
    if (result.conflicts.length) {
      console.log('\n硬冲突:');
      for (const c of result.conflicts) {
        console.log(`  ✗ [${c.type}] ${c.a} ↔ ${c.b}  (${c.repo || c.convoy || '-'})`);
        console.log(`    ${c.reason}`);
        if (c.suggested_convoy) console.log(`    建议 convoy: ${c.suggested_convoy}`);
      }
    }
    if (result.soft_warns.length) {
      console.log('\n软警告（缺 touched_files）:');
      for (const w of result.soft_warns) {
        console.log(`  ⚠ ${w.a} ↔ ${w.b}  repo=${w.repo}  missing=${(w.missing || []).join(',')}`);
      }
    }
    if (!result.conflicts.length && !result.soft_warns.length) {
      console.log('✅ 无冲突');
    }
    if (opts.task) {
      console.log(result.ok ? `\n可认领: ${opts.task}` : `\n不可认领: ${opts.task}`);
    }
  }

  const fail = !result.ok || (opts.strict && result.soft_warns?.length);
  process.exit(fail ? 1 : 0);
}

main();
