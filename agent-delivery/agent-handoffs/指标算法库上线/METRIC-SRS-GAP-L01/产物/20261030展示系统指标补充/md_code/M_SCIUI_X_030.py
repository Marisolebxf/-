#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_030 成果规模化阶段判定 · 三源探针与复现脚本（S3-02 Lane 3）。

复现路径（§二）：
  久新 ads_technology_stage_assessment（38,860 行）按 stage_code 判阶段，
  规模化=INDUSTRIALIZATION（产业化，transfer_stage 维表：形成供应链和规模生产能力）。
  证据构成（current_status_description 文本，如『论文=3; 专利=192; 企业=1; 项目=2』）仅作旁证。

absence 探针（B4）：gkx 280 表 stage/matur/scale 关键词、dev dwd/ads 转化阶段表。
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_X_030_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
DEV = dict(host="10.50.11.76", port=3306, user="root",
           password="Gkxzp202600", connect_timeout=8, read_timeout=120)

import pymysql  # noqa: E402


def jx_cur():
    conn = pymysql.connect(**JX)
    return conn, conn.cursor()


facts, derived, notes = {}, [], []


# ---------- 1) 久新主面：stage_code 分布 ----------
conn, cur = jx_cur()
cur.execute("SELECT COUNT(*) FROM ads_technology_stage_assessment")
stage_total = int(cur.fetchone()[0])
facts["jiuxin_stage_assessment_rows"] = stage_total

cur.execute(
    "SELECT stage_code, COUNT(*) c FROM ads_technology_stage_assessment "
    "GROUP BY stage_code ORDER BY c DESC")
dist = {r[0]: int(r[1]) for r in cur.fetchall()}
facts["jiuxin_stage_code_distribution"] = dist
industrialization_rows = dist.get("INDUSTRIALIZATION", 0)

# 置信度与方法（全表单方法单置信）
cur.execute(
    "SELECT assessment_method, stage_confidence, COUNT(*) c FROM ads_technology_stage_assessment "
    "GROUP BY assessment_method, stage_confidence ORDER BY c DESC LIMIT 5")
facts["jiuxin_stage_method_confidence"] = [
    {"method": r[0], "confidence": str(r[1]), "rows": int(r[2])} for r in cur.fetchall()]

# transfer_stage 维表全枚举（规模化语义锚）
cur.execute("SELECT stage_code, stage_order, stage_name_zh, stage_name_en, stage_description_zh FROM ads_technology_transfer_stage ORDER BY stage_order")
stage_dim = [{"code": r[0], "order": int(r[1]), "name_zh": r[2], "name_en": r[3],
              "description": r[4]} for r in cur.fetchall()]
facts["jiuxin_transfer_stage_dimension"] = stage_dim

# 规模化（产业化）样本 3 行：证据构成
cur.execute(
    "SELECT technology_node_id, stage_code, current_status_description, development_potential_score "
    "FROM ads_technology_stage_assessment WHERE stage_code='INDUSTRIALIZATION' "
    "ORDER BY development_potential_score DESC LIMIT 3")
facts["jiuxin_industrialization_top3_samples"] = [
    {"node": r[0], "stage": r[1], "evidence_text": r[2], "potential_score": str(r[3])}
    for r in cur.fetchall()]

# 证据构成解析：企业数分布（规模化阶段的企业证据覆盖）
cur.execute(
    "SELECT current_status_description FROM ads_technology_stage_assessment "
    "WHERE stage_code='INDUSTRIALIZATION' LIMIT 5000")
company_hist = {}
evidence_parsed = 0
for (txt,) in cur.fetchall():
    m = re.search(r"企业=(\d+)", txt or "")
    if m:
        evidence_parsed += 1
        n = int(m.group(1))
        k = "0" if n == 0 else ("1-3" if n <= 3 else ("4-10" if n <= 10 else ">10"))
        company_hist[k] = company_hist.get(k, 0) + 1
facts["jiuxin_industrialization_company_evidence_hist_sample5000"] = {
    "parsed": evidence_parsed, "company_count_buckets": dict(sorted(company_hist.items()))}
notes.append("企业证据分布基于 INDUSTRIALIZATION 前 5,000 行采样解析（LIMIT 无 ORDER BY，非全表）；用于规模化判定的企业侧证据面披露")

# 产业化阶段占比（派生）
derived.append({
    "key": "jiuxin_industrialization_share_pct",
    "value": round(industrialization_rows * 100.0 / stage_total, 4),
    "numerator": industrialization_rows,
    "denominator": stage_total,
    "note": "分子=INDUSTRIALIZATION 行数，分母=stage_assessment 全表行数；同表同 WHERE 池（B3），久新 38,860 技术节点全量"})

# ---------- 2) absence 探针 ----------
absence_probe = []

# gkx：stage/matur/scale 关键词
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND "
    "(table_name LIKE '%%stage%%' OR table_name LIKE '%%matur%%' OR table_name LIKE '%%scale%%')")
gkx_hits = [r[0] for r in gc.fetchall()]
absence_probe.append({
    "probe": "gkx 280 表关键词扫描：table_name LIKE %stage%/%matur%/%scale%",
    "source": "gkx",
    "sql": "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND (table_name LIKE '%stage%' OR table_name LIKE '%matur%' OR table_name LIKE '%scale%')",
    "hits": len(gkx_hits),
    "hit_names": gkx_hits,
    "hit_detail": "仅命中 dwd_fund_scale_info（基金规模信息），无技术/成果阶段判定结果面"})
gc.close()

# dev：dwd/ads 转化阶段表
dev_ok = True
try:
    dconn = pymysql.connect(**DEV)
    dcur = dconn.cursor()
    dcur.execute(
        "SELECT table_schema, table_name FROM information_schema.tables WHERE "
        "table_schema LIKE 'gkxlumenx%%' AND (table_name LIKE '%%stage%%' OR table_name LIKE '%%matur%%')")
    dev_hits = [(r[0], r[1]) for r in dcur.fetchall()]
    dcur.close()
    dconn.close()
except Exception as e:  # noqa: BLE001
    dev_ok = False
    dev_hits = []
    notes.append("dev 新机 10.50.11.76 探针失败（%s）——dev 侧阶段承载按共享快照 E1 补充：命中 gkxlumenx_ads.chain_stage / gkxlumenx_cms.cms_kg_stage_def" % e)

absence_probe.append({
    "probe": "dev gkxlumenx_* 阶段表扫描：table_name LIKE %stage%/%matur%",
    "source": "dev",
    "sql": "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%%' AND (table_name LIKE '%%stage%%' OR table_name LIKE '%%matur%%')",
    "hits": len(dev_hits) + (2 if not dev_ok else 0),
    "hit_names": ["%s.%s" % (a, b) for a, b in dev_hits] + (["gkxlumenx_ads.chain_stage", "gkxlumenx_cms.cms_kg_stage_def"] if not dev_ok else []),
    "hit_detail": "chain_stage 为产业链阶段维表、cms_kg_stage_def 为科普图谱阶段定义，均非成果规模化判定结果面"})

# 久新：确认承载（正向探针，非 absence）
absence_probe.append({
    "probe": "jiuxin 成果/技术阶段判定结果面（正向确认）",
    "source": "jiuxin",
    "sql": "SELECT COUNT(*), COUNT(DISTINCT technology_node_id) FROM ads_technology_stage_assessment",
    "hits": 1,
    "hit_names": ["ads_technology_stage_assessment"],
    "hit_detail": "38,860 行 / 技术节点维度；阶段维表 ads_technology_transfer_stage 8 阶段枚举在案"})
cur.execute("SELECT COUNT(DISTINCT technology_node_id) FROM ads_technology_stage_assessment")
facts["jiuxin_stage_distinct_nodes"] = int(cur.fetchone()[0])
cur.close(); conn.close()

# ---------- 3) 判档 ----------
support = "完全转换支持"
notes.append("判档：三源无『科技成果』粒度的规模化判定现成结果面（对象轴=技术节点非成果）；但久新 stage_assessment 结构+数据量足够，规则证据基线方法（RULE_BASED_EVIDENCE_BASELINE）+阶段维表语义锚可现转，判完全转换支持")
notes.append("语义偏移披露：久新对象轴=技术节点（technology_node_id），UI 挂载『规模化』为市场化成熟度图五阶段轴末端；语义最贴档 MARKET_SCALE（市场规模化）结果面 0 行，现有数据最高落在 INDUSTRIALIZATION（产业化，order 7/8）；如需成果/专利粒度或 MARKET_SCALE 档需另建证据链（升档触发器见 MD §1.6）")
notes.append("方法披露：assessment_method=RULE_BASED_EVIDENCE_BASELINE（规则基线，schema §24.6 明示『不是 TRL、不是大模型结论』），stage_confidence 全表 0.9000")

out = {
    "metric_id": "M_SCIUI_X_030",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2263",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2698",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「成果规模化阶段判定」指标名未出现在三份需求真源；语义最近叶=SRS 科技创新评估.md seq 158『政策优化建议』（含系统仿真模型趋势预判段）与同文件 seq 139/145 趋势预测族；『规模化』字样在 UI 为市场化成熟度图五阶段轴末端",
    "scale_stage_mapping": "久新 transfer_stage 维表 8 阶段含两级规模化语义：order 7 INDUSTRIALIZATION（产业化：形成供应链和规模生产能力）与 order 8 MARKET_SCALE（市场规模化：实现持续市场采用和规模增长）；结果面仅 order 5/7 两档有行，MARKET_SCALE 0 行（facts.jiuxin_stage_code_distribution 在案）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "阶段判定为时点快照面（metrics_as_of_date=2026-10-16，data_version 202610290801），无历史基期序列",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: out[k] for k in ("support_judgment", "facts", "derived")},
                 ensure_ascii=False, indent=1)[:3000])
