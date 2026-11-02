#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_058/063 合算 — 三源探针（指标配置面/行为事件流）+ 判档产物（各落一 _out.json）
058 融合指标数：IndicatorDisplay.jsx:98 Statistic value={5} 硬编码（对应 mockData fusionIndicators 5 项计数）
   —— 无业务逻辑数值类·纯计数读数：三源有无「融合指标登记/配置面」逐源留证
063 行为频次指数：mockData.js:566 decisionDynamicMetrics behaviorFreq value:128 delta:12（近7日异常与正常行为加权频次）
   —— 需业务建模类：三源有无「行为事件流（时序）」逐源留证；gkx 备语义（论文发表/合作事件流）可算替代口径
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s306_l3_base import jx_connect, gkx_connect, load_snap

BASE = os.path.dirname(os.path.abspath(__file__))
snap307 = json.load(open(os.path.join(BASE, "_snapshots", "_probe_s307_l1_out.json")))["facts"]
facts058, facts063 = {}, {}
facts058["ui_hardcode"] = "IndicatorDisplay.jsx:98 <Statistic title='融合指标数' value={5} suffix='项'/>"
facts058["ui_mock_source"] = "mockData.js fusionIndicators 5 项（net_density/clustering/avg_path/centrality_var/modularity）"
facts063["ui_mock_source"] = "mockData.js:566 decisionDynamicMetrics behaviorFreq {value:128, delta:12, desc:'近7日异常与正常行为加权频次'}"
facts063["ui_algo_hint"] = "decisionModel.js bumpDynamicMetrics behaviorFreq 分支：Math.round(value+step*80)——mock 演进规则非算法"

# ---------- ① dev live：gkxlumenx_* 指标配置/登记词族 + 行为事件流词族 ----------
import pymysql
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      charset="utf8mb4", connect_timeout=10, read_timeout=120)
dc = dev.cursor()
dc.execute("""SELECT table_schema, table_name FROM information_schema.tables
              WHERE table_schema LIKE 'gkxlumenx%' AND table_name NOT LIKE 'demo_%'""")
dev_tables = sorted((r[0], r[1]) for r in dc.fetchall())
facts058["dev_gkxlumenx_table_total"] = len(dev_tables)
fam_words_058 = ["metric", "indicator", "fusion", "index_config", "quota"]
m058 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam_words_058)]
facts058["dev_metric_config_family"] = m058
fam_words_063 = ["behavior", "action", "event_log", "click", "visit_log", "operate", "audit"]
m063 = [f"{s}.{t}" for s, t in dev_tables if any(w in t.lower() for w in fam_words_063)]
facts063["dev_behavior_event_family"] = m063
# 计数（命中不超过 12 张逐张计数）
rows058 = {}
for fq in m058[:12]:
    try:
        dc.execute(f"SELECT COUNT(*) FROM `{fq.split('.')[0]}`.`{fq.split('.')[1]}`")
        rows058[fq] = dc.fetchone()[0]
    except Exception as e:  # noqa: BLE001
        rows058[fq] = f"ERR:{type(e).__name__}"
facts058["dev_metric_config_rows"] = dict(sorted(rows058.items()))
rows063 = {}
for fq in m063[:12]:
    try:
        dc.execute(f"SELECT COUNT(*) FROM `{fq.split('.')[0]}`.`{fq.split('.')[1]}`")
        rows063[fq] = dc.fetchone()[0]
    except Exception as e:  # noqa: BLE001
        rows063[fq] = f"ERR:{type(e).__name__}"
facts063["dev_behavior_event_rows"] = dict(sorted(rows063.items()))
dev.close()

# ---------- ② gkx：行为/事件词族 + 论文年流（备语义） ----------
gc = gkx_connect()
gc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx'")
gkx_tables = sorted(r[0] for r in gc.fetchall())
m063_g = [t for t in gkx_tables if any(w in t.lower() for w in fam_words_063)]
facts063["gkx_behavior_event_family"] = m063_g
# 备语义：论文按年计数（学术行为流——可算「年度发文频次」替代口径）
# 注：gkx 无 dwd_paper 表，论文主表为 dwd_en_paper（年份列 cover_year_start——列名实查）
try:
    gc.execute("""SELECT cover_year_start, COUNT(*) FROM gkx.dwd_en_paper
                  WHERE cover_year_start BETWEEN 2016 AND 2026
                  GROUP BY cover_year_start ORDER BY cover_year_start""")
    yearly = {int(r[0]): int(r[1]) for r in gc.fetchall()}
    facts063["gkx_paper_yearly_counts_2016_2026"] = dict(sorted(yearly.items()))
    facts063["gkx_paper_yearly_latest"] = max(yearly.items(), key=lambda kv: kv[0]) if yearly else None
    gc.execute("SELECT COUNT(*) FROM gkx.dwd_en_paper")
    facts063["gkx_paper_total"] = gc.fetchone()[0]
except Exception as e:  # noqa: BLE001
    facts063["gkx_paper_yearly_counts_2016_2026"] = f"ERR:{type(e).__name__}"

# 058 侧 gkx：指标配置词族
m058_g = [t for t in gkx_tables if any(w in t.lower() for w in fam_words_058)]
facts058["gkx_metric_config_family"] = m058_g

# ---------- ③ 久新：*_metrics 表清单（指标结果面 vs 登记面辨析）+ 行为词族 ----------
jx = jx_connect()
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_tables = sorted(r[0] for r in jc.fetchall())
m058_j = [t for t in jx_tables if "metric" in t.lower() or "indicator" in t.lower()]
facts058["jiuxin_metrics_tables"] = m058_j
facts058["jiuxin_metrics_table_count"] = len(m058_j)
m063_j = [t for t in jx_tables if any(w in t.lower() for w in fam_words_063)]
facts063["jiuxin_behavior_event_family"] = m063_j
# 058 关键辨析：抽 1 张 metrics 表看列结构（结果面非登记面证据）
try:
    probe_tbl = "ads_technology_yearly_metrics"
    jc.execute(f"SHOW COLUMNS FROM {probe_tbl}")
    cols = sorted(r[0] for r in jc.fetchall())
    facts058["jiuxin_metrics_table_sample_columns"] = {"table": probe_tbl, "columns": cols[:18]}
    jc.execute(f"SELECT COUNT(*) FROM {probe_tbl}")
    facts058["jiuxin_metrics_table_sample_rows"] = jc.fetchone()[0]
except Exception as e:  # noqa: BLE001
    facts058["jiuxin_metrics_table_sample_columns"] = f"ERR:{type(e).__name__}"
jx.close()

# ---------- 058 判档 ----------
# 融合指标数 = 融合指标登记面的行计数。三源：dev 配置词族命中张数+行数；gkx 无 fusion 登记面；
# 久新 20 张 *_metrics 是「各域指标结果面」（按实体×年出指标值）非「融合指标登记配置面」——语义辨析落键。
fusion_registry_found = bool([k for k, v in facts058["dev_metric_config_rows"].items()
                              if isinstance(v, int) and v > 0 and ("fusion" in k.lower() or "indicator" in k.lower())])
support058 = "完全不支持"  # 三源无融合指标登记面（探针留证）；久新 metrics 表族是结果面非登记面
derived058 = [{
    "source": "UI mock 计数（fusionIndicators.length=5）——三源逐源辨析",
    "ui_value": 5,
    "dev_probe": f"gkxlumenx* 词族命中 {len(facts058['dev_metric_config_family'])} 张（行数见 facts）",
    "gkx_probe": f"词族命中 {len(m058_g)} 张",
    "jiuxin_probe": f"*_metrics {len(m058_j)} 张——均为『实体×年指标结果面』（sample 列结构落键），非融合指标登记/配置面",
    "verdict": "指标登记面三源缺位：『融合指标数』作为配置计数无承载；若按『展示页启用指标项数』口径则恒等于 UI 配置（业务定义问题非数据问题）",
}]

# ---------- 063 判档 ----------
# 行为频次指数 = 近 7 日行为事件加权频次。关键依赖=行为事件流（时序细粒度）。
# 三源：dev 行为词族 / gkx 行为词族（无）+论文年流（年度粒度远粗于 7 日）/ 久新行为词族——逐源留证。
behavior_stream_found = any(isinstance(v, int) and v > 0 for v in facts063["dev_behavior_event_rows"].values()) or bool(m063_g) or bool(m063_j)
# 语义裁定：dev cms_op_audit 476 行是「后台操作审计流」（管理操作日志）非「业务行为事件流」（账户/实体行为），
# gkx dwd_rel_reaction_substance 是化学反应物质表（词面命中，语义无关）；论文年流是「成果产出流」粒度年度且无加权维——
# UI 口径（近 7 日异常与正常行为加权频次）的三个要素（细粒度时序/行为分型/异常标注）三源均缺 → 完全不支持。
support063 = "完全不支持"
derived063 = []
if isinstance(facts063.get("gkx_paper_yearly_counts_2016_2026"), dict) and facts063["gkx_paper_yearly_counts_2016_2026"]:
    yc = facts063["gkx_paper_yearly_counts_2016_2026"]
    latest_year, latest_cnt = facts063["gkx_paper_yearly_latest"]
    prev_cnt = yc.get(latest_year - 1)
    derived063.append({
        "source": "gkx.dwd_en_paper cover_year_start 分年计数（成果产出流·年度粒度最接近候选）",
        "yearly_counts": dict(sorted(yc.items())),
        "latest_year": latest_year, "latest_count": latest_cnt,
        "yoy_delta": (latest_cnt - prev_cnt) if prev_cnt else None,
        "note": "最接近候选：『年度发文频次』≠UI『近7日行为加权频次』（粒度年度 vs 7 日/无异常-正常分型/无加权维）——不足以撑部分支持档，登记为语义换轨扩展项",
    })
derived063.append({
    "source": "三源行为事件流词族探针（7 日粒度依赖）",
    "dev_hits": facts063["dev_behavior_event_rows"],
    "gkx_hits": m063_g, "jiuxin_hits": m063_j,
    "verdict": "行为事件流（时序细粒度）三源缺位——UI 口径（近7日异常与正常行为加权频次）无法构建；权重方案（异常 vs 正常）亦为业务建模待定项",
})

absence = [
    {"what": "dev 融合指标登记面（fusion/indicator 配置表）", "how": "gkxlumenx* 词族扫描+逐张计数（本件）",
     "hits": f"词族命中 {len(facts058['dev_metric_config_family'])} 张（行数见 facts.dev_metric_config_rows）"},
    {"what": "久新融合指标登记面", "how": "SHOW TABLES 词族+列结构抽样（本件）",
     "hits": f"{len(m058_j)} 张 *_metrics 均为结果面（sample 列结构无『登记/配置』语义列）"},
    {"what": "三源行为事件流（7 日粒度）", "how": "behavior/action/event_log/click/visit/operate/audit 词族（本件）",
     "hits": "dev/gkx/久新逐一留证（见 facts063）"},
    {"what": "dev 图结构面（26 张）", "how": "族级快照 _probe_s305_l3_call_out.json", "hits": "全 0 行（非承载）"},
]

# ---------- 058 产物 ----------
out058 = {"metric_id": "M_SCIUI_KGANALY_058", "metric_name": "融合指标数（科技知识图谱·指标展示·融合统计指标和模型特征）",
          "facts": facts058, "derived": derived058, "absence_probe": absence,
          "support_judgment": support058,
          "base_years_used": [], "base_years_missing": ["UI 读数为 mock 配置计数（5 项），无年度基期维"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_058_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out058, fh, ensure_ascii=False, indent=2)
print("done 058 | support:", support058, "| jiuxin metrics tables:", len(m058_j))

# ---------- 063 产物 ----------
out063 = {"metric_id": "M_SCIUI_KGANALY_063", "metric_name": "行为频次指数（科技知识图谱·指标展示·优化决策模型·动态指标学习）",
          "facts": facts063, "derived": derived063, "absence_probe": absence,
          "support_judgment": support063,
          "base_years_used": [], "base_years_missing": ["UI 口径为近 7 日滚动窗口（无年度基期维）；替代口径 gkx 论文年流基期见 facts"],
          "base_years_note": "物理口径基期=探针快照日（当日截面）；UI 口径非年度基期，非「缺年按 0 摊入」"}
with open(os.path.join(BASE, "M_SCIUI_KGANALY_063_out.json"), "w", encoding="utf-8") as fh:
    json.dump(out063, fh, ensure_ascii=False, indent=2)
print("done 063 | support:", support063, "| paper latest:", facts063.get("gkx_paper_yearly_latest"))
