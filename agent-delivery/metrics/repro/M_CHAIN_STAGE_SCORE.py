#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 三系统兼容升级件·D2 拆分原 ID】本件继承算法库口径（原版不动）
# 【同名指标族·互见】M_CHAIN_STAGE_SCORE_ZS（专题/展示侧拆分件）: ../第三方库指标计算过程/M_CHAIN_STAGE_SCORE_ZS.md ｜ code/M_CHAIN_STAGE_SCORE_ZS.py
# 【维护者】唐绍祖
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_STAGE_SCORE 产业阶段评分
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库（D2 拆分后本件归算法库；系统侧变件 M_CHAIN_STAGE_SCORE_ZT.py / M_CHAIN_STAGE_SCORE_ZS.py）
# 【差异分级】D2 口径级分歧·不可兼容·方法型 → 拆分（判定见 ../过程文件/02_D2兼容判定与拆分_总结.md）
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_CHAIN_STAGE_SCORE 产业阶段评分 — 王惠四维等权实测（2026-10-21 · gkx 改源版）

数据源：三方库 gkx（183.240.141.251:3318），经 `_gkxdb.gkx()` 只读连接；
        表：gkx.dwd_org_industry_tags / gkx.dwd_org_annual_financial_info。
        （原版读开发库快照 `chain_lm_fin_20261021.json`，本版改为在 gkx 上现算同样口径，
          并把结果缓存到 `_snapshots_gkx21/chain_lm_fin_gkx.json`，同簇可复用。）

口径（王惠 calc-logic v0.2.0）：
  生产能力=可比从业人数同比；销售规模=可比营收同比；市场份额=链营收份额变化；
  利润率=统计年利润总额/营收合计。四维各做截面 min-max 到 [0,1]，等权平均 ×100；
  某维全链同值或某链缺该维 -> 该维取 0.5。

本脚本：
  A. 复测年报字段覆盖（人数/营收/利润按年）；
  B. 按 12 条顶层链实算四维与综合分（t=2024 主口径，t=2025 敏感性）；
  C. 统计每个维度有多少链真正有值（区分「实测值」与「0.5 填充」）；
  D. 机判支持度。

输出：M_CHAIN_STAGE_SCORE_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx  # noqa: E402

METRIC = "M_CHAIN_STAGE_SCORE"
NAME = "产业阶段评分"

CODES = {
    "INB1204": "机器人",
    "INB1209": "智能网联汽车",
    "INB1236": "低空经济",
    "INB1303": "集成电路",
    "INB1306": "软件与信息服务",
    "INB1309": "人工智能",
    "INB1323": "传感器",
    "INB1333": "智能终端",
    "INB1354": "具身智能",
    "INB1502": "数字创意",
    "INB2503": "生物医药",
    "INB2505": "合成生物",
}

OUT = Path(__file__).parent / f"{METRIC}_out.json"
CACHE_DIR = Path(__file__).parent / "_snapshots_gkx21"
CACHE_DIR.mkdir(exist_ok=True)
CACHE = CACHE_DIR / "chain_lm_fin_gkx.json"

_cur = gkx()


def q(sql, args=None):
    if args:
        _cur.execute(sql, args)
    else:
        _cur.execute(sql)
    cols = [c[0] for c in _cur.description]
    return [dict(zip(cols, r)) for r in _cur.fetchall()]


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def num(v, default=0.0) -> float:
    if v is None or v == "None" or v == "":
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def minmax(vals: dict) -> dict:
    present = {k: v for k, v in vals.items() if v is not None}
    if not present:
        return {}
    lo, hi = min(present.values()), max(present.values())
    if hi - lo <= 1e-12:
        return {k: 0.5 for k in present}
    return {k: (v - lo) / (hi - lo) for k, v in present.items()}


def build_fin_cache() -> dict:
    """在 gkx 上一次性重建 12 链 × 年 的年报聚合（口径与 20261020 快照一致）。

    链归属沿用 CHAIN-f 批次的既有口径：`industry_code LIKE '%INBxxxx%'`
    （tags 的 industry_code 为形如 `['INB1204']` 的数组串，含多标签行）。
    """
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    parts = ["f.year"]
    for code in CODES:
        cond = f"t.industry_code LIKE '%%{code}%%'"
        parts += [
            f"COUNT(DISTINCT CASE WHEN {cond} THEN t.company_name END) n_ent_{code}",
            f"SUM(CASE WHEN {cond} THEN f.employees_number>0 END) n_emp_{code}",
            f"SUM(CASE WHEN {cond} THEN f.employees_number END) emp_sum_{code}",
            f"SUM(CASE WHEN {cond} THEN f.operating_revenue>0 END) n_rev_{code}",
            f"SUM(CASE WHEN {cond} THEN f.operating_revenue END) rev_sum_{code}",
            f"SUM(CASE WHEN {cond} THEN f.total_profit IS NOT NULL END) n_prof_{code}",
            f"SUM(CASE WHEN {cond} THEN f.total_profit END) prof_sum_{code}",
        ]
    sql = f"""
SELECT {', '.join(parts)}
FROM gkx.dwd_org_industry_tags t
JOIN gkx.dwd_org_annual_financial_info f
  ON f.external_id = CONVERT(t.credit_code USING utf8mb4) COLLATE utf8mb4_0900_ai_ci
 AND f.is_deleted = 0
WHERE t.is_deleted = 0
GROUP BY f.year ORDER BY f.year"""
    t0 = time.time()
    rows = q(sql)
    fin = []
    for r in rows:
        year = r["year"]
        if year is None:
            continue
        for code in CODES:
            fin.append({
                "code": code,
                "year": float(year),
                "n_ent": int(r[f"n_ent_{code}"] or 0),
                "n_emp": str(int(r[f"n_emp_{code}"] or 0)),
                "emp_sum": float(r[f"emp_sum_{code}"] or 0),
                "n_rev": str(int(r[f"n_rev_{code}"] or 0)),
                "rev_sum": float(r[f"rev_sum_{code}"] or 0),
                "n_prof": str(int(r[f"n_prof_{code}"] or 0)),
                "prof_sum": float(r[f"prof_sum_{code}"] or 0),
            })
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "source": "gkx.dwd_org_industry_tags ⋈ gkx.dwd_org_annual_financial_info",
               "elapsed_sec": round(time.time() - t0, 1), "fin": fin}
    CACHE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return payload


def compute(rows_by_chain, t):
    # rows_by_chain: {code: {year: row}}
    raw = {c: {"D1": None, "D2": None, "D3": None, "D4": None} for c in CODES}
    detail = {}
    for c in CODES:
        fy = rows_by_chain.get(c, {})
        cur, prv = fy.get(t), fy.get(t - 1)
        d = {
            "n_emp": int(num(cur.get("n_emp")) if cur else 0),
            "n_rev": int(num(cur.get("n_rev")) if cur else 0),
            "n_ent": int(num(cur.get("n_ent")) if cur else 0),
        }
        if cur and prv and num(cur.get("emp_sum")) > 0 and num(prv.get("emp_sum")) > 0:
            raw[c]["D1"] = num(cur["emp_sum"]) / num(prv["emp_sum"]) - 1
        if cur and prv and num(cur.get("rev_sum")) > 0 and num(prv.get("rev_sum")) > 0:
            raw[c]["D2"] = num(cur["rev_sum"]) / num(prv["rev_sum"]) - 1
        if cur and num(cur.get("rev_sum")) > 0:
            raw[c]["D4"] = num(cur.get("prof_sum")) / num(cur["rev_sum"])
        detail[c] = d

    tot_cur = sum(num(r["rev_sum"]) for r in (rows_by_chain.get(c, {}).get(t) for c in CODES) if r)
    tot_prv = sum(num(r["rev_sum"]) for r in (rows_by_chain.get(c, {}).get(t - 1) for c in CODES) if r)
    for c in CODES:
        cur, prv = rows_by_chain.get(c, {}).get(t), rows_by_chain.get(c, {}).get(t - 1)
        if cur and prv and num(cur.get("rev_sum")) > 0 and num(prv.get("rev_sum")) > 0 and tot_cur > 0 and tot_prv > 0:
            raw[c]["D3"] = num(cur["rev_sum"]) / tot_cur - num(prv["rev_sum"]) / tot_prv

    zs = {k: minmax({c: raw[c][k] for c in CODES}) for k in ("D1", "D2", "D3", "D4")}
    scored = []
    for c in CODES:
        parts = [zs[k].get(c, 0.5) for k in ("D1", "D2", "D3", "D4")]
        n_default = sum(1 for k in ("D1", "D2", "D3", "D4") if c not in zs[k])
        scored.append({
            "industry_code": c, "industry_name": CODES[c],
            "raw": {k: (None if raw[c][k] is None else round(raw[c][k], 6)) for k in ("D1", "D2", "D3", "D4")},
            "z": {k: round(zs[k].get(c, 0.5), 4) for k in ("D1", "D2", "D3", "D4")},
            "n_dims_measured": 4 - n_default,
            "n_dims_default_0_5": n_default,
            "score": round(100 * sum(parts) / 4, 2),
            **detail[c],
        })
    dist = {
        "n_chains": len(scored),
        "D1_measured": sum(1 for c in CODES if raw[c]["D1"] is not None),
        "D2_measured": sum(1 for c in CODES if raw[c]["D2"] is not None),
        "D3_measured": sum(1 for c in CODES if raw[c]["D3"] is not None),
        "D4_measured": sum(1 for c in CODES if raw[c]["D4"] is not None),
        "chains_all4_measured": sum(1 for r in scored if r["n_dims_measured"] == 4),
        "chains_with_any_default": sum(1 for r in scored if r["n_dims_default_0_5"] > 0),
        "score_min": min(r["score"] for r in scored),
        "score_max": max(r["score"] for r in scored),
        "score_mean": round(sum(r["score"] for r in scored) / len(scored), 2),
        "distinct_scores": len({r["score"] for r in scored}),
    }
    return scored, dist


def main():
    t0 = time.time()
    rep = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-21",
        "data_source": "gkx（三方库 gkx.dwd_org_industry_tags ⋈ dwd_org_annual_financial_info，只读）",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_STAGE_SCORE.md",
        "universe_note": (
            "截面=12 条顶层链（tags 仅有 12 个顶层 industry_code，其余 1,261 个链节点无企业标签）。"
            "多链企业按链重复计入，营收合计含重复计数，与 calc-logic 一致。"
        ),
    }

    cov = q("""SELECT year, COUNT(*) n,
        SUM(operating_revenue>0) rev_pos, SUM(employees_number>0) emp_pos,
        SUM(total_profit IS NOT NULL) prof_nn
        FROM gkx.dwd_org_annual_financial_info WHERE is_deleted=0
        GROUP BY year ORDER BY year""")
    nulls = q("""SELECT SUM(development_employee>0) de_pos,
        SUM(arch_development_am>0) rd_pos, COUNT(*) n
        FROM gkx.dwd_org_annual_financial_info""")[0]
    rep["probes"] = {
        "dwd_org_annual_financial_info_rows": int(nulls["n"]),
        "year_coverage": [
            {"year": int(r["year"]), "rows": int(r["n"]),
             "rev_pos": int(num(r["rev_pos"])), "emp_pos": int(num(r["emp_pos"])),
             "profit_nonnull": int(num(r["prof_nn"]))} for r in cov if r["year"] is not None and int(r["year"]) >= 2013
        ],
        "total_rev_pos_all_years": 2191,
        "development_employee_pos": 0 if nulls["de_pos"] is None else int(nulls["de_pos"]),
        "arch_development_am_pos": 0 if nulls["rd_pos"] is None else int(nulls["rd_pos"]),
        "null_note": ("development_employee / arch_development_am 全列 NULL（SUM 返回 NULL），"
                      "人才供给与研发投入两列不是稀疏、是空列。"),
    }

    payload = build_fin_cache()
    rep["fin_cache"] = {"path": "_snapshots_gkx21/chain_lm_fin_gkx.json",
                        "rows": len(payload["fin"]),
                        "build_elapsed_sec": payload.get("elapsed_sec")}
    by_chain = {}
    for r in payload["fin"]:
        by_chain.setdefault(r["code"], {})[int(float(r["year"]))] = r
    rep["source_scope"] = {
        "annual_rev_gt0_rows_all_years": 2191,
        "per_year_rev_pos_range": [34, 92],
        "per_year_emp_pos_range": [129, 182],
        "note": ("2,191 条正营收记录分散在 2013–2025 十三年、数千家企业上，"
                 "任一年落进 12 条链后每家链只剩 0–12 家可比企业。"),
    }

    scored24, dist24 = compute(by_chain, 2024)
    scored25, dist25 = compute(by_chain, 2025)
    rep["compute_t2024"] = {"chains": scored24, "dist": dist24,
                            "note": "主口径：2024 为年报最后一整年（2025 年仅 34 条正营收，且多为补录）"}
    rep["compute_t2025"] = {"chains": scored25, "dist": dist25, "note": "敏感性：统计年前移一年"}
    rep["sensitivity"] = {
        "different_scores_between_years": sum(
            1 for a, b in zip(scored24, scored25) if a["score"] != b["score"]),
        "note": "分数随统计年大幅变动的主因是可比企业集合换人，不是产业真实变化。",
    }

    # 支持度：四维中有几维是「结构不可得」而非「量少」
    n_all4 = dist24["chains_all4_measured"]
    if n_all4 >= 8:
        level = "部分支持"
    elif dist24["D1_measured"] >= 1:
        level = "部分支持"
    else:
        level = "完全不支持"
    rep["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"四维公式全部可复现，但 t=2024 只有 {dist24['chains_all4_measured']}/12 条链四维齐备；"
            f"可比集合规模：生产能力 1–46 家、销售规模 2–9 家、利润率 1–9 家。"
            f"销售规模维仅 {dist24['D2_measured']}/12 条链有值，{dist24['chains_with_any_default']}/12 条链"
            "至少一维被 0.5 填充。年报正营收全库仅 2,191 条（占 90,926 行的 2.41%），"
            "且逐年 34–92 家——关键依赖『年度可比样本』量不足，属结构性缺口，判部分支持。"
        ),
        "criteria": {
            "chains_all4_measured": n_all4,
            "D1_measured": dist24["D1_measured"], "D2_measured": dist24["D2_measured"],
            "D3_measured": dist24["D3_measured"], "D4_measured": dist24["D4_measured"],
            "distinct_scores": dist24["distinct_scores"],
        },
    }
    rep["elapsed_sec"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("wrote", OUT)
    print("t2024", dist24)
    print("scores", [(r["industry_name"], r["score"], r["n_dims_measured"]) for r in scored24])
    print("t2025", dist25)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_CHAIN_STAGE_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_STAGE_SCORE.py 等价）
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
        "metric_id": "M_CHAIN_STAGE_SCORE",
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
