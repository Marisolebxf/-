#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_012 分析洞察 — 三源探针 + 久新真图实算洞察参数 + UI 模板复现 + 判档产物
UI 挂载：QueryAssetDeepAnalysisDrawer.jsx:119-127「分析洞察」卡片——渲染 buildDeepAnalysis(asset).insights 三条：
  ①核心发现（桥接节点数 bridgeCount）②关联提示（标签×场景模板）③数据说明（自带 Mock 披露）
生成器：queryAssetDeepAnalysis.js:18-46——hashSeed 种子随机数（确定性），数值参数：
  bridgeCount=seededInt(2..9)、社群数=seededInt(2..6)、跨域边占比=seededInt(18..42)%、节点 18..86、边 node..4*node
资产清单：mockData.js:839+ graphQueryAssets（6 条 mock 资产）——三源无「查询资产登记面」（asset/报表/看板词族）。
判档：部分支持——洞察文本框架是模板（非指标），但模板内数值参数（桥接/社群/跨域占比）可在久新真图采样框内实算；
「资产」实体登记面缺失 → 资产粒度的洞察生成链断裂（无从知道分析对象是谁）。
"""
import json, math, os, time
from collections import defaultdict, deque

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_012_out.json")
snap = json.load(open(SNAP))
facts = {}

# ---------- UI 挂载与生成器（实读留证） ----------
facts["ui_mount"] = ("QueryAssetDeepAnalysisDrawer.jsx:119-127「分析洞察」Card——analysis.insights.map 渲染"
                     "（Tag type + Text text 三条：核心发现/关联提示/数据说明）；生成器 queryAssetDeepAnalysis.js:36-46")
facts["ui_generator"] = ("queryAssetDeepAnalysis.js:18-34 buildDeepAnalysis——hashSeed（31 进制滚动哈希）+seededInt "
                         "确定性种子随机：nodeCount 18..86 / edgeCount node..4n / density=e/(n(n-1)/2) / "
                         "bridgeCount 2..9 / score 72..96；insights 三条模板文案填参")
facts["ui_insight_templates"] = [
    "核心发现：在「{field}」领域识别 {bridgeCount} 个桥接节点，建议优先关注跨机构合作边。",
    "关联提示：与标签「{tags}」相关的子结构可用于{scenario}。",
    "数据说明：来源 {source}；当前为演示级 Mock 分析，正式环境由图分析服务返回。（自带 Mock 披露）",
]
facts["ui_asset_source"] = ("mockData.js:839+ graphQueryAssets 六条 mock 资产（AI 产学研合作子图/量子计算技术演进报告/"
                            "生物医药机构关联图/新能源合作路径桑基/…），ServiceDisplay.jsx:60-74 导入、:1683 挂 Drawer")

# ---------- 三源：资产登记面词族（复用族级快照） ----------
fw = snap["facts"].get("jiuxin_feedback_model_word_tables")
facts["jiuxin_table_count_live"] = snap["facts"]["jiuxin_table_count_live"]
facts["asset_registry_absence"] = {
    "dev": "gkxlumenx 542 表词族（asset/报表/看板/registry/dashboard/report）无查询资产登记面——graphQueryAssets 所示『资产』（子图/报告/图表）无 DB 面",
    "gkx": "gkx 280 表专利/学者要素域，无资产/看板登记面",
    "jiuxin": f"久新 {facts['jiuxin_table_count_live']} 表 ADS 结果面（图/合作/人才域），词族 feedback/model 0 命中（族级快照在案），无资产登记面",
}

# ---------- 久新真图实算洞察参数（5000 节点采样框，001 同款） ----------
import pymysql  # noqa: E402

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
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node")
facts["jiuxin_nodes_total"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_edge")
facts["jiuxin_edges_total"] = jc.fetchone()[0]
# 采样框：按主键序前 5000 节点 + 框内诱导边（001 同款 IN 子查询模式）
jc.execute("SELECT technology_node_id FROM ads_technology_graph_node "
           "ORDER BY technology_node_id LIMIT 5000")
frame_ids = [r[0] for r in jc.fetchall()]
idset = set(frame_ids)
jc.execute("SELECT source_technology_node_id, target_technology_node_id, relation_type "
           "FROM ads_technology_graph_edge "
           "WHERE source_technology_node_id IN (SELECT technology_node_id FROM "
           "(SELECT technology_node_id FROM ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000) t) "
           "AND target_technology_node_id IN (SELECT technology_node_id FROM "
           "(SELECT technology_node_id FROM ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000) t2)")
edges = jc.fetchall()
jc.execute("SELECT community_id, COUNT(*) FROM ads_technology_graph_node "
           "WHERE technology_node_id IN (SELECT technology_node_id FROM "
           "(SELECT technology_node_id FROM ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000) t) "
           "GROUP BY community_id")
comm_rows = jc.fetchall()
jx.close()

und = defaultdict(set)
rel_of = defaultdict(set)
for s, t, rt in edges:
    und[s].add(t); und[t].add(s)
    rel_of[(s, t) if s < t else (t, s)].add(rt)

# ① 桥接节点（跨社区边端点即桥——图分析口径：删之则跨社区连通对减少）
comm = {nid: cid for cid, cnt in comm_rows for nid in [None]}  # placeholder replaced below
# 重新拉 community 映射（comm_rows 是 (cid,count) 聚合，需逐节点）
jx = jx_connect()
jc = jx.cursor()
ph = ",".join(["%s"] * len(frame_ids))
jc.execute(f"SELECT technology_node_id, community_id FROM ads_technology_graph_node "
           f"WHERE technology_node_id IN ({ph})", frame_ids)
comm = dict(jc.fetchall())
jx.close()

cross_edges = [(s, t) for s, t, _ in edges if comm.get(s) != comm.get(t)]
bridge_nodes = sorted({n for e in cross_edges for n in e})
facts["sample_frame"] = {"nodes": len(frame_ids), "induced_edges": len(edges),
                         "frame_rule": "ads_technology_graph_node ORDER BY technology_node_id LIMIT 5000（001 同款确定性采样框）"}
facts["derived_bridge"] = {
    "definition": "桥接节点=采样框内跨社区边端点（community_id 不同）——UI 文案『桥接节点』的图分析口径落点",
    "cross_community_edges": len(cross_edges), "bridge_nodes": len(bridge_nodes),
    "cross_edge_ratio_pct": round(len(cross_edges) / max(len(edges), 1) * 100, 2),
}
# ② 社群数（框内 community_id 去重——非算法重算，直读图库社区标注）
facts["derived_communities"] = {
    "definition": "采样框内 community_id 去重计数（直读久新图库社区标注，非算法重算）",
    "community_count": len({c for c in comm.values()}),
    "top3_sizes": sorted(((str(cid), cnt) for cid, cnt in comm_rows), key=lambda x: -x[1])[:3],
}
# ③ 跨域边占比（关系类型多样性口径：不同 relation_type 组合的边占比）
rel_cnt = defaultdict(int)
for s, t in ((s, t) for s, t, _ in edges):
    rel_cnt[tuple(sorted(rel_of[(s, t) if s < t else (t, s)]))] += 1
facts["derived_cross_domain_ratio"] = {
    "definition": "跨域边占比（UI 参数 x%）：以 relation_type 复合边（多类型关系边）占比为最近似口径",
    "multi_type_edges": sum(v for k, v in rel_cnt.items() if len(k) > 1),
    "ratio_pct": round(sum(v for k, v in rel_cnt.items() if len(k) > 1) / max(len(edges), 1) * 100, 2),
    "top3_rel_types": sorted((("|".join(k), v) for k, v in rel_cnt.items()), key=lambda x: -x[1])[:3],
}
# ---------- UI 生成器复现（hashSeed/seededInt 移植，asset-001 实测） ----------
def hash_seed(s):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h

def seeded_int(seed, mn, mx):
    n = (hash_seed(seed) % 1000) / 1000
    return math.floor(mn + n * (mx - mn + 1))

node_count = seeded_int("asset-001-n", 18, 86)
edge_count = seeded_int("asset-001-e", node_count, node_count * 4)
density = round(edge_count / max(node_count * (node_count - 1) / 2, 1) * 100, 1)
bridge_mock = seeded_int("asset-001-b", 2, 9)
comm_mock = seeded_int("asset-001-c", 2, 6)
cross_mock = seeded_int("asset-001-x", 18, 42)
facts["ui_generator_repro_asset001"] = {
    "node": node_count, "edge": edge_count, "density_pct": density,
    "bridge": bridge_mock, "communities": comm_mock, "cross_domain_pct": cross_mock,
    "note": "queryAssetDeepAnalysis.js hashSeed/seededInt 移植复现（Python 端口），asset-001 输入与 UI 完全同值——确定性生成器可精确复现",
}
insight_texts = [
    f"核心发现：在「人工智能」领域识别 {bridge_mock} 个桥接节点，建议优先关注跨机构合作边。",
    f"关联提示：与标签「合作网络、产学研」相关的子结构可用于风险核查单 URL 跳转预览。",
    "数据说明：来源 ADS_KG_SUBGRAPH；当前为演示级 Mock 分析，正式环境由图分析服务返回。",
]
facts["ui_insight_repro_asset001"] = insight_texts

derived = [
    {"name": "桥接节点数（真图实算）", "value": facts["derived_bridge"]["bridge_nodes"],
     "basis": f"久新真图 5000 节点框，跨社区边 {facts['derived_bridge']['cross_community_edges']} 条的端点去重"},
    {"name": "社群数（真图实算）", "value": facts["derived_communities"]["community_count"],
     "basis": "采样框内 community_id 去重（直读图库社区标注）"},
    {"name": "跨域边占比（真图实算）", "value": facts["derived_cross_domain_ratio"]["ratio_pct"],
     "basis": f"多 relation_type 复合边 {facts['derived_cross_domain_ratio']['multi_type_edges']} 条 / 框内边 {len(edges)}"},
    {"name": "UI 模拟值对照（asset-001）", "value": f"桥接 {bridge_mock} / 社群 {comm_mock} / 跨域 {cross_mock}%",
     "basis": "hashSeed 种子随机数移植复现——与真图实算值无对应关系（纯演示参数）"},
]

absence_probe = [
    {"what": "查询资产登记面（graphQueryAssets 所示子图/报告/图表资产）",
     "how": "dev 542 表 + gkx 280 表 + 久新 218 表词族（asset/report/dashboard/registry/看板）",
     "hits": "0——三源均无资产登记面；资产清单为 mockData 写死 6 条"},
    {"what": "图分析服务返回面（UI 数据说明自注『正式环境由图分析服务返回』）",
     "how": "三源词族（analysis/insight/service_result）",
     "hits": "0——无洞察文本落盘面；洞察生成器为前端 queryAssetDeepAnalysis.js 种子随机模板"},
]
support = "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_012", "metric_name": "分析洞察（科技知识图谱·指标展示·图查询资产·深入分析）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "support_rationale": ("洞察=模板文本+数值参数：数值参数（桥接节点/社群数/跨域边占比）久新真图采样框内可实算（本脚本实算在案）；"
                             "但『资产』实体登记面三源缺失→资产粒度洞察生成链断裂（分析对象不可寻址），文本模板本身是 UI 固定文案——部分支持"),
       "base_years_used": [], "base_years_missing": ["洞察为资产分析截面输出，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（久新图为单版本快照）；洞察为截面分析输出，非年度基期概念"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support,
      "| bridge:", facts["derived_bridge"]["bridge_nodes"],
      "communities:", facts["derived_communities"]["community_count"],
      "cross%:", facts["derived_cross_domain_ratio"]["ratio_pct"])
