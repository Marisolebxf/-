#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_REG_FINANCING 区域融资（gkx 三方库，20261023 重建版）。

口径（calc-logic V2-20260821 / 王惠 20260824_产业链分析）：
  指定区域在指定产业链上，链上企业融资事件的去重件数。

本件把它操作化为**区域×链的融资强度**：每 100 家同区域同链企业对应的融资事件数。
分母必须是**同一地区的链企业数**，不是全库企业数，也不是全省企业数。

同母体三条（§3.46 / §3.54）
  1. 分子：融资事件的 credit_code 先过 ^[0-9A-Z]{18}$，再经
     `chain_firm_index_20261023.json` 的 fin_credit_chain 挂链；
  2. 分母：同一份快照的 chain_city（credit_code 前 6 位行政区划码 → 市）；
  3. 分子城市与分母城市用**同一个函数**（credit_code[2:8]），不混用底册 city。

产物：code/M_CHAIN_REG_FINANCING_out.json
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _chain5_common as C

METRIC = "M_CHAIN_REG_FINANCING"
MIN_DENOM = 100          # 强度展示门槛：不足 100 家企业的格只报事件数，不报强度


def main():
    idx = C.load("chain_firm_index_20261023.json")
    names = idx["chain_name"]
    ev, st = C.financing(idx)

    num = Counter()
    amt = Counter()
    for e in ev:
        if e["city"] == "未匹配":
            continue
        for ch in e["chains"]:
            num[(ch, e["city"])] += 1
            if e["currency"] == "CNY" and e["amount_wan"]:
                amt[(ch, e["city"])] += e["amount_wan"]

    cells = []
    for ch, cities in idx["chain_city"].items():
        for city, firms in cities.items():
            if city == "未匹配":
                continue
            n = num.get((ch, city), 0)
            ok = firms >= MIN_DENOM
            cells.append({
                "chain": ch, "chain_name": names.get(ch), "city": city,
                "firms": firms, "events": n,
                "events_per_100_firms": round(n / firms * 100, 3) if ok and firms else None,
                "intensity_suppressed": (not ok) and n > 0,
                "cny_wan": round(amt.get((ch, city), 0.0), 2),
            })

    with_events = [c for c in cells if c["events"] > 0]
    ranked = [c for c in cells if c["events_per_100_firms"] is not None and c["firms"] >= MIN_DENOM]
    top_intensity = sorted(ranked, key=lambda c: -c["events_per_100_firms"])[:15]
    top_events = sorted(with_events, key=lambda c: -c["events"])[:20]

    # 12 链 × 深圳（本库融资记录最完整的城市，可做链间比较）
    sz_rows = []
    for ch in C.ROOTS:
        firms = idx["chain_city"].get(ch, {}).get("深圳市", 0)
        n = num.get((ch, "深圳市"), 0)
        sz_rows.append({"chain": ch, "chain_name": names.get(ch), "firms": firms, "events": n,
                        "events_per_100_firms": round(n / firms * 100, 3) if firms else None,
                        "cny_wan": round(amt.get((ch, "深圳市"), 0.0), 2)})
    sz_rows.sort(key=lambda r: -r["events"])

    # 城市汇总（全部链）
    city_firms = Counter()
    for ch, cities in idx["chain_city"].items():
        for city, f in cities.items():
            if city != "未匹配":
                city_firms[city] += f
    city_events = Counter()
    for (_ch, city), n in num.items():
        city_events[city] += n
    city_rows = [{"city": c, "firms": f, "events": city_events[c],
                  "events_per_100_firms": round(city_events[c] / f * 100, 4)}
                 for c, f in city_firms.items() if f >= 1000]
    city_rows.sort(key=lambda r: -r["firms"])
    city_top = sorted(city_rows, key=lambda r: -r["events_per_100_firms"])[:15]

    report = {
        "metric_name": "区域融资",
        "unit": "融资事件数 / 每 100 家同区域同链企业",
        "（正本见本目录 M_CHAIN_REG_FINANCING.md / calc-logic 入库件）",
        "data_source": {
            "engine": "只读快照（源：三方库 gkx @ 183.240.141.251:3318）",
            "tables": ["gkx.dwd_org_financing_info", "gkx.dwd_org_industry_tags", "gkx.dwd_dim_admin_area"],
            "snapshots": ["code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/chain_firm_index_20261023.json",
                          "code/_snapshots21/admin_area_20261022.json"],
        },
        "probes": {
            "events_after_dedup": len(ev),
            "events_city_matched": sum(1 for e in ev if e["city"] != "未匹配"),
            "events_city_unmatched": sum(1 for e in ev if e["city"] == "未匹配"),
            "city_match_pct": round(100.0 * sum(1 for e in ev if e["city"] != "未匹配") / len(ev), 2) if ev else None,
            "chain_denominator_firms": sum(v for ch in idx["chain_city"] for v in idx["chain_city"][ch].values()),
            "city_matched_firms": sum(city_firms.values()),
            "cells_total": len(cells),
            "cells_with_events": len(with_events),
            "cells_rankable": len(ranked),
            "min_denominator": MIN_DENOM,
            "cells_suppressed": sum(1 for c in cells if c["intensity_suppressed"]),
            "shenzhen_event_share_pct": round(100.0 * city_events["深圳市"] / sum(city_events.values()), 2),
        },
        "shenzhen_by_chain": sz_rows,
        "top_cells_by_events": top_events,
        "top_cells_by_intensity": top_intensity,
        "city_rows_top20_by_firms": city_rows[:20],
        "city_rows_top15_by_intensity": city_top,
        "notes": [
            "分母 = 同链同城企业数（credit_code 过 18 位校验、且有环节路径）；不是全库企业数。",
            "城市 = credit_code[2:8] 登记行政区划，不是经营地；集团子公司注册地偏差无法消除。",
            "分子与分母城市用同一函数，故「区域」是可复算的登记地口径，不是工商经营地。",
            "融资表 61.5% 的事件落在深圳，跨城市强度比（深圳 6.571 vs 北京 0.077）反映的是**源表覆盖**，不是真实融资活跃度差异。",
            "金额列 65.6% 缺失，`cny_wan` 只作辅助，不参与强度定义。",
        ],
    }
    report.update(C.base_decl(
        [2021, 2022, 2023, 2024, 2025], [2026],
        "本件是截面强度（截至 2025 年末），不按年拆分；2026 年残年事件已剔除，"
        "2019 年以前事件保留在分子（累计存量口径），故不与年度增长率混用。"))
    report["support_judgment"] = "部分支持"
    report["support_reason"] = (
        "区域×链强度可算且分子分母同母体，但城市只能取登记地、14.5% 的企业行政区划码"
        "映射不到市、融资事件 43.6% 挂不上链、61.5% 集中在深圳——跨区域比较不可用，"
        "只能做同城链间比较。")

    C.write_out(METRIC, report)
    print("cells", len(cells), "with events", len(with_events), "rankable", len(ranked))
    for r in sz_rows:
        print(r["chain"], r["chain_name"], r["firms"], r["events"], r["events_per_100_firms"])


if __name__ == "__main__":
    main()
