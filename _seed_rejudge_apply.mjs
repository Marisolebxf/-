import fs from 'node:fs';
import path from 'node:path';

const ORCH = process.cwd();
const REGISTRY = path.join(ORCH, 'agent-delivery/metrics/registry');
const MERGED = path.join(ORCH, 'agent-delivery/metrics/request/_work/rejudge/_merged.changes.json');
const APPLY = process.argv.includes('--apply');

const changes = JSON.parse(fs.readFileSync(MERGED, 'utf8'));
const byId = new Map();
for (const c of changes) byId.set(c.id, c);

function applyFile(filePath, apply) {
  const raw = fs.readFileSync(filePath);
  const hasBom = raw.length >= 3 && raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf;
  let text = raw.toString('utf8');
  if (hasBom) text = text.slice(1);
  const crlf = text.includes('\r\n');
  const eol = crlf ? '\r\n' : '\n';
  const lines = text.split(/\r?\n/);

  const out = [];
  let curId = null;
  let replaced = 0;
  let mismatch = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const mid = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
    if (mid) {
      curId = mid[1];
      out.push(line);
      continue;
    }
    const at = line.match(/^(\s*)algorithm_type:\s*(.*)$/);
    if (at && curId && byId.has(curId)) {
      const c = byId.get(curId);
      const val = at[2].trim();
      if (val === c.to) {
        // already updated
        out.push(line);
      } else if (val === c.from || val === '') {
        out.push(`${at[1]}algorithm_type: ${c.to}`);
        replaced++;
      } else {
        // current value neither from nor to -> flag
        out.push(line);
        mismatch++;
        console.log(`  MISMATCH ${curId}: 期望 from=${c.from} to=${c.to} 实际=${val}`);
      }
      continue;
    }
    out.push(line);
  }

  if (apply) {
    let result = out.join(eol);
    if (hasBom) result = '\uFEFF' + result;
    fs.writeFileSync(filePath, result, 'utf8');
  }
  return { replaced, mismatch };
}

const files = fs.readdirSync(REGISTRY).filter((n) => n.startsWith('cfg_metric-') && n.endsWith('-seed.yaml')).sort();
let totalReplaced = 0;
let totalMismatch = 0;
const matchedIds = new Set();

for (const f of files) {
  const r = applyFile(path.join(REGISTRY, f), APPLY);
  totalReplaced += r.replaced;
  totalMismatch += r.mismatch;
  if (r.replaced || r.mismatch) console.log(`${f}: replace=${r.replaced} mismatch=${r.mismatch}`);
  // collect matched ids for cross-check
  if (APPLY) {
    const t = fs.readFileSync(path.join(REGISTRY, f), 'utf8');
    for (const line of t.split(/\r?\n/)) {
      const m = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
      if (m) matchedIds.add(m[1]);
    }
  }
}

console.log('');
console.log('TOTAL replace:', totalReplaced, '| mismatch:', totalMismatch, '| 预期:', changes.length);
console.log(APPLY ? 'APPLIED (files written)' : 'DRY-RUN (no write; add --apply to write)');

if (!APPLY) {
  // dry-run: report ids not found in seed
  const seen = new Set();
  for (const f of files) {
    const t = fs.readFileSync(path.join(REGISTRY, f), 'utf8');
    for (const line of t.split(/\r?\n/)) {
      const m = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
      if (m) seen.add(m[1]);
    }
  }
  const missing = changes.filter((c) => !seen.has(c.id)).map((c) => c.id);
  console.log('changes NOT found in seed:', missing.length);
  if (missing.length) console.log(missing.join(', '));
}
