#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_STATUS · 经营状态（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_STATUS_out.json
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
        "metric_id": "M_ENT_UI_STATUS",
        "metric_name_zh": "经营状态",
        "batch": "TOPIC-UI-GAP-L01",
        "probe_date": "2026-11-04",
        "ui_evidence": [
            "repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103",
            "live 30892 企业画像抽屉（20261104 盘点实拍）",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": "完全转换支持",
        "verdict_kind": "countable",
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：登记/案件存量计数，基期=数据装载日。",
    }

    # F1 reg_status 值域分布（189,116 底册全量）
    cur.execute(
        "SELECT reg_status, COUNT(*) AS n FROM gkx.dwd_org_base_info "
        "GROUP BY reg_status ORDER BY n DESC")
    out["facts"]["reg_status_distribution"] = [
        {"reg_status": (a or "")[:40], "orgs": int(b)} for a, b in cur.fetchall()]

    # F2 底册总行数与 org_id 覆盖
    cur.execute("SELECT COUNT(*) AS n FROM gkx.dwd_org_base_info")
    out["facts"]["base_total"] = int(cur.fetchone()[0])

    dst = _HERE / "out" / "M_ENT_UI_STATUS_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
