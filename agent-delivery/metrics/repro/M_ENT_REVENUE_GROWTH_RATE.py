#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_REVENUE_GROWTH_RATE「营收增长率」→ `code/M_ENT_REVENUE_GROWTH_RATE_out.json`

口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REVENUE_GROWTH_RATE.md`）：
    逐年相邻年同比 = (rev_y - rev_{y-1}) / rev_{y-1} * 100；
    上年必须是 y-1 且非空、非 0；禁止隔年硬凑；缺上年或除零 → 该年不出增长率。
    输入只允许 `enterprise_finance_history.revenue` ← `dwd_org_annual_financial_info.operating_revenue`；
    **禁止**用 `dwd_org_stock_finance_info` 替代年报；禁止读产出列 revenue_growth_rate。

数据面：主口径数字来自族级共享快照 `code/_snapshots21/ent_fin_family_20261023.json`；
本脚本额外发 1 条窄探针，把「上年缺行 / 上年为空 / 上年为 0」三种扣除量拆开报出
（派单书 §三 要求分母为 0 或空时显式扣除并给出扣除量；快照只落了成对数）。

重跑：`cd code && python3 M_ENT_REVENUE_GROWTH_RATE.py`
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SNAP = os.path.join(HERE, "_snapshots21", "ent_fin_family_20261023.json")
OUT = os.path.join(HERE, "M_ENT_REVENUE_GROWTH_RATE_out.json")
FIN = "gkx.dwd_org_annual_financial_info"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def denom_breakdown():
    """拆开「成不了对」的三种原因。2,193 行营收非空，各自带索引回查上年一行。"""
    try:
        from _gkxdb import GKX
        import pymysql
    except Exception as e:  # 无驱动也允许读快照出其余数字
        return {"error": f"import: {e}"}
    sql = f"""
    SELECT COUNT(*) rows_rev,
           SUM(NOT EXISTS (SELECT 1 FROM {FIN} g WHERE g.org_id=f.org_id
                            AND g.`year`=f.`year`-1 AND g.is_deleted=0)) prev_no_row,
           SUM(EXISTS (SELECT 1 FROM {FIN} g WHERE g.org_id=f.org_id
                        AND g.`year`=f.`year`-1 AND g.is_deleted=0)
               AND (SELECT g.operating_revenue FROM {FIN} g WHERE g.org_id=f.org_id
                     AND g.`year`=f.`year`-1 AND g.is_deleted=0 LIMIT 1) IS NULL) prev_null,
           SUM((SELECT g.operating_revenue FROM {FIN} g WHERE g.org_id=f.org_id
                 AND g.`year`=f.`year`-1 AND g.is_deleted=0 LIMIT 1)=0) prev_zero
    FROM {FIN} f
    WHERE f.operating_revenue IS NOT NULL AND f.is_deleted=0
    """
    try:
        c = pymysql.connect(**GKX)
        try:
            cur = c.cursor()
            cur.execute("SET SESSION max_execution_time=90000")
            cur.execute(sql)
            r = cur.fetchone()
        finally:
            c.close()
    except Exception as e:
        return {"error": str(e)[:300]}
    rows, no_row, nul, zero = [int(x or 0) for x in r]
    return {"rows_revenue_nonnull": rows, "prev_year_row_absent": no_row,
            "prev_year_value_null": nul, "prev_year_value_zero": zero,
            "computable_pairs": rows - no_row - nul - zero,
            "check_note": "computable_pairs 应与快照 pairs.n 相等，作为对账"}


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    fin, asset = d["annual_fin"], d["asset_text"]
    p = fin["pairs"]
    base_orgs = d["base"]["orgs"]
    br = denom_breakdown()

    st = p["stats"]
    headline = {
        "pairs": p["n"],
        "orgs_with_pairs": p["orgs"],
        "coverage_pct_of_base": pct(p["orgs"], base_orgs),
        "base_orgs": base_orgs,
        "revenue_nonnull_rows": fin["fill"]["operating_revenue"]["nonnull"],
        "growth_median_pct": st["median"],
        "growth_mean_pct": st["mean"],
        "growth_p10_pct": st["p10"],
        "growth_p90_pct": st["p90"],
        "growth_p99_pct": st["p99"],
        "growth_max_pct": st["max"],
        "growth_min_pct": st["min"],
        "over_1000pct": p["over_1000pct"],
        "under_minus_90pct": p["under_minus_90pct"],
        "by_year": p["by_year"],
        "median_by_year": p["median_pct_by_year"],
        "denominator_breakdown": br,
        "asset_text_pairs": asset["pairs"]["n"],
        "asset_text_orgs_with_pairs": asset["pairs"]["orgs"],
        "asset_text_median_pct": asset["pairs"]["stats"]["median"],
        "asset_text_max_pct": asset["pairs"]["stats"]["max"],
        "asset_text_note": "xsze「数值+万元」文本，占位串 514,140 行已剔除；"
                           "calc-logic 未声明该表，仅作同族年报的旁证，不进主口径",
        "stock_note": "calc-logic 明文禁止用 dwd_org_stock_finance_info 替代年报，本件未使用该表算增长率",
    }

    out = {
        "metric_id": "M_ENT_REVENUE_GROWTH_RATE",
        "metric_name": "营收增长率",
        "support_judgment": "部分支持",
        "judgment_basis": {
            "formula": "(rev_y - rev_{y-1}) / rev_{y-1} * 100，仅 y-1 相邻年",
            "source_table": "gkx.dwd_org_annual_financial_info（calc-logic 声明的唯一输入）",
            "why_partial": "规则可执行、782 个「企业-年」对已算出；但仅覆盖 398 家（占底册 0.2104%），"
                           "2,193 行营收里 1,411 行因上年缺行/为空/为 0 而无法成对，"
                           "覆盖率是数据缺口而非口径缺口",
            "why_not_direct": "两库均无 enterprise_finance_history.revenue_growth_rate 结果列"
                              "（该列在本库不存在，属待落表目标）",
            "why_not_unsupported": "依赖列与年份键齐全，成对的 782 个观测已能逐条复算",
        },
        "sources": [
            {"db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp（只读）",
             "table": FIN, "rows": fin["rows"],
             "note": "窄投影 org_id/year/operating_revenue/pure_profit + 底册 LEFT JOIN"},
            {"snapshot": "code/_snapshots21/ent_fin_family_20261023.json",
             "builder": "code/_build_ent_fin_family.py",
             "note": "pairs / by_year / 中位数由快照本地计算，未在服务端做窗口函数"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info（denominator 探针）",
             "sql_kind": "2,193 行营收非空者逐行回查 y-1（uk_org_id_year 索引）",
             "note": "拆出「上年缺行 / 上年为空 / 上年为 0」三种扣除量"},
        ],
        "base_years_used": [int(y) for y in sorted(p["by_year"])],
        "base_years_missing": [int(y) for y in sorted(fin["latest_year_dist"])
                               if int(y) not in [int(x) for x in p["by_year"]]],
        "base_years_note": "增长率只用「相邻两年」：本年 %s—%s，对应上年 %s—%s。"
                           "库内财务表更早年份没有成对营收，未按 0 摊入；"
                           "各年成对数见 by_year，中位数逐年单列"
                           % (min(int(y) for y in p["by_year"]), max(int(y) for y in p["by_year"]),
                              min(int(y) for y in p["by_year"]) - 1,
                              max(int(y) for y in p["by_year"]) - 1),
        "headline": headline,
        "derived": {
            "rows_without_usable_prior": dec(
                (br.get("rows_revenue_nonnull") or 0) - p["n"],
                (br.get("rows_revenue_nonnull") or 0) - p["n"], None,
                "计数，无分母：营收非空行 2,193（探针 rows_revenue_nonnull）− 能成相邻年对的 782 对"
                "＝ 1,411 行无法算出增长率；三种扣除量（上年缺行/上年为空/上年为 0）见 "
                "headline.denominator_breakdown，未拿底册总数凑比例"),
            "pairs_per_org": dec(
                round(p["n"] / p["orgs"], 4) if p["orgs"] else None, p["n"], p["orgs"],
                "分子=成对的「企业-年」观测数 pairs.n（782 对）；"
                "分母=至少有一对的企业数 pairs.orgs（398 家）。一家企业可贡献多个增长年"),
            "positive_pairs": dec(
                p["n"] - st["neg"] - st["zero"], p["n"] - st["neg"] - st["zero"], None,
                "计数，无分母：增长率为正的对数 = 总对数 782 − 负增长 304 − 零增长 1 ＝ 477"),
            "negative_pairs": dec(
                st["neg"], st["neg"], None,
                "计数，无分母：增长率为负的对数（pairs.stats.neg，304 对）"),
            "zero_pairs": dec(
                st["zero"], st["zero"], None,
                "计数，无分母：增长率恰为 0 的对数（pairs.stats.zero，1 对）"),
            "coverage_of_rev_orgs_pct": dec(
                pct(p["orgs"], fin["orgs_any_revenue"]), p["orgs"], fin["orgs_any_revenue"],
                "分子=能算出至少一年增长率的企业数 pairs.orgs（398 家）；"
                "分母=年报里有任何一年营收非空的企业数 annual_fin.orgs_any_revenue（1,302 家）；"
                "两者之差是「只有单年营收、凑不出相邻年」的企业"),
            "asset_pairs_per_org": dec(
                round(asset["pairs"]["n"] / asset["pairs"]["orgs"], 4),
                asset["pairs"]["n"], asset["pairs"]["orgs"],
                "分子=年报资产表（文本万元）可成对的观测数 asset_text.pairs.n（3,822 对）；"
                "分母=该表有对的企业数 asset_text.pairs.orgs（1,962 家）。仅旁证，不进主口径"),
            "asset_negative_pairs": dec(
                asset["pairs"]["stats"]["neg"], asset["pairs"]["stats"]["neg"], None,
                "计数，无分母：年报资产表旁证口径下负增长的对数（asset_text.pairs.stats.neg，1,408 对）"),
            "asset_positive_pairs": dec(
                asset["pairs"]["n"] - asset["pairs"]["stats"]["neg"] - asset["pairs"]["stats"]["zero"],
                asset["pairs"]["n"] - asset["pairs"]["stats"]["neg"] - asset["pairs"]["stats"]["zero"],
                None,
                "计数，无分母：年报资产表旁证口径下正增长的对数 = 3,822 − 1,408 − 27 ＝ 2,387"),
        },
        "caveats": [
            "上年为 0 → 除零，按口径不出增长率；扣除量见 denominator_breakdown",
            ">1000%% 的 %d 对与 <-90%% 的 %d 对多为基数极小（营收千元级）所致，"
            "与「元/万元混填」同源，做榜单前须先做单位归一" % (p["over_1000pct"], p["under_minus_90pct"]),
            "KPI 取「最新能算出的一年」，不等于最新财务年——两者差一年时页面要标注年份",
            "境外财务表 calc-logic 明示不并；上市财务表明示禁用，均未使用",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(headline, ensure_ascii=False, indent=1)[:2200])
    print("->", OUT)


if __name__ == "__main__":
    main()
