#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RISK_EQUITY_FREEZE · 股权冻结数（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性负证据探针，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_RISK_EQUITY_FREEZE_out.json
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    cur.execute("SET NAMES utf8mb4")
    out = {
        "metric_id": "M_ENT_UI_RISK_EQUITY_FREEZE",
        "metric_name_zh": "股权冻结数",
        "batch": "TOPIC-UI-GAP-L01",
        "probe_date": "2026-11-04",
        "ui_evidence": [
            "repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103",
            "live 30892 企业画像抽屉（20261104 盘点实拍）",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：登记/案件存量计数，基期=数据装载日。",
    }
    KEYWORDS = ['freeze', 'frozen', 'dongjie', 'dj_']

    # absence_probe 三件套（查了什么/条件/命中几行）—— gkx 实时复核
    cur.execute("SHOW TABLES FROM gkx")
    tables = [r[0] for r in cur.fetchall()]
    out["absence_probe"].append({"probe": "gkx SHOW TABLES 全表名扫描", "scope": f"{len(tables)} 张", "keyword": KEYWORDS, "hit_tables": [t for t in tables if any(k in t.lower() for k in KEYWORDS)]})
    out["facts"]["gkx_table_total"] = len(tables)
    out["notes"].append("久新/live 探针结论见 out/M_ENT_UI_RISK_BATCH_PROBE_out.json（久新 242 张 ads_* 风险类 7 张均非本卡语义；live 对应 risk_* 表结构在 0 行）。")

    dst = _HERE / "out" / "M_ENT_UI_RISK_EQUITY_FREEZE_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
