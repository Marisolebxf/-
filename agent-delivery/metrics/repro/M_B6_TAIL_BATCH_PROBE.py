#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_B6_TAIL_BATCH_PROBE：批6尾部缺口探针（seq156/168-173/176/187-202）。
三源：gkx（企业/政策/图谱原料）+ live（图谱挂面）+ 久新（产业全景/机构）。
出参：repro/out/M_B6_TAIL_BATCH_PROBE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_B6_TAIL_BATCH_PROBE",
    "batch": "TOPIC-UI-GAP-L01 批6",
    "probe_date": "2026-11-05",
    "purpose": "尾部缺口（seq156/168-173/176/187-202）三源探针",
    "facts": {},
    "derived": {},
    "notes": [],
}


def main():
    cur = gkx()
    # seq156 产业集群企业数量：产业群口径（12 链 INB12xx-25xx）企业挂接
    cur.execute("SHOW TABLES FROM gkx LIKE 'dwd_chain%'")
    chain_tabs = [r[0] for r in cur.fetchall()]
    out["facts"]["chain_tabs"] = chain_tabs[:20]
    print("chain_tabs:", chain_tabs[:20])
    # 产业集群企业映射表候选
    for t in chain_tabs:
        if "enterprise" in t or "company" in t or "org" in t:
            cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
            out["facts"].setdefault("chain_ent_rows", {})[t] = int(cur.fetchone()[0])
    # seq168-169/171-172 投融资事件数/总额（产业口径）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_financing_info")
    out["facts"]["financing_rows"] = int(cur.fetchone()[0])
    cur.execute("""SELECT SUM(funding_amount) FROM gkx.dwd_org_financing_info
                   WHERE funding_amount IS NOT NULL""")
    out["facts"]["financing_amount_sum_raw"] = None
    try:
        v = cur.fetchone()[0]
        out["facts"]["financing_amount_sum_raw"] = float(v) if v is not None else None
    except Exception:  # noqa: BLE001
        pass
    # seq176 最新发布政策列表
    cur.execute("""SELECT title, publish_date FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL ORDER BY publish_date DESC LIMIT 5""")
    out["facts"]["latest_policy_top5"] = [{"t": str(r[0])[:40], "d": str(r[1])} for r in cur.fetchall()]
    # seq173 产业链全景（零部件链样例）：链树表
    cur.execute("SHOW TABLES FROM gkx LIKE '%chain_tree%'")
    out["facts"]["chain_tree_tabs"] = [r[0] for r in cur.fetchall()]
    cur.execute("SHOW TABLES FROM gkx LIKE '%industry_chain%'")
    ic_tabs = [r[0] for r in cur.fetchall()]
    out["facts"]["industry_chain_tabs"] = ic_tabs[:16]
    print("ic_tabs:", ic_tabs[:16])
    for t in ic_tabs[:8]:
        cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
        out["facts"].setdefault("ic_rows", {})[t] = int(cur.fetchone()[0])
    cur.close()
    # seq190 产业链图谱（CMS）：live 图谱挂面
    conn = live("DWD")
    with conn.cursor() as c:
        c.execute("""SELECT table_name FROM information_schema.tables
                     WHERE table_schema='gkxlumenx_dwd' AND table_name LIKE '%%graph%%'""")
        gtabs = [list(r.values())[0] for r in c.fetchall()]
        out["facts"]["live_graph_tabs"] = gtabs[:12]
    conn.close()
    p = os.path.join(HERE, "out", "M_B6_TAIL_BATCH_PROBE_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| financing:", out["facts"]["financing_rows"],
          "| ic_rows:", out["facts"].get("ic_rows"))


if __name__ == "__main__":
    main()
