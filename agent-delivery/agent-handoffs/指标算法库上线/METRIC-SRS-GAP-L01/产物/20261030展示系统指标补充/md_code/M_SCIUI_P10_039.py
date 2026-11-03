#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_039 全球研究主体时空分布（Q0210）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py（jiuxin ads_geo_yearly_* 正读数）
UI：SpaceTimeEvolutionNewPage.jsx:850 MetricInfo + WorldEvolutionMap。
jiuxin ads_geo_yearly_metrics 171,736 行（2000-2026）× 国家/省/市三层级 —— 完全转换支持。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_laneC_out.json"
OUT = "M_SCIUI_P10_039_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    jx = snap["jiuxin"]

    rows = jx["jiuxin_geo_yearly_metrics_rows"]
    year_counts = jx["jiuxin_geo_yearly_metrics_year_counts"]
    top12_2018 = jx["jiuxin_geo_country_top12_2018"]
    top12_2024 = jx["jiuxin_geo_country_top12_2024"]
    top12_2025 = jx["jiuxin_geo_country_top12_2025"]
    cn_city = jx["jiuxin_geo_cn_city_top12_2024"]
    type_dist = jx["jiuxin_geo_institution_type_2024"]
    profile_rows = jx["jiuxin_institution_profile_rows"]
    profile_coords = jx["jiuxin_institution_profile_rows_with_coords"]

    assert rows == 171736
    assert len(year_counts) == 27  # 2000-2026
    assert top12_2024[0]["country_en"] == "United States" and top12_2024[0]["institution_count"] == 9811
    assert top12_2024[1]["country_en"] == "China" and top12_2024[1]["institution_count"] == 4369
    assert profile_rows == 83745

    # US/China 双时点主体数（演化轨迹读数）
    def by_country(lst, en):
        return next(x for x in lst if x["country_en"] == en)
    us_2018 = by_country(top12_2018, "United States")["institution_count"]
    cn_2018 = by_country(top12_2018, "China")["institution_count"]
    us_2024 = by_country(top12_2024, "United States")["institution_count"]
    cn_2024 = by_country(top12_2024, "China")["institution_count"]
    us_2025 = by_country(top12_2025, "United States")["institution_count"]

    years = sorted(year_counts)
    out = {
        "metric_id": "M_SCIUI_P10_039",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:845-852",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:856-865",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:33-53",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「全球研究主体时空分布（Q0210）」指标名；上位功能叶 1.1.1.1.4.6.3 全球研究主体地域时空分布展示（SRS 科技时空演进展示.md:17-27 交互式时空地图分布呈现 / :34-39 地域模型多层级切换）为需求功能面上位覆盖。Q0210 为 UI 内部指标编号。",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:845-852 卡头「全球研究主体时空分布地图」+ MetricInfo title=全球研究主体时空分布（Q0210）；:856-865 WorldEvolutionMap（regions/flows/route/showHeat/focus）",
            "ui_kpi": "SpaceTimeEvolutionNewPage.jsx:670 KpiTile label=研究主体总数 metricId=Q0201（另号位）",
            "ui_mock": "mockData.js:33-53 CITY_PROFILES 20 个全球核心城市（base 2018 基准值×growth 年增×正弦波动确定性生成），:47-49 LEVELS 国家/省州/城市三档，:11 YEARS 2018-2026 九时点——ui_demo_fallback 演示值",
            "jiuxin_table": "ads_geo_yearly_metrics",
            "jiuxin_geo_yearly_metrics_rows": rows,
            "jiuxin_geo_yearly_year_span": f"{years[0]}-{years[-1]}",
            "jiuxin_geo_yearly_year_count": len(years),
            "jiuxin_geo_yearly_metrics_year_counts": year_counts,
            "jiuxin_geo_levels": {"COUNTRY": "国家级", "PROVINCE": "省/州级", "CITY": "城市级"},
            "jiuxin_profile_rows": profile_rows,
            "jiuxin_profile_rows_with_coords": profile_coords,
            "jiuxin_type_dict_table": "ads_institution_type（8 类字典：教育/医疗/企业/科研设施/非营利/政府/其他/档案文化）",
            "named_in_srs": False,
            "named_note": "指标名三份说明书 0 命中（附录 A 检索记录）；Q0210 为 mock metricId 编号非需规编号。",
        },
        "derived": [
            {
                "name": "jiuxin_geo_country_top12_2024",
                "value": top12_2024,
                "note": "2024 年国家级研究主体数 Top12（institution_count），快照键 jiuxin_geo_country_top12_2024；US 9,811 / China 4,369 / France 2,490 居前三。",
            },
            {
                "name": "jiuxin_geo_cn_city_top12_2024",
                "value": cn_city,
                "note": "2024 年中国城市级 Top12：北京市 798 / 上海 287 / 广州 183 / 南京 139 / 杭州 134 / 武汉 133 / 深圳 108 / 天津 103 / 成都 98 / 西安 96……",
            },
            {
                "name": "jiuxin_geo_institution_type_2024",
                "value": type_dist,
                "note": "2024 年国家级主体类型分布：教育 12,118 / 医疗 8,084 / 企业 7,317 / 科研设施 7,135 / 非营利 3,481 / 政府 2,909 / 其他 1,836 / 档案文化 558。",
            },
            {
                "name": "jiuxin_geo_us_china_evolution",
                "value": {"US": {"2018": us_2018, "2024": us_2024, "2025": us_2025},
                          "China": {"2018": cn_2018, "2024": cn_2024}},
                "note": "双强主体数演化：US 7,792（2018）→9,811（2024）→11,423（2025）；China 4,038（2018）→4,369（2024）。同表同年同层聚合（B3 同基）。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）全球研究主体时空序列结果面（geo_yearly 类）",
                "source": "dev",
                "sql": "information_schema 词族扫描（快照 _shared_s308_laneC_out.json dev.*；geo 词族仅 dim.city/admin_division/code_region 静态维表，无年度×地域主体序列）",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表全球主体时空分布面",
                "source": "gkx",
                "sql": "information_schema.tables 词族扫描（快照 gkx.*）",
                "hits": 0,
                "note": "gkx 无 geo_yearly/institution 时空序列面（280 表全 dwd_* 要素库）",
            },
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）正结论面",
                "source": "jiuxin",
                "sql": "SHOW TABLES + ads_geo_yearly_metrics/ads_geo_yearly_institution_type_metrics/ads_institution_profile 正读数（快照 jiuxin.*）",
                "hits": ["ads_geo_yearly_metrics(171736)", "ads_geo_yearly_institution_type_metrics(349396)", "ads_institution_profile(83745)", "ads_location(22229)"],
                "primary": "ads_geo_yearly_metrics",
            },
        ],
        "support_judgment": "完全转换支持",
        "notes": [
            "判档理由：久新 ads_geo_yearly_metrics（171,736 行，location_id×statistics_year×location_level）直接含 institution_count/paper_count/talent_count 等主体强度列，2000-2026 共 27 年无空年份、国家/省州/城市三层级齐备——「时间轴×层级切换×密度落图」整链转换即得；机构级坐标面 ads_institution_profile 83,745 行（68,226 行带经纬度）可作点层放大。三源均无现成「Q0210 时空分布」结果面（需从年度×地域聚合面转换），判完全转换支持。",
            "口径转换点：库口径=年度地域×层级的主体数序列（论文域 OpenAlex 语义主体池）；UI mock=20 城市画像确定性生成（论文/专利/资金/人才四维度）。维度差异：库以 institution_count（研究主体数）为主强度列，资金维度 UI mock 有而 geo_yearly 无专列（project_count 可近似）。",
            "2026 年不完整（6,775 地域行，为 2025 的 61%）——时序使用应截断标注。name_zh 在英文国家名行多为 NULL（美国/法国等），落图用 name_en。",
            "UI mock 20 城市/四维度/九时点为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s308_laneC.py + 快照；本脚本仅做断言+判档落盘。",
        ],
        "base_years_used": years,
        "base_years_missing": [],
        "base_years_note": "久新序列 2000-2026 共 27 年全覆盖（无空年份）；UI mock 时轴 2018-2026 为其子集。基期建议 2015（序列加厚段起点：3,009→8,456 台阶）或 2000（全序列首年）；2026 为不完整年（6,775 地域行，61% of 2025）需截断标注。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["171736", "171,736", "83745", "83,745", "68226", "22229", "349396", "9811", "4369", "2490", "7792", "4038", "11423", "798", "287", "183", "108", "12118", "8084", "7317", "7135", "2000", "2026", "2018", "2024", "2025", "27", "20", "218", "280", "542", "Q0210", "Q0201"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全转换支持 | rows:", rows, "| years:", years[0], "-", years[-1],
          "| US/China 2024:", us_2024, cn_2024)


if __name__ == "__main__":
    main()
