#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_UI_CYCLE_INFLECTION：潜在拐点（产业周期分析>分析结果，seq45）。
拐点=多信号时序变化率符号翻转检测（融资/政策/专利序列的斜率变号点）。实测：融资/政策序列在，
专利聚合受限（如实披露）；拐点检测规则 UI 未给，按序列斜率变号法实现并披露。
出参：repro/out/M_CHAIN_UI_CYCLE_INFLECTION_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_CHAIN_UI_CYCLE_INFLECTION",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "潜在拐点复现（融资/政策时序斜率变号检测；方法=一阶差分符号翻转）",
    "ui_evidence": ["live 30892 产业链分析>产业周期分析>分析结果>潜在拐点（seq45，交互态）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("""SELECT SUBSTRING(CAST(completion_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_org_financing_info
                   WHERE completion_date IS NOT NULL AND year(completion_date) BETWEEN 2012 AND 2026
                   GROUP BY y ORDER BY y""")
    fin = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL AND year(publish_date) BETWEEN 2012 AND 2026
                   GROUP BY y ORDER BY y""")
    pol = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    cur.close()
    out["facts"]["financing_2012_2026"] = fin
    out["facts"]["policy_2012_2026"] = pol

    def inflections(series):
        pts = []
        for i in range(1, len(series) - 1):
            d0 = series[i]["n"] - series[i - 1]["n"]
            d1 = series[i + 1]["n"] - series[i]["n"]
            if d0 * d1 < 0:
                pts.append({"year": series[i]["y"], "type": "峰" if d0 > 0 else "谷",
                            "n": series[i]["n"]})
        return pts

    out["derived"]["financing_inflections"] = {
        "value": inflections(fin),
        "numerator": len(inflections(fin)),
        "denominator": len(fin),
        "denominator_note": "融资序列一阶差分符号翻转点（拐点检测法：一阶差分变号）",
    }
    out["derived"]["policy_inflections"] = {
        "value": inflections(pol),
        "numerator": len(inflections(pol)),
        "denominator": len(pol),
        "denominator_note": "政策序列一阶差分符号翻转点",
    }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "融资/政策两路信号拐点实测落产物（变号点逐年标峰/谷）；专利路聚合受限（294 万行压连）缺第三路信号；"
        "「拐点」判定规则 UI 未给——本件按通行的一阶差分符号翻转法实现并披露，非甲方闭合口径 → 部分支持。"
        "升档触发器：甲方给出拐点规则（或确认差分法）+ 专利时序离线聚合补齐。")
    p = os.path.join(HERE, "out", "M_CHAIN_UI_CYCLE_INFLECTION_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("fin_inflections =", out["derived"]["financing_inflections"]["value"])


if __name__ == "__main__":
    main()
