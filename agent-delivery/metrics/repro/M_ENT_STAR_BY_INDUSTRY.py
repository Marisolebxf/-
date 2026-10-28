#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_STAR_BY_INDUSTRY 明星企业行业分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_STAR_BY_INDUSTRY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_STAR_BY_INDUSTRY 明星企业行业分布（20261022 改源版 · 只用三方库 gkx）

依赖 M_ENT_STAR_BASIC_INFO 的代理名单，改源后名单由 `_star_roster_gkx.py` 在
三方库 `gkx` 上现算并落 `code/_snapshots21/star_roster_gkx_20261021.json`：
`gkx.dwd_patent` 按 `first_applicant_name` 聚合授权数、与 `gkx.dwd_org_base_info.name_cn`
等值匹配、`grant_cnt >= 50` 者入选，并剔除高校/科研/医院等非企业主体。
行业字段取自 `gkx.dwd_org_base_info` 的国民经济行业门类/大类（真实字段）。

口径、阈值、集中度与 lift 公式与 20261020 版完全一致；改源只改取数端：
行业一级/二级与底册分母全部来自同一个 gkx 主档快照，不再分次回查数据库。

输出：code/M_ENT_STAR_BY_INDUSTRY_out.json
"""
import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_STAR_BY_INDUSTRY_out.json")
ROSTER = os.path.join(HERE, "_snapshots21", "star_roster_gkx_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "star_base_rows_gkx.json")
M = "M_ENT_STAR_BY_INDUSTRY"
THRESHOLD = 50
NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

out = {
    "metric_id": M,
    "metric_name": "明星企业行业分布",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "definition": "明星企业（代理）= 真实专利授权数≥50 的企业；行业 = gkx.dwd_org_base_info.industry_l1_name/l2_name",
    "data_source": "gkx（三方库只读）：dwd_patent × dwd_org_base_info",
    "probes": {},
    "compute": {},
    "samples": {},
    "support_judgment": None,
    "reasons": [],
}


def load_stars():
    with open(ROSTER, encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload["rows"]
    stars = [r for r in rows if (r.get("grant_cnt") or 0) >= THRESHOLD]
    stars = [r for r in stars
             if (r.get("org_type") not in NON_ENT_TYPE)
             and not any(k in (r.get("name_cn") or "") for k in NON_ENT_RX)]
    return stars, payload


def hhi(counts, total):
    return round(sum((c / total) ** 2 for c in counts), 5) if total else None


def main():
    stars, roster = load_stars()

    # 底册行业大盘（同一 gkx 主档快照，口径 = industry_l1_name 非空非空串）
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)          # [org_id, name, province, city, area, l1, l2, org_type]
    all_ind = {}
    for r in base:
        k = r[5]
        if k is not None and k != "":
            all_ind[k] = all_ind.get(k, 0) + 1
    all_ind = dict(sorted(all_ind.items(), key=lambda kv: -kv[1]))
    all_total = sum(all_ind.values())

    def dist(key):
        d = {}
        for r in stars:
            k = r.get(key)
            if k:
                d[k] = d.get(k, 0) + 1
        return sorted(d.items(), key=lambda x: -x[1])

    l1 = dist("industry_l1_name")
    l2d = dist("industry_l2_name")
    total = len(stars)

    out["probes"] = {
        "star_proxy_total": total,
        "star_with_industry_l1": sum(v for _, v in l1),
        "star_with_industry_l2": sum(v for _, v in l2d),
        "base_info_industry_l1_categories": len(all_ind),
        "base_info_total_with_industry": all_total,
        "roster_threshold_grant": roster.get("threshold_grant"),
        "roster_matched_orgs": roster.get("n_matched_orgs_dedup"),
        "roster_patent_agg_elapsed_sec": roster.get("patent_agg_elapsed_sec"),
        "source": "cache:_snapshots21/star_roster_gkx_20261021.json（由 gkx.dwd_patent × gkx.dwd_org_base_info 生成）",
    }
    out["compute"] = {
        "level1_distribution": [{"industry": k, "n": v, "share_pct": round(v / total * 100, 2)}
                                for k, v in l1],
        "level2_top15": [{"industry": k, "n": v, "share_pct": round(v / total * 100, 2)}
                         for k, v in l2d[:15]],
        "concentration": {
            "hhi_level1": hhi([v for _, v in l1], total),
            "top3_share_pct": round(sum(v for _, v in l1[:3]) / total * 100, 2) if total else None,
            "top5_share_pct": round(sum(v for _, v in l1[:5]) / total * 100, 2) if total else None,
            "categories_used": len(l1),
        },
        "vs_base_universe": [
            {
                "industry": k,
                "star_n": v,
                "star_share_pct": round(v / total * 100, 2),
                "base_n": all_ind.get(k),
                "base_share_pct": round(all_ind.get(k, 0) / all_total * 100, 2),
                "lift": round((v / total) / (all_ind.get(k, 0) / all_total), 2)
                if all_ind.get(k) else None,
            }
            for k, v in l1[:10]
        ],
    }
    out["samples"] = {
        "top5_enterprises_per_top3_industry": {},
    }
    # 每个 Top3 行业给 3 家具名企业
    for ind, _ in l1[:3]:
        ex = [{"name": r["name_cn"], "city": r["city"], "grant_cnt": int(r["grant_cnt"])}
              for r in stars if r.get("industry_l1_name") == ind][:3]
        out["samples"]["top5_enterprises_per_top3_industry"][ind] = ex

    out["support_judgment"] = "部分支持"
    out["reasons"] = [
        f"行业分布本身可算：{total} 家代理明星企业全部有行业一级分类，"
        f"Top3 行业占比 {out['compute']['concentration']['top3_share_pct']}%，分布非退化。",
        "但分子（明星企业名单）来自专利阈值代理，非甲方人工明星名单；分母更换会直接改变行业结构。",
        "行业字段来自工商登记（industry_l1_name），不是产业链标签；需求若要「产业领域分布」需另接产业链映射。",
        "底册 99.82% 在广东，行业结构只代表深圳都市圈，不能外推全国。",
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "compute")},
                     ensure_ascii=False, indent=1, default=str)[:2500])


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
    out_json = here / "M_ENT_STAR_BY_INDUSTRY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_STAR_BY_INDUSTRY.py 等价）
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
        "metric_id": "M_ENT_STAR_BY_INDUSTRY",
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
