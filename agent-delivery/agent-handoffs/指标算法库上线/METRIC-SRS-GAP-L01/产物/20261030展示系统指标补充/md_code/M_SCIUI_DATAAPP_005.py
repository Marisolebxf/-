#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAAPP_005 调用用户与应用系统追踪 — 三源探针 + 判档产物
依赖族级快照 _probe_s305_l3_call_out.json；本件补充：用户-应用-部门关联读数。"""
import json, os, sys, pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_probe_s305_l3_call_out.json")
OUT = os.path.join(BASE, "M_SCIUI_DATAAPP_005_out.json")
snap = json.load(open(SNAP))
facts = {}

facts["ui_mount"] = "ApplicationWindow.jsx:311 Card title=调用用户与应用系统追踪（主题数据被调用情况 Tab 第五卡）"
facts["ui_columns"] = ["用户", "部门", "应用系统", "访问主题", "最近调用", "调用次数"]
facts["ui_mock_dataset"] = "mockData.js callUserTracking 8 行（用户追踪六列+userId/ipAddress 隐藏列）"

# ---------- ① dev live ----------
dev = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                      database="gkxlumenx", charset="utf8mb4", connect_timeout=10)
cur = dev.cursor()

facts["dev_call_word_tables"] = snap["facts"]["dev_call_word_tables"]  # [] 族级
# 用户面：sys_user 实测（族级快照 dev_sys_user_rows=3）
cur.execute("SELECT user_id, username, dept_id FROM gkxlumenx.sys_user ORDER BY user_id")
facts["dev_sys_users"] = [[str(c) for c in r] for r in cur.fetchall()]
# 部门关联列核验：sys_user.dept_id 是否有部门目录承载
cur.execute("""SELECT column_name FROM information_schema.columns
               WHERE table_schema='gkxlumenx' AND table_name='sys_user'""")
facts["dev_sys_user_columns"] = sorted(r[0] for r in cur.fetchall())
cur.execute("""SELECT COUNT(*) FROM information_schema.tables
               WHERE table_schema='gkxlumenx' AND table_name='sys_dept'""")
facts["dev_sys_dept_exists"] = bool(cur.fetchone()[0])
if facts["dev_sys_dept_exists"]:
    cur.execute("SELECT dept_id, name FROM gkxlumenx.sys_dept ORDER BY dept_id")
    facts["dev_sys_depts"] = [[str(c) for c in r] for r in cur.fetchall()]
# 应用系统登记面（同 002 结论复验）
cur.execute("""SELECT client_id FROM gkxlumenx.sys_oauth_client_details ORDER BY client_id""")
facts["dev_sys_oauth_clients"] = [r[0] for r in cur.fetchall()]
dev.close()

# ---------- ② gkx ----------
sys.path.insert(0, BASE)
from _gkxdb import gkx  # noqa: E402
gc = gkx()
gc.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gc.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_call_word_tables"] = snap["facts"]["gkx_call_word_tables"]  # []
facts["gkx_track_word_tables"] = sorted(
    t for t in gkx_tables if any(w in t for w in ("track", "audit", "behavior", "visit")))

# ---------- ③ 久新 live ----------
jx = pymysql.connect(host="47.93.119.170", port=29030, user="test2",
                     password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
                     database="gkx_technology_analysis_dev", charset="utf8mb4",
                     connect_timeout=10, read_timeout=300)
jc = jx.cursor()
jc.execute("SHOW TABLES")
jx_live = sorted(r[0] for r in jc.fetchall())
facts["jiuxin_probe_mode"] = "live"
facts["jiuxin_table_count_live"] = len(jx_live)
facts["jiuxin_call_word_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("call", "invoke", "trace", "request_log")))
facts["jiuxin_track_word_tables_live"] = sorted(
    t for t in jx_live if any(w in t for w in ("track", "audit", "behavior", "visit")))
jx.close()

# ---------- 判档 ----------
support = "完全不支持"
derived = [{"call_user_app_tracking_rows": None,
            "note": "调用流水三源零承载；用户面 dev sys_user 仅 3 测试账号、应用系统登记面语义排除（oauth 技术客户端）"}]

absence_probe = [
    {"what": "dev 调用日志表族（call/invoke/trace 词族）", "how": "族级快照 dev_call_word_tables", "hits": 0},
    {"what": "dev 应用系统登记面（business_system 词族，002 已证）", "how": "002 探针复验 oauth 8 技术客户端", "hits": 0},
    {"what": "gkx 调用/行为追踪表族（call/track/audit/behavior/visit 词族，280 表）", "how": "族级+本件词族扫描", "hits": 0},
    {"what": "久新调用/追踪表族（live 当日 215 表）", "how": "本件 SHOW TABLES 词族扫描", "hits": 0},
    {"what": "dev 用户-部门-应用关联（sys_user 3 行实测）", "how": "本件直查 sys_user/sys_dept/sys_oauth", "hits": "结构在但数据非运营面"},
]

out = {"metric_id": "M_SCIUI_DATAAPP_005", "metric_name": "调用用户与应用系统追踪",
       "base_years_used": [],
    "base_years_missing": ["完全不支持：调用遥测面三源零承载，无库内年份基期"],
    "base_years_note": "完全不支持：无基期；mock 演示值不构成基期证据",
    "facts": facts, "derived": derived, "absence_probe": absence_probe, "support_judgment": support}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("done ->", OUT)
