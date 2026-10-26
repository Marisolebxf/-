#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_REGIONAL_COUNT_TOPIC 区域企业数量规模占比（20261021 改源版）。

口径正本：gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REGIONAL_COUNT_TOPIC.md
  stat_year × region_key COUNT + share；region_key = nation/province/city/area/scope。

本件只读快照，不连数据库。底册无 stat_year、无 region_id：
  - 以「成立年队列」代理年度（当年成立且仍在底册的企业数），并同时给存量数；
  - 区域键由 province/city 中文名映射，复合 scope 用 region_scope_member 15 行定义；
  - 分子分母同源：分母 = 同一年队列的家数，分子 = 该区域同年家数。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _w13e3_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_REGIONAL_COUNT_TOPIC_out.json")
ID = "M_ENT_REGIONAL_COUNT_TOPIC"


def main():
    base = C.base_panel()
    probe = C.load("w13e3_probe_20261023.json")
    scope = C.load("w13e3_region_scope_20261023.json")
    ch = C.chain_panel()

    years = [str(y) for y in range(C.YEAR_MIN, C.YEAR_MAX + 1)]
    year_panel = []
    for y in years:
        n = base["year_total"][y]
        city = base["year_city"][y]
        share = base["year_share_pct"][y]
        year_panel.append({
            "year": int(y),
            "cohort_cnt": n,
            "stock_cnt": base["stock_total"][y],
            "city_cnt": city,
            "city_share_pct": share,
            "scope_cnt": base["year_scope"][y],
            "scope_share_pct": {k: C.pct(v, n, 2) for k, v in base["year_scope"][y].items()},
        })

    y2025 = base["year_total"]["2025"]
    c2025 = base["year_city"]["2025"]
    s2025 = base["year_share_pct"]["2025"]
    top4_sum = sum(c2025.values())
    gd_2025 = base["year_scope"]["2025"]["gba"]

    city_rows = [{"city": k, "n": v, "share_pct": C.pct(v, base["n_rows"], 4)}
                 for k, v in list(base["city_total"].items())[:12]]
    prov_rows = [{"province": k, "n": v, "share_pct": C.pct(v, base["n_rows"], 4)}
                 for k, v in list(base["prov_total"].items())[:12]]

    result = {
        "base_rows": base["n_rows"],
        "credit_ok_rows": probe["G_base"]["credit_ok"],
        "bad_credit_rows": base["n_rows"] - probe["G_base"]["credit_ok"],
        "year_present_rows": base["n_year_present"],
        "year_missing_rows": base["n_year_missing"],
        "year_min": base["year_min"],
        "year_max": base["year_max"],
        "n_provinces": base["n_province"],
        "n_cities": base["n_city"],
        "guangdong_rows": base["prov_total"].get("广东省", 0),
        "guangdong_share_pct": C.pct(base["prov_total"].get("广东省", 0), base["n_rows"], 4),
        "nation_rows": base["n_rows"],
        "outside_guangdong_rows": base["n_rows"] - base["prov_total"].get("广东省", 0),
        "year_panel": year_panel,
        "y2025": {
            "cohort_cnt": y2025,
            "stock_cnt": base["stock_total"]["2025"],
            "city_cnt": c2025,
            "city_share_pct": s2025,
            "top4_sum": top4_sum,
            "top4_share_pct": C.pct(top4_sum, y2025, 2),
            "guangdong_share_pct": C.pct(gd_2025, y2025, 2),
            "scope_cnt": base["year_scope"]["2025"],
        },
        "y2024": {
            "cohort_cnt": base["year_total"]["2024"],
            "stock_cnt": base["stock_total"]["2024"],
            "city_cnt": base["year_city"]["2024"],
            "city_share_pct": base["year_share_pct"]["2024"],
            "scope_cnt": base["year_scope"]["2024"],
        },
        "y2015": {
            "cohort_cnt": base["year_total"]["2015"],
            "city_cnt": base["year_city"]["2015"],
            "city_share_pct": base["year_share_pct"]["2015"],
        },
        "share_change_2015_2025_pp": {
            k: round(s2025[k] - base["year_share_pct"]["2015"][k], 2) for k in C.FOCUS_CITIES
        },
        "city_total_top12": city_rows,
        "province_total_top12": prov_rows,
        "scope_total": base["scope_total"],
        "scope_share_of_nation_pct": {k: C.pct(v, base["n_rows"], 4) for k, v in base["scope_total"].items()},
        "region_key": {
            "declared": "nation:CN / province 2 位 / city 4 位 / area 6 位 / scope:gba|yrd|jjj",
            "implemented": "province 中文名 / city 中文名 / scope 成员表",
            "adcode_available_in_base": False,
            "gkx_region_id_column": probe["A_schema_scan"]["columns"]["column_hits"]["region_id"],
            "gkx_region_scope_tables": probe["A_schema_scan"]["tables"]["table_name_hits"]["region_scope"],
            "live_region_scope_tables": probe["F_live"]["table_name_hits"]["region_scope"],
            "live_region_scope_member_rows": probe["F_live"]["exact_counts"].get("gkxlumenx_dim.region_scope_member"),
            "scope_members": scope["scopes"],
            "gba_member_n": len(scope["scopes"][0]["members"]),
            "gba_missing_vs_9_city": "441200（肇庆市）不在 region_scope_member 的 gba 成员里",
            "area_level_available": False,
            "area_note": "底册 area 有值但本地快照未带区县；ent_base_geo 有 152 组省/市/区但无年键，无法做年×区县。",
        },
        "stat_year": {
            "declared": "批次自然年快照（该年末仍有效的名录）",
            "implemented": "成立年队列（incorporation_date 的年份）",
            "has_stat_year_column": False,
            "note": "底册是当前名录，不是逐年快照；成立年不等于名录年，故这里算的是「存活队列」，不是当年新增。",
        },
        "industry_filter": {
            "declared": "先经 enterprise_industry_chain，按所选产业过滤",
            "local_name_match_rows": ch["base_matched_names"],
            "local_name_match_share_pct": ch["base_matched_share_pct"],
            "note": "本地快照只能按企业名对上专利申请人名，覆盖 11.63%，不是完整 credit_code 连接；产业过滤后不能当全量口径。",
        },
        "share_basis": {
            "molecule": "某区域在 y 年的队列家数",
            "denominator": "同一年全国队列家数（同源同过滤）",
            "closure_check": "2025 年四市合计 3,061 = 当年队列 3,061，份额合计 100.00%",
            "closure_holds": top4_sum == y2025,
        },
    }

    out = {
        "metric_id": ID,
        "metric_name": "区域企业数量规模占比",
        "script": ID + ".py",
        "as_of": C.AS_OF,
        "source": {
            "db": C.DB_GKX,
            "snapshots": [
                "code/_snapshots21/base_20261021.json",
                "code/_snapshots21/chain_firm_index_20261023.json",
                "code/_snapshots21/w13e3_probe_20261023.json",
                "code/_snapshots21/w13e3_region_scope_20261023.json",
            ],
        },
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REGIONAL_COUNT_TOPIC.md",
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_constructed",
        "four_judgment": {
            "表结构直接支持（开发库+三方库）": "否：两库均无 enterprise_region_year_dist 结果表",
            "表数据直接支持（开发库+三方库）": "否：无结果表；底册无 stat_year、无 region_id",
            "依赖表结构支持（开发库/三方库）": "是：gkx 底册有 province/city/area 与成立日期；live 有 region_scope_member 15 行",
            "依赖表数据支持（开发库/三方库）": "是（家数与份额）/否（年度名录、区县年度、完整产业过滤）：底册 189,116 行、99.82% 在广东",
        },
        "base_years_used": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": "2015—2026 每年都有成立年记录，故 missing 为空；2026 是残年（仅 122 家），"
                            "在面板中保留但不用于趋势结论。1900—2014 的历史队列存在但不进入本件展示窗口，"
                            "因此不列为 missing。",
        "result": result,
        "notes": [
            "年度键是成立年，不是名录快照年：数值是「当年成立且今天仍在底册」的存活队列，不能当当年新增。",
            "底册 99.82% 在广东，全国/长三角/京津冀份额是底册内的份额，不是全国企业分布。",
            "gba 成员 8 市（缺肇庆），底册只覆盖其中 4 市，2025 年 GBA 家数与广东家数相同。",
            "份额分子分母同源：都用同一年同一过滤下的家数；2025 年四市合计恰为 3,061，闭合 100.00%。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", OUT)
    print("2025", y2025, c2025, s2025, "top4", top4_sum, "GD", gd_2025)
    print("scope", base["scope_total"])
    print("2015", base["year_city"]["2015"], base["year_share_pct"]["2015"])


if __name__ == "__main__":
    main()
