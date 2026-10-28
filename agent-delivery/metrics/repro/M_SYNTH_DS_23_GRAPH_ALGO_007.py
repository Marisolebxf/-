#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_007 紧密中心性计算与展示。

口径（networkx wf_improved 版）：
  C_C(v) = (r_v - 1) / (n - 1) * (r_v - 1) / sum_{u in R(v)} d(v,u)
其中 R(v) 是 v 所在连通分量内可达的节点集，r_v = |R(v)|，n 是所选点集节点数。
主点集 = P2 巨型连通分量（15,223 节点 / 36,965 边）——分量内 r_v = n，修正因子为 1，
C_C 退化为 (n-1)/sum d，于是「平均距离 = 1 / C_C」这条读法在主口径上成立。

零 SQL：读数来自族级共享快照 code/_snapshots21/graph_algo_23_20261023.json。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_007_out.json
"""
from __future__ import annotations

import json

import _graph_algo_23_common as C

MID = "M_SYNTH_DS_23_GRAPH_ALGO_007"


def with_distance(rows, k=20):
    """top-k 表 + 由 closeness 反推的平均距离（巨型分量内 C_C = 1/mean_dist）。"""
    out = C.topn(rows, "c_close", k, 100, 3)
    for r in out:
        c = r["value"] / 100.0
        r["implied_mean_distance"] = round(1.0 / c, 3) if c > 0 else None
    return out


def main():
    snap = C.load()
    rows = snap["nodes"]
    n2 = snap["graph"]["giant"]["n_nodes"]
    e2 = snap["graph"]["giant"]["n_edges"]
    stats = snap["centrality_stats"]

    ps_stats = {
        pid: C.rescale(stats["%s_closeness" % pid], 100)
        for pid in ("P0", "P1", "P2", "P3", "P4")
    }
    close = {r["name"]: r["c_close"] for r in rows}
    deg = {r["name"]: r["c_deg"] for r in rows}
    betw = {r["name"]: r["c_betw"] for r in rows}

    top20 = with_distance(rows, 20)

    peer = {}
    p6 = C.HERE / "M_SYNTH_DS_23_GRAPH_ALGO_006_out.json"
    if p6.exists():
        d6 = json.loads(p6.read_text(encoding="utf-8"))
        s6 = d6["results"]["subgraph_sensitivity"]
        peer["006_degree_subgraph_spearman"] = {
            "P3": s6["P3"]["spearman_vs_P2"], "P4": s6["P4"]["spearman_vs_P2"],
            "note": "同族 006 的度中心性在同样两个子图上的秩相关，用于说明「closeness 对截断更稳健」"}
        peer["006_degree_top100"] = {"P3": s6["P3"]["top100"], "P4": s6["P4"]["top100"]}

    sens = {}
    for pid in ("P3", "P4"):
        sub = C.sub_series(snap, pid, "c_close")
        common = {k: close[k] for k in sub}
        meta = next(p for p in snap["point_sets"] if p["id"] == pid)
        sens[pid] = {
            "coverage_nodes_pct": round(meta["coverage_nodes"] * 100, 2),
            "n_nodes": meta["n_nodes"],
            "spearman_vs_P2": C.spearman(common, sub),
            "top100": C.top100_overlap(close, sub),
            "max_pct": C.rescale(stats["%s_closeness" % pid], 100)["max"],
            "median_pct": C.rescale(stats["%s_closeness" % pid], 100)["median"],
        }

    # 主口径的「距离分层」：closeness 换成分量内平均距离
    dist_bands = {}
    for lo, hi, label in ((0.0, 3.0, ">=33.3 跳"), (3.0, 4.0, "25.0-33.3 跳"),
                          (4.0, 5.0, "20.0-25.0 跳"), (5.0, 10.0, "10.0-20.0 跳"),
                          (10.0, 100.0, "<10.0 跳")):
        n = sum(1 for v in close.values() if lo <= v * 100 < hi)
        dist_bands[label] = {"n": n, "share_pct": round(n / n2 * 100, 2)}

    doc = {
        "metric_id": MID,
        "metric_name": "紧密中心性计算与展示",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读族级共享快照",
        "data_source": snap["source"],
        "formula": ("C_C(v) = (r_v-1)/(n-1) * (r_v-1)/sum d(v,u)，"
                    "r_v 为分量内可达节点数（networkx wf_improved）"),
        "reporting_unit": ("正文以百分比（x100）报紧密中心性：2.239 表示 2.239%，"
                           "即 0.02239；在巨型分量内它等于「分量内平均距离」的倒数。"),
        "scope": {
            "main_point_set": "P2 巨型连通分量（15,223 节点 / 36,965 边）",
            "main_reason": ("closeness 依赖「可达节点数」，跨连通分量不可比；"
                            "只有 P2 内所有节点两两可达，读数才等价于「到全体的平均距离倒数」"),
            "sensitivity_point_sets": ["P0 全图（含 3,540 个孤立点，恒 0）", "P1 有边子图（16,896 节点 / 646 个分量）",
                                       "P3 度>=5 子图", "P4 度>=10 子图"],
        },
        "graph": C.graph_block(snap),
        "construction": snap["construction"],
        "point_sets": snap["point_sets"],
        "results": {
            "n_nodes": n2,
            "n_edges": e2,
            "centrality_stats_pct": ps_stats,
            "top20": top20,
            "top1_name": top20[0]["name"],
            "top1_pct": top20[0]["value"],
            "top1_implied_mean_distance": top20[0]["implied_mean_distance"],
            "top100_type_mix": C.type_mix(rows, "c_close", 100),
            "type_mix_all": snap["type_mix"]["all"],
            "distance_bands_from_closeness": dist_bands,
            "mean_pct": ps_stats["P2"]["mean"],
            "mean_implied_distance": round(100.0 / ps_stats["P2"]["mean"], 3),
            "median_implied_distance": round(100.0 / ps_stats["P2"]["median"], 3),
            "max_raw": round(ps_stats["P2"]["max"] / 100.0, 6),
            "mean_raw": round(ps_stats["P2"]["mean"] / 100.0, 6),
            "median_raw": round(ps_stats["P2"]["median"] / 100.0, 6),
            "min_raw": round(ps_stats["P2"]["min"] / 100.0, 6),
            "min_implied_distance": round(100.0 / ps_stats["P2"]["min"], 3),
            "max_implied_distance": round(100.0 / ps_stats["P2"]["max"], 3),
            "spearman_vs_degree": snap["rank_corr"]["degree~closeness"],
            "spearman_vs_betweenness": snap["rank_corr"]["closeness~betweenness"],
            "spearman_vs_pagerank": snap["rank_corr"]["closeness~pagerank"],
            "top100_overlap_vs_degree": snap["top100_overlap"]["degree~closeness"],
            "top100_overlap_vs_betweenness": snap["top100_overlap"]["closeness~betweenness"],
            "peer_cross_check": peer,
            "subgraph_sensitivity": sens,
            "isolates_full": snap["components"]["isolates"],
            "isolate_share_pct": round(snap["components"]["isolate_share"] * 100, 2),
            "giant_share_nodes_pct": round(snap["components"]["giant_share_nodes"] * 100, 2),
            "n_zero_closeness_giant": stats["P2_closeness"].get("n_zero"),
            "p0_zero_share_pct": round(C.rescale(stats["P0_closeness"], 100)["n_zero"] / 20436 * 100, 2),
            "derived_numbers": {
                "p0_denom_n_minus_1": next(p for p in snap["point_sets"] if p["id"] == "P0")["n_nodes"] - 1,
                "p1_denom_n_minus_1": next(p for p in snap["point_sets"] if p["id"] == "P1")["n_nodes"] - 1,
                "p2_denom_n_minus_1": n2 - 1,
                "sub_p3_denom_n_minus_1": sens["P3"]["n_nodes"] - 1,
                "sub_p4_denom_n_minus_1": sens["P4"]["n_nodes"] - 1,
                "community_modularity_012": snap["communities"]["modularity"],
            },
        },
        "display_spec": {
            "entry": "图谱页节点属性面板 / 机构榜单",
            "sort": "按紧密中心性降序，同分按机构名升序",
            "fields": ["rank", "name", "type", "degree", "papers", "value(%)",
                       "implied_mean_distance"],
            "pagination_hint": ("top20 可直接展示；全量 15,223 行见快照 nodes 数组。"
                                "展示时必须标注「在巨型分量 15,223 个机构内计算」"),
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "两库均无紧密中心性结果面（gkx 侧 enterprise_centrality 不存在，见附录 B），"
            "但所需结构只有一张边表：dwd_zh_paper.author_info_list 重建的机构合著图。"
            "在巨型分量 15,223 节点 / 36,965 边上做 15,223 次全源 BFS，精确算得每个节点的 "
            "closeness（非抽样、非近似），最大值 %s 的 %.3f%%，反推分量内平均距离 %.3f 跳。"
            "数据量足够、结构足够，现在就能算，故判完全转换支持。"
            % (top20[0]["name"], top20[0]["value"], top20[0]["implied_mean_distance"])),
        "caveats": [
            "closeness 只在连通分量内有意义；P0 含 4,186 个分量、P1 含 646 个，读数不可跨分量比较。",
            "本指标衡量「到全体的平均距离」，不衡量「认识谁」；一个边缘高校的 closeness 可能高于知名企业。",
            "节点是论文原始机构串，未做上下级归并，院系级碎片会拉低母体机构的 closeness。",
            "边只有论文共著，不含业务合作边；「近」是共著意义上的近。",
            "巨型分量占全图 74.49% 节点、96.75% 边，剩余 25.51% 的节点不在本口径内。",
        ],
        "paper_year_dist": snap["papers"]["year"],
        "sources": C.source_list(snap),
    }
    doc["edge_sources"] = C.edge_sources()
    doc.update(C.base_years(snap))
    C.write_out(MID, doc)
    print(json.dumps({"top5": top20[:5], "P2": ps_stats["P2"], "P0": ps_stats["P0"],
                      "sens": sens, "bands": dist_bands,
                      "corr_deg": doc["results"]["spearman_vs_degree"]},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
