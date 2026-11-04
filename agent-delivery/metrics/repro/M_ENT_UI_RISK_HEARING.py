#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RISK_HEARING · 开庭公告数（科技专题 UI 企业画像卡，TOPIC-UI-GAP-L01 批1）

UI 证据：live 30892 企业查询→企业画像抽屉（20261104 盘点实拍）；
repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103（risk tab，dataSource: 待源（司法/失信，Q020））。
口径（推测定义，非甲方闭合）：企业维度确定性登记记录计数，无建模假设。
数据源：gkx（183.240.141.251:3318 只读，_gkxdb.py 唯一入口）。
三源探针：out/M_ENT_UI_RISK_BATCH_PROBE_out.json（gkx/久新/live，2026-11-04）。
产出：out/M_ENT_UI_RISK_HEARING_out.json
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
        "metric_id": "M_ENT_UI_RISK_HEARING",
        "metric_name_zh": "开庭公告数",
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

    # F1 明细抽样面（sjwdbq 标签过滤 → distinct 案件）
    cur.execute(
        "SELECT COUNT(*) AS rows_, COUNT(DISTINCT sfajwybs) AS cases "
        "FROM gkx.dwd_opt_judicial_case_detail WHERE sjwdbq LIKE %s",
        ("%开庭公告%",))
    r = cur.fetchone()
    out["facts"]["detail_rows"] = int(r[0])
    out["facts"]["distinct_cases"] = int(r[1])

    # F2 明细→主面 org 关联（zzzjid = case_id，计数落到抽样面内）
    cur.execute(
        "SELECT COUNT(*) AS n FROM ("
        "  SELECT DISTINCT d.sfajwybs AS cid, m.org_id "
        "  FROM gkx.dwd_opt_judicial_case_detail d "
        "  JOIN gkx.dwd_org_opt_judicial_case m ON d.zzzjid = m.case_id "
        "  WHERE d.sjwdbq LIKE %s) t", ("%开庭公告%",))
    out["facts"]["distinct_cases_with_org"] = int(cur.fetchone()[0])

    # F3 按企业计数 Top5
    cur.execute(
        "SELECT m.org_id, m.company_name, COUNT(DISTINCT d.sfajwybs) AS c "
        "FROM gkx.dwd_opt_judicial_case_detail d "
        "JOIN gkx.dwd_org_opt_judicial_case m ON d.zzzjid = m.case_id "
        "WHERE d.sjwdbq LIKE %s "
        "GROUP BY m.org_id, m.company_name ORDER BY c DESC, m.org_id ASC LIMIT 5",
        ("%开庭公告%",))
    out["facts"]["top5_by_org"] = [
        {"org_id": a, "company_name": b, "count": int(c)} for a, b, c in cur.fetchall()]

    # F4 明细抽样面披露（50,000 行 / 37,378 案件 = 全量明细的抽样）
    cur.execute("SELECT COUNT(*) AS n FROM gkx.dwd_opt_judicial_case_detail")
    out["facts"]["detail_sample_rows"] = int(cur.fetchone()[0])
    out["facts"]["sampling_disclosure"] = "明细表为抽样面（50,000 行 / 37,378 案件），本卡计数=抽样面内 distinct 案件；升档须全量明细装载。"

    dst = _HERE / "out" / "M_ENT_UI_RISK_HEARING_out.json"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst)


if __name__ == "__main__":
    main()
