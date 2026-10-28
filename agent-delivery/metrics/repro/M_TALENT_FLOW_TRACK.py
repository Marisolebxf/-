#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 三系统兼容升级件·D2 拆分原 ID】本件继承算法库口径（原版不动）
# 【同名指标族·互见】M_TALENT_FLOW_TRACK_ZS（专题/展示侧拆分件）: ../第三方库指标计算过程/M_TALENT_FLOW_TRACK_ZS.md ｜ code/M_TALENT_FLOW_TRACK_ZS.py
# 【维护者】唐绍祖
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TALENT_FLOW_TRACK 人才流动追踪
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库（D2 拆分后本件归算法库；系统侧变体见 M_TALENT_FLOW_TRACK_ZT.py / M_TALENT_FLOW_TRACK_ZS.py）
# 【差异分级】D2 口径级分歧·不可兼容·方法型 → 拆分（判定见 ../过程文件/02_D2兼容判定与拆分_总结.md）
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TALENT_FLOW_TRACK —— 人才流动轨迹（SRS 78/79/80）。

口径：
  段 = `dwd_scholar_work_experience` 一行（机构 + 起年 + 止年，止年空按 2026）；
  一次「流动」= 同一 scholar_id 相邻两段，机构串不同，且后段起年 ≥ 前段止年
  （允许同年衔接）；同机构相邻段记「内部晋升/续聘」，不计流动。
  城际流动只统计两端都能定位且城市不同的记录；分母单列。
零 SQL；产物 code/M_TALENT_FLOW_TRACK_out.json。
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent10_common as C  # noqa: E402

METRIC = "M_TALENT_FLOW_TRACK"
NOW = 2026


def main() -> None:
    W = C.work()
    by = defaultdict(list)
    for w in W:
        o = (w["org"] or "").strip()
        y0 = w["y0"]
        if not o or not y0:
            continue
        by[w["sid"]].append((int(y0), int(w["y1"] or NOW), o, w["pos"] or "", bool(w["cur"])))

    multi = {s: v for s, v in by.items() if len(v) >= 2}
    trans = []      # (sid, y, org_from, org_to, city_from, city_to, dom)
    internal = 0
    dropped_overlap = 0
    p = C.panel()["scholars"]
    dom_of = {r["sid"]: (r["cl"][0] if r["cl"] else "未标注") for r in p}
    for sid, segs in multi.items():
        segs = sorted(segs)
        for a, b in zip(segs, segs[1:]):
            if b[0] < a[1]:
                dropped_overlap += 1
                continue
            if a[2] == b[2]:
                internal += 1
                continue
            ca = C.loc2(a[2])[1]
            cb = C.loc2(b[2])[1]
            trans.append((sid, b[0], a[2], b[2], ca, cb, dom_of.get(sid, "未标注")))

    n_from = len({t[0] for t in trans})
    both_located = [t for t in trans if "未" not in t[4] and "未" not in t[5]]
    unassigned_org = Counter(o for t in trans for o in (t[2], t[3]) if "未" in C.loc2(o)[1])
    city_tr = [t for t in trans if t[4] not in ("未归属", "未填")
               and t[5] not in ("未归属", "未填") and t[4] != t[5]]
    year = Counter(t[1] for t in trans if 1990 <= t[1] <= NOW)
    city_edges = Counter((t[4], t[5]) for t in city_tr)
    org_edges = Counter((t[2], t[3]) for t in trans)
    dom_edges = defaultdict(lambda: [0, 0])
    for t in trans:
        dom_edges[t[6]][1 if t[5] == "深圳市" else 0] += 1

    sz_in = [t for t in trans if t[5] == "深圳市" and t[4] != "深圳市"]
    sz_out = [t for t in trans if t[4] == "深圳市" and t[5] != "深圳市"]
    sz_in_by_city = Counter(t[4] for t in sz_in)
    sz_out_by_city = Counter(t[5] for t in sz_out)  # 目的地城市
    sz_dom = Counter(t[6] for t in sz_in)

    def pairs(cnt, k=15):
        return [{"from": a, "to": b, "n": n} for (a, b), n in cnt.most_common(k)]

    top_orgs = [o for o, _ in Counter(t[2] for t in trans).most_common(12)]
    org_matrix = []
    for a in top_orgs:
        for b in top_orgs:
            if a != b and org_edges.get((a, b)):
                org_matrix.append({"from": a, "to": b, "n": org_edges[(a, b)]})

    payload = {
        "support_judgment": "部分支持",
        "base_years_used": [1990, 2026],
        "base_years_missing": [2021, 2022, 2023],
        "base_years_note": "履历起止年覆盖 1950s—2026，但招聘/流动的宏观基期（2021—2023 三年"
                           "对比）没有同期快照；本件只做「全历史轨迹」一张截面，不做逐年净流入率。"
                           "「止年空」一律按 2026（当前）处理，会低估 2026 年之后的流出",
        "scope": {"universe": "dwd_scholar_work_experience 57,117 行",
                  "unit": "一次机构变更（相邻两段）",
                  "denominator_movers": n_from,
                  "denominator_transitions": len(trans),
                  "denominator_city": len(city_tr)},
        "coverage": {"work_rows": len(C.work()), "scholars_with_work": len(by),
                     "scholars_multi_segment": len(multi),
                     "movers": n_from, "transitions": len(trans),
                     "internal_moves": internal, "overlap_dropped": dropped_overlap,
                     "city_transitions": len(city_tr),
                     "city_share": C.share(len(city_tr), len(trans)),
                     "year_min": min(year) if year else None,
                     "year_max": max(year) if year else None,
                     "org_filled_pct": round(100.0 * sum(1 for w in W if (w["org"] or "").strip()) / len(W), 2),
                     "start_filled_pct": round(100.0 * sum(1 for w in W if w["y0"]) / len(W), 2),
                     "end_filled_pct": round(100.0 * sum(1 for w in W if w["y1"]) / len(W), 2),
                     "position_filled_pct": round(100.0 * sum(1 for w in W if (w["pos"] or "").strip()) / len(W), 2),
                     "seg_city_unassigned": len(trans) - len(both_located),
                     "trans_both_located": len(both_located)},
        "year_series": [{"year": y, "n": n} for y, n in sorted(year.items())],
        "org_edges": pairs(org_edges, 25),
        "org_matrix_top12": org_matrix,
        "city_edges": pairs(city_edges, 25),
        "unassigned_org_top": [{"org": o, "n": n} for o, n in unassigned_org.most_common(10)],
        "shenzhen": {"inflow": len(sz_in), "outflow": len(sz_out),
                     "net": len(sz_in) - len(sz_out),
                     "in_by_city": [{"city": k, "n": v} for k, v in sz_in_by_city.most_common(12)],
                     "out_by_city": [{"city": k, "n": v} for k, v in sz_out_by_city.most_common(12)],
                     "in_by_domain": [{"domain": k, "n": v} for k, v in sz_dom.most_common()],
                     "note": "深圳口径 = loc2 判定的深圳市机构；分支校区已修正"},
        "domain_flows": [{"domain": d, "n": sum(v), "to_sz": v[1]}
                         for d, v in sorted(dom_edges.items(), key=lambda x: -sum(x[1]))],
        "data_quality": {
            "overlap": f"{dropped_overlap} 对相邻段时间重叠（后段起年早于前段止年），已丢弃，"
                       "多数是同一单位多岗位/兼职并行",
            "same_org": f"{internal} 对同机构相邻段计入内部晋升，不计流动",
            "no_reason": "库内无离职原因/去向类型字段，流动只有「机构→机构」，无法区分主动跳槽与调动",
            "no_salary": "无薪酬字段，流动的「拉力」不可量化",
            "right_censor": "在职（cur=1）者止年按 2026 计，未来流出未知",
        },
        "diff_vs_old_draft": {
            "old": "旧稿 9,281 人可追踪、18,713 次机构变更、1,149 次城际迁移、深圳净流入 +19",
            "now": f"{len(multi):,} 人有 ≥2 段、{len(trans):,} 次机构变更、"
                   f"{len(city_tr):,} 次城际迁移、深圳净流入 {len(sz_in)-len(sz_out):+d}",
            "why": "同一份履历快照，差异来自两处：①本件要求「后段起年 ≥ 前段止年」，丢弃重叠段；"
                   "②城际只算两端均可定位者。旧稿把未归属当同城处理，因此城际次数偏高",
        },
        "findings": [
            f"{len(multi):,} 人有 2 段及以上履历，其中 {n_from:,} 人至少换过一次机构，"
            f"共 {len(trans):,} 次变更（人均 {round(len(trans)/n_from, 2)} 次）",
            f"城际迁移 {len(city_tr):,} 次（占全部变更 {C.share(len(city_tr), len(trans))}%），"
            f"深圳流入 {len(sz_in)} / 流出 {len(sz_out)} / 净 {len(sz_in)-len(sz_out):+d}",
            f"最大流向：{city_edges.most_common(1)[0][0][0]} → {city_edges.most_common(1)[0][0][1]}"
            f"（{city_edges.most_common(1)[0][1]} 次）",
        ],
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("sz", payload["shenzhen"]["inflow"], payload["shenzhen"]["outflow"])
    print("city top", payload["city_edges"][:5])
    print("org top", payload["org_edges"][:5])
    print("years", payload["year_series"][-6:])


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
    out_json = here / "M_TALENT_FLOW_TRACK_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TALENT_FLOW_TRACK.py 等价）
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
        "metric_id": "M_TALENT_FLOW_TRACK",
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
