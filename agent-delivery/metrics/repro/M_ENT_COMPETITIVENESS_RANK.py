#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_COMPETITIVENESS_RANK · 企业竞争力排名（gkx 单库代理版）

定义
----
竞争力排名 = 按企业竞争力综合分降序取前 N，并给出分项分与名次。
旧稿的综合分来自 `enterprise_score` 五维（创新/经营/成长/规模/风险），
该结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §enterprise_score、
§enterprise_ranking）。本件用四维可测代理：
  创新 0.35：min-max(log1p(专利数))
  技术广度 0.20：min-max(IPC4 distinct)
  资本活跃 0.25：min-max(log1p(投资出度 + 被投 + 股东边))
  经营年限 0.10：min-max(2025 - 成立年)
  风险扣分 0.10：风险记录数 min-max 后取负号（有记录即扣分）
权重为项目默认值，甲方未裁定；风险记录只用聚合量级，不做逐企业惩罚分。

输出：code/M_ENT_COMPETITIVENESS_RANK_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_COMPETITIVENESS_RANK_out.json"
METRIC = "M_ENT_COMPETITIVENESS_RANK"

W = {"innov": 0.35, "breadth": 0.20, "capital": 0.25, "age": 0.10, "risk": 0.10}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    base = load("base_20261021.json")  # org_id, credit, name, province, city, est_year
    org_name = {r[0]: r[2] for r in base}
    city = {r[2]: r[4] for r in base}
    est = {r[2]: r[5] for r in base}

    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c

    edges = load("ent_edges_20261021.json")
    cap = defaultdict(int)
    for src, dst in edges["invest"]:
        cap[org_name.get(src)] += 1
        cap[org_name.get(dst)] += 1
    for src, dst in edges["shareholder"]:
        cap[org_name.get(src)] += 1
        cap[org_name.get(dst)] += 1

    # 候选集：有专利 或 有资本边，且底册能给出城市/成立年
    cand = {n for n in set(pat) | {k for k, v in cap.items() if v}}
    cand = {n for n in cand if n and n in city}

    def norm(d):
        if not d:
            return {}
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    innov = norm({n: math.log1p(pat.get(n, 0)) for n in cand})
    breadth = norm({n: len(ipc.get(n, ())) for n in cand})
    capital = norm({n: math.log1p(cap.get(n, 0)) for n in cand})
    age = norm({n: (2025 - est[n]) if est.get(n) else 0 for n in cand})

    rows = []
    for n in cand:
        s = (W["innov"] * innov[n] + W["breadth"] * breadth[n]
             + W["capital"] * capital[n] + W["age"] * age[n])
        rows.append({"name": n, "city": city.get(n), "score": round(s, 4),
                     "innov": round(innov[n], 4), "breadth": round(breadth[n], 4),
                     "capital": round(capital[n], 4), "age": round(age[n], 4),
                     "patents": pat.get(n, 0), "ipc4": len(ipc.get(n, ())),
                     "capital_edges": cap.get(n, 0)})
    rows.sort(key=lambda r: (-r["score"], r["name"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    by_city = defaultdict(int)
    for r in rows[:100]:
        by_city[r["city"]] += 1

    out = {
        "metric_id": METRIC,
        "metric_name": "企业竞争力排名",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "score = 0.35*创新 + 0.20*技术广度 + 0.25*资本活跃 + 0.10*经营年限 − 0.10*风险（风险维本期未逐企业接入，见 proxy_deviation）",
        "blocking_tables": {
            "enterprise_score": {"triage": "source_absent",
                                 "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_score"},
            "enterprise_ranking": {"triage": "source_absent",
                                   "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_ranking"},
        },
        "proxy_path": "专利规模 + IPC 广度 + 资本/股东关系边 + 成立年限，四维加权排名",
        "proxy_deviation": "五维里的「经营」维（营收/利润）只有 0.73% 企业有值，不能进排名；「风险」维只有全库聚合量级、没有逐企业扣分，本件按 0 处理，等于不扣分——会把有风险记录的企业排得偏高。权重为项目默认值",
        "weights": W,
        "candidates": {"candidate_orgs": len(cand), "base_orgs": len(base),
                       "candidate_rule": "有专利或有资本关系边，且底册有城市"},
        "top100_city_mix": dict(sorted(by_city.items(), key=lambda x: -x[1])),
        "top100": rows[:100],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "enterprise_score 与 enterprise_ranking 两张结果面都不存在，但排名所需的大头可从原始表算：专利、IPC 广度、投资与股东关系、成立年限覆盖 13 万级企业，四维加权即可出完整名次与分项。缺的是经营维（营收覆盖 0.73%）与风险维（无逐企业记录），两维占旧稿权重的一部分，本件只能按 0 处理。可排名但不完整，判部分支持。",
            "criteria": {
                "result_tables": 2, "result_tables_present": 0,
                "dims_used": 4, "dims_missing": 2,
                "candidate_orgs": len(cand), "proxy_used": True,
            },
        },
        "base_years_used": [2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利侧窗口 2021—2024（2025/2026 残年不计），经营年限按 2025 减成立年；营收维因覆盖 0.73% 不进入排名，故不列营收年份。本件是截面排名，不做年度序列。",
        "sources": [
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116,
             "role": "企业主档（城市/成立年）"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "创新与广度"},
            {"path": "code/_snapshots21/ent_edges_20261021.json",
             "table": "gkx.dwd_org_invest_info + gkx.dwd_org_shareholder_info",
             "rows": 117001, "role": "资本活跃度"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} cand={len(cand)}")
    for r in rows[:5]:
        print("  ", r["rank"], r["name"][:20], r["score"], r["patents"], r["capital_edges"])


if __name__ == "__main__":
    main()
