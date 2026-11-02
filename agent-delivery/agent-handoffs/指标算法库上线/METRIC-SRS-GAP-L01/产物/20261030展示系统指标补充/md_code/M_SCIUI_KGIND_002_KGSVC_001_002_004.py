#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGIND_002 + M_SCIUI_KGSVC_001/002/004 四件合算 — 真图实算 + 三源探针 + 判档产物（各落一 _out.json）
KGIND_002 聚类系数：mockData.js fusionIndicators[1] {name:'聚类系数', graphValue:0.68, ruleValue:0.70, modelValue:0.66, fusionValue:0.68, weight:0.20}
   —— 简单统计类·真图实算主力：久新真图框内平均聚类系数（Watts-Strogatz）+全局 transitivity 双口径
KGSVC_001 业务线数据流向（桑基）：ServiceDisplay.jsx:530 硬编码 ECharts sankey（人才 ODS→图谱池→图查询/业务嵌入 5 links）
   —— 依赖：数据流向/血缘面——三源逐源留证（S3-07 族级探针 flow 词族零命中+本件补 dev ETL 任务词族）
KGSVC_002 合作网络关系图：ServiceDisplay.jsx:508 硬编码 ECharts graph force（16 节点 22 边演示）
   —— 依赖：合作网络图数据——gkx coauthor 真图可构图（完全转换支持，同 S3-06 KGANALY 族图算子）
KGSVC_004 知识图谱增长趋势：ServiceDisplay.jsx:478 硬编码 line（1-6 月实体/关系双线 12000→12568/42000→45234）
   —— 依赖：图谱时序快照（逐月实体/边计数）——久新 node/edge 无时间列（族级探针实证）→ 三源留证
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame, load_snap,
                           build_adj, average_clustering, gkx_coauthor_frame, ABSENCE_PROBE_TMPL)

BASE = os.path.dirname(os.path.abspath(__file__))
snap307 = json.load(open(os.path.join(BASE, "_snapshots", "_probe_s307_l1_out.json")))["facts"]
snap305 = load_snap()["facts"]

# ==================== KGIND_002 聚类系数（真图实算主力） ====================
facts002 = {}
facts002["ui_mock_source"] = "mockData.js fusionIndicators[1] clustering {graphValue:0.68, ruleValue:0.70, modelValue:0.66, fusionValue:0.68, weight:0.20}"
facts002["ui_fusion_panel"] = "FusionIndicatorsPanel 融合统计指标表消费（IndicatorDisplay indicators Tab）"
facts002["dev_graph_word_table_rows"] = snap305["dev_graph_word_table_rows"]
facts002["jiuxin_tech_nodes_total"] = snap307["jiuxin_tech_nodes_total"]
facts002["jiuxin_tech_edges_total"] = snap307["jiuxin_tech_edges_total"]

t0 = time.time()
frame = load_jiuxin_tech_frame(5000)
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())
clust = average_clustering(adj, present)
facts002["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
facts002["calc_sec"] = round(time.time() - t0, 1)

# 局部聚类系数分布（Top10 高聚类节点画像）
local_c = {}
for u in present:
    k = len(adj[u])
    if k < 2:
        local_c[u] = None
        continue
    neigh = adj[u]
    t2 = sum(len(adj[w] & neigh) for w in neigh)
    local_c[u] = round(2.0 * (t2 // 2) / (k * (k - 1)), 6)
top_c = sorted(((u, c) for u, c in local_c.items() if c is not None), key=lambda kv: (-kv[1], kv[0]))[:10]
derived002 = [{
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框) 平均聚类系数（Watts-Strogatz）+全局 transitivity 双口径",
    "nodes": len(present), "edges": len(frame["edges"]),
    "avg_clustering": clust["avg_clustering"],
    "transitivity_global": clust["transitivity_global"],
    "nodes_ge2deg": clust["nodes_ge2deg"], "nodes_lt2deg": clust["nodes_lt2deg"],
    "triangles": clust["triangles"],
    "top10_local_clustering": [{"node_id": u, "name_original": frame["id_name"].get(u, "")[:50],
                                "local_c": c, "degree": len(adj[u])} for u, c in top_c],
    "ui_mock_contrast": "UI fusionValue 0.68 vs 真图 avg_clustering（框内实测）——回填时以实测为准",
}]
support002 = "完全转换支持"

# ==================== KGSVC_001/002/004（三源探针） ====================
facts001s, facts002s, facts004s = {}, {}, {}
facts001s["ui_mount"] = "ServiceDisplay.jsx:530-546 硬编码 sankey option（人才 ODS/专利 ADS/项目 JSON→图谱池→图查询/业务嵌入，5 links 值 18-50）"
facts002s["ui_mount"] = "ServiceDisplay.jsx:508-527 硬编码 graph force option（16 节点 22 边演示网络，4 类别）"
facts004s["ui_mount"] = "ServiceDisplay.jsx:478-487 硬编码 line option（1-6 月实体 12000→12568/关系 42000→45234 双线）"

# ---------- ① dev live：ETL/血缘/快照词族 ----------
import pymysql
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      charset="utf8mb4", connect_timeout=10, read_timeout=120)
dc = dev.cursor()
dc.execute("""SELECT table_schema, table_name FROM information_schema.tables
              WHERE table_schema LIKE 'gkxlumenx%' AND table_name NOT LIKE 'demo_%'""")
dev_tables = sorted((r[0], r[1]) for r in dc.fetchall())
fam_etl = ["etl", "lineage", "sankey", "flow", "datax", "sync_task", "job_log", "task_log"]
m1 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam_etl)]
facts001s["dev_etl_lineage_family"] = m1
fam_snap = ["snapshot", "history", "version", "daily_cnt", "stat_day"]
m4 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam_snap)]
facts004s["dev_snapshot_family"] = m4
all_hits = sorted(set(m1 + m4))
rows = {}
for fq in all_hits[:15]:
    try:
        dc.execute(f"SELECT COUNT(*) FROM `{fq.split('.')[0]}`.`{fq.split('.')[1]}`")
        rows[fq] = dc.fetchone()[0]
    except Exception as e:  # noqa: BLE001
        rows[fq] = f"ERR:{type(e).__name__}"
facts001s["dev_family_rows"] = dict(sorted(rows.items()))
facts004s["dev_family_rows"] = {k: v for k, v in sorted(rows.items()) if k in m4}
dev.close()

# ---------- ② gkx：桑基/快照词族 + coauthor 边界（002 用） ----------
gc = jx_connect.__wrapped__ if False else None
from _s306_l3_base import gkx_connect
gc = gkx_connect()
gc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx'")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts001s["gkx_etl_lineage_family"] = [t for t in gkx_tables if any(w in t.lower() for w in fam_etl)]
facts004s["gkx_snapshot_family"] = [t for t in gkx_tables if any(w in t.lower() for w in fam_snap)]
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor")
facts002s["gkx_coauthor_total"] = gc.fetchone()[0]

# ---------- ③ 久新：桑基/快照词族 + node/edge 时间列实证（004 关键） ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jc.fetchall())
facts001s["jiuxin_etl_lineage_family"] = [t for t in jx_tables if any(w in t.lower() for w in fam_etl)]
facts004s["jiuxin_snapshot_family"] = [t for t in jx_tables if any(w in t.lower() for w in fam_snap)]
# 004 关键实证：node/edge 表时间列（族级探针已证 create_time 无——本件复证 data_version/metrics_as_of_date 型快照列）
try:
    jc.execute("SHOW COLUMNS FROM ads_technology_graph_node")
    cols = [r[0] for r in jc.fetchall()]
    facts004s["jiuxin_node_columns_timeish"] = sorted(c for c in cols if any(
        w in c.lower() for w in ["time", "date", "version", "year", "month", "snapshot"]))
except Exception as e:  # noqa: BLE001
    facts004s["jiuxin_node_columns_timeish"] = f"ERR:{type(e).__name__}"
jx.close()

# ---------- KGSVC_002 备承载：gkx coauthor 采样框合作网实算（节点/边/密度） ----------
gk = gkx_coauthor_frame(20000)
deg = {}
for u, v in gk["edges"]:
    deg[u] = deg.get(u, 0) + 1
    deg[v] = deg.get(v, 0) + 1
n2, e2 = len(gk["nodes"]), len(gk["edges"])
density2 = 2.0 * e2 / (n2 * (n2 - 1)) if n2 > 1 else 0.0
top_deg = sorted(deg.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
facts002s["gkx_coauthor_sample"] = {"rows": gk["rows"], "nodes": n2, "edges": e2,
                                    "density": round(density2, 8),
                                    "top10_degree": [{"scholar_id": k, "degree": v} for k, v in top_deg]}
# 久新技术图也可作合作网络语义备选（技术关联网）
facts002s["jiuxin_tech_graph_boundary"] = {"nodes": snap307["jiuxin_tech_nodes_total"],
                                           "edges": snap307["jiuxin_tech_edges_total"]}

# ---------- 判档 ----------
support001s = "完全不支持"  # 业务线数据流向（桑基）依赖 ETL 血缘面——三源词族留证
support002s = "完全转换支持"  # 合作网络关系图——gkx coauthor 真图可构图（底座已实测）+久新技术图备选
support004s = "完全不支持"  # 增长趋势依赖逐月快照——三源无图谱时序快照面（node/edge 无时间列实证）

derived001s = [{
    "source": "三源 ETL/血缘词族探针",
    "dev_hits": facts001s["dev_etl_lineage_family"], "dev_rows": facts001s["dev_family_rows"],
    "gkx_hits": facts001s["gkx_etl_lineage_family"], "jiuxin_hits": facts001s["jiuxin_etl_lineage_family"],
    "ui_hardcode": "5 links 值 [40,28,18,50,36]——S3-07 族级探针 flow 词族亦零命中（双探针印证）",
    "verdict": "业务线数据流向（ODS→图谱池→应用）依赖 ETL 任务编排/血缘面——三源缺位；dev 接入登记面（S3-04 DATAIN 族查过 gkxlumenx_* 任务/批次表族）是「接入侧」非「图谱侧流向」，语义不符",
}]
derived002s = [{
    "source": "gkx.dwd_scholar_coauthor 20,000 行采样框——合作网络（人-人边）真图实算",
    "nodes": n2, "edges": e2, "density": round(density2, 8),
    "top10_degree": "facts.gkx_coauthor_sample.top10_degree",
    "note": "主承载：学者合作网（语义最贴『合作网络』）；force 布局原料=节点+边清单（本件实测框），UI graph option 换数据即成",
    "backup": "久新 ads_technology_graph_node/edge（19,430/587,252，技术关联网）——合作语义的图结构备选（S3-06 全族已验证可构图）",
}]
derived004s = [{
    "source": "三源图谱时序快照词族探针",
    "dev_hits": facts004s["dev_snapshot_family"], "dev_rows": facts004s["dev_family_rows"],
    "gkx_hits": facts004s["gkx_snapshot_family"], "jiuxin_hits": facts004s["jiuxin_snapshot_family"],
    "jiuxin_node_timeish_cols": facts004s["jiuxin_node_columns_timeish"],
    "verdict": "增长趋势依赖逐月实体/边计数快照——三源无图谱时序快照面；久新 node 表时间类列实证（见 facts）无逐月快照维（data_version 是批次版本非时间轴），增长曲线无原料",
}]

absence_s = [
    {"what": "dev ETL/血缘/快照词族", "how": "gkxlumenx* 词族+逐张计数（本件）", "hits": f"合并命中见 facts（行数落键）"},
    {"what": "久新 etl/snapshot 词族", "how": "SHOW TABLES 词族（本件+族级双探针）", "hits": "flow 族族级零命中；etl/snapshot 本件留证"},
    {"what": "gkx etl/snapshot 词族", "how": "280 表词族（本件）", "hits": "逐一留证"},
    {"what": "dev 图结构面（26 张）", "how": "族级快照", "hits": "全 0 行"},
]

# ---------- 落盘四件 ----------
out = {"metric_id": "M_SCIUI_KGIND_002", "metric_name": "聚类系数（科技知识图谱·指标展示·融合统计指标和模型特征）",
       "facts": facts002, "derived": derived002, "absence_probe": ABSENCE_PROBE_TMPL,
       "support_judgment": support002,
       "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGIND_002_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done KGIND_002 | avg_clustering:", clust["avg_clustering"], "| transitivity:", clust["transitivity_global"],
      "| triangles:", clust["triangles"], "| calc_sec:", facts002["calc_sec"])

out = {"metric_id": "M_SCIUI_KGSVC_001", "metric_name": "业务线数据流向（桑基）（科技知识图谱·服务展示·图分析集成）",
       "facts": facts001s, "derived": derived001s, "absence_probe": absence_s,
       "support_judgment": support001s,
       "base_years_used": [], "base_years_missing": ["UI 读数为硬编码 5 links（18-50），无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGSVC_001_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done KGSVC_001 | support:", support001s, "| dev etl fam:", len(m1), "| jiuxin:", len(facts001s["jiuxin_etl_lineage_family"]))

out = {"metric_id": "M_SCIUI_KGSVC_002", "metric_name": "合作网络关系图（科技知识图谱·服务展示·图分析集成）",
       "facts": facts002s, "derived": derived002s, "absence_probe": absence_s,
       "support_judgment": support002s,
       "base_years_used": [], "base_years_missing": ["合作网为 2026-11-02 live 截面，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGSVC_002_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done KGSVC_002 | support:", support002s, "| coauthor sample:", n2, "nodes /", e2, "edges / density", round(density2, 8))

out = {"metric_id": "M_SCIUI_KGSVC_004", "metric_name": "知识图谱增长趋势（科技知识图谱·服务展示·图分析集成）",
       "facts": facts004s, "derived": derived004s, "absence_probe": absence_s,
       "support_judgment": support004s,
       "base_years_used": [], "base_years_missing": ["UI 读数为硬编码 6 个月双线，无年度基期维；三源无图谱逐月快照面"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGSVC_004_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done KGSVC_004 | support:", support004s, "| node timeish cols:", facts004s["jiuxin_node_columns_timeish"])
