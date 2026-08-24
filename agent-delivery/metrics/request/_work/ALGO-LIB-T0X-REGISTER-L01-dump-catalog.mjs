import { loadCatalog } from "../../../../scripts/lib/metric-registry-lib.mjs";

const catalog = loadCatalog();
const ids = [];
for (const [id, rec] of catalog.byId) {
  ids.push({
    metric_id: id,
    seed: Boolean(rec.seed),
    matrix: Boolean(rec.matrix),
  });
}
process.stdout.write(JSON.stringify(ids));
