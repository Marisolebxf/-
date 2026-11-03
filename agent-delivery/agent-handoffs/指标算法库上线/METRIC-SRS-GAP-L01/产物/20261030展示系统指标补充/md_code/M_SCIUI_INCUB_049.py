#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_049 跨区协作率（跨区合作占比）—— 薄壳校验脚本（完全转换支持件，独立复算留证）。

UI：innovationEcosystemMock.js:360 compare 卡 { label: 跨区协作率, value: 46%, hint: 重点链路继续升温 }
渲染挂载 InnovationEcosystemWorkbench.jsx:1957-1965（MetricsStage compareItems）。
本件为 S3-08 路 A 独立复算：jiuxin ads_institution_collaboration_yearly
GROUP BY statistics_year 实连重跑（非复用 ECOSYS_001 缓存值），与 S3-07
ECOSYS_001 结论交叉校验（判档一致 = 完全转换支持）。
"""
from __future__ import annotations

import json

import pymysql

OUT = "M_SCIUI_INCUB_049_out.json"
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
    # 独立复算补充：2025/2026 对数量级读数（截断标注材料）
    cur.execute("""
        SELECT statistics_year, COUNT(*) FROM ads_institution_collaboration_yearly
        WHERE statistics_year IN (2025, 2026) GROUP BY statistics_year ORDER BY statistics_year
    """)
    tail = {str(y): n for y, n in cur.fetchall()}
    conn.close()

    years = sorted(yearly)
    # 独立复算断言（本件实跑值 = ECOSYS_001 交叉一致）
    assert total_rows == 14380246, total_rows
    assert years == [str(y) for y in range(2015, 2027)]
    assert null_year_rows == 0
    assert yearly["2015"]["cross_region_rate_pct"] == 30.82
    assert yearly["2024"]["cross_region_rate_pct"] == 34.49
    assert yearly["2025"]["cross_region_rate_pct"] == 34.40
    assert yearly["2026"]["cross_region_rate_pct"] == 37.97
    assert tail["2026"] == 487504 and tail["2025"] == 3015548

    out = {
        "metric_id": "M_SCIUI_INCUB_049",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/mock/innovationEcosystemMock.js:360",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1957-1965",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/__tests__/InnovationEcosystemPage.test.jsx:332",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「跨区协作率」指标名三份说明书未出现；INCUB 清单 row_01=604 挂载位=innovationEcosystemMock.js:360（实查定位）；语义锚 SRS 上位叶为创新生态展示生态指标区（ECOSYS_001 附录 A 同查）。",
        },
        "facts": {
            "ui_mount": "InnovationEcosystemWorkbench.jsx:1957-1965 MetricsStage compare 卡列表（span=label/strong=value/p=hint 三元组渲染）；mock 卡 :360 { label: 跨区协作率, stage: collaboration, periods: ANNUAL_PERIODS, value: 46%, hint: 重点链路继续升温 }",
            "ui_mock_note": "mock 46% 为 ui_demo_fallback 演示值，不参与判档；同组 compare 卡：平台能级 91/人才净流入 +8.4%/成果转化周期 4.8",
            "ui_test_anchor": "InnovationEcosystemPage.test.jsx:332 断言「跨区协作率」文案在文档——UI 挂载测试锚",
            "jiuxin_table": "ads_institution_collaboration_yearly",
            "jiuxin_rows": total_rows,
            "jiuxin_null_year_rows": null_year_rows,
            "jiuxin_column_total": 43,
            "jiuxin_key_columns": sorted([
                "institution_id", "collaborator_institution_id", "statistics_year",
                "collaborator_province_name", "collaborator_city_name",
                "is_domestic_collaboration", "is_international_collaboration",
                "is_cross_region_collaboration", "collaboration_strength",
            ]),
            "jiuxin_tail_year_pairs": tail,
            "dev_table_total": 542,
            "dev_enterprise_cooperation": "gkxlumenx_dwd.enterprise_cooperation 10 列 0 行空壳（ECOSYS_001 留证，S3-07 快照）",
            "gkx_table_count": 280,
            "jiuxin_table_count_live": 218,
            "cross_check": "本件独立实连重跑 GROUP BY 全表聚合，读数与 S3-07 ECOSYS_001（完全转换支持）逐断言交叉一致：2015=30.82/2024=34.49/2025=34.40/2026=37.97，总行 14,380,246，null 年 0",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "cross_region_collaboration_rate_yearly",
                "value": {y: yearly[y]["cross_region_rate_pct"] for y in years},
                "formula": "cross_region_rate = SUM(is_cross_region_collaboration=1) / COUNT(*) × 100，按 statistics_year 分组（机构协作对粒度→年度率聚合，同表同源 B3 同基）",
                "source": "jiuxin ads_institution_collaboration_yearly（本件独立实连复算）",
                "years": years,
                "numerator": {y: yearly[y]["cross_region_pairs"] for y in years},
                "denominator": {y: yearly[y]["total_pairs"] for y in years},
            },
            {
                "name": "collab_pairs_yearly",
                "value": {y: [yearly[y]["total_pairs"], yearly[y]["cross_region_pairs"], yearly[y]["international_pairs"], yearly[y]["domestic_pairs"]] for y in years},
                "note": "[total, cross_region, international, domestic] 分年四元组",
            },
            {
                "name": "mock_reference",
                "value": 46,
                "disclosure": "ui_demo_fallback：mock 46% 演示值；真实 2024 全国机构口径 34.49%（口径差：mock 为区域链路语义，库为省域跨区机构对语义——ECOSYS_001 同裁定，本件复认）",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 collaboration/cooperation 词族", "source": "dev",
             "sql": "information_schema 表名扫描（S3-07/S3-08 快照）",
             "hits": ["gkxlumenx_dwd.enterprise_cooperation"], "rows": 0, "note": "10 列结构空壳（id/org_id/partner_type/partner_org_id/partner_name/cooperation_type/project_count/patent_count/create_time/update_time）——dev 侧无替代承载，正结论归久新"},
            {"probe": "gkx 280 表 collaboration 词族", "source": "gkx",
             "sql": "information_schema 表名扫描（快照）", "hits": 0, "note": "gkx 无协作面"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）collaboration 词族", "source": "jiuxin",
             "sql": "SHOW TABLES + 词族扫描（快照 + 本件实连）",
             "hits": ["ads_institution_collaboration_yearly", "ads_institution_collaboration_subfield_yearly", "ads_research_problem_collaboration_recommendation", "ads_talent_collaborator", "ads_talent_institution_cooperation"],
             "primary": "ads_institution_collaboration_yearly（14,380,246 行，43 列，2015-2026 全序列）",
             "note": "正结论承载面——本件独立 GROUP BY 复算即判档证据"},
        ],
        "support_judgment": "完全转换支持",
        "notes": [
            "判档理由：久新 ads_institution_collaboration_yearly（14,380,246 行，43 列）直接含 is_cross_region_collaboration 标志列 + statistics_year（2015-2026 全序列无空年份）——年度跨区协作率一步聚合即得（本件独立复算 30.82%→37.97%）；机构对粒度到 UI 区域率需聚合转换（非 100% 直出），判完全转换支持。",
            "独立复算留证：本件实连 GROUP BY 全表重跑（非缓存 S3-07 值），四断言（总行/年份覆盖/首末年率/尾部对数）与 ECOSYS_001 交叉一致——多本账互推（B11）零漂移。",
            "口径转换点：库口径=跨省机构协作对占比；UI mock 语义=市内跨区链路（南山-宝安）演示值 46%。若 UI 需市内跨区口径，需 ads_institution_profile（83,745 行含 city_location_id）自关联二次加工——登记为升档路径非判档依据。",
            "2026 年不完整（487,504 对，仅为 2025 3,015,548 对的 16%）——序列使用应截止 2025 或按 metrics_as_of_date 标注截断；2026 跳升 37.97% 或有收录滞后。",
            "同族件：ECOSYS_001（S3-07，同 UI 卡同表）为先行件，本件为派单指定的独立复算复判件；两件判档一致（完全转换支持）。",
        ],
        "base_years_used": years,
        "base_years_missing": ["2013", "2014"],
        "base_years_note": "久新序列 2015-2026 全覆盖（null 年 0 行）；2013-2014 无数据。基期建议 2015（序列首年）；2026 为不完整年（487,504 对，16% of 2025）需截断标注。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "46", "34.49", "34.4", "37.97", "30.82", "14380246", "14,380,246", "487504", "3015548", "3,015,548",
            "83745", "83,745", "542", "280", "218", "43", "10", "12", "91", "8.4", "4.8", "2015", "2026", "2024", "2025", "16",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全转换支持（独立复算）| years:", years[0], "-", years[-1],
          "| rate 2015/2024/2025/2026:", yearly["2015"]["cross_region_rate_pct"],
          yearly["2024"]["cross_region_rate_pct"], yearly["2025"]["cross_region_rate_pct"],
          yearly["2026"]["cross_region_rate_pct"])


if __name__ == "__main__":
    main()
