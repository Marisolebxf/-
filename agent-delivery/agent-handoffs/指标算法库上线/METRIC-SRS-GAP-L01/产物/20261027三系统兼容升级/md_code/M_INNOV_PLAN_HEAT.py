#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_PLAN_HEAT 热度指数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_PLAN_HEAT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_PLAN_HEAT —— 热度指数（三方库 gkx 版，专利零 SQL）。

王惠三维：专利热度 / 论文热度 / 项目热度，对象 = IPC4，取值 0—100。
本报告补：258 个面板方向、源内百分位归一、参考年显式选择（专利 2024 / 论文 2023 / 项目 2021）。

专利计数只读 `_snapshots21/patent_ipc4_year_20261021.json`（零专利 SQL）；
论文/项目经缓存术语词典归到 IPC4，只打两张小表，共 2 条 SQL。
"""
from __future__ import annotations

import time

import _gkxdb as D
import _plan21_common as C

METRIC = "M_INNOV_PLAN_HEAT"
Y_PATENT, Y_PAPER, Y_PROJECT = 2024, 2023, 2021
T0 = time.time()


def q(sql: str) -> list[tuple]:
    cur = D.gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute(sql)
        return list(cur.fetchall())
    finally:
        cur.close()


def count_by_ipc(texts: list[str]) -> tuple[dict[str, int], int]:
    cnt: dict[str, int] = {}
    unassigned = 0
    for t in texts:
        top = C.assign_fast(t, k=1)
        if not top:
            unassigned += 1
            continue
        cnt[top[0][0]] = cnt.get(top[0][0], 0) + 1
    return cnt, unassigned


def heat(p_pat, p_pap, p_prj, mode: str) -> list[float]:
    n = len(p_pat)
    out = []
    for i in range(n):
        dims = [p_pat[i], p_pap[i], p_prj[i]]
        if mode == "available":
            out.append(round(sum(dims) / 3, 2))  # 缺失维的百分位已按 0 计，见下
        else:
            out.append(round(sum(dims) / 3, 2))
    return out


def main() -> None:
    d = C.ipc4_year()
    panel = C.panel_ipc4()
    idx = {ipc: i for i, ipc in enumerate(panel)}
    n = len(panel)

    pat = [d.get((ipc, Y_PATENT), [0, 0])[0] for ipc in panel]
    pat_org = [d.get((ipc, Y_PATENT), [0, 0])[1] for ipc in panel]

    # 论文 2023 — 1 条 SQL
    pap_rows = q(f"""SELECT zh_name, en_name FROM gkx.dwd_zh_paper
                     WHERE LEFT(CAST(cover_year_start AS CHAR),4)='{Y_PAPER}'""")
    pap_texts = [((r[0] or "") + " " + (r[1] or "")).strip() for r in pap_rows]
    pap_cnt, pap_un = count_by_ipc(pap_texts)

    # 论文 2024（敏感性）— 1 条 SQL
    pap24_rows = q("""SELECT zh_name, en_name FROM gkx.dwd_zh_paper
                      WHERE LEFT(CAST(cover_year_start AS CHAR),4)='2024'""")
    pap24_cnt, pap24_un = count_by_ipc([((r[0] or "") + " " + (r[1] or "")).strip() for r in pap24_rows])

    # 项目 2021 — 1 条 SQL
    prj_rows = q(f"""SELECT title, keywords FROM gkx.dwd_zh_project
                     WHERE LEFT(CAST(approval_year AS CHAR),4)='{Y_PROJECT}'""")
    prj_cnt, prj_un = count_by_ipc([((r[0] or "") + " " + (r[1] or "")).strip() for r in prj_rows])

    pv_pat = [float(x) for x in pat]
    pv_pap = [float(pap_cnt.get(ipc, 0)) for ipc in panel]
    pv_prj = [float(prj_cnt.get(ipc, 0)) for ipc in panel]
    pv_pap24 = [float(pap24_cnt.get(ipc, 0)) for ipc in panel]

    p_pat, p_pap, p_prj = C.rank_pct(pv_pat), C.rank_pct(pv_pap), C.rank_pct(pv_prj)
    p_pap24 = C.rank_pct(pv_pap24)

    # 主口径：可得维等权（缺失维不参与），另给「缺失维记 0」的对照
    def combine(pp, pq, pr, mode):
        res = []
        for i in range(n):
            vals = [pp[i]]
            if pv_pap[i] > 0:
                vals.append(pq[i])
            if pv_prj[i] > 0:
                vals.append(pr[i])
            res.append(round(sum(vals) / len(vals), 2) if mode == "avail" else round((pp[i] + pq[i] + pr[i]) / 3, 2))
        return res

    main_h = combine(p_pat, p_pap, p_prj, "avail")
    zero_h = combine(p_pat, p_pap, p_prj, "zero")
    v2_h = combine(p_pat, p_pap24, p_prj, "avail")

    rows = [{
        "ipc4": ipc, "patent_2024": pat[i], "patent_org_2024": pat_org[i],
        "paper_2023": int(pv_pap[i]), "project_2021": int(pv_prj[i]),
        "pct_patent": p_pat[i], "pct_paper": p_pap[i], "pct_project": p_prj[i],
        "n_dims": 1 + (1 if pv_pap[i] > 0 else 0) + (1 if pv_prj[i] > 0 else 0),
        "heat": main_h[i], "heat_zero_dim": zero_h[i], "heat_v2_paper2024": v2_h[i],
    } for i, ipc in enumerate(panel)]
    rows.sort(key=lambda r: -r["heat"])

    def topk(k):
        return rows[:k]

    hs = [r["heat"] for r in rows]
    out = {
        "metric_id": METRIC,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "db": {"host": "183.240.141.251:3318", "schema": "gkx",
               "tables": ["dwd_zh_paper", "dwd_zh_project"],
               "patent_source": "_snapshots21/patent_ipc4_year_20261021.json（零专利 SQL）"},
        "support_judgment": "部分支持",
        "judgment_reason": (
            "三维结构齐全、258 个方向均出分，但三源无法取同一年（专利 2024 / 论文 2023 / 项目 2021），"
            "论文维单日批量入库、项目维 2022 起停录，且论文/项目方向归属依赖 Top-1 22.14% 的术语桥；"
            "「全球监测」所需国际语料不具备"
        ),
        "formula": {
            "heat": "Heat_i = mean_{s∈可得维} pct_s(x_{i,s})，" "pct=100*(rank-1)/(n-1)，n=258",
            "reference_years": {"patent": Y_PATENT, "paper": Y_PAPER, "project": Y_PROJECT},
            "normalization": "源内百分位（抗三源量纲差三个数量级）",
        },
        "base_years": C.base_year_block(
            used=[Y_PROJECT, Y_PAPER, Y_PATENT], missing=[],
            note="热度是横截面指标，分母为「258 个面板方向内的排名」，不涉及时序分母；"
                 "三个参考年各自取该源最后一个完整年，异年拼接已在正文披露。"),
        "panel": {"n_ipc4": n, "rule": "2021 与 2024 年专利量均 ≥200 件", "source_rows": C.panel_meta()},
        "sources": {
            "patent": {"year": Y_PATENT, "panel_total": sum(pat),
                       "n_zero": sum(1 for x in pat if x == 0),
                       "org_total": sum(pat_org)},
            "paper": {"year": Y_PAPER, "rows": len(pap_rows), "assigned": len(pap_rows) - pap_un,
                      "unassigned": pap_un,
                      "assigned_rate": round((len(pap_rows) - pap_un) / len(pap_rows), 4) if pap_rows else None,
                      "panel_total": int(sum(pv_pap)), "n_zero": sum(1 for x in pv_pap if x == 0)},
            "paper_2024": {"rows": len(pap24_rows), "unassigned": pap24_un,
                           "panel_total": int(sum(pv_pap24))},
            "project": {"year": Y_PROJECT, "rows": len(prj_rows), "assigned": len(prj_rows) - prj_un,
                        "unassigned": prj_un,
                        "assigned_rate": round((len(prj_rows) - prj_un) / len(prj_rows), 4) if prj_rows else None,
                        "panel_total": int(sum(pv_prj)), "n_zero": sum(1 for x in pv_prj if x == 0)},
        },
        "bridge": {"lexicon_ipc4": C.lexicon()["n_ipc4"], "lexicon_terms": C.lexicon()["n_terms"],
                   "validated_top1": 0.2214, "validated_top3": 0.4154,
                   "source": "缓存词典（_snapshots21/plan_ipc_lexicon_gkx21.json），本次未重扫专利"},
        "result": {
            "distribution": C.st(hs),
            "n_ge60": sum(1 for x in hs if x >= 60), "n_ge80": sum(1 for x in hs if x >= 80),
            "n_dims_1": sum(1 for r in rows if r["n_dims"] == 1),
            "n_dims_2": sum(1 for r in rows if r["n_dims"] == 2),
            "n_dims_3": sum(1 for r in rows if r["n_dims"] == 3),
            "top15": topk(15), "bottom10": rows[-10:], "all": rows,
        },
        "variants": {
            "v1_main": "论文 2023 · 项目 2021 · 可得维等权",
            "v2_paper2024": {"spearman_vs_v1": C.spearman(main_h, v2_h),
                             "top1": max(rows, key=lambda r: r["heat_v2_paper2024"])["ipc4"]},
            "v3_zero_dim": {"spearman_vs_v1": C.spearman(main_h, zero_h),
                            "distribution": C.st(zero_h),
                            "top1": max(rows, key=lambda r: r["heat_zero_dim"])["ipc4"],
                            "max": max(zero_h)},
        },
        "sql_count": 3,
        "elapsed_sec": None,
    }
    out["elapsed_sec"] = round(time.time() - T0, 1)
    C.write_out(METRIC, out)
    print(f"n={n} top1={rows[0]['ipc4']} {rows[0]['heat']} "
          f"paper_un={pap_un}/{len(pap_rows)} proj_un={prj_un}/{len(prj_rows)} in {out['elapsed_sec']}s")


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
    out_json = here / "M_INNOV_PLAN_HEAT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_PLAN_HEAT.py 等价）
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
        "metric_id": "M_INNOV_PLAN_HEAT",
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
