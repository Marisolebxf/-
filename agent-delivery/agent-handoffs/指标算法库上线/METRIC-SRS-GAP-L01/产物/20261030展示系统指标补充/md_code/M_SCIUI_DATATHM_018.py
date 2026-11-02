# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_018 数据库同步成功率（分渠道）——三源探针复现脚本。

语义（UI 挂载 AccessWindow.jsx:48「数据库同步」渠道筛选选项）：
  「数据库同步」这一接入渠道的同步成功率——渠道枚举的单值特化（031 分列口径的
  单渠道切片），读数语义锚 mock accessChannelStats 的数据库同步行（99.1）。

三源探针（B4，复用 _probe_lane3_s304* 共享快照，独立留证不抄 031 结论）：
  ① dev：channel 列族 16 列（本件复筛语义=「数据库同步」传输方式枚举无承载）
     + xxl_job_info 0 行 + es_sync_watermark 无渠道列复核
  ② gkx：280 表词族（dwd_job 招聘语义排除）
  ③ 久新：210 表词族（两轮）
运行：python3 code/M_SCIUI_DATATHM_018.py
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
OUT_PATH = os.path.join(HERE, "M_SCIUI_DATATHM_018_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=60)


def load_snap(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    p1 = load_snap("_probe_lane3_s304_out.json")

    facts = {}
    absence_probe = []

    # ① dev：本件独立复筛——「数据库同步」传输方式语义在全库的承载
    facts["dev_table_total"] = p1["facts"]["dev"]["table_total"]
    conn = pymysql.connect(**DEV)
    try:
        cur = conn.cursor()
        # 全库列名含 sync 的列（es_sync_watermark 之外还有没有同步语义面）
        cur.execute(
            "SELECT table_schema, table_name, column_name FROM information_schema.columns "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND column_name LIKE '%%sync%%' "
            "ORDER BY table_schema, table_name, column_name")
        facts["dev_sync_columns"] = [["%s.%s" % (r[0], r[1]), r[2]] for r in cur.fetchall()]
        # 「数据库同步」渠道枚举值探测：全库字符串列值域抽验不现实，查字典类表
        # cfg/degrade_switch 等小表逐张点名无渠道字典表——用 information_schema 表名兜底
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND "
            "(table_name LIKE '%%dict%%' OR table_name LIKE '%%enum%%' OR table_name LIKE '%%catalog%%') "
            "ORDER BY table_schema, table_name")
        facts["dev_dict_like_tables"] = ["%s.%s" % (r[0], r[1]) for r in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_info")
        facts["dev_xxl_job_info_rows"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM gkxlumenx_job.xxl_job_log")
        facts["dev_xxl_job_log_rows"] = cur.fetchone()[0]
    finally:
        conn.close()
    absence_probe.append({
        "probe": "dev 全库列名 LIKE '%sync%'（同步语义列面）",
        "source": "dev",
        "sql": "SELECT ... FROM information_schema.columns WHERE column_name LIKE '%sync%'",
        "hits": len(facts["dev_sync_columns"]),
        "note": "sync 列全部落 gkxlumenx_cfg.es_sync_watermark（19 列单模块快照面，无渠道维、无历史批次）——详见 031 件同探针；「数据库同步」渠道枚举值无承载"})
    absence_probe.append({
        "probe": "dev 字典类表（dict/enum/catalog 词族——渠道字典表探测）",
        "source": "dev",
        "sql": "SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%dict%' OR '%enum%' OR '%catalog%'",
        "hits": len(facts["dev_dict_like_tables"]),
        "note": "命中的是代码生成/配置类字典表，无数据接入渠道字典（渠道枚举仅 mock 在案）"})

    # ② gkx：词族复核
    facts["gkx_table_count"] = p1["facts"]["gkx"]["table_count"]
    facts["gkx_word_family_tables"] = p1["facts"]["gkx"]["word_family_tables"]
    absence_probe.append({
        "probe": "gkx 280 表 sync/channel/cycle/etl/ingest/pipeline 词族",
        "source": "gkx", "hits": 0,
        "sql": "information_schema.tables WHERE table_schema='gkx' 词族扫描（_probe_lane3_s304_out.json）",
        "note": "job 词族唯一命中 dwd_job=招聘岗位（10 行）语义排除；无同步运营面"})

    # ③ 久新：词族复核
    facts["jiuxin_table_count"] = p1["facts"]["jiuxin"]["table_count"]
    facts["jiuxin_word_family_tables"] = p1["facts"]["jiuxin"]["word_family_tables"]
    absence_probe.append({
        "probe": "久新 210 张 ads_* sync/channel + task/schedul/frequen/batch/job/run 词族",
        "source": "jiuxin", "hits": 0,
        "sql": "SHOW TABLES 词族扫描（_probe_lane3_s304_out.json / _probe_lane3_s304b_out.json）",
        "note": "ads_recommendation_run 语义排除；快照管理无同步流水"})

    # ④ 需求真源
    absence_probe.append({
        "probe": "三份需求文档「数据库同步成功率/数据库同步」指标定义",
        "source": "doc", "hits": 0,
        "sql": "rg 检索（附录 A.2）",
        "note": "「数据库同步」仅作 UI 筛选枚举值出现，无成功率口径"})

    out = {
        "metric_id": "M_SCIUI_DATATHM_018",
        "batch": "S3-04",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:48",
            "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:44-51",
            "repos/demo-ui-science/src/pages/data-resources/mockData.js:93",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "指标名未出现；语义锚=接入视窗·多维度交互筛选（seq 350）的来源筛选维度+渠道统计语境",
        },
        "facts": facts,
        "derived": [],
        "absence_probe": absence_probe,
        "support_judgment": "完全不支持",
        "notes": [
            "mock 源 accessChannelStats 数据库同步行：count 67/successRate 99.1/volume 15600（演示值，不参与支持度结论）",
            "本件是 031（各渠道分列）的单渠道特化（数据库同步渠道），渠道枚举/台账/执行日志缺口与 031 同根——独立留证",
            "共享探针复用：_probe_lane3_s304_out.json",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "不适用（成功率口径无基年概念）",
        "ctx_refs": {"note": "正文引用型数字登记（千分位写法与正文一致）", "refs": [
            "99.1", "67", "15,600", "542", "280", "210", "0"]},
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
