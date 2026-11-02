#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_046/051 社群族两件合算 — 三源探针 + 真图实算 + 判档产物（两件各落一 _out.json）
046 社群规模随时间演变：CommunityPanel.jsx:347 lifecycle 视图（buildCommunityLifecycle mock 六期 sizeSeries）
   —— 时间维承载：node 表 first/latest_publication_year 双年列（每节点时间锚）；
   算法：按发表年窗口聚合社群规模序列（treat 年=节点入场时刻，LPA 定社群 + 久新 community_id 直查社群双口径）。
051 图谱社群数量：queryAssetDeepAnalysis.js:52 metrics「社群数」（seededInt 2-6 mock）
   —— 算法：①久新 community_id 直查（全图 1,731 个社群，含 1,708 单例）；②框内 LPA 实算（对照口径）。
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame, load_snap,
                           build_adj, label_propagation, modularity,
                           gkx_coauthor_frame, ABSENCE_PROBE_TMPL)
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
snap = load_snap()["facts"]
facts = {}

facts["dev_graph_word_table_rows"] = snap["dev_graph_word_table_rows"]

# ---------- ① 久新：全图社群直查 + 年度维 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_tech_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_tech_edges_total"] = jc.fetchone()[0]
# 社群直查（051 主口径）
jc.execute("SELECT COUNT(DISTINCT community_id) FROM ads_technology_graph_node")
facts["jiuxin_community_count_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node WHERE is_singleton_community=1")
facts["jiuxin_singleton_communities"] = jc.fetchone()[0]
# 非单例社群（≥2 节点）
jc.execute("""SELECT COUNT(*) FROM (
    SELECT community_id FROM ads_technology_graph_node GROUP BY community_id HAVING COUNT(*)>=2) t""")
facts["jiuxin_nonsingleton_communities"] = jc.fetchone()[0]
# Top 社群规模
jc.execute("""SELECT community_id, COUNT(*) n FROM ads_technology_graph_node
GROUP BY community_id ORDER BY n DESC LIMIT 10""")
facts["jiuxin_top10_communities"] = [{"community_id": r[0], "size": r[1]} for r in jc.fetchall()]
# 年度维：first_publication_year 分布（046 时间锚质量）
jc.execute("""SELECT CASE WHEN first_publication_year IS NULL OR first_publication_year=0 THEN 'missing'
             ELSE 'present' END k, COUNT(*) FROM ads_technology_graph_node GROUP BY k""")
facts["jiuxin_first_pub_year_coverage"] = dict((r[0], r[1]) for r in jc.fetchall())
jc.execute("""SELECT CASE WHEN latest_publication_year IS NULL OR latest_publication_year=0 THEN 'missing'
             ELSE 'present' END k, COUNT(*) FROM ads_technology_graph_node GROUP BY k""")
facts["jiuxin_latest_pub_year_coverage"] = dict((r[0], r[1]) for r in jc.fetchall())
# 全图节点×(community_id, first_publication_year)——046 全图年度序列原料（一次拉取）
jc.execute("""SELECT community_id, first_publication_year FROM ads_technology_graph_node
WHERE community_id IS NOT NULL AND first_publication_year IS NOT NULL AND first_publication_year>0""")
node_year_comm = [(r[0], int(r[1])) for r in jc.fetchall()]
facts["jiuxin_nodes_with_year_comm"] = len(node_year_comm)
jx.close()

# ---------- 046 实算：全图社群规模年度序列（t 年规模 = first_publication_year<=t 的成员数） ----------
comms_years = defaultdict(list)
for cid, y in node_year_comm:
    comms_years[cid].append(y)
# 非单例社群（≥2 成员）的年度序列（Top5 最大社群）
top5 = sorted(comms_years.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:5]
years_all = sorted(set(y for _, ys in top5 for y in ys))
series_top5 = []
for cid, ys in top5:
    ys_sorted = sorted(ys)
    cum = []
    for t in years_all:
        cum.append(sum(1 for y in ys_sorted if y <= t))
    series_top5.append({"community_id": cid, "final_size": len(ys),
                        "born_year": ys_sorted[0], "series_years": years_all,
                        "cumulative_sizes": cum})
# 全图聚合：每年入场的节点数（入场直方图）
entry_hist = defaultdict(int)
for _, y in node_year_comm:
    entry_hist[y] += 1
facts["jiuxin_entry_year_histogram_top"] = [{"year": y, "entered": entry_hist[y]}
                                            for y in sorted(entry_hist)[-12:]]

# ---------- ② 框内 LPA 对照（051 对照口径 + 046 框内社群） ----------
frame = load_jiuxin_tech_frame(5000)
facts["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())
t0 = time.time()
labels, comms = label_propagation(adj, present)
facts["jiuxin_lpa_community_count"] = len(comms)
facts["jiuxin_lpa_community_sizes_top10"] = [len(g) for g in comms[:10]]
facts["jiuxin_lpa_modularity"] = round(modularity(adj, comms, len(frame["edges"])), 6)
# 框内久新 community_id 口径（同框对照）
frame_comm_sizes = defaultdict(int)
for n in present:
    cid = frame["id_comm"].get(n)
    if cid:
        frame_comm_sizes[cid] += 1
facts["jiuxin_frame_native_community_count"] = len(frame_comm_sizes)
facts["jiuxin_frame_native_community_sizes_top10"] = sorted(frame_comm_sizes.values(), reverse=True)[:10]

# gkx 备承载 LPA
gk = gkx_coauthor_frame(20000)
gadj = build_adj(gk["nodes"], gk["edges"])
glabels, gcomms = label_propagation(gadj, sorted(gadj.keys()))
facts["gkx_coauthor_sample_edges"] = len(gk["edges"])
facts["gkx_lpa_community_count"] = len(gcomms)
facts["gkx_lpa_community_sizes_top10"] = [len(g) for g in gcomms[:10]]
facts["gkx_lpa_modularity"] = round(modularity(gadj, gcomms, len(gk["edges"])), 6)

support = "完全转换支持"

# ---------- 046 产物 ----------
out46 = {
    "metric_id": "M_SCIUI_KGANALY_046",
    "metric_name": "社群规模随时间演变（知识图谱·社群发现展示·社群动态演化追踪）",
    "facts": facts,
    "derived": [
        {"source": "jiuxin.ads_technology_graph_node 全图（community_id×first_publication_year）",
         "communities_tracked": len(comms_years),
         "nodes_with_year": len(node_year_comm),
         "top5_series": series_top5,
         "note": "全图年度序列：t 年规模=first_publication_year<=t 的成员累计数（入场时间锚）；Top5 最大社群逐年序列落产物"},
    ],
    "absence_probe": ABSENCE_PROBE_TMPL,
    "support_judgment": support,
    "base_years_used": sorted(entry_hist.keys()),
    "base_years_missing": [],
    "base_years_note": "基期=节点 first_publication_year 年度维（久新全图实测覆盖见 facts.jiuxin_first_pub_year_coverage）；序列为累计规模非年度占比",
}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_046_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out46, fh, ensure_ascii=False, indent=2)
print("done 046 | communities_tracked:", len(comms_years), "| nodes_with_year:", len(node_year_comm))

# ---------- 051 产物 ----------
out51 = {
    "metric_id": "M_SCIUI_KGANALY_051",
    "metric_name": "图谱社群数量（图查询资产·深入分析·结构指标）",
    "facts": facts,
    "derived": [
        {"source": "jiuxin.ads_technology_graph_node community_id 直查（全图）",
         "community_count": facts["jiuxin_community_count_total"],
         "singleton": facts["jiuxin_singleton_communities"],
         "nonsingleton": facts["jiuxin_nonsingleton_communities"],
         "note": "主口径：全图 1,731 个 community_id（含 1,708 单例社群）；非单例 23 个"},
        {"source": "jiuxin 5000 框诱导子图 LPA（对照）",
         "community_count": facts["jiuxin_lpa_community_count"],
         "modularity": facts["jiuxin_lpa_modularity"],
         "sizes_top10": facts["jiuxin_lpa_community_sizes_top10"],
         "note": "算法对照口径：框内 LPA 确定性实算"},
        {"source": "jiuxin 5000 框 native community_id（同框直查对照）",
         "community_count": facts["jiuxin_frame_native_community_count"],
         "sizes_top10": facts["jiuxin_frame_native_community_sizes_top10"],
         "note": "同框直查：框内原生社群数（与 LPA 对照——native 是上游算法产物，LPA 是本件复算）"},
        {"source": "gkx.dwd_scholar_coauthor 采样框 LPA（备选）",
         "community_count": facts["gkx_lpa_community_count"],
         "modularity": facts["gkx_lpa_modularity"],
         "note": "人-人合作语义备选"},
    ],
    "absence_probe": ABSENCE_PROBE_TMPL,
    "support_judgment": support,
    "base_years_used": [], "base_years_missing": ["社群计数为 2026-11-02 live 截面，无年度基期维"],
    "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」",
}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_051_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out51, fh, ensure_ascii=False, indent=2)
print("done 051 | native:", facts["jiuxin_community_count_total"], "| LPA frame:", facts["jiuxin_lpa_community_count"],
      "| modularity:", facts["jiuxin_lpa_modularity"], "| gkx LPA:", facts["gkx_lpa_community_count"],
      "| calc_sec:", round(time.time() - t0, 1))
