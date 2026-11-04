# -*- coding: utf-8 -*-
"""CHAIN-ELEM-LINK probe: key mapping rates across the three candidate paths.

Read-only on both sides. Jiuxin via Doris, ours via demo DIM/DWD MySQL.
"""
import json
import os
import re
import sys
from pathlib import Path

import pymysql

DIM_PW = os.environ.get("DIM_MYSQL_PASSWORD", "")
DWD_PW = DIM_PW
if not DIM_PW:
    vals = Path(r"e:\zhipu\gkx-lumen\repos\demo-svc-platform\helm\gkx-platform\values.yaml").read_text(encoding="utf-8")
    m = re.search(r"INNOV_MYSQL_PASSWORD\s*\n?\s*value:\s*\"([^\"]+)\"", vals)
    if m:
        DIM_PW = DWD_PW = m.group(1)


def show(title, rows, limit=20):
    print(f"== {title} ({len(rows)})")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:340])


def main():
    # ---- our side: dim (subfield_topic_map, cluster map) ----
    dim = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=DIM_PW,
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=120, charset="utf8mb4",
    )
    try:
        cur = dim.cursor(pymysql.cursors.DictCursor)
        # subfield_topic_map node_id format
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT node_id) nodes FROM subfield_topic_map WHERE node_id IS NOT NULL AND node_id<>''")
        show("stm rows with node", cur.fetchall(), 3)
        cur.execute("SELECT DISTINCT node_id FROM subfield_topic_map WHERE node_id IS NOT NULL LIMIT 10")
        show("stm node_id format", cur.fetchall(), 10)
        cur.execute("SELECT COUNT(DISTINCT industry_id) inds FROM subfield_topic_map WHERE industry_id IS NOT NULL AND industry_id<>''")
        show("stm industries", cur.fetchall(), 3)
        cur.execute("SELECT DISTINCT industry_id FROM subfield_topic_map WHERE industry_id IS NOT NULL ORDER BY industry_id LIMIT 15")
        show("stm industry codes", cur.fetchall(), 15)
    finally:
        dim.close()

    # ---- our side: dwd chain nodes ----
    dwd = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=DWD_PW,
        database="demo_gkxlumenx_dwd", connect_timeout=15, read_timeout=180, charset="utf8mb4",
    )
    try:
        cur = dwd.cursor(pymysql.cursors.DictCursor)
        # node_id root codes: INB12xx / INB13xx families in chain nodes
        cur.execute("""SELECT SUBSTRING(node_id,1,7) AS root, COUNT(*) n FROM industry_chain_node
                       WHERE node_id LIKE 'INB%' GROUP BY root ORDER BY n DESC LIMIT 20""")
        show("chain node root codes", cur.fetchall(), 20)
        cur.execute("""SELECT COUNT(*) n, SUM(CASE WHEN node_id LIKE 'INB%' THEN 1 ELSE 0 END) inb FROM industry_chain_node""")
        show("chain node inb share", cur.fetchall(), 3)

        # Path ②: GB-code bridge — does our chain carry GB/T 4754 codes anywhere?
        try:
            cur.execute("SELECT industry_code, industry_name, COUNT(*) n FROM industry_chain GROUP BY industry_code, industry_name ORDER BY n DESC LIMIT 15")
            show("industry_chain codes (GB?)", cur.fetchall(), 15)
        except Exception as e:
            print("industry_chain probe failed:", str(e)[:160])
    finally:
        dwd.close()

    # ---- jiuxin side: institution_industry GB code overlap & talent industry coverage ----
    pw = os.environ.get("JX_ADS_PASSWORD")
    if not pw:
        doc = Path(r"e:\zhipu\gkx-lumen\gkx-orchestration\agent-delivery\工程过程\04-系统集成\02-对接三要素\对接文档\对端\数据库链接信息.md").read_text(encoding="utf-8")
        m = re.search(r"初始密码：(.+)$", doc, re.M)
        pw = m.group(1).strip() if m else ""
    jx = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=pw,
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=180, charset="utf8mb4",
    )
    try:
        cur = jx.cursor(pymysql.cursors.DictCursor)
        # GB code structure in jiuxin
        cur.execute("SELECT industry_level, industry_level_name, COUNT(*) n FROM ads_industry GROUP BY industry_level, industry_level_name ORDER BY industry_level")
        show("jiuxin GB levels", cur.fetchall(), 8)
        cur.execute("SELECT industry_code, industry_name_zh, industry_level FROM ads_industry WHERE industry_level IN (2,3) LIMIT 15")
        show("jiuxin GB 2-3 codes", cur.fetchall(), 15)
        # institution_industry: which GB codes covered
        cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT industry_code) codes FROM ads_institution_industry")
        show("inst industry coverage", cur.fetchall(), 3)
        cur.execute("SELECT industry_code, industry_name_zh, COUNT(*) n FROM ads_institution_industry GROUP BY industry_code, industry_name_zh ORDER BY n DESC LIMIT 12")
        show("inst industry top codes", cur.fetchall(), 12)
        # talent industry: which taxonomy
        cur.execute("SELECT taxonomy_id, COUNT(*) n, COUNT(DISTINCT industry_id) inds FROM ads_talent_industry_activity GROUP BY taxonomy_id")
        show("talent industry taxonomy", cur.fetchall(), 5)
        cur.execute("SELECT industry_code, COUNT(DISTINCT talent_id) talents FROM ads_talent_industry_activity GROUP BY industry_code ORDER BY talents DESC LIMIT 10")
        show("talent top industries", cur.fetchall(), 10)
    finally:
        jx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
