#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_029 载体地理分布地图（深圳市）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py（dev/gkx/jiuxin 三源词族+正读数）
本脚本职责：①引用共享快照断言 ②dev dim.carrier 深圳行数补充实测 ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql  # noqa: E402

SHARED = "_snapshots/_shared_s308_laneC_out.json"
OUT = "M_SCIUI_P10_029_out.json"

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

    # 深圳行数与类型分布补充实测（薄壳独立查询，非跨件缓存）
    conn = pymysql.connect(**DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dim.carrier WHERE admin_code='440300'")
    sz_rows = cur.fetchone()["c"]
    cur.execute(
        "SELECT carrier_type, COUNT(*) AS c FROM gkxlumenx_dim.carrier "
        "WHERE admin_code='440300' GROUP BY carrier_type ORDER BY c DESC")
    sz_types = {r["carrier_type"]: r["c"] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) AS c FROM gkxlumenx_dwd.enterprise_innovation_carrier")
    ent_innov_rows = cur.fetchone()["c"]
    conn.close()

    out = {
        "metric_id": "M_SCIUI_P10_029",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:766",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:696-764",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:40-43",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「载体地理分布地图（深圳市）」指标名；上位功能叶 1.1.1.1.4.6.5.1.1 地理分布地图展示（SRS 创新载体孵化载体.md:10-14）要求「交互地图选择区域，高亮创新载体及孵化载体的空间分布密度，按城市、园区、楼宇分层显示」，为需求功能面上位覆盖。",
        },
        "facts": {
            "ui_mount": "IncubationCarrierNewPage.jsx:766 SectionCard title=载体地理分布地图（深圳市）→ :767-775 CarrierMap（carriers/activeId/level/showHeat）",
            "ui_filter_chain": "IncubationCarrierNewPage.jsx:696-723 renderPanorama 左栏三重筛选（载体类别/所在区域/地图层级 城市-园区-楼宇 + 热力开关）",
            "ui_mock": "mockData.js:40-43 carriers 数组 22 家深圳载体（C01 深圳湾科技生态园…），district 覆盖 9 区（南山 6/福田 3/宝安 3/龙岗 3/龙华 2/坪山 2/罗湖 1/光明 1/盐田 1），type 4 类（孵化器 8/众创空间 5/加速器 5/产业园区 4）——ui_demo_fallback 演示值",
            "dev_dim_carrier_rows": carrier_rows,
            "dev_dim_carrier_rows_with_coords": carrier_coords,
            "dev_dim_carrier_type_dist": dev["dev_dim_carrier_type_dist"],
            "dev_dim_carrier_sz_rows": sz_rows,
            "dev_dim_carrier_sz_type_dist": sz_types,
            "dev_dim_carrier_source_note": "dim.carrier.source=v1_approx（近似坐标，admin_code 到市级）",
            "dev_dwd_enterprise_innovation_carrier_rows": ent_innov_rows,
            "dev_carrier_family_tables": dev["dev_carrier_family_table_hits"],
            "gkx_table_count": snap["gkx"]["gkx_table_count"],
            "jiuxin_table_count_live": snap["jiuxin"]["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "dev_dim_carrier_sz_share_pct",
                "value": round(sz_rows / carrier_rows * 100, 4),
                "numerator": sz_rows,
                "denominator": carrier_rows,
                "note": "分子=dim.carrier 深圳 admin_code=440300 行数，分母=dim.carrier 全表行数，同表同源（B3 同基）；表示深圳载体在开发库载体维表中的占比，非 UI 口径的深圳市全域载体分布。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）深圳市孵化载体台账（载体名+类别+深圳区级坐标/楼宇地址）",
                "source": "dev",
                "sql": "information_schema.columns 表名+列名词族扫描（carrier|incub|park + lng/lat），快照 _snapshots/_shared_s308_laneC_out.json dev.*",
                "hits": ["gkxlumenx_dim.carrier", "gkxlumenx_dim.carrier_org_rel", "gkxlumenx_dwd.enterprise_innovation_carrier", "gkxlumenx_ads.carrier_index"],
                "note": "dim.carrier 28 行全国样本（深圳仅 3 行），dwd.enterprise_innovation_carrier 0 行空壳，ads.carrier_index 为载体指数非坐标台账",
            },
            {
                "probe": "gkx 280 表孵化载体/园区/坐标词族",
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
            "判档理由：地理分布计算链（坐标装载→按区聚合→地图落点）三源可跑通，dev.gkxlumenx_dim.carrier 28 行全量带 lng/lat 坐标（派单预期「无坐标列需证」实测为有坐标列，0 空值）；但总体错位——UI 口径是深圳市 22 家孵化载体（孵化器/加速器/众创空间/产业园区）按 9 区+园区+楼宇分层，dim.carrier 是全国 10 城 university/research/incubator 样本（深圳仅 3 行，无区级/楼宇粒度，source=v1_approx 近似坐标），深圳市孵化载体台账三源零承载 → 结构面可用作骨架代理，总体面缺失。",
            "楼宇级下钻（MAP_LEVELS 城市/园区/楼宇三档）需要 building 级地址字段，dim.carrier 仅 admin_code 市级——层级维度缺失随台账缺口同源。",
            "UI mock 22 家深圳载体（district 9 区分布）为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s308_laneC.py + 快照 _snapshots/_shared_s308_laneC_out.json；本脚本仅做断言+深圳行补充实测+判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2018-2026"],
        "base_years_note": "地理分布为存量截面读数（无时序维度），不适用基期年份；dim.carrier 无年度列，载体认定批次年份未入库。若接入真实台账需以台账认定年度为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["22", "28", "3", "10", "9", "6", "542", "280", "218", "1", "2", "v1_approx", "440300"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 部分支持 | dim.carrier:", carrier_rows, "| sz:", sz_rows, "| sz_types:", sz_types)


if __name__ == "__main__":
    main()
