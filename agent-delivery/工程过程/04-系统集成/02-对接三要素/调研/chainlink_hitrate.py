# -*- coding: utf-8 -*-
"""Final hit-rate check: can our chain nodes reach jiuxin GB codes / stm nodes?

Also checks tech-side attach points (technology tables' industry columns).
"""
import json
import os
import re
import sys
from pathlib import Path

import pymysql


def show(title, rows, limit=20):
    print(f"== {title} ({len(rows)})")
    for r in rows[:limit]:
        print("  ", json.dumps(r, ensure_ascii=False, default=str)[:320])


def main():
    # our dim: stm node overlap with chain nodes
    dim = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx",
        password=os.environ.get("DIM_MYSQL_PASSWORD", "GKX@Lumen2026"),
        database="demo_gkxlumenx_dim", connect_timeout=15, read_timeout=120, charset="utf8mb4",
    )
    dwd = pymysql.connect(
        host="10.50.11.76", port=3306, user="gkxlumenx",
        password=os.environ.get("DIM_MYSQL_PASSWORD", "GKX@Lumen2026"),
        database="demo_gkxlumenx_dwd", connect_timeout=15, read_timeout=120, charset="utf8mb4",
    )
    try:
        cur = dim.cursor()
        cur.execute("SELECT DISTINCT node_id FROM subfield_topic_map WHERE node_id IS NOT NULL AND node_id<>''")
        stm_nodes = {r[0] for r in cur.fetchall()}
        cur.execute("SELECT DISTINCT industry_id FROM subfield_topic_map WHERE industry_id IS NOT NULL")
        stm_inds = {r[0] for r in cur.fetchall()}
        cur.execute("SELECT DISTINCT subfield_id FROM subfield_topic_map")
        stm_subs = {r[0] for r in cur.fetchall()}
    finally:
        dim.close()

    try:
        cur = dwd.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT node_id, node_name, node_level, chain_id FROM industry_chain_node WHERE is_deleted=0")
        nodes = cur.fetchall()
        node_ids = {r["node_id"] for r in nodes}
        # direct hits: stm node_id ∈ chain node ids
        direct = stm_nodes & node_ids
        # root-code hits: stm industry_id (INB7位) is a root of chain node
        root_hit = {i for i in stm_inds if any(nid.startswith(i) for nid in node_ids)}
        # entity_rel node granularity
        cur.execute("SELECT COUNT(DISTINCT node_id) nodes_with_ent FROM industry_chain_entity_rel WHERE node_id IS NOT NULL AND node_id<>''")
        ent_nodes = cur.fetchone()["nodes_with_ent"]
        # tech node map table (WBS-02-12 target)
        try:
            cur.execute("SELECT COUNT(*) n, COUNT(DISTINCT node_id) inds, SUM(CASE WHEN technology_node_id IS NOT NULL AND technology_node_id<>'' THEN 1 ELSE 0 END) linked FROM dwd_tech_node_industry_map")
            show("tech_node_industry_map state", cur.fetchall(), 3)
        except Exception as e:
            print("tech map probe failed:", str(e)[:140])
    finally:
        dwd.close()

    print("== hit rates")
    print("stm node_ids:", len(stm_nodes), "| chain node_ids:", len(node_ids))
    print("direct node hits (stm.node_id ∈ chain):", len(direct), sorted(direct)[:8])
    print("root hits (stm.industry_id is prefix of chain nodes):", len(root_hit), "/", len(stm_inds), sorted(root_hit))
    chain_roots = {nid[:7] for nid in node_ids}
    print("chain root families:", sorted(chain_roots))
    print("entity_rel distinct nodes:", ent_nodes)
    covered = chain_roots & stm_inds
    print("root families covered by stm industries:", len(covered), "/", len(chain_roots), sorted(covered))
    return 0


if __name__ == "__main__":
    sys.exit(main())
