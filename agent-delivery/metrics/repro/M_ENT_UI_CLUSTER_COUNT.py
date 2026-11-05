#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_CLUSTER_COUNT：企业整体概况·产业集群企业数量（seq156）复现件。
产业集群口径（live 12 链主树 × gkx 企业挂接）承载实测。
出参：repro/out/M_ENT_UI_CLUSTER_COUNT_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_CLUSTER_COUNT",
    "batch": "TOPIC-UI-GAP-L01 批6",
    "probe_date": "2026-11-05",
    "purpose": "产业集群企业数量（概况口径）承载实测",
    "ui_evidence": ["seq156 企业整体概况·产业集群企业数量（无视图证据行，概况 KPI 面）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    # live 链树与挂接表现状
    conn = live("DWD")
    with conn.cursor() as c:
        c.execute("SELECT COUNT(*) AS n FROM chain WHERE chain_id NOT LIKE 'INB17%'")
        out["facts"]["live_chain_main"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM chain_enterprise")
        out["facts"]["chain_enterprise_rows"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM enterprise_industry_chain")
        out["facts"]["eic_rows"] = int(c.fetchone()["n"])
        c.execute("SELECT COUNT(*) AS n FROM enterprise_industry_chain")
        rows_eic = c.fetchone()["n"]
    conn.close()
    # gkx 侧企业总量与深圳口径（对照 KPI）
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info")
    out["facts"]["org_total"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE city LIKE %s", ("%深圳%",))
    out["facts"]["org_sz"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT industry_code) FROM gkx.dwd_org_industry_tags
                   WHERE industry_code IS NOT NULL AND industry_code <> ''""")
    out["facts"]["org_tag_codes"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_industry_tags WHERE industry_code LIKE '%INB%'")
    out["facts"]["org_tag_inb_rows"] = int(cur.fetchone()[0])
    # industry_tags 无 org_id：以 company_name 关联机构主表去重
    cur.execute("""SELECT COUNT(DISTINCT b.org_id) FROM gkx.dwd_org_industry_tags t
                   JOIN gkx.dwd_org_base_info b ON t.company_name COLLATE utf8mb4_general_ci = b.name_cn COLLATE utf8mb4_general_ci
                   WHERE t.industry_code LIKE '%INB%'""")
    out["facts"]["org_tag_inb_orgs"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT b.org_id) FROM gkx.dwd_org_industry_tags t
                   JOIN gkx.dwd_org_base_info b ON t.company_name COLLATE utf8mb4_general_ci = b.name_cn COLLATE utf8mb4_general_ci
                   WHERE t.industry_code LIKE '%INB%' AND b.city LIKE '%深圳%'""")
    out["facts"]["org_tag_inb_orgs_sz"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "产业集群企业数量两段承载：①live 挂接表（chain_enterprise / enterprise_industry_chain）实测 "
        + str(rows_eic) + " 行（空表待灌）；②gkx 标签替代口径实测（dwd_org_industry_tags 含 INB 码行 "
        + str(out["facts"]["org_tag_inb_rows"]) + " 行——industry_code 为 JSON 数组字符串，LIKE '%INB%' 匹配——关联企业 "
        + str(out["facts"]["org_tag_inb_orgs"]) + " 家（深圳 " + str(out["facts"]["org_tag_inb_orgs_sz"]) + " 家）"
        + "）——12 链产业群企业计数可走标签面落地，与 UI 的链树口径待对齐 → 部分支持。"
        "升档触发器：chain_enterprise 灌数（12 链 ods_sync 真源）。")
    p = os.path.join(HERE, "out", "M_ENT_UI_CLUSTER_COUNT_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| eic:", out["facts"]["eic_rows"], "| tag INB orgs:", out["facts"]["org_tag_inb_orgs"])


if __name__ == "__main__":
    main()
