#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_DEV_HISTORY「企业发展历程」→ `code/M_ENT_DEV_HISTORY_out.json`

口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_DEV_HISTORY.md`）：
    每企一条 timeline = 三类事件 UNION 后按时间倒序：
      ① 财务年报（enterprise_finance_history，一行一事，时间= data_year，只带 revenue / net_profit）
      ② 专利年统计（enterprise_patent_history，一行一事，时间= apdt_year 申请年）
      ③ 重点资讯（enterprise_news，一行一事，时间= publish_time）
    无独立目标表 `enterprise_dev_history`（两库均无）；国外财务本波不并；
    禁止把 CMS / expert_knowledge / 明星企业故事当源；禁止做并购/上市/股权变更阈值识别。

本脚本零 DB，只读两份共享快照：
    `code/_snapshots21/ent_fin_family_20261023.json`（财务/资讯/交集的原始计数）
    `code/_snapshots21/patent_panel_innov_20261021.json`（专利 app_year 面板，经族快照二次汇总）

重跑：`cd code && python3 M_ENT_DEV_HISTORY.py`
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_fin_family_20261023.json")
OUT = os.path.join(HERE, "M_ENT_DEV_HISTORY_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    fin, news, pat, asset = d["annual_fin"], d["news"], d["patent_year"], d["asset_text"]
    cs = d["cross_stream"]
    base_orgs = d["base"]["orgs"]

    union = sum(cs["only_one"].values()) + cs["at_least_two"]
    headline = {
        "target_table": "enterprise_dev_history",
        "target_table_in_gkx": "enterprise_dev_history" in d["result_surfaces"]["found_in_gkx"],
        "target_absent": d["result_surfaces"]["absent_in_gkx"],
        "stream_finance_rows": fin["rows"],
        "stream_finance_orgs": cs["stream_sizes"]["financial"],
        "stream_finance_orgs_multi_year": fin["orgs_series_multi_year"],
        "stream_finance_years": [r[0] for r in fin["year_dist"] if r[3] > 0],
        "stream_patent_pairs": pat["app_year_pairs"],
        "stream_patent_applicants": pat["applicants_total"],
        "stream_patent_applicants_matched": pat["applicants_matched_base"],
        "stream_patent_orgs": cs["stream_sizes"]["patent"],
        "stream_patent_pairs_matched": pat["applicant_year_pairs_matched"],
        "stream_patent_patents_matched": pat["patents_matched"],
        "stream_patent_years": sorted(pat["year_totals"]),
        "stream_news_rows": news["rows"],
        "stream_news_orgs": cs["stream_sizes"]["news"],
        "stream_news_span": [news["date_min"], news["date_max"]],
        "stream_asset_rows": asset["parsed_rows"],
        "stream_asset_orgs": cs["stream_sizes"]["asset_text"],
        "coverage": {
            "base_orgs": base_orgs,
            "orgs_with_any_event": union,
            "orgs_with_any_event_pct": pct(union, base_orgs),
            "at_least_two_streams": cs["at_least_two"],
            "at_least_two_pct": pct(cs["at_least_two"], base_orgs),
            "at_least_three_streams": cs["at_least_three"],
            "all_four_streams": cs["all_four"],
            "only_one_stream": cs["only_one"],
            "pairwise": cs["pairwise"],
        },
        "event_counts": {
            "finance_rows_usable": fin["fill"]["operating_revenue"]["nonnull"]
                                    + fin["fill"]["pure_profit"]["nonnull"],
            "finance_rows_revenue": fin["fill"]["operating_revenue"]["nonnull"],
            "finance_rows_profit": fin["fill"]["pure_profit"]["nonnull"],
            "news_rows_in_base": news["rows_in_base"],
            "patent_pairs_matched": pat["applicant_year_pairs_matched"],
        },
        "year_windows": {
            "finance": [min(r[0] for r in fin["year_dist"] if r[3] > 0),
                        max(r[0] for r in fin["year_dist"] if r[3] > 0)],
            "patent_apply_year": [min(pat["year_totals"]), max(pat["year_totals"])],
            "news_date": [news["date_min"], news["date_max"]],
        },
        "note": "四条流的机构集合互不求并：财务 %d 家、资产表 %d 家、资讯 %d 家、"
                "专利（按第一申请人名称命中底册）%d 家；有任意一类事件的机构 %d 家（占底册 %s%%），"
                "两类及以上 %d 家" % (cs["stream_sizes"]["financial"], cs["stream_sizes"]["asset_text"],
                                   cs["stream_sizes"]["news"], cs["stream_sizes"]["patent"],
                                   union, pct(union, base_orgs), cs["at_least_two"]),
    }

    out = {
        "metric_id": "M_ENT_DEV_HISTORY",
        "metric_name": "企业发展历程",
        "support_judgment": "部分支持",
        "judgment_basis": {
            "formula": "UNION(finance_year, patent_apply_year, news_date) ORDER BY event_time DESC",
            "source_tables": ["gkx.dwd_org_annual_financial_info",
                              "gkx.dwd_patent（经 patent_panel_innov_20261021 的 app_year 面板）",
                              "gkx.dwd_org_important_news_info"],
            "why_partial": "三流原料齐全且都能落成「org_id + event_time + event_type」，"
                           "但①目标表 enterprise_dev_history 两库均无（结果无处落）；"
                           "②财务事件只有 1,302 家（0.6885%）、资讯只有 28,118 家（14.8699%），"
                           "专利流只覆盖 2021—2024 四个申请年——时间线的「早段」与「后段」都缺",
            "why_not_direct": "无 enterprise_dev_history / enterprise_timeline* 结果面，"
                              "gkx 280 表精确同名检索为 0",
            "why_not_unsupported": "三流各自的行级字段（年 / 申请年 / 日期）齐备，"
                                   "事件类型可枚举，能构成一行一事的结构",
        },
        "sources": [
            {"db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp（只读）",
             "table": "gkx.dwd_org_annual_financial_info", "rows": fin["rows"]},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_important_news_info", "rows": news["rows"]},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_patent", "rows": 2939895,
             "note": "本件不重扫，读已完成的 app_year 面板（275,135 个「申请年|第一申请人」对）"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_report_asset", "rows": asset["rows_all"],
             "note": "财务事件的补充流（文本万元），calc-logic 未声明，只作覆盖上限参考"},
            {"snapshot": "code/_snapshots21/ent_fin_family_20261023.json",
             "builder": "code/_build_ent_fin_family.py"},
            {"snapshot": "code/_snapshots21/patent_panel_innov_20261021.json",
             "note": "app_year 面板来源；件数口径=按公开件计，未做同族合并"},
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2018, 2019, 2020, 2025, 2026],
        "base_years_note": "专利事件只能用申请年 2021—2024（面板 app_year 仅这四年有「申请人-年」对；"
                           "2025/2026 虽有件数但未按申请人分年，2018—2020 库内零行）。"
                           "资讯事件 2018-01 至 2026-05 全窗可用；财务事件按各企实际年份。"
                           "三段窗口不齐是「时间线首尾薄」的直接原因，未按 0 补齐",
        "headline": headline,
        "derived": {
            "only_one_total": dec(
                sum(cs["only_one"].values()), sum(cs["only_one"].values()), None,
                "计数，无分母：只出现在 1 条事件流里的机构数（only_one 四流相加：财务 103+资产 1,626"
                "+资讯 12,259+专利 121,946＝135,934 家）"),
            "union_check": dec(
                union, sum(cs["only_one"].values()) + cs["at_least_two"], None,
                "计数，无分母：有任意一类事件的机构数 = 只在 1 流的 135,934 家 + 两类及以上 17,617 家"
                "（＝headline.coverage.orgs_with_any_event，用于与底册覆盖率互校）"),
            "finance_orgs_pct": dec(
                pct(cs["stream_sizes"]["financial"], base_orgs),
                cs["stream_sizes"]["financial"], base_orgs,
                "分子=有财务年报事件的机构数 cross_stream.stream_sizes.financial（1,416 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "asset_orgs_pct": dec(
                pct(cs["stream_sizes"]["asset_text"], base_orgs),
                cs["stream_sizes"]["asset_text"], base_orgs,
                "分子=年报资产表有可解析营收的机构数 cross_stream.stream_sizes.asset_text（7,738 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "news_orgs_pct": dec(
                pct(cs["stream_sizes"]["news"], base_orgs),
                cs["stream_sizes"]["news"], base_orgs,
                "分子=有重点资讯事件的机构数 cross_stream.stream_sizes.news（28,123 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "patent_orgs_pct": dec(
                pct(cs["stream_sizes"]["patent"], base_orgs),
                cs["stream_sizes"]["patent"], base_orgs,
                "分子=按第一申请人名称命中底册的专利流机构数 cross_stream.stream_sizes.patent（137,448 家）；"
                "分母=四市底册法人总数 base.orgs（189,116 家）"),
            "patent_orgs_minus_applicants": dec(
                cs["stream_sizes"]["patent"] - pat["applicants_matched_base"],
                cs["stream_sizes"]["patent"] - pat["applicants_matched_base"], None,
                "计数，无分母：专利流机构数 137,448（stream_sizes.patent）− 命中底册的第一申请人名称数"
                "137,441（patent_year.applicants_matched_base）＝ 7；差额来自 47 组同名的两家企业被同时计入"),
            "news_share_of_rows_pct": dec(
                pct(news["rows"], news["rows"] + fin["rows"]),
                news["rows"], news["rows"] + fin["rows"],
                "分子=重点资讯行数 news.rows（1,668,414 行）；"
                "分母=资讯+财务两流行数合计（1,668,414 + 90,926 ＝ 1,759,340 行）；"
                "专利流按「申请人-年」对计、量纲不同，故不进此分母"),
            "finance_share_of_rows_pct": dec(
                pct(fin["rows"], news["rows"] + fin["rows"]),
                fin["rows"], news["rows"] + fin["rows"],
                "分子=财务年报行数 fin.rows（90,926 行）；"
                "分母=资讯+财务两流行数合计（1,759,340 行）。与 news_share_of_rows_pct 同分母互补"),
            "applicant_match_pct": dec(
                pct(pat["applicants_matched_base"], pat["applicants_total"]),
                pat["applicants_matched_base"], pat["applicants_total"],
                "分子=第一申请人名称能在底册 189,116 个 name 中精确命中的个数"
                "（patent_year.applicants_matched_base，137,441 个）；"
                "分母=专利面板里去重后的第一申请人名称总数 applicants_total（146,915 个）"),
            "news_per_org": dec(
                round(news["rows"] / news["distinct_orgs"], 4),
                news["rows"], news["distinct_orgs"],
                "分子=重点资讯行数 news.rows（1,668,414 行）；"
                "分母=有资讯的去重机构数 news.distinct_orgs（28,123 家）"),
            "patent_pairs_per_org": dec(
                round(pat["applicant_year_pairs_matched"] / cs["stream_sizes"]["patent"], 4),
                pat["applicant_year_pairs_matched"], cs["stream_sizes"]["patent"],
                "分子=命中底册的「申请年|第一申请人」对数 patent_year.applicant_year_pairs_matched（259,338 对）；"
                "分母=专利流机构数 cross_stream.stream_sizes.patent（137,448 家）"),
            "finance_rows_per_org": dec(
                round(fin["rows"] / cs["stream_sizes"]["financial"], 4),
                fin["rows"], cs["stream_sizes"]["financial"],
                "分子=财务年报行数 fin.rows（90,926 行）；"
                "分母=有财务事件的机构数 cross_stream.stream_sizes.financial（1,416 家）"),
            "news_rows_in_base_pct": dec(
                pct(news["rows_in_base"], news["rows"]), news["rows_in_base"], news["rows"],
                "分子=org_id 能对上底册的资讯行数 news.rows_in_base（1,668,408 行）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
            "news_max_org_share_pct": dec(
                pct(news["per_org_rows"]["max"], news["rows"]),
                news["per_org_rows"]["max"], news["rows"],
                "分子=单家机构最多资讯条数 news.per_org_rows.max（138,222 条）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
            "news_top10_rows": dec(
                sum(o["news_rows"] for o in news["top10_orgs"]),
                sum(o["news_rows"] for o in news["top10_orgs"]), None,
                "计数，无分母：资讯条数前 10 家机构行数合计（news.top10_orgs[].news_rows 求和，330,331 行）"),
            "news_top10_share_pct": dec(
                pct(sum(o["news_rows"] for o in news["top10_orgs"]), news["rows"]),
                sum(o["news_rows"] for o in news["top10_orgs"]), news["rows"],
                "分子=资讯条数前 10 家机构行数合计（330,331 行）；"
                "分母=重点资讯全表行数 news.rows（1,668,414 行）"),
        },
        "cross_stream": cs,
        "patent_detail": pat,
        "news_detail": {
            "rows": news["rows"], "orgs": news["distinct_orgs"],
            "orgs_in_base": news["orgs_in_base"], "rows_in_base": news["rows_in_base"],
            "yearly": news["yearly"], "date_min": news["date_min"], "date_max": news["date_max"],
            "per_org_rows": news["per_org_rows"],
            "top10_orgs": news["top10_orgs"],
            "dup_sample": d.get("news_dup_sample", {}),
        },
        "finance_detail": {
            "rows": fin["rows"], "orgs": fin["orgs"],
            "orgs_series": fin["orgs_series"], "orgs_series_multi_year": fin["orgs_series_multi_year"],
            "revenue_nonnull_rows": fin["fill"]["operating_revenue"]["nonnull"],
            "profit_nonnull_rows": fin["fill"]["pure_profit"]["nonnull"],
            "latest_year_dist": fin["latest_year_dist"],
        },
        "caveats": [
            "财务事件「一行一事」= 一条年度记录；同一年多张报表时不去重（本库一企一年一行，实测无重）",
            "专利事件按申请年归桶，不是授权年；库里没有授权日可用，不能切「授权发生年」",
            "资讯事件占绝对多数：1,668,414 行 vs 财务 90,926 行，若直接 UNION，"
            "时间线会被资讯淹没（资讯前 10 家占 12.1%），页面必须分事件类型过滤",
            "目标表不存在 → 当前只能出「加工后暂存」，不能在页面假装已从 enterprise_dev_history 读取",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(headline, ensure_ascii=False, indent=1)[:2500])
    print("->", OUT)


if __name__ == "__main__":
    main()
