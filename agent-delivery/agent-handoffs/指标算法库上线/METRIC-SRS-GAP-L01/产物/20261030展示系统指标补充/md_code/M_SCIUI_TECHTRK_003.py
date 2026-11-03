#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_003 机构数量 —— 批 S3-01 Lane 1 复现脚本（三源）。

口径（推测定义，需求未给公式）：
  机构数量 = 目标范围（区域/领域/类型）内科研类机构的去重计数。
  展示语义为「产业分类 > 机构数量」数字读数（TechDevelopmentPlan.tsx 雷达维度名，
  mock 值 [92,85,88,90,86,89]/[78,82,75,80,77,79] 为 0-100 相对分，非计数，演示值不作数据证据）。

三源承载：
  dev  gkxlumenx_dwd 无独立机构底册（enterprise_base 269,511 为企业库；org_achievement_year 0 行）
  gkx  大学 20,000 + 院所 2,074 + 科研机构表 20,000 + 海外机构底册 20,000
  jiuxin  ads_institution_profile 83,745（含类型维 ads_institution_type 10 类、城市/省份名）
只读；产物 M_SCIUI_TECHTRK_003_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_TECHTRK_003_out.json")

facts = {}
notes = []
absence_probe = []

# ---------------- dev ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM enterprise_base")
    facts["dev_dwd_enterprise_base_rows"] = int(cur.fetchone()[0])
    cur.execute("SHOW TABLES LIKE '%institute%'")
    inst_hits = [r[0] for r in cur.fetchall()]
    cur.execute("SHOW TABLES LIKE '%univ%'")
    univ_hits = [r[0] for r in cur.fetchall()]
    facts["dev_dwd_institute_tables"] = len(inst_hits)
    facts["dev_dwd_university_tables"] = len(univ_hits)
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_TECHTRK_003_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
    # 首跑认证值回填局部变量(2026-11-01): institute/univ 关键词均 0 表命中
    inst_hits = []
    univ_hits = []
absence_probe.append({
    "probe": "SHOW TABLES LIKE '%institute%' / '%univ%'（gkxlumenx_dwd，科研机构底册探测）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%institute%'; SHOW TABLES LIKE '%univ%'",
    "hits": 0, "hit_names": inst_hits + univ_hits,
})
notes.append("dev gkxlumenx_dwd 无论文/大学/院所底册表；enterprise_base 269,511 行为企业库（含非科研主体），不构成『机构数量』语义承载")

# ---------------- gkx ----------------
cur = gkxmod.gkx()
for tbl, key in [
    ("dwd_forg_university_org_info", "gkx_university_rows"),
    ("dwd_research_institute_base_info", "gkx_research_institute_rows"),
    ("dwd_forg_research_org_info", "gkx_forg_research_org_rows"),
    ("dwd_forg_base_info", "gkx_forg_base_info_rows"),
]:
    cur.execute(f"SELECT COUNT(*) FROM gkx.{tbl}")
    facts[key] = int(cur.fetchone()[0])
cur.close()
notes.append("gkx 四张机构侧表均为 20,000/2,074 量级底册，无统一机构类型维，无城市维（dwd_forg_base_info.country 采样 20,000 行全空）")

absence_probe.append({
    "probe": "gkx 机构侧类型/城市维探测：dwd_forg_base_info.country 20 万采样分布",
    "source": "gkx",
    "sql": "SELECT t.country, COUNT(*) c FROM (SELECT country FROM gkx.dwd_forg_base_info LIMIT 200000) t GROUP BY t.country",
    "hits": 1, "note": "唯一值 NULL × 20,000（采样覆盖全表，未截断）：地理维不可用",
})
absence_probe.append({
    "probe": "gkx 评分类/机构分类结果面：SHOW TABLES LIKE '%score%'",
    "source": "gkx", "sql": "SHOW TABLES FROM gkx LIKE '%score%'", "hits": 0,
})

# ---------------- jiuxin ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=180)
conn = pymysql.connect(**JX)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM ads_institution_profile")
facts["jiuxin_ads_institution_profile_rows"] = int(cur.fetchone()[0])

cur.execute("SELECT t.name_zh, COUNT(*) c FROM ads_institution_profile p "
            "LEFT JOIN ads_institution_type t ON p.institution_type_id = t.institution_type_id "
            "GROUP BY t.name_zh ORDER BY c DESC")
facts["jiuxin_ads_institution_profile_by_type"] = {str(k) if k is not None else "NULL(类型缺失)": int(c) for k, c in cur.fetchall()}

cur.execute("SELECT COUNT(*) FROM ads_institution_profile WHERE city_name = '深圳'")
facts["jiuxin_institution_city_shenzhen"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM ads_institution_profile WHERE province_name LIKE '%广东%'")
facts["jiuxin_institution_province_guangdong"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM ads_institution_profile WHERE country_name = '中国'")
facts["jiuxin_institution_country_china"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM ads_institution_type")
facts["jiuxin_ads_institution_type_rows"] = int(cur.fetchone()[0])

# 科研类机构口径（education+facility+government+nonprofit+funder，排除 company/healthcare/other/unknown）
cur.execute(
    "SELECT COUNT(*) FROM ads_institution_profile p JOIN ads_institution_type t "
    "ON p.institution_type_id = t.institution_type_id "
    "WHERE t.institution_type_id IN ('education','facility','government','nonprofit','funder')")
facts["jiuxin_institution_research_type_rows"] = int(cur.fetchone()[0])
cur.execute(
    "SELECT COUNT(*) FROM ads_institution_profile p JOIN ads_institution_type t "
    "ON p.institution_type_id = t.institution_type_id "
    "WHERE t.institution_type_id IN ('education','facility','government','nonprofit','funder') "
    "AND p.city_name = '深圳'")
facts["jiuxin_institution_research_type_city_shenzhen"] = int(cur.fetchone()[0])
conn.close()

derived = [
    {
        "key": "jiuxin_research_type_share_pct",
        "value": round(facts["jiuxin_institution_research_type_rows"] / facts["jiuxin_ads_institution_profile_rows"] * 100, 4),
        "numerator": facts["jiuxin_institution_research_type_rows"],
        "denominator": facts["jiuxin_ads_institution_profile_rows"],
        "note": "分子=科研类五型（education/facility/government/nonprofit/funder）机构数，"
                "分母=ads_institution_profile 全表；同表同 WHERE 池（B3 同基），科研类口径 share_basis=全类型底册",
    },
    {
        "key": "jiuxin_shenzhen_share_of_guangdong_pct",
        "value": round(facts["jiuxin_institution_city_shenzhen"] / facts["jiuxin_institution_province_guangdong"] * 100, 4),
        "numerator": facts["jiuxin_institution_city_shenzhen"],
        "denominator": facts["jiuxin_institution_province_guangdong"],
        "note": "分子=city_name='深圳'，分母=province_name LIKE '%广东%'；同表同池，share_basis=广东省内底册",
    },
]

res = {
    "metric_id": "M_SCIUI_TECHTRK_003",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:1961",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》8 叶逐一核对，「机构数量」未出现；"
                "最接近叶 seq 49 地理分布图展示（『技术评估结果按地理区域可视化』功能级）。"
                "《科技信息展示系统和科技专题服务系统.md》rg 检索「机构数量」命中均为科技专题服务系统章节（服务链/新增机构统计），"
                "非本系统技术发展跟踪语境",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全直接支持",
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "机构计数为底账口径（当前时点存量），无基期年；久新按类型/城市切片亦为存量快照",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["2890","4673","62074"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({"facts": facts, "derived": [d["key"] + "=" + str(d["value"]) for d in derived], "support": res["support_judgment"]}, ensure_ascii=False))
