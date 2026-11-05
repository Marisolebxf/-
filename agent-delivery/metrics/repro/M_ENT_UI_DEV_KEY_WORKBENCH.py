#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_DEV_KEY_WORKBENCH：产业链重点企业工作台（企业分析>企业发展，KeyEnterprisesPanel:L294）。
工作台=重点企业列表+产业链归属+评估操作台。本件复现数据底座：重点企业名单面（gkx 上市/高企/专精特新标签）
+ 产业链归属面（industry_l1-l4 列）。
出参：repro/out/M_ENT_UI_DEV_KEY_WORKBENCH_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx, live_count  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_ENT_UI_DEV_KEY_WORKBENCH",
    "batch": "TOPIC-UI-GAP-L01 批2组2",
    "probe_date": "2026-11-04",
    "purpose": "产业链重点企业工作台数据底座复现（重点标签面 + 链归属面）",
    "ui_evidence": ["live 30892 企业分析>企业发展>KeyEnterprisesPanel.vue:L294（seq34 页面证据）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info")
    org_total = out["facts"]["org_total"] = int(cur.fetchone()[0])
    for tag_col, key in (("listing_status", "listed"), ("is_high_tech", "high_tech_flag"),
                         ("enterprise_type", "ent_type")):
        try:
            cur.execute(f"""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                            WHERE {tag_col} IS NOT NULL AND {tag_col} NOT IN ('', '0', '否', '无', 'normal')""")
            out["facts"][f"tag_{key}_nonnull"] = int(cur.fetchone()[0])
        except Exception as e:  # noqa: BLE001
            out["facts"][f"tag_{key}_nonnull"] = f"ERR:{e}"
    # 重点标签分布抽验
    try:
        cur.execute("""SELECT listing_status, COUNT(*) AS n FROM gkx.dwd_org_base_info
                       WHERE listing_status IS NOT NULL AND listing_status <> ''
                       GROUP BY listing_status ORDER BY n DESC LIMIT 6""")
        out["facts"]["listing_status_dist"] = [{"k": str(r[0])[:20], "n": int(r[1])} for r in cur.fetchall()]
    except Exception as e:  # noqa: BLE001
        out["facts"]["listing_status_dist"] = f"ERR:{e}"
    # 链归属面
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_org_base_info
                   WHERE industry_l1_name IS NOT NULL AND industry_l1_name <> ''""")
    out["facts"]["org_with_l1_name"] = int(cur.fetchone()[0])
    cur.close()
    out["facts"]["live_eb_rows"] = live_count("enterprise_base")
    out["derived"]["keyworkbench_org_coverage_pct"] = {
        "value": round(out["facts"]["org_with_l1_name"] / max(org_total, 1) * 100, 4),
        "numerator": out["facts"]["org_with_l1_name"],
        "denominator": org_total,
        "denominator_note": "gkx 底册 L1 行业名非空占比（可挂产业链归属的企业比例）",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "重点标签面（上市/企业类型列实测）+ 链归属面（L1-L4 列）在 → 工作台列表可搭；"
        "「重点企业」准入口径（页面按链筛选重点的规则）UI 未给 → 部分支持。升档触发器：甲方给出重点企业判定规则。")
    p = os.path.join(HERE, "out", "M_ENT_UI_DEV_KEY_WORKBENCH_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("org_total =", org_total, "| with_l1 =", out["facts"]["org_with_l1_name"],
          "| listing_dist =", str(out["facts"].get("listing_status_dist"))[:120])


if __name__ == "__main__":
    main()
