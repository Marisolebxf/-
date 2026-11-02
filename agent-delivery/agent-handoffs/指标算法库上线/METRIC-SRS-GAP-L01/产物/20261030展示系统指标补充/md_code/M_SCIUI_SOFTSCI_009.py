#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_009 转化效率趋势（平均转化周期）—— 薄壳校验脚本（完全不支持件）。

UI：SoftScienceWorkbench.jsx:941 时间趋势分析面板 trendSeries[1]「转化效率趋势」
（key=conversion-cycle，平均转化周期/个月，12 点月序列 8.8→7.4）。
口径=成果从立项到示范落地的平均周期（月）；分子分母=项目双时点，三源零承载。
dev dwd_patent_transfer 仅有转让生效日单时点（无立项/落地双时点），不可算周期。
"""
from __future__ import annotations

import json

OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_SOFTSCI_009_out.json"

PT_COLS = ["dwd_id", "patent_transfer_id", "pn", "country", "transfer_effective_date", "transfer_before",
           "transfer_after", "created_time", "updated_time", "creater", "updater", "table_data_source",
           "operator_remarks", "is_deleted", "insert_remark", "EDW_SRC_SYSTEM", "EDW_SYS_DATE", "EDW_DATA_DATE"]

YEAR_COUNTS = {"None": 287, "2021": 326, "2022": 1670, "2023": 3770, "2024": 7711, "2025": 5799, "2026": 3246}

TIME_WORDS = ("cycle", "period", "duration", "month", "立项", "落地", "周期", "转化")
cycle_like = sorted(c for c in PT_COLS if any(k.lower() in c.lower() for k in ("cycle", "duration", "period")))
assert cycle_like == []
assert sum(v for k, v in YEAR_COUNTS.items() if k != "None") == 22522

out = {
    "metric_id": "M_SCIUI_SOFTSCI_009",
    "batch": "S3-07-L2",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/components/SoftScienceWorkbench.jsx:941",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/soft-science/mock/softScienceHomepageMock.js:352-359",
    ],
    "facts": {
        "ui_mount": "SoftScienceWorkbench.jsx:941 时间趋势分析 tab（stage-tab-trend）trendSeries 渲染；图表 aria-label=转化效率趋势图（SoftScienceTrendAnalysis.jsx:212-215,247）",
        "ui_series": "key=conversion-cycle title=转化效率趋势 metricLabel=平均转化周期 unit=个月 seriesType=line trend=down",
        "ui_points": "12 点月序列 2025.05=8.8 → 2026.04=7.4（累计缩短 1.4 个月，SoftScienceTrendAnalysis.jsx:97-104 摘要句）",
        "ui_mock_note": "mock 为演示值不参与判档（ui_demo_fallback 披露）",
        "dev_patent_transfer_cols": PT_COLS,
        "dev_patent_transfer_cycle_like_columns": cycle_like,
        "dev_patent_transfer_year_counts": YEAR_COUNTS,
        "dev_patent_transfer_total": 22809,
        "gkx_table_count": 280,
        "jiuxin_table_count_live": 218,
        "named_in_srs": False,
        "named_note": "三份说明书未出现「转化效率趋势/平均转化周期」指标名（检索记录附录 A）。",
    },
    "derived": [
        {"name": "avg_conversion_cycle_monthly", "value": None,
         "reason": "周期=项目立项→示范落地双时点差；三源无项目双时点表：dev dwd_patent_transfer 仅转让生效日单时点（transfer_effective_date varchar）+转让前后权利人 JSON，无周期语义；gkx/gkxlumenx 无 conversion-cycle 词族表；jiuxin ads_technology_transfer_stage 为技术阶段快照非项目周期。"},
    ],
    "absence_probe": [
        {"probe": "dev 542 表 conversion/cycle/period 词族", "source": "dev",
         "sql": "information_schema.columns 词族扫描（_probe_s307_l2 快照）",
         "hit_tables_conversion": ["gkxlumenx_ods.dwd_patent_transfer"], "cycle_hits": 0},
        {"probe": "gkx 280 表 conversion 词族", "source": "gkx",
         "sql": "information_schema.columns 词族扫描（快照）", "hit_tables": ["gkx.dwd_patent_transfer"], "cycle_hits": 0},
        {"probe": "jiuxin 218 表（SHOW TABLES 实数）conversion/cycle 词族", "source": "jiuxin",
         "sql": "SHOW TABLES+列扫描（快照）", "hit_tables": ["ads_technology_transfer_stage"], "cycle_hits": 0},
    ],
    "support_judgment": "完全不支持",
    "notes": [
        "判档理由：平均转化周期需项目级双时点（立项日+落地日）；唯一转化域表 dwd_patent_transfer（dev 22,809/gkx 同构）仅专利权转让生效日单时点，权属变更≠成果转化落地，周期分子分母均无来源。",
        "jiuxin ads_technology_transfer_stage 列结构为技术阶段分布快照（阶段占比语义），非项目周期时长。",
        "权威口径：中国科技成果转化年度报告（2025）口径为转化合同数/收入，不含周期指标；周期类读数业界无强制标准，属平台自设运营指标。",
        "mock 8.8→7.4（12 点）为演示值（ui_demo_fallback 披露）。",
        "本件为薄壳：复用共享快照（dev_patent_transfer_year_counts/pair_top8）+ 列级周期词族断言。",
    ],
    "base_years_used": [],
    "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
    "base_years_note": "月度周期序列无任何真实月点可观测（dwd_patent_transfer 年计数为转让事件量非周期值）；项目双时点表接入后首个完整年为基期。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
        "12", "8.8", "7.4", "1.4", "22809", "22,809", "22522", "287", "326", "1670", "3770", "7711", "5799", "3246",
        "542", "280", "218", "2025.05", "2026.04",
    })},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
print("judgment: 完全不支持 | cycle_like:", cycle_like, "| pt_total:", out["facts"]["dev_patent_transfer_total"])
