#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_020 技术发展指数 —— 三源探针 + 复现脚本（批 S3-01 Lane 4）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:558
  indicatorData 首卡 { name: '技术发展指数', value: 92.5, unit: '分', yoy: 8.3 }（演示值）
  同文件 :63 technologyHeatTrendDefinition.scoreFormula：
  「热度指数 = 40% 文献活跃度 + 30% 专利活跃度 + 20% 产业事件 + 10% 政策/资本信号」——前端自带公式叙事

三源（开发库 gkxlumenx_* 禁 demo / gkx 经 _gkxdb / 久新 Doris 只读）：
  ① 开发库：无指数类结果面（探针留证）
  ② gkx：280 表无 index/exponent 类指数结果面（探针留证）
  ③ 久新：ads_geo_yearly_index 为公式批准前预留空表（COUNT=0，实测留证）——
     唯一结构就绪的指数表无数据；依赖侧 geo_yearly_metrics 年度基础指标齐全（2015-2026）

复现口径（B10 双口径并列，均须披露口径假设）：
  口径 A（深圳六基础指标 min-max 归一 + UI 前端公式权重）：paper/patent 代理/citation/project/talent/institution
         六维各按 2015-2025 序列 min-max 归一到 0-100，2025 年读数按前端公式权重合成
  口径 B（同比口径）：以 2025/2024 论文总量同比作 yoy 读数（对齐 UI '+8.3%' 语义）
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

SZ = "loc_E16782C21F18EBF8A59C1E98F9C9860B"
# UI 前端公式权重（TechDevelopmentPlan.tsx:64）：40% 文献 + 30% 专利 + 20% 产业事件 + 10% 政策/资本
UI_WEIGHTS = {"paper": 0.40, "patent": 0.30, "industry": 0.20, "policy": 0.10}

facts = {}
probes = []


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:180] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:180]})
        return []


jx = pymysql.connect(**JX)
jc = jx.cursor()

# ---- 指数结果面空表核验 ----
jc.execute("SELECT COUNT(*) FROM ads_geo_yearly_index")
facts["jiuxin_geo_yearly_index_rows"] = int(jc.fetchone()[0])

# ---- 深圳年度基础指标（geo_yearly_metrics，2015-2026）----
jc.execute(
    "SELECT statistics_year, paper_count, cited_by_count, project_count, talent_count, institution_count "
    "FROM ads_geo_yearly_metrics WHERE location_id = %s AND statistics_year >= 2015 "
    "ORDER BY statistics_year", (SZ,))
sz_series = {int(r[0]): {"paper": int(r[1] or 0), "citation": int(r[2] or 0),
                          "project": int(r[3] or 0), "talent": int(r[4] or 0),
                          "institution": int(r[5] or 0)} for r in jc.fetchall()}
facts["jiuxin_shenzhen_yearly_metrics_2015_2026"] = sz_series

# ---- 深圳关联专利代理轴（region_yearly_metrics 专利机构证据，年度）----
jc.execute(
    "SELECT statistics_year, SUM(patent_institution_evidence_count) "
    "FROM ads_technology_region_yearly_metrics WHERE location_id = %s "
    "GROUP BY statistics_year ORDER BY statistics_year", (SZ,))
sz_patent = {int(r[0]): int(r[1] or 0) for r in jc.fetchall()}
facts["jiuxin_shenzhen_patent_evidence_yearly"] = sz_patent

# ---- 全域（中国 COUNTRY）对照序列 ----
jc.execute("SELECT location_id FROM ads_location WHERE name_zh='中国' AND location_level='COUNTRY' LIMIT 1")
cn_loc = jc.fetchone()[0]
jc.execute(
    "SELECT statistics_year, paper_count FROM ads_geo_yearly_metrics "
    "WHERE location_id = %s AND statistics_year >= 2015 ORDER BY statistics_year", (cn_loc,))
facts["jiuxin_china_paper_yearly_2015_2026"] = {int(r[0]): int(r[1] or 0) for r in jc.fetchall()}
facts["jiuxin_china_location_id"] = cn_loc

jc.close()
jx.close()

# ---- 口径 A：深圳 min-max 归一（2015-2025 完整年窗，2026 PARTIAL_YEAR 不入窗）----
years_full = [y for y in range(2015, 2026)]  # 2015..2025


def minmax_norm(series_map, years):
    vals = [series_map[y] for y in years if y in series_map]
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return None, mn, mx
    return (lambda v: (v - mn) / (mx - mn) * 100), mn, mx


dims_raw = {
    "paper": {y: sz_series[y]["paper"] for y in years_full},
    "citation": {y: sz_series[y]["citation"] for y in years_full},
    "project": {y: sz_series[y]["project"] for y in years_full},
    "talent": {y: sz_series[y]["talent"] for y in years_full},
    "institution": {y: sz_series[y]["institution"] for y in years_full},
    "patent_proxy": {y: sz_patent.get(y, 0) for y in years_full},
}
norm_cache = {}
for dim, series in dims_raw.items():
    fn, mn, mx = minmax_norm(series, years_full)
    norm_cache[dim] = {"fn": fn, "min": mn, "max": mx,
                       "norm_2025": round(fn(series[2025]), 4) if fn else None}

# 前端公式四槽映射（披露映射假设）：文献→paper；专利→patent_proxy；产业事件→project（项目代理）；
# 政策/资本→institution（无政策/资本年度列，以机构参与代理——最弱假设，note 披露）
slots = {
    "paper": norm_cache["paper"]["norm_2025"],
    "patent": norm_cache["patent_proxy"]["norm_2025"],
    "industry": norm_cache["project"]["norm_2025"],
    "policy": norm_cache["institution"]["norm_2025"],
}
index_2025 = round(sum(slots[k] * UI_WEIGHTS[k] for k in slots), 4)
facts["jiuxin_shenzhen_index_norm_components"] = {
    "paper_2025": norm_cache["paper"]["norm_2025"],
    "patent_proxy_2025": norm_cache["patent_proxy"]["norm_2025"],
    "project_as_industry_2025": norm_cache["project"]["norm_2025"],
    "institution_as_policy_2025": norm_cache["institution"]["norm_2025"],
}
facts["jiuxin_shenzhen_index_2025_ui_formula"] = index_2025

# ---- 口径 B：yoy（2025 vs 2024 论文）----
yoy_paper = round((sz_series[2025]["paper"] - sz_series[2024]["paper"])
                  / sz_series[2024]["paper"] * 100, 4)
facts["jiuxin_shenzhen_paper_yoy_2025_vs_2024_pct"] = yoy_paper

# ---- gkx absence 探针 ----
gc = gkx()
rows = probe("gkx 280 表 index/exponent/指数类结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%index%' OR table_name LIKE '%exponent%')", gc)
facts["gkx_index_like_tables"] = [r[0] for r in rows]
gc.close()

# ---- dev absence 探针 ----
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev gkxlumenx_dwd+ads 指数类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_dwd','gkxlumenx_ads') AND table_name LIKE '%index%'", dc)
    facts["dev_index_like_tables"] = [[r[0], r[1]] for r in rows]
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_020_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

UI_MOCK = {"value": 92.5, "unit": "分", "yoy": 8.3}
facts["ui_mock_index_card"] = UI_MOCK
facts["ui_formula_weights"] = UI_WEIGHTS

out = {
    "metric_id": "M_SCIUI_TECHTRK_020",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:558",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:63-66",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「技术发展指数」在三份指定说明书与主需求文档均未出现（srs/ 全目录检索 0 命中）；"
                "kept_items 的 l3『观察＞技术发展指数』是筛选记录对 UI 卡片的层级归位，非 SRS 原文。",
    },
    "facts": facts,
    "derived": [
        {"key": "jiuxin_shenzhen_paper_yoy_2025_vs_2024_pct",
         "value": yoy_paper,
         "numerator": sz_series[2025]["paper"] - sz_series[2024]["paper"],
         "denominator": sz_series[2024]["paper"],
         "note": "分子=深圳 2025 论文量-2024 论文量，分母=2024 论文量；同源 jiuxin ads_geo_yearly_metrics 深圳行。"},
    ],
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "「技术发展指数」UI 是科技发展规划页 indicatorData 首卡单值 92.5 分 + yoy 8.3%（演示值，不参与支持度结论）；前端 :64 自带公式『40% 文献活跃度+30% 专利活跃度+20% 产业事件+10% 政策/资本信号』，该公式是需求侧最接近定义的文本。",
        "久新 ads_geo_yearly_index 是『公式批准前保持空表』的预留结构（实测 COUNT=0）——指数结果面结构就绪但零数据，这是本件与 019（无结构）不同的缺口形态。",
        "口径 A 读数（深圳 2025，UI 公式权重 + min-max 归一）：%s；四槽映射假设：产业事件→项目数代理、政策/资本→机构数代理（库内无深圳政策/资本年度列），映射须甲方裁定。" % index_2025,
        "口径 B yoy：深圳论文量 2025 vs 2024 同比 %s%%（对齐 UI yoy 语义；与 mock 8.3 的接近与否不构成数据证据）。" % yoy_paper,
        "2026 年是 PARTIAL_YEAR（论文 2,666 仅统计至 metrics_as_of_date），归一窗只用 2015-2025 完整年。",
        "UI mock 92.5 与口径 A 读数的任何数值接近都属构造性巧合，禁止引用为口径对齐证据（B10）。",
    ],
    "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021",
                        "2022", "2023", "2024", "2025"],
    "base_years_missing": [],
    "base_years_note": "geo_yearly_metrics 深圳 2015-2025 十一个完整年 + 2026 部分年（PARTIAL_YEAR 不入归一窗）；指数本身无历史发布版本可引。",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "92.5", "8.3", "0", "24904", "17596", "2666","28560","4179"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_020_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
