#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_UI_CYCLE_DRIVER：关键驱动因素（产业链分析>产业周期分析>分析结果，seq42）。
周期驱动因素=专利/融资/政策/新闻四类时序信号的变化率因子。实测：融资年度序列在（25,654 事件 2001-2026）、
政策年度序列在（38 年 20,000 条）；专利时序聚合受限（294 万行压连，如实披露）。
出参：repro/out/M_CHAIN_UI_CYCLE_DRIVER_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_CHAIN_UI_CYCLE_DRIVER",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "产业周期关键驱动因素复现（四类时序信号面探针）",
    "ui_evidence": ["live 30892 产业链分析>产业周期分析>分析结果>关键驱动因素（seq42，交互态）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    # 融资时序（驱动因子1：资本面）
    cur.execute("""SELECT SUBSTRING(CAST(completion_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_org_financing_info
                   WHERE completion_date IS NOT NULL AND year(completion_date) > 2000
                   GROUP BY y ORDER BY y""")
    fin = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    out["facts"]["financing_yearly"] = fin[-12:]
    # 政策时序（驱动因子2：政策面）
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL AND year(publish_date) >= 2015
                   GROUP BY y ORDER BY y""")
    out["facts"]["policy_yearly_2015"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    # 新闻面（驱动因子3：热度面）
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_important_news_info")
    out["facts"]["important_news_rows"] = int(cur.fetchone()[0])
    cur.close()
    # 派生：融资近5年增速（周期上/下行信号代理）
    recent = [x for x in fin if x["y"] >= 2021]
    if len(recent) >= 2:
        growth = round((recent[-1]["n"] / max(recent[0]["n"], 1) - 1) * 100, 4)
        out["derived"]["financing_2021_to_latest_growth_pct"] = {
            "value": growth,
            "numerator": recent[-1]["n"],
            "denominator": recent[0]["n"],
            "denominator_note": f"融资事件 {recent[0]['y']}→{recent[-1]['y']} 变化率（资本面周期信号代理）",
        }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "四类驱动信号面三在一体：融资年度序列（2001-2026 全程）、政策年度序列（2015-2021 密集，2022 起骤降如实）、"
        "重要新闻 166.8 万行；专利时序聚合两次压断连接（294 万行，gkx 读负载限）如实披露；"
        "「驱动因素→周期阶段」的归因规则 UI 未给 → 部分支持。升档触发器：甲方给出驱动归因规则（或专利时序离线聚合后补齐）。")
    p = os.path.join(HERE, "out", "M_CHAIN_UI_CYCLE_DRIVER_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("fin_tail =", fin[-5:], "| policy =", out["facts"]["policy_yearly_2015"][:5])


if __name__ == "__main__":
    main()
