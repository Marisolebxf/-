import fs from 'node:fs';
import path from 'node:path';
import { loadCatalog, parseMetricsYaml } from './scripts/lib/metric-registry-lib.mjs';

const ORCH = process.cwd();
const REGISTRY = path.join(ORCH, 'agent-delivery/metrics/registry');
const ID_ASSIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/id-assign');
const A1_METRICS = path.join(ORCH, 'agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml');
const NEW_IDS = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md');

const APPLY = process.argv.includes('--apply');

// ── 1. id-assign suggested ──
const suggested = new Map();
for (const f of fs.readdirSync(ID_ASSIGN).filter((f) => f.endsWith('.yaml') && !f.includes('-questions'))) {
  const parsed = parseMetricsYaml(fs.readFileSync(path.join(ID_ASSIGN, f), 'utf8'));
  const items = parsed.header?.items;
  if (!Array.isArray(items)) continue;
  for (const it of items) {
    if (it.metric_id && it.algorithm_type_suggested && !suggested.has(it.metric_id)) {
      suggested.set(it.metric_id, it.algorithm_type_suggested);
    }
  }
}

// ── 2. A1 表2 TEMP_ALGO -> type ──
const a1Text = fs.readFileSync(A1_METRICS, 'utf8');
const tempType = new Map();
for (const b of a1Text.split(/\n- metric_id: /)) {
  const nl = b.indexOf('\n');
  const id = (nl < 0 ? b : b.slice(0, nl)).trim();
  if (!id.startsWith('TEMP_ALGO_')) continue;
  const m = b.match(/\n\s*type:\s*(\w+)/);
  if (m) tempType.set(id, m[1]);
}

// ── 3. TEMP -> 正式号 ──
const tempToFormal = new Map();
const sec = (fs.readFileSync(NEW_IDS, 'utf8').split('## TEMP_ALGO')[1] || '');
for (const line of sec.split(/\r?\n/)) {
  const m = line.match(/\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|/);
  if (m) tempToFormal.set(m[1].trim(), m[2].trim());
}
const formalToA1 = new Map();
for (const [temp, formal] of tempToFormal) {
  const t = tempType.get(temp);
  if (t) formalToA1.set(formal, t === 'API' ? 'third_party' : t);
}

// ── 4. machine judge (与签收草表完全一致) ──
function judgeType(id, formula, name) {
  const f = `${formula || ''} ${name || ''}`;
  const low = f.toLowerCase();
  if (/graph|图|中心性|中心度|边权|edge|node|路径|网络结构|拓扑|pagerank|社群|中介中心|紧密中心|度中心|关系网|关系链|子图|图谱/.test(low)) return 'GRAPH';
  if (/(标准化|归一)/.test(f) && /(count|计数|比例|占比|ratio)/.test(low)) return 'COMPUTE';
  if (/(加权|指数|评分|score|index|综合|合成|模型|预测|聚类|相关|回归|打分|等级|rank|排名|成熟度|潜力|影响|竞争|壁垒|识别|判定|评估|诊断|抽取|推荐|分析|归一|标准化)/.test(low)) return 'MODEL';
  if (/(count|sum|avg|group by|distinct|计数|总数|数量|清单|去重|分布|环比|增长率|规模|条数|占比|比例)/.test(low)) return 'STAT';
  return 'MODEL';
}

// ── 5. final type map ──
const finalType = new Map();
const t1Skip = [];
for (const [id, rec] of loadCatalog(true).byId) {
  if (!rec.seed) continue;
  const raw = rec.seed.algorithm_type;
  if (raw && String(raw).trim() !== '' && String(raw).trim() !== 'UNKNOWN') { t1Skip.push(id); continue; }
  const sug = suggested.get(id);
  if (sug) { finalType.set(id, sug === 'API' ? 'third_party' : sug); continue; }
  const a1t = formalToA1.get(id);
  if (a1t) { finalType.set(id, a1t); continue; }
  finalType.set(id, judgeType(id, rec.seed.formula || '', rec.seed.metric_name_zh || ''));
}
console.log('finalType size:', finalType.size, '| T1 skip:', t1Skip.length);

// ── 6. backfill per file ──
function backfillFile(filePath, typeMap, apply) {
  const raw = fs.readFileSync(filePath);
  const hasBom = raw.length >= 3 && raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf;
  let text = raw.toString('utf8');
  if (hasBom) text = text.slice(1);
  const crlf = text.includes('\r\n');
  const eol = crlf ? '\r\n' : '\n';
  const lines = text.split(/\r?\n/);

  const out = [];
  let curId = null;
  let seenType = false;
  let replaced = 0;
  let inserted = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const mid = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
    if (mid) {
      curId = mid[1];
      seenType = false;
      out.push(line);
      continue;
    }
    const at = line.match(/^(\s*)algorithm_type:\s*(.*)$/);
    if (at && curId && typeMap.has(curId)) {
      const val = at[2].trim();
      const newType = typeMap.get(curId);
      if (val === 'UNKNOWN' || val === '') {
        out.push(`${at[1]}algorithm_type: ${newType}`);
        replaced++;
      } else {
        out.push(line);
      }
      seenType = true;
      continue;
    }
    if (curId && typeMap.has(curId) && !seenType) {
      const anchor = line.match(/^(\s{4})(source_tables|source_systems|update_freq|version|source_status|is_mock|mapping_status|pending_ref|ui_alias|bid_ref|acceptance_unit_id):/);
      if (anchor) {
        out.push(`    algorithm_type: ${typeMap.get(curId)}`);
        inserted++;
        seenType = true;
      }
    }
    out.push(line);
  }

  if (apply) {
    let result = out.join(eol);
    if (hasBom) result = '\uFEFF' + result;
    fs.writeFileSync(filePath, result, 'utf8');
  }
  return { replaced, inserted };
}

const files = fs.readdirSync(REGISTRY).filter((n) => n.startsWith('cfg_metric-') && n.endsWith('-seed.yaml')).sort();
let totalReplaced = 0, totalInserted = 0;
for (const f of files) {
  const r = backfillFile(path.join(REGISTRY, f), finalType, APPLY);
  totalReplaced += r.replaced;
  totalInserted += r.inserted;
  console.log(`${f}: replace=${r.replaced} insert=${r.inserted}`);
}
console.log('TOTAL replace:', totalReplaced, '| insert:', totalInserted, '| sum:', totalReplaced + totalInserted);
console.log(APPLY ? 'APPLIED (files written)' : 'DRY-RUN (no write; add --apply to write)');

// ── 7. check unmapped ids (in finalType but never matched) ──
if (!APPLY) {
  const seen = new Set();
  for (const f of files) {
    const text = fs.readFileSync(path.join(REGISTRY, f), 'utf8');
    for (const line of text.split(/\r?\n/)) {
      const mid = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
      if (mid) seen.add(mid[1]);
    }
  }
  const unmapped = [...finalType.keys()].filter((id) => !seen.has(id));
  console.log('finalType ids NOT found in seed:', unmapped.length);
  if (unmapped.length) console.log(unmapped.slice(0, 40));
}
