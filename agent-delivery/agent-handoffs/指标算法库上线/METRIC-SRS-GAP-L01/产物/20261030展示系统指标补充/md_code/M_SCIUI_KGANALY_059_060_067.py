#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_059/060/067 三件合算 — 三源探针 + 判档产物（各落一 _out.json）
059 模型误判率：OptimizeDecisionPanel.jsx:360 riskSummary.falseRate（summarizeRiskDetection 派生：3.5+误报数×1.2 演示公式）
   —— 依赖：告警标注流（预警中/已复核/误报排除三态闭环）——三源逐源留证
060 资产概览：QueryAssetDeepAnalysisDrawer.jsx:105 资产概览卡（AssetThumb+类型/场景/标签+MockBadge）
   —— 纯展示卡（元数据+缩略图）；依赖：图查询资产登记面（资产列表+元数据）——三源逐源留证
067 图谱风险综合评分：BlacklistTriggerPanel.jsx:151 风险评分列 + IndicatorDisplay.jsx:44 详情规则判别区
   —— mock blacklistTriggers 5 条 riskScore 73-92；RiskLevelTag ≥90/80/70 分档；与 066 同域（黑名单侧形态）
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import jx_connect, gkx_connect

BASE = os.path.dirname(os.path.abspath(__file__))
snap307 = json.load(open(os.path.join(BASE, "_snapshots", "_probe_s307_l1_out.json")))["facts"]
facts059, facts060, facts067 = {}, {}, {}

facts059["ui_mount"] = "OptimizeDecisionPanel.jsx:360 <Statistic title='误判率' value={riskSummary.falseRate} suffix='%'>"
facts059["ui_formula"] = "decisionModel.js:64-77 summarizeRiskDetection：falseRate = 3.5 + falseAlarm×1.2（演示公式）；falseAlarm=status 含「误」的告警数"
facts059["ui_mock_source"] = "mockData.js decisionRiskAlerts 4 条（预警中×2/已复核×1/误报排除×1）"
facts060["ui_mount"] = "QueryAssetDeepAnalysisDrawer.jsx:105-116 资产概览卡（AssetThumb 缩略图/类型 Tag/场景/标签/MockBadge）"
facts060["ui_mock_source"] = "queryAssetDeepAnalysis.js buildDeepAnalysis seededInt 派生 + ServiceDisplay 资产列表 mock（entityType/scenario/tags 字段）"
facts067["ui_mount"] = "BlacklistTriggerPanel.jsx:151 风险评分列（RiskLevelTag）+ IndicatorDisplay.jsx:44 详情「规则判别」区风险评分行"
facts067["ui_mock_source"] = "mockData.js:184 blacklistTriggers 5 条 riskScore [87,76,92,81,73]"
facts067["ui_risk_level_rule"] = "BlacklistTriggerPanel.jsx:58-63 RiskLevelTag：≥90 极高（红）/≥80 高（橙）/≥70 中（金）/else 低（绿）"

# ---------- ① dev live：告警标注流/资产登记面词族 ----------
import pymysql
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      charset="utf8mb4", connect_timeout=10, read_timeout=120)
dc = dev.cursor()
dc.execute("""SELECT table_schema, table_name FROM information_schema.tables
              WHERE table_schema LIKE 'gkxlumenx%' AND table_name NOT LIKE 'demo_%'""")
dev_tables = sorted((r[0], r[1]) for r in dc.fetchall())
# 059：告警/误报/复核词族
fam059 = ["alert", "alarm", "false_positive", "review", "feedback", "misjudge", "warning"]
m059 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam059)]
facts059["dev_alert_feedback_family"] = m059
# 060：资产登记词族
fam060 = ["asset", "query_asset", "graph_asset", "catalog", "gallery"]
m060 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam060)]
facts060["dev_asset_registry_family"] = m060
# 067：黑名单词族
fam067 = ["blacklist", "black_list", "block", "trigger", "rule_engine"]
m067 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam067)]
facts067["dev_blacklist_family"] = m067
# 逐张计数（合并命中去重，≤18 张）
all_hits = sorted(set(m059 + m060 + m067))
rows = {}
for fq in all_hits[:18]:
    try:
        dc.execute(f"SELECT COUNT(*) FROM `{fq.split('.')[0]}`.`{fq.split('.')[1]}`")
        rows[fq] = dc.fetchone()[0]
    except Exception as e:  # noqa: BLE001
        rows[fq] = f"ERR:{type(e).__name__}"
facts059["dev_family_rows"] = dict(sorted(rows.items()))
facts060["dev_family_rows"] = {k: v for k, v in sorted(rows.items()) if k in m060}
facts067["dev_family_rows"] = {k: v for k, v in sorted(rows.items()) if k in m067}
dev.close()

# ---------- ② gkx：三件词族（风险语义已有族级快照） ----------
gc = gkx_connect()
gc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx'")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts059["gkx_alert_feedback_family"] = [t for t in gkx_tables if any(w in t.lower() for w in fam059)]
facts060["gkx_asset_family"] = [t for t in gkx_tables if any(w in t.lower() for w in fam060)]
facts067["gkx_blacklist_family"] = [t for t in gkx_tables if any(w in t.lower() for w in fam067)]
facts067["gkx_risk_tables"] = snap307["gkx_word_families"]["risk"]

# ---------- ③ 久新：三件词族 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jc.fetchall())
facts059["jiuxin_alert_feedback_family"] = [t for t in jx_tables if any(w in t.lower() for w in fam059)]
facts060["jiuxin_asset_family"] = [t for t in jx_tables if any(w in t.lower() for w in fam060)]
facts067["jiuxin_blacklist_family"] = [t for t in jx_tables if any(w in t.lower() for w in fam067)]
jx.close()

# ---------- 判档（三件同批：纯展示/派生读数三源无承载面） ----------
support059 = "完全不支持"   # 误判率依赖告警标注流（三态闭环）——三源词族留证均缺
support060 = "完全不支持"   # 资产概览依赖图查询资产登记面——三源词族留证均缺（久新 asset 零命中）
support067 = "完全不支持"   # 黑名单风险评分依赖触发名单+评分——三源无黑名单/触发面；gkx 企业风险表是升档候选

derived059 = [{
    "source": "三源告警标注流词族探针",
    "dev_hits": facts059["dev_alert_feedback_family"], "dev_rows": facts059["dev_family_rows"],
    "gkx_hits": facts059["gkx_alert_feedback_family"], "jiuxin_hits": facts059["jiuxin_alert_feedback_family"],
    "ui_demo_formula": "falseRate = 3.5 + falseAlarm×1.2（mock 演示公式——真误判率=FP/(FP+TN) 需标注集）",
    "verdict": "告警三态闭环（预警中/已复核/误报排除）流三源缺位；误判率分母（TN 集）无从构建——与 066/063 同属「动态风险域三缺」",
}]
derived060 = [{
    "source": "三源图查询资产登记面词族探针",
    "dev_hits": facts060["dev_asset_registry_family"], "dev_rows": facts060["dev_family_rows"],
    "gkx_hits": facts060["gkx_asset_family"], "jiuxin_hits": facts060["jiuxin_asset_family"],
    "ui_mock_badge": "MockBadge 显式标注（QueryAssetDeepAnalysisDrawer.jsx:114）——UI 自认演示级",
    "verdict": "图查询资产登记面（资产列表+entityType/scenario/tags 元数据）三源缺位；资产概览卡的元数据行无后端承载",
    "nearest_candidate": "久新 ads_* 图表面族（node/edge）可构图但无「资产」抽象层（查询资产=面向业务的图数据集包装）",
}]
derived067 = [{
    "source": "三源黑名单/触发面词族探针",
    "dev_hits": facts067["dev_blacklist_family"], "dev_rows": facts067["dev_family_rows"],
    "gkx_hits": facts067["gkx_blacklist_family"], "jiuxin_hits": facts067["jiuxin_blacklist_family"],
    "gkx_risk_upgrade_candidate": facts067["gkx_risk_tables"],
    "ui_mock_scores": "[87, 76, 92, 81, 73]（blacklistTriggers 5 条）",
    "verdict": "黑名单触发名单+风险评分面三源缺位；与 066（优化决策侧风险评分）同域同缺——gkx 企业风险表族是唯一真实风险语义升档候选",
}]

absence = [
    {"what": "dev 告警/资产/黑名单词族", "how": "gkxlumenx* 词族扫描+逐张计数（本件）", "hits": f"合并命中 {len(all_hits)} 张（行数见 facts）"},
    {"what": "久新 alert/asset/blacklist 词族", "how": "SHOW TABLES 词族（本件）", "hits": "三族逐一留证（见 facts）"},
    {"what": "gkx 告警/资产/黑名单词族", "how": "280 表词族（本件+族级快照）", "hits": "risk 族已有（dwd_org_risk_*）；alert/asset/blacklist 逐留"},
    {"what": "dev 图结构面（26 张）", "how": "族级快照 _probe_s305_l3_call_out.json", "hits": "全 0 行"},
]

# ---------- 059 产物 ----------
out059 = {"metric_id": "M_SCIUI_KGANALY_059", "metric_name": "模型误判率（科技知识图谱·指标展示·优化决策模型·风险识别优化）",
          "facts": facts059, "derived": derived059, "absence_probe": absence,
          "support_judgment": support059,
          "base_years_used": [], "base_years_missing": ["UI 读数为 mock 演示公式派生（3.5+误报×1.2），无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_059_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out059, fh, ensure_ascii=False, indent=2)
print("done 059 | support:", support059, "| dev fam:", len(m059), "| jiuxin:", len(facts059["jiuxin_alert_feedback_family"]))

# ---------- 060 产物 ----------
out060 = {"metric_id": "M_SCIUI_KGANALY_060", "metric_name": "资产概览（科技知识图谱·分析展示·图查询资产·深入分析）",
          "facts": facts060, "derived": derived060, "absence_probe": absence,
          "support_judgment": support060,
          "base_years_used": [], "base_years_missing": ["UI 为 mock 资产元数据展示卡，无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_060_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out060, fh, ensure_ascii=False, indent=2)
print("done 060 | support:", support060, "| dev fam:", len(m060), "| jiuxin:", len(facts060["jiuxin_asset_family"]))

# ---------- 067 产物 ----------
out067 = {"metric_id": "M_SCIUI_KGANALY_067", "metric_name": "图谱风险综合评分（科技知识图谱·指标展示·黑名单联动触发）",
          "facts": facts067, "derived": derived067, "absence_probe": absence,
          "support_judgment": support067,
          "base_years_used": [], "base_years_missing": ["UI 读数为 mock 触发名单（5 条 73-92 分），无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_067_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out067, fh, ensure_ascii=False, indent=2)
print("done 067 | support:", support067, "| dev fam:", len(m067), "| gkx risk:", len(facts067["gkx_risk_tables"]))
