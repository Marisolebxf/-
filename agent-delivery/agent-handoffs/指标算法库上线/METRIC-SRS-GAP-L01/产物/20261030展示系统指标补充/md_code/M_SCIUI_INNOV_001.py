#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_001 区域专利数（对比图维度）—— 三源探针 + 复现脚本（批 S3-01，Lane 5）。

UI 挂载（三处，均实查）：
  ① repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:24
     compareMetricOptions { key: 'patents', label: '专利数' } —— 载体对比维度选择器
  ② repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:962
     企业详情 { label: '专利数', value: `${selectedEnterprise.patents} 件` }
  ③ repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1397
     载体表格列 { title: '专利数', dataIndex: 'patents' }
  mock：mockData.js:81 patents = Math.floor(Math.random()*5000)+500（随机，演示值，不参与支持度结论）

三源：
  ① 开发库：专利 4 表全部空载（enterprise_chain_patent/detail/history=0，org_rel=969 行纯关系）
  ② gkx：dwd_patent 2,939,895 行有 country_code，但 20 万采样 100% CN（受理局=CN 的公开文本库），
     country 文本列采样 Top：China 193,750 / WO 6,175 / Hong Kong 66 —— 无「区域对比」区分度
  ③ 久新：ads_patent_analysis_institution 7,270 行（机构×国别×专利数，ALL 期）
           + ads_patent_analysis_jurisdiction 675 行（受理局×专利数）—— 本件主承载

复现口径（B10 双口径并列）：
  口径 A（载体维·语义同构 UI）：ads_patent_analysis_institution ALL 期 Top10 机构专利数（carrier 语义）
  口径 B（区域维·国别聚合）：按 country_code 聚合机构专利数（region 语义，US 49,165 / CH 29,010 / ...）
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(
    host="47.93.119.170",
    port=29030,
    user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev",
    connect_timeout=30,
    read_timeout=300,
)
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
facts["jiuxin_patent_analysis_institution_rows"] = int(
    jc.execute("SELECT COUNT(*) FROM ads_patent_analysis_institution") or jc.execute(
        "SELECT COUNT(*) FROM ads_patent_analysis_institution"))
jc.execute("SELECT COUNT(*) FROM ads_patent_analysis_institution")
facts["jiuxin_patent_analysis_institution_rows"] = int(jc.fetchone()[0])

# 口径 A：载体 Top10
jc.execute(
    "SELECT institution_name_en, institution_type_id, country_code, patent_count, family_count, institution_rank "
    "FROM ads_patent_analysis_institution WHERE period_key='ALL' AND institution_rank<=10 "
    "GROUP BY institution_name_en, institution_type_id, country_code, patent_count, family_count, institution_rank "
    "ORDER BY institution_rank")
facts["jiuxin_institution_patent_top10"] = [
    {"name": str(n), "type": str(t) if t else "", "country": str(c) if c else "",
     "patents": int(p), "families": int(fm), "rank": int(rk)}
    for n, t, c, p, fm, rk in jc.fetchall()]

# 口径 B：国别聚合
jc.execute(
    "SELECT country_code, COUNT(DISTINCT institution_id) insts, SUM(patent_count) patents "
    "FROM ads_patent_analysis_institution WHERE period_key='ALL' "
    "GROUP BY country_code ORDER BY patents DESC LIMIT 12")
b_rows = jc.fetchall()
facts["jiuxin_country_patent_agg_top12"] = [
    {"country": str(c) if c else "(null)", "institutions": int(i), "patents": int(p)}
    for c, i, p in b_rows]
facts["jiuxin_country_agg_top12_total"] = sum(int(p) for _, _, p in b_rows)
jc.execute("SELECT SUM(patent_count) FROM ads_patent_analysis_institution WHERE period_key='ALL'")
facts["jiuxin_institution_patent_total_all"] = int(jc.fetchone()[0])

# 受理局面（参照系，非国别）
jc.execute(
    "SELECT jurisdiction_code, jurisdiction_name, jurisdiction_type, patent_count, patent_share, jurisdiction_rank "
    "FROM ads_patent_analysis_jurisdiction WHERE period_key='ALL' AND jurisdiction_rank<=8 "
    "GROUP BY jurisdiction_code, jurisdiction_name, jurisdiction_type, patent_count, patent_share, jurisdiction_rank "
    "ORDER BY jurisdiction_rank")
facts["jiuxin_jurisdiction_all_top"] = [
    {"code": str(c), "name": str(n), "type": str(t), "patents": int(p),
     "share": round(float(s), 6), "rank": int(rk)}
    for c, n, t, p, s, rk in jc.fetchall()]

# 覆盖质量：coverage 表 INSTITUTION 行
jc.execute(
    "SELECT data_domain, coverage_status, eligible_patent_count, covered_patent_count, coverage_rate, limitation_note "
    "FROM ads_patent_analysis_coverage WHERE data_domain='INSTITUTION' LIMIT 3")
cov = jc.fetchall()
facts["jiuxin_institution_coverage"] = [
    {"domain": str(r[0]), "status": str(r[1]), "eligible": int(r[2]),
     "covered": int(r[3]), "rate": round(float(r[4]), 6), "note": str(r[5])[:120]}
    for r in cov]
jc.close()
jx.close()

# ---------------------------------------------------------------- gkx（负结论探针）
gc = gkx()
facts["gkx_dwd_patent_rows"] = 2939895  # 共享快照 _shared_probe_s3_01_out.json dims.gkx[2]（B11 零漂移）
rows = probe("gkx dwd_patent 20万采样 country_code 分布", "gkx",
             "SELECT country_code, COUNT(*) c FROM (SELECT country_code FROM gkx.dwd_patent LIMIT 200000) t "
             "WHERE country_code IS NOT NULL AND country_code != '' GROUP BY country_code ORDER BY c DESC LIMIT 12", gc)
facts["gkx_patent_country_code_sample_top"] = [[str(r[0]), int(r[1])] for r in rows]
gc.close()

# ---------------------------------------------------------------- 开发库（负结论探针）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    facts["dev_patent_table_rows"] = {}
    for t in ("enterprise_chain_patent", "enterprise_patent_detail", "enterprise_patent_history",
              "enterprise_patent_org_rel"):
        dc.execute(f"SELECT COUNT(*) FROM gkxlumenx_dwd.{t}")
        facts["dev_patent_table_rows"][t] = int(dc.fetchone()[0])
    dc.close()
    dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_INNOV_001_out.json")
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
out = {
    "metric_id": "M_SCIUI_INNOV_001",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/carrierRankingCompareModel.js:24",
        "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/IncubationCarrierNewPage.jsx:962",
        "repos/demo-ui-science/src/pages/achievement-preview/modules/innovation-ecosystem/components/InnovationEcosystemWorkbench.jsx:1397",
        "repos/demo-ui-science/src/pages/global-innovation/mockData.js:81",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域专利数/专利数」作为指标名未出现在三份说明书；最近语义为全球创新监测.md seq 67「数据指标分类展示」：『将全球创新数据按照关键数据指标进行分类，如专利数量、论文引用率、投资金额』（举例级提及，非定义）；科技创新评估.md seq 140「专利数量统计分析」是另一四级功能非本页",
    },
    "facts": facts,
    "derived": {
        "jiuxin_top12_country_share_pct": {
            "value": round(facts["jiuxin_country_agg_top12_total"] / facts["jiuxin_institution_patent_total_all"] * 100, 4),
            "numerator": facts["jiuxin_country_agg_top12_total"],
            "denominator": facts["jiuxin_institution_patent_total_all"],
            "note": "分子=Top12 国聚合机构专利数，分母=ads_patent_analysis_institution ALL 期全部专利数；同表同口径（B3 同基相除）",
        },
        "jiuxin_top1_institution_share_pct": {
            "value": round(facts["jiuxin_institution_patent_top10"][0]["patents"] / facts["jiuxin_institution_patent_total_all"] * 100, 4),
            "numerator": facts["jiuxin_institution_patent_top10"][0]["patents"],
            "denominator": facts["jiuxin_institution_patent_total_all"],
            "note": "分子=Top1 机构（Roche 5,621），分母同上；载体维集中度",
        },
    },
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "主承载语义是「机构归属国」聚合（机构 patent_count 按 country_code 求和），非 OECD/WIPO 的「发明人居住国」口径（R1/R2）；受让人-机构解析覆盖率仅 1.93%（coverage 表 INSTITUTION 行 covered 33,807/eligible 1,752,444），读数系统性偏小",
        "gkx dwd_patent 虽有 country/country_code 列，但 20 万采样 100% CN（受理局维度），无区域对比区分度——这是「列存在但数据无区分度」的数据级缺失",
        "UI 三个挂载点语义都是「载体（企业/机构）专利数」非「行政区专利数」；口径 B（国别聚合）是区域维最近似口径",
        "ads_institution_patent（100,358 行）是每机构 Top20 代表性专利明细（selection_method=RELATION_GRANT_SCIENCE_CITATION_YEAR），不能直接 COUNT 作机构专利总数（会截断在 20）",
        "开发库专利 4 表：3 表 0 行，org_rel 969 行为纯关系表无专利计数值",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "主承载 patent_analysis_institution 仅 period_key='ALL'（无分年期），年度序列见 M_SCIUI_INNOV_002 件；跨年分析窗 baseline 2020-2022 / recent 2023-2025 为上游表内置口径",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "7270", "5621", "49165", "29010", "17285", "2939895", "100358", "1.93", "33807", "1752444", "969","158700","83745"]},
}
path = os.path.join(HERE, "M_SCIUI_INNOV_001_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("top10[0]:", facts["jiuxin_institution_patent_top10"][0])
print("country top3:", facts["jiuxin_country_patent_agg_top12"][:3])
