import fs from 'node:fs';
import path from 'node:path';
import { loadCatalog, parseMetricsYaml } from './scripts/lib/metric-registry-lib.mjs';

const ORCH = process.cwd();
const ID_ASSIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/id-assign');
const A1_METRICS = path.join(ORCH, 'agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml');
const NEW_IDS = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md');
const OLD_SIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-签收草表.md');
const OUT_SIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-签收草表.md');

// ── 1. seed catalog ──
const catalog = loadCatalog(true);

// ── 2. id-assign suggested ──
const suggested = new Map();
for (const f of fs.readdirSync(ID_ASSIGN).filter((f) => f.endsWith('.yaml') && !f.includes('-questions'))) {
  const parsed = parseMetricsYaml(fs.readFileSync(path.join(ID_ASSIGN, f), 'utf8'));
  const items = parsed.header?.items;
  if (!Array.isArray(items)) continue;
  for (const it of items) {
    if (it.metric_id && it.algorithm_type_suggested) {
      if (!suggested.has(it.metric_id)) suggested.set(it.metric_id, it.algorithm_type_suggested);
    }
  }
}

// ── 3. A1 表2 TEMP_ALGO -> algorithm.type（正则：0 缩进块序列 parseMetricsYaml 不识别）──
const a1Text = fs.readFileSync(A1_METRICS, 'utf8');
const tempType = new Map();
for (const b of a1Text.split(/\n- metric_id: /)) {
  const nl = b.indexOf('\n');
  const id = (nl < 0 ? b : b.slice(0, nl)).trim();
  if (!id.startsWith('TEMP_ALGO_')) continue;
  const m = b.match(/\n\s*type:\s*(\w+)/);
  if (m) tempType.set(id, m[1]);
}

// ── 4. new-ids TEMP -> 正式号 ──
const tempToFormal = new Map();
const newIdsText = fs.readFileSync(NEW_IDS, 'utf8');
const mapSection = newIdsText.split('## TEMP_ALGO')[1] || '';
for (const line of mapSection.split(/\r?\n/)) {
  const m = line.match(/\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|/);
  if (m) tempToFormal.set(m[1].trim(), m[2].trim());
}
const formalToA1 = new Map();
for (const [temp, formal] of tempToFormal) {
  const t = tempType.get(temp);
  if (t) formalToA1.set(formal, t === 'API' ? 'third_party' : t);
}

// ── 5. 旧草表 T3 初判 ──
const oldT3Judge = new Map();
if (fs.existsSync(OLD_SIGN)) {
  const text = fs.readFileSync(OLD_SIGN, 'utf8');
  const t3Section = (text.split('## T3 签收')[1] || '').split(/\r?\n/);
  for (const line of t3Section) {
    const m = line.match(/\|\s*\d+\s*\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(\w+)\s*\|/);
    if (m) oldT3Judge.set(m[1], m[2]);
  }
}

// ── 6. machine judge ──
function judgeType(id, formula, name) {
  const f = `${formula || ''} ${name || ''}`;
  const low = f.toLowerCase();
  if (/graph|图|中心性|中心度|边权|edge|node|路径|网络结构|拓扑|pagerank|社群|中介中心|紧密中心|度中心|关系网|关系链|子图|图谱/.test(low)) return 'GRAPH';
  if (/(标准化|归一)/.test(f) && /(count|计数|比例|占比|ratio)/.test(low)) return 'COMPUTE';
  if (/(加权|指数|评分|score|index|综合|合成|模型|预测|聚类|相关|回归|打分|等级|rank|排名|成熟度|潜力|影响|竞争|壁垒|识别|判定|评估|诊断|抽取|推荐|分析|归一|标准化)/.test(low)) return 'MODEL';
  if (/(count|sum|avg|group by|distinct|计数|总数|数量|清单|去重|分布|环比|增长率|规模|条数|占比|比例)/.test(low)) return 'STAT';
  return 'MODEL';
}

// ── 7. classify ──
const t2 = [], tTemp = [], t3 = [];
for (const [id, rec] of catalog.byId) {
  if (!rec.seed) continue;
  const rawType = rec.seed.algorithm_type;
  if (rawType && String(rawType).trim() !== '' && String(rawType).trim() !== 'UNKNOWN') continue; // T1 already filled
  const domain = rec.seed_domain || '';
  const name = rec.seed.metric_name_zh || '';
  const formula = rec.seed.formula || '';
  const sug = suggested.get(id);
  if (sug) { t2.push({ id, domain, name, suggest: sug === 'API' ? 'third_party' : sug, source: '赋号卡' }); continue; }
  const a1t = formalToA1.get(id);
  if (a1t) { tTemp.push({ id, domain, name, suggest: a1t, source: 'A1-TEMP已签' }); continue; }
  const oldJ = oldT3Judge.get(id);
  const jt = oldJ || judgeType(id, formula, name);
  t3.push({ id, domain, name, formula, suggest: jt, source: oldJ ? '旧初判' : '新初判' });
}
t2.sort((a, b) => a.id.localeCompare(b.id));
tTemp.sort((a, b) => a.id.localeCompare(b.id));
t3.sort((a, b) => a.id.localeCompare(b.id));

// ── 8. report ──
console.log('=== classification (latest 557 / in_seed 532) ===');
console.log('T1 already-filled   :', catalog.byId.size - t2.length - tTemp.length - t3.length - (557 - 532)); // rough
console.log('T2 id-assign suggest :', t2.length);
console.log('T-TEMP A1-signed     :', tTemp.length);
console.log('T3 machine/old judge :', t3.length);
console.log('TOTAL to-sign        :', t2.length + tTemp.length + t3.length);
const t3old = t3.filter((x) => x.source === '旧初判').length;
const t3new = t3.filter((x) => x.source === '新初判').length;
console.log('  T3 old-judge reused:', t3old);
console.log('  T3 new-judge       :', t3new);

// ── 9. write signoff sheet ──
const L = [];
L.push('# ALGO-LIB-SEED-TYPE-L01 · 签收草表（最新库 522 条）');
L.push('');
L.push('> 基于 `acc16b1` 补库后的最新 seed（557 条 / in_seed 532 / 已回填 10 / 待签 522）。');
L.push('> 供 `human:唐绍祖` 统签。**建议 type 仅供参考，请逐条或批量确认，签完我回填。**');
L.push('> 回填规则：`API` → seed `third_party`；`D1` 保持 `draft`；`MODEL/GRAPH/MIXED` 的 steps 不回填。');
L.push('');
L.push('## 统计');
L.push('');
L.push('| 分组 | 建议依据 | 条数 |');
L.push('|---|---|---|');
L.push(`| T2 赋号卡建议 | id-assign 赋号卡 suggested_unsigned | ${t2.length} |`);
L.push(`| T-TEMP A1 已签沿用 | A1 表2 TEMP_ALGO → 正式号 已签 type | ${tTemp.length} |`);
L.push(`| T3 机器初判 | 旧初判 ${t3old} + 新初判 ${t3new} | ${t3.length} |`);
L.push(`| **合计待签** | | **${t2.length + tTemp.length + t3.length}** |`);
L.push('');

function pushTable(title, rows, withFormula) {
  L.push(`## ${title}`);
  L.push('');
  if (withFormula) {
    L.push('| # | metric_id | domain | 中文名 | formula(截断) | 建议 type | 确认 type |');
    L.push('|---|---|---|---|---|---|---|');
  } else {
    L.push('| # | metric_id | domain | 中文名 | 建议 type | 确认 type |');
    L.push('|---|---|---|---|---|---|');
  }
  let n = 0;
  for (const r of rows) {
    n++;
    const nm = String(r.name).replace(/\|/g, '/');
    if (withFormula) {
      const fm = String(r.formula || '').replace(/\s+/g, ' ').replace(/\|/g, '/').slice(0, 60);
      L.push(`| ${n} | \`${r.id}\` | ${r.domain} | ${nm} | ${fm} | ${r.suggest} |  |`);
    } else {
      L.push(`| ${n} | \`${r.id}\` | ${r.domain} | ${nm} | ${r.suggest} |  |`);
    }
  }
  L.push('');
}

pushTable(`T2 · 赋号卡建议（${t2.length} 条）`, t2, false);
pushTable(`T-TEMP · A1 已签 type 沿用（${tTemp.length} 条）`, tTemp, false);
pushTable(`T3 · 机器初判（${t3.length} 条）`, t3, true);

fs.writeFileSync(OUT_SIGN, L.join('\n'), 'utf8');
console.log('\nWROTE', OUT_SIGN);
