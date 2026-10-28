#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_CULTIVATE_SCORE · 培育推荐评分（gkx 单库代理版）

定义
----
培育推荐评分 = 本地「苗子」企业的可培育性打分，用于培育名单排序与入库阈值。
旧稿口径是别名转发：cultivate_score = M_ENT_CULTIVATION_INDEX（三维指数），
上游指数未出数；`enterprise_diagnosis` / `enterprise_score` 两张结果面在 gkx
都不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE 对应两节）。

本件用「可培育性」的四条可测代理，明确标注为代理分：
  成长 0.35：成立年限越短越高（≤5 年满分，≥15 年 0 分，线性）
  创新 0.30：min-max(log1p(专利数))
  广度 0.20：min-max(IPC4 distinct)
  资本 0.15：min-max(log1p(融资事件数 + 被投边数))
候选集限定为「成立 3—15 年、有专利或有资本边、非高校/院所/事业单位」的企业，
避免把巨头、空壳与高校排进培育名单（高校的成立年常是改制或重新登记年）。

输出：code/M_ENT_CULTIVATE_SCORE_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_CULTIVATE_SCORE_out.json"
METRIC = "M_ENT_CULTIVATE_SCORE"

W = {"growth": 0.35, "innov": 0.30, "breadth": 0.20, "capital": 0.15}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def growth_score(year):
    if not year:
        return 0.0
    age = 2025 - year
    if age <= 5:
        return 1.0
    if age >= 15:
        return 0.0
    return round((15 - age) / 10, 4)


def main() -> None:
    base = load("base_20261021.json")
    city = {r[2]: r[4] for r in base}
    est = {r[2]: r[5] for r in base}
    org_name = {r[0]: r[2] for r in base}

    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c

    cap = defaultdict(int)
    for src, dst in load("ent_edges_20261021.json")["invest"]:
        cap[org_name.get(dst)] += 1

    fin_events = defaultdict(int)
    for r in load("chain21_fin_degree_20261022.json")["fin"]:
        fin_events[r[1]] += 1

    # 排除非企业主体：高校/院所/事业单位的「成立年」多是改制或重新登记年，
    # 不排掉会让培育名单前十里塞满大学（实测：广东工业大学 2021、华南理工 2018）。
    NON_ENT = {"事业单位", "机关", "党政机关", "社会团体", "民办非企业单位"}
    ent_type = {r[1]: r[7] for r in load("star_base_rows_gkx.json")}

    cand = {n for n in set(pat) | {k for k, v in cap.items() if v}}
    cand = {n for n in cand if n and n in city and est.get(n)
            and 3 <= 2025 - est[n] <= 15
            and ent_type.get(n) not in NON_ENT
            and not any(k in n for k in ("大学", "学院", "研究院", "研究所", "实验室"))}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    innov = norm({n: math.log1p(pat.get(n, 0)) for n in cand})
    breadth = norm({n: len(ipc.get(n, ())) for n in cand})
    capital = norm({n: math.log1p(cap.get(n, 0) + fin_events.get(n, 0)) for n in cand})

    rows = []
    for n in cand:
        g = growth_score(est[n])
        s = (W["growth"] * g + W["innov"] * innov[n]
             + W["breadth"] * breadth[n] + W["capital"] * capital[n])
        rows.append({"name": n, "city": city.get(n), "score": round(s, 4),
                     "growth": g, "innov": round(innov[n], 4),
                     "breadth": round(breadth[n], 4), "capital": round(capital[n], 4),
                     "est_year": int(est[n]), "patents": pat.get(n, 0),
                     "ipc4": len(ipc.get(n, ())),
                     "capital_edges": cap.get(n, 0), "fin_events": fin_events.get(n, 0)})
    rows.sort(key=lambda r: (-r["score"], r["name"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    out = {
        "metric_id": METRIC,
        "metric_name": "培育推荐评分",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "score = 0.35*成立年限分 + 0.30*minmax(log1p专利) + 0.20*minmax(IPC4广度) + 0.15*minmax(log1p(融资+被投))",
        "blocking_tables": {
            "enterprise_diagnosis": {"triage": "source_absent",
                                     "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_diagnosis"},
            "enterprise_score": {"triage": "source_absent",
                                 "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_score"},
        },
        "upstream_note": "旧稿口径是别名转发 cultivate_score = M_ENT_CULTIVATION_INDEX；该上游指数未出数，本件不转发、直接给代理分，代理分不可当作验收值",
        "proxy_path": "成立年限 + 专利 + IPC 广度 + 融资/被投 → 加权；候选集限 3—15 年企业",
        "proxy_deviation": "上游三维指数（潜力/成长/恢复）没有出数；本件用成立年限替代「成长」、用专利替代「潜力」、用融资替代「恢复」，三项都是代理；权重为项目默认值；候选集排除了 15 年以上企业，等于只给「苗子」打分，不覆盖全库",
        "weights": W,
        "candidates": {"candidate_orgs": len(cand), "base_orgs": len(base),
                       "age_window": [3, 15]},
        "top100": rows[:100],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "上游指数未出数、两张结果面都不存在，但培育场景要的四类信号在 gkx 有真实载体：成立年份（全量）、专利与 IPC 广度（13 万级）、融资事件（2.5 万条）与投资边（4.7 万条）。四项加权可出可解释的培育名单与分项分，故不判完全不支持；但旧稿三维（潜力/成长/恢复）是三个复合指数，本件用单指标替代，代理偏差明确，且权重未裁定，故判部分支持。",
            "criteria": {
                "result_tables": 2, "result_tables_present": 0,
                "dims_proxied": 4, "upstream_index_available": False,
                "candidate_orgs": len(cand), "proxy_used": True,
            },
        },
        "base_years_used": [2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "成立年限以 2025 为基准年；专利窗口 2021—2024（2025/2026 残年不计）；融资事件年份跨 2000—2026，本件只数条数不按年切。截面评分，不做年度序列。",
        "sources": [
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "成立年/城市"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "专利与广度"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json",
             "table": "gkx.dwd_org_financing_info", "rows": 25654, "role": "融资事件"},
            {"path": "code/_snapshots21/ent_edges_20261021.json",
             "table": "gkx.dwd_org_invest_info", "rows": 46967, "role": "被投边"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} cand={len(cand)}")
    for r in rows[:5]:
        print("  ", r["rank"], r["name"][:20], r["score"], r["est_year"], r["patents"])


if __name__ == "__main__":
    main()
