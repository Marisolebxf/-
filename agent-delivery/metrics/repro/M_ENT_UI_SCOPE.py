#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_SCOPE · 经营范围（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_SCOPE_out.json
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
        "metric_id": "M_ENT_UI_SCOPE",
        "metric_name_zh": "经营范围",
        "batch": "TOPIC-UI-GAP-L01",
        "probe_date": "2026-11-04",
        "ui_evidence": [
            "repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103",
            "live 30892 企业画像抽屉（20261104 盘点实拍）",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": "部分支持",
        "verdict_kind": "countable",
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：登记/案件存量计数，基期=数据装载日。",
    }

    # F1 年报基础表行数（qyzyywhd = 企业主营业务活动/经营范围）
    cur.execute("SELECT COUNT(*) AS n FROM gkx.dwd_org_annual_report_base")
    out["facts"]["report_rows"] = int(cur.fetchone()[0])

    # F2 qyzyywhd 非空覆盖
    cur.execute(
        "SELECT SUM(qyzyywhd IS NOT NULL AND qyzyywhd <> '') AS has_scope "
        "FROM gkx.dwd_org_annual_report_base")
    out["facts"]["has_scope_rows"] = int(cur.fetchone()[0] or 0)

    # F3 样例（脱敏截断）
    cur.execute(
        "SELECT jgmc, LEFT(qyzyywhd, 60) AS scope_head FROM gkx.dwd_org_annual_report_base "
        "WHERE qyzyywhd IS NOT NULL AND qyzyywhd <> '' LIMIT 5")
    out["facts"]["sample_scope"] = [{"org_name": a, "scope_head": b} for a, b in cur.fetchall()]

    # F4 与底册名称代理关联演示
    try:
        cur.execute(
            "SELECT COUNT(*) AS n FROM gkx.dwd_org_annual_report_base a "
            "JOIN gkx.dwd_org_base_info b ON a.jgmc = b.name_cn")
        out["facts"]["name_join_hits"] = int(cur.fetchone()[0])
    except Exception as e:
        out["facts"]["name_join_err"] = str(e)

    dst = _HERE / "out" / "M_ENT_UI_SCOPE_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
