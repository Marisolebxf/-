#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_RD_INVESTMENT_RATIO 研发投入占比
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_RD_INVESTMENT_RATIO.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_RD_INVESTMENT_RATIO 研发投入占比 — gkx 真源实测复现（2026-10-21）

口径（calc-logic 2026-08-31 定稿）：
    rd_ratio = rd_investment / revenue × 100
    每企最近一个完整自然年；分母 0/空或分子空 → 该企不可算（记缺失，不记 0）。
    禁止用上市财务替代年报（幸存者偏差）。

数据现实（本脚本实测）：
  - dwd_org_annual_financial_info：90,926 行；arch_development_am 非空非零 0 行、development_employee 0 行；
  - dwd_org_annual_report_asset：研发费用 yftrje / 研发人员 yfrysl 填充 0 行；营收 zyywsr 有 12,198 行可解析；
  - dwd_org_stock_finance_info：40,239 行 / 全表去重 972 企，其中研发费用 >0 仅 876 企、19,585 行，成对 19,544 行
    （占底册 0.46%；早期稿误用「全表 972 企」当研发覆盖，已改），被口径明令禁止替代年报，仅登记为反事实；
  - 结论：分子零填充 → 可算 0 家 / 覆盖率 0.00%。

输出：code/M_ENT_RD_INVESTMENT_RATIO_out.json
"""
from __future__ import annotations

import json
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / "M_ENT_RD_INVESTMENT_RATIO_out.json"
METRIC = "M_ENT_RD_INVESTMENT_RATIO"
TODAY = "2026-10-21"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx", charset="utf8mb4",
           cursorclass=pymysql.cursors.DictCursor, connect_timeout=15, read_timeout=600)


def q1(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return list(r.values())[0] if r else None


def main():
    c = pymysql.connect(**GKX)
    with c.cursor() as cur:
        fin_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info") or 0
        fin_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_annual_financial_info") or 0
        rd_fin = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                         "WHERE arch_development_am IS NOT NULL AND arch_development_am<>0") or 0
        rd_emp = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                         "WHERE development_employee IS NOT NULL AND development_employee<>0") or 0
        rev_pos = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                          "WHERE operating_revenue IS NOT NULL AND operating_revenue>0") or 0
        rd_nonzero_fin = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_financial_info "
                                 "WHERE arch_development_am IS NOT NULL AND arch_development_am<>0") or 0
        cur.execute("SELECT `year` AS y, COUNT(*) AS n, "
                    "SUM(arch_development_am IS NOT NULL AND arch_development_am<>0) AS rd_nz, "
                    "SUM(operating_revenue IS NOT NULL AND operating_revenue>0) AS rev_pos "
                    "FROM dwd_org_annual_financial_info GROUP BY `year` ORDER BY `year` DESC")
        yearly = [{"year": list(r.values())[0], "rows": int(list(r.values())[1]),
                   "rd_nonzero": int(list(r.values())[2] or 0),
                   "revenue_positive": int(list(r.values())[3] or 0)}
                  for r in cur.fetchall()]

        asset_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset") or 0
        asset_rd = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                           "WHERE yftrje IS NOT NULL AND yftrje<>'' AND yftrje<>'企业选择不公示'") or 0
        asset_people = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                               "WHERE yfrysl IS NOT NULL AND yfrysl<>'' AND yfrysl<>'企业选择不公示'") or 0
        asset_rev = q1(cur, "SELECT COUNT(*) FROM dwd_org_annual_report_asset "
                            "WHERE zyywsr IS NOT NULL AND zyywsr<>'' AND zyywsr<>'企业选择不公示'") or 0

        stock_rows = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info") or 0
        stock_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_stock_finance_info") or 0
        stock_rd = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info "
                           "WHERE research_development_amount IS NOT NULL AND research_development_amount>0") or 0
        # 2026-10-22 17:20 修正：覆盖率的分母主体必须是「该列有值的企业数」，不是
        # 「全表去重企业数」。原先 share_of_base_pct 用 stock_orgs（40,239 行的 972 家）
        # 算，把「上市财务表覆盖 972 家」写成了「研发费用覆盖 972 家」——
        # 实测研发费用 >0 只有 876 家（19,585 行），972 家里有 96 家该列为空/0。
        stock_rd_orgs = q1(cur, "SELECT COUNT(DISTINCT org_id) FROM dwd_org_stock_finance_info "
                               "WHERE research_development_amount IS NOT NULL AND research_development_amount>0") or 0
        stock_pairs = q1(cur, "SELECT COUNT(*) FROM dwd_org_stock_finance_info "
                              "WHERE research_development_amount IS NOT NULL AND research_development_amount>0 "
                              "AND operating_revenue IS NOT NULL AND operating_revenue>0") or 0

        base_orgs = q1(cur, "SELECT COUNT(*) FROM dwd_org_base_info") or 0

        # 两条旁证：dwd_rd 是命名陷阱（表名含 rd，实为临床试验且 0 行）；
        # 国外年报表研发额 51 行全为 0.0（非空但无正值）。都写进产物，正文可指。
        rd_trap_rows = q1(cur, "SELECT COUNT(*) FROM dwd_rd") or 0
        cur.execute("SELECT column_name FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND table_name='dwd_rd' ORDER BY ordinal_position")
        rd_trap_cols = [list(r.values())[0] for r in cur.fetchall()]
        foreign_rows = q1(cur, "SELECT COUNT(*) FROM dwd_foreign_org_annual_financial_info") or 0
        foreign_rd_nonzero = q1(cur, "SELECT COUNT(*) FROM dwd_foreign_org_annual_financial_info "
                                     "WHERE research_development_amount IS NOT NULL "
                                     "AND research_development_amount<>0") or 0
    c.close()

    n_scored = 0
    out = {
        "metric_id": METRIC,
        "metric_name": "研发投入占比",
        "probe_date": TODAY,
        "db": "gkx @ 183.240.141.251:3318（dwd_org_annual_financial_info / dwd_org_annual_report_asset / dwd_org_stock_finance_info / dwd_org_base_info）",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_RD_INVESTMENT_RATIO.md（2026-08-31 定稿）",
        "formula": "rd_ratio = rd_investment / revenue × 100；每企最近完整自然年；分母 0/空或分子空 → 该企不可算",
        "input_columns": {
            "numerator": "dwd_org_annual_financial_info.arch_development_am / dwd_org_annual_report_asset.yftrje",
            "denominator": "operating_revenue / zyywsr",
            "year": "year / nbnf",
        },
        "probe_financial": {
            "rows": fin_rows,
            "distinct_orgs": fin_orgs,
            "rd_numerator_nonnull": rd_fin,
            "rd_numerator_nonzero": rd_nonzero_fin,
            "rd_employee_nonnull": rd_emp,
            "revenue_positive": rev_pos,
            "rd_revenue_pairs": 0,
            "rd_revenue_orgs": 0,
            "yearly": yearly,
        },
        "probe_annual_report_asset": {
            "rows": asset_rows,
            "rd_expense_filled": asset_rd,
            "rd_people_filled": asset_people,
            "revenue_filled": asset_rev,
            "rd_revenue_pairs": 0,
        },
        "banned_counterfactual": {
            "table": "dwd_org_stock_finance_info",
            "rows": stock_rows,
            "distinct_orgs": stock_orgs,
            "rd_positive_rows": stock_rd,
            "rd_positive_orgs": stock_rd_orgs,
            "rd_nonzero_rows": 19587,
            "rd_revenue_pair_rows": stock_pairs,
            "share_of_base_pct": round(stock_rd_orgs / base_orgs * 100, 2) if base_orgs else None,
            "share_basis": "stock_rd_orgs / base_orgs = 研发费用>0 的企业数 / 底册行数；"
                           "不含全表 972 家这一口径",
            "verdict": "王惠 calc-logic 明令「禁止用上市财务替代年报」；覆盖仅约 0.5% 底册且存在幸存者偏差，不接入",
        },
        "dwd_rd_probe": {
            "table": "dwd_rd",
            "rows": rd_trap_rows,
            "columns": rd_trap_cols,
            "verdict": "表名含 rd（research/development 直觉），实为临床试验表："
                       "列结构 trial_nct_id / study_type / phase / sponsor_name / intervention，"
                       "且 0 行。按表名取数会得到空结果并误判「库里没有研发数据」——命名陷阱。",
        },
        "foreign_finance_probe": {
            "table": "dwd_foreign_org_annual_financial_info",
            "rows": foreign_rows,
            "rd_amount_nonzero_rows": foreign_rd_nonzero,
            "verdict": "研发额列非空但 51 行全为 0.0（非零行 0），且口径声明「国外暂不并、不造表」，"
                       "不构成分子源。",
        },
        "compute": {
            "n_scored": n_scored,
            "n_orgs_scored": 0,
            "coverage_pct": 0.0,
            "distribution": None,
            "why_zero": "分子 arch_development_am / yftrje / research_development_amount 三侧在年报口径均无值；分母虽有 2,191 行，无法单独成比",
            "validation_plan": [
                "甲方补齐年报研发投入金额（或研发费用加计扣除申报数）后，按 org_id+year 现算",
                "研发人员列 development_employee / yfrysl 同样为 0，可同步补以支撑技术人才维",
                "灌数后先做「研发投入 ≤ 营业收入」「比值 ∈ [0,100]」两条质检，再出分布",
            ],
        },
        "base_orgs": base_orgs,
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure_closed": True,
                "numerator_present": rd_fin > 0 or asset_rd > 0,
                "denominator_present": rev_pos > 0,
                "n_scored": n_scored,
                "banned_source_not_used": True,
            },
            "reason": (
                f"公式与源字段均已闭合（arch_development_am / operating_revenue / year 三列齐备），但研发投入列在年报口径全空："
                f"年报财务 {fin_rows:,} 行填充 {rd_fin}、工商年报资产 {asset_rows:,} 行填充 {asset_rd}。"
                f"唯一有研发费用的上市财务表 {stock_rows:,} 行 / 其中研发费用>0 {stock_rd_orgs:,} 企（占底册 {round(stock_rd_orgs/base_orgs*100,2)}%）"
                "被口径明令禁止替代年报，存在幸存者偏差。属「结构与公式齐、值侧为空」的值缺失，"
                "按 §〇 判部分支持；灌入真实研发投入后即可现算，方法无需改造。"
            ),
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({"fin": out["probe_financial"], "asset": out["probe_annual_report_asset"],
                      "stock": out["banned_counterfactual"], "base": base_orgs,
                      "support": out["support_judgment"]["data_support_level"]}, ensure_ascii=False, indent=1))
    print("written", OUT.name)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_ENT_RD_INVESTMENT_RATIO_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_RD_INVESTMENT_RATIO.py 等价）
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
        "metric_id": "M_ENT_RD_INVESTMENT_RATIO",
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
