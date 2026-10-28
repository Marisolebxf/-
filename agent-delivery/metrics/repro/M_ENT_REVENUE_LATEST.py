#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_REVENUE_LATEST 营收
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库（D2 拆分后本件归算法库；系统侧变件 M_ENT_REVENUE_LATEST_ZT.py / M_ENT_REVENUE_LATEST_ZS.py）
# 【差异分级】D2 口径级分歧·不可兼容·方法型 → 拆分（判定见 ../过程文件/02_D2兼容判定与拆分_总结.md）
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_REVENUE_LATEST「营收（最新年度）」→ `code/M_ENT_REVENUE_LATEST_out.json`

口径（`gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REVENUE_LATEST.md`）：
    每企一条 = 该 org_id 的 MAX(data_year) 那一行 `operating_revenue`。
    无财务行 / 值为空 → 该企无法计算（不是整条指标无法执行）。
    不挂产业；国外对等表 0 行不并；禁止抄 `enterprise_base.revenue_latest`。

本脚本零 DB：主口径数字全部来自族级共享快照
`code/_snapshots21/ent_fin_family_20261023.json`（由 `code/_build_ent_fin_family.py` 扫库生成）。
「补充参考」段用同一格式的年度资产表（文本「万元」）与上市财务表做横向对照，**不合并、不加总**。

重跑：`cd code && python3 M_ENT_REVENUE_LATEST.py`
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21", "ent_fin_family_20261023.json")
OUT = os.path.join(HERE, "M_ENT_REVENUE_LATEST_out.json")


def pct(a, b):
    return round(a / b * 100, 4) if b else None


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量表达式。"""
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main():
    d = json.load(open(SNAP, encoding="utf-8"))
    fin, asset, stock = d["annual_fin"], d["asset_text"], d["stock_fin"]
    base_orgs = d["base"]["orgs"]

    st = fin["latest_stats"]
    years_used = [int(r[0]) for r in fin["year_dist"] if r[3] > 0 and r[0]]
    orgs_rev = fin["orgs_any_revenue"]
    ub = orgs_rev + asset["orgs_parsed"]
    ua = d.get("unit_audit", {})

    headline = {
        "annual_fin_rows": fin["rows"],
        "annual_fin_orgs": fin["orgs"],
        "revenue_nonnull_rows": fin["fill"]["operating_revenue"]["nonnull"],
        "revenue_null_rows": fin["revenue_null_rows"],
        "orgs_with_latest_revenue": orgs_rev,
        "coverage_pct_of_base": pct(orgs_rev, base_orgs),
        "base_orgs": base_orgs,
        "latest_rev_median_yuan": st["median"],
        "latest_rev_mean_yuan": st["mean"],
        "latest_rev_p10_yuan": st["p10"],
        "latest_rev_p90_yuan": st["p90"],
        "latest_rev_p99_yuan": st["p99"],
        "latest_rev_max_yuan": st["max"],
        "latest_rev_min_yuan": st["min"],
        "latest_rev_neg_orgs": st["neg"],
        "latest_rev_zero_orgs": st["zero"],
        "latest_year_dist": fin["latest_year_dist"],
        "unit_bands": fin["unit_bands"],
        "unit_band_note": "金额列是 double，库内不声明单位；以下 5 段按数值量级切，"
                          "用来暴露「元/万元」混填：<1e3 元段 207 家、1e3—1e4 元段 346 家，"
                          "两者合计 553 家不可能是一年的营业收入（最低 1 元级）",
        "asset_text_orgs": asset["orgs_parsed"],
        "asset_text_latest_positive_orgs": asset["latest_stats_yuan"]["n"],
        "asset_text_median_yuan": asset["latest_stats_yuan"]["median"],
        "asset_text_rows": asset["rows_all"],
        "asset_text_placeholder_rows": asset["placeholder_rows"],
        "asset_text_placeholder_pct": pct(asset["placeholder_rows"], asset["rows_all"]),
        "stock_orgs_with_revenue": stock["rev_pos_orgs"],
        "stock_rows": stock["rows"],
        "stock_period_max": stock["period_max"],
        "two_source_upper_bound_orgs": ub,
        "two_source_upper_bound_pct": pct(ub, base_orgs),
        "two_source_note": "fin 与 asset 是两张不同年报表，机构号未求交，"
                           "故只给「两表直接相加」的上界，不宣称并集",
        "unit_audit": {
            "pairs_compared": ua.get("pairs_compared"),
            "ratio_buckets": ua.get("ratio_buckets"),
            "mislabel_share_pct": ua.get("mislabel_share_pct"),
            "verdict": ua.get("verdict"),
            "action": ua.get("action"),
            "example": ua.get("example"),
            "authoritative_orgs_pos": ua.get("annual_fin_authoritative", {}).get("orgs_pos"),
            "authoritative_median_yuan": ua.get("annual_fin_authoritative", {}).get("stats", {}).get("median"),
            "authoritative_buckets": ua.get("annual_fin_authoritative", {}).get("buckets"),
            "anchor_ok": ua.get("annual_fin_authoritative", {}).get("anchor_ok"),
        },
    }

    out = {
        "metric_id": "M_ENT_REVENUE_LATEST",
        "metric_name": "营收（最新年度营业收入）",
        "support_judgment": "部分支持",
        "judgment_basis": {
            "formula": "revenue = operating_revenue @ MAX(year) per org",
            "source_table": "gkx.dwd_org_annual_financial_info（calc-logic 声明的唯一输入）",
            "why_partial": "结构与规则完整、可按企取最新年；但 8,127 家有财务行的机构里"
                           "只有 1,302 家（占底册 0.6885%）在最新年有营收值，"
                           "其余 6,825 家最新年该列为空——覆盖不足是数据缺口，不是口径缺口",
            "why_not_direct": "两库均无 enterprise_finance_history / enterprise_base.revenue_latest "
                              "结果面，须按企取最新年现算",
            "why_not_unsupported": "依赖表、年份列、机构号键齐全，1,302 家已能算出完整一条（含最新年标记）",
        },
        "sources": [
            {"db": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp（只读）",
             "table": "gkx.dwd_org_annual_financial_info", "rows": fin["rows"],
             "note": "26 列宽表，uk_org_id_year 有索引；本次窄投影 4 列 + 底册 LEFT JOIN 取名/城市"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_report_asset", "rows": asset["rows_all"],
             "note": "补充参考：xsze 为「数值+万元」文本，正则取数并换算元"},
            {"db": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_stock_finance_info", "rows": stock["rows"],
             "note": "补充参考：上市口径，calc-logic 未声明可替代年报"},
            {"snapshot": "code/_snapshots21/ent_fin_family_20261023.json",
             "builder": "code/_build_ent_fin_family.py"},
        ],
        "base_years_used": years_used,
        "base_years_missing": [],
        "base_years_note": "按企取「最新年」，各企锚年不同（见 latest_year_dist）；"
                           "库内财务年表年份区间 %s—%s 全部在扫描范围内，无排除年。"
                           "某企最新年营收为空时该企不计入，不向前补年、不写 0"
                           % (years_used[0], years_used[-1]),
        "headline": headline,
        "derived": {
            "orgs_without_latest_revenue": dec(
                fin["orgs"] - orgs_rev, fin["orgs"] - orgs_rev, None,
                "计数，无分母：有财务行的机构 8,127 家（annual_fin.orgs）− 最新年营收非空的 1,302 家"
                "（orgs_any_revenue）＝ 6,825 家，最新年该列为空，不向前补年、不写 0"),
            "fin_org_coverage_pct": dec(
                pct(orgs_rev, fin["orgs"]), orgs_rev, fin["orgs"],
                "分子=最新年营收非空的机构数 annual_fin.orgs_any_revenue（1,302 家）；"
                "分母=有财务行的机构数 annual_fin.orgs（8,127 家）。"
                "注意与 headline.coverage_pct_of_base（分母 189,116 底册）不是同一个分母"),
            "rev_rows_share_pct": dec(
                pct(fin["fill"]["operating_revenue"]["nonnull"], fin["rows"]),
                fin["fill"]["operating_revenue"]["nonnull"], fin["rows"],
                "分子=营收列非空的财务行数 fill.operating_revenue.nonnull（2,193 行）；"
                "分母=财务年报表总行数 annual_fin.rows（90,926 行）"),
            "bands_below_10k": dec(
                fin["unit_bands"]["lt_1e3"] + fin["unit_bands"]["1e3_1e4"],
                fin["unit_bands"]["lt_1e3"] + fin["unit_bands"]["1e3_1e4"], None,
                "计数，无分母：最新营收落在 <1e3 元段 207 家 + 1e3—1e4 元段 346 家 ＝ 553 家，"
                "两段合计即「一年营收不足 1 万元」的不合理量级企业数"),
            "buckets_under_100_yuan": dec(
                ua.get("annual_fin_authoritative", {}).get("buckets", {}).get("<=100元(明显错值)"),
                ua.get("annual_fin_authoritative", {}).get("buckets", {}).get("<=100元(明显错值)"), None,
                "计数，无分母：外部锚定校验（unit_audit.annual_fin_authoritative.buckets）里"
                "最新营收 ≤100 元、判为明显错值的机构数"),
            "usable_ge_1e8": dec(
                fin["unit_bands"]["ge_1e8"], fin["unit_bands"]["ge_1e8"], None,
                "计数，无分母：最新营收 ≥1e8 元（1 亿元）的机构数（annual_fin.unit_bands.ge_1e8）"),
            "asset_parsed_share_pct": dec(
                pct(asset["parsed_rows"], asset["xsze_wan_rows"]),
                asset["parsed_rows"], asset["xsze_wan_rows"],
                "分子=能按「数值+万元」正则解析出行数 asset_text.parsed_rows（12,616 行）；"
                "分母=营收文本列非空的候选行数 asset_text.xsze_wan_rows（12,621 行）；"
                "其余 514,140 行是「企业选择不公示」占位串，未进分母"),
            "asset_latest_positive_share_pct": dec(
                pct(asset["latest_stats_yuan"]["n"], asset["orgs_parsed"]),
                asset["latest_stats_yuan"]["n"], asset["orgs_parsed"],
                "分子=资产表每企最新年营收可解析且为正的机构数 asset_text.latest_stats_yuan.n（6,596 家）；"
                "分母=资产表有可解析营收的机构数 asset_text.orgs_parsed（7,738 家）。仅补充参考，不并主口径"),
            "unit_10k_pairs": dec(
                ua.get("ratio_buckets", {}).get("10000x"),
                ua.get("ratio_buckets", {}).get("10000x"), None,
                "计数，无分母：两表同一企业-年营收相差整 10,000 倍的对数"
                "（unit_audit.ratio_buckets['10000x']，1,435 对）"),
            "unit_same_pairs": dec(
                ua.get("ratio_buckets", {}).get("1x"),
                ua.get("ratio_buckets", {}).get("1x"), None,
                "计数，无分母：两表同一企业-年营收字面一致（1x）的对数（unit_audit.ratio_buckets['1x']，484 对）"),
            "unit_fin_missing_x10000": dec(
                ua.get("ratio_buckets", {}).get("fin_missing_x10000"),
                ua.get("ratio_buckets", {}).get("fin_missing_x10000"), None,
                "计数，无分母：经外部锚判定为 annual_fin 漏乘 10,000 的对数"
                "（unit_audit.ratio_buckets['fin_missing_x10000']，703 对）"),
            "unit_asset_label_wrong": dec(
                ua.get("ratio_buckets", {}).get("asset_label_wrong"),
                ua.get("ratio_buckets", {}).get("asset_label_wrong"), None,
                "计数，无分母：判为资产表「万元」标签写错的对数"
                "（unit_audit.ratio_buckets['asset_label_wrong']，8 对）"),
            "unit_undeterminable": dec(
                ua.get("ratio_buckets", {}).get("undeterminable"),
                ua.get("ratio_buckets", {}).get("undeterminable"), None,
                "计数，无分母：无外部锚、无法判定哪张表单位错的对数"
                "（unit_audit.ratio_buckets['undeterminable']，724 对）"),
            "unit_other": dec(
                ua.get("ratio_buckets", {}).get("other"),
                ua.get("ratio_buckets", {}).get("other"), None,
                "计数，无分母：比值落在 1x / 10,000x / 0.0001x 之外的对数"
                "（unit_audit.ratio_buckets['other']，113 对）"),
            "mean_over_median": dec(
                round(st["mean"] / st["median"], 4), st["mean"], st["median"],
                "分子=最新营收均值 latest_stats.mean（138,963,840.3824 元）；"
                "分母=最新营收中位数 latest_stats.median（16,553.27 元）。倍率即右偏程度"),
            "p90_over_median": dec(
                round(st["p90"] / st["median"], 4), st["p90"], st["median"],
                "分子=最新营收 P90 latest_stats.p90（80,058,401.21 元）；"
                "分母=最新营收中位数 latest_stats.median（16,553.27 元）"),
            "anchor_2014_2016_share_pct": dec(
                pct(fin["latest_year_dist"].get("2014", 0) + fin["latest_year_dist"].get("2015", 0)
                    + fin["latest_year_dist"].get("2016", 0), orgs_rev),
                fin["latest_year_dist"].get("2014", 0) + fin["latest_year_dist"].get("2015", 0)
                + fin["latest_year_dist"].get("2016", 0), orgs_rev,
                "分子=最新财务年落在 2014 的 476 家 + 2015 的 305 家 + 2016 的 172 家 ＝ 953 家"
                "（annual_fin.latest_year_dist）；分母=最新年营收非空的机构数 orgs_any_revenue（1,302 家）"),
        },
        "latest_year_dist": fin["latest_year_dist"],
        "year_dist": fin["year_dist"],
        "fill": fin["fill"],
        "top10": fin["top10_by_latest_rev"],
        "asset_text": {
            "rows_all": asset["rows_all"], "orgs_all": asset["orgs_all"],
            "xsze_wan_rows": asset["xsze_wan_rows"], "parsed_rows": asset["parsed_rows"],
            "orgs_parsed": asset["orgs_parsed"],
            "placeholder_rows": asset["placeholder_rows"],
            "blank_rows": asset["blank_rows"],
            "latest_stats_yuan": asset["latest_stats_yuan"],
            "latest_year_dist": asset["latest_year_dist"],
            "unit_note": asset["unit_note"],
        },
        "stock": {
            "rows": stock["rows"], "orgs": stock["orgs"],
            "rev_pos_rows": stock["rev_pos_rows"], "rev_pos_orgs": stock["rev_pos_orgs"],
            "period_min": stock["period_min"], "period_max": stock["period_max"],
            "y2025_dec": stock["y2025_dec"],
        },
        "caveats": [
            "营收列是 double，库内不声明单位；量级分布跨 8 个数量级，原样输出、不做单位归一",
            "最新年 ≠ 同一年：1,302 家的锚年分布在 %s 之间，跨企横比必须先对齐年份"
            % "/".join(sorted(fin["latest_year_dist"])),
            "年报资产表的 xsze 有 514,140 行是「企业选择不公示」占位串，"
            "按空处理（不按 0），故该表只能当补充参考",
            "境外财务表 51 行、12 家，calc-logic 明示不并，本件未并",
        ],
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(headline, ensure_ascii=False, indent=1)[:2200])
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
    out_json = here / "M_ENT_REVENUE_LATEST_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_REVENUE_LATEST.py 等价）
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
        "metric_id": "M_ENT_REVENUE_LATEST",
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
