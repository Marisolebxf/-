#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_034 知识图谱节点按类型分组的指标对比 — 多指标矩阵实算 + 判档产物
与 033 同挂载点（CentralityPanel.jsx:664）不同侧面：033=平均度单指标条形图；
034=按类型分组的**多指标对比矩阵**（度/加权度/成员度/中心性横比）。
本件在久新节点表采样框上按 chain_role × phase 两维分组，输出 4 指标对比矩阵。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_034_out.json")

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/CentralityPanel.jsx:664（typeBarOption；SRS row_01=497 名录「指标对比（节点类型维度对照）」）"
facts["ui_semantics"] = "节点类型维度上的多指标对照矩阵（SRS 原文「实体与连接的规模/结构统计」）"
facts["ui_demo_fallback"] = "演示层 mock 四类单指标；本件扩为 chain_role 分组 × 4 指标矩阵"
facts["srs_anchor"] = "与 033 同挂载点不同指标侧面：033 单指标条形图，034 多指标对比"
facts["cat"] = "无业务逻辑数值类"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
edges_main = [tuple(e) for e in c["main_edges"]]
deg = gb.degree_map(nodes, edges_main)
# 行结构: 0=id,1=name,2=zh,3=en,4=phase,5=chain_role,6=community_role,7=community_id,8=wd,9=first_pub,10=latest_pub

facts["jiuxin_nodes_total"] = c["nodes_total"]
facts["jiuxin_edges_total"] = c["edges_total"]
facts["frame_nodes"] = len(nodes)
facts["frame_edges"] = len(edges_main)

# 全表 membership_score 直查（030 已验证全表轻查可跑）
jx = gb.jx_connect()
jc = jx.cursor()
jc.execute("""SELECT technology_node_id, membership_score FROM ads_technology_graph_node""")
ms_map = {r[0]: (float(r[1]) if r[1] is not None else None) for r in jc.fetchall()}
jx.close()

# 按链路角色分组的 4 指标矩阵
groups = {}
for r in c["node_rows"]:
    g = r[5] or "NULL"
    groups.setdefault(g, []).append(r)

matrix = []
for g in sorted(groups):
    rs = groups[g]
    degs = [deg.get(r[0], 0) for r in rs]
    wds = [float(r[8]) for r in rs if r[8] is not None]
    mss = [ms_map.get(r[0]) for r in rs]
    mss = [m for m in mss if m is not None]
    cores = [1.0 if (r[6] or "") == "CORE" else 0.0 for r in rs]
    matrix.append({
        "chain_role": g,
        "n_nodes": len(rs),
        "avg_degree": round(sum(degs) / len(degs), 4),
        "avg_weighted_degree": round(sum(wds) / len(wds), 4) if wds else None,
        "avg_membership_score": round(sum(mss) / len(mss), 4) if mss else None,
        "core_ratio": round(sum(cores) / len(cores), 4),
    })

# 交叉维：phase × chain_role 节点计数矩阵（类型双维对照）
cross = {}
for r in c["node_rows"]:
    ph = r[4] or "NULL"
    ch = r[5] or "NULL"
    cross.setdefault(ph, {}).setdefault(ch, 0)
    cross[ph][ch] += 1
cross_sorted = {ph: dict(sorted(d.items())) for ph, d in sorted(cross.items())}

derived = [{
    "source": "jiuxin 采样框（5,000 节点）chain_role 分组 × 4 指标矩阵 + phase×chain 交叉计数",
    "metrics": ["avg_degree(诱导子图无向度)", "avg_weighted_degree(全图加权度)", "avg_membership_score(社区归属强度)", "core_ratio(CORE 角色占比)"],
    "matrix_by_chain_role": matrix,
    "cross_phase_x_chain_count": cross_sorted,
}]

absence_probe = [
    {"what": "久新 entity_type 多指标面", "how": "节点表 26 列全扫", "hits": "0（同质图；以 chain_role 分组 + 表内现成多指标列替代）"},
    {"what": "gkx 多指标分组面", "how": "280 表词族扫描", "hits": "0"},
    {"what": "UI 多指标对比来源", "how": "CentralityPanel.jsx 读码", "hits": "单指标 typeBarOption mock；多指标矩阵为本件按 SRS 名录语义扩展"},
]

out = {"metric_id": "M_SCIUI_KGANALY_034", "metric_name": "知识图谱节点按类型分组的指标对比（节点类型维度对照）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（分组指标矩阵为当日 live 截面）"],
       "base_years_note": "物理口径基期=探针快照日；分组多指标对比为截面统计，无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
for m in matrix:
    print(m["chain_role"], "n=", m["n_nodes"], "deg=", m["avg_degree"], "wd=", m["avg_weighted_degree"], "ms=", m["avg_membership_score"], "core%", m["core_ratio"])
