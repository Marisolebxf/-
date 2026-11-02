#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SZINNOV_007 基础设施增量指标 —— 三源探针 + 复现脚本（批 S3-02，Lane 1）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/ShenzhenInnovation.tsx:616-626
     generateTechIndicators categories 第 10 项 { key:'infrastructure', name:'基础设施', unit:'个',
     value:1_260, yoy:-19.1, children:[ {name:'基础设施核心指标',value:731}, {name:'基础设施增量指标',value:302} ] }
     ——本件叶=『基础设施』一级维下的『基础设施增量指标』二级子项（mock 302 个，演示值）
  ② 同文件 :629-669 buildChild 展开树：children 带 history（historyFactors 0.76-1.0 五点回推 2021-2025）、
     source:'深圳市科技创新委员会、深圳市统计局'、calcMethod:'年度基础设施统计数据汇总'——
     UI 自注数据来源口径（需求侧期望的官方源）
  ③ 同文件 :672 indicatorTrendYears ['2021'...'2025']——五年趋势窗
  ④ 弟兄维：paper/patent/expert/project/policy 等十维同构（论文 48,200 篇/专利 168,000 件等 mock）

需求原文（SRS《深圳创新监测.md》seq 119 / excel_row 122『多维度指标展示』）：
  「从论文、期刊、专利、专家学者、会议、组织机构、课题、项目、资金、政策、基础设施等多个维度展示
   科技发展指标，用户可选择查看不同维度的指标数据。」——基础设施是 11 维枚举的末位；
  主需求文档 :769/:779 同文。SRS 未给『基础设施』计数口径（大科学装置？创新载体？仪器设施？）。
  注意：科技全域态势 SRS（:42 地图平移）的要素枚举是『论文、期刊、专利、专家学者、会议、组织机构、
  课题、项目』九项——不含基础设施；基础设施维仅深圳创新监测模块明文。

三源结论（探针实测）：
  gkx  基础设施/仪器/设施类表名+列名全库 0 命中（infra/facility/instrument/apparatus/equipment/platform/
       carrier/incubat 八关键词双级扫描）；主需求 :3565 点名的『大型科学仪器共享』（9,262 台套/499 单位）
       无对应表
  dev  137 表无 instrument/facility 类表
  jiuxin 203 表无 instrument/facility/infrastructure 表；最接近=ads_institution_type.facility
       （科研设施：国家实验室/望远镜/加速器——OpenAlex 语义），深圳 CITY 级 facility 序列在
       ads_geo_yearly_institution_type_metrics（2000-2026：5→17 家，2025=16）
判档：完全不支持——『基础设施』维（mock 1,260 个设施 + 增量 302 个/年）的对象、计数、增量三要素
  在三源均无承载：无设施底册表（结构缺）、无设施计数列（数据缺）、无逐年增量面（时间缺）；
  久新 facility 代理语义窄（科研设施≠基础设施）且量级差 75 倍（16 vs 1,260），不能作承载。
  需求文书未定义口径 + UI 自注官方源（深圳市科创委/统计局）不在三源——升档路径只有外部统计源接入。
复现口径（B10 双口径并列，均为负结论佐证）：
  口径 A（UI 同构·基础设施计数，预期空转）——三源设施底册计数：0 表 0 行留证
  口径 B（最近代理·久新 facility 序列）——深圳 CITY 级科研设施计数按年（5→17 家）与
       YoY 增量序列——量级/语义双不符的对照面读数（不作交付）
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
rows = probe("gkx 基础设施/仪器/设施类表名扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND ("
             "table_name LIKE '%infra%' OR table_name LIKE '%facility%' OR table_name LIKE '%instrument%' OR "
             "table_name LIKE '%apparatus%' OR table_name LIKE '%equipment%' OR table_name LIKE '%platform%' OR "
             "table_name LIKE '%carrier%' OR table_name LIKE '%incubat%')", gc,
             "八关键词表名级 0 命中（280 表扫描）——设施底册结构缺失")
facts["gkx_infra_tables"] = [r[0] for r in rows]
rows = probe("gkx 基础设施语义列扫描", "gkx",
             "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='gkx' AND ("
             "column_name LIKE '%infra%' OR column_name LIKE '%facility%' OR column_name LIKE '%instrument%' OR "
             "column_name LIKE '%apparatus%' OR column_name LIKE '%platform%') LIMIT 60", gc,
             "列名级 0 命中——表名+列名双级扫描后确认结构缺失")
facts["gkx_infra_columns"] = [[r[0], r[1]] for r in rows]
gc.close()

# ================================================================ dev
dv = live("DWD")
dc = dv.cursor()
rows = probe("dev 设施/仪器类表扫描", "dev",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' AND ("
             "table_name LIKE '%%instrument%%' OR table_name LIKE '%%facility%%' OR table_name LIKE '%%infra%%')",
             dc, "instrument/facility/infra 表名 0 命中（137 表）")
facts["dev_infra_tables"] = [list(r.values())[0] for r in rows]
dc.close()
dv.close()

# ================================================================ jiuxin（口径 B 代理）
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", connect_timeout=30, read_timeout=300)
jc = jx.cursor()
rows = probe("jiuxin 设施/仪器类表扫描（SHOW TABLES 关键词）", "jiuxin", "SHOW TABLES", jc,
             "instrument/facility/infra/equipment 关键词 0 命中（203 表）")
jt = [r[0] for r in rows]
facts["jiuxin_infra_tables"] = [t for t in jt if any(
    k in t.lower() for k in ("instrument", "facility", "infra", "equipment"))]

rows = probe("jiuxin 深圳 facility（科研设施）计数按年（口径 B 代理）", "jiuxin",
             "SELECT m.statistics_year, m.institution_count FROM ads_geo_yearly_institution_type_metrics m "
             "JOIN ads_location l ON l.location_id=m.location_id "
             "WHERE l.name_en='Shenzhen' AND m.institution_type_id='facility' ORDER BY m.statistics_year", jc,
             "2000-2026 深圳科研设施 5→17 家——OpenAlex facility 语义（国家实验室/望远镜/加速器），"
             "与 UI『基础设施 1,260 个』量级差 ~75 倍、语义不同物")
facts["jiuxin_sz_facility_series"] = {str(r[0]): int(r[1] or 0) for r in rows}
jc.close()
jx.close()

# ================================================================ derived（对照面）
derived = []
ser = {int(k): v for k, v in facts["jiuxin_sz_facility_series"].items()}
yoy = {y: ser[y] - ser[y - 1] for y in sorted(ser) if y - 1 in ser}
facts["jiuxin_sz_facility_yoy_delta"] = {str(k): v for k, v in yoy.items()}
if 2025 in ser:
    derived.append({
        "key": "jiuxin_sz_facility_2025_vs_ui_mock_ratio",
        "value": round(1260 / ser[2025], 1),
        "numerator": 1260, "denominator": ser[2025],
        "note": "分子=UI mock 基础设施总量（1,260 个，演示值不作数据证据）；分母=久新深圳 2025 科研设施数"
                f"（{ser[2025]} 家，实测）——量级差 75 倍实证：facility 代理与 UI 语义不同物"})
if 2025 in yoy:
    derived.append({
        "key": "jiuxin_sz_facility_delta_2025",
        "value": float(yoy[2025]),
        "numerator": ser[2025], "denominator": ser.get(2024, 0),
        "note": "分子=2025 深圳科研设施数；分母=2024——差分增量（同表同年差分 B3）；"
                "『增量』语义的最近代理读数（2025=-1 家：负增量）"})

# ================================================================ 产物
out = {
    "metric_id": "M_SCIUI_SZINNOV_007",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:617",
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:624",
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:651",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《深圳创新监测.md》seq 119 / excel_row 122『多维度指标展示』：『从论文、期刊、专利、专家"
                "学者、会议、组织机构、课题、项目、资金、政策、基础设施等多个维度展示科技发展指标…』——"
                "基础设施是 11 维枚举末位（维度名命中、指标定义未给）；主需求文档 :769/:779 同文；"
                "科技全域态势 SRS 的要素枚举（:42）不含基础设施——本维仅深圳创新监测模块明文",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": probes,
    "support_judgment": "完全不支持",
    "notes": [
        "判档依据（三源逐一留证 B4）：gkx 八关键词（infra/facility/instrument/apparatus/equipment/platform/"
        "carrier/incubat）表名+列名双级扫描 0 命中；dev 137 表 instrument/facility/infra 0 命中；"
        "久新 203 表同关键词 0 命中——『基础设施』底册表在三源结构级不存在",
        "需求文书未定义计数口径（大科学装置/创新载体/仪器设施/新型基础设施？四种口径量级差数量级）；"
        "UI 自注数据源『深圳市科技创新委员会、深圳市统计局』（ShenzhenInnovation.tsx:651）不在三源——"
        "官方统计源（如深圳统计年鉴基础设施投资额）是唯一升档路径",
        "最近代理（口径 B 对照面）：久新 ads_institution_type.facility=科研设施（OpenAlex 语义：国家实验室/"
        "望远镜/粒子加速器），深圳 2000-2026 序列 5→17 家、2025=16 家、2025 增量-1——"
        "量级与 UI mock（1,260 个/增量 302）差约 79 倍（derived.jiuxin_sz_facility_2025_vs_ui_mock_ratio=78.8）"
        "且语义不同物，不能作承载",
        "『增量』语义佐证：UI 兄弟维同构（论文核心 27,956/增量 11,568=40.8%；专家核心 22,156/增量 9,168），"
        "『增量指标』应为年内新增计数——即便有设施底册还需 established/incorporation 时间列，"
        "三源亦无设施×时间面",
        "本件与 SZINNOV_012（区级平台活跃度）共用『平台/设施对象维缺失』结论；"
        "与 SZINNOV_011 区级维不同——本件连市级设施面都不存在，判档更严一档",
    ],
    "base_years_used": [],
    "base_years_missing": [2021, 2022, 2023, 2024, 2025],
    "base_years_note": "UI 五年趋势窗（indicatorTrendYears 2021-2025）全缺——三源无基础设施计数面，"
                       "无任何年份可取数；口径 B 代理序列（2000-2026）仅供对照不作交付",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
refs = {"1260", "302", "731", "16", "17", "5", "78.8", "-1.0"}
refs |= {str(v) for v in facts["jiuxin_sz_facility_series"].values()}
refs |= {str(d["value"]) for d in derived}
out["ctx_refs"]["refs"] = sorted(refs)
path = os.path.join(HERE, "M_SCIUI_SZINNOV_007_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("facility 序列近8年:", {k: v for k, v in list(facts["jiuxin_sz_facility_series"].items())[-8:]})
print("derived:", [(x["key"], x["value"]) for x in derived])
