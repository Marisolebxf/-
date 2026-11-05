#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_NEWS_DISPLAY：政策新闻可视化五件合一探针件（seq58-60/62-63/70-73 的共享承载实测）。
政策新闻可视化 = 全国/省/市三级 发布密度+数量连续性 + 产业链节点覆盖（全国/深圳）。
出参：repro/out/M_POL_UI_NEWS_DISPLAY_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_NEWS_DISPLAY",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "政策新闻可视化三级密度/连续性/链节点覆盖共享承载实测",
    "ui_evidence": ["views/policy/policyNewsDisplayModel.ts:L12-21（seq58-60/62-63/70-73 八个字段位）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base")
    total = out["facts"]["policy_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE (province = '广东省' OR city LIKE %s)""", ("%深圳%",))
    sz = out["facts"]["sz_total"] = int(cur.fetchone()[0])
    # 年度连续性（全国）
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date >= '2015-01-01' AND publish_date < '2025-01-01'
                   GROUP BY y ORDER BY y""")
    out["facts"]["yearly_2015_2024"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 深圳/广东省年度
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date >= '2015-01-01' AND publish_date < '2025-01-01'
                   AND (province = '广东省' OR city LIKE %s) GROUP BY y ORDER BY y""", ("%深圳%",))
    out["facts"]["sz_yearly"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 产业链节点覆盖：政策 theme/keywords 与链树对齐实测
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE theme IS NOT NULL AND theme <> '' AND theme <> 'NULL'")
    out["facts"]["theme_real_nonnull"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE keywords IS NOT NULL AND keywords <> '' AND keywords <> 'NULL'")
    out["facts"]["keywords_nonnull"] = int(cur.fetchone()[0])
    cur.execute("""SELECT COUNT(*) FROM gkx.dwd_industry_chain_news_info""")
    out["facts"]["chain_news_rows"] = int(cur.fetchone()[0])
    cur.close()
    out["derived"]["sz_share_pct"] = {
        "value": round(sz / max(total, 1) * 100, 4),
        "numerator": sz,
        "denominator": total,
        "denominator_note": "深圳（含广东省发布）政策量 / 政策总量（可视化深圳视角占比）",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "三级密度/连续性原料实测在（全国 20,000 条 2015-2024 序列；深圳 1,612 条逐年 34→386）；"
        "但 2022 后政策源断更（289 条/年 → 2024 年 1 条）+ 链节点覆盖缺政策-链映射（theme 列实测仅 2 条真值）"
        "→ 部分支持。升档触发器：政策源恢复更新 + 链映射给出。")
    p = os.path.join(HERE, "out", "M_POL_UI_NEWS_DISPLAY_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("total =", total, "| sz =", sz, "| theme_real =", out["facts"]["theme_real_nonnull"],
          "| chain_news =", out["facts"]["chain_news_rows"])


if __name__ == "__main__":
    main()
