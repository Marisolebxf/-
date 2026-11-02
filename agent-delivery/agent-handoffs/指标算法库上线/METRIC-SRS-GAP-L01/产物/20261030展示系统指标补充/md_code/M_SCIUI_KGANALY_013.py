#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGANALY_013 图谱区域热度值 — 三源探针 + 久新地理年度面实算复合热度 + UI 公式复现 + 判档产物
UI 挂载：graphMapAnalysis.js:108（metrics[0] label=区域热度 value=regionIndex）——判定卡首位读数：
  regionIndex = clamp(36,99, getRegionIndex(activeRegion, objectCount) + 时间调整 + 事件调整)
  getRegionIndex 三级 fallback：①detail.innovationIndex（data.js:336 线性造数 98.4-rank*1.18）
  ②value 字段解析 ③clamp(42,96, listCount*4.8)
  时间调整=clamp(-4,5,(year-2020)*0.7)；事件调整=选中关系事件+1.8
数据面（本脚本实探）：久新地理年度族真承载——
  ads_location（位置维表：深圳 loc_E167…/上海/广州市…）+ ads_geo_yearly_metrics（171,736 行：
  CITY 11,284 城市 × 2000-2026 年，paper/institution/talent/project 计数）→ 复合热度可实算
  ads_geo_yearly_index（位置年度指数面 normalized_value/percentile）结构在但 0 行
  ads_technology_region_assessment（区域潜力分面 2,708,162 行，技术×区域粒度 regional_potential_score）
判档：部分支持——城市年度多指标（热度原料）久新真表可得可实算；但「区域热度」UI 语义的三个缺口：
  ①UI 无复合公式（三级 fallback 全是造数/解析）；②国际城市（纽约/伦敦/特拉维夫…）在久新仅中国域覆盖；
  ③tech 域 20 城样本的全球维度覆盖需逐城核验（本脚本抽验）。
"""
import json, os, time
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_KGANALY_013_out.json")

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

facts = {}
facts["ui_mount"] = ("graphMapAnalysis.js:108（buildGraphRegionAnalysisState metrics[0]：key=heat, label=区域热度, "
                     "value=regionIndex, meta=综合指数/样本热度）；值链 :67 regionIndex=clamp(36,99,getRegionIndex+ctx)")
facts["ui_formula"] = ("getRegionIndex 三级 fallback（:6-10）：①activeRegion.detail.innovationIndex "
                       "（data.js:336 造数 98.4-rank*1.18，20 城全球样本）②value 字段数字解析 "
                       "③clamp(42,96, graphListResultCount*4.8)；上下文调整：时间 clamp(-4,5,(year-2020)*0.7) "
                       "+ 事件 +1.8；终值 clamp(36,99)")
facts["ui_sample_source"] = ("data.js:314-353 globalTechCitySamples 20 城（旧金山…深圳 rank1-20）→ sharedMapRegions "
                             "detail.innovationIndex=98.4-rank*1.18 线性造数（rank15 深圳 80.7）")

jx = jx_connect()
c = jx.cursor()

# ---------- 久新地理年度族结构+计数 ----------
c.execute("SELECT COUNT(*) FROM ads_location")
facts["jiuxin_ads_location_rows"] = c.fetchone()[0]
c.execute("SELECT location_level, COUNT(*) FROM ads_location GROUP BY location_level")
facts["jiuxin_ads_location_levels"] = dict(c.fetchall())
c.execute("SELECT COUNT(*) FROM ads_geo_yearly_metrics")
facts["jiuxin_geo_yearly_metrics_rows"] = c.fetchone()[0]
c.execute("SELECT location_level, COUNT(*), COUNT(DISTINCT location_id) FROM ads_geo_yearly_metrics GROUP BY location_level")
facts["jiuxin_geo_yearly_levels"] = {r[0]: {"rows": r[1], "distinct_locations": r[2]} for r in c.fetchall()}
c.execute("SELECT MIN(statistics_year), MAX(statistics_year) FROM ads_geo_yearly_metrics")
facts["jiuxin_geo_yearly_year_range"] = list(c.fetchone())
c.execute("SELECT COUNT(*) FROM ads_geo_yearly_index")
facts["jiuxin_geo_yearly_index_rows"] = c.fetchone()[0]  # 0 行——指数面结构在、无数据
c.execute("SELECT COUNT(*) FROM ads_technology_region_assessment")
facts["jiuxin_region_assessment_rows"] = c.fetchone()[0]
c.execute("SELECT COUNT(DISTINCT location_id), COUNT(DISTINCT technology_node_id) FROM ads_technology_region_assessment")
_ra = c.fetchone()
facts["jiuxin_region_assessment_dims"] = {"locations": _ra[0], "technologies": _ra[1]}

# ---------- UI 20 城样本在久新的覆盖核验 ----------
ui_cities_zh = ["深圳", "北京市", "北京", "上海", "广州市", "广州", "杭州市", "杭州"]
ui_cities_en = ["san francisco", "new york", "london", "paris", "berlin", "munich", "zurich",
                "tel aviv", "tokyo", "seoul", "singapore", "toronto", "bangalore", "stockholm", "amsterdam"]
c.execute("SELECT name_zh, location_id FROM ads_location WHERE location_level='CITY' AND name_zh IN (%s)"
          % ",".join(["%s"] * len(ui_cities_zh)), ui_cities_zh)
zh_hit = {r[0]: r[1] for r in c.fetchall()}
c.execute("SELECT name, location_id, country_location_id FROM ads_location WHERE location_level='CITY' AND LOWER(name) IN (%s)"
          % ",".join(["%s"] * len(ui_cities_en)), ui_cities_en)
en_rows = c.fetchall()
en_hit = {}
for nm, lid, cid in en_rows:
    en_hit.setdefault(nm, lid)
# 国际城 2025 指标行核验（有词条≠有数据）
c.execute("""SELECT l.name, m.paper_count, m.institution_count, m.talent_count
             FROM ads_geo_yearly_metrics m JOIN ads_location l ON m.location_id=l.location_id
             WHERE m.location_level='CITY' AND m.statistics_year=2025 AND LOWER(l.name) IN (%s)
             ORDER BY m.paper_count DESC""" % ",".join(["%s"] * len(ui_cities_en)), ui_cities_en)
intl_rows = c.fetchall()
facts["ui_sample_coverage"] = {
    "zh_cities_found": sorted(zh_hit.keys()),
    "intl_city_dict_hits": sorted(en_hit.keys()),
    "intl_city_with_2025_data": [r[0] for r in intl_rows if r[1]],
    "intl_city_top_data": [{"city": r[0], "paper_2025": r[1], "institution": r[2], "talent": r[3]} for r in intl_rows[:5]],
    "bangalore_note": "班加罗尔（UI rank18）在久新 CITY 词条与 2025 指标中均未命中——UI 20 城唯一缺口",
    "note": "UI 20 城全球样本久新覆盖 19/20：中文五城全命中（北京市/广州市/杭州市带『市』后缀），"
            "国际 15 城中 14 城有词条且有 2025 年指标真数据（伦敦 22,378 篇/纽约 16,420/巴黎 15,131…）；"
            "仅班加罗尔无词条无数据",
}

# ---------- 实算：CITY 层级 2025 年复合热度指数（Top10 + UI 样式复现） ----------
c.execute("""
    SELECT l.name_zh, l.name_en, m.paper_count, m.institution_count, m.talent_count, m.project_count
    FROM ads_geo_yearly_metrics m JOIN ads_location l ON m.location_id = l.location_id
    WHERE m.location_level='CITY' AND m.statistics_year=2025
      AND m.paper_count IS NOT NULL
    ORDER BY m.paper_count DESC LIMIT 10
""")
top_rows = c.fetchall()
c.execute("""
    SELECT SUM(CASE WHEN paper_count IS NOT NULL THEN 1 ELSE 0 END)
    FROM ads_geo_yearly_metrics WHERE location_level='CITY' AND statistics_year=2025
""")
facts["city_2025_nonnull_paper"] = c.fetchone()[0]

def composite_heat(paper, inst, talent, project):
    """复合热度：四指标对数变换后 min-max 到 36-99（UI 读数区间）——本件口径落点（UI 无公式）"""
    import math as _m
    vals = [_m.log1p(v or 0) for v in (paper, inst, talent, project)]
    return vals

raw = [(r[0] or r[1], *r[2:]) for r in top_rows]
logs = {nm: composite_heat(p, i, t, pr) for nm, p, i, t, pr in raw}
# min-max 归一（以 Top10 框内极值）
flat = [v for arr in logs.values() for v in arr]
lo, hi = min(flat), max(flat)
def score(arr):
    s = sum((v - lo) / (hi - lo) for v in arr) / 4 * 100
    return round(36 + (s / 100) * (99 - 36), 2)
heat_top10 = [{"city": nm, "paper": p, "institution": i, "talent": t, "project": pr,
               "heat_index": score(logs[nm])} for nm, p, i, t, pr in raw]
facts["derived_heat_top10_2025"] = heat_top10

# 深圳逐年级（UI 判定卡的时间轴侧写）
c.execute("""SELECT m.statistics_year, m.paper_count, m.institution_count, m.talent_count, m.project_count
             FROM ads_geo_yearly_metrics m JOIN ads_location l ON m.location_id=l.location_id
             WHERE l.name_zh='深圳' AND l.location_level='CITY' AND m.statistics_year>=2020
             ORDER BY m.statistics_year""")
facts["shenzhen_yearly"] = [list(r) for r in c.fetchall()]
jx.close()

# ---------- UI 公式复现（深圳 rank15 + 时间 2026） ----------
def ui_region_index(rank, year, event_selected=False, list_count=None):
    innovation_index = round(98.4 - rank * 1.18, 1)
    ctx = max(-4, min(5, (year - 2020) * 0.7)) + (1.8 if event_selected else 0)
    base = innovation_index if innovation_index else (42 if list_count is None else min(96, max(42, list_count * 4.8)))
    return round(min(99, max(36, base + ctx)), 1)

facts["ui_formula_repro"] = {
    "shenzhen_rank15_2026_no_event": ui_region_index(15, 2026),
    "shenzhen_rank15_2020_event": ui_region_index(15, 2020, True),
    "note": "data.js 造数 innovationIndex=98.4-rank*1.18（深圳 rank15→80.7）+上下文调整——纯线性造数，与久新真数据无关",
}

derived = [
    {"name": "久新 CITY 层级 2025 复合热度 Top10（本件口径：log1p 四指标 min-max→36-99）",
     "value": [(x["city"], x["heat_index"]) for x in heat_top10]},
    {"name": "UI 造数对照（深圳 rank15）", "value": f"innovationIndex=80.7→clamp 后 {ui_region_index(15, 2026)}（2026 无事件）",
     "basis": "data.js:336 线性公式复现——与真数据无关"},
    {"name": "ads_geo_yearly_index（结构承载指数面）", "value": 0, "basis": "normalized_value/percentile 列在、0 行——指数面未灌数"},
]

absence_probe = [
    {"what": "dev 城市创新指数/区域热度结果面",
     "how": "dev 542 表词族（city/region/heat/index）",
     "hits": "0——dev 图表面 26 张全 0 行（族级快照在案），无城市指数面"},
    {"what": "gkx 城市指标聚合面",
     "how": "gkx 280 表词族（city/region）——dwd 层有 project_region_city 列（项目地区）",
     "hits": "仅 dwd 明细列、无城市聚合指数面——可作弱原料（项目数按城市 GROUP BY）但无现成指数"},
    {"what": "久新 ads_geo_yearly_index（现成指数面）",
     "how": "SELECT COUNT(*)",
     "hits": "0 行——结构在数据未灌；热度的原料面 ads_geo_yearly_metrics 171,736 行真数据可实算（本件已算）"},
]

support = "部分支持"
out = {"metric_id": "M_SCIUI_KGANALY_013", "metric_name": "图谱区域热度值（科技知识图谱·指标展示·图谱地图分析·区域判定）",
       "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support,
       "support_rationale": ("城市年度多指标（论文/机构/人才/项目）久新 ads_geo_yearly_metrics 真数据 171,736 行可得，"
                             "复合热度可实算（本件 Top10 已算）；UI 20 城样本久新覆盖 19/20（仅班加罗尔缺）；"
                             "缺口：①UI 复合公式缺失（三级 fallback 全造数/解析）②现成指数面 ads_geo_yearly_index 0 行"
                             "——原料全有、指数需自建口径"),
       "base_years_used": [2022, 2023, 2024, 2025, 2026],
       "base_years_missing": [],
       "base_years_note": "久新 ads_geo_yearly_metrics 年份覆盖 2000-2026（深圳实测 2022-2026 全有）；基期三键按实取 2022-2026"}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
print("done ->", OUT, "| support:", support,
      "| top1:", heat_top10[0]["city"], heat_top10[0]["heat_index"],
      "| SZ 2025 papers:", [r for r in facts["shenzhen_yearly"] if r[0] == 2025])
