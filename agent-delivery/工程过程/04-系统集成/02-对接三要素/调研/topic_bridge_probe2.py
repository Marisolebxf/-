# -*- coding: utf-8 -*-
"""Topic-bridge supplementary probe v2 (fixed SQL)."""
import json
import os
import sys

import pymysql

FOCUS_SUBFIELD_KEYWORDS = ("机械工程", "电气与电子工程", "人工智能", "计算机视觉", "仪器科学", "能源工程", "生物", "材料", "交通", "海洋", "控制")


def doris_read(cur, sql, args=None):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql, args)


def show(title, rows, limit=20):
    print(f"== {title} ({len(rows)})")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:300])


def main():
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=os.environ["JX_ADS_PASSWORD"],
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=180, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        for kw in FOCUS_SUBFIELD_KEYWORDS:
            doris_read(cur, "SELECT s.name_zh AS subfield, t.name_zh AS topic, t.topic_id "
                            "FROM ads_discipline_topic t JOIN ads_discipline_subfield s ON t.subfield_id=s.subfield_id "
                            "WHERE s.name_zh LIKE %s LIMIT 3", (f"%{kw}%",))
            rows = cur.fetchall()
            if rows:
                show(f"subfield [{kw}]", rows, 3)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT topic_id) topics, SUM(patent_count) patents "
                        "FROM ads_patent_analysis_topic")
        show("patent_analysis_topic totals", cur.fetchall(), 3)
        doris_read(cur, "SELECT topic_name_zh, SUM(patent_count) patents FROM ads_patent_analysis_topic "
                        "WHERE topic_name_zh IS NOT NULL AND topic_name_zh<>'' GROUP BY topic_name_zh ORDER BY patents DESC LIMIT 10")
        show("patent by topic top", cur.fetchall(), 10)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
