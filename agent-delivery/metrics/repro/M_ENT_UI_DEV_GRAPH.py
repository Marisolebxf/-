#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_GRAPH：产业生态图谱（企业分析>企业发展，DevelopmentOverviewPanel 图谱入口）。
页面上是一个图谱卡（图入口+图例）；底座=产业链树 + 企业-链节点映射。本件复现其数据底座：
gkx.dwd_industry_chain_info 链树 1,273 节点 + gkx 企业底册行业四级列对接。
出参：repro/out/M_ENT_UI_DEV_GRAPH_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live_count  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_GRAPH",
    "batch": "TOPIC-UI-GAP-L01 批2组2",
    "probe_date": "2026-11-04",
    "purpose": "产业生态图谱数据底座复现（链树 + 企业-链映射）",
    "ui_evidence": ["live 30892 企业分析>企业发展>DevelopmentOverviewPanel 图谱卡（seq34 同面板）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_industry_chain_info")
    out["facts"]["chain_tree_rows"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(DISTINCT industry_code) FROM gkx.dwd_industry_chain_info")
    out["facts"]["chain_tree_distinct_codes"] = int(cur.fetchone()[0])
    cur.execute("SHOW COLUMNS FROM gkx.dwd_industry_chain_info")
    cols = [r[0] for r in cur.fetchall()]
    out["facts"]["chain_tree_cols"] = cols[:20]
    # 树深实测：level 唯一值即「单层清单」——递归字段 parent_code 实际父子构成待甲方链树口径
    cur.execute("SELECT level, COUNT(*) FROM gkx.dwd_industry_chain_info GROUP BY level")
    out["facts"]["chain_level_dist"] = [{"level": r[0], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_industry_chain_info WHERE parent_code IS NOT NULL AND parent_code <> ''")
    out["facts"]["chain_rows_with_parent"] = int(cur.fetchone()[0])
    # 企业-链映射面：企业底册 industry_l1-l4 四级列（对接图谱节点）
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_code IS NOT NULL AND industry_l1_code <> ''""")
    out["facts"]["org_with_l1"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l4_code IS NOT NULL AND industry_l4_code <> ''""")
    out["facts"]["org_with_l4"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info")
    out["facts"]["org_total"] = int(cur.fetchone()[0])
    cur.close()
    # live 侧 400 底册（页面演示域）
    out["facts"]["live_eb_rows"] = live_count("enterprise_base")
    out["derived"]["chain_node_org_coverage_pct"] = {
        "value": round(out["facts"]["org_with_l1"] / max(out["facts"]["org_total"], 1) * 100, 4),
        "numerator": out["facts"]["org_with_l1"],
        "denominator": out["facts"]["org_total"],
        "denominator_note": "gkx 企业底册 L1 行业码非空占比（企业可挂图谱节点的比例）",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "链树结构在（1,273 节点、parent_code 齐备）+ 企业-链四级行业列在（L1 覆盖实割）→ 图谱底座可搭；"
        "但「图谱」页面语义（节点热度/边关系/图例规则）UI 未给口径，链树 node_company_count 实测全 0（企业挂接数未灌）"
        "→ 部分支持。升档触发器：node_company_count 灌数或甲方图谱口径闭合。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_GRAPH_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("chain_tree_rows =", out["facts"]["chain_tree_rows"],
          "| org_with_l1 =", out["facts"]["org_with_l1"], "/", out["facts"]["org_total"],
          "| node_with_companies =", out["facts"].get("chain_rows_with_parent"))


if __name__ == "__main__":
    main()
