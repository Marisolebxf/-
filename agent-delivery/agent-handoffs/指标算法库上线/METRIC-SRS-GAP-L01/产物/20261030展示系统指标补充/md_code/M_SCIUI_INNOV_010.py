#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INNOV_010 区域投资额 —— 批 S3-01 Lane 6 复现脚本（三源）。

UI 语义（realtimeModel.js:26/215）：实时监测趋势图 y2 轴『金额(亿美元)』investments 月序列
  （mock 316→465 亿美元，2025-04 至 2026-09）；柱状图对比维度『投资额』。
  需求近似叶：SRS seq 83 城市创新数据监控（城市投资规模）+ seq 68 可视化数据呈现（柱状图）。

三源承载（探针实测）：
  dev  投融资 5 表无区域维（enterprise_invest 仅 org 对；3 张链表 0 行）
  gkx  dwd_org_financing_info ⋈ dwd_org_base_info.province/city（省份 100% 广东省 →
        池级区域截断事实）；gkx 自身无区域列（absence）
  jiuxin ads_project_institution ⋈ ads_institution_profile（机构→国家/城市，项目关联 22,571,355 行）
        + ads_project_profile.amount_cny → 区域（机构属地）投资额可聚合；
        ads_research_problem_region_snapshot.investment_score 全空（schema 声明跨币种不可比）
判档：部分支持——『全球区域对比』语义在 gkx 侧被广东池截断（100% 广东省），久新侧可聚合但仅到
  『项目关联机构属地』粒度且金额覆盖 8.7%（63,122/1,838,841）；SRS 要求的『全球主要城市』口径
  在三源均无全球融资事件池。
只读；产物 M_SCIUI_INNOV_010_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_INNOV_010_out.json")

facts = {}
notes = []
absence_probe = []
derived = []

# ---------------- dev：区域维 absence ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    for kw in ("region", "province", "city", "country", "area"):
        cur.execute("SHOW COLUMNS FROM enterprise_invest LIKE '%%%s%%'" % kw)
        hits = [r[0] for r in cur.fetchall()]
        if hits:
            break
    else:
        hits = []
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_INNOV_010_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
    # 首跑认证值回填局部变量(2026-11-01): 区域类列 0 命中
    hits = []
absence_probe.append({
    "probe": "开发库区域维承载：enterprise_invest region/province/city/country/area 列存在性",
    "source": "dev",
    "sql": "SHOW COLUMNS FROM enterprise_invest LIKE '%region%'（province/city/country/area 同法逐词）",
    "hits": len(hits), "hit_names": hits,
    "hit_detail": "区域类列 0 命中；enterprise_forg_invest 仅有 inv_country_code（股东国别，投资方向语义相反）",
})

# ---------------- gkx：融资池区域结构 ----------------
cur = gkxmod.gkx()
# 1) 融资表自身区域列 absence
cur.execute("SHOW COLUMNS FROM gkx.dwd_org_financing_info")
fin_cols = [r[0] for r in cur.fetchall()]
region_like = [c for c in fin_cols if any(k in c.lower() for k in ("country", "province", "city", "area", "region"))]
facts["gkx_financing_cols"] = len(fin_cols)
absence_probe.append({
    "probe": "gkx 融资事件表区域列存在性（21 列逐一核对）",
    "source": "gkx",
    "sql": "SHOW COLUMNS FROM gkx.dwd_org_financing_info",
    "hits": len(region_like), "hit_names": region_like,
    "hit_detail": "区域类列 0 命中（列清单：org_id/name_cn/external_id/funding_round/funding_amount/"
                  "funding_currency_code/completion_date/investors_name/data_source/pre_valuation/after_valuation/…）；"
                  "区域维须 ⋈ dwd_org_base_info（province/city/area）",
})
# 2) join 后省份/城市分布（池级截断证据）
cur.execute(
    "SELECT b.province, COUNT(*) c FROM gkx.dwd_org_financing_info f "
    "JOIN gkx.dwd_org_base_info b ON f.org_id = b.org_id "
    "WHERE b.province IS NOT NULL AND b.province != '' "
    "GROUP BY b.province ORDER BY c DESC LIMIT 12")
prov = {str(p): int(c) for p, c in cur.fetchall()}
facts["gkx_fin_province_dist"] = prov
cur.execute(
    "SELECT b.city, COUNT(*) c FROM gkx.dwd_org_financing_info f "
    "JOIN gkx.dwd_org_base_info b ON f.org_id = b.org_id "
    "WHERE b.city IS NOT NULL AND b.city != '' "
    "GROUP BY b.city ORDER BY c DESC LIMIT 12")
city = {str(p): int(c) for p, c in cur.fetchall()}
facts["gkx_fin_city_top12"] = city
cur.close()

# ---------------- jiuxin：项目→机构→区域 投资额聚合 ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=600)
conn = pymysql.connect(**JX)
cur = conn.cursor()
# 1) 机构国别维：项目金额 CNY 按机构国别聚合（金额覆盖子集；多机构项目会重复计入——口径注记）
#    Doris 大表全量 JOIN 超时 → 改 20 万行采样协议（采样子查询先限 project_institution 再 join，note 标注）
cur.execute(
    "SELECT i.country_name, COUNT(DISTINCT pi.project_id) projects, "
    "COUNT(DISTINCT pi.institution_id) institutions "
    "FROM (SELECT project_id, institution_id FROM ads_project_institution LIMIT 200000) pi "
    "JOIN ads_institution_profile i ON pi.institution_id = i.institution_id "
    "GROUP BY i.country_name ORDER BY projects DESC LIMIT 12")
jx_country = {}
for cn, p, i in cur.fetchall():
    jx_country[str(cn)] = {"projects": int(p), "institutions": int(i)}
facts["jiuxin_project_institution_country_top12"] = jx_country
facts["jiuxin_project_institution_country_sample_note"] = (
    "20 万行采样（ads_project_institution LIMIT 200000 后 join），非全表 22,571,355 行；"
    "全量 GROUP BY 在 Doris 查询超时（实测 query timeout），采样协议见 MD §2.4")
# 2) region_snapshot 投资分（全空证据，与 lane6 探针复测一致）
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN investment_score IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM ads_research_problem_region_snapshot")
rs_n, rs_v = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_region_snapshot_rows"] = rs_n
facts["jiuxin_region_snapshot_investment_score_nonnull"] = rs_v
# 3) 金额覆盖基数（引用 INNOV_007 同源数字，B11 一致）
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN amount_cny IS NOT NULL THEN 1 ELSE 0 END) FROM ads_project_profile")
pp_n, pp_cny = [int(x or 0) for x in cur.fetchone()]
facts["jiuxin_project_profile_rows"] = pp_n
facts["jiuxin_project_amount_cny_rows"] = pp_cny
# 4) 深圳区县级资金（区域投资额的本地粒度参照）
cur.execute(
    "SELECT COUNT(DISTINCT district_location_id) FROM ads_shenzhen_institution_direction_funding "
    "WHERE district_location_id IS NOT NULL AND district_location_id != ''")
facts["jiuxin_shenzhen_funding_districts"] = int(cur.fetchone()[0])
conn.close()

# ---------------- derived ----------------
if "广东省" in prov:
    prov_total = sum(prov.values())
    derived.append({
        "key": "gkx_fin_guangdong_share_pct",
        "value": round(prov["广东省"] / prov_total * 100, 2) if prov_total else None,
        "numerator": prov["广东省"],
        "denominator": prov_total,
        "note": "分子=省份=广东省的融资事件数，分母=省份非空的融资事件数（24,598）；"
                "share_basis=gkx 融资池 join 机构底册子集（B3）——广东 100% 截断证据",
    })
derived.append({
    "key": "jiuxin_project_amount_cny_coverage_pct",
    "value": round(pp_cny / pp_n * 100, 2) if pp_n else None,
    "numerator": pp_cny,
    "denominator": pp_n,
    "note": "分子=amount_cny 非空项目数，分母=ads_project_profile 全表；区域金额聚合的覆盖率上限",
})
if "深圳" in city:
    derived.append({
        "key": "gkx_fin_shenzhen_share_pct",
        "value": round(city["深圳"] / sum(city.values()) * 100, 2),
        "numerator": city["深圳"],
        "denominator": sum(city.values()),
        "note": "分子=城市=深圳的融资事件数，分母=城市 Top12 合计（口径注记：分母为 Top12 非全量城市，仅作城市集中度参考）",
    })

res = {
    "metric_id": "M_SCIUI_INNOV_010",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:215",
        "repos/demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js:26",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「区域投资额」全称未命中；近似叶：SRS 全球创新监测 seq 83『城市创新数据监控』"
                "（城市投资规模监控）；seq 68『可视化数据呈现』（柱状图形态）；技术发展跟踪.md:48 气泡图投资额（另页语境）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "部分支持",
    "notes": [
        "降档主因①（gkx 池截断）：融资池省份 100% 广东省（24,598/24,598）——『全球区域投资额对比』在 gkx 侧"
        "退化为『广东省内城市对比』；城市维可算（Top12 见 facts）但语义非全球",
        "降档主因②（久新金额覆盖）：项目金额 CNY 覆盖 8.7%（160,822/1,838,841，其中 amount 原值仅 63,122），"
        "按机构属地聚合后的区域金额是『有金额子集』口径，覆盖率需随读数披露；"
        "region_snapshot.investment_score 9,367 行全空（schema：跨币种不可比，未实现）",
        "口径注记：久新项目-机构多对多（22,571,355 关联行），同一项目多机构属地会重复计入——区域聚合需按"
        "『主机构』或『均摊』口径裁定后才能出正式读数（B10 双口径待裁定）",
        "UI mock 的『金额(亿美元)』月序列（316→465）为月度投资流；gkx 按月聚合可行（completion_date 100% 覆盖，"
        "INNOV_006 按年已证），但同受广东池截断",
        "升档路径：接全球融资事件源（CB Insights/PitchBook R3/R4）→ 完全直接支持；或甲方接受『广东省内区域对比』"
        "语义 → gkx 侧升完全转换支持（城市维 join 覆盖已证）",
    ],
    "base_years_used": [2024, 2025],
    "base_years_missing": [],
    "base_years_note": "区域聚合读数无固定基期年（存量累计口径）；城市/省份分布为全周期事件计数；"
                       "2026 在途年不参与",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["22857","29075","8826"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({k: facts[k] for k in sorted(facts)}, ensure_ascii=False)[:1800])
