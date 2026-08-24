import fs from 'node:fs';
import path from 'node:path';
import { loadCatalog, parseMetricsYaml } from './scripts/lib/metric-registry-lib.mjs';

const ORCH = process.cwd();
const ID_ASSIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/id-assign');
const A1_METRICS = path.join(ORCH, 'agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml');
const NEW_IDS = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md');
const OUTDIR = path.join(ORCH, 'agent-delivery/metrics/request/_work/rejudge');

// suggested
const suggested = new Map();
for (const f of fs.readdirSync(ID_ASSIGN).filter((f) => f.endsWith('.yaml') && !f.includes('-questions'))) {
  const parsed = parseMetricsYaml(fs.readFileSync(path.join(ID_ASSIGN, f), 'utf8'));
  const items = parsed.header?.items;
  if (!Array.isArray(items)) continue;
  for (const it of items) {
    if (it.metric_id && it.algorithm_type_suggested && !suggested.has(it.metric_id)) suggested.set(it.metric_id, it.algorithm_type_suggested);
  }
}
// A1 tempType + formal M_* (T1)
const a1Text = fs.readFileSync(A1_METRICS, 'utf8');
const tempType = new Map();
const t1Set = new Set();
for (const b of a1Text.split(/\n- metric_id: /)) {
  const nl = b.indexOf('\n');
  const id = (nl < 0 ? b : b.slice(0, nl)).trim();
  if (!id) continue;
  const m = b.match(/\n\s*type:\s*(\w+)/);
  if (id.startsWith('TEMP_ALGO_')) {
    if (m) tempType.set(id, m[1]);
  } else if (id.startsWith('M_')) {
    if (m) t1Set.add(id);
  }
}
// temp -> formal
const tempToFormal = new Map();
const sec = (fs.readFileSync(NEW_IDS, 'utf8').split('## TEMP_ALGO')[1] || '');
for (const line of sec.split(/\r?\n/)) {
  const m = line.match(/\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|/);
  if (m) tempToFormal.set(m[1].trim(), m[2].trim());
}
const formalSet = new Set(tempToFormal.values());

const catalog = loadCatalog(true);
const byDomain = new Map();
for (const [id, rec] of catalog.byId) {
  if (!rec.seed) continue;
  const raw = rec.seed.algorithm_type;
  if (!raw || String(raw).trim() === '' || String(raw).trim() === 'UNKNOWN') continue; // only backfilled 522
  const dom = rec.seed_domain || 'OTHER';
  let group;
  if (t1Set.has(id)) group = 'T1';
  else if (suggested.has(id)) group = 'T2';
  else if (formalSet.has(id)) group = 'TTEMP';
  else group = 'T3';
  if (!byDomain.has(dom)) byDomain.set(dom, []);
  byDomain.get(dom).push({
    id,
    group,
    name: String(rec.seed.metric_name_zh || ''),
    definition: String(rec.seed.definition || '').replace(/\s+/g, ' ').trim(),
    formula: String(rec.seed.formula || '').replace(/\s+/g, ' ').trim(),
    curType: String(raw).trim(),
  });
}

fs.mkdirSync(OUTDIR, { recursive: true });

// index
const idx = [];
idx.push('# 522 条 §2.1 重判明细 · 索引');
idx.push('');
idx.push('> 每 domain 一个文件，逐条列 id / 分组 / 中文名 / definition / formula / 现type。');
idx.push('> 分组：T1=A1表2正式号已签 · T2=赋号卡建议 · TTEMP=A1表2 TEMP已签 · T3=机器初判。');
idx.push('');
const doms = [...byDomain.keys()].sort();
let total = 0;
for (const d of doms) {
  const n = byDomain.get(d).length;
  total += n;
  idx.push(`- ${d}: ${n} 条`);
}
idx.push('');
idx.push(`合计 ${total} 条`);

for (const d of doms) {
  const rows = byDomain.get(d).sort((a, b) => a.group.localeCompare(b.group) || a.id.localeCompare(b.id));
  const L = [];
  L.push(`# 重判明细 · ${d}（${rows.length} 条）`);
  L.push('');
  L.push('| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |');
  L.push('|---|---|---|---|---|---|---|---|---|');
  let n = 0;
  for (const r of rows) {
    n++;
    const def = r.definition.replace(/\|/g, '/').slice(0, 160);
    const fml = r.formula.replace(/\|/g, '/').slice(0, 120);
    L.push(`| ${n} | \`${r.id}\` | ${r.group} | ${r.name.replace(/\|/g, '/')} | ${r.curType} | ${def} | ${fml} |  |  |`);
  }
  L.push('');
  fs.writeFileSync(path.join(OUTDIR, `${d}.md`), L.join('\n'), 'utf8');
}

idx.push('');
idx.push('## 输出文件');
for (const d of doms) idx.push(`- \`rejudge/${d}.md\``);

fs.writeFileSync(path.join(OUTDIR, 'INDEX.md'), idx.join('\n'), 'utf8');

console.log('domains:', doms.length, '| total:', total);
for (const d of doms) console.log(' ', d, byDomain.get(d).length);
console.log('WROTE to', OUTDIR);
