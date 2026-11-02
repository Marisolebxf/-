#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_033 按节点类型分组比较 — 久新节点表发展阶段/链路角色分组实算 + 判档产物
UI 语义（CentralityPanel.jsx:664 typeBarOption）：按节点类型分组的平均度条形图。
久新节点表无 entity type 列，但有语义最近的两个「类型维」：
current_development_phase（发展阶段 6 档）与 chain_role（产业链角色）——分组均值可直查。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_033_out.json")

facts = {}
facts["ui_mount"] = "pages/tech-knowledge-graph/CentralityPanel.jsx:664（typeBarOption 按类型平均度条形图）"
facts["ui_semantics"] = "节点按类型分组的中心性对比（SRS row_01=496：按节点类型分组比较）"
facts["ui_demo_fallback"] = "typeBarOption 演示数据为论文/专利/学者/机构四类 mock 分组——真图无 entity_type 列"
facts["srs_anchor"] = "SRS 原文「实体与连接的规模/结构统计」；类型维以发展阶段/链路角色两档语义替代（本表最近类型维）"
facts["cat"] = "无业务逻辑数值类"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
names = {r[0]: r[1] for r in c["node_rows"]}
# 缓存行结构: 0=id,1=name,2=zh,3=en,4=phase,5=chain_role,6=community_role,7=community_id,8=wd,9=first_pub,10=latest_pub
edges_main = [tuple(e) for e in c["main_edges"]]
deg = gb.degree_map(nodes, edges_main)

facts["jiuxin_nodes_total"] = c["nodes_total"]
facts["jiuxin_edges_total"] = c["edges_total"]
facts["frame_nodes"] = len(nodes)
facts["frame_edges"] = len(edges_main)

def group_stats(keyidx, label):
    groups = {}
    for r in c["node_rows"]:
        g = (r[keyidx] or "NULL")
        groups.setdefault(g, []).append(deg.get(r[0], 0))
    out = []
    for g in sorted(groups):
        vals = groups[g]
        out.append({"group": g, "label": label, "n_nodes": len(vals),
                    "avg_degree": round(sum(vals) / len(vals), 4),
                    "max_degree": max(vals),
                    "total_degree": sum(vals)})
    return out

phase_groups = group_stats(4, "current_development_phase")
chain_groups = group_stats(5, "chain_role")

derived = [{
    "source": "jiuxin 采样框（5,000 节点/38,383 诱导边）分组平均度",
    "dimension_1_development_phase": phase_groups,
    "dimension_2_chain_role": chain_groups,
    "frame_avg_degree": round(sum(deg.values()) / len(nodes), 4),
}]

absence_probe = [
    {"what": "久新节点 entity_type 列（论文/专利/学者/机构四类）", "how": "节点表 26 列 DESCRIBE 全扫", "hits": "0（表为技术节点同质图，无实体类型列）——语义最近类型维=发展阶段/链路角色"},
    {"what": "gkx 分组承载", "how": "280 表词族扫描", "hits": "0（scholar_coauthor 等为同质图）"},
    {"what": "dev 分组面", "how": "族级快照", "hits": "0 行"},
    {"what": "UI 类型分组来源", "how": "CentralityPanel.jsx 读码", "hits": "typeBarOption mock 四类（论文/专利/学者/机构）——演示层"},
]

out = {"metric_id": "M_SCIUI_KGANALY_033", "metric_name": "按节点类型分组比较（科技知识图谱·中心性面板·类型分组条形图）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（分组平均度为当日 live 截面）"],
       "base_years_note": "物理口径基期=探针快照日；分组对比为截面统计，无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
for g in phase_groups:
    print("phase:", g["group"], "n=", g["n_nodes"], "avg_deg=", g["avg_degree"])
for g in chain_groups:
    print("chain:", g["group"], "n=", g["n_nodes"], "avg_deg=", g["avg_degree"])
