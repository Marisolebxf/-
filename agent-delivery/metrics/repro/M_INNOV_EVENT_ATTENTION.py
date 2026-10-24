#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_EVENT_ATTENTION｜事件关注度 —— 负证据件。

判定：**完全不支持**。事件关注度这一维拒拟，理由分三层：
  1. 事件面不存在：`innovation_event` / `dwd_innovation_event` 逐字命中 0 张表；
     `dwd_event` 只有 20 行，全部是 2026-05-13/14 的国药励展系展会，不是通用事件面。
  2. 正本口径也不可算：`calc-logic/INNOV/M_INNOV_EVENT_ATTENTION.md` 定义在
     `dwd_policy_base` 的 `content/abstract`、`theme`、`quote_policy` 上，而
     `theme` 与 `quote_policy` 各只有 2 行真值（19,998 行是字符串 'NULL'），
     `policy_support` 20,000 行全是 JSON null。
  3. 专利被引**不是**事件关注：引文表 20,031 行 / 144,020 次被引只能说明论文影响，
     本件明确不拿它冒充事件关注，只在 `patent_citation_context` 里作对照留痕。

可交的替代口径只有一个：`dwd_org_important_news_info` 的报道条数/覆盖企业数，
且必须写「媒体关注 ≠ 事件关注」。替代读数不是本指标的值。

运行：`cd code && python3 M_INNOV_EVENT_ATTENTION.py`
产物：`code/M_INNOV_EVENT_ATTENTION_out.json`
"""
from __future__ import annotations

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "_snapshots21")
OFFICIAL = os.path.join(ROOT, "第三方库指标计算过程")
OUT = os.path.join(HERE, "M_INNOV_EVENT_ATTENTION_out.json")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def pct(num, den, note, digits=4):
    return {
        "value": round(num / den * 100, digits) if den else None,
        "numerator": num,
        "denominator": den,
        "denominator_note": note,
    }


def ratio(num, den, note, digits=4):
    return {
        "value": round(num / den, digits) if den else None,
        "numerator": num,
        "denominator": den,
        "denominator_note": note,
    }


def main() -> None:
    f3 = load("f3_facts_20261023.json")
    ev = f3["dwd_event"]
    news = f3["dwd_org_important_news_info"]
    cit = f3["dwd_zh_paper_citation"]

    # 正本公式依赖的死列：从正式区兄弟件读，不自己重跑
    policy_md = os.path.join(OFFICIAL, "M_POLICY_RELATION_DEGREE.md")
    assert os.path.exists(policy_md), "正式区缺 M_POLICY_RELATION_DEGREE.md"
    with open(os.path.join(HERE, "M_POLICY_RELATION_DEGREE_out.json"), encoding="utf-8") as fh:
        field_truth = json.load(fh)["field_truth"]

    derived = {
        "media_rows_per_org": ratio(
            news["rows"], news["distinct_org"],
            "分母 = 28,123 家有报道的企业；分子 = 1,668,414 条报道"),
        "org_coverage_of_base_pct": pct(
            news["distinct_org"], 189116,
            "分母 = 企业底册 189,116 家（共享常量）；分子 = 有报道企业 28,123 家"),
        "rows_since_2025_share_pct": pct(
            news["rows_since_2025"], news["rows"],
            "分母 = 全部报道 1,668,414 条；分子 = 2025-01-01 起 518,531 条"),
        "y2023_share_pct": pct(
            news["y2023"], news["rows"],
            "分母 = 全部报道；分子 = 2023 年 308,765 条"),
        "y2024_share_pct": pct(
            news["y2024"], news["rows"],
            "分母 = 全部报道；分子 = 2024 年 366,413 条"),
        "y2025_share_pct": pct(
            news["y2025"], news["rows"],
            "分母 = 全部报道；分子 = 2025 年 421,067 条"),
        "y2026_share_pct": pct(
            news["y2026"], news["rows"],
            "分母 = 全部报道；分子 = 2026 年 97,464 条（只到 05-08，残年）"),
        "event_like_share_pct": pct(
            news["event_title_rows_all"], news["rows"],
            "分母 = 全部报道；分子 = 活动词标题 18,884 条（媒体代理，不是事件）"),
        "quote_policy_dead_pct": pct(
            field_truth["quote_policy_rows_literal_null"], 20000,
            "分母 = dwd_policy_base 20,000 行；分子 = quote_policy 为字符串 'NULL' 的 19,998 行"),
        "theme_dead_pct": pct(
            20000 - field_truth["theme_rows_real"], 20000,
            "分母 = dwd_policy_base 20,000 行；分子 = theme 非真值的 19,998 行"),
        "patent_citation_per_paper": ratio(
            cit["citation_sum"], cit["rows"],
            "仅作对照：分母 = 有引文记录的 20,031 篇；分子 = 144,020 次被引。"
            "这不是事件关注度，不得替代"),
    }

    out = {
        "metric_id": "M_INNOV_EVENT_ATTENTION",
        "metric_name_zh": "事件关注度",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "事件关注度需要事件面；gkx 无事件表（innovation_event / dwd_innovation_event 逐字 0），"
            "`dwd_event` 20 行且是单一展会系列；正本依赖的 policy 文本三维中 theme/quote_policy "
            "各 19,998/20,000 是字符串 'NULL'。三个来源同时断掉，故判完全不支持，"
            "不构造分数、不拿专利被引冒充。"
        ),
        "rejected_dimensions": [
            {"dimension": "事件关注度（正本三维：正文规模/主题覆盖/引用政策数）",
             "status": "拒拟",
             "reason": "事件面缺失；正本 source_table dwd_policy_base 的 theme/quote_policy 基本全空"},
            {"dimension": "专利被引→事件关注",
             "status": "禁止替代",
             "reason": "专利被引是论文/专利影响，不是事件被报道/被讨论；见专利被引对照，不参与结论"},
        ],
        "event_face": {
            "innovation_event_hits": f3["absence_probe"]["innovation_event"]["hits"],
            "dwd_innovation_event_hits": f3["absence_probe"]["dwd_innovation_event"]["hits"],
            "dwd_event_rows": ev["rows"],
            "dwd_event_date_min": ev["date_min"],
            "dwd_event_date_max": ev["date_max"],
            "dwd_event_distinct_name": ev["distinct_event_name"],
            "single_series_evidence": (
                "20 行只覆盖 2026-05-13 与 2026-05-14 两天，组织者 top5 全含“国药励展”，"
                "event_url 全部指向 mm.reed-sinopharm.com；这是单一展会系列，不是事件面。"
            ),
        },
        "policy_formula_break": {
            "calc_logic_ref": "metrics/calc-logic/INNOV/M_INNOV_EVENT_ATTENTION.md",
            "source_table": "dwd_policy_base",
            "field_truth": field_truth,
            "verdict": "正文规模可用（content 19,203 行有值），但主题覆盖与引用政策数两维几乎全空；"
                       "三维等权公式实际只剩一维，不能出 0—100 分。",
        },
        "media_attention_alternative": {
            "caliber": "替代口径：媒体关注 ≠ 事件关注",
            "source_table": "gkx.dwd_org_important_news_info",
            "rows": news["rows"],
            "distinct_org": news["distinct_org"],
            # 2026-10-23 补：口径脚注。复核时我按 name_cn 去重得 28,154，与 28,123 不符，
            # 差点判成错数——实为同一 org_id 有多种名称写法。写进产物，省得下一个人再查一遍。
            "distinct_org_caliber": ("按 COUNT(DISTINCT org_id) 计；按 name_cn 去重为 28,154，"
                                      "差额是同一 org_id 的不同写法，家数一律按 org_id 计"),
            "date_min": news["date_min"],
            "date_max": news["date_max"],
            "rows_since_2025": news["rows_since_2025"],
            "y2023": news["y2023"],
            "y2024": news["y2024"],
            "y2025": news["y2025"],
            "y2026": news["y2026"],
            "event_title_rows_all": news["event_title_rows_all"],
            "not_the_metric": True,
        },
        "patent_citation_context": {
            "rows": cit["rows"],
            "citation_sum": cit["citation_sum"],
            "citation_avg": cit["citation_avg"],
            "used_as_event_attention": False,
            "note": "只作“禁止替代”的对照值；本件任何结论都不使用这组数。",
        },
        "base_years_used": [2023, 2024, 2025, 2026],
        "base_years_missing": [],
        "base_years_note": (
            "媒体读数取 2023—2026 近窗；2026 只到 2026-05-08，是残年，不摊成全年。"
            "2018—2022 的报道存在，但本件只做近窗对照，不进基期；"
            "事件表只有 2026-05 两天，无法构成年度基期。"
        ),
        "sources": [
            {"path": "code/_snapshots21/f3_facts_20261023.json",
             "what": "dwd_event 20 行、dwd_org_important_news_info 年度与覆盖、引文表、负证据"},
            {"path": "code/M_POLICY_RELATION_DEGREE_out.json",
             "what": "dwd_policy_base 的 theme/quote_policy 真值行数（正式区兄弟件）"},
        ],
        "derived": derived,
        "absence_probe": {
            "innovation_event": f3["absence_probe"]["innovation_event"],
            "dwd_innovation_event": f3["absence_probe"]["dwd_innovation_event"],
            "dwd_event": {
                "condition": "information_schema.tables WHERE table_schema='gkx' AND table_name='dwd_event'",
                "hits": 1,
                "rows": ev["rows"],
                "verdict": "表存在但 20 行单一展会系列，不构成事件关注度的分母",
            },
            "dwd_policy_base": {
                "condition": "information_schema.tables WHERE table_schema='gkx' AND table_name='dwd_policy_base'",
                "hits": 1,
                "rows": 20000,
                "verdict": "正本源表存在，但 theme/quote_policy 各 19,998 行为字符串 'NULL'",
            },
        },
        "reproduce": "cd code && python3 M_INNOV_EVENT_ATTENTION.py",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {OUT} verdict=完全不支持 news={news['rows']} orgs={news['distinct_org']}")


if __name__ == "__main__":
    main()
