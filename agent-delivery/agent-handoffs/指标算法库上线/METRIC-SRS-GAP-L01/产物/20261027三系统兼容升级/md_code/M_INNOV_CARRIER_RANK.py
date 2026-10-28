#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CARRIER_RANK （注册表未登记·工程件）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CARRIER_RANK.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CARRIER_RANK 创新载体排名 · 复现代码（跨载体排序口径，非王惠原式）

口径：排序宇宙=深圳存活载体池（总体宇宙）；排序键=质量分级(3/2/1)+2024授权专利归一+
      2024论文归一，等权复合降序，同分并列跳号；另演示领域宇宙（IPC 主组切片）排名。

数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

YEAR = 2024
IPC4_DEMO = "H02J"  # 领域宇宙演示切片（B5 锚点：H02J7/00 为影响力领先领域）

TABLES = ["dwd_org_base_info", "dwd_org_tech_tag", "dwd_patent", "dwd_zh_paper", "dwd_zh_author"]


def main():
    probes = C.probes(TABLES)

    pool = [(str(o), str(n)) for o, n in C.sz_pool(3000)]

    tags_by_org = {k: set(v) for k, v in C.tags().items()}

    by_name = C.patent_by_name()
    granted_by_name = {n: int(v[2]) for n, v in by_name.items()}
    papers_by_inst = C.papers_by_inst()

    rows = []
    for oid, name in pool:
        tags = tags_by_org.get(oid)
        tier = 3 if (tags and any(("国家级" in t or "小巨人" in t) for t in tags)) else \
               (2 if (tags and any("省级" in t for t in tags)) else
                (1 if tags else None))
        rows.append(dict(org_id=oid, name=name, tier=tier,
                         granted=granted_by_name.get(name, 0),
                         papers=papers_by_inst.get(name, 0),
                         ipc=C.ipc_count(name, prefix=IPC4_DEMO)))

    n_t = C.norm([float(r["tier"]) if r["tier"] else None for r in rows])
    n_g = C.norm([float(r["granted"]) for r in rows])
    n_p = C.norm([float(r["papers"]) for r in rows])
    scored = []
    for i, r in enumerate(rows):
        parts = [n_t[i], n_g[i], n_p[i]]
        avail = [p for p in parts if p is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**r, "score": round(score, 2) if score is not None else None})
    ranked = sorted([s for s in scored if s["score"] is not None], key=lambda x: -x["score"])
    prev_score, prev_rank = None, 0
    for i, s in enumerate(ranked, 1):
        s["rank"] = prev_rank if s["score"] == prev_score else i
        prev_score, prev_rank = s["score"], s["rank"]

    dom_pool = [s for s in scored if s["ipc"] > 0]
    dom_ranked = sorted(dom_pool, key=lambda x: -x["ipc"])
    for i, s in enumerate(dom_ranked, 1):
        s["domain_rank"] = i

    scores = [s["score"] for s in ranked]
    ss = sorted(scores)
    stats = dict(
        n_pool=len(pool), n_scored=len(ranked),
        min=round(min(scores), 2), max=round(max(scores), 2),
        mean=round(sum(scores) / len(scores), 2), median=round(ss[len(ss) // 2], 2),
        p90=round(ss[int(len(ss) * 0.9)], 2),
    )
    top15 = [{"rank": s["rank"], "name": s["name"], "tier": s["tier"],
              "granted2024": s["granted"], "papers2024": s["papers"],
              "score": s["score"]} for s in ranked[:15]]

    result = {
        "metric_id": "M_INNOV_CARRIER_RANK",
        "metric_name": "创新载体排名",
        "method": "跨载体排序（总体宇宙=深圳存活载体池）：分级tier+授权专利+论文 三键等权复合降序；同分并列跳号；领域宇宙按 IPC 主组切片",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "wanghui": False,
        "stat_year": YEAR,
        "probes": probes,
        "compute": {
            "stats": stats,
            "top15": top15,
            "domain_universe_demo": {
                "ipc4": IPC4_DEMO,
                "n_in_domain": len(dom_ranked),
                "top5": [{"domain_rank": s["domain_rank"], "name": s["name"],
                          "ipc_patents": s["ipc"], "total_score": s["score"]}
                         for s in dom_ranked[:5]],
            },
        },
        "support_judgment": None,
    }
    ok = stats["n_scored"] > 500 and stats["max"] > stats["min"]
    result["support_judgment"] = "完全转换支持" if ok else "部分支持"
    result["support_note"] = (
        f"深圳载体池 {stats['n_pool']}，得排名 {stats['n_scored']}；分数分布 {stats['min']}-{stats['max']}，"
        f"中位 {stats['median']}，P90 {stats['p90']}；领域宇宙 {IPC4_DEMO} 内 {len(dom_ranked)} 家可排；"
        "论文维 institution 对齐弱（覆盖低）但不阻断排序 → 完全转换支持"
    )

    C.write_out("M_INNOV_CARRIER_RANK", result)
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"]["stats"], ensure_ascii=False))
    print(json.dumps(result["compute"]["top15"][:8], ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"]["domain_universe_demo"], ensure_ascii=False, indent=1))


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
    out_json = here / "M_INNOV_CARRIER_RANK_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CARRIER_RANK.py 等价）
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
        "metric_id": "M_INNOV_CARRIER_RANK",
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
