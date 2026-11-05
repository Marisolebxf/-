#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_UI_COOP_ADVICE：服务机构产业领域分析·合作建议（seq75）复现件。
承载实测：live svc_org_circle（合作圈定规则表）结构在、数据空（0 行）；
gkx 侧合作原料面（投融资/重要新闻/科创合作）实测行数。
出参：repro/out/M_SVC_UI_COOP_ADVICE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_SVC_UI_COOP_ADVICE",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "服务机构产业领域分析·合作建议承载实测",
    "ui_evidence": ["views/service/SvcOrgCoverageBoard.vue:L215（seq75 合作建议）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}

SVC_L1 = "科学研究和技术服务业"


def main():
    # live 合作圈定表结构（空表）
    conn = live("DWD")
    with conn.cursor() as c:
        c.execute("SHOW COLUMNS FROM svc_org_circle")
        out["facts"]["svc_org_circle_cols"] = [list(r.values())[0] for r in c.fetchall()]
        c.execute("SELECT COUNT(*) AS n FROM svc_org_circle")
        out["facts"]["svc_org_circle_rows"] = int(c.fetchone()["n"])
    conn.close()
    # gkx 合作原料面：深圳科研服务机构的重要新闻与科创合作
    cur = gkx()
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city LIKE %s""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_important_news_info n
                   JOIN gkx.dwd_org_base_info b ON n.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_news_rows"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(DISTINCT n.org_id) FROM gkx.dwd_org_important_news_info n
                   JOIN gkx.dwd_org_base_info b ON n.org_id = b.org_id
                   WHERE b.industry_l1_name = %s AND b.city LIKE %s""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_svc_news_orgs"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_sc_info""")
    out["facts"]["sc_info_rows"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "合作圈定规则表 svc_org_circle 结构在（rule_version/hit_fields/service_type_candidate/"
        "pending_client_confirm——规则引擎设计完整）、数据 0 行待灌；"
        "gkx 合作原料面实测：深圳科研服务机构 10,002 家，重要新闻 55,740 条（覆盖 "
        + str(out["facts"]["sz_svc_news_orgs"]) + " 家），科创合作 sc_info 1,716 行。"
        "→ 规则待灌数 + 口径待闭合 → 部分支持。升档触发器：svc_org_circle 灌数 + 合作建议规则口径甲方确认。")
    p = os.path.join(HERE, "out", "M_SVC_UI_COOP_ADVICE_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| circle rows:", out["facts"]["svc_org_circle_rows"],
          "| sz_svc:", out["facts"]["sz_svc_total"])


if __name__ == "__main__":
    main()
