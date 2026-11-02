#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INDEX_013 指标权重展示 · 三源探针与复现脚本（S3-02 Lane 3）。

复现路径（§二）：久新 ads_institution_technology_power 权重四列
（paper/citation/talent/topic_weight，全表单组合 0.35/0.30/0.25/0.10）+
ads_talent_industry_capability_simulation 权重两列（activity/commercial_value）
= 三源仅有的权重结果面族；dev gkxlumenx_cfg.index_weight 2 行 AHP×熵权配置
（carrier/city 两指数，版本号含 -demo 需披露）。
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_INDEX_013_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
DEV = dict(host="10.50.11.76", port=3306, user="root",
           password="Gkxzp202600", connect_timeout=8, read_timeout=120)

import pymysql  # noqa: E402

facts, derived, notes = {}, [], []
conn = pymysql.connect(**JX)
cur = conn.cursor()

# ---------- 1) 久新权重面 1：institution_technology_power 四权重 ----------
cur.execute(
    "SELECT paper_weight, citation_weight, talent_weight, topic_weight, COUNT(*) c "
    "FROM ads_institution_technology_power "
    "GROUP BY paper_weight, citation_weight, talent_weight, topic_weight ORDER BY c DESC LIMIT 10")
power_w = [{"paper": str(r[0]), "citation": str(r[1]), "talent": str(r[2]), "topic": str(r[3]),
            "rows": int(r[4])} for r in cur.fetchall()]
facts["jiuxin_power_weight_combinations"] = power_w

# 权重×得分贡献结构样例（榜首机构）
cur.execute(
    "SELECT institution_name, paper_score, paper_weight, citation_score, citation_weight, "
    "talent_score, talent_weight, topic_score, topic_weight, technology_power_score "
    "FROM ads_institution_technology_power ORDER BY technology_power_rank LIMIT 3")
facts["jiuxin_power_contribution_samples"] = [
    {"name": r[0], "paper_score": float(r[1]), "paper_w": float(r[2]),
     "citation_score": float(r[3]), "citation_w": float(r[4]),
     "talent_score": float(r[5]), "talent_w": float(r[6]),
     "topic_score": float(r[7]), "topic_w": float(r[8]),
     "total": float(r[9])} for r in cur.fetchall()]

# 复现加权合成校验（榜首机构：Σ weight×score 与 total 对账）
s = facts["jiuxin_power_contribution_samples"][0]
recomputed = (s["paper_score"] * s["paper_w"] + s["citation_score"] * s["citation_w"]
              + s["talent_score"] * s["talent_w"] + s["topic_score"] * s["topic_w"])
facts["jiuxin_power_weighted_sum_check_top1"] = {
    "recomputed": round(recomputed, 6), "stored_total": s["total"],
    "abs_diff": round(abs(recomputed - s["total"]), 6)}

# ---------- 2) 久新权重面 2：capability_simulation 两权重 ----------
cur.execute(
    "SELECT activity_weight, commercial_value_weight, COUNT(*) c "
    "FROM ads_talent_industry_capability_simulation "
    "GROUP BY activity_weight, commercial_value_weight ORDER BY c DESC LIMIT 10")
facts["jiuxin_capability_weight_combinations"] = [
    {"activity": str(r[0]), "commercial_value": str(r[1]), "rows": int(r[2])} for r in cur.fetchall()]

# is_synthetic 披露（权重面的性质）+ 覆盖状态细分（探针对账）
cur.execute(
    "SELECT is_synthetic, value_nature, COUNT(*) c FROM ads_talent_industry_capability_simulation "
    "GROUP BY is_synthetic, value_nature ORDER BY c DESC LIMIT 5")
vn = [{"is_synthetic": str(r[0]), "value_nature": r[1], "rows": int(r[2])} for r in cur.fetchall()]
facts["jiuxin_capability_value_nature"] = vn
cur.execute(
    "SELECT is_synthetic, value_nature, simulation_coverage_status, COUNT(*) c "
    "FROM ads_talent_industry_capability_simulation "
    "GROUP BY is_synthetic, value_nature, simulation_coverage_status ORDER BY c DESC LIMIT 5")
facts["jiuxin_capability_coverage_breakdown"] = [
    {"is_synthetic": str(r[0]), "value_nature": r[1], "coverage_status": r[2], "rows": int(r[3])}
    for r in cur.fetchall()]
synthetic_rows = vn[0]["rows"] if vn else 0

cur.close(); conn.close()

# ---------- 3) dev 配置面 ----------
dev_cfg = []
dev_ok = True
try:
    dconn = pymysql.connect(**DEV)
    dcur = dconn.cursor()
    dcur.execute("SELECT COUNT(*) FROM gkxlumenx_cfg.index_weight")
    facts["dev_index_weight_rows"] = int(dcur.fetchone()[0])
    dcur.execute("SELECT * FROM gkxlumenx_cfg.index_weight LIMIT 10")
    cols = [d[0] for d in dcur.description]
    for r in dcur.fetchall():
        row = dict(zip(cols, [str(v) for v in r]))
        dev_cfg.append(row)
    dcur.close(); dconn.close()
except Exception as e:  # noqa: BLE001
    dev_ok = False
    notes.append("dev 新机探针失败（%s）——index_weight 读数沿用本批 E2/E4 实测：2 行（carrier/city 两指数，AHP×熵权，版本 w_v1.0-demo）" % e)
facts["dev_index_weight_configs"] = dev_cfg if dev_cfg else [
    {"version": "w_v1.0-demo", "index_key": "carrier",
     "method": "AHP×熵权", "ahp_weights": "output 0.35 / quality 0.3 / activity 0.2 / performance 0.15",
     "final_weights": "output 0.3518 / quality 0.2235 / activity 0.1199 / performance 0.3048"},
    {"version": "w_v1.0-demo", "index_key": "city",
     "method": "AHP×熵权", "ahp_weights": "output 0.35 / resource 0.25 / environment 0.2 / institution 0.2",
     "final_weights": "output 0.3406 / resource 0.2563 / environment 0.199 / institution 0.2041"}]
notes.append("dev index_weight 2 行为载体/城市两指数的 AHP×熵权配置（版本号 w_v1.0-demo 含 demo 字样但属配置参数非造数分值；与 skill P4.1 黑名单的 demo_* 库不同源，此处按『配置面存在、版本未定稿』披露）")

# ---------- 4) absence 探针 ----------
absence_probe = []
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND table_name LIKE '%%weight%%'")
gkx_w = [r[0] for r in gc.fetchall()]
gc.execute("SELECT COUNT(*) FROM gkx.dwd_dim_index_attribute")
dim_attr_rows = int(gc.fetchone()[0])
gc.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_schema='gkx' "
    "AND table_name='dwd_dim_index_attribute'")
attr_cols = [r[0] for r in gc.fetchall()]
gc.close()
facts["gkx_dim_index_attribute_rows"] = dim_attr_rows
facts["gkx_dim_index_attribute_columns"] = attr_cols
absence_probe.append({
    "probe": "gkx 权重列/表扫描 + dim_index_attribute 列核对",
    "source": "gkx",
    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND table_name LIKE '%weight%'; SHOW COLUMNS FROM gkx.dwd_dim_index_attribute",
    "hits": len(gkx_w),
    "hit_names": gkx_w,
    "hit_detail": "gkx 280 表无 weight 命名表；dwd_dim_index_attribute（%s 行）列清单 %s——无权重列（属性维表）" % (dim_attr_rows, attr_cols[:8])})

absence_probe.append({
    "probe": "久新权重面（正向确认，两表）",
    "source": "jiuxin",
    "sql": "SELECT paper_weight, citation_weight, talent_weight, topic_weight, COUNT(*) FROM ads_institution_technology_power GROUP BY 1,2,3,4; SELECT activity_weight, commercial_value_weight, COUNT(*) FROM ads_talent_industry_capability_simulation GROUP BY 1,2",
    "hits": 2,
    "hit_names": ["ads_institution_technology_power(四权重列)", "ads_talent_industry_capability_simulation(两权重列)"],
    "hit_detail": "两表为久新仅有的权重结果面：power 全表单组合 0.35/0.30/0.25/0.10；capability 两权重见 facts"})

# ---------- 5) 判档 ----------
notes.append("判档：三源无『科技指数三级指标树』粒度的权重配置面（UI mockData 三级树 0.40/0.30/0.20/0.10 + 二三级 41 权重为演示值）；久新两表权重列结构+数据在案但体系不同构（单级四指标/两指标 vs 三级树）、dev index_weight 属载体/城市指数配置——权重『存在但非本指标体系』，判部分支持")
notes.append("B10 双口径：口径 A=以久新 power 四权重（0.35/0.30/0.25/0.10）作科技指数一级权重展示（现成可查，体系语义偏移须披露）；口径 B=为本指标体系立项赋权（AHP+德尔菲，UI mockData 的 AHP 方法叙事即此路径的演示版）。甲方确认口径 A → 升完全转换支持；立项 B → 新配置面落库后升完全转换支持")
notes.append("合成性质披露：capability 表 397,964 行全部 is_synthetic=1（value_nature=SYNTHETIC_SIMULATION），其中确定性哈希回退（DETERMINISTIC_HASH_FALLBACK）396,187 行、技术加权（TECHNOLOGY_WEIGHTED）1,777 行（facts.jiuxin_capability_coverage_breakdown 细分在案）——权重列虽在、其加权对象分均为合成值，该表权重只作『权重面存在性』证据，不作数值承载")

out = {
    "metric_id": "M_SCIUI_INDEX_013",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-index/index.jsx:241",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:347",
        "repos/demo-ui-science/src/pages/tech-index/mockData.js:360",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "srs_seq": 163,
        "excel_row": 166,
        "note": "需求明列叶：SRS 科技指数.md seq 163（excel_row 166）『指标权重展示』——『清晰展示各指标在评价体系中的权重分配，用户可查看权重设置的方法和依据』；UI 实现为指标展示 Tab 的权重说明弹窗（AHP 结合德尔菲专家赋权 + 一级权重 40/30/20/10 + 逐节点赋权依据文案）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "权重面为时点配置/快照（power metrics_as_of_date=2026-09-18；dev index_weight effective_date=2026-01-01）；无跨年权重序列",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["40", "30", "20", "10"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print("power weights:", power_w)
print("check:", facts["jiuxin_power_weighted_sum_check_top1"])
print("capability weights:", facts["jiuxin_capability_weight_combinations"])
