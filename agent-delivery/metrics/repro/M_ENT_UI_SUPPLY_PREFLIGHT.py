#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_SUPPLY_PREFLIGHT：数据与权限预检结果（企业供应链关系分析>预检面板，seq26）。
预检=选中企业后，面板对供应链关系数据的可用性自检（有无供数、权限、关系边）。本件复现三源可用性实测。
出参：repro/out/M_ENT_UI_SUPPLY_PREFLIGHT_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live_count  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_SUPPLY_PREFLIGHT",
    "batch": "TOPIC-UI-GAP-L01 批2组2",
    "probe_date": "2026-11-04",
    "purpose": "供应链关系分析预检面板复现（供数面/关系边面可用性三源实测）",
    "ui_evidence": ["live 30892 企业分析>企业供应链关系分析>数据与权限预检（seq26，选企业后交互态）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    # 关系边面：供应商/客户/投融资图谱类承载实测
    cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema='gkx' AND (table_name LIKE '%%supplier%%'
                   OR table_name LIKE '%%customer%%' OR table_name LIKE '%%invest%%'
                   OR table_name LIKE '%%holding%%') ORDER BY table_name""")
    rel_tabs = [r[0] for r in cur.fetchall()][:16]
    out["facts"]["supply_relation_tables"] = {}
    for t in rel_tabs:
        cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
        out["facts"]["supply_relation_tables"][t] = int(cur.fetchone()[0])
    # 企业-企业投资关系（供应链代理边）
    cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema='gkx' AND (table_name LIKE '%%org_outbound_invest%%'
                   OR table_name LIKE '%%org_invest%%')""")
    inv_tabs = [r[0] for r in cur.fetchall()]
    if inv_tabs:
        t0 = inv_tabs[0]
        cur.execute(f"SELECT COUNT(*) FROM gkx.{t0}")
        out["facts"]["org_invest_main_table"] = {"table": t0, "rows": int(cur.fetchone()[0])}
    cur.close()
    out["facts"]["live_eb_rows"] = live_count("enterprise_base")
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "预检面板语义=「有/无数据+权限」自检：供数面（底册 189,116 行）与关系边面（投资/供应商类表实测落产物）在，"
        "预检判定逻辑可搭；但面板的权限判定规则（用户角色×数据域矩阵）属系统配置非数据口径，UI 未给 → 部分支持。"
        "升档触发器：甲方给出权限矩阵或页面接口契约。")
    p = os.path.join(HERE, "out", "M_ENT_UI_SUPPLY_PREFLIGHT_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("rel_tabs =", {k: v for k, v in list(out["facts"]["supply_relation_tables"].items())[:5]})


if __name__ == "__main__":
    main()
