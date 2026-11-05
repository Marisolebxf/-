#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_CLUSTER_RANK：产业集群企业数量排名（企业分析>企业发展，DevelopmentOverviewPanel 排序指标）。
按产业集群统计企业数并排名。本件实测：集群映射仅在共享 demo dim（禁引），live DIM 16 表无集群面
→ 以 gkx L1 行业为集群代理复现统计口径；等 demo/正式集群映射授权落地即按映射表重算。
出参：repro/out/M_ENT_UI_DEV_CLUSTER_RANK_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live_count  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_CLUSTER_RANK",
    "batch": "TOPIC-UI-GAP-L01 批2组2",
    "probe_date": "2026-11-04",
    "purpose": "产业集群企业数量排名复现（集群代理=L1 行业；映射表授权后切换）",
    "ui_evidence": ["live 30892 企业分析>企业发展>DevelopmentOverviewPanel.vue:L3（seq35 排序指标）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT industry_l1_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name IS NOT NULL AND industry_l1_name <> ''
                   GROUP BY industry_l1_name ORDER BY n DESC LIMIT 10""")
    out["facts"]["l1_cluster_rank_top10"] = [{"cluster": r[0], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT COUNT(DISTINCT industry_l1_name) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name IS NOT NULL AND industry_l1_name <> ''""")
    out["facts"]["l1_distinct"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name IS NOT NULL AND industry_l1_name <> ''""")
    out["facts"]["org_with_l1"] = int(cur.fetchone()[0])
    cur.close()
    out["facts"]["live_eb_rows"] = live_count("enterprise_base")
    out["facts"]["live_dim_has_cluster_map"] = False
    out["derived"]["l1_top1_share_pct"] = {
        "value": round(out["facts"]["l1_cluster_rank_top10"][0]["n"] / max(out["facts"]["org_with_l1"], 1) * 100, 4),
        "numerator": out["facts"]["l1_cluster_rank_top10"][0]["n"],
        "denominator": out["facts"]["org_with_l1"],
        "denominator_note": "Top1 集群（制造业）企业数 / 有 L1 归属企业总数",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "统计口径可复现（GROUP BY 集群 → COUNT → 排名，Top10 实测落产物）；"
        "但「产业集群」语义映射表（Q068 口径 industry_cluster_map）仅存在于共享 demo dim——按铁律禁引禁写，"
        "live DIM 16 表实测无集群面 → 以 L1 行业为代理。升档触发器：集群映射表在可写库落地（append 档）。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_CLUSTER_RANK_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("l1_top10 =", [(x["cluster"][:8], x["n"]) for x in out["facts"]["l1_cluster_rank_top10"][:4]])


if __name__ == "__main__":
    main()
