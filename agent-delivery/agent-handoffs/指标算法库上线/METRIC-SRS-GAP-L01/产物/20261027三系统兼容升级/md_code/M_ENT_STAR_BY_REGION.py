#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_STAR_BY_REGION 明星企业区域分布
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_STAR_BY_REGION.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ENT_STAR_BY_REGION 明星企业区域分布（20261022 改源版 · 只用三方库 gkx）

依赖代理名单缓存 `code/_snapshots21/star_roster_gkx_20261021.json`（由
`_star_roster_gkx.py` 在三方库 `gkx` 上现算：`gkx.dwd_patent` 按
`first_applicant_name` 聚合授权数、与 `gkx.dwd_org_base_info.name_cn` 等值匹配，
`grant_cnt >= 50` 入选并剔除高校/科研/医院）。属地字段取自
`gkx.dwd_org_base_info` 的 province / city / area（真实工商登记地）。

口径、阈值、集中度与 lift 公式与 20261020 版完全一致；改源只改取数端：
区县与底册分母都来自同一份 gkx 主档快照，不再分次回查数据库。

输出：code/M_ENT_STAR_BY_REGION_out.json
"""
import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M_ENT_STAR_BY_REGION_out.json")
ROSTER = os.path.join(HERE, "_snapshots21", "star_roster_gkx_20261021.json")
BASE = os.path.join(HERE, "_snapshots21", "star_base_rows_gkx.json")
M = "M_ENT_STAR_BY_REGION"
THRESHOLD = 50
NON_ENT_TYPE = {"事业单位", "民办非企业单位", "社会团体", "机关", "基金会", "群众团体"}
NON_ENT_RX = ("大学", "学院", "研究院", "研究所", "医院", "学校", "协会", "基金会")

out = {
    "metric_id": M,
    "metric_name": "明星企业区域分布",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "definition": "明星企业（代理）= 真实专利授权数≥50 的企业；区域 = gkx.dwd_org_base_info.province/city",
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
    total = len(stars)

    prov, city, dist_area = {}, {}, {}
    for r in stars:
        p = r.get("province")
        ct = r.get("city")
        if p:
            prov[p] = prov.get(p, 0) + 1
        if ct:
            city[ct] = city.get(ct, 0) + 1
        a = r.get("area")
        if a:
            dist_area[a] = dist_area.get(a, 0) + 1

    prov_d = sorted(prov.items(), key=lambda x: -x[1])
    city_d = sorted(city.items(), key=lambda x: -x[1])
    area_d = sorted(dist_area.items(), key=lambda x: -x[1])

    # 底册分母（同一 gkx 主档快照）
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)          # [org_id, name, province, city, area, l1, l2, org_type]
    base_total = len(base)
    base_prov_cnt = {}
    for r in base:
        p = r[2]
        if p is not None and p != "":
            base_prov_cnt[p] = base_prov_cnt.get(p, 0) + 1
    base_prov = sorted(base_prov_cnt.items(), key=lambda x: -x[1])[:8]

    out["probes"] = {
        "star_proxy_total": total,
        "star_with_province": sum(v for _, v in prov_d),
        "star_with_city": sum(v for _, v in city_d),
        "star_with_area": sum(v for _, v in area_d),
        "base_info_total": int(base_total),
        "roster_threshold_grant": roster.get("threshold_grant"),
        "roster_matched_orgs": roster.get("n_matched_orgs_dedup"),
        "roster_patent_agg_elapsed_sec": roster.get("patent_agg_elapsed_sec"),
        "source": "cache:_snapshots21/star_roster_gkx_20261021.json（由 gkx.dwd_patent × gkx.dwd_org_base_info 生成）",
        "coverage_disclosure": "底册 99.82% 在广东（深圳 50.55%/广州 26.23%/东莞 17.76%/惠州 5.28%），"
                               "省外样本不足 0.2%，全国名次不可解释，只可作省内/都市圈比较",
    }
    out["compute"] = {
        "province_distribution": [{"province": k, "n": v, "share_pct": round(v / total * 100, 2)}
                                  for k, v in prov_d],
        "city_top15": [{"city": k, "n": v, "share_pct": round(v / total * 100, 2)}
                       for k, v in city_d[:15]],
        "area_top10": [{"area": k, "n": v, "share_pct": round(v / total * 100, 2)}
                       for k, v in area_d[:10]],
        "concentration": {
            "hhi_city": hhi([v for _, v in city_d], total),
            "top1_city": city_d[0][0] if city_d else None,
            "top1_city_share_pct": round(city_d[0][1] / total * 100, 2) if city_d else None,
            "top3_city_share_pct": round(sum(v for _, v in city_d[:3]) / total * 100, 2) if total else None,
            "guangdong_share_pct": round(prov.get("广东省", 0) / total * 100, 2),
        },
        "vs_base_universe": [{
            "province": p,
            "base_n": int(n),
            "base_share_pct": round(int(n) / base_total * 100, 2),
            "star_n": prov.get(p, 0),
            "star_share_pct": round(prov.get(p, 0) / total * 100, 2),
        } for p, n in base_prov],
    }
    out["samples"] = {
        "top10_enterprises_shenzhen": [
            {"name": r["name_cn"], "city": r["city"], "industry_l1": r["industry_l1_name"],
             "grant_cnt": int(r["grant_cnt"])}
            for r in stars if r.get("city") == "深圳市"][:10],
        "top5_enterprises_other_cities": [
            {"name": r["name_cn"], "city": r["city"], "industry_l1": r["industry_l1_name"],
             "grant_cnt": int(r["grant_cnt"])}
            for r in stars if r.get("city") != "深圳市"][:5],
    }

    out["support_judgment"] = "部分支持"
    out["reasons"] = [
        f"区域分布可算：{total} 家代理明星企业，深圳占 {out['compute']['concentration']['top1_city_share_pct']}%，"
        f"Top3 城市占 {out['compute']['concentration']['top3_city_share_pct']}%，分布可解释。",
        "分子（明星名单）为专利阈值代理，与甲方 CMS 人工名单不等价，属地分布会随名单口径变化。",
        "底册 99.82% 在广东，省外不足 0.2%，「全国区域分布」不可解释，只能作深圳都市圈比较。",
        "工商注册地 ≠ 实际经营地（部分集团注册在深圳、生产在东莞/惠州），区域口径需甲方确认。",
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
    out_json = here / "M_ENT_STAR_BY_REGION_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_STAR_BY_REGION.py 等价）
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
        "metric_id": "M_ENT_STAR_BY_REGION",
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
