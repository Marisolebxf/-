#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_025 平均度数时间趋势 — 三源探针 + 久新真图年度度数趋势实算 + 判档产物
口径：累积快照（snapshot）年度平均度数——年份窗口 [t0, y] 内激活边（first_evidence_year<=y）全量重算平均度。
锚文献：BTW 2023 temporal degree（快照度数时序）；Freeman 1978（度中心性）；UI 度中心性 Tab「度数时间趋势」。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_025_out.json")
snap_probe = json.load(open(os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")))

facts = {}
facts["ui_mount"] = "CentralityPanel.jsx:669 Card title=度数时间趋势（算法展示·中心性计算展示·度中心性 Tab 第三卡；trendOption 折线 :357-371，degreeTrend 数据源 centralityAlgo.js buildDegreeTrend :247-255 为 mock 生成式）"
facts["ui_trend_source"] = "centralityAlgo.js:247-255 buildDegreeTrend：base=degreeRaw，乘 (0.7+0.1i+扰动) 递增系数——前端无历史数据、为生成式模拟"
facts["srs_anchor"] = "算法展示.md seq 428（excel_row 431）度中心性计算与展示：「同时提供趋势分析，展示节点在不同时间段的度数变化」"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
names = {r[0]: r[1] for r in c["node_rows"]}
edges_main = [tuple(e) for e in c["main_edges"]]
evo = [tuple(r) for r in c["evo_rows"]]

facts["jiuxin_tech_nodes_total"] = c["nodes_total"]
facts["jiuxin_tech_edges_total"] = c["edges_total"]
facts["jiuxin_tech_sample_nodes"] = len(nodes)
facts["jiuxin_tech_sample_induced_edges"] = len(edges_main)
facts["jiuxin_evo_edges_induced"] = len(evo)
nonnull_years = [r[2] for r in evo if r[2] is not None]
facts["jiuxin_evo_year_nonnull"] = len(nonnull_years)
facts["jiuxin_evo_year_null"] = len(evo) - len(nonnull_years)

# 确定性年度序列：2016-2025（近年窗口；2026 年不完整仅 175 框内边不入窗，B10 披露）
YEARS = list(range(2016, 2026))
snapshot_avg_degree = {}
snapshot_edges = {}
for y in YEARS:
    active = [(r[0], r[1]) for r in evo if r[2] is not None and r[2] <= y]
    snapshot_edges[y] = len(active)
    if not active:
        snapshot_avg_degree[y] = None
        continue
    deg = gb.degree_map(nodes, active)
    present = [n for n in nodes if deg.get(n, 0) > 0]
    snapshot_avg_degree[y] = round(sum(deg[n] for n in present) / len(present), 4) if present else None

trend = [{"year": y, "active_edges": snapshot_edges[y], "avg_degree_present_nodes": snapshot_avg_degree[y]} for y in YEARS]

# Top 度数节点的年度轨迹（UI 折线=每节点一条线）：框内终态度数 Top5（确定性：度降序、同度 node_id 升序）
deg_final = gb.degree_map(nodes, edges_main)
top5 = sorted(nodes, key=lambda n: (-deg_final.get(n, 0), n))[:5]
trajectories = {}
for nid in top5:
    tr = []
    for y in YEARS:
        active = [(r[0], r[1]) for r in evo if r[2] is not None and r[2] <= y]
        d = sum(1 for u, v in active if u == nid or v == nid)
        tr.append(d)
    trajectories[nid] = tr

derived = [{
    "source": "jiuxin.ads_technology_evolution_edge 累积快照（5000 节点框，first_evidence_year<=y）",
    "mode": "snapshot_cumulative",
    "years": YEARS,
    "snapshot_trend": trend,
    "avg_degree_first_year": trend[0]["avg_degree_present_nodes"],
    "avg_degree_last_year": trend[-1]["avg_degree_present_nodes"],
    "top5_trajectories": [{"node_id": nid, "name_original": names.get(nid, ""), "final_degree": deg_final.get(nid, 0), "series": trajectories[nid]} for nid in top5],
}]

absence_probe = [
    {"what": "dev 图结构面时序承载（graph_node/edge 快照版本表）", "how": "族级快照 26 张词族计数", "hits": "26 张全 0 行——无历史快照数据"},
    {"what": "UI 前端度数趋势数据源", "how": "centralityAlgo.js:247-255 读码", "hits": "buildDegreeTrend 为生成式模拟（base*(0.7+0.1i)），非历史数据"},
    {"what": "久新现成度数趋势结果面", "how": "词族扫描（probe_s305）", "hits": "0——需现场转换计算"},
    {"what": "gkx 学者合作网时间维", "how": "dwd_scholar_coauthor 列核对", "hits": "无年份/时间列（coauthor 快照表）——备选承载无时序"},
]

out = {"metric_id": "M_SCIUI_KGANALY_025", "metric_name": "平均度数时间趋势（科技知识图谱·度中心性 Tab）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
       "base_years_missing": ["2026（窗口截至 2025-12-31：2026 框内证据边仅 175 条属不完整年度，不入窗防失真）"],
       "base_years_note": "年度基期=演化边 first_evidence_year 累积快照窗口 2016-2025（10 个完整年度）；不完整年度 2026 剔除并披露，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
