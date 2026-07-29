#!/usr/bin/env node
/**
 * Backfill task.update_time for Feishu「更新时间」sortable clock.
 *
 * Heuristic (max of available stamps, else fallback):
 *   completed_at | claimed_at | last_seen_at | date-only → noon +08:00
 *   missing all → 2026-06-01T00:00:00+08:00
 *
 * Does NOT overwrite existing update_time unless --force.
 *
 *   node scripts/backfill-update-time.mjs --dry-run
 *   node scripts/backfill-update-time.mjs --apply
 *   node scripts/backfill-update-time.mjs --apply --force
 */

import {
  applyBlockUpdate,
  findTaskBlocks,
  getScalar,
  nowIsoPlus8,
  parseTaskBlock,
  readRegistryText,
  touchUpdateTime,
  writeRegistryText,
} from './lib/task-registry-lib.mjs';

const FALLBACK = '2026-06-01T00:00:00+08:00';

function parseArgs(argv) {
  const out = { dryRun: true, apply: false, force: false, help: false };
  for (const a of argv) {
    if (a === '--apply') {
      out.apply = true;
      out.dryRun = false;
    } else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--force') out.force = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  if (out.apply) out.dryRun = false;
  return out;
}

function toPlus8Iso(d) {
  return nowIsoPlus8(d);
}

function parseStamp(raw) {
  if (!raw) return null;
  const s = String(raw).trim().replace(/^["']|["']$/g, '');
  if (!s) return null;
  // date-only YYYY-MM-DD → noon Asia/Shanghai
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
    const d = new Date(`${s}T12:00:00+08:00`);
    return Number.isNaN(d.getTime()) ? null : d;
  }
  const d = new Date(s);
  return Number.isNaN(d.getTime()) ? null : d;
}

function heuristicUpdateTime(task) {
  const candidates = [task.completed_at, task.claimed_at, task.last_seen_at]
    .map(parseStamp)
    .filter(Boolean);
  if (!candidates.length) return FALLBACK;
  const maxMs = Math.max(...candidates.map((d) => d.getTime()));
  return toPlus8Iso(new Date(maxMs));
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/backfill-update-time.mjs --dry-run
  node scripts/backfill-update-time.mjs --apply
  node scripts/backfill-update-time.mjs --apply --force`);
    process.exit(0);
  }

  const lines = readRegistryText().split(/\r?\n/);
  let newLines = lines;
  const changes = [];

  // Update from end so earlier block indices stay valid
  const locs = findTaskBlocks(newLines);
  for (let i = locs.length - 1; i >= 0; i--) {
    const loc = locs[i];
    const block = newLines.slice(loc.start, loc.end);
    const task = parseTaskBlock(block);
    if (!task.id) continue;
    const existing = getScalar(block, 'update_time');
    if (existing && !opts.force) continue;
    const next = heuristicUpdateTime(task);
    if (existing === next && !opts.force) continue;
    touchUpdateTime(block, next);
    changes.push({ id: task.id, from: existing || '(none)', to: next });
    newLines = applyBlockUpdate(newLines, loc, block);
  }

  console.log(`backfill-update-time: ${changes.length} task(s)  mode=${opts.dryRun ? 'DRY-RUN' : 'APPLY'}${opts.force ? ' FORCE' : ''}`);
  for (const c of changes.slice(0, 30)) {
    console.log(`  ${c.id}: ${c.from} → ${c.to}`);
  }
  if (changes.length > 30) console.log(`  … +${changes.length - 30} more`);

  if (opts.dryRun) {
    console.log('\n（dry-run：加 --apply 才会写 registry）');
    return;
  }
  if (!changes.length) {
    console.log('No changes needed.');
    return;
  }
  writeRegistryText(newLines.join('\n'));
  console.log(`\n✅ wrote ${changes.length} update_time value(s). Next: outbound Feishu sync.`);
}

main();
