#!/usr/bin/env python3
"""CHAIN 域共享公共库（B3 批次 20261020）

供各 M_CHAIN_* 指标薄壳脚本 import：
- connect_dev(db) / connect_gkx()
- q / q1 查询助手
- probe_rows(schema_tables) 当日行数复测
- load_sz_cityset() 深圳主体集合（gkx.dwd_org_base_info）
- 桥：gkx.dwd_org_industry_tags 按链聚合（服务端 GROUP BY，避免拉全表）
"""
from __future__ import annotations

import json
from pathlib import Path

import pymysql

ROOT = Path(__file__).resolve().parents[6]
ENV_GKX = ROOT / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"
SNAPSHOT_DIR = Path(__file__).parent / "_snapshots"

DEV = dict(
    host="111.198.38.90",
    port=34306,
    user="gkxlumenx",
    password="GKX@Lumen2026",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=20,
    read_timeout=600,
)


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def connect_dev(db: str):
    # 2026-10-22 从 20261020 目录迁入时禁用：DEV 指向 111.198.38.90 的演示库。
    # 本目录的交付件一律只走 gkx（见 DATA_FACTS_gkx21.md §3.19/§3.21）。
    # 保留函数名是为了让老脚本 import 时不炸；真正调用即报错，避免静默连错库。
    raise RuntimeError("connect_dev 已禁用：本目录只允许 gkx（connect_gkx）")


def connect_gkx():
    e = load_dotenv(ENV_GKX)
    return pymysql.connect(
        host=e["GKX_SRC_HOST"],
        port=int(e["GKX_SRC_PORT"]),
        user=e["GKX_SRC_USER"],
        password=e["GKX_SRC_PASSWORD"],
        database=e.get("GKX_SRC_DB", "gkx"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=20,
        read_timeout=600,
    )


def q(conn, sql: str, args=None):
    with conn.cursor() as cur:
        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        return cur.fetchall()


def q1(conn, sql: str, args=None):
    rows = q(conn, sql, args)
    return rows[0] if rows else None


def count(conn, schema: str, table: str):
    try:
        return int(q1(conn, f"SELECT COUNT(*) AS n FROM `{schema}`.`{table}`")["n"])
    except Exception as e:  # noqa: BLE001
        return f"ERR {str(e)[:60]}"


def is_sz(city) -> bool:
    return city is not None and "深圳" in str(city)


def write_out(metric_id: str, payload: dict):
    out = Path(__file__).parent / f"{metric_id}_out.json"

    def _default(o):
        from decimal import Decimal
        from datetime import date, datetime
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return str(o)

    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default), encoding="utf-8")
    print("wrote", out)
    return out
