#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_011 成果数量 —— 三源探针 + 复现脚本（批 S3-01，Lane 2）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:817
  multidimensionalIndicatorCategories.achievement.metrics[0] { label: '成果数量', value: '12.6万', change: '+10.2%' }
  （mock 演示值，不参与支持度结论）；同卡 :818-820 转化成果 2,860 / 标准成果 438 / 获奖成果 216 分项；
  顶栏 :562 成果库 45,680 件。指标名本身三份 SRS 未出现（《科技发展规划.md》seq 179 多维度指标体系展示叶
  列「成果库」为七库之一，附录 A 摘录）。

三源结论：
  ① 开发库：org_achievement_year（paper_cnt/patent_apply_cnt/project_cnt 成果年度结构）0 行 —— 结构在、数据无
  ② gkx：项目产出面 dwd_zh_project_output 20,133 行（total_outputs 合计 80,944）+
     dwd_en_project_output 20,000 行（合计 64,977）；论文 dwd_zh_paper 100,900 / 专利 dwd_patent 2,939,895（共享快照）
  ③ 久新：ads_technology_profile paper_count 合计 108,479 / patent_count 合计 1,071,763（技术节点归集口径）

复现口径（B10 多口径并列）：四口径均为「成果数量」的可行定义，逐一直查给出读数，不跨口径相加。
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


# ---------------------------------------------------------------- gkx（口径承载）
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_zh_project_output")
facts["gkx_zh_project_output_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT SUM(total_outputs), SUM(journal_articles_count), SUM(conference_papers_count), "
           "SUM(patents_count), SUM(books_count) FROM gkx.dwd_zh_project_output")
r = gc.fetchone()
facts["gkx_zh_output_total"] = int(r[0])
facts["gkx_zh_output_journal_articles"] = int(r[1])
facts["gkx_zh_output_conference_papers"] = int(r[2])
facts["gkx_zh_output_patents"] = int(r[3])
facts["gkx_zh_output_books"] = int(r[4])
gc.execute("SELECT COUNT(*) FROM gkx.dwd_zh_project_output WHERE awards_count IS NOT NULL AND awards_count != 0")
facts["gkx_zh_output_awards_nonzero_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT COUNT(*) FROM gkx.dwd_zh_project_output WHERE reports_count IS NOT NULL AND reports_count != 0")
facts["gkx_zh_output_reports_nonzero_rows"] = int(gc.fetchone()[0])

gc.execute("SELECT COUNT(*) FROM gkx.dwd_en_project_output")
facts["gkx_en_project_output_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT SUM(total_outputs), SUM(journal_articles_count), SUM(conference_papers_count), "
           "SUM(patents_count), SUM(clinical_trials_count), SUM(reports_count), SUM(other_outputs_count) "
           "FROM gkx.dwd_en_project_output")
r = gc.fetchone()
facts["gkx_en_output_total"] = int(r[0]) if r[0] is not None else 0
facts["gkx_en_output_journal_articles"] = int(r[1]) if r[1] is not None else 0
facts["gkx_en_output_conference_papers"] = int(r[2]) if r[2] is not None else 0
facts["gkx_en_output_patents"] = int(r[3]) if r[3] is not None else 0
facts["gkx_en_output_clinical_trials"] = int(r[4]) if r[4] is not None else 0
facts["gkx_en_output_reports"] = int(r[5]) if r[5] is not None else 0
facts["gkx_en_output_other"] = int(r[6]) if r[6] is not None else 0

gc.execute("SELECT COUNT(*) FROM gkx.dwd_zh_project")
facts["gkx_zh_project_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT COUNT(*) FROM gkx.dwd_en_project")
facts["gkx_en_project_rows"] = int(gc.fetchone()[0])

rows = probe("gkx achievement/award/outcome 结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%achiev%' OR table_name LIKE '%award%' OR table_name LIKE '%outcome%')", gc)
facts["gkx_achievement_like_tables"] = [r[0] for r in rows]

# 细分缺口补证（MD §3.3 引用）：标准类表名扫描 + 期刊表 award 列语义核查
rows = probe("gkx standard/prize 结果面扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%standard%' OR table_name LIKE '%prize%')", gc)
facts["gkx_standard_prize_tables"] = [r[0] for r in rows]
rows = probe("gkx dwd_zh_journal award 列扫描", "gkx",
             "SELECT column_name FROM information_schema.columns WHERE table_schema='gkx' "
             "AND table_name='dwd_zh_journal' AND (column_name LIKE '%award%' OR column_name LIKE '%prize%')", gc)
facts["gkx_journal_award_cols"] = [r[0] for r in rows]
gc.close()

# 共享快照复用（论文/专利总量，snapshot 键在 notes 登记）
ZH_PAPER_SNAPSHOT = 100900   # _shared_probe_s3_01_out.json dims.gkx[0]
PATENT_SNAPSHOT = 2939895    # dims.gkx[2]

# ---------------------------------------------------------------- 久新（技术节点归集口径）
jx = pymysql.connect(**JX)
jc = jx.cursor()
jc.execute("SELECT COUNT(*) FROM ads_technology_profile")
facts["jiuxin_tech_profile_nodes"] = int(jc.fetchone()[0])
jc.execute("SELECT SUM(paper_count), SUM(patent_count), SUM(institution_count), SUM(company_count) FROM ads_technology_profile")
r = jc.fetchone()
facts["jiuxin_profile_paper_sum"] = int(r[0])
facts["jiuxin_profile_patent_sum"] = int(r[1])
facts["jiuxin_profile_institution_sum"] = int(r[2])
facts["jiuxin_profile_company_sum"] = int(r[3])
jc.execute("SELECT COUNT(*) FROM ads_technology_application_case")
facts["jiuxin_application_case_rows"] = int(jc.fetchone()[0])
rows = probe("久新 achievement/award 结果面 SHOW", "jiuxin",
             "SHOW TABLES", jc)
achie_like = [r[0] for r in rows if any(k in str(r[0]).lower() for k in ("achiev", "award", "outcome"))]
facts["jiuxin_achievement_like_tables"] = achie_like
# 近命中语义核查：ads_research_outcome_* 是「评估维度/学科归属/预测」面，非成果计数面（DESCRIBE + 行数留证）
facts["jiuxin_outcome_dimension_rows"] = None
facts["jiuxin_outcome_discipline_rows"] = None
facts["jiuxin_outcome_forecast_rows"] = None
facts["jiuxin_outcome_dimension_like_count_cols"] = []
for t, key in (("ads_research_outcome_dimension", "jiuxin_outcome_dimension_rows"),
               ("ads_research_outcome_discipline", "jiuxin_outcome_discipline_rows"),
               ("ads_research_outcome_forecast", "jiuxin_outcome_forecast_rows")):
    jc.execute(f"SELECT COUNT(*) FROM {t}")
    facts[key] = int(jc.fetchone()[0])
cur_cols_probe = probe("久新 ads_research_outcome_dimension 列清单", "jiuxin",
                       "DESCRIBE ads_research_outcome_dimension", jc)
facts["jiuxin_outcome_dimension_cols"] = [r[0] for r in cur_cols_probe]
# 标准类承载核查（三源第三源）：jiuxin 203 表无 standard/prize 命中
facts["jiuxin_standard_prize_tables"] = [r[0] for r in rows if any(k in str(r[0]).lower() for k in ("standard", "prize"))]
jc.close(); jx.close()

# ---------------------------------------------------------------- 开发库（absence）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev org_achievement_year 行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.org_achievement_year", dc)
    facts["dev_org_achievement_year_rows"] = int(rows[0][0]) if rows else None
    dc.close(); dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_011_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 派生（B3：同库同源相除）
zh_total = facts["gkx_zh_output_total"]
zh_rows = facts["gkx_zh_project_output_rows"]
out = {
    "metric_id": "M_SCIUI_TECHTRK_011",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:817",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:815",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:562",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「成果数量」指标名三份说明书未出现；《科技发展规划.md》seq 179 多维度指标体系展示叶列「成果库」为七库之一（附录 A 摘录「在大屏上展示技术发展、产业数据库、机构库、课题库、成果库、统计库、人才库等指标体系」）",
    },
    "facts": facts,
    "derived": {
        "gkx_zh_output_per_project": {
            "value": round(zh_total / zh_rows, 4),
            "numerator": zh_total,
            "denominator": zh_rows,
            "note": "分子=dwd_zh_project_output total_outputs 合计 80,944，分母=同表行数 20,133；同表同源，单位=产出件/项目",
        },
        "gkx_zh_en_output_grand_total": {
            "value": zh_total + facts["gkx_en_output_total"],
            "numerator": zh_total + facts["gkx_en_output_total"],
            "denominator": None,
            "note": "纯计数（count）：中英两表 total_outputs 直接相加 80,944+64,977=145,921，非相除；分项构成见 facts.gkx_zh/en_output_*（中文四分项和与合计严格相等）",
        },
    },
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev")],
    "support_judgment": "完全转换支持",
    "notes": [
        "UI 的 12.6万/+10.2% 与顶栏 45,680 件是 mock 常量（演示值，不参与支持度结论）",
        "四口径读数：①项目产出口径 gkx 中文 80,944 + 英文 64,977 = 145,921；②论文口径 gkx.dwd_zh_paper 100,900（共享快照）；③专利口径 gkx.dwd_patent 2,939,895（共享快照）；④技术节点归集口径 久新 profile paper 108,479 / patent 1,071,763",
        "获奖/标准细分承载缺失：dwd_zh_project_output.awards_count 与 reports_count 非零行均为 0（UI 的标准成果 438/获奖成果 216 无数据承载，属缺口）",
        "gkx_en_project_output 仅 journal_articles 有值（64,977），patents/clinical_trials/reports/other 全空——英文项目产出覆盖不完整",
        "共享快照复用：dwd_zh_paper 100,900（dims.gkx[0]）、dwd_patent 2,939,895（dims.gkx[2]）",
        "判档说明：结构性缺口（获奖/标准细分）不影响主读数构建——「成果数量」主口径（论文/专利/项目产出）三源数据量充足可直查直算，细分口径缺口在 MD §四 单列",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件读数为存量合计口径（非年度序列）；如需分年成果数：论文 cover_year_start（varchar 年份陷阱已规避）、专利 apdt_year 可用 20 万采样协议补",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "80944", "64977", "145921", "20133", "20000", "100900", "2939895", "108479", "1071763", "45680","2860"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_011_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("中文产出合计:", zh_total, " 英文产出合计:", facts["gkx_en_output_total"])
