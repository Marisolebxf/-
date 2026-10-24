#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_05_GBA_ANALYSIS_004（短板因素分析）复现脚本。

口径：王惠「同 M_INNOV_GBA_SWOT_WEAKNESS」——11 城中排名落入末段（rank ≥ 9）的分项
即短板，须给出表现证据与可操作改进建议。

关键实测：王惠原阈值 rank ≥ 9 在 4 城宇宙下恒不命中（n=4 < 9），必须做比例映射；
本脚本同时输出 direct / scaled / strict 三档，用「阈值不可移植」本身作为证据。

输出：M_INNOV_DS_05_GBA_ANALYSIS_004_out.json
"""
from __future__ import annotations

import math

from _innov_h_common import (GBA11, gkx_light_check, load_json, norm_minmax, pct,
                             rank_desc, save_out)

METRIC = "M_INNOV_DS_05_GBA_ANALYSIS_004"

SUBITEMS = [
    ("res_paper", "论文产出", "创新资源", False, "dwd_zh_author 无城市键"),
    ("res_patent", "专利产出", "创新资源", True, "patent_cnt"),
    ("res_rd", "研发经费投入", "创新资源", True, "rd_funding"),
    ("org_cnt", "创新机构数量", "创新机构", True, "org_cnt"),
    ("org_hightech", "高新技术企业数", "创新机构", True, "hightech_cnt"),
    ("org_output", "机构创新产出", "创新机构", True, "patent_cnt"),
    ("mech_joint", "联合专利合作", "创新机制", False, "无 applicants 列；applicants 表覆盖 0.96%"),
    ("mech_transfer", "技术转移", "创新机制", False, "转移表无机构外键"),
    ("mech_project", "合作项目", "创新机制", False, "funded_institution 未对齐"),
    ("env_policy", "政策供给", "创新环境", True, "policy_cnt"),
    ("env_valid", "政策有效性", "创新环境", False, "status 全为「有效」，无失效样本"),
    ("env_density", "高企密度", "创新环境", True, "hightech_density"),
]

# 王惠原表固定映射（V1.5-20260830 §第二步·改进建议），不另跑模型
REMEDY = {
    "res_patent": "加大专利申请与布局",
    "res_paper": "加强论文产出与合作发表",
    "res_rd": "提高研发人员或上市研发经费",
    "org_cnt": "引入和培育创新主体",
    "org_output": "提升机构专利与论文产出",
    "org_hightech": "推动高企认定与科研院所建设",
    "mech_joint": "推动多主体联合申请",
    "mech_project": "增加多机构立项",
    "mech_transfer": "提高专利转移占比",
    "env_policy": "完善地方创新政策供给",
    "env_valid": "拓展政策主题覆盖",
    "env_density": "提高高新技术企业占比",
}


def main():
    idx = load_json("M_INNOV_GBA_INDEX_BUNDLE_out.json")
    swot = load_json("M_INNOV_GBA_SWOT_BUNDLE_out.json")
    probe = load_json("_probe_innov_h_gkx_out.json", {}) or {}
    rows = idx["rows"]
    n = len(rows)
    available = [r["city"] for r in rows if r.get("org_cnt", 0) > 0]
    missing = [c for c in GBA11 if c not in available]

    items = []
    for code, cn, sub, ok, field_or_reason in SUBITEMS:
        if not ok:
            items.append({"item": code, "name_cn": cn, "sub_index": sub,
                          "computable": False, "reason": field_or_reason})
            continue
        vals = [r[field_or_reason] for r in rows]
        norms = norm_minmax(vals)
        items.append({
            "item": code, "name_cn": cn, "sub_index": sub, "computable": True,
            "values": {r["city"]: r[field_or_reason] for r in rows},
            "ranks": {r["city"]: rank_desc(vals, r[field_or_reason]) for r in rows},
            "norms": {r["city"]: round(v, 4) for r, v in zip(rows, norms)},
            "remedy": REMEDY.get(code),
        })

    n_comp = sum(1 for i in items if i["computable"])
    thr_direct = 9                                  # 王惠原文（11 城）
    thr_scaled = max(1, math.ceil(n * 9 / 11))      # 4 城 → 4（末位）
    thr_loose = max(1, math.ceil(n * 0.73))         # 4 城 → 3（末 27%~50% 区间）

    city_out = []
    for r in rows:
        city = r["city"]
        d, s, l = [], [], []
        for it in items:
            if not it["computable"]:
                continue
            rk = it["ranks"][city]
            rec = {"item": it["item"], "name_cn": it["name_cn"], "sub_index": it["sub_index"],
                   "value": it["values"][city], "rank": rk, "of": n,
                   "gap_to_leader": round(it["norms"][city], 4),
                   "remedy": it["remedy"]}
            if rk >= thr_direct:
                d.append(rec)
            if rk >= thr_scaled:
                s.append(rec)
            if rk >= thr_loose:
                l.append(rec)
        # 王惠兜底：无命中则取 rank 最大的 1 项，标 weak_signal=1
        fallback = None
        if not l:
            pool = [{"item": it["item"], "name_cn": it["name_cn"], "sub_index": it["sub_index"],
                     "value": it["values"][city], "rank": it["ranks"][city], "of": n,
                     "gap_to_leader": round(it["norms"][city], 4), "remedy": it["remedy"]}
                    for it in items if it["computable"]]
            fallback = max(pool, key=lambda x: x["rank"])
        city_out.append({
            "city": city, "rank_overall_by_capacity_index": None,
            "n_weak_direct": len(d), "n_weak_scaled": len(s), "n_weak_loose": len(l),
            "weak_direct": d, "weak_scaled": s, "weak_loose": l,
            "weak_signal_fallback": fallback,
            "mean_norm_of_weak_loose": round(sum(x["gap_to_leader"] for x in l) / len(l), 4) if l else None,
        })

    def bay_area(key):
        cnt = {}
        for c in city_out:
            for x in c[key]:
                cnt[x["item"]] = cnt.get(x["item"], 0) + 1
        return dict(sorted(cnt.items(), key=lambda kv: -kv[1]))

    bay_direct = bay_area("weak_direct")
    bay_loose = bay_area("weak_loose")
    bay_wk_direct = [k for k, v in bay_direct.items() if v >= 4]
    bay_wk_loose = [k for k, v in bay_loose.items() if v >= 4]

    live = gkx_light_check("SELECT COUNT(*) AS c FROM dwd_org_base_info")

    out = {
        "metric_id": METRIC,
        "metric_name": "短板因素分析",
        "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_GBA_SWOT_WEAKNESS.md（王惠口径）",
        "source_artifacts": [
            "code/M_INNOV_GBA_INDEX_BUNDLE_out.json",
            "code/M_INNOV_GBA_SWOT_BUNDLE_out.json",
            "code/_probe_innov_h_gkx_out.json",
        ],
        "probes": {
            "gkx_live_count_org": live,
            "n_cities_available": n,
            "cities_available": available,
            "cities_missing": missing,
            "gba_coverage_pct": pct(n, 11),
            "subitems_total": len(SUBITEMS),
            "subitems_computable": n_comp,
            "subitems_coverage_pct": pct(n_comp, len(SUBITEMS)),
            "index_bundle_rows": rows,
        },
        "thresholds": {
            "wanghui_original": "11 城 rank ≥ 9（末 3 位）",
            "direct_on_4_cities": thr_direct,
            "direct_hits": 0,
            "scaled_bottom_27pct": thr_scaled,
            "loose_bottom_73pct_start": thr_loose,
            "note": "rank≥9 在 4 城下恒不命中（0 行）→ 原阈值不可移植；scaled 退化为「末位=短板」，loose 使 50% 城市入选",
        },
        "subitems": items,
        "city_results": city_out,
        "summary": {
            "cities_with_weak_direct": [c["city"] for c in city_out if c["n_weak_direct"] > 0],
            "cities_with_weak_scaled": [c["city"] for c in city_out if c["n_weak_scaled"] > 0],
            "cities_with_weak_loose": [c["city"] for c in city_out if c["n_weak_loose"] > 0],
            "n_weak_scaled_total": sum(c["n_weak_scaled"] for c in city_out),
            "n_weak_loose_total": sum(c["n_weak_loose"] for c in city_out),
            "mech_index_constant": all(r["mech_index"] == 50.0 for r in rows),
            "joint_patent_all_zero": all(r["joint_patent"] == 0 for r in rows),
            "bay_area_item_city_counts_direct": bay_direct,
            "bay_area_item_city_counts_loose": bay_loose,
            "bay_area_weakness_items_direct": bay_wk_direct,
            "bay_area_weakness_items_loose": bay_wk_loose,
            "weak_signal_cities": [c["city"] for c in city_out if c["weak_signal_fallback"]],
        },
        "support_judgment": "部分支持",
        "support_note": (
            f"11 城仅 {n} 城有数据；12 分项 {n_comp} 项可算；王惠 rank≥9 阈值在 4 城宇宙零命中，"
            "比例映射后短板识别退化为「末位识别」，且机制维因 joint_patent 全 0 被中位赋值 50 分、完全不可分辨 → 部分支持"
        ),
    }
    save_out(METRIC, out)


if __name__ == "__main__":
    main()
