#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_LATEST_LIST：政策扶持·最新政策动态·最新发布政策列表（seq176）复现件。
最新发布政策 Top 实测（按 publish_date 倒序）。
出参：repro/out/M_POL_UI_LATEST_LIST_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_LATEST_LIST",
    "batch": "TOPIC-UI-GAP-L01 批6",
    "probe_date": "2026-11-05",
    "purpose": "最新发布政策列表承载实测",
    "ui_evidence": ["seq176 最新政策动态 tab 列表（政策扶持）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT title, publish_date, ministry, `rank` FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL
                   ORDER BY publish_date DESC LIMIT 10""")
    out["facts"]["latest_top10"] = [
        {"t": str(r[0])[:40], "d": str(r[1]), "m": str(r[2])[:16], "rank": str(r[3])[:14]}
        for r in cur.fetchall()]
    cur.execute("SELECT MAX(publish_date) FROM gkx.dwd_policy_base")
    out["facts"]["latest_date"] = str(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base
                   WHERE publish_date >= '2022-01-01'""")
    out["facts"]["policy_2022_plus"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "列表链路可复现（按 publish_date 倒序 Top10 落产物，库内最新 " + out["facts"]["latest_date"] + "）；"
        "但 2022 后源断更（2022+ 仅 " + str(out["facts"]["policy_2022_plus"]) + " 条）——「最新」语义失真（2022 后无新政策入库）"
        "→ 部分支持。升档触发器：政策源恢复更新（ods_sync append）。")
    p = os.path.join(HERE, "out", "M_POL_UI_LATEST_LIST_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| latest:", out["facts"]["latest_date"], "| 2022+:", out["facts"]["policy_2022_plus"])


if __name__ == "__main__":
    main()
