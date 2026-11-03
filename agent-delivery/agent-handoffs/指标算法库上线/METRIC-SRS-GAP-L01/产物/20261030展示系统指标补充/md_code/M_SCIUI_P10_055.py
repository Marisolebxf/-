#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_055 机构入网仪器开放率（openRate%）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py
UI：InstrumentSharingNewPage.jsx:1065 机构详情 Modal + :809 机构开放率TopN 图 + :241/:829 进度条位。
lineage 指定源表 ads_is_org_open_rate —— 三源 0 实存 → 完全不支持。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_laneC_out.json"
OUT = "M_SCIUI_P10_055_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]

    assert jx["jiuxin_ads_is_hits"] == []
    assert dev["dev_ads_is_hits"] == []
    assert gkx["gkx_instrument_family"] == []

    out = {
        "metric_id": "M_SCIUI_P10_055",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:1065",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:809",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/InstrumentSharingNewPage.jsx:256-259",
            "repos/demo-ui-science/src/pages/achievement-preview-new/instrument-sharing-new/mockData.js:261-264",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「机构入网仪器开放率」指标名；SRS 大型科学仪器共享.md:187「按照科研院所、高校、企业、检测机构等类别，自动在地图高亮展示各服务机构的地理分布及资源状态」/:235「实时动态统计各服务机构仪器资源开放率、当前活跃状态及使用频率」上位覆盖。",
        },
        "facts": {
            "ui_mount": "三挂载位：:1065 机构详情 Modal { label: 开放率, value: `${activeOrg.openRate}%` }；:809「机构开放率 TopN」图（CHART_METRICS.orgOpenRate）；:241 地图点副题 `${o.type} · 开放率 ${o.openRate}% · ${o.activeStatus}` + :829 活跃度列表 Progress percent={o.openRate}",
            "ui_compute_chain": ":256-259 orgOpenRateTop = [...INSTITUTIONS].sort((a,b)=>b.openRate-a.openRate).slice(0,8)；:423 图数据 orgOpenRateTop.map((o)=>o.openRate)",
            "ui_mock": "mockData.js INSTITUTIONS 14 机构 openRate 48-90%（ORG-009 深圳市计量院 90 最高/ORG-014 比亚迪中央研究院 48 最低）——ui_demo_fallback 演示值",
            "ui_lineage_note": "CHART_METRICS.orgOpenRate lineage（mockData.js:261-264）: 口径：机构开放率 = 开放共享仪器数 ÷ 入网仪器数 × 100%。源表：ads_is_org_open_rate；更新频率：T+1——UI 侧口径契约指定源表",
            "probe_jiuxin_ads_is": jx["jiuxin_ads_is_hits"],
            "probe_dev_ads_is": dev["dev_ads_is_hits"],
            "probe_gkx_instrument_family": gkx["gkx_instrument_family"],
            "probe_jiuxin_instrument_family": jx["jiuxin_instrument_family"],
            "probe_dev_open_rate_cols": "dev 全库 open_rate 列词族 0 命中（information_schema.columns 扫描，快照 dev_instrument_family_hits 无 open_rate 命中）",
            "probe_dev_table_total": dev["dev_table_total"],
            "probe_gkx_table_count": gkx["gkx_table_count"],
            "probe_jiuxin_table_count_live": jx["jiuxin_table_count_live"],
            "family_note": "P10_040 平台级共享率（同 ads_is_* 族）/P10_041 共享能力评分（openRate 为输入维）/P10_037 使用频率（同族）——本件为机构粒度变体，独立留证",
        },
        "derived": [
            {
                "name": "org_instrument_open_rate",
                "value": None,
                "note": "负结论 null 登记：机构开放率=机构开放共享仪器数÷机构入网仪器数（lineage 公式），分子分母均需机构-仪器台账与开放标志——指定源表 ads_is_org_open_rate 三源 0 实存；机构-仪器关联（org_id×instrument_id×open_flag）任何形式等价物零承载。公式无法执行。",
            },
        ],
        "absence_probe": [
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）ads_is_org_open_rate 指定源表 + ads_is* 族",
                "source": "jiuxin",
                "sql": "SHOW TABLES LIKE 'ads_is%'（快照 jiuxin_ads_is_hits=[]）",
                "hits": 0,
            },
            {
                "probe": "dev 17 schema（542 表）open_rate/share_rate 列 + 机构-仪器关联表",
                "source": "dev",
                "sql": "information_schema.columns 词族扫描（快照：open_rate/open_share 0 命中；ads_is_hits=[]；机构侧表 realdata_research_org_stat 0 行空壳且无仪器关联）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表机构仪器台账/开放标志列",
                "source": "gkx",
                "sql": "information_schema 词族扫描（快照 gkx_instrument_family=[]）；dwd_medical_device 无 org×instrument×open 结构（company_name 为注册商语义非入网机构）",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：机构开放率是 P10_040 平台共享率的机构粒度下钻——lineage 公式（开放共享仪器数÷入网仪器数）要求机构-仪器台账 + 开放标志对；指定源表 ads_is_org_open_rate 与整个 ads_is_* 族在久新 218 表 0 实存，dev 542 表 open_rate 列 0 命中，gkx 280 表仪器族 0（dwd_medical_device 的 company_name 是 FDA 注册商语义非入网管理机构）。分子分母两依赖均无承载 → 完全不支持。",
            "mock 14 机构 48-90% 为演示值（ui_demo_fallback 披露）；S3-07 批共享探针（_probe_s307_l2）已证 gkx 医疗器械面无开放标志列，本件独立留证。",
            "修复路径：共享平台 ADS 接入（ads_is_org + ads_is_org_open_rate，或 org×instrument 台账自算）→ 完全直接支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "机构开放率为存量截面读数（机构-仪器关系变更低频）；mock 14 机构单时点演示。若接入 ADS 表（T+1）可建月度序列，以接入月为基期。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["48", "90", "14", "8", "218", "542", "280", "1065", "261"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | ads_is jiuxin/dev:", jx["jiuxin_ads_is_hits"], dev["dev_ads_is_hits"])


if __name__ == "__main__":
    main()
