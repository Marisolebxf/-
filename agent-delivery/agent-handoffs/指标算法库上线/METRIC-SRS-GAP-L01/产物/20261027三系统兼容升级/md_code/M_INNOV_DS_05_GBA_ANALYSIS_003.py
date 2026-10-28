#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_05_GBA_ANALYSIS_003（优势因素分析）复现脚本。

口径：王惠「同 M_INNOV_GBA_SWOT_STRENGTH」——从四子指数分项中识别该城相对领先项
（11 城排名 ≤3），输出优势清单、表现（原始值+排名）与影响程度（归一值）。

本脚本复用同日父指标实测产物（不重跑探针）：
  - M_INNOV_GBA_INDEX_BUNDLE_out.json  ：4 个可算城市的 7 个分项原始值
  - M_INNOV_GBA_SWOT_BUNDLE_out.json   ：父指标的分项清单/阈值映射
  - _probe_innov_h_gkx_out.json        ：gkx 结构行数（11 城覆盖判定）
并做一次 gkx 轻量连通性核验（失败不阻断，记录 status）。

输出：M_INNOV_DS_05_GBA_ANALYSIS_003_out.json
"""
from __future__ import annotations

import math

from _innov_h_common import (GBA11, gkx_light_check, load_json, norm_minmax, pct,
                             rank_desc, row_count, row_count_source, save_out)

METRIC = "M_INNOV_DS_05_GBA_ANALYSIS_003"

# 王惠口径的 12 分项 → 本库可算性（依据父指标实测与 gkx 结构探针）
SUBITEMS = [
    # (代号, 中文, 所属子指数, 可算?, 不可算原因 / 代理说明, 取值函数名)
    ("res_paper", "论文产出", "创新资源", False, "dwd_zh_author 无城市键，作者单位到城市未对齐", None),
    ("res_patent", "专利产出", "创新资源", True, "first_applicant_name 名称对齐", "patent_cnt"),
    ("res_rd", "研发经费投入", "创新资源", True, "dwd_org_stock_finance_info.research_development_amount 按 org_id 汇总", "rd_funding"),
    ("org_cnt", "创新机构数量", "创新机构", True, "机构底册按 city 计数", "org_cnt"),
    ("org_hightech", "高新技术企业数", "创新机构", True, "dwd_org_tech_tag 高新技术标签", "hightech_cnt"),
    ("org_output", "机构创新产出", "创新机构", True, "专利产出代理（与 res_patent 同源，须披露）", "patent_cnt"),
    ("mech_joint", "联合专利合作", "创新机制", False, "dwd_patent 无 applicants 列；dwd_patent_applicants 仅 25,753 行（覆盖 0.96%）", None),
    ("mech_transfer", "技术转移", "创新机制", False, "dwd_patent_transfer 无机构外键，transfer_before/after 名称对齐未闭合", None),
    ("mech_project", "合作项目", "创新机制", False, "dwd_zh_project.funded_institution 未与机构底册对齐（未测）", None),
    ("env_policy", "政策供给", "创新环境", True, "dwd_policy_base.city 计数", "policy_cnt"),
    ("env_valid", "政策有效性", "创新环境", False, "policy_base 全表 20,000 行 status 均为「有效」，无失效样本", None),
    ("env_density", "高企密度", "创新环境", True, "高新技术企业数 / 机构数", "hightech_density"),
]
ITEM_VALUE = {s[0]: s[5] for s in SUBITEMS if s[3]}


def main():
    idx = load_json("M_INNOV_GBA_INDEX_BUNDLE_out.json")
    swot = load_json("M_INNOV_GBA_SWOT_BUNDLE_out.json")
    probe = load_json("_probe_innov_h_gkx_out.json", {}) or {}
    rows = idx["rows"]

    available = [r["city"] for r in rows if r.get("org_cnt", 0) > 0]
    missing = [c for c in GBA11 if c not in available]
    n = len(rows)

    # ---- 分项排名与归一（本地重算，不依赖父脚本的 rank 字段） ----
    items = []
    for code, cn, sub, ok, note, field in SUBITEMS:
        if not ok:
            items.append({"item": code, "name_cn": cn, "sub_index": sub,
                          "computable": False, "reason": note})
            continue
        vals = [r[field] for r in rows]
        norms = norm_minmax(vals)
        items.append({
            "item": code, "name_cn": cn, "sub_index": sub, "computable": True,
            "values": {r["city"]: r[field] for r in rows},
            "norms": {r["city"]: round(v, 4) for r, v in zip(rows, norms)},
            "ranks": {r["city"]: rank_desc(vals, r[field]) for r in rows},
        })

    n_computable = sum(1 for i in items if i["computable"])

    # ---- 两种阈值：王惠原阈值（11 城 rank≤3）与按城数比例映射 ----
    thr_direct = 3                       # 王惠原文：11 城 rank ≤ 3
    thr_scaled = max(1, math.ceil(n * 3 / 11))   # 4 城时 = 2
    thr_strict = max(1, round(n * 3 / 11))       # 4 城时 = 1（top 27%）

    city_out = []
    for r in rows:
        city = r["city"]
        lst_direct, lst_scaled, lst_strict = [], [], []
        for it in items:
            if not it["computable"]:
                continue
            rk = it["ranks"][city]
            rec = {"item": it["item"], "name_cn": it["name_cn"], "sub_index": it["sub_index"],
                   "value": it["values"][city], "rank": rk, "of": n,
                   "influence": it["norms"][city]}
            if rk <= thr_direct:
                lst_direct.append(rec)
            if rk <= thr_scaled:
                lst_scaled.append(rec)
            if rk <= thr_strict:
                lst_strict.append(rec)
        # 王惠兜底：无命中则取 rank 最小的 1 项，标 weak_signal=1
        fallback = None
        if not lst_scaled:
            pool = [{"item": it["item"], "name_cn": it["name_cn"], "sub_index": it["sub_index"],
                     "value": it["values"][city], "rank": it["ranks"][city], "of": n,
                     "influence": it["norms"][city]} for it in items if it["computable"]]
            fallback = min(pool, key=lambda x: x["rank"])
        city_out.append({
            "city": city,
            "n_strength_direct": len(lst_direct),
            "n_strength_scaled": len(lst_scaled),
            "n_strength_strict": len(lst_strict),
            "strength_direct": lst_direct,
            "strength_scaled": lst_scaled,
            "strength_strict": lst_strict,
            "weak_signal_fallback": fallback,
            "mean_influence_of_strengths": round(
                sum(x["influence"] for x in lst_scaled) / len(lst_scaled), 4) if lst_scaled else None,
        })

    # 湾区整体聚合：某分项在 ≥4 城进入优势 → 记为湾区优势（王惠原文）
    def bay_area(key):
        cnt = {}
        for c in city_out:
            for x in c[key]:
                cnt[x["item"]] = cnt.get(x["item"], 0) + 1
        return {k: v for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])}

    bay_direct = bay_area("strength_direct")
    bay_scaled = bay_area("strength_scaled")
    bay_adv_direct = [k for k, v in bay_direct.items() if v >= 4]
    bay_adv_scaled = [k for k, v in bay_scaled.items() if v >= 4]

    live = gkx_light_check("SELECT COUNT(*) AS c FROM dwd_patent")

    out = {
        "metric_id": METRIC,
        "metric_name": "优势因素分析",
        "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_STRENGTH.md（王惠口径）",
        "source_artifacts": [
            "code/M_INNOV_GBA_INDEX_BUNDLE_out.json（父指标同日实测，4 城分项原始值）",
            "code/M_INNOV_GBA_SWOT_BUNDLE_out.json（父指标阈值映射对照）",
            "code/_probe_innov_h_gkx_out.json（gkx 结构行数）",
        ],
        "probes": {
            "gkx_live_count_patent": live,
            "n_cities_available": n,
            "cities_available": available,
            "cities_missing": missing,
            "gba_coverage_pct": pct(n, 11),
            "subitems_total": len(SUBITEMS),
            "subitems_computable": n_computable,
            "subitems_coverage_pct": pct(n_computable, len(SUBITEMS)),
            "gkx_rows": {
                "dwd_org_base_info": row_count(probe, "dwd_org_base_info"),
                "dwd_patent": row_count(probe, "dwd_patent"),
                "dwd_policy_base": row_count(probe, "dwd_policy_base"),
                "source": {
                    "dwd_org_base_info": row_count_source(probe, "dwd_org_base_info"),
                    "dwd_patent": row_count_source(probe, "dwd_patent"),
                    "dwd_policy_base": row_count_source(probe, "dwd_policy_base"),
                },
            },
            "gkx_live_count_patent_c": ((live.get("rows") or [{}])[0].get("c")
                                       if live.get("status") == "ok" else None),
        },
        "thresholds": {
            "wanghui_original": "11 城 rank ≤ 3",
            "direct_on_4_cities": thr_direct,
            "scaled_top_share_27pct": thr_scaled,
            "strict_round_27pct": thr_strict,
            "note": "4 城宇宙下 rank≤3 等于「非末位」（75% 城入选），阈值不可移植；strict 变体仅深圳入选",
        },
        "subitems": items,
        "city_results": city_out,
        "summary": {
            "cities_with_any_strength_scaled": [c["city"] for c in city_out if c["n_strength_scaled"] > 0],
            "cities_with_any_strength_strict": [c["city"] for c in city_out if c["n_strength_strict"] > 0],
            "shenzhen_strength_items": next(([x["item"] for x in c["strength_scaled"]]
                                             for c in city_out if c["city"] == "深圳"), []),
            "n_strength_scaled_total": sum(c["n_strength_scaled"] for c in city_out),
            "n_strength_strict_total": sum(c["n_strength_strict"] for c in city_out),
            "bay_area_item_city_counts_direct": bay_direct,
            "bay_area_item_city_counts_scaled": bay_scaled,
            "bay_area_advantage_items_direct": bay_adv_direct,
            "bay_area_advantage_items_scaled": bay_adv_scaled,
            "weak_signal_cities": [c["city"] for c in city_out if c["weak_signal_fallback"]],
        },
        "support_judgment": "部分支持",
        "support_note": (
            f"11 城中仅 {n} 城（{'/'.join(available)}）有机构底册，{len(missing)} 城无数据；"
            f"12 分项仅 {n_computable} 项可算（论文/联合专利/转移/合作项目/政策有效性缺测）；"
            "优势识别仅能覆盖少数城市，且「深圳在全部可算分项均居首」使其余城市优势清单为空 → 部分支持"
        ),
    }
    save_out(METRIC, out)


if __name__ == "__main__":
    main()
