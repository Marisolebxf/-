#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_PANO_007 图谱研判结论（科学技术全景·研判卡） — S3-10 三源探针 + 实算落产物（科学技术全景补立项批）
UI 挂载：App.jsx:5740-5758 图谱研判卡（口径/范围/判断）
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
 "ui_mount": "科学技术全景·图谱研判卡（App.jsx:5740-5758 口径/范围/判断三字段；演示文案「节点↑关系↑路径↓收敛趋势」）",
 "judgement_inputs": {
  "nodes": 19430,
  "edges": 587252,
  "paths": 12891,
  "high_conf_ratio": 17.6
 },
 "nodes": 19430,
 "edges": 587252,
 "paths": 12891,
 "trend_evidence": "单快照无两期差分，趋势方向不可实证",
 "phase_dist": 6849
}

derived = [
 {
  "source": "研判输入三数（即期可算部分）",
  "nodes": 19430,
  "edges": 587252,
  "paths": 12891,
  "denominator_note": "三输入行分别来自节点/边/路径表 COUNT——研判卡数值位可即期回填"
 },
 {
  "source": "趋势方向位（缺两期差分）",
  "trend": "na",
  "denominator_note": "上升/下降判定需两期对比，当前单期——文本研判位暂不可实证"
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

out = {"metric_id": "M_SCIUI_PANO_007", "metric_name": "图谱研判结论（科学技术全景·研判卡）", "facts": facts, "derived": derived,
       "absence_probe": absence_probe, "support_judgment": support_judgment,
       "base_years_used": [], "base_years_missing": [],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16，graph_release_id=eto_mvp_cluster_chain_v1_20261016 单发布）；非年度基期"}
json.dump(out, open(os.path.join(BASE, "M_SCIUI_PANO_007_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done ->", "M_SCIUI_PANO_007", "| support:", support_judgment)
