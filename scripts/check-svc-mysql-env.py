# -*- coding: utf-8 -*-
"""连通性检查：Demo 库可读；不打印密码。先 load-svc-mysql-env.ps1。"""
from __future__ import annotations

import os
import sys

try:
    import pymysql
except ImportError:
    print("ERROR: 需要 pymysql — pip install pymysql")
    sys.exit(1)

host = os.environ.get("ENTAN_MYSQL_HOST") or os.environ.get("SVC_ODS_HOST") or ""
port = int(os.environ.get("ENTAN_MYSQL_PORT") or os.environ.get("SVC_ODS_PORT") or "0")
user = os.environ.get("ENTAN_MYSQL_USER") or os.environ.get("SVC_ODS_USER") or ""
pwd = os.environ.get("ENTAN_MYSQL_PASSWORD") or os.environ.get("SVC_ODS_PWD") or ""
ods = os.environ.get("ENTAN_MYSQL_ODS_DB", "demo_gkxlumenx_ods")

if not (host and port and user and pwd):
    print("ERROR: 环境变量未加载。请先: . .\\scripts\\load-svc-mysql-env.ps1")
    sys.exit(1)

if not str(ods).startswith("demo_"):
    print(f"ERROR: ODS 目标必须是 demo_*，当前={ods}")
    sys.exit(1)

print(f"connect {host}:{port} as {user} …")
conn = pymysql.connect(
    host=host, port=port, user=user, password=pwd,
    charset="utf8mb4", connect_timeout=15,
)
cur = conn.cursor()
cur.execute("SHOW DATABASES")
dbs = {r[0] for r in cur.fetchall()}
need = ["demo_gkxlumenx_ods", "demo_gkxlumenx_dwd", "demo_gkxlumenx_ads", "gkxlumenx_ods"]
for name in need:
    print(f"  {'OK' if name in dbs else 'MISSING'}: {name}")

if "demo_gkxlumenx_ods" in dbs:
    cur.execute("SELECT DATABASE()")
    cur.execute("USE `demo_gkxlumenx_ods`")
    cur.execute("SHOW TABLES LIKE 'dwd_org_base_info'")
    row = cur.fetchone()
    print(f"  demo ODS dwd_org_base_info: {'OK' if row else 'MISSING'}")

conn.close()
print("DONE")
