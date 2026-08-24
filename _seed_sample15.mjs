import fs from 'node:fs';
import path from 'node:path';
import { loadCatalog, parseMetricsYaml } from './scripts/lib/metric-registry-lib.mjs';

const ORCH = process.cwd();
const ID_ASSIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/id-assign');
const A1_METRICS = path.join(ORCH, 'agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml');
const NEW_IDS = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md');

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
// A1 tempType
const a1Text = fs.readFileSync(A1_METRICS, 'utf8');
const tempType = new Map();
for (const b of a1Text.split(/\n- metric_id: /)) {
  const nl = b.indexOf('\n');
  const id = (nl < 0 ? b : b.slice(0, nl)).trim();
  if (!id.startsWith('TEMP_ALGO_')) continue;
  const m = b.match(/\n\s*type:\s*(\w+)/);
  if (m) tempType.set(id, m[1]);
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
const groups = { T2: [], TTEMP: [], T3real: [], T3ph: [] };
for (const [id, rec] of catalog.byId) {
  if (!rec.seed) continue;
  const raw = rec.seed.algorithm_type;
  if (!raw || String(raw).trim() === '' || String(raw).trim() === 'UNKNOWN') continue; // only backfilled
  const formula = String(rec.seed.formula || '');
  const name = rec.seed.metric_name_zh || '';
  const dom = rec.seed_domain || '';
  const item = { id, dom, name, type: String(raw).trim(), formula };
  if (suggested.has(id)) groups.T2.push(item);
  else if (formalSet.has(id)) groups.TTEMP.push(item);
  else if (/pending_cosign|pending_algorithm|pending_data_lead|未签|待会签|待定|待补/.test(formula)) groups.T3ph.push(item);
  else groups.T3real.push(item);
}
for (const k of Object.keys(groups)) groups[k].sort((a, b) => a.id.localeCompare(b.id));

// 确定性分层抽样：取分布较散的若干条
function pick(arr, n, step) {
  const out = [];
  if (!arr.length) return out;
  for (let i = 0; i < n && i < arr.length; i++) {
    out.push(arr[Math.floor((i * arr.length) / n)]);
  }
  return out;
}

const sample = [
  ...pick(groups.T2, 3),
  ...pick(groups.TTEMP, 3),
  ...pick(groups.T3real, 4),
  ...pick(groups.T3ph, 5),
];

console.log('=== 分组规模 ===');
console.log('T2(赋号卡):', groups.T2.length, '| T-TEMP(A1沿用):', groups.TTEMP.length, '| T3真实公式:', groups.T3real.length, '| T3占位符:', groups.T3ph.length);
console.log('');
console.log('=== 抽检 15 条 ===');
for (const s of sample) {
  console.log(`[${s.dom}] ${s.id}`);
  console.log(`  中文名: ${s.name}`);
  console.log(`  回填type: ${s.type}`);
  console.log(`  formula: ${s.formula.replace(/\s+/g, ' ').slice(0, 100)}`);
  console.log('');
}
