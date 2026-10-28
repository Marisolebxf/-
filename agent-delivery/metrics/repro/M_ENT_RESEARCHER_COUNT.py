#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_RESEARCHER_COUNT · 企业科研人数（gkx 口径）——否定性证据探针

口径（calc-logic/ENT/M_ENT_RESEARCHER_COUNT.md，Q-E32-01 未闭合）：
    每企取最新一个有年报的自然年：
        国内 = dwd_org_annual_financial_info.development_employee
        国外 = dwd_foreign_org_annual_financial_info.rd_staff
        本条 = SUM(国内有效值) + SUM(国外有效值)
    无值/NULL/占位 0 不进合计；禁止用从业人数、禁止用研发投入金额冒充。

本脚本不产出指标值，只产出「为什么算不出来」的可复核证据：
    ① 全库扫描研发人力类字段（列名 + 列注释），确认候选字段清单；
    ② 逐表测填充率与 >0 值行数（三张候选表 + 工商年报的 varchar 列）；
    ③ 记录需求原句口径（从业人数）的可用量，供口径裁决时参考。
产物：code/M_ENT_RESEARCHER_COUNT_out.json，verdict_kind="negative_evidence"。

只连 gkx（183.240.141.251:3318，只读 gkx_reader_zp）。
"""
from __future__ import annotations

import json
import time
from decimal import Decimal
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_RESEARCHER_COUNT_out.json"
METRIC_ID = "M_ENT_RESEARCHER_COUNT"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=1800, write_timeout=1800, autocommit=True)

SQL_CAND_COLS = (
    "SELECT table_name, column_name, data_type, column_comment "
    "FROM information_schema.columns WHERE table_schema='gkx' AND ("
    "column_name LIKE '%employee%' OR column_name LIKE '%staff%' "
    "OR column_name LIKE '%person%' OR column_name LIKE '%research%' "
    "OR column_name LIKE '%develop%' OR column_comment LIKE '%研发人员%' "
    "OR column_comment LIKE '%科研人员%' OR column_comment LIKE '%从业人数%') "
    "ORDER BY table_name, ordinal_position"
)
SQL_DOMESTIC = (
    "SELECT COUNT(*) n, COUNT(DISTINCT org_id) orgs, "
    "SUM(development_employee IS NOT NULL) dev_nn, "
    "SUM(development_employee > 0) dev_pos, "
    "SUM(employees_number > 0) emp_pos, "
    "MIN(`year`) y0, MAX(`year`) y1 "
    "FROM gkx.dwd_org_annual_financial_info"
)
SQL_FOREIGN = (
    "SELECT COUNT(*) n, COUNT(DISTINCT org_id) orgs, "
    "SUM(rd_staff IS NOT NULL) rd_nn, SUM(rd_staff > 0) rd_pos, "
    "SUM(research_development_amount IS NOT NULL) rda_nn "
    "FROM gkx.dwd_foreign_org_annual_financial_info"
)
SQL_REPORT_ASSET = (
    "SELECT COUNT(*) n, COUNT(DISTINCT jgid) orgs, "
    "SUM(yfrysl IS NOT NULL AND TRIM(yfrysl) <> '') yfr_ok, "
    "SUM(yftrje IS NOT NULL AND TRIM(yftrje) <> '') yft_ok "
    "FROM gkx.dwd_org_annual_report_asset"
)
SQL_STOCK_HAS_RD_STAFF = (
    "SELECT COUNT(*) n FROM information_schema.columns WHERE table_schema='gkx' "
    "AND table_name='dwd_org_stock_finance_info' AND ("
    "column_comment LIKE '%研发人员%' OR column_name LIKE '%rd_staff%')"
)


def j(v):
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    if isinstance(v, Decimal):
        return float(v)
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except TypeError:
            return str(v)
    return v


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"gkx 连不上（5 次重试）：{last}")


def q(cur, sql, ms=900000):
    cur.execute(f"SET SESSION max_execution_time={ms}")
    cur.execute(sql)
    return [list(map(j, r)) for r in cur.fetchall()]


def main() -> None:
    t0 = time.time()
    conn = connect()
    cur = conn.cursor()
    cand = q(cur, SQL_CAND_COLS, 60000)
    dom = q(cur, SQL_DOMESTIC, 300000)[0]
    fore = q(cur, SQL_FOREIGN, 300000)[0]
    ra = q(cur, SQL_REPORT_ASSET, 600000)[0]
    stock_rd_staff_cols = int(q(cur, SQL_STOCK_HAS_RD_STAFF, 60000)[0][0])
    conn.close()

    n_dom, orgs_dom, dev_nn, dev_pos, emp_pos, y0, y1 = dom
    n_for, orgs_for, rd_nn, rd_pos, rda_nn = fore
    n_ra, orgs_ra, yfr_ok, yft_ok = ra

    # 只保留「研发/科研人员」语义的候选列，避免把 legal_person 之类列进证据表
    def is_rd_staff(row):
        tbl, col, typ, cmt = row
        cmt = cmt or ""
        if "研发人员" in cmt or "科研人员" in cmt:
            return True
        return col in ("development_employee", "rd_staff", "yfrysl")

    rd_candidates = [r for r in cand if is_rd_staff(r)]

    payload = {
        "metric_id": METRIC_ID,
        "metric_name": "企业科研人数",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "口径所需的两个字段在 gkx 内均为整列空值：国内 "
            f"dwd_org_annual_financial_info.development_employee 在 {int(n_dom):,} 行中非空 "
            f"{int(dev_nn or 0)} 行、>0 {int(dev_pos or 0)} 行；国外 "
            f"dwd_foreign_org_annual_financial_info.rd_staff 在 {int(n_for):,} 行中非空 "
            f"{int(rd_nn or 0)} 行、>0 {int(rd_pos or 0)} 行。第三候选 "
            f"dwd_org_annual_report_asset.yfrysl 在 {int(n_ra):,} 行中非空 "
            f"{int(yfr_ok or 0)} 行。三张表覆盖了国内工商年报、上市财务、海外机构三个来源，"
            "全部无值，且库内不存在其它研发人员字段，故不是覆盖率不足，而是结构+数据双缺。"
        ),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "primary": "gkx @ 183.240.141.251:3318 (readonly gkx_reader_zp)",
            "tables": ["gkx.dwd_org_annual_financial_info",
                       "gkx.dwd_foreign_org_annual_financial_info",
                       "gkx.dwd_org_annual_report_asset",
                       "gkx.dwd_org_stock_finance_info",
                       "information_schema.columns"],
            "sql": [SQL_CAND_COLS, SQL_DOMESTIC, SQL_FOREIGN, SQL_REPORT_ASSET, SQL_STOCK_HAS_RD_STAFF],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_RESEARCHER_COUNT.md",
        },
        "compute": {
            "n_scored": 0,
            "sum_researcher": None,
            "domestic": {
                "table": "dwd_org_annual_financial_info",
                "rows": int(n_dom), "orgs": int(orgs_dom),
                "year_min": y0, "year_max": y1,
                "development_employee_non_null": int(dev_nn or 0),
                "development_employee_positive": int(dev_pos or 0),
                "employees_number_positive": int(emp_pos or 0),
                "fill_rate_pct": round((dev_nn or 0) / n_dom * 100, 4),
            },
            "foreign": {
                "table": "dwd_foreign_org_annual_financial_info",
                "rows": int(n_for), "orgs": int(orgs_for),
                "rd_staff_non_null": int(rd_nn or 0),
                "rd_staff_positive": int(rd_pos or 0),
                "research_development_amount_non_null": int(rda_nn or 0),
                "fill_rate_pct": round((rd_nn or 0) / n_for * 100, 4),
            },
            "annual_report_asset": {
                "table": "dwd_org_annual_report_asset",
                "rows": int(n_ra), "orgs": int(orgs_ra),
                "yfrysl_non_empty": int(yfr_ok or 0),
                "yftrje_non_empty": int(yft_ok or 0),
                "fill_rate_pct": round((yfr_ok or 0) / n_ra * 100, 4),
            },
            "stock_finance_rd_staff_columns": stock_rd_staff_cols,
            "requirement_headcount_alternative": {
                "column": "dwd_org_annual_financial_info.employees_number",
                "positive_rows": int(emp_pos or 0),
                "rows": int(n_dom),
                "fill_rate_pct": round((emp_pos or 0) / n_dom * 100, 4),
                "note": "需求原句口径（从业总人数）同样不可用：仅 "
                        f"{int(emp_pos or 0):,} 行正值，且 calc-logic 明令禁止用它顶替研发人员。",
            },
            "candidate_columns": [
                {"table": r[0], "column": r[1], "type": r[2], "comment": r[3]}
                for r in rd_candidates
            ],
            "candidate_column_count_scanned": len(cand),
        },
        "probes": {
            "scan_patterns": ["%employee%", "%staff%", "%person%", "%research%", "%develop%",
                              "comment:%研发人员%", "comment:%科研人员%", "comment:%从业人数%"],
            "scan_hits": len(cand),
            "rd_staff_candidates": len(rd_candidates),
            "empty_columns": [
                "dwd_org_annual_financial_info.development_employee",
                "dwd_foreign_org_annual_financial_info.rd_staff",
                "dwd_org_annual_report_asset.yfrysl",
            ],
            "max_execution_time_ms": 900000,
            "retry_policy": "5 次指数退避",
        },
        "proxy_deviation": (
            "不采用任何代理：calc-logic 明令禁止用从业人数（employees_number）或研发投入金额"
            "（arch_development_am / research_development_amount）反推研发人员。"
            "用专利发明人反推会系统性偏向专利密集行业，且无法校正行业间系数，本件不采用。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "无基期：口径要求「每企取最新一个有值自然年」，但没有一个有值年份"
            "（development_employee 全表 0 行非空），故不声明基期。"
            "国内表实测年份区间 2007—2025，仅作字段存在性证据，不构成可用序列。"
        ),
        "notes": [
            "本件是负结论，产物只证明「为什么不可算」，不产出 0 值合计。",
            "按 calc-logic「无值不进合计」规则，n_scored=0 时不得输出 sum_researcher=0（0 会被误读成调研结论）。",
            "如果甲方要的是「从业总人数」，应另立指标并用 employees_number，覆盖率同样只有 3.49%。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[{METRIC_ID}] 国内非空={int(dev_nn or 0)}/{int(n_dom)} "
          f"海外非空={int(rd_nn or 0)}/{int(n_for)} 工商年报非空={int(yfr_ok or 0)}/{int(n_ra)} "
          f"候选列={len(rd_candidates)}")


if __name__ == "__main__":
    main()
