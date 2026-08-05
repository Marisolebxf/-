# -*- coding: utf-8 -*-
"""ODS 库 dwd_org_base_info 表结构+值分布探查脚本（可复现）。
凭证从环境变量读取，禁止硬编码。需先 set 或 $env: 设置：
  SVC_ODS_HOST / SVC_ODS_PORT / SVC_ODS_USER / SVC_ODS_PWD
"""
import pymysql, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HOST = os.environ.get("SVC_ODS_HOST", "")
PORT = int(os.environ.get("SVC_ODS_PORT", "0"))
USER = os.environ.get("SVC_ODS_USER", "")
PWD = os.environ.get("SVC_ODS_PWD", "")
if not (HOST and PORT and USER and PWD):
    print("ERROR: 请先设置环境变量 SVC_ODS_HOST/PORT/USER/PWD（凭证禁止入库）")
    sys.exit(1)

def main():
    # 先连上 server，列出所有库，确认 gkxlumenx_ods 是否存在
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PWD,
                           charset='utf8mb4', connect_timeout=15)
    cur = conn.cursor()

    print("=== [1] 所有数据库 ===")
    cur.execute("SHOW DATABASES")
    dbs = [r[0] for r in cur.fetchall()]
    print(dbs)

    # 确认目标库
    target = None
    for c in ["gkxlumenx_ods", "gkxlumen_ods", "ods"]:
        if c in dbs:
            target = c
            break
    if not target:
        # 模糊匹配含 ods 的
        ods_like = [d for d in dbs if "ods" in d.lower()]
        print("含 ods 的库:", ods_like)
        if ods_like:
            target = ods_like[0]
    print(f"\n=== 目标库: {target} ===")
    if not target:
        print("未找到 ods 库，退出")
        return

    cur.execute(f"USE `{target}`")

    print("\n=== [2] 库内所有表（含 org/base 的）===")
    cur.execute("SHOW TABLES")
    tables = [r[0] for r in cur.fetchall()]
    print(f"总表数: {len(tables)}")
    org_tables = [t for t in tables if "org" in t.lower() or "base" in t.lower()]
    print("含 org/base 的表:", org_tables)

    # 找 dwd_org_base_info 或类似
    base_table = None
    for c in ["dwd_org_base_info", "org_base_info"]:
        if c in tables:
            base_table = c
            break
    if not base_table:
        base_like = [t for t in tables if "base_info" in t.lower()]
        print("含 base_info 的表:", base_like)
        if base_like:
            base_table = base_like[0]
    print(f"\n=== 目标表: {base_table} ===")
    if not base_table:
        print("未找到 base_info 表，退出")
        return

    print(f"\n=== [3] {base_table} 建表 DDL ===")
    cur.execute(f"SHOW CREATE TABLE `{base_table}`")
    row = cur.fetchone()
    print(row[1] if row else "无")

    print(f"\n=== [4] {base_table} 列清单（字段名/类型/注释）===")
    cur.execute(f"""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
        ORDER BY ORDINAL_POSITION
    """, (target, base_table))
    cols = cur.fetchall()
    for c in cols:
        print(f"  {c[0]:35s} | {c[1]:25s} | NULL={c[2]:3s} | {c[3]}")
    print(f"列总数: {len(cols)}")

    # 重点检查 industry / org_type / business_scope
    col_names = [c[0] for c in cols]
    print("\n=== [5] 关键字段存在性检查 ===")
    for k in ["industry", "industry_l1_name", "industry_l1_code", "industry_l2_name",
              "industry_l3_name", "industry_class", "org_type", "business_scope",
              "main_activities", "area", "district"]:
        print(f"  {k:25s}: {'✅ 存在' if k in col_names else '❌ 不存在'}")

    print(f"\n=== [6] {base_table} 行数 ===")
    cur.execute(f"SELECT COUNT(*) FROM `{base_table}`")
    print(f"  总行数: {cur.fetchone()[0]}")

    print(f"\n=== [7] org_type 字段值分布（TOP 30）===")
    if "org_type" in col_names:
        cur.execute(f"""
            SELECT org_type, COUNT(*) AS cnt
            FROM `{base_table}`
            WHERE org_type IS NOT NULL AND org_type <> ''
            GROUP BY org_type
            ORDER BY cnt DESC
            LIMIT 30
        """)
        rows = cur.fetchall()
        print(f"  {'org_type':50s} | cnt")
        print(f"  {'-'*50} | ---")
        for r in rows:
            print(f"  {str(r[0]):50s} | {r[1]}")
        # 非空率
        cur.execute(f"SELECT COUNT(*) FROM `{base_table}` WHERE org_type IS NOT NULL AND org_type <> ''")
        nonnull = cur.fetchone()[0]
        cur.execute(f"SELECT COUNT(*) FROM `{base_table}`")
        total = cur.fetchone()[0]
        print(f"\n  org_type 非空率: {nonnull}/{total} = {nonnull/total*100:.1f}%" if total else "  无数据")
    else:
        print("  org_type 字段不存在，跳过")

    print(f"\n=== [8] business_scope 字段值抽样（前 10 条非空）===")
    if "business_scope" in col_names:
        cur.execute(f"""
            SELECT business_scope FROM `{base_table}`
            WHERE business_scope IS NOT NULL AND business_scope <> ''
            LIMIT 10
        """)
        for i, r in enumerate(cur.fetchall(), 1):
            txt = (r[0] or "")[:120]
            print(f"  [{i}] {txt}")
        # 非空率
        cur.execute(f"SELECT COUNT(*) FROM `{base_table}` WHERE business_scope IS NOT NULL AND business_scope <> ''")
        nonnull = cur.fetchone()[0]
        cur.execute(f"SELECT COUNT(*) FROM `{base_table}`")
        total = cur.fetchone()[0]
        print(f"\n  business_scope 非空率: {nonnull}/{total} = {nonnull/total*100:.1f}%" if total else "  无数据")
    else:
        print("  business_scope 字段不存在，跳过")

    conn.close()
    print("\n=== 完成 ===")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
