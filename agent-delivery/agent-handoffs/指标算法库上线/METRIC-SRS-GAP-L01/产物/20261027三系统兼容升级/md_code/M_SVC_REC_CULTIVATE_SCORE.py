#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SVC_REC_CULTIVATE_SCORE 培育综合评分（W14-S2）。

数据面：只读 code/_snapshots21/svc21_rec_20261023.json（族级快照，零 DB）。
口径：王惠四维 + calc-logic 会签的等权默认。技术创新能力两分子列（研发人员、研发投入）
整列为空 → 该维恒缺，按「缺维 = 可用维均值」不参与合成；服务成效以重要新闻条数代理；
市场缺口以「池内同行业营收份额」代理。正文显式声明「本件口径，非甲方口径」。

运行：cd code && python3 M_SVC_REC_CULTIVATE_SCORE.py
产出：code/M_SVC_REC_CULTIVATE_SCORE_out.json
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FAMILY = os.path.join(SNAP, "svc21_rec_20261023.json")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
OUT = os.path.join(HERE, "M_SVC_REC_CULTIVATE_SCORE_out.json")


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    fam = json.load(open(FAMILY, encoding="utf-8"))
    facts = json.load(open(FACTS, encoding="utf-8"))
    names = {o: (v.get("name") or "") for o, v in facts["pool"].items()}
    c = fam["cultivate"]
    pop = fam["pool"]
    cov = c["dim_coverage"]

    dims = {
        "现有规模": {
            "weight": 0.25, "within_weights": [0.5, 0.5], "status": "可算（低覆盖）",
            "indicators": ["从业人员数 employees_number", "资产总额 total_assets"],
            "coverage": {"employees": cov["employees"], "assets": cov["assets"]},
            "raw_dist": {"employees": c["dim_dist"]["employees"], "assets": c["dim_dist"]["assets"]},
            "score_dist": c["dim_scores"]["现有规模"],
        },
        "技术创新能力": {
            "weight": 0.25, "within_weights": [0.5, 0.5], "status": "恒缺",
            "indicators": ["研发人员占比 development_employee / employees_number",
                           "研发投入强度 arch_development_am / operating_revenue"],
            "coverage": {"rd_people": cov["rd_people"], "rd_ratio": cov["rd_ratio"]},
            "raw_dist": {"rd_people": {"n": 0}, "rd_ratio": {"n": 0}},
            "score_dist": c["dim_scores"]["技术创新能力"],
            "why": "dwd_org_annual_financial_info 全表 90,926 行中两列 0 行非空——列建好未灌数，不是覆盖率低",
        },
        "服务成效": {
            "weight": 0.25, "within_weights": [0.5, 0.5], "status": "仅代理",
            "indicators": ["服务企业数 svc_served_ent_count（待建）", "服务项目数 svc_project_count（待建）"],
            "proxy": "dwd_org_important_news_info 重要新闻条数（两条待建字段均无承载表）",
            "coverage": {"news": cov["news"]},
            "raw_dist": {"news": c["dim_dist"]["news"]},
            "score_dist": c["dim_scores"]["服务成效"],
        },
        "市场缺口": {
            "weight": 0.25, "within_weights": None, "status": "代理可算",
            "indicators": ["市场占有率 = 机构营业收入 ÷ 池内同门类营收合计"],
            "coverage": {"revenue": cov["revenue"], "share": cov["share"]},
            "raw_dist": {"revenue": c["dim_dist"]["revenue"], "market_share_pct": c["dim_dist"]["market_share_pct"]},
            "score_dist": c["dim_scores"]["市场缺口"],
            "why": "目标市场同类机构清单（旧稿 svc_org_card.industry）无 gkx 承载，降级为池内同门类（base_info.industry）",
        },
    }

    top = [{"org_id": oid, "name": names.get(oid, ""), "score": sc} for oid, sc in c["score"]["top10"]]
    vec = c["org_vec"]
    # 「现有规模」维非空 ⇔ 员工数或资产总额至少一项有值（org_vec[o][0]=avg(c_emp,c_assets)）；
    # 原产物把这项写死成 1030，此处改为从快照逐机构复算，数值不变（808+717−495 重叠＝1,030）
    scale_union = sum(1 for v in vec.values() if v[0] is not None)
    dims_cnt = {int(k): v for k, v in c["score"]["dims_count_dist"]}
    for t in top:
        v = vec.get(t["org_id"]) or [None, None, None, None]
        t["dims"] = {"现有规模": v[0], "技术创新能力": v[1], "服务成效": v[2], "市场缺口": v[3]}
        avail = [x for x in v if x is not None]
        t["dims_available"] = len(avail)
        t["mean_of_available"] = round(sum(avail) / len(avail), 4) if avail else None

    out = {
        "metric_id": "M_SVC_REC_CULTIVATE_SCORE",
        "metric_name": "培育综合评分",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_constructible",
        "base_years_used": list(range(2013, 2026)),
        "base_years_missing": list(range(2007, 2013)),
        "base_years_note": (
            "非固定年窗：现有规模取每家机构最近一个有值的年报年（从业人员/资产总额），"
            "窗口随机构而异；财务表在池内非空值只落 2013—2025，2007—2012 池内 0 行非空，"
            "列入 missing，不按 0 摊入。服务成效的新闻条数无年份窗口（全历史累计）；"
            "市场缺口取最近一个有值年的营业收入，同门类分母只汇总同一年的有值机构。"
        ),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "mode": "read-only",
             "tables": ["dwd_org_org_product_info", "dwd_org_base_info",
                        "dwd_org_annual_financial_info", "dwd_org_important_news_info"],
             "snapshot": "code/_snapshots21/svc21_rec_20261023.json",
             "upstream": fam["source"]["upstream"]},
        ],
        "params": {
            "population": "city='深圳市' 的服务机构",
            "population_n": c["target_population"],
            "dim_weights": c["weights"]["dim"],
            "within_weights": c["weights"]["within"],
            "normalization": "极值归一化 0—100；计数型（人数/资产/新闻/营收）先 log(1+x) 再归一化；比率型直接归一化",
            "missing_rule": "缺维 = 可用维得分等权均值；可用维 < 2 不入榜",
            "market_share_rule": "同门类 = dwd_org_base_info.industry 一级门类；营收 ≤ 0 视为缺失",
            "non_authoritative": "本件口径，非甲方口径",
            "finance_rows_total": 90926,
            "finance_orgs_pool": 6759,
            "finance_orgs_sz": 3946,
        },
        "derived": {
            "sz_share_of_pool_pct": dec(
                round(pop["sz"] / pop["total"] * 100, 4), pop["sz"], pop["total"],
                "分子=深圳服务机构数 rec.pool.sz（25,597 家）；"
                "分母=服务机构池总数 rec.pool.total（44,153 家，含 21 家城市未标注）"),
            "employees_pct": dec(
                round(cov["employees"] / c["target_population"] * 100, 4),
                cov["employees"], c["target_population"],
                "分子=年报里从业人员数（employees_number）至少一年有值且非 0 的深圳机构数"
                "（cultivate.dim_coverage.employees，808 家）；分母=深圳服务机构池 25,597 家"
                "（cultivate.target_population）"),
            "assets_pct": dec(
                round(cov["assets"] / c["target_population"] * 100, 4),
                cov["assets"], c["target_population"],
                "分子=年报里资产总额（total_assets）至少一年有值且非 0 的深圳机构数"
                "（cultivate.dim_coverage.assets，717 家）；分母=深圳服务机构池 25,597 家"),
            "news_pct": dec(
                round(cov["news"] / c["target_population"] * 100, 4),
                cov["news"], c["target_population"],
                "分子=有重点新闻条数的深圳机构数（cultivate.dim_coverage.news，13,732 家）；"
                "分母=深圳服务机构池 25,597 家。服务成效维以新闻条数代理"),
            "revenue_pct": dec(
                round(cov["revenue"] / c["target_population"] * 100, 4),
                cov["revenue"], c["target_population"],
                "分子=年报里营业收入（operating_revenue）至少一年有值且非 0 的深圳机构数"
                "（cultivate.dim_coverage.revenue，673 家，尚有 1 家为非正值已单列 revenue_nonpositive）；"
                "分母=深圳服务机构池 25,597 家"),
            "share_pct_of_pop": dec(
                round(cov["share"] / c["target_population"] * 100, 4),
                cov["share"], c["target_population"],
                "分子=能算出「同门类营收份额」的深圳机构数（cultivate.dim_coverage.share，672 家）；"
                "分母=深圳服务机构池 25,597 家。比 revenue 少 1 家是营收非正值无法进份额"),
            "scored_share_pct": dec(
                round(c["score"]["scored_orgs"] / c["target_population"] * 100, 4),
                c["score"]["scored_orgs"], c["target_population"],
                "分子=可用维 ≥2、进入综合分排名的深圳机构数 cultivate.score.scored_orgs（981 家）；"
                "分母=深圳服务机构池 25,597 家"),
            "scale_union": dec(
                scale_union, scale_union, None,
                "计数，无分母：员工数或资产总额至少一项有值的深圳机构数（由 org_vec 首维逐机构复算："
                "808 员工 + 717 资产 − 495 两项都有的重叠 ＝ 1,030 家）"),
            "scale_union_pct": dec(
                round(scale_union / c["target_population"] * 100, 4),
                scale_union, c["target_population"],
                "分子=现有规模维有值的深圳机构数（员工数或资产总额至少一项有值，1,030 家）；"
                "分母=深圳服务机构池 25,597 家"),
            "two_dim_orgs": dec(
                dims_cnt.get(2), dims_cnt.get(2), None,
                "计数，无分母：可用维恰为 2 的机构数（cultivate.score.dims_count_dist 中 '2' 档，425 家）"),
            "three_dim_orgs": dec(
                dims_cnt.get(3), dims_cnt.get(3), None,
                "计数，无分母：可用维恰为 3 的机构数（cultivate.score.dims_count_dist 中 '3' 档，556 家）。"
                "四维齐全 0 家，因技术创新能力两列全表为空"),
        },
        "population": {
            "total": pop["total"],
            "sz": pop["sz"],
            "sz_share_of_pool_pct": round(pop["sz"] / pop["total"] * 100, 4),
            "unassigned_city": pop["unassigned_city"],
            "sz_ind_rows": pop["sz_ind_rows"],
            "sz_size_rows": pop["sz_size_rows"],
        },
        "dimensions": dims,
        "value": {
            "scored_orgs": c["score"]["scored_orgs"],
            "scored_share_pct": round(c["score"]["scored_orgs"] / c["target_population"] * 100, 4),
            "dims_count_dist": c["score"]["dims_count_dist"],
            "score_dist": c["score"]["score_dist"],
            "score_deciles": c["score"]["score_deciles"],
            "top10": top,
        },
        "worked_example": {
            "org_id": top[0]["org_id"],
            "name": top[0]["name"],
            "dims": top[0]["dims"],
            "dims_available": top[0]["dims_available"],
            "mean_of_available": top[0]["mean_of_available"],
            "score": top[0]["score"],
            "note": "三维可用（技术创新能力恒缺）：(100.0 + 54.247 + 99.9981) / 3 = 84.7484",
        },
        "robustness": {
            "entropy_weights": c["entropy_weights"],
            "rank_corr": c["rank_corr"],
            "reading": ("综合分与服务成效（新闻条数）秩相关 0.7527、与现有规模 0.7559、"
                        "与市场缺口 -0.0250；市场缺口经极值归一化后 672 家里 p90 仅 0.1048 分，"
                        "实际不参与排序。综合分在可算机构上近似「规模 + 新闻量」的等权合成。"),
        },
        "gaps": [
            {"gap": "研发人员数", "detail": "development_employee 全表 0 行非空", "impact": "技术创新能力维恒缺"},
            {"gap": "研发投入", "detail": "arch_development_am 全表 0 行非空", "impact": "同上"},
            {"gap": "服务企业数/服务项目数", "detail": "svc_served_ent_count / svc_project_count 待建，无承载表",
             "impact": "服务成效只能用新闻条数代理，口径不对齐"},
            {"gap": "同行业营收总额", "detail": "目标市场同类机构清单缺失，降级为池内同门类",
             "impact": "份额分母偏小；单机构门类必得 100 分（2 个门类）"},
            {"gap": "财务覆盖", "detail": "深圳 25,597 家中仅 673 家有正营收、808 家有从业人数、717 家有资产",
             "impact": "四维齐全 0 家，合成只能是三维"},
        ],
        "cross_refs": {
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/SVC/M_SVC_REC_CULTIVATE_SCORE.md",
            "（正本见本目录 M_SVC_REC_CULTIVATE_SCORE.md / calc-logic 入库件）",
            "sibling": ["M_SVC_REC_ATTRACT_SCORE", "M_SVC_REC_CANDIDATE_CNT"],
        },
    }

    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("written", OUT)
    print("population", out["population"]["sz"], "scored", out["value"]["scored_orgs"],
          "share", out["value"]["scored_share_pct"])
    print("median", out["value"]["score_dist"]["median"], "max", out["value"]["score_dist"]["max"])
    print("coverage", cov)


if __name__ == "__main__":
    main()
