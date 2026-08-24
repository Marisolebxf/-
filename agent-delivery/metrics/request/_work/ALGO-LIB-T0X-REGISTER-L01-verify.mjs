import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getMetric, loadCatalog } from "../../../../scripts/lib/metric-registry-lib.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const plan = JSON.parse(
  fs.readFileSync(path.join(dir, "ALGO-LIB-T0X-REGISTER-L01-plan.json"), "utf8"),
);
loadCatalog(true);

const extra = [
  "M_ENT_KEY_TOTAL",
  "M_CHAIN_REG_COMMERCIALIZATION",
  "M_CHAIN_LINK_HEALTH",
  "M_CHAIN_GLOBAL_CASE_MATCH",
];
const ids = [
  ...plan.fl_rows.map((r) => r.metric_id),
  ...extra,
  ...Object.values(plan.temp_map).slice(0, 5),
];

let fail = 0;
const rows = [];
for (const id of ids) {
  const r = getMetric(id);
  const seed = Boolean(r.found?.seed);
  const at = r.kit?.algorithm_type || r.algorithm_type;
  const d1 = r.readiness?.d1_def_status || r.d1;
  const isFlReuse = plan.fl_rows.some((r) => r.metric_id === id && r.action === "reuse");
  const ok = seed && (isFlReuse || (at === "UNKNOWN" && (d1 === "draft" || d1 == null)));
  if (!ok) fail += 1;
  rows.push({
    metric_id: id,
    seed,
    matrix: Boolean(r.found?.matrix),
    algorithm_type: at,
    d1,
    ok,
    error: r.error || null,
  });
}

const out = {
  checked: rows.length,
  fail,
  fl: plan.fl_rows.length,
  fl_seed: plan.fl_rows.filter((r) => getMetric(r.metric_id).found?.seed).length,
  rows: rows.filter((x) => !x.ok),
};
process.stdout.write(JSON.stringify(out, null, 2));
if (fail) process.exit(1);
