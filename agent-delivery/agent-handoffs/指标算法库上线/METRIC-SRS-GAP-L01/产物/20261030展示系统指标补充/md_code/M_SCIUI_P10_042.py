#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_042 孵化载体地理分布全景图 —— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py（dev/gkx/jiuxin 三源词族+正读数）
本脚本职责：①引用共享快照断言 ②dev 全景代理面补充实测（跨 type×district 联动统计） ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

import pymysql  # noqa: E402

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_laneC_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_042_out.json"

DEV = dict(
    host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
    charset="utf8mb4", connect_timeout=15, read_timeout=120, autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    carrier_rows = dev["dev_dim_carrier_rows"]
    carrier_coords = dev["dev_dim_carrier_rows_with_coords"]
    assert carrier_rows == 28, "dim.carrier 行数应为 28（共享快照）"
    assert carrier_coords == carrier_rows, "dim.carrier 坐标覆盖应全量"

    # 全景代理面补充实测：type×city 交叉（联动统计链验证）+ 覆盖城市数（薄壳独立查询）
    conn = pymysql.connect(**DEV)
    cur = conn.cursor()
    cur.execute(
        "SELECT carrier_type, admin_code, COUNT(*) AS c FROM gkxlumenx_dim.carrier "
        "GROUP BY carrier_type, admin_code ORDER BY c DESC, carrier_type")
    type_city_rows = cur.fetchall()
    cur.execute("SELECT COUNT(DISTINCT admin_code) AS c FROM gkxlumenx_dim.carrier")
    city_cnt = cur.fetchone()["c"]
    cur.execute(
        "SELECT admin_code, COUNT(*) AS c FROM gkxlumenx_dim.carrier "
        "GROUP BY admin_code ORDER BY c DESC")
    city_dist = {r["admin_code"]: r["c"] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dim.carrier_org_rel")
    rel_rows = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_ads.carrier_index")
    idx_rows = cur.fetchone()["c"]
    conn.close()

    type_city_map: dict = {}
    for r in type_city_rows:
        type_city_map.setdefault(r["carrier_type"], {})[r["admin_code"]] = r["c"]

    out = {
        "metric_id": "M_SCIUI_P10_042",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:696-781",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:586-590",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:786-820",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:1489-1507",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「孵化载体地理分布全景图」指标名；上位功能叶 1.1.1.1.4.6.5.1 创新载体与孵化载体分布全景可视化（SRS 创新载体孵化载体.md:21 bid_desc「支持基于地理信息全景的创新载体分布、孵化载体分布及相关详细信息的介绍与展示」；:27「按城市、园区、楼宇分层显示。全景模式让管理者快速把握创新资源格局」）为需求功能面上位覆盖。本件与 P10_029 同族（P10_029=地图卡单件，本件=分布全景整页骨架：三重筛选+地图+列表+分类统计+势能联动）。",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:696-781 renderPanorama 三栏全景（左=载体筛选 :700-723 三重筛选+热力开关；中=:766-777 载体地理分布地图（P10_029 同卡）；右=媒体/资讯卡）；页顶 KpiTile 行 :1489-1507（监测载体总数 M_IC_CARRIER_TOTAL 等 5 项）",
            "ui_filter_chain": ":704 载体类别 Radio.Group（联动地图/列表/统计）→ :708-711 所在区域 Select（9 区）→ :713-716 地图层级 城市/园区/楼宇 Radio → :718 热力开关 Checkbox → filteredCarriers 驱动 :725 载体列表/:766 地图/:786-820 分类别统计卡",
            "ui_stats_chain": ":586-590 filteredStats（count/districts 覆盖区数/ents 入驻企业合计）→ :807-810 筛选结果统计三读数；:786-820 分类别筛选与统计分析卡（趋势+构成 donut+统计）",
            "ui_mock": "mockData.js:40-43 carriers 22 家深圳载体（district 9 区/type 4 类：孵化器 8/众创空间 5/加速器 5/产业园区 4），每条含 lat/lng/building/enterpriseCount/potentialScore——ui_demo_fallback 演示值",
            "ui_level_note": "MAP_LEVELS 城市/园区/楼宇三档层级切换：dim.carrier 仅 admin_code 市级，楼宇层级无承载",
            "dev_dim_carrier_rows": carrier_rows,
            "dev_dim_carrier_rows_with_coords": carrier_coords,
            "dev_dim_carrier_type_dist": dev["dev_dim_carrier_type_dist"],
            "dev_dim_carrier_city_count": city_cnt,
            "dev_dim_carrier_city_dist_top": dict(list(city_dist.items())[:5]),
            "dev_dim_carrier_type_city_cross": type_city_map,
            "dev_dim_carrier_source_note": "dim.carrier.source=v1_approx（近似坐标，admin_code 到市级）",
            "dev_dim_carrier_org_rel_rows": rel_rows,
            "dev_ads_carrier_index_rows": idx_rows,
            "dev_dwd_enterprise_innovation_carrier_rows": dev["dev_dwd_enterprise_innovation_carrier_rows"],
            "dev_carrier_family_tables": dev["dev_carrier_family_table_hits"],
            "gkx_table_count": snap["gkx"]["gkx_table_count"],
            "gkx_carrier_family": snap["gkx"]["gkx_carrier_family"],
            "jiuxin_table_count_live": snap["jiuxin"]["jiuxin_table_count_live"],
            "jiuxin_carrier_family": snap["jiuxin"]["jiuxin_carrier_family"],
        },
        "derived": [
            {
                "name": "dev_dim_carrier_type_city_linkage_demo",
                "value": {t: sum(c.values()) for t, c in type_city_map.items()},
                "note": "type×city 交叉计数（联动统计链验证：类别筛选→城市聚合可跑通）；各 type 计数与 dev_dim_carrier_type_dist 同基（B3：同表 gkxlumenx_dim.carrier）。",
            },
            {
                "name": "dev_dim_carrier_top_city_share_pct",
                "value": round(max(city_dist.values()) / carrier_rows * 100, 4),
                "numerator": max(city_dist.values()),
                "denominator": carrier_rows,
                "note": "分子=载体数最多城市的行数，分母=dim.carrier 全表行数，同表同源（B3 同基）；表示代理面的城市集中度，非深圳市全景口径。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）深圳市孵化载体全景台账（载体+类别+区级坐标+楼宇地址+势能分）",
                "source": "dev",
                "sql": "information_schema.columns 表名+列名词族扫描（carrier|incub|park + lng/lat），快照 _snapshots/_shared_s308_laneC_out.json dev.dev_carrier_family_table_hits",
                "hits": ["gkxlumenx_dim.carrier", "gkxlumenx_dim.carrier_org_rel", "gkxlumenx_dwd.enterprise_innovation_carrier", "gkxlumenx_ads.carrier_index"],
                "note": "dim.carrier 28 行全国样本（type×city 交叉见 facts）；dwd.enterprise_innovation_carrier 0 行空壳；ads.carrier_index 0 行载体指数面；无势能分/楼宇字段",
            },
            {
                "probe": "gkx 280 表载体/孵化/园区词族（含全景统计面）",
                "source": "gkx",
                "sql": "information_schema.tables table_name REGEXP carrier|incub|park（快照 gkx.gkx_carrier_family）",
                "hits": 0,
            },
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）载体/孵化/园区词族",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名词族匹配（快照 jiuxin.jiuxin_carrier_family）",
                "hits": 0,
            },
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：全景图是「三重筛选→地图+列表联动→分类统计+势能热力」整页骨架，其核心依赖与 P10_029 同源（载体坐标台账）。dev.gkxlumenx_dim.carrier 28 行全量坐标可验证「类别筛选→城市聚合→落图」联动链（type×city 交叉实测跑通），但为全国 10 城样本（深圳仅 3 行、无区级/楼宇粒度、无势能分列），深圳市孵化载体全景台账三源零承载（dwd.enterprise_innovation_carrier 0 行空壳、ads.carrier_index 0 行、gkx/jiuxin 词族 0 命中）→ 结构面代理可用，总体面+层级面+势能面缺失，判部分支持。",
            "与 P10_029 的分件边界：P10_029=中栏地图卡单件（地理分布地图深圳市）；本件=分布全景整页骨架（renderPanorama 三栏+分类别统计卡+KPI 行），复用同一坐标台账依赖，探针同源共享快照，独立薄壳落盘。",
            "楼宇层级（MAP_LEVELS 第三档）与势能热力层（按 potentialScore 渲染）均无库内承载：dim.carrier 无 building/potential 列，势能分仅 mock。",
            "UI mock 22 家深圳载体全景（9 区×4 类）为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s308_laneC.py + 快照 _snapshots/_shared_s308_laneC_out.json；本脚本仅做断言+type×city 联动补充实测+判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2018-2026"],
        "base_years_note": "分布全景为存量截面读数（无时序维度），不适用基期年份；dim.carrier 无年度列，载体认定批次年份未入库。趋势卡（载体数量趋势 2022-2026H1）为 mock 演示序列。若接入真实台账需以台账认定年度为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["22", "28", "3", "10", "9", "6", "5", "4", "542", "280", "218", "v1_approx", "440300", "0"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 部分支持 | dim.carrier:", carrier_rows, "| cities:", city_cnt, "| type_city:", type_city_map)


if __name__ == "__main__":
    main()
