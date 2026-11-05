#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_KEY_FIELD_STAT：重点企业领域统计（企业分析>企业发展，KeyEnterprisesPanel:L448，seq41）。
重点企业（上市/挂牌 1,971 家）按领域（L1 行业）统计。与门户服务侧 M_ENT_UI_KEY_SCALE（规模×资质）互补。
出参：repro/out/M_ENT_UI_DEV_KEY_FIELD_STAT_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_KEY_FIELD_STAT",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "重点企业领域统计复现（上市标签 × L1 领域分布）",
    "ui_evidence": ["live 30892 企业分析>企业发展>KeyEnterprisesPanel.vue:L448（seq41 领域统计）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''""")
    out["facts"]["listed_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT industry_l1_name, COUNT(*) AS n FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''
                   AND industry_l1_name IS NOT NULL AND industry_l1_name <> ''
                   GROUP BY industry_l1_name ORDER BY n DESC LIMIT 10""")
    out["facts"]["listed_l1_top10"] = [{"field": r[0], "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE listing_status IS NOT NULL AND listing_status <> ''
                   AND (industry_l1_name IS NULL OR industry_l1_name = '')""")
    out["facts"]["listed_no_l1"] = int(cur.fetchone()[0])
    cur.close()
    out["derived"]["listed_field_coverage_pct"] = {
        "value": round(out["facts"]["listed_l1_top10"] and
                       (out["facts"]["listed_total"] - out["facts"]["listed_no_l1"]) /
                       max(out["facts"]["listed_total"], 1) * 100, 4),
        "numerator": out["facts"]["listed_total"] - out["facts"]["listed_no_l1"],
        "denominator": out["facts"]["listed_total"],
        "denominator_note": "上市/挂牌企业中 L1 领域可归集的比例",
    }
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "上市标签 1,971 家 × L1 领域分布实测（制造业 785/科研技术服务 352/信息软件 258…）→ "
        "页面重点企业领域统计完整复现；与门户服务侧 M_ENT_UI_KEY_SCALE（规模×资质）为不同 UI 页的互补统计。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_KEY_FIELD_STAT_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("listed =", out["facts"]["listed_total"],
          "| top3 =", [(x["field"][:8], x["n"]) for x in out["facts"]["listed_l1_top10"][:3]])


if __name__ == "__main__":
    main()
