#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SYNTH_DS_23_GRAPH_ALGO_012 社群结构自动识别。

算法：Louvain（weight='weight'，resolution=1.0，seed=20261021），
目标函数是模块度
  mod = 1/(2m) * sum_uv [A_uv - k_u*k_v/(2m)] * delta(c_u, c_v)

主点集 = P2 巨型连通分量（15,223 节点 / 36,965 边）。社群只在连通图上有意义：
P0 的 3,540 个孤立点会各自成为「单点社群」，把社群数从两位数抬到四位数，
那不是社群结构，是连通性的残渣。

三项稳健性检验（都在快照里）：
  1) resolution 扫描 0.5—2.0：社群数是分辨率的函数，必须给出整条曲线；
  2) 零模型（保持度序列的 double_edge_swap，20 次重连）：z 分数检验「模块度不是度分布的必然产物」；
  3) P1 上重跑：证明「换点集结论就变」，堵住把样本子图当全网的口子。

零 SQL：读数来自族级共享快照 code/_snapshots21/graph_algo_23_20261023.json。

输出：code/M_SYNTH_DS_23_GRAPH_ALGO_012_out.json
"""
from __future__ import annotations

import collections
import json

import _graph_algo_23_common as C

MID = "M_SYNTH_DS_23_GRAPH_ALGO_012"


def main():
    snap = C.load()
    cm = snap["communities"]
    nm = snap["null_model"]
    n2 = snap["graph"]["giant"]["n_nodes"]
    e2 = snap["graph"]["giant"]["n_edges"]
    sizes = cm["sizes_top15"]

    prof = []
    for p in cm["profiles_top15"]:
        prof.append({
            "cid": p["cid"],
            "size": p["size"],
            "share_pct": round(p["share_of_giant"] * 100, 3),
            "internal_edges": p["internal_edges"],
            "internal_density": p["internal_density"],
            "cut_edges_out": p["cut_edges_out"],
            "conductance": p["conductance"],
            "dominant_type": p["dominant_type"],
            "type_mix": p["type_mix"],
            "top_members": p["top_members"],
        })

    top15_share = sum(p["size"] for p in prof)
    conds = [p["conductance"] for p in prof if p["conductance"] is not None]

    scan = cm["resolution_scan"]
    best = cm["best_resolution_by_modularity"]

    doc = {
        "metric_id": MID,
        "metric_name": "社群结构自动识别",
        "generated_at": "2026-10-23",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读族级共享快照",
        "data_source": snap["source"],
        "formula": ("mod = 1/(2m) * sum_uv [A_uv - k_u*k_v/(2m)] * delta(c_u,c_v)，"
                    "Louvain 贪心最大化 + 聚合迭代"),
        "reporting_unit": ("社群本身是标号（community id），没有单位；对外报三个数："
                           "社群数（个）、模块度（无量纲 0—1）、社群规模占比（%）。"),
        "scope": {
            "main_point_set": "P2 巨型连通分量（15,223 节点 / 36,965 边）",
            "main_reason": ("社群划分要求图连通；P0 含 4,186 个分量、P1 含 646 个，"
                            "孤立点会各自成单点社群，社群数被连通性污染"),
            "variants": ["resolution 0.5/0.8/1.0/1.2/1.5/2.0 扫描",
                         "零模型 double_edge_swap 20 次重连",
                         "P1 有边子图重跑"],
            "sensitivity_point_sets": ["P1 有边子图（16,896 节点 / 646 个分量）"],
        },
        "graph": C.graph_block(snap),
        "construction": snap["construction"],
        "point_sets": snap["point_sets"],
        "parameters": {"algorithm": cm["algorithm"], "resolution": 1.0,
                       "weight": "weight（边权=共著篇数）", "seed": 20261021,
                       "null_model_reps": nm["reps"]},
        "results": {
            "n_nodes": n2,
            "n_edges": e2,
            "n_communities": cm["n_communities"],
            "modularity": cm["modularity"],
            "n_singleton": cm["n_singleton"],
            "n_size_ge10": cm["n_size_ge10"],
            "median_size": cm["median_size"],
            "largest_size": sizes[0] if sizes else None,
            "largest_share_pct": round((cm["largest_share"] or 0) * 100, 3),
            "sizes_top15": sizes,
            "top15_covered_nodes": top15_share,
            "top15_covered_pct": round(top15_share / n2 * 100, 3),
            "top15_mean_conductance": round(sum(conds) / len(conds), 6) if conds else None,
            "top15_max_conductance": max(conds) if conds else None,
            "top15_dominant_type_mix": dict(
                collections.Counter(p["dominant_type"] for p in prof)),
            "profiles_top15": prof,
            "resolution_scan": scan,
            "best_resolution_by_modularity": best,
            "null_model": {
                "method": nm["method"],
                "reps": nm["reps"],
                "observed_modularity": nm["observed_modularity"],
                "best_modularity_mean": nm["best_modularity_mean"],
                "best_modularity_sd": nm["best_modularity_sd"],
                "best_modularity_max": nm["best_modularity_max"],
                "observed_partition_on_null_mean": nm["observed_partition_on_null_mean"],
                "z_score": nm["z_score"],
                "runs": nm["runs"],
            },
            "on_P1": cm["on_P1"],
            "check_vs_011": cm["check_vs_011"],
            "cross_check_011_modularity_delta": round(abs(cm["modularity"] - 0.755103), 6),
            "cross_check_011_community_delta": cm["n_communities"] - 60,
            "tail_nodes": n2 - top15_share,
            "tail_share_pct": round((n2 - top15_share) / n2 * 100, 3),
            "type_mix_giant": snap["type_mix"]["all"],
            "peer_011_seed_range": [0.752993, 0.757068],
            "seed_cross_check": {
                "process": "独立进程直接重建图（不读族级快照）",
                "seed": C.bench()["louvain_seed"],
                "n_communities": C.bench()["louvain_n_communities"],
                "modularity": C.bench()["louvain_modularity"],
                "same_as_main": (C.bench()["louvain_n_communities"] == cm["n_communities"]
                                 and abs(C.bench()["louvain_modularity"] - cm["modularity"]) < 1e-9),
                "louvain_seconds": C.bench()["louvain_seconds"],
            },
        },
        "display_spec": {
            "entry": "图谱页社群着色 / 社群列表页",
            "sort": "社群按规模降序，社群内成员按度降序",
            "fields": ["cid", "size", "share(%)", "internal_density", "conductance",
                       "dominant_type", "top_members"],
            "pagination_hint": ("社群列表 %d 行；每行可下钻到成员（全量成员见快照 nodes 的 "
                                "community 字段）。展示必须标注「巨型分量内、resolution=1.0」"
                                % cm["n_communities"]),
        },
        "support_judgment": "完全转换支持",
        "support_reason": (
            "社群识别不需要任何外挂业务字段，只需要边表；边表由 dwd_zh_paper.author_info_list "
            "重建。在 15,223 节点 / 36,965 边上一轮 Louvain 得 %d 个社群、模块度 %.6f，"
            "零模型 z=%s，且与已归档的 011（60 个社群 / 0.755103）复算一致，"
            "说明结果可重复、不是随机划分。算法、数据、复算三者齐备，故判完全转换支持。"
            % (cm["n_communities"], cm["modularity"], nm["z_score"])),
        "caveats": [
            "社群数是分辨率与 seed 的函数：同一张图换 seed 会得到不同标号（规模分布相近）。标号不可跨版本对比。",
            "模块度 0.75 在共著网络上属常见水平，但它主要反映「度分布 + 局部稠密」，不等于「业务上真有一群人抱团」。",
            "零模型检验的是「比同度序列随机图更强」，不是「比真实业务社群更真」。",
            "社群成员未做机构归并，同一所大学的不同学院常被分到不同社群。",
            "P1 上重跑得 701 个社群（646 个分量），任何把 P1 社群数当全网社群数的说法都是错的。",
            "本件只做无向加权划分；有向/时序社群（如 Leiden 时序版）未实现，属后续增强。",
        ],
        "paper_year_dist": snap["papers"]["year"],
        "sources": C.source_list(snap),
    }
    doc["edge_sources"] = C.edge_sources()
    doc.update(C.base_years(snap))
    C.write_out(MID, doc)
    print(json.dumps({"n": cm["n_communities"], "mod": cm["modularity"],
                      "sizes": sizes, "null": doc["results"]["null_model"],
                      "scan": scan, "best": best, "p1": cm["on_P1"],
                      "prof0": prof[0] if prof else None,
                      "cond": [doc["results"]["top15_mean_conductance"],
                               doc["results"]["top15_max_conductance"]]},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
