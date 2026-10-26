#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""土地创新产出效益与利用效率（M_INNOV_KEYD_LAND）——B-sample 降档实现。

注册表定义：「土地利用类型上的创新产出效益（xlsx 104）与土地利用效率（xlsx 105）共核，
对象=GIS 用地/产出图层」。要算地均产出，最少需要三样东西：地块边界（面积）、
用地类型（工业/商服/科研）、地块级产出归属。三样在 gkx 全都没有——
`dwd_dim_admin_area` 是纯行政区划树（19,633 行，29 列里没有面积、没有 polygon），
`dwd_org_base_info` 只有点（addr_lng/addr_lat），没有面。

本件因此降档为「空间强度替代读数」：用注册点位的格网密度 + 创新行业占比刻画
「哪里创新活动最密」，并明确声明这不等于「地均产出」。

正本依赖 `carrier_index`（载体指数）/ `city_index`（城市指数）/ `innovation_point_map`
（创新点位图）/ `carrier_org_rel`（载体-企业关系），四表在 gkx 全部查无；live 的 ads/dim
侧只有造数表（carrier_index 140 行、innovation_point_map 261 行等），不参与计算。

本件改用的可算面：`dwd_org_base_info` 的注册地址坐标（深圳 95,525/95,600 点，99.92%），
按 0.005°（≈553 m × 512 m）格网聚合，得到「企业空间热点」。这不是「创新载体」——
载体是有物理边界、有运营主体、有入驻企业清单的园区/孵化器；本件只有注册点。
两者差在哪、能替代到哪一步，写进 `substitution` 段，不混为一谈。

运行：cd code && python3 _probe_keyd_w15n1.py && python3 M_INNOV_KEYD_LAND.py
输出：code/M_INNOV_KEYD_LAND_out.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_KEYD_LAND_out.json")
TZ = timezone(timedelta(hours=8))

CITY = "深圳市"
CITY_AREA_KM2 = 1997.47          # 深圳市行政区域面积（公开统计口径）
W = {"K1_scale": 0.50, "K2_innov_mix": 0.30, "K3_specialization": 0.20}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0] * len(vals)
    return [(v - lo) / (hi - lo) * 100 for v in vals]


def gini(counts):
    xs = sorted(counts)
    n = len(xs)
    s = sum(xs)
    if n == 0 or s == 0:
        return 0.0
    cum = 0.0
    for i, x in enumerate(xs, 1):
        cum += i * x
    return round((2 * cum) / (n * s) - (n + 1) / n, 6)


def main() -> int:
    snap = load("keyd_land_w15n1_20261023.json")
    pts = snap["points"]
    grid = snap["grid"]
    hot = snap["hotspots"]

    rows = []
    for h in hot:
        rows.append({
            "cell": h["cell"], "lng": h["lng"], "lat": h["lat"],
            "orgs": h["orgs"], "share_city_pct": h["share_pct"],
            "district": h["district"], "district_purity_pct": h["district_share_pct"],
            "top_industry": h["industry"], "top_industry_share_pct": h["industry_share_pct"],
            "innov_share_pct": h["innov_ind_share_pct"],
            "ind_top3": h["ind_top3"],
            "_K1": round(math.log1p(h["orgs"]) / math.log1p(hot[0]["orgs"]) * 100, 4),
        })
    z2 = minmax([r["innov_share_pct"] for r in rows])
    z3 = minmax([r["top_industry_share_pct"] for r in rows])
    for r, a, b in zip(rows, z2, z3):
        r["_K2"] = round(a, 4)
        r["_K3"] = round(b, 4)
        r["score"] = round(W["K1_scale"] * r["_K1"] + W["K2_innov_mix"] * r["_K2"]
                           + W["K3_specialization"] * r["_K3"], 4)
    rows.sort(key=lambda r: -r["score"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["landmark_label"] = f"{r['district']}·{r['top_industry']}集聚区"

    # ---- 客观熵权（对照）----
    cols = [[r["_K1"] for r in rows], [r["_K2"] for r in rows], [r["_K3"] for r in rows]]
    n = len(rows)
    ent, det = [], {}
    for j, c in enumerate(cols):
        s = sum(c) or 1.0
        p = [(v / s) if v > 0 else 0.0 for v in c]
        e = -1.0 / math.log(n) * sum(x * math.log(x) for x in p if x > 0)
        ent.append(1 - e)
        det[list(W)[j]] = {"entropy": round(e, 6), "divergence": round(1 - e, 6)}
    tot = sum(ent) or 1.0
    ent = [w / tot for w in ent]

    # ---- 熵权对照排名（敏感性）----
    ent_map = dict(zip(W, ent))
    for r in rows:
        r["_score_entropy"] = round(ent_map["K1_scale"] * r["_K1"] + ent_map["K2_innov_mix"] * r["_K2"]
                                    + ent_map["K3_specialization"] * r["_K3"], 4)
    ent_ranked = sorted(rows, key=lambda r: -r["_score_entropy"])
    main_top10 = {r["landmark_label"] + f"#{r['rank']}" for r in rows[:10]}
    ent_top10 = {r["landmark_label"] + f"#{i}" for i, r in enumerate(ent_ranked[:10], 1)}
    overlap = len({r["cell"][0] * 100000 + r["cell"][1] for r in rows[:10]}
                  & {r["cell"][0] * 100000 + r["cell"][1] for r in ent_ranked[:10]})
    sensitivity = {
        "main_top1": {"label": rows[0]["landmark_label"], "orgs": rows[0]["orgs"], "score": rows[0]["score"]},
        "entropy_top5": [{"rank": i, "label": r["landmark_label"], "orgs": r["orgs"],
                          "score": r["_score_entropy"], "innov_share_pct": r["innov_share_pct"]}
                         for i, r in enumerate(ent_ranked[:5], 1)],
        "top10_overlap": overlap,
        "top1_flip": rows[0]["cell"] != ent_ranked[0]["cell"],
        "note": ("熵权把 72.56% 的权重压到行业集中度，榜首直接换成罗湖·批发零售集聚区（276 家、创新占比 9.06%），"
                 "主榜前 10 只剩 6 个在熵权前 10；熵权不是「更对」，只是说明榜首由权重决定，不由数据决定"),
    }

    # ---- 城市级读数 ----
    city_density = round(pts["city_total_orgs"] / CITY_AREA_KM2, 4)
    cells = grid["cells"]
    cell_km2 = round(grid["cell_m_lat"] * grid["cell_m_lng"] / 1e6, 6)
    cells_total_km2 = round(cells * cell_km2, 4)
    hot_cells_km2 = round(30 * cell_km2, 4)
    derived = {
        "city_org_density_per_km2": {
            "value": city_density, "numerator": pts["city_total_orgs"],
            "denominator": CITY_AREA_KM2,
            "denominator_note": "深圳 95,600 家 / 1,997.47 km²；分母是全市行政面积（公开口径），不是建成区面积",
        },
        "top30_share_pct": {
            "value": grid["top30_share_pct"], "numerator": grid["top30_orgs"],
            "denominator": pts["usable_in_box"],
            "denominator_note": "前 30 个格网 10,329 家 / 可用点位 95,525 家",
        },
        "top30_area_share_pct": {
            "value": round(hot_cells_km2 / CITY_AREA_KM2 * 100, 6),
            "numerator": hot_cells_km2, "denominator": CITY_AREA_KM2,
            "denominator_note": f"前 30 格面积 {hot_cells_km2} km² / 全市 1,997.47 km²",
        },
        # 2026-10-23 补：这两个敏感性口径原先是我手写进 out.json 的，
        # 重跑脚本就消失了（正文引用它们 → md_vs_out 报 2 处未命中）。
        # **手改产物的字段活不过一次 rebuild**，必须由脚本自己写。
        "top30_area_share_pct_griddenom": {
            "value": round(hot_cells_km2 / cells_total_km2 * 100, 4),
            "numerator": hot_cells_km2, "denominator": cells_total_km2,
            "denominator_note": (f"前 30 格面积 {hot_cells_km2} km² / 有企业落点的格网面积 "
                                 f"{cells_total_km2} km²（敏感性口径；主口径分母为全市 1,997.47 km²）"),
        },
        "top30_share_area_ratio_griddenom": {
            "value": round(grid["top30_share_pct"]
                           / (hot_cells_km2 / cells_total_km2 * 100), 4),
            "numerator": grid["top30_share_pct"],
            "denominator": round(hot_cells_km2 / cells_total_km2 * 100, 4),
            "denominator_note": ("前 30 格机构份额 10.8129% / 格网口径面积份额（敏感性口径；"
                                 "主口径倍数 25.4123，分母为全市面积）"),
        },
        "concentration_ratio": {
            "value": round(grid["top30_share_pct"] / (hot_cells_km2 / CITY_AREA_KM2 * 100), 4),
            "numerator": grid["top30_share_pct"],
            "denominator": round(hot_cells_km2 / CITY_AREA_KM2 * 100, 6),
            "denominator_note": "份额比面积：占 0.42% 的面积承载 10.81% 的企业，倍数即此值",
        },
        "coord_missing_pct": {
            "value": round((pts["city_total_orgs"] - pts["with_lng"]) / pts["city_total_orgs"] * 100, 4),
            "numerator": pts["city_total_orgs"] - pts["with_lng"],
            "denominator": pts["city_total_orgs"],
            "denominator_note": "缺坐标 75 家 / 深圳底册 95,600 家",
        },
        "coverage_pct": {
            "value": pts["coverage_pct"], "numerator": pts["with_lng"],
            "denominator": pts["city_total_orgs"],
            "denominator_note": "有经纬度 95,525 家 / 深圳底册 95,600 家",
        },
        "hhi": {"value": grid["hhi"], "numerator": None, "denominator": cells,
                "denominator_note": f"格网份额平方和，{cells} 个格网；均匀分布理论值 {round(1 / cells, 8)}"},
        "hhi_over_uniform": {"value": round(grid["hhi"] / (1.0 / cells), 4), "numerator": round(grid["hhi"], 8),
                             "denominator": round(1.0 / cells, 8),
                             "denominator_note": "实测 HHI / 完全均匀时的 1/3510；倍数 = 集聚程度"},
        "hot1_single_cell_share_pct": {
            "value": grid["top1_share_pct"], "numerator": hot[0]["orgs"],
            "denominator": pts["usable_in_box"],
            "denominator_note": "单格 985 家 / 95,525 家；该格同时是「疑似挂靠地址」重点怀疑对象",
        },
        "innov_share_top30_avg_pct": {
            "value": round(sum(r["innov_share_pct"] for r in rows) / len(rows), 4),
            "numerator": round(sum(r["innov_share_pct"] for r in rows), 4),
            "denominator": len(rows),
            "denominator_note": "前 30 格「科研技术服务业+信息传输软件业」占比的算术均值",
        },
            "city_innov_share_pct": {
                # 2026-10-23 修：原来 value 是「两个行业的 share_pct 相加」，
                # 而 share_pct 各自已是 2 位小数的舍入值（13.41 + 10.48 = 23.89），
                # 与真实分子分母相除（23.8807）差 0.0093。**分项舍入再相加，误差会放大**，
                # 与 M_ENT_AVG_RD_INVESTMENT.chain_unmapped_sum_pct 是同一类错。
                # 改为直接用分子/分母求值，舍入前的分项相加结果留在 note 里。
                "value": round((snap["industries"][2]["orgs"] + snap["industries"][3]["orgs"])
                               / pts["usable_in_box"] * 100, 4),
                "numerator": snap["industries"][2]["orgs"] + snap["industries"][3]["orgs"],
                "denominator": pts["usable_in_box"],
                "denominator_note": ("全市信息传输软件业 12,815 家 + 科研技术服务业 9,997 家 / 95,525 家。"
                                     "注意：若把两个行业各自 2 位小数的 share_pct 相加会得 23.89，"
                                     "比直除的 23.8807 高 0.0093，那是分项舍入累加，不是口径差"),
            },
    }

    out = {
        "metric_id": "M_INNOV_KEYD_LAND",
        "metric_name": "土地创新产出效益与利用效率",
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "support_judgment": "部分支持",
        "verdict_reason": (
            "正本要的是「地块 × 用地类型 × 创新产出」的三元组，gkx 三样全无："
            "carrier_index / city_index / innovation_point_map / carrier_org_rel 四表查无，"
            "`dwd_dim_admin_area` 无面积列（只有 code/name 层级），`dwd_org_base_info` 只有点没有面。"
            "因此地均产出（亿元/km²）、土地利用效率、用地类型分组效益全部不可算。"
            "可算的只有替代读数：深圳 95,525 个注册点位（覆盖 99.92%）按 0.005° 格网聚合后的"
            "密度、集聚度（HHI/份额比）与创新行业占比——这是「创新活动空间强度」，不是地均产出。"
        ),
        "source": {
            "library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
            "mode": "read-only", "touched": False,
            "note": "本件零 SQL：点位由 _probe_keyd_w15n1.py 从 dwd_org_base_info 一次拉取后落盘",
        },
        "sources": ["code/_snapshots21/keyd_land_w15n1_20261023.json"],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": (
            "本件是**截面空间快照**，不是年度序列：点位取 gkx 当前时点（2026-10-23）的注册地址，"
            "不涉年份窗口；工商底册不含「首次入驻载体年份」，所以无法回溯任一地标的历史。"
            "base_years_used 记 2026 仅表示「取数时点」，不代表任何统计年度。"
        ),
        "scope": f"{CITY} 全域注册地址点位（格网 0.005°）；替代读数，非地块级地均产出",
        "evaluation_set": [r["landmark_label"] + f"#{r['rank']}" for r in rows[:20]],
        "substitution": {
            "replaced": "innovation_point_map / carrier_index（点位于载体）→ dwd_org_base_info 注册地址点位",
            "same": "两者都带坐标，都能做密度、邻域与集聚分析",
            "different": [
                "正本的分子是「该地块上的创新产出（专利/高企/研发投入）」，本件分子是「该格网里的企业法人数」",
                "正本的分母是「地块面积（km²，按用地类型）」，本件的分母只能是「全市行政面积」",
                "一个园区内 500 家企业 → 点位显示 500 家，地块仍只有 1 块（点位≠地块）",
                "挂靠地址会让上千家无实体办公的企业共享一个坐标（假热点）",
            ],
            "consequence": "本件输出只能叫「企业空间热点」，不能叫「创新载体地图」；"
                           f"第 1 名单格 {hot[0]['orgs']} 家、主导行业却是租赁和商务服务业 23.96%，"
                           "这是挂靠地址的典型形态，已在下游逐条标注可疑",
        },
        "grid": {
            "cell_deg": snap["cell_deg"],
            "cell_m_lat": grid["cell_m_lat"], "cell_m_lng": grid["cell_m_lng"],
            "cell_km2": cell_km2,
            "cells": cells,
            "cells_total_km2": cells_total_km2,
            "city_area_km2": CITY_AREA_KM2,
            "grid_covers_km2_pct": round(cells_total_km2 / CITY_AREA_KM2 * 100, 4),
            "note": "格网只覆盖「有点位落下的格子」，不是全市无缝网格；"
                    "山区/水域/无企业格不在 3,510 个格内，故 cells_total_km2 < 全市面积",
        },
        "points": pts,
        "city_metrics": {
            "org_density_per_km2": city_density,
            "hhi": grid["hhi"],
            "top30_share_pct": grid["top30_share_pct"],
            "top1_share_pct": grid["top1_share_pct"],
            "median_cell_orgs": grid["median_cell"],
            "cells_with_one_org": grid["cells_with_1"],
            "districts": snap["districts"],
            "industries": snap["industries"],
        },
        "weights": {
            "main": W, "main_is_official": False, "weights_are_authored": True,
            "rationale": "规模占一半（地标的首要含义是「够大」），创新行业占比 0.3（区分商务楼宇与科技集群），"
                         "行业集中度 0.2（专业园区比混合楼宇更像载体）",
            "entropy": {k: round(w, 4) for k, w in zip(W, ent)},
            "entropy_detail": det,
            "sensitivity": sensitivity,
        },
        "landmarks": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows],
        "derived": derived,
        "not_computable": [
            {"item": "地均产出（亿元/km²）", "why": "无地块面积、无园区边界；只有点，没有面"},
            {"item": "土地利用效率（按用地类型分组）", "why": "全库无「用地类型」字段；`dwd_dim_admin_area` 只有行政区划层级"},
            {"item": "地块级创新产出归属", "why": "专利/论文只有机构名与城市，没有地块编号，无法把产出落到地块"},
            {"item": "载体容积率/建筑面积", "why": "无载体实体表，`carrier_index` gkx 查无"},
            {"item": "载体内企业清单", "why": "`carrier_org_rel` gkx 查无；live 57 行为造数"},
            {"item": "载体等级（国家级/省级孵化器）", "why": "无认定名录表；`dwd_org_base_info.org_type` 不区分载体等级"},
            {"item": "区级地均/人均载体密度", "why": "`dwd_dim_admin_area` 只有 code/name 层级，无面积、无 polygon"},
            {"item": "地标的历史演化", "why": "底册无入驻年份，只有当前注册地址"},
        ],
        "absence_probe": {
            "carrier_index": {
                "query": "information_schema.tables WHERE table_name='carrier_index' AND table_schema NOT LIKE 'demo_%'",
                "param": "carrier_index", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_ads": 140},
                "conclusion": "gkx 查无；live ads 140 行为造数（MOCK_TABLE_REGISTRY 已登记），不参与计算",
            },
            "city_index": {
                "query": "information_schema.tables WHERE table_name='city_index' AND table_schema NOT LIKE 'demo_%'",
                "param": "city_index", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_ads": 70},
                "conclusion": "gkx 查无；live ads 70 行（14 城 × 5 年，weight_version=w_v1.0-demo）为造数",
            },
            "innovation_point_map": {
                "query": "information_schema.tables WHERE table_name='innovation_point_map' AND table_schema NOT LIKE 'demo_%'",
                "param": "innovation_point_map", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_ads": 261},
                "conclusion": "gkx 查无；live ads 261 行为造数",
            },
            "carrier_org_rel": {
                "query": "information_schema.tables WHERE table_name='carrier_org_rel' AND table_schema NOT LIKE 'demo_%'",
                "param": "carrier_org_rel", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_dim": 57},
                "conclusion": "gkx 查无；live dim 57 行为造数",
            },
            "admin_division": {
                "query": "information_schema.tables WHERE table_name='admin_division' AND table_schema NOT LIKE 'demo_%'",
                "param": "admin_division", "hit_tables": [], "hit_rows": 0, "count": None,
                "live_hits": {"gkxlumenx_dim": 11},
                "conclusion": "gkx 查无；替代面用 dwd_dim_admin_area（19,633 行区划树，无面积列）",
            },
        },
        "reproduce": "cd code && python3 _probe_keyd_w15n1.py && python3 M_INNOV_KEYD_LAND.py",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    for r in rows[:12]:
        print(f"  {r['rank']:>2} {r['score']:6.2f} {r['landmark_label'][:34]:<34} "
              f"orgs={r['orgs']:>4} innov={r['innov_share_pct']:5.2f}% "
              f"({r['lng']},{r['lat']})")
    print("entropy:", out["weights"]["entropy"])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
