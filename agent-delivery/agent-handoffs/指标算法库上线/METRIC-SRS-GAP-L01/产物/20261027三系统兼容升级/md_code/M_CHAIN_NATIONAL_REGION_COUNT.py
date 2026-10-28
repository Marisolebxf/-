#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_NATIONAL_REGION_COUNT 全国分布区域数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_NATIONAL_REGION_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_NATIONAL_REGION_COUNT · 全国分布区域数（20261021 改源版，直连 gkx）

口径（calc-logic 0.2.0，徐滕强 2026-10-14 拍板）
------------------------------------------------
指定产业链的链上主体总部所在**省级行政区**去重数，链维 KPI。空 province 不计数。

数据源（20261021 改源）
-----------------------
  `gkx.dwd_org_industry_tags`（2,283,762 行，链标签）
  `gkx.dwd_org_base_info`（189,116 行，province / city）
  链树 `gkx.dwd_industry_chain_info`（1,273 节点 / 12 条顶层链）
旧版走开发库 + 本地快照，本版全部现查三方库；公式、去重规则、空值规则未改。

本脚本要回答的不是「算得出来吗」，而是「算出来的数能不能叫全国」
--------------------------------------------------------------
链标签宇宙 2,283,762 行里，只有 52,906 条标签（35,046 家）能在 `dwd_org_base_info` 找到属地；
这 35,046 家里 35,022 家在广东（99.93%），省外仅 **24 家**。
因此 12 条链的「省级行政区去重数」实算只有 1~8，其中 2 条链只有 1 个省（广东）。

→ 结论：公式可执行、数值可复算，但「全国分布」语义不成立，判**部分支持**，
  且禁止把 24 家（或全底册的 339 家）当作全国覆盖的证据。

输出：code/M_CHAIN_NATIONAL_REGION_COUNT_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkx21_common import (CITY4, ROOTS, base_province_dist, base_rows,  # noqa: E402
                          chain_city_from_bridge, chain_names, chain_tag_universe,
                          bridge, write_out)

METRIC = "M_CHAIN_NATIONAL_REGION_COUNT"


def main():
    t0 = time.time()
    names = chain_names()
    br = bridge()
    geo = chain_city_from_bridge(br)
    tag = chain_tag_universe()
    prov_all, city_all = base_province_dist()
    n_pairs = {(r[3], r[4]) for r in base_rows()}

    # 链 → 省 / 市 计数（只在可落属地的子集上）
    per_chain = {}
    for r in ROOTS:
        prov = Counter(geo["chain_prov"].get(r, {}))
        city = Counter(geo["chain_city"].get(r, {}))
        prov.pop(None, None)
        prov.pop("", None)
        n_geo = sum(prov.values())
        per_chain[r] = {
            "chain": r, "name": names.get(r),
            "tag_enterprises": tag["counts"].get(r),
            "geo_matched": n_geo,
            "geo_match_pct": round(n_geo / tag["counts"][r] * 100, 2) if tag["counts"].get(r) else None,
            "region_count": len(prov),
            "province_dist": dict(prov.most_common()),
            "city_count": len([c for c in city if c]),
            "city_dist": dict(city.most_common(6)),
        }

    all_prov = Counter()
    seen_cc = {}
    for b in br:
        p = b["p"]
        seen_cc.setdefault((p, b["cc"]), True)
    for p, cc in seen_cc:
        all_prov[p] += 1
    n_geo = len({b["cc"] for b in br if b["cc"]})
    out_guangdong = {p: n for p, n in all_prov.items() if p and p != "广东省"}

    # 反例：如果直接拿 tags 宇宙当分母会得到什么
    naive = {r: per_chain[r]["region_count"] for r in ROOTS}
    gc = sum(n for p, n in prov_all.items() if p)
    gd = prov_all.get("广东省", 0)

    rep = {
        "metric_id": METRIC,
        "metric_name": "全国分布区域数",
        "date": "2026-10-21",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_NATIONAL_REGION_COUNT.md (0.2.0)",
        "formula": "COUNT(DISTINCT province) over chain members with non-empty province",
        "data_source": {
            "engine": "三方库 gkx（183.240.141.251:3318），唯一连库入口 code/_gkxdb.py",
            "tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_org_base_info", "gkx.dwd_industry_chain_info"],
            "join": "tags STRAIGHT_JOIN base ON base.external_id = tags.credit_code COLLATE utf8mb4_0900_ai_ci",
            "join_note": "两列排序规则不同（0900_ai_ci vs general_ci），且 tags.credit_code 无索引，"
                         "必须标签表驱动 + 哈希，否则退化为 2.28M×189K 嵌套循环",
        },
        "hard_constraint": {
            "headline": ("本库不存在可支撑「全国分布」的属地样本：链上 2,283,762 条标签中仅 52,906 条"
                         "（35,046 家，1.53%）可落属地，其中 35,022 家在广东（99.93%），省外合计 24 家"),
            "base_info_gd_share_pct": round(gd / gc * 100, 2) if gc else None,
            "base_info_out_of_gd": gc - gd,
            "base_info_n": gc,
            "tags_universe": tag["n_all"],
            "tags_distinct_credit": tag["n_cc"],
            "geo_joinable": n_geo,
            "geo_join_rows": geo["tag_rows_joinable"],
            "geo_join_pct": round(n_geo / (tag["n_cc"] or 1) * 100, 2),
            "chain_tagged_out_of_gd": sum(out_guangdong.values()),
            "note": ("省外 24 家的口径是「既有产业链标签、又能落到主档属地」的企业；"
                     "全底册省外 339 家是另一个更大的集合，两者都远不足以代表全国。"),
        },
        "per_chain": [per_chain[r] for r in ROOTS],
        "distribution": {
            "region_count_values": sorted(set(naive.values())),
            "chains_with_1_province": [r for r in ROOTS if naive[r] == 1],
            "chains_with_le2_provinces": [r for r in ROOTS if naive[r] <= 2],
            "max_region_count": max(naive.values()),
            "median_region_count": sorted(naive.values())[len(naive) // 2],
            "out_of_guangdong_detail": out_guangdong,
        },
        "base_info_distribution": {
            "source": "gkx.dwd_org_base_info GROUP BY province/city（现查）",
            "n_pairs": len(n_pairs),
            "total": gc,
            "guangdong_pct": round(gd / gc * 100, 2) if gc else None,
            "province_top": dict(sorted(prov_all.items(), key=lambda x: -x[1])[:8]),
            "city_top": dict(sorted(city_all.items(), key=lambda x: -x[1])[:8]),
        },
        "naive_trap": {
            "what_if_use_tag_universe": ("若把 2,283,762 条链标签当分母，会得出「每链覆盖全国」的错觉；"
                                         "实际这 2.28M 条标签里 97.7% 没有任何属地字段可查，"
                                         "剩下 2.3% 几乎全部落在深圳都市圈"),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": ("省级行政区轴与链—企桥结构齐全，公式可执行、数值可复算；"
                       "但链上主体 97.7% 无属地、可落属地的 99.93% 在广东，省外仅 24 家，"
                       "「全国分布」这一关键依赖维在本库无样本 → 按 §〇 判部分支持。"
                       "不得把 24 家（或底册省外 339 家）冒充全国覆盖。"),
            "criteria": {"structure": True, "province_axis": True,
                         "national_sample": False, "computable": True},
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    write_out(METRIC, rep)
    print(json.dumps({"hard": rep["hard_constraint"], "dist": rep["distribution"]},
                     ensure_ascii=False, indent=1))
    for p in rep["per_chain"]:
        print(p["chain"], p["name"], p["tag_enterprises"], p["geo_matched"], p["region_count"])


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
    out_json = here / "M_CHAIN_NATIONAL_REGION_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_NATIONAL_REGION_COUNT.py 等价）
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
        "metric_id": "M_CHAIN_NATIONAL_REGION_COUNT",
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
