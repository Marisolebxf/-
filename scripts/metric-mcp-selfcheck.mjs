#!/usr/bin/env node
/**
 * One runnable check for metric-registry-lib.
 * Fail the process if seed/matrix parse or join is broken.
 */
import {
  loadCatalog,
  getMetric,
  queryMetrics,
  summarizeMetrics,
} from './lib/metric-registry-lib.mjs';

let failed = 0;
function assert(cond, msg) {
  if (cond) {
    console.log(`ok  ${msg}`);
    return;
  }
  failed++;
  console.error(`FAIL  ${msg}`);
}

const catalog = loadCatalog(true);
const entSeed = catalog.seedFiles.find((f) => f.domain === 'ENT');
assert(Boolean(entSeed), 'ENT seed file loaded');
if (entSeed) {
  assert(
    entSeed.declared_total == null || entSeed.parsed === Number(entSeed.declared_total),
    `ENT seed parsed=${entSeed.parsed} declared=${entSeed.declared_total}`,
  );
}

const total = getMetric('M_ENT_TOTAL_COUNT');
assert(!total.error, `M_ENT_TOTAL_COUNT exists (${total.error || 'ok'})`);
assert(Boolean(total.kit?.definition), 'M_ENT_TOTAL_COUNT has definition');
assert(
  String(total.kit?.definition || '').includes('统一社会信用代码'),
  'M_ENT_TOTAL_COUNT definition mentions credit code',
);
assert(total.kit?.algorithm_type === 'UNKNOWN', 'missing algorithm_type → UNKNOWN');
assert(Boolean(total.found?.seed), 'M_ENT_TOTAL_COUNT found in seed');
if (total.found?.matrix) {
  assert(Boolean(total.readiness?.d4_ingestion_status), 'M_ENT_TOTAL_COUNT has D4');
} else {
  console.log('note  M_ENT_TOTAL_COUNT has no matrix row (honest miss)');
}

const byName = queryMetrics({ q: '企业总数', domain: 'ENT', limit: 8 });
assert(
  byName.metrics.some((m) => m.metric_id === 'M_ENT_TOTAL_COUNT'),
  'query 企业总数 hits M_ENT_TOTAL_COUNT',
);

const miss = getMetric('M_NO_SUCH_METRIC_XYZ');
assert(Boolean(miss.error), 'unknown id returns error');

const tnie = getMetric('M_TNIE_EVENT_COUNT');
assert(!tnie.error, 'M_TNIE_EVENT_COUNT exists');
assert(
  String(tnie.kit?.definition || '').includes('events'),
  'folded definition (>) parsed',
);
assert(
  Array.isArray(tnie.kit?.source_tables) && tnie.kit.source_tables.length >= 2,
  'TNIE block-list source_tables',
);

const chain = getMetric('M_CHAIN_MARKET_SIZE');
assert(!chain.error, 'M_CHAIN_MARKET_SIZE exists');
assert(
  Array.isArray(chain.kit?.source_tables) && chain.kit.source_tables.length >= 2,
  'CHAIN block-list source_tables',
);

const evalM = getMetric('M_ENT_TECH_POWER_SCORE');
assert(!evalM.error, 'M_ENT_TECH_POWER_SCORE exists');
assert(evalM.readiness?.d2_schema_detail?.mysql_dwd?.status === 'ready', 'nested d2_schema_detail');
assert(evalM.readiness?.d4_ingestion_stages?.ods_synced === 'todo', 'flow-map d4_ingestion_stages');
assert(evalM.found?.seed && evalM.found?.matrix, 'EVAL metric joined seed+matrix');

const sz = getMetric('M_CHAIN_SZ_ENTERPRISE_COUNT');
assert(!sz.error, 'CHAIN matrix-only-or-joined id exists');
assert(sz.readiness?.d1_def_status === 'aligned', 'CHAIN D1 from matrix');

const summary = summarizeMetrics();
assert(summary.total >= 100, `catalog size ${summary.total} >= 100`);
assert(Boolean(summary.coverage), 'summary has coverage');

const svc = summarizeMetrics('SVC');
assert(svc.coverage.matrix_only > 0 || svc.total > 0, 'SVC domain queryable');

if (failed) {
  console.error(`\n${failed} check(s) failed`);
  process.exit(1);
}
console.log('\nmetric-mcp-selfcheck passed');
