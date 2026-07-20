#!/usr/bin/env node
/**
 * Backfill delivery_phase on tasks missing it.
 * Rules aligned with feishu-bitable.yaml#delivery_phase_classify
 *   definition | implementation | crosscut
 * Does NOT overwrite existing delivery_phase.
 *
 *   node scripts/backfill-delivery-phase.mjs
 *   node scripts/backfill-delivery-phase.mjs --dry-run
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(__dirname, '..');
const REGISTRY = path.join(ORCH, 'agent-delivery', 'task-registry.yaml');
const CONFIG = path.join(ORCH, 'agent-delivery', 'feishu-bitable.yaml');

const dryRun = process.argv.includes('--dry-run');

function loadClassify() {
  const raw = fs.readFileSync(CONFIG, 'utf8');
  const out = {
    default: 'crosscut',
    crosscutEpicPrefixes: ['E-PLATFORM-', 'E-PERM-'],
    crosscutIdRegex:
      '(ORCH-|PLATFORM-|PERM-|E-PLATFORM-|E-PERM-)',
    definitionIdRegex:
      '(PACK-L0|METRIC-OPEN|UX-L0|V1-HIFI|V1-FINAL|PDR-G1|G2-SIGNOFF|V2-LUMEN|V2-DEMO|DG-G3|-PDR-|HIFI-|WIREFRAME|USM-|TRACE-)',
    implementationIdRegex:
      '(IMPL-|JAVA-|FE-WIRE|FE-PERM|-API-|ALGO-ALIGN|QA-ACCEPT|DATA-PATH|DATA-IMPL|ENT-JAVA-|ENT-ARCH-API|ENT-DATA-|ENT-ALGO-)',
  };
  const block = raw.match(/delivery_phase_classify:\s*\r?\n((?:  .+\r?\n)+)/);
  if (!block) return out;
  const b = block[1];
  const d = b.match(/^\s+default:\s*(\w+)/m);
  if (d) out.default = d[1];
  const cx = b.match(/^\s+crosscut_id_regex:\s*"(.*)"/m);
  if (cx) out.crosscutIdRegex = cx[1];
  const df = b.match(/^\s+definition_id_regex:\s*"(.*)"/m);
  if (df) out.definitionIdRegex = df[1];
  const im = b.match(/^\s+implementation_id_regex:\s*"(.*)"/m);
  if (im) out.implementationIdRegex = im[1];
  const pf = b.match(/^\s+crosscut_epic_prefixes:\s*\[(.*?)\]/m);
  if (pf) {
    out.crosscutEpicPrefixes = pf[1]
      .split(',')
      .map((s) => s.trim().replace(/^["']|["']$/g, ''))
      .filter(Boolean);
  }
  return out;
}

function classify(id, epic, rules) {
  const allowed = new Set(['definition', 'implementation', 'crosscut']);
  for (const pfx of rules.crosscutEpicPrefixes) {
    if (pfx && epic.startsWith(pfx)) return 'crosscut';
  }
  if (new RegExp(rules.crosscutIdRegex).test(id)) return 'crosscut';
  if (new RegExp(rules.definitionIdRegex).test(id)) return 'definition';
  if (new RegExp(rules.implementationIdRegex).test(id)) {
    return 'implementation';
  }
  return allowed.has(rules.default) ? rules.default : 'crosscut';
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
    if (m) {
      return m[1].replace(/^["']|["']$/g, '').replace(/\s+#.*$/, '').trim();
    }
  }
  return '';
}

function insertAfter(block, afterKeys, linesToInsert) {
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

const rules = loadClassify();
const text = fs.readFileSync(REGISTRY, 'utf8');
const nl = text.includes('\r\n') ? '\r\n' : '\n';
const lines = text.split(/\r?\n/);
const blocks = findTaskBlocks(lines);

let filled = 0;
let skipped = 0;
const summary = { definition: 0, implementation: 0, crosscut: 0 };

for (let b = blocks.length - 1; b >= 0; b--) {
  const { start, end } = blocks[b];
  const block = lines.slice(start, end);
  const id =
    getScalar(block, 'id') ||
    (block[0].match(/id:\s*(.+)/) || [])[1]?.trim().replace(/^["']|["']$/g, '');
  if (getScalar(block, 'delivery_phase')) {
    skipped++;
    continue;
  }
  const epic = getScalar(block, 'epic');
  const phase = classify(id || '', epic, rules);
  summary[phase] = (summary[phase] || 0) + 1;
  filled++;
  const insert = [
    `    delivery_phase: ${phase}  # backfill delivery_phase_v1`,
  ];
  insertAfter(block, ['epic', 'status', 'title'], insert);
  if (!dryRun) {
    lines.splice(start, end - start, ...block);
  } else if (filled <= 8) {
    console.log(`[DRY] ${id}: epic=${epic || '-'} → ${phase}`);
  }
}

console.log(
  `${dryRun ? '[DRY] ' : ''}backfill delivery_phase: filled=${filled} skipped_existing=${skipped} ` +
    `definition=${summary.definition} implementation=${summary.implementation} crosscut=${summary.crosscut}`,
);

if (!dryRun) {
  const out = lines.join(nl);
  fs.writeFileSync(REGISTRY, out.endsWith(nl) ? out : `${out}${nl}`, 'utf8');
  console.log(`wrote ${REGISTRY}`);
}
