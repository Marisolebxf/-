#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CARRIER_VALUE_RANK_SZ 深圳创新载体创新价值排名
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CARRIER_VALUE_RANK_SZ.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CARRIER_VALUE_RANK_SZ 深圳创新载体创新价值排名 · 复现代码（王惠 V1.5-20260830，20261021 换源版）

入集：深圳存续载体（企业底册 + 科研机构底册）。
三维：技术价值(专利 value + 期刊 impact) / 应用价值(专利转移件数 + 论文下载) / 潜在影响力(专利被引 + 论文被引)。
深圳批内极值归一、等权 ×100、降序排名（并列同名次）。统计年 2024。
数据源：三方库 `gkx`（唯一入口 `code/_gkxdb.py`），**不含任何 demo_* / _devdb**。

换源说明（20261021）
--------------------
* 载体入集：`dwd_org_base_info` 深圳存续 `ORDER BY dwd_id LIMIT 2000` → 2,000 家；
  `dwd_research_institute_base_info` 深圳存续 → **0 家**（gkx 该表 1,014 行深圳机构，但 `reg_status`
  全部为空串，`LIKE '%存续%'` 不命中）——与旧版 `n_sz_carriers=2000` 完全一致。
  旧脚本无 `ORDER BY`，抽取不确定；本版按主键定序以便复现，集合语义不变。
* 技术维：`SUM(value)` 2024 按申请人名；期刊 `impact_score` 在 gkx 为 0 行非空 → 技术维实际只有专利一条腿。
* 应用维：转移表 2024 窗内仍按 JSON 名称文本包含匹配；论文 `download_num` 2024 窗内合计。
* 潜在维：`dwd_patent_cited`（20,515 行）按 pn 对齐；论文 `citation_num` 2024 窗内合计。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _gkx21_city as C  # noqa: E402
import _gkxdb  # noqa: E402

METRIC_ID = "M_INNOV_CARRIER_VALUE_RANK_SZ"
YEAR = 2024
SZ_LIMIT = 2000


def norm_vals(xs):
    xs2 = [x for x in xs if x is not None]
    if not xs2:
        return [None] * len(xs)
    lo, hi = min(xs2), max(xs2)
    if hi == lo:
        return [0.5 if x is not None else None for x in xs]
    return [((x - lo) / (hi - lo)) if x is not None else None for x in xs]


def sz_carriers():
    """深圳存续载体：企业底册 LIMIT 2000 + 科研机构底册 LIMIT 1000（后者实测 0 命中）。"""
    rows = C._q("SELECT org_id, name_cn FROM gkx.dwd_org_base_info "
                "WHERE reg_status LIKE '%%存续%%' AND city LIKE '%%深圳%%' "
                "ORDER BY dwd_id LIMIT %s", (SZ_LIMIT,))
    out = [(oid, nm, "cn") for oid, nm in rows]
    rows2 = C._q("SELECT org_id, name_cn FROM gkx.dwd_research_institute_base_info "
                 "WHERE reg_status LIKE '%%存续%%' AND city LIKE '%%深圳%%' "
                 "ORDER BY dwd_id LIMIT %s", (SZ_LIMIT // 2,))
    out += [(oid, nm, "inst") for oid, nm in rows2]
    return out


def journal_impact_nonnull():
    rows = C._q("SELECT COUNT(*) FROM gkx.dwd_zh_journal WHERE impact_score IS NOT NULL")
    return int(rows[0][0])


def main():
    probes = {t: C.inventory_rows(t) for t in
              ("dwd_org_base_info", "dwd_research_institute_base_info", "dwd_patent",
               "dwd_patent_cited", "dwd_patent_transfer", "dwd_zh_paper",
               "dwd_zh_paper_citation", "dwd_zh_journal")}
    rows = sz_carriers()
    names = {r[1] for r in rows if r[1]}
    if not names:
        raise SystemExit("no SZ carriers")

    scan = C.patent_scan()
    pat_value = {k: float(v) for k, v in scan["value_2024"].items() if k in names}
    pat_cited = {k: float(v) for k, v in scan["cited_2024"].items() if k in names}

    transfer_hit = {}
    for pn, tb, ta in C.transfer_2024():
        blob = f"{tb}|{ta}"
        for n in names:
            if n in blob:
                transfer_hit[n] = transfer_hit.get(n, 0) + 1
                break

    pinst = C.paper_institution_stats(YEAR)
    paper_dl = {n: pinst[n]["download"] for n in names if n in pinst}
    paper_cited = {n: pinst[n]["cited"] for n in names if n in pinst}
    paper_impact = {}  # impact_score 全 NULL（见 journal_impact_nonnull 探针）
    impact_nonnull = journal_impact_nonnull()

    carriers = []
    for oid, name, src in rows:
        tv, pi = pat_value.get(name), paper_impact.get(name)
        tech = None
        if tv is not None or pi is not None:
            tech = float(tv or 0) + float(pi or 0)
        app = float(transfer_hit.get(name, 0)) + float(paper_dl.get(name, 0) or 0)
        pot = float(pat_cited.get(name, 0)) + float(paper_cited.get(name, 0))
        carriers.append({"org_id": oid, "name": name, "src": src,
                         "tech": tech, "app": app, "pot": pot})

    n_t = norm_vals([c["tech"] for c in carriers])
    n_a = norm_vals([c["app"] for c in carriers])
    n_p = norm_vals([c["pot"] for c in carriers])

    scored = []
    for i, c in enumerate(carriers):
        dims = [n_t[i], n_a[i], n_p[i]]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**c, "score": score})

    valid = [s for s in scored if s["score"] is not None and (s["tech"] or s["app"] or s["pot"])]
    valid.sort(key=lambda x: -x["score"])
    rank, prev = 0, None
    for idx, s in enumerate(valid, 1):
        if s["score"] != prev:
            rank, prev = idx, s["score"]
        s["rank"] = rank

    scores = [s["score"] for s in valid]
    stats = {}
    if scores:
        ss = sorted(scores)
        stats = dict(n=len(scores), positive=len([s for s in scores if s > 0]),
                     min=round(min(scores), 2), max=round(max(scores), 2),
                     mean=round(sum(scores) / len(scores), 2), median=round(ss[len(ss) // 2], 2))

    cov = {
        "tech_patent_value": len([c for c in carriers if c["tech"] is not None]),
        "tech_paper_impact": len(paper_impact),
        "app_transfer_or_dl": len([c for c in carriers if c["app"] > 0]),
        "pot_cited": len([c for c in carriers if c["pot"] > 0]),
    }
    result = {
        "metric_id": METRIC_ID,
        "metric_name": "深圳创新载体创新价值排名",
        "method": "王惠 V1.5-20260830：深圳批内三维极值归一等权×100 降序排名",
        "stat_year": YEAR,
        "data_source": "gkx（三方库 183.240.141.251:3318，只读账号；不含任何演示库引用）",
        "probes": probes,
        "journal_impact_nonnull": impact_nonnull,
        "compute": {
            "n_sz_carriers": len(rows),
            "dim_coverage": cov,
            **({"stats": stats} if stats else {}),
            "top10": [{"name": t["name"], "tech": t["tech"], "app": t["app"],
                       "pot": t["pot"], "score": round(t["score"], 2), "rank": t["rank"]}
                      for t in valid[:10]],
        },
        "support_judgment": None,
    }
    tech_ok = cov["tech_patent_value"] > 50
    app_ok = cov["app_transfer_or_dl"] > 50
    pot_ok = cov["pot_cited"] > 50
    dims_ok_count = sum([tech_ok, app_ok, pot_ok])
    has_dist = bool(stats) and stats["max"] > stats["min"]
    if dims_ok_count == 3 and has_dist:
        result["support_judgment"] = "完全转换支持"
    elif dims_ok_count >= 1 and has_dist:
        result["support_judgment"] = "部分支持"
    else:
        result["support_judgment"] = "完全不支持"
    result["support_note"] = (
        f"深圳载体 {len(rows)}；三维覆盖：技术 {cov['tech_patent_value']}（专利 value 可算，期刊 impact 全 NULL 缺测）、"
        f"应用 {cov['app_transfer_or_dl']}（download_num 全 0；转移 JSON 名称对齐命中极低）、"
        f"潜在 {cov['pot_cited']}（2024 窗内 cited 无命中）；"
        f"排名可产出（n={stats.get('n', 0)}，专利价值驱动）但实质退化为技术维单维排序 → 部分支持"
    )

    path = HERE / f"{METRIC_ID}_out.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    print(json.dumps(result["compute"], ensure_ascii=False)[:1600])


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
    out_json = here / "M_INNOV_CARRIER_VALUE_RANK_SZ_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CARRIER_VALUE_RANK_SZ.py 等价）
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
        "metric_id": "M_INNOV_CARRIER_VALUE_RANK_SZ",
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
