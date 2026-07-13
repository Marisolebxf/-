#!/usr/bin/env node
/**
 * Backfill effort_points + difficulty on tasks missing them.
 * Heuristic (token_v1): map estimated_tokens → S/M/L/XL + Fibonacci points.
 * Does NOT overwrite existing effort_points / difficulty.
 *
 *   node scripts/backfill-effort-points.mjs
 *   node scripts/backfill-effort-points.mjs --dry-run
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(__dirname, '..');
const REGISTRY = path.join(ORCH, 'agent-delivery', 'task-registry.yaml');

const dryRun = process.argv.includes('--dry-run');

function mapFromTokens(tokens) {
  if (tokens == null || !Number.isFinite(tokens)) {
    return { difficulty: 'M', effort_points: 3 };
  }
  if (tokens < 100_000) return { difficulty: 'S', effort_points: 1 };
  if (tokens < 300_000) return { difficulty: 'M', effort_points: 3 };
  if (tokens < 600_000) return { difficulty: 'L', effort_points: 5 };
  if (tokens < 1_000_000) return { difficulty: 'XL', effort_points: 8 };
  return { difficulty: 'XL', effort_points: 13 };
}

function findTaskBlocks(lines) {
  const blocks = [];
  let inTasks = false;
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (/^tasks:\s*$/.test(lines[i])) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    if (/^\s+- id:\s*/.test(lines[i])) {
      if (start >= 0) blocks.push({ start, end: i });
      start = i;
    }
  }
  if (start >= 0) blocks.push({ start, end: lines.length });
  return blocks;
}

function getScalar(block, key) {
  const re = new RegExp(`^\\s+${key}:\\s*(.+?)\\s*$`);
  for (const line of block) {
    const m = line.match(re);
    if (m) return m[1].replace(/^["']|["']$/g, '').replace(/\s+#.*$/, '').trim();
  }
  return '';
}

function insertAfter(block, afterKeys, linesToInsert) {
  // Prefer insert after estimated_tokens, else status, else after id line
  for (const key of afterKeys) {
    const re = new RegExp(`^\\s+${key}:\\s*`);
    for (let i = 0; i < block.length; i++) {
      if (re.test(block[i])) {
        block.splice(i + 1, 0, ...linesToInsert);
        return true;
      }
    }
  }
  block.splice(1, 0, ...linesToInsert);
  return true;
}

const text = fs.readFileSync(REGISTRY, 'utf8');
const nl = text.includes('\r\n') ? '\r\n' : '\n';
const lines = text.split(/\r?\n/);
const blocks = findTaskBlocks(lines);

let filled = 0;
let skipped = 0;
const summary = { S: 0, M: 0, L: 0, XL: 0 };

// Process from end so indices stay valid when splicing into `lines`
for (let b = blocks.length - 1; b >= 0; b--) {
  const { start, end } = blocks[b];
  const block = lines.slice(start, end);
  const id = getScalar(block, 'id') || (block[0].match(/id:\s*(.+)/) || [])[1]?.trim();
  const hasPoints = Boolean(getScalar(block, 'effort_points'));
  const hasDiff = Boolean(getScalar(block, 'difficulty'));
  if (hasPoints && hasDiff) {
    skipped++;
    continue;
  }

  const tokRaw = getScalar(block, 'estimated_tokens');
  const tokens = tokRaw ? Number(tokRaw.replace(/_/g, '')) : null;
  const mapped = mapFromTokens(Number.isFinite(tokens) ? tokens : null);

  const insert = [];
  if (!hasPoints) {
    insert.push(
      `    effort_points: ${mapped.effort_points}  # backfill token_v1`,
    );
  }
  if (!hasDiff) {
    insert.push(`    difficulty: ${mapped.difficulty}  # backfill token_v1`);
  }
  if (!getScalar(block, 'effort_source')) {
    insert.push(
      `    effort_source: backfill_token_heuristic  # coordinator 可改后删除`,
    );
  }
  if (!insert.length) {
    skipped++;
    continue;
  }

  insertAfter(block, ['estimated_tokens', 'status', 'title'], insert);
  summary[mapped.difficulty] = (summary[mapped.difficulty] || 0) + 1;
  filled++;

  if (!dryRun) {
    lines.splice(start, end - start, ...block);
  } else if (filled <= 5) {
    console.log(
      `[DRY] ${id}: tokens=${tokRaw || '-'} → ${mapped.difficulty}/${mapped.effort_points}`,
    );
  }
}

console.log(
  `${dryRun ? '[DRY] ' : ''}backfill: filled=${filled} skipped_existing=${skipped} ` +
    `S=${summary.S} M=${summary.M} L=${summary.L} XL=${summary.XL}`,
);

if (!dryRun) {
  const out = lines.join(nl);
  fs.writeFileSync(REGISTRY, out.endsWith(nl) ? out : `${out}${nl}`, 'utf8');
  console.log(`wrote ${REGISTRY}`);
}
