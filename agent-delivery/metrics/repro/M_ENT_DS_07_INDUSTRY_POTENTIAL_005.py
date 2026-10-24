#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_DS_07_INDUSTRY_POTENTIAL_005 技术影响力评估（零 DB，族级快照重算）。

口径（calc-logic / Q009）：
  两维——专利被引影响力（SUM(cited_by_nums)/专利去重数）与标准必要专利（SEP 数量/占比）；
  两维极值归一后等权。对象是产业（12 条链），不是单件专利。

实测边界：
  · 被引表 20,515 行 / 20,000 件，仅 467 件能回连 `dwd_patent`（2.335%）；
  · 467 件里 98 家权利人落在底册、35 家落在 12 条链，链内专利合计 190 件；
  · SEP 表与列在 gkx / live 均不存在，第二维**未测**（不是 0）。
因此本件只交付被引维的可复算子项，不冒充两维合成后的「技术影响力」。
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_ds07_cited_20261023.json")
OUT = os.path.join(HERE, "M_ENT_DS_07_INDUSTRY_POTENTIAL_005_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else 0.0


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    chains = d["per_chain"]
    linked = d["patent_link"]
    agg = d["agg"]

    linked_chain_patents = sum(x["patent_n"] for x in chains)
    linked_chain_cited = sum(x["cited_sum"] for x in chains)

    # 被引子项：链内篇均 + 占可比池（链内 190 件）的份额
    for x in chains:
        x["cited_share_in_linked_pct"] = pct(x["cited_sum"], linked_chain_cited)
        x["patent_share_in_linked_pct"] = pct(x["patent_n"], linked_chain_patents)

    # 极值归一的被引子指数（仅 aux，不参与合成）
    vals = [x["mean_cited"] for x in chains]
    lo, hi = min(vals), max(vals)
    for x in chains:
        x["citation_subindex_0_100"] = round(
            (x["mean_cited"] - lo) / (hi - lo) * 100, 4) if hi > lo else 0.0

    ranked = [x for x in chains if x["patent_n"] > 0]
    zero_chains = [x for x in chains if x["patent_n"] == 0]

    # 集中度：Top10 权利人的被引占**全样本**份额；链内只占可比池
    top10 = d["top_applicants"][:10]
    top10_sum = sum(x["cited_sum"] for x in top10)

    # 派生比值：分子分母都取本件产物内的同名字段，正文只引用这里的结果
    huawei = next((x for x in d["top_applicants"] if x["applicant"].startswith("华为")), None)
    smart_terminal = next((x for x in chains if x["chain_name"] == "智能终端"), None)
    derived = {
        "unmatched_in_patent_n": agg["cited_patent_n"] - linked["matched_in_patent_n"],
        "zero_cited_patent_n": agg["cited_patent_n"] - agg["positive_patent_n"],
        "zero_cited_pct": pct(agg["cited_patent_n"] - agg["positive_patent_n"],
                              agg["cited_patent_n"]),
        "huawei_applicant": huawei["applicant"] if huawei else None,
        "huawei_cited_sum": huawei["cited_sum"] if huawei else None,
        "huawei_cited_share_of_linked_chain_pct": pct(huawei["cited_sum"], linked_chain_cited)
                                                   if huawei else 0.0,
        "smart_terminal_cited_sum": smart_terminal["cited_sum"] if smart_terminal else None,
        "huawei_cited_share_of_smart_terminal_chain_pct": pct(
            huawei["cited_sum"], smart_terminal["cited_sum"])
            if huawei and smart_terminal else 0.0,
        "pooled_mean_cited_uncovered_as_zero": round(
            agg["cited_sum"] / linked["patent_table_total"], 4)
            if linked["patent_table_total"] else 0.0,
        "denominator_note": "unmatched_in_patent_n = 被引专利 20,000 − 回连成功 467；"
                            "huawei_cited_share_of_linked_chain_pct 的分母是链内被引 415 次；"
                            "huawei_cited_share_of_smart_terminal_chain_pct 的分母是智能终端链被引 261 次；"
                            "pooled_mean_cited_uncovered_as_zero 的分母是全库专利 2,939,895 件。",
    }

    doc = {
        "metric_id": "M_ENT_DS_07_INDUSTRY_POTENTIAL_005",
        "metric_name": "技术影响力评估",
        "script": "M_ENT_DS_07_INDUSTRY_POTENTIAL_005.py",
        "data_source": "gkx @ 183.240.141.251:3318（只读）",
        "grain": "industry (12 chains) -> citation_impact_subscore + SEP(not_measurable)",
        "probes": {
            "cited_rows": agg["cited_rows"],
            "cited_patent_n": agg["cited_patent_n"],
            "cited_sum": agg["cited_sum"],
            "positive_patent_n": agg["positive_patent_n"],
            "positive_rate_pct": agg["positive_rate_pct"],
            "mean_cited": agg["mean_cited"],
            "median_cited": agg["median_cited"],
            "median_positive_cited": agg["median_positive_cited"],
            "max_cited": agg["max_cited"],
            "p90_cited": agg["p90_cited"],
            "patent_table_total": linked["patent_table_total"],
            "sample_share_pct": linked["sample_share_pct"],
            "matched_in_patent_n": linked["matched_in_patent_n"],
            "match_rate_pct": linked["match_rate_pct"],
            "matched_cited_sum": linked["matched_cited_sum"],
            "matched_share_of_cited_sum_pct": pct(linked["matched_cited_sum"], agg["cited_sum"]),
            "positive_mean_cited": round(agg["cited_sum"] / agg["positive_patent_n"], 4),
            "linked_share_of_matched_cited_pct": pct(linked_chain_cited, linked["matched_cited_sum"]),
            "unmatched_share_of_matched_cited_pct": pct(linked["unmatched_chain"]["cited_sum"], linked["matched_cited_sum"]),
            "applicant_n": linked["applicant_n"],
            "applicant_in_base_n": linked["applicant_in_base_n"],
            "applicant_in_chain_n": linked["applicant_in_chain_n"],
            "linked_chain_patent_n": linked_chain_patents,
            "linked_chain_cited_sum": linked_chain_cited,
            "linked_chain_patent_share_pct": pct(linked_chain_patents,
                                                 linked["matched_in_patent_n"]),
            "unmatched_chain": linked["unmatched_chain"],
            "chain_n_with_patent": len(ranked),
            "chain_n_zero": len(zero_chains),
            "zero_chain_names": [x["chain_name"] for x in zero_chains],
            "top10_citation_share_pct": d["top10_citation_share_pct"],
            "top10_citation_sum": top10_sum,
            "denominator_note": "篇均被引的分母是「该链可回连且去重的专利件数」，"
                                "份额分母是链内可比池 190 件 / 415 次；"
                                "不得用 2,939,895 件或 189,116 家做链内份额分母。",
        },
        "derived": derived,
        "probes_negative": {
            "sep_status": d["sep_probe"]["status"],
            "sep_patent_n": None,
            "sep_share_pct": None,
            "gkx_sep_tables": d["sep_probe"]["sep_like_tables_gkx"],
            "gkx_sep_columns": d["sep_probe"]["sep_like_columns_gkx"],
            "live_sep": d["sep_probe"]["live"],
            "gkx_side": d["negative_evidence"]["gkx_side"],
            "live_side": d["negative_evidence"]["live_side"],
            "coverage_side": d["negative_evidence"]["coverage_side"],
            "note": d["sep_probe"]["note"],
        },
        "result": {
            "chain_rows": chains,
            "year_rows": d["per_year"],
            "top_applicants": d["top_applicants"],
            "citation_subindex_only": True,
            "composite_formula": "0.5 * citation_subindex + 0.5 * SEP_subindex",
            "composite_status": "not_computable",
            "composite_reason": "SEP 维未测（无表/无标签），等权合成会把缺失维当 0 摊入，"
                                "因此不输出总分，只输出被引子项。",
        },
        "support_judgment": "部分支持",
        "verdict_kind": "partial_sample",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面/存量件：被引次数是截至库内快照的累计值，可回连样本集中在 "
                           "2021—2023 申请年；不设年度基期，不做跨年 CAGR，不把无被引年份按 0 摊入。",
        "sources": [
            "code/_snapshots21/ent_ds07_cited_20261023.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/base_20261021.json",
            "gkx.dwd_patent_cited (20,515 rows)",
            "gkx.dwd_patent (2,939,895 rows; pn 索引回连)",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print("wrote", OUT)
    print("chains with patent", len(ranked), "zero", len(zero_chains))
    print("linked chain patents", linked_chain_patents, "cited", linked_chain_cited)
    print("top", [(x["chain_name"], x["patent_n"], x["cited_sum"], x["mean_cited"]) for x in chains[:4]])


if __name__ == "__main__":
    main()
