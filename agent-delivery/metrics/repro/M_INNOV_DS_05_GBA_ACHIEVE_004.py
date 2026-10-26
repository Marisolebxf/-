#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_05_GBA_ACHIEVE_004（湾区创新热点区域）复现与结果绑定。

口径：王惠 V1.5（同 M_INNOV_GBA_HOTSPOT）。
- 空间单元：城市/区县（行政区，非规则格网）
- 创新密度 = 2019-2024 专利件数 / 该区县机构数
- 热点判定：密度 ≥ 全区县 P70 分位
- 主类型：专利/论文/项目 三源中件数最大者

复现策略：读取 M_INNOV_GBA_HOTSPOT_out.json（已在 gkx 真源跑通 25 个区县，
未重扫专利大表），绑定结果并补充覆盖度探针。
"""
import json, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "M_INNOV_GBA_HOTSPOT_out.json")
OUT = os.path.join(HERE, "M_INNOV_DS_05_GBA_ACHIEVE_004_out.json")

PROBES = {
    "probe_note": "上批探针留存：gkx 主机 2026-10-21 10:33 起一度 TCP 超时；11:08 连接已可建立，但 dwd_org_base_info 城市聚合在 read_timeout=600 内未返回，本脚本未完成全量复测。",
    "areas_total": 25,
    "cities_with_area": ["广州市", "深圳市", "惠州市"],
    "cities_without_area": ["东莞市"],
    "gba_cities_total": 11,
    "city_coverage": "4/11（含东莞市级；港澳无区县底册）",
    "forg_hk_macau_hits": 0,
    "paper_area_key": False,
    "project_area_key": False,
    "sources_used": ["dwd_patent", "dwd_org_base_info"],
}

JUDGMENT = "部分支持"
BASIS = ("区县维密度、主类型、P70 热点标签在 25 个区县上可算并已输出（8 个热点，越秀 23.825 最高）；"
         "但 11 城中仅广州、深圳、惠州有区县字段（东莞仅市级、港澳无底册，forg 表港澳命中 0），"
         "论文与项目表无区县键、只能作专利单源，故为部分支持。")


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    rows = d.get("rows", [])
    hot = [r for r in rows if r.get("hotspot")]
    dens = [r["density"] for r in rows]
    by_city = {}
    for r in rows:
        by_city.setdefault(r["city"], []).append(r)
    out = {
        "metric_id": "M_INNOV_DS_05_GBA_ACHIEVE_004",
        "name": "湾区创新热点区域",
        "formula_owner": "王惠",
        "vendor_metric": "M_INNOV_GBA_HOTSPOT",
        "generated_at": "2026-10-21",
        "reused_from": "M_INNOV_GBA_HOTSPOT_out.json (2026-10-20)",
        "params": {"unit": "district", "window": [2019, 2024],
                   "density": "patents / orgs", "threshold": "P70"},
        "probes": {**PROBES, "areas": len(rows)},
        "compute": {
            "p70": d.get("p70"),
            "hotspot_count": len(hot),
            "density_min": min(dens), "density_max": max(dens),
            "density_mean": round(statistics.mean(dens), 3),
            "density_median": round(statistics.median(dens), 3),
            "hotspots": hot,
            "city_summary": {c: {"areas": len(v),
                                 "orgs": sum(x["orgs"] for x in v),
                                 "patents_2019_24": sum(x["patents_2019_24"] for x in v)}
                             for c, v in by_city.items()},
        },
        "samples": rows[:10],
        "support_judgment": JUDGMENT,
        "support_basis": BASIS,
        "notes": [
            "热点门槛 P70=12.329，恰好等于广州天河密度，故天河以『≥ 阈值』入选，边界值需在页面注明。",
            "密度是单位机构产出强度，不是地理面积密度；宝安区机构 25,192 家、专利 265,725 件，密度被摊薄至 10.548，未入选。",
            "主类型全部为专利：论文/项目无区县键，三源比较实际退化为单源。",
            "东莞 2024 年 GDP 与专利体量均属湾区前列，但因无 area 字段只能出市级，区县榜缺失，须披露。",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("saved", OUT, "hot", len(hot), "p70", d.get("p70"))


if __name__ == "__main__":
    main()
