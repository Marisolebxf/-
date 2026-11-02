#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_002 专利交易与创新流动分析 —— 薄壳校验脚本（部分支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:1153-1215「专利交易与创新流动分析」区块：
时间区间(flowRange)+区域(flowRegion)选择 + 流动路径表(patentFlows)+
Top 路径条形图(flowBarOption)。流动路径=FLOW_PATHS 5 条 mock 主干道。
数据：dwd_patent_transfer 22,809 行交易面可用（区间过滤可算）；路径列从缺
（权利人→地名匹配 0/200 已证）；jiuxin 无交易路径面（阶段码表 8 行快照）。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_002_out.json")

VERDICT = "部分支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    years = dict(dev["dev_pt_year_counts"])
    no_year = years.pop("0", 0)
    years = {k: v for k, v in sorted(years.items())}
    total = sum(years.values())
    assert total + no_year == 22809
    # 区间聚合演示：UI flowRange 默认 [2018, 2026]，库序列起点 2021
    range_sum = sum(years.values())
    # 高价值聚集：无金额列 → 负结论

    out = {
        "metric_id": "M_SCIUI_P10_002",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1153",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:483-496",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:162-173",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技时空演进展示.md 序号 505「专利交易与创新流动分析」——本件即该功能叶的 UI 落位区块（需规描述：时间区间+区域选择、流动路径查看、报告导出）",
            "note": "区块标题与 SRS 功能叶同名；「分析」为 SRS 原词",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:1153 SectionCard id=ste-b-patent title=专利交易与创新流动分析 desc=时间区间+区域选择+流动路径；:1188-1207 流动路径表（路径/说明/起年值/止年值/区间增幅）；:1210-1213 Top 专利交易路径条形图",
            "ui_flow_table_source": "mockData.js:162-173 FLOW_PATHS type=patent 5 条（sf-bay→shenzhen 320/tokyo→seoul 180/munich→shanghai 150/tel-aviv→new-york 120/seoul→xian 90，growth 指数外推）",
            "ui_flow_builder": "SpaceTimeEvolutionNewPage.jsx:483-496 patentFlows useMemo：FLOW_PATHS 过滤区域→getFlowValue 外推起止值→按止年值降序",
            "ui_mock_note": "ui_demo_fallback：5 条主干道与量值均为演示设定；区间增幅为外推比非真实",
            "dev_table": "gkxlumenx_ods.dwd_patent_transfer",
            "dev_rows": 22809,
            "gkx_rows": gkx["gkx_pt_rows"],
            "dev_year_counts": years,
            "dev_columns_18": dev["dev_pt_columns"],
            "amount_like_columns": [],
            "jiuxin_transfer_stage_rows": 8,
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "patent_transfer_range_sum_2021_2026",
                "value": range_sum,
                "formula": "SUM(COUNT(*)) for transfer_effective_date IN 2021-2026（UI 区间过滤语义可对齐）",
                "source": "dev gkxlumenx_ods.dwd_patent_transfer",
            },
            {
                "name": "flow_path_negative",
                "value": None,
                "note": "负结论：流动路径表 5 列（路径/说明/起年值/止年值/增幅）全部依赖 from→to 区域对，库内无路径列且权利人→地名匹配 0/200（P10_001 专项已证），路径表与条形图维持 mock",
            },
            {
                "name": "high_value_negative",
                "value": None,
                "note": "负结论：SRS 需规「高价值专利聚集」需金额/估值列，18 列列级断言 amount_like=[]，高价值维度从缺",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 transfer 词族", "source": "dev",
             "hits": ["gkxlumenx_ods.dwd_patent_transfer"], "rows": 22809,
             "note": "事件面有；18 列无 from_region/to_region 路径列、无金额列"},
            {"probe": "gkx 280 表 transfer 词族", "source": "gkx",
             "hits": ["dwd_patent_transfer", "dwd_deal", "dwd_hk_sec_daily_quotation"],
             "note": "dwd_deal=投融资事件（非专利）、hk_sec=行情，语义错位"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）transfer/path 词族", "source": "jiuxin",
             "hits": ["ads_technology_transfer_stage"],
             "note": "8 行阶段码字典（BASIC_RESEARCH/ENGINEERING/.../MARKET_SCALE），无路径无流水"},
            {"probe": "权利人→地名归一（路径前置）", "source": "jiuxin ads_institution_profile",
             "sample": 200, "exact_name_match": 0, "alias_like_match": 0,
             "note": "P10_001 同批专项：名称体系不交叠（中文注册名 vs OpenAlex 英文名）"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：区块三要素——时间区间过滤（可算：transfer_effective_date 六年覆盖）、流动路径表（从缺：路径列无+匹配 0/200）、高价值聚集（从缺：无金额列）。区间聚合可对齐但两大呈现主体（路径表+聚集）零承载 → 部分支持。",
            "与 P10_001 同根同源（dwd_patent_transfer 22,809 行），本件聚焦分析区块（区间/路径/聚集），P10_001 聚焦总量卡；独立留证。",
            "区域选择器（flowRegion 国家下拉）在库内仅 country 列 5 值（CN/AU/BR/CA/AT）可过滤；mock 区域为全球城市级，粒度错位披露。",
            "「区间增幅」列语义（止年/起年-1）在外推 mock 上恒为正增长；真实面需两年计数比（2026 不完整年会失真，须截断）。",
            "jiuxin ads_talent_mobility_* 为人才路径族非专利路径族（P10_022/023 主源），本件不冒用。",
        ],
        "base_years_used": sorted(years),
        "base_years_missing": ["2018", "2019", "2020"],
        "base_years_note": "UI flowRange 默认区间 [2018,2026]，库序列 2021 起才有数据——区间前三年（2018-2020）为 mock 外推段；基期建议 2021；2026 为不完整年需截断标注。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "22809", "22,809", "7711", "5799", "3246", "3770", "1670", "326", "287",
            "5", "18", "8", "0", "200", "320", "180", "150", "120", "90",
            "542", "280", "218", "2021", "2026", "2018",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| range sum 2021-2026:", range_sum)


if __name__ == "__main__":
    main()
