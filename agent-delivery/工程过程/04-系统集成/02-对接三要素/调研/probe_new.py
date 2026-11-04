# -*- coding: utf-8 -*-
"""Probe the fresh scan for specific questions. Read-only on the JSON."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "_raw_schema.json").read_text(encoding="utf-8"))
cols = {}
for c in data["columns"]:
    cols.setdefault(c["table"], []).append(c)
tables = {t["table"]: t for t in data["tables"]}

# 1. keywords for the six 还没有 metrics
PROBES = {
    "invest/amount": ["invest", "funding", "amount_cny"],
    "barrier/communication": ["barrier", "communicat", "沟通"],
    "culture": ["culture", "融合"],
    "resistance": ["resist", "阻力"],
    "cost": ["cost", "成本"],
    "pain/bottleneck": ["pain", "bottleneck", "痛点", "堵点", "难点"],
}
for label, needles in PROBES.items():
    hits = []
    for t, cs in cols.items():
        for c in cs:
            cl = c["column"].lower()
            if any(n.lower() in cl for n in needles):
                hits.append(f"{t}.{c['column']}")
    print(f"[{label}] {len(hits)}")
    for h in hits[:25]:
        print("   ", h)

# 2. where did tech_id / mapping_status go
print("[tech_id / mapping_status]")
for t, cs in cols.items():
    for c in cs:
        if c["column"] in ("tech_id", "mapping_status"):
            print("   ", f"{t}.{c['column']}")

# 3. sz_gkx tables detail
for t in ("ads_sz_gkx_industry_cluster", "ads_sz_gkx_industry_cluster_subfield", "ads_sz_gkx_industry_cluster_topic"):
    print(f"[{t}] rows={tables[t]['table_rows']}")
    for c in cols[t]:
        print("   ", c["column"], c["type"], (c.get("comment") or "")[:60])

# 4. new families' table counts
fams = ["ads_media_", "ads_patent_analysis_", "ads_recommendation_", "ads_research_outcome_",
        "ads_resource_", "ads_shenzhen_institution_", "ads_sz_gkx_", "ads_talent_capability_",
        "ads_technology_disruption_", "ads_topic_country"]
for fam in fams:
    ts = [t for t in tables if t.startswith(fam)]
    print(f"[fam {fam}] {len(ts)} tables, {sum(tables[t]['table_rows'] or 0 for t in ts)} rows")

# 5. research_problem vs research_outcome overlap check
print("[institution_news cols]")
for c in cols.get("ads_institution_news", []):
    print("   ", c["column"], (c.get("comment") or "")[:60])
print("[tech hotspot staging tables]")
for t in ("ads_technology_hotspot_signal", "ads_technology_hotspot_signal_filter_stage_20261031", "ads_technology_hotspot_signal_unfiltered_20261031"):
    print("   ", t, tables[t]["table_rows"])
