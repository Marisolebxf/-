#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-09 路 α 补充探针 B：内容主档面深度实查（THINK_006/009 专用）。

dev cms_content_* / v_cms_* / app_article / news 族逐表行数+发布时间列分布；
gkx dwd_news_base / dwd_org_important_news_info / dwd_industry_chain_news_info 年度分布；
jiuxin ads_talent_media_report 结构核（内容语义裁定用）。
铁律：dev 只认 gkxlumenx_*；gkx 只读；jiuxin SHOW TABLES 实数。
产物：code/_snapshots/_probe_s309_alpha_b_out.json
"""
import json
import os
import time

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_snapshots", "_probe_s309_alpha_b_out.json")

R = {"generated": "2026-11-02", "probe": "S3-09-alpha-B 内容主档面深度实查"}

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=300)

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Ue_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          cursorclass=pymysql.cursors.DictCursor, connect_timeout=30, read_timeout=600)


def retry_connect(cfg, n=3):
    last = None
    for _ in range(n):
        try:
            return pymysql.connect(**cfg)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3)
    raise last


# ============ ① dev：cms/app/news 内容面结构+行数+时间列 ============
dev_out = {}
try:
    conn = retry_connect(DEV)
    cur = conn.cursor()
    # cms_content_news / cms_content_sz / cms_content_region_roster 结构与行数
    for schema, table in [("gkxlumenx_cms", "cms_content_news"),
                          ("gkxlumenx_cms", "cms_content_sz"),
                          ("gkxlumenx_cms", "cms_content_region_roster"),
                          ("gkxlumenx_dwd", "policy_latest_news"),
                          ("gkxlumenx_dwd", "chain_news"),
                          ("gkxlumenx_dwd", "enterprise_news"),
                          ("gkxlumenx_ods", "news")]:
        key = f"{schema}.{table}"
        try:
            cur.execute(f"SELECT COLUMN_NAME AS col FROM information_schema.columns "
                        f"WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME='{table}' ORDER BY ORDINAL_POSITION")
            cols = [r["col"] for r in cur.fetchall()]
            cur.execute(f"SELECT COUNT(*) AS n FROM `{schema}`.`{table}`")
            n = cur.fetchone()["n"]
            dev_out[key] = {"columns": cols, "rows": n}
        except Exception as e:  # noqa: BLE001
            dev_out[key] = {"error": repr(e)}
    # v_cms_* 视图族行数（词族命中面 COUNT；v_cms_ent 已知 208,397）
    for schema, view in [("gkxlumenx_cms", "v_cms_ent"), ("gkxlumenx_cms", "v_cms_pol"),
                         ("gkxlumenx_cms", "v_cms_prod"), ("gkxlumenx_cms", "v_cms_svc")]:
        key = f"{schema}.{view}"
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM `{schema}`.`{view}`")
            dev_out[key] = {"rows": cur.fetchone()["n"]}
        except Exception as e:  # noqa: BLE001
            dev_out[key] = {"error": repr(e)}
    # policy_latest_news 发布时间年度分布（THINK_009 时序候选）
    if "publish_time" in dev_out.get("gkxlumenx_dwd.policy_latest_news", {}).get("columns", []):
        cur.execute("SELECT SUBSTRING(publish_time,1,4) AS y, COUNT(*) AS n "
                    "FROM gkxlumenx_dwd.policy_latest_news GROUP BY y ORDER BY y")
        dev_out["policy_latest_news_year_dist"] = {str(r["y"]): r["n"] for r in cur.fetchall()}
    # news(ods) 年度分布
    if "publish_time" in dev_out.get("gkxlumenx_ods.news", {}).get("columns", []):
        cur.execute("SELECT SUBSTRING(publish_time,1,4) AS y, COUNT(*) AS n "
                    "FROM gkxlumenx_ods.news GROUP BY y ORDER BY y")
        dev_out["ods_news_year_dist"] = {str(r["y"]): r["n"] for r in cur.fetchall()}
    # 竞赛词族列级补探（competition/contest/prize/award 列名在 dev 542 表分布）
    cur.execute("SELECT TABLE_SCHEMA AS sch, TABLE_NAME AS tbl, COLUMN_NAME AS col "
                "FROM information_schema.columns "
                "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' AND (COLUMN_NAME LIKE '%%competition%%' "
                "OR COLUMN_NAME LIKE '%%contest%%' OR COLUMN_NAME LIKE '%%prize%%' "
                "OR COLUMN_NAME LIKE '%%award%%' OR COLUMN_NAME LIKE '%%participant%%') "
                "ORDER BY TABLE_SCHEMA, TABLE_NAME LIMIT 100")
    dev_out["competition_like_columns"] = [
        f"{r['sch']}.{r['tbl']}.{r['col']}" for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    dev_out["error"] = repr(e)
R["dev"] = dev_out

# ============ ② gkx：news 族年度分布（内容时序候选） ============
gkx_out = {}
try:
    conn = retry_connect(GKX)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    # dwd_news_base 列结构 + 年度分布
    cur.execute("SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='gkx' AND table_name='dwd_news_base' ORDER BY ordinal_position")
    gkx_out["dwd_news_base_columns"] = [r[0] for r in cur.fetchall()]
    for col, key in [("publish_date", "dwd_news_base_publish_year_dist"),
                     ("publish_time", "dwd_news_base_publish_year_dist")]:
        try:
            cur.execute(f"SELECT SUBSTRING({col},1,4) AS y, COUNT(*) AS n FROM gkx.dwd_news_base "
                        f"GROUP BY y ORDER BY y")
            gkx_out[key] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
            gkx_out["dwd_news_base_time_col"] = col
            break
        except Exception:  # noqa: BLE001
            continue
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    gkx_out["error"] = repr(e)
R["gkx"] = gkx_out

# ============ ③ jiuxin：ads_talent_media_report 结构核 ============
jx = {}
try:
    conn = retry_connect(JX)
    cur = conn.cursor()
    cur.execute("DESCRIBE ads_talent_media_report")
    jx["talent_media_report_columns"] = [list(r.values())[0] for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    jx["error"] = repr(e)
R["jiuxin"] = jx

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print("probe written:", OUT)
for k, v in dev_out.items():
    if not k.startswith("error"):
        print("dev", k, "->", (v.get("rows") if isinstance(v, dict) else v))
print("gkx news_base cols:", len(gkx_out.get("dwd_news_base_columns", [])),
      "| time col:", gkx_out.get("dwd_news_base_time_col"))
print("gkx year dist:", gkx_out.get("dwd_news_base_publish_year_dist"))
print("jiuxin media_report cols:", jx.get("talent_media_report_columns"))
