#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TNIE_EVENT_COUNT｜抽取事件条数。

零 SQL，只读 `code/_snapshots21/f3_facts_20261023.json`。

结论先行：
  - 真事件计数**不可建**。`dwd_event` 只有 20 行，且 20 行全部落在 2026-05-13/14
    两天，是国药励展（Reed Sinopharm）单一展会系列，不是通用事件表；
  - `innovation_event` / `dwd_innovation_event` 在 gkx 逐字命中 0 张表；
  - 注册表 source_tables 里的 `ads_tech_news_extraction` / `ads_tech_news_event` /
    `sandbox_sqlite_extractions` 也全部 0 张表。
  - 唯一可交的是**代理口径**：`dwd_org_important_news_info` 里标题含
    「论坛/大会/峰会/展会/博览会/发布会/研讨会/交易会/年会/仪式」的报道条数。
    每一条都必须带「代理口径：媒体报道 ≠ 事件发生」。

运行：`cd code && python3 M_TNIE_EVENT_COUNT.py`
产物：`code/M_TNIE_EVENT_COUNT_out.json`
"""
from __future__ import annotations

import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_TNIE_EVENT_COUNT_out.json")


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

    event_days = 2  # 2026-05-13 至 2026-05-14（含首尾）
    derived = {
        "events_per_day": ratio(
            ev["rows"], event_days,
            "分母 = dwd_event 覆盖的自然日数 2（2026-05-13 至 2026-05-14）；分子 = 20 行"),
        "expo_word_share_pct": pct(
            ev["name_has_expo_word"], ev["rows"],
            "分母 = dwd_event 20 行；分子 = event_name 含论坛/大会/展会/博览会/交易会的 17 行"),
        "medicine_share_pct": pct(
            ev["name_has_medicine"], ev["rows"],
            "分母 = dwd_event 20 行；分子 = event_name 含“医药”的 10 行"),
        "event_table_share_of_news_pct": pct(
            ev["rows"], news["rows"],
            "分母 = dwd_org_important_news_info 1,668,414 条报道；分子 = dwd_event 20 行"),
        "proxy_report_share_all_pct": pct(
            news["event_title_rows_all"], news["rows"],
            "代理口径：分母 = 全库报道 1,668,414 条；分子 = 标题含 10 个活动词的 18,884 条"),
        "proxy_report_share_since2025_pct": pct(
            news["event_title_rows_since_2025"], news["rows_since_2025"],
            "代理口径：分母 = 2025-01-01 起报道 518,531 条；分子 = 同期活动词标题 6,213 条"),
        "proxy_reports_per_org_since2025": ratio(
            news["event_title_rows_since_2025"], news["distinct_org"],
            "代理口径：分母 = 28,123 家覆盖企业；分子 = 2025 起活动词标题 6,213 条"),
    }

    out = {
        "metric_id": "M_TNIE_EVENT_COUNT",
        "metric_name_zh": "抽取事件条数",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "support_judgment": "部分支持",
        "verdict_kind": "proxy_partial",
        "judgment_reason": (
            "真事件计数不可建：`dwd_event` 仅 20 行、只覆盖 2026-05-13/14 两天、"
            "20 个名称 19 个组织者全部是国药励展系展会；事件表与抽取结果表在 gkx 均 0 张。"
            "只能交「媒体报道中的活动型标题条数」代理，且逐条标注媒体≠事件，故判部分支持。"
        ),
        "official_event_count": {
            "value": None,
            "status": "rejected",
            "reason": "没有通用事件表；20 行单一展会系列不构成事件面，不能当事件条数。",
        },
        "event_table": {
            "rows": ev["rows"],
            "date_min": ev["date_min"],
            "date_max": ev["date_max"],
            "distinct_event_name": ev["distinct_event_name"],
            "distinct_organizer": ev["distinct_organizer"],
            "name_has_expo_word": ev["name_has_expo_word"],
            "name_has_medicine": ev["name_has_medicine"],
            "organizer_top": ev["organizer_top"],
            "single_series_evidence": (
                "20 行日期全部是 2026-05-13 或 2026-05-14；组织者 top5 全部含“国药励展”；"
                "event_url 全部指向 mm.reed-sinopharm.com 同一站点。"
            ),
        },
        "proxy": {
            "caliber": "代理口径：媒体报道 ≠ 事件发生",
            "source_table": "gkx.dwd_org_important_news_info",
            "rows_total": news["rows"],
            "distinct_org": news["distinct_org"],
            "date_min": news["date_min"],
            "date_max": news["date_max"],
            "event_words": news["event_words"],
            "event_title_rows_all": news["event_title_rows_all"],
            "event_title_rows_since_2025": news["event_title_rows_since_2025"],
            "rows_since_2025": news["rows_since_2025"],
            "not_an_event_count": True,
        },
        "chain_news_context": {
            "rows": f3["dwd_industry_chain_news_info"]["rows"],
            "year_counts": f3["dwd_industry_chain_news_info"]["year_counts"],
            "role": "产业链新闻条数，只作媒体面背景，不是事件计数",
        },
        "base_years_used": [2025, 2026],
        "base_years_missing": [],
        "base_years_note": (
            "事件表只有 2026-05-13/14 两天；代理口径取 2025-01-01 起（media 表 2026 只到 05-08，"
            "是残年）。2018—2024 的报道存在但本件不做年度事件序列，故不进基期；"
            "不把 2026 残年摊成全年。"
        ),
        "sources": [
            {"path": "code/_snapshots21/f3_facts_20261023.json",
             "what": "dwd_event 20 行明细、dwd_org_important_news_info 总量与活动词标题计数、负证据"},
        ],
        "derived": derived,
        "absence_probe": {
            "dwd_innovation_event": f3["absence_probe"]["dwd_innovation_event"],
            "innovation_event": f3["absence_probe"]["innovation_event"],
            "ads_tech_news_extraction": f3["absence_probe"]["ads_tech_news_extraction"],
            "ads_tech_news_event": f3["absence_probe"]["ads_tech_news_event"],
            "sandbox_sqlite_extractions": f3["absence_probe"]["sandbox_sqlite_extractions"],
            "dwd_event": {
                "condition": "information_schema.tables WHERE table_schema='gkx' AND table_name='dwd_event'",
                "hits": 1,
                "rows": ev["rows"],
                "verdict": "表存在但只有 20 行单一展会系列，不能建通用事件计数",
            },
        },
        "reproduce": "cd code && python3 M_TNIE_EVENT_COUNT.py",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {OUT} event_rows={ev['rows']} proxy_all={news['event_title_rows_all']} "
          f"proxy_since2025={news['event_title_rows_since_2025']}")


if __name__ == "__main__":
    main()
