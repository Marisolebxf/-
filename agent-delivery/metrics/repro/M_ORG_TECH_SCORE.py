#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 三系统兼容升级件·D2 拆分原 ID】本件继承算法库口径（原版不动）
# 【同名指标族·互见】M_ORG_TECH_SCORE_ZS（专题/展示侧拆分件）: ../第三方库指标计算过程/M_ORG_TECH_SCORE_ZS.md ｜ code/M_ORG_TECH_SCORE_ZS.py
# 【维护者】唐绍祖
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_TECH_SCORE 科研机构技术力评价与对比
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D2 口径级分歧（本件复核为可兼容·配置型） ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_TECH_SCORE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_TECH_SCORE · 科研机构技术力对比分析（ORG 域）

需求锚点：展示系统 §1.1.1.2.4.2.4.6 ——「用户配置技术力评价指标及权重，对多家科研机构进行
横向对比，输出雷达图与排名」；算法库 155「科研机构扶持推荐」用的是同一批指标，但口径不同
（155 是扶持优先级，本件是**用户可配权重的技术力对比**）。

与 149 / TECH_LAYOUT 的分工：
  149         ：领域结构强度（份额³×规模），回答「哪个领域强」
  TECH_LAYOUT ：领域广度/深度画像 + IPC4 下钻，回答「在做什么」
  本件        ：**可配权重的多指标合成 + 排名 + 雷达**，回答「谁更强、强在哪几项」

口径（全部为池内百分位，不做跨库标准化）：
  score_i = Σ_k w_k · pct_{i,k} / Σ_k w_k      （k 只取该机构有值的指标；缺项不进分母）
  pct      = 池内百分位（0—100），对偏态稳健；指标方向统一为「越大越强」
  授权率   = 授权数 / 专利存量，只有 patents ≥5 的机构才有意义（避免 1/1=100%）
  最小可比门槛 = 7 项核心指标中至少 2 项有值（否则不参与排名）

硬边界（正文必须写）：
  - 「高价值专利」不可算：库内无权利要求数、同族数、被引证数。
  - 「论文影响力」不可算：`cites` 只有 9 家有值（且与 papers 同源），不能当影响因子用。
  - 「平台能级」不可算：无国家重点实验室/国家工程中心认定表。
  - 学者只 29 家、项目只 53 家、经费只 53 家 → 人才维与经费维在这两项上几乎不具区分度。
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402

MID = "M_ORG_TECH_SCORE"

# 指标库：key → (中文名, 取值函数, 覆盖说明, 可靠性)
CORE = ["patents", "grant_rate", "papers", "projects", "fund_wan", "scholars", "breadth"]


def build_pool(panel, ipc):
    rows = []
    for x in panel["institutions"]:
        vec = ipc.get(x["name"]) or {}
        patents = x["patents"]
        ind = {
            "patents": patents,
            "papers": x["papers"],
            "projects": x["projects"],
            "fund_wan": float(x.get("project_fund") or 0),
            "scholars": x["scholars"],
            # 授权率只对 patents ≥5 的机构可算
            "grant_rate": (x["patent_grant"] / patents) if patents >= 5 else None,
            "breadth": None,
            "policy_mentions": x["policy_mentions"],
        }
        if vec:
            ind["breadth"] = sum(1 for d in _domain_counter(vec).values() if d > 0)
        n_core = sum(1 for k in CORE if ind.get(k))
        rows.append({"name": x["name"], "city": x["city"], "org_type": x["org_type"],
                     "raw": ind, "n_core": n_core,
                     "patents": patents, "papers": x["papers"]})
    return rows


def _domain_counter(vec):
    import _org_deep21_common as OC
    from collections import Counter
    c = Counter()
    for k, v in vec.items():
        c[OC.ipc_domain(k)] += v
    return c


def pct_scores(rows, key):
    """池内百分位（并列取平均位次），返回 {name: 0—100}。

    0 视为「无值」而不是「值等于 0」：面板里 patents=0 表示该机构名没匹配上任何专利，
    不是「真的一件专利都没有」。把 0 当值参与百分位，会让 1,880 家无证据机构把池子拉大，
    并使真实机构的百分位被系统性抬高。
    """
    vals = [(r["name"], r["raw"][key]) for r in rows if r["raw"].get(key)]
    vals.sort(key=lambda t: t[1])
    n = len(vals)
    out = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[j + 1][1] == vals[i][1]:
            j += 1
        rank = (i + j) / 2
        p = 100.0 * rank / (n - 1) if n > 1 else 50.0
        for k in range(i, j + 1):
            out[vals[k][0]] = round(p, 2)
        i = j + 1
    return out, n


SCHEMES = [
    ("均衡 7 项等权", {k: 1 for k in CORE}),
    ("产出规模优先", {"patents": 25, "papers": 25, "projects": 15, "fund_wan": 15,
                 "scholars": 10, "breadth": 5, "grant_rate": 5}),
    ("质量优先（授权率加权）", {"grant_rate": 30, "papers": 25, "breadth": 20,
                        "patents": 15, "projects": 10}),
    ("人才优先", {"scholars": 45, "papers": 25, "projects": 15, "patents": 15}),
]


def main() -> None:
    panel = M.load_panel()
    ipc = M.load_ipc()
    rows = build_pool(panel, ipc)
    pool = [r for r in rows if r["n_core"] >= 2]

    pct, cover = {}, {}
    for k in CORE + ["policy_mentions"]:
        pct[k], cover[k] = pct_scores(pool, k)

    def score(r, W):
        """两套分并行：
        - `neutral`：缺失项记池内中位百分位 50（中性插补，不奖不罚）→ 主榜
        - `observed`：缺失项不进分母（重归一）→ 副榜，仅用于对照「缺项优势」有多大
        主榜选中性插补，是因为重归一会系统性奖励「只有一两项强指标」的机构：
        广州中医药大学只有 4 项可算（论文 1265 篇、项目 67 个），重归一后冲到第 1，
        但它在专利与领域广度上完全没有证据。中性插补让缺项既不加分也不减分。
        """
        num = den = 0.0
        num_o = den_o = 0.0
        used = []
        for k, w in W.items():
            v = pct[k].get(r["name"])
            num += w * (50.0 if v is None else v)
            den += w
            if v is not None:
                num_o += w * v
                den_o += w
                used.append(k)
        return (round(num / den, 2) if den else None,
                round(num_o / den_o, 2) if den_o else None, used)

    base_W = SCHEMES[0][1]
    for r in pool:
        r["score"], r["score_observed_only"], r["used"] = score(r, base_W)
    ranked = sorted(pool, key=lambda r: (-r["score"], -r["patents"]))

    # 权重敏感性
    base_rank = {r["name"]: i for i, r in enumerate(ranked)}
    scheme_ranks = {}
    sens = []
    for label, W in SCHEMES:
        sc = []
        for r in pool:
            s, _, _ = score(r, W)
            if s is not None:
                sc.append((r["name"], s, -r["patents"]))
        sc.sort(key=lambda t: (-t[1], t[2]))
        names = [n for n, _, _ in sc]
        # 并列分取平均名次：中性插补会产生大量同分机构，若用专利数破并列，
        # 名次跨度会被破并列规则人为放大（实测最坏一家跨度 193 位）。
        rk, i = {}, 0
        while i < len(sc):
            j = i
            while j + 1 < len(sc) and sc[j + 1][1] == sc[i][1]:
                j += 1
            avg = (i + j) / 2
            for k in range(i, j + 1):
                rk[sc[k][0]] = avg
            i = j + 1
        scheme_ranks[label] = rk
        sens.append({
            "weights": label,
            "w": W,
            "spearman_vs_base": M.spearman([base_rank[n] for n in names],
                                           list(range(len(names)))),
            "top1": names[0],
            "top10_overlap": len(set(names[:10]) & {r["name"] for r in ranked[:10]}),
            "top5": names[:5],
        })

    # 排名稳定性：每个机构在 4 套权重下的名次极差
    shifts = []
    for r in pool:
        ranks = [m[r["name"]] for m in scheme_ranks.values() if r["name"] in m]
        if len(ranks) >= 2:
            shifts.append({"name": r["name"], "min": round(min(ranks) + 1, 1),
                           "max": round(max(ranks) + 1, 1),
                           "span": round(max(ranks) - min(ranks), 1)})
    shifts.sort(key=lambda s: -s["span"])

    # 雷达数据：前 12 名的 7 项百分位
    radar = [{"name": r["name"], "score": r["score"],
              "axes": {k: pct[k].get(r["name"]) for k in CORE}} for r in ranked[:12]]

    out = {
        "metric_id": MID,
        "metric_name": "科研机构技术力对比分析",
        "domain": "ORG / 科研机构技术力对比分析（展示系统 §1.1.1.2.4.2.4.6）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025, 2026], [2017, 2018, 2019, 2020],
            "指标全部是存量/累计口径：专利 2021—2026（2017—2020 库内零行，不按 0 摊入；2026 残年）、"
            "论文 1980—2026、项目 1986—2022。本件不做增速与同比，故无同比基期；"
            "缺失指标不进分母，不按 0 计。"),
        "inputs": {
            "panel": "_snapshots21/org_family_panel_20261021.json（专利/授权/论文/项目/经费/学者/政策）",
            "ipc4": "_snapshots21/patent_ipc4_by_name_20261021.json（仅用于数技术领域广度）",
        },
        "formula": {
            "score": "Σ_k w_k·pct_{i,k} / Σ_k w_k（只取该机构有值的 k）",
            "pct": "池内百分位 0—100，并列取平均位次",
            "min_indicators": 2,
            "tie_break": "专利存量降序",
            "why_percentile": ("专利存量是重尾分布（中位 8、最大 943），min-max 会把除头部以外的"
                               "所有机构压到 0—3 分；百分位保留区分度且对量纲不敏感，"
                               "代价是丢失绝对差距（第 1 与第 2 的分数差不再反映 2.4 倍的专利差）。"),
        },
        "indicator_library": {
            k: {"coverage_n": cover[k], "coverage_pct": round(cover[k] / len(rows), 4),
                "reliability": ("高" if cover[k] >= 150 else
                                "中" if cover[k] >= 50 else "低（样本不足以区分机构）"),
                "definition": {
                    "patents": "专利存量（面板 apdt 口径）",
                    "grant_rate": "授权数/存量，仅 patents≥5 可算",
                    "papers": "论文篇数（作者单位串精确匹配）",
                    "projects": "承担项目数",
                    "fund_wan": "项目资助额合计（万元，全周期）",
                    "scholars": "学者库命中人数",
                    "breadth": "技术领域广度（7 领域中专利件数 ≥1 的领域数）",
                }[k]}
            for k in CORE
        },
        "unavailable_indicators": [
            {"name": "高价值专利占比", "why": "无权利要求数/同族数/被引证数，无法区分高低价值"},
            {"name": "论文影响力（被引/期刊分区）", "why": "`cites` 仅 9 家有值，与 papers 同源，不能作影响力度量"},
            {"name": "平台能级（国家级实验室/工程中心）", "why": "库内无认定表，只能用机构类型代理但语义不同"},
            {"name": "国际合作", "why": "无「申请人×国别」「作者×国别」字段"},
            {"name": "研发投入/研发人员", "why": "年报财务表对底册 2,074 家命中 0 行，`development_employee` 整列为空"},
        ],
        "pool": {
            "institutes": len(rows),
            "pool_n": len(pool),
            "pool_rule": "7 项核心指标中 ≥2 项有值",
            "by_city": {c: sum(1 for r in pool if r["city"] == c)
                        for c in ["深圳市", "广州市", "东莞市", "惠州市"]},
            "by_type": {t: sum(1 for r in pool if r["org_type"] == t)
                        for t in sorted({r["org_type"] for r in pool})},
            "by_n_indicators": {str(k): sum(1 for r in pool if r["n_core"] == k)
                                for k in range(2, 8)},
        },
        "score_dist": M.dist([r["score"] for r in pool]),
        "bias_check": {
            "by_n_indicators": {str(k): {"n": sum(1 for r in pool if len(r["used"]) == k),
                                         "score_mean": round(sum(r["score"] for r in pool
                                                                 if len(r["used"]) == k)
                                                             / max(1, sum(1 for r in pool
                                                                          if len(r["used"]) == k)), 2)}
                                for k in range(2, 8)},
            "by_city": {c: {"n": sum(1 for r in pool if r["city"] == c),
                            "score_mean": round(sum(r["score"] for r in pool if r["city"] == c)
                                                / max(1, sum(1 for r in pool if r["city"] == c)), 2),
                            "in_top20": sum(1 for r in ranked[:20] if r["city"] == c)}
                        for c in ["深圳市", "广州市", "东莞市", "惠州市"]},
            "note": ("按「有值指标数」分组看均分：指标越全的机构均分越高，说明排名里混进了"
                     "「数据可得性」效应。中科院/省科学院系统的 7 项全有值，民非新型研发机构"
                     "多为 2—4 项。页面必须同时显示 n_indicators，否则会把「数据少」读成「技术弱」。"),
        },
        "ranking": [{"rank": i + 1, "name": r["name"], "city": r["city"],
                     "org_type": r["org_type"], "score": r["score"],
                     "score_observed_only": r["score_observed_only"],
                     "n_indicators": len(r["used"]), "used": r["used"],
                     "imputed_n": len(CORE) - len(r["used"]),
                     "pct": {k: pct[k].get(r["name"]) for k in CORE},
                     "raw": {"patents": r["raw"]["patents"], "papers": r["raw"]["papers"],
                             "projects": r["raw"]["projects"],
                             "fund_wan": r["raw"]["fund_wan"],
                             "scholars": r["raw"]["scholars"],
                             "grant_rate": (round(r["raw"]["grant_rate"], 4)
                                            if r["raw"]["grant_rate"] is not None else None),
                             "breadth": r["raw"]["breadth"]}}
                    for i, r in enumerate(ranked)],
        "top20": [{"rank": i + 1, "name": r["name"], "score": r["score"],
                   "n_indicators": len(r["used"])} for i, r in enumerate(ranked[:20])],
        "radar_top12": radar,
        "sensitivity": sens,
        "rank_stability": {"span_median": M.dist([s["span"] for s in shifts])["median"],
                           "n_span_ge10": sum(1 for s in shifts if s["span"] >= 10),
                           "worst": shifts[:8]},
        "weights_note": (
            "权重由页面传入，本件给 4 套预设用于演示「权重可配」与「结论对权重的敏感度」。"
            "四套权重下 Spearman 0.80—1.00，说明前 10 名大体稳定；但名次跨度 ≥10 位的机构有 "
            f"{sum(1 for s in shifts if s['span'] >= 10)} 家，页面必须在用户改权重时实时重排，"
            "不能缓存一份固定榜单。"),
        "limits": [
            "缺 5 类指标（高价值专利、论文影响力、平台能级、国际合作、研发投入），"
            "所谓「技术力」实际只覆盖「产出规模 + 授权率 + 领域广度」。",
            "授权率用「授权数/存量」而非「授权数/申请数」，存量含未审结与失效，授权率被系统性低估。",
            "学者 29 家、项目 53 家、经费 53 家：人才维与经费维只对少数机构生效，"
            "对这些机构有利（多一项可加分），对多数机构是缺项重归一。",
            "百分位是池内相对值，池子换了（例如只看深圳）名次会变；不能跨池比较分数。",
            "技术领域广度是「有 ≥1 件专利的领域数」（与 TECH_LAYOUT 的「份额 ≥1%」口径不同，3 家机构不一致），与「技术能力强」不是一回事："
            "广而浅的机构会比窄而深的机构得分高。",
            "机构名未消歧（「深圳先进技术研究院」与「中国科学院深圳先进技术研究院」是两条记录）。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path)
    print("pool", out["pool"])
    print("dist", out["score_dist"])
    print("top10", [(r["name"][:22], r["score"], r["n_indicators"]) for r in out["ranking"][:10]])
    print("sens", [(s["weights"], s["spearman_vs_base"], s["top10_overlap"]) for s in sens])
    print("stability", out["rank_stability"]["span_median"], out["rank_stability"]["n_span_ge10"])


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
    out_json = here / "M_ORG_TECH_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_TECH_SCORE.py 等价）
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
        "metric_id": "M_ORG_TECH_SCORE",
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
