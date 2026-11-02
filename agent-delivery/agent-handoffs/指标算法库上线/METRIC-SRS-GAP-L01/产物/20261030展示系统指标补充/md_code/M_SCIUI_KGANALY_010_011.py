#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_010 模型召回率 / M_SCIUI_KGANALY_011 模型预测准确率 — 三源探针 + 训练样本可行性 + 判档产物
UI 挂载：OptimizeDecisionPanel.jsx（决策反馈闭环 Tab）：
  010 召回率：:128 trainPerfOption legend、:134 trainColumns recall 列、:150 传参 runAutoTrain
  011 准确率：:128 legend、:133 trainColumns accuracy 列、:149 传参
两件同源同判：召回率/准确率是分类模型评估指标，需要「模型预测记录 + 真实标注（ground truth）」对。
三源核查：dev 无模型训练/评估面；gkx 无；久新无（feedback/model 词族 0 命中）。
判定：完全不支持——风险分类场景（金融欺诈/信用违约）的标注数据三源均无立项。
"""
import json, os, sys, time, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s306_l1_out.json")
OUT10 = os.path.join(BASE, "M_SCIUI_KGANALY_010_out.json")
OUT11 = os.path.join(BASE, "M_SCIUI_KGANALY_011_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount_010"] = ("OptimizeDecisionPanel.jsx:128 trainPerfOption legend data=['准确率','召回率','F1']；"
                          ":134 trainColumns { title:'召回率', dataIndex:'recall', render: v=>`${v}%` }；"
                          ":150 runAutoTrain(trainHistory, algorithm, perf) 触发新增训练记录")
facts["ui_mount_011"] = ("OptimizeDecisionPanel.jsx:128 legend；:133 trainColumns { title:'准确率', dataIndex:'accuracy', render: v=>`${v}%` }；"
                          ":149 runAutoTrain 传参")
facts["ui_mock_train_history"] = [
    {"id": "tr-1", "time": "2026-05-15 02:00", "algorithm": "hybrid_rule", "accuracy": 92.8, "recall": 88.5, "f1": 90.6, "latencyMs": 45, "status": "deployed", "note": "Q1样本重训，准确率+3.2%"},
    {"id": "tr-2", "time": "2026-05-01 02:00", "algorithm": "temporal_gcn", "accuracy": 90.1, "recall": 86.2, "f1": 88.1, "latencyMs": 52, "status": "archived", "note": "时序窗口扩至 30 天"},
    {"id": "tr-3", "time": "2026-04-15 02:00", "algorithm": "graphsage", "accuracy": 88.4, "recall": 84.0, "f1": 86.1, "latencyMs": 41, "status": "archived", "note": "基线图表示模型"},
]
facts["ui_sim_source"] = ("decisionModel.js:21-44 runAutoTrain——accuracy=min(97, base+boost*(0.3+rand*0.8))、"
                          "recall=min(96, base+boost*(0.2+rand*0.7)) 的 Math.random 增益模拟（boost 按算法 1.2/0.9/0.7），非真训练；"
                          "文件头 ponytail 自注『本地规则模拟自适应/训练/反馈，真源待 algo 训练管线』")
facts["ui_risk_scenario_note"] = ("mockData.js:591-596 decisionRiskAlerts 场景=金融欺诈/信用违约风控预警——"
                                  "科技图谱域数据源无此业务场景立项，评估标注（是否真欺诈/真违约）无处产生")

# ---------- ① dev：模型训练/评估面词族（族级快照） ----------
facts["dev_ops_word_table_rows"] = snap["facts"].get("dev_ops_word_table_rows") or {}
# dev topic_enterprise.evaluation_template 是评估模板配置非模型评估记录（语义排除）
facts["dev_eval_template_note"] = "gkxlumenx_topic_enterprise.evaluation_template 为企业评估模板配置（UI 配置面），非模型训练/评估记录——语义排除"

# ---------- ② gkx：模型/标注面词族 ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx'")
facts["gkx_table_count"] = gc.fetchone()[0]
gc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
           "AND (table_name LIKE '%label%' OR table_name LIKE '%model%' OR table_name LIKE '%train%' "
           "OR table_name LIKE '%fraud%' OR table_name LIKE '%risk_eval%')")
facts["gkx_model_label_word_tables"] = sorted(r[0] for r in gc.fetchall())
gc.close()

# ---------- ③ 久新：模型/标注/风险面词族 ----------
facts["jiuxin_feedback_model_word_tables"] = snap["facts"]["jiuxin_feedback_model_word_tables"]
facts["jiuxin_table_count_live"] = snap["facts"]["jiuxin_table_count_live"]

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
jc.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jc.fetchall())
facts["jiuxin_label_word_tables"] = sorted(
    t for t in jx_tables if any(w in t.lower() for w in ("label", "model", "train", "fraud", "risk", "eval")))
facts["jiuxin_capability_model_semantic_exclusion"] = (
    "jiuxin ads_talent_capability_model 词族唯一命中——SHOW CREATE TABLE 实查：人员能力综合评分『权重配置』面"
    "（research_perseverance_weight 等 9 个权重/阈值列），无 accuracy/recall/预测记录/标注列，语义排除")
# 黑名单/风险链相关表深探（黑名单触发族的数据面——若有黑名单记录可作弱标注源）
facts["jiuxin_blacklist_word_tables"] = sorted(
    t for t in jx_tables if any(w in t.lower() for w in ("blacklist", "black_list", "trigger")))
facts["jiuxin_blacklist_word_note"] = "blacklist/trigger 词族 0 命中——风险预警无落盘，误报复核反馈环（rating）亦无承载"
jx.close()

absence_probe = [
    {"what": "dev 模型训练/评估记录面（train_history/model_eval/prediction_log）",
     "how": "dev 542 表词族扫描（train/model/eval/predict）+ops 词族计数",
     "hits": "0——evaluation_template 为配置模板（语义排除）；无训练记录、无预测落盘、无标注面"},
    {"what": "gkx 分类模型预测+标注对（召回率/准确率的计算原料）",
     "how": "gkx 280 表词族扫描（label/model/train/fraud/risk_eval）",
     "hits": "0——要素库无风险分类场景、无预测记录、无 ground truth 标注"},
    {"what": "久新模型训练/反馈/标注面",
     "how": "久新 218 表词族扫描（feedback/model/train/label/fraud/risk/eval/blacklist）",
     "hits": "0——ADS 结果面为图/合作/人才域，无决策模型评估面（feedback_model 词族 0 命中）"},
]

# 复现脚本内置实算校验：按 UI 同款公式（decisionModel.js:21-28）对 mock 初值跑确定性推进（rand 取中点）
BOOST = {"hybrid_rule": 1.2, "gat": 0.9}
def sim_next(algorithm, base_accuracy, base_recall, base_latency_ms):
    boost = BOOST.get(algorithm, 0.7)
    accuracy = round(min(97, base_accuracy + boost * (0.3 + 0.4)), 1)  # rand 取中点近似
    recall = round(min(96, base_recall + boost * (0.2 + 0.35)), 1)
    f1 = round(2 * accuracy * recall / (accuracy + recall), 1)
    latency = max(28, round(base_latency_ms + 0.5))
    return {"algorithm": algorithm, "accuracy": accuracy, "recall": recall, "f1": f1, "latencyMs": latency}
# 注：真 UI 用 Math.random()，此处中点仅验证公式形态（boost/上限/联动）——不是训练结果

derived_common = [
    {"formula": "recall = TP/(TP+FN)，accuracy = (TP+TN)/(TP+TN+FP+FN)",
     "note": "分类评估标准定义（需预测落盘+ground truth 标注对），三源均无此计算原料"},
    {"formula": "UI 模拟公式（decisionModel.js:24）recall = min(96, base + boost*(0.2+rand*0.7))",
     "note": "复现脚本 sim_next() 按 UI 同款公式形态对 mock 初值 84.0 推进（rand 中点）——验证增益逻辑，非训练结果"},
    {"derived": "sim_next('hybrid_rule', 92.8, 88.5, 45) = accuracy 93.6 / recall 89.2 / f1 91.3 / latency 46ms（mock 下一拍演示值）",
     "note": "mock 演示链自洽性校验——三源无对应真值，此演示值仅供公式复现，不得入指标口径"},
]
sim_check = sim_next("hybrid_rule", 92.8, 88.5, 45)
assert abs(sim_check["recall"] - 89.2) < 0.01 and abs(sim_check["accuracy"] - 93.6) < 0.01, sim_check

support = "完全不支持"
base = {"facts": facts, "derived": derived_common, "absence_probe": absence_probe, "support_judgment": support,
        "base_years_used": [], "base_years_missing": ["召回率/准确率为模型评估截面读数，无年度基期维"],
        "base_years_note": "物理口径基期=探针快照日；评估指标为训练批次截面量，非年度基期概念"}

out10 = dict(base); out10.update({"metric_id": "M_SCIUI_KGANALY_010",
    "metric_name": "模型召回率（科技知识图谱·指标展示·优化决策模型·模型自动迭代）"})
with open(OUT10, "w", encoding="utf-8") as fh:
    json.dump(out10, fh, ensure_ascii=False, indent=2)
out11 = dict(base); out11.update({"metric_id": "M_SCIUI_KGANALY_011",
    "metric_name": "模型预测准确率（科技知识图谱·指标展示·优化决策模型·模型自动迭代）"})
with open(OUT11, "w", encoding="utf-8") as fh:
    json.dump(out11, fh, ensure_ascii=False, indent=2)
print("done ->", OUT10, "&", OUT11, "| support:", support)
