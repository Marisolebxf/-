#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RISK_BANKRUPTCY · 破产案件数（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_RISK_BANKRUPTCY_out.json
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
        "metric_id": "M_ENT_UI_RISK_BANKRUPTCY",
        "metric_name_zh": "破产案件数",
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

    # F1 源表总行数（无 org_id 列，名称代理）
    cur.execute("SELECT COUNT(*) AS n FROM gkx.dwd_org_bankruptcy_public_cases")
    out["facts"]["total_rows"] = int(cur.fetchone()[0])

    # F2 名称代理 Top10（respondent_info LIKE 匹配示意，用高频词样例核验语义）
    cur.execute(
        "SELECT respondent_info, COUNT(*) AS c FROM gkx.dwd_org_bankruptcy_public_cases "
        "GROUP BY respondent_info ORDER BY c DESC, respondent_info ASC LIMIT 10")
    out["facts"]["top10_sample"] = [
        {"value": (a or "")[:60], "count": int(c)} for a, c in cur.fetchall()]

    # F3 名称匹配演示（以库内真实企业名样例演示 LIKE 代理口径与误配率评估）
    try:
        cur.execute(
            "SELECT b.name_cn, COUNT(*) AS c FROM gkx.dwd_org_bankruptcy_public_cases a "
            "JOIN (SELECT name_cn FROM gkx.dwd_org_base_info WHERE city LIKE '%深圳%' LIMIT 50) b "
            "  ON a.respondent_info LIKE CONCAT('%%', b.name_cn, '%%') "
            "GROUP BY b.name_cn ORDER BY c DESC LIMIT 5")
        out["facts"]["shenzhen_name_match_demo"] = [
            {"name_cn": a, "count": int(c)} for a, c in cur.fetchall()]
    except Exception as e:
        out["facts"]["name_match_demo_err"] = str(e)

    dst = _HERE / "out" / "M_ENT_UI_RISK_BANKRUPTCY_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
