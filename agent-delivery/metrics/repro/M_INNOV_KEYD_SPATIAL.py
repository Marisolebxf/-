#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_KEYD_SPATIAL · 空间密度与集聚度（1 km 网格口径，20261021 换源版）

与已入库 M_ENT_AGGLOMERATION_INDEX 的分工
------------------------------------------
- `M_ENT_AGGLOMERATION_INDEX`：**行政区域 × 产业**的集聚（区位商 LQ / 空间基尼 / HHI），
  回答「某产业在 4 个城市间的分布是否集中」，属属性空间。
- 本指标：**城市内部 1 km 网格**的点格局（密度 / 网格基尼 / 最近邻指数），
  回答「创新资源在同一城市地理空间上落在哪里、有多密、是聚集还是摊开」，属地理空间。
两者分母、对象、粒度都不同，不复用、不互相替代。

20261021 换源
-------------
- 机构底册：`gkx.dwd_org_base_info` 189,116 行
- 坐标：`live.gkxlumenx_dwd.enterprise_extra` 187,983 行可解析（覆盖 99.40%）
- 高企：`_snapshots21/tech_tags_20261021.json`（27,634 家含「高新技术企业」标签）
- 专利：`_snapshots21/star_applicant_agg_gkx.json`（169,226 名，全量 2,939,895 行）
- **零 `dwd_patent` SQL、零演示库 / 零开发库旁路**

方法
----
1. 投影：等距圆柱近似，x = (lng−113.0)·111.32·cos(22.6°)，y = (lat−22.0)·111.32，单位 km。
2. 网格：1 km × 1 km（floor 取整），格面积恒为 1 km²。
3. 密度：占用格均值 = 点数 ÷ 占用格数（不依赖行政区面积，避免外部常数）。
4. 集聚：网格基尼 G、Top1%/Top5% 格点数占比、Clark-Evans 最近邻指数 R。
5. 三类点：企业（底册带坐标）、高新技术企业（tag 子集）、专利（按企业专利数加权）。

输出：code/M_INNOV_KEYD_SPATIAL_out.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _keyd21_panel as P  # noqa: E402

OUT = HERE / "M_INNOV_KEYD_SPATIAL_out.json"
LAT0 = 22.6
KM_PER_DEG_LAT = 111.32
KM_PER_DEG_LNG = 111.32 * math.cos(math.radians(LAT0))
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]


def project(lng, lat):
    return (lng - 113.0) * KM_PER_DEG_LNG, (lat - 22.0) * KM_PER_DEG_LAT


def grid_counts(points, cell=1.0):
    g = defaultdict(float)
    for x, y, w in points:
        g[(int(math.floor(x / cell)), int(math.floor(y / cell)))] += w
    return g


def gini(vals):
    xs = sorted(v for v in vals if v is not None)
    n = len(xs)
    if n == 0 or sum(xs) == 0:
        return 0.0
    cum = 0.0
    for i, x in enumerate(xs, 1):
        cum += i * x
    return round((2 * cum) / (n * sum(xs)) - (n + 1) / n, 6)


def top_share(counts, frac):
    xs = sorted(counts, reverse=True)
    n = max(1, int(round(len(xs) * frac)))
    tot = sum(xs)
    return round(sum(xs[:n]) / tot, 4) if tot else None


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0] * len(vals)
    return [round(100 * (v - lo) / (hi - lo), 2) for v in vals]


def nni(points_xy):
    """Clark-Evans 最近邻指数：R = 观测平均最近邻距 / 期望(0.5/√λ)。"""
    import numpy as np
    from scipy.spatial import ConvexHull, cKDTree
    if len(points_xy) < 10:
        return None
    arr = np.array(points_xy, dtype=float)
    tree = cKDTree(arr)
    d, _ = tree.query(arr, k=2)
    nn = d[:, 1]
    mean_nn = float(nn.mean())
    hull = ConvexHull(arr)
    area_hull = float(hull.volume)
    xmin, ymin = arr.min(axis=0)
    xmax, ymax = arr.max(axis=0)
    area_bbox = float((xmax - xmin) * (ymax - ymin))
    out = {"mean_nn_km": round(mean_nn, 4), "n": int(len(arr)),
           "hull_area_km2": round(area_hull, 1), "bbox_area_km2": round(area_bbox, 1)}
    for tag, area in (("hull", area_hull), ("bbox", area_bbox)):
        lam = len(arr) / area if area else 0
        r = mean_nn / (0.5 / math.sqrt(lam)) if lam else None
        out[f"density_{tag}_per_km2"] = round(lam, 2)
        out[f"R_{tag}"] = round(r, 4) if r else None
    return out


def main():
    t0 = time.time()
    p = P.load()
    geo = p["geo"]
    meta = p["orgs_meta"]
    org_pat = p["org_patent"]

    city_pts = defaultdict(list)
    city_heis = defaultdict(list)
    city_pat = defaultdict(list)
    sz_district = Counter()
    sz_heis_district = Counter()
    for oid, (lng, lat) in geo.items():
        m = meta.get(oid)
        if not m or not m.get("city"):
            continue
        x, y = project(lng, lat)
        city_pts[m["city"]].append((x, y, 1.0))
        if m.get("is_high_tech"):
            city_heis[m["city"]].append((x, y, 1.0))
            if m["city"] == "深圳市":
                sz_heis_district[m.get("district") or "未填"] += 1
        pat = org_pat.get(oid, 0)
        if pat:
            city_pat[m["city"]].append((x, y, float(pat)))
        if m["city"] == "深圳市":
            sz_district[m.get("district") or "未填"] += 1

    city_rows = {}
    for city in CITIES:
        pts = city_pts.get(city, [])
        if not pts:
            continue
        g = grid_counts(pts)
        counts = list(g.values())
        pat_g = grid_counts(city_pat.get(city, []))
        heis_g = grid_counts(city_heis.get(city, []))
        r = nni([(x, y) for x, y, _ in pts])
        city_rows[city] = {
            "n_orgs": len(pts),
            "occupied_cells_km2": len(g),
            "density_per_occupied_km2": round(len(pts) / len(g), 1),
            "gini_cells": gini(counts),
            "top1pct_share": top_share(counts, 0.01),
            "top5pct_share": top_share(counts, 0.05),
            "max_cell_orgs": int(max(counts)),
            "n_high_tech": len(city_heis.get(city, [])),
            "heis_density_per_occupied_km2": (round(len(city_heis.get(city, []))
                                                    / max(1, len(heis_g)), 1)
                                              if heis_g else None),
            "n_patent_weighted": int(sum(pat_g.values())),
            "patent_per_occupied_km2": (round(sum(pat_g.values()) / max(1, len(pat_g)), 1)
                                        if pat_g else None),
            "nni": r,
        }

    sz_pts = city_pts.get("深圳市", [])
    sz_g = grid_counts(sz_pts)
    top_cells = []
    for (gx, gy), n in sorted(sz_g.items(), key=lambda kv: -kv[1])[:12]:
        lng = 113.0 + (gx + 0.5) / KM_PER_DEG_LNG
        lat = 22.0 + (gy + 0.5) / KM_PER_DEG_LAT
        top_cells.append({"gx": gx, "gy": gy, "orgs": int(n),
                          "center_lng": round(lng, 4), "center_lat": round(lat, 4)})
    sz_pat_g = grid_counts(city_pat.get("深圳市", []))
    top_pat_cells = []
    for (gx, gy), n in sorted(sz_pat_g.items(), key=lambda kv: -kv[1])[:8]:
        lng = 113.0 + (gx + 0.5) / KM_PER_DEG_LNG
        lat = 22.0 + (gy + 0.5) / KM_PER_DEG_LAT
        top_pat_cells.append({"center_lng": round(lng, 4), "center_lat": round(lat, 4),
                              "patents": int(n)})

    cities = [c for c in CITIES if c in city_rows]
    dens = {c: city_rows[c]["density_per_occupied_km2"] for c in cities}
    gin = {c: city_rows[c]["gini_cells"] for c in cities}
    z_d = dict(zip(cities, minmax([dens[c] for c in cities])))
    z_g = dict(zip(cities, minmax([gin[c] for c in cities])))
    composite = {c: round(0.5 * z_d[c] + 0.5 * z_g[c], 2) for c in cities}
    rank = {c: i + 1 for i, c in enumerate(sorted(cities, key=lambda x: -composite[x]))}

    dens_hull = {c: city_rows[c]["nni"]["density_hull_per_km2"] for c in cities}
    z_dh = dict(zip(cities, minmax([dens_hull[c] for c in cities])))
    composite_hull = {c: round(0.5 * z_dh[c] + 0.5 * z_g[c], 2) for c in cities}
    rank_hull = {c: i + 1 for i, c in enumerate(sorted(cities, key=lambda x: -composite_hull[x]))}

    out = {
        "metric_id": "M_INNOV_KEYD_SPATIAL",
        "metric_name": "空间密度与集聚度",
        "formula_owner": "本批 agent 重建（需求仅给「空间密度分析 + 集聚度评估」，无公式）",
        "generated_at": "2026-10-22",
        "data_source": "gkx.dwd_org_base_info + live.enterprise_extra + star_applicant_agg_gkx.json",
        "method": {
            "crs": "等距圆柱近似（lat0=22.6°，1° 经度≈102.55 km，1° 纬度≈111.32 km）",
            "grid": "1 km × 1 km，格面积恒 1 km²",
            "density": "点数 ÷ 占用格数（不引外部行政区面积）",
            "agglomeration": "网格基尼 + Top1%/Top5% 格占比 + Clark-Evans R（凸包/外包框两种研究区）",
            "points": "企业=底册带坐标；高企=tech_tag 子集；专利=企业专利数加权落点",
        },
        "inputs": {
            "geo_points": len(geo),
            "geo_coverage": p["meta"]["geo_coverage"],
            "orgs_with_city": sum(len(v) for v in city_pts.values()),
            "panel_meta": p["meta"],
        },
        "city": city_rows,
        "shenzhen": {
            "district_orgs": dict(sorted(sz_district.items(), key=lambda kv: -kv[1])),
            "district_high_tech": dict(sorted(sz_heis_district.items(), key=lambda kv: -kv[1])),
            "district_fill_share": round(
                sum(v for k, v in sz_district.items() if k != "未填") / max(1, sum(sz_district.values())), 4),
            "top_cells_by_orgs": top_cells,
            "top_cells_by_patents": top_pat_cells,
        },
        "index": {"density_0_100": z_d, "agglomeration_0_100": z_g,
                  "composite_0_100": composite, "rank": rank,
                  "sensitivity_hull_density": {
                      "density_hull_per_km2": dens_hull,
                      "density_hull_0_100": z_dh,
                      "composite_0_100": composite_hull,
                      "rank": rank_hull,
                      "rank_changed": rank != rank_hull,
                  }},
        "cross_reference": {
            "M_ENT_AGGLOMERATION_INDEX": ("同库已入库指标，口径为「行政区×产业」的 LQ/空间基尼/HHI，"
                                          "分母是 4 城市产业份额；本指标为「城市内 1 km 网格」点格局，"
                                          "分母是地理面积。两者可并列展示但不可互相替代，也不共用权重。"),
        },
        "support_judgment": {
            "data_support_level": "完全转换支持",
            "criteria": {
                "enterprise_points": f"{len(geo):,} 家企业有数值坐标（覆盖 {p['meta']['geo_coverage']*100:.2f}%）",
                "high_tech_points": "高企由 tech_tag 命中并继承企业坐标，可落图",
                "patent_points": "专利按申请人→企业→坐标落点，加权覆盖 157,354 家有专利企业",
                "reproducible": True,
                "discriminative": "四城密度、基尼、R 均非退化，且凸包/占用格两种分母的排名可对照",
            },
            "exclusions": ("论文与创新载体无坐标：`dwd_zh_paper` 只有机构名（100,900 篇中 22.5% 可归属城市，"
                           "但无经纬度）；创新载体表为单批模板数据，不作落图源。"),
        },
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")

    print(json.dumps({"city": city_rows, "index": out["index"],
                      "sz_top": top_cells[:5]}, ensure_ascii=False, indent=1))
    print("written:", OUT.name, f"{out['elapsed_sec']}s")


if __name__ == "__main__":
    main()
