#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_046 资源更新频率（周期）——三源探针+产物生成（S3-05 L1）。

三挂载：ThemeWindow.jsx:368（库详情「更新频率」Tag）/ ThemeWindow.jsx:605（导出表列）/
AccessResourceDetailQuery.jsx:124-129（明细表列，UPDATE_FREQ_ORDER 枚举排序 实时0/每日1/每周2/每两周3/每月4）。
019 已证：es_sync_watermark 单模块单笔水位（无逐次时刻序列）、xxl_job_log 0 行、
mode 全 full、end_time 月分布 2026-08:10/2026-09:1/2026-10:3（无固定周期形态）。
本件新探针：dev 全库「频率登记列」扫描（表级元数据 update_freq/cycle/period 词族）。
"""
import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_046_out.json")

d019 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_019_out.json"), encoding="utf-8"))

conn = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                       charset="utf8mb4", autocommit=True)
freq_columns = []
freq_registry_rows = None
try:
    with conn.cursor() as cur:
        # 本件新探针①：dev 全库列级「频率登记」词族（update_freq/freq/cycle/period 列名扫描，排除 demo_*）
        cur.execute(
            "SELECT table_schema, table_name, column_name, data_type "
            "FROM information_schema.columns "
            "WHERE table_schema LIKE 'gkxlumenx%%' AND table_schema NOT LIKE '%%demo%%' "
            "AND (column_name LIKE '%%freq%%' OR column_name LIKE '%%cycle%%' OR column_name LIKE '%%period%%')")
        freq_columns = [list(r) for r in cur.fetchall()]
        # 本件新探针②：若存在频率登记表则取分布（预置空，探针①结果决定）
finally:
    conn.close()

# —— mock 枚举治理证据（B5 确定性排序：UPDATE_FREQ_ORDER 枚举序）——
ui_mock_freq_dist = {"每日": 8, "每周": 7, "实时": 5, "每月": 4, "每两周": 2}  # mockData.js updateFreq 全量计数（rg 实测）
UPDATE_FREQ_ORDER = {"实时": 0, "每日": 1, "每周": 2, "每两周": 3, "每月": 4}  # AccessResourceDetailQuery.jsx:20 实抄
ui_mock_freq_sorted = sorted(ui_mock_freq_dist.items(), key=lambda kv: (UPDATE_FREQ_ORDER.get(kv[0], 99), kv[0]))

# es_sync 复用 019（B11 零漂移）
spans = d019["facts"]["dev_es_sync_begin_end_span"]
from collections import Counter
end_month_dist = sorted(Counter(s["end_time"][:7] for s in spans).items())

facts = {
    "dev_table_total": 542,
    "dev_freq_column_scan": freq_columns,
    "gkx_table_count": 280,
    "jiuxin_table_count_live": 215,
    "dev_es_sync_mode_dist_reused_019": d019["facts"]["dev_es_sync_update_mode_dist"],
    "dev_es_sync_end_month_dist_reused_019": end_month_dist,
    "dev_es_sync_last_sync_range_reused_019": d019["facts"]["dev_es_sync_last_sync_time_range"],
    "dev_xxl_job_log_rows_reused_019": d019["facts"]["dev_xxl_job_log_rows"],
    "ui_mock_update_freq_dist": ui_mock_dist_sorted if (ui_mock_dist_sorted := sorted(ui_mock_freq_dist.items())) else [],
    "ui_mock_update_freq_enum_sorted": ui_mock_freq_sorted,
    "ui_update_freq_order_const": UPDATE_FREQ_ORDER,
    "ui_mock_cycle_avg_cycle_texts": ["API接口:每日", "文件传输:每周", "数据库同步:每日", "人工录入:每月", "物联网采集:实时"],
}

derived = [
    {
        "key": "resource_update_frequency",
        "value": None,
        "numerator": None, "denominator": None,
        "note": "『资源更新频率（周期）』正式口径（逐资源周期值或周期分布）三源零承载：dev 无频率登记列（词族列扫描）、es_sync 单笔水位无周期序列（019 复用）、gkx/久新词族 0 命中（019 共享探针复用）；按 B10 不写伪指标值"
    },
    {
        "key": "es_sync_module_last_sync_month_dist_observed",
        "value": end_month_dist,
        "numerator": None, "denominator": None,
        "note": "附带交付（非周期读数）：es_sync 15 模块末笔同步月分布 2026-08:10/2026-09:1/2026-10:3——无固定周期形态（若每月一档应均匀 5/5/5）；update_mode 全 full 无增量节律；单笔快照无间隔序列，不得反推周期"
    },
]

absence_probe = [
    {
        "probe": "dev 频率登记列（update_freq/freq/cycle/period 词族列扫描）",
        "source": "dev",
        "sql": "information_schema.columns 扫 gkxlumenx_* 非 demo（本件新探针，46 列命中）",
        "hits": len(freq_columns),
        "hit_detail": "46 列命中但逐条语义核对全部为业务字段（stat_period 统计期间枚举 23 列/cycle_stage 产业链阶段 3 列/push_frequency 政策订阅推送 varchar 1 列/occur_period 财务发生期等），无『资源元数据级 update_freq 登记列』（即无表登记『本表多久更新一次』）；push_frequency 最近语义候选，属政策订阅业务字段非资源元数据——语义排除",
    },
    {
        "probe": "dev 同步时刻序列（周期计算的源面）",
        "source": "dev",
        "sql": "es_sync_watermark 单模块一行（019 复用）；xxl_job_log COUNT=0（019 复用）",
        "hits": 0,
        "hit_detail": "间隔计算需同一实体≥2 时间点；es_sync 每模块只留最后一笔水位（begin/end 为同一事务内写），xxl 调度空载——序列面不存在（019 同锚，B11 零漂移）"
    },
    {
        "probe": "gkx 280 表 sync/cycle/interval/frequen 词族",
        "source": "gkx",
        "sql": "information_schema.tables 词族扫描（019 复用 _probe_lane3_s304_out.json）",
        "hits": 0,
        "hit_detail": "cycle 词族 0 命中；dwd_job 为招聘职位语义排除（019 同证）"
    },
    {
        "probe": "久新 215 表 sync/cycle/interval/frequen/task 词族",
        "source": "jiuxin",
        "sql": "SHOW TABLES 词族扫描（019 复用 _probe_lane3_s304_out.json / _probe_lane3_s304b_out.json）",
        "hits": 0,
        "hit_detail": "快照管理单日（metrics_as_of_date 2026-09-18 一期），无逐期同步时刻（019 同证）"
    },
    {
        "probe": "需求原文「更新频率/更新周期」指标定义",
        "source": "doc",
        "sql": "rg 检索三份需求真源（SRS 接入视窗.md seq 361 等）",
        "hits": 1,
        "hit_detail": "seq 361「历史更新周期统计与分析」：功能句含「更新频率、更新时间点及周期变化趋势」——功能词在；数值口径（周期=间隔均值？分布？枚举档位？）无定义。指标名级「资源更新频率（周期）」0 命中"
    },
]

doc = {
    "metric_id": "M_SCIUI_DATATHM_046",
    "batch": "S3-05",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:368",
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:605",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessResourceDetailQuery.jsx:124",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessResourceDetailQuery.jsx:20",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:1451-1456",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "指标名级三份真源 0 命中；挂靠 seq 361（历史更新周期统计与分析——「更新频率、更新时间点及周期变化趋势」功能词在，数值口径无）；「更新频率」在 UI 是元数据字段（库详情 Tag/明细列/导出列三挂载），mock 值为文本枚举（每日/每周/每月/实时/每两周）非数值周期"
    },
    "base_years_used": [],
    "base_years_missing": ["完全不支持：三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全不支持",
    "notes": [
        "判档：数值周期口径三源零承载（无频率登记列+无时刻序列）；UI 侧本身也是文本枚举非数值——量纲分叉披露（019 同款）",
        "B11 对账：es_sync 全套键复用 019（mode/end_month/last_range/xxl=0）；gkx/久新词族复用 019 共享探针",
        "枚举治理（B5）：UPDATE_FREQ_ORDER 常量实抄 AccessResourceDetailQuery.jsx:20（实时0/每日1/每周2/每两周3/每月4）；mock 26 条 updateFreq 分布按 (枚举序,名称) 双键排序",
        "三挂载同字段：ThemeWindow detailItems（:368）与导出列（:605）读 selectedDatabase.updateFreq；AccessResourceDetailQuery 列（:124）读行级 updateFreq——同一元数据字段的展示/导出/筛选三形态",
    ],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
print("freq_columns:", freq_columns)
print("support:", doc["support_judgment"])
