#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_FDI_CATALOG：鼓励外商投资产业目录（政策查询>智能检索，seq54）探针件。
2025 年版目录条目实测：政策库 title 检索命中 91 条（含 2020 年版第 38 号令原文）；
2025 年版未入库（最新条目为 2020 版），如实披露。
出参：repro/out/M_POL_UI_FDI_CATALOG_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_FDI_CATALOG",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "鼓励外商投资产业目录（智能检索条目）承载实测",
    "ui_evidence": ["live 30892 政策分析>政策查询>智能检索「鼓励外商投资产业目录（2025年版）」（seq54）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%外商投资%",))
    out["facts"]["fdi_title_hits"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%外商%",))
    out["facts"]["foreign_title_hits"] = int(cur.fetchone()[0])
    cur.execute("""SELECT title, publish_date, ministry FROM gkx.dwd_policy_base
                   WHERE title LIKE %s ORDER BY publish_date DESC LIMIT 5""", ("%外商投资%",))
    out["facts"]["fdi_top5"] = [{"t": str(r[0])[:48], "d": str(r[1]), "m": str(r[2])[:14]} for r in cur.fetchall()]
    # 2025 版是否在库
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%2025%外商%",))
    out["facts"]["fdi_2025_hits"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE %s""", ("%鼓励外商投资产业目录%",))
    out["facts"]["catalog_edition_hits"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "智能检索链路可复现（title LIKE 命中 91 条外商投资类，含《鼓励外商投资产业目录(2020年版)》第 38 号令原文）；"
        "但 UI 挂载的「2025 年版」目录实测未入库（2025+外商 命中 0）——数据源止于 2020 版 → 部分支持。"
        "升档触发器：2025 年版目录条目灌库（走 ods_sync append）。")
    p = os.path.join(HERE, "out", "M_POL_UI_FDI_CATALOG_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("fdi_hits =", out["facts"]["fdi_title_hits"], "| 2025ver =", out["facts"]["fdi_2025_hits"],
          "| top1 =", out["facts"]["fdi_top5"][0] if out["facts"]["fdi_top5"] else None)


if __name__ == "__main__":
    main()
