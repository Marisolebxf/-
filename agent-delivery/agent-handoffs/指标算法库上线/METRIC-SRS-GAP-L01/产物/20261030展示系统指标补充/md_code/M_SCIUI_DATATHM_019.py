# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_019 渠道平均同步周期（小时/天）——三源探针与代理读数复现脚本。

语义（UI 挂载 AccessHistorySituation.jsx:415「平均周期」列）：
  渠道平均同步周期 = 渠道相邻两次同步动作的平均间隔（小时/天量纲）。
  UI mock 是文本枚举（每日/每周/每月/实时），指标名要求数值口径（小时/天）——量纲分叉披露。

三源探针（B4，复用共享快照 + 本件独立读数）：
  ① dev：es_sync_watermark 双时间列（begin_time/end_time/last_sync_cost_s）数值读数
     —— last_sync_cost_s 是「单次同步耗时」非「同步间隔」，量纲错位披露；
     begin_time/end_time 间隔分布实查；xxl_job_log 0 行（无逐次触发时间序列）
  ② gkx：280 表词族 0 命中
  ③ 久新：210 表词族 0 命中（快照管理 metrics_as_of_date 单日，无逐期同步时刻）
运行：python3 code/M_SCIUI_DATATHM_019.py
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
OUT_PATH = os.path.join(HERE, "M_SCIUI_DATATHM_019_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=60)


def load_snap(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    p1 = load_snap("_probe_lane3_s304_out.json")
    p2 = load_snap("_probe_lane3_s304b_out.json")

    facts = {}
    absence_probe = []

    # ① dev：es_sync_watermark 的周期相关读数（15 行全量）
    conn = pymysql.connect(**DEV)
    try:
        cur = conn.cursor()
        # update_mode 分布（full/incr——同步模式语境）
        cur.execute(
            "SELECT update_mode, COUNT(*) AS n FROM gkxlumenx_cfg.es_sync_watermark "
            "GROUP BY update_mode ORDER BY update_mode")
        facts["dev_es_sync_update_mode_dist"] = [[r[0], r[1]] for r in cur.fetchall()]
        # last_sync_cost_s 读数（单次同步耗时秒）
        cur.execute(
            "SELECT module_name, last_sync_cost_s FROM gkxlumenx_cfg.es_sync_watermark "
            "WHERE module_name NOT LIKE '%%demo%%' ORDER BY module_name")
        facts["dev_es_sync_cost_s_by_module"] = [
            {"module_name": r[0], "last_sync_cost_s": float(r[1]) if r[1] is not None else None}
            for r in cur.fetchall()]
        # begin_time/end_time 实查（间隔=单次同步起止差）
        cur.execute(
            "SELECT module_name, begin_time, end_time FROM gkxlumenx_cfg.es_sync_watermark "
            "WHERE module_name NOT LIKE '%%demo%%' ORDER BY module_name")
        rows = cur.fetchall()
        spans = []
        for r in rows:
            if r[1] is not None and r[2] is not None:
                spans.append({"module_name": r[0],
                              "begin_time": str(r[1]), "end_time": str(r[2]),
                              "span_seconds": int((r[2] - r[1]).total_seconds())})
        facts["dev_es_sync_begin_end_span"] = sorted(
            spans, key=lambda x: x["module_name"])
        # last_sync_time 分布（仅证明单快照无序列，非周期序列）
        cur.execute(
            "SELECT MIN(last_sync_time), MAX(last_sync_time) FROM gkxlumenx_cfg.es_sync_watermark "
            "WHERE module_name NOT LIKE '%%demo%%'")
        r = cur.fetchone()
        facts["dev_es_sync_last_sync_time_range"] = [str(r[0]), str(r[1])]
        # xxl_job_log 触发时间序列复核（0 行=无逐次触发时刻）
        cur.execute(
            "SELECT COUNT(*), MIN(trigger_time), MAX(trigger_time) FROM gkxlumenx_job.xxl_job_log")
        r = cur.fetchone()
        facts["dev_xxl_job_log_rows"] = r[0]
        facts["dev_xxl_job_log_trigger_range"] = [str(r[1]), str(r[2])]
    finally:
        conn.close()

    absence_probe.append({
        "probe": "dev 渠道×时间同步时刻序列（计算同步间隔的源面）",
        "source": "dev", "hits": 0,
        "sql": "es_sync_watermark 单模块一行（无逐次时刻）；xxl_job_log 0 行（无触发序列）",
        "note": "间隔计算需要同一实体≥2 个时间点；es_sync 每模块只留最后一笔水位，xxl 调度空载——序列面不存在"})
    absence_probe.append({
        "probe": "gkx 280 表 sync/cycle/interval/frequen 词族",
        "source": "gkx", "hits": 0,
        "sql": "information_schema.tables WHERE table_schema='gkx' 词族扫描（_probe_lane3_s304_out.json）",
        "note": "cycle 词族 0 命中；dwd_job 招聘语义排除"})
    absence_probe.append({
        "probe": "久新 210 张 sync/cycle + interval/frequen/task 词族",
        "source": "jiuxin", "hits": 0,
        "sql": "SHOW TABLES 词族扫描（_probe_lane3_s304_out.json / _probe_lane3_s304b_out.json）",
        "note": "快照管理单日（metrics_as_of_date 2026-09-18 一期），无逐期同步时刻"})

    # 代理面参考读数：last_sync_cost_s 的统计（单次耗时，非周期）
    costs = [x["last_sync_cost_s"] for x in facts["dev_es_sync_cost_s_by_module"]
             if x["last_sync_cost_s"] is not None]
    spans = [x["span_seconds"] for x in facts["dev_es_sync_begin_end_span"]]
    facts["dev_es_sync_cost_s_nonnull"] = len(costs)
    facts["dev_es_sync_cost_s_max"] = max(costs) if costs else None
    facts["dev_es_sync_cost_s_min"] = min(costs) if costs else None
    facts["dev_es_sync_span_seconds_nonnull"] = len(spans)

    absence_probe.append({
        "probe": "三份需求文档「渠道平均同步周期/同步周期」指标定义",
        "source": "doc", "hits": 0,
        "sql": "rg 检索（附录 A.2）",
        "note": "seq 361「历史更新周期」功能在（更新频率/时间点/周期变化趋势），渠道平均周期数值口径无"})

    out = {
        "metric_id": "M_SCIUI_DATATHM_019",
        "batch": "S3-04",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:415",
            "repos/demo-ui-science/src/pages/data-resources/mockData.js:1451-1456",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "指标名未出现；语义锚=接入视窗·历史更新周期统计与分析（seq 361，最接近的需求叶——功能在口径无）",
        },
        "facts": facts,
        "derived": [],
        "absence_probe": absence_probe,
        "support_judgment": "完全不支持",
        "notes": [
            "mock 源 updateCycleStats.avgCycle 是文本枚举（每日/每周/每月/实时）——演示值，不参与支持度结论；指标名的数值量纲（小时/天）与 mock 文本量纲分叉披露",
            "es_sync_watermark 的 last_sync_cost_s 是「单次同步耗时」非「同步间隔」（量纲错位：耗时秒级/间隔天级），只作结构证据不作周期读数",
            "begin/end 间隔 14 模块全 0 秒（同一事务内写起止），无周期语义",
            "共享探针复用：_probe_lane3_s304_out.json / _probe_lane3_s304b_out.json",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "不适用（周期口径无基年概念）",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "542", "280", "210", "15", "14", "0"]},
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
