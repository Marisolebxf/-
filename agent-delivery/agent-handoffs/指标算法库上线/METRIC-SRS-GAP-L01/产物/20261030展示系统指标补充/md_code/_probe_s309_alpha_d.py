#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-09 路 α 补充探针 D：dev enterprise_news NULL/空/类型分布修正（探针 C 的
bad_year 查询因 '' 与 DATETIME 比较报错，改写为字符串比较）+ gkx dwd_news_base
fbsj（发布时间拼音列）年度分布。

产物：code/_snapshots/_probe_s309_alpha_d_out.json
"""
import json
import os
import time

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_snapshots", "_probe_s309_alpha_d_out.json")

R = {"generated": "2026-11-02", "probe": "S3-09-alpha-D enterprise_news 质量修正 + gkx fbsj 分布"}

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=600)

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)


def retry_connect(cfg, n=4):
    last = None
    for _ in range(n):
        try:
            return pymysql.connect(**cfg)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5)
    raise last


dev_out = {}
try:
    conn = retry_connect(DEV)
    cur = conn.cursor()
    # publish_time 列类型确认
    cur.execute("SELECT COLUMN_TYPE AS t, IS_NULLABLE AS nul FROM information_schema.columns "
                "WHERE TABLE_SCHEMA='gkxlumenx_dwd' AND TABLE_NAME='enterprise_news' AND COLUMN_NAME='publish_time'")
    r = cur.fetchone()
    dev_out["enterprise_news_publish_time_type"] = {"type": r["t"], "nullable": r["nul"]} if r else None
    # 空/异常年行数（纯字符串比较，避免 DATETIME 报错）
    cur.execute("SELECT COUNT(*) AS n FROM gkxlumenx_dwd.enterprise_news "
                "WHERE publish_time IS NULL OR CHAR_LENGTH(TRIM(CAST(publish_time AS CHAR))) < 4")
    dev_out["enterprise_news_empty_time_rows"] = cur.fetchone()["n"]
    # news_type 分布（内容分类轴参照）
    cur.execute("SELECT news_type, COUNT(*) AS n FROM gkxlumenx_dwd.enterprise_news "
                "GROUP BY news_type ORDER BY n DESC LIMIT 15")
    dev_out["enterprise_news_type_top"] = [{"news_type": r["news_type"], "n": r["n"]} for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    dev_out["error"] = repr(e)
R["dev"] = dev_out

gkx_out = {}
try:
    conn = retry_connect(GKX)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    # fbsj=发布时间（拼音缩写列）；判型后取年分布
    cur.execute("SELECT column_name, column_type FROM information_schema.columns "
                "WHERE table_schema='gkx' AND table_name='dwd_news_base' AND column_name='fbsj'")
    r = cur.fetchone()
    gkx_out["fbsj_type"] = {"column": r[0], "type": r[1]} if r else None
    cur.execute("SELECT SUBSTRING(CAST(fbsj AS CHAR),1,4) AS y, COUNT(*) AS n FROM gkx.dwd_news_base "
                "GROUP BY y ORDER BY y LIMIT 40")
    gkx_out["dwd_news_base_fbsj_year_dist"] = {str(k): int(v) for k, v in cur.fetchall()}
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    gkx_out["error"] = repr(e)
R["gkx"] = gkx_out

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print("probe written:", OUT)
print("dev publish_time type:", dev_out.get("enterprise_news_publish_time_type"))
print("dev empty rows:", dev_out.get("enterprise_news_empty_time_rows"))
print("dev type top:", json.dumps(dev_out.get("enterprise_news_type_top", []), ensure_ascii=False)[:300])
print("gkx fbsj type:", gkx_out.get("fbsj_type"))
print("gkx fbsj year dist:", json.dumps(gkx_out.get("dwd_news_base_fbsj_year_dist", {}), ensure_ascii=False)[:500])
