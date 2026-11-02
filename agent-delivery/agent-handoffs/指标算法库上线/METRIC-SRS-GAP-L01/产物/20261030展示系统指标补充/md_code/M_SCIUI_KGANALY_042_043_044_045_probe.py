#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_042/043/044/045 模型/告警面四件合探 — 三源探针 + 判档产物（四件各落一 _out.json）
042 算法模型准确率：IndicatorDisplay.jsx:103 KPI「模型准确率 92.8%」（mock 常量；源头 OptimizeDecisionPanel perf.accuracy）
043 活跃告警条数：IndicatorDisplay.jsx:93 KPI「活跃告警数 3 个」（mock 常量；源头 alerts 数组）
044 模型漏检率：OptimizeDecisionPanel.jsx:359 Statistic「漏检率」（decisionModel.js summarizeRiskDetection 公式 mock）
045 模型误报率（目标域）：OptimizeDecisionPanel.jsx:381 Statistic「目标误报率」（applyFeedbackLoop 公式 mock）
四件同属「模型运营/告警事件」语义族：需要 模型版本+预测明细+人工标注（042/044/045）或 告警事件台账（043）。
探针：三源模型/告警/标注/训练词族逐一扫描留证。
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import jx_connect, gkx_connect, load_snap

BASE = os.path.dirname(os.path.abspath(__file__))
snap = load_snap()["facts"]
facts_common = {}

# dev：模型/告警词族表（dev 542 表全清单扫描——用 information_schema，一次拉全）
import pymysql
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      charset="utf8mb4", connect_timeout=10, read_timeout=120)
dc = dev.cursor()
dc.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES \
WHERE TABLE_SCHEMA LIKE 'gkxlumenx%'")
dev_tables = [(r[0], r[1]) for r in dc.fetchall()]
import re
model_words = re.compile(r"(model|train|predict|inference|version|deploy|algo)", re.I)
alert_words = re.compile(r"(alert|alarm|warn|risk_event|blacklist|trigger)", re.I)
label_words = re.compile(r"(label|annotat|feedback|review|audit)", re.I)
model_hits, alert_hits, label_hits = [], [], []
for sch, tab in sorted(dev_tables):
    if model_words.search(tab):
        model_hits.append(f"{sch}.{tab}")
    if alert_words.search(tab):
        alert_hits.append(f"{sch}.{tab}")
    if label_words.search(tab):
        label_hits.append(f"{sch}.{tab}")
facts_common["dev_model_word_tables"] = model_hits
facts_common["dev_alert_word_tables"] = alert_hits
facts_common["dev_label_word_tables"] = label_hits
# 逐一精确计数（小表直接 COUNT）
def count_rows(t):
    dc.execute(f"SELECT COUNT(*) FROM {t}")
    return dc.fetchone()[0]
facts_common["dev_model_word_table_rows"] = {t: count_rows(t) for t in sorted(model_hits)}
facts_common["dev_alert_word_table_rows"] = {t: count_rows(t) for t in sorted(alert_hits)}
facts_common["dev_label_word_table_rows"] = {t: count_rows(t) for t in sorted(label_hits)}
# 已在案的 dev 黑名单表面（S3-05 快照）+ 图表面全空
facts_common["dev_graph_word_table_rows"] = snap["dev_graph_word_table_rows"]
dev.close()

# gkx：模型/告警/标注词族（280 表）
gc = gkx_connect()
gc.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='gkx'")
gkx_tables = [r[0] for r in gc.fetchall()]
facts_common["gkx_model_word_tables"] = sorted(t for t in gkx_tables if model_words.search(t))
facts_common["gkx_alert_word_tables"] = sorted(t for t in gkx_tables if alert_words.search(t))
facts_common["gkx_label_word_tables"] = sorted(t for t in gkx_tables if label_words.search(t))

# 久新：模型/告警/标注词族（live SHOW TABLES 当日实测）
jx = jx_connect()
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_tables = [r[0] for r in jc.fetchall()]
facts_common["jiuxin_table_count_live"] = len(jx_tables)
facts_common["jiuxin_model_word_tables"] = sorted(t for t in jx_tables if model_words.search(t))
facts_common["jiuxin_alert_word_tables"] = sorted(t for t in jx_tables if alert_words.search(t))
facts_common["jiuxin_label_word_tables"] = sorted(t for t in jx_tables if label_words.search(t))
jx.close()

absence_probe = [
    {"what": "dev 模型训练/预测/版本面（model/train/predict/version/deploy 词族）",
     "how": "information_schema 542 表名扫描+逐表精确 COUNT", "hits": facts_common["dev_model_word_tables"]},
    {"what": "dev 告警事件面（alert/alarm/warn/risk_event/blacklist/trigger 词族）",
     "how": "同上", "hits": facts_common["dev_alert_word_tables"]},
    {"what": "dev 人工标注/反馈面（label/annotat/feedback/review/audit 词族）",
     "how": "同上", "hits": facts_common["dev_label_word_tables"]},
    {"what": "gkx 模型/告警/标注词族（280 表）",
     "how": "information_schema 表名扫描", "hits": {"model": facts_common["gkx_model_word_tables"], "alert": facts_common["gkx_alert_word_tables"], "label": facts_common["gkx_label_word_tables"]}},
    {"what": "久新 模型/告警/标注词族（live 实测表数）",
     "how": "SHOW TABLES 表名扫描", "hits": {"model": facts_common["jiuxin_model_word_tables"], "alert": facts_common["jiuxin_alert_word_tables"], "label": facts_common["jiuxin_label_word_tables"]}},
    {"what": "dev 图谱结构面（图算法指标的图原料）",
     "how": "族级快照 _probe_s305_l3_call_out.json", "hits": "26 张全 0 行——图原料空壳，模型特征训练的图谱侧无起点"},
]

specs = [
    ("M_SCIUI_KGANALY_042", "算法模型准确率（知识图谱·指标展示 KPI）",
     "IndicatorDisplay.jsx:103 Statistic title=模型准确率 value=92.8%（mock 常量，源头 OptimizeDecisionPanel perf.accuracy=92.8 → runAutoTrain mock 演化）",
     "decisionModel.js runAutoTrain（mock 随机演化：accuracy=base+boost×(0.3+rand×0.8)，非真训练）"),
    ("M_SCIUI_KGANALY_043", "活跃告警条数（知识图谱·指标展示 KPI）",
     "IndicatorDisplay.jsx:93 Statistic title=活跃告警数 value=3 suffix=个（mock 常量，源头 alerts 数组 3 条硬编码）",
     "IndicatorDisplay.jsx:60-65 alerts 数组硬编码（无台账源）"),
    ("M_SCIUI_KGANALY_044", "模型漏检率（知识图谱·优化决策模型）",
     "OptimizeDecisionPanel.jsx:359 Statistic title=漏检率 value=riskSummary.missRate suffix=%（decisionModel.js summarizeRiskDetection 公式 mock）",
     "decisionModel.js:74 missRate=+(2.1+falseAlarm×0.3).toFixed(1)——由 4 条 mock 告警算出 2.4%，非真漏检统计"),
    ("M_SCIUI_KGANALY_045", "模型误报率（目标域）（知识图谱·优化决策模型·决策反馈闭环）",
     "OptimizeDecisionPanel.jsx:381 Statistic title=目标误报率 value=feedbackAdj.falsePositiveRate suffix=%（decisionModel.js applyFeedbackLoop 公式 mock）",
     "decisionModel.js:57 falsePositiveRate=max(1, 8-valid+falsePos×1.5)——由 4 条 mock 反馈算出 4.5%，非真误报统计"),
]

for mid, mname, mount, algo in specs:
    out = {"metric_id": mid, "metric_name": mname,
           "facts": {**facts_common, "ui_mount": mount, "ui_algo_source": algo},
           "derived": [],
           "absence_probe": absence_probe,
           "support_judgment": "完全不支持",
           "base_years_used": [], "base_years_missing": ["模型运营/告警事件台账三源均无，无年度基期维"],
           "base_years_note": "模型预测明细与人工标注、告警事件台账三源未立项——指标无分子分母来源，不涉年度基期；非「缺年按 0 摊入」"}
    path = os.path.join(BASE, f"{mid}_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("done ->", path, "| support: 完全不支持")
