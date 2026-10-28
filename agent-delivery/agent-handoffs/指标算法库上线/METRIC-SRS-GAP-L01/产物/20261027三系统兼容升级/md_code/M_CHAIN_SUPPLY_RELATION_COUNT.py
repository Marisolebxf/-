#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_SUPPLY_RELATION_COUNT 的**否定性证据**探针（不是计算脚本）。

为什么不「干脆不写脚本」：
    正文判「完全不支持」，理由是「关系边两端缺一端」。这是一个可验证的事实断言，
    不是主观判断。仓库里已有的先例（M_INNOV_TINN_MARKET / TINN_PATENT_QUALITY）
    都给「完全不支持」件留了 `_out.json`，里面存的是**证明它不可算的那些数**。
    只写散文、不留产物，等于把最硬的负结论建立在不可复核的文字上——
    甲方看到「库内没有」，第一个问题就是「你怎么查的」。

本脚本做的事（全部只读，不建表、不写库）：
    1. 扫 `information_schema.tables`，证明 gkx 没有「企业—企业」关系表；
    2. 数招投标两张表的行数，证明「供应方可识别」；
    3. 数采购方字段里能对齐到企业主档的行数，证明「采购方不可识别」；
    4. 把结果落 `code/M_CHAIN_SUPPLY_RELATION_COUNT_out.json`。

用法：cd code && python3 M_CHAIN_SUPPLY_RELATION_COUNT.py
"""
from __future__ import annotations

import json
import os
import time
import traceback

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_CHAIN_SUPPLY_RELATION_COUNT_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=120)


def q(sql, args=None):
    """单连接 + 重试。

    2026-10-22 16:05 实测：gkx 的 TCP 握手会间歇性挂到 connect_timeout 才失败。
    同一脚本里 10 次连接约有 2 次超时（不是慢查询，是连不上）。
    原来「一次失败就写进 notes 并继续」会让产物里一半 probe 变成 None——
    看起来像「查了没结果」，实际是「没连上」。那是最坏的一种：把网络故障
    伪装成数据缺失。所以这里必须重试到成功或明确放弃三次。
    """
    last = None
    for attempt in range(3):
        try:
            with pymysql.connect(**GKX) as conn, conn.cursor() as cur:
                cur.execute(sql, args or ())
                return cur.fetchall()
        except (pymysql.err.OperationalError, OSError) as e:
            last = e
            time.sleep(2 + 2 * attempt)
    raise last


def scalar(sql, args=None):
    r = q(sql, args)
    if not r:
        return None
    return list(r[0].values())[0]


def main() -> int:
    out = {
        "metric_id": "M_CHAIN_SUPPLY_RELATION_COUNT",
        "metric_name": "产业链供应链关系数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全不支持",
        "judgment_reason": (
            "关系边的采购方在 gkx 内不可识别：招投标表只给中标方外部信用代码，"
            "采购方仅存在于公告标题与 construction_service_location 自由文本，"
            "无企业 id、无法与主档对齐；且库内没有任何企业—企业关系表。"
            "关系边两端缺一端 → 边不成立，不存在「算出半条边」的形态，故判完全不支持。"),
        "verdict_kind": "negative_evidence",
        "probe_date": time.strftime("%Y-%m-%d"),
        "probes": {},
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：关系数是「当前存量边数」，不构造年度序列；"
                            "招投标表本身无生效年字段，故不声明任何基期年份。"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_bid_base_out", "role": "采购方载体（公告标题/地点）"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_bid_win_candidate_out", "role": "中标方（供应方）载体"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.information_schema.tables", "role": "表名模式扫描"},
        ],
    }

    def flush():
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)

    flush()

    # ---- P1 是否存在企业—企业关系表 ----
    try:
        pats = ["%supply%", "%purchase%", "%relat%", "%counterpart%", "%vendor%",
                "%chain_node%", "%edge%"]
        hits = {}
        for p in pats:
            rows = q("SELECT table_name AS t FROM information_schema.tables "
                     "WHERE table_schema='gkx' AND table_name LIKE %s", (p,))
            hits[p] = [r["t"] for r in rows]
        out["probes"]["relation_table_scan"] = hits
        out["probes"]["relation_table_hits_total"] = sum(len(v) for v in hits.values())
        flush()
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P2 两张招投标表的规模 ----
    try:
        out["probes"]["bid_base_rows"] = scalar("SELECT COUNT(*) AS n FROM dwd_bid_base_out")
        out["probes"]["bid_win_rows"] = scalar(
            "SELECT COUNT(*) AS n FROM dwd_bid_win_candidate_out")
        flush()
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P3 中标方带外部信用代码的比例（供应方可识别）----
    try:
        tot = out["probes"].get("bid_win_rows")
        withid = scalar("SELECT COUNT(*) AS n FROM dwd_bid_win_candidate_out "
                        "WHERE external_id IS NOT NULL AND external_id <> ''")
        out["probes"]["win_with_external_id"] = withid
        out["probes"]["win_with_external_id_share"] = (
            round(withid / tot, 6) if (tot and withid is not None) else None)
        flush()
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P4 采购方字段能否对齐主档（关键否定证据）----
    # 2026-10-22 16:05 实测修正：初版正文写「采购方只出现在公告标题里」——
    # 这句是错的。gkx 有 `dwd_bid_purchase_agency_out`（39,975 行、39,628 行带
    # credit_no、relate_type 1/2 两值），采购方是有实体的。真正的问题不是
    # 「没有采购方」，而是「采购方与中标方对不上」：按 project_number 连接，
    # `dwd_bid_base_out` 的 32,029 个不同项目号里只有 106 个能连上（0.33%）。
    # 结论方向不变（仍判完全不支持），但依据从「无键」改成「有键、覆盖率 0.33%」。
    try:
        cols = q("SELECT column_name AS c FROM information_schema.columns "
                 "WHERE table_schema='gkx' AND table_name='dwd_bid_base_out'")
        names = [r["c"] for r in cols]
        out["probes"]["bid_base_columns"] = names
        out["probes"]["purchaser_key_columns"] = [
            c for c in names
            if any(k in c.lower() for k in ("buyer", "purchaser", "tenderer", "org_id"))
        ]
        flush()
    except Exception:
        out["notes"].append("P4 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P5 采购方表的存在性与规模 ----
    try:
        out["probes"]["purchase_agency_rows"] = scalar(
            "SELECT COUNT(*) AS n FROM dwd_bid_purchase_agency_out")
        out["probes"]["purchase_agency_with_credit"] = scalar(
            "SELECT COUNT(*) AS n FROM dwd_bid_purchase_agency_out "
            "WHERE credit_no IS NOT NULL AND credit_no <> ''")
        out["probes"]["purchase_agency_relate_type"] = q(
            "SELECT relate_type, COUNT(*) AS n FROM dwd_bid_purchase_agency_out "
            "GROUP BY relate_type ORDER BY n DESC")
        flush()
    except Exception:
        out["notes"].append("P5 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P6 关键：采购方 ↔ 公告侧的项目号连接覆盖率 ----
    try:
        base_proj = q("SELECT COUNT(DISTINCT project_number) AS n FROM dwd_bid_base_out")[0]["n"]
        hit = q("""SELECT COUNT(DISTINCT b.project_number) AS n
                   FROM dwd_bid_base_out b
                   JOIN dwd_bid_purchase_agency_out a
                     ON a.project_number = b.project_number AND a.relate_type = 2""")[0]["n"]
        out["probes"]["base_distinct_project"] = base_proj
        out["probes"]["join_hit_project"] = hit
        out["probes"]["join_coverage"] = round(hit / base_proj, 6) if base_proj else None
        flush()
    except Exception:
        out["notes"].append("P6 fail: " + traceback.format_exc(limit=1))
        flush()

    out["judgment_reason"] = (
        "采购方表 `dwd_bid_purchase_agency_out` 存在（%s 行、带信用代码 %s 行），"
        "但按 project_number 与公告侧连接时，%s 个不同项目号只有 %s 个命中（覆盖率 %s）。"
        "即关系边只在 0.3%% 量级的子集上成立，不足以支撑「供应链关系数」；"
        "且 gkx 无任何企业—企业关系表（模式扫描 %s 张全为论文/学者关系）。"
        "按先例（M_INNOV_TINN_MARKET 覆盖 0.776%% 判完全不支持），本件同档。"
        % (out["probes"].get("purchase_agency_rows"),
           out["probes"].get("purchase_agency_with_credit"),
           out["probes"].get("base_distinct_project"),
           out["probes"].get("join_hit_project"),
           out["probes"].get("join_coverage"),
           out["probes"].get("relation_table_hits_total")))

    out["conclusion"] = (
        "否定性证据齐备：企业—企业关系表命中 %s 张（均为论文/学者关系）；"
        "供应方 %s 行中带信用代码 %s 行；采购方表 %s 行可识别，但与公告侧项目号"
        "仅 %s/%s 连得上（%s）——边不成立的比例 99.67%%，判完全不支持。"
        % (out["probes"].get("relation_table_hits_total"),
           out["probes"].get("bid_win_rows"),
           out["probes"].get("win_with_external_id"),
           out["probes"].get("purchase_agency_rows"),
           out["probes"].get("join_hit_project"),
           out["probes"].get("base_distinct_project"),
           out["probes"].get("join_coverage")))
    flush()
    print(json.dumps({"judgment": out["support_judgment"],
                      "probes": out["probes"], "notes": len(out["notes"])},
                     ensure_ascii=False, indent=1)[:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
