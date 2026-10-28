#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_DEEP_154_1 科研机构引入推荐模型
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_DEEP_154_1.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_DEEP_154_1 · 科研机构引入推荐模型（ORG 域，重建件）

需求锚点：算法库序号 154 ——「为深圳引进外部科研机构提供候选清单与优先级依据。
结合机构科研能力、与本地产业需求的契合度、合作基础与落地可行性，形成可解释的推荐结果。」

重建说明（为什么不能沿用旧稿）：
  旧版 `_quarantine/20261022_demo_helper/M_ORG_DEEP_154_1.py` 依赖 `_org_graph_common`，
  后者第 32 行在模块级导入演示库连接器，`D.ODS` 即演示库，全文 13 处演示表名
  （DATA_FACTS §3.21 第 3 类）。本件从 `gkx` 时代的落盘快照重取，**不 import 任何被隔离的 helper**。

本件口径（零 SQL，只读快照）：
  候选池 = 底册 2,074 家中 `city != 深圳市` 的 1,060 家（底册 100% 广东省，无省外机构）。
  A 能级   = pct_rank(log1p(专利存量 + 2×论文 + 项目数))，覆盖 205 家有信号的候选。
  Q 需求契合 = **未计算**。旧稿称取自 `M_TALENT_SZ_SUPPLY_DEMAND` 的 `by_domain_share`，
             而该产物不在本目录 `code/` 下，且其 `if os.path.exists()` 守卫会把缺失静默跳过。
             本件把它显式写成「Q 维缺需求数据、未计算」，不以任何代理值顶替。
  C 协同   = minmax_log(3×与深机构合著篇次 + 2×与深企业合著篇次)，仅对「有论文记录」的候选可算。
  S 稀缺   = Σ_d v_{i,d}(1 − s^SZ_d)，v 为候选技术领域结构（IPC4 优先，其次项目学科/论文关键词），
             s^SZ 为深圳 74 家有 IPC 机构的技术领域份额。
  F 可行   = 机构类型(40/25/10) + 登记年限(30/20/10) + 开办资金(30/20/10)，注册资金单位按万元（见 limits）。
  Score    = Σ w_k v_k / Σ w_k，w = (A .30, C .20, S .15, F .10)，Q 的 .25 槽位空置后重归一。

硬边界（正文必须逐条披露）：
  - 候选池只有省内，**不能**称「全国/全球引入清单」；
  - 没有历史引入标签（引进名单、引进后产出），**不是**训练出来的模型；
  - Q 维缺数据，**不能**称「与深圳产业需求契合度高/低」；
  - C 维只覆盖 23 家候选，S 维只覆盖 129 家，缺维在剩余维重归一。
"""
from __future__ import annotations

import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402
import _org_deep21_common as OC  # noqa: E402

MID = "M_ORG_DEEP_154_1"
NOW_YEAR = 2026


def dom_vectors(panel, ipc):
    """候选技术领域结构：IPC4 优先；无专利者退回「项目学科 + 论文关键词」。"""
    dom = defaultdict(Counter)
    src = {}
    for nm, vec in ipc.items():
        for k, c in vec.items():
            dom[nm][OC.ipc_domain(k)] += int(c)
        src[nm] = "ipc4"
    for x in panel["institutions"]:
        nm = x["name"]
        if dom.get(nm):
            continue
        d = OC.text_domain(x.get("discipline_top") or "")
        if d:
            dom[nm][d] += 1
            src[nm] = "discipline"
        for kw in (x.get("kw_top") or []):
            dd = OC.text_domain(kw)
            if dd:
                dom[nm][dd] += 1
                src.setdefault(nm, "keyword")
    return dom, src


def feasible(r, reg):
    """F 维 0—100：类型 40 / 年限 30 / 资金 30。省内已由候选池保证，不作为加分项。"""
    ty = reg.get("org_type") or r["org_type"]
    f_type = 40 if ty == "事业单位" else (25 if ty == "民办非企业单位" else 10)
    iy = reg.get("inc_year")
    age = (NOW_YEAR - iy) if iy else None
    if age is None:
        f_age = 0
    elif age >= 10:
        f_age = 30
    elif age >= 3:
        f_age = 20
    else:
        f_age = 10
    cap = reg.get("capital_wan")
    if cap is None:
        f_cap = 0
    elif cap >= 1000:
        f_cap = 30
    elif cap >= 100:
        f_cap = 20
    else:
        f_cap = 10
    return f_type + f_age + f_cap, {"type": f_type, "age": f_age, "capital": f_cap,
                                    "age_years": age, "capital_wan": cap}


def branch_hint(name, sz_names):
    """按名称前 6 字匹配深圳已有机构，提示「可能已在深设分支」（只作尽调线索）。"""
    if len(name) < 6:
        return []
    head = name[:6]
    return sorted(n for n in sz_names if n.startswith(head) and n != name)[:4]


def main() -> None:
    panel = M.load_panel()
    inst = panel["institutions"]
    ipc = M.load_ipc()
    reg_doc, reg = M.load_reg()
    base_city, base_dup = M.load_base_city()
    city_by_name = {x["name"]: x["city"] for x in inst}

    sz, cand = M.sz_and_candidates(inst)
    sz_names = {x["name"] for x in sz}

    inst_hits, comp_hits, co_detail = M.coauthor_sz(panel, city_by_name, base_city)
    dom, dom_src = dom_vectors(panel, ipc)

    # 深圳技术领域份额（S 维分母）——只用深圳有 IPC 的 74 家
    sz_dom = Counter()
    for x in sz:
        for d, c in dom.get(x["name"], {}).items():
            if dom_src.get(x["name"]) == "ipc4":
                sz_dom[d] += c
    sz_tot = sum(sz_dom.values())
    sz_share = {d: c / sz_tot for d, c in sz_dom.items()} if sz_tot else {}

    rows = []
    for x in cand:
        nm = x["name"]
        sig = sum(1 for k in ("patents", "papers", "projects", "scholars") if x[k])
        if not sig:
            continue
        dv = dom.get(nm) or {}
        s_raw = None
        if dv:
            t = sum(dv.values())
            s_raw = sum(c / t * (1 - sz_share.get(d, 0.0)) for d, c in dv.items())
        c_raw = 3 * inst_hits.get(nm, 0) + 2 * comp_hits.get(nm, 0)
        f_val, f_parts = feasible(x, reg.get(nm, {}))
        rows.append({
            "name": nm, "city": x["city"], "org_type": x["org_type"],
            "patents": x["patents"], "patent_grant": x["patent_grant"],
            "papers": x["papers"], "projects": x["projects"], "scholars": x["scholars"],
            "fund_wan": round(float(x.get("project_fund") or 0), 1),
            "transfer_in": x["transfer_in"], "policy_mentions": x["policy_mentions"],
            "signals": sig,
            "A_raw": round(math.log1p(x["patents"] + 2 * x["papers"] + x["projects"]), 4),
            "C_raw": c_raw,
            "S_raw": round(s_raw, 4) if s_raw is not None else None,
            "F": f_val, "F_parts": f_parts,
            "co_sz_inst": inst_hits.get(nm, 0), "co_sz_company": comp_hits.get(nm, 0),
            "dom_src": dom_src.get(nm), "dom_vec": {d: c for d, c in dv.items()},
            "inc_year": f_parts["age_years"] and reg.get(nm, {}).get("inc_year"),
            "capital_wan": f_parts["capital_wan"],
        })

    # ---- 归一：A/S 用分位（长尾稳健），C 用 log1p min-max（89% 为 0，分位会把「有 1 篇」顶到 98）----
    prA = M.pct_rank([r["A_raw"] for r in rows])
    for r, v in zip(rows, prA):
        r["A"] = round(v, 1)
    sub_s = [r for r in rows if r["S_raw"] is not None]
    prS = M.pct_rank([r["S_raw"] for r in sub_s])
    for r, v in zip(sub_s, prS):
        r["S"] = round(v, 1)
    for r in rows:
        r.setdefault("S", None)
    sub_c = [r for r in rows if r["papers"] > 0]
    mmC = M.minmax_log([r["C_raw"] for r in sub_c])
    for r, v in zip(sub_c, mmC):
        r["C"] = v
    for r in rows:
        r.setdefault("C", None)          # 无论文记录 ⇒ C 不可算（缺失，不是 0）

    W = {"A": .30, "Q": .25, "C": .20, "S": .15, "F": .10}
    for r in rows:
        parts = [("A", r["A"])]
        if r["C"] is not None:
            parts.append(("C", r["C"]))
        if r["S"] is not None:
            parts.append(("S", r["S"]))
        parts.append(("F", r["F"]))
        wsum = sum(W[k] for k, _ in parts)
        r["score"] = round(sum(W[k] * v for k, v in parts) / wsum, 2)
        r["n_dims"] = len(parts)
        r["dims_used"] = [k for k, _ in parts]

    scored = sorted([r for r in rows if r["n_dims"] >= 3], key=lambda r: -r["score"])
    vals = [r["score"] for r in scored]
    p90 = sorted(vals)[int(len(vals) * .90)]
    rec = [r for r in scored if r["score"] >= p90 and r["n_dims"] >= 3 and r["signals"] >= 3]
    # 同分/边界：把等于 P90 的所有机构都纳入，避免「卡在阈值上被随机截断」
    full = [r for r in rows if r["n_dims"] == 4]

    # ---- 权重敏感性（只在四维齐全的 129 家里比较，避免缺维重归一混淆）----
    base_rank = {r["name"]: r["score"] for r in full}
    schemes = [("基准 0.30/0.20/0.15/0.10", {"A": .30, "C": .20, "S": .15, "F": .10}),
               ("能级优先 0.50/0.20/0.15/0.15", {"A": .50, "C": .20, "S": .15, "F": .15}),
               ("协同优先 0.25/0.45/0.15/0.15", {"A": .25, "C": .45, "S": .15, "F": .15}),
               ("稀缺优先 0.25/0.20/0.40/0.15", {"A": .25, "C": .20, "S": .40, "F": .15})]
    sens = []
    base_sorted = [r["name"] for r in sorted(full, key=lambda r: -r["score"])]
    for label, Wx in schemes:
        vals_x = sorted(((r["name"], sum(Wx[k] * r[k] for k in ("A", "C", "S", "F")) / sum(Wx.values()))
                         for r in full), key=lambda t: -t[1])
        names = [n for n, _ in vals_x]
        sens.append({
            "weights": label,
            "spearman_vs_base": M.spearman([base_rank[n] for n in names],
                                           [v for _, v in vals_x]),
            "top1": names[0],
            "top10_overlap": len(set(names[:10]) & set(base_sorted[:10])),
            "top5": names[:5],
        })

    def card(r, with_hint=True):
        d = {"name": r["name"], "city": r["city"], "org_type": r["org_type"],
             "score": r["score"], "n_dims": r["n_dims"], "dims_used": r["dims_used"],
             "A": r["A"], "C": r["C"], "S": r["S"], "F": r["F"],
             "signals": r["signals"],
             "patents": r["patents"], "patent_grant": r["patent_grant"],
             "papers": r["papers"], "projects": r["projects"], "scholars": r["scholars"],
             "fund_wan": r["fund_wan"], "co_sz_inst": r["co_sz_inst"],
             "co_sz_company": r["co_sz_company"],
             "dom_src": r["dom_src"], "dom_vec": r["dom_vec"],
             "inc_year": r["inc_year"], "capital_wan": r["capital_wan"],
             "F_parts": r["F_parts"]}
        if with_hint:
            d["sz_branch_hint"] = branch_hint(r["name"], sz_names)
        return d

    city_stat = {}
    for c in ["广州市", "东莞市", "惠州市"]:
        sub = [r for r in scored if r["city"] == c]
        city_stat[c] = {"candidates": sum(1 for x in cand if x["city"] == c),
                        "with_signal": sum(1 for x in cand if x["city"] == c
                                           and (x["patents"] or x["papers"] or x["projects"] or x["scholars"])),
                        "scored": len(sub),
                        "score_mean": round(sum(r["score"] for r in sub) / len(sub), 2) if sub else None,
                        "in_recommended": sum(1 for r in rec if r["city"] == c)}

    out = {
        "metric_id": MID,
        "metric_name": "科研机构引入推荐模型（重建件）",
        "domain": "ORG / 科研机构深度分析（序号 154）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false；旧稿 AI-20261016 已被隔离重建）",
        "support_judgment": "部分支持",
        "rebuild_note": ("旧版依赖 `_org_graph_common`（模块级导入演示库连接器，连演示库），"
                         "已隔离至 `_quarantine/20261022_demo_helper/`。本件从 gkx 快照重取，"
                         "不 import 被隔离的三件 helper。"),
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "本件是横截面排序，不计算同比/增速。专利为 2021—2026 存量（库内 apdt_year 仅此六年，"
            "2017—2020 零行，不按 0 摊入；2026 为残年）；论文 100,900 篇覆盖 1980—2026，"
            "项目 58,452 条覆盖 1986—2022。任一年份都不作趋势外推。"),
        "inputs": {
            "roster": "gkx.dwd_research_institute_base_info 2,074 家（100% 广东省）",
            "panel": "_snapshots21/org_family_panel_20261021.json（专利存量/授权、论文、项目、学者、合著对）",
            "ipc4": "_snapshots21/patent_ipc4_by_name_20261021.json（581,585 行）",
            "reg": "_snapshots21/org_reg_gkx21.json（2,074 行登记字段，source 字段记录 gkx 主机与拉取时间）",
            "base_city": "_snapshots21/base_20261021.json（189,116 行企业底册 name→city，判「深圳企业」）",
        },
        "q_dim_status": {
            "available": False,
            "definition_in_requirement": "与本地产业需求的契合度",
            "upstream_claimed_by_old_version": "M_TALENT_SZ_SUPPLY_DEMAND 的 by_domain_share",
            "why_missing": ("该产物不在本目录 code/ 下（旧版用 `if os.path.exists(DEMAND)` 守卫，"
                            "缺文件时整维静默跳过、脚本仍 exit 0）。本目录内没有深圳岗位需求按域的份额表，"
                            "因此 Q 维缺需求数据、未计算——不以任何代理值顶替，也不把「跳过」写成「已算」。"),
            "consequence": "得分只含 A/C/S/F 四维，不能读成「产业需求契合度」；Q 修复后需整体重跑并重排。",
        },
        "coverage": {
            "institutes": len(inst),
            "shenzhen": len(sz),
            "candidates_total": len(cand),
            "candidates_with_signal": len(rows),
            "candidate_signal_pct": round(len(rows) / len(cand), 4),
            "candidates_zero_signal": len(cand) - len(rows),
            "with_patents": sum(1 for r in rows if r["patents"]),
            "with_papers": sum(1 for r in rows if r["papers"]),
            "with_projects": sum(1 for r in rows if r["projects"]),
            "with_scholars": sum(1 for r in rows if r["scholars"]),
            "with_domain_vector": sum(1 for r in rows if r["dom_vec"]),
            "with_domain_ipc": sum(1 for r in rows if r["dom_src"] == "ipc4"),
            "with_sz_inst_coauthor": sum(1 for r in rows if r["co_sz_inst"] > 0),
            "with_sz_company_coauthor": sum(1 for r in rows if r["co_sz_company"] > 0),
            "scored_n_dims_ge3": len(scored),
            "scored_n_dims_4": len(full),
            "base_city_dup_names": base_dup,
        },
        "dims": {
            "weights": W,
            "A": "pct_rank(log1p(专利存量 + 2×论文 + 项目数))；论文在机构署名上比专利更稳定，故 2 倍权重",
            "Q": "未计算（见 q_dim_status）",
            "C": "minmax_log(3×与深机构合著篇次 + 2×与深企业合著篇次)；仅对「有论文记录」的候选可算",
            "S": "Σ_d v_{i,d}(1 − s^SZ_d)；v 优先 IPC4，其次项目学科/论文关键词；s^SZ 取深圳 74 家有 IPC 机构",
            "F": "机构类型 40/25/10 + 登记年限 30/20/10 + 开办资金 30/20/10（万元，满 1000 万记满）",
            "renormalize": "缺维在剩余维重归一；nd=3 表示 A/F 加 C 或 S 之一，nd=4 表示四维齐全",
        },
        "sz_domain_baseline": {
            "orgs_with_ipc": sum(1 for x in sz if dom_src.get(x["name"]) == "ipc4"),
            "patents": sz_tot,
            "share": {d: round(v, 4) for d, v in sorted(sz_share.items(), key=lambda kv: -kv[1])},
        },
        "score_dist": M.dist(vals),
        "thresholds": {"p90": round(p90, 2), "min_dims": 3, "min_signals": 3,
                       "rule": "score ≥ P90 且 nd ≥ 3 且 signals ≥ 3；缺维机构不参与该年的「四维齐全」敏感性"},
        "recommended_n": len(rec),
        "recommended": [card(r) for r in rec],
        "recommended_present_in_sz": {
            "n": sum(1 for r in rec if branch_hint(r["name"], sz_names)),
            "names": [r["name"] for r in rec if branch_hint(r["name"], sz_names)],
            "clean_n": sum(1 for r in rec if not branch_hint(r["name"], sz_names)),
            "clean": [card(r) for r in rec if not branch_hint(r["name"], sz_names)],
            "note": ("`sz_branch_hint` 是「候选机构名出现在深圳机构名里」的字符串命中，"
                     "如「广州中医药大学」命中「广州中医药大学深圳医院（福田）」。这类候选已有深圳分支，"
                     "对它们做「引入」在政策上无意义，页面应置灰或单列「已布局」，"
                     "主榜按 `clean` 口径出。字符串命中会漏（分支机构改名、仅设办事处），"
                     "所以 `clean` 也不等于「确未布局」。"),
        },
        "top30": [card(r) for r in scored[:30]],
        "full_dim_ranking": [card(r, with_hint=False) for r in sorted(full, key=lambda r: -r["score"])],
        "sensitivity": sens,
        "city_stat": city_stat,
        "org_type_stat": {
            t: {"scored": sum(1 for r in scored if r["org_type"] == t),
                "in_recommended": sum(1 for r in rec if r["org_type"] == t),
                "score_mean": round(sum(r["score"] for r in scored if r["org_type"] == t)
                                    / max(1, sum(1 for r in scored if r["org_type"] == t)), 2)}
            for t in sorted({r["org_type"] for r in scored})
        },
        "counterfactual": [
            {"if": "要出全国/全球引入清单", "needs": "省外与海外机构底册",
             "status": "底册 2,074 家 100% 广东省（深圳 1,014 / 广州 822 / 东莞 127 / 惠州 111）",
             "verdict": "不可做"},
            {"if": "要训练一个引入推荐模型", "needs": "历史引入名单 + 引进后 3—5 年产出/留存标签",
             "status": "0 条标签", "verdict": "不可做（本件是确定性 MCDA，不是监督学习）"},
            {"if": "要算「产业需求契合」", "needs": "深圳岗位需求按技术域的份额表（by_domain_share）",
             "status": "该产物不在本目录；Q 维未计算", "verdict": "不可做"},
            {"if": "要算「落地成本/投入产出」", "needs": "土地、编制、财政投入、机构意愿",
             "status": "0 条", "verdict": "不可做"},
        ],
        "limits": [
            "候选池只有省内非深 1,060 家，不能称「全国/全球引入清单」。",
            "Q 维缺需求数据、未计算；得分不含「产业需求契合」，任何「契合度高」的表述越界。",
            "C 维只覆盖 23 家候选（有与深合著记录者），其余候选按缺失处理并在剩余维重归一；"
            "合著仅来自 100,900 篇论文的作者单位串，企业侧署名常写子公司，收录不全。",
            "S 维只覆盖 129 家（有 IPC 或项目学科/关键词），76 家有信号候选无技术结构证据。",
            "F 维的 `registered_capital_value` 列注释写「元」，实测量级为万元（中位 100、最大 222,916），"
            "按万元使用；若甲方口径为元，F 的资金项需整体重标。",
            "登记日期是法人登记日，不等于建所年份（中科院广州能源所登记 2016，建所 1978），"
            "F 的年限项对老所系统性偏低。",
            "无历史引入标签，阈值 P90 是规则阈值，不是训练出来的分界线。",
            "机构名跨源未消歧：如「中国科学院深圳先进技术研究院」与「深圳先进技术研究院」在底册中是两条记录。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path)
    print("coverage", out["coverage"])
    print("dist", out["score_dist"], "p90", out["thresholds"]["p90"])
    print("recommended", len(rec), [(r["name"], r["score"]) for r in rec[:12]])
    print("sens", [(s["weights"], s["spearman_vs_base"], s["top10_overlap"]) for s in sens])


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
    out_json = here / "M_ORG_DEEP_154_1_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_DEEP_154_1.py 等价）
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
        "metric_id": "M_ORG_DEEP_154_1",
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
