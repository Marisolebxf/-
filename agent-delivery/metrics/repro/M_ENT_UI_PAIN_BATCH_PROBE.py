#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2·组1 探针：痛难点四维（市场拓展/技术研发/管理/融资）+ 科研人数
三源：gkx（183.240.141.251:3318）+ live gkxlumenx_*（111.198.38.90:34306）+ 久新 ads_*
铁律：只读；demo_* 禁引；探针命中数落 _out.json
"""
import json
import os
import pymysql
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkxdb import gkx, live, gkx_count, live_count  # noqa: E402

out = {
    "metric_id": "M_ENT_UI_PAIN_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01",
    "probe_date": "2026-11-04",
    "purpose": "批2·组1（痛难点四维+科研人数）三源探针",
    "ui_evidence": [
        "live 30892 企业分析>企业发展痛难点分析>诊断范围（市场拓展/技术研发/管理/融资 四维勾选）",
        "live 30892 门户服务>企业发展>企业整体概况「科研人数」badge（20261104 盘点实拍）",
    ],
    "facts": {},
    "derived": {},
    "absence_probe": [],
    "support_judgment": None,
    "notes": [],
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "截面件为主；科研人数为存量截面。",
}

cur = gkx()

# ---------- A. gkx 承载面 ----------
# A1 痛难点语义相关表（pain/problem/diagnos 关键词）
cur.execute("SHOW TABLES FROM gkx")
all_tables = [r[0] for r in cur.fetchall()]
out["facts"]["gkx_table_total"] = len(all_tables)
kw = {"pain": [], "problem": [], "diagnos": [], "difficult": []}
for t in all_tables:
    tl = t.lower()
    for k in kw:
        if k in tl:
            kw[k].append(t)
out["facts"]["gkx_painlike_tables"] = kw

# A2 融资维候选：dwd_org_financing_info 行数（M_ENT_PAINPOINT 族已用）
try:
    out["facts"]["gkx_financing_rows"] = gkx_count("dwd_org_financing_info")
except Exception as e:
    out["facts"]["gkx_financing_rows"] = f"ERR:{e}"
# A3 市场拓展维候选：供应商/客户关系（supply）
try:
    out["facts"]["gkx_supply_rows"] = gkx_count("dwd_org_supply_chain")
except Exception:
    out["facts"]["gkx_supply_rows"] = "无表 dwd_org_supply_chain"
# A4 科研人数候选：学者-当前任职机构
cur.execute("""
    SELECT COUNT(DISTINCT we.scholar_id)
    FROM gkx.dwd_scholar_work_experience we
    WHERE we.is_current = 1""")
out["facts"]["gkx_scholar_current_total"] = cur.fetchone()[0]
cur.execute("""
    SELECT we.org_name_en, COUNT(DISTINCT we.scholar_id) AS n
    FROM gkx.dwd_scholar_work_experience we
    WHERE we.is_current = 1 AND we.org_name_en IS NOT NULL AND we.org_name_en <> ''
    GROUP BY we.org_name_en ORDER BY n DESC LIMIT 5""")
out["facts"]["gkx_scholar_by_org_top5"] = [{"org": r[0], "n": r[1]} for r in cur.fetchall()]
cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
out["facts"]["gkx_scholar_total"] = cur.fetchone()[0]

# ---------- B. live 面 ----------
conn = live()
cur = conn.cursor()
cur.execute("SHOW TABLES")
dwd_tables = [list(r.values())[0] for r in cur.fetchall()]
out["facts"]["live_dwd_painlike"] = [t for t in dwd_tables if any(k in t.lower() for k in ("pain", "problem", "diagnos", "research_staff"))]

conn2 = live("ADS")
cur2 = conn2.cursor()
cur2.execute("SHOW TABLES")
ads_tables = [list(r.values())[0] for r in cur2.fetchall()]
pain_ads = [t for t in ads_tables if any(k in t.lower() for k in ("pain", "problem", "diagnos", "staff", "research"))]
out["facts"]["live_ads_painlike"] = pain_ads
out["facts"].setdefault("live_ads_rows", {})
for t in pain_ads[:8]:
    try:
        cur2.execute(f"SELECT COUNT(*) FROM {t}")
        out["facts"]["live_ads_rows"][t] = list(cur2.fetchone().values())[0]
    except Exception as e:
        out["facts"]["live_ads_rows"][t] = f"ERR:{e}"

cur.execute("SHOW COLUMNS FROM enterprise_base")
cols = [list(r.values())[0] for r in cur.fetchall()]
out["facts"]["live_enterprise_base_research_cols"] = [c for c in cols if any(k in c.lower() for k in ("research", "staff", "scholar", "person", "employee"))]

# ---------- C. 久新面（ads_talent_yearly_metrics / ads_technology_stage_assessment） ----------
# 凭据：调研工作区 database_info.yaml jiuxin_warehouse（test2 只读，不进 git）
jx = None
try:
    jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                         password=os.environ.get("JX_DORIS_PASSWORD", ""),
                         database="gkx_technology_analysis_dev", connect_timeout=20, read_timeout=120,
                         autocommit=True)
    jc = jx.cursor()
    jc.execute("SET NAMES utf8mb4")
    jc.execute("SHOW TABLES")
    jt = [r[0] for r in jc.fetchall()]
    out["facts"]["jiuxin_table_total"] = len(jt)
    for t in ("ads_talent_yearly_metrics", "ads_talent_profile", "ads_technology_stage_assessment",
              "ads_technology_region_assessment"):
        if t in jt:
            jc.execute(f"SELECT COUNT(*) FROM {t}")
            n = jc.fetchone()[0]
            jc.execute(f"SHOW COLUMNS FROM {t}")
            ccols = [r[0] for r in jc.fetchall()]
            out["facts"][f"jiuxin_{t}"] = {"rows": n, "ncols": len(ccols),
                                           "cols_sample": ccols[:16]}
        else:
            out["facts"][f"jiuxin_{t}"] = "无表"
except Exception as e:
    out["facts"]["jiuxin_error"] = f"ERR:{e}"
finally:
    if jx:
        jx.close()

out_p = HERE / "out" / "M_ENT_UI_PAIN_BATCH_PROBE_out.json"
out_p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("saved", out_p)
for k, v in out["facts"].items():
    print(" ", k, "=", str(v)[:110])
