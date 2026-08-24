/**
 * 淮政玮 2026-08-25：新 COMPUTE 口径
 * 加权合成若子指标含评价模型（密度/评分/指数/壁垒等）→ MODEL。
 * 将 §2.1 重判的 30 条 MODEL→COMPUTE 退回 MODEL。
 */
import fs from 'node:fs';
import path from 'node:path';

const ORCH = process.cwd();
const REGISTRY = path.join(ORCH, 'agent-delivery/metrics/registry');
const MERGED = path.join(ORCH, 'agent-delivery/metrics/request/_work/rejudge/_merged.changes.json');
const APPLY = process.argv.includes('--apply');

const ids = new Set(
  JSON.parse(fs.readFileSync(MERGED, 'utf8'))
    .filter((c) => c.from === 'MODEL' && c.to === 'COMPUTE')
    .map((c) => c.id),
);

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
  const done = [];

  for (const line of lines) {
    const mid = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
    if (mid) {
      curId = mid[1];
      out.push(line);
      continue;
    }
    const at = line.match(/^(\s*)algorithm_type:\s*(.*)$/);
    if (at && curId && ids.has(curId)) {
      const val = at[2].trim();
      if (val === 'MODEL') {
        out.push(line);
      } else if (val === 'COMPUTE') {
        out.push(`${at[1]}algorithm_type: MODEL`);
        replaced++;
        done.push(curId);
      } else {
        out.push(line);
        mismatch++;
        console.log(`  MISMATCH ${curId}: 期望 COMPUTE 实际=${val}`);
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
  return { replaced, mismatch, done };
}

const files = fs
  .readdirSync(REGISTRY)
  .filter((n) => n.startsWith('cfg_metric-') && n.endsWith('-seed.yaml'))
  .sort();

let totalReplaced = 0;
let totalMismatch = 0;
const allDone = [];
for (const f of files) {
  const r = applyFile(path.join(REGISTRY, f), APPLY);
  totalReplaced += r.replaced;
  totalMismatch += r.mismatch;
  allDone.push(...r.done);
  if (r.replaced || r.mismatch) console.log(`${f}: replace=${r.replaced} mismatch=${r.mismatch}`);
}

console.log('ids=', ids.size, 'replace=', totalReplaced, 'mismatch=', totalMismatch);
console.log(APPLY ? 'APPLIED' : 'DRY-RUN');
console.log(allDone.join(','));
