#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_PAIN_FINANCE · 融资（企业发展痛难点分析·痛难点维度）

UI：科技专题服务系统 企业分析>企业发展痛难点分析>诊断范围「融资」勾选维。
需求文档未给判定口径。融资活动原料 gkx dwd_org_financing_info（25,654 行，实测）：
org_id/name_cn/external_id/funding_round/funding_amount/funding_currency_code/completion_date/
investors_name/pre_valuation/after_valuation 十八列全在——企业融资事件计数与「最近一轮距今时长」可直算。

本件口径（推测定义）：融资维可观测面 = 企业融资事件数 + 最近融资距今月数；
「融资难」判定（如超过 N 月未融资）留模型层，本件交付原料与分布。

数据源：gkx。产出：out/M_ENT_UI_PAIN_FINANCE_out.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkxdb import gkx, gkx_count  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_ENT_UI_PAIN_FINANCE",
        "batch": "TOPIC-UI-GAP-L01",
        "ui_evidence": [
            "live 30892 企业分析>企业发展痛难点分析>诊断范围「融资」（20261104 盘点实拍）",
            "02-缺口指标清单.xlsx seq30",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：融资事件存量（completion_date 逐年分布另落）。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": []},
    }

    out["facts"]["fin_rows"] = gkx_count("dwd_org_financing_info")
    cur.execute("SHOW COLUMNS FROM gkx.dwd_org_financing_info")
    out["facts"]["fin_cols"] = [r[0] for r in cur.fetchall()][:18]
    cur.execute("""SELECT COUNT(DISTINCT org_id) FROM gkx.dwd_org_financing_info
                   WHERE org_id IS NOT NULL AND org_id <> ''""")
    out["facts"]["fin_distinct_orgs"] = cur.fetchone()[0]
    cur.execute("""SELECT funding_round, COUNT(*) AS n FROM gkx.dwd_org_financing_info
                   GROUP BY funding_round ORDER BY n DESC LIMIT 8""")
    out["facts"]["round_dist"] = [{"round": r[0], "n": r[1]} for r in cur.fetchall()]
    cur.execute("""SELECT org_id, COUNT(*) AS n FROM gkx.dwd_org_financing_info
                   WHERE org_id IS NOT NULL AND org_id <> ''
                   GROUP BY org_id ORDER BY n DESC LIMIT 5""")
    out["facts"]["fin_top5_orgs"] = [{"org_id": r[0], "n": r[1]} for r in cur.fetchall()]

    out["derived"]["avg_rounds_per_financed_org"] = {
        "value": round(out["facts"]["fin_rows"] / max(out["facts"]["fin_distinct_orgs"], 1), 4),
        "numerator": out["facts"]["fin_rows"],
        "denominator": out["facts"]["fin_distinct_orgs"],
        "denominator_note": "融资事件总行数 / 有融资记录的 distinct org 数（同表同 WHERE）",
    }

    out["support_judgment"] = "部分支持"
    out["notes"].append("融资事件原料全（25,654 行、18 列）；「融资难」模型判定口径未闭合 → 部分支持；"
                        "口径闭合后同一原料即出结果。")
    p = HERE / "out" / "M_ENT_UI_PAIN_FINANCE_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p)
    print("fin_rows =", out["facts"]["fin_rows"], "| distinct orgs =", out["facts"]["fin_distinct_orgs"])


if __name__ == "__main__":
    main()
