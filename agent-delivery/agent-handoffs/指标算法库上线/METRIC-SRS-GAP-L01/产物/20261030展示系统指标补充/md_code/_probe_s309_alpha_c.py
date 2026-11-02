#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-09 路 α 补充探针 C：gkx news 族结构补探（探针 B gkx 连接抖动重试）+ 
dev enterprise_news 年度分布实算（THINK_009 宽口径代理候选）。

产物：code/_snapshots/_probe_s309_alpha_c_out.json
"""
import json
import os
import time

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_snapshots", "_probe_s309_alpha_c_out.json")

R = {"generated": "2026-11-02", "probe": "S3-09-alpha-C gkx news 补探 + enterprise_news 年度分布"}

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


# ============ ① gkx：dwd_news_base 列结构 + 年度分布 ============
gkx_out = {}
try:
    conn = retry_connect(GKX)
    cur = conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='gkx' AND table_name='dwd_news_base' ORDER BY ordinal_position")
    gkx_out["dwd_news_base_columns"] = [r[0] for r in cur.fetchall()]
    # 时间列裁定：实有列再取分布
    cols = gkx_out["dwd_news_base_columns"]
    time_col = next((c for c in cols if c in ("publish_date", "publish_time", "pub_date")), None)
    gkx_out["dwd_news_base_time_col"] = time_col
    if time_col:
        cur.execute(f"SELECT SUBSTRING({time_col},1,4) AS y, COUNT(*) AS n FROM gkx.dwd_news_base "
                    f"GROUP BY y ORDER BY y")
        gkx_out["dwd_news_base_year_dist"] = {str(r[0]): int(r[1]) for r in cur.fetchall()}
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    gkx_out["error"] = repr(e)
R["gkx"] = gkx_out

# ============ ② dev：enterprise_news 年度分布（1,668,414 行时序候选） ============
dev_out = {}
try:
    conn = retry_connect(DEV)
    cur = conn.cursor()
    cur.execute("SELECT SUBSTRING(publish_time,1,4) AS y, COUNT(*) AS n "
                "FROM gkxlumenx_dwd.enterprise_news GROUP BY y ORDER BY y")
    dev_out["enterprise_news_year_dist"] = {str(r["y"]): r["n"] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) AS n FROM gkxlumenx_dwd.enterprise_news WHERE publish_time IS NULL "
                "OR publish_time = '' OR SUBSTRING(publish_time,1,4) NOT BETWEEN '2000' AND '2026'")
    dev_out["enterprise_news_bad_year_rows"] = cur.fetchone()["n"]
    # news_type 分布（内容分类轴参照）
    cur.execute("SELECT news_type, COUNT(*) AS n FROM gkxlumenx_dwd.enterprise_news "
                "GROUP BY news_type ORDER BY n DESC LIMIT 15")
    dev_out["enterprise_news_type_top"] = [{"news_type": r["news_type"], "n": r["n"]} for r in cur.fetchall()]
    cur.close(); conn.close()
except Exception as e:  # noqa: BLE001
    dev_out["error"] = repr(e)
R["dev"] = dev_out

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=str)
print("probe written:", OUT)
print("gkx cols:", len(gkx_out.get("dwd_news_base_columns", [])), "| time col:", gkx_out.get("dwd_news_base_time_col"))
print("gkx year dist:", json.dumps(gkx_out.get("dwd_news_base_year_dist", {}), ensure_ascii=False)[:400])
print("dev ent_news year dist:", json.dumps(dev_out.get("enterprise_news_year_dist", {}), ensure_ascii=False)[:600])
print("dev ent_news bad year rows:", dev_out.get("enterprise_news_bad_year_rows"))
print("dev ent_news type top:", dev_out.get("enterprise_news_type_top"))
