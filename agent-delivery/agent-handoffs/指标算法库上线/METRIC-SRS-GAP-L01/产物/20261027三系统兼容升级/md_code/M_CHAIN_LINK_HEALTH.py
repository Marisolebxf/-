#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_LINK_HEALTH 环节健康度（gkx 三方库，20261023 重建版）。

口径（calc-logic/CHAIN/M_CHAIN_LINK_HEALTH.md）：
  五维等权：技术成熟度 / 人才供给 / 市场容量 / 融资资本 / 政策覆盖，
  min-max 归一到 0—100 后求均值。对象 = 环节节点（本件取 L1，9 位码，41 个）。

本件**不拍总分**，只给「有源的子维」与「无源的子维」：
  技术成熟度  —— 可算：L1 节点下专利申请人（name→L1）的申请量 / L1 挂接企业数
  融资资本    —— 可算：L1 节点下融资事件数 / L1 挂接企业数
  人才供给    —— 不可算：`development_employee` 在年报财务表 90,926 行里 0 行有值
  市场容量    —— 不可算：链内营收快照仅 650 家，L1 层每格覆盖 < 1%
  政策覆盖    —— 不可算：政策表无环节码列，标题不含 L1 码，无法做节点归属
无源子维一律 null，不填 0（填 0 = 断言「该维健康度为 0」，是错误结论）。

归一方法：百分位秩（0—100），不是 min-max。原因是 41 个 L1 里企业数从 46 到
537,129，min-max 会把 1 家企业的极端密度拉成 100 分；百分位秩只表达相对位置。

产物：code/M_CHAIN_LINK_HEALTH_out.json
"""
from __future__ import annotations

from collections import Counter

import _chain5_common as C

METRIC = "M_CHAIN_LINK_HEALTH"


def pct_rank(values: dict, reverse: bool = False) -> dict:
    """百分位秩：最小 0、最大 100（并列取平均秩）。reverse=True 表示值越大分越低。"""
    items = sorted(values.items(), key=lambda kv: kv[1], reverse=reverse)
    n = len(items)
    out = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        avg_rank = (i + j) / 2.0
        score = 0.0 if n == 1 else round(avg_rank / (n - 1) * 100, 2)
        for k in range(i, j + 1):
            out[items[k][0]] = score
        i = j + 1
    return out


def main():
    idx = C.load("chain_firm_index_20261023.json")
    agg = C.load("star_applicant_agg_gkx.json")["agg"]
    rev_rows = C.load("chain21_revenue_20261022.json")["stock"]
    ev, st = C.financing(idx)

    pat = Counter()
    names_hit = 0
    for nm, l1 in idx["name_l1"].items():
        v = agg.get(nm)
        if not v:
            continue
        pat[l1] += v[0]
        names_hit += 1

    latest = {}
    for r in rev_rows:
        org = r[0]
        if org not in latest or str(r[3]) > str(latest[org][3]):
            latest[org] = r
    rev_n, rev_sum = Counter(), Counter()
    for org, r in latest.items():
        l1 = idx["rev_credit_l1"].get(r[2])
        if l1 and r[4] is not None:
            ls = l1 if isinstance(l1, list) else [l1]
            for k in ls:
                rev_n[k] += 1
                rev_sum[k] += float(r[4])

    fin = Counter()
    for e in ev:
        l1 = idx["fin_credit_l1"].get(e["credit"]) if e["credit"] else None
        if l1:
            ls = l1 if isinstance(l1, list) else [l1]
            for k in ls:
                fin[k] += 1

    rows = []
    for code, firms in idx["l1_firms"].items():
        p = pat.get(code, 0)
        f = fin.get(code, 0)
        rn = rev_n.get(code, 0)
        rows.append({
            "node": code,
            "node_name": idx["l1_name"].get(code),
            "chain": idx["l1_chain"].get(code),
            "chain_name": idx["chain_name"].get(idx["l1_chain"].get(code)),
            "firms_attached": firms,
            "patent_applies": p,
            "patent_per_firm": round(p / firms, 4) if firms else None,
            "fin_events": f,
            "fin_per_1000_firms": round(f / firms * 1000, 3) if firms else None,
            "rev_firms": rn,
            "rev_coverage_pct": round(100.0 * rn / firms, 4) if firms else None,
            "rev_latest_sum_yuan": round(rev_sum.get(code, 0.0), 2),
        })

    tech = pct_rank({r["node"]: r["patent_per_firm"] for r in rows if r["patent_per_firm"] is not None})
    cap = pct_rank({r["node"]: r["fin_per_1000_firms"] for r in rows if r["fin_per_1000_firms"] is not None})
    for r in rows:
        r["tech_score"] = tech.get(r["node"])
        r["capital_score"] = cap.get(r["node"])
        r["talent_score"] = None
        r["market_score"] = None
        r["policy_score"] = None
        r["health_score"] = None
        r["partial_2dim_index"] = round((r["tech_score"] + r["capital_score"]) / 2, 2)
        r["partial_note"] = "仅技术+资本两维（等权可用维平均），权重覆盖 2/5=0.40，不是健康度"
    rows.sort(key=lambda r: -r["partial_2dim_index"])

    top = rows[:10]
    bottom = rows[-10:]
    weak = sorted(rows, key=lambda r: r["partial_2dim_index"])[:10]

    def _rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0] * len(v)
        for pos, i in enumerate(order):
            out[i] = pos
        return out

    rx = _rank([r["tech_score"] for r in rows])
    ry = _rank([r["capital_score"] for r in rows])
    n = len(rows)
    rho = round(1 - 6 * sum((rx[i] - ry[i]) ** 2 for i in range(n)) / (n * (n * n - 1)), 4)

    report = {
        "metric_name": "环节健康度",
        "unit": "0—100（子维百分位秩）；总分 health_score = null",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_LINK_HEALTH.md",
        "data_source": {
            "engine": "只读快照（源：三方库 gkx @ 183.240.141.251:3318）",
            "tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_patent（经申请人聚合缓存）",
                       "gkx.dwd_org_financing_info", "gkx.dwd_org_annual_financial_info",
                       "gkx.dwd_policy_base"],
            "snapshots": ["code/_snapshots21/chain_firm_index_20261023.json",
                          "code/_snapshots21/star_applicant_agg_gkx.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/chain21_revenue_20261022.json"],
        },
        "probes": {
            "l1_nodes": len(rows),
            "l1_firm_attachments": sum(r["firms_attached"] for r in rows),
            "chain_firms_unique": sum(idx["chain_firms"].values()),
            "patent_names_mapped": names_hit,
            "patent_names_total": len(agg),
            "patent_applies_mapped": sum(pat.values()),
            "patent_table_rows": 2939895,
            "patent_coverage_pct": round(100.0 * sum(pat.values()) / 2939895, 2),
            "fin_events_l1_sum": sum(fin.values()),
            "fin_events_chain_unique": len(ev),
            "fin_multi_l1_note": "同一企业挂多个 L1 时事件按 L1 各计 1 次，故 L1 求和 > 事件数",
            "rev_firms_l1_sum": sum(rev_n.values()),
            "rev_firms_chain_unique": len(latest),
            "talent_nonnull_rows": 0,
            "talent_total_rows": 90926,
            "policy_policy_rows": 20000,
            "policy_node_code_columns": 0,
            "policy_title_hits_at_l1": None,
            "min_firms": min(r["firms_attached"] for r in rows),
            "max_firms": max(r["firms_attached"] for r in rows),
            "nodes_with_rev_coverage_ge_5pct": sum(1 for r in rows if (r["rev_coverage_pct"] or 0) >= 5),
            "max_rev_coverage_pct": max((r["rev_coverage_pct"] or 0) for r in rows),
            "rank_correlation_tech_capital": rho,
        },
        "l1_rows": rows,
        "top10": [{"node": r["node"], "name": r["node_name"], "chain_name": r["chain_name"],
                   "index": r["partial_2dim_index"]} for r in top],
        "bottom10": [{"node": r["node"], "name": r["node_name"], "chain_name": r["chain_name"],
                      "index": r["partial_2dim_index"]} for r in weak],
        "notes": [
            "企业数是「叶—企挂接」去重到 L1 的挂接数，41 个 L1 求和 1,749,995 > 链企业 1,714,458，差额来自同一企业挂多个 L1。",
            "专利数是「申请人名→L1」可匹配子集：949,894 件，占专利表 2,939,895 行的 32.32%；未匹配的 67.68% 不进分子。",
            "技术/资本得分是 41 个节点的相对百分位，不是绝对水平；跨批不可比。",
            "人才、市场、政策三维 null，不参与任何合计；partial_2dim_index 只是「两维可用均值」，不得当健康度发布。",
        ],
    }
    report.update(C.base_decl(
        [2021, 2022, 2023, 2024], [2025, 2026],
        "专利面板完整覆盖 2021—2024（2025 年 440,401 件、2026 年 74,810 件为残年，不进分母）；"
        "本件用全量专利存量（2021—2026 年申请合计）算密度，不做年度增速，故基期用于说明"
        "「专利面板从 2021 年才有数据、2017—2020 年零行」，不把缺失年按 0 摊入。"))
    report["support_judgment"] = "部分支持"
    report["support_reason"] = (
        "五维里只有技术成熟度与融资资本两维能在 L1 节点层闭合（合计权重 2/5=0.40）；"
        "人才列整列为空、营收覆盖 <1%、政策无环节码，三维永久不可得，故不能输出 0—100 总分。")

    C.write_out(METRIC, report)
    print("L1", len(rows), "pat", sum(pat.values()), "fin", sum(fin.values()), "rev", sum(rev_n.values()))
    for r in top[:8]:
        print(r["node"], r["node_name"], r["chain_name"], r["partial_2dim_index"], r["firms_attached"])


if __name__ == "__main__":
    main()
