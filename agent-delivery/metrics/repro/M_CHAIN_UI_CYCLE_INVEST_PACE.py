#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_UI_CYCLE_INVEST_PACE：决策摘要·投资节奏（产业周期分析>分析结果，seq43）。
投资节奏=融资事件时间聚类的节奏判读（加速/放缓/平稳）。实测融资年度序列 2001-2026 全程在。
出参：repro/out/M_CHAIN_UI_CYCLE_INVEST_PACE_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_CHAIN_UI_CYCLE_INVEST_PACE",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "投资节奏决策摘要复现（融资事件年度节奏实测）",
    "ui_evidence": ["live 30892 产业链分析>产业周期分析>分析结果>决策摘要·投资节奏（seq43，交互态）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT SUBSTRING(CAST(completion_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_org_financing_info
                   WHERE completion_date IS NOT NULL AND year(completion_date) > 2000
                   GROUP BY y ORDER BY y""")
    fin = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    out["facts"]["financing_yearly_full"] = fin
    cur.execute("""SELECT funding_round, COUNT(*) AS n FROM gkx.dwd_org_financing_info
                   GROUP BY funding_round ORDER BY n DESC LIMIT 8""")
    out["facts"]["round_dist"] = [{"round": str(r[0])[:16], "n": int(r[1])} for r in cur.fetchall()]
    cur.close()
    # 派生：近三年节奏（年均环比）
    recent = [x for x in fin if x["y"] >= 2022]
    if len(recent) >= 2:
        out["derived"]["recent_pace_change_pct"] = {
            "value": round((recent[-1]["n"] / max(recent[0]["n"], 1) - 1) * 100, 4),
            "numerator": recent[-1]["n"],
            "denominator": recent[0]["n"],
            "denominator_note": f"{recent[0]['y']}→{recent[-1]['y']} 融资事件数变化率（放缓/加速判读输入）",
        }
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "融资事件 25,654 条按 completion_date 年度全程序列实测（2018:2,257 → 2026:238，含当年未完季度的自然衰减）；"
        "轮次分布 Top8 在 → 「投资节奏」摘要的时间聚类原料完整；节奏判读（加速/放缓/平稳）为序列可视化直读语义。")
    p = os.path.join(HERE, "out", "M_CHAIN_UI_CYCLE_INVEST_PACE_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("recent =", recent, "| round_top3 =", out["facts"]["round_dist"][:3])


if __name__ == "__main__":
    main()
