#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_030 图谱综合评分 — 久新节点表现三档加权实算 + 判档产物
UI 语义（graphObjectDetail.js:144）：score=86 / relationStrength=82——对象级 0-100 综合分 mock。
久新节点表现成三档：结构表现（weighted_degree）+ 社区角色（community_role）+ 成员度表现
（membership_score）——min-max 归一 + 0.4/0.3/0.3 加权合成同尺度综合分。
"""
import json
import os

import pymysql

import _s306_graph_base as gb

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_030_out.json")

facts = {}
facts["ui_mount"] = "graphObjectDetail.js:144（score=86, relationStrength=82 mock）| InstrumentSharingPage.jsx:407/467"
facts["ui_semantics"] = "图谱对象详情页综合评分卡：0-100 分制对象级综合表现（SRS row_01=493，引进评估＞综合评分）"
facts["ui_demo_fallback"] = "score=86/relationStrength=82 为前端 mock 常数，无后端评分承载（三源扫描 0 评分面）"
facts["srs_anchor"] = "SRS 分类「需业务建模类」——权重设计需立项调研，本件以表现三档 0.4/0.3/0.3 参照组合作操作化口径"
facts["cat"] = "需业务建模类"

ROLE_SCORE = {"CORE": 1.0, "BRIDGE": 0.7, "MEMBER": 0.4, "ISOLATE": 0.1}

c = gb.load_cache()
names = {r[0]: r[1] for r in c["node_rows"]}
frame_ids = [r[0] for r in c["node_rows"]]
frame_set = set(frame_ids)

# 全表直查三档列（19,430 行轻查询；限流 1203 则 15s 重试）
jx = gb.jx_connect()
jc = jx.cursor()
jc.execute("""SELECT technology_node_id, weighted_degree, community_role, membership_score,
                     technology_name_original
              FROM ads_technology_graph_node""")
allrows = jc.fetchall()
jx.close()

n_all = len(allrows)
wd = [float(r[1]) for r in allrows if r[1] is not None]
ms = [float(r[3]) for r in allrows if r[3] is not None]
wd_min, wd_max = min(wd), max(wd)
ms_min, ms_max = min(ms), max(ms)
facts["jiuxin_nodes_total"] = c["nodes_total"]
facts["jiuxin_edges_total"] = c["edges_total"]
facts["weighted_degree_range"] = [wd_min, wd_max]
facts["membership_score_range"] = [ms_min, ms_max]

def comp_score(r):
    wd_norm = ((float(r[1]) - wd_min) / (wd_max - wd_min)) if (r[1] is not None and wd_max > wd_min) else 0.0
    role_norm = ROLE_SCORE.get((r[2] or "").upper(), 0.1)
    ms_norm = ((float(r[3]) - ms_min) / (ms_max - ms_min)) if (r[3] is not None and ms_max > ms_min) else 0.0
    return 100 * (0.4 * wd_norm + 0.3 * role_norm + 0.3 * ms_norm)

allnames = {r[0]: (r[4] or "") for r in allrows}

scored_all = [(r[0], comp_score(r)) for r in allrows]
scored_all.sort(key=lambda x: (-x[1], x[0]))
frame_scores = sorted([s for i, s in scored_all if i in frame_set])
n_frame = len(frame_scores)
avg_all = sum(s for _, s in scored_all) / n_all
avg_frame = sum(frame_scores) / n_frame

role_dist = {}
for r in allrows:
    role_dist[r[2] or "NULL"] = role_dist.get(r[2] or "NULL", 0) + 1

def pct(a, p):
    k = (len(a) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(a) - 1)
    return a[lo] + (a[hi] - a[lo]) * (k - lo)

top10 = [{"node_id": i, "name_original": allnames.get(i, ""), "score": round(s, 2)} for i, s in scored_all[:10]]

derived = [{
    "source": "jiuxin.ads_technology_graph_node 全表 19,430 节点（无采样——轻列直查）",
    "formula": "score = 100*(0.4*norm(weighted_degree) + 0.3*role_score + 0.3*norm(membership_score))",
    "role_score_map": ROLE_SCORE,
    "weights": {"structure_wd": 0.4, "community_role": 0.3, "membership": 0.3},
    "nodes_scored": n_all,
    "role_distribution": dict(sorted(role_dist.items())),
    "avg_score_all": round(avg_all, 2),
    "avg_score_frame5000": round(avg_frame, 2),
    "p50": round(pct(frame_scores, 0.50), 2),
    "p90": round(pct(frame_scores, 0.90), 2),
    "p99": round(pct(frame_scores, 0.99), 2),
    "max": round(frame_scores[-1], 2),
    "top10_global": top10,
    "ui_mock_reference": {"score": 86, "relationStrength": 82, "note": "mock 常数；本件实算 P90=高分带与 mock 量级可比"},
}]

absence_probe = [
    {"what": "久新现成综合评分列", "how": "节点表 26 列 DESCRIBE 全扫（score/rating/composite）", "hits": "0 直存评分列；但三档成分列（weighted_degree/community_role/membership_score）满承载"},
    {"what": "gkx 综合评分承载", "how": "280 表词族扫描", "hits": "0"},
    {"what": "dev 综合评分面", "how": "族级快照", "hits": "0 行"},
    {"what": "UI 综合分来源", "how": "graphObjectDetail.js 读码", "hits": "score=86/relationStrength=82 mock 常数"},
]

out = {"metric_id": "M_SCIUI_KGANALY_030", "metric_name": "图谱综合评分（科技知识图谱·引进评估·综合评分）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe,
       "support_judgment": "完全转换支持",
       "base_years_used": [],
       "base_years_missing": ["无年度基期维（评分为当日 live 截面加权合成，无历史快照对比）"],
       "base_years_note": "物理口径基期=探针快照日；综合评分为截面合成分，无时序基期；非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
dv = derived[0]
print("scored", dv["nodes_scored"], "avg_all", dv["avg_score_all"], "avg_frame", dv["avg_score_frame5000"])
print("p50/p90/p99/max", dv["p50"], dv["p90"], dv["p99"], dv["max"])
print("roles", dv["role_distribution"])
for t in dv["top10_global"][:3]:
    print("top:", t["name_original"][:40], t["score"])
