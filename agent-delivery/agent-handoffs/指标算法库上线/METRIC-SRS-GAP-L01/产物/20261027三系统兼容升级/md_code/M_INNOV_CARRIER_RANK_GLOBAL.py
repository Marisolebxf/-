#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CARRIER_RANK_GLOBAL 创新载体多维度排名
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CARRIER_RANK_GLOBAL.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CARRIER_RANK_GLOBAL 创新载体多维度排名 · 复现代码（王惠 V1.5 口径）

消费 M_INNOV_CARRIER_INDEX_GLOBAL 指数，产出三个名次宇宙：总体 / 领域(IPC 主组) / 地区(城市)。
入集/三维/归一与 INDEX_GLOBAL 完全一致（同批 3,000 载体），此处仅做 RANK 与宇宙切片。
RANK 语义：同分同名次（1,1,3...），与王惠 logic「RANK(index_score) 地区内」一致。

数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

YEAR = 2024
CARRIER_N = 2000

TABLES = ["dwd_org_base_info", "dwd_research_institute_base_info", "dwd_forg_base_info",
          "dwd_org_annual_financial_info", "dwd_org_stock_finance_info", "dwd_org_tech_tag",
          "dwd_patent", "dwd_zh_paper"]


NULLISH = {"", "NULL", "NONE", "-"}


def _valid_name(n):
    return bool(n) and str(n).strip().upper() not in NULLISH


def _top1(group, key):
    """取某宇宙内名次最高且名称非占位符的载体。"""
    valid = [x for x in group if x.get(key) is not None and _valid_name(x.get("name"))]
    return min(valid, key=lambda x: x[key]) if valid else None


def add_ranks(scored, key_name="rank"):
    """对有分载体按分数降序给名次；同分同名次（SQL RANK 语义）。"""
    valid = [s for s in scored if s["score"] is not None]
    valid.sort(key=lambda x: -x["score"])
    rank = 0
    prev = None
    for idx, s in enumerate(valid, 1):
        if s["score"] != prev:
            rank = idx
            prev = s["score"]
        s[key_name] = rank
    return len(valid)


def main():
    probes = C.probes(TABLES)

    pool = C.carrier_pool(CARRIER_N, CARRIER_N // 4, CARRIER_N // 2)
    city_map = C.pool_city()
    rows = [(oid, name, city_map.get(oid, ""), src) for oid, name, src in pool]
    org_ids = list({r[0] for r in rows})

    annual = C.annual_fin(org_ids)
    stock = C.stock_fin(org_ids)

    by_name = C.patent_by_name()
    pat_by_name = {n: (int(v[0]), int(v[1])) for n, v in by_name.items()}
    zh_papers = C.papers_by_inst()

    hightech = {oid for oid, tags in C.tags().items()
                if any("高新技术" in t for t in tags)}

    carriers = []
    for oid, name, city, src in rows:
        a = annual.get(oid)
        dev = (a[1] if a and a[1] is not None else (a[2] if a else None))
        rev = a[3] if a else None
        if rev is None and oid in stock:
            rev = stock[oid][1]
        pat = pat_by_name.get(name, (0, 0))
        tag = (1 if oid in hightech else (None if src == "forg" else 0))
        carriers.append({"org_id": oid, "name": name, "city": city, "src": src,
                         "dev": float(dev) if dev is not None else None,
                         "rev": float(rev) if rev is not None else None,
                         "patents": pat[0], "granted": pat[1],
                         "papers": zh_papers.get(name, 0), "tag": tag})

    n_dev = C.norm([c["dev"] for c in carriers])
    n_rev = C.norm([c["rev"] for c in carriers])
    n_pat = C.norm([c["patents"] + c["papers"] for c in carriers])
    n_grt = C.norm([c["granted"] for c in carriers])
    n_tag = C.norm([c["tag"] for c in carriers])

    scored = []
    for i, c in enumerate(carriers):
        res_parts = [n_dev[i], n_rev[i]]
        res = (sum(p for p in res_parts if p is not None) / len(res_parts)) if any(p is not None for p in res_parts) else None
        cap_parts = [p for p in [n_grt[i], n_tag[i]] if p is not None]
        cap = (sum(cap_parts) / len(cap_parts)) if cap_parts else None
        dims = [res, n_pat[i], cap]
        avail = [d for d in dims if d is not None]
        score = (sum(avail) / len(avail) * 100) if avail else None
        scored.append({**c, "score": score})

    n_ranked_global = add_ranks(scored)

    by_city = {}
    for s in scored:
        key = (s["city"] or "").replace("市", "") or "未知"
        by_city.setdefault(key, []).append(s)
    city_rank_rows = []
    for key, group in by_city.items():
        n_g = add_ranks(group, "rank_region")
        top1 = _top1(group, "rank_region")
        city_rank_rows.append({"city": key, "n_carriers": len(group), "n_ranked": n_g,
                               "top1_name": top1["name"] if top1 else None,
                               "top1_score": round(top1["score"], 2) if top1 else None})
    city_rank_rows.sort(key=lambda r: -r["n_carriers"])

    names = [r[1] for r in rows]
    demo_fields = C.top_ipc4(names, 4)
    field_stats = []
    for f in demo_fields:
        field_hits = {nm: C.ipc_count(nm, exact=f) for nm in names}
        field_hits = {k: v for k, v in field_hits.items() if v > 0}
        members = [s for s in scored if s["name"] in field_hits]
        n_f = add_ranks(members, "rank_field")
        top1 = _top1(members, "rank_field")
        field_stats.append({"ipc4": f, "n_carriers": len(members), "n_ranked": n_f,
                            "top1_name": top1["name"] if top1 else None,
                            "top1_score": round(top1["score"], 2) if top1 else None})

    result = {
        "metric_id": "M_INNOV_CARRIER_RANK_GLOBAL",
        "metric_name": "创新载体多维度排名",
        "consumes": "M_INNOV_CARRIER_INDEX_GLOBAL（同批 3,000 载体指数，见同名 _out.json）",
        "method": "王惠 V1.5：RANK(index_score) 三个宇宙——总体 / 领域(IPC 主组) / 地区(城市)；同分同名次",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "stat_year": YEAR,
        "probes": probes,
        "compute": {
            "n_carriers": len(carriers),
            "global_rank": {"n_ranked": n_ranked_global},
            "top10_global": [{"name": s["name"], "src": s["src"], "score": round(s["score"], 2), "rank": s["rank"]}
                             for s in sorted([x for x in scored if x["score"] is not None],
                                             key=lambda x: (x["rank"], -x["patents"]))[:10]],
            "region_rank": city_rank_rows[:12],
            "field_rank_demo": field_stats,
        },
        "support_judgment": None,
    }
    n_city = len(city_rank_rows)
    n_field = len([f for f in field_stats if f["n_ranked"] >= 30])
    has_dist = n_ranked_global > 100
    if n_ranked_global and n_city >= 3 and n_field >= 3 and has_dist:
        result["support_judgment"] = "部分支持"
    else:
        result["support_judgment"] = "部分支持" if (n_ranked_global and has_dist) else "完全不支持"
    result["support_note"] = (
        f"三宇宙均可产出名次：总体 {n_ranked_global}、地区切片 {n_city} 城（前 {min(12, n_city)} 城入表）、"
        f"领域演示 {len(field_stats)} 个 IPC 主组（{n_field} 个 n_ranked≥30）；但指数上游三维中资源维严重缺测"
        f"（年报 dev/rev 覆盖极低）且指数依赖名称对齐——排名链路可算、指数语义被削弱 → 部分支持"
    )

    C.write_out("M_INNOV_CARRIER_RANK_GLOBAL", result)
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False))
    print(json.dumps(result["compute"], ensure_ascii=False)[:2200])


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
    out_json = here / "M_INNOV_CARRIER_RANK_GLOBAL_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CARRIER_RANK_GLOBAL.py 等价）
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
        "metric_id": "M_INNOV_CARRIER_RANK_GLOBAL",
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
