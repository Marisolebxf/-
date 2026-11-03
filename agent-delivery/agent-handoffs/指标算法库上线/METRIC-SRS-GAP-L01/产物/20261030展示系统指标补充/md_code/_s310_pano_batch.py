#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-10 批（科学技术全景补立项）7 件三源探针 + 实算落产物
共享快照：_snapshots/_probe_s310_*.json（2026-11-02 当日实测）
每件独立输出 M_SCIUI_PANO_0x_out.json；support_judgment 按实测证据定档。
零 demo_*；久新 live 只读；gkx 经 _gkxdb.py；dev 引族级快照。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SN = os.path.join(BASE, "_snapshots")

def load(name):
    return json.load(open(os.path.join(SN, name)))

basic = load("_probe_s310_basic_out.json")       # 节点/边/路径/证据分布
pano = load("_probe_s310_pano_out.json")         # 三源词族 + 久新列质量
keypath = load("_probe_s310_keypath_out.json")   # 演化路径实算
keynode = load("_probe_s310_keynode_out.json")   # 关键节点口径实算
entity = load("_probe_s310_entity_out.json")     # 关键实体 Top5 + 社区/链角色
change = load("_probe_s310_change_out.json")     # 版本/发布单快照证据
s306 = load("_probe_s306_l1_out.json")           # 族级快照（dev 空壳/久新 218 表）

def base_years_note():
    return ("物理口径基期=图快照日（metrics_as_of_date=2026-10-16，graph_release_id=eto_mvp_cluster_chain_v1_20261016 单发布）；"
            "非年度基期，无「缺年按 0 摊入」情形")

def absence():
    return [
        {"what": "dev 现成图统计/路径/实体结果面", "how": "dev 图词族 26 张计数（S306 族级快照引用）",
         "hits": "全 0 行——结构在数据空"},
        {"what": "gkx 现成图统计结果面", "how": "gkx 词族扫描 graph_stat/key_path/centrality/entity_rank（S3-10 共享探针）",
         "hits": "0——coauthor 1,187,606 边可作备选推导，无现成结果行"},
        {"what": "久新现成对应指标行", "how": "久新 218 表词族 path/rank/stat/entity（S3-10 共享探针）",
         "hits": "表级词族命中 ads_technology_evolution_path_step 等，可转换实算（本件已实算）"},
    ]

def write(metric_id, name, facts, derived, support, extra=None):
    out = {"metric_id": metric_id, "metric_name": name,
           "facts": facts, "derived": derived, "absence_probe": absence(),
           "support_judgment": support,
           "base_years_used": [], "base_years_missing": [],
           "base_years_note": base_years_note()}
    if extra:
        out.update(extra)
    p = os.path.join(BASE, f"{metric_id}_out.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("done ->", metric_id, "| support:", support)
    return p

# ============ PANO-01 图谱节点总数 ============
f1 = {"ui_mount": "科学技术全景主视图·图谱统计卡「图谱节点」读数（App.jsx:5767 analysisContext.stats；graphInteractionState.js:273 演示值 1,148）",
      "jx_nodes": basic["nodes_total"], "jx_communities": basic["communities"], "jx_singleton": basic["singleton"],
      "jx_name_col_only_original": 19430, "jx_name_zh_null": 0,
      "dev_graph_tables_nonzero": {}, "gkx_fam_graph_stat_tables": pano["facts"]["gkx_fam_graph_stat_tables"]}
d1 = [{"source": "久新 ads_technology_graph_node COUNT(*)", "nodes_total": basic["nodes_total"],
       "denominator_note": "全表行数即节点总数（19,430），含 1,708 单点社区节点（口径披露：剔孤立=17,722）"}]
write("M_SCIUI_PANO_001", "图谱节点总数（科学技术全景·图谱统计卡）", f1, d1, "完全转换支持")

# ============ PANO-02 关联关系总数 ============
f2 = {"ui_mount": "科学技术全景主视图·图谱统计卡「关联关系」读数（graphInteractionState.js:274 演示值 1,722）",
      "jx_edges": basic["edges_total"], "edges_high": basic["edges_high"], "edges_medium": basic["edges_medium"],
      "edges_low": basic["edges_low"], "edge_direction": s306["facts"].get("jiuxin_edge_direction_dist"),
      "reltype": change["reltype"]}
d2 = [{"source": "久新 ads_technology_graph_edge COUNT(*)", "edges_total": basic["edges_total"],
       "denominator_note": "全边表行数（587,252，含方向重复边——WEAK_DEPENDENCY 257,347 为最大族）"},
      {"source": "高置信边占比", "high_conf_ratio_pct": round(basic["edges_high"]/basic["edges_total"]*100, 2),
       "denominator_note": f"HIGH 边 {basic['edges_high']} / 全边 {basic['edges_total']}×100"}]
write("M_SCIUI_PANO_002", "关联关系总数（科学技术全景·图谱统计卡）", f2, d2, "完全转换支持")

# ============ PANO-03 关键节点数 ============
f3 = {"ui_mount": "科学技术全景主视图·图谱统计卡「关键节点」读数（graphInteractionState.js:275 演示值 114；领域下钻 42/36/31）",
      "core_role_count": keynode["core_role_count"], "wd_ge100": keynode["wd_ge100"], "wd_ge50": keynode["wd_ge50"],
      "pos_quantiles": keynode["pos_quantiles"], "core_by_comm_top5": keynode["core_by_comm_top5"]}
d3 = [{"source": "口径A：community_role=CORE 计数", "count": keynode["core_role_count"],
       "denominator_note": "图内置角色判定（CORE 3,495/19,430）"},
      {"source": "口径B：weighted_degree>=100 阈值计数", "count": keynode["wd_ge100"],
       "denominator_note": "阈值 100 ≈ 全图 Top1% 分位（102.65，S310 keynode 快照）"},
      {"source": "口径C：Top1% 分位法", "count": 177,
       "denominator_note": "17,722 正度数节点×1%≈177（分位数 102.64831551）"}]
write("M_SCIUI_PANO_003", "关键节点数（科学技术全景·图谱统计卡）", f3, d3, "完全转换支持")

# ============ PANO-04 关键路径数 ============
f4 = {"ui_mount": "科学技术全景主视图·图谱统计卡「关键路径」读数（graphInteractionState.js:276 演示值 28；关键路径 Tab 列表）",
      "paths": keypath["paths"], "steps": keypath["steps"], "avg_len": keypath["avg_len"],
      "max_len": keypath["max_len"], "min_len": keypath["min_len"], "by_method": keypath["by_method"],
      "len_dist": keypath["len_dist"], "truncated_paths": keypath["truncated_paths"],
      "score_nonnull_avg": 63.5676, "score_min": 55.463582, "score_max": 96.0}
d4 = [{"source": "久新 ads_technology_evolution_path_step COUNT(DISTINCT path_id)", "path_count": keypath["paths"],
       "denominator_note": "47,909 步聚合为 12,891 条路径（每路径 step 2–8）"},
      {"source": "平均路径长度", "avg_len": keypath["avg_len"],
       "denominator_note": "Σpath_length/路径数 12,891（按步级 path_length 均值，库内预计算列）"}]
write("M_SCIUI_PANO_004", "关键路径数（科学技术全景·图谱统计卡）", f4, d4, "完全转换支持")

# ============ PANO-05 关键实体Top5关联强度 ============
f5 = {"ui_mount": "科学技术全景·关键实体Tab「关键关联对象 Top5」（App.jsx:5789 chart-title；边权归一化排序）",
      "top5_norm": entity["top5_norm"], "top_communities": entity["top_communities"],
      "chainrole_wd": entity["chainrole_wd"], "core_nodes": entity["core_nodes"]}
d5 = [{"source": "Top1 归一化关联强度", "name": entity["top5_norm"][0]["name"],
       "weighted_degree": entity["top5_norm"][0]["weighted_degree"],
       "norm_strength_pct": entity["top5_norm"][0]["norm_strength"],
       "denominator_note": "weighted_degree/max(weighted_degree)×100——max=1010.90780192"},
      {"source": "Top5 全列表（具名）", "names": [t["name"] for t in entity["top5_norm"]],
       "denominator_note": "ORDER BY weighted_degree DESC 排序固定（并列按 node_id ASC）"}]
write("M_SCIUI_PANO_005", "关键实体Top5关联强度（科学技术全景·关键实体Tab）", f5, d5, "完全转换支持")

# ============ PANO-06 图谱关系变化监测 ============
f6 = {"ui_mount": "科学技术全景·研判区「关系变化类型」卡：新增32/增强18/引用链9（graphInteractionState.js:283-286 演示值；SRS 序号22 支持按时间轴显示）",
      "graph_release_dist": change["release_dist"], "data_version_dist": change["data_version_dist"],
      "asof_dist": change["asof_dist"], "reltype_now": change["reltype"],
      "path_step_year": entity["path_step_year"], "year_span": entity["year_span"]}
d6 = [{"source": "单快照事实", "release_count": 1, "snapshot_date": "2026-10-16",
       "denominator_note": "graph_release_id 全表单值——差分监测需 ≥2 期快照，现仅 1 期"},
      {"source": "代理口径：边首证年代分布（2019+ vs <2019）", "steps_2019plus": entity["path_step_year"][1][1],
       "steps_before2019": entity["path_step_year"][0][1],
       "denominator_note": "edge_first_evidence_year 年代二分——期内增量代理（非两期快照差分）"}]
write("M_SCIUI_PANO_006", "图谱关系变化监测（科学技术全景·时间轴变化卡）", f6, d6, "部分支持")

# ============ PANO-07 图谱研判结论 ============
f7 = {"ui_mount": "科学技术全景·图谱研判卡（App.jsx:5740-5758 口径/范围/判断三字段；演示文案「节点↑关系↑路径↓收敛趋势」）",
      "judgement_inputs": basic["judgement_inputs"], "nodes": basic["nodes_total"], "edges": basic["edges_total"],
      "paths": keypath["paths"], "trend_evidence": "单快照无两期差分，趋势方向不可实证", "phase_dist": entity.get("phase_observed")}
d7 = [{"source": "研判输入三数（即期可算部分）", "nodes": basic["nodes_total"], "edges": basic["edges_total"],
       "paths": keypath["paths"], "denominator_note": "三输入行分别来自节点/边/路径表 COUNT——研判卡数值位可即期回填"},
      {"source": "趋势方向位（缺两期差分）", "trend": "na",
       "denominator_note": "上升/下降判定需两期对比，当前单期——文本研判位暂不可实证"}]
write("M_SCIUI_PANO_007", "图谱研判结论（科学技术全景·研判卡）", f7, d7, "部分支持")

# ============ PANO-08 图谱数据导入规模 ============
f8 = {"ui_mount": "科学技术全景·图谱数据导入（App.jsx:7213 提示「已导入 N 个节点、M 条关系」；SRS 序号17）",
      "ui_demo_only": True, "note": "UI 导入为会话级 Mock（演示图 15 节点），后端无导入落库面"}
d8 = []
write("M_SCIUI_PANO_008", "图谱数据导入规模（科学技术全景·维护技术图谱）", f8, d8, "不适用（UI 功能运行态，非业务统计指标）")

print("\nS3-10 共 8 件 out.json 落盘完成")
