#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_CYCLE_STAGE 产业周期阶段
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_CYCLE_STAGE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_CYCLE_STAGE · 产业周期阶段（gkx 单库代理版）

口径（王惠四步法的可执行化版本，旧稿沿用框架）
----------------------------------------------
阶段 ∈ {孕育期, 成长期, 成熟期, 衰退期}。原四步是「结构—增速—盈利—判定」，
本件逐腿做可用性检验，只保留能通过检验的腿：

  L1 融资热度腿（主判）：链内企业融资事件数，2022—2024 三年合计 / 2018—2020 三年合计 − 1
       >= +10% → 成长期；-10% ~ +10% → 成熟期；<= -10% → 衰退期
  L2 年龄结构腿（辅判）：成立年份分布 → 近 5 年新设占比 new_share
       new_share >= 0.25 且 L1 >= 0 → 孕育期（覆盖 L1 结论）
  L3 营收增速腿（**已试算并否决**）：链内样本营收 CAGR
       否决理由：有效样本 n_rev 从 2014 年 198 家掉到 2022 年 11 家，CAGR 量的是
       财报覆盖衰减，不是产业增速（详见 l3_revenue_rejected）。

数据事实
--------
`chain_stage` 在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §chain_stage）。
L1：`dwd_org_financing_info` 25,654 行（chain21_fin_degree），按企业名挂链命中 14,626 行。
L2：`dwd_org_industry_tags` × `dwd_org_base_info.incorporation_date`（chain21_year）。
L3：`dwd_org_annual_financial_info` + `dwd_org_stock_finance_info`（chain_lm_fin）。

输出：code/M_CHAIN_CYCLE_STAGE_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_CHAIN_CYCLE_STAGE_out.json"
METRIC = "M_CHAIN_CYCLE_STAGE"

RECENT = (2020, 2024)
PRE = (2018, 2020)
POST = (2022, 2024)


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def _median_year(yrs):
    if not yrs:
        return None
    tot = sum(yrs.values())
    acc = 0
    for y in sorted(yrs):
        acc += yrs[y]
        if acc >= tot / 2:
            return y
    return None


def main() -> None:
    year_by_chain = defaultdict(lambda: defaultdict(int))
    for k, n in load("chain21_year_20261022.json")["chain_year"].items():
        code, y = k.split("|")
        year_by_chain[code][int(y)] += n

    names = {c["chain"]: c["name"] for c in load("chain_panel21.json")["chains"]}
    name2chain = load("chain21_layer_20261022.json")["names"]

    fin_rows = load("chain21_fin_degree_20261022.json")["fin"]
    fin_by_chain = defaultdict(lambda: defaultdict(int))
    matched = 0
    for r in fin_rows:
        ch = name2chain.get(r[1])
        if not ch:
            continue
        matched += 1
        fin_by_chain[ch][int(str(r[6])[:4])] += 1

    rev = defaultdict(list)
    for r in load("chain_lm_fin_20261021.json")["fin"]:
        rev[r["code"]].append(r)

    rows = []
    cov = {"chains": 0, "fin_matched": matched, "fin_rows": len(fin_rows),
           "fin_unmatched": len(fin_rows) - matched,
           "fin_match_rate": round(matched / len(fin_rows), 4) if fin_rows else None,
           "tag_rows": load("chain21_year_20261022.json")["tag_rows"],
           "multi_chain_rows": load("chain21_layer_20261022.json")["multi_chain_rows"],
           "fin_le_50_events": 0, "total_orgs_with_year": 0}
    for code in sorted(names):
        yrs = year_by_chain.get(code, {})
        total = sum(yrs.values())
        recent = sum(n for y, n in yrs.items() if RECENT[0] <= y <= RECENT[1])
        new_share = round(recent / total, 4) if total else None
        cov["chains"] += 1
        cov["total_orgs_with_year"] += total

        fy = fin_by_chain.get(code, {})
        pre = sum(fy.get(y, 0) for y in range(PRE[0], PRE[1] + 1))
        post = sum(fy.get(y, 0) for y in range(POST[0], POST[1] + 1))
        fin_chg = round(post / pre - 1, 4) if pre >= 20 else None
        if fin_chg is None or min(pre, post) < 50:
            cov["fin_le_50_events"] += 1

        if new_share is not None and new_share >= 0.25 and (fin_chg or 0) >= 0:
            stage = "孕育期"
        elif fin_chg is None:
            stage = "不可判"
        elif fin_chg >= 0.10:
            stage = "成长期"
        elif fin_chg > -0.10:
            stage = "成熟期"
        else:
            stage = "衰退期"

        # L3：营收腿否决证据（保留计算，只为证明它不可用）
        pts = [r for r in rev.get(code, []) if r["n_rev"] > 0 and r["rev_sum"]]
        pts.sort(key=lambda r: r["year"])
        l3 = None
        if len(pts) >= 2:
            a, b = pts[0], pts[-1]
            span = b["year"] - a["year"]
            cagr = round((b["rev_sum"] / a["rev_sum"]) ** (1 / span) - 1, 4) if span else None
            l3 = {"first_year": a["year"], "first_n": a["n_rev"],
                  "last_year": b["year"], "last_n": b["n_rev"], "cagr": cagr,
                  "n_ratio": round(b["n_rev"] / a["n_rev"], 3)}

        rows.append({
            "chain": code, "chain_name": names[code],
            "orgs_with_year": total, "median_est_year": _median_year(yrs),
            "new_share_2020_2024": new_share,
            "fin_events_pre_2018_2020": pre, "fin_events_post_2022_2024": post,
            "fin_event_change": fin_chg,
            "fin_events_total": sum(fy.values()),
            "stage": stage,
            "confidence": "跨窗口各>=50 事件" if fin_chg is not None and min(pre, post) >= 50 else "样本不足",
            "l3_revenue_rejected": l3,
        })

    dist = defaultdict(int)
    for r in rows:
        dist[r["stage"]] += 1

    out = {
        "metric_id": METRIC,
        "metric_name": "产业周期阶段",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "融资热度腿：post(2022-2024)/pre(2018-2020)-1 >=+10% 成长、-10%~+10% 成熟、<=-10% 衰退；new_share>=25% 且热度>=0 覆盖为孕育",
        "blocking_tables": {
            "chain_stage": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_stage",
            }
        },
        "proxy_path": "L1 链内融资事件数三年窗口对比（主判）+ L2 成立年份结构（辅判/孕育覆盖）",
        "proxy_deviation": "融资事件按企业名挂链命中 14,626/25,654=57.0%，链内未命中部分按无归属处理；融资热度反映资本关注度而非产出，衰退期的语义是「资本退潮」不是「产业萎缩」",
        "rejected_proxy": {
            "leg": "链内样本营收 CAGR",
            "why": "有效样本 n_rev 逐年塌陷（如软件与信息服务 2014 年 198 家 → 2022 年 11 家），CAGR 度量的是财报覆盖衰减而不是产业增速；各链 CAGR 落在 -99% ~ +26%，与深圳产业实际不符，故不采用",
            "evidence": "chains[].l3_revenue_rejected",
        },
        "stage_rule": {"pre_window": list(PRE), "post_window": list(POST),
                       "growth_threshold": 0.10, "birth_override": 0.25, "min_events": 50},
        "coverage": cov,
        "stage_distribution": dict(sorted(dist.items())),
        "chains": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "chain_stage 结果面不存在，三条候选腿里营收腿被数据证据否决（样本从 198 家塌到 11 家），但融资腿与年龄结构腿成立：25,654 条融资事件中 14,626 条可挂链，12 链各有 175—5,024 条事件，跨窗口样本均 >=50 的有 11 链。阶段标签可由「资本热度方向 + 年龄结构」规则映射得到，不需要外部参数表与结果面，故判部分支持；但热度≠产出，且 8 链落在衰退期的结论主要由 2022—2024 融资退潮驱动，只能作方向性判断。",
            "criteria": {
                "result_table_exists": False,
                "legs_total": 3,
                "legs_usable": 2,
                "legs_rejected": 1,
                "chains_judged": sum(1 for r in rows if r["stage"] != "不可判"),
                "chains_total": len(rows),
                "proxy_used": True,
            },
        },
        "base_years_used": [2018, 2019, 2020, 2022, 2023, 2024],
        "base_years_missing": [2021],
        "base_years_note": "主判腿用两个三年窗口（2018—2020 与 2022—2024）对比，2021 为疫情异常年，主动留空不入窗口，不是缺年补 0；年龄腿用截至 2024 的成立年份分布。融资事件在 2025—2026 大幅减少（919/618→238），为未完整年度，不入窗口。",
        "sources": [
            {"path": "code/_snapshots21/chain21_fin_degree_20261022.json",
             "table": "gkx.dwd_org_financing_info", "rows": 25654,
             "role": "链×年融资事件数（L1 主判腿）"},
            {"path": "code/_snapshots21/chain21_year_20261022.json",
             "table": "gkx.dwd_org_industry_tags × gkx.dwd_org_base_info",
             "rows": 35046, "role": "链×成立年份分布（L2 辅判腿）"},
            {"path": "code/_snapshots21/chain_lm_fin_20261021.json",
             "table": "gkx.dwd_org_annual_financial_info + gkx.dwd_org_stock_finance_info",
             "rows": 156, "role": "L3 营收腿（已否决，仅留证）"},
            {"path": "code/_snapshots21/chain21_layer_20261022.json",
             "table": "gkx.dwd_org_industry_tags", "rows": 36993,
             "role": "企业名→链映射"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name}")
    print(f"  chains={cov['chains']} fin_matched={cov['fin_matched']}/{cov['fin_rows']} "
          f"low_sample={cov['fin_le_50_events']} dist={dict(dist)}")
    for r in rows:
        print(f"  {r['chain']} {r['chain_name'][:8]:<8} pre={r['fin_events_pre_2018_2020']:<5} "
              f"post={r['fin_events_post_2022_2024']:<5} chg={r['fin_event_change']} "
              f"new={r['new_share_2020_2024']} -> {r['stage']}")


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
    out_json = here / "M_CHAIN_CYCLE_STAGE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_CYCLE_STAGE.py 等价）
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
        "metric_id": "M_CHAIN_CYCLE_STAGE",
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
