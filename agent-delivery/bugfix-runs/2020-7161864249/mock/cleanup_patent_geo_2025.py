#!/usr/bin/env python3
"""Precisely remove the approved 2025 patent-map demo rows."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pymysql

BATCH_ID = "mock_patent_geo_2025_20261111"
MANIFEST = Path(__file__).with_name("seed-rows-2025.json")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("batch_id") != BATCH_ID:
        raise RuntimeError("unexpected manifest batch_id")
    org_ids = sorted({row["org_id"] for row in manifest.get("rows", [])})
    if not org_ids:
        raise RuntimeError("empty cleanup manifest")
    sys.path.insert(0, os.environ.get("GKX_PY_APP", ""))
    from gkx_common.config import config  # noqa: PLC0415
    c = config()
    conn = pymysql.connect(
        host=c.mysql_host, port=c.mysql_port, user=c.mysql_user,
        password=c.mysql_password, database=c.mysql_database,
        charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10, read_timeout=60, autocommit=False,
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DATABASE() AS db")
            if cur.fetchone()["db"] != "demo_gkxlumenx_dwd":
                raise RuntimeError("cleanup must run against demo_gkxlumenx_dwd")
            placeholders = ",".join(["%s"] * len(org_ids))
            cur.execute(
                f"DELETE FROM enterprise_patent_history WHERE data_year=2025 AND org_id IN ({placeholders})",
                org_ids,
            )
            deleted = cur.rowcount
        conn.commit()
        print(json.dumps({"batch_id": BATCH_ID, "deleted": deleted}, ensure_ascii=False))
        return 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
