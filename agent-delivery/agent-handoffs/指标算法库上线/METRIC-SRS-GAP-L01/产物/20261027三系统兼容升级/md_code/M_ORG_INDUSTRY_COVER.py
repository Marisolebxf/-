#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_INDUSTRY_COVER 科研机构产业领域覆盖
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_INDUSTRY_COVER.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_INDUSTRY_COVER · 科研机构产业领域覆盖（ORG 域）

需求锚点：展示系统 §1.1.1.2.4.2.4.1.2 ——「系统自动识别并展示所选科研机构参与的产业领域，
以图表形式呈现各领域的覆盖分析」；算法库序号 99「科研机构涉及产业领域」。

本件只回答「覆盖有多广」，不回答「结构长什么样」——后者是 M_ORG_TECH_LAYOUT 的职责，
两件共用同一份 IPC 映射，但输出不同（本件：广度/熵/覆盖机构数；布局件：份额/HHI/补强清单）。

口径（零 SQL）：
  技术部类 = IPC 首字母 A—H（WIPO 官方八部）。这是**技术分类**，不是产业分类。
  覆盖广度 = 该机构专利命中的部类个数（1—8）。
  覆盖熵   = 香农熵 / ln(8)，0=单一部类，1=八部类均分。
  覆盖率   = 有 IPC4 证据的机构数 / 底册机构数（按城市分别算）。
  专利/机构 = 入图专利件数 / 有 IPC 的机构数（避免用底册总数稀释）。

硬边界（正文必须写）：
  - 库内**没有** IPC→国民经济行业 / 深圳「20+8」产业链的映射字典，所以「产业领域」四个字
    在本件只能落到「技术部类」这一层，不能宣称已识别产业。凡出现「产业」字样，
    必须同时写「部类代理」。
  - 专利只覆盖 194/2,074 家（9.35%）；其余 1,880 家不是「零覆盖」，是「无证据」。
  - `dwd_org_industry_tags` 的 credit_code 与机构底册只有 3.5% 命中（DATA_FACTS §3.1），
    不能拿它当产业标签来源。
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402

MID = "M_ORG_INDUSTRY_COVER"


def main() -> None:
    panel = M.load_panel()
    inst = panel["institutions"]
    ipc = M.load_ipc()

    rows = []
    sec_org = Counter()          # 部类 → 有该部类证据的机构数
    sec_pat = Counter()          # 部类 → 专利件数
    combos = Counter()           # 部类组合（如 A+C+G）
    for x in inst:
        vec = ipc.get(x["name"])
        if not vec:
            continue
        sc = M.section_counter(vec)
        tot = sum(sc.values())
        if not tot:
            continue
        rows.append({
            "name": x["name"], "city": x["city"], "org_type": x["org_type"],
            "patents": tot, "ipc4_n": len(vec),
            "breadth": len(sc),
            "entropy": M.entropy_norm(sc, 8),
            "hhi": M.hhi(sc),
            "top_section": sc.most_common(1)[0][0],
            "top_share": round(sc.most_common(1)[0][1] / tot, 4),
            "vec": {s: sc[s] for s in M.SECTIONS if sc.get(s)},
            "combo": "+".join(s for s in M.SECTIONS if sc.get(s)),
        })
        for s, c in sc.items():
            sec_org[s] += 1
            sec_pat[s] += c
        combos["+".join(s for s in M.SECTIONS if sc.get(s))] += 1

    orgs_ipc = len(rows)
    pat_mapped = sum(r["patents"] for r in rows)
    ipc4_used = len({k for v in ipc.values() for k in v})

    breadth_dist = Counter(r["breadth"] for r in rows)

    city_stat = {}
    for city in ["深圳市", "广州市", "东莞市", "惠州市"]:
        roster = [x for x in inst if x["city"] == city]
        sub = [r for r in rows if r["city"] == city]
        pats = sum(r["patents"] for r in sub)
        sec = Counter()
        for r in sub:
            for s, c in r["vec"].items():
                sec[s] += c
        city_stat[city] = {
            "roster": len(roster),
            "orgs_with_ipc": len(sub),
            "coverage_rate": round(len(sub) / len(roster), 4) if roster else 0,
            "patents_mapped": pats,
            "section_share": {s: round(c / pats, 4) for s, c in sec.most_common()} if pats else {},
            "section_coverage_n": {s: sum(1 for r in sub if r["vec"].get(s)) for s in M.SECTIONS},
            "breadth_mean": round(sum(r["breadth"] for r in sub) / len(sub), 2) if sub else None,
            "entropy_mean": round(sum(r["entropy"] for r in sub) / len(sub), 4) if sub else None,
            "hhi_mean": round(sum(r["hhi"] for r in sub) / len(sub), 4) if sub else None,
            "patents_per_org": round(pats / len(sub), 2) if sub else None,
        }

    org_type_stat = {}
    for t in sorted({r["org_type"] for r in rows}):
        sub = [r for r in rows if r["org_type"] == t]
        org_type_stat[t] = {
            "orgs_with_ipc": len(sub),
            "breadth_mean": round(sum(r["breadth"] for r in sub) / len(sub), 2),
            "entropy_mean": round(sum(r["entropy"] for r in sub) / len(sub), 4),
            "patents": sum(r["patents"] for r in sub),
        }

    # 覆盖广度榜：先广度，再专利量（避免 1 件专利恰好跨 3 部类的小机构排在前面）
    top = sorted(rows, key=lambda r: (-r["breadth"], -r["patents"]))
    single = [r for r in rows if r["breadth"] == 1]

    out = {
        "metric_id": MID,
        "metric_name": "科研机构产业领域覆盖",
        "domain": "ORG / 科研机构涉及产业分析（展示系统 §1.1.1.2.4.2.4.1.2 / 算法库 99）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "专利为 2021—2026 存量口径（库内 apdt_year 仅此六年，2017—2020 零行，不按 0 摊入；"
            "2026 为残年）。本件不跨年比较，不做趋势。"),
        "inputs": {
            "ipc4": "_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行，按申请人名精确匹配底册）",
            "roster": "gkx.dwd_research_institute_base_info 2,074 家",
            "section_rule": "IPC 首字母 A—H；小类 = main_classification_ipcr 前 4 位",
        },
        "definition_note": (
            "需求要的是「产业领域」，库内没有 IPC→国民经济行业/20+8 链字典，本件只能给到 "
            "「技术部类（IPC section）」这一层，属于**部类代理**。覆盖率、广度、熵三项可算；"
            "「某机构属于生物医药产业」这类判断不可算，正文不得出现。"),
        "coverage": {
            "institutes": len(inst),
            "orgs_with_ipc": orgs_ipc,
            "orgs_with_ipc_pct": round(orgs_ipc / len(inst), 4),
            "patents_mapped": pat_mapped,
            "ipc4_classes_used": ipc4_used,
            "ipc4_universe": 634,
            "section_universe": 8,
            "sections_observed": len([s for s in M.SECTIONS if sec_org.get(s)]),
        },
        "breadth_dist": {str(k): v for k, v in sorted(breadth_dist.items())},
        "breadth_dist_note": "广度=命中部类数；8 部类全覆盖的机构 0 家，最高 7 部类 4 家。",
        "entropy_dist": M.dist([r["entropy"] for r in rows]),
        "hhi_dist": M.dist([r["hhi"] for r in rows]),
        "section_stat": {
            s: {"name": M.SECTION_NAMES[s], "orgs": sec_org.get(s, 0),
                "patents": sec_pat.get(s, 0),
                "share": round(sec_pat.get(s, 0) / pat_mapped, 4) if pat_mapped else 0}
            for s in M.SECTIONS
        },
        "combo_top": [{"combo": k, "orgs": v} for k, v in combos.most_common(12)],
        "city_stat": city_stat,
        "org_type_stat": org_type_stat,
        "profiles": [{"name": r["name"], "city": r["city"], "org_type": r["org_type"],
                      "patents": r["patents"], "ipc4_n": r["ipc4_n"],
                      "breadth": r["breadth"], "entropy": r["entropy"], "hhi": r["hhi"],
                      "vec": r["vec"],
                      "share": {k: round(v / r["patents"], 4) for k, v in r["vec"].items()}}
                     for r in sorted(rows, key=lambda r: (-r["patents"]))],
        "top_breadth": [
            {"name": r["name"], "city": r["city"], "org_type": r["org_type"],
             "breadth": r["breadth"], "entropy": r["entropy"], "hhi": r["hhi"],
             "patents": r["patents"], "ipc4_n": r["ipc4_n"], "vec": r["vec"]}
            for r in top[:30]
        ],
        "single_section": {
            "n": len(single),
            "pct": round(len(single) / orgs_ipc, 4) if orgs_ipc else 0,
            "examples": [{"name": r["name"], "city": r["city"], "section": r["top_section"],
                          "patents": r["patents"]}
                         for r in sorted(single, key=lambda r: -r["patents"])[:10]],
            "note": "只落在一个部类，不等于只做一个产业；IPC 部类粒度极粗（G 同时含物理与计算）。",
        },
        "limits": [
            "「产业领域」口径缺失：库内无 IPC→国民经济行业 / 深圳 20+8 链字典，"
            "本件只交付技术部类覆盖，不能宣称已识别产业。",
            "专利只覆盖 194/2,074 家（9.35%）；1,880 家无 IPC 证据，不能读成「零覆盖」。",
            "IPC 部类粒度粗：G 含物理+计算，C 含化学+材料+生物化学，部类份额不能直接当产业结构。",
            "只用主分类（main_classification_ipcr）第一段，副分类未计，广度略低估。",
            "机构名精确匹配，未做别名合并：同一机构的不同写法会分成两条记录。",
            "`dwd_org_industry_tags` 的 credit_code 与底册只有 3.5% 命中（DATA_FACTS §3.1），"
            "不能作为产业标签来源。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path)
    print("coverage", out["coverage"])
    print("breadth", out["breadth_dist"])
    print("sections", {s: v["orgs"] for s, v in out["section_stat"].items()})
    print("top", [(r["name"], r["breadth"], r["patents"]) for r in out["top_breadth"][:6]])


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
    out_json = here / "M_ORG_INDUSTRY_COVER_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_INDUSTRY_COVER.py 等价）
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
        "metric_id": "M_ORG_INDUSTRY_COVER",
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
