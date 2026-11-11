#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS-L2-DS09-KEY-DEMO-L01 · demo 数仓落地脚本（demo_gkxlumenx_ads 表族 + 搬运 + demo 补数）

背景：SEED-L01 实灌库是 gkxlumenx_ads（正式命名），demo_gkxlumenx_ads 无 ts_plan_* 表族。
本脚本把 DS-09 数据面落到 demo 库（用户指令 2026-11-11：数据面切 demo_gkxlumenx_，有数据就用、
没有数据就 mock 入库），Java 只读表原则（D18）不变：

  1) 建表：SHOW CREATE TABLE 自 gkxlumenx_ads 逐表克隆到 demo_gkxlumenx_ads（表结构永随真源，幂等）
  2) 搬运：INSERT INTO demo.t (cols) SELECT cols FROM gkxlumenx_ads.t（列交集，真实种子行全量搬运）
  3) demo 补数：ts_plan_key_area_carrier 增列 service_capacity / resource_focus（仅 demo 库，正式库不动），
     按 sort_no 确定性公式灌值 —— 值源从 FE 写死公式（model 层 buildCarrierListRows）迁到表行，
     正式态数据侧回填真值后 FE 无感切换（D18：mock 行写 ADS 表，接口只读表，禁止接口返回写死 mock）

正式库 gkxlumenx_ads 只读不写；demo 库每次运行 TRUNCATE 后重灌（幂等，可重复执行）。

用法（密码只走环境变量，沿 SEED-L01 约定）：
  python seed_demo_warehouse.py --dry-run
  TS_PLAN_MYSQL_PASSWORD=... python seed_demo_warehouse.py --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import pymysql

HOST = "10.50.11.76"
PORT = 3306
USER = "gkxlumenx"
SRC_DB = "gkxlumenx_ads"      # SEED-L01 实灌库（只读真源）
DST_DB = "demo_gkxlumenx_ads"  # demo 数据面（本脚本目标库）

# demo 补数列（仅建在 demo 库；列注释标明 demo mock 性质与真值回填口径）
DEMO_EXTRA_COLUMNS = {
    "ts_plan_key_area_carrier": [
        ("service_capacity",
         "ALTER TABLE `{dst}`.`ts_plan_key_area_carrier` ADD COLUMN `service_capacity` smallint unsigned NULL "
         "COMMENT '服务能力分 0-100 🧪（demo 补数列：GREATEST(62, 94-(sort_no-1)*3) 确定性公式，与原 FE 演示公式同形；"
         "正式态数据侧回填真值后本列随种子版本翻换；TS-L2-DS09-KEY-DEMO-L01）'"),
        ("resource_focus",
         "ALTER TABLE `{dst}`.`ts_plan_key_area_carrier` ADD COLUMN `resource_focus` varchar(16) NULL "
         "COMMENT '资源重点 🧪（demo 补数列：ELT(MOD(sort_no-1,3)+1, 开放共享/产业转化/科研支撑) 轮转；"
         "正式态数据侧回填真值；TS-L2-DS09-KEY-DEMO-L01）'"),
    ],
}


def connect(db: str) -> pymysql.connections.Connection:
    password = os.environ.get("TS_PLAN_MYSQL_PASSWORD")
    if not password:
        sys.exit("[seed-demo] 缺少环境变量 TS_PLAN_MYSQL_PASSWORD（密码只走环境变量，沿 SEED-L01 约定）")
    return pymysql.connect(host=HOST, port=PORT, user=USER, password=password,
                           database=db, charset="utf8mb4",
                           connect_timeout=10, read_timeout=60, write_timeout=60)


def list_ts_plan_tables(cur) -> list[str]:
    cur.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema=%s AND table_name LIKE 'ts_plan_%%' ORDER BY table_name", (SRC_DB,))
    return [r[0] for r in cur.fetchall()]


def clone_schema(cur, table: str) -> None:
    """SHOW CREATE TABLE 真源克隆（DDL 永随 gkxlumenx_ads，无需手工同步）。"""
    cur.execute(f"SHOW CREATE TABLE `{SRC_DB}`.`{table}`")
    create_sql = cur.fetchone()[1]
    # SHOW CREATE TABLE 返回的语句不带库前缀，连接默认库是源库 → 必须改写到 demo 库执行
    create_sql = re.sub(r"^CREATE TABLE `([^`]+)`", rf"CREATE TABLE `{DST_DB}`.`\1`", create_sql, count=1)
    cur.execute(f"DROP TABLE IF EXISTS `{DST_DB}`.`{table}`")
    cur.execute(create_sql)


def copy_rows(cur, table: str, columns: list[str]) -> None:
    col_list = ",".join(f"`{c}`" for c in columns)
    cur.execute(f"TRUNCATE TABLE `{DST_DB}`.`{table}`")
    cur.execute(f"INSERT INTO `{DST_DB}`.`{table}` ({col_list}) SELECT {col_list} FROM `{SRC_DB}`.`{table}`")


def table_columns(cur, db: str, table: str) -> set[str]:
    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema=%s AND table_name=%s", (db, table))
    return {r[0] for r in cur.fetchall()}


def copy_columns(cur, table: str) -> list[str]:
    """搬运列 = 源表 ∩ demo 表（demo 补数列在源表不存在，必须排除，否则 SELECT 报未知列）。"""
    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position", (SRC_DB, table))
    return [r[0] for r in cur.fetchall() if r[0] in table_columns(cur, DST_DB, table)]


def apply_demo_extras(cur, dry_run: bool) -> list[str]:
    """demo 补数列：缺则 ALTER 建列（幂等）。返回建过的列名清单。"""
    created: list[str] = []
    for table, cols in DEMO_EXTRA_COLUMNS.items():
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema=%s AND table_name=%s", (DST_DB, table))
        existing = {r[0] for r in cur.fetchall()}
        for name, ddl in cols:
            if name in existing:
                continue
            print(f"  [extra] {DST_DB}.{table} 增列 {name}")
            if not dry_run:
                cur.execute(ddl.format(dst=DST_DB))
            created.append(f"{table}.{name}")
    return created


def fill_demo_extras(cur, dry_run: bool) -> None:
    """demo 补数：确定性公式灌值（与原 FE 演示公式同形，行数=22 载体行）。"""
    sql = (
        "UPDATE `{dst}`.`ts_plan_key_area_carrier` SET "
        "`service_capacity` = GREATEST(62, 94 - (sort_no - 1) * 3), "
        "`resource_focus` = ELT(MOD(sort_no - 1, 3) + 1, '开放共享', '产业转化', '科研支撑')"
    ).format(dst=DST_DB)
    if not dry_run:
        cur.execute(sql)


def verify(cur) -> list[tuple[str, int, int]]:
    cur.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema=%s AND table_name LIKE 'ts_plan_%%' ORDER BY table_name", (DST_DB,))
    tables = [r[0] for r in cur.fetchall()]
    out = []
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM `{SRC_DB}`.`{table}`")
        src = cur.fetchone()[0]
        cur.execute(f"SELECT COUNT(*) FROM `{DST_DB}`.`{table}`")
        dst = cur.fetchone()[0]
        out.append((table, src, dst))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="DS-09 demo 数仓落地（demo_gkxlumenx_ads）")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划不执行")
    parser.add_argument("--apply", action="store_true", help="实际执行（建表+搬运+补数）")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("请指定 --dry-run 或 --apply")

    conn = connect(SRC_DB)
    try:
        with conn.cursor() as cur:
            tables = list_ts_plan_tables(cur)
            print(f"[seed-demo] 真源 {SRC_DB} ts_plan_* 共 {len(tables)} 表")
            print(f"[seed-demo] 目标 {DST_DB}（{'DRY-RUN' if args.dry_run else 'APPLY'}）")

            for table in tables:
                print(f"  [clone] {table}")
                if not args.dry_run:
                    clone_schema(cur, table)

            created = apply_demo_extras(cur, args.dry_run)
            if created:
                print(f"[seed-demo] demo 补数列新建：{', '.join(created)}")

            for table in tables:
                columns = copy_columns(cur, table)
                print(f"  [copy ] {table}: {len(columns)} 列")
                if not args.dry_run and columns:
                    copy_rows(cur, table, columns)

            if not args.dry_run:
                fill_demo_extras(cur, args.dry_run)
            print("[seed-demo] demo 补数：service_capacity / resource_focus 按 sort_no 确定性公式灌值（22 载体行）")

            if not args.dry_run:
                conn.commit()
                report = verify(cur)
                bad = [(t, s, d) for t, s, d in report if s != d]
                for table, src, dst in report:
                    mark = "OK " if src == dst else "MISMATCH"
                    print(f"  [{mark}] {table}: src={src} dst={dst}")
                if bad:
                    sys.exit(f"[seed-demo] 行数不一致：{bad}")
                cur.execute(
                    "SELECT COUNT(*) FROM `{}`.`ts_plan_key_area_carrier` WHERE service_capacity IS NOT NULL".format(DST_DB))
                print(f"[seed-demo] 补数列非空行：{cur.fetchone()[0]}")
                print("[seed-demo] 完成 ✅")
            else:
                print("[seed-demo] dry-run 结束（未执行任何写入）")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
