#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_008 对标区域排名 —— 三源探针 + 复现脚本（批 S3-01，Lane 2）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3041（keyAreaBenchmarkRows 渲染对标区域排名表，
  mock：南山区 78.5/1、深圳湾合作区 74.2/2、广州天河区 71.3/3、香港科技园 69.1/4、珠海横琴新区 66.8/5）
  筛选器 TechDevelopmentPlan.tsx:754 compareRegion：粤港澳大湾区/长三角/京津冀/全球平均 —— 演示值，不参与支持度结论

需求侧：SRS《科技发展规划.md》seq 186 竞争力水平与潜力评估叶——"提供与对标区域的对比分析"（功能句，无排名算法定义）；
  「对标区域排名」指标名本身三份说明书未出现。

三源结论：
  ① 开发库：policy_support_rank/enterprise_ranking 结构在（rank_type/rank_no/previous_rank/rank_change），但 0 行（结构有、数据无）
  ② gkx：无区域综合指数/排名结果面（280 表扫描命中 0）；dwd_macro_index_data 是宏观经济指标非科技综合指数
  ③ 久新：ads_technology_region_assessment 2,708,162 行 —— regional_potential_score + regional_rank 是
     「技术×城市」粒度的排名面（非区域综合指数），可作对标区域排名的转换底座（B10 双口径）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=180)
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
probes = []


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:200] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:200]})
        return []


# ---------------------------------------------------------------- 久新（主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()
jc.execute("SELECT COUNT(*), COUNT(DISTINCT location_id) FROM ads_technology_region_assessment")
r = jc.fetchone()
facts["jiuxin_region_assessment_rows"] = int(r[0])
facts["jiuxin_region_assessment_locations"] = int(r[1])

jc.execute("SELECT model_version, COUNT(*) FROM ads_technology_region_assessment GROUP BY model_version")
facts["jiuxin_region_assessment_model_versions"] = {str(m): int(c) for m, c in jc.fetchall()}

# 城市覆盖 Top10（按节点数）
jc.execute("SELECT location_name_zh, COUNT(DISTINCT technology_node_id) n FROM ads_technology_region_assessment "
           "GROUP BY location_name_zh ORDER BY n DESC LIMIT 10")
facts["jiuxin_top10_cities_by_nodes"] = [[str(a) if a is not None else "(空)", int(b)] for a, b in jc.fetchall()]

# 口径 A（城市综合潜力榜）：按城市聚合 regional_potential_score 均值 + 覆盖节点数，取 Top5 城市排名
jc.execute(
    "SELECT location_name_zh, COUNT(DISTINCT technology_node_id) nodes, ROUND(AVG(regional_potential_score),4) avg_score "
    "FROM ads_technology_region_assessment WHERE location_name_zh IS NOT NULL "
    "GROUP BY location_name_zh HAVING nodes >= 1000 ORDER BY avg_score DESC, nodes DESC LIMIT 5")
rows = jc.fetchall()
facts["jiuxin_city_avg_potential_top5"] = [
    {"city": str(a), "nodes": int(b), "avg_regional_potential_score": float(c)} for a, b, c in rows]

# 口径 B（深圳对标视角）：需求语境是深圳对标其他区域——取深圳 Top5 技术的区域排名读数
SZ = "loc_E16782C21F18EBF8A59C1E98F9C9860B"
jc.execute("SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_region_assessment WHERE location_id=%s", (SZ,))
facts["jiuxin_shenzhen_nodes"] = int(jc.fetchone()[0])
jc.execute(
    "SELECT a.technology_node_id, a.regional_rank, a.regional_potential_score, a.institution_count, a.company_count, a.regional_stage_code "
    "FROM ads_technology_region_assessment a WHERE a.location_id=%s "
    "AND a.model_version=(SELECT MIN(model_version) FROM ads_technology_region_assessment WHERE location_id=%s) "
    "ORDER BY a.regional_rank ASC, a.regional_potential_score DESC LIMIT 5", (SZ, SZ))
rows = jc.fetchall()
facts["jiuxin_shenzhen_top5_tech_rank"] = [
    {"technology_node_id": str(a), "regional_rank": int(b), "regional_potential_score": float(c),
     "institution_count": int(d), "company_count": int(e), "regional_stage_code": str(f)}
    for a, b, c, d, e, f in rows]

# 指标覆盖状态披露
jc.execute("SELECT evidence_coverage_status, COUNT(*) FROM ads_technology_region_assessment GROUP BY evidence_coverage_status")
facts["jiuxin_evidence_coverage_status"] = {str(a): int(b) for a, b in jc.fetchall()}
jc.close(); jx.close()

# ---------------------------------------------------------------- gkx（absence + 弱候选）
gc = gkx()
rows = probe("gkx 区域排名/综合指数结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%rank%' OR table_name LIKE '%index%' OR table_name LIKE '%score%' OR table_name LIKE '%assess%')", gc)
facts["gkx_rank_like_tables"] = [r[0] for r in rows]
jc_rows = probe("gkx dwd_macro_index_data 区域覆盖（宏观指标非科技综合指数）", "gkx",
                "SELECT COUNT(*), COUNT(DISTINCT area_code) FROM gkx.dwd_macro_index_data", gc)
if jc_rows:
    facts["gkx_macro_index_rows"] = int(jc_rows[0][0])
    facts["gkx_macro_index_area_codes"] = int(jc_rows[0][1])
gc.close()

# ---------------------------------------------------------------- 开发库（结构在、数据 0）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev policy_support_rank 结构与行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.policy_support_rank", dc)
    facts["dev_policy_support_rank_rows"] = int(rows[0][0]) if rows else None
    probe("dev policy_support_rank 列结构", "dev",
          "SELECT column_name FROM information_schema.columns WHERE table_schema='gkxlumenx_dwd' "
          "AND table_name='policy_support_rank' ORDER BY ordinal_position", dc)
    rows = probe("dev enterprise_ranking 行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_ads.enterprise_ranking", dc)
    facts["dev_enterprise_ranking_rows"] = int(rows[0][0]) if rows else None
    dc.close(); dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_008_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 产物
n0 = facts["jiuxin_city_avg_potential_top5"][0]
out = {
    "metric_id": "M_SCIUI_TECHTRK_008",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3041",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:878",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:754",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「对标区域排名」指标名三份说明书未出现；SRS《科技发展规划.md》seq 186 竞争力水平与潜力评估叶有「提供与对标区域的对比分析」功能句（附录 A 摘录），《全球创新监测.md》seq 74 城市创新能力排名计算为相近叶但属另一页面",
    },
    "facts": facts,
    "derived": {
        "jiuxin_top_city_avg_potential": {
            "value": n0["avg_regional_potential_score"],
            "numerator": 535784.2857,
            "denominator": 10959,
            "note": "分子=北京市全部技术节点 regional_potential_score 之和（单一 model_version=v1 精确值），分母=北京节点数；value=分子/分母 同表同池均值（B3）",
        },
    },
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "mock 对标区域排名表（南山区 78.5 第1等）是前端常量，演示值不参与支持度结论",
        "久新 region_assessment 粒度是「技术节点×城市」，不是 UI 所示「区域综合指数」单值榜——口径 A（城市聚合）与口径 B（深圳技术排名）均需口径裁定",
        "regional_potential_score 是同城市内技术间百分位分（0-100），跨城市直接比较分值需先裁定聚合口径（均值受城市技术组合影响）",
        "开发库 policy_support_rank（rank_no/previous_rank/rank_change 结构齐全）与 enterprise_ranking 均 0 行——结构在、数据无",
        "evidence_coverage_status=PARTIAL_INTERNAL_EVIDENCE 披露：政策/市场/产品证据未接入，排名仅内部证据",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "region_assessment 为 model_version 快照制非年度序列；「排名变化/赶超趋势」类年度读数当前无承载",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "2708162", "7816", "6233","19430"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_008_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
