#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DS_07_POLICY_GUARD_001｜发展战略引导力评估（王惠三维，零 SQL 复现）

王惠三维（calc-logic 原公式）：
  D1 前瞻性 战略顶层规划覆盖率 = title/keywords/keypoints/theme 命中「规划/纲要/远景/行动计划」
  D2 系统性 政策承接完整度     = quote_policy 非空政策数 / 有效政策总数
  D3 针对性 精准扶持措施覆盖率 = policy_support.support_way ≥1 条政策数 / 总数
合成：三维比率等权 ×100，缺维不进平均（不按 0 摊入）。

本批额外做两项实测（POLICY 族口径要求）：
  - 全文匹配敏感性：把 D1 的匹配面从 title 扩到 title+content，披露标题层与全文层的差值；
  - 文号/时效不参与本指标，但 quote_policy 的第二条数组在库内已截断，作为数据质量事实登记。

数据：只读 code/_snapshots21 快照（policy_content 18,763 行用于全文敏感性），零 SQL。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_DS_07_POLICY_GUARD_001_out.json")

FORWARD_WORDS = ["规划", "纲要", "远景", "行动计划"]
PLACEHOLDER = {"", "NULL", "NONE", "-", "[]"}


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER or s == "null" else s


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    rows = load("pg_policy_rows_20261021.json")
    content = load("policy_content_20261021.json")
    aux = load("policy_aux_20261022.json")
    n = len(rows)

    content_by_id = {}
    for r in content:
        # [id, title, content, abstract] 形态（169 同源快照）
        cid = r[0]
        body = nn(r[2]) if len(r) > 2 else ""
        abs_ = nn(r[4]) if len(r) > 4 else ""
        content_by_id[cid] = (body, abs_)

    fwd_hit = 0
    fwd_titles = []
    theme_hit = 0
    for r in rows:
        title = nn(r.get("title"))
        if any(w in title for w in FORWARD_WORDS):
            fwd_hit += 1
            if len(fwd_titles) < 8:
                fwd_titles.append(title[:70])

    # theme 字段命中（全表仅 2 行有 theme 文本）
    for tr in aux["probes"].get("theme_quote_rows", []):
        if any(w in nn(tr.get("theme")) for w in FORWARD_WORDS):
            theme_hit += 1

    # 全文敏感性：title 或 content/abstract 命中
    full_hit = 0
    full_only = 0
    for r in rows:
        title = nn(r.get("title"))
        body, abs_ = content_by_id.get(r["id"], ("", ""))
        th = any(w in title for w in FORWARD_WORDS)
        bh = any(w in body or w in abs_ for w in FORWARD_WORDS)
        if th or bh:
            full_hit += 1
        if bh and not th:
            full_only += 1

    quote_rows = aux["probes"].get("theme_quote_rows", [])
    quote_hit = sum(1 for r in quote_rows if nn(r.get("quote_policy")))
    quote_titles = [nn(r.get("theme"))[:40] for r in quote_rows if nn(r.get("quote_policy"))]

    support_hit = 0  # policy_support 全表 0 行非占位符（a23 字段探针 ps=0）

    fwd_rate = fwd_hit / n
    quote_rate = quote_hit / n
    support_rate = support_hit / n

    dims = [
        {"key": "D1_forward", "name": "前瞻性（战略顶层规划覆盖率）",
         "hit": fwd_hit, "n": n, "rate_pct": round(fwd_rate * 100, 4),
         "available": True,
         "basis": "title 命中规划/纲要/远景/行动计划；keywords/keypoints 0 行、theme 2 行（均未命中）",
         "examples": fwd_titles},
        {"key": "D2_quote", "name": "系统性（政策承接完整度）",
         "hit": quote_hit, "n": n, "rate_pct": round(quote_rate * 100, 4),
         "available": quote_hit > 0,
         "basis": "quote_policy 非占位符；仅 2 行，其中 1 行数组在库内已截断",
         "examples": quote_titles},
        {"key": "D3_support", "name": "针对性（精准扶持措施覆盖率）",
         "hit": support_hit, "n": n, "rate_pct": 0.0,
         "available": False,
         "basis": "policy_support 全表 0 行有效（字面 null 占位），support_way 不可解析",
         "examples": []},
    ]
    avail = [d for d in dims if d["available"]]
    score = sum(d["rate_pct"] for d in avail) / len(avail)

    out = {
        "metric_id": "M_POLICY_DS_07_POLICY_GUARD_001",
        "title": "发展战略引导力评估",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": ("三维中前瞻性可算（1,085/20,000=5.42%，标题层）；系统性只有 2 条政策有引用"
                           "（0.01%）；针对性 policy_support 全表 0 行有效，整维不可算。"
                           "缺一个必需维 → 部分支持。"),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本指标为截面文本标记率，不设跨年基期。政策表年份只用于背景描述，"
                            "不进入任何分母；2022 年后为采集残片（2023 年 0 行），不外推。"),
        "sources": {
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（title/publish_year）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文/摘要，全文敏感性）",
            "policy_aux": "code/_snapshots21/policy_aux_20261022.json（theme/quote_policy 2 行）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（policy_support=0 的字段证据）",
            "db": "gkx @ 183.240.141.251:3318（只读；本脚本零 SQL）",
        },
        "population": {"rows": n, "status_values": aux["probes"].get("status_dist"),
                       "rows_with_content_snapshot": len(content_by_id)},
        "dims": dims,
        "dims_available": f"{len(avail)}/3",
        "guidance_score": round(score, 2),
        "formula": "三维比率等权 ×100；缺维不进平均（D3 不参与分母）",
        "fulltext_sensitivity": {
            "title_hit": fwd_hit,
            "title_or_content_hit": full_hit,
            "content_only_hit": full_only,
            "title_rate_pct": round(100.0 * fwd_hit / n, 4),
            "fulltext_rate_pct": round(100.0 * full_hit / n, 4),
            "note": ("主口径按王惠用标题/标签字段，命中 1,085 条；把正文纳入后升至 "
                     f"{full_hit} 条（{round(100.0 * full_hit / n, 2)}%），其中 {full_only} 条只在正文命中。"
                     "两层的差值说明：5.42% 是「标题写了规划语汇」的比例，不是「政策实际具备规划属性」；"
                     "发布时必须标明匹配面，不能把标题命中率说成政策前瞻性水平。"),
        },
        "data_quality_notes": [
            "quote_policy 全表仅 2 行非占位符，其中 id=18352858 的 JSON 数组在库内已截断（缺右括号与后续元素），只能按「有引用」计数，不能按条数统计。",
            "policy_support 全表 20,000 行为字面 'null'（小写），是非空但无值的占位串；按非空计数会误判为 100% 覆盖。",
            "status 全表单一值「有效」，有效占比 100% 是样本框构造；本指标不使用该字段做分母。",
        ],
        "verdict": ("引导力得分 = 2.72（2/3 维参与）。该分数不可读成「政策前瞻性只有 2.72 分」，"
                    "因为三维里两维的真实值都接近 0，等权平均被单维拖平；正确读法是"
                    "「D1 标题层 5.42% / D2 0.01% / D3 不可判」，分数只作排序占位，不作质量结论。"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "dims_available",
                                          "guidance_score", "fulltext_sensitivity")},
                     ensure_ascii=False, indent=1))
    print("dims:", [(d["key"], d["hit"], d["rate_pct"]) for d in dims])
    print("->", OUT)


if __name__ == "__main__":
    main()
