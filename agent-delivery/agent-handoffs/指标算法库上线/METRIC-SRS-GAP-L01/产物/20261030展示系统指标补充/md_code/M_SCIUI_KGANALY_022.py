#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_022 图谱实体增量（每分钟）— 三源时间维负证据（与 007 同判共证据）+ 判档产物
UI 挂载：realtimeMonitor.js:6（MONITOR_METRICS 首卡：key=entityRate, label=实体增量/分钟, unit=条,
  threshold=400, warnHigh）→ RealtimeMonitorPanel.jsx setInterval 3s 随机游走模拟（初值 168 条/分钟）。
与 007（关系增量/分钟）同面板同数据流同判：分钟级增量要求逐条入库时间戳或事件流——
  ①久新图单版本批处理快照（node 表 19,430 行 update_time 全表单值 2026-10-26 06:00:00、data_version 单版本）
  ②gkx 学者要素表 create_time 天级 ETL 回填 ③dev 无接入事件面。
007 探针（M_SCIUI_KGANALY_007.py）已覆盖边表时间维；本脚本补节点表侧证（update_time/data_version 分布）后同判。
"""
import json, os, time
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_022_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = ("realtimeMonitor.js:5-10 MONITOR_METRICS 首卡（:6 key=entityRate, label=实体增量/分钟, "
                     "unit=条, threshold=400, warnHigh）；RealtimeMonitorPanel.jsx:26-36 setInterval 3s "
                     "tickMonitorSnapshot 随机游走（±9% jitter，下限 50），初值 168 条/分钟")
facts["ui_init_value"] = 168
facts["ui_threshold"] = 400
facts["sibling_007_note"] = ("姊妹件 M_SCIUI_KGANALY_007（关系增量/分钟，:7 第二卡）已判完全不支持——"
                             "同面板四卡同吃一条数据流；本件共享其三源时间维负证据，仅计数对象从边换节点")

# ---------- 久新节点表时间维侧证（007 探边表，本件补节点表） ----------
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
jc.execute("SELECT MIN(update_time), MAX(update_time) FROM ads_technology_graph_node")
mn, mx = jc.fetchone()
facts["jiuxin_node_update_time_range"] = {"min": str(mn), "max": str(mx),
                                          "single_value": str(mn) == str(mx)}
jc.execute("SELECT data_version, COUNT(*) FROM ads_technology_graph_node GROUP BY data_version")
facts["jiuxin_node_data_version_dist"] = [[str(r[0]), r[1]] for r in jc.fetchall()]
jx.close()

absence_probe = [
    {"what": "dev 分钟级节点接入事件面",
     "how": "dev 542 表词族（ingest/stream/event_log/node）+族级快照",
     "hits": "0——sys_audit_log 0 行；sys_log 用户操作日志语义排除；dev 图表面 26 张全 0 行（族级快照在案）"},
    {"what": "久新节点表逐条入库时间戳/版本序列",
     "how": "ads_technology_graph_node update_time MIN/MAX + data_version GROUP BY（本脚本实测）",
     "hits": f"update_time 全表单值 {str(mn)}（MIN=MAX）；data_version 单版本 {facts['jiuxin_node_data_version_dist']}——"
             "批处理覆盖写入，无行级时间、无历史版本"},
    {"what": "gkx 节点侧分钟级时间维",
     "how": "M_SCIUI_KGANALY_007.py 探针（dwd_scholar create_time 天级回填分布）",
     "hits": "天级 ETL 回填（4 批次日级分布，末日 94.5%）——回填吞吐≠图谱增长，且天级非分钟级"},
]

derived = [
    {"formula": "entityRate_t = |{n : n 在 [t-1min, t) 入库}|（UI 语义）",
     "derived": "三源无分钟级事件流/行级时间戳——不可算",
     "note": "与 007（边增量）同构：监控面板四卡共享时间维负证据"},
    {"formula": "可转换最低粒度=快照间增量 |N_v2|-|N_v1|",
     "derived": f"久新单版本快照（{facts['jiuxin_nodes_total']} 节点、data_version 单值）——无第二版本可比",
     "note": "版本保留（多 data_version 落盘）可升部分支持（天/周级）；分钟级须接入层事件流立项"},
]

support = "完全不支持"
out = {"metric_id": "M_SCIUI_KGANALY_022", "metric_name": "图谱实体增量（每分钟）（科技知识图谱·实时监控·实体增量卡）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "support_rationale": ("分钟级实体增量要求逐条入库时间戳或事件流，三源均无：久新节点表 19,430 行 "
                             "update_time 全表单值（批处理覆盖）、data_version 单版本；gkx 天级回填；dev 无事件面。"
                             "与 007（关系增量）同面板同判共证据，仅计数对象从边换节点"),
       "base_years_used": [], "base_years_missing": ["实体增量为分钟级速率读数，无年度基期维"],
       "base_years_note": "物理口径基期=探针快照日；速率类读数非年度基期概念"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT, "| support:", support,
      "| node update_time single:", facts["jiuxin_node_update_time_range"]["single_value"],
      "| versions:", len(facts["jiuxin_node_data_version_dist"]))
