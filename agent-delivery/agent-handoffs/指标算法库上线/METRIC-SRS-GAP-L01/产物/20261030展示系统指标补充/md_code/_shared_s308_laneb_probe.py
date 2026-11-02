#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-08 路B 共享探针（P10_001/002/004/008/014/015/019/021/022/023/025 共 11 件）。

一次跑三源，落共享快照 _snapshots/_shared_s308_laneb_probe_out.json；
各件薄壳 py 读快照 + 各自独立实算/复核。

采集面：
  A. dev（10.50.11.76:3306 live，只认 gkxlumenx_*，demo_* 物理禁入）：
     - dwd_patent_transfer 规模/年份分布/权利人样本/省别样本（P10_001/002 流动语义=交易）
     - satisfaction / interact / comment / contribution 词族列扫描（P10_004/008/014/021）
     - talent / personnel / mobility 词族扫描（P10_022/023）
     - trajectory / route / track 词族扫描（P10_015/025）
     - carrier 服务频率面复核（P10_019：reservation/service 词族 + dim.carrier 列）
  B. gkx（183.240.141.251:3318 只读）：transfer/talent/trajectory/satisfaction/interact 词族
  C. jiuxin（Doris 47.93.119.170:29030，SHOW TABLES 实数勿写死）：
     - ads_talent_mobility_yearly_flow 结构+规模+年份分布（P10_022/023 候选主源）
     - transfer / talent / trajectory / satisfaction / interact / mobility 词族全扫
"""
from __future__ import annotations

import json
import os
import re

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP_DIR = os.path.join(BASE, "_snapshots")
SNAP = os.path.join(SNAP_DIR, "_shared_s308_laneb_probe_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=15, read_timeout=300)
GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60, read_timeout=600,
           autocommit=True)
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          connect_timeout=15, read_timeout=600)

FORBIDDEN = ("demo_", "_devdb")

FAMILIES = {
    "transfer":   ["transfer", "transaction", "deal", "license"],
    "talent":     ["talent", "personnel", "scholar", "mobility", "migrat"],
    "trajectory": ["trajectory", "route", "track", "replay", "flow_path"],
    "satisfaction": ["satisf", "survey", "rating", "feedback", "evaluat"],
    "interact":   ["interact", "comment", "like_", "share", "review"],
    "service":    ["service", "reserv", "booking", "appoint", "usage"],
}


def _chk(name: str) -> str:
    low = (name or "").lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise RuntimeError("[铁律] 禁入 %r（demo_*/_devdb 禁引）" % name)
    return name


def fam_hit(text: str):
    t = (text or "").lower()
    return sorted({fam for fam, words in FAMILIES.items()
                   for w in words if w in t})


def probe_dev() -> dict:
    conn = pymysql.connect(**DEV)
    out: dict = {}
    try:
        cur = conn.cursor()
        # 词族扫描：表名 + 列名（information_schema，全 schema gkxlumenx%）
        cur.execute("SELECT schema_name FROM information_schema.schemata "
                    "WHERE schema_name LIKE 'gkxlumenx%'")
        schemas = sorted(list(r.values())[0] for r in cur.fetchall())
        _chk(" ".join(schemas))
        out["dev_schema_count"] = len(schemas)
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%'")
        tables = [tuple(r.values()) for r in cur.fetchall()]
        out["dev_table_total"] = len(tables)
        out["dev_table_name_hits"] = sorted(
            {"%s.%s" % (s, t): fam_hit(t) for s, t in tables if fam_hit(t)}.items())
        cur.execute(
            "SELECT table_schema, table_name, column_name "
            "FROM information_schema.columns WHERE table_schema LIKE 'gkxlumenx%'")
        col_hits = {}
        for r in cur.fetchall():
            v = list(r.values())
            f = fam_hit(v[2])
            if f:
                col_hits.setdefault("%s.%s" % (v[0], v[1]), set()).update(f)
        out["dev_column_name_hits"] = {k: sorted(v) for k, v in sorted(col_hits.items())}

        # dwd_patent_transfer 实测（dev 侧与 gkx 同构）
        cur.execute("SELECT COUNT(*) n FROM gkxlumenx_ods.dwd_patent_transfer")
        out["dev_pt_rows"] = int(cur.fetchone()["n"])
        cur.execute(
            "SELECT LEFT(transfer_effective_date,4) y, COUNT(*) n "
            "FROM gkxlumenx_ods.dwd_patent_transfer "
            "GROUP BY LEFT(transfer_effective_date,4) ORDER BY y")
        out["dev_pt_year_counts"] = {str(r["y"]): int(r["n"]) for r in cur.fetchall()}
        cur.execute(
            "SELECT COUNT(*) n FROM gkxlumenx_ods.dwd_patent_transfer "
            "WHERE transfer_effective_date IS NULL OR transfer_effective_date='' "
            "   OR LENGTH(transfer_effective_date)<4")
        out["dev_pt_no_year_rows"] = int(cur.fetchone()["n"])
        cur.execute("SHOW COLUMNS FROM gkxlumenx_ods.dwd_patent_transfer")
        out["dev_pt_columns"] = sorted(r["Field"] for r in cur.fetchall())
        # 转让人/受让人省别样本（流动方向语义）
        try:
            cur.execute(
                "SELECT transfer_before, transfer_after "
                "FROM gkxlumenx_ods.dwd_patent_transfer LIMIT 3")
            out["dev_pt_holder_sample"] = [
                {"before": str(r["transfer_before"])[:120],
                 "after": str(r["transfer_after"])[:120]} for r in cur.fetchall()]
        except Exception as e:  # noqa: BLE001
            out["dev_pt_holder_sample_error"] = str(e)[:200]

        # dim.carrier 服务/频次相关列（P10_019）
        try:
            cur.execute("SHOW COLUMNS FROM gkxlumenx_dim.carrier")
            out["dev_dim_carrier_columns"] = sorted(r["Field"] for r in cur.fetchall())
            cur.execute("SELECT COUNT(*) n FROM gkxlumenx_dim.carrier")
            out["dev_dim_carrier_rows"] = int(cur.fetchone()["n"])
        except Exception as e:  # noqa: BLE001
            out["dev_dim_carrier_error"] = str(e)[:200]
        # 预约/服务流水表行数复核（INCUB 族已证零承载，本批独立复核）
        for tbl in ["gkxlumenx_ods.dwd_instrument_reservation",
                    "gkxlumenx_dwd.service_record"]:
            try:
                cur.execute("SELECT COUNT(*) n FROM %s" % tbl)
                out["dev_%s_rows" % tbl.split(".")[-1]] = int(cur.fetchone()["n"])
            except Exception:  # noqa: BLE001
                out["dev_%s_rows" % tbl.split(".")[-1]] = "表不存在"
    finally:
        conn.close()
    return out


def probe_gkx() -> dict:
    conn = pymysql.connect(**GKX)
    out: dict = {}
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema='gkx'")
        out["gkx_table_count"] = int(cur.fetchone()[0])
        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='gkx'")
        tables = [r[0] for r in cur.fetchall()]
        out["gkx_table_name_hits"] = sorted(
            {t: fam_hit(t) for t in tables if fam_hit(t)}.items())
        cur.execute(
            "SELECT table_name t, column_name c FROM information_schema.columns "
            "WHERE table_schema='gkx'")
        col_hits = {}
        for t, c in cur.fetchall():
            f = fam_hit(c)
            if f:
                col_hits.setdefault(t, set()).update(f)
        out["gkx_column_name_hits"] = {k: sorted(v) for k, v in sorted(col_hits.items())}
        # gkx 侧专利交易表规模复核
        cur.execute("SELECT COUNT(*) FROM gkx.dwd_patent_transfer")
        out["gkx_pt_rows"] = int(cur.fetchone()[0])
        cur.execute(
            "SELECT LEFT(transfer_effective_date,4) y, COUNT(*) n "
            "FROM gkx.dwd_patent_transfer "
            "GROUP BY LEFT(transfer_effective_date,4) ORDER BY y")
        out["gkx_pt_year_counts"] = {str(y): int(n) for y, n in cur.fetchall()}
        # gkx 人才面（dwd_scholar / dwd_scholar_work_exp P4 探针已采，此处计数复核）
        for t in ["dwd_scholar", "dwd_scholar_work_exp", "dwd_scholar_education_exp"]:
            try:
                cur.execute("SELECT COUNT(*) FROM gkx.%s" % t)
                out["gkx_%s_rows" % t] = int(cur.fetchone()[0])
            except Exception:  # noqa: BLE001
                out["gkx_%s_rows" % t] = "表不存在"
    finally:
        conn.close()
    return out


def probe_jiuxin() -> dict:
    conn = pymysql.connect(**JX)
    out: dict = {}
    try:
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        tables = sorted(list(r.values())[0] if isinstance(r, dict) else r[0]
                        for r in rows)
        out["jiuxin_table_count_live"] = len(tables)  # 现场实数，勿写死
        out["jiuxin_table_name_hits"] = sorted(
            {t: fam_hit(t) for t in tables if fam_hit(t)}.items())
        # 列名扫描（Doris information_schema 可能受限，逐表 DESCRIBE 绕行）
        col_hits = {}
        scan_fail = []
        for t in tables:
            try:
                cur.execute("DESCRIBE `%s`" % t)
                for r in cur.fetchall():
                    c = list(r.values())[0] if isinstance(r, dict) else r[0]
                    f = fam_hit(str(c))
                    if f:
                        col_hits.setdefault(t, set()).update(f)
            except Exception as e:  # noqa: BLE001
                scan_fail.append({"table": t, "error": str(e)[:120]})
        out["jiuxin_column_name_hits"] = {k: sorted(v) for k, v in sorted(col_hits.items())}
        out["jiuxin_describe_failures"] = scan_fail

        # 人才流动表实测（P10_022/023 候选主源）
        def val(r, i=0):
            return list(r.values())[i] if isinstance(r, dict) else r[i]

        def safe(q):
            cur.execute(q)
            return cur.fetchall()

        try:
            rows_ = safe("SELECT COUNT(*) n FROM ads_talent_mobility_yearly_flow")
            out["jx_talent_flow_rows"] = int(val(rows_[0]))
            rows_ = safe("SELECT statistics_year, COUNT(*) n, SUM(talent_count) tc, "
                         "SUM(mobility_event_count) mc FROM ads_talent_mobility_yearly_flow "
                         "WHERE statistics_year IS NOT NULL "
                         "GROUP BY statistics_year ORDER BY statistics_year")
            out["jx_talent_flow_yearly"] = [
                {"year": int(val(r, 0)), "rows": int(val(r, 1)),
                 "talent_count_sum": int(val(r, 2) or 0),
                 "mobility_event_sum": int(val(r, 3) or 0)} for r in rows_]
            rows_ = safe("SELECT COUNT(*) n FROM ads_talent_mobility_yearly_flow "
                         "WHERE statistics_year IS NULL")
            out["jx_talent_flow_null_year_rows"] = int(val(rows_[0]))
            rows_ = safe("SELECT flow_dimension, COUNT(*) n FROM ads_talent_mobility_yearly_flow "
                         "GROUP BY flow_dimension ORDER BY n DESC")
            out["jx_talent_flow_dimensions"] = [
                {"dimension": str(val(r, 0)), "rows": int(val(r, 1))} for r in rows_]
            rows_ = safe("SELECT flow_level, COUNT(*) n FROM ads_talent_mobility_yearly_flow "
                         "GROUP BY flow_level ORDER BY n DESC")
            out["jx_talent_flow_levels"] = [
                {"level": str(val(r, 0)), "rows": int(val(r, 1))} for r in rows_]
        except Exception as e:  # noqa: BLE001
            out["jx_talent_flow_error"] = str(e)[:300]
    finally:
        conn.close()
    return out


def main() -> None:
    snap = {"batch": "S3-08-laneB", "families": FAMILIES}
    snap["dev"] = probe_dev()
    snap["gkx"] = probe_gkx()
    snap["jiuxin"] = probe_jiuxin()
    os.makedirs(SNAP_DIR, exist_ok=True)
    with open(SNAP, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1, default=str)
    print("written:", SNAP)
    print("dev tables:", snap["dev"]["dev_table_total"],
          "| gkx tables:", snap["gkx"]["gkx_table_count"],
          "| jiuxin tables:", snap["jiuxin"]["jiuxin_table_count_live"])
    print("dev pt rows:", snap["dev"]["dev_pt_rows"],
          "| gkx pt rows:", snap["gkx"]["gkx_pt_rows"],
          "| jx talent flow rows:", snap["jiuxin"].get("jx_talent_flow_rows"))


if __name__ == "__main__":
    main()
