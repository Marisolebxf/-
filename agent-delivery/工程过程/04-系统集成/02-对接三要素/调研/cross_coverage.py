# -*- coding: utf-8 -*-
"""Final cross-check: which cluster/subfield combos from Jiuxin are already
covered by our subfield_topic_map via industry links, and where the gaps are."""
import json
import os
import sys

import pymysql

PW = os.environ.get("DIM_MYSQL_PASSWORD", "")


def main():
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=os.environ["JX_ADS_PASSWORD"],
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=120, charset="utf8mb4",
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT cluster_code, subfield_id, subfield_name_zh, relation_type, mapping_weight "
                    "FROM ads_sz_gkx_industry_cluster_subfield")
        jrows = cur.fetchall()
    finally:
        conn.close()

    conn = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=PW,
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=60, charset="utf8mb4",
    )
    try:
        cur = conn.cursor()
        cur.execute("""SELECT m.cluster_id, t.subfield_id, COUNT(DISTINCT t.industry_id)
            FROM industry_cluster_map m
            JOIN subfield_topic_map t ON FIND_IN_SET(
                (SELECT industry_id FROM industry_cluster_map m2 WHERE m2.cluster_id = m.cluster_id AND m2.is_active=1 LIMIT 1), '') >= 0
            GROUP BY m.cluster_id, t.subfield_id""")
        # simpler: fetch both and join in python
        cur.execute("SELECT cluster_id, industry_id FROM industry_cluster_map WHERE is_active=1")
        cmap = {}
        for cluster_id, industry_id in cur.fetchall():
            cmap.setdefault(cluster_id, []).append(industry_id)
        cur.execute("SELECT subfield_id, industry_id, node_id FROM subfield_topic_map")
        stm = cur.fetchall()
    finally:
        conn.close()

    by_sub = {}
    for subfield_id, industry_id, node_id in stm:
        by_sub.setdefault(subfield_id, set()).add(industry_id)

    print("cluster | CORE/映射覆盖情况（久新 67 条组合）")
    covered = 0
    partial = 0
    gaps = []
    for cluster_code, subfield_id, name_zh, relation, weight in sorted(jrows):
        linked_industries = by_sub.get(subfield_id, set())
        cluster_l0 = set(cmap.get(cluster_code, []))
        hit = linked_industries & cluster_l0
        if linked_industries and cluster_l0 and hit:
            covered += 1
            mark = "FULL"
        elif linked_industries and cluster_l0:
            partial += 1
            mark = "SUB-ONLY"
        elif cluster_l0:
            partial += 1
            mark = "CLUSTER-NO-SUB"
        else:
            gaps.append((cluster_code, subfield_id, name_zh, relation))
            mark = "GAP"
        if mark != "FULL":
            print(f"{mark:15} {cluster_code} {subfield_id} {name_zh} [{relation}] linked_to={sorted(linked_industries)} cluster_L0={sorted(cluster_l0)}")
    print()
    print(f"FULL {covered} / 67; non-full {67 - covered}; unmapped-cluster rows {len(gaps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
