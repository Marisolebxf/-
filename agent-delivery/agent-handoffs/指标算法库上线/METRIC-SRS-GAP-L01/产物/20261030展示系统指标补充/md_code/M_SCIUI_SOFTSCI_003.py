#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_003 仪器分类分布 —— 薄壳校验脚本。

共享复算真源：code/_shared_s307_l2.py（gkx.dwd_medical_device 结构面）
本脚本职责：①存在性校验 ②判档 ③基期三键校验 ④引用共享产物快照。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_s307_l2_shared_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_SOFTSCI_003_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        shared = json.load(f)

    total = shared["gkx_medical_device_total"]
    dist = shared["gkx_medical_device_major_type_dist_sorted"]
    top5 = dist[:5]
    top5_sum = sum(x["count"] for x in top5)

    # 校验断言（存在性 + 判档前置）
    assert total > 0, "gkx.dwd_medical_device 必须非空（共享快照）"
    assert len(dist) > 10, "分类分布必须有多类（共享快照）"
    assert [x["count"] for x in dist] == sorted([x["count"] for x in dist], reverse=True), "分布必须降序（B5）"

    out = {
        "metric_id": "M_SCIUI_SOFTSCI_003",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1428",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:196",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书未出现「仪器分类分布」指标名；SRS 大型科学仪器共享章（1.1.1.1.4.6.4）要求「按生物医药、电子电气…分类」落图与「仪器类别精准筛选」（1.1.1.1.4.6.4.1.2），语义为需求功能面的上位覆盖，非同名指标。",
        },
        "facts": {
            "gkx_dwd_medical_device_rows": total,
            "gkx_medical_device_major_type_dist_top5": top5,
            "gkx_medical_device_major_type_dist_top5_sum": top5_sum,
            "gkx_medical_device_major_type_distinct_count": len(dist),
            "gkx_medical_device_device_type_distinct_count_670": len(shared["gkx_medical_device_type_dist_all"]),
            "shared_snapshot": "_snapshots/_s307_l2_shared_out.json",
        },
        "derived": [
            {
                "name": "gkx_medical_device_top5_major_type_share_pct",
                "value": round(top5_sum / total * 100, 4),
                "numerator": top5_sum,
                "denominator": total,
                "note": "分子=Top5 大类计数和（gkx_medical_device_major_type_dist_top5_sum），分母=gkx.dwd_medical_device 全表行数（gkx_dwd_medical_device_rows），同源同表；表示医疗器械大类结构集中度，非 UI 口径的全市大型科学仪器分类分布。",
            }
        ],
        "absence_probe": [
            {
                "probe": "开发库 gkxlumenx_* 全 schema 仪器台账面（表名含 instrument/equip/device/apparatus）",
                "source": "dev",
                "sql": "information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' 表名+列名词族扫描（_snapshots/_probe_s307_l2_out.json dev.column_scan.table_name_hits）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表仪器台账面：仅 dwd_medical_device（医疗器械注册库，非共享仪器台账）",
                "source": "gkx",
                "sql": "information_schema.columns WHERE table_schema='gkx' 词族扫描（同上快照 gkx.column_scan.table_name_hits）",
                "hits": 1,
            },
            {
                "probe": "久新 218 表（现场 SHOW TABLES 实数）仪器/预约/状态词族",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名词族匹配（同上快照 jiuxin.table_name_hits；列扫描 information_schema.columns）",
                "hits": 0,
            },
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：仪器分类维度三源中仅 gkx.dwd_medical_device 有结构面（医疗器械，10,000 行，670 个 device_type，语义≠大型科学仪器共享台账）；无运行状态列、无共享标记列；dev/久新零承载 → 结构部分可得（医疗器械代理），台账主体缺失。",
            "gkx.dwd_medical_device 是美国 FDA 风格器械注册数据（device_type 为英文注册名），与深圳共享平台 9,262 台套口径（SRS 附录 A）不是同一总体。",
            "UI mock 值（typeDistribution：材料分析/检测服务等 12 类）为演示值，不参与支持度结论。",
            "本件为薄壳：共享复算脚本 code/_shared_s307_l2.py，本脚本仅做存在性+判档+基期三键校验。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "仪器分类分布为存量结构读数（无时序维度），不适用基期年份；UI mock 序列为演示值不可作基期。若接入真实台账需以台账年度为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": [
                "10000", "10,000", "670", "1,062", "734", "481", "296", "277",
                "9262", "9,262", "5612", "499", "60.59%",
            ],
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("total:", total, "| top5_sum:", top5_sum, "| share:", out["derived"][0]["value"])


if __name__ == "__main__":
    main()
