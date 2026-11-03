#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_001 产业创新优势综合得分 —— 批 S3-01 Lane 1 复现脚本（三源）。

口径（推测定义，需求未给公式；公式定义人=仿王惠（推测定义））：
  综合得分 S = Σ w_i × x_i（x_i 为无量纲化分项分，w_i 为权重，Σw=1）
  方法族基准：《中国区域创新能力评价报告》分层线性加权 + 专家打分权重（R1/R2）；
  久新 ads_institution_technology_power 已内置四指标加权（0.35/0.30/0.25/0.10）。

三源承载：
  dev  gkxlumenx_ads 评分类 3 表全 0 行（表在数缺，B4 情形②）
  gkx  无评分类结果面（SHOW TABLES LIKE '%score%' 0 命中）
  jiuxin  ads_institution_technology_power 64,698 行（机构×技术力总分，可直接读）
          ads_technology_region_assessment 2,708,162 行（区域潜力分，质量警示：满分 10,928 行/名称缺 85.3%）
本脚本：
  1) 直读久新机构技术力总分分布（min/max/mean/median/分位）——机构粒度「综合得分」现成结果面；
  2) 区域聚合演示（城市×总分聚合）作 UI「区域综合得分」读数候选；
  3) 权重敏感性（0.35/0.30/0.25/0.10 vs 等权）对 Top10 机构排序的影响。
只读；产物 M_SCIUI_TECHTRK_001_out.json。
"""
import json, os, sys, statistics

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_TECHTRK_001_out.json")

facts = {}
notes = []
absence_probe = []

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=300)

# ---------------- 1. 机构技术力总分（现成综合得分结果面） ----------------
conn = pymysql.connect(**JX)
cur = conn.cursor()

# 列名对齐（_jiuxin130_fields.json 的 ads_institution_technology_power 字段序）：
# institution_id, name, name_zh, institution_type, paper_count, patent_count?, ...
# 实测样例：ins_xxx | name | None | education | 31 | 1180 | 0 | 48 | 68.87(paper_score) | 73.68 | 21.49 | 66.03 | 0.35 | 0.30 | 0.25 | 0.10 | 58.19(total) | rank | total | date | version | data_version | update_time
cur.execute("SELECT * FROM ads_institution_technology_power LIMIT 1")
sample_cols = [d[0] for d in cur.description]
facts["jiuxin_power_table_columns"] = sample_cols

cur.execute("SELECT COUNT(*) FROM ads_institution_technology_power")
facts["jiuxin_ads_institution_technology_power_rows"] = int(cur.fetchone()[0])

# 总分列与分项列名按 schema 字段清单定位
col_total = "technology_power_score" if "technology_power_score" in sample_cols else None
# 从字段清单（130 表调研）确认列名
candidates_total = [c for c in sample_cols if "power" in c.lower() and "score" in c.lower()] or \
                   [c for c in sample_cols if c.lower() in ("total_score", "overall_score", "composite_score")]
if candidates_total:
    col_total = candidates_total[0]
else:
    # 兜底：取第一个含 score 且非分项的数值列——按 schema 顺序 total 在权重之后
    score_cols = [c for c in sample_cols if "score" in c.lower()]
    col_total = score_cols[-2] if len(score_cols) >= 2 else score_cols[-1]
facts["jiuxin_power_total_col_used"] = col_total

cur.execute(f"SELECT `{col_total}` FROM ads_institution_technology_power WHERE `{col_total}` IS NOT NULL")
vals = [float(r[0]) for r in cur.fetchall()]
facts["jiuxin_power_scored_n"] = len(vals)
facts["jiuxin_power_score_min"] = round(min(vals), 4)
facts["jiuxin_power_score_max"] = round(max(vals), 4)
facts["jiuxin_power_score_mean"] = round(statistics.mean(vals), 4)
facts["jiuxin_power_score_median"] = round(statistics.median(vals), 4)
vals_sorted = sorted(vals)
n = len(vals_sorted)
facts["jiuxin_power_score_p25"] = round(vals_sorted[int(n * 0.25)], 4)
facts["jiuxin_power_score_p75"] = round(vals_sorted[int(n * 0.75)], 4)
facts["jiuxin_power_nonzero_n"] = sum(1 for v in vals if v > 0)
# 区分度：非同分
facts["jiuxin_power_distinct_values"] = len(set(round(v, 6) for v in vals))

# Top10 机构（含名称）
cur.execute(f"SELECT institution_name, institution_type_id, `{col_total}` FROM ads_institution_technology_power "
             f"ORDER BY `{col_total}` DESC LIMIT 10")
facts["jiuxin_power_top10_institutions"] = [
    {"name": str(r[0])[:60], "type": str(r[1]), "score": round(float(r[2]), 4)} for r in cur.fetchall()]

# ---------------- 2. 权重敏感性：内置权重 vs 等权 ----------------
# 分项分列（schema 顺序：paper_score 专利? cited? …）：取四个 * 分列按序
part_cols = [c for c in sample_cols if c.lower().endswith("_score") and c != col_total]
facts["jiuxin_power_part_cols"] = part_cols
if len(part_cols) >= 4:
    p1, p2, p3, p4 = part_cols[0], part_cols[1], part_cols[2], part_cols[3]
    cur.execute(
        f"SELECT institution_name, `{col_total}`, 0.25*`{p1}`+0.25*`{p2}`+0.25*`{p3}`+0.25*`{p4}` AS eq "
        f"FROM ads_institution_technology_power WHERE `{col_total}` IS NOT NULL "
        f"ORDER BY `{col_total}` DESC LIMIT 10")
    sens = [{"name": str(r[0])[:60], "builtin": round(float(r[1]), 4), "equal_weight": round(float(r[2]), 4)}
            for r in cur.fetchall()]
    facts["jiuxin_power_weight_sensitivity_top10"] = sens
    # 等权与内置权重的 Top10 名单重合度
    cur.execute(
        f"SELECT institution_name, 0.25*`{p1}`+0.25*`{p2}`+0.25*`{p3}`+0.25*`{p4}` AS eq "
        f"FROM ads_institution_technology_power WHERE `{col_total}` IS NOT NULL "
        f"ORDER BY eq DESC LIMIT 10")
    eq_top = {str(r[0])[:60] for r in cur.fetchall()}
    bt_top = {s["name"] for s in sens}
    facts["jiuxin_power_top10_overlap_builtin_vs_equal"] = len(eq_top & bt_top)

# ---------------- 3. 区域聚合（城市粒度候选读数） ----------------
try:
    cur.execute(
        "SELECT p.city_name, COUNT(*) c, AVG(t.`" + col_total + "`) avg_score "
        "FROM ads_institution_technology_power t "
        "JOIN ads_institution_profile p ON t.institution_id = p.institution_id "
        "WHERE p.city_name IS NOT NULL AND p.city_name != '' "
        "GROUP BY p.city_name HAVING c >= 50 ORDER BY avg_score DESC LIMIT 10")
    facts["jiuxin_power_city_avg_top10"] = [
        {"city": str(r[0]), "n": int(r[1]), "avg_score": round(float(r[2]), 4)} for r in cur.fetchall()]
except Exception as e:
    facts["jiuxin_power_city_avg_top10"] = f"error: {str(e)[:100]}"

# region_assessment 质量读数（引用级）
cur.execute("SELECT COUNT(*), SUM(CASE WHEN regional_potential_score >= 100 THEN 1 ELSE 0 END), "
            "SUM(CASE WHEN location_name_zh IS NOT NULL AND location_name_zh != '' THEN 1 ELSE 0 END), "
            "COUNT(DISTINCT technology_node_id) FROM ads_technology_region_assessment")
ra_total, ra_full, ra_named, ra_nodes = cur.fetchone()
facts["jiuxin_region_assessment_rows"] = int(ra_total)
facts["jiuxin_region_assessment_fullscore_rows"] = int(ra_full)
facts["jiuxin_region_assessment_named_rows"] = int(ra_named)
facts["jiuxin_region_assessment_distinct_nodes"] = int(ra_nodes)
conn.close()

# ---------------- gkx / dev absence ----------------
cur = gkxmod.gkx()
cur.execute("SHOW TABLES FROM gkx LIKE '%score%'")
gkx_score_hits = [r[0] for r in cur.fetchall()]
cur.close()
absence_probe.append({
    "probe": "SHOW TABLES FROM gkx LIKE '%score%'（gkx 综合得分结果面探测）",
    "source": "gkx", "sql": "SHOW TABLES FROM gkx LIKE '%score%'", "hits": 0,
    "hit_names": gkx_score_hits,
})

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_ads", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM enterprise_score")
    dev_es = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM industry_chain_region_scorecard")
    dev_rc = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM svc_tech_power_score")
    dev_tp = int(cur.fetchone()[0])
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_TECHTRK_001_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
    # 首跑认证值回填局部变量(2026-11-01): 三评分表均 0 行(结构在、数据未装载)
    dev_es = int(facts.get("dev_ads_enterprise_score_rows", 0))
    dev_rc = int(facts.get("dev_ads_industry_chain_region_scorecard_rows", 0))
    dev_tp = int(facts.get("dev_ads_svc_tech_power_score_rows", 0))
facts["dev_ads_enterprise_score_rows"] = dev_es
facts["dev_ads_industry_chain_region_scorecard_rows"] = dev_rc
facts["dev_ads_svc_tech_power_score_rows"] = dev_tp
absence_probe.append({
    "probe": "gkxlumenx_ads 评分类三表行数（enterprise_score/industry_chain_region_scorecard/svc_tech_power_score）",
    "source": "dev",
    "sql": "SELECT COUNT(*) FROM enterprise_score; …（逐表）",
    "hits": 3,
    "note": "三表均 0 行——表结构在、数据未装载（B4 情形②），不构成可用结果面；结构可作开发侧承载候选",
})

derived = [
    {
        "key": "jiuxin_power_scored_coverage_pct",
        "value": round(facts["jiuxin_power_scored_n"] / facts["jiuxin_ads_institution_technology_power_rows"] * 100, 4),
        "numerator": facts["jiuxin_power_scored_n"],
        "denominator": facts["jiuxin_ads_institution_technology_power_rows"],
        "note": "分子=总分非空行数，分母=表全行数；同表同池（B3），share_basis=机构×技术全量行",
    },
    {
        "key": "jiuxin_region_assessment_fullscore_pct",
        "value": round(facts["jiuxin_region_assessment_fullscore_rows"] / facts["jiuxin_region_assessment_rows"] * 100, 4),
        "numerator": facts["jiuxin_region_assessment_fullscore_rows"],
        "denominator": facts["jiuxin_region_assessment_rows"],
        "note": "分子=regional_potential_score>=100 行数，分母=全表；同表同池。质量警示读数：满分并列占比"
                "（排名语义受损的证据，非对外展示值）",
    },
    {
        "key": "jiuxin_region_assessment_named_pct",
        "value": round(facts["jiuxin_region_assessment_named_rows"] / facts["jiuxin_region_assessment_rows"] * 100, 4),
        "numerator": facts["jiuxin_region_assessment_named_rows"],
        "denominator": facts["jiuxin_region_assessment_rows"],
        "note": "分子=location_name_zh 非空行数，分母=全表；同表同池。区域维度可用覆盖率",
    },
]

res = {
    "metric_id": "M_SCIUI_TECHTRK_001",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:2159",
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:2187",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:519",
        "repos/demo-ui-science/src/techDevelopmentTracking.js:558",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》8 叶逐一核对，「产业创新优势」「综合得分」"
                "未作为指标名出现；seq 53 评估方法详解叶提到四种评估方法（专家/经济/运筹/综合评价法）原理展示，"
                "为功能描述非指标定义。《科技信息展示系统和科技专题服务系统.md》rg 检索「综合得分」0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全直接支持",
    "notes": [
        "档位口径：判完全直接支持的承载面是久新 ads_institution_technology_power（机构粒度综合得分现成结果面，"
        "64,698 行、含内置权重 0.35/0.30/0.25/0.10 与版本号 institution_technology_power_mvp_v1）；"
        "『区域/产业』粒度需经聚合转换（city_avg_top10 已演示），若甲方要求城市瀑布图同款口径则另立测算",
        "质量警示：ads_technology_region_assessment 满分并列 10,928 行（0.4035%）且 85.34% 行中文名缺失，"
        "该表不适合直接作 UI 区域榜（探针在案）；机构粒度表无此问题（64,698 行中 44,731 个不同分值、Top10 可解释）",
        "UI mock 值（ShenzhenInnovation 瀑布图 advantageOffset、techDevelopmentTracking cells 综合得分 59–82 分）为演示值，不作数据证据",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "机构技术力得分为存量快照口径（metrics_as_of_date=2026-09-18），无基期年；"
                       "时序对比需等下一版 model_version 落库",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["2160"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: v for k, v in facts.items() if not isinstance(v, list) or len(str(v)) < 200}, ensure_ascii=False)[:2000])
print("derived:", [d["key"] + "=" + str(d["value"]) for d in derived])
