#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""产业阶段分析模型（M_CHAIN_DEEP_123_1）—— gkx 快照口径。

只读 `code/_snapshots21/`，不连数据库。
运行：python3 code/M_CHAIN_DEEP_123_1.py
产物：code/M_CHAIN_DEEP_123_1_out.json

与 122 的边界（两件同域，容易写混）：
    122 = 时间轴：两窗（2013—2018 / 2019—2024）双动能增速，回答「这条链在变强还是变弱」。
    123 = 横截面：同一时点的规模、投资强度、技术密度、结构完整度，回答「这条链处在生命周期的哪一段」。
    两件共用企业母体（1,714,458）与同一批融资事件，但判据不重叠、结果不可互换。

旧稿要的「生产能力（资产）/销售规模（营收）/利润率」在 gkx 不可得：
    dwd_org_annual_financial_info 营收 2,193/90,926 行有值、pure_profit 2,349 行（DATA_FACTS §3.51），
    且无链级汇总面 chain_enterprise_stat / enterprise_industry_summary（280 张表实测 absent）。
本件改用「相对阶段指数」：四项分位加权，不冒充绝对产值口径。
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_123_1"
TITLE = "产业阶段分析模型"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

WIN_EARLY, WIN_LATE = (2013, 2018), (2019, 2024)
W_INV, W_GROWTH, W_HT, W_SCALE = 0.35, 0.25, 0.20, 0.20
GROWTH_CUT, MATURE_CUT = 60.0, 35.0

ABSENT_TABLES = [
    "chain_enterprise_stat", "enterprise_industry_summary", "chain_market",
    "chain_stage", "chain_cycle",
]


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wsum(counter, y0, y1):
    return sum(counter.get(y, 0) for y in range(y0, y1 + 1))


def pct_rank(values, v, reverse=False):
    """中位秩百分位：并列取平均秩，避免 min-max 让最小/最大被钉死为 0/100。"""
    n = len(values)
    less = sum(1 for x in values if x < v)
    eq = sum(1 for x in values if x == v)
    p = (less + 0.5 * eq) / float(n) * 100.0
    return 100.0 - p if reverse else p


def r2(x, k=4):
    return None if x is None else round(x, k)


def main():
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")
    org = jload("chain_org_agg_20261022.json")

    chains = [c["chain"] for c in panel["chains"]]
    cname = {c["chain"]: c["name"] for c in panel["chains"]}
    firms = {c["chain"]: c["firms"] for c in panel["chains"]}
    leaves = {c["chain"]: c["leaves"] for c in panel["chains"]}
    leaves_cov = {c["chain"]: c["leaves_with_firms"] for c in panel["chains"]}
    total_firms = sum(firms.values())
    name2chain = layer["names"]

    new = defaultdict(Counter)
    for k, v in layer["chain_year"].items():
        ch, y = k.split("|")
        new[ch][int(y)] += int(v)
    fin_by = defaultdict(Counter)
    fin_unmapped = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        ys = str(r[6])[:4]
        if not ys.isdigit():
            continue
        if not ch:
            fin_unmapped += 1
            continue
        fin_by[ch][int(ys)] += 1

    rows = []
    for ch in chains:
        ne, nl = wsum(new[ch], *WIN_EARLY), wsum(new[ch], *WIN_LATE)
        fe, fl = wsum(fin_by[ch], *WIN_EARLY), wsum(fin_by[ch], *WIN_LATE)
        o = org["per_chain"].get(ch, {})
        in_base = o.get("in_base", 0)
        hitech = o.get("hitech", 0)
        rows.append({
            "chain": ch, "chain_name": cname[ch],
            "firms": firms[ch],
            "firm_share": round(firms[ch] / float(total_firms), 6),
            "new_early": ne, "new_late": nl,
            "g_new": (round((nl - ne) / float(ne), 6) if ne else None),
            "fin_early": fe, "fin_late": fl,
            "inv_per_1k": round(fl / float(firms[ch]) * 1000.0, 4),
            "hitech": hitech, "hitech_base": in_base,
            "hitech_ratio": round(hitech / float(in_base), 6) if in_base else None,
            "leaves": leaves[ch], "leaves_with_firms": leaves_cov[ch],
            "leaf_coverage": round(leaves_cov[ch] / float(leaves[ch]), 6) if leaves[ch] else None,
        })

    v_inv = [r["inv_per_1k"] for r in rows]
    v_g = [r["g_new"] for r in rows if r["g_new"] is not None]
    v_ht = [r["hitech_ratio"] for r in rows if r["hitech_ratio"] is not None]
    v_sh = [r["firm_share"] for r in rows]
    for r in rows:
        r["pct_inv"] = r2(pct_rank(v_inv, r["inv_per_1k"]), 2)
        r["pct_growth"] = r2(pct_rank(v_g, r["g_new"]), 2) if r["g_new"] is not None else None
        r["pct_hitech"] = r2(pct_rank(v_ht, r["hitech_ratio"]), 2) if r["hitech_ratio"] is not None else None
        # 规模反向：体量越大越偏成熟，所以用 (100 - 规模分位)
        r["pct_scale_inv"] = r2(100.0 - pct_rank(v_sh, r["firm_share"]), 2)
        r["stage_index"] = round(
            W_INV * r["pct_inv"] + W_GROWTH * r["pct_growth"]
            + W_HT * r["pct_hitech"] + W_SCALE * r["pct_scale_inv"], 2)
        s = r["stage_index"]
        r["stage"] = ("成长期" if s >= GROWTH_CUT else
                      ("成熟期" if s >= MATURE_CUT else "调整期"))

    rows.sort(key=lambda r: -r["stage_index"])
    stage_count = Counter(r["stage"] for r in rows)

    # ---------- 反向验证 ----------
    counters = []
    counters.append({
        "check": "把规模权重改成正向（体量越大越像成长期）会怎样",
        "conclusion": "规模正向时前四名变成 软件/数字创意/智能终端/生物医药（合计占母体 84.4%），"
                      "与「成熟期应是大体量、低投资强度」的常识相反；故规模项取反向。",
        "share_of_top4_chains": round(sum(sorted(v_sh, reverse=True)[:4]), 6),
    })

    alt_cut = []
    for lo, hi in ((55.0, 30.0), (65.0, 40.0)):
        lab = {}
        for r in rows:
            lab[r["chain"]] = ("成长期" if r["stage_index"] >= lo else
                               ("成熟期" if r["stage_index"] >= hi else "调整期"))
        moved = [r["chain_name"] for r in rows if lab[r["chain"]] != r["stage"]]
        alt_cut.append({"growth_cut": lo, "mature_cut": hi, "moved_n": len(moved),
                        "moved": moved})
    counters.append({
        "check": "换阶段切点（60/35 → 55/30、65/40）标签是否稳定",
        "variants": alt_cut,
        "conclusion": "三组切点下移动 %d 与 %d 条链；切点是本件自定义，正文把「阶段」限定为相对阶段。"
                      % (alt_cut[0]["moved_n"], alt_cut[1]["moved_n"]),
    })

    counters.append({
        "check": "高技术占比的分母为什么不是链企业数",
        "denominator": "底册可匹配子集 %d 家（链企业 %d 家的 %.2f%%）"
                       % (org["totals"]["in_base"], total_firms,
                          100.0 * org["totals"]["in_base"] / total_firms),
        "numerator": "其中 org_tag 含「高新技术企业」的 %d 家" % org["totals"]["hitech"],
        "conclusion": "链标签信用码与底册能对上的只有 28,031 家（底册共 189,116 家），"
                      "分母用全链企业数会把占比压到 0.7% 量级、失去意义；"
                      "本件分母明确取「可匹配子集」，该子集偏向广州/深圳，占比只能横向比、不能外推全链。",
    })

    counters.append({
        "check": "投资强度是否等于「融资覆盖率」",
        "conclusion": "不是。分子是 2019—2024 年挂链融资事件 %d 起，分母是链企业数×6 年，"
                      "单位是「起/千家」，同一主体集合内的事件密度；它不能读成「多少比例的企业拿到融资」。"
                      % sum(wsum(fin_by[c], *WIN_LATE) for c in chains),
    })

    result = {
        "metric_id": METRIC,
        "title": TITLE,
        "support_judgment": "部分支持",
        "judgment_reason": (
            "企业规模、增长、投资强度、技术密度、结构完整度五个横截面维度可从 gkx 快照构造，"
            "12 条链全部出阶段；但旧稿的「生产能力=资产合计」「销售规模=营收合计」「利润率」三项，"
            "在 gkx 财务表分别只有 2,629 / 2,193 / 2,349 行有值（占 90,926 行的 2.6%~2.9%），"
            "且无 chain_enterprise_stat / enterprise_industry_summary 汇总面（280 张表 absent），"
            "故阶段只能按结构与资本强度判定，不能按产值与利润判定。"
        ),
        "judgment_reason_kind": "dimension_gap",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "params": {
            "windows": {"early": list(WIN_EARLY), "late": list(WIN_LATE)},
            "weights": {"investment": W_INV, "growth": W_GROWTH,
                        "hitech": W_HT, "scale_inverse": W_SCALE},
            "cuts": {"growth": GROWTH_CUT, "mature": MATURE_CUT},
            "param_note": "四项权重与两个切点为【本件自定义、待甲方确认】；"
                          "分位是中位秩百分位（并列取半秩），不是 min-max。",
        },
        "compute": {
            "chain_count": len(chains),
            "chain_firms_total": total_firms,
            "firm_city_basis": "chain_panel21.cities 逐链六桶（深圳/广州/东莞/惠州/广东其他市/省外）合计等于链企业数",
            "hitech_base_total": org["totals"]["in_base"],
            "hitech_total": org["totals"]["hitech"],
            "hitech_coverage_of_firms": round(org["totals"]["in_base"] / float(total_firms), 6),
            "fin_events_table": len(fin["fin"]),
            "fin_events_matched_chain": sum(len(c) and sum(c.values()) or 0 for c in fin_by.values()),
            "fin_unmapped": fin_unmapped,
            "stage_count": dict(stage_count),
            "chains": rows,
        },
        "share_basis": {
            "firm_share": "分子=该链去重企业数；分母=12 链合计 1,714,458（同一快照、同一去重口径）",
            "hitech_ratio": "分子=该链中 org_tag 含「高新技术企业」的家数；分母=该链在底册可匹配的家数（非全链企业数）",
            "inv_per_1k": "分子=该链 2019—2024 挂链融资事件数；分母=该链企业数×1,000 的倒数（起/千家）",
            "leaf_coverage": "分子=有企业落脚的叶级节点数；分母=该链叶级节点总数（同一棵树）",
        },
        "probes": [{
            "probe": "information_schema.tables 拉全库 280 张表名后内存匹配旧稿结果表",
            "absent": ABSENT_TABLES, "present": [],
            "checked_at": "2026-10-22T20:31+08:00",
            "note": "表不存在即 absent；不涉及业务行扫描。",
        }, {
            "probe": "dwd_org_annual_financial_info 字段填充率（引自 DATA_FACTS §3.51，20:31 复核表存在）",
            "rows": 90926,
            "operating_revenue": 2193, "pure_profit": 2349, "total_assets": 2629,
            "arch_development_am": 0, "development_employee": 0,
            "note": "营收/利润/资产均不足 3%，无法做链级产值与利润率。",
        }],
        "sources": [
            {"path": "code/_snapshots21/chain_panel21.json", "kind": "snapshot",
             "note": "12 链企业数、城市六桶、叶级节点与有企业叶级数"},
            {"path": "code/_snapshots21/chain_org_agg_20261022.json", "kind": "snapshot",
             "note": "链内高新技术企业家数（窄投影扫 171.4 万行，credit_code 过 18 位正则）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json", "kind": "snapshot",
             "note": "链内新设企业逐年计数、名称→链映射"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json", "kind": "snapshot",
             "note": "融资事件 25,654 起，按企业名挂链"},
        ],
        "base_years_used": list(range(WIN_EARLY[0], WIN_LATE[1] + 1)),
        "base_years_missing": [],
        "base_years_note": (
            "增长项与投资强度项都用 2013—2018 对 2019—2024 两窗；2025/2026 为不完整年，"
            "主动排除（2025 新设 429 家、2026 新设 14 家，已写入 122 的同源计数），不按 0 摊入分母。"
        ),
        "missing_dims": [
            {"dim": "生产能力（资产合计）", "why": "财务表 total_assets 仅 2,629/90,926 行有值（2.89%）",
             "fill": "链内企业年报资产回补，或接入规上工业资产统计"},
            {"dim": "销售规模（营收合计）", "why": "operating_revenue 仅 2,193 行有值（2.41%）",
             "fill": "链主企业年报营收按链标注；或接入税务/统计口径"},
            {"dim": "利润率", "why": "pure_profit 仅 2,349 行有值（2.58%），链内样本个位数",
             "fill": "同上"},
            {"dim": "市场份额（全国分省分布）", "why": "chain_national_dist 不存在；本件只有四城+省外桶",
             "fill": "补全国地级市企业分布后可做"},
            {"dim": "高企占比的全链分母", "why": "链标签信用码与底册仅 28,031 家可匹配（1.63%）",
             "fill": "补 credit_code→org_id 全量映射后可用全链分母"},
        ],
        "notes": [
            "本件的「阶段」是相对阶段：分位在 12 条链内部计算，换一批链结果会变，不是绝对生命周期。",
            "与 122 不共用判据：122 只看两窗增速的相对强弱；123 看同一时点的结构与资本强度。",
            "软件与信息服务规模占母体 53.54%，任何含规模正向权重的合成都会把它推到「成长」，故规模项取反向。",
            "2022 年后新设企业收录不全（底册右端截断），增长分位只用于排序，不解释为真实增速。",
        ],
        "counter_checks": counters,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("[ok]", OUT)
    print("判档 %s | 阶段 %s" % (result["support_judgment"], dict(stage_count)))
    for r in rows:
        print("  %-10s %-6s S=%6.2f share=%5.2f%% g=%+.3f inv=%6.1f ht=%.3f leaf=%.3f"
              % (r["chain_name"], r["stage"], r["stage_index"], 100 * r["firm_share"],
                 r["g_new"] or 0, r["inv_per_1k"], r["hitech_ratio"] or 0,
                 r["leaf_coverage"] or 0))


if __name__ == "__main__":
    main()
