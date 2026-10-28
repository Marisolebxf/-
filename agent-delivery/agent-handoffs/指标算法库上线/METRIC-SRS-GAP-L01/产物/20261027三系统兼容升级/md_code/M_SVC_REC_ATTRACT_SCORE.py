#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_REC_ATTRACT_SCORE 招引综合评分（W14-S2）。

数据面：只读 code/_snapshots21/svc21_rec_20261023.json（族级快照，零 DB）。
口径：王惠四维 + calc-logic 会签的等权默认；本件对「研发投入强度」「有效发明专利占比」
两处不可得子指标做显式降级（研发列全空 → 技术领先性仅由专利授权件数代理），
并在正文声明「本件口径，非甲方口径」。

运行：cd code && python3 M_SVC_REC_ATTRACT_SCORE.py
产出：code/M_SVC_REC_ATTRACT_SCORE_out.json
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAMILY = os.path.join(SNAP, "svc21_rec_20261023.json")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_REC_ATTRACT_SCORE_out.json")


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    fam = json.load(open(FAMILY, encoding="utf-8"))
    facts = json.load(open(FACTS, encoding="utf-8"))
    names = {o: (v.get("name") or "") for o, v in facts["pool"].items()}
    a = fam["attract"]
    pop = fam["pool"]

    dims = {}
    for key, label, raw_key, status, why in [
        ("industry", "产业匹配度", "industry_fit", "代理可算",
         "产业契合度用 12 个 20+8 集群标签命中数 ÷ 12；产业链协同度用投资/股东双向边数 ÷ 12 链去脏企业并集"),
        ("tech", "技术领先性", "tech_grant", "仅代理",
         "研发投入强度分子 arch_development_am 全表 0 行非空；有效发明专利占比无类型/法律状态；仅专利授权件数可算"),
        ("growth", "发展潜力", "rev_cagr", "覆盖极低",
         "营收/净利润 CAGR 需两个正值年；外部池仅 249 / 220 家有营收 CAGR，187 家两项齐全"),
        ("coop", "对外合作意愿", "out_edges", "代理可算",
         "对外合作项目数（svc_coop_project_count）待建；以 dwd_org_invest_info 出向投资边与覆盖城市数代理"),
    ]:
        dims[label] = {
            "status": status,
            "why": why,
            "weight": a["weights"]["dim"][label],
            "within_weights": a["weights"]["within"].get(label),
            "coverage": {
                "industry_fit": a["dim_coverage"]["industry_fit"],
                "chain_deg_nonzero": a["dim_coverage"]["chain_deg_nonzero"],
                "tech_grant": a["dim_coverage"]["tech_grant"],
                "growth_rev": a["dim_coverage"]["growth_rev"],
                "growth_np": a["dim_coverage"]["growth_np"],
                "growth_both": a["dim_coverage"]["growth_both"],
                "out_edges_nonzero": a["dim_coverage"]["out_edges_nonzero"],
                "region_cover": a["dim_coverage"]["region_cover"],
            },
            "raw_dist": a["dim_dist"].get(raw_key),
            "score_dist": a["dim_scores"].get(label),
        }

    top = []
    for oid, sc in a["score"]["top10"]:
        top.append({"org_id": oid, "name": names.get(oid, ""), "score": sc})

    out = {
        "metric_id": "M_SVC_REC_ATTRACT_SCORE",
        "metric_name": "招引综合评分",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_constructible",
        "base_years_used": list(range(2013, 2026)),
        "base_years_missing": list(range(2007, 2013)),
        "base_years_note": (
            "本件不是固定年窗指标：营收/净利润增长率取每家机构最近两个正值年算 CAGR，"
            "窗口随机构而异。财务表 gkx.dwd_org_annual_financial_info 在池内非空值只落在 "
            "2013—2025；2007—2012 在池内 0 行非空（整段无 data），故列入 missing 而不是按 0 摊入。"
            "规模/营收类不进入本件综合分，只作为发展潜力维的输入；专利侧不按年筛选（聚合无年份列）。"
        ),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["dwd_org_org_product_info", "dwd_org_base_info",
                        "dwd_org_industry_tags", "dwd_org_invest_info",
                        "dwd_org_shareholder_info", "dwd_org_annual_financial_info",
                        "dwd_patent"],
             "snapshot": "code/_snapshots21/svc21_rec_20261023.json",
             "upstream": fam["source"]["upstream"]},
        ],
        "params": {
            "population": "非深圳、且有城市的服务机构 = 广州 + 东莞 + 惠州",
            "population_n": a["target_population"],
            "excluded_unassigned_city": a["excluded_unassigned"],
            "dim_weights": a["weights"]["dim"],
            "within_weights": a["weights"]["within"],
            "normalization": "极值归一化 0—100；计数型指标先 log(1+x) 压缩再归一化",
            "missing_rule": "缺维 = 该机构可用维得分的等权均值；可用维 < 2 不入榜",
            "growth_rule": "最近两个正值年 CAGR，截断 −95%—+300%",
            "const": a["const"],
            "non_authoritative": "本件口径，非甲方口径",
            "finance_rows_total": 90926,
            "operating_revenue_rows": 2193,
            "rd_cols_nonnull": 0,
            "product_info_rows": 45011,
            "shareholder_edges_total": 372205,
            "no_patent_match": 8540,
        },
        "derived": {
            "external_share_of_pool_pct": dec(
                round(a["target_population"] / pop["total"] * 100, 4),
                a["target_population"], pop["total"],
                "分子=外部池（非深圳、有城市：广州+东莞+惠州）机构数 attract.target_population（18,535 家）；"
                "分母=服务机构池总数 rec.pool.total（44,153 家，含深圳 25,597 家与 21 家城市未标注）"),
            "industry_fit_pct": dec(
                round(a["dim_coverage"]["industry_fit"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["industry_fit"], a["target_population"],
                "分子=12 个 20+8 集群标签至少命中 1 个的外部机构数 dim_coverage.industry_fit（7,139 家）；"
                "分母=外部池 18,535 家（attract.target_population）"),
            "chain_nonzero_pct": dec(
                round(a["dim_coverage"]["chain_deg_nonzero"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["chain_deg_nonzero"], a["target_population"],
                "分子=投资/股东双向边能挂到 12 条链之一的外部机构数 dim_coverage.chain_deg_nonzero（3,568 家）；"
                "分母=外部池 18,535 家"),
            "tech_grant_pct": dec(
                round(a["dim_coverage"]["tech_grant"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["tech_grant"], a["target_population"],
                "分子=有专利授权件数的外部机构数 dim_coverage.tech_grant（9,995 家，技术领先性维唯一可用代理）；"
                "分母=外部池 18,535 家"),
            "growth_rev_pct": dec(
                round(a["dim_coverage"]["growth_rev"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["growth_rev"], a["target_population"],
                "分子=能算出营收 CAGR（需两个正值年）的外部机构数 dim_coverage.growth_rev（249 家）；"
                "分母=外部池 18,535 家"),
            "growth_both_pct": dec(
                round(a["dim_coverage"]["growth_both"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["growth_both"], a["target_population"],
                "分子=营收与净利润两项 CAGR 都齐的外部机构数 dim_coverage.growth_both（187 家）；"
                "分母=外部池 18,535 家。发展潜力维只对这一小撮可用"),
            "out_edges_pct": dec(
                round(a["dim_coverage"]["out_edges_nonzero"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["out_edges_nonzero"], a["target_population"],
                "分子=有出向投资边的外部机构数 dim_coverage.out_edges_nonzero（2,644 家，对外合作意愿代理）；"
                "分母=外部池 18,535 家"),
            "region_cover_pct": dec(
                round(a["dim_coverage"]["region_cover"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["region_cover"], a["target_population"],
                "分子=出向投资覆盖到城市的机构数 dim_coverage.region_cover（937 家，合作意愿的第二个子项）；"
                "分母=外部池 18,535 家"),
            "rev_any_pct": dec(
                round(a["dim_coverage"]["rev_any"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["rev_any"], a["target_population"],
                "分子=外部池里有任一营收年报的机构数 dim_coverage.rev_any（531 家）；"
                "分母=外部池 18,535 家"),
            "emp_any_pct": dec(
                round(a["dim_coverage"]["emp_any"] / a["target_population"] * 100, 4),
                a["dim_coverage"]["emp_any"], a["target_population"],
                "分子=外部池里有任一员工数年报的机构数 dim_coverage.emp_any（774 家）；"
                "分母=外部池 18,535 家"),
            "zero_pct": dec(
                round(a["score"]["score_dist"]["zeros"] / a["target_population"] * 100, 4),
                a["score"]["score_dist"]["zeros"], a["target_population"],
                "分子=综合分为 0 的外部机构数 score.score_dist.zeros；"
                "分母=外部池 18,535 家（不是入榜的 scored_orgs，故含未入榜者）"),
            "grid_tech_lead_pct": dec(
                round(a["weight_grid"]["winner_share"][0][1] / a["weight_grid"]["combos"] * 100, 4),
                a["weight_grid"]["winner_share"][0][1], a["weight_grid"]["combos"],
                "分子=权重网格里由「技术领先性」主导的组合数 weight_grid.winner_share[0][1]（1,076 个）；"
                "分母=权重网格组合总数 weight_grid.combos（1,771 个）。"
                "分子分母都是组合数，不是机构数"),
        },
        "population": {
            "total": pop["total"],
            "sz": pop["sz"],
            "external": pop["external"],
            "unassigned_city": pop["unassigned_city"],
            "city_rows": pop["city_rows"],
        },
        "dimensions": dims,
        "value": {
            "scored_orgs": a["score"]["scored_orgs"],
            "dims_count_dist": a["score"]["dims_count_dist"],
            "score_dist": a["score"]["score_dist"],
            "score_deciles": a["score"]["score_deciles"],
            "top10": top,
        },
        "robustness": {
            "entropy_weights": a["entropy_weights"],
            "weight_grid": a["weight_grid"],
            "rank_corr": a["rank_corr"],
            "reading": ("综合分与专利授权件数的秩相关 0.7279、与出向投资边 0.5771、与产业链度 0.5959；"
                        "权重网格 1,771 个 5% 组合里 1,076 个由技术领先性主导（60.76%），"
                        "说明名次对权重敏感，本件只发布分布与分位，不发布单一冠军榜。"),
        },
        "gaps": [
            {"gap": "研发投入强度", "detail": "arch_development_am 全表 90,926 行 0 行非空",
             "impact": "技术领先性失去一半定义，只剩专利代理"},
            {"gap": "有效发明专利占比", "detail": "仅有申请人名聚合的申请/授权件数，无专利类型与法律状态",
             "impact": "无法只取有效发明专利，代理口径偏宽"},
            {"gap": "对外合作项目数", "detail": "svc_coop_project_count 待建，gkx 280 表无承载",
             "impact": "以投资边代理，只覆盖 2,644 / 18,535 家"},
            {"gap": "财务覆盖", "detail": "外部池 531 / 18,535 家有营收年报（2.86%），187 家双增长率齐全",
             "impact": "发展潜力维只对 1.01% 的机构可用，综合分实际是三维合成"},
        ],
        "cross_refs": {
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_REC_ATTRACT_SCORE.md",
            "（正本见本目录 M_SVC_REC_ATTRACT_SCORE.md / calc-logic 入库件）",
            "sibling": ["M_SVC_REC_CULTIVATE_SCORE", "M_SVC_REC_CANDIDATE_CNT"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("population", out["population"]["external"], "scored", out["value"]["scored_orgs"])
    print("median", out["value"]["score_dist"]["median"], "p90", out["value"]["score_dist"]["p90"])
    print("coverage", a["dim_coverage"])


if __name__ == "__main__":
    main()
