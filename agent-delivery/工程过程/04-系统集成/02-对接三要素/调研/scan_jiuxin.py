# -*- coding: utf-8 -*-
"""Re-scan the Jiuxin read-only Doris library.

Read-only: SHOW TABLES / SHOW FULL COLUMNS / SELECT COUNT(*) only.
Writes _raw_schema.json next to this file. Password comes from env
JX_ADS_PASSWORD; never printed, never committed.
"""
import io
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "_raw_schema.json"


def doris_read(cur, sql):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql)


def main():
    password = os.environ.get("JX_ADS_PASSWORD")
    if not password:
        raise SystemExit("set JX_ADS_PASSWORD")
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=password,
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20,
        read_timeout=600,
        charset="utf8mb4",
    )
    tables = []
    columns = []
    total_rows = 0
    try:
        cur = conn.cursor()
        doris_read(cur, "SELECT VERSION()")
        version = str(cur.fetchone()[0])
        doris_read(cur, "SHOW TABLES")
        names = [row[0] for row in cur.fetchall()]
        bad = [n for n in names if not re.fullmatch(r"[A-Za-z0-9_]+", n)]
        if bad:
            raise RuntimeError("unexpected table names: %r" % bad)
        for index, name in enumerate(names, start=1):
            doris_read(cur, f"SHOW FULL COLUMNS FROM `{name}`")
            desc = [item[0] for item in cur.description]
            cols = [dict(zip(desc, row)) for row in cur.fetchall()]
            doris_read(cur, f"SELECT COUNT(*) FROM `{name}`")
            count = int(cur.fetchone()[0])
            total_rows += count
            tables.append({
                "table": name,
                "table_rows": count,
                "column_count": len(cols),
            })
            for pos, col in enumerate(cols, start=1):
                columns.append({
                    "table": name,
                    "pos": pos,
                    "column": str(col.get("Field")),
                    "type": None if col.get("Type") is None else str(col.get("Type")),
                    "nullable": str(col.get("Null")),
                    "key": "" if col.get("Key") is None else str(col.get("Key")),
                    "comment": "" if col.get("Comment") is None else str(col.get("Comment")),
                })
            print(f"[{index}/{len(names)}] {name} rows={count} cols={len(cols)}", flush=True)
    finally:
        conn.close()

    payload = {
        "database": os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        "scanned_at": date.today().isoformat(),
        "server_version": version,
        "table_count": len(tables),
        "tables": tables,
        "columns": columns,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print("tables", len(tables), "columns", len(columns), "total_rows", total_rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
