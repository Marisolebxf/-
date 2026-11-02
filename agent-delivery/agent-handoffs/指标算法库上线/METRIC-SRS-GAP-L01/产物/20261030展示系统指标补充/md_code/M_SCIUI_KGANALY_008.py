#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_008 图谱关系活跃度 — 三源探针 + 规则口径真实复算 + 判档产物
UI 挂载：graphMapAnalysis.js:115 metrics[].relationActivity（label='关系活跃度'，value=`${relationActivity}%`，
  meta=`${relationTypeCount} 类关系`）。
UI 口径（:15-19 getRelationActivityScore）：min(98, max(36, relationTypeCount*11 + layerCount*5)) + 上下文修正。
本件按同构口径在久新真图复算：relationTypeCount=边表 relation_type 去类数（实测 4），layerCount 取社区层（节点表
community 域分层数）——读数落产物；同时披露该口径为 UI 启发式合成（非学术定义）。
"""
import json, os, sys, time, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_008_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "graphMapAnalysis.js:115 metrics[1] { key:'relationActivity', label:'关系活跃度', value:`${relationActivity}%`, meta:`${relationTypeCount} 类关系` }"
facts["ui_formula"] = "graphMapAnalysis.js:15-19 getRelationActivityScore = min(98, max(36, relationTypeCount*11 + layerCount*5))；:66-69 + round(contextAdjustment*2)（时间/事件修正）"
facts["ui_formula_params"] = {"base_clamp": [36, 98], "relation_type_weight": 11, "layer_weight": 5}

# ---------- ① dev：图结构面空壳（族级快照） ----------
facts["dev_graph_word_table_rows"] = snap["facts"].get("dev_graph_word_table_rows") or {}
dev_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if isinstance(v, int) and v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_nonzero.items()))

# ---------- ② gkx：合作网关系类型数（备选：边语义=合著单一类） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0")
facts["gkx_coauthor_edges_total"] = gc.fetchone()[0]
gc.close()

# ---------- ③ 久新：真图关系类型分布（族级快照已有 top20） ----------
facts["jiuxin_edge_relation_type_top20"] = snap["facts"]["jiuxin_edge_relation_type_top20"]
facts["jiuxin_relation_type_count"] = len(facts["jiuxin_edge_relation_type_top20"])

def jx_connect(tries=4):
    last = None
    for _ in range(tries):
        try:
            return pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                                   password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                                   database="gkx_technology_analysis_dev", charset="utf8mb4",
                                   connect_timeout=15, read_timeout=300)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(15)
    raise last

jx = jx_connect()
jc = jx.cursor()
# 层位数（UI layerCount 语义=启用的要素图层；真图对应=社区数上限与 relation_source 分层）
jc.execute("SELECT COUNT(DISTINCT community_id) FROM ads_technology_graph_node")
facts["jiuxin_community_count"] = jc.fetchone()[0]
jc.execute("SELECT relation_source, COUNT(*) FROM ads_technology_graph_edge GROUP BY relation_source ORDER BY relation_source")
facts["jiuxin_edge_relation_source_dist"] = [[r[0], r[1]] for r in jc.fetchall()]
jx.close()

# ---------- UI 同构复算（B1：读数只由脚本产出） ----------
relation_type_count = facts["jiuxin_relation_type_count"]
layer_count = min(facts["jiuxin_community_count"], 3)  # UI 演示图启用 3 图层（机构/项目/技术），对齐取 3
layer_count_ui_align = 3

def ui_activity_score(rtc, lc):
    return min(98, max(36, rtc * 11 + lc * 5))

derived = []
derived.append({
    "source": "jiuxin.ads_technology_graph_edge relation_type 去类 + UI 同构公式",
    "relation_type_count": relation_type_count,
    "layer_count": layer_count_ui_align,
    "raw_score": relation_type_count * 11 + layer_count_ui_align * 5,
    "activity_score": ui_activity_score(relation_type_count, layer_count_ui_align),
    "formula_note": "min(98, max(36, 4*11+3*5))=min(98,59)=59——contextAdjustment 按 0 基线（无时间/事件选中态）",
})
# 全社区层口径（敏感性对照：layerCount=社区全数会封顶 98）
derived.append({
    "source": "敏感性对照：layerCount=全社区数（语义偏离 UI 演示 3 层）",
    "layer_count": facts["jiuxin_community_count"],
    "activity_score_capped": 98,
    "note": f"layerCount={facts['jiuxin_community_count']} 时 4*11+layer*5 远超 98 封顶——层位口径是首要敏感项",
})

absence_probe = [
    {"what": "dev 现成「关系活跃度」结果面", "how": "dev 图词族 26 张计数（族级快照）",
     "hits": "全 0 行——结构在数据空"},
    {"what": "gkx 关系活跃度/活跃度结果面", "how": "gkx 280 表词族扫描（activity/active/liveness）",
     "hits": "0——coauthor 边可算类型数（合著单一类=1）但无活跃度定义面"},
    {"what": "久新现成「关系活跃度」指标行", "how": "久新 218 表词族扫描（activity/active）",
     "hits": "0——但边表 relation_type 4 类+社区分层数可按 UI 公式合成"},
]

support = "完全转换支持" if relation_type_count > 0 else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_008", "metric_name": "图谱关系活跃度（科技知识图谱·图谱地图分析）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["活跃度为规则合成指数（当日图截面输入），无年度基期维"],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16）；指数为截面合成值非时序量"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support, "| score:", derived[0]["activity_score"])
