#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_TREND_INDEX 产业链变化趋势指数（gkx 三方库，20261023 重建版）。

口径（calc-logic/CHAIN/M_CHAIN_TREND_INDEX.md）四因子等权：
  企业增减 / 专利增速 / 资讯热度变化 / 投融资变化，各因子 min-max 归一到 0—100。

本件只保留**同一可比时间窗（2021—2024，3 年 CAGR）**内能闭合的两因子：
  专利增速  —— `patent_panel_innov_20261021.json.app_year`（2021—2024 全覆盖）
  投融资变化 —— 融资事件数（去重后，按 completion_date 年份）
两个不可得因子一律 null：
  企业增减  —— `chain21_year_20261022.json` 只把 35,046 家链企业（2.04%）对上底册成立年；
  资讯热度  —— 新闻表 108,052 行只覆盖 2025-02-01—2026-07-27，2021—2024 零行。

时间列唯一：专利用 `apdt_year`（申请年），融资用 `completion_date` 的年份；
绝不把 `pbdt`（公开年）混进专利增速，也不把融资 `estiblish_time` 当事件年。

产物：code/M_CHAIN_TREND_INDEX_out.json
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _chain5_common as C

METRIC = "M_CHAIN_TREND_INDEX"
YEARS = [2021, 2022, 2023, 2024]


def cagr(first: float, last: float, periods: int = 3):
    if not first or last is None:
        return None
    if first <= 0 or last < 0:
        return None
    return round(((last / first) ** (1.0 / periods) - 1) * 100, 2)


def pct_rank(values: dict) -> dict:
    items = sorted(values.items(), key=lambda kv: kv[1])
    n, out, i = len(items), {}, 0
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        s = 0.0 if n == 1 else round((i + j) / 2.0 / (n - 1) * 100, 2)
        for k in range(i, j + 1):
            out[items[k][0]] = s
        i = j + 1
    return out


def main():
    idx = C.load("chain_firm_index_20261023.json")
    names = idx["chain_name"]
    panel = C.load("patent_panel_innov_20261021.json")
    app_year = panel["app_year"]
    nc = idx["name_chain"]
    py = defaultdict(Counter)
    for k, v in app_year.items():
        y, nm = k.split("|", 1)
        ch = nc.get(nm)
        if not ch:
            continue
        for c in (ch if isinstance(ch, list) else [ch]):
            py[c][y] += v

    ev, st = C.financing(idx)
    fy = defaultdict(Counter)
    for e in ev:
        y = int(e["year"])
        if y not in YEARS:
            continue
        for c in e["chains"]:
            fy[c][y] += 1

    firm_year = C.load("chain21_year_20261022.json")
    news = C.load("news21_chain_items_20261022.json")

    rows = []
    for c in C.ROOTS:
        pser = [py[c].get(str(y), 0) for y in YEARS]
        fser = [fy[c].get(y, 0) for y in YEARS]
        rows.append({
            "chain": c, "chain_name": names.get(c),
            "patent_series": dict(zip([str(y) for y in YEARS], pser)),
            "fin_events_series": dict(zip([str(y) for y in YEARS], fser)),
            "patent_cagr_pct": cagr(pser[0], pser[3]),
            "fin_events_cagr_pct": cagr(fser[0], fser[3]),
            "patent_yoy_2024_pct": round((pser[3] / pser[2] - 1) * 100, 2) if pser[2] else None,
            "fin_yoy_2024_pct": round((fser[3] / fser[2] - 1) * 100, 2) if fser[2] else None,
            "firm_growth_pct": None,
            "news_growth_pct": None,
        })

    ps = pct_rank({r["chain"]: r["patent_cagr_pct"] for r in rows})
    fs = pct_rank({r["chain"]: r["fin_events_cagr_pct"] for r in rows})
    for r in rows:
        r["patent_score"] = ps[r["chain"]]
        r["fin_score"] = fs[r["chain"]]
        r["firm_score"] = None
        r["news_score"] = None
        r["trend_index_2f"] = round((r["patent_score"] + r["fin_score"]) / 2, 2)
        r["trend_index_4f"] = None
        r["sign_agreement"] = (r["patent_cagr_pct"] >= 0) == (r["fin_events_cagr_pct"] >= 0)
        r["weight_coverage"] = 0.5
    rows.sort(key=lambda r: -r["trend_index_2f"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    agree = sum(1 for r in rows if r["sign_agreement"])
    report = {
        "metric_name": "产业链变化趋势指数",
        "unit": "0—100（两因子相对指数）；trend_index_4f = null",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_TREND_INDEX.md",
        "data_source": {
            "engine": "只读快照（源：三方库 gkx @ 183.240.141.251:3318）",
            "tables": ["gkx.dwd_patent（经面板缓存）", "gkx.dwd_org_financing_info",
                       "gkx.dwd_org_base_info", "gkx.dwd_industry_chain_news_info"],
            "snapshots": ["code/_snapshots21/patent_panel_innov_20261021.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/chain_firm_index_20261023.json",
                          "code/_snapshots21/chain21_year_20261022.json",
                          "code/_snapshots21/news21_chain_items_20261022.json"],
        },
        "probes": {
            "window": "2021—2024（3 年 CAGR）",
            "patent_app_year_rows": len(app_year),
            "patent_applies_mapped": sum(sum(v.values()) for v in py.values()),
            "patent_table_rows": 2939895,
            "patent_coverage_pct": round(100.0 * sum(sum(v.values()) for v in py.values()) / 2939895, 2),
            "fin_events_window": sum(sum(v.values()) for v in fy.values()),
            "fin_events_all": len(ev),
            "firm_year_joined_rows": firm_year["joined_rows"],
            "firm_year_chain_firms": sum(idx["chain_firms"].values()),
            "firm_year_coverage_pct": round(100.0 * firm_year["joined_rows"] / sum(idx["chain_firms"].values()), 2),
            "firm_year_chain_rows": sum(firm_year["chain_year"].values()),
            "news_rows": news["meta"]["rows"],
            "news_date_min": "2025-02-01",
            "news_date_max": "2026-07-27",
            "news_rows_in_window": 0,
            "patent_2025_rows": panel["year_all"].get("2025"),
            "patent_2026_rows": panel["year_all"].get("2026"),
            "chains_with_positive_patent_cagr": sum(1 for r in rows if r["patent_cagr_pct"] > 0),
            "chains_with_positive_fin_cagr": sum(1 for r in rows if r["fin_events_cagr_pct"] > 0),
            "chains_with_sign_agreement": agree,
            "sum_fin_2021": sum(r["fin_events_series"]["2021"] for r in rows),
            "sum_fin_2024": sum(r["fin_events_series"]["2024"] for r in rows),
            "sum_patent_2021": sum(r["patent_series"]["2021"] for r in rows),
            "sum_patent_2024": sum(r["patent_series"]["2024"] for r in rows),
        },
        "chain_rows": rows,
        "factor_status": [
            {"factor": "企业增减", "status": "null",
             "evidence": "底册成立年仅对上 35,046/1,714,457 家链企业（2.04%），样本不代表性"},
            {"factor": "专利增速", "status": "可算",
             "evidence": "2021—2024 四年齐全；2025/2026 为残年，不进窗口"},
            {"factor": "资讯热度变化", "status": "null",
             "evidence": "新闻表 108,052 行只覆盖 2025-02-01—2026-07-27，2021—2024 零行"},
            {"factor": "投融资变化", "status": "可算（事件数口径）",
             "evidence": "去重后 2021—2024 分别 872/687/501/353 起；金额 58% 缺失，不用金额增速"},
        ],
        "notes": [
            "符号一致的链 8/12；4 条方向相反：智能网联汽车（专利 −18.22%、融资 +7.72%）、"
            "低空经济（专利 −0.27%、融资 +14.47%）、软件与信息服务（专利 +0.16%、融资 −36.35%）、"
            "生物医药（专利 +0.60%、融资 −49.47%）。这 4 条的合成分被两因子互相抵消，"
            "读表时必须同时看两列原始 CAGR。",
            "12 条链融资事件从 2021 年 872 起降到 2024 年 353 起（−59.5%）；这可能是真实降温，也可能是源表近年覆盖下降——本件无法区分，故不把该降幅当因果结论。",
            "专利是申请人名匹配子集（883,300 件，占全表 30.05%），不是全量专利；未匹配的 69.95% 不进分子。",
            "`trend_index_2f` 只覆盖 2/4 因子（权重 0.50），不得当四因子趋势指数发布。",
        ],
    }
    report.update(C.base_decl(
        YEARS, [2025, 2026],
        "2021—2024 是唯一同时满足「专利面板四年齐全 + 融资事件完整」的窗口；"
        "专利 2025 年 440,401 件、2026 年 74,810 件为残年，2025 年融资 561 起也低于 2024 年，"
        "均不进 CAGR 分母。2017—2020 年专利表零行，不补 0、不做外推。"))
    report["support_judgment"] = "部分支持"
    report["support_reason"] = (
        "四因子里企业增减（底册覆盖 2.04%）与资讯热度（窗口内零行）不可得，"
        "只剩专利增速与融资事件增速两维，且融资降幅无法区分真实降温与源表覆盖下降。")

    C.write_out(METRIC, report)
    print("rows", len(rows), "agree", agree)
    for r in rows:
        print(r["chain"], r["chain_name"], r["patent_cagr_pct"], r["fin_events_cagr_pct"], r["trend_index_2f"])


if __name__ == "__main__":
    main()
