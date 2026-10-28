#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_MARKET_SHARE 市场份额
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_MARKET_SHARE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_MARKET_SHARE · 市场份额（gkx 单库·无分母版）

定义
----
市场份额 = 企业营收 / 该企业所在市场的总规模。分子与分母必须同口径、同边界
（同一产品/同一区域/同一年），否则比率没有意义。需求原文与旧稿都把它作为
商业力评估「市场维」的原子读数。

为什么判「完全不支持」
----------------------
分子有、但极稀疏：`dwd_org_stock_finance_info` 42,661 行 + `dwd_org_annual_financial_info`
93,945 行，落到「企业×年 营收>0」的只有 2,191 条年记录 / 39,395 条月度存量记录，
按企业去重 1,388 家，占底册 189,116 家的 0.73%。
分母没有任何来源：gkx 没有市场规模表、没有行业产值表、没有第三方市占率表
（`chain_market` 在 gkx 不存在，source_absent，见 TABLE_ABSENCE_EVIDENCE §chain_market）。

本件仍做了一次「链内样本份额」试算，用来证明代理不成立：把分母换成「链内样本
企业营收合计」，得到的是样本内相对份额，不是市场份额——样本只覆盖链内 1,300 家
（且集中在上市公司），分母随样本变动而变，换一批企业份额就整体漂移。试算结果
留在 rejected_proxy_trial，不进结论。

输出：code/M_ENT_MARKET_SHARE_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_MARKET_SHARE_out.json"
METRIC = "M_ENT_MARKET_SHARE"


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def main() -> None:
    rev = load("chain21_revenue_20261022.json")
    annual = rev["annual"]
    stock = rev["stock"]
    name2chain = load("chain21_layer_20261022.json")["names"]

    by_ent = defaultdict(float)
    for r in annual:
        # [org_id, name, credit, year, revenue, ?, profit]
        if r[4] and r[4] > 0:
            by_ent[(r[1], r[3])] = max(by_ent[(r[1], r[3])], float(r[4]))

    # 基准年取「有效企业数最多」的一年（2014，752 家）；末年 2025 只有 34 家，
    # 用它会让试算变成小样本噪声，故不取 max(year)。
    year_orgs = defaultdict(set)
    for (name, y), v in by_ent.items():
        year_orgs[int(y)].add(name)
    latest_year = max(year_orgs, key=lambda y: (len(year_orgs[y]), y)) if year_orgs else None
    latest = {}
    for (name, y), v in by_ent.items():
        if int(y) == latest_year:
            latest[name] = v
    orgs_all_years = len({n for (n, y) in by_ent})

    chain_rev = defaultdict(float)
    chain_top = defaultdict(list)
    for name, v in latest.items():
        ch = name2chain.get(name)
        if not ch:
            continue
        chain_rev[ch] += v
        chain_top[ch].append((name, v))

    trial = []
    for ch in sorted(chain_top):
        top = sorted(chain_top[ch], key=lambda x: -x[1])[:5]
        tot = chain_rev[ch]
        trial.append({
            "chain": ch, "sample_ents": len(chain_top[ch]),
            "sample_revenue_sum": round(tot, 2),
            "top5": [{"name": n, "revenue": round(v, 2),
                      "share_of_sample": round(v / tot, 4)} for n, v in top],
        })

    orgs_with_rev = len(latest)
    out = {
        "metric_id": METRIC,
        "metric_name": "市场份额",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "share_i = revenue_i / market_size(产品×区域×年)；本件缺 market_size",
        "blocking_tables": {
            "chain_market": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_market",
            }
        },
        "numerator_facts": {
            "stock_rows": len(stock), "annual_rows": len(annual),
            "orgs_with_positive_revenue_base_year": orgs_with_rev,
            "orgs_with_positive_revenue_all_years": orgs_all_years,
            "latest_year": latest_year,
            "base_orgs": 189116,
            "coverage_rate": round(orgs_all_years / 189116, 5),
        },
        "denominator_facts": {
            "market_size_table_exists": False,
            "industry_output_table_exists": False,
            "third_party_share_table_exists": False,
            "searched_keywords": ["market_size", "market_share", "industry_output",
                                  "chain_market", "产业规模", "产值"],
        },
        "rejected_proxy_trial": {
            "proxy": "分母换成链内样本营收合计（链内相对份额）",
            "why_rejected": "样本只有 1,388 家有营收（0.73%），且集中在上市公司；分母随样本变动而变，换一批企业份额整体漂移；份额的方向性偏差不可控，不能作为市场份额交付",
            "chains": trial,
        },
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": "市场份额的分母（市场规模/行业产值/第三方市占率）在 gkx 完全没有来源，chain_market 表不存在；分子侧只有 0.73% 的企业有营收（1,388/189,116），且集中在上市公司。分母无源、分子极稀疏，比率不成立。链内样本份额试算已做，但其分母是样本营收而不是市场规模，属构造性偏差，明确否决。故判完全不支持，只写需求与恢复路径。",
            "criteria": {
                "numerator_exists": True,
                "numerator_coverage": round(orgs_all_years / 189116, 5),
                "denominator_exists": False,
                "proxy_trialed": True,
                "proxy_accepted": False,
            },
        },
        "base_years_used": [latest_year] if latest_year else [],
        "base_years_missing": [],
        "base_years_note": f"分子基准年取 {latest_year}（有效企业最多的年份，{orgs_with_rev} 家）；2025 只有 34 家，属残年，不用它做试算。全期去重 {orgs_all_years} 家。年份不是本件的瓶颈，分母缺失才是：即使补齐十年营收，没有市场规模仍然算不出份额，故 base_years_missing 留空而不是列一串年份。",
        "sources": [
            {"path": "code/_snapshots21/chain21_revenue_20261022.json",
             "table": "gkx.dwd_org_stock_finance_info + gkx.dwd_org_annual_financial_info",
             "rows": 41586, "role": "分子（企业营收）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993,
             "role": "企业名→链（试算用）"},
            {"path": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md",
             "role": "§chain_market 分母无源的证据块"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} orgs_with_rev={orgs_with_rev} "
          f"latest={latest_year} cov={out['numerator_facts']['coverage_rate']}")
    for t in trial:
        print(f"  trial {t['chain']} ents={t['sample_ents']} sum={t['sample_revenue_sum']:.3e}")


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
    out_json = here / "M_ENT_MARKET_SHARE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_MARKET_SHARE.py 等价）
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
        "metric_id": "M_ENT_MARKET_SHARE",
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
