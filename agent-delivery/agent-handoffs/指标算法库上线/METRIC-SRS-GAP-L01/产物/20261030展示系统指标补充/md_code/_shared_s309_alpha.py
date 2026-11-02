#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-09 路 α（THINK 前半 6 件）族级共享探针：三源一次实探，产物供各薄壳复用。

覆盖词族/事实面（按件分组）：
- THINK_002 供方分析能力评分：score/rating/evaluat/assess 词族复核（dev 列级 + gkx + jiuxin，
  INCUB_043/047 已证评分面+模型双缺——本探针独立留证，含 dev 评分域表行数复证）
- THINK_003 竞赛项目评审得分（project score）：competition/contest/award/review/score 词族
- THINK_004 参与人数：participant/registration/enroll 词族
- THINK_005 竞赛奖金总额：prize/bonus/fund 词族
- THINK_006 平台内容总条数：content/article/publish/media 词族（内容主档面）
- THINK_009 内容发布时间趋势：同上 + publish_time/created_time/publish_date 列级时序

铁律：dev 只认 gkxlumenx_*（禁 demo_*/_devdb）；gkx 只读；jiuxin SHOW TABLES 实数勿写死表数。
产物：code/_snapshots/_shared_s309_alpha_out.json
"""
import json
import os
import time

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_snapshots", "_shared_s309_alpha_out.json")

R = {"generated": "2026-11-02", "lane": "S3-09-Alpha"}

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=300)

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
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


# ============ ① dev live（10.50.11.76，只认 gkxlumenx_*） ============
dev_out = {}
try:
    conn = retry_connect(DEV)
    cur = conn.cursor()
    cur.execute("SELECT TABLE_SCHEMA AS sch, TABLE_NAME AS tbl FROM information_schema.tables "
                "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' ORDER BY TABLE_SCHEMA, TABLE_NAME")
    dev_tables = [f"{r['sch']}.{r['tbl']}" for r in cur.fetchall()]
    dev_out["table_total"] = len(dev_tables)
    fams = {
        "score": ["score", "rating", "evaluat", "assess"],
        "competition": ["competition", "contest", "award", "prize", "match_"],
        "participant": ["participant", "registration", "enroll", "signup"],
        "content": ["content", "article", "publish", "media", "news", "cms"],
    }
    for g, ws in fams.items():
        dev_out[f"word_{g}"] = sorted([t for t in dev_tables if any(w in t.lower() for w in ws)])
    # 评分域表行数复证（THINK_002 独立留证；INCUB_043/047 已证双缺）
    for schema, table in [("gkxlumenx_ads", "enterprise_score"), ("gkxlumenx_ads", "carrier_index")]:
        key = f"{schema}.{table}"
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM `{schema}`.`{table}`")
            dev_out[key] = {"rows": cur.fetchone()["n"]}
        except Exception as e:  # noqa: BLE001
            dev_out[key] = {"error": repr(e)}
    # 内容主档候选列级扫描（THINK_006/009）：内容域表有哪些、行数几何
    content_tables = dev_out.get("word_content", [])
    dev_out["content_table_rows"] = {}
    for t in content_tables[:40]:
        sch, tbl = t.split(".", 1)
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM `{sch}`.`{tbl}`")
            dev_out["content_table_rows"][t] = cur.fetchone()["n"]
        except Exception as e:  # noqa: BLE001
            dev_out["content_table_rows"][t] = repr(e)
    # 列级：publish_time/publish_date/view_count/like_count 列分布（THINK_009/010/011/012 底座）
    cur.execute("SELECT TABLE_SCHEMA AS sch, TABLE_NAME AS tbl, COLUMN_NAME AS col "
                "FROM information_schema.columns "
                "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%%' AND (COLUMN_NAME LIKE '%%publish%%' "
                "OR COLUMN_NAME LIKE '%%view_count%%' OR COLUMN_NAME LIKE '%%like_count%%' "
                "OR COLUMN_NAME LIKE '%%browse%%') "
                "ORDER BY TABLE_SCHEMA, TABLE_NAME LIMIT 200")
    dev_out["publish_view_like_columns"] = [
        f"{r['sch']}.{r['tbl']}.{r['col']}" for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    dev_out["error"] = repr(e)
R["dev"] = dev_out

# ============ ② gkx（183.240.141.251:3318 只读） ============
gkx_out = {}
try:
    conn = retry_connect(GKX)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' ORDER BY table_name")
    gkx_tables = sorted([r[0] for r in cur.fetchall()])
    gkx_out["table_count"] = len(gkx_tables)
    fams_g = {
        "score": ["score", "rating", "evaluat", "assess"],
        "competition": ["competition", "contest", "award", "prize", "match_"],
        "participant": ["participant", "registration", "enroll", "signup"],
        "content": ["content", "article", "publish", "media", "news", "cms"],
    }
    for g, ws in fams_g.items():
        gkx_out[f"word_{g}"] = sorted([t for t in gkx_tables if any(w in t.lower() for w in ws)])
    # 内容域表行数（词族命中面逐一 COUNT）
    gkx_content = gkx_out.get("word_content", [])
    gkx_out["content_table_rows"] = {}
    for t in gkx_content[:60]:
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM gkx.`{t}`")
            gkx_out["content_table_rows"][t] = int(cur.fetchone()[0])
        except Exception as e:  # noqa: BLE001
            gkx_out["content_table_rows"][t] = repr(e)
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    gkx_out["error"] = repr(e)
R["gkx"] = gkx_out

# ============ ③ jiuxin（Doris，SHOW TABLES 实数勿写死） ============
jx = {}
try:
    conn = retry_connect(JX)
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = sorted([list(r.values())[0] for r in cur.fetchall()])
    jx["table_count_live"] = len(tables)
    fams_j = {
        "score": ["score", "rating", "evaluat", "assess"],
        "competition": ["competition", "contest", "award", "prize", "match_"],
        "participant": ["participant", "registration", "enroll", "signup"],
        "content": ["content", "article", "publish", "media", "news", "cms"],
    }
    for g, ws in fams_j.items():
        jx[f"word_{g}"] = sorted([t for t in tables if any(w in t.lower() for w in ws)])
    # 内容/竞赛域表行数实查
    for grp in ("word_content", "word_competition", "word_participant", "word_score"):
        jx[f"{grp}_rows"] = {}
        for t in jx.get(grp, [])[:40]:
            try:
                cur.execute(f"SELECT COUNT(*) AS n FROM `{t}`")
                jx[f"{grp}_rows"][t] = cur.fetchone()["n"]
            except Exception as e:  # noqa: BLE001
                jx[f"{grp}_rows"][t] = repr(e)
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    jx["error"] = repr(e)
R["jiuxin"] = jx

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print("probe written:", OUT)
print("dev tables:", dev_out.get("table_total"), "| gkx:", gkx_out.get("table_count"),
      "| jiuxin live:", jx.get("table_count_live"))
print("dev word_score:", dev_out.get("word_score"))
print("dev word_competition:", dev_out.get("word_competition"))
print("dev word_content:", dev_out.get("word_content"))
print("dev content_table_rows:", dev_out.get("content_table_rows"))
print("gkx word_score:", gkx_out.get("word_score"))
print("gkx word_content:", gkx_out.get("word_content"))
print("gkx content_table_rows:", gkx_out.get("content_table_rows"))
print("jiuxin word_score:", jx.get("word_score"))
print("jiuxin word_competition:", jx.get("word_competition"))
print("jiuxin word_content:", jx.get("word_content"))
print("jiuxin word_content_rows:", jx.get("word_content_rows"))
