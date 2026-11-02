#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_001 专利交易与创新流动 —— 薄壳校验脚本（部分支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:1073 ElementCard「专利交易与创新流动」
（stat = kpis.patents 全球年度专利交易总量，件）。
数据：dev gkxlumenx_ods.dwd_patent_transfer 22,809 行已证（本批独立复核）；
kpis.patents 读数可由年度计数直算（口径 A）；流动语义（跨区域路径）需
权利人名称→机构画像地名解析，匹配率 0/200 已证不可行（口径 B 从缺）。
"""
from __future__ import annotations

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_001_out.json")

VERDICT = "部分支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx = snap["dev"], snap["gkx"]

    years = dev["dev_pt_year_counts"]
    no_year = years.pop("0", 0)
    years = {k: v for k, v in sorted(years.items())}
    total = sum(years.values())
    assert dev["dev_pt_rows"] == 22809
    assert gkx["gkx_pt_rows"] == 22809
    assert total + no_year == 22809
    assert years["2024"] == 7711 and years["2021"] == 326

    # 2026 不完整年强度（vs 2025 全年）
    strength_2026 = round(years["2026"] / years["2025"] * 100, 1)

    out = {
        "metric_id": "M_SCIUI_P10_001",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1073",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:401-407",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技时空演进展示.md 序号 505「专利交易与创新流动分析」功能叶（需规描述：支持自动整合专利交易和转让数据，用户可选择时间区间和区域，查看科技成果流动路径及高价值专利聚集）",
            "note": "「专利交易与创新流动」卡片名为 UI 简称；上位功能叶 505 覆盖交易整合与流动路径两侧语义",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:1073 ElementCard title=专利交易与创新流动，stat=`${formatNumber(kpis.patents)} 件`，desc=全球年度专利交易总量，onClick 跳 ste-b-patent 分析区块",
            "ui_kpis_source": "mockData.js:401-407 getGlobalTotals→aggregateStats：26 城 base.patents 按 growth*0.9 指数外推逐年求和（纯演示外推，非真实交易）",
            "ui_mock_note": "ui_demo_fallback：mock 年度专利交易量为 CITY_PROFILES 外推演示值，不参与判档",
            "dev_table": "gkxlumenx_ods.dwd_patent_transfer",
            "dev_rows": dev["dev_pt_rows"],
            "gkx_rows": gkx["gkx_pt_rows"],
            "dev_year_counts": years,
            "dev_no_year_rows": no_year,
            "dev_columns_18": dev["dev_pt_columns"],
            "dev_country_dist": {"CN": 16848, "AU": 5421, "BR": 493, "CA": 43, "AT": 4},
            "dev_holder_name_form_sample_2024_1000": {"org_form": 1745, "person_form": 426},
            "jiuxin_transfer_table": "ads_technology_transfer_stage（8 行阶段码表快照，非交易流水）",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": snap["jiuxin"]["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "patent_transfer_yearly_counts",
                "value": years,
                "formula": "COUNT(*) GROUP BY LEFT(transfer_effective_date,4)（口径 A：年度交易事件量）",
                "source": "dev gkxlumenx_ods.dwd_patent_transfer（gkx 同构同值）",
            },
            {
                "name": "year_2026_strength_pct",
                "value": strength_2026,
                "formula": f"{years['2026']}/{years['2025']}×100（2026 为不完整年收录强度）",
                "share_basis": "同表同年计数相除（B3 同基）",
            },
            {
                "name": "flow_path_semantic_gap",
                "value": None,
                "note": "负结论登记：流动路径口径（跨区域 from→to）需权利人名称→机构画像地名解析；200 样本精确名/别名匹配 0 命中（jiuxin ads_institution_profile 83,745 行，name_zh 覆盖 5,180），路径不可算",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 transfer 词族（表名+列名双扫）", "source": "dev",
             "hits": ["gkxlumenx_ods.dwd_patent_transfer"], "rows": 22809,
             "note": "交易事件面有（单时点）；无流动路径列"},
            {"probe": "gkx 280 表 transfer 词族", "source": "gkx",
             "hits": ["dwd_patent_transfer", "dwd_deal", "dwd_hk_sec_daily_quotation"],
             "note": "dwd_patent_transfer 与 dev 同构同值 22,809；dwd_deal=投融资交易、hk_sec=港股行情，语义错位"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）transfer 词族", "source": "jiuxin",
             "hits": ["ads_technology_transfer_stage"],
             "note": "8 行阶段码表（BASIC_RESEARCH..MARKET_SCALE），快照占比语义非交易流水"},
            {"probe": "权利人→地名解析（流动路径前置）", "source": "jiuxin ads_institution_profile",
             "sample": 200, "exact_name_match": 0, "alias_like_match": 0,
             "note": "名称体系不交叠（转让表中文注册名 vs 画像英文 OpenAlex 名），路径维度从缺"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：年度交易总量读数（kpis.patents 对应值）可由 dwd_patent_transfer 年度计数直算（22,809 行 2021-2026 六年序列）——总盘子口径可用；但「流动」语义（跨区域路径 from→to）需权利人地名归属，200 样本匹配率 0，路径维度从缺。关键维度缺失 → 部分支持。",
            "dev/gkx 两源同构同值（22,809/年分布逐一相同），任一可作计算源；本件以 dev 为主源。",
            "口径差披露：UI 卡语义为「全球年度专利交易总量」（mock 全球 26 城外推）；库口径为专利权属变更事件（CN 16,848/AU 5,421/BR 493/CA 43/AT 4），且权属变更≠商业化交易（含赠与/内部划转/继承）。",
            "2026 为不完整年（3,246 行，强度 56.0%），年度序列对外应截断标注。",
            "SOFTSCI_009（转化效率趋势）已证同表 18 列无周期列；本件与 P10_002（分析页）同根同源、独立留证。",
        ],
        "base_years_used": sorted(years),
        "base_years_missing": ["2019", "2020"],
        "base_years_note": "transfer_effective_date 覆盖 2021-2026 六年（另 287 行无年份）；2019-2020 无数据。基期建议 2021（序列首年）；2026 为不完整年需截断标注。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "22809", "22,809", "7711", "7,711", "5799", "5,799", "3246", "3,246", "3770", "1670", "326",
            "287", "16848", "5421", "493", "43", "4", "1745", "426", "200", "0", "56.0", "56",
            "542", "280", "218", "8", "18", "83745", "5180", "2021", "2024", "2026",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| years:", sorted(years), "| 2026 strength:", strength_2026)


if __name__ == "__main__":
    main()
