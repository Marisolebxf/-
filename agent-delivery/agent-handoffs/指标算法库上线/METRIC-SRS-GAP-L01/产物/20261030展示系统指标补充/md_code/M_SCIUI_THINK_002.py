#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_THINK_002 供方分析能力评分 —— 薄壳校验脚本（负结论件）。

UI：ThinkTankService.jsx:652 服务类型详情抽屉「供方分析能力」行
（值='不作为本目录，见服务类型页说明'）+:394 服务类型 Tab 说明句
（供方返回的分析能力不作为服务类型：论文分析、专利分析…七项）。
mockData.js:123 thinkTankSupplierCapabilities 七能力枚举（无分值）。
口径=智库服务平台对数据/服务供给方专业分析能力的打分——评分面+模型双缺
（S3-08 INCUB_043/047 已证同门先例；本件独立留证）。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_alpha_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_THINK_002_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["gkxlumenx_ads.enterprise_score"]["rows"] == 0
    assert gkx["word_score"] == []
    assert len(dev["word_score"]) == 7

    out = {
        "metric_id": "M_SCIUI_THINK_002",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx:652",
            "repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx:394",
            "repos/demo-ui-science/src/pages/tech-service/mockData.js:123-125",
            "repos/demo-ui-science/src/pages/tech-service/ThinkTankService.jsx:46",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「供方分析能力评分」指标名三份需求说明书未出现；清单 row_01=705（_phase3_screen_v3.json kept_items）自注「评分维度需立项调研确定」——功能意图在（供方能力目录化）、评分口径未给。科技智库/竞赛页为主需求科技创新服务全景平台（1.2 域）UI 挂载件。",
        },
        "facts": {
            "ui_mount": "ThinkTankService.jsx:652 服务类型详情抽屉「归档说明」区 { label: 供方分析能力, value: '不作为本目录，见服务类型页说明' } 行——清单挂载位",
            "ui_declare": "ThinkTankService.jsx:394 服务类型 Tab 说明句：服务类型为运营临时目录（confirm 标签）；供方返回的分析能力不作为服务类型：论文分析、专利分析、科研项目分析、社会网络分析、技术趋势分析、聚类分析、共性网络分析",
            "ui_capabilities": "mockData.js:123-125 thinkTankSupplierCapabilities 七项能力枚举数组（纯字符串清单，无任何分值/权重字段）——ui_demo_fallback 演示枚举",
            "ui_source_label": "ThinkTankService.jsx:46 SOURCE_LABEL.supplier='供方'——mock 数据来源标注体系（supplier/ops/system/collect/confirm/pending 六级）",
            "dev_table_total": dev["table_total"],
            "dev_score_word_tables": dev["word_score"],
            "dev_enterprise_score": {"rows": dev["gkxlumenx_ads.enterprise_score"]["rows"],
                                     "note": "14 列含 score_total/score_level/model_version（S3-08 lane_a 快照已证列结构）0 行空壳"},
            "gkx_table_count": gkx["table_count"],
            "gkx_score_word_tables": gkx["word_score"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_score_word_tables": jx["word_score"],
            "jiuxin_score_family_rows": jx["word_score_rows"],
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "supplier_analysis_capability_score",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "供方分析能力评分 = 对数据/服务供给方（咨询机构/检测机构等）专业分析能力的量化打分。评分事实面（供方×能力×分值）与评分模型（维度/权重/分制）三源零承载；UI 侧七能力为纯枚举清单（无分值）→ 不可构建，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 评分结果面（score/rating/evaluat/assess 词族 542 表）",
                "source": "dev",
                "sql": "information_schema.tables 表名词族扫描 + 行数实证（_shared_s309_alpha.py 快照 dev.word_score）",
                "hits": 7,
                "hit_detail": "enterprise_score 0 行空壳（INCUB_043/047 已证 14 列）；industry_chain_region_scorecard/svc_tech_power_score 为产业链区域/企业技术实力域；code_operating_status 为经营状态字典；policy_support_assessment(+_indicator) 为政策支持评估域；evaluation_template 为评估 BI 模板——智库供方分析能力评分域 0 命中",
            },
            {
                "probe": "gkx score 词族（280 表）",
                "source": "gkx",
                "sql": "information_schema.tables 表名词族扫描（快照 gkx.word_score）",
                "hits": 0,
                "note": "gkx word_score=[]——要素库无评分面",
            },
            {
                "probe": "jiuxin 供方分析能力评分（SHOW TABLES 实数 218 表）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + score/assessment 词族匹配 + 行数（快照 jiuxin.word_score/word_score_rows）",
                "hits": 13,
                "hit_detail": "评分族全为人才维度（talent_capability 99,996 行/talent_potential 100,000 行，INCUB_027 留证）、技术维度（technology_potential 38,860 行/disruption 97,150 行/bottleneck 92,544 行/region 2,708,162 行等）与科研难题维度（research_problem_potential 812 行）——无供方分析能力评分面",
            },
            {
                "probe": "评分模型定义（维度/权重/分制）+ 供方目录",
                "source": "doc",
                "sql": "三份说明书 + 主需求 rg 供方分析能力|供方|分析能力",
                "hits": 1,
                "hit_detail": "清单 row_01=705 自注「评分维度需立项调研确定」——UI 侧仅能力枚举无打分语义；三说明书无供方评分公式",
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：供方分析能力评分需①评分事实面（供方×能力×分值）②评分模型（维度/权重）两层。dev 评分词族 7 表逐一排除（唯一结构面 enterprise_score 0 行空壳且为企业域）；gkx 280 表 0 命中；jiuxin 13 表评分族全为人才/技术/科研难题维度。UI 侧七能力为纯枚举清单（mockData.js:123-125，无分值无权重），详情抽屉自认「不作为本目录」。两层皆缺。",
            "同门先例：S3-08 INCUB_043（综合能力评分）/INCUB_047（仪器共享能力评分）已证评分面+模型双缺（dev enterprise_score/carrier_index 双 0 行空壳、gkx 0 表、jiuxin 人才/技术维度）——本件独立留证，三源实探复证同构缺口，判档一致。",
            "UI 语义披露：本件挂载位非数值卡而是「归档说明」文字行（值=不作为本目录）——UI 侧自证供方能力目录化但未评分；SOURCE_LABEL 六级来源标注体系（:46）中 supplier=供方字段来源标签，非评分。",
            "升档路径：供方评价体系立项（维度/权重/分制）+ 供方×能力×分值面落库 → 完全转换支持；供方平台评价接口直连 → 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "供方分析能力评分为当期截面读数（评分快照）；三源无评分面无历史序列；UI 七能力枚举亦无年度维度。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["7", "13", "542", "280", "218", "0", "14", "99996", "99,996", "100000", "100,000", "38860", "97150", "92544", "2708162", "812"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | dev/gkx/jiuxin score hits:", len(dev["word_score"]), 0, len(jx["word_score"]))


if __name__ == "__main__":
    main()
