#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_POT_SCI_INFL · 产业科学影响力（0—100）

口径（calc-logic 真源）
----------------------
二维加权平均：论文被引次数（SUM citation_num）/ 国际合作论文比例（作者地址国别≥2）。
对象＝**产业**（不是区域、不是机构），得分 0—100。

可算边界（本批实测，详见 MD §三）
--------------------------------
* `dwd_zh_paper_citation` 20,031 行，`citation_num` 100% 非空，合计 144,020；
* `dwd_zh_author` 62,002 行覆盖 20,048 篇，与上表按 paper_id 交集 20,031 篇（两表同域）；
* 但**两表的 paper_id 只有 782/100,900（0.78%）能对上 `dwd_zh_paper.id`**，因此拿不到发表年、
  期刊、语种，也无法与机构主数据按论文主键关联；
* 机构串 → 底册机构名 → industry_l1：作者行命中率 **0.36%（218/60,970）**，可归属论文 **127/20,031（0.63%）**；
  底册里高校/医院等 2,264 个名称没有 industry_l1，而论文作者恰恰集中在这类机构；
* `dwd_en_paper_cited_by_info` 77,144 行，但 `dwd_en_paper` 仅 1,387 行，可对上 5 行 → 英文侧被引不可用；
* 国际合作按 affiliation 国别词推断，仅 58/20,031 篇命中（0.29%），方差近 0。

结论：论文级被引（D1）**可算且质量好**；国际合作（D2）与国际/产业归属**不可用**，故判部分支持。
本脚本交付「机构级 D1 排行」，同时输出产业级覆盖诊断与 D2 全量统计，不把 0.63% 覆盖包装成产业排名。

运行：python3 code/M_INNOV_POT_SCI_INFL.py（零新增 SQL，全部读 _probe_a26 快照）
"""
from __future__ import annotations

import json
import os
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _a26_common as C

MID = "M_INNOV_POT_SCI_INFL"
MIN_PAPERS_INDUSTRY = 100  # 产业入榜的最小论文量（当前最高仅 33 篇 → 无产业达标，不排名）
MIN_PAPERS_ORG = 20        # 机构级入榜门槛


def main() -> None:
    cites = C.zh_citations()
    auths = C.zh_authors()
    pairs = sorted(set(cites) & set(auths))
    oind, _ = C.org_industry()

    paper_rows = []
    for pid in pairs:
        insts = auths[pid]
        orgs = []
        for inst, _aff in insts:
            for tok in C.inst_tokens(inst):
                m = C.match_org_any(tok)
                if m:
                    orgs.append(m)
                    break
        orgs = sorted(set(orgs))
        inds = sorted({oind[o][0] for o in orgs if o in oind})
        intl = any(C.is_foreign(aff) for _i, aff in insts)
        paper_rows.append({"paper_id": pid, "cited": cites[pid], "n_auth": len(insts),
                           "orgs": orgs, "inds": inds, "intl": intl})

    attributed = [p for p in paper_rows if p["inds"]]
    n_pairs = len(pairs)
    n_auth_rows = sum(len(v) for v in auths.values())
    n_inst_rows = sum(1 for v in auths.values() for i, _a in v if i)
    matched_rows = 0
    industry_rows = 0
    for v in auths.values():
        for inst, _a in v:
            m = None
            for tok in C.inst_tokens(inst):
                m = C.match_org_any(tok)
                if m:
                    break
            if m:
                matched_rows += 1
                if m in oind:
                    industry_rows += 1

    # ---------------- 论文级（全部 20,031 篇）----------------
    cited_all = [p["cited"] for p in paper_rows]
    intl_n = sum(1 for p in paper_rows if p["intl"])
    intl_cited = sum(p["cited"] for p in paper_rows if p["intl"])
    dom_cited = sum(p["cited"] for p in paper_rows if not p["intl"])

    # ---------------- 机构级 ----------------
    org_agg = defaultdict(lambda: {"papers": 0, "cited": 0, "intl": 0, "inds": Counter()})
    for p in paper_rows:
        for o in p["orgs"]:
            a = org_agg[o]
            a["papers"] += 1
            a["cited"] += p["cited"]
            a["intl"] += 1 if p["intl"] else 0
            if o in oind:
                a["inds"][oind[o][0]] += 1
    org_rows = [{"org": k, "papers": v["papers"], "cited": v["cited"],
                 "intl_papers": v["intl"],
                 "intl_share": round(v["intl"] / v["papers"], 4) if v["papers"] else None,
                 "cited_per_paper": round(v["cited"] / v["papers"], 2) if v["papers"] else None,
                 "industry_l1": v["inds"].most_common(1)[0][0] if v["inds"] else None}
                for k, v in org_agg.items()]
    org_rows.sort(key=lambda r: (-r["cited"], -r["papers"]))
    org_eligible = [r for r in org_rows if r["papers"] >= MIN_PAPERS_ORG]
    if org_eligible:
        rk = C.rank_pct([r["cited"] for r in org_eligible])
        for k, r in enumerate(org_eligible):
            r["score_d1"] = rk[k]
        org_eligible.sort(key=lambda r: -r["score_d1"])

    # ---------------- 产业级（仅可归属子集）----------------
    ind_agg = defaultdict(lambda: {"papers": 0, "cited": 0.0, "intl": 0})
    for p in attributed:
        share = 1.0 / len(p["inds"])
        for ind in p["inds"]:
            a = ind_agg[ind]
            a["papers"] += 1
            a["cited"] += p["cited"] * share
            a["intl"] += 1 if p["intl"] else 0
    ind_rows = [{"industry_l1": k, "papers": v["papers"], "cited_alloc": round(v["cited"], 2),
                 "intl_papers": v["intl"],
                 "intl_share": round(v["intl"] / v["papers"], 4) if v["papers"] else None,
                 "cited_per_paper": round(v["cited"] / v["papers"], 2) if v["papers"] else None}
                for k, v in ind_agg.items()]
    eligible = [r for r in ind_rows if r["papers"] >= MIN_PAPERS_INDUSTRY]
    if eligible:
        c_rank = C.rank_pct([r["cited_alloc"] for r in eligible])
        i_rank = C.rank_pct([r["intl_share"] for r in eligible])
        for k, r in enumerate(eligible):
            r["score"] = round(0.5 * c_rank[k] + 0.5 * i_rank[k], 2)
        eligible.sort(key=lambda r: -r["score"])
    ind_rows.sort(key=lambda r: -r["papers"])

    # 论文级被引分布（做基准，回答「20,031 篇是否够」）
    top_papers = sorted(paper_rows, key=lambda p: -p["cited"])[:20]

    # 英文侧孤儿率
    pr = C.probe()
    en_ids = {r[0] for r in json.loads(
        (C.SNAP / "probe_infl_20261022" / "en_paper.json").read_text(encoding="utf-8"))["rows"]}
    en_cited = pr["en_cited"]["rows"]
    en_hit = len({r[0] for r in en_cited} & en_ids)

    res = {
        "metric_id": MID,
        "metric_name": "产业科学影响力",
        "also_known_as": "潜力点科研影响力（派单标签）",
        "support_judgment": "部分支持",
        "object": "产业（industry_l1，国民经济行业门类）",
        "generated_from": "gkx.dwd_zh_paper_citation(20,031) ⋈ gkx.dwd_zh_author(62,002) 按 paper_id 同域；"
                          "机构→产业用 _snapshots21/star_base_rows_gkx.json（189,116 行底册）",
        "sql_count": 0,
        "method": {
            "formula": "D1=Σ citation_num；D2=国际合作论文数/论文数（affiliation 命中外国国别词）。"
                       "D1 在机构级按百分位输出（≥20 篇）；D2 仅作统计，不参与合成；产业级因覆盖 <1% 不排名",
            "weights": "不合成二维权重：D2 仅 58 篇命中、方差近 0，合成会让权重落到噪声上",
            "coattribution": "一篇论文可命中多个产业时按 1/n 分摊被引，不重复计数",
            "international": "无国别字段，按 affiliation 文本命中 58 个外国国别词/55 个英文国别词判定；"
                             "港澳台不计入「国际合作」",
        },
        "coverage": {
            "papers_with_citation": len(cites),
            "papers_with_authors": len(auths),
            "papers_joined": n_pairs,
            "zh_paper_total": 100900,
            "citation_author_join_rate_vs_zh_paper": round(n_pairs / 100900, 6),
            "zh_paper_id_hit": 782,
            "author_rows": n_auth_rows,
            "author_rows_with_institution": n_inst_rows,
            "author_rows_matched_to_base_org": matched_rows,
            "author_row_match_rate": round(matched_rows / n_auth_rows, 6) if n_auth_rows else None,
            "author_rows_with_industry": industry_rows,
            "author_row_industry_rate": round(industry_rows / n_auth_rows, 6) if n_auth_rows else None,
            "papers_attributed_to_industry": len(attributed),
            "paper_attribution_rate": round(len(attributed) / n_pairs, 6) if n_pairs else None,
            "base_orgs_without_industry_l1": 2264,
            "industries_with_any_paper": len(ind_rows),
            "industries_ranked": len(eligible),
            "industry_min_papers": MIN_PAPERS_INDUSTRY,
            "orgs_ranked": len(org_eligible),
            "en_cited_rows": len(en_cited),
            "en_paper_rows": len(en_ids),
            "en_cited_hit": en_hit,
        },
        "paper_level": {
            "n": n_pairs,
            "citation_sum": sum(cited_all),
            "citation_stats": C.st([float(x) for x in cited_all]),
            "intl_papers": intl_n,
            "intl_share": round(intl_n / n_pairs, 4) if n_pairs else None,
            "intl_cited": intl_cited,
            "domestic_cited": dom_cited,
            "cited_per_paper": round(sum(cited_all) / n_pairs, 3) if n_pairs else None,
            "intl_cited_per_paper": round(intl_cited / intl_n, 3) if intl_n else None,
        },
        "institution_level": {"n": len(org_rows), "min_papers": MIN_PAPERS_ORG,
                              "n_ranked": len(org_eligible),
                              "ranked": org_eligible,
                              "top30": org_rows[:30],
                              "note": "机构级只出 D1（被引合计）百分位分；D2 国际合作仅 58/20,031 篇命中，"
                                      "方差近 0，不参与合成分"},
        "industry_level": {
            "all": ind_rows,
            "ranked": eligible,
            "note": "产业级仅 127 篇可归属论文、单一产业最高 33 篇，低于 100 篇门槛，故不产出产业排名；"
                    "此处只作覆盖诊断，不可对外发布",
        },
        "top_papers": top_papers,
        "base_year_block": C.base_year_block(
            [], [], "被引表与作者表均无发表年字段，且 paper_id 与 dwd_zh_paper.id 仅 0.78% 可连，"
                    "无法构造年度分母；本指标按截面计算"),
        "gaps": [
            "dwd_zh_paper_citation 的 20,031 行与 dwd_zh_paper 的 100,900 行只有 782 个 id 交集，"
            "年份/期刊/语种无法挂接",
            "dwd_zh_author 无国家字段，国际合作只能按 affiliation 文本国别词推断",
            "dwd_en_paper_cited_by_info 77,144 行对 dwd_en_paper 1,387 行仅命中 5 行，英文侧被引不可用",
            "机构串到行业底册的匹配率 4.76%，产业级归属是当前最大瓶颈",
            "dwd_scholar.citation_nums 为学者级被引，无法拆到单篇论文，不能替代论文被引",
        ],
    }
    C.write_out(MID, res)
    print(json.dumps({k: res[k] for k in ("support_judgment", "coverage", "paper_level")},
                     ensure_ascii=False, indent=1))
    print("ranked industries:", json.dumps(eligible[:5], ensure_ascii=False))


if __name__ == "__main__":
    main()
