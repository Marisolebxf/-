# -*- coding: utf-8 -*-
"""XJOIN feasibility probes v3 — schema-discovered columns. Read-only."""
import json
import os
import sys

import pymysql


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW", "DESCRIBE"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def colnames(cur, table):
    doris_read(cur, f"SHOW FULL COLUMNS FROM {table}")
    return [c["Field"] for c in cur.fetchall()]


def pick(names, *keywords):
    return [n for n in names if any(k in n.lower() for k in keywords)]


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
        connect_timeout=20, read_timeout=180, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # Scene 3: location
        loc_cols = colnames(cur, "ads_location")
        show("ads_location cols", [{"c": c} for c in loc_cols], 30)
        doris_read(cur, "SELECT * FROM ads_location WHERE location_id = 'loc_E16782C21F18EBF8A59C1E98F9C9860B'")
        show("shenzhen loc row", cur.fetchall(), 3)
        doris_read(cur, "SELECT id_namespace, COUNT(*) n, MIN(mapping_status) ms FROM ads_location_external_id "
                        "GROUP BY id_namespace ORDER BY n DESC")
        show("ext id namespaces", cur.fetchall(), 15)
        doris_read(cur, "SELECT COUNT(*) n FROM ads_location_external_id WHERE id_namespace='AMAP_ADCODE'")
        show("amap adcode count (GB-like)", cur.fetchall(), 3)
        doris_read(cur, "SELECT mapping_status, COUNT(*) n FROM ads_location_external_id GROUP BY mapping_status")
        show("mapping status", cur.fetchall(), 6)

        # Scene 4: institution identity
        doris_read(cur, "SELECT * FROM ads_institution_type ORDER BY institution_type_id")
        show("institution types", cur.fetchall(), 15)
        doris_read(cur, "SELECT institution_type_id, COUNT(*) n FROM ads_institution_profile GROUP BY institution_type_id ORDER BY n DESC")
        show("profile by type", cur.fetchall(), 15)
        ip_cols = colnames(cur, "ads_institution_profile")
        ident = pick(ip_cols, "credit", "usci", "legal", "register", "website", "domain", "homepage", "url")
        show("institution identity-ish cols", [{"c": c} for c in ident], 20)
        doris_read(cur, "SHOW FULL COLUMNS FROM ads_institution_profile")
        ipc = cur.fetchall()
        show("identity col comments", [{"c": c["Field"], "cm": (c.get("Comment") or "")[:70]} for c in ipc if c["Field"] in ident], 20)

        # Scene 5: policy evidence
        doris_read(cur, "SHOW FULL COLUMNS FROM ads_technology_policy_evidence")
        show("tech policy cols", cur.fetchall(), 18)
        doris_read(cur, "SELECT relation_type, COUNT(*) n FROM ads_research_problem_policy_evidence GROUP BY relation_type ORDER BY n DESC")
        show("rp policy relations", cur.fetchall(), 10)
        doris_read(cur, "SELECT statistics_year, COUNT(*) n FROM ads_research_problem_policy_evidence GROUP BY statistics_year ORDER BY 1 DESC LIMIT 8")
        show("rp policy years", cur.fetchall(), 8)

        # Scene 6: synthesis tables
        doris_read(cur, "SHOW TABLES LIKE '%synth%'")
        show("synth tables", cur.fetchall(), 10)
        doris_read(cur, "SHOW TABLES LIKE '%evaluation%'")
        show("evaluation tables", cur.fetchall(), 15)
        doris_read(cur, "SHOW TABLES LIKE '%recommendation%'")
        show("recommendation tables", cur.fetchall(), 12)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
