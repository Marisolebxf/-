#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RISK_ILLEGAL · 严重违法数（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_RISK_ILLEGAL_out.json
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
        "metric_id": "M_ENT_UI_RISK_ILLEGAL",
        "metric_name_zh": "严重违法数",
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

    # F1 源表总行数与 org 关联覆盖
    cur.execute("SELECT COUNT(*) AS n, SUM(org_id IS NOT NULL AND org_id <> '') AS j FROM gkx.dwd_org_company_illegal")
    r = cur.fetchone()
    out["facts"]["total_rows"] = int(r[0])
    out["facts"]["org_joinable_rows"] = int(r[1] or 0)
    out["facts"]["org_join_rate"] = out["facts"]["org_joinable_rows"] / out["facts"]["total_rows"] if out["facts"]["total_rows"] else None

    # F2 按企业计数 Top10（UI 卡语义同向核验：单企业 COUNT）
    cur.execute(
        "SELECT org_id, name_cn, COUNT(*) AS c FROM gkx.dwd_org_company_illegal "
        "WHERE org_id IS NOT NULL AND org_id <> '' "
        "GROUP BY org_id, name_cn ORDER BY c DESC, org_id ASC LIMIT 10")
    out["facts"]["top10_by_org"] = [
        {"org_id": a, "name_cn": b, "count": int(c)} for a, b, c in cur.fetchall()]

    # F3 计数分布（区分度：n_scored / 非零 / 非全体同分）
    cur.execute(
        "SELECT cnt, COUNT(*) AS orgs FROM ("
        "  SELECT org_id, COUNT(*) AS cnt FROM gkx.dwd_org_company_illegal "
        "  WHERE org_id IS NOT NULL AND org_id <> '' GROUP BY org_id) t "
        "GROUP BY cnt ORDER BY cnt LIMIT 15")
    out["facts"]["count_distribution"] = [{"count": int(a), "orgs": int(b)} for a, b in cur.fetchall()]

    dst = _HERE / "out" / "M_ENT_UI_RISK_ILLEGAL_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
