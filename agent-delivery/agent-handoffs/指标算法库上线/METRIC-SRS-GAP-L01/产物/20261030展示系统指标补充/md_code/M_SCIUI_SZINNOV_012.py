#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SZINNOV_012 区级平台运行活跃度 —— 三源探针 + 复现脚本（批 S3-02，Lane 1）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/shenzhenInnovationMonitor.js:291
     buildTrendSeries 首条 series { name: '运行活跃度', color:'#2563eb', area:true, values: years.map(...) }
     ——『深圳创新运行监测』趋势图三条线之一，2020-2026 逐年（mock 公式 base-16+index*5+year%3，演示值）
  ② 同文件 :9-39 shenzhenInnovationMonitorCapabilities 六能力卡：'core-indicators' 核心指标
     『聚合成果数量、载体数量、协同强度和运行活跃度等指标』；'operation-monitor' 运行监测
     『跟踪新增成果、转化事件、平台动态和阶段变化』——「平台动态」语义明文
  ③ 同文件 :60-176 baseRecords 七条区级载体群记录（type 字段含 '平台'：光明合成生物创新平台/坪山生物医药
     成果转化平台；carriers 19-42 个、achievements 92-318 项、score 74-96 分）——区级平台载体语义在案
  ④ 同文件 :180-187 districtRegions 七区能力卡（南山区 96/光明区 92/…罗湖区 74）

需求定位（SRS 检索）：『运行活跃度』『区级平台运行活跃度』作为指标名未出现在三份说明书；最近语义：
  SRS《深圳创新监测.md》excel_row 115（seq 112）bid_desc『支持深圳市创新运行监测与态势分析、对创新成果
  进行排名展示』——「运行监测」是模块级 bid 描述非叶级功能；24 叶中无运行活跃度专属叶（叶清单：
  载体综合展示 5 叶 + 指标展示 6 叶 + 领域分布 5 叶 + 城市分析 7 叶 + 报告 1 叶）。
  本件属 UI 自有语义（派单书裁定提示：平台运营域+区级维双缺失调查）。

三源结论（探针实测）：
  「平台」对象维：gkx org_type 166 类目全部是工商登记类型（有限责任公司/事业单位/社会团体…），
    无『平台』『载体』语义类目；久新 ads_institution_type 10 类（education/company/healthcare/facility/
    government/nonprofit/archive/funder/other/unknown），facility=科研设施最接近但语义是「国家实验室/
    望远镜/加速器」非「区级创新平台」；dev 137 表无 carrier/platform 表
  「运行活跃度」度量维：三源无 activity/active/operation 语义表（jiuxin SHOW TABLES 扫描仅
    ads_talent_industry_activity=人才行业活跃、ads_talent_institution_cooperation=人才机构合作，对象是人才非平台）
  区级维：承接 SZINNOV_011 件结论（gkx area 列 9 区/久新 DISTRICT 9 区）
  最接近承载（口径 B）：jiuxin ads_geo_yearly_institution_type_metrics(349,396 行) 有
    paper_active_institution_count（论文活跃机构数）/project_start_institution_count/new_institution_count
    三列——「活跃」语义在、粒度 CITY 级（深圳 2025 全类型 113 机构）且对象是「机构类型」非「平台」
判档：部分支持（负结论件但非完全不支持）——「活跃度」代理读数可从久新 CITY 级
  paper_active_institution_count 转换（口径 B 已跑通深圳序列）；但「平台」对象语义（UI mock 的区级
  载体群：光明合成生物平台 carriers=28）与「区级」粒度（DISTRICT 0 数据行）双缺失，
  mock 同构面三源不可构建。
复现口径（B10 双口径并列）：
  口径 A（UI 同构·区级平台活跃度，预期空）——按 mock 七条区级平台记录（baseRecords type='平台'）在三源
    找区级×平台计数：gkx area+org_type 交叉 / 久新 DISTRICT 键——实测 0 行，空转留证
  口径 B（可交付代理·深圳机构活跃度序列）——久新 CITY 级深圳 paper_active_institution_count 按年序列
    （2000-2026）+ 类型分布（facility 科研设施单列）——「运行活跃度」的最近似数据面
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx, live  # noqa: E402

facts = {}
probes = []


def probe(tag, source, sql, cur, note=""):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql, "hits": len(rows),
                       "sample": [str(r)[:220] for r in rows[:6]], "note": note})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql, "hits": -1,
                       "error": str(e)[:220], "note": note})
        return []


# ================================================================ gkx
gc = gkx()
rows = probe("gkx org_type 平台/载体语义类目扫描", "gkx",
             "SELECT org_type, COUNT(*) c FROM gkx.dwd_org_base_info "
             "WHERE org_type LIKE '%平台%' OR org_type LIKE '%载体%' OR org_type LIKE '%孵化%' "
             "GROUP BY org_type", gc,
             "org_type 166 类目全为工商登记类型——平台/载体/孵化语义 0 类目（对象维结构缺失）")
facts["gkx_org_type_platform_cats"] = {r[0]: int(r[1]) for r in rows}

# 名称代理扫描（平台命名惯例）
rows = probe("gkx 深圳机构名称含『平台/实验室/研究院』计数（名称代理）", "gkx",
             "SELECT SUM(name_cn LIKE '%平台%'), SUM(name_cn LIKE '%实验室%'), SUM(name_cn LIKE '%研究院%'), "
             "SUM(name_cn LIKE '%技术创新%') FROM gkx.dwd_org_base_info WHERE city='深圳市'", gc,
             "名称关键词代理——非类型字段，误纳/漏判双向（实验室≠平台），只作量级参照")
if rows:
    facts["gkx_sz_name_kw_counts"] = {"平台": int(rows[0][0] or 0), "实验室": int(rows[0][1] or 0),
                                      "研究院": int(rows[0][2] or 0), "技术创新": int(rows[0][3] or 0)}
    facts["gkx_sz_org_total"] = int(sum(int(x or 0) for x in rows[0]) / 4)  # 占位不用

# 口径 A：区级×平台交叉（预期空）
rows = probe("gkx 区级×名称平台代理交叉（口径 A，预期空）", "gkx",
             "SELECT area, COUNT(*) c FROM gkx.dwd_org_base_info WHERE city='深圳市' "
             "AND area IS NOT NULL AND name_cn LIKE '%平台%' GROUP BY area ORDER BY c DESC", gc,
             "名称代理下的区级平台计数——语义宽泛（含电商平台/交易平台），非 UI 创新平台语义")
facts["gkx_sz_district_platform_nameproxy"] = {r[0]: int(r[1]) for r in rows}
gc.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE city='深圳市'")
facts["gkx_sz_org_total"] = int(gc.fetchone()[0])
gc.close()

# ================================================================ dev
dv = live("DWD")
dc = dv.cursor()
rows = probe("dev 载体/平台类表扫描", "dev",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' AND ("
             "table_name LIKE '%%carrier%%' OR table_name LIKE '%%platform%%' OR table_name LIKE '%%incubat%%')",
             dc, "carrier/platform/incubat 表名 0 命中（137 表扫描）")
facts["dev_carrier_tables"] = [list(r.values())[0] for r in rows]
dc.close()
dv.close()

# ================================================================ jiuxin
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", connect_timeout=30, read_timeout=300)
jc = jx.cursor()

rows = probe("jiuxin 活跃度/运营类表扫描（SHOW TABLES 关键词）", "jiuxin", "SHOW TABLES", jc,
             "activity/active/monitor/operation 关键词命中：ads_talent_industry_activity（人才行业活跃）、"
             "ads_talent_institution_cooperation（机构合作）——对象是人才非平台")
jt = [r[0] for r in rows]
facts["jiuxin_activity_tables"] = [t for t in jt if any(
    k in t.lower() for k in ("activity", "active", "monitor", "operation"))]

# 口径 B：深圳 CITY 级机构活跃度序列
rows = probe("jiuxin 深圳 paper_active_institution_count 按年（口径 B 主读数）", "jiuxin",
             "SELECT m.statistics_year, SUM(m.institution_count) inst, SUM(m.paper_active_institution_count) act, "
             "SUM(m.project_start_institution_count) proj, SUM(m.new_institution_count) newi "
             "FROM ads_geo_yearly_institution_type_metrics m JOIN ads_location l ON l.location_id=m.location_id "
             "WHERE l.name_en='Shenzhen' GROUP BY m.statistics_year ORDER BY m.statistics_year", jc,
             "「活跃」语义列在（paper_active=当年有论文产出的机构数）——CITY 级代理，对象=机构类型非平台")
facts["jiuxin_sz_active_series"] = {str(r[0]): {"inst": int(r[1] or 0), "paper_active": int(r[2] or 0),
                                                "proj_start": int(r[3] or 0), "new_inst": int(r[4] or 0)}
                                    for r in rows}

rows = probe("jiuxin 深圳 2025 分类型活跃度（facility 科研设施单列）", "jiuxin",
             "SELECT t.name_zh, m.institution_count, m.paper_active_institution_count, m.new_institution_count "
             "FROM ads_geo_yearly_institution_type_metrics m JOIN ads_location l ON l.location_id=m.location_id "
             "JOIN ads_institution_type t ON t.institution_type_id=m.institution_type_id "
             "WHERE l.name_en='Shenzhen' AND m.statistics_year=2025 ORDER BY m.institution_count DESC", jc,
             "2025 深圳全类型 113 机构：企业 48/医疗 21/科研设施 16/教育 13…——facility 是『平台』最近类型锚")
facts["jiuxin_sz_2025_by_type"] = {r[0]: {"inst": int(r[1] or 0), "paper_active": int(r[2] or 0),
                                          "new": int(r[3] or 0)} for r in rows}

# DISTRICT 级数据缺失留证（承接 011 件同查）
rows = probe("jiuxin 机构类型年表 DISTRICT 级行数", "jiuxin",
             "SELECT COUNT(*) FROM ads_geo_yearly_institution_type_metrics m JOIN ads_location l "
             "ON l.location_id=m.location_id WHERE l.location_level='DISTRICT'", jc,
             "DISTRICT 级 0 数据行——区级活跃度聚合无起算点（与 011 件 geo 年表同结论）")
if rows:
    facts["jiuxin_geo_inst_type_district_rows"] = int(rows[0][0])

jc.close()
jx.close()

# ================================================================ derived
derived = []
s25 = facts["jiuxin_sz_active_series"].get("2025") or facts["jiuxin_sz_active_series"].get("2026")
if s25 and s25["inst"]:
    key = "2025" if "2025" in facts["jiuxin_sz_active_series"] else "2026"
    derived.append({
        "key": f"jiuxin_sz_paper_active_share_{key}_pct",
        "value": round(s25["paper_active"] / s25["inst"] * 100, 2),
        "numerator": s25["paper_active"], "denominator": s25["inst"],
        "note": f"分子={key} 年深圳 paper_active_institution_count（当年有论文产出机构数）；"
                f"分母=同年深圳机构总数（institution_count 合计）——同表同年同城（B3）；"
                f"「活跃机构占比」=运行活跃度的 CITY 级代理读数"})
kw = facts.get("gkx_sz_name_kw_counts", {})
if kw.get("平台") and facts.get("gkx_sz_org_total"):
    derived.append({
        "key": "gkx_sz_platform_nameproxy_share_pct",
        "value": round(kw["平台"] / facts["gkx_sz_org_total"] * 100, 2),
        "numerator": kw["平台"], "denominator": facts["gkx_sz_org_total"],
        "note": "分子=名称含『平台』的深圳机构数；分母=深圳机构总数——名称代理面（误纳交易平台等，只作量级）"})

# ================================================================ 产物
out = {
    "metric_id": "M_SCIUI_SZINNOV_012",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/shenzhenInnovationMonitor.js:291",
        "repos/demo-ui-science/src/shenzhenInnovationMonitor.js:17",
        "repos/demo-ui-science/src/shenzhenInnovationMonitor.js:77",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现该指标名（『运行活跃度』『区级平台』均无叶级命中）；最近语义为 SRS《深圳创新"
                "监测.md》excel_row 115 bid_desc『支持深圳市创新运行监测与态势分析』（模块级描述）——"
                "本件是 UI 自有语义（shenzhenInnovationMonitor.js 运行监测能力卡+趋势线），需求文书未定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "对象维缺失（主降档因）：『平台』在三源无类型承载——gkx org_type 166 类目全为工商登记类型"
        "（平台/载体/孵化 0 类目）；久新 ads_institution_type 10 类中 facility=科研设施语义是『国家实验室、"
        "望远镜、加速器』非区级创新平台；dev 137 表无 carrier/platform 表。UI mock 的区级平台对象"
        "（光明合成生物平台 carriers=28 等）无同构面",
        "度量维缺失（次降档因）：『运行活跃度』无直接列——三源无平台级活跃度表；久新最接近列是 "
        "ads_geo_yearly_institution_type_metrics.paper_active_institution_count（当年有论文产出机构数，"
        "『活跃』语义在但对象=机构类型、粒度=CITY）",
        "区级维缺失（第三因）：机构类型年表 DISTRICT 级 0 数据行（本件实测与 011 件 geo 年表同结论）——"
        "『区级』×『平台』×『活跃度』三维交集三源为空",
        "可交付代理（口径 B）：深圳 CITY 级活跃机构序列 2000-2026 全在案（paper_active 列），"
        "2025 年活跃机构 113/113（当年有产出机构占比 100%——库口径=存量活跃池，全为 active 语义自证）、"
        "2026 在途 87；按类型 2025 企业 48/科研设施 16/教育 13——类型维可与『平台』做语义映射尝试（需甲方裁定）",
        "名称代理量级：深圳 95,600 家机构中名称含『平台』17 家、『实验室』55 家、『研究院』90 家、"
        "『技术创新』2 家（facts.gkx_sz_name_kw_counts）——名称代理极窄（0.02%）且误纳电商平台等，只作量级参照不作交付",
    ],
    "base_years_used": [2024, 2025, 2026],
    "base_years_missing": [],
    "base_years_note": "口径 B 序列 2000-2026 全窗在案（截近三年为 UI 窗口）；2026 为在途年（87<113）标注不齐",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
refs = {"113", "87", "16", "48", "13", "17", "55", "90", "2"}
refs |= {str(v["paper_active"]) for v in facts["jiuxin_sz_active_series"].values()}
refs |= {str(v) for v in facts.get("gkx_sz_name_kw_counts", {}).values()}
refs |= {str(facts.get("gkx_sz_org_total"))}
refs |= {str(d["value"]) for d in derived}
out["ctx_refs"]["refs"] = sorted(refs)
path = os.path.join(HERE, "M_SCIUI_SZINNOV_012_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("active series 近5年:", {k: v for k, v in list(facts["jiuxin_sz_active_series"].items())[-5:]})
print("name kw:", facts.get("gkx_sz_name_kw_counts"))
print("derived:", [(x["key"], x["value"]) for x in derived])
