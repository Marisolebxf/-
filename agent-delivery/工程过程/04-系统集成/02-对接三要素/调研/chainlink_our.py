# -*- coding: utf-8 -*-
"""CHAIN-ELEM-LINK probe, our side: demo demo_gkxlumenx_dim / dwd chain tables.

Read-only. Password from helm values via env DIM_MYSQL_PASSWORD.
"""
import json
import os
import re
import sys
from pathlib import Path

import pymysql

PW_ENV = os.environ.get("DIM_MYSQL_PASSWORD", "")
if not PW_ENV:
    vals = Path(r"e:\zhipu\gkx-lumen\repos\demo-svc-platform\helm\gkx-platform\values.yaml").read_text(encoding="utf-8")
    m = re.search(r"INNOV_MYSQL_PASSWORD\s*\n?\s*value:\s*\"([^\"]+)\"", vals)
    PW_ENV = m.group(1) if m else ""


def show(title, rows, limit=20):
    print(f"== {title} ({len(rows)})")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:340])


def main():
    conn = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx", password=PW_ENV,
        database="demo_gkxlumenx_dwd", connect_timeout=15, read_timeout=120, charset="utf8mb4",
    )
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SHOW TABLES")
        tables = [list(r.values())[0] for r in cur.fetchall()]
        chain_tables = [t for t in tables if "chain" in t or "industry" in t]
        show("chain/industry tables in dwd", [{"t": t} for t in chain_tables], 30)

        if "industry_chain_node" in tables:
            cur.execute("SHOW FULL COLUMNS FROM industry_chain_node")
            show("industry_chain_node cols", [{"c": c["Field"], "cm": (c.get("Comment") or "")[:50]} for c in cur.fetchall()], 25)
            cur.execute("SELECT COUNT(*) n FROM industry_chain_node")
            show("node count", cur.fetchall(), 2)
            cur.execute("SELECT * FROM industry_chain_node LIMIT 8")
            show("node sample", cur.fetchall(), 8)

        if "industry_chain_entity_rel" in tables:
            cur.execute("SHOW FULL COLUMNS FROM industry_chain_entity_rel")
            show("entity_rel cols", [{"c": c["Field"], "cm": (c.get("Comment") or "")[:50]} for c in cur.fetchall()], 20)
            cur.execute("SELECT COUNT(*) n, SUM(CASE WHEN node_id IS NULL OR node_id='' THEN 1 ELSE 0 END) empty_node FROM industry_chain_entity_rel")
            show("entity_rel node_id emptiness", cur.fetchall(), 3)
            cur.execute("SELECT node_id, COUNT(*) n FROM industry_chain_entity_rel WHERE node_id IS NOT NULL AND node_id<>'' GROUP BY node_id ORDER BY n DESC LIMIT 10")
            show("entity_rel top node_ids", cur.fetchall(), 10)
            cur.execute("SELECT entity_type, COUNT(*) n FROM industry_chain_entity_rel GROUP BY entity_type")
            show("entity_rel types", cur.fetchall(), 10)

        if "industry_chain_info" in tables:
            cur.execute("SHOW FULL COLUMNS FROM industry_chain_info")
            show("chain_info cols", [{"c": c["Field"], "cm": (c.get("Comment") or "")[:50]} for c in cur.fetchall()], 20)
            cur.execute("SELECT COUNT(*) n FROM industry_chain_info")
            show("chain count", cur.fetchall(), 2)
            codecol = None
            cur.execute("SHOW FULL COLUMNS FROM industry_chain_info")
            for c in cur.fetchall():
                if c["Field"] == "industry_code":
                    codecol = "industry_code"
            if codecol:
                cur.execute(f"SELECT {codecol} AS code, COUNT(*) n FROM industry_chain_info GROUP BY {codecol} ORDER BY n DESC LIMIT 15")
                show("chain codes", cur.fetchall(), 15)

        if "enterprise_industry_chain" in tables:
            cur.execute("SELECT chain_code, COUNT(*) n FROM enterprise_industry_chain WHERE chain_code IS NOT NULL AND chain_code<>'' GROUP BY chain_code ORDER BY n DESC LIMIT 15")
            show("ent chain_code dist", cur.fetchall(), 15)
            cur.execute("SELECT COUNT(*) n, SUM(CASE WHEN node_id IS NULL OR node_id='' THEN 1 ELSE 0 END) empty_node FROM enterprise_industry_chain")
            show("ent chain node emptiness", cur.fetchall(), 3)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
