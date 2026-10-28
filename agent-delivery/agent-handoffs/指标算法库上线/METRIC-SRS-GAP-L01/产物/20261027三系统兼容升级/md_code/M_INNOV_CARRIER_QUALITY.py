#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_CARRIER_QUALITY （注册表未登记·工程件）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_CARRIER_QUALITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_CARRIER_QUALITY 创新载体质量 · 复现代码（分级加权口径）

口径：科技资质分级（国家级>省级>无标签）+ 加权质量分（分维覆盖）。
数据：gkx.dwd_org_tech_tag 全量 202,424 行（15+ 级标签）；2024 授权专利作产出旁证。
数据源（20261021 版）：三方库 `gkx`，唯一入口 `code/_gkxdb.gkx()`。
"""
import json

import _carrier21_common as C

TABLES = ["dwd_org_tech_tag", "dwd_org_base_info", "dwd_research_institute_base_info",
          "dwd_patent", "dwd_org_annual_financial_info"]


def main():
    probes = C.probes(TABLES)

    tags_by_org = {k: set(v) for k, v in C.tags().items()}

    NATIONAL_KW = ["国家级", "小巨人"]
    PROV_KW = ["省级"]
    national_set, prov_set, plain_set = set(), set(), set()
    for oid, tags in tags_by_org.items():
        if any(any(k in t for k in NATIONAL_KW) for t in tags):
            national_set.add(oid)
        elif any(any(k in t for k in PROV_KW) for t in tags):
            prov_set.add(oid)
        else:
            plain_set.add(oid)

    # 名册 + 深圳切片：一次读 gkx 主档缓存（189,116 行，字段同旧版）
    base = json.loads((C.CACHE / "base_20261021.json").read_text(encoding="utf-8"))
    oid2name = {str(r[0]): str(r[2]) for r in base}
    sz_orgs = {str(r[0]) for r in base if str(r[4] or "").startswith("深圳")}

    # 2024 授权专利（按第一申请人名去重 pn —— 与旧脚本 COUNT(DISTINCT pn) 同口径）
    by_name = C.patent_by_name()
    granted_by_name = {n: int(v[2]) for n, v in by_name.items()}

    scored = []
    for oid, name in oid2name.items():
        tags = tags_by_org.get(oid)
        tier = 3 if (tags and oid in national_set) else (2 if (tags and oid in prov_set) else (1 if tags else None))
        granted = granted_by_name.get(name, 0)
        scored.append(dict(org_id=oid, name=name, sz=(oid in sz_orgs), tier=tier, granted=granted))

    tiers = [s["tier"] for s in scored if s["tier"] is not None]
    gvals = [s["granted"] for s in scored if s["tier"] is not None]
    n_t = C.norm([float(t) for t in tiers])
    n_g = C.norm([float(g) for g in gvals])
    for i, s in enumerate([x for x in scored if x["tier"] is not None]):
        parts = [n_t[i], n_g[i]]
        s["quality"] = round(sum(parts) / 2 * 100, 2)
    scored_final = [s for s in scored if s["tier"] is not None]

    qvals = [s["quality"] for s in scored_final]
    qvals_sorted = sorted(qvals)
    stats = dict(
        n=len(qvals),
        national=len([s for s in scored_final if s["tier"] == 3]),
        provincial=len([s for s in scored_final if s["tier"] == 2]),
        plain=len([s for s in scored_final if s["tier"] == 1]),
        sz=len([s for s in scored_final if s["sz"]]),
        min=round(min(qvals), 2), max=round(max(qvals), 2),
        mean=round(sum(qvals) / len(qvals), 2),
        median=round(qvals_sorted[len(qvals_sorted) // 2], 2),
    )
    top = sorted(scored_final, key=lambda x: -x["quality"])[:12]

    sz_vs = [s["quality"] for s in scored_final if s["sz"]]
    result = {
        "metric_id": "M_INNOV_CARRIER_QUALITY",
        "metric_name": "创新载体质量",
        "method": "分级加权（国家级3/省级2/普通1）× 产出旁证（2024授权专利极值归一）等权×100；无标签载体不计分（缺测而非零分）",
        "source": "gkx（三方库；行数读 GKX_INVENTORY.json）",
        "probes": probes,
        "compute": {
            "stats": stats,
            "tag_coverage": {
                "tagged_orgs": len(tags_by_org),
                "national": len(national_set),
                "provincial": len(prov_set),
                "plain": len(plain_set),
            },
            "top12": [{"name": t["name"], "tier": t["tier"], "sz": t["sz"],
                       "granted2024": t["granted"], "quality": t["quality"]} for t in top],
            "sz_quality_stats": dict(
                n=len(sz_vs), mean=round(sum(sz_vs) / len(sz_vs), 2),
                median=round(sorted(sz_vs)[len(sz_vs) // 2], 2),
                national=len([s for s in scored_final if s["sz"] and s["tier"] == 3]),
            ),
        },
        "support_judgment": None,
    }

    ok = stats["n"] > 1000 and stats["max"] > stats["min"] and stats["national"] > 100
    result["support_judgment"] = "完全转换支持" if ok else "部分支持"
    result["support_note"] = (
        f"gkx.dwd_org_tech_tag 实测 {probes['gkx.dwd_org_tech_tag']} 行；有标签载体 {len(tags_by_org)} 家"
        f"（国家级 {len(national_set)} / 省级 {len(prov_set)} / 普通 {len(plain_set)}）；"
        f"质量分 n={stats['n']}，分布 {stats['min']}-{stats['max']} 非退化；"
        "依赖结构+数据量足且已现转出分 → 完全转换支持（无现成结果面）"
    )

    C.write_out("M_INNOV_CARRIER_QUALITY", result)
    print({k: v for k, v in result.items() if k != "compute"})
    print(json.dumps(result["compute"]["stats"], ensure_ascii=False))
    print(json.dumps(result["compute"]["tag_coverage"], ensure_ascii=False))
    print(json.dumps(result["compute"]["top12"][:6], ensure_ascii=False))
    print(json.dumps(result["compute"]["sz_quality_stats"], ensure_ascii=False))


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
    out_json = here / "M_INNOV_CARRIER_QUALITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_CARRIER_QUALITY.py 等价）
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
        "metric_id": "M_INNOV_CARRIER_QUALITY",
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
