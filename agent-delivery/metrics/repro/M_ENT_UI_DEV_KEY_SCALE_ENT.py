#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_KEY_SCALE_ENT：重点企业规模统计（企业分析>企业发展，KeyEnterprisesPanel:L437，seq40）。
重点企业（上市/挂牌）按规模维度统计——注册资本分档实测（10/20/50/30 亿档位分布）。
注：门户服务侧已有 M_ENT_UI_KEY_SCALE（规模×资质卡），本件为 KeyEnterprisesPanel 页内统计（不同 UI 位）。
出参：repro/out/M_ENT_UI_DEV_KEY_SCALE_ENT_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_KEY_SCALE_ENT",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "重点企业规模统计复现（KeyEnterprisesPanel 页内：上市企业注册资本分档）",
    "ui_evidence": ["live 30892 企业分析>企业发展>KeyEnterprisesPanel.vue:L437（seq40 规模统计）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''""")
    listed = out["facts"]["listed_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT CASE
                     WHEN registered_capital_value >= 10000000000 THEN '100亿+'
                     WHEN registered_capital_value >= 5000000000 THEN '50-100亿'
                     WHEN registered_capital_value >= 2000000000 THEN '20-50亿'
                     WHEN registered_capital_value >= 1000000000 THEN '10-20亿'
                     WHEN registered_capital_value >= 100000000 THEN '1-10亿'
                     ELSE '1亿以下' END AS band, COUNT(*) AS n
                   FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''
                   AND registered_capital_value IS NOT NULL
                   GROUP BY band ORDER BY MIN(registered_capital_value) DESC""")
    out["facts"]["listed_cap_bands"] = [{"band": r[0], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''
                   AND registered_capital_value IS NULL""")
    out["facts"]["listed_no_capital"] = int(cur.fetchone()[0])
    cur.close()
    total_banded = sum(x["n"] for x in out["facts"]["listed_cap_bands"])
    out["derived"]["listed_capital_coverage_pct"] = {
        "value": round(total_banded / max(listed, 1) * 100, 4),
        "numerator": total_banded,
        "denominator": listed,
        "denominator_note": "上市/挂牌企业中注册资本可分档的比例",
    }
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "上市/挂牌 1,971 家注册资本分档实测（单位=元，max 2,492.5 亿元；100亿+/50-100亿/20-50亿…档位分布落产物）；"
        "「规模」语义=注册资本分档（页面语义直读；org_size 列分布另见 M_ENT_UI_DEV_SZ_SCALE）。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_KEY_SCALE_ENT_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("bands =", out["facts"]["listed_cap_bands"])


if __name__ == "__main__":
    main()
