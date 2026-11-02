#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_043 综合能力评分（机构能力画像）—— 薄壳校验脚本（负结论件）。

UI：InstrumentSharingPage.jsx:1073 机构能力画像卡「综合能力评分」雷达图
（metric=activeAgency.score 分）+ :1067 机构汇总「综合能力分」+ :1034 机构表
score 列。score = Math.round(Σ instrument.score / instrumentCount)——机构级
评分=成员仪器 score 均值，mock 自设分制（94/91/87/76）。
探针：dev 评分面 enterprise_score（14 列含 score_total）0 行、svc_tech_power_score
（含 service_type 维）0 行、carrier_index 0 行；gkx score 词族 0 表；久新评分族
（talent_capability/technology_potential）为人才/技术维度——机构·仪器服务域评分
三源零承载。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_043_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    es = dev["gkxlumenx_ads.enterprise_score"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert es["rows"] == 0
    assert "score_total" in es["columns"]

    out = {
        "metric_id": "M_SCIUI_INCUB_043",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:1073",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:955",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/components/InstrumentSharingPage.jsx:555",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「综合能力评分」指标名三份说明书未出现；语义锚 SRS 大型科学仪器共享.md 序号 535「点击机构节点，系统弹窗显示机构优势资源、历史服务评价、共享能力评分等多维数据」（机构弹窗多维数据分句）——功能要求在、评分口径未给。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingPage.jsx:1073 机构能力画像「综合能力评分」雷达图卡（SoftChartFrame metric=activeAgency.score unit=分 badge=多维评估）+ :1067 机构汇总行「综合能力分」",
            "ui_radar_dims": "AGENCY_RADAR_DIMS（:947-952）五维：利用率/服务质量/资源覆盖/响应能力/创新活跃度，max=100",
            "ui_radar_fn": "buildAgencyRadarOption（:955-989）：服务质量维=score×0.9、资源覆盖=instrumentCount×4（cap 100）、响应=serviceTotal/12、创新=reservationTotal/8——mock 评分五维合成式",
            "ui_aggregation": "机构 score = Math.round(Σ instrument.score / instrumentCount)（:555 buildAgencyCapabilityRows——成员仪器 mock score 94/91/87/76 的均值）",
            "ui_mock_note": "mock instruments[].score 4 值 94/91/87/76（分制 0-100）——ui_demo_fallback 演示值，不参与支持度结论；评分模型（权重/维度）无任何定义",
            "dev_table_total": dev["table_total"],
            "dev_enterprise_score": {"columns": es["columns"], "rows": es["rows"]},
            "dev_svc_tech_power_score": {"note": "word_score 命中 gkxlumenx_ads.svc_tech_power_score（企业技术实力评分域，含 service_type 维度列名依词族命中登记）——本指标为机构·仪器服务域评分，语义不匹配", "rows": None},
            "dev_carrier_index_rows": dev["gkxlumenx_ads.carrier_index"]["rows"],
            "gkx_table_count": gkx["table_count"],
            "gkx_score_word_tables": gkx["word_score"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_score_note": "久新评分族（ads_talent_capability_assessment 99,996 行/ads_talent_potential_result 100,000 行，INCUB_027 已证）为人才维度；ads_technology_potential_* 为技术维度——无机构·仪器服务域评分面（INCUB_027 检索留证，本批复用结论）",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "agency_comprehensive_capability_score",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "机构综合能力评分 = 多维加权分（UI 五维：利用率/服务质量/资源覆盖/响应/创新）。评分事实面（机构×分值×维度）与模型权重三源零承载 → 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev 评分结果面（score/rating/evaluat/assess 词族 542 表）",
             "source": "dev", "sql": "information_schema 表名扫描 + 行数实证（_shared_s308_lane_a.py 快照）",
             "hits": 7,
             "hit_detail": "enterprise_score（14 列含 score_total/score_level/model_version）0 行；carrier_index 0 行；svc_tech_power_score 为企业技术实力域；其余为政策评估/操作状态字典/BI 模板语义——机构·仪器服务域评分全空壳"},
            {"probe": "gkx score 词族（280 表）",
             "source": "gkx", "sql": "information_schema 表名扫描（快照）",
             "hits": 0, "note": "gkx word_score=[]——要素库无评分面"},
            {"probe": "久新 机构·仪器服务域评分（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 评分族语义核（INCUB_027 留证复用）",
             "hits": 0,
             "hit_detail": "评分族全为人才（talent_capability 99,996 行/talent_potential 100,000 行）与技术（technology_potential）维度——机构·仪器服务域 0 命中"},
            {"probe": "评分模型定义（五维/权重/分制）",
             "source": "doc", "sql": "三份说明书 + 主需求 rg 综合能力评分|共享能力评分",
             "hits": 1,
             "hit_detail": "SRS 序号 535 机构弹窗多维数据分句（共享能力评分字样）——功能要求在，无评分公式/权重/分制定义"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：机构综合能力评分需①评分事实面（机构×分值）②评分模型（维度/权重）两层。三源评分面逐一排除：dev enterprise_score/svc_tech_power_score/carrier_index 三结构承载全 0 行；gkx 0 表；久新评分族为人才/技术维度。模型层三说明书仅有功能分句无定义——两层皆缺。",
            "UI 侧评分是 mock 自设分制：机构 score=成员仪器 mock score 均值，雷达五维由 score/instrumentCount/serviceTotal/reservationTotal 四个 mock 字段线性合成（系数 0.9/4/12/8 无依据）——演示态自证。",
            "同族关系：INCUB_047（仪器共享能力评分，组织级 score 列）同 UI 页同评分域不同挂载位；P10_041（共享能力评分）路 C 同族——三件独立留证。",
            "语义锚 SRS 序号 535「共享能力评分等多维数据」证明需求意图在（机构节点弹窗）——若接入深圳共享平台机构评价数据可升档。",
            "升档路径：共享平台机构评价结果接入（机构×评分×维度面落库）→ 完全转换支持；平台侧评分接口直连 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "综合能力评分为当期截面读数（评分快照）；三源无评分面无历史序列；mock 亦无年度序列。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted(
            [             "94", "91", "87", "76", "100", "5", "0.9", "4", "12", "8", "542", "280", "218",
             "99996", "99,996", "100000", "100,000", "14", "0"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 机构评分面三源空壳/0 命中")


if __name__ == "__main__":
    main()
