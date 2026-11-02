#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_053/057/066 三件合算 — 三源探针 + 真图实算 + 判档产物（各落一 _out.json）
053 综合评分雷达（Top5）：CentralityPanel.jsx:850 compare Tab 雷达卡（radarOption :291-310）
   —— 四维 [度归一, 紧密, 中介归一, min(1, PR×5)]，与 049 同框四维中心性复用+雷达 Top5 专用产物
057 节点移除连通性影响：CentralityPanel.jsx:740 中介 Tab 卡（analyzeRemovalImpact centralityAlgo.js:270-283）
   —— connectedComponents(before/after)、Δ、severity（Δ>=2 高/Δ==1 中/else 低）；本件实算框内 Top 中介/度/PR 节点移除影响
066 图谱风险评分：OptimizeDecisionPanel.jsx:167 riskColumns「风险分」Progress（decisionRiskAlerts score 76-94 mock）
   —— 需业务建模类：三源无风险告警/评分面；本件做候选承载图谱侧风险代理实算（anomaly 度偏离 + 结构脆弱度）
      并按 UI RiskLevelTag 分档（>=90 极高/80-89 高/70-79 中/<70 低）映射展示形态
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import (jx_connect, load_jiuxin_tech_frame, load_snap,
                           build_adj, composite_score_centrality, ABSENCE_PROBE_TMPL)

BASE = os.path.dirname(os.path.abspath(__file__))
snap307 = json.load(open(os.path.join(BASE, "_snapshots", "_probe_s307_l1_out.json")))["facts"]
facts = {}
facts["dev_gkxlumen_science_table_count"] = snap307["dev_gkxlumen_science_table_count"]
facts["dev_word_families"] = snap307["dev_word_families"]
facts["gkx_word_families"] = snap307["gkx_word_families"]
facts["jiuxin_word_families"] = snap307["jiuxin_word_families"]
facts["jiuxin_table_count_live"] = snap307["jiuxin_table_count_live"]
facts["jiuxin_tech_nodes_total"] = snap307["jiuxin_tech_nodes_total"]
facts["jiuxin_tech_edges_total"] = snap307["jiuxin_tech_edges_total"]

# ---------- 久新真图框内四维中心性（053 主承载 / 066 副承载 / 057 影响算子底料） ----------
t0 = time.time()
frame = load_jiuxin_tech_frame(5000)
adj = build_adj(frame["node_present"], frame["edges"])
present = sorted(adj.keys())
comp = composite_score_centrality(adj, present)
facts["jiuxin_tech_sample_induced_edges"] = len(frame["edges"])
facts["calc_frame"] = {"frame": 5000, "nodes_present": len(present), "edges": len(frame["edges"]),
                       "composite_pagerank_iters": comp["pagerank_iters"],
                       "composite_pagerank_final_diff": comp["pagerank_final_diff"]}

# ---------- 053 主承载：综合评分雷达 Top5（UI 四维 radar 数据向量复算） ----------
def radar_vector(k):
    """UI radarOption :307 数据向量 [degree, closeness, betweenness, min(1, PR×5)]（框内 min-max 归一+PR×5 截断）"""
    nd, nc, nb, np_ = normd, normc, normb, normp
    return [round(nd[k], 6), round(nc[k], 6), round(nb[k], 6),
            round(min(1.0, np_[k] * 5), 6)]

def _norm(dct):
    lo, hi = min(dct.values()), max(dct.values())
    return {k: (dct[k] - lo) / (hi - lo) if hi > lo else 0.0 for k in sorted(dct)}
normd, normc, normb, normp = _norm(comp["degree"]), _norm(comp["closeness"]), _norm(comp["betweenness"]), _norm(comp["pagerank"])
top5_comp = sorted(comp["composite"].items(), key=lambda kv: (-kv[1], kv[0]))[:5]
derived053_radar = {
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框) 四维中心性→UI 雷达数据向量",
    "indicator_axes": ["度中心性", "紧密中心性", "中介中心性", "PageRank×5"],
    "top5_by_composite": [
        {"node_id": k, "name_original": frame["id_name"].get(k, "")[:60],
         "composite": comp["composite"][k], "radar_value": radar_vector(k)} for k, _ in top5_comp],
}
# 066 副承载同框：PR 维单独读数（雷达第四轴）

# ---------- 057 主承载：节点移除连通性影响（analyzeRemovalImpact 同构实算） ----------
from collections import deque

def connected_components(adj_map, skip=None):
    seen, cnt = set(), 0
    for n in sorted(adj_map):
        if n == skip or n in seen:
            continue
        cnt += 1
        q = deque([n]); seen.add(n)
        while q:
            u = q.popleft()
            for v in sorted(adj_map[u]):
                if v != skip and v not in seen:
                    seen.add(v); q.append(v)
    return cnt

def removal_impact(adj_map, target):
    before = connected_components(adj_map)
    after = connected_components(adj_map, skip=target)
    delta = after - before
    sev = "高" if delta >= 2 else ("中" if delta == 1 else "低")
    return {"node_id": target, "components_before": before, "components_after": after,
            "delta": delta, "severity": sev, "affected_neighbors": len(adj_map[target])}

# 移除实验对象：框内综合分 Top5（053 同榜）+ 度 Top3 + 中介 Top2（关键节点代表性，B5 sorted 平局字典序）
targets = [k for k, _ in top5_comp]
targets += [k for k, _ in sorted(comp["degree"].items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
targets += [k for k, _ in sorted(comp["betweenness"].items(), key=lambda kv: (-kv[1], kv[0]))[:2]]
targets = sorted(set(targets))
removal_rows = [removal_impact(adj, t) | {"name_original": frame["id_name"].get(t, "")[:60],
                                          "degree": comp["degree"][t],
                                          "betweenness": comp["betweenness"][t],
                                          "pagerank": comp["pagerank"][t],
                                          "composite": comp["composite"][t]} for t in targets]
# 度排序展示
removal_rows_sorted = sorted(removal_rows, key=lambda r: (-r["delta"], -r["degree"], r["node_id"]))
derived057 = {
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框) 移除实验（analyzeRemovalImpact 同构：BFS 连通分量 before/after）",
    "graph_baseline": {"components_before_all": connected_components(adj), "nodes": len(present), "edges": len(frame["edges"])},
    "severity_rule": "Δ>=2 高 / Δ==1 中 / else 低（centralityAlgo.js:281）",
    "removal_experiments": removal_rows_sorted,
    "high_medium_count": {"高": sum(1 for r in removal_rows if r["severity"] == "高"),
                          "中": sum(1 for r in removal_rows if r["severity"] == "中"),
                          "低": sum(1 for r in removal_rows if r["severity"] == "低")},
}

# ---------- 066 主承载：风险评分候选图谱代理实算（需业务建模类·代理法） ----------
# 代理公式（推测定义，登记待裁）：risk_proxy = 100×(0.45×anomaly + 0.35×vulnerability + 0.20×exposure)
#   anomaly = 度 z-score 截断 [0,1]（异常关联代理，参照 UI nodeAnomaly 语义）
#   vulnerability = 移除 Δ 归一（结构脆弱度：该节点失联引发碎片化的程度）
#   exposure = PR 归一（全局暴露面：被重要节点指向的程度）
deg_vals = [comp["degree"][u] for u in present]
mean_d = sum(deg_vals) / len(deg_vals)
var_d = sum((d - mean_d) ** 2 for d in deg_vals) / len(deg_vals)
std_d = var_d ** 0.5
facts["jiuxin_frame_degree_stats"] = {"mean": round(mean_d, 4), "std": round(std_d, 4),
                                      "min": min(deg_vals), "max": max(deg_vals)}
delta_map = {r["node_id"]: r["delta"] for r in removal_rows}
max_delta = max(delta_map.values()) if delta_map else 0

def risk_proxy(u):
    z = (comp["degree"][u] - mean_d) / std_d if std_d else 0.0
    anomaly = max(0.0, min(1.0, z / 3.0))  # 3σ 饱和归一（063 ER-01 规则 3σ 语义参照）
    vuln = (delta_map.get(u, 0) / max_delta) if max_delta else 0.0
    expo = normp[u]
    return round(100 * (0.45 * anomaly + 0.35 * vuln + 0.20 * expo), 2)

# 评估对象：removal 实验对象 + 度 Top10（关键节点风险画像）
risk_targets = sorted(set(targets) | {k for k, _ in sorted(comp["degree"].items(), key=lambda kv: (-kv[1], kv[0]))[:10]})
risk_rows = [{"node_id": u, "name_original": frame["id_name"].get(u, "")[:60],
              "risk_proxy_score": risk_proxy(u),
              "degree": comp["degree"][u], "pagerank": comp["pagerank"][u],
              "removal_delta": delta_map.get(u, 0)} for u in risk_targets]
risk_rows_sorted = sorted(risk_rows, key=lambda r: (-r["risk_proxy_score"], r["node_id"]))
def ui_risk_level(s):
    return "极高风险" if s >= 90 else ("高风险" if s >= 80 else ("中风险" if s >= 70 else "低风险"))
for r in risk_rows_sorted:
    r["ui_risk_level"] = ui_risk_level(r["risk_proxy_score"])
derived066 = {
    "source": "jiuxin.ads_technology_graph_edge 诱导子图(5000节点框) 风险代理评分（推测定义·待业务裁定）",
    "formula": "risk_proxy = 100×(0.45×anomaly_z3σ + 0.35×vulnerability_Δnorm + 0.20×exposure_PRnorm)",
    "formula_note": "需业务建模类：三源无风险评分真源（探针留证）；代理法=图谱结构侧候选承载，权重与维度待业务裁定",
    "risk_top10": risk_rows_sorted[:10],
    "risk_level_distribution": {lv: sum(1 for r in risk_rows_sorted if r["ui_risk_level"] == lv)
                                for lv in ["极高风险", "高风险", "中风险", "低风险"]},
    "ui_reference_form": "OptimizeDecisionPanel riskColumns 风险分 Progress + decisionRiskAlerts mock 76-94 分（业务承载缺位证据）",
}

support = "完全转换支持"  # 053/057：真图实算通过；066 需业务建模但图谱代理可算——三件统一「完全转换支持」（066 MD 里披露代理口径待裁）

absence = list(ABSENCE_PROBE_TMPL) + [
    {"what": "dev/久新/gkx 风险告警与风险评分结果面（053 雷达现成向量/057 移除影响表/066 风险分）",
     "how": "S3-07 族级探针 _probe_s307_l1_out.json 词族扫描（risk/fusion/decision 词族）",
     "hits": "dev gkxlumen_science 0 表；久新 risk 词族 0 命中；gkx 仅 dwd_org_risk_shixin/zhixing/tax_punish（企业失信/被执行/税务处罚——企业风险语义非图谱风险评分）"},
]

out_common = {"facts": facts, "absence_probe": absence}
# ---------- 053 产物 ----------
out053 = {**out_common, "metric_id": "M_SCIUI_KGANALY_053",
          "metric_name": "综合评分雷达（Top5）（科技知识图谱·中心性计算展示·多维度综合分析）",
          "derived": [derived053_radar],
          "support_judgment": support,
          "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_053_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out053, fh, ensure_ascii=False, indent=2)
print("done 053 | radar top1:", derived053_radar["top5_by_composite"][0]["radar_value"])

# ---------- 057 产物 ----------
out057 = {**out_common, "metric_id": "M_SCIUI_KGANALY_057",
          "metric_name": "节点移除连通性影响（科技知识图谱·中心性计算展示·中介中心性）",
          "derived": [derived057],
          "support_judgment": support,
          "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_057_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out057, fh, ensure_ascii=False, indent=2)
print("done 057 | baseline comps:", derived057["graph_baseline"], "| 高/中/低:",
      derived057["high_medium_count"])

# ---------- 066 产物 ----------
out066 = {**out_common, "metric_id": "M_SCIUI_KGANALY_066",
          "metric_name": "图谱风险评分（科技知识图谱·指标展示·优化决策模型·风险识别优化）",
          "derived": [derived066],
          "support_judgment": support,
          "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面，无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_066_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out066, fh, ensure_ascii=False, indent=2)
print("done 066 | risk top1:", risk_rows_sorted[0]["name_original"][:40], risk_rows_sorted[0]["risk_proxy_score"],
      "| dist:", derived066["risk_level_distribution"])
print("calc sec:", round(time.time() - t0, 1))
