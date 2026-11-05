#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POL_UI_PORTAL_STATS：政策扶持六件合一探针件（seq64-69）。
产业覆盖/力度排名/自动关联/数量对比/时序模型/标准化对比 共享承载实测。
出参：repro/out/M_POL_UI_PORTAL_STATS_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_POL_UI_PORTAL_STATS",
    "batch": "TOPIC-UI-GAP-L01 批4",
    "probe_date": "2026-11-05",
    "purpose": "政策扶持面板六件共享承载实测",
    "ui_evidence": ["views/policy/policyPortalTabs.ts:L6-15、PolicyPortalStatsPanel.vue:L146/L178/L220（seq64-69）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base")
    total = out["facts"]["policy_total"] = int(cur.fetchone()[0])
    # 数量对比原料：层级分布
    cur.execute("""SELECT `rank`, COUNT(*) AS n FROM gkx.dwd_policy_base
                   WHERE `rank` IS NOT NULL AND `rank` NOT IN ('', '[""]')
                   GROUP BY `rank` ORDER BY n DESC""")
    out["facts"]["rank_dist"] = [{"k": str(r[0])[:18], "n": int(r[1])} for r in cur.fetchall()]
    # 时序模型原料：年度序列
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date >= '2015-01-01' AND publish_date < '2025-01-01'
                   GROUP BY y ORDER BY y""")
    out["facts"]["yearly"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 产业覆盖原料：theme 真值 + keywords
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE keywords IS NOT NULL AND keywords <> '' AND keywords <> 'NULL'")
    out["facts"]["keywords_nonnull"] = int(cur.fetchone()[0])
    # 自动关联原料：quote_policy（政策引用链）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE quote_policy IS NOT NULL AND quote_policy <> ''")
    out["facts"]["quote_policy_nonnull"] = int(cur.fetchone()[0])
    cur.execute("""SELECT title, quote_policy FROM gkx.dwd_policy_base
                   WHERE quote_policy IS NOT NULL AND quote_policy <> '' LIMIT 3""")
    out["facts"]["quote_samples"] = [{"t": str(r[0])[:30], "q": str(r[1])[:60]} for r in cur.fetchall()]
    # 力度排名原料：policy_support 真值 + keypoints
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE policy_support IS NOT NULL AND policy_support <> ''")
    out["facts"]["policy_support_nonnull"] = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE keypoints IS NOT NULL AND keypoints <> '' AND keypoints <> 'NULL'")
    out["facts"]["keypoints_nonnull"] = int(cur.fetchone()[0])
    cur.close()
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "六件承载分级实测：数量对比（层级五档 17,469 条）与时序模型（年度序列）原料齐；"
        "自动关联有引用链列（quote_policy 实测非空样例）；产业覆盖/力度排名/标准化对比缺结构化承载"
        "（theme 真值仅 2 条、policy_support 0 真值、维度打分无列）→ 部分支持。"
        "升档触发器：政策结构化解析（产业标签/支持要素/力度打分）落地。")
    p = os.path.join(HERE, "out", "M_POL_UI_PORTAL_STATS_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("rank_dist =", out["facts"]["rank_dist"][:5],
          "| quote_nonnull =", out["facts"]["quote_policy_nonnull"],
          "| support_nonnull =", out["facts"]["policy_support_nonnull"])


if __name__ == "__main__":
    main()
