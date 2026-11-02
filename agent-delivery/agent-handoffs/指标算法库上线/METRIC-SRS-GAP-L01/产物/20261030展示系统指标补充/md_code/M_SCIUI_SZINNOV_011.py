#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_SZINNOV_011 指标空间分布分析（区级地图）—— 三源探针 + 复现脚本（批 S3-02，Lane 1）。

UI 挂载（实查）：
  ① repos/demo-ui-science/src/ShenzhenInnovation.tsx:3583-3588
     <h4 className="pp-l6-section-title">空间分布分析</h4> + szi-domain-district-scope（全市/单区 chip 切换，
     handleDomainDistrictReset / selectedDomainDistrict）——领域空间分布 Tab 右栏「数据指标」区标题
  ② 同文件 :3616-3634 详细数据指标展示 szi-domain-stats 四卡（企业数量/专利数量/研发投入(亿元)/人才数量，
     domainMetricStats 汇总）——空间分布的数值面
  ③ 同文件 :224-228 mapDisplayModeOptions（标记点/热力图/混合）与 :3554+ domainHeatLayerPoints 热力层——
     区级 GIS 展示形态；shenzhenDistricts 常量（:186-199）深圳 10+1 区中心坐标
  ④ mock：generateTechDomains（:863-880）八大领域 enterprises/patents/rdInvestment/talents 四维
     （合成生物 4,820 企业/30,100 专利/516.2 亿研发/92,400 人才——演示值，不作数据证据）

需求原文（SRS《深圳创新监测.md》seq 126 / excel_row 129『空间分布分析』）：
  「分析各科技领域的空间分布特征，包括分布范围、中心位置、扩散方向，用户可查看各领域的空间分布模式
   和发展趋势。」+ 相邻叶 seq 124 热力图展示『利用热力图直观展示深圳市各科技领域的空间分布和聚集程度』。
  主需求文档 :781+ 同模块（1.1.1.1.4.1.6.3）。→ 区级 GIS 粒度是需求明文（派单书 §0.3）。

三源结论（探针实测）：
  gkx  dwd_dim_admin_area(20,000) 是村级粒度（12 位码 19,988 行）：深圳 4403 前缀 34 行、8 区有键、
       坪山区(440310) 0 行；无 level 列（层级靠编码位数推断）——区划字典可用但坪山缺键
       区级聚合主路径 = dwd_org_base_info(189,116) city='深圳市' 95,600 行 → area 列（9 区有值：
       宝安 25,192 / 龙岗 17,445 / 南山 16,039 / 龙华 13,879 / 福田 8,810 / 光明 6,879 / 罗湖 3,630 /
       坪山 3,027 / 盐田 680——大鹏新区 0 行）；领域维 = industry_l1_name（国民经济行业分类，
       与 UI 八大未来产业语义不同）
  dev  gkxlumenx_dwd.enterprise_base(400) 深圳 46 行 district 列在（7 区有值）——精选层小盘；
       enterprise_industry_chain(100) 产业维
  jiuxin ads_location(22,226) 有 DISTRICT 级 9 行=深圳 9 区（宝安/龙岗/盐田/福田/光明/罗湖/龙华/坪山/
       南山——大鹏缺）；ads_geo_yearly_metrics(171,736)/ads_geo_yearly_institution_type_metrics(349,396)
       层级仅 CITY/PROVINCE/COUNTRY/CONTINENT——DISTRICT 级 0 数据行；
       ads_institution_profile.district_location_id 全库仅 124 机构有区级键（深圳 9 区 124 行全量）
判档：部分支持——区级「载体计数」可算（gkx org 95,600 行 area 维聚合一次跑通，口径 A 即交付面）；
  但需求原文的『各科技领域』语义维（UI 八大未来产业）在三源区级粒度上均无映射
  （gkx industry_l1_name 是国民经济分类；久新 field 维只有机构级无区级聚合面）；
  坪山/大鹏两区在 gkx 区划字典 0 键、久新 9 区缺大鹏——10+1 区覆盖不齐。
复现口径（B10 双口径并列）：
  口径 A（gkx 区级载体分布·企业数量卡同构）——深圳 9 区 org_base_info area 计数 + 区内 Top3 行业
  口径 B（久新区级科研机构分布）——ads_institution_profile 深圳九区机构计数（小盘对照，验证 DISTRICT 键链）
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

# 区划字典：深圳子树
rows = probe("gkx dwd_dim_admin_area 深圳子树（4403 前缀逐区计数）", "gkx",
             "SELECT SUBSTRING(cur_code,1,6) p6, COUNT(*) c FROM gkx.dwd_dim_admin_area "
             "WHERE cur_code LIKE '4403%%' GROUP BY p6 ORDER BY c DESC", gc,
             "440303罗湖/440304福田/440305南山/440306宝安/440307盐田/440308(盐田并入前)/440309龙华/"
             "440310坪山 0 行/440311光明/440361大鹏——村级字典，坪山无键")
facts["gkx_admin_area_sz_prefix"] = {r[0]: int(r[1]) for r in rows}
facts["gkx_admin_area_sz_rows"] = sum(int(r[1]) for r in rows)

# 口径 A：区级载体分布（area 列聚合）
rows = probe("gkx 深圳机构 area 区级分布（口径 A 主读数）", "gkx",
             "SELECT area, COUNT(*) c FROM gkx.dwd_org_base_info WHERE city='深圳市' "
             "AND area IS NOT NULL AND area != '' GROUP BY area ORDER BY c DESC", gc,
             "95,600 家深圳机构按 9 区聚合；大鹏新区 0 行")
facts["gkx_sz_org_by_district"] = {r[0]: int(r[1]) for r in rows}
gc.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE city='深圳市'")
facts["gkx_sz_org_total"] = int(gc.fetchone()[0])

# 区内 Top3 行业（领域维现状：国民经济分类非八大未来产业）
rows = probe("gkx 深圳机构 area×industry_l1_name Top（每区 Top3）", "gkx",
             "SELECT area, industry_l1_name, COUNT(*) c FROM gkx.dwd_org_base_info "
             "WHERE city='深圳市' AND area IN ('南山区','宝安区','龙岗区') AND industry_l1_name IS NOT NULL "
             "GROUP BY area, industry_l1_name ORDER BY area, c DESC LIMIT 30", gc,
             "领域维=industry_l1_name（国民经济行业分类）——与 UI 八大未来产业（合成生物/量子信息…）语义不同")
dist_top_ind = {}
for d, ind, n in rows:
    lst = dist_top_ind.setdefault(d, [])
    if len(lst) < 3:
        lst.append((ind, int(n)))
facts["gkx_sz_district_top_industries_sample"] = dist_top_ind
gc.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE city='深圳市' AND industry_l1_name IS NOT NULL")
facts["gkx_sz_org_with_industry"] = int(gc.fetchone()[0])

gc.close()

# ================================================================ dev
dv = live("DWD")
dc = dv.cursor()
rows = probe("dev enterprise_base 深圳区级分布（精选层）", "dev",
             "SELECT district, COUNT(*) c FROM enterprise_base WHERE city='深圳市' "
             "GROUP BY district ORDER BY c DESC", dc,
             "400 行精选层中深圳 46 家、7 区有值（宝安18/南山8/龙华7/福田4/龙岗4/光明3/坪山2）")
facts["dev_sz_base_by_district"] = {r["district"]: int(list(r.values())[1]) for r in rows if r["district"]}
dc.execute("SELECT COUNT(*) FROM enterprise_base WHERE city='深圳市'")
facts["dev_sz_base_total"] = int(dc.fetchone()["COUNT(*)"])
dc.close()
dv.close()

# ================================================================ jiuxin
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", connect_timeout=30, read_timeout=300)
jc = jx.cursor()

rows = probe("jiuxin ads_location DISTRICT 级行数与名单", "jiuxin",
             "SELECT name_zh, location_id FROM ads_location WHERE location_level='DISTRICT'", jc,
             "DISTRICT 级全库仅 9 行=深圳 9 区（大鹏缺）——久新区级地理键存在性主证据")
facts["jiuxin_district_locations"] = {r[0]: r[1] for r in rows}

# geo 年表 DISTRICT 0 行（数据级缺失）
rows = probe("jiuxin ads_geo_yearly_metrics 层级分布（DISTRICT 判定）", "jiuxin",
             "SELECT m.location_level, COUNT(*) c FROM ads_geo_yearly_metrics m GROUP BY m.location_level "
             "ORDER BY c DESC", jc,
             "CITY 132,975 / PROVINCE 33,518 / COUNTRY 5,081 / CONTINENT 162——DISTRICT 0 行（对齐共享快照 #44 零漂移）")
facts["jiuxin_geo_yearly_levels"] = {r[0]: int(r[1]) for r in rows}

# 口径 B：institution_profile 区级
rows = probe("jiuxin ads_institution_profile 深市区级机构分布（口径 B）", "jiuxin",
             "SELECT p.district_name, COUNT(*) c FROM ads_institution_profile p JOIN ads_location l "
             "ON l.location_id=p.district_location_id WHERE l.location_level='DISTRICT' "
             "GROUP BY p.district_name ORDER BY c DESC", jc,
             "全库 district 键机构 124 家，深圳 9 区全量——DISTRICT 键链可用性验证（小盘）")
facts["jiuxin_district_institutions"] = {r[0]: int(r[1]) for r in rows}
jc.execute("SELECT COUNT(*) FROM ads_institution_profile WHERE district_location_id IS NOT NULL")
facts["jiuxin_profile_with_district_total"] = int(jc.fetchone()[0])

jc.close()
jx.close()

# ================================================================ derived
derived = []
d = facts["gkx_sz_org_by_district"]
facts["gkx_sz_district_covered"] = sum(d.values())
if d and facts["gkx_sz_org_total"]:
    top = max(d, key=d.get)
    derived.append({
        "key": "gkx_sz_district_org_top_share_pct",
        "value": round(d[top] / facts["gkx_sz_org_total"] * 100, 2),
        "numerator": d[top], "denominator": facts["gkx_sz_org_total"],
        "note": f"分子=Top1 区（{top} {d[top]} 家）；分母=深圳机构总数（city=深圳市 全量）；"
                f"同表同口径（gkx.dwd_org_base_info，B3）——空间集中度读数"})
    derived.append({
        "key": "gkx_sz_district_org_coverage_pct",
        "value": round(facts["gkx_sz_district_covered"] / facts["gkx_sz_org_total"] * 100, 2),
        "numerator": facts["gkx_sz_district_covered"], "denominator": facts["gkx_sz_org_total"],
        "note": "分子=area 列 9 区有值行数；分母=深圳机构总数——区级聚合覆盖率（大鹏 0 行在分母缺口内）"})
if facts.get("jiuxin_district_institutions") and facts.get("jiuxin_profile_with_district_total"):
    tot = sum(facts["jiuxin_district_institutions"].values())
    derived.append({
        "key": "jiuxin_district_institution_coverage_pct",
        "value": round(tot / facts["jiuxin_profile_with_district_total"] * 100, 2),
        "numerator": tot, "denominator": facts["jiuxin_profile_with_district_total"],
        "note": "分子=深圳 9 区 district 键机构数；分母=全库 district 键机构总数（124）——"
                "久新 DISTRICT 键全为深圳（区级键仅服务深圳创新监测域）"})

# ================================================================ 产物
out = {
    "metric_id": "M_SCIUI_SZINNOV_011",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:3584",
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:3621",
        "repos/demo-ui-science/src/ShenzhenInnovation.tsx:224",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《深圳创新监测.md》seq 126 / excel_row 129『空间分布分析』（深圳市各科技领域分布展示面板）："
                "『分析各科技领域的空间分布特征，包括分布范围、中心位置、扩散方向…』；相邻叶 seq 124 热力图展示；"
                "seq 112 多层级地理展示明文『可从区级、街道级、产业园级…逐级查看』——区级 GIS 粒度需求明文",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": probes,
    "support_judgment": "部分支持",
    "notes": [
        "判档主轴=区级粒度承载（派单书 §0.3）：gkx 主路径 dwd_org_base_info.city='深圳市' 95,600 行按 area 列"
        "聚合 9 区一次跑通（口径 A 交付面）；但『各科技领域』语义维不闭合——gkx industry_l1_name 是国民经济"
        "行业分类非 UI 八大未来产业，久新 field 维无区级聚合面，三源区级×领域映射需甲方裁定",
        "10 区覆盖不齐（硬事实）：gkx 区划字典深圳子树 34 行中坪山区(440310) 0 键、机构 area 列大鹏新区 0 行；"
        "久新 ads_location DISTRICT 9 行缺大鹏——UI shenzhenDistricts 10 区（9 行政区+大鹏新区）中坪山区在久新有键"
        "且 gkx 机构面有值（3,027 家），大鹏新区双源机构面皆 0——区级地图 10 格有 1 格无数据",
        "久新 CITY 面（ads_geo_yearly_metrics 171,736 行/CITY 132,975）对区级地图无直接承载——"
        "DISTRICT 级 0 数据行（探针在案）；ads_institution_profile.district_location_id 全库仅 124 机构"
        "（深圳 9 区全量=小盘对照），区级科研指标只能机构级自聚合",
        "口径 A 读数（企业数量卡同构）：宝安 25,192 / 龙岗 17,445 / 南山 16,039 / 龙华 13,879 / 福田 8,810 / "
        "光明 6,879 / 罗湖 3,630 / 坪山 3,027 / 盐田 680（大鹏 0）——Top1 宝安占深圳机构总量 26.35%",
        "『中心位置/扩散方向』类空间形态学分析（需求原文分句）三源无 GIS 坐标面承载：gkx org 表有 addr_lng/addr_lat "
        "坐标列（量级未探），可作 v2 扩展（热力图形态）；本件以区级计数为 v1 交付",
    ],
    "base_years_used": [2026],
    "base_years_missing": [],
    "base_years_note": "口径 A 为存量截面（org 底册当期）；需求的时间趋势面（seq 126『发展趋势』）"
                       "需注册年序列（org.incorporation_date 可回算，见 SZINNOV_007 件），本件不展开",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
refs = {"26.35"}
refs |= {str(v) for v in facts["gkx_sz_org_by_district"].values()}
refs |= {str(facts["gkx_sz_org_total"])}
refs |= {str(v) for v in facts.get("jiuxin_district_institutions", {}).values()}
refs |= {str(d["value"]) for d in derived}
out["ctx_refs"]["refs"] = sorted(refs)
path = os.path.join(HERE, "M_SCIUI_SZINNOV_011_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("gkx 区分布:", facts["gkx_sz_org_by_district"])
print("derived:", [(x["key"], x["value"]) for x in derived])
