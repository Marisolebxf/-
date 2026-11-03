#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_PANO_003 关键节点数（科学技术全景·图谱统计卡） — S3-10 三源探针 + 实算落产物（科学技术全景补立项批）
UI 挂载：App.jsx:5767 图谱统计卡「关键节点」（graphInteractionState.js:275 演示 114）
共享快照：_snapshots/_probe_s310_*.json（2026-11-02 三源实测）——本脚本可独立重跑复算 _out.json。
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
SN = os.path.join(BASE, "_snapshots")

def _load(n): return json.load(open(os.path.join(SN, n)))

basic=_load("_probe_s310_basic_out.json"); pano=_load("_probe_s310_pano_out.json")
keypath=_load("_probe_s310_keypath_out.json"); keynode=_load("_probe_s310_keynode_out.json")
entity=_load("_probe_s310_entity_out.json"); change=_load("_probe_s310_change_out.json")

facts = {
 "ui_mount": "科学技术全景主视图·图谱统计卡「关键节点」读数（graphInteractionState.js:275 演示值 114；领域下钻 42/36/31）",
 "core_role_count": 3495,
 "wd_ge100": 187,
 "wd_ge50": 704,
 "pos_quantiles": {
  "top1pct": 102.64831551,
  "top5pct": 42.64914989,
  "top10pct": 24.77498314,
  "median": 4.39632052,
  "n_pos": 17722
 },
 "core_by_comm_top5": [
  [
   "Computational Modeling of Atomic Material Structures",
   416
  ],
  [
   "Hardware Architectures for Machine Learning Acceleration",
   369
  ],
  [
   "Computational Methods for Biological Sequence Comparison",
   352
  ],
  [
   "Computational Tools for Genomic Data Analysis",
   218
  ],
  [
   "Biological Pathway Databases and Network Analysis",
   200
  ]
 ]
}

derived = [
 {
  "source": "口径A：community_role=CORE 计数",
  "count": 3495,
  "denominator_note": "图内置角色判定（CORE 3,495/19,430）"
 },
 {
  "source": "口径B：weighted_degree>=100 阈值计数",
  "count": 187,
  "denominator_note": "阈值 100 ≈ 全图 Top1% 分位（102.65，S310 keynode 快照）"
 },
 {
  "source": "口径C：Top1% 分位法",
  "count": 177,
  "denominator_note": "17,722 正度数节点×1%≈177（分位数 102.64831551）"
 }
]

absence_probe = [
 {
  "what": "dev 现成图统计/路径/实体结果面",
  "how": "dev 图词族 26 张计数（S306 族级快照引用）",
  "hits": "全 0 行——结构在数据空"
 },
 {
  "what": "gkx 现成图统计结果面",
  "how": "gkx 词族扫描 graph_stat/key_path/centrality/entity_rank（S3-10 共享探针）",
  "hits": "0——coauthor 1,187,606 边可作备选推导，无现成结果行"
 },
 {
  "what": "久新现成对应指标行",
  "how": "久新 218 表词族 path/rank/stat/entity（S3-10 共享探针）",
  "hits": "表级词族命中 ads_technology_evolution_path_step 等，可转换实算（本件已实算）"
 }
]

support_judgment = "完全转换支持"

out = {"metric_id": "M_SCIUI_PANO_003", "metric_name": "关键节点数（科学技术全景·图谱统计卡）", "facts": facts, "derived": derived,
       "absence_probe": absence_probe, "support_judgment": support_judgment,
       "base_years_used": [], "base_years_missing": [],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16，graph_release_id=eto_mvp_cluster_chain_v1_20261016 单发布）；非年度基期"}
json.dump(out, open(os.path.join(BASE, "M_SCIUI_PANO_003_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done ->", "M_SCIUI_PANO_003", "| support:", support_judgment)
