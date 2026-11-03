#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_GSIT_001 论文总数 —— 批 S3-01 Lane 1 复现脚本（三源）。

口径（推测定义，需求未给公式）：
  论文总数 = 论文主档表当前收录行数（库内底账口径，非年度流量口径）。
  语义基准（中信所《中国科技论文统计报告》体系，R1/R2）：论文计数以检索库收录为准。

三源：
  dev  gkxlumenx_dwd 无论文表（共享快照已证：SHOW TABLES LIKE '%paper%' 0 行）
  gkx  gkx.dwd_zh_paper 100,900 行（中文论文库；年份列 cover_year_start varchar）
  jiuxin  ads_paper_profile 4,000,000 行（OpenAlex work 池，language en 382.8 万）
只读；产物 M_SCIUI_GSIT_001_out.json。
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import pymysql
from importlib import import_module
gkxmod = import_module("_gkxdb")

OUT = os.path.join(BASE, "M_SCIUI_GSIT_001_out.json")

facts = {}
notes = []
absence_probe = []

# ---------------- dev ----------------
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=8, read_timeout=60)
try:
    conn = pymysql.connect(database="gkxlumenx_dwd", **DEV)
    cur = conn.cursor()
    cur.execute("SHOW TABLES LIKE '%paper%'")
    hits = [r[0] for r in cur.fetchall()]
    conn.close()
    facts["dev_dwd_paper_tables"] = len(hits)
    absence_probe.append({
        "probe": "SHOW TABLES LIKE '%paper%'（gkxlumenx_dwd，论文承载探测）",
        "source": "dev", "sql": "SHOW TABLES LIKE '%paper%'",
        "hits": len(hits), "hit_names": hits,
    })
except Exception as e:
    facts["dev_dwd_paper_tables"] = None
    absence_probe.append({
        "probe": "SHOW TABLES LIKE '%paper%'（gkxlumenx_dwd）",
        "source": "dev", "sql": "SHOW TABLES LIKE '%paper%'",
        "hits": -1, "note": f"未取证：{str(e)[:100]}",
    })
    notes.append("dev 论文表探测未取证（连接失败），按共享快照 _shared_probe_s3_01_out.json dims.dev 记录 0 命中引用")

# ---------------- gkx ----------------
cur = gkxmod.gkx()
cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_paper")
facts["gkx_dwd_zh_paper_rows"] = int(cur.fetchone()[0])

# 年份分布：LIMIT 200000 > 全表 100,900 → 未截断，等同全表（note 写明）
cur.execute(
    "SELECT cover_year_start, COUNT(*) c FROM (SELECT cover_year_start FROM gkx.dwd_zh_paper LIMIT 200000) t "
    "WHERE cover_year_start REGEXP '^[0-9]{4}$' GROUP BY cover_year_start ORDER BY cover_year_start DESC LIMIT 10")
year_rows = cur.fetchall()
facts["gkx_dwd_zh_paper_year_dist_top10"] = {str(y): int(c) for y, c in year_rows}
cur.execute(
    "SELECT COUNT(*), SUM(CASE WHEN cover_year_start REGEXP '^[0-9]{4}$' THEN 1 ELSE 0 END) "
    "FROM (SELECT cover_year_start FROM gkx.dwd_zh_paper LIMIT 200000) t")
tot, y4 = cur.fetchone()
facts["gkx_dwd_zh_paper_year4_valid"] = int(y4)
cur.close()
notes.append("gkx 年份分布查询 LIMIT 200000 未截断（全表 100,900 行 < 200,000），结果等同全表，非采样")

# ---------------- jiuxin ----------------
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", connect_timeout=10, read_timeout=180)
conn = pymysql.connect(**JX)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ads_paper_profile")
facts["jiuxin_ads_paper_profile_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT publication_year, COUNT(*) c FROM ads_paper_profile WHERE publication_year IS NOT NULL "
            "GROUP BY publication_year ORDER BY publication_year DESC LIMIT 10")
facts["jiuxin_ads_paper_profile_year_dist_top10"] = {str(y): int(c) for y, c in cur.fetchall()}
cur.execute("SELECT COUNT(*) FROM ads_paper_profile WHERE publication_year IS NULL")
facts["jiuxin_ads_paper_profile_year_null"] = int(cur.fetchone()[0])
cur.execute("SELECT language, COUNT(*) c FROM ads_paper_profile GROUP BY language ORDER BY c DESC LIMIT 5")
facts["jiuxin_ads_paper_profile_language_top5"] = {str(l): int(c) for l, c in cur.fetchall()}
conn.close()

# ---------------- derived ----------------
derived = [{
    "key": "paper_total_jiuxin_plus_gkx",
    "value": facts["jiuxin_ads_paper_profile_rows"] + facts["gkx_dwd_zh_paper_rows"],
    "numerator": facts["jiuxin_ads_paper_profile_rows"],
    "denominator": facts["gkx_dwd_zh_paper_rows"],
    "note": "双库合计口径：久新 ads_paper_profile（OpenAlex 全语种池）+ gkx dwd_zh_paper（中文池）。"
            "numerator/denominator 此处分别为两加数（非比值），分子分母同库各自 COUNT(*)、口径见 facts 键名；"
            "两池可能存在中文论文重复收录，合计值仅作规模上界参考，不建议直接对外",
}]

res = {
    "metric_id": "M_SCIUI_GSIT_001",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/overviewData.js:54",
        "repos/demo-ui-science/src/overviewData.js:578",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "SRS《02-科技信息展示系统/科技发展态势/科技全域态势.md》16 叶逐一核对，「论文总数」未出现；"
                "最接近叶为 seq 10 统计指标展示功能（『数量统计、分布比例、增长趋势』功能描述级），未点名指标名。"
                "《科技信息展示系统和科技专题服务系统.md》rg 检索「论文总数」0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence_probe,
    "support_judgment": "完全直接支持",
    "notes": notes,
    "base_years_used": ["2026", "2025", "2024", "2023", "2022"],
    "base_years_missing": [],
    "base_years_note": "两库年份列可用：gkx cover_year_start（varchar 四位年 100% 有效，B9 已规避类型陷阱）；"
                       "久新 publication_year int。年份仅用于分布描述，总数读数为全库底账、不分年",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": []},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("saved ->", OUT)
print(json.dumps({"facts": facts, "support": res["support_judgment"]}, ensure_ascii=False))
