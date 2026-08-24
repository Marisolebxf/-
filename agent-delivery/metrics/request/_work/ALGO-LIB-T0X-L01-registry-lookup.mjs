import fs from "node:fs";
import { getMetric, summarizeMetrics } from "../../../../scripts/lib/metric-registry-lib.mjs";

const idsPath = process.argv[2];
const ids = JSON.parse(fs.readFileSync(idsPath, "utf8"));
const summary = summarizeMetrics();
const rows = ids.map((id) => {
  const r = getMetric(id);
  if (r.error) return { metric_id: id, seed: false, matrix: false, missing: true };
  return {
    metric_id: id,
    seed: Boolean(r.found?.seed),
    matrix: Boolean(r.found?.matrix),
    algorithm_type: r.kit?.algorithm_type || r.algorithm_type || null,
    d1: r.readiness?.d1_def_status || r.d1 || null,
    missing: false,
  };
});
process.stdout.write(JSON.stringify({ summary, rows }));
