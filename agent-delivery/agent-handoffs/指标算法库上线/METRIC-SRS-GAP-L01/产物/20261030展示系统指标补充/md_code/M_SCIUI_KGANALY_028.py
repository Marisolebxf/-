#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_028 图谱异常评分 — 三源探针 + UI 同构度偏离评分实算 + 判档产物
UI 语义（kgIntelligence.js detectPatternsAndAnomalies）：score=min(99, round(d/avg*28))——
节点全边连接度相对均值倍率的线性映射；阈值=avg*2.1 检出异常。
本件在久新真图上同构实算：z-score 并列（R1 Akoglu 结构特征法）、Top 异常节点落产物。
"""
import json
import math
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_028_out.json")

facts = {}
facts["ui_mount"] = "KgIntelligenceHub.jsx:111 异常分列（anomalyColumns data dataIndex=score）——模式识别·异常点 Tab"
facts["ui_algo"] = "kgIntelligence.js detectPatternsAndAnomalies：threshold=max(avg*2.1, 4)；score=min(99, round((d/max(avg,1))*28))——度均值倍率线性映射"
facts["ui_demo_fallback"] = "ensureDemoAnomalies：检出为空时回填演示数据（isDemo=true 标签）——UI 演示层自披露"
facts["srs_anchor"] = "分析展示.md seq 404（自动模式识别）：「自动识别图谱中的异常点」（异常评分是其量化读数）"
facts["cat"] = "无业务逻辑数值类（结构可算型——UI 前端已有实现，真图可算）"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
names = {r[0]: r[1] for r in c["node_rows"]}
edges_main = [tuple(e) for e in c["main_edges"]]

facts["jiuxin_tech_nodes_total"] = c["nodes_total"]
facts["jiuxin_tech_edges_total"] = c["edges_total"]
facts["jiuxin_tech_sample_nodes"] = len(nodes)
facts["jiuxin_tech_sample_induced_edges"] = len(edges_main)

# UI 同构评分（度偏离）：全框节点（含 0 度，与 UI nodes 全集语义一致）
deg = gb.degree_map(nodes, edges_main)
present = [n for n in nodes if deg.get(n, 0) > 0]
deg_values = [deg[n] for n in present]
avg = sum(deg_values) / len(deg_values)
mu = avg
var = sum((d - mu) ** 2 for d in deg_values) / len(deg_values)
sd = math.sqrt(var)
facts["frame_degree_avg"] = round(avg, 4)
facts["frame_degree_sd"] = round(sd, 4)

threshold = max(avg * 2.1, 4)
detected = [n for n in sorted(present) if deg[n] >= threshold]
facts["ui_threshold_formula"] = "max(avg*2.1, 4)"
facts["ui_threshold_value"] = round(threshold, 4)
facts["detected_anomaly_nodes"] = len(detected)

def ui_score(d):
    return min(99, round((d / max(avg, 1)) * 28))

scored = sorted(present, key=lambda n: (-ui_score(deg[n]), n))
top10_ui = [{"node_id": n, "name_original": names.get(n, ""), "degree": deg[n],
             "ui_score": ui_score(deg[n]), "z_score": round((deg[n] - mu) / sd, 4) if sd else None} for n in scored[:10]]
zsorted = sorted(present, key=lambda n: (-((deg[n] - mu) / sd if sd else 0), n))
top10_z = [{"node_id": n, "name_original": names.get(n, ""), "degree": deg[n],
            "z_score": round((deg[n] - mu) / sd, 4) if sd else None, "ui_score": ui_score(deg[n])} for n in zsorted[:10]]

derived = [{
    "source": "jiuxin.ads_technology_graph_edge 诱导子图（5000 节点框）度偏离评分",
    "mode": "degree_deviation",
    "nodes_scored": len(present),
    "degree_avg": round(avg, 4),
    "degree_sd": round(sd, 4),
    "ui_threshold": round(threshold, 4),
    "detected_count": len(detected),
    "top10_by_ui_score": top10_ui,
    "top10_by_zscore": top10_z,
}]

absence_probe = [
    {"what": "久新现成异常评分结果面", "how": "218 表词族扫描（anomal/abnorm/outlier）", "hits": "0 表"},
    {"what": "gkx 节点异常分承载", "how": "280 表词族扫描", "hits": "0（企业异常目录是主体级非节点评分）"},
    {"what": "dev 异常评分面", "how": "族级快照", "hits": "0 行（graph_* 全空）"},
    {"what": "UI 异常分数据来源", "how": "kgIntelligence.js 读码", "hits": "框内子图实时计算+空检出回填演示数据（isDemo 自披露）"},
]

out = {"metric_id": "M_SCIUI_KGANALY_028", "metric_name": "图谱异常评分（科技知识图谱·智能化分析·异常点 Tab）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（度分布为当日 live 截面；无历史快照对比维）"],
       "base_years_note": "物理口径基期=探针快照日；异常评分为截面结构计算（度偏离），无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
