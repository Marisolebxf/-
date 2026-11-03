#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-07 L2 批共享词族探针（SOFTSCI 仪器/孵化 + ECOSYS 跨区协作 + INCUB 7 件）。

判「无承载」前三源逐一留证（派单 §3 / s304 §3 方法论）：
  ① dev live 10.50.11.76:3306 gkxlumenx_*（禁 demo_*/_devdb）
  ② gkx 183.240.141.251:3318（280 表，经 _gkxdb.py）
  ③ 久新 jiuxin 47.93.119.170:29030 gkx_technology_analysis_dev（Doris，只读）

词族：仪器(instrument/equip/device/apparatus)、预约(reserv/book/appoint)、
满意度(satisf/survey/rating/feedback)、孵化(incub/hatch/carrier)、毕业(graduate)、
成长(growth/maturity)、使用率(usage/utiliz)、热度(heat/hot)、
转化(conversion/transfer/commercializ)、跨区协作(cross/collab/coop/region)。
"""
from __future__ import annotations

import json
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

import pymysql  # noqa: E402

OUT = "_snapshots/_probe_s307_l2_out.json"

DEV = dict(
    host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
    charset="utf8mb4", connect_timeout=15, read_timeout=120, autocommit=True,
)
JIUXIN = dict(
    host="47.93.119.170", port=29030, user="test2",
    password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
    database="gkx_technology_analysis_dev", charset="utf8mb4",
    connect_timeout=20, read_timeout=180, autocommit=True,
)

WORD_FAMILIES = {
    "instrument": ["instrument", "equip", "device", "apparatus"],
    "reservation": ["reserv", "booking", "appoint", "book_"],
    "satisfaction": ["satisf", "survey", "rating", "feedback", "nps"],
    "incubation": ["incub", "hatch", "carrier", "graduat"],
    "growth": ["growth", "maturity"],
    "usage": ["usage", "utiliz", "machine_hour"],
    "heat": ["heat", "hot"],
    "conversion": ["conversion", "transfer", "commercializ", "transform"],
    "collaboration": ["collab", "coop", "cross_region", "crossreg"],
}

SHEET = {
    "M_SCIUI_SOFTSCI_003": ["instrument"],
    "M_SCIUI_SOFTSCI_004": ["instrument"],
    "M_SCIUI_SOFTSCI_007": ["incubation"],
    "M_SCIUI_SOFTSCI_009": ["conversion"],
    "M_SCIUI_SOFTSCI_010": ["reservation"],
    "M_SCIUI_SOFTSCI_012": ["satisfaction"],
    "M_SCIUI_SOFTSCI_015": ["instrument"],
    "M_SCIUI_ECOSYS_001": ["collaboration"],
    "M_SCIUI_INCUB_007": ["instrument", "usage", "heat"],
    "M_SCIUI_INCUB_008": ["instrument", "usage"],
    "M_SCIUI_INCUB_011": ["incubation", "growth"],
    "M_SCIUI_INCUB_012": ["incubation"],
}


def match_families(name: str) -> list[str]:
    low = (name or "").lower()
    return sorted(
        fam for fam, words in WORD_FAMILIES.items()
        if any(w in low for w in words)
    )


def scan_mysql_columns(cur, schema_pattern: str, label: str) -> dict:
    """扫 information_schema.columns 的表名+列名命中（dev/gkx 通用）。"""
    cur.execute(
        "SELECT table_schema, table_name, column_name FROM information_schema.columns "
        "WHERE table_schema LIKE %s",
        (schema_pattern,),
    )
    rows = cur.fetchall()
    table_names = sorted({(r[0], r[1]) for r in rows})
    table_hits, column_hits = {}, []
    for sch, tbl in table_names:
        fams = match_families(tbl)
        if fams:
            table_hits[f"{sch}.{tbl}"] = fams
    for sch, tbl, col in rows:
        fams = match_families(col)
        if fams and f"{sch}.{tbl}" not in table_hits:
            column_hits.append({"table": f"{sch}.{tbl}", "column": col, "families": fams})
    column_hits.sort(key=lambda x: (x["table"], x["column"]))
    return {
        "schema_pattern": schema_pattern,
        "table_count": len(table_names),
        "table_name_hits": table_hits,
        "column_name_hits_outside_hit_tables": column_hits[:400],
        "column_hit_overflow": max(0, len(column_hits) - 400),
    }


def main() -> None:
    out = {"generated": 20261102, "batch": "S3-07-L2", "word_families": WORD_FAMILIES,
           "metric_sheet": SHEET, "dev": {}, "gkx": {}, "jiuxin": {}}

    # ---------------- ① dev live ----------------
    dev_fail = 0
    try:
        conn = pymysql.connect(**DEV)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name LIKE 'gkxlumenx%'")
        out["dev"]["gkxlumenx_schema_count"] = int(cur.fetchone()[0])
        cur.execute(
            "SELECT table_schema, COUNT(*) FROM information_schema.tables "
            "WHERE table_schema LIKE 'gkxlumenx%' GROUP BY table_schema ORDER BY table_schema"
        )
        out["dev"]["tables_per_schema"] = {r[0]: int(r[1]) for r in cur.fetchall()}
        out["dev"]["column_scan"] = scan_mysql_columns(cur, "gkxlumenx%", "dev")
        # 载体维表结构 + 行数（孵化族重点候选）
        for full in ("gkxlumenx_dim.carrier", "gkxlumenx_dim.carrier_org_rel",
                     "gkxlumenx_dwd.enterprise_innovation_carrier"):
            sch, tbl = full.split(".")
            cur.execute(
                "SELECT column_name, column_type FROM information_schema.columns "
                "WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position", (sch, tbl))
            cols = [[r[0], r[1]] for r in cur.fetchall()]
            cur.execute(f"SELECT COUNT(*) FROM `{sch}`.`{tbl}`")
            n = int(cur.fetchone()[0])
            out["dev"][f"struct::{full}"] = {"columns": cols, "row_count": n}
        # 跨区协作候选：region 维表
        for full in ("gkxlumenx_dim.region_scope", "gkxlumenx_dim.region_scope_member"):
            sch, tbl = full.split(".")
            cur.execute(f"SELECT COUNT(*) FROM `{sch}`.`{tbl}`")
            out["dev"][f"rows::{full}"] = int(cur.fetchone()[0])
        cur.close(); conn.close()
    except Exception as e:  # noqa: BLE001
        dev_fail += 1
        out["dev"]["error"] = repr(e)
    out["dev"]["connect_failures"] = dev_fail

    # ---------------- ② gkx ----------------
    try:
        cur = gkx()
        out["gkx"]["column_scan"] = scan_mysql_columns(cur, "gkx", "gkx")
        cur.close()
    except Exception as e:  # noqa: BLE001
        out["gkx"]["error"] = repr(e)

    # ---------------- ③ jiuxin（Doris）----------------
    jx_fail = 0
    try:
        jconn = pymysql.connect(**JIUXIN)
        jcur = jconn.cursor()
        # 表数勿写死：现场 SHOW TABLES
        jcur.execute("SHOW TABLES")
        tables = sorted(r[0] for r in jcur.fetchall())
        out["jiuxin"]["table_count_live"] = len(tables)
        tbl_hits = {t: match_families(t) for t in tables if match_families(t)}
        out["jiuxin"]["table_name_hits"] = tbl_hits
        # 列名扫描：information_schema.columns 可能被拒 → SHOW COLUMNS 绕行
        col_scan = {}
        try:
            jcur.execute(
                "SELECT table_name, column_name FROM information_schema.columns "
                "WHERE table_schema='gkx_technology_analysis_dev'"
            )
            col_rows = jcur.fetchall()
            for tbl, col in col_rows:
                fams = match_families(col)
                if fams and not match_families(tbl):
                    col_scan.setdefault(tbl, []).append({"column": col, "families": fams})
            out["jiuxin"]["column_scan_via"] = "information_schema"
        except Exception as e:  # noqa: BLE001
            out["jiuxin"]["column_scan_via"] = f"SHOW TABLES fallback ({type(e).__name__})"
            col_scan = {}
            for t in tables:
                try:
                    jcur.execute(f"SHOW COLUMNS FROM `{t}`")
                    for r in jcur.fetchall():
                        col = r[0]
                        fams = match_families(col)
                        if fams and not match_families(t):
                            col_scan.setdefault(t, []).append({"column": col, "families": fams})
                except Exception as e2:  # noqa: BLE001
                    if "1203" in str(e2):
                        time.sleep(15)
                        jcur.execute(f"SHOW COLUMNS FROM `{t}`")
                        for r in jcur.fetchall():
                            col = r[0]
                            fams = match_families(col)
                            if fams and not match_families(t):
                                col_scan.setdefault(t, []).append({"column": col, "families": fams})
        out["jiuxin"]["column_name_hits_outside_hit_tables"] = {
            k: sorted(v, key=lambda x: x["column"]) for k, v in sorted(col_scan.items())
        }
        # ECOSYS 跨区协作重点候选表结构
        for t in ("ads_institution_collaboration_yearly",
                  "ads_institution_collaboration_subfield_yearly",
                  "ads_topic_country_snapshot", "ads_geo_yearly_metrics",
                  "ads_location", "ads_talent_mobility_yearly_flow"):
            try:
                jcur.execute(f"SHOW COLUMNS FROM `{t}`")
                out["jiuxin"][f"struct::{t}"] = [r[0] for r in jcur.fetchall()]
            except Exception as e2:  # noqa: BLE001
                if "1203" in str(e2):
                    time.sleep(15)
                    jcur.execute(f"SHOW COLUMNS FROM `{t}`")
                    out["jiuxin"][f"struct::{t}"] = [r[0] for r in jcur.fetchall()]
                else:
                    out["jiuxin"][f"struct::{t}"] = f"ERROR {e2!r}"
        jcur.close(); jconn.close()
    except Exception as e:  # noqa: BLE001
        jx_fail += 1
        out["jiuxin"]["error"] = repr(e)
    out["jiuxin"]["connect_failures"] = jx_fail

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("written:", OUT)
    print("dev schemas:", out["dev"].get("gkxlumenx_schema_count"),
          "| gkx tables:", out["gkx"].get("column_scan", {}).get("table_count"),
          "| jiuxin tables:", out["jiuxin"].get("table_count_live"))
    print("dev table hits:", list(out["dev"].get("column_scan", {}).get("table_name_hits", {}).items())[:20])
    print("gkx table hits:", list(out["gkx"].get("column_scan", {}).get("table_name_hits", {}).items())[:20])
    print("jiuxin table hits:", list(out["jiuxin"].get("table_name_hits", {}).items())[:20])


if __name__ == "__main__":
    main()
