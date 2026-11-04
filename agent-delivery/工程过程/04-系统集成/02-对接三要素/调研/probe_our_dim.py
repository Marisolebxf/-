# -*- coding: utf-8 -*-
"""Probe our demo DIM tables (industry_cluster / industry_cluster_map / subfield_topic_map)."""
import json
import os
import re
import sys
from pathlib import Path

import pymysql

PW = os.environ.get("DIM_MYSQL_PASSWORD", "")


def show(title, rows, limit=30):
    print(f"== {title} ({len(rows)} rows)")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:300])


def main():
    conn = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=PW,
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=60, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT cluster_id, cluster_name, cluster_group, is_active FROM industry_cluster ORDER BY cluster_id")
        show("our industry_cluster", cur.fetchall(), 20)
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT cluster_id) clusters, COUNT(DISTINCT industry_id) industries "
                    "FROM industry_cluster_map WHERE is_active=1")
        show("our industry_cluster_map", cur.fetchall(), 5)
        cur.execute("SELECT cluster_id, industry_id FROM industry_cluster_map WHERE is_active=1 ORDER BY cluster_id, industry_id LIMIT 25")
        show("our map sample", cur.fetchall(), 25)
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT subfield_id) subfields, COUNT(DISTINCT industry_id) industries "
                    "FROM subfield_topic_map")
        show("our subfield_topic_map", cur.fetchall(), 5)
        cur.execute("SELECT DISTINCT subfield_id FROM subfield_topic_map LIMIT 5")
        show("our subfield id format", cur.fetchall(), 5)
        cur.execute("SELECT DISTINCT node_id, node_name FROM subfield_topic_map LIMIT 8")
        show("our node sample", cur.fetchall(), 8)
        cur.execute("SELECT COUNT(DISTINCT subfield_id) n FROM subfield_topic_map")
        our_subs = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(DISTINCT discipline_id) n FROM discipline_subfield")
        print("== counts:", "our mapped subfields", our_subs)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
