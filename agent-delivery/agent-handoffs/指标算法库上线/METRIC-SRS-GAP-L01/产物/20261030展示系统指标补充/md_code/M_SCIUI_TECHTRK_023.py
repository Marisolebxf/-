#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_023 技术趋势判断结论 —— 三源探针 + 复现脚本（批 S3-01 Lane 4）。

UI 挂载：repos/demo-ui-science/src/techDevelopmentTracking.js:1554
  buildTechnologyTrackingTechnologyDetailSections 第三段「发展趋势」：
  { label: '趋势判断', value: trendJudgement }——一行自然语言结论
  生成器 buildTechnologyTrackingTrendJudgement(target)（js:1461-1469）：
  有 trend 文本 → 「{topic}在当前时间范围内保持{trend}的增长趋势，需结合成熟度、产业化潜力和投资需求继续复核。」
  无 trend 有热力切片 → 年度读数句；兜底 → 持续跟踪句。

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：无趋势判断结果面（探针留证）
  ② gkx：280 表无 trend/conclusion 类技术趋势结果面（探针留证）
  ③ 久新：ads_technology_hotspot_yearly.trend_status（RISING/STABLE/DECLINING/INSUFFICIENT_EVIDENCE/
     BASELINE 五态枚举，233,160 行）+ hotspot_snapshot.hotspot_status（五态状态机）——本件主承载

复现口径（B10 双口径并列）：
  口径 A（库侧枚举结论·年度）：trend_status 逐年分布 + 2025→2026 同比分向（up/down/flat 计数）
  口径 B（自然语言模板·UI 同构）：按 UI 模板规则用库侧读数生成结论句（演示生成能力，非数据证据）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30, read_timeout=300, autocommit=True,
)

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

V2 = "technology_insight_mvp_v2_eto_cluster_technology"

facts = {}
probes = []


def probe(tag, source, sql, cur, note=""):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql, "note": note,
                       "hits": len(rows), "sample": [str(r)[:180] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql, "note": note,
                       "hits": -1, "error": str(e)[:180]})
        return []


jx = pymysql.connect(**JX)
jc = jx.cursor()

# ---- 口径 A：trend_status 逐年分布 ----
jc.execute(
    "SELECT statistics_year, trend_status, COUNT(*) FROM ads_technology_hotspot_yearly "
    "GROUP BY statistics_year, trend_status ORDER BY statistics_year DESC, 3 DESC")
year_status = {}
for y, s, c in jc.fetchall():
    year_status.setdefault(int(y), {})[str(s)] = int(c)
facts["jiuxin_trend_status_by_year"] = dict(sorted(year_status.items(), reverse=True))

# 全版本 trend_status 汇总
jc.execute("SELECT trend_status, COUNT(*) FROM ads_technology_hotspot_yearly GROUP BY trend_status ORDER BY 2 DESC")
facts["jiuxin_trend_status_total"] = {str(r[0]): int(r[1]) for r in jc.fetchall()}

# 2025→2026 同比分向（up/down/flat）
jc.execute(
    "SELECT SUM(CASE WHEN b.hotspot_score > a.hotspot_score THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN b.hotspot_score < a.hotspot_score THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN b.hotspot_score = a.hotspot_score THEN 1 ELSE 0 END), COUNT(*) "
    "FROM ads_technology_hotspot_yearly a JOIN ads_technology_hotspot_yearly b "
    "ON a.technology_node_id = b.technology_node_id AND a.statistics_year = 2025 AND b.statistics_year = 2026")
r = jc.fetchone()
facts["jiuxin_hotspot_2025_to_2026_direction"] = {
    "up": int(r[0]), "down": int(r[1]), "flat": int(r[2]), "total": int(r[3])}

# ---- snapshot 状态机（v2）----
jc.execute(
    "SELECT hotspot_status, COUNT(*) FROM ads_technology_hotspot_snapshot "
    "WHERE model_version = %s GROUP BY hotspot_status ORDER BY 2 DESC", (V2,))
facts["jiuxin_hotspot_status_v2"] = {str(r[0]): int(r[1]) for r in jc.fetchall()}

# ---- 口径 B：UI 同构模板生成（用库侧读数）----
d2526 = facts["jiuxin_hotspot_2025_to_2026_direction"]
yoy_avg = None
jc.execute(
    "SELECT AVG(b.hotspot_score - a.hotspot_score) FROM ads_technology_hotspot_yearly a "
    "JOIN ads_technology_hotspot_yearly b ON a.technology_node_id = b.technology_node_id "
    "AND a.statistics_year = 2025 AND b.statistics_year = 2026")
r = jc.fetchone()
yoy_avg = round(float(r[0]), 4)
facts["jiuxin_hotspot_2025_to_2026_avg_delta"] = yoy_avg

if yoy_avg is not None and yoy_avg < 0:
    direction_word = "下行"
elif yoy_avg is not None and yoy_avg > 0:
    direction_word = "上行"
else:
    direction_word = "持平"
conclusion_b = (
    "候选技术节点池在 2025→2026 观测窗整体呈%s（均分变化 %s，上行 %d / 下行 %d / 持平 %d，共 %d 节点）；"
    "2026 为部分观测年，趋势读数须结合成熟度、产业化潜力和投资需求继续复核。" % (
        direction_word, yoy_avg, d2526["up"], d2526["down"], d2526["flat"], d2526["total"]))
facts["generated_conclusion_ui_style"] = conclusion_b

# ---- UI 模板规则登记 ----
facts["ui_trend_judgement_template"] = {
    "branch_trend": "{topic}在当前时间范围内保持{trend}的增长趋势，需结合成熟度、产业化潜力和投资需求继续复核。",
    "branch_heatmap": "{topic}在 {year} 年{metric}为 {value}，建议与相邻年份评估结果对比。",
    "branch_fallback": "{topic}需结合当前时间范围内的热度、成熟度、潜力和风险变化持续跟踪。",
}

jc.close()
jx.close()

# ---- gkx 探针 ----
gc = gkx()
rows = probe("gkx 280 表 trend/conclusion/judg 类结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%trend%' OR table_name LIKE '%conclusion%' OR table_name LIKE '%judg%')", gc)
facts["gkx_trend_like_tables"] = [r[0] for r in rows]
gc.close()

# ---- dev 探针 ----
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads 趋势结论类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%trend%' OR table_name LIKE '%conclusion%')", dc)
    facts["dev_trend_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_023_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# 派生：2026 年可判定节点占比（RISING+STABLE+DECLINING / 总）
y2026 = year_status.get(2026, {})
decidable_2026 = y2026.get("RISING", 0) + y2026.get("STABLE", 0) + y2026.get("DECLINING", 0)
total_2026 = sum(y2026.values())
derived = [
    {"key": "jiuxin_trend_decidable_share_2026_pct",
     "value": round(100.0 * decidable_2026 / total_2026, 4) if total_2026 else None,
     "numerator": decidable_2026,
     "denominator": total_2026,
     "note": "分子=2026 年 trend_status 可判定（RISING+STABLE+DECLINING）节点数，分母=2026 年全部节点行 19,430；同源 jiuxin hotspot_yearly 2026 行。"},
]

out = {
    "metric_id": "M_SCIUI_TECHTRK_023",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1554",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1461-1469",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1514",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「趋势判断」作为指标名在三份指定说明书 0 命中（技术发展跟踪.md 无该词）；"
                "srs/04-科技专题服务系统/科技专题内容运营中心/可视化管理.md:64 的「辅助趋势判断」是产业趋势可视化语境（其他系统板块）；"
                "需求侧最接近的是技术发展跟踪.md seq 55『结果变化趋势』（022 件承接的功能词）。",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "「技术趋势判断结论」UI 语义是详情卡「发展趋势」段的一行自然语言（模板三分支：trend 文本/热力切片/兜底句），由前端函数确定性生成——它是结论的『呈现形态』而非计算结果。",
        "库侧承载是结构化趋势状态而非自然语言：hotspot_yearly.trend_status 五态枚举（RISING/STABLE/DECLINING/INSUFFICIENT_EVIDENCE/BASELINE）逐节点逐年；snapshot.hotspot_status 五态状态机（EARLY_EMERGING/ESTABLISHED_GROWING/MATURE/WATCH/INSUFFICIENT_EVIDENCE）。",
        "可判定率是核心读数：2026 年 93.61% 节点证据不足（INSUFFICIENT_EVIDENCE 18,188/19,430），可下升/降/平结论的仅 6.39%（1,242 节点）——『结论』在当前证据面下大面积不可生成，这是本件区别于普通趋势指标的批量大 gap。",
        "2025→2026 同比分向：上行 6,849 / 下行 11,123 / 持平 1,458（全池 19,430 节点）；均分变化 -10.9538（口径 A 读数，2026 部分年偏置须披露）。",
        "口径 B 示例结论（UI 同构模板用库侧读数生成，证明可生成性）：见 facts.generated_conclusion_ui_style；语义槽（成熟度/产业化潜力/投资需求复核句）在库侧分别有 stage/potential/bottleneck 承载，可组装。",
    ],
    "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021",
                        "2022", "2023", "2024", "2025", "2026"],
    "base_years_missing": [],
    "base_years_note": "hotspot_yearly 2015-2026 全序列可用；2026 为 PARTIAL_YEAR（metrics_as_of_date=2026-10-16 截止），跨年比较读数须带部分年披露。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "233160", "19430", "18188", "6849", "11123", "1458", "197593","1556","1557","35534","7741"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_023_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
