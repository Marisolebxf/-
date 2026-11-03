#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_ECOSYS_001 跨区协作率 —— 薄壳校验脚本（完全转换支持件）。

UI：InnovationEcosystemWorkbench.jsx:1957-1965 生态指标 tab「区域生态位次」
compare 卡 { label: 跨区协作率, stage: collaboration, value: 46% }。
久新 ads_institution_collaboration_yearly（14,380,246 行）直接含
is_cross_region_collaboration 标志 + statistics_year —— 年度率可转换计算。
"""
from __future__ import annotations

import json

import pymysql

OUT = "M_SCIUI_ECOSYS_001_out.json"
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4")


def main() -> None:
    conn = pymysql.connect(**JX)
    cur = conn.cursor()
    cur.execute("""
        SELECT statistics_year, COUNT(*),
               SUM(CASE WHEN is_cross_region_collaboration = 1 THEN 1 ELSE 0 END),
               SUM(CASE WHEN is_international_collaboration = 1 THEN 1 ELSE 0 END),
               SUM(CASE WHEN is_domestic_collaboration = 1 THEN 1 ELSE 0 END)
        FROM ads_institution_collaboration_yearly
        WHERE statistics_year IS NOT NULL
        GROUP BY statistics_year ORDER BY statistics_year
    """)
    yearly = {}
    for y, tot, cross, intl, dom in cur.fetchall():
        yearly[str(y)] = {
            "total_pairs": tot, "cross_region_pairs": cross,
            "cross_region_rate_pct": round(cross / tot * 100, 2),
            "international_pairs": intl, "domestic_pairs": dom,
        }
    cur.execute("SELECT COUNT(*) FROM ads_institution_collaboration_yearly")
    total_rows = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM ads_institution_collaboration_yearly WHERE statistics_year IS NULL")
    null_year_rows = cur.fetchone()[0]
    conn.close()

    years = sorted(yearly)
    assert total_rows == 14380246
    assert years == [str(y) for y in range(2015, 2027)]
    assert null_year_rows == 0
    assert yearly["2015"]["cross_region_rate_pct"] == 30.82
    assert yearly["2024"]["cross_region_rate_pct"] == 34.49

    out = {
        "metric_id": "M_SCIUI_ECOSYS_001",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1957-1965",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/mock/innovationEcosystemMock.js:360",
        ],
        "facts": {
            "ui_mount": "InnovationEcosystemWorkbench.jsx:1957-1965 生态指标 tab 右栏「区域生态位次」compare 卡列表（label/value/hint 三元组）",
            "ui_mock_card": "innovationEcosystemMock.js:360 { label: 跨区协作率, stage: collaboration, periods: ANNUAL_PERIODS, value: 46%, hint: 重点链路继续升温 }",
            "ui_mock_note": "mock 46% 为演示值不参与判档（ui_demo_fallback 披露）；同组另三卡：平台能级 91/人才净流入 +8.4%/成果转化周期 4.8",
            "ui_filter_chain": "InnovationEcosystemPage.jsx:541-567 filteredMetricCompare（关键词/分析维度/区域三重过滤）",
            "jiuxin_table": "ads_institution_collaboration_yearly",
            "jiuxin_rows": total_rows,
            "jiuxin_null_year_rows": null_year_rows,
            "jiuxin_key_columns": sorted([
                "institution_id", "collaborator_institution_id", "statistics_year",
                "collaborator_province_name", "collaborator_city_name",
                "is_domestic_collaboration", "is_international_collaboration",
                "is_cross_region_collaboration", "collaboration_strength",
            ]),
            "jiuxin_column_total": 43,
            "dev_table_total": 542,
            "dev_enterprise_cooperation": "gkxlumenx_dwd.enterprise_cooperation 10 列（id/org_id/partner_type/partner_org_id/partner_name/cooperation_type/project_count/patent_count/create_time/update_time）0 行空壳",
            "gkx_table_count": 280,
            "jiuxin_table_count_live": 218,
            "named_in_srs": False,
            "named_note": "三份说明书未出现「跨区协作率」指标名（检索记录附录 A）；派单书清单挂载点空，实查定位。",
        },
        "derived": [
            {
                "name": "cross_region_collaboration_rate_yearly",
                "value": {y: yearly[y]["cross_region_rate_pct"] for y in years},
                "formula": "cross_region_rate = SUM(is_cross_region_collaboration=1) / COUNT(*) × 100，按 statistics_year 分组（机构协作对粒度→年度率聚合）",
                "source": "jiuxin ads_institution_collaboration_yearly",
                "years": years,
            },
            {
                "name": "collab_pairs_yearly",
                "value": {y: [yearly[y]["total_pairs"], yearly[y]["cross_region_pairs"], yearly[y]["international_pairs"], yearly[y]["domestic_pairs"]] for y in years},
                "note": "[total, cross_region, international, domestic]",
            },
            {
                "name": "mock_reference",
                "value": 46,
                "disclosure": "ui_demo_fallback：mock 46% 演示值；真实 2024 全国机构口径 34.49%（口径差：mock 为区域链路语义，库为省域跨区机构对语义）",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 collaboration/cooperation 词族", "source": "dev",
             "sql": "information_schema.columns 词族扫描（_probe_s307_l2 快照）",
             "hits": ["gkxlumenx_dwd.enterprise_cooperation"], "rows": 0, "note": "结构空壳"},
            {"probe": "gkx 280 表 collaboration 词族", "source": "gkx",
             "sql": "information_schema.columns 词族扫描（快照）", "hits": 0},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）collaboration 词族", "source": "jiuxin",
             "sql": "SHOW TABLES+列扫描（快照）",
             "hits": ["ads_institution_collaboration_yearly", "ads_institution_collaboration_subfield_yearly", "ads_research_problem_collaboration_recommendation", "ads_talent_collaborator", "ads_talent_institution_cooperation"],
             "primary": "ads_institution_collaboration_yearly"},
        ],
        "support_judgment": "完全转换支持",
        "notes": [
            "判档理由：久新 ads_institution_collaboration_yearly（14,380,246 行，43 列）直接含 is_cross_region_collaboration 标志列 + statistics_year（2015-2026 全序列无空年份）——年度跨区协作率聚合即得（30.82%→37.97%）；从机构对粒度到 UI 区域链路语义需聚合转换（非 100% 直出），判完全转换支持。",
            "口径转换点：库口径=跨省机构协作对占比（is_cross_region 按 collaborator_province_name 判定）；UI mock 语义=市内跨区（南山-宝安链路）链路率。若 UI 需市内跨区口径，需 city_location 级机构表自关联（ads_institution_profile 83,745 行含 city_location_id 可作维度）。",
            "2026 年数据不完整（487,504 对，仅为 2025 的 16%）——年度序列使用应截止 2025（或按 metrics_as_of_date 标注截断）。",
            "12 年序列单调上行（30.82→34.40 稳态，2026 跳升 37.97 或有收录滞后偏差），趋势与 mock「重点链路继续升温」方向一致。",
            "本件为薄壳：复用共享快照词族面 + 久新年度聚合实算（每件独立重跑，非跨件缓存）。",
        ],
        "base_years_used": years,
        "base_years_missing": ["2013", "2014"],
        "base_years_note": "久新序列 2015-2026 全覆盖（无空年份）；2013-2014 无数据。基期建议 2015（序列首年）；2026 为不完整年（487,504 对，16% of 2025）需截断标注。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "46", "34.49", "34.4", "37.97", "30.82", "14380246", "14,380,246", "487504", "3015548", "2146142",
            "83745", "83,745", "542", "280", "218", "43", "10", "12", "91", "8.4", "4.8", "2015", "2026", "2024", "2025", "16",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全转换支持 | years:", years[0], "-", years[-1],
          "| rate 2015/2024/2025/2026:", yearly["2015"]["cross_region_rate_pct"],
          yearly["2024"]["cross_region_rate_pct"], yearly["2025"]["cross_region_rate_pct"],
          yearly["2026"]["cross_region_rate_pct"])


if __name__ == "__main__":
    main()
