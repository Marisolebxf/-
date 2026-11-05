#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_UI_CYCLE_POLICY_WINDOW：决策摘要·政策窗口期（产业周期分析>分析结果，seq44）。
政策窗口期=政策发布强度的时序峰谷判读（窗口开启/关闭）。实测政策年度序列 2015-2021（20,000 条主表）。
出参：repro/out/M_CHAIN_UI_CYCLE_POLICY_WINDOW_out.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gkxdb import gkx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {
    "metric_id": "M_CHAIN_UI_CYCLE_POLICY_WINDOW",
    "batch": "TOPIC-UI-GAP-L01 批3",
    "probe_date": "2026-11-04",
    "purpose": "政策窗口期决策摘要复现（政策发布时序峰谷实测）",
    "ui_evidence": ["live 30892 产业链分析>产业周期分析>分析结果>决策摘要·政策窗口期（seq44，交互态）"],
    "facts": {},
    "derived": {},
    "notes": [],
    "support_judgment": None,
}


def main():
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_policy_base")
    out["facts"]["policy_total"] = int(cur.fetchone()[0])
    cur.execute("""SELECT SUBSTRING(CAST(publish_date AS CHAR),1,4) AS y, COUNT(*) AS n
                   FROM gkx.dwd_policy_base
                   WHERE publish_date IS NOT NULL AND year(publish_date) >= 2000
                   GROUP BY y ORDER BY y""")
    out["facts"]["policy_yearly_2000"] = [{"y": int(r[0]), "n": int(r[1])} for r in cur.fetchall()]
    cur.execute("SHOW COLUMNS FROM gkx.dwd_policy_base")
    out["facts"]["policy_cols"] = [r[0] for r in cur.fetchall()][:22]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")
    out["facts"]["global_policy_rows"] = int(cur.fetchone()[0])
    cur.close()
    # 派生：峰年识别
    py = [x for x in out["facts"]["policy_yearly_2000"] if x["y"] >= 2015]
    if py:
        peak = max(py, key=lambda x: x["n"])
        out["derived"]["policy_peak_year"] = {
            "value": peak["y"],
            "numerator": peak["n"],
            "denominator": sum(x["n"] for x in py),
            "denominator_note": f"2015+ 峰年 {peak['y']}（{peak['n']} 条）占 2015+ 总量比例——窗口强度判读输入",
        }
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "政策发布时序实测：2015-2021 年均 1,261-2,402 条（2020 峰值 2,402），2022 起骤降至 289 条——"
        "时序面完整可判读；但「政策窗口期」的链级语义（哪个产业的窗口）需政策-产业链映射，"
        "且 2022 后政策源断更（数据源采集停更如实披露）→ 部分支持。升档触发器：政策源恢复更新 + 链映射给出。")
    p = os.path.join(HERE, "out", "M_CHAIN_UI_CYCLE_POLICY_WINDOW_out.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("saved", p)
    print("policy_total =", out["facts"]["policy_total"], "| recent =", py)


if __name__ == "__main__":
    main()
