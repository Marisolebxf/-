#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_AVG_RD_INVESTMENT「平均研发投入」→ `code/M_ENT_AVG_RD_INVESTMENT_out.json`

口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_AVG_RD_INVESTMENT.md`）：
    选定产业内全部法人、最近一个完整自然年度 R&D 经费内部支出的算术平均；
    产业键 = 未来产业 cluster_id；成员按 org_id 去重后再 AVG；
    rd 空或占位 0 → 该企不进均；**禁止**用 `dwd_org_stock_finance_info`（覆盖不到全部法人）；
    **禁止**各产业预聚合加总冒充去重平均。

本脚本零 DB，只读族级共享快照 `code/_snapshots21/ent_fin_family_20261023.json`。
核心结论是「口径认的列整列为空」：`dwd_org_annual_financial_info.arch_development_am`
非空 0 行、`development_employee` 非空 0 行，故国内年报口径的研发均值算不出；
快照里的 `stock_rd_chain` 段是**唯一有数的产业切面**，但它违反 calc-logic 的禁用条款，
只能当「若甲方同意放开上市样本口径」的可行性与量级证据，不能当本指标交付值。

重跑：`cd code && python3 M_ENT_AVG_RD_INVESTMENT.py`
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_fin_family_20261023.json")
OUT = os.path.join(HERE, "M_ENT_AVG_RD_INVESTMENT_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    fin, stock, forg, ch = d["annual_fin"], d["stock_fin"], d["forg_fin"], d["stock_rd_chain"]
    base_orgs = d["base"]["orgs"]
    fill = fin["fill"]

    st = stock["rd_latest_stats_yuan"]
    y25 = stock["y2025_dec"]
    headline = {
        "annual_fin_rows": fin["rows"],
        "arch_development_am_nonnull": fill["arch_development_am"]["nonnull"],
        "arch_development_am_nonzero": fill["arch_development_am"]["nonzero"],
        "development_employee_nonnull": fill["development_employee"]["nonnull"],
        "fixed_assets_nonnull": fill["fixed_assets"]["nonnull"],
        "annual_fin_orgs": fin["orgs"],
        "base_orgs": base_orgs,
        "forg_rows": forg["rows"], "forg_rd_positive_rows": forg["rd_pos_rows"],
        "forg_rd_nonnull_rows": forg["rd_nonnull_rows"],
        "stock_rows": stock["rows"], "stock_orgs": stock["orgs"],
        "stock_rd_positive_rows": stock["rd_pos_rows"],
        "stock_rd_positive_orgs": stock["rd_pos_orgs"],
        "stock_rd_zero_rows": stock["rd_zero_rows"],
        "stock_rd_all_zero_orgs": stock["rd_all_zero_orgs"],
        "stock_coverage_pct_of_base": pct(stock["rd_pos_orgs"], base_orgs),
        "rd_any_period_mean_yuan": st["mean"], "rd_any_period_median_yuan": st["median"],
        "rd_any_period_p90_yuan": st["p90"], "rd_any_period_p99_yuan": st["p99"],
        "rd_any_period_max_yuan": st["max"],
        "rd_any_period_org_count": stock["rd_pos_orgs"],
        "rd_any_period_org_period_year": stock["rd_latest_period_year"],
        "y2025_dec_rows": y25["rows"], "y2025_dec_rd_pos_rows": y25["rd_pos_rows"],
        "y2025_dec_rd_sum_yuan": y25["rd_sum_yuan"],
        "y2025_dec_rd_mean_yuan": y25["rd_mean_yuan"],
        "y2025_dec_rd_median_yuan": y25["rd_median_yuan"],
        "y2025_dec_note": "主口径：occur_period=202512 的 FY2025 年报行，645 家研发费>0；"
                          "与 rd_any_period_* 那组（876 家、各取自己最后一个报告期，"
                          "其中 616 家落在 2026 一季报）不可混用",
        "both_rev_rd_orgs": stock["both_rev_rd_orgs"],
        "chain_mapped_orgs": ch["chain_mapped_orgs"],
        "chain_unmapped_orgs": ch["chain_unmapped_orgs"],
        "l1_mapped_orgs": ch["l1_mapped_orgs"],
        "by_chain": ch["by_chain"],
        "by_l1": ch["by_l1"],
        "top10_rd": stock["top10_rd"],
        "chain_sample_note": "FY2025 有研发费的上市样本 %d 家里 %d 家能挂到 12 条未来产业链，%d 家只能挂行业大类 L1；"
                             "链上企业总数取 chain_firms（软件与信息服务 917,842 家），"
                             "样本占比见 listed_sample_cov_pct"
                             % (ch["listed_orgs_with_rd"], ch["chain_mapped_orgs"], ch["chain_unmapped_orgs"]),
    }

    # 12 条链的研发费合计（分子共用；与 derived 里 chain_unmapped_sum_pct 的差额口径一致）
    chain_sum = sum(x["sum_yuan"] for x in ch["by_chain"])

    out = {
        "metric_id": "M_ENT_AVG_RD_INVESTMENT",
        "metric_name": "平均研发投入",
        "support_judgment": "部分支持",
        "judgment_basis": {
            "formula": "AVG(rd_investment) over DISTINCT org_id in selected cluster, latest full year",
            "source_table": "gkx.dwd_org_annual_financial_info.arch_development_am（calc-logic 的 ODS 源）",
            "why_partial": "国内年报研发列整列为空（非空 0 行 / 90,926 行），产业键 cluster_id 在该列上无值可聚合；"
                           "唯一有数的是上市财报表（FY2025 645 家、任一报告期 876 家，占底册 0.4632%），"
                           "而 calc-logic 明禁以它替代——缺口是「非上市法人的研发金额」这一整块",
            "why_not_unsupported": "依赖表、列、机构号、年份键全在，645 家 FY2025 上市样本的均值/中位数"
                                   "与 12 条链的切面均已算出（可作为放开口径后的下界）",
            "why_not_transformed": "缺口不是「加工没做」，而是分子对 99.54% 的法人根本不存在，"
                                   "任何转换都无法把空列变成金额",
        },
        "sources": [
            {"db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp（只读）",
             "table": "gkx.dwd_org_annual_financial_info", "rows": fin["rows"],
             "note": "列级填充率探针：arch_development_am / development_employee / fixed_assets 三列全空"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_stock_finance_info", "rows": stock["rows"],
             "note": "上市研发费，calc-logic 禁用为主口径；本件只作可行性证据"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_foreign_org_annual_financial_info", "rows": forg["rows"],
             "note": "境外研发列 51 行全为 0.0，不可用"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
             "note": "645 个统一社会信用代码的链归属（industry_code 首个 INB 码前 7 位）"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_base_info", "rows": base_orgs,
             "note": "industry_l1_name 行业大类 + 底册规模"},
            {"snapshot": "code/_snapshots21/ent_fin_family_20261023.json",
             "builder": "code/_build_ent_fin_family.py"},
            {"snapshot": "code/_snapshots21/chain_firm_year_20261023.json",
             "note": "12 条链的链名与链上企业总数（分母参照）"},
        ],
        "base_years_used": [2025],
        "base_years_missing": [2020, 2021, 2022, 2023, 2024],
        "base_years_note": "「最近一个完整自然年」= 2025（上市财报表 occur_period=202512 的 743 行年报口径）。"
                           "2026 只有一季报、残年，不进均值；2020—2024 未单年出均值——"
                           "vintage 差异会让同一家企业在不同年份进不同的样本，"
                           "跨年不具可比性，故只取 2025 一个锚年，其余年份显式列为未用",
        "headline": headline,
        "derived": {
            "orgs_without_any_rd": dec(
                base_orgs - stock["rd_pos_orgs"], base_orgs - stock["rd_pos_orgs"], None,
                "计数，无分母：底册 189,116 家 − 任一报告期研发费>0 的上市样本 876 家"
                "（rd_pos_orgs）＝ 没有任何研发费记录的机构规模，是差集不是比例"),
            "fy2025_orgs_without_rd": dec(
                stock["orgs"] - y25["rd_pos_rows"], stock["orgs"] - y25["rd_pos_rows"], None,
                "计数，无分母：上市财务样本 972 家（stock_fin.orgs）− FY2025 研发费>0 的 645 家"
                "（y2025_dec.rd_pos_rows），即无 FY2025 年报或该年研发费为空的 327 家"),
            "fy2025_sum_vs_chain_sum_ratio": dec(
                round(chain_sum / y25["rd_sum_yuan"], 6), chain_sum, y25["rd_sum_yuan"],
                "分子=12 条未来产业链切片研发费合计（by_chain[].sum_yuan 求和，覆盖 495 家）；"
                "分母=FY2025 年报研发费合计 rd_sum_yuan（645 家）。倍率<1 说明 150 家未能挂链，"
                "差额见 chain_unmapped_sum_pct"),
            "fy2025_mean_vs_any_period": dec(
                round(y25["rd_mean_yuan"] / st["mean"], 4), y25["rd_mean_yuan"], st["mean"],
                "分子=FY2025 年报研发费均值 rd_mean_yuan（645 家）；"
                "分母=任一报告期研发费均值 rd_latest_stats_yuan.mean（876 家，各取自己最后一个报告期）。"
                "倍率>1 因 FY2025 单年样本更偏上市大盘股"),
            "fy2025_median_vs_any_period": dec(
                round(y25["rd_median_yuan"] / st["median"], 4), y25["rd_median_yuan"], st["median"],
                "分子=FY2025 年报研发费中位数 rd_median_yuan（645 家）；"
                "分母=任一报告期研发费中位数 rd_latest_stats_yuan.median（876 家）"),
            "chain_mapped_share_pct": dec(
                pct(ch["chain_mapped_orgs"], ch["listed_orgs_with_rd"]),
                ch["chain_mapped_orgs"], ch["listed_orgs_with_rd"],
                "分子=研发费能挂到 12 条未来产业链的上市机构数 chain_mapped_orgs（495 家）；"
                "分母=FY2025 有研发费的上市机构数 listed_orgs_with_rd（645 家）"),
            "fy2025_coverage_pct_of_base": dec(
                pct(y25["rd_pos_rows"], base_orgs), y25["rd_pos_rows"], base_orgs,
                "分子=FY2025 研发费>0 的上市机构数 y2025_dec.rd_pos_rows（645 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "any_period_coverage_pct_of_base": dec(
                pct(stock["rd_pos_orgs"], base_orgs), stock["rd_pos_orgs"], base_orgs,
                "分子=任一报告期研发费>0 的上市机构数 stock_fin.rd_pos_orgs（876 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "any_period_over_fy2025_mean": dec(
                round(st["mean"] / y25["rd_mean_yuan"], 4), st["mean"], y25["rd_mean_yuan"],
                "分子=任一报告期研发费均值（876 家）；分母=FY2025 年报研发费均值（645 家）。"
                "与 fy2025_mean_vs_any_period 互为倒数"),
            "chain_unmapped_sum_pct": dec(
                round((y25["rd_sum_yuan"] - chain_sum) / y25["rd_sum_yuan"] * 100, 4),
                y25["rd_sum_yuan"] - chain_sum, y25["rd_sum_yuan"],
                "分子=未挂链的 150 家 FY2025 研发费合计（rd_sum_yuan − 12 条链 sum_yuan 之和）；"
                "分母=FY2025 年报研发费合计 rd_sum_yuan。value 由分子/分母直接相除、保留 4 位小数 = 9.0664。"
                "若改为「100 − 12 条链各自 4 位小数份额之和」，会得 9.0665（见同段 "
                "chain_unmapped_sum_rounded_pct）；差 0.0001 是 12 个分项各自舍入后累加，"
                "**两数都保留、不得混用**，主口径用直除"),
            "chain_unmapped_sum_rounded_pct": {
                "value": round(100 - sum(x["share_of_rd_sum_pct"] for x in ch["by_chain"]), 4),
                "numerator": round(sum(x["share_of_rd_sum_pct"] for x in ch["by_chain"]), 4),
                "denominator": 100,
                "denominator_note": ("12 条链各自 4 位小数份额之和 X，本值 = 100 − X。"
                                     "分项舍入累加使它比直除的 9.0664 高 0.0001；"
                                     "只用于说明「分项相加不等于整体相除」，不作主口径"),
            },
            # 2026-10-23 改名：原键名 rd_nonnull_row_share_pct 说 nonnull，分子取的却是
            # rd_pos_rows（研发费>0，19,585 行），不是 rd_nonnull_rows（19,695 行）。
            # 「一个键名一个定义」——名字撒谎比数字错更难被发现，因为数字过闸了。
            # 值不变（48.6717），两个数都留在 note 里供对账。
            "rd_pos_row_share_pct": dec(
                pct(stock["rd_pos_rows"], stock["rows"]), stock["rd_pos_rows"], stock["rows"],
                "分子=上市财务表研发费>0 的行 rd_pos_rows（19,585 行）；"
                "分母=上市财务表总行 stock_fin.rows（40,239 行）。"
                "并列参考：rd_nonnull_rows（研发费非空）19,695 行，占比 48.95%——两个口径差 110 行，"
                "本键采用「>0」口径，键名已相应改为 rd_pos_*"),
        },
        "annual_fin_fill": fill,
        "stock_detail": {
            "rd_latest_stats_yuan": st,
            "rd_latest_period_year": stock["rd_latest_period_year"],
            "y2025_dec": y25,
            "top10_rd": stock["top10_rd"],
            "rd_zero_rows": stock["rd_zero_rows"],
            "rd_all_zero_orgs": stock["rd_all_zero_orgs"],
            "period_min": stock["period_min"], "period_max": stock["period_max"],
        },
        "forg_detail": {
            "rows": forg["rows"], "orgs": forg["orgs"],
            "rd_nonnull_rows": forg["rd_nonnull_rows"], "rd_pos_rows": forg["rd_pos_rows"],
            "rd_staff_pos_rows": forg["rd_staff_pos_rows"],
            "overlap_orgs_with_stock": forg["overlap_orgs_with_stock"],
            "sample": forg["sample"],
        },
        "chain_section": {
            "listed_orgs_with_rd": ch["listed_orgs_with_rd"],
            "credit_codes": ch["credit_codes"],
            "chain_mapped_orgs": ch["chain_mapped_orgs"],
            "chain_unmapped_orgs": ch["chain_unmapped_orgs"],
            "l1_mapped_orgs": ch["l1_mapped_orgs"],
            "by_chain": ch["by_chain"],
            "by_l1": ch["by_l1"],
            "unit_note": ch["unit_note"],
        },
        "caveats": [
            "年报研发列整列为空是「库里没有数」，不是「这些企业没研发」——不得按 0 解释",
            "645 家 FY2025 上市样本的均值只能当量级参照：上市企业规模系统性高于全量法人，"
            "直接当「产业平均研发投入」会高估",
            "212 家上市机构全部报告期研发费为 0（rd_all_zero_orgs），按口径不进均，不是缺失",
            "「选定产业」的 cluster_id 与链码不是同一套键，本件用链码做替代切面时已注明不构成口径等价",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in headline.items() if k not in ("by_chain", "by_l1", "top10_rd")},
                     ensure_ascii=False, indent=1)[:2200])
    print("->", OUT)


if __name__ == "__main__":
    main()
