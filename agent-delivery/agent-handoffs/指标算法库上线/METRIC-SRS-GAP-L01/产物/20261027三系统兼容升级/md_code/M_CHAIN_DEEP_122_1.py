#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""产业链周期分析模型（M_CHAIN_DEEP_122_1）—— gkx 快照口径。

只读 `code/_snapshots21/`，不连数据库。运行：python3 code/M_CHAIN_DEEP_122_1.py
产物：code/M_CHAIN_DEEP_122_1_out.json

本件口径（与旧稿刻意切割，见 DATA_FACTS §3.30 一族的「结果表不存在」）：
    周期 = 链内「新设—融资」双动能在时间轴上的相对强弱，判成 上行/见顶平台/调整。
    非周期 = 市场营收/价格/产能/库存刻画的经济周期。gkx 无 chain_market、无价格与产能表，
    dwd_org_annual_financial_info 的营收只有 2,193/90,926 行有值（§3.51），无法聚合链级营收。

两条腿的母体不同，因此不相除，只各自看增速：
    L1 新设腿：底册成立年 ∩ 链标签，逐链逐年计数（覆盖率约 2%，右端截断）。
    L2 融资腿：融资事件表按企业名挂链，逐链逐年计数（挂链率 57%）。
    两腿同向才采信方向；绝对水平不作结论。
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_122_1"
TITLE = "产业链周期分析模型"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

WIN_EARLY = (2013, 2018)
WIN_LATE = (2019, 2024)
ALT_EARLY, ALT_LATE = (2011, 2016), (2017, 2022)
MIN_SAMPLE = 500
DELTA = 0.10

# 旧稿点名的结果面表：全部不在 gkx（2026-10-22 20:31 实测 information_schema，280 张表）
ABSENT_TABLES = [
    "chain_market", "chain_cycle", "chain_stage", "chain_investment",
    "chain_enterprise_stat", "enterprise_industry_summary", "chain_national_dist",
]


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def growth(a, b):
    return None if not a else round((b - a) / float(a), 6)


def med(xs):
    return round(statistics.median(xs), 6) if xs else None


def main():
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")

    chains = [c["chain"] for c in panel["chains"]]
    cname = {c["chain"]: c["name"] for c in panel["chains"]}
    firms = {c["chain"]: c["firms"] for c in panel["chains"]}
    base_total = sum(firms.values())
    name2chain = layer["names"]

    # ---------------- L1 新设腿 ----------------
    new = defaultdict(Counter)
    for k, v in layer["chain_year"].items():
        ch, y = k.split("|")
        new[ch][int(y)] += int(v)
    new_total = sum(sum(c.values()) for c in new.values())
    new_in_win = sum(v for c in new.values() for y, v in c.items()
                     if WIN_EARLY[0] <= y <= WIN_LATE[1])

    # ---------------- L2 融资腿 ----------------
    fin_by = defaultdict(Counter)
    fin_unmapped = 0
    fin_bad_date = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        ys = str(r[6])[:4]
        if not ys.isdigit():
            fin_bad_date += 1
            continue
        if not ch:
            fin_unmapped += 1
            continue
        fin_by[ch][int(ys)] += 1
    fin_matched = sum(sum(c.values()) for c in fin_by.values())

    def wsum(counter, y0, y1):
        return sum(counter.get(y, 0) for y in range(y0, y1 + 1))

    rows = []
    for ch in chains:
        ne, nl = wsum(new[ch], *WIN_EARLY), wsum(new[ch], *WIN_LATE)
        fe, fl = wsum(fin_by[ch], *WIN_EARLY), wsum(fin_by[ch], *WIN_LATE)
        peak_year, peak_value = None, -1
        for y in range(WIN_EARLY[0], WIN_LATE[1] + 1):
            tot = new[ch].get(y, 0) + fin_by[ch].get(y, 0)
            if tot > peak_value:
                peak_year, peak_value = y, tot
        rows.append({
            "chain": ch, "chain_name": cname[ch], "firms": firms[ch],
            "new_early": ne, "new_late": nl, "fin_early": fe, "fin_late": fl,
            "g_new": growth(ne, nl), "g_fin": growth(fe, fl),
            "sample": nl + fl, "peak_year": peak_year, "peak_value": peak_value,
        })

    g_new = [r["g_new"] for r in rows if r["g_new"] is not None]
    g_fin = [r["g_fin"] for r in rows if r["g_fin"] is not None]
    m_new, m_fin = med(g_new), med(g_fin)

    for r in rows:
        rel = [x - m for x, m in ((r["g_new"], m_new), (r["g_fin"], m_fin))
               if x is not None]
        r["rel_new"] = None if r["g_new"] is None else round(r["g_new"] - m_new, 6)
        r["rel_fin"] = None if r["g_fin"] is None else round(r["g_fin"] - m_fin, 6)
        r["momentum"] = round(sum(rel) / len(rel), 6) if rel else None
        if r["sample"] < MIN_SAMPLE or r["momentum"] is None:
            r["cycle"] = "观察中（样本不足）"
        elif r["momentum"] >= DELTA:
            r["cycle"] = "上行期"
        elif r["momentum"] <= -DELTA:
            r["cycle"] = "调整期"
        else:
            r["cycle"] = "见顶平台期"

    # ---------------- 反向验证 ----------------
    counters = []

    abs_down = [r["chain_name"] for r in rows if r["g_fin"] is not None and r["g_fin"] <= -0.30]
    abs_up = [r["chain_name"] for r in rows if r["g_fin"] is not None and r["g_fin"] >= 0.30]
    counters.append({
        "check": "绝对阈值法（g_fin≥+30% 上行 / ≤−30% 调整）会把几条链判成衰退",
        "up_chains": abs_up, "down_chains": abs_down,
        "down_n": len(abs_down), "up_n": len(abs_up),
        "conclusion": "12 条链的融资增速中位数为 %s；按绝对阈值有 %d 条被记为调整、%d 条记为上行，"
                      "把「全行业融资市场降温」误读成「个别链衰退」。故改用相对 12 链中位数的动能。"
                      % (m_fin, len(abs_down), len(abs_up)),
    })

    tail = {}
    for y in (2022, 2023, 2024, 2025, 2026):
        tail[y] = {"new": sum(new[c].get(y, 0) for c in chains),
                   "fin": sum(fin_by[c].get(y, 0) for c in chains)}
    counters.append({
        "check": "窗口为什么止于 2024：尾年是否为不完整年",
        "national_by_year": {str(k): v for k, v in tail.items()},
        "conclusion": "新设腿 2024 年 %d 家、2025 年 %d 家、2026 年 %d 家；2025/2026 是半个年度，"
                      "纳入会把右端截断误判成断崖。融资腿 2026 年 %d 起同样不完整。"
                      % (tail[2024]["new"], tail[2025]["new"], tail[2026]["new"], tail[2026]["fin"]),
    })

    counters.append({
        "check": "新设腿只有 %d 家，能否代表 %d 家母体" % (new_total, base_total),
        "new_firm_matched": new_total,
        "chain_firms": base_total,
        "coverage": round(new_total / float(base_total), 6),
        "conclusion": "新设腿覆盖率 %.2f%%（底册成立年 ∩ 链标签，且一企多链会重复计数），"
                      "只能看形状不能看绝对量；融资腿独立成源、挂链 %d/%d 起，两腿同向才采信方向。"
                      % (100.0 * new_total / base_total, fin_matched, len(fin["fin"])),
    })

    alt = {}
    for ch in chains:
        ne, nl = wsum(new[ch], *ALT_EARLY), wsum(new[ch], *ALT_LATE)
        fe, fl = wsum(fin_by[ch], *ALT_EARLY), wsum(fin_by[ch], *ALT_LATE)
        alt[ch] = {"g_new": growth(ne, nl), "g_fin": growth(fe, fl)}
    am_new = med([v["g_new"] for v in alt.values() if v["g_new"] is not None])
    am_fin = med([v["g_fin"] for v in alt.values() if v["g_fin"] is not None])
    flips = []
    for r in rows:
        v = alt[r["chain"]]
        rel = [x - m for x, m in ((v["g_new"], am_new), (v["g_fin"], am_fin))
               if x is not None]
        mom = sum(rel) / len(rel) if rel else None
        lab = ("上行期" if mom is not None and mom >= DELTA else
               ("调整期" if mom is not None and mom <= -DELTA else "见顶平台期"))
        r["alt_momentum"] = None if mom is None else round(mom, 6)
        if lab != r["cycle"]:
            flips.append({"chain": r["chain_name"], "main": r["cycle"], "alt": lab,
                          "alt_momentum": r["alt_momentum"]})
    counters.append({
        "check": "换窗口（%d-%d vs %d-%d）标签是否稳定" % (ALT_EARLY + ALT_LATE),
        "alt_median_g_new": am_new, "alt_median_g_fin": am_fin,
        "flip_n": len(flips), "flips": flips,
        "conclusion": "12 条链中 %d 条标签翻转、%d 条稳定；翻转链逐条列入正文，不隐藏。"
                      % (len(flips), 12 - len(flips)),
    })

    order = {"上行期": 0, "见顶平台期": 1, "调整期": 2, "观察中（样本不足）": 3}
    rows.sort(key=lambda r: (order[r["cycle"]],
                             -(r["momentum"] if r["momentum"] is not None else -9)))
    stage_count = Counter(r["cycle"] for r in rows)

    result = {
        "metric_id": METRIC,
        "title": TITLE,
        "support_judgment": "部分支持",
        "judgment_reason": (
            "时间轴上的双动能（链内新设企业数、挂链融资事件数）可从 gkx 快照得到，12 条链全部出标签；"
            "但旧稿的「产业周期」以市场规模/增长率/利润率/投融资额为状态量，"
            "gkx 无 chain_market、无 chain_cycle 等 7 张结果表（information_schema 实测 absent），"
            "财务表营收仅 2,193/90,926 行有值，故只交付相对动能周期，不交付价格/产能/利润周期。"
        ),
        "judgment_reason_kind": "dimension_gap",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "params": {
            "windows": {"early": list(WIN_EARLY), "late": list(WIN_LATE)},
            "alt_windows": {"early": list(ALT_EARLY), "late": list(ALT_LATE)},
            "stage_delta": DELTA, "min_sample": MIN_SAMPLE,
            "threshold_note": "±0.10 的动能阈值与 500 的最小样本为【本件自定义、待甲方确认】，"
                              "不是外部权威分档；口径是「相对 12 链中位数」，不是绝对景气度。",
        },
        "compute": {
            "chain_count": len(chains),
            "chain_firms_total": base_total,
            "new_firm_matched": new_total,
            "new_firm_in_window": new_in_win,
            "new_firm_coverage": round(new_total / float(base_total), 6),
            "fin_events_table": len(fin["fin"]),
            "fin_events_matched_chain": fin_matched,
            "fin_unmapped": fin_unmapped,
            "fin_bad_date": fin_bad_date,
            "fin_match_rate": round(fin_matched / float(len(fin["fin"])), 6),
            "median_g_new": m_new, "median_g_fin": m_fin,
            "national_by_year": {str(y): {"new": sum(new[c].get(y, 0) for c in chains),
                                          "fin": sum(fin_by[c].get(y, 0) for c in chains)}
                                 for y in range(2013, 2025)},
            "stage_count": dict(stage_count),
            "chains": rows,
        },
        "share_basis": {
            "growth_new": "分子分母都是同一链、同一来源的新设企业计数（6 年窗口合计），"
                          "窗口原始计数已落 new_early/new_late",
            "growth_fin": "分子分母都是同一链、同一来源的挂链融资事件计数，"
                          "窗口原始计数已落 fin_early/fin_late",
            "no_cross_ratio": "新设腿与融资腿母体不同，未做任何相除；coverage 的分子分母同源（底册∩链标签 / 链企业总数）",
        },
        "probes": [{
            "probe": "information_schema.tables 拉全库 280 张表名后内存匹配旧稿结果表",
            "absent": ABSENT_TABLES,
            "present": [],
            "checked_at": "2026-10-22T20:31+08:00",
            "note": "查表名为只读元数据查询，不触达业务数据；absent 即表不存在，不是「查询失败」。",
        }],
        "sources": [
            {"path": "code/_snapshots21/chain21_layer_20261022.json", "kind": "snapshot",
             "note": "链内新设企业逐年计数（chain_year，底册成立年 ∩ 链标签）与名称→链映射"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json", "kind": "snapshot",
             "note": "融资事件 25,654 起（org_id/企业名/轮次/完成日期）"},
            {"path": "code/_snapshots21/chain_panel21.json", "kind": "snapshot",
             "note": "12 链企业数、深圳企业数、专利与融资覆盖"},
            {"path": "code/_snapshots21/domain_constants.json", "kind": "snapshot",
             "note": "项目级共享常量（链企业母体 1,714,458）"},
        ],
        "base_years_used": list(range(WIN_EARLY[0], WIN_LATE[1] + 1)),
        "base_years_missing": [],
        "base_years_note": (
            "两窗各 6 年：2013—2018 与 2019—2024，端点年份在 params.windows 与 "
            "compute.national_by_year 双落盘。2025/2026 为不完整年，主动排除并已写入 "
            "counter_checks（新设 2025 年 %d 家、2026 年 %d 家），不按 0 摊入分母。"
            % (tail[2025]["new"], tail[2026]["new"])
        ),
        "missing_dims": [
            {"dim": "市场规模/营收时间序列",
             "why": "gkx 无 chain_market；dwd_org_annual_financial_info 营收仅 2,193/90,926 行有值，"
                    "且无链级汇总面",
             "fill": "接入规上工业产值或链主企业年报营收（按链标注）"},
            {"dim": "利润率", "why": "同表 pure_profit 2,349 行有值（2.58%），链内样本个位数",
             "fill": "补齐链内企业年报利润后再做链级汇总"},
            {"dim": "价格/产能/库存", "why": "gkx 280 张表里无价格指数、产能利用率、库存表",
             "fill": "接入行业价格指数（PPIRM 分行业）与产能利用率"},
            {"dim": "周期阈值的外部标定", "why": "库内无周期阶段参数表，本件阈值自定",
             "fill": "由甲方给出行业景气阈值或历史回测拐点"},
        ],
        "notes": [
            "本件是「相对动能周期」：只回答某链在 12 链中相对变强还是变弱，不回答绝对市场规模涨跌。",
            "与 M_CHAIN_DEEP_123_1 的边界：122 沿时间轴切阶段，123 用横截面结构（高技术占比、投资强度、环节深度）判阶段；"
            "两件共用企业母体，但不共用判据。",
            "与 M_CHAIN_DEEP_119_1 的关系：119 用同一批新设/融资数做「事件累计分位」，本件做两窗增速对比；"
            "同一母体、不同问法，数值不可互换。",
            "新设腿存在右端截断：底册对 2022 年后注册的企业收录不全，导致 12 条链的 g_new 全为负。"
            "这一形状不能读成「全行业萎缩」，只能读成「相对排序」。",
        ],
        "counter_checks": counters,
        "elapsed_sec": None,
    }
    result.pop("elapsed_sec")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("[ok]", OUT)
    print("判档 %s | 阶段 %s" % (result["support_judgment"], dict(stage_count)))
    for r in rows:
        print("  %-10s %-14s g_new=%+.3f g_fin=%+.3f mom=%+.3f peak=%s"
              % (r["chain_name"], r["cycle"], r["g_new"] or 0, r["g_fin"] or 0,
                 r["momentum"] or 0, r["peak_year"]))
    print("母体 %d | 新设覆盖 %d (%.2f%%) | 挂链融资 %d/%d"
          % (base_total, new_total, 100.0 * new_total / base_total, fin_matched, len(fin["fin"])))


if __name__ == "__main__":
    main()
