# 把 MCP metric-query(domain=TALENT, fields=full) 的输出压成一行一条，供 C01 盘点引用（只读）
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for m in d["metrics"]:
    k, r = m.get("kit", {}), m.get("readiness", {})
    ex = m.get("extras", {})
    pages = sorted({p for s in ex.get("srs_refs", []) for p in s.get("page_ids", [])})
    print("|".join(map(str, [
        m["metric_id"], m["metric_name_zh"], m["algorithm_type"], m["d1"], m["d4"],
        ",".join(k.get("source_tables", [])), ",".join(k.get("source_systems", [])), k.get("update_freq"),
        r.get("d3_source_mapping_status"), r.get("d1_pending_ref"), ex.get("module"), m.get("srs_ref_count"),
        ",".join(pages)])))
