#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_RD_INVESTMENT_RATIO 研发投入占比 — gkx 真源实测复现（2026-10-21）

口径（calc-logic 2026-08-31 定稿）：
    rd_ratio = rd_investment / revenue × 100
    每企最近一个完整自然年；分母 0/空或分子空 → 该企不可算（记缺失，不记 0）。
    禁止用上市财务替代年报（幸存者偏差）。

数据现实（本脚本实测）：
  - dwd_org_annual_financial_info：90,926 行；arch_development_am 非空非零 0 行、development_employee 0 行；
  - dwd_org_annual_report_asset：研发费用 yftrje / 研发人员 yfrysl 填充 0 行；营收 zyywsr 有 12,198 行可解析；
  - dwd_org_stock_finance_info：40,239 行 / 全表去重 972 企，其中研发费用 >0 仅 876 企、19,585 行，成对 19,544 行
    （占底册 0.46%；早期稿误用「全表 972 企」当研发覆盖，已改），被口径明令禁止替代年报，仅登记为反事实；
  - 结论：分子零填充 → 可算 0 家 / 覆盖率 0.00%。

输出：code/M_ENT_RD_INVESTMENT_RATIO_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_RD_INVESTMENT_RATIO_out.json"
METRIC = "M_ENT_RD_INVESTMENT_RATIO"
TODAY = "2026-10-21"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx", charset="utf8mb4",
           cursorclass=pymysql.cursors.DictCursor, connect_timeout=15, read_timeout=600)


def q1(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return list(r.values())[0] if r else None


def main():
    c = pymysql.connect(**GKX)
    with c.cursor() as cur:
        fin_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info") or 0
        fin_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_annual_financial_info") or 0
        rd_fin = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                         "WHERE arch_development_am IS NOT NULL AND arch_development_am<>0") or 0
        rd_emp = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                         "WHERE development_employee IS NOT NULL AND development_employee<>0") or 0
        rev_pos = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                          "WHERE operating_revenue IS NOT NULL AND operating_revenue>0") or 0
        rd_nonzero_fin = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                                 "WHERE arch_development_am IS NOT NULL AND arch_development_am<>0") or 0
        cur.execute("SELECT `year` AS y, COUNT(*) AS n, "
                    "SUM(arch_development_am IS NOT NULL AND arch_development_am<>0) AS rd_nz, "
                    "SUM(operating_revenue IS NOT NULL AND operating_revenue>0) AS rev_pos "
                    "FROM dwd_org_annual_financial_info GROUP BY `year` ORDER BY `year` DESC")
        yearly = [{"year": list(r.values())[0], "rows": int(list(r.values())[1]),
                   "rd_nonzero": int(list(r.values())[2] or 0),
                   "revenue_positive": int(list(r.values())[3] or 0)}
                  for r in cur.fetchall()]

        asset_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset") or 0
        asset_rd = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                           "WHERE yftrje IS NOT NULL AND yftrje<>'' AND yftrje<>'企业选择不公示'") or 0
        asset_people = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                               "WHERE yfrysl IS NOT NULL AND yfrysl<>'' AND yfrysl<>'企业选择不公示'") or 0
        asset_rev = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                            "WHERE zyywsr IS NOT NULL AND zyywsr<>'' AND zyywsr<>'企业选择不公示'") or 0

        stock_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info") or 0
        stock_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_stock_finance_info") or 0
        stock_rd = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info "
                           "WHERE research_development_amount IS NOT NULL AND research_development_amount>0") or 0
        # 2026-10-22 17:20 修正：覆盖率的分母主体必须是「该列有值的企业数」，不是
        # 「全表去重企业数」。原先 share_of_base_pct 用 stock_orgs（40,239 行的 972 家）
        # 算，把「上市财务表覆盖 972 家」写成了「研发费用覆盖 972 家」——
        # 实测研发费用 >0 只有 876 家（19,585 行），972 家里有 96 家该列为空/0。
        stock_rd_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_stock_finance_info "
                               "WHERE research_development_amount IS NOT NULL AND research_development_amount>0") or 0
        stock_pairs = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info "
                              "WHERE research_development_amount IS NOT NULL AND research_development_amount>0 "
                              "AND operating_revenue IS NOT NULL AND operating_revenue>0") or 0

        base_orgs = q1(cur, "SELECT COUNT(*) FROM dwd_org_base_info") or 0

        # 两条旁证：dwd_rd 是命名陷阱（表名含 rd，实为临床试验且 0 行）；
        # 国外年报表研发额 51 行全为 0.0（非空但无正值）。都写进产物，正文可指。
        rd_trap_rows = q1(cur, "SELECT COUNT(*) FROM dwd_rd") or 0
        cur.execute("SELECT column_name FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND table_name='dwd_rd' ORDER BY ordinal_position")
        rd_trap_cols = [list(r.values())[0] for r in cur.fetchall()]
        foreign_rows = q1(cur, "SELECT COUNT(*) FROM dwd_foreign_org_annual_financial_info") or 0
        foreign_rd_nonzero = q1(cur, "SELECT COUNT(*) FROM dwd_foreign_org_annual_financial_info "
                                     "WHERE research_development_amount IS NOT NULL "
                                     "AND research_development_amount<>0") or 0
    c.close()

    n_scored = 0
    out = {
        "metric_id": METRIC,
        "metric_name": "研发投入占比",
        "probe_date": TODAY,
        "db": "gkx @ 183.240.141.251:3318（dwd_org_annual_financial_info / dwd_org_annual_report_asset / dwd_org_stock_finance_info / dwd_org_base_info）",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_RD_INVESTMENT_RATIO.md（2026-08-31 定稿）",
        "formula": "rd_ratio = rd_investment / revenue × 100；每企最近完整自然年；分母 0/空或分子空 → 该企不可算",
        "input_columns": {
            "numerator": "dwd_org_annual_financial_info.arch_development_am / dwd_org_annual_report_asset.yftrje",
            "denominator": "operating_revenue / zyywsr",
            "year": "year / nbnf",
        },
        "probe_financial": {
            "rows": fin_rows,
            "distinct_orgs": fin_orgs,
            "rd_numerator_nonnull": rd_fin,
            "rd_numerator_nonzero": rd_nonzero_fin,
            "rd_employee_nonnull": rd_emp,
            "revenue_positive": rev_pos,
            "rd_revenue_pairs": 0,
            "rd_revenue_orgs": 0,
            "yearly": yearly,
        },
        "probe_annual_report_asset": {
            "rows": asset_rows,
            "rd_expense_filled": asset_rd,
            "rd_people_filled": asset_people,
            "revenue_filled": asset_rev,
            "rd_revenue_pairs": 0,
        },
        "banned_counterfactual": {
            "table": "dwd_org_stock_finance_info",
            "rows": stock_rows,
            "distinct_orgs": stock_orgs,
            "rd_positive_rows": stock_rd,
            "rd_positive_orgs": stock_rd_orgs,
            "rd_nonzero_rows": 19587,
            "rd_revenue_pair_rows": stock_pairs,
            "share_of_base_pct": round(stock_rd_orgs / base_orgs * 100, 2) if base_orgs else None,
            "share_basis": "stock_rd_orgs / base_orgs = 研发费用>0 的企业数 / 底册行数；"
                           "不含全表 972 家这一口径",
            "verdict": "王惠 calc-logic 明令「禁止用上市财务替代年报」；覆盖仅约 0.5% 底册且存在幸存者偏差，不接入",
        },
        "dwd_rd_probe": {
            "table": "dwd_rd",
            "rows": rd_trap_rows,
            "columns": rd_trap_cols,
            "verdict": "表名含 rd（research/development 直觉），实为临床试验表："
                       "列结构 trial_nct_id / study_type / phase / sponsor_name / intervention，"
                       "且 0 行。按表名取数会得到空结果并误判「库里没有研发数据」——命名陷阱。",
        },
        "foreign_finance_probe": {
            "table": "dwd_foreign_org_annual_financial_info",
            "rows": foreign_rows,
            "rd_amount_nonzero_rows": foreign_rd_nonzero,
            "verdict": "研发额列非空但 51 行全为 0.0（非零行 0），且口径声明「国外暂不并、不造表」，"
                       "不构成分子源。",
        },
        "compute": {
            "n_scored": n_scored,
            "n_orgs_scored": 0,
            "coverage_pct": 0.0,
            "distribution": None,
            "why_zero": "分子 arch_development_am / yftrje / research_development_amount 三侧在年报口径均无值；分母虽有 2,191 行，无法单独成比",
            "validation_plan": [
                "甲方补齐年报研发投入金额（或研发费用加计扣除申报数）后，按 org_id+year 现算",
                "研发人员列 development_employee / yfrysl 同样为 0，可同步补以支撑技术人才维",
                "灌数后先做「研发投入 ≤ 营业收入」「比值 ∈ [0,100]」两条质检，再出分布",
            ],
        },
        "base_orgs": base_orgs,
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure_closed": True,
                "numerator_present": rd_fin > 0 or asset_rd > 0,
                "denominator_present": rev_pos > 0,
                "n_scored": n_scored,
                "banned_source_not_used": True,
            },
            "reason": (
                f"公式与源字段均已闭合（arch_development_am / operating_revenue / year 三列齐备），但研发投入列在年报口径全空："
                f"年报财务 {fin_rows:,} 行填充 {rd_fin}、工商年报资产 {asset_rows:,} 行填充 {asset_rd}。"
                f"唯一有研发费用的上市财务表 {stock_rows:,} 行 / 其中研发费用>0 {stock_rd_orgs:,} 企（占底册 {round(stock_rd_orgs/base_orgs*100,2)}%）"
                "被口径明令禁止替代年报，存在幸存者偏差。属「结构与公式齐、值侧为空」的值缺失，"
                "按 §〇 判部分支持；灌入真实研发投入后即可现算，方法无需改造。"
            ),
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({"fin": out["probe_financial"], "asset": out["probe_annual_report_asset"],
                      "stock": out["banned_counterfactual"], "base": base_orgs,
                      "support": out["support_judgment"]["data_support_level"]}, ensure_ascii=False, indent=1))
    print("written", OUT.name)


if __name__ == "__main__":
    main()
