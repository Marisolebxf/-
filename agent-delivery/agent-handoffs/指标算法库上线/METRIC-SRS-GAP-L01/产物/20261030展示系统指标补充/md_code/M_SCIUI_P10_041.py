#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_041 共享能力评分 —— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py
UI：InstrumentSharingNewPage.jsx:1067 机构详情 Modal「共享能力评分」+ :790/:832 列表位 + mock INSTITUTIONS.score。
INCUB_047 同族（组织级评分）：三源评分面均无仪器共享语义承载 → 完全不支持。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_laneC_out.json"
OUT = "M_SCIUI_P10_041_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]

    assert jx["jiuxin_ads_is_hits"] == []
    assert gkx["gkx_instrument_family"] == []
    assert jx["jiuxin_instrument_family"] == []

    out = {
        "metric_id": "M_SCIUI_P10_041",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:1067",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:790",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:832",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:180-196",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「共享能力评分」指标名；SRS 大型科学仪器共享.md:203「点击机构节点，系统弹窗显示机构优势资源、历史服务评价、共享能力评分等多维数据」为上位功能句（机构弹窗多维数据）。",
        },
        "facts": {
            "ui_mount": "InstrumentSharingNewPage.jsx:1067 机构详情 Modal Descriptions 项 { label: 共享能力评分, value: `${activeOrg.score} 分` }；:1036 Modal 标题注释（优势资源/历史评价/共享能力评分）",
            "ui_list_positions": "InstrumentSharingNewPage.jsx:790 机构列表副行「共享能力评分 {o.score}」；:832 活跃度列表「使用频率 {o.usageFreq} 次/月 · 共享能力评分 {o.score}」",
            "ui_mock": "mockData.js INSTITUTIONS 14 家机构 score 字段 82-95 分制（ORG-001 中科院深圳先进院 92/ORG-002 南方科技大学 95/ORG-009 深圳市计量院 93……）——ui_demo_fallback 演示值",
            "srs_upstream": "SRS :203 机构节点弹窗多维数据（优势资源/历史服务评价/共享能力评分）",
            "probe_dev_table_total": dev["dev_table_total"],
            "probe_gkx_table_count": gkx["gkx_table_count"],
            "probe_jiuxin_table_count_live": jx["jiuxin_table_count_live"],
            "probe_jiuxin_ads_is_hits": jx["jiuxin_ads_is_hits"],
            "family_note": "INCUB_047 仪器共享能力评分（组织级 score，分制）同族——同根因（评分模型依赖仪器共享运营数据，三源零承载）",
        },
        "derived": [
            {
                "name": "org_instrument_sharing_capability_score",
                "value": None,
                "note": "负结论 null 登记：共享能力评分模型的输入面（机构-仪器台账/开放率/使用频率/服务评价流水）三源均无承载，评分不可计算；dev 侧 40+ score 列族（enterprise_score/carrier_index 等）均为企业/产业链/政策域评分，无仪器共享语义面。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）仪器共享机构评分面（score 列 + instrument/org 语义）",
                "source": "dev",
                "sql": "information_schema.columns 表名+列名扫描（快照 _shared_s308_laneC_out.json；score 列命中 40+ 表全为企业/链/政策/载体指数域，ads.realdata_research_org_stat.capability_score 0 行空壳且语义为科研能力非仪器共享）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表仪器共享评分面",
                "source": "gkx",
                "sql": "information_schema 词族扫描（快照 gkx_instrument_family=[]）",
                "hits": 0,
            },
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）ads_is* 评分表/仪器共享语义面",
                "source": "jiuxin",
                "sql": "SHOW TABLES LIKE 'ads_is%' + instrument/instrument 词族（快照均空）",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：共享能力评分（组织级）是复合评分——输入维含机构入网仪器规模/开放率/使用频率/服务评价，这些上游依赖（共享平台 ADS 表族）三源零承载（P10_040/055/037 同根因）；dev 侧虽有 40+ score 列族但全部是企业/产业链/政策/载体指数域，无一承载仪器共享语义；ads.realdata_research_org_stat（capability_score）为 0 行空壳且语义是科研能力。评分模型无输入即无输出 → 完全不支持。",
            "评分口径无权威国标：科技部考核细则（R1）评的是管理单位开放共享评价考核结果（合格/良好/优秀档），非百分制能力分——UI mock 82-95 分制为平台自设运营评分。",
            "修复路径：随共享平台 ADS 表族接入（P10_040 主缺口），评分模型（开放率×使用频率×评价加权）即可建 → 升完全转换支持；若共享平台侧已有机构评分接口直连 → 完全直接支持。",
            "INCUB_047（路A 件）为同族件，本件独立留证不复用其结论。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "评分为存量截面读数（无时序维度）；mock 14 机构单时点演示。若评分模型落地，建议以模型上线年为基期建立年度序列。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["14", "82", "95", "92", "93", "542", "280", "218", "40", "1036", "1067"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | ads_is in jiuxin:", jx["jiuxin_ads_is_hits"])


if __name__ == "__main__":
    main()
