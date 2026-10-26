#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_MARKET_SIZE 产业链市场规模 —— 否定性证据探针。

结论：**完全不支持**。本脚本不产出任何「市场规模」数值，只证明为什么算不出来。
按派单书 v6 第七条纪律，判「完全不支持」的件必须有一个专门证明「为什么不可算」
的脚本，产物写 `verdict_kind="negative_evidence"`，否则负结论不可复核。

四条被逐一否掉的路径
--------------------
1. **企业年报营收加总**（注册表公式 `SUM(ent_annual_revenue)`）
   链路本身可执行，但金额源覆盖率 0.0174%：1,714,457 家挂链企业里只有 299 家
   有年报营收（`chain21_revenue_20261022.json` 的 annual 块）。统计年 2024 只有
   20 条链内记录、覆盖 7 条链，另 5 条链为 0。这不是「市场规模」，是样本清单。
2. **上市公司财务表**（`dwd_org_stock_finance_info`）
   39,395 行是**月度/期记录**（125 个不同 `occur_period`），971 家企业；同一企业
   多期重复，直接求和等于把 12 个月加成一个「年」。按最新期取数也只能覆盖 971 家。
3. **融资事件金额**（`dwd_org_financing_info`）
   25,654 起事件里 16,828 起（65.60%）无金额；币种 CNY 17,442 / 空 7,515 /
   USD 591 / HKD 106，币种不统一且无汇率表，不能相加。且融资额是**资本投入**，
   不是营业收入，语义上不能当市场规模。
4. **政策文本金额**（`dwd_policy_base`）
   表里没有金额列，金额只存在于正文与摘要的自由文本，且同一份政策两处金额差三个
   数量级（28,251.51 亿元 vs 51 亿元，见 DATA_FACTS §3.56 末段），正则抽取不可用。

另外排除 live `gkxlumenx_ads.chain_market`：该表 40 行（8 链 × 5 年），
`_work_gkx21/TABLE_MAP.json` 判 `B-sample`，note 明写「仅 live ADS 样例级
（<1000 行），不作结果面」。

零数据库：只读 `code/_snapshots21/` 下四份快照 + 两份工作区清单。
运行：cd code && python3 M_CHAIN_MARKET_SIZE.py
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
WORK = BASE.parent / "_work_gkx21"
METRIC = "M_CHAIN_MARKET_SIZE"
CREDIT_OK = re.compile(r"^[0-9A-Z]{18}$")
CHAIN_FIRMS_TOTAL = 1_714_457          # §3.50 去脏 + 链内，新件默认口径
ROOTS = ["INB1204", "INB1209", "INB1236", "INB1303", "INB1306", "INB1309",
         "INB1323", "INB1333", "INB1354", "INB1502", "INB2503", "INB2505"]


def load(p):
    return json.loads((SNAP / p).read_text(encoding="utf-8"))


def main():
    rev = load("chain21_revenue_20261022.json")
    fin = load("chain21_fin_degree_20261022.json")["fin"]
    pol = load("policy_base_20261021.json")
    idx = load("chain_firm_index_20261023.json")
    name_chain = idx["name_chain"]
    chain_name = idx["chain_name"]

    stock, annual = rev["stock"], rev["annual"]

    # ---- 路径 1：年报营收按链聚合 ----
    per_chain = {}
    for ch in ROOTS:
        per_chain[ch] = {
            "chain_name": chain_name[ch],
            "chain_firms": idx["chain_firms"].get(ch),
            "revenue_rows_all_years": 0,
            "firms_all_years": set(),
            "rows_by_year": collections.Counter(),
            "sum_2024_yi": 0.0,
            "firms_2024": 0,
            "max_firm_2024_yi": 0.0,
        }
    for r in annual:
        ch = name_chain.get(r[1])
        if not ch or ch not in per_chain:
            continue
        y = int(float(r[3]))
        v = float(r[4])
        c = per_chain[ch]
        c["revenue_rows_all_years"] += 1
        c["firms_all_years"].add(r[2] or r[0])
        c["rows_by_year"][y] += 1
        if y == 2024:
            c["sum_2024_yi"] += v / 1e8
            c["firms_2024"] += 1
            c["max_firm_2024_yi"] = max(c["max_firm_2024_yi"], v / 1e8)

    chain_rows = []
    for ch in ROOTS:
        c = per_chain[ch]
        n = len(c["firms_all_years"])
        chain_rows.append({
            "industry_code": ch,
            "industry_name": c["chain_name"],
            "chain_firms": c["chain_firms"],
            "revenue_rows_all_years": c["revenue_rows_all_years"],
            "distinct_firms_with_annual_revenue": n,
            "coverage_of_chain_firms": round(n / c["chain_firms"], 8) if c["chain_firms"] else None,
            "rows_by_year": {str(k): v for k, v in sorted(c["rows_by_year"].items())},
            "firms_2024": c["firms_2024"],
            "sum_2024_yi": round(c["sum_2024_yi"], 2),
            "max_single_firm_2024_yi": round(c["max_firm_2024_yi"], 2),
            "top1_share_2024": round(c["max_firm_2024_yi"] / c["sum_2024_yi"], 4)
            if c["sum_2024_yi"] else None,
        })

    ann_firms = {r[2] or r[0] for r in annual if name_chain.get(r[1])}
    y2024 = [r for r in annual if int(float(r[3])) == 2024 and name_chain.get(r[1])]
    n_chains_2024 = len({name_chain[r[1]] for r in y2024})

    # ---- 路径 2：上市公司财务表（月度记录）----
    periods = sorted({str(r[3]) for r in stock})
    stock_orgs = {r[0] for r in stock}
    stock_credits = {r[2] for r in stock if CREDIT_OK.match(r[2] or "")}

    # ---- 路径 3：融资金额 ----
    amt_empty = sum(1 for r in fin if not (r[4] or "").strip())
    cur_dist = collections.Counter((r[5] or "空") for r in fin)

    # ---- 路径 4：政策表金额列 ----
    pol_keys = sorted(pol[0].keys()) if pol else []
    amount_cols = [k for k in pol_keys if re.search(r"(amount|money|fund|金额|资金|budget)", k, re.I)]

    # ---- 路径 5：live ADS 样例表 ----
    live = json.loads((WORK / "LIVE_INVENTORY.json").read_text(encoding="utf-8"))
    tmap = json.loads((WORK / "TABLE_MAP.json").read_text(encoding="utf-8"))
    cm_live = live.get("gkxlumenx_ads.chain_market", {})
    cm_map = tmap.get("chain_market", {})

    sum_2024 = round(sum(r["sum_2024_yi"] for r in chain_rows), 2)
    zero_chains = [r["industry_name"] for r in chain_rows if r["firms_2024"] == 0]

    out = {
        "metric_id": METRIC,
        "metric_name": "市场规模",
        "unit": "亿元",
        "metric_value": None,
        "value_null_reason": (
            "五条金额路径逐一否掉：年报营收覆盖率 0.0174%、上市公司表是月度记录、"
            "融资额缺 65.60% 且币种不统一、政策表无金额列、live ADS 样例表 40 行不作结果面。"
            "不出数不是「还没算」，是「按任何一条路算出来的都不是市场规模」。"
        ),
        "verdict_kind": "negative_evidence",
        "support_judgment": "完全不支持",
        "definition": (
            "产业链下全部关联企业的年度营业收入合计（只计企业主体，不计机构/人才），"
            "单位亿元，统计年与 ENT 年报字段对齐。"
        ),
        "registry_formula": (
            "SUM(ent_annual_revenue) WHERE enterprise_code IN "
            "(SELECT entity_id FROM industry_chain_entity_rel WHERE chain_id=:chain_id "
            "AND entity_type='enterprise') AND fiscal_year=:stat_year"
        ),
        "chain_universe": {
            "chain_firms_total": CHAIN_FIRMS_TOTAL,
            "source_note": (
                "§3.50 去脏（^[0-9A-Z]{18}$）+ 链内口径 1,714,457；"
                "旧件 1,714,458 为未去脏链内口径，本件不使用。"
            ),
            "chains": len(ROOTS),
        },
        "path_1_annual_revenue": {
            "source": "code/_snapshots21/chain21_revenue_20261022.json 的 annual 块"
                      "（gkx.dwd_org_annual_financial_info，operating_revenue>0）",
            "table_rows": 90926,
            "positive_revenue_rows": len(annual),
            "positive_share_of_table": round(len(annual) / 90926, 6),
            "chain_attributable_rows": sum(r["revenue_rows_all_years"] for r in chain_rows),
            "chain_attributable_firms": len(ann_firms),
            "coverage_of_chain_firms": round(len(ann_firms) / CHAIN_FIRMS_TOTAL, 8),
            "rows_2024": len(y2024),
            "chains_with_2024_rows": n_chains_2024,
            "chains_zero_2024": zero_chains,
            "naive_sum_2024_yi": sum_2024,
            "per_chain": chain_rows,
            "why_rejected": (
                f"2024 年链内只有 {len(y2024)} 条记录、覆盖 {n_chains_2024} 条链，"
                f"{len(zero_chains)} 条链为 0。把它们相加得到的 {sum_2024} 亿元"
                "是「有年报的少数企业营收之和」，不是产业链市场规模；"
                "且覆盖与否和链大小无关（生物医药 138,742 家企业 2024 年 0 条记录），"
                "缺失不是随机的，不能外推。"
            ),
        },
        "path_2_listed_finance": {
            "source": "code/_snapshots21/chain21_revenue_20261022.json 的 stock 块"
                      "（gkx.dwd_org_stock_finance_info，operating_revenue>0）",
            "rows": len(stock),
            "distinct_orgs": len(stock_orgs),
            "distinct_credit_18": len(stock_credits),
            "distinct_periods": len(periods),
            "period_examples": periods[:3] + periods[-3:],
            "why_rejected": (
                f"{len(stock)} 行只有 {len(stock_orgs)} 家企业、却是 {len(periods)} 个不同"
                "会计期（occur_period 形如 201812），是月/期流水而非年度口径。"
                "直接求和会把同一企业的多期重复计入；按最新期取数又只剩不到千家企业，"
                "且全部是上市/发债主体，系统性偏向大企业。"
            ),
        },
        "path_3_financing": {
            "source": "code/_snapshots21/chain21_fin_degree_20261022.json 的 fin",
            "events": len(fin),
            "amount_empty": amt_empty,
            "amount_empty_share": round(amt_empty / len(fin), 4),
            "currency_dist": dict(cur_dist),
            "why_rejected": (
                "金额缺失 65.60%，且 CNY/USD/HKD 混列、无汇率表，不能相加；"
                "更根本的是融资额是资本投入（股权融资），不是营业收入，"
                "语义上不能替代市场规模。已交付 M_CHAIN_INVEST_TOTAL 也只能发布"
                "「单币种金额」，不能发布跨币种合计。"
            ),
        },
        "path_4_policy": {
            "source": "code/_snapshots21/policy_base_20261021.json",
            "rows": len(pol),
            "columns": pol_keys,
            "amount_columns_found": amount_cols,
            "why_rejected": (
                f"{len(pol)} 条政策的 {len(pol_keys)} 个字段里没有金额列"
                f"（amount 类列命中 {len(amount_cols)} 个）。金额只存在于正文/摘要自由文本，"
                "且同一份政策两处金额差三个数量级（28,251.51 亿元 vs 51 亿元，"
                "DATA_FACTS §3.56 末段），正则抽取会取到错值。"
            ),
        },
        "path_5_live_ads": {
            "table": "gkxlumenx_ads.chain_market",
            "live_rows": cm_live.get("rows"),
            "table_map_case": cm_map.get("case"),
            "table_map_note": cm_map.get("note"),
            "why_rejected": (
                "40 行 = 8 链 × 5 年的样例级 ADS 表；TABLE_MAP 判 B-sample 并明写"
                "「不作结果面」。它没有可核验的取数链路（上游 gkx 无对应明细），"
                "引用它等于把样例值当实测值。"
            ),
        },
        "rejected_alternatives": {
            "enterprise_count_times_coefficient": (
                "禁止：用「企业数 × 行业均值营收」自造市场规模。系数没有库内来源，"
                "且企业规模分布极度右偏（年报最大 1,090.56 亿元 / 最小 -443.71 元量级），"
                "任何常数系数都会把结果放大或缩小两三个数量级。"
            ),
            "gdp_or_output_share": (
                "禁止：用深圳 GDP 或工业总产值乘「链占比」倒推。本库没有链级产值份额，"
                "链占比只能由企业数近似，等于第一种错法换了个名字。"
            ),
        },
        "missing_for_repair": [
            {"field": "链上企业年度营业收入（全量）",
             "why": "注册表公式的唯一金额输入；现覆盖 0.0174%",
             "provider": "税务申报/统计年鉴规上企业库/工商年报营收"},
            {"field": "企业—链归属的稳定主键",
             "why": "现有链归属靠 industry_code，企业营收表靠 org_id，两者只能按名称桥接",
             "provider": "统一社会信用代码级别的链归属表"},
            {"field": "币种与汇率",
             "why": "融资额跨币种不可加",
             "provider": "外管局中间价或统一折算人民币"},
            {"field": "链级产值/营收官方口径",
             "why": "即便企业级营收补齐，也需要口径基准做校验",
             "provider": "统计部门产业链增加值核算"},
        ],
        "why_not_partial": (
            "四档里的「部分支持」要求「部分依赖维可得、其余缺」。本件的**唯一**核心"
            "依赖维就是金额，金额覆盖率 0.0174% 且非随机缺失，等于核心维不具备；"
            "结构（链归属、统计年）齐全但没有可加的金额，属于「结构与数据均不具备"
            "可算闭环」，故判完全不支持，而不是部分支持。与已交付 M_CHAIN_MARKET_GROWTH"
            "（增长率，同判完全不支持）保持同一母指标口径。"
        ),
        "support_judgment_reason": (
            "五条金额路径全部否掉；链上企业年度营收覆盖 299/1,714,457 = 0.0174%，"
            "2024 年只有 20 条记录、5 条链为 0。不出数。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本件不产出任何年度序列，故无基期可用/缺失之说。年报营收覆盖的年份"
            "实测为 2013—2025（299 家、532 条链内记录），但每年样本都是不同企业，"
            "不存在可比的同主体两期，未按任何年份摊入分母。"
        ),
    }

    dst = BASE / f"{METRIC}_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{METRIC}: value=null, chain firms with revenue="
          f"{len(ann_firms)}/{CHAIN_FIRMS_TOTAL}, 2024 rows={len(y2024)} "
          f"chains_with_rows={n_chains_2024}, naive_sum_2024={sum_2024}亿")


if __name__ == "__main__":
    main()
