#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_DS_23_GRAPH_ALGO_009 PageRank 算法计算与展示。

口径（无向、无权、alpha=0.85、tol=1e-12、幂迭代，max_iter=500）：
  PR(v) = (1-alpha)/n + alpha * sum_{u in N(v)} PR(u)/d_u
保留阻尼带来的悬挂节点均匀分摊：base = alpha * sum_{dangling} PR / n。

主点集 = P2 巨型连通分量（15,223 节点 / 36,965 边）。
展示单位用「万分比」（x10000）：均匀分布时每个节点 = 10000/15223 = 0.657，
所以 0.657 就是均值线，1.300 表示均匀值的 1.98 倍。

另做三组对照，全部落在同一快照里：
  1) alpha 扫描 0.50/0.70/0.85/0.95：看排名对阻尼的敏感度；
  2) 加权版（边权 = 共同署名篇数）：看「合作次数」是否改变头部；
  3) 有向版（署名顺序 = 通讯/一作 -> 合作者）：看方向是否改变头部。

零 SQL：读数来自族级共享快照 code/_snapshots21/graph_algo_23_20261023.json。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_009_out.json
"""
from __future__ import annotations

import json

import _graph_algo_23_common as C

MID = "M_SYNTH_DS_23_GRAPH_ALGO_009"
BP = 10000.0


def decorated(rows, key, n, unif):
    out = C.topn(rows, key, n, BP, 4)
    for r in out:
        r["value_bp"] = r["value"]
        r["mult_vs_uniform"] = round(r["value_bp"] / unif, 3) if unif else None
    return out


def overlap(a, b, k=20):
    return len(set(x["name"] for x in a[:k]) & set(x["name"] for x in b[:k]))


def main():
    snap = C.load()
    pr = snap["pagerank"]
    rows = snap["nodes"]
    n2 = snap["graph"]["giant"]["n_nodes"]
    e2 = snap["graph"]["giant"]["n_edges"]
    unif = BP / n2

    st_plain = snap["centrality_stats"]["P2_pagerank"]
    st_weight = snap["centrality_stats"]["P2_pagerank_weighted"]
    st_dir = snap["centrality_stats"]["P2_pagerank_directed"]
    st_p1 = snap["centrality_stats"]["P1_pagerank"]

    def bp(s):
        return {"min": round(s["min"] * BP, 5), "p25": round(s["p25"] * BP, 5),
                "median": round(s["median"] * BP, 5), "mean": round(s["mean"] * BP, 5),
                "p75": round(s["p75"] * BP, 5), "p90": round(s["p90"] * BP, 5),
                "max": round(s["max"] * BP, 5)}

    top20 = decorated(rows, "c_pr", 20, unif)
    top20_w = decorated(rows, "c_pr_w", 20, unif)
    top20_d = decorated(rows, "c_pr_dir", 20, unif)

    peer = {}
    p7 = C.HERE / "M_SYNTH_DS_23_GRAPH_ALGO_007_out.json"
    if p7.exists():
        d7 = json.loads(p7.read_text(encoding="utf-8"))
        peer["007_closeness_vs_pagerank"] = {
            "spearman": d7["results"]["spearman_vs_pagerank"],
            "note": "同族 007 报的「紧密中心性 ~ PageRank」秩相关，用于说明两者几乎无关"}

    scan = []
    for s in pr["alpha_scan"]:
        scan.append({
            "alpha": s["alpha"],
            "iterations": s["iterations"],
            "residual": s["residual"],
            "top1": s["top1"],
            "max_bp": round(s["max"] * BP, 4),
            "spearman_vs_alpha085": s["spearman_vs_alpha085"],
        })

    doc = {
        "metric_id": MID,
        "metric_name": "PageRank算法计算与展示",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读族级共享快照",
        "data_source": snap["source"],
        "formula": "PR(v) = (1-alpha)/n + alpha * sum_{u in N(v)} PR(u)/d_u，alpha=0.85",
        "reporting_unit": ("正文以万分比（x10000）报 PageRank。均匀分布时每节点 = 10000/n = %.3f，"
                           "故 0.657 是均值线，1.300 表示均匀的 1.98 倍。"
                           % unif),
        "scope": {
            "main_point_set": "P2 巨型连通分量（15,223 节点 / 36,965 边），无向无权，alpha=0.85",
            "main_reason": ("PageRank 的随机游走在分量内封闭；P2 是唯一一个「游走不会被卡死」的点集。"
                            "P0 含 3,540 个孤立点（阻尼项把它们摊成均匀底噪），P1 含 646 个分量"),
            "variants": ["加权版（边权=共著篇数）", "有向版（署名顺序）", "alpha 0.50/0.70/0.85/0.95"],
            "sensitivity_point_sets": ["P1 有边子图（16,896 节点 / 38,208 边，646 个分量）"],
        },
        "graph": C.graph_block(snap),
        "construction": snap["construction"],
        "point_sets": snap["point_sets"],
        "parameters": {"alpha": pr["alpha"], "tol": pr["tol"],
                       "iterations_unweighted": pr["iterations_unweighted"],
                       "residual_unweighted": pr["residual_unweighted"],
                       "iterations_weighted": pr["iterations_weighted"],
                       "residual_weighted": pr["residual_weighted"],
                       "iterations_directed": pr["iterations_directed"],
                       "residual_directed": pr["residual_directed"]},
        "results": {
            "n_nodes": n2,
            "n_edges": e2,
            "uniform_bp": round(unif, 4),
            "stats_bp_unweighted": bp(st_plain),
            "stats_bp_weighted": bp(st_weight),
            "stats_bp_directed": bp(st_dir),
            "stats_bp_P1": bp(st_p1),
            "top20": top20,
            "top1_name": top20[0]["name"],
            "top1_bp": top20[0]["value_bp"],
            "top1_mult": top20[0]["mult_vs_uniform"],
            "top1_degree": top20[0]["degree"],
            "top1_papers": top20[0]["papers"],
            "top100_type_mix": C.type_mix(rows, "c_pr", 100),
            "type_mix_all": snap["type_mix"]["all"],
            "top100_share_of_mass_pct": round(sum(
                sorted((r["c_pr"] for r in rows), reverse=True)[:100]) * 100, 3),
            "top1pct_share_of_mass_pct": round(sum(
                sorted((r["c_pr"] for r in rows), reverse=True)[:152]) * 100, 3),
            "alpha_scan": scan,
            "top1_stability_across_alpha": len(set(s["top1"] for s in scan)) == 1,
            "top20_overlap_unweighted_vs_weighted": overlap(top20, top20_w),
            "top20_overlap_unweighted_vs_directed": overlap(top20, top20_d),
            "top20_weighted": top20_w,
            "top20_directed": top20_d,
            "peer_cross_check": peer,
            "spearman_vs_degree": snap["rank_corr"]["degree~pagerank"],
            "spearman_vs_betweenness": snap["rank_corr"]["betweenness~pagerank"],
            "top100_overlap_vs_degree": snap["top100_overlap"]["degree~pagerank"],
            "directed_graph": snap["directed_graph"],
            "pearson_degree_papers": snap["pearson_degree_papers"],
        },
        "display_spec": {
            "entry": "图谱页节点属性面板 / 影响力榜",
            "sort": "按 PageRank 降序，同分按机构名升序",
            "fields": ["rank", "name", "type", "degree", "papers", "value_bp",
                       "mult_vs_uniform"],
            "pagination_hint": ("top20 可直接展示；全量 15,223 行见快照 nodes 数组的 c_pr 字段。"
                                "展示必须标注「巨型分量内、alpha=0.85、无向无权」"),
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "两库均无 PageRank 结果面，但边表可由 dwd_zh_paper.author_info_list 重建，"
            "算法本身在内存里 40 次迭代收敛（残差 %.2e）。在 15,223 节点 / 36,965 边上算得"
            "头部 %.4f 万分比（均匀值的 %.2f 倍），并用 alpha 扫描、加权版、有向版三组对照"
            "证明头部不是参数假象。数据与算法都具备，故判完全转换支持。"
            % (pr["residual_unweighted"], top20[0]["value_bp"], top20[0]["mult_vs_uniform"])),
        "caveats": [
            "PageRank 在无向图上等价于「度中心性的阻尼版」，与度高度相关（见 spearman_vs_degree）；它不是独立信息源。",
            "有向版依赖 author_info_list 的顺序语义，而该字段的「一作/通讯」位置在部分刊物上不规范，故只作对照不作主口径。",
            "加权版把「合作 5 篇」当成 5 条边，等于放大高产合作对；主口径仍用无权版。",
            "alpha 越大头部越集中；0.85 是惯例值，扫描表给了 0.50/0.70/0.95 的对照。",
            "节点未做机构归并，PageRank 会被「高产子机构」抬高，不能直接当企业影响力。",
        ],
        "paper_year_dist": snap["papers"]["year"],
        "sources": C.source_list(snap),
    }
    doc["edge_sources"] = C.edge_sources()
    # 引用网闭合率：两张表都要登记（2026-10-23 补）。
    # 只引 `dwd_zh_paper_citation` 会把结论说成「0.0% ⇒ 引用网全断」，
    # 而 `dwd_zh_paper_reference` 比它宽 36%（196,619 vs 144,020 id），
    # 且有 165 个 id 能落回本库（0.0857%）。数字很小、结论不变，
    # 但「0」和「165」是两种事实：前者是「表不可用」，后者是「id 空间不同源」。
    # 正文按后者写，故产物也必须留这两个数，否则正文无法复核。
    doc["citation_closure"] = snap["citation_closure"]
    doc.update(C.base_years(snap))
    C.write_out(MID, doc)
    print(json.dumps({"uniform": round(unif, 4), "top10": top20[:10],
                      "stats": doc["results"]["stats_bp_unweighted"],
                      "scan": scan,
                      "ov": [doc["results"]["top20_overlap_unweighted_vs_weighted"],
                             doc["results"]["top20_overlap_unweighted_vs_directed"]],
                      "mass": [doc["results"]["top100_share_of_mass_pct"],
                               doc["results"]["top1pct_share_of_mass_pct"]],
                      "corr": doc["results"]["spearman_vs_degree"]},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
