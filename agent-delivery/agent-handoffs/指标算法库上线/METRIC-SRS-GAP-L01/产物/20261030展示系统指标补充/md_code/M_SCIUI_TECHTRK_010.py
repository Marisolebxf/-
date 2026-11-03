#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_010 强化产业转化效率 —— 三源探针 + 复现脚本（批 S3-01，Lane 2）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:858
  keyAreaScenarioPlans 方案B { title: '强化产业转化效率', priority: '高', expectedEffect: '+22.9%', resourceGap: '-19.8%' }
  —— 场景方案卡片的预期效果常量（mock 演示值，不参与支持度结论）；同页 :815-821 成果库卡含
     「转化成果 2,860 / +8.9%」分项。指标名本身三份 SRS 未出现（《科技发展规划.md》seq 190
     资源配置优化建议叶有"支持方案模拟和效果预测"功能句）。

三源结论：
  ① 开发库：org_achievement_year（含 financing_cnt/project_cnt 结构）0 行；enterprise_fund_project 0 行 —— 结构在、数据无
  ② gkx：无 transfer/conversion 结果面（唯 dwd_patent_transfer 22,809 行专利转移事件，是转化侧弱代理）
  ③ 久新：ads_technology_application_case 181,735 行（全部 case_type=RESEARCH_PROJECT，
     market_status=NOT_VERIFIED_AS_MARKET_APPLICATION）；ads_technology_bottleneck_assessment 92,544 行
     转化堵点诊断 —— 转化「过程面」在，「效率」（分子分母口径）无现成结果面

复现口径（B10 双口径）：
  口径 A（专利转移转化率）：gkx 近5年专利转移事件 22,809 / dwd_patent 总量 2,939,895（共享快照）
  口径 B（科研项目转化强度）：久新 2023+ 应用案例 24,799 / 全部应用案例 181,735
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


# ---------------------------------------------------------------- gkx（口径 A 弱代理）
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_patent_transfer")
facts["gkx_patent_transfer_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT SUBSTRING(transfer_effective_date,1,4) y, COUNT(*) c FROM gkx.dwd_patent_transfer "
           "WHERE transfer_effective_date IS NOT NULL AND transfer_effective_date != '' "
           "GROUP BY y ORDER BY y DESC LIMIT 10")
facts["gkx_patent_transfer_by_year"] = {str(y): int(c) for y, c in gc.fetchall()}
gc.execute("SELECT COUNT(*) FROM gkx.dwd_patent_transfer WHERE transfer_effective_date IN ('', '0') OR transfer_effective_date IS NULL OR SUBSTRING(transfer_effective_date,1,4) NOT REGEXP '^[12][0-9]{3}$'")
facts["gkx_patent_transfer_invalid_year_rows"] = int(gc.fetchone()[0])
rows = probe("gkx transfer/conversion 结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%transfer%' OR table_name LIKE '%convers%' OR table_name LIKE '%transformat%')", gc)
facts["gkx_transfer_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 久新（口径 B 主承载）
jx = pymysql.connect(**JX)
jc = jx.cursor()
jc.execute("SELECT COUNT(*), COUNT(DISTINCT technology_node_id) FROM ads_technology_application_case")
r = jc.fetchone()
facts["jiuxin_application_case_rows"] = int(r[0])
facts["jiuxin_application_case_nodes"] = int(r[1])
jc.execute("SELECT case_type, COUNT(*) FROM ads_technology_application_case GROUP BY case_type")
facts["jiuxin_case_type_dist"] = {str(a): int(b) for a, b in jc.fetchall()}
jc.execute("SELECT market_status, COUNT(*) FROM ads_technology_application_case GROUP BY market_status")
facts["jiuxin_market_status_dist"] = {str(a): int(b) for a, b in jc.fetchall()}
jc.execute("SELECT application_stage, COUNT(*) FROM ads_technology_application_case GROUP BY application_stage")
facts["jiuxin_application_stage_dist"] = {str(a) if a is not None else "(空)": int(b) for a, b in jc.fetchall()}
jc.execute("SELECT COUNT(*) FROM ads_technology_application_case WHERE effective_start_year >= 2023")
facts["jiuxin_case_rows_2023plus"] = int(jc.fetchone()[0])
jc.execute("SELECT COUNT(*), COUNT(DISTINCT technology_node_id) FROM ads_technology_bottleneck_assessment")
r = jc.fetchone()
facts["jiuxin_bottleneck_assessment_rows"] = int(r[0])
facts["jiuxin_bottleneck_nodes"] = int(r[1])
jc.execute("SELECT bottleneck_code, COUNT(*) FROM ads_technology_bottleneck_assessment GROUP BY bottleneck_code ORDER BY 2 DESC")
facts["jiuxin_bottleneck_code_dist"] = {str(a): int(b) for a, b in jc.fetchall()}
jc.close(); jx.close()

# ---------------------------------------------------------------- 开发库（absence）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev org_achievement_year 行数（成果年度表，含 project_cnt/financing_cnt）", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.org_achievement_year", dc)
    facts["dev_org_achievement_year_rows"] = int(rows[0][0]) if rows else None
    rows = probe("dev enterprise_fund_project 行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_fund_project", dc)
    facts["dev_enterprise_fund_project_rows"] = int(rows[0][0]) if rows else None
    dc.close(); dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_010_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 派生（B3 同基相除）
# 口径 A：近5年（2021-2026 有效年）专利转移事件 / 专利总量（共享快照 2,939,895）
valid_years = {y: c for y, c in facts["gkx_patent_transfer_by_year"].items()
               if y.startswith(("20", "21")) and y.isdigit() and 2000 < int(y) <= 2026}
transfers_5y = sum(c for y, c in valid_years.items() if int(y) >= 2021)
facts["gkx_patent_transfer_rows_2021plus"] = transfers_5y
PATENT_TOTAL_SNAPSHOT = 2939895  # 共享快照 _shared_probe_s3_01_out.json: dims.gkx[2].data[0][0]

# 口径 B：2023+ 案例 / 全案例
cases_total = facts["jiuxin_application_case_rows"]
cases_2023 = facts["jiuxin_case_rows_2023plus"]

out = {
    "metric_id": "M_SCIUI_TECHTRK_010",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:858",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:815",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:818",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「强化产业转化效率」指标名三份说明书未出现；《科技发展规划.md》seq 190 资源配置优化建议叶有「支持方案模拟和效果预测」功能句（附录 A 摘录），UI 的 expectedEffect +22.9% 是方案卡预期效果常量非效率公式",
    },
    "facts": facts,
    "derived": {
        "gkx_patent_transfer_rate_2021plus": {
            "value": round(transfers_5y / PATENT_TOTAL_SNAPSHOT * 100, 4),
            "numerator": transfers_5y,
            "denominator": PATENT_TOTAL_SNAPSHOT,
            "note": "分子=gkx.dwd_patent_transfer 2021+ 生效年事件数（全表精确 COUNT），分母=gkx.dwd_patent 总量（共享快照 _shared_probe_s3_01_out.json，同库同源）；比值为百分数",
        },
        "jiuxin_case_recency_ratio": {
            "value": round(cases_2023 / cases_total * 100, 4),
            "numerator": cases_2023,
            "denominator": cases_total,
            "note": "分子=久新 application_case effective_start_year>=2023 行数，分母=同表全行；同表同源",
        },
    },
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "部分支持",
    "notes": [
        "UI 的 +22.9%/-19.8% 是方案卡 mock 常量（演示值，不参与支持度结论），不是效率定义",
        "「转化效率」权威口径（成果转化率=转化成果数/成果总数，教育部/科技部口径）所需分子（已转化成果）在三源均无权威承载：久新案例仅证明科研项目关联（market_status 全表 NOT_VERIFIED_AS_MARKET_APPLICATION）",
        "gkx 专利转移口径 A 是权利人变更事件代理，包含转让/赠与/继承等非产业化转移，会高估转化；口径 B 是项目时序新鲜度，非效率语义——两口径均需甲方裁定",
        "久新 bottleneck_assessment 全部为证据缺口诊断（PROJECT_EVIDENCE_GAP 38,860 / MARKET_DATA_UNAVAILABLE 38,860 / ENTERPRISE_PARTICIPATION_GAP 14,824），非堵点因果结论",
        "共享快照复用：dwd_patent 总量 2,939,895（snapshot 键 dims.gkx[2]）；dwd_patent_transfer 为本件新增探针",
    ],
    "base_years_used": ["2021", "2022", "2023", "2024", "2025", "2026"],
    "base_years_missing": [],
    "base_years_note": "口径 A 用 2021-2026 生效年（transfer_effective_date varchar 前四位，287 行 '0' 值已剔除并单列 invalid 计数）；口径 B 用 effective_start_year>=2023",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "22809", "2939895", "181735", "24799", "92544", "13415","19356","25992","2860","29905"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_010_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("口径A 转移率 %:", out["derived"]["gkx_patent_transfer_rate_2021plus"]["value"],
      " 口径B 案例新鲜度 %:", out["derived"]["jiuxin_case_recency_ratio"]["value"])
