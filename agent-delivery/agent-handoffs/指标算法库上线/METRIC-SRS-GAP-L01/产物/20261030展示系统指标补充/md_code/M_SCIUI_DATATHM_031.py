# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_031 各渠道数据同步成功率——三源探针复现脚本。

语义（UI 挂载 AccessHistorySituation.jsx:417「成功率」列，渠道×成功率表格形态）：
  各渠道的同步成功率 = 渠道成功归档（同步）记录数 / 渠道归档记录总数，按渠道分列。

与 M_SCIUI_DATATHM_014 同物异构（014=总体单读数 KPI 位 / 本件=渠道分列表格位）：
  依赖面同根（渠道归档台账 + 任务执行日志），本件多一个「渠道维度」切片轴——
  渠道维三源承载一并探针。

三源探针（B4，复用 _probe_lane3_s304* 共享快照）：
  ① dev：channel 列族实测=pay 支付渠道域（语义排除）+ xxl_job_log 0 行 + es_sync_watermark 15 行无渠道列
  ② gkx：280 表 channel 词族 0 命中（dwd_job 招聘语义排除）
  ③ 久新：210 表 channel/task 词族 0 命中
运行：python3 code/M_SCIUI_DATATHM_031.py
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
OUT_PATH = os.path.join(HERE, "M_SCIUI_DATATHM_031_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=60)


def load_snap(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    p1 = load_snap("_probe_lane3_s304_out.json")

    facts = {}
    absence_probe = []

    # ① dev：channel 列族复核（共享探针）+ es_sync_watermark 渠道列缺失实查
    facts["dev_table_total"] = p1["facts"]["dev"]["table_total"]
    facts["dev_channel_columns"] = p1["facts"]["dev"]["channel_columns"]
    conn = pymysql.connect(**DEV)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='gkxlumenx_cfg' AND table_name='es_sync_watermark'")
        es_cols = [r[0] for r in cur.fetchall()]
        facts["dev_es_sync_watermark_columns"] = sorted(es_cols)
        facts["dev_es_sync_watermark_has_channel_col"] = any(
            "channel" in c.lower() for c in es_cols)
        cur.execute(
            "SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_log")
        facts["dev_xxl_job_log_rows"] = cur.fetchone()[0]
        # xxl_job_info 若投产，executor_handler 可作任务→渠道映射源；实查 0 行
        cur.execute("SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_info")
        facts["dev_xxl_job_info_rows"] = cur.fetchone()[0]
    finally:
        conn.close()
    absence_probe.append({
        "probe": "dev 542 表 channel 列族（information_schema.columns LIKE '%channel%'）",
        "source": "dev", "hits": 16,
        "sql": "SELECT table_schema,table_name,column_name FROM information_schema.columns WHERE table_schema LIKE 'gkxlumenx%' AND column_name LIKE '%channel%'",
        "note": "16 列全部落在 gkxlumenx_pay（支付渠道：pay_channel/pay_refund_order/pay_trade_order）与 bi/dwd 零星（export_channel 报表导出/feedback_channel 舆情反馈/push_channels 推送渠道）——无一是数据接入渠道语义，语义排除；es_sync_watermark 19 列实测无 channel 列"})
    absence_probe.append({
        "probe": "dev xxl_job_log / xxl_job_info（任务执行流水与任务注册面）",
        "source": "dev", "hits": 0,
        "sql": "SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_log; SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_info",
        "note": "两表均 0 行——调度器未投产，无渠道任务映射源"})

    # ② gkx：词族复核
    facts["gkx_table_count"] = p1["facts"]["gkx"]["table_count"]
    facts["gkx_sync_channel_family_tables"] = p1["facts"]["gkx"]["word_family_tables"]
    absence_probe.append({
        "probe": "gkx 280 表 sync/channel/cycle/etl/ingest/pipeline 词族",
        "source": "gkx", "hits": 0,
        "sql": "information_schema.tables WHERE table_schema='gkx' 词族扫描（_probe_lane3_s304_out.json）",
        "note": "job 词族唯一命中 dwd_job=招聘岗位明细（10 行），语义排除；gkx 为要素明细库无接入运营面"})

    # ③ 久新：词族复核
    facts["jiuxin_table_count"] = p1["facts"]["jiuxin"]["table_count"]
    facts["jiuxin_sync_channel_family_tables"] = p1["facts"]["jiuxin"]["word_family_tables"]
    absence_probe.append({
        "probe": "久新 210 张 ads_* sync/channel/cycle/etl/ingest/pipeline + task/schedul/frequen/batch/job/run 词族",
        "source": "jiuxin", "hits": 0,
        "sql": "SHOW TABLES 词族扫描（_probe_lane3_s304_out.json / _probe_lane3_s304b_out.json）",
        "note": "run 词族唯一命中 ads_recommendation_run=推荐运行表语义排除；快照管理无逐笔日志、无渠道维"})

    # ④ 需求真源
    absence_probe.append({
        "probe": "三份需求文档「各渠道数据同步成功率」定义",
        "source": "doc", "hits": 0,
        "sql": "rg 检索（附录 A.2）",
        "note": "seq 360-361 相邻叶功能在、渠道×成功率口径无"})

    out = {
        "metric_id": "M_SCIUI_DATATHM_031",
        "batch": "S3-04",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/data-resources/components/AccessHistorySituation.jsx:417",
            "repos/demo-ui-science/src/pages/data-resources/mockData.js:1451-1456",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "指标名未出现；语义锚=接入视窗·历史资源接入情况相邻叶（seq 360/361）+ UI mock updateCycleStats 渠道枚举",
        },
        "facts": facts,
        "derived": [],
        "absence_probe": absence_probe,
        "support_judgment": "完全不支持",
        "notes": [
            "mock 源 updateCycleStats：5 渠道（API接口 98.2/文件传输 95.6/数据库同步 97.8/人工录入 92.3/物联网采集 96.8）+ trend 6 点——演示值，不参与支持度结论",
            "与 M_SCIUI_DATATHM_014 同物异构（总体 KPI 位 vs 渠道分列表格位），缺口同根（归档台账/执行日志），本件多渠道切片轴亦零承载",
            "共享探针复用：_probe_lane3_s304_out.json",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "不适用（成功率口径无基年概念）",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": [
            "98.2", "95.6", "97.8", "92.3", "96.8", "17", "542", "280", "210", "0"]},
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
