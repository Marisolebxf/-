#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_INVEST_TOTAL 投融资总额（gkx 三方库，20261023 重建版）。

口径（calc-logic V1.0-20260904 / 王惠 20260904_ai补漏）：
  指定产业链在统计窗内相关投融资事件的**金额合计**，并派生增长率。
  真源 `chain_investment` 在 gkx 不存在（TABLE_ABSENCE_EVIDENCE 记为 demo_ads 面），
  改源为 `gkx.dwd_org_financing_info`，经 credit_code 挂链（本批唯一链归属口径）。

三条硬约束
  1. **跨币种不相加**：`funding_currency_code` 有 CNY / USD / HKD / 空 四类，
     只给单币种内合计。空币种的 7,515 行全部无金额，不构成第四种币种。
  2. **金额是文本**：`funding_amount` 形如 `8320.0万人民币` / `4.7亿人民币`，
     解析为万元；解析不了的不进分母，单独计数。
  3. **事件先去重**：(主体, completion_date, round, 金额文本) 四元组去重，
     重复行 7,776（30.3%）—— 不去重会把同一轮融资按投资方行数放大数倍。

产物：code/M_CHAIN_INVEST_TOTAL_out.json
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _chain5_common as C

METRIC = "M_CHAIN_INVEST_TOTAL"


def main():
    idx = C.load("chain_firm_index_20261023.json")
    names = idx["chain_name"]
    ev, st = C.financing(idx, only_mapped=False)

    per = defaultdict(lambda: {"events": 0, "orgs": set(), "amt_events": 0,
                               "cny": 0.0, "usd": 0.0, "hkd": 0.0,
                               "top": 0.0, "big": 0,
                               "by_year": defaultdict(lambda: {"events": 0, "cny": 0.0})})
    for e in ev:
        for ch in e["chains"]:
            d = per[ch]
            d["events"] += 1
            d["orgs"].add(e["credit"] or e["name"])
            y = str(e["year"])
            d["by_year"][y]["events"] += 1
            if e["amount_wan"] is not None:
                d["amt_events"] += 1
                if e["currency"] == "CNY":
                    d["cny"] += e["amount_wan"]
                    d["by_year"][y]["cny"] += e["amount_wan"]
                    d["top"] = max(d["top"], e["amount_wan"])
                    if e["amount_wan"] >= 1000000:      # ≥100 亿元
                        d["big"] += 1
                elif e["currency"] == "USD":
                    d["usd"] += e["amount_wan"]
                elif e["currency"] == "HKD":
                    d["hkd"] += e["amount_wan"]

    rows = []
    for ch in C.ROOTS:
        d = per[ch]
        ys = {y: {"events": v["events"], "cny_wan": round(v["cny"], 2)}
              for y, v in sorted(d["by_year"].items()) if 2019 <= int(y) <= 2025}
        cny_24 = d["by_year"].get("2024", {}).get("cny", 0.0)
        cny_23 = d["by_year"].get("2023", {}).get("cny", 0.0)
        cny_25 = d["by_year"].get("2025", {}).get("cny", 0.0)
        rows.append({
            "chain": ch, "chain_name": names.get(ch),
            "firms": idx["chain_firms"].get(ch),
            "events": d["events"], "n_orgs": len(d["orgs"]),
            "events_with_amount": d["amt_events"],
            "amount_coverage_pct": round(100.0 * d["amt_events"] / d["events"], 2) if d["events"] else None,
            "cny_wan": round(d["cny"], 2),
            "usd_wan": round(d["usd"], 2),
            "hkd_wan": round(d["hkd"], 2),
            "cny_per_firm_wan": round(d["cny"] / idx["chain_firms"][ch], 4) if idx["chain_firms"].get(ch) else None,
            "top_event_cny_wan": round(d["top"], 2),
            "top_event_share_pct": round(100.0 * d["top"] / d["cny"], 2) if d["cny"] else None,
            "events_ge_100yi": d["big"],
            "by_year": ys,
            "cny_yoy_2024_pct": round((cny_24 / cny_23 - 1) * 100, 2) if cny_23 else None,
            "cny_yoy_2025_pct": round((cny_25 / cny_24 - 1) * 100, 2) if cny_24 else None,
        })
    rows.sort(key=lambda r: -r["cny_wan"])

    cur = Counter()
    cur_amt = Counter()
    for e in ev:
        cur[e["currency"]] += 1
        if e["amount_wan"] is not None:
            cur_amt[e["currency"]] += 1
    currency_block = {k: {"events": cur[k], "events_with_amount": cur_amt[k]} for k in ("CNY", "USD", "HKD", "(空)")}

    # 单币种总额（全表事件，含未挂链）——只做规模说明，不与链表相加
    totals = {}
    for c in ("CNY", "USD", "HKD"):
        sub = [e for e in ev if e["currency"] == c and e["amount_wan"] is not None]
        totals[c] = {"events_with_amount": len(sub),
                     "amount_wan": round(sum(e["amount_wan"] for e in sub), 2)}
    mapped_cny = sum(r["cny_wan"] for r in rows)
    totals["mapped_cny_wan"] = round(mapped_cny, 2)
    totals["unmapped_cny_wan"] = round(totals["CNY"]["amount_wan"] - mapped_cny, 2)

    top = sorted([e for e in ev if e["amount_wan"] and e["currency"] == "CNY"
                  and e["chains"]], key=lambda x: -x["amount_wan"])[:10]
    top_block = [{"name": e["name"], "chain": e["chains"][0], "year": e["year"],
                  "cny_wan": round(e["amount_wan"], 2)} for e in top]

    # 全表按年（CNY，仅已挂链事件），用于正文的年度对比
    all_year = defaultdict(lambda: {"events": 0, "cny": 0.0})
    for e in ev:
        if e["chains"] and e["currency"] == "CNY":
            y = str(e["year"])
            all_year[y]["events"] += 1
            if e["amount_wan"]:
                all_year[y]["cny"] += e["amount_wan"]
    year_block = {y: {"events": v["events"], "cny_wan": round(v["cny"], 2)}
                  for y, v in sorted(all_year.items()) if 2019 <= int(y) <= 2025}

    round_block = dict(Counter(e["round"] for e in ev).most_common(20))
    mapped_amt_events = sum(r["events_with_amount"] for r in rows)
    report = {
        "metric_name": "投融资总额",
        "unit": "万元（单币种内合计；不做汇率折算）",
        "（正本见本目录 M_CHAIN_INVEST_TOTAL.md / calc-logic 入库件）",
        "data_source": {
            "engine": "只读快照（源：三方库 gkx @ 183.240.141.251:3318）",
            "tables": ["gkx.dwd_org_financing_info", "gkx.dwd_org_industry_tags"],
            "event_snapshot": "code/_snapshots21/chain21_fin_degree_20261022.json（fin 数组，25,654 行）",
            "chain_snapshot": "code/_snapshots21/chain_firm_index_20261023.json（credit→链，同批新建）",
        },
        "probes": {
            "rows_raw": st["rows"],
            "duplicate_rows": st["duplicate_rows"],
            "no_date_rows": st.get("no_date", 0),
            "out_of_window_rows": st["out_of_window"],
            "events_after_dedup": len(ev),
            "events_chain_mapped": st["chain_mapped"],
            "events_chain_unmapped": st["chain_unmapped"],
            "chain_mapped_pct": round(100.0 * st["chain_mapped"] / len(ev), 2) if ev else None,
            "events_with_amount": sum(1 for e in ev if e["amount_wan"] is not None),
            "events_without_amount": sum(1 for e in ev if e["amount_wan"] is None),
            "amount_coverage_pct": round(100.0 * sum(1 for e in ev if e["amount_wan"] is not None) / len(ev), 2) if ev else None,
            "currency_conflict_rows": st["currency_conflict"],
            "currency": currency_block,
            "round_distribution_top20": round_block,
            "mapped_events_with_amount": mapped_amt_events,
            "mapped_amount_coverage_pct": round(100.0 * mapped_amt_events / st["chain_mapped"], 2) if st["chain_mapped"] else None,
            "window": "1990-01-01—2025-12-31（2026 年 253 起残年事件不计）",
        },
        "currency_totals": totals,
        "year_block_cny_mapped": year_block,
        "chain_rows": rows,
        "top10_cny_events": top_block,
        "notes": [
            "跨币种不相加：CNY/USD/HKD 三列并列，任何合计都标注币种。",
            "USD 398 起有金额、HKD 105 起有金额，但本件不折算汇率，故不进 CNY 总额。",
            "空币种 7,515 起全部无金额，不构成第四种币种；它们只进入事件数分母。",
            "未挂链事件 7,688 起（43.6%）不进链表；链表合计只代表可归属子集。",
            "金额是下限：57.99% 的已挂链事件没有金额字段，链间比较只在「有金额」子集内成立。",
            "事件类型混杂：新三板 3,349、IPO 872、并购 775、股权转让 1,260 等均计入「投融资」；"
            "这些是交易/挂牌口径，不是 VC 轮次，金额不可与 A/B/C 轮直接比。",
            "头部污染：恒大地产（7,000,000 万元，2017）落在生物医药链，顺丰/万科/平安落在人工智能链——"
            "集团型企业被多条链打标签，融资并不等于链内业务融资；每链 top1 占比见 chain_rows。",
        ],
    }

    report.update(C.base_decl(
        [2019, 2020, 2021, 2022, 2023, 2024, 2025], [2026],
        "2019—2025 为年度金额序列；2026 年表内有 253 起事件但只到 7 月，属残年，不计入分母、"
        "不参与同比；1990 年以前无事件。年度金额只对 CNY 单币种成立，USD/HKD 不折算。"))
    report["support_judgment"] = "部分支持"
    report["support_reason"] = (
        "事件数与单币种金额可算，但 65.6% 的事件无金额、43.6% 的事件挂不上链、"
        "三种币种不能相加，且增长率只在 CNY 子集内成立——按四档定义属「始终有部分维度不可得」。")

    C.write_out(METRIC, report)
    print("events", len(ev), "mapped", st["chain_mapped"], "CNY亿", round(totals["CNY"]["amount_wan"] / 10000, 1))
    for r in rows:
        print(r["chain"], r["chain_name"], r["events"], r["events_with_amount"], round(r["cny_wan"] / 10000, 1))


if __name__ == "__main__":
    main()
