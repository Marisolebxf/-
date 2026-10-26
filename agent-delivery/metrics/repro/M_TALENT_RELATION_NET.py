#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_RELATION_NET —— 人才合作关系网络（SRS 72/73/74/75）。

数据：`dwd_scholar_coauthor`（is_deleted=0）落盘快照。
  degree 表：20,011 个 ego，[sid, 去重合作者数 d, 合著篇次合计 w, 单对最大篇次 mx, 首末时间]；
  深圳切片 1：scholar_id ∈ 深圳机构 → 9,066 条出边（116 个 ego）；
  深圳切片 2：co_scholar_org_name_zh LIKE '%深圳%' → 2,779 条入边（1,732 个深圳机构合作者）。
注意：`dwd_scholar_coauthor` 每 ego 的 co_scholar_id 去重后被截断在 100（实测 6,810 人 =100），
度分布右端是删失的，均值只能当「下界」。本件不产出介数/紧密中心度（需要全量边表）。
零 SQL；产物 code/M_TALENT_RELATION_NET_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_RELATION_NET"


def topk(cnt, k):
    return sorted(cnt.items(), key=lambda kv: (-kv[1], str(kv[0])))[:k]


def main() -> None:
    raw = C.load("coauthor160_20261022.json")
    deg = [(r[0], int(r[1] or 0), int(float(r[2] or 0)), int(r[3] or 0)) for r in raw["degree"]]
    dvals = [d for _, d, _, _ in deg]
    wvals = [w for _, _, w, _ in deg]
    n = len(deg)
    sum_d = sum(dvals)
    egos = {r[0]: r for r in deg}
    p = {r["sid"]: r for r in C.rows()}

    mean_d = sum_d / n
    mean_w = sum(wvals) / n
    cov = sum((d - mean_d) * (w - mean_w) for d, w in zip(dvals, wvals))
    var_d = sum((d - mean_d) ** 2 for d in dvals)
    var_w = sum((w - mean_w) ** 2 for w in wvals)
    pearson = round(cov / (var_d * var_w) ** 0.5, 4) if var_d and var_w else None

    top = sorted(deg, key=lambda x: -x[2])[:20]
    top_rows = [{"sid": s, "name": p.get(s, {}).get("name", "—"),
                 "org": p.get(s, {}).get("org", "—"),
                 "city": p.get(s, {}).get("city", "—"),
                 "degree": d, "weight": w, "max_pair": mx} for s, d, w, mx in top]

    e1 = raw["sz_ego_edges"]
    e2 = raw["sz_alter_edges"]
    sz_egos = {r[0] for r in e1}
    sz_alter_ids = {r[1] for r in e1}
    sz_org = Counter(r[3] for r in e1 if r[3].strip())
    ego_org = Counter(p[s]["org"] for s in sz_egos if s in p)
    in_edges_by_org = Counter(r[3] for r in e2 if r[3].strip())
    in_top_alters = Counter((r[2], r[3]) for r in e2 if r[2].strip())
    e1_deg = Counter(r[0] for r in e1)

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "合作表带 create_time（最早/最晚），但不是论文发表年，无法构建年度网络；"
                           "本件只做当前全量截面",
        "scope": {"universe": "dwd_scholar_coauthor 中有 ≥1 条合作记录的 ego", "egos": n,
                  "edge_definition": "ego—co_scholar_id 去重对（无向边按 2 次度计）",
                  "degree_cap": 100},
        "coverage": {"egos": n, "degree_sum": sum_d,
                     "undirected_edges_est": sum_d // 2,
                     "weight_sum": sum(wvals), "weight_mean": round(mean_w, 2),
                     "capped_at_100": sum(1 for d in dvals if d >= 100),
                     "capped_share": C.share(sum(1 for d in dvals if d >= 100), n),
                     "degree_ge50": sum(1 for d in dvals if d >= 50),
                     "ego_in_master": len(set(egos) & {r[0] for r in C.scholars_all()}),
                     "ego_in_master_share": C.share(len(set(egos) & {r[0] for r in C.scholars_all()}), n)},
        "degree_stats": {"mean": round(mean_d, 2), "median": C.pctl(dvals, 0.5),
                         "p10": C.pctl(dvals, 0.10), "p25": C.pctl(dvals, 0.25),
                         "p75": C.pctl(dvals, 0.75), "p90": C.pctl(dvals, 0.90),
                         "p99": C.pctl(dvals, 0.99), "max": max(dvals),
                         "gini": C.gini(dvals),
                         "density": round(2 * (sum_d / 2) / (n * (n - 1)), 8)},
        "weight_corr": {"pearson_degree_weight": pearson,
                        "note": "w = SUM(co_paper_count)，同一对合作者的合著篇次合计；"
                                "与度高度正相关说明「广撒网」与「深度合作」同向"},
        "top_egos": top_rows,
        "shenzhen_out": {"egos": len(sz_egos), "edges": len(e1),
                         "distinct_alters": len(sz_alter_ids),
                         "mean_edges_per_ego": round(len(e1) / len(sz_egos), 2),
                         "ego_in_panel": len([s for s in sz_egos if s in p]),
                         "ego_org_top": [{"org": k, "n": v} for k, v in topk(ego_org, 12)],
                         "alter_org_top": [{"org": k, "n": v} for k, v in topk(sz_org, 12)],
                         "top_ego_degree": [{"sid": s, "degree": d,
                                             "org": p.get(s, {}).get("org", "")}
                                            for s, d in topk(e1_deg, 10)]},
        "shenzhen_in": {"edges": len(e2), "distinct_sz_alters": len({r[1] for r in e2}),
                        "distinct_outside_egos": len({r[0] for r in e2}),
                        "sz_alter_org_top": [{"org": k, "n": v}
                                             for k, v in topk(in_edges_by_org, 12)],
                        "top_named_alters": [{"name": k[0], "org": k[1], "edges": v}
                                             for k, v in topk(in_top_alters, 10)],
                        "note": "这一侧是「库外/全库 ego → 深圳机构合作者」的入边，"
                                "与 shenzhen_out 不是同一张子图，不能相加当无向边"},
        "data_quality": {
            "cap": f"{sum(1 for d in dvals if d >= 100):,} 个 ego 的度正好 100（34.03%），"
                   "是 SQL 端截断不是真实值；均值 59.35 只能解释为下界",
            "no_edge_list": "快照只落盘了 degree 聚合表 + 两张深圳切片，没有 59 万条无向边；"
                            "因此连通分量、聚类系数、介数中心度、平均路径长度本件一律不产出",
            "name_only": "深圳入边里 1,732 个合作者只有 P 开头的外部 id + 姓名，无法回连到 "
                         "scholar_id，跨库同一人未合并",
            "universe": "合著表的 20,011 个 ego 属于属性宇宙（与主档 21,316 只交集 1,839，"
                        "9.19%），所以 top_egos 的姓名/机构 91% 为空——不是缺失，是两个宇宙不重叠；"
                        "深圳 116 个 ego 里只有 39 个能在主档取到机构",
            "time": "create_time 是记录写入时间（2026-07-24），不是论文年份，做不了网络演化",
            "weight_semantics": "co_paper_count 为同一对合作者的合著篇次，未做作者贡献度加权",
        },
        "diff_vs_old_draft": {
            "old": "旧稿写「1,187,606 条合作边」——这是度数和（有向计数），不是无向边数",
            "now": f"度数和 {sum_d:,}，无向边估计 {sum_d//2:,}；ego {n:,} 个；"
                   f"深圳出边 {len(e1):,} / 入边 {len(e2):,}",
            "why": "本件把「度数和」与「无向边」分开写，并在所有均值处标注 100 截断",
        },
        "findings": [
            f"{n:,} 个 ego、度数和 {sum_d:,}（无向边约 {sum_d//2:,}），中位度 "
            f"{C.pctl(dvals,0.5)}、均值 {round(mean_d,2)}、Gini {C.gini(dvals)}",
            f"34.03% 的 ego 度被截断在 100，右尾不可信；度与合著篇次 Pearson={pearson}",
            f"深圳出边 {len(e1):,} 条 / {len(sz_egos)} 个 ego（人均 "
            f"{round(len(e1)/len(sz_egos),2)} 条），深圳入边 {len(e2):,} 条指向 "
            f"{len({r[1] for r in e2})} 个深圳机构合作者",
        ],
    }
    C.write(METRIC, payload)
    print("stats", payload["degree_stats"], "pearson", pearson)
    print("coverage", payload["coverage"])
    print("sz out", payload["shenzhen_out"]["egos"], payload["shenzhen_out"]["edges"],
          payload["shenzhen_out"]["mean_edges_per_ego"], ego_org.most_common(5))
    print("sz in", payload["shenzhen_in"]["edges"], payload["shenzhen_in"]["distinct_sz_alters"],
          in_edges_by_org.most_common(5))
    print("top", [(x["name"], x["org"], x["degree"], x["weight"]) for x in top_rows[:5]])


if __name__ == "__main__":
    main()
