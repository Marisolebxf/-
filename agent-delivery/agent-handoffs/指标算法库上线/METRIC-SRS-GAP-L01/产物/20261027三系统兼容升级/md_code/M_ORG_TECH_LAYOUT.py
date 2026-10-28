#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_TECH_LAYOUT 科研机构技术领域布局
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_TECH_LAYOUT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_TECH_LAYOUT · 科研机构布局技术领域分析（ORG 域）

需求锚点：展示系统 §1.1.1.2.4.2.4.2 ——「分析所选科研机构在细分技术领域的布局广度与深度，
通过专利、论文等数据映射技术标签。用户可识别机构核心技术优势与研究聚焦点」。

与 M_ORG_DEEP_149_1 的分工（同一份 IPC 映射，两套输出，不许互相替代）：
  149：机构×领域 的**强度分**（份额³ × 规模折算）+ 城市前 5 领域的补强清单 → 回答「该往哪补」
  本件：机构×领域 的**广度与深度画像** + IPC4 细分下钻 + 论文/项目侧潜在布局 → 回答「它在做什么」
  本件不打分、不加权、不做补强判定；页面是「选中机构 → 画像卡 / 多机构对比」交互形态。

口径：
  广度 breadth = 份额 ≥1% 的领域个数（0—7）。
  深度 depth    = 领域内份额 × log(1+该领域专利件数的领域内分位) 不合用；本件只用三列原值：
                  share（领域内份额）、patents（件数）、ipc4_n（该领域用到的小类数），
                  再按份额分四档：核心 ≥30% / 重点 10—30% / 一般 1—10% / 无证据 <1%。
  聚焦度 hhi    = Σ share²（7 领域口径，1/7≈0.143 为最分散）。
  潜在布局      = 论文关键词或项目学科指向某领域、但该领域无 IPC 证据 → 记 `potential`，不出分。

硬边界：
  - 只有主分类 IPC4（`main_classification_ipcr` 前 4 位），副分类未计 → 广度和深度都略低估。
  - 专利只覆盖 194/2,074 家（9.35%）；其余 1,880 家是「无证据」，不是「零布局」。
  - 论文关键词仅 9 家、项目学科 53 家；「潜在布局」只对这 62 家可能成立。
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_TECH_LAYOUT"
TIERS = [("核心", 0.30, 1.01), ("重点", 0.10, 0.30), ("一般", 0.01, 0.10)]


def tier_of(share: float) -> str:
    for name, lo, hi in TIERS:
        if lo <= share < hi:
            return name
    return "无证据"


def profile(name: str, vec: dict, inst_row: dict) -> dict:
    dom = Counter()
    dom_ipc = defaultdict(Counter)
    for k, c in vec.items():
        d = OC.ipc_domain(k)
        dom[d] += c
        dom_ipc[d][k] += c
    tot = sum(dom.values())
    share = {d: dom.get(d, 0) / tot for d in M.DOMAINS}
    breadth = sum(1 for d in M.DOMAINS if share[d] >= 0.01)
    domains = {}
    for d in M.DOMAINS:
        s = share[d]
        top = dom_ipc[d].most_common(5)
        domains[d] = {
            "patents": dom.get(d, 0),
            "share": round(s, 4),
            "ipc4_n": len(dom_ipc[d]),
            "tier": tier_of(s),
            "top_ipc4": [{"code": k, "n": c} for k, c in top],
        }
    # 论文/项目侧的潜在布局：文本证据指向某领域，但该领域 IPC 份额 <1%
    potential = []
    src = []
    if inst_row.get("discipline_top"):
        td = OC.text_domain(inst_row["discipline_top"])
        if td:
            src.append("discipline")
            if share.get(td, 0) < 0.01:
                potential.append({"domain": td, "evidence": f"项目学科={inst_row['discipline_top']}"})
    for kw in (inst_row.get("kw_top") or [])[:5]:
        td = OC.text_domain(kw)
        if td:
            if "kw" not in src:
                src.append("kw")
            if share.get(td, 0) < 0.01 and not any(p["domain"] == td for p in potential):
                potential.append({"domain": td, "evidence": f"论文关键词={kw}"})
    return {
        "name": name, "city": inst_row["city"], "org_type": inst_row["org_type"],
        "patents": tot, "ipc4_n": len(vec), "breadth": breadth,
        "hhi": round(sum(s * s for s in share.values()), 4),
        "domains": domains,
        "core": [d for d in M.DOMAINS if domains[d]["tier"] == "核心"],
        "focus": [d for d in M.DOMAINS if domains[d]["tier"] in ("核心", "重点")],
        "potential": potential,
        "evidence_src": src,
        "top_ipc4": [{"code": k, "n": c} for k, c in Counter(vec).most_common(8)],
    }


def main() -> None:
    panel = M.load_panel()
    inst = panel["institutions"]
    by_name = {x["name"]: x for x in inst}
    ipc = M.load_ipc()

    profs = []
    for nm, vec in ipc.items():
        if nm not in by_name or not vec:
            continue
        profs.append(profile(nm, vec, by_name[nm]))
    profs.sort(key=lambda p: (-p["breadth"], -p["patents"]))

    breadth_dist = Counter(p["breadth"] for p in profs)
    tier_stat = Counter()
    for p in profs:
        for d in M.DOMAINS:
            tier_stat[(d, p["domains"][d]["tier"])] += 1

    # 领域 × 档位矩阵（行=领域，列=档位）
    matrix = {d: {t: tier_stat.get((d, t), 0) for t in ("核心", "重点", "一般", "无证据")}
              for d in M.DOMAINS}

    # 只看「核心」领域：哪家机构在几个领域是核心
    core_dist = Counter(len(p["core"]) for p in profs)

    # 城市与类型
    city_stat = {}
    for c in ["深圳市", "广州市", "东莞市", "惠州市"]:
        sub = [p for p in profs if p["city"] == c]
        dom = Counter()
        for p in sub:
            for d in M.DOMAINS:
                dom[d] += p["domains"][d]["patents"]
        tot = sum(dom.values())
        city_stat[c] = {
            "orgs": len(sub),
            "patents": tot,
            "breadth_mean": round(sum(p["breadth"] for p in sub) / len(sub), 2) if sub else None,
            "hhi_mean": round(sum(p["hhi"] for p in sub) / len(sub), 4) if sub else None,
            "core_org_n": {d: sum(1 for p in sub if p["domains"][d]["tier"] == "核心")
                           for d in M.DOMAINS},
            "share": {d: round(dom[d] / tot, 4) for d in M.DOMAINS} if tot else {},
        }
    type_stat = {}
    for t in sorted({p["org_type"] for p in profs}):
        sub = [p for p in profs if p["org_type"] == t]
        type_stat[t] = {
            "orgs": len(sub),
            "breadth_mean": round(sum(p["breadth"] for p in sub) / len(sub), 2),
            "hhi_mean": round(sum(p["hhi"] for p in sub) / len(sub), 4),
            "patents": sum(p["patents"] for p in sub),
        }

    # 多机构对比：选三家不同形态的机构，输出交集/并集领域
    pick = ["中国科学院深圳先进技术研究院", "鹏城实验室", "广东省科学院新材料研究所"]
    sel = [next((p for p in profs if p["name"] == n), None) for n in pick]
    sel = [p for p in sel if p]
    common = set(sel[0]["core"]) if sel else set()
    for p in sel[1:]:
        common &= set(p["core"])
    union = set()
    for p in sel:
        union |= set(p["focus"])
    compare = {
        "orgs": [{"name": p["name"], "breadth": p["breadth"], "hhi": p["hhi"],
                  "core": p["core"], "focus": p["focus"]} for p in sel],
        "common_core": sorted(common),
        "union_focus": sorted(union),
        "note": ("交集按「核心」档（份额 ≥30%）求、并集按「重点及以上」求。交集为空说明三家"
                 "没有共同主领域；这不代表不能合作，只说明技术语言不重叠。"),
    }

    # 潜在布局：有文本证据但无 IPC 证据的机构
    pot = [p for p in profs if p["potential"]]
    pot_orgs = len({p["name"] for p in profs if p["evidence_src"]})

    out = {
        "metric_id": MID,
        "metric_name": "科研机构布局技术领域分析",
        "domain": "ORG / 科研机构布局技术领域分析（展示系统 §1.1.1.2.4.2.4.2）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "专利为 2021—2026 存量（库内 apdt_year 仅此六年，2017—2020 零行，不按 0 摊入；"
            "2026 为残年）。本件是横截面画像，不做年度趋势，故不使用同比基期。"),
        "inputs": {
            "ipc4": "_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
            "panel": "_snapshots21/org_family_panel_20261021.json（论文/项目/学者/学科/关键词）",
            "rules": "_org_deep21_common.IPC_RULES（245 条前缀规则 + 14 部级兜底）",
        },
        "definition_note": (
            "「广度」= 份额 ≥1% 的领域数；「深度」用 share / patents / ipc4_n 三列原值，"
            "再按份额分核心（≥30%）/ 重点（10—30%）/ 一般（1—10%）/ 无证据（<1%）四档。"
            "档位阈值是规则值，没有外部标定；换阈值会改变「核心领域」的名单，"
            "但不会改变 share 的排序。"),
        "coverage": {
            "institutes": len(inst),
            "orgs_with_ipc": len(profs),
            "orgs_with_ipc_pct": round(len(profs) / len(inst), 4),
            "patents_mapped": sum(p["patents"] for p in profs),
            "ipc4_used": len({k for v in ipc.values() for k in v}),
            "with_text_evidence": pot_orgs,
            "with_potential_only": len(pot),
        },
        "breadth_dist": {str(k): v for k, v in sorted(breadth_dist.items())},
        "core_domain_dist": {str(k): v for k, v in sorted(core_dist.items())},
        "tier_matrix": matrix,
        "city_stat": city_stat,
        "org_type_stat": type_stat,
        "compare_demo": compare,
        "potential_layout": {
            "n": len(pot),
            "examples": [{"name": p["name"], "city": p["city"],
                          "potential": p["potential"],
                          "ipc_patents": p["patents"]} for p in
                         sorted(pot, key=lambda p: -p["patents"])[:12]],
            "note": ("「潜在」= 文本证据指向该领域，但该领域 IPC 份额 <1%。"
                     "它只能说明「该机构在这条线上有非专利产出」，不能说「正在布局」。"),
        },
        "profiles": profs,
        "top_breadth": profs[:20],
        "focus_top": sorted(profs, key=lambda p: -p["hhi"])[:15],
        "limits": [
            "专利只覆盖 194/2,074 家（9.35%）；1,880 家无画像，不能读成「无技术布局」。",
            "只用主分类 IPC4 第一段，副分类未计；跨领域专利只归一个领域，广度略低估。",
            "「核心/重点/一般」阈值是规则值（30%/10%/1%），未经业务标定。",
            "论文关键词只 9 家、项目学科只 53 家，「潜在布局」覆盖极窄。",
            "IPC 规则把 `G` 部大量归入基础科学（测量/光学/控制），会把仪器类机构画成基础科学型。",
            "机构名精确匹配，未做别名合并；同一机构不同写法会分成两张画像。",
            "本件不打分。任何「技术力排名」必须走 M_ORG_TECH_SCORE，不能拿 breadth/hhi 代替。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path)
    print("coverage", out["coverage"])
    print("breadth", out["breadth_dist"])
    print("core_dist", out["core_domain_dist"])
    print("tier", {d: out["tier_matrix"][d] for d in M.DOMAINS})
    print("compare", compare["common_core"], len(compare["union_focus"]))


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
    out_json = here / "M_ORG_TECH_LAYOUT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_TECH_LAYOUT.py 等价）
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
        "metric_id": "M_ORG_TECH_LAYOUT",
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
