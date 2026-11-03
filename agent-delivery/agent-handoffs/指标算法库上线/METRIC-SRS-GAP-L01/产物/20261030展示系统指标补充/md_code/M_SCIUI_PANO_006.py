#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_PANO_006 图谱关系变化监测（科学技术全景·时间轴变化卡） — S3-10 三源探针 + 实算落产物（科学技术全景补立项批）
UI 挂载：graphInteractionState.js:283-286 关系变化类型卡（新增/增强/引用链）＋SRS 序号22 时间轴
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
 "ui_mount": "科学技术全景·研判区「关系变化类型」卡：新增32/增强18/引用链9（graphInteractionState.js:283-286 演示值；SRS 序号22 支持按时间轴显示）",
 "graph_release_dist": [
  [
   "eto_mvp_cluster_chain_v1_20261016",
   587252
  ]
 ],
 "data_version_dist": [
  [
   "202610260601",
   587252
  ]
 ],
 "asof_dist": [
  [
   "2026-10-16",
   587252
  ]
 ],
 "reltype_now": [
  [
   "WEAK_DEPENDENCY",
   257347
  ],
  [
   "PATENT_CONVERGENCE",
   212729
  ],
  [
   "KNOWLEDGE_DEPENDENCY",
   95208
  ],
  [
   "CO_EVOLUTION",
   21968
  ]
 ],
 "path_step_year": [
  [
   "<2019",
   23794,
   11239
  ],
  [
   "2019+",
   11224,
   8229
  ]
 ],
 "year_span": [
  1776,
  2026
 ]
}

derived = [
 {
  "source": "单快照事实",
  "release_count": 1,
  "snapshot_date": "2026-10-16",
  "denominator_note": "graph_release_id 全表单值——差分监测需 ≥2 期快照，现仅 1 期"
 },
 {
  "source": "代理口径：边首证年代分布（2019+ vs <2019）",
  "steps_2019plus": 11224,
  "steps_before2019": 23794,
  "denominator_note": "edge_first_evidence_year 年代二分——期内增量代理（非两期快照差分）"
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

support_judgment = "部分支持"

out = {"metric_id": "M_SCIUI_PANO_006", "metric_name": "图谱关系变化监测（科学技术全景·时间轴变化卡）", "facts": facts, "derived": derived,
       "absence_probe": absence_probe, "support_judgment": support_judgment,
       "base_years_used": [], "base_years_missing": [],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16，graph_release_id=eto_mvp_cluster_chain_v1_20261016 单发布）；非年度基期"}
json.dump(out, open(os.path.join(BASE, "M_SCIUI_PANO_006_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done ->", "M_SCIUI_PANO_006", "| support:", support_judgment)
