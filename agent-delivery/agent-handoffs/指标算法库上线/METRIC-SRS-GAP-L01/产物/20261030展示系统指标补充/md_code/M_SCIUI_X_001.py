#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_X_001 产业产值分析（总产值/增加值/利润）—— 三源探针 + 复现脚本（批 S3-02，Lane 1）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3733
     <Panel title="产业产值分析" subtitle="总产值、增加值和利润按时间与企业类型对照。">
     —— industrySub === 'output' 分支；ViewDimensionBar 切企业类型，EChart 渲染 outputOption
  ② 同文件 :2472-2486 outputOption：三条 series（总产值 bar / 增加值 bar / 利润 line），
     x 轴 2019-2025 年，y 轴亿元，mock 值 1200→2010 / 380→662 / 86→136（演示值，不作数据证据）
  ③ tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:830-844
     buildOutputValueOption 同构三 series（scaleSeries 因子缩放）
  ④ :140 产业产值指标卡（score 71，权重 16% —— X_002 件引用）

需求原文（SRS seq 148 / excel_row 151，科技创新评估.md:185-198）：
  「收集并统计特定产业的总产值、增加值、利润等经济指标，用户可按时间范围、地域、企业类型等维度
   查看产业产值情况，系统提供柱状图、折线图等可视化形式展示产值变化趋势。」
  主需求文档 :935-937 同文。→ 真实经济指标语义（派单书 §0.2 明示），非专利/论文代理。

三源结论（探针实测）：
  gkx  dwd_output_value / dwd_high_tech_output / dwd_industry_added_value 三表不存在（表名扫描 0 命中，
       仅 dwd_en_project_output / dwd_zh_project_output = 项目「成果产出」计数，语义甄别排除）；
       主承载 = dwd_macro_index_data(20,000) ⋈ dwd_dim_index_attribute(867)：
       深圳 4403 前缀 28 个经济指标码命中（规上工业增加值 180 行 / GDP 98 行 /
       战略性新兴产业及 20 大产业增加值 53 行，JDZ 绝对值 + TB 同比双口径）
  dev  gkxlumenx_dwd.enterprise_finance_history 90,926 行（8,127 企业 × 2014-2025 年财务史）：
       revenue / total_profit 列在；但绝对值行极少（2025 年 6,908 行中 revenue 仅 34 行），
       行业维 join 缺（enterprise_industry_chain 仅 100 行、industry_distribution 0 行）
  jiuxin 203 表无产值/GDP/营收表（SHOW TABLES 关键词扫描 0 命中）；
       ads_industry(1,971)/ads_institution_industry(1,354,245) 是专利-产业映射，无经济金额列（对照面）

复现口径（B10 双口径并列）：
  口径 A（深圳 20 大产业增加值·2025 报告窗口）——gkx 长表 JDZ 绝对值行，取每产业最近一期累计值（亿元），
       与战略性新兴产业增加值并列；量纲陷阱披露（unit_show 万元 vs unit_use 元 4 个数量级差）
  口径 B（时间趋势对齐）——GDP / 规上工业增加值 / 三次产业增加值年度 JDZ 序列（深圳），
       同键多值/序列倒退等质量硬伤随行披露（GBA 件先验复核）
判档：部分支持——「产业×年份×总产值/增加值/利润」三列齐备的现成面三源皆无：
  gkx 有城市级宏观序列（量纲/同键多值硬伤）+ 产业级增加值散点（非逐年）；
  dev 有企业级利润/营收但绝对值覆盖 <1% 且无产业维 join；久新无经济面。
  UI mock 2019-2025 七年逐年三序列的可回填度：gkx 深圳仅散点、dev 近年为空——时间×产业双维不齐。
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


def f0(x):
    return float(x) if x is not None else None


# ================================================================ gkx 主承载
gc = gkx()

# 表名级负结论（三表不存在断言本批留证）
rows = probe("gkx 产值/经济类表名扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND ("
             "table_name LIKE '%output%' OR table_name LIKE '%value%' OR table_name LIKE '%economic%' OR "
             "table_name LIKE '%gdp%' OR table_name LIKE '%profit%' OR table_name LIKE '%macro%')", gc,
             "dwd_output_value/dwd_high_tech_output/dwd_industry_added_value 0 命中（GBA 近亲断言复核）；"
             "dwd_*_project_output 为项目成果计数非经济产值")
facts["gkx_econ_table_scan"] = [r[0] for r in rows]

# zh/en_project_output 语义甄别（防误用）
rows = probe("gkx dwd_zh_project_output 语义甄别", "gkx",
             "SELECT COUNT(*) FROM gkx.dwd_zh_project_output", gc, "20,133 行=课题成果计数（论文/专利/获奖数），非经济产值")
facts["gkx_zh_project_output_rows"] = int(rows[0][0]) if rows else None

# 深圳经济指标码总命中
rows = probe("gkx 深圳 4403 经济指标码命中（GDP/增加值/产值/营收）", "gkx",
             "SELECT d.index_code, d.index_name, COUNT(*) rows_ FROM gkx.dwd_macro_index_data m "
             "JOIN gkx.dwd_dim_index_attribute d ON d.index_code=m.index_code "
             "WHERE m.area_code LIKE '4403%%' AND (d.index_name LIKE '%%产值%%' OR d.index_name LIKE '%%增加值%%' "
             "OR d.index_name LIKE '%%生产总值%%' OR d.index_name LIKE '%%营业收入%%') "
             "GROUP BY d.index_code, d.index_name ORDER BY rows_ DESC LIMIT 40", gc,
             "28 码命中；产值=0 码（利润类全库 0 码）")
facts["gkx_sz_econ_index_codes"] = [{"code": r[0], "name": r[1], "rows": int(r[2])} for r in rows]
facts["gkx_sz_econ_index_code_count"] = len(facts["gkx_sz_econ_index_codes"])

# 利润类全库负结论
rows = probe("gkx 指标字典利润类命中", "gkx",
             "SELECT index_code, index_name FROM gkx.dwd_dim_index_attribute WHERE index_name LIKE '%%利润%%'", gc,
             "利润口径 gkx 全库 0 码（X_001 三分项之一的结构级缺失）")
facts["gkx_profit_index_codes"] = [r[0] for r in rows]

# —— 口径 A：深圳 20 大产业增加值（JDZ 绝对值行）
SZ_IND = {
    "ftts_tzjz_09": "战略性新兴产业增加值",
    "a71336": "生物医药与健康产业增加值", "a71337": "网络与通信产业增加值",
    "a71338": "半导体与集成电路产业增加值", "a71339": "超高清视频显示产业增加值",
    "a71340": "智能终端产业增加值", "a71341": "智能传感器产业增加值",
    "a71342": "软件与信息服务产业增加值", "a71343": "数字创意产业增加值",
    "a71344": "现代时尚产业增加值", "a71349": "新能源产业增加值",
    "a71350": "安全节能环保产业增加值", "a71351": "智能网联汽车产业增加值",
    "a71352": "高端医疗器械产业增加值", "a71353": "生物医药产业增加值",
    "a71354": "大健康产业增加值", "a76246": "人工智能产业增加值",
    "a76247": "高端装备与仪器产业增加值", "a76248": "低空经济与空天产业增加值",
    "ftts_tzjz_09_06": "新材料产业增加值", "ftts_tzjz_09_09": "高端装备制造产业增加值",
    "ftts_tzjz_09_10": "绿色低碳产业增加值", "ftts_tzjz_09_11": "海洋经济产业增加值",
}
codes_sql = ",".join("'%s'" % k for k in SZ_IND)
gc.execute(
    f"SELECT index_code, occur_period, index_value, unit_use FROM gkx.dwd_macro_index_data "
    f"WHERE area_code LIKE '4403%%' AND index_code IN ({codes_sql}) AND dim_cal='JDZ' "
    f"ORDER BY index_code, occur_period DESC")
ind_abs = {}
for code, per, val, unit in gc.fetchall():
    if val is None:
        continue
    name = SZ_IND[code]
    rec = ind_abs.setdefault(name, {"rows_jdz": 0, "latest_period": None, "latest_yi": None, "periods": []})
    rec["rows_jdz"] += 1
    rec["periods"].append(int(per))
    if rec["latest_period"] is None or int(per) > rec["latest_period"]:
        rec["latest_period"] = int(per)
        rec["latest_yi"] = round(float(val) / 1e8, 2)  # 元 → 亿元
        rec["latest_unit_use"] = str(unit)
# 量纲陷阱登记：字典 unit_show vs 数据行 unit_use（GBA 件 §3.5 先验）
rows = probe("gkx 产业增加值指标字典量纲", "gkx",
             "SELECT index_code, index_name, unit_show FROM gkx.dwd_dim_index_attribute "
             f"WHERE index_code IN ({codes_sql}) LIMIT 25", gc,
             "unit_show=万元 vs 数据行 unit_use=元 → 同指标两处量纲差 4 个数量级（B9 陷阱）")
facts["gkx_sz_industry_added_value"] = {
    k: {kk: vv for kk, vv in v.items() if kk != "periods"} | {"period_span": (min(v["periods"]), max(v["periods"])) if v["periods"] else None}
    for k, v in sorted(ind_abs.items(), key=lambda kv: -(kv[1]["latest_yi"] or 0))}
facts["gkx_sz_industry_av_industry_count"] = len(ind_abs)
facts["gkx_sz_industry_av_jdz_rows"] = sum(v["rows_jdz"] for v in ind_abs.values())

# —— 口径 B：深圳 GDP / 规上工业增加值 / 三次产业 年度 JDZ 序列
for key, code in (("gdp", "gmjj_jjzl_01"), ("ind_above_scale", "gmjj_jjzl_01_02_01_01"),
                  ("prim", "gmjj_jjzl_01_01"), ("sec", "gmjj_jjzl_01_02"), ("ter", "gmjj_jjzl_01_03")):
    gc.execute(
        f"SELECT occur_period, index_value FROM gkx.dwd_macro_index_data "
        f"WHERE index_code='{code}' AND area_code LIKE '4403%%' AND dim_cal='JDZ' AND MOD(occur_period,100)=12 "
        f"ORDER BY occur_period")
    series = {}
    for per, val in gc.fetchall():
        y = int(per) // 100
        series.setdefault(y, []).append(round(float(val) / 1e8, 2))
    facts[f"gkx_sz_{key}_yearly_jdz_yi"] = dict(sorted(series.items()))

# GDP 同键多值与倒退复核（GBA 件先验的深圳面零漂移对账）
gdp = facts["gkx_sz_gdp_yearly_jdz_yi"]
facts["gkx_sz_gdp_multi_value_years"] = {str(y): v for y, v in gdp.items() if len(v) > 1}
facts["gkx_sz_gdp_value_count"] = sum(len(v) for v in gdp.values())

gc.close()

# ================================================================ dev 副承载
dv = live("DWD")
dc = dv.cursor()

rows = probe("dev 企业财务史按年覆盖", "dev",
             "SELECT data_year, COUNT(*) n, SUM(revenue IS NOT NULL) rev_n, SUM(total_profit IS NOT NULL) prof_n "
             "FROM enterprise_finance_history GROUP BY data_year ORDER BY CAST(data_year AS DECIMAL(10,1)) DESC LIMIT 12",
             dc, "90,926 行 × 2014-2025；绝对值行极少（2025 年 rev 34/6,908）")
facts["dev_fin_history_yearly"] = [
    {"year": str(r["data_year"]), "rows": int(r["n"]), "rev_nonnull": int(r["rev_n"] or 0),
     "profit_nonnull": int(r["prof_n"] or 0)} for r in rows]
dc.execute("SELECT COUNT(*), COUNT(DISTINCT org_id) FROM enterprise_finance_history")
n, n_org = gc_vals = [int(x) for x in dc.fetchone().values()]
facts["dev_fin_history_rows"] = n
facts["dev_fin_history_orgs"] = n_org

rows = probe("dev 产业维承载（join 前提）", "dev",
             "SELECT (SELECT COUNT(*) FROM enterprise_industry_chain), "
             "(SELECT COUNT(*) FROM enterprise_industry_distribution), "
             "(SELECT COUNT(*) FROM enterprise_industry_summary)", dc,
             "产业链映射仅 100 行 / 分布表 0 行 / 汇总表 0 行——企业×产业 join 面不足 1%")
if rows:
    vals = [int(x) for x in rows[0].values()]
    facts["dev_industry_join_tables"] = {"chain": vals[0], "distribution": vals[1], "summary": vals[2]}

rows = probe("dev 营收/利润量纲样本", "dev",
             "SELECT org_id, data_year, revenue, total_profit FROM enterprise_finance_history "
             "WHERE revenue IS NOT NULL ORDER BY CAST(data_year AS DECIMAL(10,1)) DESC, revenue DESC LIMIT 6",
             dc, "量纲疑似万元（revenue 175,984 → 17.6 亿），无字段注释佐证")
facts["dev_revenue_sample"] = [
    {"org": str(r["org_id"])[:8], "year": str(r["data_year"]), "revenue": f0(r["revenue"]),
     "profit": f0(r["total_profit"])} for r in rows]

# 产值语义列表名级负结论
rows = probe("dev 产值/增加值/GDP 表名扫描", "dev",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkxlumenx_dwd' AND ("
             "table_name LIKE '%%output%%' OR table_name LIKE '%%gdp%%' OR table_name LIKE '%%added%%' "
             "OR table_name LIKE '%%value%%')", dc,
             "output/gdp/added/value 表名 0 命中（仅 finance_history 三表）")
facts["dev_output_gdp_tables"] = [list(r.values())[0] for r in rows]

dc.close()
dv.close()

# ================================================================ jiuxin 对照面
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", connect_timeout=30, read_timeout=300)
jc = jx.cursor()
rows = probe("jiuxin 203 表产值/GDP/营收/利润表扫描（SHOW TABLES 关键词）", "jiuxin",
             "SHOW TABLES", jc,
             "output/gdp/economic/finance/revenue/profit 关键词 0 命中（Doris 无 information_schema 权限，用 SHOW TABLES 扫）")
jt = [r[0] for r in rows]
econ_kw = ("output", "gdp", "economic", "finance", "revenue", "profit", "added")
facts["jiuxin_econ_tables"] = [t for t in jt if any(k in t.lower() for k in econ_kw)]
# 产业维对照面（专利-产业映射，非经济面）
jc.execute("SELECT COUNT(*) FROM ads_industry")
facts["jiuxin_ads_industry_rows"] = int(jc.fetchone()[0])
jc.execute("SELECT COUNT(*) FROM ads_institution_industry")
facts["jiuxin_ads_institution_industry_rows"] = int(jc.fetchone()[0])
probes.append({"probe": "jiuxin ads_industry / ads_institution_industry 行数（对照面登记）",
               "source": "jiuxin",
               "sql": "SELECT COUNT(*) FROM ads_industry; SELECT COUNT(*) FROM ads_institution_industry",
               "hits": 2,
               "note": "1,971 行产业分类 + 1,354,245 行机构×产业专利计数——专利映射维，无经济金额列，仅作对照面不作主口径"})
jc.close()
jx.close()

# ================================================================ derived
gdp_2021 = facts["gkx_sz_gdp_yearly_jdz_yi"].get("2021", [])
derived = []
# D1: 战新产业增加值占 GDP 比（深圳 2021，JDZ 年度对齐；分子分母同表同源 B3）
zhanxin_2021 = next((v["latest_yi"] for k, v in facts["gkx_sz_industry_added_value"].items()
                     if k == "战略性新兴产业增加值" and v["latest_period"] // 100 == 2021), None)
if gdp_2021 and zhanxin_2021:
    gdp_max_2021 = max(gdp_2021)
    derived.append({
        "key": "gkx_sz_zhanxin_share_of_gdp_2021_pct",
        "value": round(zhanxin_2021 / gdp_max_2021 * 100, 2),
        "numerator": zhanxin_2021, "denominator": gdp_max_2021,
        "note": "分子=深圳2021战新产业增加值(JDZ,亿元,码ftts_tzjz_09)；分母=深圳2021 GDP JDZ 最大值(30,664.85亿,"
                "同键4值取最大——2021有4条:76,048,720,000/887,367,000,000/7,091,000,000/3,066,485,000,000 元)；"
                "两值同表 gkx.dwd_macro_index_data 同为 JDZ 年度口径（B3 同基）；比值仅作量级参照非对外口径"})
# D1: 分子分母同城同年对齐点数（深圳 GDP × 产业增加值，JDZ 年度口径，GBA 件方法在深圳产业面的复用）
av_years = set()
for v in facts["gkx_sz_industry_added_value"].values():
    if v["latest_period"] is not None and v["latest_period"] % 100 == 12:
        av_years.add(v["latest_period"] // 100)
gdp_years = {y for y, vals in facts["gkx_sz_gdp_yearly_jdz_yi"].items() if vals}
aligned = sorted(av_years & gdp_years)
derived.append({
    "key": "gkx_sz_industry_gdp_aligned_year_count",
    "value": float(len(aligned)),
    "numerator": len(aligned),
    "denominator": 1,
    "note": "分子=产业增加值 JDZ 年度值与 GDP JDZ 年度值同年对齐的年份数(" + ",".join(map(str, aligned)) +
            ")；分母=1（计数型派生）；产业增加值年度行仅 2021/2022/2024 落年，GDP 年度 17 值 13 年——"
            "产业×GDP 双口径逐年对齐面=3 年（B10 判档依据：远够不上 UI 2019-2025 七年双序列）"})
# D2: dev 财务史绝对值覆盖率（2025 年）
y25 = next((r for r in facts["dev_fin_history_yearly"] if r["year"].startswith("2025")), None)
if y25:
    derived.append({
        "key": "dev_fin_2025_revenue_coverage_pct",
        "value": round(y25["rev_nonnull"] / y25["rows"] * 100, 2),
        "numerator": y25["rev_nonnull"], "denominator": y25["rows"],
        "note": "分子=2025年revenue非空行，分母=2025年财务史全行（dev gkxlumenx_dwd.enterprise_finance_history，同表同年 B3）"})

# ================================================================ 产物
out = {
    "metric_id": "M_SCIUI_X_001",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:3733",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation/TechInnovationEvaluationPage.tsx:2472",
        "repos/demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx:830",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《科技创新评估.md》seq 148 / excel_row 151『产业产值分析』：『收集并统计特定产业的总产值、增加值、"
                "利润等经济指标，用户可按时间范围、地域、企业类型等维度查看产业产值情况…』；主需求文档 :935-937 同文（1.1.1.1.4.1.7.3.3）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "降档主因：UI mock 是『产业×2019-2025逐年×总产值/增加值/利润』三序列面，三源无一承载——gkx 深圳侧 "
        "28 个经济码中『产值』『利润』两类 0 码（利润全库 0 码），『增加值』有 22 个产业码但 JDZ 绝对值行"
        "散点化（17 个产业有值共 24 行、period 跨 2014-2025 且多为季度/半年累计非年末）；dev 企业财务史有 "
        "revenue/total_profit 列但绝对值行覆盖率 <1%（2025 年 34/6,908）且产业维 join 表仅 100 行；久新 203 表无经济金额表",
        "gkx 主承载读数（口径 A）：深圳 17 个产业有 JDZ 绝对值行（24 行，period 跨 2014-2025）——"
        "Top：网络与通信 2,046.53 亿@2021 年末、超高清视频显示 826.69 亿@2025Q3、新能源 753.89 亿@2023Q3、"
        "海洋经济 574.64 亿@2023Q3、高端装备制造 529.38 亿@2024Q3——『按产业看增加值』单点可行；"
        "但产业级报告期多为季度/半年累计（202409/202509/202503/202206 等，occur_period≠年末），年度值只有 2021/2022/2024 零星",
        "B9 量纲陷阱在案：指标字典 unit_show=万元 vs 数据行 unit_use=元，同指标两处差 4 个数量级（GBA 件 §3.5 先验，本批复核）；"
        "occur_period 为累计期（202109=前三季度累计），年度值须 dim_cal='JDZ' 且 occur_period%100=12 双滤",
        "深圳 GDP 序列质量硬伤复核（GBA 件先验零漂移）：2021 年同键 4 值（76,048,720,000 至 3,066,485,000,000 元，"
        "相差 40 倍）、2008→2009 倒退 70.07%——城市级 GDP 序列不可直接对外",
        "dev enterprise_finance_history 是唯一『企业类型』维度候选（90,926 行×8,127 企业×2014-2025），"
        "但 revenue 绝对值近年塌缩（2015 年 471 行 → 2025 年 34 行）+ 无产业 join 面 → 只能作『企业级利润/营收』零星读数",
        "久新 ads_industry(1,971)/ads_institution_industry(1,354,245) 为专利-产业映射（对照面），"
        "无经济金额列——派单书『专利/论文只能作对照面』纪律落实",
    ],
    "base_years_used": [2021, 2023, 2024, 2025],
    "base_years_missing": [2019, 2020, 2022],
    "base_years_note": "口径 A 取各产业最近期 JDZ 报告期（2014-2025 散布，众数在 2021/2023-2025）；"
                       "UI mock 窗口 2019-2025 中 2019/2020/2022 无任何产业 JDZ 年度行",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
path = os.path.join(HERE, "M_SCIUI_X_001_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    # ctx_refs 回填（数字来自 facts，B1）
refs = set()
for v in facts["gkx_sz_industry_added_value"].values():
    if v.get("latest_yi") is not None:
        refs.add(str(v["latest_yi"]))
for d in derived:
    refs.add(str(d["value"]))
out["ctx_refs"]["refs"] = sorted(refs)
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("产业增加值码数:", facts["gkx_sz_industry_av_industry_count"], "JDZ 行:", facts["gkx_sz_industry_av_jdz_rows"])
print("Top3:", list(facts["gkx_sz_industry_added_value"].items())[:3])
