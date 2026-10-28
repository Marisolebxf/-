#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_SZ_ADVANTAGE_SCORE 深圳优势评分
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_SZ_ADVANTAGE_SCORE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_SZ_ADVANTAGE_SCORE · 深圳优势评分（四城对标，2026-10-21）

王惠口径（M_CHAIN_SZ_ADVANTAGE_SCORE V2-20260824）：
  四维 = 企业(数量/规模/质量各 1/3)、专利(数量)、政策(数量)、人才(数量/水平各 1/2)
  每个三级在默认对标集合 C={北京,上海,广州,深圳} 上 min-max 至 0–100，四维各 0.25 合成。

本实现的现实约束（全部披露）：
  * 默认对标集合 C 在开发库中无法成立：底册北京仅 163 家、上海仅 16 家，
    可比的只有深圳/广州/东莞/惠州四城 → 本报告按四城对标，禁止称「全国对标/全国排名」；
  * 政策维：policy_base 的 keywords/keypoints 全 NULL，只能用 title 字面命中，12 链合计仅 15 条；
  * 人才维：链上高校/科研机构（tags.company_name ∩ 深圳机构名）= 0 行，链级人才无法算。

输入：_snapshots/sz_chain_matrix_20261021.json
输出：code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _sz5_common as S  # noqa: E402

METRIC = "M_CHAIN_SZ_ADVANTAGE_SCORE"
NAME = "深圳优势评分"
PAT_NOTE = ("专利数来自 _snapshots/chain_h_stream_20261021.json 的 pat_city_chain："
            "200,000 件专利样本（占 293.99 万件的 6.80%）、61,229 个申请人名，"
            "按链上企业 company_name 字面匹配后归集到四城，是抽样计数而非全量。")


def compute() -> dict:
    m = S.load_matrix()
    rows = []
    for c, nm in S.chains(m):
        # 企业维三级
        cnt = {city: m["ent_city_base"][c][city] for city in S.CITY4}
        rev = {city: m["revenue"]["by_chain_city_yi"][c][city] for city in S.CITY4}
        inten = {city: (m["rd"]["by_chain_city"][c][city]["intensity_pct"] or 0.0) for city in S.CITY4}
        sc, _ = S.minmax(cnt)
        sr, _ = S.minmax(rev)
        si, _ = S.minmax(inten)
        ent_dim = {city: round((sc[city] + sr[city] + si[city]) / 3, 2) for city in S.CITY4}

        # 专利维
        pat = {city: int(m["patent"]["by_chain_city"].get(c, {}).get(city, 0)) for city in S.CITY4}
        pat_dim, pat_meta = S.minmax(pat)

        # 政策维（title 字面命中）
        pol = {city: int(m["policy_title_hits"][c][city]) for city in S.CITY4}
        pol_total = sum(pol.values())
        pol_dim, pol_meta = S.minmax(pol) if pol_total >= 3 else (None, {"insufficient": True, "total": pol_total})

        # 人才维：链级不可得
        tal_dim = None

        avail = {"企业": ent_dim, "专利": pat_dim}
        sz_avail = round(sum(d[city] for d in avail.values() for city in [ "深圳市"]) / len(avail), 2)

        full = {}
        for city in S.CITY4:
            parts = [ent_dim[city], pat_dim[city]]
            if pol_dim:
                parts.append(pol_dim[city])
            parts += [50.0] * (4 - len(parts))  # 缺维按王惠「全体相同取 50」降级填充
            full[city] = round(sum(parts) / 4, 2)

        rows.append({
            "industry_code": c, "industry_name": nm,
            "dims": {"企业": ent_dim, "专利": pat_dim, "政策": pol_dim, "人才": tal_dim},
            "sz_score_available_dims": sz_avail,
            "sz_score_wanghui4_filled": full["深圳市"],
            "city_scores_available": {city: round(sum(d[city] for d in avail.values()) / len(avail), 2)
                                      for city in S.CITY4},
            "city_scores_wanghui4": full,
            "sz_rank_available": 1 + sum(1 for city in S.CITY4
                                         if round(sum(d[city] for d in avail.values()) / len(avail), 2) > sz_avail),
            "sz_rank_wanghui4": 1 + sum(1 for city in S.CITY4 if full[city] > full["深圳市"]),
            "raw": {"count": cnt, "revenue_yi": rev, "rd_intensity_pct": inten, "patent_sample": pat,
                    "policy_title": pol},
            "meta": {"patent": pat_meta, "policy": pol_meta,
                     "policy_available": pol_dim is not None, "talent_available": False},
        })
    rows.sort(key=lambda r: -r["sz_score_available_dims"])

    avail_scores = [r["sz_score_available_dims"] for r in rows]
    full_scores = [r["sz_score_wanghui4_filled"] for r in rows]
    rank_a = [r["sz_rank_available"] for r in rows]
    rank_w = [r["sz_rank_wanghui4"] for r in rows]
    n_pol_avail = sum(1 for r in rows if r["meta"]["policy_available"])
    rep = {
        "metric_id": METRIC, "metric_name": NAME, "date": "2026-10-21",
        "calc_logic_ref": "metrics/calc-logic/CHAIN/M_CHAIN_SZ_ADVANTAGE_SCORE.md (V2-20260824)",
        "formula": ("每三级在四城集合 min-max 至 0–100；企业维=(数量+规模+质量)/3；"
                    "可得维口径 =（企业+专利）等权；王惠满配口径 =0.25×(企业+专利+政策+人才)，缺维填 50"),
        "benchmark_set": {"cities": S.CITY4, "n": 4,
                          "why_not_beijing_shanghai": "底册北京 163 家、上海 16 家，与深圳 95,600 家不可比；"
                                                      "四城对标是本库唯一可解释的截面"},
        "per_chain": rows,
        "stats_sz_available": S.stats(avail_scores),
        "stats_sz_wanghui4": S.stats(full_scores),
        "rank_available": {k: rank_a.count(k) for k in sorted(set(rank_a))},
        "rank_wanghui4": {k: rank_w.count(k) for k in sorted(set(rank_w))},
        "rank_change": sum(1 for a, b in zip(rank_a, rank_w) if a != b),
        "corr_available_vs_wanghui4": S.spearman(avail_scores, full_scores),
        "dim_availability": {
            "企业": {"available": True, "caveat": "规模维营收覆盖 0.65% 底册企业，质量维 876 家上市企业"},
            "专利": {"available": True, "caveat": PAT_NOTE},
            "政策": {"available": n_pol_avail == 12, "chains_with_signal": n_pol_avail,
                     "caveat": "keywords/keypoints 全 NULL，仅 title 字面命中；12 链合计 15 条，远不足以度量政策强度"},
            "人才": {"available": False,
                     "caveat": "链上高校/科研机构挂链 0 行；城市级学者仅 199 人（深圳），且学位表与主档 ID 交集 8.69%"},
        },
    }
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": ("四维中只有企业维与专利维可算（企业维仍受营收 0.65%、研发 876 家稀疏所限；"
                   "专利维为 6.80% 抽样），政策维 10/12 链无任何命中、人才维链级完全无数据；"
                   "按 §〇「始终有部分依赖维得不到足够数据」判『部分支持』。"
                   "另：需求原文要求『深圳与全国产业数据对比』，本库省外样本 0.18%，全国对标不可实现。"),
        "criteria": {"dims_available": 2, "dims_required": 4,
                     "policy_chains_with_signal": n_pol_avail,
                     "talent_chain_rows": m["talent_institute_on_chain_sz"][0]["n"],
                     "benchmark_cities": 4},
    }
    rep["elapsed_sec"] = None
    return rep


def main():
    t0 = time.time()
    rep = compute()
    rep["elapsed_sec"] = round(time.time() - t0, 1)
    S.write_out(METRIC, rep)
    print("available stats", rep["stats_sz_available"], "ranks", rep["rank_available"])
    print("wanghui4 stats", rep["stats_sz_wanghui4"], "ranks", rep["rank_wanghui4"],
          "changed", rep["rank_change"], "corr", rep["corr_available_vs_wanghui4"])
    for r in rep["per_chain"]:
        print(f"  {r['industry_name']:10s} avail={r['sz_score_available_dims']:6.2f} r={r['sz_rank_available']} "
              f"| wh4={r['sz_score_wanghui4_filled']:6.2f} r={r['sz_rank_wanghui4']} "
              f"| ent={r['dims']['企业']['深圳市']:.1f} pat={r['dims']['专利']['深圳市']:.1f}")


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
    out_json = here / "M_CHAIN_SZ_ADVANTAGE_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_SZ_ADVANTAGE_SCORE.py 等价）
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
        "metric_id": "M_CHAIN_SZ_ADVANTAGE_SCORE",
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
