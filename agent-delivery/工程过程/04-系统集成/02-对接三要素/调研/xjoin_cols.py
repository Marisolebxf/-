# -*- coding: utf-8 -*-
"""Dump column names for key tables, then probe with correct names."""
import json
import os
import sys

import pymysql


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW", "DESCRIBE"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def cols(cur, table):
    doris_read(cur, f"SHOW FULL COLUMNS FROM {table}")
    return [c["Field"] for c in cur.fetchall()]


def show(title, rows, limit=25):
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
        for t in ("ads_industry", "ads_institution_industry", "ads_talent_industry_activity",
                  "ads_technology_commercial_value_simulation"):
            show(t, [{"col": c} for c in cols(cur, t)], 60)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
