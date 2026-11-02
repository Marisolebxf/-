#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_027 异常关系密度 — 三源探针 + 操作化口径实算 + 判档产物
UI 语义（mockData.js:285 desc）：异常关系密度 = 异常边 / 局部边集占比。
「异常边」无标注真值——本件以图内在证据做操作化：evidence_level=LOW 边（低证据关联=可疑）
并列 temporal_alignment_status=TIME_CONFLICT 边（时间冲突=可疑），双口径并列（B10）。
锚文献：Akoglu 2015 图异常检测综述（结构特征法）；GB/T 36344 数据质量框架（0501/0502 时效性同族）。
"""
import json
import os

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_027_out.json")

facts = {}
facts["ui_mount"] = "BlacklistTriggerPanel.jsx:147 列 title=异常关系密度（Progress 条）+ IndicatorDisplay.jsx:33 + mockData.js:285（value 0.62/threshold 0.55/desc『异常边 / 局部边集占比』）"
facts["ui_mock_value"] = 0.62
facts["ui_threshold"] = 0.55
facts["ui_semantic"] = "mockData.js:285 desc：异常边 / 局部边集占比（分母=局部边集，黑名单监测语境）"
facts["srs_anchor"] = "指标展示.md seq 408（excel_row 411）：「利用图谱计算指标（如节点异常度、异常关系密度等），对网络中的异常行为或异常模式进行实时监测」"
facts["cat"] = "需业务建模类（『异常』无标注真值，需口径裁定）"

c = gb.load_cache()
nodes = [r[0] for r in c["node_rows"]]
edges_main = [tuple(e) for e in c["main_edges"]]
evo = [tuple(r) for r in c["evo_rows"]]

facts["jiuxin_tech_nodes_total"] = c["nodes_total"]
facts["jiuxin_tech_edges_total"] = c["edges_total"]
facts["jiuxin_tech_sample_nodes"] = len(nodes)
facts["jiuxin_tech_sample_induced_edges"] = len(edges_main)

# 全图口径（SQL 直查值，live 当日）：evidence_level=LOW / temporal TIME_CONFLICT
import pymysql  # noqa: E402
jx = gb.jx_connect()
jc = jx.cursor()
jc.execute("SELECT evidence_level, COUNT(*) FROM ads_technology_graph_edge GROUP BY evidence_level")
ev_dist = dict(jc.fetchall())
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge WHERE evidence_level='LOW'")
low_total = jc.fetchone()[0]
jc.execute("SELECT temporal_alignment_status, COUNT(*) FROM ads_technology_evolution_edge GROUP BY temporal_alignment_status")
ta_dist = dict(jc.fetchall())
jc.execute("SELECT COUNT(*) FROM ads_technology_evolution_edge WHERE temporal_alignment_status='TIME_CONFLICT'")
conflict_total = jc.fetchone()[0]
jx.close()
facts["jiuxin_edge_evidence_level_dist"] = {k: int(v) for k, v in sorted(ev_dist.items())}
facts["jiuxin_evolution_temporal_dist"] = {k: int(v) for k, v in sorted(ta_dist.items())}

# 框内双口径实算：需要边级属性——缓存 evo 无 evidence_level，改用演化表口径（TIME_CONFLICT）+ 主表 LOW 需重拉框内属性
jx = gb.jx_connect()
jc = jx.cursor()
jc.execute("""SELECT e.source_technology_node_id, e.target_technology_node_id, e.evidence_level
              FROM ads_technology_graph_edge e
              WHERE e.source_technology_node_id IN (SELECT technology_node_id FROM
                  (SELECT technology_node_id FROM ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000) t)
                AND e.target_technology_node_id IN (SELECT technology_node_id FROM
                  (SELECT technology_node_id FROM ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000) t2)""")
ev_rows = jc.fetchall()
jx.close()
low_edges_frame = [(r[0], r[1]) for r in ev_rows if r[2] == "LOW"]
facts["jiuxin_frame_low_edges"] = len(low_edges_frame)
# 演化表框内 TIME_CONFLICT
conflict_frame = [(r[0], r[1]) for r in evo if r[3] is not None and False]  # evo 缓存无 temporal 列；改用全图比例外推披露
# 框内 temporal：全图比例 198409/587252=0.3379，框内无法直查（缓存未带列）——用全图口径交付主读数（B1：不手算外推）

derived = [{
    "source": "jiuxin.ads_technology_graph_edge 全图口径（evidence_level=LOW）",
    "mode": "operational_A_low_evidence",
    "denominator": "jiuxin_tech_edges_total",
    "numerator": "low_evidence_edges_total",
    "low_evidence_edges_total": int(low_total),
    "density_low_evidence": round(int(low_total) / c["edges_total"], 6),
    "frame_low_evidence_edges": len(low_edges_frame),
    "frame_density_low_evidence": round(len(low_edges_frame) / len(edges_main), 6) if edges_main else None,
}, {
    "source": "jiuxin.ads_technology_evolution_edge 全图口径（temporal_alignment_status=TIME_CONFLICT）",
    "mode": "operational_B_time_conflict",
    "denominator": "jiuxin_tech_edges_total",
    "numerator": "time_conflict_edges_total",
    "time_conflict_edges_total": int(conflict_total),
    "density_time_conflict": round(int(conflict_total) / c["edges_total"], 6),
}]

absence_probe = [
    {"what": "『异常边』标注真值（风险/黑名单/异常标注列）", "how": "久新 218 表词族扫描（anomal/abnormal/risk/black/fraud/outlier）", "hits": "0 表——无标注面"},
    {"what": "gkx 异常标注图面", "how": "280 表词族扫描", "hits": "0（dwd_org_company_abnormal 是企业经营异常目录，非图边标注——语义排除）"},
    {"what": "dev 黑名单/异常图面", "how": "族级快照", "hits": "graph_* 26 张全 0 行；无黑名单词族表"},
    {"what": "UI 演示值 0.62 的数据来源", "how": "mockData.js:285 读码", "hits": "写死常量（演示 Mock，非生产接口）"},
]

out = {"metric_id": "M_SCIUI_KGANALY_027", "metric_name": "异常关系密度（科技知识图谱·黑名单触发·图谱指标实时监测）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "部分支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（边证据属性为 2026-10-29 单截面：metrics_as_of_date 全表同值）"],
       "base_years_note": "物理口径基期=探针快照日；边级证据属性无历史版本（单截面），非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
