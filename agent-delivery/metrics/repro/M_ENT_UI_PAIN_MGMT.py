#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_PAIN_MGMT · 管理（企业发展痛难点分析·痛难点维度）

UI：科技专题服务系统 企业分析>企业发展痛难点分析>诊断范围「管理」勾选维。
需求文档未给判定口径；gkx 无 management/管理类专用表（批探针 gkx_painlike_tables 零命中）。

本件口径（推测定义）：管理维可观测面 = 企业治理结构可观测项
（gkx dwd_org_base_info 登记注册规模/高管/股东类表——以探针实存为准）；
管理效能类语义（人均产值、管理费用率）依赖财务表王惠 src 列（arch_development_am 等），
M_ENT_PAINPOINT 族已核 gkx 财务表九列全在。

数据源：gkx（登记+财务）。产出：out/M_ENT_UI_PAIN_MGMT_out.json
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
        "metric_id": "M_ENT_UI_PAIN_MGMT",
        "batch": "TOPIC-UI-GAP-L01",
        "ui_evidence": [
            "live 30892 企业分析>企业发展痛难点分析>诊断范围「管理」（20261104 盘点实拍）",
            "02-缺口指标清单.xlsx seq29",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": []},
    }

    # F1 治理/高管/股东类表探针
    cur.execute("SHOW TABLES FROM gkx")
    tabs = [r[0] for r in cur.fetchall()]
    gov_like = [t for t in tabs if any(k in t.lower() for k in ("manage", "executive", "senior", "holder", "shareholder", "personnel", "staff", "team"))]
    out["facts"]["gkx_govlike_tables"] = gov_like
    rows_map = {}
    for t in gov_like[:8]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
            rows_map[t] = cur.fetchone()[0]
        except Exception as e:
            rows_map[t] = f"ERR:{e}"
    out["facts"]["gkx_govlike_rows"] = rows_map

    # F2 财务表管理费用列（王惠 src 九列全在的财务表）
    cur.execute("SHOW TABLES FROM gkx LIKE '%financial%'")
    fin_tables = [r[0] for r in cur.fetchall() if "bak" not in r[0]]
    out["facts"]["gkx_fin_tables"] = fin_tables
    for t in fin_tables[:3]:
        cur.execute(f"SHOW COLUMNS FROM gkx.{t}")
        cols = [r[0] for r in cur.fetchall()]
        mgmt_cols = [c for c in cols if "manage" in c.lower() or "admin" in c.lower()]
        if mgmt_cols:
            cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
            out["facts"].setdefault("fin_mgmt", {})[t] = {
                "rows": cur.fetchone()[0], "mgmt_cols": mgmt_cols,
            }

    out["support_judgment"] = "部分支持"
    out["notes"].append("治理结构可观测项与财务管理费用列可探；「管理构成痛难点」判定口径未闭合；"
                        "若探针治理类表为空/缺 → 该维升「完全不支持」的触发器=管理语义专用表零承载。")
    p = HERE / "out" / "M_ENT_UI_PAIN_MGMT_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p)
    print("govlike:", out["facts"]["gkx_govlike_tables"])


if __name__ == "__main__":
    main()
