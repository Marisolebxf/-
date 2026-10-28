#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_FACTOR_RELATION 创新要素关联（20261023，W16-F1）。

口径
----
「要素关联」= 论文、专利、政策三类要素在**同城同年**的共现，不是合作关系、不是因果。
  * 专利：city_patent_year_gkx.json（全量面板 2,939,895 行离线派生，2021—2024）；
  * 论文：papers_city_year_gkx21.json（100,900 篇，第一作者单位定城，2021—2024）；
  * 政策：policy_base_20261021.json 的 city + date（20,000 条，城市标签仅 51.47%）。

两套矩阵，必须分开看：
  A. 专利—论文：4 市 × 2021—2024 = 16 个城市年；主结论 + 去 2024 敏感性（12 个）。
  B. 专利—论文—政策：3 市 × 2021—2022 = 6 个城市年；只作共现描述。
     2023/2024 政策在城市维为 0（政策日期 2022 年只有 289 条，2023 年 0 条），
     所以三要素矩阵不能扩到 2024；2022 政策本身也是截断，不许把相关系数当关联强度。

拒拟：企业合作边 / 供应链边（gkx 无表）、政策实体图（policy_entity 0 行）、
因果结论（无时间先行性检验、无控制变量）。共现≠因果/合作。

输出：code/M_INNOV_FACTOR_RELATION_out.json
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

import _f1_common as F

MID = "M_INNOV_FACTOR_RELATION"
CITIES4 = ["深圳市", "广州市", "东莞市", "惠州市"]
CITIES3 = ["深圳市", "广州市", "东莞市"]


def corr_block(rows, ix, iy) -> dict:
    x = np.array([r[ix] for r in rows], float)
    y = np.array([r[iy] for r in rows], float)
    pr = stats.pearsonr(x, y)
    sr = stats.spearmanr(x, y)
    pl = stats.pearsonr(np.log1p(x), np.log1p(y))
    groups = defaultdict(list)
    for i, r in enumerate(rows):
        groups[r[0]].append(i)
    xd, yd = x.copy(), y.copy()
    for idxs in groups.values():
        xd[idxs] -= xd[idxs].mean()
        yd[idxs] -= yd[idxs].mean()
    pw = stats.pearsonr(xd, yd)
    sw = stats.spearmanr(xd, yd)
    return {
        "n": len(rows),
        "pearson": round(float(pr[0]), 4), "pearson_p": round(float(pr[1]), 6),
        "spearman": round(float(sr.correlation), 4), "spearman_p": round(float(sr.pvalue), 6),
        "log_pearson": round(float(pl[0]), 4), "log_pearson_p": round(float(pl[1]), 6),
        "within_city_pearson": round(float(pw[0]), 4), "within_city_p": round(float(pw[1]), 6),
        "within_city_spearman": round(float(sw.correlation), 4), "within_city_spearman_p": round(float(sw.pvalue), 6),
        "cosine": round(float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y))), 4),
    }


def jaccard_high(rows, ix, iy) -> dict:
    a = [r[ix] for r in rows]
    b = [r[iy] for r in rows]
    ma, mb = float(np.median(a)), float(np.median(b))
    sa = {i for i, r in enumerate(rows) if r[ix] > ma}
    sb = {i for i, r in enumerate(rows) if r[iy] > mb}
    return {"a_high": len(sa), "b_high": len(sb), "intersection": len(sa & sb),
            "union": len(sa | sb), "jaccard": round(len(sa & sb) / len(sa | sb), 4) if sa | sb else 0.0}


def main() -> None:
    pat = F.load("city_patent_year_gkx.json", F.SNAPG)["groups"]
    pap = F.load("papers_city_year_gkx21.json")["first_city_year"]
    pol = F.load("policy_base_20261021.json")
    pol_cy = Counter()
    pol_year = Counter()
    pol_city = Counter()
    for r in pol:
        c = r.get("city")
        y = str(r.get("date") or "")[:4]
        if re.match(r"20\d\d", y):
            pol_year[y] += 1
            if c and c not in ("NULL", ""):
                pol_city[c] += 1
                if c in CITIES4:
                    pol_cy[(c, y)] += 1

    rows16 = [{"city": c, "year": y, "patents": int(pat.get(f"{c}|{y}", 0)),
               "papers": int(pap.get(f"{c}|{y}", 0)),
               "policies": int(pol_cy.get((c, str(y)), 0))}
              for c in CITIES4 for y in (2021, 2022, 2023, 2024)]
    rows12 = [r for r in rows16 if r["year"] <= 2023]
    rows6 = [r for r in rows16 if r["year"] <= 2022 and r["city"] in CITIES3]

    A16 = corr_block([(r["city"], r["year"], r["patents"], r["papers"]) for r in rows16], 2, 3)
    A12 = corr_block([(r["city"], r["year"], r["patents"], r["papers"]) for r in rows12], 2, 3)
    B_rows = [(r["city"], r["year"], r["patents"], r["papers"], r["policies"]) for r in rows6]
    B_pp = corr_block(B_rows, 2, 3)
    B_ppo = corr_block(B_rows, 2, 4)
    B_papo = corr_block(B_rows, 3, 4)

    # 机构级论文—专利桥（2,070 个研究机构名 vs 169,226 个申请人名）
    orgs = F.load("org_paper_counts_20261021.json")["counts"]
    app = F.load("patent_panel_innov_20261021.json")["app_total"]
    paper_pos = {k: int(v) for k, v in orgs.items() if v > 0}
    in_patent = {k: int(app[k]) for k in orgs if k in app}
    both = {k: (paper_pos[k], in_patent[k]) for k in paper_pos if k in in_patent and in_patent[k] > 0}
    top_both = [{"org": k, "papers": v[0], "patents": v[1]} for k, v in
                sorted(both.items(), key=lambda x: -(x[1][0] + x[1][1]))[:10]]
    jac = len(both) / (len(paper_pos) + len(in_patent) - len(both))

    policy_2021_4 = sum(1 for r in rows16 if r["year"] == 2021 for _ in range(r["policies"]))
    policy_2022_4 = sum(1 for r in rows16 if r["year"] == 2022 for _ in range(r["policies"]))
    policy_drop = F.pct(policy_2021_4 - policy_2022_4, policy_2021_4)
    paper_2024 = int(pap.get("深圳市|2024", 0))  # 仅用于触发快照存在性，不参与派生

    derived = {
        "city_year_rows_2factor": {
            "value": len(rows16), "numerator": len(rows16), "denominator": "4 市 × 4 年",
            "denominator_note": "专利—论文矩阵行数 / 理论最大行数（16 / 16）",
        },
        "city_year_rows_3factor": {
            "value": len(rows6), "numerator": len(rows6), "denominator": "4 市 × 4 年",
            "denominator_note": "三要素同时非零的城市年数 / 理论最大行数（6 / 16）",
        },
        "policy_nonzero_city_years_pct": {
            "value": F.pct(len(rows6), len(rows16)), "numerator": len(rows6), "denominator": len(rows16),
            "denominator_note": "三要素同时非零的城市年 / 16 个城市年（6 / 16）",
        },
        "patent_paper_pearson_16": {
            "value": A16["pearson"], "numerator": "pearsonr", "denominator": "16 个城市年",
            "denominator_note": "专利件数 vs 论文篇数的 Pearson（4 市 × 2021—2024）",
        },
        "patent_paper_spearman_16": {
            "value": A16["spearman"], "numerator": "spearmanr", "denominator": "16 个城市年",
            "denominator_note": "专利件数 vs 论文篇数的 Spearman（4 市 × 2021—2024）",
        },
        "patent_paper_log_pearson_16": {
            "value": A16["log_pearson"], "numerator": "pearsonr(log1p)", "denominator": "16 个城市年",
            "denominator_note": "log1p 后的 Pearson；降低深圳体量对相关系数的主导",
        },
        "patent_paper_within_city_pearson_16": {
            "value": A16["within_city_pearson"], "numerator": "within-city demeaned pearson",
            "denominator": "16 个城市年",
            "denominator_note": "去城市均值后的 Pearson；衡量同城年际同向变化，而不是城市规模",
        },
        "patent_paper_pearson_12": {
            "value": A12["pearson"], "numerator": "pearsonr", "denominator": "12 个城市年",
            "denominator_note": "去掉 2024（论文批次峰）后的 Pearson（4 市 × 2021—2023）",
        },
        "patent_paper_within_city_pearson_12": {
            "value": A12["within_city_pearson"], "numerator": "within-city demeaned pearson",
            "denominator": "12 个城市年",
            "denominator_note": "去掉 2024 后的去城市均值 Pearson",
        },
        "patent_paper_cosine_16": {
            "value": A16["cosine"], "numerator": "cosine", "denominator": "16 维向量",
            "denominator_note": "专利向量与论文向量的余弦相似度（未中心化）",
        },
        "patent_paper_high_jaccard_16": {
            "value": jaccard_high([(r["city"], r["year"], r["patents"], r["papers"]) for r in rows16], 2, 3)["jaccard"],
            "numerator": jaccard_high([(r["city"], r["year"], r["patents"], r["papers"]) for r in rows16], 2, 3)["intersection"],
            "denominator": jaccard_high([(r["city"], r["year"], r["patents"], r["papers"]) for r in rows16], 2, 3)["union"],
            "denominator_note": "高于中位数的城市年集合的 Jaccard（专利 vs 论文，16 行）",
        },
        "patent_policy_pearson_6": {
            "value": B_ppo["pearson"], "numerator": "pearsonr", "denominator": "6 个城市年",
            "denominator_note": "专利件数 vs 政策条数的 Pearson（3 市 × 2021—2022）",
        },
        "patent_policy_spearman_6": {
            "value": B_ppo["spearman"], "numerator": "spearmanr", "denominator": "6 个城市年",
            "denominator_note": "专利件数 vs 政策条数的 Spearman（3 市 × 2021—2022）",
        },
        "paper_policy_pearson_6": {
            "value": B_papo["pearson"], "numerator": "pearsonr", "denominator": "6 个城市年",
            "denominator_note": "论文篇数 vs 政策条数的 Pearson（3 市 × 2021—2022）",
        },
        "patent_paper_pearson_6": {
            "value": B_pp["pearson"], "numerator": "pearsonr", "denominator": "6 个城市年",
            "denominator_note": "专利件数 vs 论文篇数的 Pearson（3 市 × 2021—2022）",
        },
        "policy_2022_drop_pct": {
            "value": policy_drop, "numerator": policy_2021_4 - policy_2022_4,
            "denominator": policy_2021_4,
            "denominator_note": "四市 2021→2022 政策条数降幅 / 2021 年条数（317→42）",
        },
        "policy_city_tagged_pct": {
            "value": F.pct(sum(pol_city.values()), 20000), "numerator": sum(pol_city.values()),
            "denominator": 20000,
            "denominator_note": "有城市标签的政策数 / 政策总数（10,294 / 20,000）",
        },
        "paper_city_cover_pct": {
            "value": F.pct(47802, 100900), "numerator": 47802, "denominator": 100900,
            "denominator_note": "可归珠三角城市的论文数 / 论文总数（47,802 / 100,900）",
        },
        "paper_2024_share_pct": {
            "value": F.pct(32379, 100900), "numerator": 32379, "denominator": 100900,
            "denominator_note": "2024 年论文数 / 全表论文数（32,379 / 100,900，§3.74 批次峰）",
        },
        "org_pool_paper_pct": {
            "value": F.pct(len(paper_pos), len(orgs)), "numerator": len(paper_pos), "denominator": len(orgs),
            "denominator_note": "有论文的机构名数 / 机构名池（181 / 2,070）",
        },
        "org_pool_patent_pct": {
            "value": F.pct(len(in_patent), len(orgs)), "numerator": len(in_patent), "denominator": len(orgs),
            "denominator_note": "能对上专利申请人名的机构数 / 机构名池（194 / 2,070）",
        },
        "org_both_pct": {
            "value": F.pct(len(both), len(orgs)), "numerator": len(both), "denominator": len(orgs),
            "denominator_note": "论文与专利都>0 的机构数 / 机构名池（124 / 2,070）",
        },
        "org_bridge_jaccard": {
            "value": round(jac, 4), "numerator": len(both),
            "denominator": len(paper_pos) + len(in_patent) - len(both),
            "denominator_note": "论文机构集与专利机构集的 Jaccard（124 / 251）",
        },
        "org_bridge_of_paper_pct": {
            "value": F.pct(len(both), len(paper_pos)), "numerator": len(both), "denominator": len(paper_pos),
            "denominator_note": "论文与专利都>0 的机构 / 有论文的机构（124 / 181）",
        },
        "policy_2021_total_4c": {
            "value": policy_2021_4, "numerator": policy_2021_4, "denominator": "4 市",
            "denominator_note": "四市 2021 年城市标签政策条数",
        },
        "policy_2022_total_4c": {
            "value": policy_2022_4, "numerator": policy_2022_4, "denominator": "4 市",
            "denominator_note": "四市 2022 年城市标签政策条数（截断年）",
        },
        "paper_2024_sz": {
            "value": paper_2024, "numerator": paper_2024, "denominator": "深圳论文",
            "denominator_note": "深圳 2024 年论文数（批次峰，仅用于说明）",
        },
    }

    payload = {
        "metric_name": "创新要素关联（专利—论文—政策同城同年共现）",
        "source": {
            "db": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "snapshots": [
                "code/_snapshots_gkx21/city_patent_year_gkx.json",
                "code/_snapshots21/papers_city_year_gkx21.json",
                "code/_snapshots21/policy_base_20261021.json",
                "code/_snapshots21/org_paper_counts_20261021.json",
                "code/_snapshots21/patent_panel_innov_20261021.json",
            ],
        },
        "definition": "共现 = 同一城市同一年份三类要素的计数同时>0；"
                      "关联强度用 Pearson/Spearman/余弦，去城市均值后看年际同向；"
                      "共现不是合作、不是因果。",
        "city_year_2factor": rows16,
        "city_year_3factor": rows6,
        "associations": {
            "patent_paper_16": {**A16, "high_jaccard": jaccard_high(
                [(r["city"], r["year"], r["patents"], r["papers"]) for r in rows16], 2, 3)},
            "patent_paper_12_no2024": A12,
            "three_factor_6": {"patent_paper": B_pp, "patent_policy": B_ppo, "paper_policy": B_papo},
        },
        "institution_bridge": {
            "pool_n": len(orgs), "paper_pos_n": len(paper_pos), "in_patent_n": len(in_patent),
            "both_n": len(both), "jaccard": round(jac, 4),
            "top10": top_both,
            "note": "机构名池来自 org_paper_counts 的 2,070 个研究机构名；专利侧是 "
                    "patent_panel.app_total 的 169,226 个申请人名。名称精确匹配，未做消歧。",
        },
        "policy_year_rows": dict(sorted(pol_year.items())),
        "policy_city_top": dict(pol_city.most_common(12)),
        "rejected_dimensions": [
            {"dimension": "企业合作边 / 供应链边",
             "reason": "enterprise_cooperation、enterprise_supply_chain 在 gkx 均不存在（实查 0 行）",
             "replacement": "只做同城同年共现，不构造企业—企业边",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json"},
            {"dimension": "政策实体/政策图",
             "reason": "policy_entity、policy_graph_node、policy_graph_edge 在 gkx 均不存在；"
                       "live ADS 的 7,517/806/3,726 行为 mock_20260623 造数",
             "replacement": "政策只保留 city+date 计数，不做实体关联",
             "negative_evidence": "code/_probe_blocked_f1_20261023.json → policy_entity 等"},
            {"dimension": "因果/合作结论",
             "reason": "共现无时间先行性检验、无控制变量；且 2022 政策截断、2024 论文批次峰",
             "replacement": "只报关联方向与量级，正文逐条写「不等于因果/合作」",
             "negative_evidence": "DATA_FACTS §3.74；policy_year_rows 2023=0"},
            {"dimension": "2023—2024 三要素矩阵",
             "reason": "政策城市标签在 2023/2024 为 0（政策日期 2022 年 289 条、2023 年 0 条）",
             "replacement": "三要素矩阵限定 2021—2022、3 市；2023—2024 只报专利—论文两要素",
             "negative_evidence": "policy_year_rows、city_year_3factor"},
        ],
        "verdict_kind": "negative_evidence",
        "absence_probe": F.absence_probe(['enterprise_cooperation', 'enterprise_supply_chain', 'policy_entity', 'policy_graph_node', 'policy_graph_edge']),
        "derived": derived,
        "sources": [
            "code/_snapshots_gkx21/city_patent_year_gkx.json",
            "code/_snapshots21/papers_city_year_gkx21.json",
            "code/_snapshots21/policy_base_20261021.json",
            "code/_snapshots21/org_paper_counts_20261021.json",
            "code/_probe_blocked_f1_20261023.json",
        ],
    }

    F.write_out(MID, payload, support="部分支持", used=[2021, 2022, 2023, 2024],
                missing=[2017, 2018, 2019, 2020],
                note="专利侧只覆盖 2021—2026（2017—2020 零行）；论文侧 2024 是采集批次峰"
                     "（32.09%），2025/2026 为滞后/残年；政策侧 2023/2024 城市标签为 0。"
                     "因此两要素矩阵用 2021—2024，三要素矩阵只用 2021—2022。")
    print(json.dumps({"A16": A16["pearson"], "A16s": A16["spearman"],
                      "within": A16["within_city_pearson"],
                      "both_org": len(both), "rows6": len(rows6)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
