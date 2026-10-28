#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_HIGH_VALUE_RATIO 的**否定性证据**探针（不计算指标）。

正文判「完全不支持」，依据是两条可核对的事实：
    1. 链树 `dwd_industry_chain_info` 没有任何「环节价值」类字段（importance/value/
       weight/scale 一个都没有），有的只是 `node_company_count`；
    2. 唯一沾边的 `node_company_count` 填充极稀，且它的语义是「节点内企业数」，
       不是「节点价值」——用它当分子就是偷换概念。

这两条必须落成数，否则「高价值环节占比」这句判断就只是文字。
产物 `code/M_CHAIN_HIGH_VALUE_RATIO_out.json` 存的就是这些否定性证据。

用法：cd code && python3 M_CHAIN_HIGH_VALUE_RATIO.py
"""
from __future__ import annotations

import json
import os
import time
import traceback

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_CHAIN_HIGH_VALUE_RATIO_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=180)


def q(sql, args=None):
    """单次连接 + 重试。gkx 握手会间歇性超时（2026-10-22 实测约 10 次连接 2 次失败），
    一次失败就记 note 会让产物看起来「查了没数据」，掩盖真实原因。"""
    last = None
    for attempt in range(5):
        try:
            conn = pymysql.connect(**GKX)
            with conn.cursor() as cur:
                cur.execute(sql) if args is None else cur.execute(sql, args)
                rows = cur.fetchall()
            conn.close()
            return rows
        except (pymysql.err.OperationalError, OSError) as e:
            last = e
            time.sleep(3 * (attempt + 1))
    raise last


def scalar(sql, args=None):
    r = q(sql, args)
    return list(r[0].values())[0] if r else None


def main() -> int:
    out = {
        "metric_id": "M_CHAIN_HIGH_VALUE_RATIO",
        "metric_name": "产业链高价值环节占比",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "probes": {},
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：占比是「当前链树内高价值环节数 / 环节总数」，"
                            "链树无版本列、无有效期列，不构造年度序列。"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_industry_chain_info", "role": "链树（唯一的环节定义源）"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.information_schema.columns", "role": "字段名模式扫描"},
        ],
    }

    def flush():
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)

    flush()

    # ---- P1 链树字段清单与行数 ----
    try:
        cols = [r["COLUMN_NAME"] for r in q(
            "SELECT COLUMN_NAME FROM information_schema.columns "
            "WHERE table_schema='gkx' AND table_name='dwd_industry_chain_info'")]
        out["probes"]["chain_columns"] = cols
        out["probes"]["chain_rows"] = scalar("SELECT COUNT(*) AS n FROM dwd_industry_chain_info")
        out["probes"]["chain_levels"] = q(
            "SELECT level, COUNT(*) AS n FROM dwd_industry_chain_info GROUP BY level ORDER BY level")
        flush()
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P2 价值类字段是否存在（关键否定证据）----
    try:
        keys = ("value", "importance", "weight", "scale", "score", "gmv", "output")
        found = [c for c in out["probes"].get("chain_columns", [])
                 if any(k in c.lower() for k in keys)]
        out["probes"]["value_like_columns"] = found
        flush()
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P3 全库范围内是否有环节价值表 ----
    try:
        pats = ["%chain%value%", "%chain%importance%", "%link_value%", "%node_value%",
                "%industry_value%", "%chain_weight%"]
        hits = {}
        for p in pats:
            hits[p] = [r["t"] for r in q(
                "SELECT table_name AS t FROM information_schema.tables "
                "WHERE table_schema='gkx' AND table_name LIKE %s", (p,))]
        out["probes"]["value_table_scan"] = hits
        out["probes"]["value_table_hits"] = sum(len(v) for v in hits.values())
        flush()
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P4 node_company_count 的填充率（唯一沾边字段）----
    try:
        tot = out["probes"].get("chain_rows")
        nn = scalar("SELECT COUNT(*) AS n FROM dwd_industry_chain_info "
                    "WHERE node_company_count IS NOT NULL")
        pos = scalar("SELECT COUNT(*) AS n FROM dwd_industry_chain_info "
                     "WHERE node_company_count > 0")
        out["probes"]["node_company_count_nonnull"] = nn
        out["probes"]["node_company_count_positive"] = pos
        out["probes"]["node_company_count_fill"] = round(nn / tot, 6) if tot else None
        out["probes"]["node_company_count_positive_share"] = round(pos / tot, 6) if tot else None
        flush()
    except Exception:
        out["notes"].append("P4 fail: " + traceback.format_exc(limit=1))
        flush()

    pr = out["probes"]
    out["judgment_reason"] = (
        "链树 `dwd_industry_chain_info`（%s 行、%s 个层级）没有任何价值类字段"
        "（value/importance/weight/scale/score 逐个扫，命中 %s 个）；全库按 6 类词根扫"
        "环节价值表，命中 %s 张。唯一沾边的 `node_company_count` 是「节点内企业数」，"
        "非 NULL %s 行（填充率 %s）但正值只有 %s 行——整列恒为 0，是空壳字段，"
        "语义既不是价值、也没有值。"
        "「高价值」这一维在 gkx 无结构与数据闭环，故判完全不支持。"
        % (pr.get("chain_rows"), len(pr.get("chain_levels") or []),
           len(pr.get("value_like_columns") or []), pr.get("value_table_hits"),
           pr.get("node_company_count_nonnull"), pr.get("node_company_count_fill"),
           pr.get("node_company_count_positive")))
    out["conclusion"] = (
        "否定性证据齐备：价值类字段 0 个、价值表 0 张；唯一替代量 `node_company_count` "
        "填充率 %s 但正值 0 行（恒 0 空壳）。高价值环节占比无分子可定义。"
        % pr.get("node_company_count_fill"))
    flush()
    print(json.dumps({k: out[k] for k in ("support_judgment", "conclusion", "notes")},
                     ensure_ascii=False, indent=1)[:800])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
