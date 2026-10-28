#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_CITY_TALENT_INDEX_SZ —— 深圳重点人才指数

口径来源：注册表 `formula = pending_cosign: human:唐绍祖（未签）`、`algorithm_type: third_party`、
`source_tables: [pending_ods]`；`calc-logic/INNOV` 下无同 ID 正本；注册表还明写
「与 M_INNOV_CITY_TALENT_INDEX_GLOBAL 不同宇宙 → 不 reuse（Q-MO-DS06-02）」。
本件因此**不与 GLOBAL 共用合成口径**：GLOBAL 以城市为对象、规模叶参与加权；
本件以「深圳重点人才池」为对象，只用人均/占比叶，规模只作披露不参与合成。

零 DB：只读 code/_snapshots21 族级快照。
  talent_w15n1_20261023.json       城市级事实面（本批探针）
  talent22_panel_20261022.json     20,420 名可锚定学者画像（含 h / 论文 / 专利 / 境外经历）

运行：cd code && python3 M_INNOV_CITY_TALENT_INDEX_SZ.py
"""
from __future__ import annotations

import collections
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_CITY_TALENT_INDEX_SZ_out.json")

CITY = "深圳市"
REF_MIN = 50          # 参照城市门槛：可锚定学者 ≥50 人（用于百分位秩）
# (叶编号, profile 字段, 中文名)
LEAVES = [
    ("S1_h_median", "h_median", "学术质量（h 中位数）"),
    ("S2_h_ge50_share", "h_ge50_share", "拔尖密度（h≥50 占比）"),
    ("S3_active_3y_share", "active_3y_share", "近三年活跃率（末日发文年 ≥2023）"),
    ("S4_pat_person_share", "pat_person_share", "产业贡献率（有专利发明人匹配记录的人占比）"),
    ("S5_intl_share", "intl_share", "国际化率（有境外任职或境外学历记录的人占比）"),
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct_rank(values, target):
    """target 在 values 中的百分位秩（0—100，含并列取中位秩）。"""
    lt = sum(1 for v in values if v < target)
    eq = sum(1 for v in values if v == target)
    return (lt + 0.5 * eq) / len(values) * 100


def main() -> int:
    tp = load("talent_w15n1_20261023.json")["facts"]
    panel = load("talent22_panel_20261022.json")["scholars"]

    by_city = collections.defaultdict(list)
    for s in panel:
        by_city[s.get("city")].append(s)

    def profile(sub):
        n = len(sub)
        hs = [s["h"] for s in sub if isinstance(s.get("h"), (int, float))]
        return {
            "scholars": n,
            "h_median": statistics.median(hs) if hs else None,
            "h_ge30": sum(1 for h in hs if h >= 30),
            "h_ge50": sum(1 for h in hs if h >= 50),
            "h_ge50_share": round(sum(1 for h in hs if h >= 50) / n * 100, 4) if n else None,
            "active_3y": sum(1 for s in sub if (s.get("y1") or 0) >= 2023),
            "active_3y_share": round(sum(1 for s in sub if (s.get("y1") or 0) >= 2023) / n * 100, 4) if n else None,
            "pat_persons": sum(1 for s in sub if (s.get("pat") or 0) > 0),
            "pat_person_share": round(sum(1 for s in sub if (s.get("pat") or 0) > 0) / n * 100, 4) if n else None,
            "intl": sum(1 for s in sub if (s.get("work_for") or 0) > 0 or (s.get("edu_for") or 0) > 0),
            "intl_share": round(sum(1 for s in sub
                                   if (s.get("work_for") or 0) > 0 or (s.get("edu_for") or 0) > 0) / n * 100, 4) if n else None,
            "academicians": sum(int(s.get("acad") or 0) for s in sub),
            "cite_sum": int(sum(s["cite"] for s in sub if isinstance(s.get("cite"), (int, float)))),
            "paper_sum": int(sum(s["paper"] for s in sub if isinstance(s.get("paper"), (int, float)))),
            "co_deg_filled": sum(1 for s in sub if s.get("co_deg") is not None),
        }

    np_profile = profile(panel)
    sz = profile(by_city[CITY])
    ref = {c: profile(v) for c, v in by_city.items()
           if c not in ("未归属", "未填", "海外") and len(v) >= REF_MIN}

    # ---- 五叶：深圳在三类参照系里的位置
    leaf_rows = []
    for key, pkey, label in LEAVES:
        vals = [ref[c][pkey] for c in ref if ref[c][pkey] is not None]
        target = sz[pkey]
        leaf_rows.append({
            "leaf": key,
            "label": label,
            "sz_value": round(target, 4),
            "national_value": round(np_profile[pkey], 4),
            "ref_cities": len(vals),
            "ref_median": round(statistics.median(vals), 4),
            "ref_max": round(max(vals), 4),
            "ref_min": round(min(vals), 4),
            "pct_rank": round(pct_rank(vals, target), 2),
            "sz_over_national": round(target / np_profile[pkey], 4) if np_profile[pkey] else None,
        })
    score = round(sum(r["pct_rank"] for r in leaf_rows) / len(leaf_rows), 2)

    # ---- 参照城市全表（按 S2 拔尖密度降序，便于看深圳的位置）
    ref_rows = []
    for c, p in ref.items():
        ref_rows.append({"city": c, **{k: p[pk] for k, pk, _ in LEAVES}, "scholars": p["scholars"],
                         "academicians": p["academicians"]})
    ref_rows.sort(key=lambda r: -(r["S2_h_ge50_share"] or 0))

    # ---- 深圳池的构成（披露用）
    sz_panel = by_city[CITY]
    y1_dist = collections.Counter((s.get("y1") or 0) // 5 * 5 for s in sz_panel)
    h_bucket = collections.Counter(
        "h≥50" if (s.get("h") or 0) >= 50 else "30≤h<50" if (s.get("h") or 0) >= 30
        else "10≤h<30" if (s.get("h") or 0) >= 10 else "h<10" for s in sz_panel)

    out = {
        "metric_id": "M_INNOV_CITY_TALENT_INDEX_SZ",
        "metric_name_zh": "深圳重点人才指数",
        "main_is_official": False,
        "support_judgment": "部分支持",
        "verdict_kind": "self_built_substitute",
        "sources": [
            "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）",
            "code/_snapshots21/talent_w15n1_20261023.json",
            "code/_snapshots21/talent22_panel_20261022.json",
        ],
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": ("活跃率叶的「近三年」窗口锁 2021—2023：2024 年中文论文语料是回填孤峰"
                            "（32,379 篇，为 2023 年 4.87 倍），2025—2026 为残年；2017—2020 专利零行"
                            "（DATA_FACTS §3.13），故不进任何分母。"),
        "params": {
            "object": "深圳重点人才池（city 字段归城的 213 名可锚定学者）",
            "ref_pool": f"全国可锚定学者 ≥{REF_MIN} 人的城市（{len(ref)} 个）",
            "synthesis": "五叶各自取百分位秩（0—100），等权平均；不用规模叶，故不是总量排名",
            "main_is_official": False,
            "missing_dim_policy": "缺维写 null、不进分母；本件五叶全可得，无缺维",
        },
        "headline": {
            "city": CITY,
            "index": score,
            "leaves": len(leaf_rows),
            "sz_scholars": sz["scholars"],
            "national_scholars": np_profile["scholars"],
            "sz_share_of_national_pct": round(sz["scholars"] / np_profile["scholars"] * 100, 4),
            "ref_cities": len(ref),
            "sz_h_median": sz["h_median"],
            "national_h_median": np_profile["h_median"],
            "sz_h_ge50_share": sz["h_ge50_share"],
            "national_h_ge50_share": np_profile["h_ge50_share"],
            "sz_active_3y_share": sz["active_3y_share"],
            "national_active_3y_share": np_profile["active_3y_share"],
            "sz_pat_person_share": sz["pat_person_share"],
            "national_pat_person_share": np_profile["pat_person_share"],
            "sz_intl_share": sz["intl_share"],
            "national_intl_share": np_profile["intl_share"],
            "sz_academicians": sz["academicians"],
            "sz_cite_sum": sz["cite_sum"],
            "sz_paper_sum": sz["paper_sum"],
        },
        "leaves": leaf_rows,
        "ref_cities": ref_rows,
        "pool_composition": {
            "h_buckets": dict(h_bucket),
            "last_paper_year_5y_bucket": {str(k): v for k, v in sorted(y1_dist.items())},
            "co_deg_filled": sz["co_deg_filled"],
            "co_deg_filled_pct": round(sz["co_deg_filled"] / sz["scholars"] * 100, 4),
        },
        "derived": {
            "sz_share_of_national_pct": {
                "value": round(sz["scholars"] / np_profile["scholars"] * 100, 4),
                "numerator": sz["scholars"], "denominator": np_profile["scholars"],
                "denominator_note": "深圳 213 / 全国可锚定学者 20,420",
            },
            "sz_h_ge50_over_national": {
                "value": round(sz["h_ge50_share"] / np_profile["h_ge50_share"], 4),
                "numerator": sz["h_ge50_share"], "denominator": np_profile["h_ge50_share"],
                "denominator_note": f"深圳 h≥50 占比 {sz['h_ge50_share']}% / 全国 {round(np_profile['h_ge50_share'], 4)}%",
            },
            "sz_h_ge30_over_national": {
                "value": round(sz["h_ge30"] / sz["scholars"] / (np_profile["h_ge30"] / np_profile["scholars"]), 4),
                # 2026-10-23 修：原写 numerator=73 / denominator=213 记的是**人数**，
                # 而 value 是两个**占比**相除。读者拿 73/213 只会得到 34.2723%，
                # 得不到 1.7208，等于 note 写了但算不回去（新闸 audit_derived_arith 抓到）。
                # 改为把两个占比放分子分母、人数退回 note。
                "numerator": round(sz["h_ge30"] / sz["scholars"] * 100, 4),
                "denominator": round(np_profile["h_ge30"] / np_profile["scholars"] * 100, 4),
                "denominator_note": (
                    f"深圳 h≥30 占比 {round(sz['h_ge30'] / sz['scholars'] * 100, 4)}%"
                    f"（{sz['h_ge30']}/{sz['scholars']} 人）"
                    f" / 全国 h≥30 占比 {round(np_profile['h_ge30'] / np_profile['scholars'] * 100, 4)}%"
                    f"（{np_profile['h_ge30']}/{np_profile['scholars']} 人）"),
            },
            "sz_active_deficit_pct": {
                "value": round(sz["active_3y_share"] - np_profile["active_3y_share"], 4),
                "numerator": sz["active_3y_share"], "denominator": np_profile["active_3y_share"],
                "denominator_note": (f"深圳 {sz['active_3y_share']}% − 全国 "
                                     f"{round(np_profile['active_3y_share'], 4)}%，负值表示深圳池的语料末日更早"),
            },
            "sz_intl_over_national": {
                "value": round(sz["intl_share"] / np_profile["intl_share"], 4),
                "numerator": sz["intl_share"], "denominator": np_profile["intl_share"],
                "denominator_note": f"深圳 {sz['intl_share']}% / 全国 {round(np_profile['intl_share'], 4)}%",
            },
            "sz_pat_over_national": {
                "value": round(sz["pat_person_share"] / np_profile["pat_person_share"], 4),
                "numerator": sz["pat_person_share"], "denominator": np_profile["pat_person_share"],
                "denominator_note": (f"深圳 {sz['pat_person_share']}% / 全国 "
                                     f"{round(np_profile['pat_person_share'], 4)}%"),
            },
            "sz_academician_share_pct": {
                "value": round(sz["academicians"] / sz["scholars"] * 100, 4),
                "numerator": sz["academicians"], "denominator": sz["scholars"],
                "denominator_note": "深圳 5 人 / 213 人；院士来自 dwd_scholar_talent_flag（112 人全库）",
            },
            "gz_over_sz_scholars": {
                "value": round((ref.get("广州市") or {}).get("scholars", 0) / sz["scholars"], 4),
                "numerator": (ref.get("广州市") or {}).get("scholars", 0), "denominator": sz["scholars"],
                "denominator_note": (f"广州 {(ref.get('广州市') or {}).get('scholars', 0)} / "
                                     f"深圳 {sz['scholars']}（同一归城口径）"),
            },
        },
        "checks": {
            "five_leaves": len(leaf_rows) == 5,
            "pct_rank_in_range": all(0 <= r["pct_rank"] <= 100 for r in leaf_rows),
            "sz_in_ref_pool": CITY in ref,
            "ref_pool_min": min(p["scholars"] for p in ref.values()),
            "score_equals_leaf_mean": abs(round(score, 2) - round(sum(r["pct_rank"] for r in leaf_rows) / 5, 2)) < 0.005,
            "national_equals_panel": np_profile["scholars"] == len(panel),
        },
        "notes": [
            "本件与 GLOBAL 不同宇宙（注册表 Q-MO-DS06-02 明令不 reuse）：GLOBAL 以城市为对象、"
            "规模叶进加权；本件以深圳人才池为对象，只取人均/占比叶，规模仅披露。",
            "指数是自建替代读数，`main_is_official=false`；注册表 formula 未签。",
            "深圳池 213 人是「机构串能归城 + 姓名唯一 + 在中文语料里有论文」三重筛选后的子集，"
            "不是深圳人才总量；比例叶受筛选强度影响（北京池更深、普通人更多，比率被拉低）。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["headline"], ensure_ascii=False, indent=1))
    for r in leaf_rows:
        print(r["leaf"], r["sz_value"], "nat", r["national_value"], "pct", r["pct_rank"])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
