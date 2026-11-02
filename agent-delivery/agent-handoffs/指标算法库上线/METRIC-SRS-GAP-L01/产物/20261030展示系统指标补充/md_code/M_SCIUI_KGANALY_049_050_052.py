#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_049/050/052 尾三件合算 — 三源探针 + 真图实算 + 判档产物（三件各落一 _out.json）
049 图谱综合得分：CentralityPanel.jsx:599 compare Tab「综合分」（centralityAlgo.js 四维加权 normalize 0-1 composite）
   —— 算法：度/紧密/中介/PR 四维 min-max 归一后加权（UI weights 默认各 25%；Brandes+全源 BFS 框内实算）
050 图谱合作强度（合作边权重）：queryAssetDeepAnalysis.js:88 bars 图 x 轴首项「合作强度」（mock 85 递减）
   —— 语义：合作边权重统计；主承载久新边表 relation_confidence_score（27.08-100）/total_citation_count（0-142）
      + gkx co_paper_count（1-1062）真合作强度列
052 跨领域关系边占比：queryAssetDeepAnalysis.js:53 metrics「跨域边占比」（seededInt 18-42% mock）
   —— 算法：久新全图边两端 community_id 异同计数（已实测 cross=205,023/587,252=34.9123%——本件独立复算+产物落键）
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame, load_snap,
                           build_adj, composite_score_centrality, gkx_coauthor_frame,
                           ABSENCE_PROBE_TMPL)

BASE = os.path.dirname(os.path.abspath(__file__))
snap = load_snap()["facts"]
facts = {}
facts["dev_graph_word_table_rows"] = snap["dev_graph_word_table_rows"]

# ---------- ① 久新 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_tech_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_tech_edges_total"] = jc.fetchone()[0]

# 050 主承载：边权重列分布（confidence/citation）
jc.execute("""SELECT MIN(relation_confidence_score), MAX(relation_confidence_score),
              AVG(relation_confidence_score) FROM ads_technology_graph_edge""")
r = jc.fetchone()
facts["jiuxin_edge_confidence_min_max_avg"] = [float(r[0]), float(r[1]), round(float(r[2]), 6)]
jc.execute("""SELECT MIN(total_citation_count), MAX(total_citation_count), AVG(total_citation_count)
              FROM ads_technology_graph_edge""")
r = jc.fetchone()
facts["jiuxin_edge_citation_min_max_avg"] = [int(r[0]), int(r[1]), round(float(r[2]), 3)]
# 分桶分布（合作强度画像）
jc.execute("""SELECT CASE WHEN relation_confidence_score>=80 THEN 'c80_100'
             WHEN relation_confidence_score>=60 THEN 'c60_80'
             WHEN relation_confidence_score>=40 THEN 'c40_60' ELSE 'c0_40' END b, COUNT(*)
             FROM ads_technology_graph_edge GROUP BY b""")
facts["jiuxin_edge_confidence_buckets"] = dict(sorted((r[0], r[1]) for r in jc.fetchall()))
jc.execute("""SELECT CASE WHEN total_citation_count>=10 THEN 'cit10_plus'
             WHEN total_citation_count>=3 THEN 'cit3_10'
             WHEN total_citation_count>=1 THEN 'cit1_3' ELSE 'cit0' END b, COUNT(*)
             FROM ads_technology_graph_edge GROUP BY b""")
facts["jiuxin_edge_citation_buckets"] = dict(sorted((r[0], r[1]) for r in jc.fetchall()))
# 权重 Top10 边（具名样例：两端节点名）
jc.execute("""SELECT e.source_technology_node_id, e.target_technology_node_id,
              e.relation_confidence_score, e.total_citation_count
              FROM ads_technology_graph_edge e
              ORDER BY e.relation_confidence_score DESC, e.total_citation_count DESC
              LIMIT 10""")
top_edges = jc.fetchall()
jc.execute("SELECT technology_node_id, technology_name_original FROM ads_technology_graph_node")
id_name = {r[0]: (r[1] or "") for r in jc.fetchall()}
facts["jiuxin_top10_edges_by_confidence"] = [
    {"source_id": s, "target_id": t, "source_name": id_name.get(s, "")[:60],
     "target_name": id_name.get(t, "")[:60], "confidence": float(c), "citations": int(ct)}
    for s, t, c, ct in top_edges]

# 052 主承载：全图跨社群边（node 端点 community 映射本地配对——无 join 版）
jc.execute("SELECT technology_node_id, community_id FROM ads_technology_graph_node")
cid = dict(jc.fetchall())
jc.execute("SELECT source_technology_node_id, target_technology_node_id FROM ads_technology_graph_edge")
intra = cross = unmatched = 0
cross_edges_sample = []
for s, t in jc.fetchall():
    cs, ct = cid.get(s), cid.get(t)
    if cs is None or ct is None:
        unmatched += 1
    elif cs == ct:
        intra += 1
    else:
        cross += 1
        if len(cross_edges_sample) < 5:
            cross_edges_sample.append((s, t))
facts["jiuxin_cross_comm_edges"] = cross
facts["jiuxin_intra_comm_edges"] = intra
facts["jiuxin_edge_endpoint_unmatched"] = unmatched
jx.close()

# ---------- 049 主承载：框内四维中心性综合分（Brandes+BFS+PR 一次算） ----------
t0 = time.time()
frame = load_jiuxin_tech_frame(5000)
facts["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())
comp = composite_score_centrality(adj, present)
facts["jiuxin_composite_weights"] = {"degree": 0.25, "closeness": 0.25, "betweenness": 0.25, "pagerank": 0.25}
facts["jiuxin_composite_pagerank_iters"] = comp["pagerank_iters"]
facts["jiuxin_composite_pagerank_final_diff"] = comp["pagerank_final_diff"]
top10_comp = sorted(comp["composite"].items(), key=lambda kv: (-kv[1], kv[0]))[:10]
derived49 = {
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框) 四维中心性综合分",
    "nodes": len(present), "edges": len(frame["edges"]),
    "weights": facts["jiuxin_composite_weights"],
    "composite_top10": [{"node_id": k, "name_original": frame["id_name"].get(k, "")[:60],
                         "composite": v,
                         "degree_raw": comp["degree"][k],
                         "closeness": comp["closeness"][k],
                         "betweenness": comp["betweenness"][k],
                         "pagerank": comp["pagerank"][k]} for k, v in top10_comp],
    "composite_distribution": {
        "min": min(comp["composite"].values()), "max": max(comp["composite"].values()),
        "mean": round(sum(comp["composite"].values()) / len(comp["composite"]), 6)},
}

# ---------- 050 gkx 备承载：co_paper_count 真合作强度 ----------
gk = gkx_coauthor_frame(20000)
gc_weights = [gk["edge_weights"][e] for e in gk["edges"]]
facts["gkx_coauthor_sample_edges"] = len(gk["edges"])
facts["gkx_co_paper_count_min_max_avg"] = [min(gc_weights), max(gc_weights),
                                           round(sum(gc_weights) / len(gc_weights), 4)]
facts["gkx_co_paper_count_ge2_edges"] = sum(1 for w in gc_weights if w >= 2)
facts["gkx_top10_edges_by_co_paper"] = sorted(
    ({"source": u, "target": v, "co_paper_count": w} for (u, v), w in gk["edge_weights"].items()),
    key=lambda d: (-d["co_paper_count"], d["source"], d["target"]))[:10]

support = "完全转换支持"

# ---------- 049 产物 ----------
out49 = {"metric_id": "M_SCIUI_KGANALY_049", "metric_name": "图谱综合得分（知识图谱·中心性计算展示·多维度综合分析）",
         "facts": facts,
         "derived": [derived49],
         "absence_probe": ABSENCE_PROBE_TMPL, "support_judgment": support,
         "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
         "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_049_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out49, fh, ensure_ascii=False, indent=2)
print("done 049 | top1 composite:", derived49["composite_top10"][0]["composite"],
      "| dist:", derived49["composite_distribution"], "| calc_sec:", round(time.time() - t0, 1))

# ---------- 050 产物 ----------
out50 = {"metric_id": "M_SCIUI_KGANALY_050", "metric_name": "图谱合作强度（合作边权重）（图查询资产·深入分析）",
         "facts": facts,
         "derived": [
             {"source": "jiuxin.ads_technology_graph_edge relation_confidence_score（技术关联强度，全图）",
              "edges": facts["jiuxin_tech_edges_total"],
              "min_max_avg": facts["jiuxin_edge_confidence_min_max_avg"],
              "buckets": facts["jiuxin_edge_confidence_buckets"],
              "top10_edges": "facts.jiuxin_top10_edges_by_confidence（具名样例）",
              "note": "主口径：关系置信度（27.08-100，均值 49.02）——技术关联强度画像"},
             {"source": "jiuxin.ads_technology_graph_edge total_citation_count（引用计数强度，全图）",
              "edges": facts["jiuxin_tech_edges_total"],
              "min_max_avg": facts["jiuxin_edge_citation_min_max_avg"],
              "buckets": facts["jiuxin_edge_citation_buckets"],
              "note": "并列口径：引用计数（0-142，均值 1.168）——证据量强度"},
             {"source": "gkx.dwd_scholar_coauthor co_paper_count（真·合作强度=合著论文数，采样框）",
              "edges": facts["gkx_coauthor_sample_edges"],
              "min_max_avg": facts["gkx_co_paper_count_min_max_avg"],
              "ge2_edges": facts["gkx_co_paper_count_ge2_edges"],
              "top10_edges": "facts.gkx_top10_edges_by_co_paper",
              "note": "备承载（语义最贴合『合作』）：合著论文数 1-1062，框内 ≥2 篇边数落键"},
         ],
         "absence_probe": ABSENCE_PROBE_TMPL, "support_judgment": support,
         "base_years_used": [], "base_years_missing": ["边权重为 2026-11-02 live 截面，无年度基期维"],
         "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_050_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out50, fh, ensure_ascii=False, indent=2)
print("done 050 | conf avg:", facts["jiuxin_edge_confidence_min_max_avg"][2],
      "| gkx co_paper avg:", facts["gkx_co_paper_count_min_max_avg"][2])

# ---------- 052 产物 ----------
total_edges = facts["jiuxin_cross_comm_edges"] + facts["jiuxin_intra_comm_edges"] + facts["jiuxin_edge_endpoint_unmatched"]
cross_ratio = round(facts["jiuxin_cross_comm_edges"] / total_edges * 100, 6)
out52 = {"metric_id": "M_SCIUI_KGANALY_052", "metric_name": "跨领域关系边占比（图查询资产·深入分析·结构指标）",
         "facts": facts,
         "derived": [
             {"source": "jiuxin 全图边×community_id 配对（无 join 本地配对，B5 sorted）",
              "total_edges": total_edges,
              "cross_edges": facts["jiuxin_cross_comm_edges"],
              "intra_edges": facts["jiuxin_intra_comm_edges"],
              "unmatched": facts["jiuxin_edge_endpoint_unmatched"],
              "cross_ratio_pct": cross_ratio,
              "numerator": facts["jiuxin_cross_comm_edges"],
              "denominator": total_edges,
              "denominator_note": "分母=全图总边数（587,252）＝跨+同+未配对；分子=两端 community_id 不同的边",
              "note": "主口径：全图社群维跨域占比 34.9123%（单例社群也计入跨域——口径披露见 MD §2.2）"},
         ],
         "absence_probe": ABSENCE_PROBE_TMPL, "support_judgment": support,
         "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
         "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_052_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out52, fh, ensure_ascii=False, indent=2)
print("done 052 | cross:", facts["jiuxin_cross_comm_edges"], "/", total_edges, "=", cross_ratio, "%")
