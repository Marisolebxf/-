#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RISK_TAX · 税收违法数（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_RISK_TAX_out.json
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
        "metric_id": "M_ENT_UI_RISK_TAX",
        "metric_name_zh": "税收违法数",
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

    # F1 源表总行数与 org 关联覆盖（2026-11-04 复核：org_id 列存在且全覆盖）
    cur.execute("SELECT COUNT(*) AS n, SUM(org_id IS NOT NULL AND org_id <> '') AS j FROM gkx.dwd_org_risk_tax_punish")
    r = cur.fetchone()
    out["facts"]["total_rows"] = int(r[0])
    out["facts"]["org_joinable_rows"] = int(r[1] or 0)
    out["facts"]["org_join_rate"] = out["facts"]["org_joinable_rows"] / out["facts"]["total_rows"] if out["facts"]["total_rows"] else None

    # F2 按企业计数 Top10
    cur.execute(
        "SELECT org_id, taxpayer_name, COUNT(*) AS c FROM gkx.dwd_org_risk_tax_punish "
        "WHERE org_id IS NOT NULL AND org_id <> '' "
        "GROUP BY org_id, taxpayer_name ORDER BY c DESC, org_id ASC LIMIT 10")
    out["facts"]["top10_by_org"] = [
        {"org_id": a, "name_cn": b, "count": int(c)} for a, b, c in cur.fetchall()]

    # F3 名称匹配演示（以库内真实企业名样例演示 LIKE 代理口径与误配率评估）
    try:
        cur.execute(
            "SELECT b.name_cn, COUNT(*) AS c FROM gkx.dwd_org_risk_tax_punish a "
            "JOIN (SELECT name_cn FROM gkx.dwd_org_base_info WHERE city LIKE '%深圳%' LIMIT 50) b "
            "  ON a.taxpayer_name LIKE CONCAT('%%', b.name_cn, '%%') "
            "GROUP BY b.name_cn ORDER BY c DESC LIMIT 5")
        out["facts"]["shenzhen_name_match_demo"] = [
            {"name_cn": a, "count": int(c)} for a, c in cur.fetchall()]
    except Exception as e:
        out["facts"]["name_match_demo_err"] = str(e)

    dst = _HERE / "out" / "M_ENT_UI_RISK_TAX_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
