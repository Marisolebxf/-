/**
 * 淮政玮 2026-08-25：按智树实现范围回写 seed algorithm_type = third_party。
 * 口径：scope-baseline.md §0 + 智树范围明细；A1 coverage_status=third_party；
 *       给人说明 §2.1 API/third_party = 封装调用不伪展开。
 * 只改 algorithm_type；不改 definition/formula/源表/D1。
 * 用法：node ...mjs            # dry-run
 *       node ...mjs --apply    # 写 seed
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  queryMetrics,
  summarizeMetrics,
  invalidateMetricCache,
  ORCH_ROOT,
} from '../../../../../scripts/lib/metric-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const APPLY = process.argv.includes('--apply');
const REGISTRY = path.join(ORCH_ROOT, 'agent-delivery/metrics/registry');
const A1 = path.join(
  ORCH_ROOT,
  'agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-requirements.yaml',
);

const TOPIC_345 = new Set(['TECH', 'ORG', 'TALENT']);

/** 展示态势完整链路里、智树可从 ADS 自算的技术要素计数。 */
const KEEP_STAT = new Set([
  'M_TECH_PAPER_PATENT_CNT',
  'M_TECH_INVEST_AMOUNT',
  'M_TECH_OUTPUT_SCALE',
]);

/** 展示：人才态势 / 知识图谱（数据资源默认运营 STAT，不按页号灌 third_party）。 */
const DISPLAY_API_ID_RE =
  /_DS[_-](?:13|14|15|16|21|22|23|24)[_-]/;

/** 展示态势里明确外采的人才/专家指数（发展规划「人才流动」仍是智树）。 */
const INNOV_TALENT_ALLOW = new Set([
  'M_INNOV_CITY_TALENT_INDEX_GLOBAL',
  'M_INNOV_CITY_TALENT_INDEX_SZ',
  'M_INNOV_EXPERT_ACTIVITY',
  'M_INNOV_EXPERT_HINDEX',
]);

/** 科技创新评估 = 展示态势完整链路，智树自算。 */
const KEEP_ZHISHU_ID_RE = /_DS[_-]07[_-]TECH[_-]INNOV[_-]/;

function tempToOfficial(tempId) {
  const m = String(tempId).match(/^TEMP_ALGO_ALGO-([A-Z]+)-([A-Z]+)-(\d+)_(\d+)$/);
  if (!m) return null;
  return `M_${m[1]}_${m[2]}_${m[3]}_${m[4]}`;
}

function parseA1ThirdPartyOfficialIds() {
  const text = fs.readFileSync(A1, 'utf8');
  const blocks = text.split(/\n(?=- requirement_id:)/);
  const ids = [];
  for (const b of blocks) {
    if (!/coverage_status:\s*third_party/.test(b)) continue;
    for (const m of b.matchAll(/metric_id:\s*(TEMP_ALGO_[A-Z0-9_-]+)/g)) {
      const off = tempToOfficial(m[1]);
      if (off) ids.push({ temp: m[1], official: off });
    }
  }
  return ids;
}

function isQueryResult(row) {
  const id = String(row.metric_id || '');
  const name = String(row.metric_name_zh || '');
  return /_QUERY$/.test(id) || name.includes('查询结果');
}

function pageIdsOf(row) {
  const refs = row.extras?.srs_refs || [];
  const pages = [];
  for (const r of refs) {
    for (const p of r.page_ids || []) pages.push(String(p));
  }
  return pages;
}

function classify(row) {
  const id = row.metric_id;
  const domain = row.domain_code || '';
  const type = row.algorithm_type || 'UNKNOWN';
  const pages = pageIdsOf(row);
  const reasons = [];

  if (KEEP_STAT.has(id)) {
    return { action: 'keep', reasons: ['态势要素计数：智树 ADS STAT'] };
  }
  if (isQueryResult(row)) {
    return { action: 'keep', reasons: ['查询结果：n/a_ops，不进九新/third_party'] };
  }
  if (KEEP_ZHISHU_ID_RE.test(id)) {
    return { action: 'keep', reasons: ['DS-07 科技创新评估：展示态势完整链路'] };
  }

  if (TOPIC_345.has(domain)) {
    reasons.push(`专题3/4/5域 ${domain}：智树不实现`);
  }
  if (DISPLAY_API_ID_RE.test(id)) {
    reasons.push('展示人才态势/知识图谱页 OPEN 号');
  }
  if (pages.some((p) => /DS-(?:13|14|15|16|21|22|23|24)/.test(p))) {
    reasons.push(`srs page_ids=${pages.filter((p) => /DS-(?:13|14|15|16|21|22|23|24)/.test(p)).join(',')}`);
  }
  if (INNOV_TALENT_ALLOW.has(id)) {
    reasons.push('展示态势外采：人才指数/专家');
  }

  if (reasons.length === 0) return { action: 'keep', reasons: ['不在智树外包切面'] };
  if (type === 'third_party') return { action: 'already', reasons };
  return { action: 'set', reasons };
}

function allSeedRows() {
  const out = [];
  for (const domain of [
    'ENT',
    'CHAIN',
    'SVC',
    'POLICY',
    'SYNTH',
    'INNOV',
    'TECH',
    'ORG',
    'TALENT',
    'COMMON',
    'TNIE',
  ]) {
    const r = queryMetrics({ domain, limit: 2000, fields: 'full' });
    out.push(...r.metrics);
  }
  return out;
}

function applySeed(ids) {
  const files = fs
    .readdirSync(REGISTRY)
    .filter((n) => n.startsWith('cfg_metric-') && n.endsWith('-seed.yaml'))
    .sort();
  const want = new Set(ids);
  const done = [];
  for (const f of files) {
    const filePath = path.join(REGISTRY, f);
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
    for (const line of lines) {
      const mid = line.match(/^  - metric_id:\s*['"]?([^'"\s]+)/);
      if (mid) {
        curId = mid[1];
        out.push(line);
        continue;
      }
      const at = line.match(/^(\s*)algorithm_type:\s*(.*)$/);
      if (at && curId && want.has(curId)) {
        const val = at[2].trim().replace(/^['"]|['"]$/g, '');
        if (val !== 'third_party') {
          out.push(`${at[1]}algorithm_type: third_party`);
          replaced++;
          done.push({ id: curId, from: val, file: f });
        } else {
          out.push(line);
        }
        continue;
      }
      out.push(line);
    }
    if (APPLY && replaced) {
      let result = out.join(eol);
      if (hasBom) result = '\uFEFF' + result;
      fs.writeFileSync(filePath, result, 'utf8');
    }
  }
  return done;
}

const a1 = parseA1ThirdPartyOfficialIds();
const rows = allSeedRows();
const byId = new Map(rows.map((r) => [r.metric_id, r]));

const a1MissingInSeed = a1.filter((x) => !byId.has(x.official));
const decisions = [];
for (const row of rows) {
  const c = classify(row);
  decisions.push({
    metric_id: row.metric_id,
    domain: row.domain_code,
    name: row.metric_name_zh,
    from: row.algorithm_type,
    action: c.action,
    reasons: c.reasons,
  });
}

const toSet = decisions.filter((d) => d.action === 'set');
const already = decisions.filter((d) => d.action === 'already');
const kept = decisions.filter((d) => d.action === 'keep' && TOPIC_345.has(d.domain));

const applied = APPLY ? applySeed(toSet.map((d) => d.metric_id)) : [];
if (APPLY) invalidateMetricCache();
const after = summarizeMetrics();

const report = {
  apply: APPLY,
  a1_third_party_reqs: a1.length,
  a1_official_missing_in_seed: a1MissingInSeed,
  set: toSet.length,
  already: already.length,
  keep_in_topic_345: kept,
  by_from: toSet.reduce((m, d) => {
    m[d.from] = (m[d.from] || 0) + 1;
    return m;
  }, {}),
  by_domain: toSet.reduce((m, d) => {
    m[d.domain] = (m[d.domain] || 0) + 1;
    return m;
  }, {}),
  to_set: toSet,
  already_sample_n: already.length,
  applied,
  type_after: after.by_algorithm_type,
  total_after: after.total,
};

const outJson = path.join(__dirname, APPLY ? 'apply-result.json' : 'dry-run.json');
fs.writeFileSync(outJson, JSON.stringify(report, null, 2), 'utf8');
console.log(
  JSON.stringify(
    {
      apply: APPLY,
      a1_third_party: a1.length,
      a1_missing_seed: a1MissingInSeed.length,
      set: toSet.length,
      already: already.length,
      keep_topic_345: kept.length,
      by_from: report.by_from,
      by_domain: report.by_domain,
      type_after: after.by_algorithm_type,
      json: outJson,
    },
    null,
    2,
  ),
);
