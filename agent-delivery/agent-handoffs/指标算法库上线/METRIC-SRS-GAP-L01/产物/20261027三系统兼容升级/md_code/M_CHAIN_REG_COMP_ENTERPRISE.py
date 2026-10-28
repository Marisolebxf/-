#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_COMP_ENTERPRISE 竞争力-企业能力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_COMP_ENTERPRISE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_REG_COMP_ENTERPRISE 竞争力-企业能力（区域）（20261021 复现）

口径（calc-logic/CHAIN/M_CHAIN_REG_COMP_ENTERPRISE.md，human:王惠）：
  加权平均三个三级指标（权重待甲方确认）：
    A 人均产值   = 营业收入 ÷ 从业人数            ← dwd_org_annual_financial_info
    B 研发投入强度 = 研发经费 ÷ 营业收入 × 100%     ← dwd_org_stock_finance_info
    C 有效专利数量 = 企业作为第一专利权人的有效发明专利件数 ← dwd_patent(kind) + dwd_patent_legal

本脚本按链×城 48 单元逐格复现 A/B/C（中位数聚合，抗极值），并给等权 min-max 合成分备查；
权重未定稿，故合成分仅作敏感性演示，不作正式值。

输出：code/M_CHAIN_REG_COMP_ENTERPRISE_out.json
"""
from __future__ import annotations

import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_reg_common import CHAIN_AXIS, CITY4, STAT_YEAR, load_panel, load_patent, load_small, stats, write_out  # noqa: E402

MID = "M_CHAIN_REG_COMP_ENTERPRISE"
CHAIN_CN = {
    "INB1306": "软件与信息服务", "INB1309": "人工智能", "INB1333": "智能终端", "INB1502": "数字创意",
    "INB2505": "合成生物", "INB1204": "机器人", "INB1303": "集成电路", "INB1323": "传感器",
    "INB1354": "具身智能", "INB1209": "智能网联汽车", "INB1236": "低空经济", "INB2503": "生物医药",
}


def med(xs):
    xs = sorted(xs)
    return round(xs[len(xs) // 2], 4) if xs else None


def minmax(vals):
    lo, hi = min(vals), max(vals)
    return [round(100 * (v - lo) / (hi - lo), 1) if hi > lo else 0.0 for v in vals]


def main() -> None:
    t0 = time.time()
    panel = load_panel()
    small = load_small()
    pat = load_patent()

    org_city = {r[0]: r[4] for r in small["orgmap"] if r[4]}
    org_credit = {r[0]: r[1] for r in small["orgmap"] if r[1]}
    ent_chain = panel["ent_chain"]
    name_city = {r[2]: r[4] for r in small["orgmap"] if r[2] and r[4]}

    def chains_of(org_id):
        return [c for c in ent_chain.get(org_credit.get(org_id, ""), []) if c in CHAIN_AXIS]

    # A 人均产值：每 org 取「营收与人数均有效」的最新年度
    best = {}
    for org_id, yr, rev, emp, assets in small["annual_fin"]:
        if not yr or int(yr) > STAT_YEAR:
            continue
        if rev in (None, 0) or emp in (None, 0):
            continue
        if rev < 0:
            continue
        y = int(yr)
        if org_id not in best or y > best[org_id][0]:
            best[org_id] = (y, float(rev) / float(emp), float(rev), float(emp))
    a_vals = defaultdict(list)
    a_year = Counter()
    for org_id, (y, per, rev, emp) in best.items():
        city = org_city.get(org_id)
        if city not in CITY4:
            continue
        a_year[y] += 1
        for ch in chains_of(org_id):
            a_vals[(ch, city)].append(per)

    # B 研发投入强度：上市财务，期次 <= 统计年，营收>0 且研发>=0
    b_vals = defaultdict(list)
    b_org = defaultdict(set)
    for org_id, period, rev, rd, emp in small["stock_fin"]:
        if not period:
            continue
        p = str(period)
        if not p[:4].isdigit() or int(p[:4]) > STAT_YEAR:
            continue
        if rev in (None, 0) or rd is None or rev <= 0:
            continue
        city = org_city.get(org_id)
        if city not in CITY4:
            continue
        for ch in chains_of(org_id):
            b_vals[(ch, city)].append(100.0 * float(rd) / float(rev))
            b_org[(ch, city)].add(org_id)

    # C 发明授权：name_patent[name] = [总件数, kind=B 授权发明件数]
    c_vals = defaultdict(int)
    c_org = defaultdict(int)
    for name, (total, invented) in pat["name_patent"].items():
        city = name_city.get(name)
        if city not in CITY4 or not invented:
            continue
        for ch in panel["name_chain"].get(name, []):
            ch_code = ch[0] if isinstance(ch, (list, tuple)) else ch
            if ch_code in CHAIN_AXIS:
                c_vals[(ch_code, city)] += int(invented)
                c_org[(ch_code, city)] += 1

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for city in CITY4:
            k = (ch, city)
            row["cells"][city] = {
                "per_capita_output_cny": med(a_vals.get(k, [])),
                "per_capita_n_orgs": len(a_vals.get(k, [])),
                "rd_intensity_pct": med(b_vals.get(k, [])),
                "rd_n_orgs": len(b_org.get(k, ())),
                "granted_invention_patents": c_vals.get(k, 0),
                "patent_n_orgs": c_org.get(k, 0),
                "chain_enterprises": int(panel["chain_city"].get(ch, {}).get(city, 0)),
            }
        matrix.append(row)

    a_all = [row["cells"][c]["per_capita_output_cny"] for row in matrix for c in CITY4]
    b_all = [row["cells"][c]["rd_intensity_pct"] for row in matrix for c in CITY4]
    c_all = [row["cells"][c]["granted_invention_patents"] for row in matrix for c in CITY4]
    a_fill = [v if v is not None else 0 for v in a_all]
    b_fill = [v if v is not None else 0 for v in b_all]
    na, nb, nc = minmax(a_fill), minmax(b_fill), minmax(c_all)
    for i, row in enumerate(matrix):
        for j, city in enumerate(CITY4):
            idx = i * 4 + j
            row["cells"][city]["composite_equal_weight_0_100"] = round(
                (na[idx] + nb[idx] + nc[idx]) / 3, 1)
            row["cells"][city]["_norm"] = {"A": na[idx], "B": nb[idx], "C": nc[idx]}

    raw_pairs = [float(rev) / float(emp) for _, yr, rev, emp, _a in small["annual_fin"]
                 if yr and rev not in (None, 0) and emp not in (None, 0) and rev > 0]
    implausible = sum(1 for v in raw_pairs if v < 1000)
    cov = [row["cells"][c]["per_capita_n_orgs"] for row in matrix for c in CITY4]
    rdc = [row["cells"][c]["rd_n_orgs"] for row in matrix for c in CITY4]
    total_chain_orgs = len(ent_chain)
    payload = {
        "metric_id": MID,
        "metric_name": "竞争力-企业能力",
        "date": "2026-10-21",
        "formula_owner": "王惠（calc-logic/CHAIN/M_CHAIN_REG_COMP_ENTERPRISE.md）",
        "stat_year": STAT_YEAR,
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "weights": "未定稿（原稿「权重待甲方确认」），合成分按等权 1/3 演示",
        "composite_note": "A/B/C 等权合成；其中 A 存在量纲不一致（见 probes.per_capita_implausible_pct），合成分仅作敏感性演示，不作正式值",
        "probes": {
            "annual_rows": len(small["annual_fin"]),
            "annual_orgs_valid_rev_emp": len(best),
            "annual_year_dist": dict(sorted(a_year.items())),
            "stock_fin_rows": len(small["stock_fin"]),
            "stock_rd_orgs": len({r[0] for r in small["stock_fin"] if r[2] and r[3] is not None}),
            "patent_names": len(pat["name_patent"]),
            "chain_orgs_total_cells": total_chain_orgs,
            "chain_orgs_unique": len(ent_chain),
            "patent_legal_rows": len(small["patent_legal"]),
            "patent_total_rows": pat["n_patent"],
            "per_capita_pairs_raw": len(raw_pairs),
            "per_capita_implausible_pct": round(100 * implausible / len(raw_pairs), 1) if raw_pairs else None,
            "per_capita_raw_median": round(sorted(raw_pairs)[len(raw_pairs) // 2], 2) if raw_pairs else None,
        },
        "matrix": matrix,
        "stats_A_per_capita": stats(a_all),
        "stats_B_rd_intensity": stats(b_all),
        "stats_C_granted_invention": stats(c_all),
        "stats_coverage_orgs_A": stats(cov),
        "stats_coverage_orgs_B": stats(rdc),
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"三个三级指标中 C 满覆盖（2,939,895 件专利按第一申请人现转，发明授权 kind=B "
                f"{pat['kind_dist'].get('B', 0):,} 件）；B 仅覆盖 875 家上市主体（{len(small['stock_fin']):,} 行财务），"
                f"占 4 市链上企业 {total_chain_orgs:,} 家的 {100 * 875 / total_chain_orgs:.1f}%；"
                f"A 仅 850 家有营收+人数有效配对（{len(small['annual_fin']):,} 行年报），最新年度集中在 "
                f"{max(a_year) if a_year else 'NA'} 及以前（2013–2018 为主），且 {round(100 * implausible / len(raw_pairs), 1)}% 的公司-年"
                f"「营收÷人数」低于 1,000 元/人（量纲不一致，疑为万元与元混用），A 在单位确认前不可用。"
                f"故只能给部分支持：C 可正式出数，A/B 只能出「有样本单元」的参考值并须标注覆盖率。"
            ),
            "criteria": {"A_orgs": len(best), "B_orgs_stock": 875,
                         "A_cells_null": sum(1 for v in a_all if v is None),
                         "B_cells_null": sum(1 for v in b_all if v is None),
                         "C_cells_zero": sum(1 for v in c_all if v == 0)},
        },
        "notes": [
            "C「有效专利」未过法律状态：`dwd_patent_legal` 仅 20,000 行（对 2.94M 专利覆盖率 0.68%），"
            "按 pn 关联会系统性漏判，故以 `kind='B'`（授权发明）作有效发明上界代理，属高估，已在正文披露。",
            "B 的研发口径来自上市财务 `research_development_amount`，只覆盖股份公司/上市主体；未上市中小企业研发无处可取，"
            "这是「部分支持」的主因，不能用营收×行业均值等假设补。",
            "A 的年报时效性差：`dwd_org_annual_financial_info` 90,926 行中仅 850 家营收+人数同时有效，"
            "最新年度分布见 probes.annual_year_dist（峰值 2014 年 567 条），跨年混用已在单元内取「每企最新年」缓解。",
            "人均产值单位元/人；中位数聚合以免少数巨头（如营收 4.19 亿/1,050 人）拉动整格。",
            "等权合成分仅为敏感性演示；权重未定稿前不发布正式竞争力分值。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("A", stats(a_all))
    print("B", stats(b_all))
    print("C", stats(c_all))
    print("cov A", stats(cov), "cov B", stats(rdc))


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_CHAIN_REG_COMP_ENTERPRISE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_COMP_ENTERPRISE.py 等价）
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
        "metric_id": "M_CHAIN_REG_COMP_ENTERPRISE",
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
