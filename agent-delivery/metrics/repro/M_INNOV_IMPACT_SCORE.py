#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""创新影响分数（M_INNOV_IMPACT_SCORE）——B-sample 降档实现。

正本口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/INNOV/M_INNOV_IMPACT_SCORE.md`）：
    二维加权：产出规模（机构=专利数+论文数；领域=专利数）／网络影响（机构=合作邻居数；
    领域=专利被引合计），取值 0—100，对实体节点排名。

本件实测结果：
    - 机构侧两维**都能算**：论文数/专利数（产出规模）、共著图邻居数（网络影响）；
    - 领域侧只有产出规模能算；领域被引合计**接不上 IPC**（被引表 20,000 件里仅 467 件
      能在 `dwd_patent` 回连，2.335%，且回连后不带 IPC），故领域网络维置 null、不重归一化；
    - 阻塞表 `graph_node` / `impact_prediction` 在 gkx 查无（详见 absence_probe）。

零 SQL：全量读 `_snapshots21/impact_w15n1_20261023.json`（由 `_probe_impact_w15n1.py` 落盘）。

运行：cd code && python3 M_INNOV_IMPACT_SCORE.py
输出：code/M_INNOV_IMPACT_SCORE_out.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_IMPACT_SCORE_out.json")
TZ = timezone(timedelta(hours=8))

LEAVES = [
    ("I1_patent_scale", "patents", "产出规模｜专利件数"),
    ("I2_paper_scale", "papers", "产出规模｜中文论文篇数"),
    ("I3_coauthor_degree", "degree", "网络影响｜共著图邻居数"),
    ("I4_grant_rate", "grant_rate", "产出质量｜专利授权率"),
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.0 for _ in vals]
    return [(v - lo) / (hi - lo) * 100 for v in vals]


def entropy_weights(cols):
    """客观熵权（只作对照，不进主分）。cols: 各叶已归一化到 0—100 的列。"""
    n = len(cols[0])
    ws, detail = [], {}
    for j, c in enumerate(cols):
        s = sum(c) or 1.0
        p = [(v / s) if v > 0 else 0.0 for v in c]
        k = 1.0 / math.log(n)
        e = -k * sum(x * math.log(x) for x in p if x > 0)
        d = 1 - e
        ws.append(d)
        detail[j] = {"entropy": round(e, 6), "divergence": round(d, 6)}
    tot = sum(ws) or 1.0
    return [w / tot for w in ws], detail


def spearman(a, b):
    n = len(a)
    ra = {v: i for i, v in enumerate(sorted(a))}
    rb = {v: i for i, v in enumerate(sorted(b))}
    d2 = sum((ra[x] - rb[y]) ** 2 for x, y in zip(a, b))
    return 1 - 6 * d2 / (n * (n * n - 1))


def main() -> int:
    snap = load("impact_w15n1_20261023.json")
    rows = snap["steps"]["inst_join"]["rows_all"]
    # rows_all = 4,039 家（共著图节点 ∩ 第一申请人），是全量打分盘。
    for r in rows:
        r["grant_rate"] = round(r["grants"] / r["patents"] * 100, 4) if r["patents"] else None

    usable = [r for r in rows if r["grant_rate"] is not None]
    cols, leaf_meta = [], {}
    for key, field, label in LEAVES:
        if field == "grant_rate":
            vals = [r["grant_rate"] for r in usable]
        else:
            vals = [r[field] for r in usable]
        z = minmax(vals)
        for r, v in zip(usable, z):
            r["_" + key] = round(v, 4)
        cols.append(z)
        leaf_meta[key] = {
            "label": label,
            "raw_min": min(vals), "raw_max": max(vals),
            "raw_median": sorted(vals)[len(vals) // 2],
            "norm_note": "min-max 到 0—100；归一盘=共著图节点∩第一申请人的 %d 家" % len(usable),
        }

    eq = [0.25] * 4
    ent, ent_detail = entropy_weights(cols)
    for r in usable:
        r["score_equal"] = round(sum(r["_" + k] * w for (k, _, _), w in zip(LEAVES, eq)), 4)
        r["score_entropy"] = round(sum(r["_" + k] * w for (k, _, _), w in zip(LEAVES, ent)), 4)
        r["score_scale_only"] = round((r["_I1_patent_scale"] + r["_I2_paper_scale"]) / 2, 4)
        r["score_network_only"] = round(r["_I3_coauthor_degree"], 4)

    def rank_by(key):
        order = sorted(usable, key=lambda r: -r[key])
        return {r["inst"]: i + 1 for i, r in enumerate(order)}

    rk_eq, rk_ent = rank_by("score_equal"), rank_by("score_entropy")
    rk_sc, rk_nw = rank_by("score_scale_only"), rank_by("score_network_only")
    rk_pt = rank_by("_I1_patent_scale")
    for r in usable:
        r["rank_equal"] = rk_eq[r["inst"]]
        r["rank_entropy"] = rk_ent[r["inst"]]
        r["rank_scale_only"] = rk_sc[r["inst"]]
        r["rank_network_only"] = rk_nw[r["inst"]]
        r["rank_patent_only"] = rk_pt[r["inst"]]

    top = sorted(usable, key=lambda r: -r["score_equal"])[:25]

    # ---- 权重敏感性：网络维权重 w 从 0 扫到 1，另三维均分 (1-w)/3 ----
    def score_with_w(r, w):
        return (r["_I3_coauthor_degree"] * w
                + (r["_I1_patent_scale"] + r["_I2_paper_scale"] + r["_I4_grant_rate"]) / 3 * (1 - w))

    sweeps, leader_changes = [], []
    prev = None
    for i in range(0, 101):
        w = i / 100
        order = sorted(usable, key=lambda r: -score_with_w(r, w))
        lead = order[0]["inst"]
        if lead != prev:
            leader_changes.append({"w_network": round(w, 2), "leader": lead,
                                   "runner_up": order[1]["inst"],
                                   "gap": round(score_with_w(order[0], w) - score_with_w(order[1], w), 4)})
            prev = lead
        if i % 10 == 0:
            sweeps.append({"w_network": round(w, 2), "leader": lead,
                           "leader_score": round(score_with_w(order[0], w), 4),
                           "top3": [o["inst"] for o in order[:3]]})

    # ---- 排名轨道：同一批主体在不同权重下的位次（比「榜首是否换人」更有信息）----
    track_names = [r["inst"] for r in sorted(usable, key=lambda x: -x["score_equal"])[:8]]
    track_names += ["华为技术有限公司", "比亚迪股份有限公司"]
    track_names = list(dict.fromkeys(track_names))
    rank_track = {}
    for w in (0.0, 0.25, 0.5, 0.75, 1.0):
        order = sorted(usable, key=lambda r: -score_with_w(r, w))
        pos = {r["inst"]: i + 1 for i, r in enumerate(order)}
        rank_track[f"w={w:.2f}"] = {nm: pos.get(nm) for nm in track_names}

    # ---- 领域侧（IPC 小类）----
    ipc = snap["steps"]["patent"]["ipc_top"] if isinstance(snap["steps"]["patent"]["ipc_top"][0], list) else None
    ipc_all = load("patent_panel_innov_20261021.json")["ipc_all"]
    ipc_rows = sorted(ipc_all.items(), key=lambda kv: -kv[1])
    ipc_max = ipc_rows[0][1]
    ipc_top = [{
        "ipc4": k, "patents": v,
        "scale_score": round(math.log1p(v) / math.log1p(ipc_max) * 100, 4),
        "network_score": None,
        "network_note": "领域被引合计不可算：被引表与专利主表仅 2.335% 可回连，且回连不带 IPC",
    } for k, v in ipc_rows[:20]]

    # ---- 派生比值 ----
    n = len(usable)
    pat_sum = sum(r["patents"] for r in usable)
    pap_sum = sum(r["papers"] for r in usable)
    print(f"universe n={n} patents={pat_sum:,} papers={pap_sum:,}")
    derived = {
        "top1_patent_share_pct": {
            "value": round(usable[0]["patents"] / pat_sum * 100, 4) if False else None,
            "numerator": None, "denominator": pat_sum,
            "denominator_note": "榜内专利合计（分子见 top1_patent_count）",
        },
    }
    # 上面那格用真实计算覆盖（避免手写）
    top1 = max(usable, key=lambda r: r["patents"])
    derived["top1_patent_share_pct"] = {
        "value": round(top1["patents"] / pat_sum * 100, 4),
        "numerator": top1["patents"], "denominator": pat_sum,
        "denominator_note": f"{top1['inst']} 专利件数 / 榜内 {n} 家专利合计 {pat_sum:,} 件",
    }
    derived["top10_patent_share_pct"] = {
        "value": round(sum(sorted((r["patents"] for r in usable), reverse=True)[:10]) / pat_sum * 100, 4),
        "numerator": sum(sorted((r["patents"] for r in usable), reverse=True)[:10]),
        "denominator": pat_sum,
        "denominator_note": f"榜内专利前 10 家合计 / 榜内 {n} 家专利合计 {pat_sum:,} 件",
    }
    hw = next(r for r in usable if r["inst"] == "华为技术有限公司")
    hwn = next(r for r in usable if r["inst"] == "华南理工大学")
    derived["huawei_grant_rate_pct"] = {
        "value": hw["grant_rate"], "numerator": hw["grants"], "denominator": hw["patents"],
        "denominator_note": f"华为授权 {hw['grants']:,} 件 / 申请 {hw['patents']:,} 件；"
                            f"分子分母同主体同口径，不做行业调整",
    }
    derived["scut_grant_rate_pct"] = {
        "value": hwn["grant_rate"], "numerator": hwn["grants"], "denominator": hwn["patents"],
        "denominator_note": f"华南理工授权 {hwn['grants']:,} 件 / 申请 {hwn['patents']:,} 件",
    }
    derived["huawei_over_scut_patents"] = {
        "value": round(hw["patents"] / hwn["patents"], 4),
        "numerator": hw["patents"], "denominator": hwn["patents"],
        "denominator_note": f"华为 {hw['patents']:,} 件 / 华南理工 {hwn['patents']:,} 件（同为第一申请人等值计件）",
    }
    derived["scut_over_huawei_degree"] = {
        "value": round(hwn["degree"] / hw["degree"], 4),
        "numerator": hwn["degree"], "denominator": hw["degree"],
        "denominator_note": f"华南理工共著邻居 {hwn['degree']} / 华为 {hw['degree']}（同一张共著图）",
    }
    derived["paper_per_patent_scut"] = {
        "value": round(hwn["papers"] / hwn["patents"], 6),
        "numerator": hwn["papers"], "denominator": hwn["patents"],
        "denominator_note": f"华南理工论文 {hwn['papers']} 篇 / 专利 {hwn['patents']:,} 件；"
                            f"论文只计中文语料，英文论文不在库",
    }
    derived["city_cited_coverage_pct"] = {
        "value": snap["steps"]["domain_cited"]["match_rate_pct"],
        "numerator": snap["steps"]["domain_cited"]["matched_in_patent_n"],
        "denominator": snap["steps"]["domain_cited"]["cited_patents"],
        "denominator_note": "被引表 20,000 件里能在 dwd_patent 回连 467 件；这是领域网络维置 null 的依据",
    }
    derived["graph_patent_intersection_pct"] = {
        "value": snap["steps"]["inst_join"]["intersection_pct_of_graph"],
        "numerator": snap["steps"]["inst_join"]["intersection"],
        "denominator": snap["steps"]["inst_join"]["graph_nodes"],
        "denominator_note": "共著图 20,436 个机构串中，同时是第一申请人的 4,039 个；"
                            "机构串不归并院系，同校不同院系算不同节点",
    }

    out = {
        "metric_id": "M_INNOV_IMPACT_SCORE",
        "metric_name": "创新影响分数",
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "support_judgment": "部分支持",
        "verdict_reason": (
            "机构侧二维（产出规模/网络影响）全部可算，能给出可复算的 0—100 分与排名；"
            "领域侧只有产出规模可算，网络影响（专利被引合计）因被引表与专利主表仅 2.335% 可回连、"
            "且回连不带 IPC 字段而置 null，不重归一化。阻塞表 graph_node / impact_prediction 在 gkx 查无。"
        ),
        "source": {
            "library": "gkx",
            "host": "183.240.141.251:3318",
            "user": "gkx_reader_zp",
            "mode": "read-only",
            "touched": False,
            "note": "本件零 SQL：读 _probe_impact_w15n1.py 落盘的快照（该探针只读本地快照，亦零 SQL）",
        },
        "sources": [
            "code/_snapshots21/impact_w15n1_20261023.json",
            "code/_snapshots21/a25_paper_panel.json",
            "code/_snapshots21/star_applicant_agg_gkx.json",
            "code/_snapshots21/patent_panel_innov_20261021.json",
            "code/_snapshots21/ent_ds07_cited_20261023.json",
            "code/_snapshots21/w15n1_table_probe_20261023.json",
        ],
        "base_years_used": [2021, 2022, 2023],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "专利 apdt_year 在 2017—2020 零行（DATA_FACTS §3.13），故 missing 记这四年；"
            "2024 论文是回填孤峰（32,379 篇 = 32.09%，§3.74），不按 0 摊入、也不计入 used；"
            "2025—2026 专利只有 440,401 / 74,810 件，明显是尚未公开完全的残年，同样不进窗口。"
            "本件为截面计件，窗口只用于解释「件数覆盖哪个年代」，不参与归一。"
        ),
        "scope": "机构（第一申请人 ∩ 共著图节点）；领域（IPC 小类）",
        "scope_note": (
            "机构盘 = 共著图节点（全语料≥2 篇）∩ 专利第一申请人，共 4,039 家；"
            "四个叶子的 min-max 分母都是这 4,039 家，跨盘比较会失真。"
            "图节点按原始机构串计，同校不同院系是不同节点（如「清华大学」与"
            "「清华大学深圳国际研究生院」分列），未做归并。"
        ),
        "evaluation_set": [r["inst"] for r in top],
        "universe": {
            "graph_nodes": snap["steps"]["inst_join"]["graph_nodes"],
            "patent_applicants": snap["steps"]["inst_join"]["patent_applicants"],
            "intersection": snap["steps"]["inst_join"]["intersection"],
            "join_rule": snap["steps"]["inst_join"]["join_rule"],
            "scored_n": n,
        },
        "weights": {
            "main": {k: 0.25 for k, _, _ in LEAVES},
            "main_is_official": False,
            "weights_are_authored": True,
            "rationale": "正本只说「加权平均」，未给权重；本件四叶等权，并把熵权作客观对照",
            "entropy": {k: round(w, 4) for (k, _, _), w in zip(LEAVES, ent)},
            "entropy_detail": {k: ent_detail[i] for i, (k, _, _) in enumerate(LEAVES)},
            "equal": {k: 0.25 for k, _, _ in LEAVES},
        },
        "leaves": leaf_meta,
        "top_institutions": [{
            "rank": r["rank_equal"], "inst": r["inst"],
            "score": r["score_equal"], "score_entropy": r["score_entropy"],
            "patents": r["patents"], "grants": r["grants"], "grant_rate_pct": r["grant_rate"],
            "papers": r["papers"], "coauthor_degree": r["degree"],
            "leaf": {k: r["_" + k] for k, _, _ in LEAVES},
            "rank_patent_only": r["rank_patent_only"],
            "rank_network_only": r["rank_network_only"],
            "rank_scale_only": r["rank_scale_only"],
        } for r in top],
        "rank_consistency": {
            "spearman_equal_vs_entropy": round(spearman([r["score_equal"] for r in usable],
                                                        [r["score_entropy"] for r in usable]), 4),
            "spearman_equal_vs_patent_only": round(spearman([r["score_equal"] for r in usable],
                                                            [r["_I1_patent_scale"] for r in usable]), 4),
            "spearman_equal_vs_network_only": round(spearman([r["score_equal"] for r in usable],
                                                             [r["_I3_coauthor_degree"] for r in usable]), 4),
            "n": n,
            "note": "榜内 Spearman；越接近 1 说明综合分几乎被该单维决定",
        },
        "weight_sensitivity": {
            "design": "网络维权重 w ∈ [0,1]，其余三维均分 (1−w)/3",
            "leader_changes": leader_changes,
            "rank_track": rank_track,
            "sweep": sweeps,
            "note": "榜首对网络维权重不敏感（w 从 0 到 1 都是同一家），但 3—10 名在 w=0.25 与 w=1 之间几乎全部换位；"
                    "所以「谁是第一」在这套数据上是稳的，「前十是谁」不稳",
        },
        "domain_ipc": {
            "dim_status": {"产出规模": "可算", "网络影响": "不可算（置 null）"},
            "renormalize": False,
            "renormalize_note": "领域侧只有一维有值，若把网络维从分母剔除就等于宣称「被引为 0」，"
                                "故按缺维处置：该维置 null、总分不重归一化，只报单维产出分",
            "ipc_max": {"ipc4": ipc_rows[0][0], "patents": ipc_max},
            "top": ipc_top,
            "n_classes": len(ipc_all),
            "sum_patents": sum(ipc_all.values()),
        },
        "derived": derived,
        "coverage": {
            "paper_with_citation_pct": snap["steps"]["paper_inst"]["papers_with_citation_pct"],
            "patent_cited_match_pct": snap["steps"]["domain_cited"]["match_rate_pct"],
            "inst_intersection_pct_of_graph": snap["steps"]["inst_join"]["intersection_pct_of_graph"],
            "inst_intersection_pct_of_applicants": snap["steps"]["inst_join"]["intersection_pct_of_applicants"],
        },
        "absence_probe": {
            "graph_node": {"query": "information_schema.tables WHERE table_schema='gkx' AND table_name='graph_node'",
                           "param": "graph_node", "hit_tables": [], "hit_rows": 0,
                           "count": None, "conclusion": "gkx 查无此表；live 四 schema 亦无同名非 demo 表"},
            "impact_prediction": {"query": "information_schema.tables WHERE table_schema='gkx' AND table_name='impact_prediction'",
                                  "param": "impact_prediction", "hit_tables": [], "hit_rows": 0,
                                  "count": None, "conclusion": "gkx 查无此表；live 四 schema 亦无同名非 demo 表"},
            "note": "检索于 2026-10-23 由 code/_probe_w15n1_tables.py 与 code/_probe_keyd_w15n1.py 两次实测，"
                    "命中行数 0 即「不存在」，不是「有表但 0 行」",
        },
        "reproduce": "cd code && python3 _probe_impact_w15n1.py && python3 M_INNOV_IMPACT_SCORE.py",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"scored {n} institutions")
    for r in out["top_institutions"][:12]:
        print(f"  {r['rank']:>2} {r['score']:>6.2f} {r['inst']:<22} "
              f"pat={r['patents']:>6} pap={r['papers']:>4} deg={r['coauthor_degree']:>4} "
              f"grant={r['grant_rate_pct']}")
    print("entropy:", out["weights"]["entropy"])
    print("flips:", [(c["w_network"], c["leader"]) for c in leader_changes])
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
