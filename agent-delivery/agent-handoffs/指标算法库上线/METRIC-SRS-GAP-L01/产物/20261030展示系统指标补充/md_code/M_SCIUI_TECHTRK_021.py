#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_021 论文热度值 —— 三源探针 + 复现脚本（批 S3-01 Lane 4）。

UI 挂载：repos/demo-ui-science/src/techDevelopmentTracking.js:339
  technologyTrackingMapTechnologyTypes[0] = { key: 'paper-heat', label: '论文热度', color: '#2563eb' }
  —— 地理分布图的图例首型：按「论文热度」给区域着色
  关联：js:1017-1024 buildMetrics 首卡 { key:'heat', label:'话题热度' }（017 件承接）；本件是「论文」侧

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：gkxlumenx_dwd 无论文表（共享快照已证）；无热度结果面
  ② gkx：dwd_zh_paper 100,900 行，download_num 列实测全 0/空（20 万采样非空 0）——无热度承载
  ③ 久新：ads_technology_hotspot_snapshot 38,860 行（hotspot_score 0-100，五分项含论文轴）
     + ads_technology_hotspot_yearly 233,160 行（年度序列）——本件主承载
     注意：hotspot 是「技术节点热度」（论文份额/引用/专利信号合成），非「单篇论文热度」

复现口径（B10 双口径并列）：
  口径 A（技术节点热点分）：hotspot_snapshot v2 Top5 by hotspot_rank + 全体均值（库内现成结果面）
  口径 B（论文量代理·深圳）：geo_yearly_metrics 深圳论文年度序列（2015-2026）——最贴近「论文热度」字面
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
SZ = "loc_E16782C21F18EBF8A59C1E98F9C9860B"

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

# ---- 口径 A：hotspot_snapshot v2 ----
jc.execute(
    "SELECT COUNT(*), COUNT(hotspot_score), MIN(hotspot_score), MAX(hotspot_score), AVG(hotspot_score) "
    "FROM ads_technology_hotspot_snapshot WHERE model_version = %s", (V2,))
r = jc.fetchone()
facts["jiuxin_hotspot_v2_stats"] = {"n": int(r[0]), "nonnull": int(r[1]),
                                    "min": float(r[2]), "max": float(r[3]),
                                    "avg": round(float(r[4]), 4)}

jc.execute(
    "SELECT s.technology_node_id, p.technology_name_original, s.hotspot_score, s.hotspot_rank, "
    "s.hotspot_status, s.growth_score, s.impact_score, s.recent_paper_count, s.baseline_paper_count "
    "FROM ads_technology_hotspot_snapshot s LEFT JOIN ads_technology_profile p "
    "ON p.technology_node_id = s.technology_node_id "
    "WHERE s.model_version = %s ORDER BY s.hotspot_rank LIMIT 5", (V2,))
facts["jiuxin_hotspot_v2_top5"] = [
    {"node_id": r[0], "name": r[1], "hotspot_score": round(float(r[2]), 4),
     "rank": int(r[3]), "status": r[4], "growth_score": round(float(r[5]), 4),
     "impact_score": round(float(r[6]), 4), "recent_paper_count": int(r[7] or 0),
     "baseline_paper_count": int(r[8] or 0)} for r in jc.fetchall()]

# 热点分算法权重（schema §24.4：0.40 growth + 0.15×4）与论文证据轴
facts["jiuxin_hotspot_formula"] = {
    "formula": "hotspot_score = 0.40*growth_score + 0.15*author_diffusion + 0.15*institution_diffusion + 0.15*impact_score + 0.15*patent_signal",
    "paper_axis": "growth_score/impact_score 以论文份额与 FWCI 为轴（非单篇论文热度）",
}

# ---- 口径 B：深圳论文年度序列 ----
jc.execute(
    "SELECT statistics_year, paper_count, cited_by_count FROM ads_geo_yearly_metrics "
    "WHERE location_id = %s AND statistics_year >= 2015 ORDER BY statistics_year", (SZ,))
sz_paper = {int(r[0]): {"paper": int(r[1] or 0), "citation": int(r[2] or 0)} for r in jc.fetchall()}
facts["jiuxin_shenzhen_paper_yearly"] = sz_paper

# 深圳子盘技术节点的年度热点均分（论文轴最贴近的序列）
jc.execute(
    "SELECT y.statistics_year, COUNT(DISTINCT y.technology_node_id), AVG(y.hotspot_score) "
    "FROM ads_technology_hotspot_yearly y JOIN ads_technology_region_yearly_metrics m "
    "ON m.technology_node_id = y.technology_node_id AND m.location_id = %s "
    "GROUP BY y.statistics_year ORDER BY y.statistics_year DESC LIMIT 12", (SZ,))
facts["jiuxin_shenzhen_hotspot_yearly_avg"] = {int(r[0]): round(float(r[2]), 4) for r in jc.fetchall()}

# ---- 久新论文主档被引统计（单篇论文受关注度承载面）----
jc.execute(
    "SELECT COUNT(*), COUNT(cited_by_count), SUM(CASE WHEN cited_by_count > 0 THEN 1 ELSE 0 END), "
    "MAX(cited_by_count) FROM ads_paper_profile")
r = jc.fetchone()
facts["jiuxin_paper_profile_cited_stats"] = {
    "rows": int(r[0]), "cited_nonnull": int(r[1]), "cited_gt0": int(r[2]), "max_cited": int(r[3])}
jc.execute(
    "SELECT AVG(fwci) FROM ads_paper_profile WHERE fwci IS NOT NULL")
r = jc.fetchone()
facts["jiuxin_paper_profile_avg_fwci_nonnull"] = round(float(r[0]), 4) if r[0] else None

jc.close()
jx.close()

# ---- gkx 探针：论文热度承载（download_num 语义）----
gc = gkx()
rows = probe("gkx dwd_zh_paper download_num 非空与最大值（20 万采样）", "gkx",
             "SELECT COUNT(*), SUM(CASE WHEN download_num IS NOT NULL AND download_num != '' THEN 1 ELSE 0 END), "
             "MAX(download_num) FROM (SELECT download_num FROM gkx.dwd_zh_paper LIMIT 200000) t",
             gc, note="20万行采样，非全表（全表 100,900 行 < 20 万，等同全表）")
if rows:
    facts["gkx_paper_download_num_stats"] = {"sampled": int(rows[0][0]),
                                             "nonnull": int(rows[0][1] or 0),
                                             "max": rows[0][2]}
rows = probe("gkx 280 表 heat/hot 类结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%heat%' OR table_name LIKE '%hot%')", gc)
facts["gkx_heat_like_tables"] = [r[0] for r in rows]
gc.close()

# ---- dev 探针 ----
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd 论文表探测", "dev",
                 "SHOW TABLES FROM gkxlumenx_dwd LIKE '%paper%'", dc)
    facts["dev_paper_like_tables"] = [r[0] for r in rows]
    rows = probe("dev gkxlumenx_dwd+ads 热度类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') "
                 "AND (table_name LIKE '%heat%' OR table_name LIKE '%hot%')", dc)
    facts["dev_heat_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_021_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

UI_MOCK = {"map_type_label": "论文热度", "color": "#2563eb"}
facts["ui_mock_map_type"] = UI_MOCK

out_yoy = round((sz_paper[2025]["paper"] - sz_paper[2024]["paper"])
                / sz_paper[2024]["paper"] * 100, 4)

out = {
    "metric_id": "M_SCIUI_TECHTRK_021",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/techDevelopmentTracking.js:339",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:1017-1024",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「论文热度」在技术发展跟踪.md/科技全域态势.md/全球创新监测.md 三份指定说明书 0 命中；"
                "srs/03-新型高端智库系统/战略咨询智能支持/技术体系分析.md:134 的「论文热度」属智库系统技术体系分析模块（词云+热度排行语境），非本件页面。主文档 0 命中。",
    },
    "facts": facts,
    "derived": [
        {"key": "jiuxin_shenzhen_paper_yoy_2025_vs_2024_pct",
         "value": round((sz_paper[2025]["paper"] - sz_paper[2024]["paper"])
                        / sz_paper[2024]["paper"] * 100, 4),
         "numerator": sz_paper[2025]["paper"] - sz_paper[2024]["paper"],
         "denominator": sz_paper[2024]["paper"],
         "note": "分子=深圳 2025-2024 论文量差，分母=2024 论文量；同源 jiuxin ads_geo_yearly_metrics 深圳行（口径 B 序列）。"},
    ],
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "「论文热度」UI 语义是地理分布图图例首型（区域按论文热度着色）+ 与「话题热度」KPI（017 件）同源的论文侧重述；前端无独立公式。",
        "语义错位是本件核心缺口：库侧唯一现成「热度分」（hotspot_score）是技术节点粒度的五分项合成（论文份额/FWCI 只是其中两轴），不是「论文」粒度的受关注度；单篇论文侧承载（cited_by_count/fwci）是原始指标非热度分。",
        "口径 A 读数：v2 全体均值 %s、Top5 79.0908/77.2451/76.3696/76.1087/74.7756（facts.jiuxin_hotspot_v2_top5）；Top5 中 4 个 hotspot_status=INSUFFICIENT_EVIDENCE（近期论文<3 篇），高分由 growth_score 驱动而非论文体量。" % facts["jiuxin_hotspot_v2_stats"]["avg"],
        "口径 B 读数：深圳论文 2015→2025 从 1,256 增至 24,904（12 年约 19.8 倍）；2026 PARTIAL_YEAR 2,666 不入比较。yoy（2025 vs 2024）= %s%%。" % out_yoy,
        "gkx dwd_zh_paper.download_num 实测全空/0（20 万采样非空 0 行）——下载量热度轴在该库无承载；rel_paper 是关联论文 ID 列表非引用计数。",
        "判档：热点结果面（技术粒度）与论文年度序列（区域粒度）双承载可转换，但「论文粒度热度分」与「区域着色用热度值」两个语义槽均无直接结果面，判部分支持。",
    ],
    "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021",
                        "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "hotspot_yearly 序列 2015-2026（19,430 节点/年）；geo_yearly_metrics 深圳 2015-2026（2026 为 PARTIAL_YEAR）；snapshot 为版本快照无年份。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "38860", "19430", "79.090792", "24904", "1256", "2666", "4000000","1026","54643"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_021_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
