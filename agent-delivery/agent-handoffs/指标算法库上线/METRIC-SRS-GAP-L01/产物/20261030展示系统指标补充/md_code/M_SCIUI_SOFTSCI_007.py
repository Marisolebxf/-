#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SOFTSCI_007 孵化毕业统计 —— 薄壳校验脚本（部分支持件）。

UI：IncubationCarrierPage.jsx:1009「孵化毕业统计」= 在孵(柱)+已毕业(柱)+毕业率(线)。
dev dim.carrier→carrier_org_rel 链路承载载体维与在驻关系（tenant=39 在驻可近似在孵），
毕业语义零承载（rel_type 域={self,tenant}、end_date 全 NULL、无毕业状态列）。
本件为三件套中唯一部分支持件（在孵数可算、毕业数/毕业率不可算）。
"""
from __future__ import annotations

import json

import pymysql

OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_SOFTSCI_007_out.json"
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600", charset="utf8mb4")
FAMILIES = ("graduat", "incubat", "onincub", "inincub")


def q(conn, sql):
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def main() -> None:
    conn = pymysql.connect(database="information_schema", **DEV)

    rows = q(conn, """
        SELECT TABLE_NAME AS t, COLUMN_NAME AS c
        FROM information_schema.columns
        WHERE TABLE_SCHEMA IN ('gkxlumenx_dim','gkxlumenx_dwd','gkxlumenx_ads')
          AND TABLE_NAME IN ('carrier','carrier_org_rel','enterprise_innovation_carrier','carrier_index')
        ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
    """)
    tables: dict = {}
    for r in rows:
        tables.setdefault(r["t"], []).append(r["c"])

    counts = {}
    for t in sorted(tables):
        db = {"carrier": "gkxlumenx_dim", "carrier_org_rel": "gkxlumenx_dim",
              "enterprise_innovation_carrier": "gkxlumenx_dwd", "carrier_index": "gkxlumenx_ads"}[t]
        counts[t] = q(conn, f"SELECT COUNT(*) AS n FROM {db}.{t}")[0]["n"]

    rel_domain = q(conn, """
        SELECT rel_type, COUNT(*) AS n,
               SUM(CASE WHEN end_date IS NULL THEN 1 ELSE 0 END) AS open_rels,
               MIN(start_date) AS mn, MAX(start_date) AS mx
        FROM gkxlumenx_dim.carrier_org_rel GROUP BY rel_type ORDER BY rel_type
    """)
    carrier_types = q(conn, """
        SELECT carrier_type, carrier_level, COUNT(*) AS n
        FROM gkxlumenx_dim.carrier GROUP BY carrier_type, carrier_level
        ORDER BY carrier_type, carrier_level
    """)
    conn.close()

    eic_cols = tables.get("enterprise_innovation_carrier", [])
    ci_cols = tables.get("carrier_index", [])
    grad_eic = sorted(c for c in eic_cols if any(k in c.lower() for k in FAMILIES))
    grad_ci = sorted(c for c in ci_cols if any(k in c.lower() for k in FAMILIES))
    rel_types = sorted(r["rel_type"] for r in rel_domain)
    tenant_rows = next((r for r in rel_domain if r["rel_type"] == "tenant"), None)

    assert counts.get("carrier", 0) == 28 and counts.get("carrier_org_rel", 0) == 57
    assert rel_types == ["self", "tenant"]
    assert grad_eic == [] and grad_ci == []

    out = {
        "metric_id": "M_SCIUI_SOFTSCI_007",
        "batch": "S3-07-L2",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/incubation-carrier/components/IncubationCarrierPage.jsx:1009",
        ],
        "facts": {
            "ui_mount": "IncubationCarrierPage.jsx:1009 SoftChartFrame title=孵化毕业统计 badge=在孵 vs 毕业",
            "ui_build_fn": "IncubationCarrierPage.jsx:657 buildIncubationGraduationOption：在孵企业(bar,stack)+已毕业(bar,stack)+毕业率(line,右轴max=100)",
            "ui_rate_formula": "IncubationCarrierPage.jsx:710 Math.round(d.graduated/(d.inIncubation+d.graduated)*100)",
            "ui_mock_data": "incubationCarrierMock.js:279-284 五载体 inIncubation/graduated：(86,24)(112,38)(64,19)(58,12)(72,16)",
            "ui_mock_note": "mock 为演示值不参与判档；五载体毕业率=22/25/23/17/18%，均值 21%（ui_demo_fallback 披露）",
            "dev_table_total": 542,
            "dev_carrier_tables": {t: {"columns": tables[t], "rows": counts[t]} for t in sorted(tables)},
            "dev_dim_carrier_rows": counts.get("carrier", 0),
            "dev_dim_carrier_types": carrier_types,
            "dev_carrier_rel_rows": counts.get("carrier_org_rel", 0),
            "dev_carrier_rel_type_domain": rel_domain,
            "dev_graduation_columns_eic": grad_eic,
            "dev_graduation_columns_ci": grad_ci,
            "dev_empty_indicator_tables": ["gkxlumenx_dwd.enterprise_innovation_carrier=0", "gkxlumenx_ads.carrier_index=0"],
            "gkx_table_count": 280,
            "jiuxin_table_count_live": 218,
            "srs_anchor": None,
            "named_in_srs": False,
            "named_note": "三份说明书未出现「孵化毕业统计/毕业率」指标名（检索记录附录 A）。",
        },
        "derived": [
            {
                "name": "carrier_in_incubation_approx",
                "value": tenant_rows["n"] if tenant_rows else None,
                "formula": "COUNT(*) WHERE rel_type='tenant' AND end_date IS NULL（在驻近似在孵）",
                "disclosure": "tenant 在驻关系 ≠ 在孵企业认定（在孵需注册+入驻协议+科技型属性），近似口径 ui_demo_fallback 披露",
            },
            {
                "name": "graduation_counts_and_rate",
                "value": None,
                "reason": "毕业语义零承载：rel_type 域={self,tenant} 无毕业态、end_date 全 NULL、无毕业企业名单表",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 incub/hatch/carrier/graduat 词族", "source": "dev",
             "sql": "information_schema.columns 词族扫描（_probe_s307_l2 快照）",
             "hits": 4, "hit_tables": ["gkxlumenx_ads.carrier_index", "gkxlumenx_dim.carrier", "gkxlumenx_dim.carrier_org_rel", "gkxlumenx_dwd.enterprise_innovation_carrier"]},
            {"probe": "gkx 280 表 incub/hatch/carrier/graduat 词族", "source": "gkx",
             "sql": "information_schema.columns 词族扫描（快照）", "hits": 0},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）incub/hatch/carrier/graduat 词族", "source": "jiuxin",
             "sql": "SHOW TABLES+列扫描（快照）", "hits": 0},
        ],
        "support_judgment": "部分支持",
        "notes": [
            "判档理由：载体维（dim.carrier 28 行 university/research）+ 在驻关系（carrier_org_rel tenant=39）可算「在孵(近似)」柱；「已毕业」柱与「毕业率」线零承载——毕业语义需 rel_type 毕业态或毕业企业名单表，三源均无。三系列缺二，判部分支持。",
            "口径转换点：UI 毕业率分母=在孵+已毕业（期末口径）；权威口径（火炬 2019 指标体系 2.2/黄石 2.2/工信部 2025 六(八)）= 考核期毕业企业数 ÷ 在孵企业总数，接入时需转换。",
            "同族关联：INCUB_012（在孵企业毕业率，IncubationCarrierNewPage.jsx:1396）同根因不同页挂载，各自独立留证；INCUB_015 修复建议已引本件。",
            "mock 五载体（86/24、112/38、64/19、58/12、72/16）为演示值（ui_demo_fallback 披露）。",
            "本件为薄壳：复用共享快照 + dev 载体链路四表实连复核（行数/列清单/rel_type 域断言）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "carrier_org_rel.start_date 仅 2024-01-01 单值（tenant 39 行同日），无年度序列；enterprise_innovation_carrier/carrier_index 0 行无 stat_period 可用。接入毕业数据后首个完整考核年为基期。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "5", "28", "57", "39", "18", "2024-01-01", "86", "24", "112", "38", "64", "19", "58", "12", "72", "16",
            "22", "25", "23", "17", "21", "542", "280", "218", "4", "2", "6", "10", "1000", "500", "20", "30", "50", "75",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("written:", OUT)
    print("judgment: 部分支持 | carrier=28 rel=57 tenant=", tenant_rows["n"] if tenant_rows else None,
          "| grad_cols:", grad_eic, grad_ci, "| empty:", out["facts"]["dev_empty_indicator_tables"])


if __name__ == "__main__":
    main()
