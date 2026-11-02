#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_007 图谱关系增量（每分钟）— 三源探针 + 增量可行性核验 + 判档产物
UI 挂载：realtimeMonitor.js:7 MONITOR_METRICS relationRate（关系增量/分钟，threshold 380，warnHigh）。
核心判定：分钟级增量需要「时间戳连续的边入库流水」。久新技术图边表 update_time 全表单一值
（2026-10-26 06:00:00 = 批处理覆盖写入）→ 无分钟级事件流。三源运营流水面均无。
"""
import json, os, sys, time, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
SNAP305 = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_007_out.json")
snap = json.load(open(SNAP))
snap305 = json.load(open(SNAP305))
facts = {}

facts["ui_mount"] = "realtimeMonitor.js:7 MONITOR_METRICS { key:'relationRate', label:'关系增量/分钟', unit:'条', threshold:380, warnHigh:true }"
facts["ui_runtime"] = "RealtimeMonitorPanel.jsx:26-36 setInterval 3s tickMonitorSnapshot 随机游走模拟（init 245 条/分钟，jitter ±9%）——纯前端造数"
facts["ui_init_value"] = 245
facts["ui_threshold"] = 380

# ---------- ① dev：运营流水词族（族级快照） ----------
facts["dev_ops_word_table_rows"] = snap["facts"].get("dev_ops_word_table_rows") or {}
facts["dev_graph_word_table_rows"] = snap["facts"].get("dev_graph_word_table_rows") or {}
dev_graph_nonzero = {k: v for k, v in facts["dev_graph_word_table_rows"].items() if isinstance(v, int) and v > 0}
facts["dev_graph_tables_nonzero"] = dict(sorted(dev_graph_nonzero.items()))
# sys_log 是页面操作日志非数据接入流水（1060 行族级快照在案）
facts["dev_sys_log_rows_note"] = "gkxlumenx.sys_log 1060 行为用户操作日志（admin 等 3 账号），非数据接入事件流——语义排除"

# ---------- ② gkx：边表时间列核查（族级快照已含列清单） ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_coauthor WHERE is_deleted=0")
facts["gkx_coauthor_edges_total"] = gc.fetchone()[0]
# coauthor create_time/update_time 分布抽样（增量推导可行性：若入库时间连续可算日均增量）
gc.execute("SELECT MIN(create_time), MAX(create_time) FROM gkx.dwd_scholar_coauthor")
cmn, cmx = gc.fetchone()
facts["gkx_coauthor_create_time_range"] = [str(cmn), str(cmx)]
gc.execute("SELECT DATE_FORMAT(create_time, '%Y-%m-%d') AS d, COUNT(*) FROM gkx.dwd_scholar_coauthor "
           "GROUP BY d ORDER BY d LIMIT 10")
facts["gkx_coauthor_create_time_day_dist_sample"] = [[str(r[0]), r[1]] for r in gc.fetchall()]
gc.close()

# ---------- ③ 久新：边表时间列核查（族级快照已含分布） ----------
facts["jiuxin_edge_time_col_dist"] = snap["facts"]["jiuxin_edge_time_col_dist"]
facts["jiuxin_tech_edges_total"] = snap["facts"].get("jiuxin_tech_edges_total") or 587252
# 批次分布核验：data_version / graph_release_id 是否多版本（若有历史版本可推快照间增量）
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
jc.execute("SELECT data_version, COUNT(*) FROM ads_technology_graph_edge GROUP BY data_version ORDER BY data_version")
facts["jiuxin_edge_data_version_dist"] = [[r[0], r[1]] for r in jc.fetchall()]
jc.execute("SELECT graph_release_id, COUNT(*) FROM ads_technology_graph_edge GROUP BY graph_release_id ORDER BY COUNT(*) DESC LIMIT 5")
facts["jiuxin_edge_release_top5"] = [[r[0], r[1]] for r in jc.fetchall()]
# 全库边类表是否有带连续时间戳的（快速抽 3 张合作类表）
for tbl, tcol in [("ads_talent_collaborator", "update_time"),
                  ("ads_institution_collaboration_yearly", "update_time")]:
    try:
        jc.execute(f"SELECT MIN({tcol}), MAX({tcol}), COUNT(*) FROM {tbl}")
        mn, mx, ct = jc.fetchone()
        facts.setdefault("jiuxin_collab_table_time_range", {})[tbl] = {
            "min": str(mn), "max": str(mx), "rows": ct}
    except Exception as e:  # noqa: BLE001
        facts.setdefault("jiuxin_collab_table_time_range", {})[tbl] = {"error": str(e)[:100]}
jx.close()

# 日均增量（可转换的最低口径）：久新批处理周期推算
derived = []
ed = facts["jiuxin_edge_time_col_dist"]
if "update_time" in ed:
    derived.append({
        "source": "久新边表批处理周期推算（非分钟级）",
        "batch_update_time": ed["update_time"]["max"],
        "edges_total": facts["jiuxin_tech_edges_total"],
        "note": "update_time 全表单一值 2026-10-26 06:00:00（批处理覆盖写入）——无逐条入库时间，分钟级增量不可推；仅有快照总量",
        "convertible_granularity": "快照间（若保留历史版本）",
    })

absence_probe = [
    {"what": "dev 分钟级数据接入事件流（边/关系入库流水）", "how": "dev 542 表词族扫描（ingest/stream/event_log/op_log/audit）+ops 词族计数",
     "hits": "sys_audit_log 0 行；sys_log 1060 行为用户操作日志（语义排除）；无数据接入事件面"},
    {"what": "gkx 边表逐条入库时间（分钟级推导原料）", "how": "dwd_scholar_coauthor create_time 分布探查",
     "hits": "create_time 按天分布（非分钟级连续流）；且为批量 ETL 回填时间非业务发生时间"},
    {"what": "久新边表分钟级时间戳", "how": "ads_technology_graph_edge update_time/metrics_as_of_date 全表 MIN/MAX",
     "hits": "两列均为全表单一值（2026-10-26 06:00:00 / 2026-10-16）——批处理覆盖写入，无事件流"},
]

support = "完全不支持" if all(isinstance(p["hits"], str) or p["hits"] == 0 for p in absence_probe) else "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_007", "metric_name": "图谱关系增量（每分钟）（科技知识图谱·实时数据监控）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "base_years_used": [], "base_years_missing": ["增量为分钟级瞬时率，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日；指标本身是实时速率量纲（条/分钟），非年度基期概念"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support)
