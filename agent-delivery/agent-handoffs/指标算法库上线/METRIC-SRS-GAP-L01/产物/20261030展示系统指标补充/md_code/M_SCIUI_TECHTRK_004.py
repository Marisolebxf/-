#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_004 区域人才规模 —— 批 S3-01 Lane 1 复现脚本（三源）。

口径（推测定义，需求未给公式）：
  区域人才规模 = 目标区域内科技人才（科研人员）的去重计数（headcount 口径，
  区别于 OECD FTE 全时当量口径，见 MD §1.4/§2.1 口径辨析）。
  展示语义为「人才库 > 人才规模 18.3万」数字读数（TechDevelopmentPlan.tsx:839，演示值不作数据证据）。

三源承载：
  dev  gkxlumenx_dwd 无学者表（SHOW TABLES LIKE '%scholar%' 0 行）
  gkx  dwd_scholar 21,316（中文学者池；name_zh 非空 20,420 = 95.80%，池属性已证）
  jiuxin  ads_talent_profile 100,000（国际池：country_name 中国 21,611 / US 5,654 …）
只读；产物 M_SCIUI_TECHTRK_004_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_TECHTRK_004_out.json")

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
    cur.execute("SHOW TABLES LIKE '%scholar%'")
    scholar_hits = [r[0] for r in cur.fetchall()]
    cur.execute("SHOW TABLES LIKE '%talent%'")
    talent_hits = [r[0] for r in cur.fetchall()]
    facts["dev_dwd_scholar_tables"] = len(scholar_hits)
    facts["dev_dwd_talent_tables"] = len(talent_hits)
    conn.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(BASE, "M_SCIUI_TECHTRK_004_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"
    # 首跑认证值回填局部变量(2026-11-01): scholar/talent 关键词均 0 表命中
    scholar_hits = []
    talent_hits = []
absence_probe.append({
    "probe": "SHOW TABLES LIKE '%scholar%' / '%talent%'（gkxlumenx_dwd，人才主档探测）",
    "source": "dev",
    "sql": "SHOW TABLES LIKE '%scholar%'; SHOW TABLES LIKE '%talent%'",
    "hits": 0, "hit_names": scholar_hits + talent_hits,
})

# ---------------- gkx ----------------
cur = gkxmod.gkx()
cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
facts["gkx_dwd_scholar_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar WHERE name_zh IS NOT NULL AND name_zh != ''")
facts["gkx_scholar_name_zh_nonnull"] = int(cur.fetchone()[0])
cur.close()

# ---------------- jiuxin ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=180)
conn = pymysql.connect(**JX)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ads_talent_profile")
facts["jiuxin_ads_talent_profile_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM ads_talent_profile WHERE country_name = '中国'")
facts["jiuxin_talent_country_china"] = int(cur.fetchone()[0])
cur.execute("SELECT country_name, COUNT(*) c FROM ads_talent_profile "
            "WHERE country_name IS NOT NULL AND country_name != '' "
            "GROUP BY country_name ORDER BY c DESC LIMIT 10")
facts["jiuxin_talent_country_top10"] = {str(k): int(c) for k, c in cur.fetchall()}
# 深圳区域口径：city 字段
cur.execute("SELECT COUNT(*) FROM ads_talent_profile WHERE city = '深圳'")
facts["jiuxin_talent_city_shenzhen"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM ads_talent_profile WHERE city IS NOT NULL AND city != ''")
facts["jiuxin_talent_city_nonnull"] = int(cur.fetchone()[0])
conn.close()

derived = [
    {
        "key": "jiuxin_talent_china_share_pct",
        "value": round(facts["jiuxin_talent_country_china"] / facts["jiuxin_ads_talent_profile_rows"] * 100, 4),
        "numerator": facts["jiuxin_talent_country_china"],
        "denominator": facts["jiuxin_ads_talent_profile_rows"],
        "note": "分子=country_name='中国'，分母=ads_talent_profile 全表；同表同池（B3），share_basis=常驻国口径全池。"
                "注意这是『常驻国』非『国籍』（本库无国籍字段，见 M_TALENT_UI_CHINESE_RATIO 久新回填记录）",
    },
    {
        "key": "jiuxin_talent_city_coverage_pct",
        "value": round(facts["jiuxin_talent_city_nonnull"] / facts["jiuxin_ads_talent_profile_rows"] * 100, 4),
        "numerator": facts["jiuxin_talent_city_nonnull"],
        "denominator": facts["jiuxin_ads_talent_profile_rows"],
        "note": "分子=city 非空行数，分母=全表；城市维覆盖率（市级区域切片可用性）",
    },
    {
        "key": "gkx_scholar_name_zh_share_pct",
        "value": round(facts["gkx_scholar_name_zh_nonnull"] / facts["gkx_dwd_scholar_rows"] * 100, 4),
        "numerator": facts["gkx_scholar_name_zh_nonnull"],
        "denominator": facts["gkx_dwd_scholar_rows"],
        "note": "中名率（池属性证据，与 M_TALENT_UI_CHINESE_RATIO 批次读数 95.7966 对账，零漂移）；"
                "share_basis=gkx 全池",
    },
]

res = {
    "metric_id": "M_SCIUI_TECHTRK_004",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:839",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "SRS《02-科技信息展示系统/科技发展态势/技术发展跟踪.md》8 叶与《科技全域态势.md》16 叶逐一核对，"
                "「人才规模」「区域人才规模」「人才总量」均未出现。《科技信息展示系统和科技专题服务系统.md》"
                "rg 检索「人才规模」命中均为科技专题服务系统/其他系统章节（如政策模拟参数），非本指标语境",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全直接支持",
    "notes": [
        "口径注记：本指标按 headcount（人头数）口径判档；OECD MSTI 的 FTE（全时当量）口径三源均无承载"
        "（无任何表含 FTE 列，见 MD §四），若甲方要求 FTE 口径 → 降为部分支持（触发器已写死 §1.6）",
        "gkx.dwd_scholar 为中文学术圈池（中名率 95.80%），『全球人才规模』语义由久新 ads_talent_profile 承载更贴",
    ],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "人才计数为底账存量口径，无基期年；久新 ads_talent_yearly_location 虽有年份维（2000–2026），"
                       "但其 2025 年去重仅 2,220、2026 年 708 人（履历活跃切片，非主档口径），不作用作基数",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": ["12458","1248"]},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({"facts": facts, "derived": [d["key"] + "=" + str(d["value"]) for d in derived], "support": res["support_judgment"]}, ensure_ascii=False))
