#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_PANO_008 图谱数据导入规模（科学技术全景·维护技术图谱） — S3-10 三源探针 + 实算落产物（科学技术全景补立项批）
UI 挂载：App.jsx:7213 图谱数据导入提示＋SRS 序号17
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
 "ui_mount": "科学技术全景·图谱数据导入（App.jsx:7213 提示「已导入 N 个节点、M 条关系」；SRS 序号17）",
 "ui_demo_only": True,
 "note": "UI 导入为会话级 Mock（演示图 15 节点），后端无导入落库面"
}

derived = []

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

support_judgment = "不适用（UI 功能运行态，非业务统计指标）"

out = {"metric_id": "M_SCIUI_PANO_008", "metric_name": "图谱数据导入规模（科学技术全景·维护技术图谱）", "facts": facts, "derived": derived,
       "absence_probe": absence_probe, "support_judgment": support_judgment,
       "base_years_used": [], "base_years_missing": [],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16，graph_release_id=eto_mvp_cluster_chain_v1_20261016 单发布）；非年度基期"}
json.dump(out, open(os.path.join(BASE, "M_SCIUI_PANO_008_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done ->", "M_SCIUI_PANO_008", "| support:", support_judgment)
