# -*- coding: utf-8 -*-
"""Cross-check subfield IDs: Jiuxin ads_sz_gkx_industry_cluster_subfield vs our
demo_gkxlumenx_dim.discipline_subfield + subfield_topic_map + industry_cluster_map."""
import json
import os
import sys
from pathlib import Path

import pymysql

PW = os.environ.get("DIM_MYSQL_PASSWORD", "")


def jx():
    return pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=os.environ["JX_ADS_PASSWORD"],
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=120, charset="utf8mb4",
    )


def ours():
    return pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=PW,
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=60, charset="utf8mb4",
    )


def main():
    conn = jx()
    try:
        cur = conn.cursor()
        cur.execute("SELECT cluster_code, subfield_id, subfield_name_zh, openalex_subfield_id, relation_type "
                    "FROM ads_sz_gkx_industry_cluster_subfield")
        jrows = cur.fetchall()
    finally:
        conn.close()
    j_ids = {r[1]: (r[2], r[3], r[4]) for r in jrows}

    conn = ours()
    try:
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = {r[0] for r in cur.fetchall()}
        print("our dim tables:", sorted(tables))
        disc = {}
        if "discipline_subfield" in tables:
            cur.execute("SELECT subfield_id, name_zh, openalex_id FROM discipline_subfield")
            disc = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
        cur.execute("SELECT cluster_id, industry_id FROM industry_cluster_map WHERE is_active=1")
        cmap = cur.fetchall()
        cur.execute("SELECT DISTINCT subfield_id FROM subfield_topic_map")
        linked = {r[0] for r in cur.fetchall()}
        cur.execute("SELECT subfield_id, COUNT(*) n FROM subfield_topic_map GROUP BY subfield_id")
        linked_n = {r[0]: r[1] for r in cur.fetchall()}
    finally:
        conn.close()

    print()
    print("jiuxin cluster subfields:", len(j_ids), "distinct", len(set(j_ids)))
    print("our discipline_subfield rows:", len(disc))
    both = set(j_ids) & set(disc)
    print("id overlap jiuxin-vs-discipline_subfield:", len(both), "/", len(j_ids))
    name_mismatch = [i for i in both if (disc[i][0] or "") != (j_ids[i][0] or "")]
    print("name mismatches:", len(name_mismatch), name_mismatch[:5])
    print("openalex id mismatches:", [i for i in both if str(disc[i][1]) != str(j_ids[i][2])][:5])
    print("jiuxin-only ids:", len(set(j_ids) - set(disc)))
    in_linked = set(j_ids) & linked
    print("jiuxin cluster subfields already linked in subfield_topic_map:", len(in_linked))
    cover = {}
    for i in in_linked:
        cover[i] = linked_n[i]
    print("avg links per covered subfield:", round(sum(cover.values()) / len(cover), 2) if cover else 0)
    print()
    print("jiuxin CORE subfields not yet in our cluster->L0 map (cluster has no mapped L0):")
    print("our cluster_map rows:", len(cmap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
