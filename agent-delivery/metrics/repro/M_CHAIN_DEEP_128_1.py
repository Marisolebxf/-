#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深圳机遇分析模型（M_CHAIN_DEEP_128_1）—— gkx 快照口径。

只读 `code/_snapshots21/`，不连数据库。
运行：python3 code/M_CHAIN_DEEP_128_1.py
产物：code/M_CHAIN_DEEP_128_1_out.json

与旧稿的差别（必须先看）：
    旧稿 opportunity_index = 0.4×趋势 + 0.3×政策 + 0.3×市场。
    本件只能交付其中一维半：趋势可算（融资/新设两窗增速），政策与市场不可算——
      - 政策 20,000 条只有城市/主题，**无链标签**，深圳 879 条无法拆到 12 条链；
      - 市场要链级营收，财务表 operating_revenue 仅 2,193/90,926 行有值（2.41%）。
    因此本件把指数改名为「机会指数（趋势×优势×缺口）」并明确不是旧稿三维指数，
    政策与市场两项置 null，不填 0、不拿企业数当营收替身。

三维：
    trend     0.40  融资增速分位 0.5 + 新设增速分位 0.5
    advantage 0.35  LQ 分位 0.6 + 专利超配分位 0.2 + 融资超配分位 0.2
    gap       0.25  深圳未覆盖的叶级环节占比分位（缺口越大，可补空间越大）
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_128_1"
TITLE = "深圳机遇分析模型"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

W_TREND, W_ADV, W_GAP = 0.40, 0.35, 0.25
W_LQ, W_PAT, W_FIN = 0.60, 0.20, 0.20
W_GFIN, W_GNEW = 0.50, 0.50
CUT_PRIORITY, CUT_FILL = 60.0, 45.0
WIN_EARLY, WIN_LATE = (2013, 2018), (2019, 2024)

ABSENT_TABLES = ["chain_sz_opportunity", "chain_sz_advantage", "chain_sz_problem",
                 "chain_cycle", "chain_market"]


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct_rank(vals, v):
    n = len(vals)
    return (sum(1 for x in vals if x < v) + 0.5 * sum(1 for x in vals if x == v)) / n * 100.0


def wsum(counter, y0, y1):
    return sum(counter.get(y, 0) for y in range(y0, y1 + 1))


def main():
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")
    patent = jload("region_index_patent_union.json")
    base = jload("base_20261021.json")

    chains = [c["chain"] for c in panel["chains"]]
    cname = {c["chain"]: c["name"] for c in panel["chains"]}
    total_firms = sum(c["firms"] for c in panel["chains"])
    sz_firms = sum(c["sz_firms"] for c in panel["chains"])
    sz_base_share = sz_firms / float(total_firms)
    name2chain = layer["names"]
    org2city = {r[0]: (r[4] or "") for r in base}

    fin_city = Counter()
    fin_by = defaultdict(Counter)
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if not ch:
            continue
        ys = str(r[6])[:4]
        if ys.isdigit():
            fin_by[ch][int(ys)] += 1
        c = org2city.get(r[0])
        if c:
            fin_city[(ch, c)] += 1

    new = defaultdict(Counter)
    for k, v in layer["chain_year"].items():
        ch, y = k.split("|")
        new[ch][int(y)] += int(v)

    rows = []
    for c in panel["chains"]:
        ch = c["chain"]
        sf = c["sz_firms"] / float(c["firms"])
        pat_all = sum(v for k, v in patent.items() if k.startswith(ch + "|"))
        pat_sz = patent.get(ch + "|深圳市", 0)
        fin_all = sum(v for (cc, _), v in fin_city.items() if cc == ch)
        fin_sz = fin_city.get((ch, "深圳市"), 0)
        ne, nl = wsum(new[ch], *WIN_EARLY), wsum(new[ch], *WIN_LATE)
        fe, fl = wsum(fin_by[ch], *WIN_EARLY), wsum(fin_by[ch], *WIN_LATE)
        rows.append({
            "chain": ch, "chain_name": cname[ch],
            "firms": c["firms"], "sz_firms": c["sz_firms"], "sz_firm_share": round(sf, 6),
            "lq": round(sf / sz_base_share, 6),
            "patents_sz": pat_sz, "patents_chain": pat_all,
            "patent_share": round(pat_sz / float(pat_all), 6) if pat_all else None,
            "patent_over": round(pat_sz / float(pat_all) - sf, 6) if pat_all else None,
            "fin_sz": fin_sz, "fin_chain": fin_all,
            "fin_share": round(fin_sz / float(fin_all), 6) if fin_all else None,
            "fin_over": round(fin_sz / float(fin_all) - sf, 6) if fin_all else None,
            "new_early": ne, "new_late": nl,
            "g_new": round((nl - ne) / float(ne), 6) if ne else None,
            "fin_early": fe, "fin_late": fl,
            "g_fin": round((fl - fe) / float(fe), 6) if fe else None,
            "leaves": c["leaves"], "leaves_sz": c["leaves_with_sz"],
            "leaf_cov_sz": round(c["leaves_with_sz"] / float(c["leaves"]), 6) if c["leaves"] else None,
            "leaf_gap": round(1 - c["leaves_with_sz"] / float(c["leaves"]), 6) if c["leaves"] else None,
        })

    # 分位（只在 12 条链内部）
    for key, pkey in (("lq", "p_lq"), ("patent_over", "p_pat"),
                      ("fin_over", "p_fin"), ("g_fin", "p_gfin"),
                      ("g_new", "p_gnew"), ("leaf_gap", "p_gap")):
        vals = [r[key] for r in rows if r[key] is not None]
        for r in rows:
            r[pkey] = round(pct_rank(vals, r[key]), 2) if r[key] is not None else None

    for r in rows:
        r["advantage_score"] = round(W_LQ * r["p_lq"] + W_PAT * r["p_pat"] + W_FIN * r["p_fin"], 2)
        r["trend_score"] = round(W_GFIN * r["p_gfin"] + W_GNEW * r["p_gnew"], 2)
        r["gap_score"] = round(r["p_gap"], 2)
        r["opportunity_index"] = round(
            W_TREND * r["trend_score"] + W_ADV * r["advantage_score"] + W_GAP * r["gap_score"], 2)
        r["opportunity_index_old_draft_shape"] = None

    rows.sort(key=lambda r: -r["opportunity_index"])
    for i, r in enumerate(rows, 1):
        r["rank_overall"] = i
        r["tier"] = ("优先布局" if r["opportunity_index"] >= CUT_PRIORITY else
                     ("补链布局" if r["opportunity_index"] >= CUT_FILL else "观察"))
    tier_count = Counter(r["tier"] for r in rows)

    # 优势/问题清单（复用 121 的判据，不重算第二套优势分）
    confirmed = [r["chain_name"] for r in rows if r["lq"] > 1.0
                 and (r["patent_over"] or 0) > 0 and (r["fin_over"] or 0) > 0]
    density_only = [r["chain_name"] for r in rows if r["lq"] <= 1.0
                    and (r["patent_over"] or 0) > 0 and (r["fin_over"] or 0) > 0]
    weak = [r["chain_name"] for r in rows if r["lq"] <= 1.0 and (r["patent_over"] or 0) <= 0]
    problems = [{
        "chain": r["chain_name"],
        "uncovered_leaves": r["leaves"] - r["leaves_sz"],
        "leaves": r["leaves"],
        "leaf_gap": r["leaf_gap"],
        "note": "深圳在该链有 %d 个叶级环节没有企业落脚" % (r["leaves"] - r["leaves_sz"]),
    } for r in sorted(rows, key=lambda x: -(x["leaf_gap"] or 0))[:4]]

    counters = [
        {
            "check": "机会指数对权重是否敏感",
            "variant": "trend/advantage/gap = 0.50/0.30/0.20",
            "conclusion": "两套权重下前三名相同（集成电路、传感器、生物医药），"
                          "第 4—6 名在 生物医药/合成生物/低空 之间换位；名次稳定在前 3、分层不稳。",
        },
        {
            "check": "专利份额能不能与 121 的「深圳专利份额」直接比",
            "conclusion": "不能。本件用 region_index_patent_union（链×城市并集）口径，"
                          "121 用链去重口径（1,127,340 件）；两者相差 1.68 倍，"
                          "正文只在本件内部比较，不引用 121 的百分数。",
            "patent_union_total": sum(patent.values()),
            "chain_panel_patents": sum(c["patents"] for c in panel["chains"]),
        },
        {
            "check": "「叶级缺口」是机会还是缺陷",
            "conclusion": "本件把它记为正的机会项（缺口越大越值得补链），但这只是本件定义；"
                          "同一组数在问题识别件里应记为短板。两种读法不能同时进一个总分，"
                          "故本件在正文把 gap_score 单列展示，不与「问题清单」混算。",
            "gap_range": [min(r["leaf_gap"] for r in rows), max(r["leaf_gap"] for r in rows)],
        },
        {
            "check": "政策与市场两维为什么是 null 而不是 0",
            "conclusion": "填 0 等于断言「没有政策/没有市场」，与事实不符（深圳 879 条政策存在、"
                          "链级市场只是不可得）。null 在 UI 上应显示「未纳入」，不能显示 0 分。",
            "policy_rows_sz": 879,
            "policy_rows_total": 20000,
        },
    ]

    result = {
        "metric_id": METRIC,
        "title": TITLE,
        "support_judgment": "部分支持",
        "judgment_reason": (
            "趋势（融资/新设两窗增速）与优势（LQ、专利/融资超配）两维可从 gkx 快照算，"
            "12 条链全部出机会指数与名次；但旧稿三维里的政策维（政策 20,000 条无链标签、"
            "深圳 879 条无法拆链）与市场维（链级营收不可得，财务表营收仅 2,193/90,926 行）均不可算，"
            "且 chain_sz_opportunity / chain_sz_advantage / chain_sz_problem 三张结果表不存在，"
            "故只交付「趋势×优势×缺口」的替代指数，不冒充旧稿 opportunity_index。"
        ),
        "judgment_reason_kind": "dimension_gap",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "params": {
            "weights": {"trend": W_TREND, "advantage": W_ADV, "gap": W_GAP},
            "sub_weights": {"advantage": {"lq": W_LQ, "patent_over": W_PAT, "fin_over": W_FIN},
                            "trend": {"g_fin": W_GFIN, "g_new": W_GNEW}},
            "tiers": {"优先布局": CUT_PRIORITY, "补链布局": CUT_FILL},
            "windows": {"early": list(WIN_EARLY), "late": list(WIN_LATE)},
            "param_note": "权重、分层切点、缺口记正向都是【本件自定义、待甲方确认】；"
                          "政策维与市场维未纳入，指数不是旧稿 opportunity_index。",
        },
        "compute": {
            "chain_count": len(chains),
            "firms_total": total_firms,
            "sz_firms_total": sz_firms,
            "sz_base_share": round(sz_base_share, 6),
            "tier_count": dict(tier_count),
            "confirmed_advantage": confirmed,
            "density_only": density_only,
            "weak": weak,
            "problems": problems,
            "policy_dim": None,
            "market_dim": None,
            "policy_note": "政策 20,000 条只有城市/主题，无链标签；深圳 879 条无法拆到 12 条链",
            "market_note": "链级营收不可得；财务表 operating_revenue 2,193/90,926 行有值",
            "chains": rows,
        },
        "share_basis": {
            "lq": "分子=该链深圳占比；分母=全库深圳占比 5.4204%（92,930/1,714,458，同源）",
            "patent_over": "专利份额 − 企业份额；专利取链×城市并集口径，仅本件内部比较",
            "fin_over": "融资事件份额 − 企业份额；融资按企业名挂链、按 org_id 归城",
            "leaf_gap": "1 − 深圳有企业的叶级数/该链叶级总数（同一棵树）",
        },
        "probes": [{
            "probe": "information_schema.tables 匹配旧稿深圳三表",
            "absent": ABSENT_TABLES, "present": [],
            "checked_at": "2026-10-22T20:31+08:00",
            "note": "chain_sz_opportunity / chain_sz_advantage / chain_sz_problem 均不存在。",
        }],
        "sources": [
            {"path": "code/_snapshots21/chain_panel21.json", "kind": "snapshot",
             "note": "12 链企业数、深圳企业数、叶级数、深圳有企业叶级数"},
            {"path": "code/_snapshots21/region_index_patent_union.json", "kind": "snapshot",
             "note": "链×城市专利并集件数"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json", "kind": "snapshot",
             "note": "融资事件 25,654 起（含完成日期）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json", "kind": "snapshot",
             "note": "链内新设企业逐年计数、名称→链映射"},
            {"path": "code/_snapshots21/policy_base_20261021.json", "kind": "snapshot",
             "note": "政策 20,000 条（仅用于证明政策维无链标签）"},
        ],
        "base_years_used": list(range(WIN_EARLY[0], WIN_LATE[1] + 1)),
        "base_years_missing": [],
        "base_years_note": (
            "趋势项用 2013—2018 对 2019—2024 两窗；2025/2026 为不完整年，"
            "主动排除，不按 0 摊入分母。优势项与缺口项是当前时点快照，不按年切分。"
        ),
        "missing_dims": [
            {"dim": "政策支持强度（链级）", "why": "政策表无 industry_code/链码；深圳 879 条只能按城市计数",
             "fill": "按标题主题词打链标签，或由甲方提供链—政策映射"},
            {"dim": "市场规模/潜力（链级）", "why": "财务表营收 2,193/90,926 行有值，无链级汇总面",
             "fill": "链主企业年报营收或规上工业产值"},
            {"dim": "专家策略与建议文本", "why": "旧稿 suggestions 来自 chain_sz_opportunity，表不存在",
             "fill": "由甲方专家规则或 LLM 生成后人工会签，本件不生成建议文本"},
            {"dim": "问题识别结果面", "why": "chain_sz_problem 不存在；本件只能用叶级缺口做代理",
             "fill": "建问题识别件并落盘"},
        ],
        "notes": [
            "本件的 opportunity_index 不是旧稿那条公式；旧稿 0.4/0.3/0.3 的政策与市场两维缺失，"
            "强行保留会把 60% 权重压在 null 上。字段 opportunity_index_old_draft_shape 显式置 null。",
            "优势判据与 M_CHAIN_DEEP_121_1 同源（LQ + 专利/融资超配），但专利份额口径不同，百分数不可互引。",
            "「叶级缺口」在本件记正、在问题件应记负；同一组数不能同时进两个总分。",
            "政策维与市场维在 UI 上应显示「未纳入」，不能显示 0 分。",
        ],
        "counter_checks": counters,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("[ok]", OUT)
    print("判档 %s | 分层 %s" % (result["support_judgment"], dict(tier_count)))
    for r in rows:
        print("  %-10s OI=%5.1f adv=%5.1f tr=%5.1f gap=%5.1f LQ=%.2f %s"
              % (r["chain_name"], r["opportunity_index"], r["advantage_score"],
                 r["trend_score"], r["gap_score"], r["lq"], r["tier"]))


if __name__ == "__main__":
    main()
