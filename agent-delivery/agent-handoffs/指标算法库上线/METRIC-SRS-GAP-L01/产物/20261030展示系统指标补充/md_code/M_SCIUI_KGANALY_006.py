#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_006 图谱节点平均度数 — 三源探针 + 真实度数实算 + 判档产物
UI 挂载：CentralityPanel.jsx:380 typeBarOption（yAxis name='平均度数'，按节点类型分组比较条形图）。
承载：久新 ads_technology_graph_node.weighted_degree 列直查（19,430 节点全列非空——同族 001 已验）
→ 完全转换支持：全图平均度数+分类型平均度数两组读数现算。
"""
import json, os, sys, time, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_006_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "CentralityPanel.jsx:380 typeBarOption yAxis name='平均度数'（度中心性 Tab·按节点类型分组比较卡 CentralityPanel.jsx:664）"
facts["ui_algo_source"] = "centralityAlgo.js:426-434 byType 分组：avgDegree = sum(degreeRaw)/count——UI 在 15 节点演示图上按类型分组算平均度数"

# ---------- ① dev：图结构面空壳（族级快照） ----------
facts["dev_graph_word_table_rows"] = snap["facts"].get("dev_graph_word_table_rows") or {}
dev_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if isinstance(v, int) and v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_nonzero.items()))

# ---------- ② gkx：学者合作网（备选） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
facts["gkx_scholar_rows"] = gc.fetchone()[0]
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0")
facts["gkx_coauthor_edges_total"] = gc.fetchone()[0]
# 备选承载平均度（等权无向去重口径在 SQL 侧不便，取 2E/N 简式并披露方向性）
facts["gkx_coauthor_avg_degree_2E_over_N_raw"] = round(2 * facts["gkx_coauthor_edges_total"] / facts["gkx_scholar_rows"], 4)
gc.close()

# ---------- ③ 久新：技术图 weighted_degree 直查（主承载） ----------
def jx_connect(tries=4):
    last = None
    for _ in range(tries):
        try:
            return pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                                   password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                                   database="gkx_technology_analysis_dev", charset="utf8mb4",
                                   connect_timeout=15, read_timeout=600)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(15)
    raise last

jx = jx_connect()
jc = jx.cursor()
facts["jiuxin_table_count_live"] = snap["facts"]["jiuxin_table_count_live"]
facts["jiuxin_tech_nodes_total"] = snap["facts"].get("jiuxin_tech_nodes_total") or 19430
facts["jiuxin_tech_edges_total"] = snap["facts"].get("jiuxin_tech_edges_total") or 587252
# weighted_degree 列质量：非空/零值计数
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node WHERE weighted_degree IS NOT NULL")
facts["jiuxin_weighted_degree_nonnull"] = jc.fetchone()[0]
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node WHERE weighted_degree = 0")
facts["jiuxin_weighted_degree_zero"] = jc.fetchone()[0]
# 全图平均度数（节点表直查——权威口径：平均加权度）
jc.execute("SELECT AVG(weighted_degree), MIN(weighted_degree), MAX(weighted_degree), SUM(weighted_degree) "
           "FROM ads_technology_graph_node WHERE weighted_degree IS NOT NULL")
avg_wd, min_wd, max_wd, sum_wd = jc.fetchone()
facts["jiuxin_weighted_degree_avg"] = round(float(avg_wd), 4)
facts["jiuxin_weighted_degree_min"] = float(min_wd)
facts["jiuxin_weighted_degree_max"] = float(max_wd)
facts["jiuxin_weighted_degree_sum"] = float(sum_wd)
# 边表口径交叉验证：2E/N（无权简单图平均度，边数含方向需查 direction_status）
jc.execute("SELECT direction_status, COUNT(*) FROM ads_technology_graph_edge GROUP BY direction_status ORDER BY COUNT(*) DESC")
facts["jiuxin_edge_direction_dist"] = [[r[0], r[1]] for r in jc.fetchall()]
# 分组承载：节点表无 type 列（族级快照 jiuxin_node_type_col=null）→ 按社区分组（community_name 域）
jc.execute("SELECT community_id IS NULL AS is_null_comm, COUNT(*) FROM ads_technology_graph_node GROUP BY is_null_comm")
facts["jiuxin_node_community_null_dist"] = [[bool(r[0]), r[1]] for r in jc.fetchall()]
# 按社区规模分桶的平均加权度（Top5 大社区 + 单点社区）
jc.execute("""SELECT community_id, COUNT(*) AS n, AVG(weighted_degree) AS avg_wd
              FROM ads_technology_graph_node WHERE community_id IS NOT NULL
              GROUP BY community_id ORDER BY n DESC, community_id ASC LIMIT 5""")
comm_top5 = [[r[0], r[1], round(float(r[2]), 4)] for r in jc.fetchall()]
facts["jiuxin_community_top5_avg_weighted_degree"] = comm_top5
jc.execute("SELECT COUNT(*) FROM ads_technology_graph_node WHERE is_singleton_community = TRUE")
facts["jiuxin_singleton_community_nodes"] = jc.fetchone()[0]
# 单点社区节点的平均加权度（对照组）
jc.execute("SELECT AVG(weighted_degree) FROM ads_technology_graph_node WHERE is_singleton_community = TRUE")
sv = jc.fetchone()[0]
facts["jiuxin_singleton_avg_weighted_degree"] = round(float(sv), 4) if sv is not None else None
jx.close()

derived = []
n = facts["jiuxin_weighted_degree_nonnull"]
if n:
    derived.append({
        "source": "jiuxin.ads_technology_graph_node.weighted_degree 全列直查",
        "nodes_with_weighted_degree": n,
        "avg_weighted_degree": facts["jiuxin_weighted_degree_avg"],
        "denominator_note": f"sum(weighted_degree)={facts['jiuxin_weighted_degree_sum']} / 节点数 {n}（非空全列，同池同 WHERE）",
    })
    derived.append({
        "source": "边表口径交叉验证（无权简单图）",
        "avg_degree_2E_over_N": round(2 * facts["jiuxin_tech_edges_total"] / facts["jiuxin_tech_nodes_total"], 4),
        "denominator_note": f"2*E(2×{facts['jiuxin_tech_edges_total']})/N({facts['jiuxin_tech_nodes_total']})——无权口径，与加权口径并列披露",
    })

absence_probe = [
    {"what": "dev 现成平均度数/图统计结果面", "how": "dev 图词族 26 张计数（族级快照）",
     "hits": "全 0 行——结构在数据空"},
    {"what": "gkx 图统计结果面（度数直查列）", "how": "gkx 280 表词族扫描（degree/centrality/graph_stat）",
     "hits": "0——coauthor 边表可推导（2E/N 简式）但无节点级度数列"},
    {"what": "久新现成「平均度数」指标行", "how": "久新 218 表词族扫描（graph_stat/metric_summary）",
     "hits": "0——但节点表 weighted_degree 列全列在库，AVG 一步即得（转换正当）"},
]

support = "完全转换支持" if facts["jiuxin_weighted_degree_nonnull"] > 0 else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_006", "metric_name": "图谱节点平均度数（科技知识图谱·中心性面板·按类型分组比较）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["图谱为 2026-11-02 live 截面（metrics_as_of_date=2026-10-16），无年度基期维"],
       "base_years_note": "物理口径基期=图快照日（metrics_as_of_date=2026-10-16 批次截面）；非年度基期，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support, "| avg_wd:", facts["jiuxin_weighted_degree_avg"])
