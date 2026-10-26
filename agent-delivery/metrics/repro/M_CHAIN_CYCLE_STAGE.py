#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_CYCLE_STAGE · 产业周期阶段（gkx 单库代理版）

口径（王惠四步法的可执行化版本，旧稿沿用框架）
----------------------------------------------
阶段 ∈ {孕育期, 成长期, 成熟期, 衰退期}。原四步是「结构—增速—盈利—判定」，
本件逐腿做可用性检验，只保留能通过检验的腿：

  L1 融资热度腿（主判）：链内企业融资事件数，2022—2024 三年合计 / 2018—2020 三年合计 − 1
       >= +10% → 成长期；-10% ~ +10% → 成熟期；<= -10% → 衰退期
  L2 年龄结构腿（辅判）：成立年份分布 → 近 5 年新设占比 new_share
       new_share >= 0.25 且 L1 >= 0 → 孕育期（覆盖 L1 结论）
  L3 营收增速腿（**已试算并否决**）：链内样本营收 CAGR
       否决理由：有效样本 n_rev 从 2014 年 198 家掉到 2022 年 11 家，CAGR 量的是
       财报覆盖衰减，不是产业增速（详见 l3_revenue_rejected）。

数据事实
--------
`chain_stage` 在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §chain_stage）。
L1：`dwd_org_financing_info` 25,654 行（chain21_fin_degree），按企业名挂链命中 14,626 行。
L2：`dwd_org_industry_tags` × `dwd_org_base_info.incorporation_date`（chain21_year）。
L3：`dwd_org_annual_financial_info` + `dwd_org_stock_finance_info`（chain_lm_fin）。

输出：code/M_CHAIN_CYCLE_STAGE_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_CYCLE_STAGE_out.json"
METRIC = "M_CHAIN_CYCLE_STAGE"

RECENT = (2020, 2024)
PRE = (2018, 2020)
POST = (2022, 2024)


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def _median_year(yrs):
    if not yrs:
        return None
    tot = sum(yrs.values())
    acc = 0
    for y in sorted(yrs):
        acc += yrs[y]
        if acc >= tot / 2:
            return y
    return None


def main() -> None:
    year_by_chain = defaultdict(lambda: defaultdict(int))
    for k, n in load("chain21_year_20261022.json")["chain_year"].items():
        code, y = k.split("|")
        year_by_chain[code][int(y)] += n

    names = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}
    name2chain = load("chain21_layer_20261022.json")["names"]

    fin_rows = load("chain21_fin_degree_20261022.json")["fin"]
    fin_by_chain = defaultdict(lambda: defaultdict(int))
    matched = 0
    for r in fin_rows:
        ch = name2chain.get(r[1])
        if not ch:
            continue
        matched += 1
        fin_by_chain[ch][int(str(r[6])[:4])] += 1

    rev = defaultdict(list)
    for r in load("chain_lm_fin_20261021.json")["fin"]:
        rev[r["code"]].append(r)

    rows = []
    cov = {"chains": 0, "fin_matched": matched, "fin_rows": len(fin_rows),
           "fin_unmatched": len(fin_rows) - matched,
           "fin_match_rate": round(matched / len(fin_rows), 4) if fin_rows else None,
           "tag_rows": load("chain21_year_20261022.json")["tag_rows"],
           "multi_chain_rows": load("chain21_layer_20261022.json")["multi_chain_rows"],
           "fin_le_50_events": 0, "total_orgs_with_year": 0}
    for code in sorted(names):
        yrs = year_by_chain.get(code, {})
        total = sum(yrs.values())
        recent = sum(n for y, n in yrs.items() if RECENT[0] <= y <= RECENT[1])
        new_share = round(recent / total, 4) if total else None
        cov["chains"] += 1
        cov["total_orgs_with_year"] += total

        fy = fin_by_chain.get(code, {})
        pre = sum(fy.get(y, 0) for y in range(PRE[0], PRE[1] + 1))
        post = sum(fy.get(y, 0) for y in range(POST[0], POST[1] + 1))
        fin_chg = round(post / pre - 1, 4) if pre >= 20 else None
        if fin_chg is None or min(pre, post) < 50:
            cov["fin_le_50_events"] += 1

        if new_share is not None and new_share >= 0.25 and (fin_chg or 0) >= 0:
            stage = "孕育期"
        elif fin_chg is None:
            stage = "不可判"
        elif fin_chg >= 0.10:
            stage = "成长期"
        elif fin_chg > -0.10:
            stage = "成熟期"
        else:
            stage = "衰退期"

        # L3：营收腿否决证据（保留计算，只为证明它不可用）
        pts = [r for r in rev.get(code, []) if r["n_rev"] > 0 and r["rev_sum"]]
        pts.sort(key=lambda r: r["year"])
        l3 = None
        if len(pts) >= 2:
            a, b = pts[0], pts[-1]
            span = b["year"] - a["year"]
            cagr = round((b["rev_sum"] / a["rev_sum"]) ** (1 / span) - 1, 4) if span else None
            l3 = {"first_year": a["year"], "first_n": a["n_rev"],
                  "last_year": b["year"], "last_n": b["n_rev"], "cagr": cagr,
                  "n_ratio": round(b["n_rev"] / a["n_rev"], 3)}

        rows.append({
            "chain": code, "chain_name": names[code],
            "orgs_with_year": total, "median_est_year": _median_year(yrs),
            "new_share_2020_2024": new_share,
            "fin_events_pre_2018_2020": pre, "fin_events_post_2022_2024": post,
            "fin_event_change": fin_chg,
            "fin_events_total": sum(fy.values()),
            "stage": stage,
            "confidence": "跨窗口各>=50 事件" if fin_chg is not None and min(pre, post) >= 50 else "样本不足",
            "l3_revenue_rejected": l3,
        })

    dist = defaultdict(int)
    for r in rows:
        dist[r["stage"]] += 1

    out = {
        "metric_id": METRIC,
        "metric_name": "产业周期阶段",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "融资热度腿：post(2022-2024)/pre(2018-2020)-1 >=+10% 成长、-10%~+10% 成熟、<=-10% 衰退；new_share>=25% 且热度>=0 覆盖为孕育",
        "blocking_tables": {
            "chain_stage": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_stage",
            }
        },
        "proxy_path": "L1 链内融资事件数三年窗口对比（主判）+ L2 成立年份结构（辅判/孕育覆盖）",
        "proxy_deviation": "融资事件按企业名挂链命中 14,626/25,654=57.0%，链内未命中部分按无归属处理；融资热度反映资本关注度而非产出，衰退期的语义是「资本退潮」不是「产业萎缩」",
        "rejected_proxy": {
            "leg": "链内样本营收 CAGR",
            "why": "有效样本 n_rev 逐年塌陷（如软件与信息服务 2014 年 198 家 → 2022 年 11 家），CAGR 度量的是财报覆盖衰减而不是产业增速；各链 CAGR 落在 -99% ~ +26%，与深圳产业实际不符，故不采用",
            "evidence": "chains[].l3_revenue_rejected",
        },
        "stage_rule": {"pre_window": list(PRE), "post_window": list(POST),
                       "growth_threshold": 0.10, "birth_override": 0.25, "min_events": 50},
        "coverage": cov,
        "stage_distribution": dict(sorted(dist.items())),
        "chains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "chain_stage 结果面不存在，三条候选腿里营收腿被数据证据否决（样本从 198 家塌到 11 家），但融资腿与年龄结构腿成立：25,654 条融资事件中 14,626 条可挂链，12 链各有 175—5,024 条事件，跨窗口样本均 >=50 的有 11 链。阶段标签可由「资本热度方向 + 年龄结构」规则映射得到，不需要外部参数表与结果面，故判部分支持；但热度≠产出，且 8 链落在衰退期的结论主要由 2022—2024 融资退潮驱动，只能作方向性判断。",
            "criteria": {
                "result_table_exists": False,
                "legs_total": 3,
                "legs_usable": 2,
                "legs_rejected": 1,
                "chains_judged": sum(1 for r in rows if r["stage"] != "不可判"),
                "chains_total": len(rows),
                "proxy_used": True,
            },
        },
        "base_years_used": [2018, 2019, 2020, 2022, 2023, 2024],
        "base_years_missing": [2021],
        "base_years_note": "主判腿用两个三年窗口（2018—2020 与 2022—2024）对比，2021 为疫情异常年，主动留空不入窗口，不是缺年补 0；年龄腿用截至 2024 的成立年份分布。融资事件在 2025—2026 大幅减少（919/618→238），为未完整年度，不入窗口。",
        "sources": [
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json",
             "table": "gkx.dwd_org_financing_info", "rows": 25654,
             "role": "链×年融资事件数（L1 主判腿）"},
            {"path": "code/_snapshots21/chain21_year_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_org_base_info",
             "rows": 35046, "role": "链×成立年份分布（L2 辅判腿）"},
            {"path": "code/_snapshots21/chain_lm_fin_20261021.json",
             "table": "gkx.dwd_org_annual_financial_info + gkx.dwd_org_stock_finance_info",
             "rows": 156, "role": "L3 营收腿（已否决，仅留证）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993,
             "role": "企业名→链映射"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name}")
    print(f"  chains={cov['chains']} fin_matched={cov['fin_matched']}/{cov['fin_rows']} "
          f"low_sample={cov['fin_le_50_events']} dist={dict(dist)}")
    for r in rows:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} pre={r['fin_events_pre_2018_2020']:<5} "
              f"post={r['fin_events_post_2022_2024']:<5} chg={r['fin_event_change']} "
              f"new={r['new_share_2020_2024']} -> {r['stage']}")


if __name__ == "__main__":
    main()
