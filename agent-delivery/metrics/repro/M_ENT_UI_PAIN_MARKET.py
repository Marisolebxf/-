#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_PAIN_MARKET · 市场拓展（企业发展痛难点分析·痛难点维度）

UI：科技专题服务系统 企业分析>企业发展痛难点分析>诊断范围「市场拓展」勾选维（live 30892，20261104 盘点）。
诊断范围四维之一；页面模型输出「痛难点类型卡」。需求文档未给四维的判定口径（Q 未闭合）。

本件口径（推测定义，非甲方闭合）：
  市场拓展维可观测面 = 企业招投标活动强度（gkx dwd_bid_base_out 招投标公告，org_id 关联）
  + 市场类登记（gkx dwd_market）；该维「是否构成痛难点」的模型判定留页面/算法层，本件交付可观测原料与计数。

数据源：gkx（招投标 39,962 行）+ live（无 pain 专用表披露）。产出：out/M_ENT_UI_PAIN_MARKET_out.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkxdb import gkx, live, gkx_count  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_ENT_UI_PAIN_MARKET",
        "batch": "TOPIC-UI-GAP-L01",
        "ui_evidence": [
            "live 30892 企业分析>企业发展痛难点分析>诊断范围「市场拓展」（20261104 盘点实拍）",
            "调研工作区 1104 盘点缺口清单 seq27（盘点产物不入仓，仅作溯源说明）",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "企业发展痛难点分析模型需求叶存在（bid-reference 科技专题服务算法库 企业发展痛难点分析）,"
                    "但「市场拓展」维的判定口径未给出（Q 未闭合）。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：招投标/市场登记存量计数。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": []},
    }

    # F1 招投标承载（公告面无 org_id；企业维走中标候选人表）
    out["facts"]["bid_rows"] = gkx_count("dwd_bid_base_out")
    out["facts"]["bid_note"] = "dwd_bid_base_out 无 org_id（公告粒度）；企业维关联走 dwd_bid_win_candidate_out"
    out["facts"]["bidwin_rows"] = gkx_count("dwd_bid_win_candidate_out")
    cur.execute("""SELECT COUNT(DISTINCT org_id) FROM gkx.dwd_bid_win_candidate_out
                   WHERE org_id IS NOT NULL AND org_id <> ''""")
    out["facts"]["bidwin_distinct_orgs"] = cur.fetchone()[0]

    # F2 市场登记面
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_market")
    out["facts"]["market_rows"] = cur.fetchone()[0]
    cur.execute("SHOW COLUMNS FROM gkx.dwd_market")
    out["facts"]["market_cols"] = [r[0] for r in cur.fetchall()][:14]

    # F3 样例
    cur.execute("""SELECT org_id, COUNT(*) AS n FROM gkx.dwd_bid_win_candidate_out
                   WHERE org_id IS NOT NULL AND org_id <> ''
                   GROUP BY org_id ORDER BY n DESC LIMIT 5""")
    out["facts"]["bidwin_top5_orgs"] = [{"org_id": r[0], "n": r[1]} for r in cur.fetchall()]

    # D 派生
    out["derived"]["bidwin_org_coverage"] = {
        "value": round(out["facts"]["bidwin_distinct_orgs"] / max(out["facts"]["bidwin_rows"], 1) * 100, 4),
        "numerator": out["facts"]["bidwin_distinct_orgs"],
        "denominator": out["facts"]["bidwin_rows"],
        "denominator_note": "中标候选人表 distinct org_id 数 / 其总行数（同表同 WHERE；值为去重率非覆盖率，键名如实）",
    }

    out["support_judgment"] = "部分支持"
    out["notes"].append("招投标/市场原料在（gkx），但「构成痛难点」的模型判定口径未闭合（Q 未闭合）→ 部分支持；"
                        "口径闭合后按同一原料即可出模型结果。")
    p = HERE / "out" / "M_ENT_UI_PAIN_MARKET_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p)
    print("bid_rows =", out["facts"]["bid_rows"], "| bidwin_rows =", out["facts"]["bidwin_rows"], "| bidwin orgs =", out["facts"]["bidwin_distinct_orgs"])


if __name__ == "__main__":
    main()
