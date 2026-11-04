# -*- coding: utf-8 -*-
"""Compare Jiuxin ads_sz_gkx_industry_cluster* with our seed
industry-cluster-sz-10+5-2026.yaml. Read-only: Jiuxin via Doris SELECT,
our side from the in-repo seed (DIM unreachable from this network today).
"""
import json
import os
import re
import sys
from pathlib import Path

import pymysql
import yaml

HERE = Path(__file__).resolve().parent
SEED = Path(__file__).resolve().parents[4] / "data" / "data-design" / "storage" / "CHAIN" / "seeds" / "industry-cluster-sz-10+5-2026.yaml"


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW", "DESCRIBE"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def main():
    seed = yaml.safe_load(SEED.read_text(encoding="utf-8"))
    ours = {c["cluster_id"]: c for c in seed["clusters"]}
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=os.environ["JX_ADS_PASSWORD"],
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=120, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        doris_read(cur, "SELECT cluster_code, cluster_name_zh, group_name, industry_names, industry_member_count "
                        "FROM ads_sz_gkx_industry_cluster ORDER BY cluster_code")
        theirs = {r["cluster_code"]: r for r in cur.fetchall()}
        doris_read(cur, "SELECT cluster_code, subfield_id, subfield_name_zh, openalex_subfield_id, relation_type, mapping_weight "
                        "FROM ads_sz_gkx_industry_cluster_subfield ORDER BY cluster_code, subfield_id")
        subs = cur.fetchall()
        doris_read(cur, "SELECT cluster_code, COUNT(*) topics, SUM(industry_chain_stage='UPSTREAM') up, "
                        "SUM(industry_chain_stage='MIDSTREAM') mid, SUM(industry_chain_stage='DOWNSTREAM') down "
                        "FROM ads_sz_gkx_industry_cluster_topic GROUP BY cluster_code ORDER BY cluster_code")
        stages = {r["cluster_code"]: r for r in cur.fetchall()}
    finally:
        conn.close()

    print("== cluster-by-cluster: theirs (Jiuxin) vs ours (seed)")
    all_codes = sorted(set(theirs) | set(ours))
    for code in all_codes:
        t = theirs.get(code)
        o = ours.get(code)
        if t and o:
            names_t = json.loads(t["industry_names"])
            ok = t["cluster_name_zh"] == o["name"] and t["group_name"][:3].lower() == o["group"][:3]
            flag = "OK " if ok else "DIFF"
            print(f"{flag} {code} {t['cluster_name_zh']} / {o['name']} | {t['group_name']} / {o['group']} | L0 ours {len(o['l0'])}")
            print(f"     theirs industries: {names_t}")
            print(f"     ours L0: {[l['industry_id'] + ' ' + l['name'] for l in o['l0']]}")
            st = stages.get(code, {})
            print(f"     subfields {len([s for s in subs if s['cluster_code']==code])}, "
                  f"topics {st.get('topics')} (up {st.get('up')} / mid {st.get('mid')} / down {st.get('down')})")
        elif t:
            print(f"THEIRS-ONLY {code} {t['cluster_name_zh']}")
        else:
            print(f"OURS-ONLY   {code} {o['name']}")

    print()
    print("== subfield id overlap with our subfield_topic_map (from previous probe: ids like sub_<hex32>)")
    sub_ids = {s["subfield_id"] for s in subs}
    print("jiuxin distinct subfield_id:", len(sub_ids))
    print("sample:", sorted(sub_ids)[:5])
    return 0


if __name__ == "__main__":
    sys.exit(main())
