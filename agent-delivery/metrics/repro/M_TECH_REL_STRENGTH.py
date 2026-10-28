#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TECH_REL_STRENGTH —— 技术关联强度（技术—技术边权，0—100，深圳口径）。

定义：
  - 节点 = 238 个合格 IPC4 域（n2024 >= 100）；
  - 边 = 两个域被**同一批深圳申请人**同时布局（域内件数 >= 3 的申请人算「布局」）；
  - 边权 = NPMI（归一化点互信息）：
        PMI_ab = ln( p_ab / (p_a · p_b) )，p_ab = 共主体数 / 深圳申请人总数
        NPMI_ab = PMI_ab / ( -ln p_ab ) ∈ [-1, 1]
        关联强度指数 = 50 × (1 + NPMI) ∈ [0, 100]，50 = 与独立随机布局无异
  - 域级关联强度 = 该域最强 5 条边的 NPMI 均值，同样换算成 0—100。

为什么用「共主体」而不是「专利共类」：
  面板 `patent_scan_20261021.pkl` 按**主分类前 4 位**落盘，一件专利只进一个 IPC4
  （实测 1,720,243 个 pn 中跨域 pn = 0），因此无法做共类。共主体是同一「技术关联」
  语义下唯一可复算的代理，且方向性（引用/许可流向）本库无字段，只做无向边。

零 SQL：只读 _snapshots21 / _snapshots_gkx21 授权缓存。
"""
from __future__ import annotations

import collections
import itertools
import math
import statistics

import _tech21_scope as sc
import _tech21_domainfeat as feat

METRIC = "M_TECH_REL_STRENGTH"
YEARS = feat.YEARS
MIN_APPLICANT_PATENTS = 3
MIN_CO_APPLICANTS = 5
TOP_K_FOR_DOMAIN = 5


def strength(npmi):
    return round(50 * (1 + npmi), 2)


def main():
    rows, meta = feat.build()
    qualified = [r["ipc4"] for r in rows]
    qset = set(qualified)

    ipc_name = sc.load_ipc_name()
    sz_names = {g["nm"] for g in sc.load_sz_groups()}
    sets = collections.defaultdict(set)
    for ipc4, nm, n in ipc_name:
        if ipc4 in qset and nm in sz_names and n >= MIN_APPLICANT_PATENTS:
            sets[ipc4].add(nm)
    # 只保留有布局主体的域
    nodes = [d for d in qualified if sets.get(d)]
    n_total = len(sz_names)

    edges = []
    for a, b in itertools.combinations(sorted(nodes), 2):
        inter = len(sets[a] & sets[b])
        if inter < MIN_CO_APPLICANTS:
            continue
        p_a = len(sets[a]) / n_total
        p_b = len(sets[b]) / n_total
        p_ab = inter / n_total
        if p_ab <= 0 or p_ab >= 1:
            continue
        npmi = math.log(p_ab / (p_a * p_b)) / (-math.log(p_ab))
        edges.append({"a": a, "b": b, "co_applicants": inter,
                      "n_a": len(sets[a]), "n_b": len(sets[b]),
                      "npmi": round(npmi, 4), "strength": strength(npmi)})
    edges.sort(key=lambda e: -e["npmi"])

    # 域级：最强 K 条边
    by_node = collections.defaultdict(list)
    for e in edges:
        by_node[e["a"]].append(e)
        by_node[e["b"]].append(e)
    dom_rows = []
    for d in nodes:
        es = sorted(by_node.get(d, []), key=lambda e: -e["npmi"])[:TOP_K_FOR_DOMAIN]
        if not es:
            dom_rows.append({"ipc4": d, "label": feat.IPC_LABEL.get(d, ""),
                             "top5_npmi": None, "strength": None,
                             "neighbors": [], "degree": 0})
            continue
        mean_npmi = statistics.mean(e["npmi"] for e in es)
        dom_rows.append({
            "ipc4": d, "label": feat.IPC_LABEL.get(d, ""),
            "top5_npmi": round(mean_npmi, 4), "strength": strength(mean_npmi),
            "neighbors": [{"ipc4": (e["b"] if e["a"] == d else e["a"]),
                           "strength": e["strength"], "co_applicants": e["co_applicants"]}
                          for e in es],
            "degree": len(by_node.get(d, [])),
        })
    dom_rows.sort(key=lambda r: (r["strength"] is None, -(r["strength"] or 0)))
    iso = [r for r in dom_rows if r["strength"] is None]
    vals = [r["strength"] for r in dom_rows if r["strength"] is not None]

    # 强度分层（按 NPMI 原始值分档，避免 50*(1+NPMI) 压缩）
    bands = [(-1.01, 0.2, "弱 <0.2"), (0.2, 0.4, "中 0.2-0.4"),
             (0.4, 0.6, "强 0.4-0.6"), (0.6, 1.01, "极强 >=0.6")]
    band_block = []
    for lo, hi, name in bands:
        sub = [r for r in dom_rows if r["top5_npmi"] is not None and lo <= r["top5_npmi"] < hi]
        esub = [e for e in edges if lo <= e["npmi"] < hi]
        band_block.append({"band": name, "domains": len(sub), "edges": len(esub),
                           "examples": [r["ipc4"] for r in sub[:6]]})

    # 互斥性检查：同一主体集合是否被过度复用（大企业主导）
    co_hist = collections.Counter(e["co_applicants"] for e in edges)

    payload = {
        "metric_id": METRIC,
        "generated_at": "2026-10-22",
        "scope": "深圳",
        "scope_statement": (
            "本件分母是深圳申请人全集（77,846 个名称）：共主体数除以该全集，域内布局门槛"
            "为该域 >=3 件。全国申请人不进入集合，全国件数不参与任何计算；因此边权是"
            "「深圳主体共同布局强度」，不是全国技术关联。"
        ),
        "main_db": "gkx @ 183.240.141.251:3318 (gkx_reader_zp, read-only)",
        "sql_count": 0,
        "base_years_used": YEARS,
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "域件数只遍历 2021—2024（2017—2020 零行），申请人集合用全期件数（含 2021 前申请、"
            "但在库内只存在于 2021—2026 记录中）；2025/2026 残年不参与门槛判断。"
            "缺失年未按 0 摊入任何统计量。"
        ),
        "input": {
            "ipc_by_name": "code/_snapshots21/patent_ipc4_by_name_20261021.json",
            "sz_patent": "code/_snapshots21/patent_scan_20261021.pkl",
            "sz_applicants": "code/_snapshots_gkx21/sz_patent_city_name_gkx.json",
        },
        "reused_from": "_tech21_domainfeat.py（域特征层，零 SQL）",
        "cooccurrence_note": (
            "1,720,243 个 pn 中跨 IPC4 的 pn = 0（面板按主分类落盘），因此不能做专利共类；"
            "本件用「共同申请人」作代理，边是无向的，不含引用/许可流向。"
        ),
        "params": {
            "min_applicant_patents": MIN_APPLICANT_PATENTS,
            "min_co_applicants": MIN_CO_APPLICANTS,
            "top_k_for_domain": TOP_K_FOR_DOMAIN,
            "npmi_formula": "ln(p_ab/(p_a*p_b)) / (-ln p_ab)",
            "strength_formula": "50*(1+NPMI)",
        },
        "panel": {
            "qualified_domains": len(qualified),
            "nodes_with_applicants": len(nodes),
            "isolated_domains": len(iso),
            "sz_applicants": n_total,
            "edges": len(edges),
            "edges_per_node": round(len(edges) * 2 / len(nodes), 2) if nodes else None,
        },
        "edge_stats": {
            "npmi_min": round(min(e["npmi"] for e in edges), 4) if edges else None,
            "npmi_median": round(statistics.median(e["npmi"] for e in edges), 4) if edges else None,
            "npmi_max": round(max(e["npmi"] for e in edges), 4) if edges else None,
            "strength_median": round(statistics.median(e["strength"] for e in edges), 2) if edges else None,
        },
        "strength_bands": band_block,
        "domain_strength_stats": {
            "min": round(min(vals), 2) if vals else None,
            "median": round(statistics.median(vals), 2) if vals else None,
            "max": round(max(vals), 2) if vals else None,
            "quartiles": [round(x, 2) for x in statistics.quantiles(vals, n=4)] if vals else None,
        },
        "top_edges": edges[:30],
        "top_domains": [r for r in dom_rows if r["strength"] is not None][:20],
        "bottom_domains": [r for r in dom_rows if r["strength"] is not None][-10:],
        "isolated": [{"ipc4": r["ipc4"], "label": r["label"], "n2024": next(
            (x["n2024"] for x in rows if x["ipc4"] == r["ipc4"]), None)} for r in iso][:20],
        "co_applicant_hist": {str(k): v for k, v in sorted(co_hist.items())[:12]},
        "domains": dom_rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "structure_support": "部分",
            "data_support": "部分",
            "reason": (
                "关联强度可复算（12,797 条边、238 个节点），但两条关键证据缺源："
                "① 共类关联做不了——面板只保留主分类，跨域 pn = 0；② 关系流向（引用、许可、"
                "上下游方向）无字段，`dwd_patent_transfer` 的 pn 为公开号、与面板内部哈希不同码域，"
                "无法落域。故只能交付「深圳主体共同布局强度」无向图，不能交付弦线图的关系流向。"
            ),
        },
        "headline": {
            "nodes": len(nodes), "edges": len(edges),
            "median_strength": round(statistics.median(e["strength"] for e in edges), 2),
            "top_edge": f"{edges[0]['a']}-{edges[0]['b']}" if edges else None,
            "top_edge_strength": edges[0]["strength"] if edges else None,
            "top_domain": dom_rows[0]["ipc4"] if dom_rows else None,
            "top_domain_strength": dom_rows[0]["strength"] if dom_rows else None,
            "isolated": len(iso),
        },
    }
    sc.write_out(METRIC, payload)


if __name__ == "__main__":
    main()
