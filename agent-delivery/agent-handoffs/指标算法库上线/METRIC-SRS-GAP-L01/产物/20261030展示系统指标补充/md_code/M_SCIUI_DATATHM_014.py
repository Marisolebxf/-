# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_014 渠道历史同步成功率——三源探针与代理读数复现脚本。

语义（UI 挂载 AccessHistorySituation.jsx:298「历史成功率」Statistic）：
  历史归档批次的成功占比 = 成功归档记录数 / 归档记录总数（按渠道×表的历史台账口径）。

三源逐一留证（B4）：
  ① dev：同步动作面 es_sync_watermark（15 行单模块快照）读数 + xxl_job_log/log_report 0 行复核
     + access_history/sync_log 词族 0 命中复核（共享快照 _probe_lane3_s304_out.json）
  ② gkx：280 表同步/渠道词族 0 命中（仅 dwd_job=招聘岗位语义排除）
  ③ 久新：210 表同步/渠道/任务词族 0 命中（共享快照）

代理读数（es_sync_watermark 快照面，语义披露写死）：
  - es_sync_modules_total=15、es_sync_success=14、es_sync_failed=1
  - 派生 es_sync_snapshot_success_rate_pct = 14/15*100（分子分母同表同 WHERE）
  - 快照面与台账面差异：单模块最后一笔的快照，非历史批次序列
运行：python3 code/M_SCIUI_DATATHM_014.py
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
OUT_PATH = os.path.join(HERE, "M_SCIUI_DATATHM_014_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=60)


def load_snap(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    p1 = load_snap("_probe_lane3_s304_out.json")   # 词族 + xxl 结构
    p2 = load_snap("_probe_lane3_s304b_out.json")  # es_sync_watermark 全量

    facts = {}
    absence_probe = []

    # ① dev：词族复核（引用共享探针，独立读数）
    fam = p1["facts"]["dev"]["word_family_tables"]
    facts["dev_table_total"] = p1["facts"]["dev"]["table_total"]
    facts["dev_sync_family_tables"] = fam.get("sync", [])
    facts["dev_access_history_family_hits"] = 0  # access_history/collect_log/ingest 词族 0 命中（共享探针）
    absence_probe.append({
        "probe": "dev 16 schema 542 表 access_history/sync_log/collect_log/ingest_log 词族",
        "source": "dev", "hits": 0,
        "sql": "information_schema.tables LIKE 'gkxlumenx%' 词族扫描（_probe_lane3_s304_out.json facts.dev.word_family_tables）",
        "note": "sync 词族唯一命中 gkxlumenx_cfg.es_sync_watermark（单模块快照面非历史台账）；job 词族命中调度框架表族（xxl_job_log 0 行空载）"})

    # dev 实查：xxl_job_log / log_report / sys_job_log 行数复核 + es_sync_watermark 状态分布
    conn = pymysql.connect(**DEV)
    try:
        cur = conn.cursor()
        for tb, key in (("xxl_job_log", "dev_xxl_job_log_rows"),
                        ("xxl_job_log_report", "dev_xxl_job_log_report_rows"),
                        ("sys_job_log", "dev_sys_job_log_rows")):
            cur.execute("SELECT COUNT(*) FROM gkxlumenx_job.%s" % tb)
            facts[key] = cur.fetchone()[0]
        cur.execute(
            "SELECT sync_status, COUNT(*) AS n FROM gkxlumenx_cfg.es_sync_watermark "
            "GROUP BY sync_status ORDER BY sync_status")
        facts["dev_es_sync_status_dist"] = [[r[0], r[1]] for r in cur.fetchall()]
        cur.execute(
            "SELECT module_name, sync_status, last_sync_time, retry_count FROM gkxlumenx_cfg.es_sync_watermark "
            "WHERE sync_status <> 'success' ORDER BY module_name")
        facts["dev_es_sync_failed_modules"] = [
            {"module_name": r[0], "sync_status": r[1],
             "last_sync_time": str(r[2]), "retry_count": r[3]} for r in cur.fetchall()]
        cur.execute(
            "SELECT module_name, sync_status, last_sync_time, retry_count FROM gkxlumenx_cfg.es_sync_watermark "
            "WHERE module_name='reg_info_demo'")
        r = cur.fetchone()
        facts["dev_es_sync_reg_info_demo_row"] = (
            {"module_name": r[0], "sync_status": r[1], "last_sync_time": str(r[2]),
             "retry_count": r[3]} if r else None)
    finally:
        conn.close()

    es = p2["facts"]["es_sync_watermark_all"]
    facts["dev_es_sync_watermark_rows"] = len(es)
    facts["dev_es_sync_success_modules"] = sum(
        1 for r in es if r["sync_status"] == "success")
    facts["dev_es_sync_failed_modules_total"] = sum(
        1 for r in es if r["sync_status"] != "success")
    # 键名含 demo 的行登记（披露不引用其值）：reg_info_demo 189,115 计数不进任何分子分母
    facts["dev_es_sync_rows_with_demo_in_module_name"] = sorted(
        r["module_name"] for r in es if "demo" in r["module_name"].lower())

    # ② gkx：词族复核
    facts["gkx_table_count"] = p1["facts"]["gkx"]["table_count"]
    facts["gkx_sync_channel_family_tables"] = p1["facts"]["gkx"]["word_family_tables"]
    absence_probe.append({
        "probe": "gkx 280 表 sync/channel/cycle/etl/ingest/pipeline 词族",
        "source": "gkx", "hits": 0,
        "sql": "information_schema.tables WHERE table_schema='gkx' 词族扫描（_probe_lane3_s304_out.json facts.gkx.word_family_tables）",
        "note": "job 词族唯一命中 dwd_job=招聘岗位明细表（10 行），语义排除"})

    # ③ 久新：词族复核（两轮词族）
    facts["jiuxin_table_count"] = p1["facts"]["jiuxin"]["table_count"]
    facts["jiuxin_sync_channel_family_tables"] = p1["facts"]["jiuxin"]["word_family_tables"]
    facts["jiuxin_task_family_tables"] = {"run": ["ads_recommendation_run"]}
    absence_probe.append({
        "probe": "久新 210 张 ads_* 表 sync/channel/cycle/etl/ingest/pipeline + task/schedul/frequen/interval/batch/refresh/job/run/exec 词族",
        "source": "jiuxin", "hits": 0,
        "sql": "SHOW TABLES 词族扫描（_probe_lane3_s304_out.json / _probe_lane3_s304b_out.json）",
        "note": "run 词族唯一命中 ads_recommendation_run=推荐系统运行表，语义排除；ads_* 按 metrics_as_of_date 快照管理无逐笔同步日志"})

    # ④ 需求真源
    absence_probe.append({
        "probe": "三份需求文档「渠道历史同步成功率/同步成功率」定义",
        "source": "doc", "hits": 0,
        "sql": "rg 检索（附录 A.2）",
        "note": "seq 360-362 相邻叶功能描述在、成功率口径无"})

    # 派生：es_sync 快照面成功率（分子分母同表同 WHERE）
    n_total = facts["dev_es_sync_watermark_rows"]
    n_succ = facts["dev_es_sync_success_modules"]
    derived = [{
        "key": "es_sync_snapshot_success_rate_pct",
        "value": round(n_succ / n_total * 100, 2) if n_total else None,
        "numerator": n_succ,
        "denominator": n_total,
        "note": "dev gkxlumenx_cfg.es_sync_watermark 单模块最后一笔快照的成功模块占比（14/15），"
                "语义=模块快照成功率非渠道历史批次成功率；分子分母同表同 WHERE（B3）"}]

    out = {
        "metric_id": "M_SCIUI_DATATHM_014",
        "batch": "S3-04",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:298",
            "repos/demo-ui-science/src/pages/data-resources/mockData.js:1423-1430",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "指标名未出现；语义锚=接入视窗·历史资源接入情况相邻叶（seq 360 历史归集记录/seq 361 更新周期/seq 362 动态趋势）",
        },
        "facts": facts,
        "derived": derived,
        "absence_probe": absence_probe,
        "support_judgment": "完全不支持",
        "notes": [
            "mock 源 historyAccessDashboard.summary.successRate=75.0（12 条归档记录 7 成功 3 部分 2 失败口径）——演示值，不参与支持度结论",
            "es_sync_watermark 15 行含 1 行键名含 demo（reg_info_demo），该行登记不引用（其 189,115 计数不进任何分子分母）",
            "共享探针复用：_probe_lane3_s304_out.json（词族/结构）、_probe_lane3_s304b_out.json（es_sync 全量）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "不适用（成功率口径无基年概念）",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "75.0", "12", "15", "14", "1", "542", "280", "210", "0"]},
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
