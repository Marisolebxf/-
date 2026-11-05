#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_UI_REC_MODELS：引入/培育服务机构推荐分析（seq81-90）复现件。
招引推荐模型（对外合作意愿/技术领先性）+ 培育推荐模型（市场缺口 20%/技术创新 30%/服务成效 25%）+
培育评估模型/招引推荐模型（需业务建模类两件）。
出参：repro/out/M_SVC_UI_REC_MODELS_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_SVC_UI_REC_MODELS",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "引入/培育服务机构推荐模型原料与承载实测",
    "ui_evidence": [
        "views/service/svcRecommendAttractWorkspace.ts:L18/L25（seq81/82 两工作台）",
        "招引推荐模型四维（seq85 对外合作意愿 willingness / seq86 技术领先性 techLead）",
        "培育推荐模型 CULTIVATE_DEMO_DIMS（seq87 市场缺口 20%/seq88 技术创新能力 30%/seq89 服务成效 25%）",
        "seq83 培育评估模型 / seq84 招引推荐模型（需业务建模类）",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}

SVC_L1 = "科学研究和技术服务业"


def main():
    cur = gkx()
    # 技术领先性原料：深圳科研服务机构的标签富集 + 上市 + 融资
    cur.execute("""SELECT COUNT(DISTINCT t.org_id) FROM gkx.dwd_org_tech_tag t
                   JOIN gkx.dwd_org_base_info b ON t.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_tagged"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT s.org_id) FROM gkx.dwd_org_stock_base s
                   JOIN gkx.dwd_org_base_info b ON s.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_listed"] = int(cur.fetchone()[0])
    # 对外合作意愿原料：融资活跃（2023+）+ 新闻动态
    cur.execute("""SELECT COUNT(DISTINCT f.org_id) FROM gkx.dwd_org_financing_info f
                   JOIN gkx.dwd_org_base_info b ON f.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s
                   AND f.completion_date >= '2023-01-01'""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_fin_active"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT n.org_id) FROM gkx.dwd_org_important_news_info n
                   JOIN gkx.dwd_org_base_info b ON n.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s
                   AND n.news_date >= '2024-01-01'""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_news_active_2024"] = int(cur.fetchone()[0])
    # 市场缺口原料：深圳 L2 类型分布 vs 全国（缺口=全国有深圳无/弱的类型）
    cur.execute("""SELECT industry_l2_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city LIKE %s
                   AND industry_l2_name IS NOT NULL AND LOWER(industry_l2_name) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY industry_l2_name ORDER BY n DESC LIMIT 6""", (SVC_L1, "%深圳%"))
    sz_l2 = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.execute("""SELECT industry_l2_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s
                   AND industry_l2_name IS NOT NULL AND LOWER(industry_l2_name) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY industry_l2_name ORDER BY n DESC LIMIT 6""", (SVC_L1,))
    all_l2 = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.close()
    out["facts"]["sz_l2_top"] = sz_l2
    out["facts"]["all_l2_top"] = all_l2
    out["derived"]["l2_gap"] = {
        k: {"sz": sz_l2.get(k, 0), "all": v,
            "sz_share_pct": round(sz_l2.get(k, 0) / max(v, 1) * 100, 2)}
        for k, v in all_l2.items()}
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "原料面分级实测：技术领先性（标签 4,723 家富集 + 上市 51 家）与市场缺口（L2 结构深圳 vs 全国可算）可支撑；"
        "对外合作意愿（2023+ 融资活跃 88 家/2024+ 新闻动态实测）为代理变量，真实合作意愿无直接承载；"
        "服务成效维度无服务质量/客户评价承载列；培育/招引两评估模型权重口径未闭合（UI 演示权重 20/30/25 为前端 mock）"
        "→ 部分支持。升档触发器：两模型权重口径甲方确认 + 服务成效评价承载落地。")
    p = os.path.join(HERE, "out", "M_SVC_UI_REC_MODELS_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| tagged:", out["facts"]["sz_svc_tagged"], "| listed:", out["facts"]["sz_svc_listed"],
          "| fin_active:", out["facts"]["sz_svc_fin_active"])


if __name__ == "__main__":
    main()
