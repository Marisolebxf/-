#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_TYPE_DIST 政策类型分布 —— 只读共用快照，不连库。

本件能算的是 `type`（文种/文件类型）分布；需求要求的「产业政策/人才政策/
企业扶持政策」属主题分类，对应 `theme`，全表只有 2 行有效值。
故交付「文种分布」降级口径，并把主题维缺失写进产物与正文。
产出：code/M_POLICY_TYPE_DIST_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MID = "M_POLICY_TYPE_DIST"
HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21" / "policy_dims_20261023.json"
FILL = HERE / "_snapshots21" / "policy_field_fill_20261022.json"
AUX = HERE / "_snapshots21" / "policy_aux_20261022.json"
OUT = HERE / f"{MID}_out.json"


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def main() -> int:
    s = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = s["rows"]
    td = s["type_dist"]
    tc = s["type_class_dist"]

    type_rows = [
        {"type": k, "n": v, "pct": pct(v, rows),
         "is_null_placeholder": k == "__NULL__"}
        for k, v in td.items()
    ]
    class_rows = [{"type_class": k, "n": v, "pct": pct(v, rows)} for k, v in tc.items()]

    fill = json.loads(FILL.read_text(encoding="utf-8")) if FILL.exists() else {}
    fields = fill.get("fields", {})
    theme_nonempty = fields.get("theme", {}).get("nonempty")
    keywords_nonempty = fields.get("keywords", {}).get("nonempty")
    keyphrases_nonempty = fields.get("keyphrases", {}).get("nonempty")

    aux = json.loads(AUX.read_text(encoding="utf-8")) if AUX.exists() else {}
    theme_rows = (aux.get("probes", {}) or {}).get("theme_quote_rows", [])
    theme_values = []
    for r in theme_rows:
        raw = r.get("theme") or ""
        try:
            vals = json.loads(raw) if raw else []
        except Exception:
            vals = [raw]
        theme_values.append({"id": r.get("id"), "theme": vals})

    known_docs = tc.get("政策文件类", 0) + tc.get("规范性文件类", 0)
    res = {
        "metric_id": MID,
        "metric_name": "政策类型分布",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "需求要的「产业政策/人才政策/企业扶持政策」是主题分类，对应 `theme`；"
            "该列全表只有 2 行有效值（0.01%），`keywords`/`keypoints` 各 0 行，"
            "`policy_support` 20,000 行全为小写字符串 'null'。现能算的 `type` 是文种"
            "（其他通知/公示公告/申报通知/政策文件-…），不是政策主题。主题维始终不可得，"
            "只能交付「文种分布」降级口径，故判部分支持。"
        ),
        "source": s["source"],
        "snapshot": "code/_snapshots21/policy_dims_20261023.json",
        "builder": "code/_build_policy_dims_20261023.py",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指标：统计库内全部政策的文种分布，不设年度分母。"
            "publish_year 缺 3 行，不影响本件（本件不按年切分）。"
        ),
        "type_dist": type_rows,
        "type_total": sum(td.values()),
        "total_rows": rows,
        "type_class_dist": class_rows,
        "type_class_total": sum(tc.values()),
        "document_purity": {
            "policy_or_normative_rows": known_docs,
            "policy_or_normative_pct": pct(known_docs, rows),
            "transaction_rows": tc.get("事务通知类", 0),
            "transaction_pct": pct(tc.get("事务通知类", 0), rows),
            "unlabeled_rows": tc.get("未标注", 0),
            "unlabeled_pct": pct(tc.get("未标注", 0), rows),
            "policy_with_interpretation_rows": known_docs + tc.get("政策解读", 0),
            "policy_with_interpretation_pct": pct(known_docs + tc.get("政策解读", 0), rows),
            "type_kinds": len(td),
            "note": "政策文件类 6,881 + 规范性文件类 644 = 7,525 条；事务通知类 10,596 条；未标注 1,862 条；政策解读 17 条，四类合计 20,000。",
        },
        "topic_dimension": {
            "theme_nonempty_rows": theme_nonempty,
            "theme_pct": pct(theme_nonempty or 0, rows),
            "keywords_nonempty_rows": keywords_nonempty,
            "keyphrases_nonempty_rows": keyphrases_nonempty,
            "policy_support_valid_rows": 0,
            "policy_support_literal_null_rows": rows,
            "theme_sample_rows": theme_values,
            "note": "2 条 theme 记录里出现「创业扶持/财政支持/融资服务/科技创新/乡村振兴」等主题标签，证明主题分类字段存在，但只有 2 行，无法做 20,000 条的分布。",
        },
        "requested_taxonomy": {
            "requested": ["产业政策", "人才政策", "企业扶持政策"],
            "derivable_from_type": False,
            "derivable_from_theme": False,
            "reason": "type 是文种，theme 只有 2 行；两列都不承载「产业/人才/企业扶持」的三分法。",
        },
        "known_estimate": s["known_estimate"],
        "population_notes": [
            "分母是 20,000 行库内存量；文种分布不是政策主题分布，不能用来回答「人才政策有多少条」。",
            "字面 'NULL' 1,862 行（9.31%）是未标注文种，不是 SQL NULL，不能当有效类型。",
            "事务通知类 10,596 行（52.98%）包含其他通知 5,782、公示公告 2,995、申报通知 1,819；直接数「政策数」会被发文习惯污染。",
            "政策解读 17 行单列，不并入政策文件类；若并入，政策文件+规范性文件为 7,542 条（37.71%）。",
        ],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} types={len(type_rows)} total={res['type_total']} classes={[(x['type_class'], x['n']) for x in class_rows]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
