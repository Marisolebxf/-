#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_059 三坐标测量机保有量（台套）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py（dev/gkx/jiuxin 三源词族+正读数）
本脚本职责：①引用共享快照断言 ②gkx dwd_medical_device CMM 词族补充实测（语义错位定量） ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

from _gkxdb import gkx  # noqa: E402

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_laneC_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_059_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    gkx_snap = snap["gkx"]
    med_rows = gkx_snap["gkx_dwd_medical_device_rows"]
    measure_like = gkx_snap["gkx_medical_device_measure_like_rows"]
    measure_samples = gkx_snap["gkx_medical_device_measure_like_samples"]
    assert med_rows == 10000, "dwd_medical_device 行数应为 10000（共享快照）"

    # CMM 词族补充实测（薄壳独立查询）：坐标/COORDINAT/CMM 三 pattern
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_medical_device WHERE device_name LIKE '%坐标%'")
    cmm_zh = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_medical_device WHERE UPPER(device_name) LIKE '%COORDINAT%'")
    cmm_en = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_medical_device WHERE UPPER(device_name) LIKE '%CMM%'")
    cmm_abbr = cur.fetchone()[0]
    # 语义错位样本：device_type 顶层分布 top5（证明是医疗器械注册库）
    cur.execute(
        "SELECT device_type, COUNT(*) AS c FROM gkx.dwd_medical_device "
        "GROUP BY device_type ORDER BY c DESC LIMIT 5")
    type_top5 = {r[0]: r[1] for r in cur.fetchall()}
    cur.close()

    out = {
        "metric_id": "M_SCIUI_P10_059",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:131",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:507",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:613-615",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:237-240",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「三坐标测量机保有量」指标名；上位功能叶 1.1.1.1.4.6.6.2 大型科学仪器信息可视化盘点/仪器类别精准筛选（SRS 大型科学仪器共享.md:59「用户可按功能类别（如医药、电子、材料、化工）快速筛选仪器清单……统计不同类别仪器的总量和使用状态」）为需求功能面上位覆盖；三坐标测量机作为「机械」类别下的具体机种，其保有量=类别台账分类计数的实例。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingNewPage.jsx:507 仪器盘点左栏类别复选框「{categoryCounts[c] || 0} 台套」（机械类 3 台套，含 INS-0023 三坐标测量机 GLOBAL S 07.10.07）；:613-615「类别总量与共享状态统计」CHART_METRICS.categoryStatus（M_IS_CATEGORY_STATUS）",
            "ui_instrument_row": "mockData.js:131 INS-0023 三坐标测量机（category=机械，Hexagon 瑞典 GLOBAL S 07.10.07，深圳市计量质量检测研究院几何量所，220 元/小时，2020-03-22 购置，160 万元原值）——ui_demo_fallback 演示值",
            "ui_lineage": "mockData.js:237-240 categoryStatus lineage：按设备分类统计入网仪器台套数及共享状态分布；源表 ads_is_instrument_registry；T+1",
            "ui_mock": "mock 32 台套/12 类别中「机械」3 台套（INS-0022 五轴数控加工中心/INS-0023 三坐标测量机/INS-0024 激光干涉仪）——ui_demo_fallback 演示值",
            "gkx_dwd_medical_device_rows": med_rows,
            "gkx_medical_device_measure_like_rows": measure_like,
            "gkx_medical_device_measure_like_samples": measure_samples,
            "gkx_medical_device_cmm_zh_rows": cmm_zh,
            "gkx_medical_device_cmm_en_rows": cmm_en,
            "gkx_medical_device_cmm_abbr_rows": cmm_abbr,
            "gkx_medical_device_type_top5": type_top5,
            "gkx_semantic_mismatch_note": "dwd_medical_device 是 FDA 医疗器械注册库（device_type 顶层为 Orthopaedic prostheses 等临床品类），非共享仪器入网台账——语义错位载体（派单预期披露项）",
            "dev_instrument_family_hits": snap["dev"]["dev_instrument_family_hits"],
            "dev_ads_is_hits": snap["dev"]["dev_ads_is_hits"],
            "gkx_table_count": gkx_snap["gkx_table_count"],
            "gkx_instrument_family": gkx_snap["gkx_instrument_family"],
            "jiuxin_table_count_live": snap["jiuxin"]["jiuxin_table_count_live"],
            "jiuxin_instrument_family": snap["jiuxin"]["jiuxin_instrument_family"],
        },
        "derived": [
            {
                "name": "cmm_holdings_count",
                "value": None,
                "note": "负结论登记：三坐标测量机保有量需「入网仪器台账（名称+类别+归属机构）」按机种分类计数；指定源表 ads_is_instrument_registry 三源 0 实存；gkx dwd_medical_device 10,000 行为 FDA 医疗器械注册库（device_type 临床品类），CMM 词族实测 坐标/COORDINAT/CMM 三 pattern 均 0 命中——即使 MEASUR 词族 2 行（MEASURING SCREWDRIVER 等）也是手术器械语义。语义错位禁伪算，null 登记。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）入网仪器台账（ads_is_instrument_registry 或同义）",
                "source": "dev",
                "sql": "information_schema 表名词族扫描 ads_is* + instrument（快照 dev.dev_ads_is_hits / dev.dev_instrument_family_hits）",
                "hits": 0,
                "note": "ads_is 族 0 实存；instrument 词族命中 4 表均为异域列（chain_hotspot.news_freq_score 等）",
            },
            {
                "probe": "gkx 280 表共享仪器/入网台账词族",
                "source": "gkx",
                "sql": "information_schema.tables table_name REGEXP instrument|share_rate（快照 gkx.gkx_instrument_family）",
                "hits": 0,
            },
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）仪器/入网词族",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名词族匹配（快照 jiuxin.jiuxin_instrument_family）",
                "hits": 0,
            },
            {
                "probe": "gkx dwd_medical_device CMM 机种计数（候选代理面语义核验）",
                "source": "gkx",
                "sql": "SELECT COUNT(*) WHERE device_name LIKE '%坐标%' / UPPER LIKE '%COORDINAT%' / UPPER LIKE '%CMM%'（薄壳独立实测）",
                "hits": 0,
                "note": "三 pattern 均 0 命中；device_type top5 全为临床品类——注册库≠共享仪器台账，语义错位披露",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：三坐标测量机保有量 = 入网仪器台账按机种（三坐标测量机/CMM）分类计数。指定源表 ads_is_instrument_registry 三源 0 实存（dev ads_is=0/gkx instrument 族=0/jiuxin instrument 族=0）；唯一 10,000 行设备面 gkx dwd_medical_device 是 FDA 医疗器械注册库——CMM 词族（坐标/COORDINAT/CMM）实测 0 命中，device_type 顶层为 Orthopaedic prostheses 等临床品类，与共享仪器台账语义错位（派单预期「语义错位披露」落实为四 pattern 零命中+品类分布实证）。分类计数无分母无分子，判完全不支持。",
            "与 P10_037/P10_040/P10_041/P10_055 同族同因：共享平台 ADS 表族（ads_is_*）整体未接入是路C仪器域结构性主缺口，本件为该族「机种粒度下钻件」。",
            "UI mock 32 台套/机械 3 台套为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s308_laneC.py + 快照 _snapshots/_shared_s308_laneC_out.json；本脚本仅做断言+CMM 词族补充实测+判档落盘。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2018-2026"],
        "base_years_note": "保有量为存量截面读数（无时序维度），不适用基期年份；dwd_medical_device 无入网年度列（FDA 注册语义）。若接入真实台账需以入网登记年度为基期，UI 购置日期字段（purchaseDate 2020-03-22 演示值）提示口径应为购置/入网年。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["32", "3", "12", "10000", "2", "0", "542", "280", "218", "INS-0023", "2020-03-22", "160"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | med_rows:", med_rows, "| cmm zh/en/abbr:", cmm_zh, cmm_en, cmm_abbr, "| type_top5:", type_top5)


if __name__ == "__main__":
    main()
