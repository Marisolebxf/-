# -*- coding: utf-8 -*-
"""Topic-bridge feasibility probe: can Topic (platform topic_id) be the bridge
between our chain nodes and Jiuxin's three elements?

Read-only. Checks:
1. Topic coverage: talent topics / subfields, paper topics, institution topics
2. subfield_topic_map topic-level linkage potential (our subfield -> jiuxin topic)
3. emerging topic tables as candidate aggregation layer
"""
import json
import os
import re
import sys
from pathlib import Path

import pymysql


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def show(title, rows, limit=20):
    print(f"== {title} ({len(rows)})")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:340])


def main():
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=os.environ["JX_ADS_PASSWORD"],
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20, read_timeout=240, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # Topic dictionary size
        doris_read(cur, "SELECT COUNT(*) n FROM ads_discipline_topic")
        show("discipline_topic rows", cur.fetchall(), 3)
        doris_read(cur, "SELECT COUNT(DISTINCT subfield_id) subs FROM ads_discipline_topic")
        show("topics by subfield distinct", cur.fetchall(), 3)
        doris_read(cur, "SELECT s.subfield_id, s.name_zh, COUNT(t.topic_id) topics "
                        "FROM ads_discipline_topic t JOIN ads_discipline_subfield s ON t.subfield_id=s.subfield_id "
                        "GROUP BY s.subfield_id, s.name_zh ORDER BY topics DESC LIMIT 10")
        show("top subfields by topic count", cur.fetchall(), 10)

        # Talent topic coverage (avoid array column scan: use topic_profile)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT talent_id) talents, COUNT(DISTINCT topic_id) topics "
                        "FROM ads_talent_topic_profile")
        show("talent_topic_profile", cur.fetchall(), 3)

        # Institution topic coverage
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT institution_id) insts, COUNT(DISTINCT topic_id) topics "
                        "FROM ads_institution_topic_entry")
        show("institution_topic_entry", cur.fetchall(), 3)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT institution_id) insts, COUNT(DISTINCT topic_id) topics "
                        "FROM ads_institution_discipline_profile")
        show("institution_discipline_profile", cur.fetchall(), 3)

        # Paper topic coverage (bulk table: use lightweight aggregation via topic_profile instead)
        doris_read(cur, "SELECT COUNT(*) n FROM ads_paper_profile")
        show("paper rows", cur.fetchall(), 3)

        # Emerging topic yearly as aggregate layer (4,516 topics)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT topic_id) topics FROM ads_emerging_topic_yearly_metrics")
        show("emerging yearly metrics", cur.fetchall(), 3)
        doris_read(cur, "SELECT topic_id, topic_name_zh, paper_count FROM ads_emerging_topic_snapshot "
                        "ORDER BY paper_count DESC LIMIT 8")
        show("emerging snapshot top", cur.fetchall(), 8)

        # Patent analysis by topic (new family, 365k rows)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT topic_id) topics FROM ads_patent_analysis_topic")
        show("patent_analysis_topic", cur.fetchall(), 3)
        doris_read(cur, "SELECT COUNT(*) n, COUNT(DISTINCT assignee_id) assignees FROM ads_patent_analysis_topic_assignee LIMIT 1")
        try:
            show("patent topic assignee", cur.fetchall(), 3)
        except Exception:
            pass
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
