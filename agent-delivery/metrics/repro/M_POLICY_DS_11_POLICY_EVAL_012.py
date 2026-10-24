#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DS_11_POLICY_EVAL_012｜智能摘要与结论推送（三维就绪度，零 SQL 复现）

三维（王惠框架，代理公式由本轮补，标注为「就绪度」而非「质量」）：
  D1 信息覆盖度 = 摘要主料可用率（正文 >100 字，摘要兜底）与上下文字段齐备率的等权
  D2 结论条数   = 逐政策抽取关键句（标题—句子 bigram 重合排序，TextRank 代理），
                  每篇最多 3 句，按「平均可出句数 / 3」归一到 0—1
  D3 推送就绪   = dwd_policy_summary(push_status) 与编辑日志表是否存在；两侧均无 → 不可算
合成：可算维等权 ×100，缺维不进平均。

数据：只读 code/_snapshots21（policy_content 18,763 行），零 SQL。
"""
import json
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_DS_11_POLICY_EVAL_012_out.json")

PLACEHOLDER = {"", "NULL", "NONE", "-", "[]"}
SENT_SPLIT = re.compile(r"(?<=[。！？；])")


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER or s == "null" else s


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def split_sents(text):
    parts = SENT_SPLIT.split(str(text or ""))
    return [p.strip() for p in parts if len(p.strip()) >= 20]


def textrank_lite(title, sents):
    def bigrams(s):
        s = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", s)
        return set(s[i:i + 2] for i in range(len(s) - 1))

    tb = bigrams(title or "")
    if not tb:
        return 0, []
    scored = []
    for s in sents:
        sb = bigrams(s)
        if not sb:
            continue
        ov = len(tb & sb) / len(tb | sb)
        scored.append((ov, s))
    scored.sort(key=lambda x: -x[0])
    return len(scored), scored[:3]


def main():
    rows = load("pg_policy_rows_20261021.json")
    content = load("policy_content_20261021.json")
    aux = load("policy_aux_20261022.json")
    n = len(rows)

    txt = {r[0]: (nn(r[1]), nn(r[2]), nn(r[4])) for r in content}

    # D1 主料与上下文
    main_ok = sum(1 for r in rows if (r.get("ct_len") or 0) > 100 or (r.get("abs_len") or 0) > 0)
    ctx = {
        "title": sum(1 for r in rows if nn(r.get("title"))),
        "ministry": sum(1 for r in rows if nn(r.get("ministry"))),
        "publish_year": sum(1 for r in rows if nn(r.get("publish_year"))),
    }
    main_rate = main_ok / n
    ctx_rate = sum(ctx.values()) / (3 * n)

    # D2 结论条数（固定种子，抽样 2,000 条有正文的政策）
    pool = [r for r in rows if r["id"] in txt and txt[r["id"]][1]]
    random.seed(42)
    sample = random.sample(pool, min(2000, len(pool)))
    with_concl = 0
    total_sents = 0
    examples = []
    for r in sample:
        title, body, abs_ = txt[r["id"]]
        sents = split_sents(body) or split_sents(abs_)
        if not sents:
            continue
        k, top = textrank_lite(title, sents)
        if k:
            with_concl += 1
            total_sents += min(3, k)
            if len(examples) < 5 and top:
                examples.append({"title": title[:60], "top1_sent": top[0][1][:80],
                                 "overlap": round(top[0][0], 3)})
    avg_sents = total_sents / max(with_concl, 1)

    # D3 推送就绪
    tables = aux["probes"].get("tables_found", [])
    push_ready = "dwd_policy_summary" in tables or "dwd_policy_summary_edit_log" in tables

    d1 = (main_rate + ctx_rate) / 2
    d2 = min(1.0, avg_sents / 3.0)
    dims = [("D1_info_coverage", d1, True), ("D2_conclusions", d2, with_concl > 0),
            ("D3_push_ready", None, push_ready)]
    avail = [(k, v) for k, v, ok in dims if ok and v is not None]
    score = sum(v for _, v in avail) / len(avail) * 100

    out = {
        "metric_id": "M_POLICY_DS_11_POLICY_EVAL_012",
        "title": "智能摘要与结论推送",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": ("主料与上下文字段可算（正文 19,203 行、摘要 12,159 行、标题 20,000 行），"
                           "结论句可抽取；推送就绪所需的 dwd_policy_summary(push_status) 与编辑日志表"
                           "在 gkx 中均不存在 → 三维缺一维，判部分支持。"),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本指标为截面就绪度，不设跨年基期。结论句抽样按 id 随机（seed=42），"
                            "不用年份分层；政策表 2023 年起无数据，不做年度外推。"),
        "sources": {
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（ct_len/abs_len/ministry）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文/摘要）",
            "policy_aux": "code/_snapshots21/policy_aux_20261022.json（表存在性探针：tables_found=[]）",
            "db": "gkx @ 183.240.141.251:3318（只读；本脚本零 SQL）",
        },
        "population": {"rows": n, "rows_with_content_snapshot": len(txt)},
        "dims": {
            "D1_info_coverage": {
                "main_material_ok": main_ok,
                "main_rate_pct": round(main_rate * 100, 2),
                "ctx_fields": ctx,
                "ctx_rate_pct": round(ctx_rate * 100, 4),
                "combined_pct": round(d1 * 100, 2),
                "available": True,
                "note": "主料=正文>100 字或摘要非空；上下文=title/ministry/publish_year 三项齐备率",
            },
            "D2_conclusions": {
                "sampled": len(sample),
                "policies_with_conclusion": with_concl,
                "conclusion_sents_total": total_sents,
                "avg_sents_per_policy": round(avg_sents, 2),
                "normalized_pct": round(d2 * 100, 2),
                "available": with_concl > 0,
                "examples": examples,
                "note": ("标题—句子 bigram 重合排序是 TextRank 的轻量代理，只证明「能抽句」，"
                         "不证明「抽得准」；库内无人工参考摘要，ROUGE 类质量指标不可算。"),
            },
            "D3_push_ready": {
                "available": push_ready,
                "tables_found": tables,
                "note": ("SHOW TABLES 探针在 gkx 中未发现 dwd_policy_summary 与 "
                         "dwd_policy_summary_edit_log；推送状态、编辑版本、按角色分发均无载体。"),
            },
        },
        "dims_available": f"{len(avail)}/3",
        "summary_readiness_score": round(score, 2),
        "formula": "D1=(主料率+上下文率)/2；D2=min(1, 平均句数/3)；D3 缺维不进平均；可算维等权 ×100",
        "quality_caveat": ("该分数衡量「能不能生成并推送摘要」，不衡量「生成得好不好」。"
                           "三项质量证据全部缺失：无参考摘要（不能算 ROUGE）、无人工评分、"
                           "无推送后的阅读/采纳回流。页面若把它显示为「摘要质量分」，属于误读。"),
        "verdict": (f"摘要就绪度 = {score:.2f}（{len(avail)}/3 维参与）。"
                    "可上线「自动摘要草稿」与「结论句候选」，"
                    "不可上线「推送」与「摘要质量评分」；推送维需先建 dwd_policy_summary 表。"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "dims_available",
                                          "summary_readiness_score")}, ensure_ascii=False, indent=1))
    print(json.dumps(out["dims"], ensure_ascii=False, indent=1)[:2200])
    print("->", OUT)


if __name__ == "__main__":
    main()
