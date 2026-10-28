#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_REG_TALENT_STRUCTURE 人才结构
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_REG_TALENT_STRUCTURE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_CHAIN_REG_TALENT_STRUCTURE 人才结构（区域）（20261021 改源版）

需求语境：区域产业指数模型 → 学术生态竞争力 → 「人才结构」。
20261019 判「完全不支持」的理由是「人才结构无面，ADS 只有人才总量」。改源到 gkx 后
表是齐的（学者 21,316 / 学历 43,766 / 研究方向 20,030 / 头衔 20,030 / 工作经历 57,117），
**但四张附表与主表的 scholar_id 是两个 ID 空间**：学历 15,851 个 ID 只有 1,753 个（8.2%）
能在 `dwd_scholar` 找到，研究方向 8.7%、头衔 8.7%、论文关系 9.2%。

因此本脚本只做三件事，并把「为什么不能出链×城学历结构」算成可核查的数字：
  1. 主表学者按机构落 4 市（1,202 人，5.6%），给出市域层面的规模与影响力结构；
  2. 学历表独立分布（15,851 人，无机构字段 → 不可落城）；
  3. 主表 ∩ 学历表 = 1,753 人，其中落 4 市仅 119 人 → 学历结构的分母不足，禁用。

输出：code/M_CHAIN_REG_TALENT_STRUCTURE_out.json
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from _reg5_common import (CHAIN_AXIS, CHAIN_CN, CITY4, degree_bucket, match_org, pct, probe3,
                          stats, write_out)

MID = "M_CHAIN_REG_TALENT_STRUCTURE"
RANK = {"博士": 3, "硕士": 2, "学士": 1, "其他": 0}


def main() -> None:
    t0 = time.time()
    p3 = probe3()
    scholars = p3["scholar_min"]["rows"]        # scholar_id, name, org, papers, cites, h
    degree = p3["degree_min"]["rows"]
    direction = p3["direction_min"]["rows"]
    talent = p3["talent_min"]["rows"]
    degree_dist = __import__("_reg5_common")._load("reg5_probe_20261021.json", {})["queries"]["degree_dist"]["rows"]

    dmap = defaultdict(list)
    for sid, d in degree:
        dmap[sid].append(d)
    dmatch = set(dmap)

    city_of, kind_ct = {}, Counter()
    matched_any = 0
    for sid, nm, org, pn, cn, h in scholars:
        c, k = match_org(org)
        if c:
            matched_any += 1
            kind_ct[k] += 1
        if c in CITY4:
            city_of[sid] = c

    city_scholars = Counter(city_of.values())
    city_degree = Counter()
    city_degree_rank = defaultdict(dict)
    for sid, c in city_of.items():
        ds = dmap.get(sid)
        if not ds:
            continue
        b = degree_bucket(ds)
        city_degree[(c, b)] += 1
        city_degree_rank[c][sid] = b

    city_impact = {}
    for c in CITY4:
        rows = [r for r in scholars if city_of.get(r[0]) == c]
        h = [int(r[5] or 0) for r in rows]
        city_impact[c] = {
            "scholars": len(rows),
            "papers_sum": sum(int(r[3] or 0) for r in rows),
            "citations_sum": sum(int(r[4] or 0) for r in rows),
            "h_median": round(sorted(h)[len(h) // 2], 2) if h else None,
            "h_ge_10": sum(1 for x in h if x >= 10),
            "h_ge_30": sum(1 for x in h if x >= 30),
            "with_degree": sum(1 for r in rows if r[0] in dmatch),
            "degree_share_pct": pct(sum(1 for r in rows if r[0] in dmatch), len(rows)),
            "degree_buckets": {b: city_degree[(c, b)] for b in ("博士", "硕士", "学士", "其他")},
        }

    # 学历表独立分布（按人取最高）
    best = {}
    for sid, d in degree:
        b = degree_bucket([d])
        if sid not in best or RANK[b] > RANK[best[sid]]:
            best[sid] = b
    deg_dist = Counter(best.values())
    deg_total = sum(deg_dist.values())

    names = {r[0] for r in scholars}
    dset = {r[0] for r in degree}
    dirset = {r[0] for r in direction}
    tset = {r[0] for r in talent}
    acad = [sid for sid, a in talent if int(a or 0) == 1]
    acad_in4 = [s for s in acad if s in city_of]

    # 研究方向 → 链（代理，仅量化可用性，不进主值）
    kw = {
        "INB1306": ["software", "information service"], "INB1309": ["artificial intelligence", "machine learning", "deep learning"],
        "INB1333": ["consumer electronic", "display"], "INB1502": ["digital media", "cultural", "animation"],
        "INB2505": ["synthetic biology", "biomanufacturing", "metabolic engineering"],
        "INB1204": ["robotic", "manipulator"], "INB1303": ["semiconductor", "integrated circuit", "wafer"],
        "INB1323": ["sensor", "sensing"], "INB1354": ["embodied", "humanoid"],
        "INB1209": ["autonomous vehicle", "connected vehicle", "lidar"], "INB1236": ["uav", "drone", "low-altitude"],
        "INB2503": ["biomedical", "cancer", "clinical", "pharmac", "genomic"],
    }
    dir_chain = {}
    for sid, f in direction:
        fl = (f or "").lower()
        hit = [ch for ch, ks in kw.items() if any(k in fl for k in ks)]
        if hit:
            dir_chain[sid] = hit
    dir_cells = Counter()
    deg_cells = Counter()
    for sid, chs in dir_chain.items():
        c = city_of.get(sid)
        if c:
            for ch in chs:
                dir_cells[(ch, c)] += 1
                if sid in dmatch:
                    deg_cells[(ch, c)] += 1

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for c in CITY4:
            row["cells"][c] = {
                "scholars_by_research_direction": dir_cells.get((ch, c), 0),
                "scholars_in_city": dir_cells.get((ch, c), 0),
                "degree_records_in_city": deg_cells.get((ch, c), 0),
            }
        matrix.append(row)

    payload = {
        "metric_id": MID,
        "metric_name": "人才结构（区域）",
        "date": "2026-10-22",
        "formula_owner": "徐滕强（CHAIN 域 calc-logic，仅给指标名）",
        "source": ("gkx.dwd_scholar(21,316) + dwd_scholar_education_background(43,766) + "
                   "dwd_scholar_research_direction(20,030) + dwd_scholar_talent_flag(20,030)"),
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "city_scholars": {c: city_scholars.get(c, 0) for c in CITY4},
        "city_impact": city_impact,
        "degree_distribution_standalone": {
            "scholars": deg_total,
            "buckets": dict(deg_dist),
            "shares_pct": {k: pct(v, deg_total) for k, v in deg_dist.items()},
            "note": "学历表无机构/城市字段，只能给全国分布，不能落 4 市。",
        },
        "matrix": matrix,
        "matrix_note": ("矩阵内 scholars_in_city 是**链归属后**的人数（研究方向英文词代理），"
                        "不是市域学者总量；市域总量见 city_scholars。链维度只有 14/48 单元非零，"
                        "degree_records_in_city 进一步按主表∩学历表收敛，多数单元为 0。"),
        "probes": {
            "scholars_total": len(scholars),
            "scholars_with_org": sum(1 for r in scholars if (r[2] or "").strip()),
            "scholars_org_matched": matched_any,
            "scholars_org_matched_pct": pct(matched_any, len(scholars)),
            "org_match_kind": dict(kind_ct),
            "scholars_in_city4": sum(city_scholars.values()),
            "scholars_in_city4_pct": pct(sum(city_scholars.values()), len(scholars)),
            "degree_rows": 43766,
            "degree_distinct_ids": len(dset),
            "scholar_degree_overlap": len(names & dset),
            "scholar_degree_overlap_pct": pct(len(names & dset), len(names)),
            "direction_distinct_ids": len(dirset),
            "scholar_direction_overlap": len(names & dirset),
            "scholar_direction_overlap_pct": pct(len(names & dirset), len(names)),
            "talent_distinct_ids": len(tset),
            "scholar_talent_overlap": len(names & tset),
            "scholar_talent_overlap_pct": pct(len(names & tset), len(names)),
            "academicians": len(acad),
            "academicians_in_city4": len(acad_in4),
            "city4_with_degree": sum(city_impact[c]["with_degree"] for c in CITY4),
            "city4_degree_share_pct": pct(sum(city_impact[c]["with_degree"] for c in CITY4),
                                          sum(city_scholars.values())),
            "direction_chain_cells_nonzero": sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)]),
            "degree_raw_dist_top": degree_dist[:12],
        },
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": (
                f"人才结构的核心是「链上人才按学历/职称分层」，但两跳都断：其一，学历表 15,851 个 scholar_id "
                f"与主表 21,316 个只有 {len(names & dset):,} 个（{pct(len(names & dset), len(names))}%）能对上，"
                f"研究方向与头衔同样只有 8.7%，四张附表实际是另一个学者宇宙；其二，能落 4 市的主表学者仅 "
                f"{sum(city_scholars.values()):,} 人（{pct(sum(city_scholars.values()), len(scholars))}%），"
                f"其中同时有学历记录的只有 {sum(city_impact[c]['with_degree'] for c in CITY4)} 人，"
                f"不足以支撑任何市域学历分布；其三，学者机构以高校为主，与产业链标签无挂接，链维只能靠研究方向英文词代理，"
                f"48 个单元里仅 {sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)])} 个非零。"
                f"结构与数据均不构成可算闭环，故维持完全不支持。"
            ),
            "criteria": {"scholars": len(scholars), "scholar_degree_overlap_pct": pct(len(names & dset), len(names)),
                         "scholar_direction_overlap_pct": pct(len(names & dirset), len(names)),
                         "city4_scholars": sum(city_scholars.values()),
                         "city4_with_degree": sum(city_impact[c]["with_degree"] for c in CITY4),
                         "chain_cells_nonzero": sum(1 for ch in CHAIN_AXIS for c in CITY4 if dir_cells[(ch, c)])},
        },
        "notes": [
            "四张学者附表（学历/研究方向/头衔/论文关系）与主表 scholar_id 交集 8.2%—9.2%，"
            "这是主键不统一，不是抽样；任何跨表人口统计都会把分母打掉九成。",
            "主表 `scholar_org_id` 21,316 行**全为空串**，机构归属只能用 `scholar_org_name_zh` 文本匹配，"
            "精确命中 16,120、前缀命中 2,192、城市词兜底 29，仍余 2,488 条匹配不上。",
            "学者总体以高校/中科院为主（机构 TOP：中国科学院 728、上海交通大学 703、北京大学 364），"
            "4 市只占 5.6%，这是全国学者库的结构，不是深圳都市圈的人才结构。",
            "研究方向字段是英文短语（如 Synthetic Biology;Enzyme Engineering），可做链领域代理，"
            "但一个学者可命中多条链，且只覆盖 8.7% 主表人口，**不进入任何正式值**。",
            "`dwd_scholar_work_experience` 57,117 行同样存在 ID 空间问题（20,028 个 ID），未计入本指标。",
            "替代路线见 §四：若甲方能把学者主键统一，或给学历表补机构/城市字段，本指标可立即升级为部分支持。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("scholars", len(scholars), "org matched", matched_any, "in4", sum(city_scholars.values()))
    print("degree overlap", len(names & dset), "city4 degree", sum(city_impact[c]["with_degree"] for c in CITY4))
    print("degree dist", dict(deg_dist), "academicians", len(acad), "in4", len(acad_in4))
    print("dir cells nonzero", payload["probes"]["direction_chain_cells_nonzero"])


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
    out_json = here / "M_CHAIN_REG_TALENT_STRUCTURE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_REG_TALENT_STRUCTURE.py 等价）
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
        "metric_id": "M_CHAIN_REG_TALENT_STRUCTURE",
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
