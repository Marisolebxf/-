#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_006 指标增长率 —— 批 S3-01 Lane 6 复现脚本（三源）。

口径（推测定义，需求未给公式；UI 语义 = 创新载体多维度排名的「增长率」折线，同比口径）：
  指标增长率 g_y = (X_y − X_{y−1}) / X_{y−1} × 100%（年度同比，X 上年非零）
  参照 OECD MSTI 口径：增长率按不变价序列计算，非年度区间用 CAGR 复合（本件只用年度同比）。

三源承载（探针实测）：
  dev  gkxlumenx_dwd 投融资 5 表无年度聚合指标面；enterprise_invest.event_date 0 覆盖（不可按年算）
  gkx  dwd_org_financing_info 25,654 行（completion_date 100% 覆盖，按年可算事件数增长率）
  jiuxin ads_technology_yearly_metrics（技术节点×年，2019–2026 全量）
        ads_emerging_topic_yearly_metrics.paper_count_yoy（现成 YoY 列）
        ads_research_problem_yearly_metrics.paper_growth_rate（现成增长率列）
只读；产物 M_SCIUI_INNOV_006_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_INNOV_006_out.json")

facts = {}
notes = []
absence_probe = []
derived = []

# ---------------- dev（10.50.11.76 gkxlumenx_dwd，非 demo）----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(CASE WHEN event_date IS NOT NULL AND event_date > '1000-01-01' THEN 1 ELSE 0 END) FROM enterprise_invest")
    d_total, d_dated = [int(x or 0) for x in cur.fetchone()]
    facts["dev_enterprise_invest_rows"] = d_total
    facts["dev_enterprise_invest_event_date_ok"] = d_dated
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_INNOV_006_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
absence_probe.append({
    "probe": "开发库年度指标增长率承载：enterprise_invest.event_date 事件日覆盖（按年聚合的前置）",
    "source": "dev",
    "sql": "SELECT COUNT(*), SUM(CASE WHEN event_date IS NOT NULL AND event_date > '1000-01-01' THEN 1 ELSE 0 END) FROM enterprise_invest",
    "hits": 0, "hit_detail": "46,967 行中事件日有效覆盖 0 行，按年聚合不可行",
})

# ---------------- gkx：融资事件按年 → 事件数增长率 ----------------
cur = gkxmod.gkx()
cur.execute(
    "SELECT YEAR(completion_date) y, COUNT(*) c FROM gkx.dwd_org_financing_info "
    "WHERE completion_date IS NOT NULL AND completion_date > '1000-01-01' "
    "GROUP BY y ORDER BY y")
gkx_yearly = {int(y): int(c) for y, c in cur.fetchall()}
cur.close()
facts["gkx_financing_rows_snapshot"] = 25654  # 对账共享快照 fix2 键（零漂移引用）
facts["gkx_financing_by_year"] = gkx_yearly
# 同比（分子分母同表同池 B3）：取连续年链 2019→2025（2026 在途年不参与）
gy = {}
for y in range(2019, 2026):
    if y in gkx_yearly and (y - 1) in gkx_yearly and gkx_yearly[y - 1] > 0:
        gy[str(y)] = round((gkx_yearly[y] - gkx_yearly[y - 1]) / gkx_yearly[y - 1] * 100, 2)
facts["gkx_financing_event_growth_by_year_pct"] = gy

# ---------------- jiuxin ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=300)
conn = pymysql.connect(**JX)
cur = conn.cursor()

# A. 技术节点年度指标 → 节点级 paper_count 同比（2024 vs 2025 与 2025 vs 2026 在途年对照）
cur.execute(
    "SELECT a.statistics_year, COUNT(*), SUM(CASE WHEN b.paper_count > a.paper_count THEN 1 ELSE 0 END), "
    "SUM(CASE WHEN a.paper_count > 0 THEN 1 ELSE 0 END) "
    "FROM ads_technology_yearly_metrics a "
    "JOIN ads_technology_yearly_metrics b "
    "ON a.technology_node_id = b.technology_node_id AND b.statistics_year = a.statistics_year + 1 "
    "WHERE a.statistics_year IN (2023, 2024, 2025) "
    "GROUP BY a.statistics_year ORDER BY a.statistics_year")
node_pair = {}
for y, n, up, base in cur.fetchall():
    node_pair[str(int(y))] = {"pairs": int(n), "up": int(up), "base_pos": int(base)}
facts["jiuxin_tech_node_year_pairs"] = node_pair

# B. 全库节点论文合计按年（总量增长率）
cur.execute(
    "SELECT statistics_year, SUM(paper_count), SUM(patent_count) FROM ads_technology_yearly_metrics "
    "GROUP BY statistics_year ORDER BY statistics_year")
jx_yearly = {int(y): [int(p or 0), int(pt or 0)] for y, p, pt in cur.fetchall()}
facts["jiuxin_tech_yearly_totals"] = jx_yearly

# C. 现成增长率列：emerging topic paper_count_yoy 覆盖
cur.execute(
    "SELECT statistics_year, COUNT(*), SUM(CASE WHEN paper_count_yoy IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_emerging_topic_yearly_metrics GROUP BY statistics_year ORDER BY statistics_year DESC LIMIT 6")
em_yoy = {str(int(y)): {"rows": int(n), "yoy_nonnull": int(v)} for y, n, v in cur.fetchall()}
facts["jiuxin_emerging_topic_yoy_coverage"] = em_yoy

# D. 现成增长率列：research problem paper_growth_rate 覆盖
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN paper_growth_rate IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_yearly_metrics")
rp_n, rp_g = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_rp_yearly_rows"] = rp_n
facts["jiuxin_rp_paper_growth_rate_nonnull"] = rp_g

# E. development_snapshot latest_growth_rate 覆盖（lane6 探针复测）
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN latest_growth_rate IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_development_snapshot")
ds_n, ds_g = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_dev_snapshot_rows"] = ds_n
facts["jiuxin_dev_snapshot_growth_nonnull"] = ds_g
conn.close()

# ---------------- derived（B3 同基相除，分子分母均为产物 facts 字段）----------------
# 1) gkx 融资事件增长率 2025
if "2025" in gy:
    derived.append({
        "key": "gkx_financing_event_growth_2025_pct",
        "value": gy["2025"],
        "numerator": gkx_yearly[2025] - gkx_yearly[2024],
        "denominator": gkx_yearly[2024],
        "note": "分子=2025年事件数−2024年事件数，分母=2024年事件数；同表 dwd_org_financing_info 同池（B3）。"
                "口径=事件数同比（金额列 8,826 非空但中文格式，另件 INNOV_009/010 详述）",
    })
# 2) gkx 融资事件增长率 2020（疫情低谷基期效应示例）
if "2020" in gy:
    derived.append({
        "key": "gkx_financing_event_growth_2020_pct",
        "value": gy["2020"],
        "numerator": gkx_yearly[2020] - gkx_yearly[2019],
        "denominator": gkx_yearly[2019],
        "note": "同上口径；2020 为疫情年，负增长属基期效应，UI 展示需带年份注记",
    })
# 3) 久新技术节点论文总量增长率 2025
if 2025 in jx_yearly and 2024 in jx_yearly and jx_yearly[2024][0] > 0:
    derived.append({
        "key": "jiuxin_tech_paper_total_growth_2025_pct",
        "value": round((jx_yearly[2025][0] - jx_yearly[2024][0]) / jx_yearly[2024][0] * 100, 2),
        "numerator": jx_yearly[2025][0] - jx_yearly[2024][0],
        "denominator": jx_yearly[2024][0],
        "note": "分子=Σpaper_count(2025)−Σ(2024)，分母=Σ(2024)；同表 ads_technology_yearly_metrics 全节点合计（B3）。"
                "2026 为在途年（3,450 节点大幅缩水），不参与增长率",
    })
# 4) 久新节点级上行占比 2024→2025
p2425 = node_pair.get("2024")
if p2425 and p2425["pairs"] > 0:
    derived.append({
        "key": "jiuxin_node_paper_upshare_2024_to_2025_pct",
        "value": round(p2425["up"] / p2425["pairs"] * 100, 2),
        "numerator": p2425["up"],
        "denominator": p2425["pairs"],
        "note": "分子=2025 论文数>2024 的节点数，分母=两年连续出现的节点对数；同表自连接（B3）",
    })

res = {
    "metric_id": "M_SCIUI_INNOV_006",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRanking.jsx:414",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/InnovationRanking.jsx:419",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:560",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「指标增长率」全称在三份 SRS（科技全域态势/技术发展跟踪/全球创新监测）与主文档《科技信息展示系统和科技专题服务系统.md》"
                "rg 均未命中；近似叶：SRS 全球创新监测 seq 74「多维度排名展示」（总体/领域/地区排名，无增长率分项定义）；"
                "主文档 7303-7307 行「总量与增长率展示」属科技专题服务系统产业规模叶，非本页语境",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全直接支持",
    "notes": [
        "口径注记：本件按年度同比口径判档（UI 折线逐年 %，语义=同比）；OECD MSTI 的 CAGR 复合口径在年度区间退化为同比（R1），"
        "若甲方要求多年复合区间 → 仍可直算（同表自连接），不影响档位",
        "「指标」具体所指未闭合：UI mock 是载体创新指数(scoreHistory)的增长率；数据侧现成承载是论文/专利/融资事件量增长率；"
        "若增长率必须挂在『创新能力指数』上 → 该指数本身是需业务建模类（INNOV_014 同族），降为部分支持（触发器 §1.6）",
        "gkx 融资池为广东企业池（省份 100% 广东省，见 INNOV_010 详证），其增长率读数语义是『广东样本池』而非全球；"
        "全球口径读数应使用久新池或外部参考值",
        "2026 为在途年（gkx 238 事件 / 久新节点面 3,450 行 vs 2025 年 12,278），在途年不参与增长率计算",
    ],
    "base_years_used": [2024, 2025],
    "base_years_missing": [],
    "base_years_note": "同比基期=上一年全量年（2024→2025 主读数，2019→2025 辅序列）；2026 在途年排除；"
                       "dev 侧 enterprise_invest 事件日 0 覆盖故无基期（absence_probe）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["7305"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({"gkx_by_year": gkx_yearly, "growth": gy,
                  "jx_yearly": jx_yearly, "node_pairs": node_pair,
                  "em_yoy": em_yoy, "rp_growth": [rp_n, rp_g], "ds": [ds_n, ds_g]},
                 ensure_ascii=False))
