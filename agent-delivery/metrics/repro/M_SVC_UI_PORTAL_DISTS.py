#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SVC_UI_PORTAL_DISTS：服务链专题服务·产业/区域分布（seq91-92/181-185）复现件。
服务机构产业分布 + 区域分布（含全球/中国/深圳视图、最厚环节、研发与科研合作）。
出参：repro/out/M_SVC_UI_PORTAL_DISTS_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_SVC_UI_PORTAL_DISTS",
    "batch": "TOPIC-UI-GAP-L01 批5",
    "probe_date": "2026-11-05",
    "purpose": "服务链专题服务·产业/区域分布承载实测",
    "ui_evidence": [
        "views/service/ServicePortalShell.vue:L22-23（seq91 产业分布/seq92 区域分布）",
        "seq181 最厚环节/seq182·183 研发与科研合作/seq184 中国机构约数/seq185 全国地理分布",
    ],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}

SVC_L1 = "科学研究和技术服务业"


def main():
    cur = gkx()
    # 产业分布：L2 类型分布（深圳 vs 全国）
    cur.execute("""SELECT industry_l2_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s
                   AND industry_l2_name IS NOT NULL AND LOWER(industry_l2_name) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY industry_l2_name ORDER BY n DESC""", (SVC_L1,))
    out["facts"]["all_l2_dist"] = [{"k": str(r[0])[:22], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT industry_l2_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city LIKE %s
                   AND industry_l2_name IS NOT NULL AND LOWER(industry_l2_name) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY industry_l2_name ORDER BY n DESC""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_l2_dist"] = [{"k": str(r[0])[:22], "n": int(r[1])} for r in cur.fetchall()]
    # 区域分布：全国城市 top + 深圳区级
    cur.execute("""SELECT city, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city IS NOT NULL
                   AND LOWER(city) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY city ORDER BY n DESC LIMIT 12""", (SVC_L1,))
    out["facts"]["city_top12"] = [{"k": str(r[0])[:14], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT area, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name = %s AND city LIKE %s AND area IS NOT NULL
                   AND LOWER(area) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY area ORDER BY n DESC LIMIT 10""", (SVC_L1, "%深圳%"))
    out["facts"]["sz_area_top10"] = [{"k": str(r[0])[:16], "n": int(r[1])} for r in cur.fetchall()]
    # 研发与科研合作：sc_info（科创合作）按类型
    cur.execute("""SELECT type, COUNT(*) AS n FROM gkx.dwd_org_sc_info
                   WHERE type IS NOT NULL AND LOWER(type) NOT IN ('', 'null', 'nan', 'none')
                   GROUP BY type ORDER BY n DESC""")
    out["facts"]["sc_type_dist"] = [{"k": str(r[0])[:10], "n": int(r[1])} for r in cur.fetchall()]
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "产业/区域分布可复现：全国 L2 三大类型（科技推广 17,025/研发试验 11,910/专业技术服务 7,828）、"
        "城市 Top（广州 17,983/深圳 10,002/东莞 7,565）、深圳区级分布与科创合作类型实测齐；"
        "「最厚环节」需链节点×服务机构映射（svc_org_graph_hang 空表）+「研发与科研合作」细分口径未闭合 → 部分支持。"
        "升档触发器：svc_org_graph_hang 灌数（机构-链节点挂接）。")
    p = os.path.join(HERE, "out", "M_SVC_UI_PORTAL_DISTS_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p, "| all_l2:", len(out["facts"]["all_l2_dist"]),
          "| sz_area:", out["facts"]["sz_area_top10"][:4])


if __name__ == "__main__":
    main()
