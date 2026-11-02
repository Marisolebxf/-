#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_026 度数时间趋势（节点级） — 三源探针 + 久新真图节点度数轨迹实算 + 判档产物
口径：节点级年度累积度数序列 deg_y(v)（UI 折线一节点一线的原生语义）。
与 025（图级平均）共享时间维原料与采样框；本件交付节点级轨迹 + 上升最快新兴节点识别。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_026_out.json")

facts = {}
facts["ui_mount"] = "CentralityPanel.jsx:669 Card title=度数时间趋势（trendOption 折线 legend=节点名，一节点一线——节点级形态是 UI 原生语义）"
facts["ui_trend_source"] = "centralityAlgo.js:247-255 buildDegreeTrend(rows) 取前 6 节点生成式模拟（0.7+0.1i 系数）——非历史数据"
facts["srs_anchor"] = "算法展示.md seq 428（excel_row 431）：「同时提供趋势分析，展示节点在不同时间段的度数变化」"
facts["cat"] = "简单统计类（节点级度数计数按年展开）"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
names = {r[0]: r[1] for r in c["node_rows"]}
edges_main = [tuple(e) for e in c["main_edges"]]
evo = [tuple(r) for r in c["evo_rows"]]

facts["jiuxin_tech_nodes_total"] = c["nodes_total"]
facts["jiuxin_tech_edges_total"] = c["edges_total"]
facts["jiuxin_tech_sample_nodes"] = len(nodes)
facts["jiuxin_tech_sample_induced_edges"] = len(edges_main)
facts["jiuxin_evo_year_nonnull"] = sum(1 for r in evo if r[2] is not None)

YEARS = list(range(2016, 2026))

# 节点级轨迹：框内全部有边节点逐一计数（确定性：节点 sorted，年份写死）
present = set()
for u, v in edges_main:
    present.add(u); present.add(v)
node_list = sorted(present)
trajectories = {}
for y in YEARS:
    active = [(r[0], r[1]) for r in evo if r[2] is not None and r[2] <= y]
    for nid in node_list:
        trajectories.setdefault(nid, []).append(sum(1 for u, v in active if u == nid or v == nid))

# 上升最快节点（新兴技术识别）：2016 vs 2025 度数增量 Top5（确定性：增量降序、同增 id 升序）
deltas = sorted(((trajectories[n][-1] - trajectories[n][0], n) for n in node_list), key=lambda t: (-t[0], t[1]))[:5]
rising = [{"node_id": n, "name_original": names.get(n, ""), "deg_2016": trajectories[n][0], "deg_2025": trajectories[n][-1], "delta": d} for d, n in deltas]

# 终态度数 Top5（与 025 互证）
deg_final = gb.degree_map(nodes, edges_main)
top5 = sorted(nodes, key=lambda n: (-deg_final.get(n, 0), n))[:5]
top5_tr = [{"node_id": n, "name_original": names.get(n, ""), "final_degree": deg_final.get(n, 0), "series": trajectories[n]} for n in top5]

# 全体节点增量的分布读数（趋势区分度证据）
all_deltas = [trajectories[n][-1] - trajectories[n][0] for n in node_list]
all_deltas_sorted = sorted(all_deltas)
n_all = len(all_deltas_sorted)
derived = [{
    "source": "jiuxin.ads_technology_evolution_edge 节点级年度累积度数（5000 节点框）",
    "mode": "node_trajectory_cumulative",
    "years": YEARS,
    "nodes_scored": n_all,
    "top5_final_trajectories": top5_tr,
    "rising_top5_by_delta": rising,
    "delta_distribution": {
        "min": all_deltas_sorted[0], "median": all_deltas_sorted[n_all // 2],
        "p90": all_deltas_sorted[int(n_all * 0.9)], "max": all_deltas_sorted[-1],
    },
}]

absence_probe = [
    {"what": "dev 图历史快照承载", "how": "族级快照 26 张词族计数", "hits": "全 0 行——无历史数据"},
    {"what": "UI 前端节点趋势数据源", "how": "centralityAlgo.js:247-255 读码", "hits": "生成式模拟非历史读数"},
    {"what": "久新现成节点度数轨迹结果面", "how": "词族扫描（probe_s305）", "hits": "0——需现场转换"},
    {"what": "gkx 合作网时间维", "how": "dwd_scholar_coauthor 列核对", "hits": "无年份列——备选承载无时序"},
]

out = {"metric_id": "M_SCIUI_KGANALY_026", "metric_name": "度数时间趋势（节点级·科技知识图谱·度中心性 Tab）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": YEARS,
       "base_years_missing": ["2026（不完整年度：框内证据边仅 175 条，不入窗）"],
       "base_years_note": "节点级年度累积度数窗口 2016-2025（十个完整年度）；与 025 共享快照口径与时间维原料（first_evidence_year）"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
