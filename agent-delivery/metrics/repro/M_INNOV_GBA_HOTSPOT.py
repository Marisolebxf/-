#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_HOTSPOT · 湾区创新热点区域（20261021 版，gkx 单库）

王惠 V1.5（`M_INNOV_GBA_HOTSPOT.md`）三件套：
  区域主键 region_key = city + area（area 空则只用 city）
  创新密度 = (专利件数 + 论文件数 + 项目件数) / 该区县存续机构数
  主要创新类型 = 三类件数取最大（并列专利优先）
  热点标签 = 有效区县（机构数 ≥ 3）内，密度 ≥ P70 记 1；有效区县 < 5 不出标签

本库实测：论文维（作者单位与底册对齐率 1.01%）与项目维（funded_institution 整列为空）
均不可得，密度退化为**专利单口径**；主要创新类型因此恒为 patent，只作披露不作结论。
"""
from __future__ import annotations

import _gba21_common as G

METRIC = "M_INNOV_GBA_HOTSPOT"


def main():
    pat = G.patents()
    base = G.base_rows()
    ipc = G.ipc_by_city()
    pr1 = G.load("gba_probe_20261021.json")["probes"]
    pr2 = G.load("gba_probe2_20261021.json")

    # 区县（存续）机构数
    org_area = {}
    for r in base:
        c = r.get("city")
        if c not in G.CITY4:
            continue
        a = (r.get("area") or "").strip() or c
        org_area[(c, a)] = org_area.get((c, a), 0) + 1

    regions = []
    for (c, a), n_org in org_area.items():
        k = c + "|" + a
        pn = pat["area_total"].get(k, 0)
        regions.append({"city": c, "area": a, "region_key": k,
                        "orgs": n_org, "patents": pn, "papers": None, "projects": None,
                        "density": round(pn / n_org, 4) if n_org else None})

    valid = [r for r in regions if r["orgs"] >= 3]
    p70 = G.percentile([r["density"] for r in valid], 0.70)
    for r in regions:
        r["main_type"] = ("patent" if (r["patents"] or 0) > 0 else None)
        r["is_hotspot"] = int(bool(p70 is not None and r["orgs"] >= 3
                                   and r["density"] is not None and r["density"] >= p70))
        r["ipc_top3_city_level"] = [[x[0], x[1]] for x in
                                    (ipc["by_city_short"].get(G.SHORT[r["city"]], {})
                                     .get("top") or [])[:3]]
    regions.sort(key=lambda r: -(r["density"] or 0))

    n_hot = sum(r["is_hotspot"] for r in regions)
    city_roll = {}
    for c in G.CITY4:
        rs = [r for r in regions if r["city"] == c]
        city_roll[c] = {"n_regions": len(rs),
                        "orgs": sum(r["orgs"] for r in rs),
                        "patents": sum(r["patents"] for r in rs),
                        "n_hotspot": sum(r["is_hotspot"] for r in rs),
                        "density": round(sum(r["patents"] for r in rs) /
                                         sum(r["orgs"] for r in rs), 4)}

    result = {
        "metric_id": METRIC,
        "name": "湾区创新热点区域",
        "formula_owner": "王惠（V1.5-20260830，口径原样沿用）",
        "asof": "2026-10-22",
        "formula": "density = 成果件数 / 存续机构数；is_hotspot = density ≥ P70 且 orgs ≥ 3",
        "window": ["2021", "2024"],
        "rows": regions,
        "city_rollup": city_roll,
        "thresholds": {"p70_density": p70, "min_orgs": 3,
                       "valid_regions": len(valid), "all_regions": len(regions),
                       "n_hotspot": n_hot,
                       "hotspot_share": round(n_hot / len(regions), 4)},
        "degraded_dims": {
            "papers": {"status": "缺测（未补 0）",
                       "evidence": (f"dwd_zh_author {pr1['zh_author']['rows']:,} 行只覆盖 "
                                    f"{pr1['zh_author']['distinct_paper']:,} 篇（100,900 篇的 19.87%）；"
                                    f"作者单位与底册精确对齐率 "
                                    f"{pr2['zh_author_inst']['exact_hit_rate']:.2%}"),
                       "consequence": "论文件数在区县层不可得，密度分子只含专利"},
            "projects": {"status": "缺测（未补 0）",
                         "evidence": (f"dwd_zh_project funded_institution "
                                      f"{pr1['project']['no_funded_institution']:,}/"
                                      f"{pr1['project']['rows']:,} 行整列为空（100%）"),
                         "consequence": "项目件数在区县层不可得，密度分子只含专利"},
            "main_type": {"status": "退化为常数",
                          "evidence": "论文/项目两源为 0，任一有专利的区县 main_type 恒为 patent",
                          "consequence": "『主要创新类型』子项当前无区分度，不可作为结论呈现；"
                                         "IPC 前 3 位只到城市级，是代理细节而非区县实证"},
            "dongguan_area": {"status": "结构性缺区县",
                              "evidence": "东莞市 33,590 家机构 area 全为空，区域键退化为「东莞市」",
                              "consequence": "东莞只能作为 1 个整体区域参与排序，无法与深圳 9 区同层比较"},
        },
        "sensitivity": {
            "spearman_density_vs_orgs": G.spearman(
                [r["density"] for r in regions if r["density"] is not None],
                [r["orgs"] for r in regions if r["density"] is not None]),
            "p70_variants": {"valid_orgs_ge_3": p70,
                             "all_regions": G.percentile(
                                 [r["density"] for r in regions if r["density"] is not None], 0.70)},
            "note": "P70 只在机构数 ≥3 的有效区县内取分位；全区域口径作对照，两者阈值不同",
        },
        "probes": {
            "base_rows": len(base),
            "patent_panel_rows": pat["panel_rows"],
            "patent_unmapped_window": pat["unmapped_rows"],
            "patent_city_check_vs_city_cluster": G.city_patent_check(),
            "ipc_window": ipc["window"],
            "ipc_note": ipc["note"],
            "regions_with_zero_patents": sum(1 for r in regions if not r["patents"]),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "区域主键（city+area）与专利件数可算，26 个区县出密度与热点标签；"
            "但论文维（作者单位对齐 1.01%）、项目维（funded_institution 100% 空）整维缺测，"
            "密度实为专利单口径，主要创新类型退化为常数；11 城仅 4 城有区县数据，"
            "东莞无区县 → 部分支持"
        ),
    }
    G.write_out(METRIC, result)
    print("regions", len(regions), "valid", len(valid), "p70", p70, "hot", n_hot)
    for r in regions[:12]:
        print(r["city"], r["area"], r["orgs"], r["patents"], r["density"], r["is_hotspot"])
    print("city_rollup", city_roll)


if __name__ == "__main__":
    main()
