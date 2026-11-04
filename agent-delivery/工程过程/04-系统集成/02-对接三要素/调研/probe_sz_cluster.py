# -*- coding: utf-8 -*-
"""Probe the ads_sz_gkx_industry_cluster* tables and compare with our DIM.

Read-only SELECTs on both sides. No passwords printed.
"""
import io
import json
import os
import re
import sys
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW", "DESCRIBE"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def jx_conn():
    password = os.environ.get("JX_ADS_PASSWORD")
    if not password:
        raise SystemExit("set JX_ADS_PASSWORD")
    return pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=password,
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20,
        read_timeout=120,
        charset="utf8mb4",
    )


def our_conn():
    # gkxlumenx password from env or helm values; never printed
    pw = os.environ.get("DIM_MYSQL_PASSWORD")
    if not pw:
        vals = Path(r"e:\zhipu\gkx-lumen\repos\demo-svc-platform\helm\gkx-platform\values.yaml").read_text(encoding="utf-8")
        m = re.search(r"INNOV_MYSQL_PASSWORD\s*\n?\s*value:\s*\"([^\"]+)\"", vals)
        pw = m.group(1) if m else ""
    if not pw:
        raise SystemExit("set DIM_MYSQL_PASSWORD")
    return pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=pw,
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=60, charset="utf8mb4",
    )


def show(title, rows, limit=25):
    print(f"== {title} ({len(rows)} rows)")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:400])


def main():
    conn = jx_conn()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        doris_read(cur, "SELECT * FROM ads_sz_gkx_industry_cluster ORDER BY cluster_code")
        show("cluster", cur.fetchall(), 20)
        doris_read(cur, "SELECT cluster_code, COUNT(*) n, COUNT(DISTINCT subfield_id) subfields "
                        "FROM ads_sz_gkx_industry_cluster_subfield GROUP BY cluster_code ORDER BY cluster_code")
        show("subfield by cluster", cur.fetchall(), 20)
        doris_read(cur, "SELECT relation_type, review_status, COUNT(*) n FROM ads_sz_gkx_industry_cluster_subfield "
                        "GROUP BY relation_type, review_status")
        show("subfield relation/status", cur.fetchall(), 10)
        doris_read(cur, "SELECT * FROM ads_sz_gkx_industry_cluster_subfield LIMIT 8")
        show("subfield sample", cur.fetchall(), 8)
        doris_read(cur, "SELECT industry_chain_stage, review_status, relation_type, COUNT(*) n "
                        "FROM ads_sz_gkx_industry_cluster_topic GROUP BY industry_chain_stage, review_status, relation_type")
        show("topic stage/status", cur.fetchall(), 15)
        doris_read(cur, "SELECT * FROM ads_sz_gkx_industry_cluster_topic LIMIT 6")
        show("topic sample", cur.fetchall(), 6)
        doris_read(cur, "SELECT cluster_release_id, mapping_release_id, metric_definition_version, MAX(data_version) dv, "
                        "MAX(update_time) ts FROM ads_sz_gkx_industry_cluster GROUP BY cluster_release_id, mapping_release_id, metric_definition_version")
        show("release/version", cur.fetchall(), 10)
        # shenzhen institution funding tables too (industry hook via funding)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT institution_id) inst FROM ads_shenzhen_institution_direction_funding")
        show("sz funding", cur.fetchall(), 5)
    finally:
        conn.close()

    conn = our_conn()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT cluster_id, cluster_name, cluster_group, is_active FROM industry_cluster ORDER BY cluster_id")
        show("our industry_cluster", cur.fetchall(), 20)
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT cluster_id) clusters, COUNT(DISTINCT industry_id) industries FROM industry_cluster_map WHERE is_active=1")
        show("our industry_cluster_map", cur.fetchall(), 5)
        cur.execute("SELECT cluster_id, industry_id FROM industry_cluster_map WHERE is_active=1 ORDER BY cluster_id, industry_id LIMIT 25")
        show("our map sample", cur.fetchall(), 25)
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT subfield_id) subfields, COUNT(DISTINCT industry_id) industries FROM subfield_topic_map")
        show("our subfield_topic_map", cur.fetchall(), 5)
        cur.execute("SELECT DISTINCT subfield_id FROM subfield_topic_map LIMIT 5")
        show("our subfield id format", cur.fetchall(), 5)
        cur.execute("SELECT DISTINCT node_id, node_name FROM subfield_topic_map LIMIT 8")
        show("our node sample", cur.fetchall(), 8)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
