#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版唯一数据入口：三方库 gkx（只读）+ 真实 live 开发库兜底。

铁律（本文件物理强制）：
  1. `demo_gkxlumenx_*` 一律禁引 —— `_check_schema()` 见 'demo_' 直接 raise。
  2. 三方库连接**不得**传 `database=` 或 `charset=` 参数 —— 该实例（9.7.0-commercial）
     传这两个参数会在握手阶段挂死（表现为 `Can't connect ... timed out`，实测 20s 超时）。
     正确做法：不带 db 连上 → `SET NAMES utf8mb4` → 查询时写全 `gkx.表名`。
  3. 行数一律 `COUNT(*)`；`TABLE_ROWS` 只在 >100 万行时作估算并标注。

两套数据面：
  gkx  —— 三方供应商要素库，280 表（279 个 dwd_*），核心源表与 demo 同名同字段。
  live —— 旧机 111.198.38.90:34306 的开发库 gkxlumenx_*，仅用于补齐 gkx 没有的项目自建派生表
          （enterprise_base / *_score / chain_* 等）。新机 10.50.11.76 的 gkxlumenx_* 是空壳，不用。

用法：
    from _gkxdb import gkx, live, gkx_count, live_count
    cur = gkx()                      # 三方库游标（已 SET NAMES utf8mb4）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_patent")
    n = live_count("enterprise_base")   # -> gkxlumenx_dwd.enterprise_base
"""
from __future__ import annotations

import pymysql
import time

# ---------------------------------------------------------------- 三方库 gkx

GKX = dict(
    host="183.240.141.251",
    port=3318,
    user="gkx_reader_zp",
    password="Zp_Use_Gkx_db@123456",
    connect_timeout=60,
    read_timeout=600,
    write_timeout=600,
    autocommit=True,
)

# ---------------------------------------------------------- live 开发库兜底

LIVE = dict(
    host="111.198.38.90",
    port=34306,
    user="gkxlumenx",
    password="GKX@Lumen2026",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=20,
    read_timeout=600,
)

LIVE_SCHEMAS = {
    "ODS": "gkxlumenx_ods",
    "DWD": "gkxlumenx_dwd",
    "ADS": "gkxlumenx_ads",
    "DIM": "gkxlumenx_dim",
    "CFG": "gkxlumenx_cfg",
}

FORBIDDEN = ("demo_gkxlumenx", "demo_")


# ---------------------------------------------------------------- 铁律校验

def _check_schema(name: str) -> str:
    """任何 schema 名含 demo_ 一律拒绝，物理层落实「禁引 demo_*」。"""
    low = (name or "").lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise RuntimeError(
                "[铁律] 禁止访问 %r：20261021 版只允许 gkx 与 live gkxlumenx_*，"
                "demo_* 是演示/造数面，禁引。" % (name,)
            )
    return name


# ---------------------------------------------------------------- 连接器

_gkx_conn = None


def gkx():
    """返回三方库游标。

    注意：不传 database / charset，连上后 SET NAMES utf8mb4。
    """
    global _gkx_conn
    if _gkx_conn is None or not _gkx_conn.open:
        # 该实例在批量扫描后会出现 20—60 秒的握手抖动（实测 2026-10-22 15:10），
        # 单次 connect 超时会让整批件失败。这里重试 3 次，不改变任何查询语义。
        last = None
        for _ in range(3):
            try:
                _gkx_conn = pymysql.connect(**GKX)
                break
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(3)
        else:
            raise last
    cur = _gkx_conn.cursor()
    cur.execute("SET NAMES utf8mb4")
    return cur


def live(which: str = "DWD"):
    """返回 live 开发库连接（DictCursor）。which 可写 ODS/DWD/ADS/DIM/CFG 或完整 schema 名。"""
    db = LIVE_SCHEMAS.get(which.upper(), which)
    _check_schema(db)
    return pymysql.connect(database=db, **LIVE)


# ---------------------------------------------------------------- 便捷查询

def _first(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return list(row.values())[0]
    return row[0]


def gkx_count(table: str) -> int:
    """三方库精确行数。table 可写 'dwd_patent' 或 'gkx.dwd_patent'。"""
    _check_schema(table)
    t = table if table.startswith("gkx.") else "gkx." + table
    cur = gkx()
    try:
        cur.execute("SELECT COUNT(*) FROM " + t)
        return int(_first(cur.fetchone()))
    finally:
        cur.close()


def live_count(table: str, which: str = "DWD") -> int:
    """live 库精确行数。table 可写 'enterprise_base' 或 'gkxlumenx_dwd.enterprise_base'。"""
    _check_schema(table)
    if "." in table:
        sch, t = table.split(".", 1)
        conn = live(sch)
    else:
        t = table
        conn = live(which)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM `" + t + "`")
            return int(_first(cur.fetchone()))
    finally:
        conn.close()


def gkx_exists(table: str) -> bool:
    cur = gkx()
    try:
        cur.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_schema='gkx' AND table_name=%s",
            (table,),
        )
        return cur.fetchone() is not None
    finally:
        cur.close()


def live_exists(table: str, which: str = "DWD") -> bool:
    sch = LIVE_SCHEMAS.get(which.upper(), which)
    _check_schema(sch)
    conn = live(sch)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
                (sch, table),
            )
            return cur.fetchone() is not None
    finally:
        conn.close()


def gkx_columns(table: str):
    cur = gkx()
    try:
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='gkx' AND table_name=%s ORDER BY ordinal_position",
            (table,),
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()


if __name__ == "__main__":
    c = gkx()
    c.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='gkx'")
    print("gkx tables =", c.fetchone()[0])
    c.close()
    print("gkx.dwd_patent =", gkx_count("dwd_patent"))
    print("live.enterprise_base =", live_count("enterprise_base"))
