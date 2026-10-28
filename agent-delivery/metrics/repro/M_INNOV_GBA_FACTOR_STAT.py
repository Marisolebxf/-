#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_FACTOR_STAT · 湾区创新能力因素统计（20261021 版，gkx 单库）

需求落点：bid §1.1.1.1.4.1.5.3.2「对大湾区的创新资源、创新机构、创新机制、创新环境等
创新能力促成因素进行统计分析，用户可以查看各因素的详细数据和分布情况」。

四因素 × 可算性（本库实测）：
  资源  专利（面板 2021–2024）+ 上市公司研发费用（2019–2024，仅 12 月）     可算
  机构  存续机构数 + 高企去重数 + 科研院所数                                  可算
  机制  联合专利 / 合作项目 / 成果转化                                        三子项全不可算
  环境  有效市级政策数 + 高企密度                                             可算（政策城市归属 6.06%）

本脚本只读本地快照，零 SQL、零 demo 字面量。
"""
from __future__ import annotations

import _gba21_common as G

METRIC = "M_INNOV_GBA_FACTOR_STAT"


def _wrong_caliber():
    """错误口径（把 03/06/09/12 四期相加）的合计，用于披露虚增倍数。"""
    stock = G.load("cityfam_stock_2019_2026_20261021.json") or []
    org2city = {r["org_id"]: r.get("city") for r in G.base_rows()}
    tot = 0.0
    for oid, period, amt in stock:
        if amt is None:
            continue
        y = str(period)[:4]
        if org2city.get(oid) in G.CITY4 and "2019" <= y <= "2024":
            tot += float(amt)
    return round(tot / 1e8, 2)


def main():
    pat = G.patents()
    rd = G.rd()
    hi = G.hitech_by_city()
    pol = G.policy_by_city()
    ri = G.research_inst()
    base = G.base_rows()
    base_orgs = {c: sum(1 for r in base if r.get("city") == c) for c in G.CITY4}
    pr1 = G.load("gba_probe_20261021.json")["probes"]
    pr2 = G.load("gba_probe2_20261021.json")

    rows = []
    for c in G.CITY4:
        org_total = base_orgs[c] + ri["by_city"].get(c, 0)
        rows.append({
            "city": c,
            # 资源
            "patents_2021_24": pat["city_total"].get(c, 0),
            "rd_2019_24_yi": rd["by_city_sum_yi"].get(c, 0.0),
            "rd_orgs": rd["orgs_by_city"].get(c, 0),
            # 机构
            "orgs_base": base_orgs[c],
            "research_inst": ri["by_city"].get(c, 0),
            "orgs_total": org_total,
            "hightech_cnt": hi["by_city"].get(c, 0),
            # 机制（全部缺测）
            "joint_patent_cnt": None,
            "coop_project_cnt": None,
            "patent_transfer_cnt": None,
            # 环境
            "policy_valid_cnt": pol["by_city"].get(c, 0),
            "hightech_density": round(hi["by_city"].get(c, 0) / org_total, 5) if org_total else None,
        })

    metrics = ["patents_2021_24", "rd_2019_24_yi", "rd_orgs", "orgs_total",
               "hightech_cnt", "research_inst", "policy_valid_cnt"]
    for m in metrics:
        tot = sum(r[m] or 0 for r in rows)
        for r in rows:
            r["share_" + m] = round((r[m] or 0) / tot, 4) if tot else None

    factor_detail = {
        "资源": {
            "status": "可算（2/2 子项）",
            "items": {
                "专利资源": {"raw": {r["city"]: r["patents_2021_24"] for r in rows},
                             "source": "A-12 面板 app_year × 底册 name→city（零 DB）"},
                "研发投入": {"raw": {r["city"]: r["rd_2019_24_yi"] for r in rows},
                             "source": "gkx.dwd_org_stock_finance_info，仅上市公司、仅 12 月"},
            },
        },
        "机构": {
            "status": "可算（3/3 子项）",
            "items": {
                "载体数量": {"raw": {r["city"]: r["orgs_total"] for r in rows},
                             "source": "底册 org_id 去重 + 科研院所（两者 org_id 无交集）"},
                "科技型机构": {"raw": {r["city"]: r["hightech_cnt"] for r in rows},
                               "source": "gkx.dwd_org_tech_tag（高新技术企业 + 国家级高新技术企业）"},
                "科研院所": {"raw": {r["city"]: r["research_inst"] for r in rows},
                             "source": "gkx.dwd_research_institute_base_info 2,074 行"},
            },
        },
        "机制": {
            "status": "不可算（0/3 子项）",
            "items": {
                "联合专利": {"raw": None,
                             "why": (f"dwd_patent 无 applicants 列；dwd_patent_applicants 仅 "
                                     f"{pr1['applicants']['rows']:,} 行 / {pr1['applicants']['distinct_pn']:,} 个 pn，"
                                     f"占主表 {pr1['applicants']['distinct_pn']/G.PAT_TOTAL:.2%}；"
                                     f"共申请人名与底册精确对齐率仅 {pr2['applicants_name']['exact_hit_rate']:.2%}")},
                "合作项目": {"raw": None,
                             "why": (f"dwd_zh_project 的 funded_institution {pr1['project']['no_funded_institution']:,}/"
                                     f"{pr1['project']['rows']:,} 行整列为空；participating_institution 为单机构名，"
                                     f"含分隔符（可拆多机构）的仅 29 行 = 0.05%，『≥2 机构』结构上不成立")},
                "成果转化": {"raw": None,
                             "why": (f"dwd_patent_transfer {pr1['transfer']['rows']:,} 行 / "
                                     f"{pr1['transfer']['distinct_pn']:,} 个 pn（0.68% 封闭抽样）；"
                                     f"转移前后权利人名称与底册精确对齐率 {pr2['transfer_name']['exact_hit_rate']:.2%}")},
            },
        },
        "环境": {
            "status": "可算（2/2 子项，政策城市归属仅 6.06%）",
            "items": {
                "政策供给": {"raw": {r["city"]: r["policy_valid_cnt"] for r in rows},
                             "source": "gkx.dwd_policy_base 20,000 行，全表 status 均为「有效」"},
                "高企密度": {"raw": {r["city"]: r["hightech_density"] for r in rows},
                             "source": "高企去重数 / 机构总数"},
            },
        },
    }

    result = {
        "metric_id": METRIC,
        "name": "湾区创新能力因素统计",
        "formula_owner": "仿王惠 ai-1020（四因素框架沿用，统计呈现为本批定义）",
        "asof": "2026-10-22",
        "windows": {"patent": ["2021", "2024"], "rd": ["2019", "2024"]},
        "rows": rows,
        "factor_detail": factor_detail,
        "factor_coverage": {"computable_factors": 3, "total_factors": 4, "pct": 0.75,
                            "computable_subitems": 7, "total_subitems": 10},
        "city_coverage": {"computable": G.CITY4, "missing": G.MISSING7,
                          "n_computable": 4, "n_gba11": 11, "pct": round(4 / 11, 4)},
        "totals": {
            "patents_2021_24_4city": sum(r["patents_2021_24"] for r in rows),
            "rd_2019_24_yi_4city": round(sum(r["rd_2019_24_yi"] for r in rows), 2),
            "orgs_total_4city": sum(r["orgs_total"] for r in rows),
            "hightech_4city": sum(r["hightech_cnt"] for r in rows),
            "policy_4city": sum(r["policy_valid_cnt"] for r in rows),
        },
        "probes": {
            "patent_panel_rows": pat["panel_rows"],
            "patent_unmapped_window": pat["unmapped_rows"],
            "patent_unmapped_pct": round(pat["unmapped_rows"] /
                                         sum(v for y, v in pat["year_all"].items()
                                             if "2021" <= y <= "2024"), 4),
            "patent_city_check_vs_city_cluster": G.city_patent_check(),
            "policy_rows": pol["rows"],
            "policy_placeholder_rows": pol["placeholder_rows"],
            "policy_city_attribution_pct": round(sum(pol["by_city"].values()) / pol["rows"], 4),
            "rd_total_yi": round(sum(rd["by_city_sum_yi"].values()), 2),
            "rd_wrong_caliber_yi": _wrong_caliber(),
            "rd_orgs_total": rd["orgs_total"],
            "rd_anomaly_2024": rd["anomaly"].get("2024"),
            "mechanism_probe": factor_detail["机制"]["items"],
        },
        "distribution": {
            "share_by_metric": {m: {r["city"]: r["share_" + m] for r in rows} for m in metrics},
            "note": "分布 = 该因素原始值在四城合计中的占比；四城合计为分母，不是湾区 11 城",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "四因素中资源/机构/环境可统计（7/10 子项），机制维三子项因缺列、整列为空、"
            "样本仅 0.68% 而全不可算；11 城仅 4 城有机构底册；研发投入仅上市公司年报口径"
            "（856 家，占四城底册 0.45%）；政策城市归属仅 6.06%（惠州为 0）→ 部分支持"
        ),
    }
    G.write_out(METRIC, result)
    for r in rows:
        print(r["city"], r["patents_2021_24"], r["rd_2019_24_yi"], r["orgs_total"],
              r["hightech_cnt"], r["policy_valid_cnt"], r["hightech_density"])
    print("totals", result["totals"])


if __name__ == "__main__":
    main()
