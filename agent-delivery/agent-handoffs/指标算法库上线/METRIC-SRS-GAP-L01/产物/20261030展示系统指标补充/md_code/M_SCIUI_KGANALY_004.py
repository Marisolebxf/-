#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_004 专家引进评估子图 — 三源探针 + 真实合作子图构建 + 判档产物
UI 挂载：mockData.js:968 asset-008「专家引进评估子图」（查询资产深析抽屉，graph 类型缩略图）。
承载判定：久新 ads_talent_profile（10 万学者档）+ ads_talent_collaborator（505 万合作边）
→ 完全转换支持：专家-合作网络两表齐备，可现算「候选专家×合作网×成果关联」子图。
ego 诱导子图：邻居间连边用「按 collaborator_talent_id IN 邻居框 拉边再本地过滤」避免 Doris 大 IN JOIN 超时。
"""
import json, os, sys, time, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_004_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "mockData.js:968 asset-008「专家引进评估子图」displayKind=graph entityType=专家 tags=[专家,引进,项目] source=ADS_KG_SUBGRAPH scenario=人才服务台嵌入"
facts["ui_drawer"] = "QueryAssetDeepAnalysisDrawer.jsx:119 分析洞察卡（深析抽屉 buildDeepAnalysis）"

# ---------- ① dev：图结构面空壳（族级快照复用） ----------
facts["dev_graph_word_table_rows"] = snap["facts"].get("dev_graph_word_table_rows") or {}
dev_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if v and isinstance(v, int) and v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_nonzero.items()))

# ---------- ② gkx：学者合作网（备选承载） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
facts["gkx_scholar_rows"] = gc.fetchone()[0]
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0")
facts["gkx_coauthor_edges_total"] = gc.fetchone()[0]
gc.close()

# ---------- ③ 久新：人才档+合作边（主承载） ----------
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
facts["jiuxin_talent_profile_rows"] = snap["facts"]["jiuxin_talent_profile_rows"]
facts["jiuxin_talent_collaborator_rows"] = snap["facts"]["jiuxin_talent_collaborator_rows"]

# 人才档/合作表列名
jc.execute("DESC ads_talent_profile")
prof_cols = [r[0] for r in jc.fetchall()]
facts["jiuxin_talent_profile_columns_sample"] = sorted(prof_cols[:40])
jc.execute("DESC ads_talent_collaborator")
coll_cols = [r[0] for r in jc.fetchall()]
facts["jiuxin_talent_collaborator_columns"] = coll_cols
strength_col = "collaboration_score" if "collaboration_score" in coll_cols else None
facts["jiuxin_collab_strength_col"] = strength_col

# ego 选择：合作度数 Top1（确定性：同度按 id 升序；实测 0.1s）
jc.execute("SELECT talent_id, COUNT(*) AS deg FROM ads_talent_collaborator "
           "GROUP BY talent_id ORDER BY deg DESC, talent_id ASC LIMIT 5")
top_degree = [[r[0], r[1]] for r in jc.fetchall()]
facts["jiuxin_talent_degree_top5"] = top_degree
ego_id, ego_deg = top_degree[0]
facts["jiuxin_ego_talent_id"] = ego_id

# ego 一跳邻居（实测 0.3s）
jc.execute("SELECT collaborator_talent_id FROM ads_talent_collaborator WHERE talent_id=%s LIMIT 500", (ego_id,))
neighbors = [r[0] for r in jc.fetchall()]
facts["jiuxin_ego_neighbor_count"] = len(neighbors)
nb = sorted(set(neighbors))
facts["jiuxin_ego_neighbor_frame"] = len(nb)
nb_set = set(nb)

# 邻居间诱导边：按 talent_id（分布键侧）IN 邻居框拉边，本地按对端过滤
# （实测：talent_id IN 500 → 69,524 行 16.7s 可行；collaborator_talent_id IN 大框 JOIN 超时 1105——路径在案）
induced_edges = set()
total_pairs = 0
batch = 250
for i in range(0, len(nb), batch):
    chunk = nb[i:i + batch]
    ph = ",".join(["%s"] * len(chunk))
    jc.execute(f"SELECT talent_id, collaborator_talent_id FROM ads_talent_collaborator "
               f"WHERE talent_id IN ({ph})", chunk)
    for u, v in jc.fetchall():
        total_pairs += 1
        if v in nb_set:
            key = (u, v) if u <= v else (v, u)
            induced_edges.add(key)
facts["jiuxin_ego_induced_edges"] = len(induced_edges)
facts["jiuxin_induced_pull_pairs_total"] = total_pairs

# ego 人才档属性样例（评估卡字段）
id_col = "talent_id" if "talent_id" in prof_cols else prof_cols[0]
jc.execute(f"SELECT * FROM ads_talent_profile WHERE {id_col}=%s LIMIT 1", (ego_id,))
ego_row = jc.fetchone()
facts["jiuxin_ego_profile_sample_fields"] = [str(x)[:60] if x is not None else None for x in (ego_row or [])][:12]

# 成果关联（引进评估三联边的「成果」侧）：co_paper/co_project/co_patent 聚合在邻居框上
jc.execute("SELECT SUM(co_paper_count), SUM(co_project_count), SUM(co_patent_count) "
           "FROM ads_talent_collaborator WHERE talent_id=%s", (ego_id,))
sp, sq, spt = jc.fetchone()
facts["jiuxin_ego_co_paper_total"] = int(sp or 0)
facts["jiuxin_ego_co_project_total"] = int(sq or 0)
facts["jiuxin_ego_co_patent_total"] = int(spt or 0)
jx.close()

derived = []
n = len(nb)
possible = n * (n - 1) // 2
density = round(len(induced_edges) / possible, 6) if possible else None
derived.append({
    "source": "jiuxin.ads_talent_profile + ads_talent_collaborator ego 诱导子图",
    "ego_talent_id": str(ego_id),
    "ego_degree": ego_deg,
    "neighbors_frame": n,
    "induced_edges_within_neighbors": len(induced_edges),
    "derived_density": density,
    "denominator_note": f"induced_edges({len(induced_edges)})/C({n},2)={possible}",
    "co_output_totals": {"co_paper": int(sp or 0), "co_project": int(sq or 0), "co_patent": int(spt or 0)},
})

absence_probe = [
    {"what": "dev 现成「专家引进评估子图」结果面/查询资产登记面", "how": "dev 表名词族扫描（asset/subgraph/kg_）+图词族 26 张计数",
     "hits": "图词族 26 张全 0 行（族级快照）；查询资产登记面不存在（资产清单只在 UI mockData.js 硬编码 8 条）"},
    {"what": "gkx 专家-项目-成果关联边（引进评估三联边）", "how": "gkx 280 表词族扫描（project/achievement/expert_introduction）",
     "hits": "0——gkx 有学者合作边（coauthor 1,187,606）无「引进评估」业务面"},
    {"what": "久新专家引进评估结果面", "how": "久新 218 表词族扫描（introduction/recruit/expert_assess）",
     "hits": "0——无业务评估面，但人才档+合作边两表齐备可构建子图"},
]

support = "完全转换支持" if facts.get("jiuxin_ego_neighbor_count", 0) > 0 else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_004", "metric_name": "专家引进评估子图（科技知识图谱·图查询资产·深析抽屉）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["子图为 2026-11-02 live 截面快照，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support, "| ego", ego_id, "deg", ego_deg, "nb", n, "edges", len(induced_edges))
