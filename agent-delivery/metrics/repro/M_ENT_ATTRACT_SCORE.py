#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_ATTRACT_SCORE · 招引推荐评分（gkx 单库代理版）

定义
----
招引推荐评分 = 「这家企业值不值得招引」的可比分数，用于招引名单排序与入围阈值。
旧稿口径是别名转发：attract_score = M_ENT_ATTRACTION_INDEX（三维指数），上游未出数；
`enterprise_score` 在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §enterprise_score）。

本件给代理分，四项：
  技术 0.40：min-max(log1p(专利数))
  广度 0.20：min-max(IPC4 distinct)
  资本 0.30：min-max(log1p(融资事件数 + 对外投资出度 + 被投边))
  属地适配 0.10：企业在深圳都市圈内=1，省内其他市=0.6，省外=0.3
候选集排除高校/院所/事业单位。风险维未接入（无逐企业记录），按 0 处理。

输出：code/M_ENT_ATTRACT_SCORE_out.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_ATTRACT_SCORE_out.json"
METRIC = "M_ENT_ATTRACT_SCORE"

W = {"tech": 0.40, "breadth": 0.20, "capital": 0.30, "geo": 0.10}
GBA = {"深圳市", "广州市", "东莞市", "惠州市"}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    base = load("base_20261021.json")
    city = {r[2]: r[4] for r in base}
    org_name = {r[0]: r[2] for r in base}

    ipc = defaultdict(set)
    pat = defaultdict(int)
    for ipc4, name, c in load("patent_ipc4_by_name_20261021.json"):
        ipc[name].add(ipc4)
        pat[name] += c

    cap = defaultdict(int)
    for src, dst in load("ent_edges_20261021.json")["invest"]:
        cap[org_name.get(src)] += 1
        cap[org_name.get(dst)] += 1
    fin_events = defaultdict(int)
    for r in load("chain21_fin_degree_20261022.json")["fin"]:
        fin_events[r[1]] += 1

    NON_ENT = {"事业单位", "机关", "党政机关", "社会团体", "民办非企业单位"}
    ent_type = {r[1]: r[7] for r in load("star_base_rows_gkx.json")}

    cand = {n for n in set(pat) | {k for k, v in cap.items() if v}}
    cand = {n for n in cand if n and n in city and ent_type.get(n) not in NON_ENT
            and not any(k in n for k in ("大学", "学院", "研究院", "研究所", "实验室"))}

    def norm(d):
        lo, hi = min(d.values()), max(d.values())
        span = (hi - lo) or 1.0
        return {k: (v - lo) / span for k, v in d.items()}

    tech = norm({n: math.log1p(pat.get(n, 0)) for n in cand})
    breadth = norm({n: len(ipc.get(n, ())) for n in cand})
    capital = norm({n: math.log1p(cap.get(n, 0) + fin_events.get(n, 0)) for n in cand})

    def geo(n):
        c = city.get(n)
        if c in GBA:
            return 1.0
        if c and str(c).startswith("广东"):
            return 0.6
        return 0.3

    rows = []
    for n in cand:
        g = geo(n)
        s = (W["tech"] * tech[n] + W["breadth"] * breadth[n]
             + W["capital"] * capital[n] + W["geo"] * g)
        rows.append({"name": n, "city": city.get(n), "score": round(s, 4),
                     "tech": round(tech[n], 4), "breadth": round(breadth[n], 4),
                     "capital": round(capital[n], 4), "geo_fit": g,
                     "patents": pat.get(n, 0), "ipc4": len(ipc.get(n, ())),
                     "capital_edges": cap.get(n, 0), "fin_events": fin_events.get(n, 0)})
    rows.sort(key=lambda r: (-r["score"], r["name"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    outside_sz = [{"rank": i, **{k: r[k] for k in ("name", "city", "score", "patents")}}
                  for i, r in enumerate([x for x in rows if x["city"] != "深圳市"][:30], 1)]

    out = {
        "metric_id": METRIC,
        "metric_name": "招引推荐评分",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "score = 0.40*minmax(log1p专利) + 0.20*minmax(IPC4广度) + 0.30*minmax(log1p(融资+投资边)) + 0.10*属地适配",
        "blocking_tables": {
            "enterprise_score": {"triage": "source_absent",
                                 "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_score"},
        },
        "upstream_note": "旧稿口径是别名转发 attract_score = M_ENT_ATTRACTION_INDEX；上游指数未出数，本件不转发、直接给代理分，代理分不可当作验收值",
        "proxy_path": "专利 + 广度 + 资本活跃 + 属地适配；候选集排除非企业主体",
        "proxy_deviation": "招引的三维指数（技术/成长/区域）无出数；本件用专利替代技术、用资本事件替代成长、用城市归属替代区域匹配；风险维未接入（按 0，不扣分），会把有风险记录的企业排得偏高；权重为项目默认值",
        "weights": W,
        "candidates": {"candidate_orgs": len(cand), "base_orgs": len(base)},
        "top100": rows[:100],
        "top30_outside_shenzhen": outside_sz,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "上游指数与 enterprise_score 都不存在，但招引排序要的信号在 gkx 有真实载体：专利、IPC 广度、融资事件、投资/股东边、企业城市归属，覆盖 13 万级企业。四项加权可出名单、分项分与「深圳以外候选」子表，故不判完全不支持；但三维修正为单指标代理、风险维未接入、权重未裁定，故判部分支持。",
            "criteria": {
                "result_tables": 1, "result_tables_present": 0,
                "dims_proxied": 4, "upstream_index_available": False,
                "candidate_orgs": len(cand), "proxy_used": True,
            },
        },
        "base_years_used": [2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": "专利窗口 2021—2024（2025/2026 残年不计）；融资事件不按年切，只数条数；属地适配取当前城市。截面评分，不做年度序列。",
        "sources": [
            {"path": "code/_snapshots21/base_20261021.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "城市归属"},
            {"path": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
             "table": "gkx.dwd_patent", "rows": 581585, "role": "技术与广度"},
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json",
             "table": "gkx.dwd_org_financing_info", "rows": 25654, "role": "融资事件"},
            {"path": "code/_snapshots21/ent_edges_20261021.json",
             "table": "gkx.dwd_org_invest_info + gkx.dwd_org_shareholder_info",
             "rows": 117001, "role": "资本活跃"},
            {"path": "code/_snapshots21/star_base_rows_gkx.json",
             "table": "gkx.dwd_org_base_info", "rows": 189116, "role": "登记类型（排除非企业）"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} cand={len(cand)}")
    for r in rows[:5]:
        print("  ", r["rank"], r["name"][:20], r["score"], r["city"], r["patents"])


if __name__ == "__main__":
    main()
