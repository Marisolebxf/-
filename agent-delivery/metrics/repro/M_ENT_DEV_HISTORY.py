#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_DEV_HISTORY 企业发展历程
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_DEV_HISTORY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_ENT_DEV_HISTORY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_DEV_HISTORY.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_ENT_DEV_HISTORY",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
