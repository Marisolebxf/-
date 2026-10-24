#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_ORG_INDEX · 湾区创新机构指数（20261021 版，gkx 单库）

王惠 V1.5 三子项：
  载体数量   = 该城存续机构（企业底册 + 科研院所，按 org_id 去重）
  载体产出   = 统计年专利件数 + 中英文论文件数
  科技型机构 = 高企（高新技术企业标签）去重数 + 科研院所数
  指数       = 三子项在「本批城市」内极值归一后等权 ×100
缺测维不补 0，剩余维权重归一（王惠原文）。

本库实测：论文维不可得（作者单位与底册精确对齐率 1.01%，见 MECH_INDEX/FACTOR_STAT 同源探针），
故载体产出退化为**专利单口径**，并在 out.json 的 degraded_dims 中显式登记。
"""
from __future__ import annotations

import _gba21_common as G

METRIC = "M_INNOV_GBA_ORG_INDEX"


def main():
    pat = G.patents()
    hi = G.hitech_by_city()
    ri = G.research_inst()
    base = G.base_rows()
    base_orgs = {c: sum(1 for r in base if r.get("city") == c) for c in G.CITY4}

    rows = []
    for c in G.CITY4:
        org_total = base_orgs[c] + ri["by_city"].get(c, 0)
        sci = hi["by_city"].get(c, 0) + ri["by_city"].get(c, 0)
        rows.append({
            "city": c,
            "orgs_base": base_orgs[c],
            "research_inst": ri["by_city"].get(c, 0),
            "orgs_total": org_total,
            "output_patents_2021_24": pat["city_total"].get(c, 0),
            "output_papers": None,
            "sci_orgs_hitech": hi["by_city"].get(c, 0),
            "sci_orgs_total": sci,
        })

    n_org = G.norm01([r["orgs_total"] for r in rows])
    n_out = G.norm01([r["output_patents_2021_24"] for r in rows])
    n_sci = G.norm01([r["sci_orgs_total"] for r in rows])
    for i, r in enumerate(rows):
        r["norm_orgs"] = round(n_org[i], 4)
        r["norm_output"] = round(n_out[i], 4)
        r["norm_sci"] = round(n_sci[i], 4)
        r["org_index"] = round((n_org[i] + n_out[i] + n_sci[i]) / 3 * 100, 2)
        # 敏感性：剔除论文缺测影响后的「两维指数」（载体数量 + 科技型机构）
        r["org_index_2dim"] = round((n_org[i] + n_sci[i]) / 2 * 100, 2)
        r["output_per_org"] = round(r["output_patents_2021_24"] / r["orgs_total"], 2)
        r["hitech_density"] = round(r["sci_orgs_hitech"] / r["orgs_total"], 5)
    rows.sort(key=lambda r: -r["org_index"])

    total_org = sum(r["orgs_total"] for r in rows)
    result = {
        "metric_id": METRIC,
        "name": "创新机构指数（湾区）",
        "formula_owner": "王惠（V1.5-20260830，口径原样沿用）",
        "asof": "2026-10-22",
        "formula": "org_index = (norm(载体数量) + norm(载体产出) + norm(科技型机构)) / 3 × 100",
        "normalization": "min-max，在本批 4 个可算城市内；王惠原文为 11 城",
        "rows": rows,
        "totals": {
            "orgs_total_4city": total_org,
            "base_orgs_4city": sum(base_orgs.values()),
            "research_inst_4city": sum(ri["by_city"].values()),
            "hitech_4city": sum(hi["by_city"].values()),
            "patents_2021_24_4city": sum(r["output_patents_2021_24"] for r in rows),
        },
        "degraded_dims": {
            "output_papers": {
                "status": "缺测，未补 0（王惠：缺测维不补 0，剩余维权重归一）",
                "evidence": ("dwd_zh_author 62,002 行覆盖 20,048 篇（100,900 篇的 19.87%）；"
                             "作者单位与底册 name_cn 精确对齐 618/60,970 行 = 1.01%，"
                             "归一化后 620 行 = 1.02%"),
                "consequence": "载体产出实际只含专利，论文产出不可作为证据",
            },
            "city_universe": {
                "defined": 11, "available": 4,
                "missing": G.MISSING7,
                "consequence": "min-max 只能在 4 城内做，末位城恒为 0，指数不可与 11 城口径互换",
            },
        },
        "sensitivity": {
            "index_3dim_vs_2dim": {r["city"]: [r["org_index"], r["org_index_2dim"]] for r in rows},
            "spearman_index_vs_orgs": G.spearman(
                [r["org_index"] for r in rows], [r["orgs_total"] for r in rows]),
            "spearman_output_vs_orgs": G.spearman(
                [r["output_patents_2021_24"] for r in rows], [r["orgs_total"] for r in rows]),
        },
        "probes": {
            "base_rows": len(base),
            "base_orgs_note": "底册 189,116 行，四城 188,774（99.82%），其余 342 家落在省外",
            "hitech_tag_rows": hi["tag_rows"],
            "hitech_rule": hi["tag_rule"],
            "research_inst_rows": ri["rows"],
            "research_inst_overlap_with_base": 0,
            "patent_panel_rows": pat["panel_rows"],
            "patent_unmapped_window": pat["unmapped_rows"],
            "patent_city_check_vs_city_cluster": G.city_patent_check(),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "三子项中载体数量与科技型机构完整可算（底册 189,116 行、高企标签 202,424 行、科研院所 2,074 行），"
            "载体产出只剩专利单口径（论文作者单位与底册对齐率 1.01%，整维缺测）；"
            "11 城仅 4 城有机构底册，港澳在 dwd_forg_base_info 中为 0 —— 故判部分支持"
        ),
    }
    G.write_out(METRIC, result)
    for r in rows:
        print(r["city"], r["orgs_total"], r["sci_orgs_total"], r["output_patents_2021_24"],
              r["org_index"], r["org_index_2dim"])
    print("spearman", result["sensitivity"])


if __name__ == "__main__":
    main()
