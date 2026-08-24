import fs from 'node:fs';
import path from 'node:path';
import { loadCatalog, parseMetricsYaml } from './scripts/lib/metric-registry-lib.mjs';

const ORCH = process.cwd();
const ID_ASSIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/id-assign');

// 1. load seed catalog (fresh)
const catalog = loadCatalog(true);

// 2. scan id-assign for suggested mapping
const suggested = new Map(); // metric_id -> { type, file }
let suggestedCount = 0;
let reuseCount = 0;
if (fs.existsSync(ID_ASSIGN)) {
  const files = fs.readdirSync(ID_ASSIGN).filter((f) => f.endsWith('.yaml') && !f.includes('-questions'));
  for (const f of files) {
    const text = fs.readFileSync(path.join(ID_ASSIGN, f), 'utf8');
    const parsed = parseMetricsYaml(text);
    const items = parsed.header?.items;
    if (!Array.isArray(items)) continue;
    for (const it of items) {
      suggestedCount++;
      const id = it.metric_id;
      const t = it.algorithm_type_suggested;
      if (id && t) {
        if (!suggested.has(id)) suggested.set(id, { type: t, file: f });
      }
    }
  }
}

// 3. classify in_seed metrics
let t1 = 0, t2 = 0, t3 = 0;
const t2List = [], t3List = [];
for (const [id, rec] of catalog.byId) {
  if (!rec.seed) continue; // only in_seed
  const rawType = rec.seed.algorithm_type;
  const hasType = rawType && String(rawType).trim() !== '' && String(rawType).trim() !== 'UNKNOWN';
  if (hasType) { t1++; continue; }
  const sug = suggested.get(id);
  if (sug) { t2++; t2List.push({ id, domain: rec.seed_domain, suggested: sug.type }); }
  else { t3++; t3List.push({ id, domain: rec.seed_domain }); }
}

console.log('=== latest-seed classification ===');
console.log('registry byId total        :', catalog.byId.size);
console.log('in_seed count              :', t1 + t2 + t3);
console.log('id-assign items scanned    :', suggestedCount);
console.log('id-assign unique suggested :', suggested.size);
console.log('T1 already-has-type        :', t1);
console.log('T2 has-suggested           :', t2);
console.log('T3 no-source (needs judge) :', t3);
console.log('T2+T3 to-sign              :', t2 + t3);

// T2 by domain
const t2ByDom = {}, t3ByDom = {};
for (const x of t2List) t2ByDom[x.domain] = (t2ByDom[x.domain] || 0) + 1;
for (const x of t3List) t3ByDom[x.domain] = (t3ByDom[x.domain] || 0) + 1;
console.log('T2 by domain:', JSON.stringify(t2ByDom));
console.log('T3 by domain:', JSON.stringify(t3ByDom));

// suggested types that never matched an in_seed id (diagnostic)
const unmatched = [];
for (const [id, v] of suggested) {
  const rec = catalog.byId.get(id);
  if (!rec || !rec.seed) unmatched.push(`${id}->${v.type} (${v.file})`);
}
console.log('suggested NOT in seed (count):', unmatched.length);
