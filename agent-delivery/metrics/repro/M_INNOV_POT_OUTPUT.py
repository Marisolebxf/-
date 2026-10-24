#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_POT_OUTPUT｜产业产值（本件按派单书重建为「创新产出」读数）。

零 SQL：只读两份已落盘快照。
  - `code/_snapshots21/patent_panel_innov_20261021.json`（dwd_patent 全量 2,939,895 行）
  - `code/_snapshots21/f3_facts_20261023.json`（dwd_zh_paper 年份分布、负证据）

口径边界（必须写进正文）：
  1. 专利/论文产出量可现算；
  2. `svc_org_card` 在 gkx 逐字命中 0 张表 → **服务机构产出维拒拟**，
     不拿 `dwd_org_base_info` / `dwd_org_org_product_info` 的机构数冒充产出量；
  3. 注册表原定义是「特定产业总产值/增加值/利润」，gkx 无经济产出表，
     本件只交创新产出（专利/论文），产业产值本体判不可算，见 `registry_gap`。

运行：`cd code && python3 M_INNOV_POT_OUTPUT.py`
产物：`code/M_INNOV_POT_OUTPUT_out.json`
"""
from __future__ import annotations

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_POT_OUTPUT_out.json")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def derive(num, den, note, digits=4):
    return {
        "value": round(num / den, digits) if den else None,
        "numerator": num,
        "denominator": den,
        "denominator_note": note,
    }


def pct(num, den, note, digits=4):
    return {
        "value": round(num / den * 100, digits) if den else None,
        "numerator": num,
        "denominator": den,
        "denominator_note": note,
    }


def main() -> None:
    pat = load("patent_panel_innov_20261021.json")
    f3 = load("f3_facts_20261023.json")

    patent_year = {str(k): int(v) for k, v in pat["year_all"].items()}
    patent_total = int(pat["rows"])
    patent_ipc = int(sum(pat["ipc_all"].values()))
    paper_year = {str(k): int(v) for k, v in f3["dwd_zh_paper_year"].items()}
    paper_total = sum(paper_year.values())

    p2021_2024 = sum(patent_year[str(y)] for y in (2021, 2022, 2023, 2024))
    a2021_2023 = sum(paper_year.get(str(y), 0) for y in (2021, 2022, 2023))
    a2024 = paper_year.get("2024", 0)
    a2023 = paper_year.get("2023", 0)

    patent_cagr = (patent_year["2024"] / patent_year["2021"]) ** (1 / 3) - 1
    paper_cagr = (paper_year["2023"] / paper_year["2021"]) ** (1 / 2) - 1

    derived = {
        "patent_2021_2024_share_pct": pct(
            p2021_2024, patent_total,
            "分母 = 专利公开总量 2,939,895 件（patent_panel_innov.rows）"),
        "patent_ipc_coverage_pct": pct(
            patent_ipc, patent_total,
            "分母 = 专利公开总量；分子 = 主分类 IPC 非空件数 2,420,915（ipc_all 求和）"),
        "patent_cagr_2021_2024_pct": {
            "value": round(patent_cagr * 100, 4),
            "numerator": patent_year["2024"],
            "denominator": patent_year["2021"],
            "denominator_note": (
                "CAGR = (分子 / 分母)^(1/3) − 1；分子 = 2024 年 606,468 件，"
                "分母 = 2021 年 604,512 件，不是全库总量"),
        },
        "paper_2021_2023_share_pct": pct(
            a2021_2023, paper_total,
            "分母 = 中文论文全库 100,900 篇（f3_facts.dwd_zh_paper_year 求和）"),
        "paper_2024_share_pct": pct(
            a2024, paper_total,
            "分母 = 中文论文全库；分子 = 2024 年 32,379 篇（入库批次峰）"),
        "paper_2024_vs_2023_multiple": {
            "value": round(a2024 / a2023, 4),
            "numerator": a2024,
            "denominator": a2023,
            "denominator_note": "分母 = 2023 年 6,651 篇；倍率不是增幅，未减 1",
        },
        "paper_cagr_2021_2023_pct": {
            "value": round(paper_cagr * 100, 4),
            "numerator": paper_year["2023"],
            "denominator": paper_year["2021"],
            "denominator_note": (
                "CAGR = (分子 / 分母)^(1/2) − 1；分子 = 2023 年 6,651 篇，"
                "分母 = 2021 年 6,758 篇，窗口刻意不含 2024 批次峰"),
        },
    }

    out = {
        "metric_id": "M_INNOV_POT_OUTPUT",
        "metric_name_zh": "产业产值（重建为创新产出读数：专利/论文）",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "partial_missing_dimension",
        "judgment_reason": (
            "专利与论文两个产出维都能从 gkx 现算（2,939,895 件 / 100,900 篇），"
            "但服务机构产出维的源表 `svc_org_card` 在 gkx 逐字命中 0 张表，整维拒拟；"
            "注册表原定义「产业总产值/增加值/利润」也没有经济产出表可算。"
            "有整维缺失，故判部分支持，不判完全转换支持。"
        ),
        "sources": [
            {"path": "code/_snapshots21/patent_panel_innov_20261021.json",
             "what": "dwd_patent 全量 2,939,895 行的 apdt_year 与 IPC4 聚合"},
            {"path": "code/_snapshots21/f3_facts_20261023.json",
             "what": "dwd_zh_paper 年份分布、svc_org_card 负证据、论文分类覆盖"},
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "专利侧 2017—2020 在 dwd_patent.apdt_year 零行，不按 0 摊入；2025（440,401）"
            "与 2026（74,810）是采集残年，不进 CAGR。论文侧基期取 2021—2023，"
            "2024 是入库批次峰（32,379 篇，占全库 32.09%），不摊入趋势；2025/2026 为残年。"
        ),
        "total": {
            "patent_rows": patent_total,
            "patent_with_ipc": patent_ipc,
            "paper_rows": paper_total,
            "patent_2021_2024": p2021_2024,
            "paper_2021_2023": a2021_2023,
        },
        "patent_year_counts": patent_year,
        "paper_year_counts": {str(y): paper_year[str(y)]
                              for y in range(2019, 2027) if str(y) in paper_year},
        "paper_type_dist": f3["dwd_zh_paper_type"],
        "service_org_output": {
            "status": "rejected",
            "source_table": "svc_org_card",
            "absence_hits": f3["absence_probe"]["svc_org_card"]["hits"],
            "absence_condition": f3["absence_probe"]["svc_org_card"]["condition"],
            "pool_rows_seen": f3["dwd_org_org_product_info"]["rows"],
            "pool_orgs_seen": f3["dwd_org_org_product_info"]["distinct_org"],
            "not_used_as_output": True,
            "reason": (
                "`dwd_org_org_product_info` 只有服务机构名录与业务描述（45,011 行 / 44,153 家），"
                "没有营收、服务量、项目数等产出字段；机构数不是产出量，禁止冒充。"
            ),
        },
        "registry_gap": {
            "registry_definition": "特定产业总产值、增加值、利润；按时间/地域/企业类型看趋势。ADS 经济统计读面。",
            "gkx_economic_output_table": None,
            "status": "不可算",
            "note": (
                "gkx 280 张表里没有产业总产值/增加值/利润结果面；本件按派单书把「产出」落到"
                "专利/论文两个创新产出维，产业产值本体仍缺，待甲方裁定是否改口径。"
            ),
        },
        "derived": derived,
        "absence_probe": {
            "svc_org_card": f3["absence_probe"]["svc_org_card"],
        },
        "reproduce": "cd code && python3 M_INNOV_POT_OUTPUT.py",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {OUT} patent={patent_total} paper={paper_total} "
          f"p2021_2024={p2021_2024} a2021_2023={a2021_2023}")


if __name__ == "__main__":
    main()
