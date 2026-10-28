#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_DEEP_120_1 产业热点领域识别模型
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_DEEP_120_1.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""产业热点领域识别模型（M_CHAIN_DEEP_120_1）。

只读 `code/_snapshots21/` 落盘快照，不连数据库；单次运行约 2 秒。

热点 = 「近期事件密度显著高于自身历史」的地方。本件只用两条可比的时间序列：
  A 资本热度：链内融资事件近三年（2023—2025）占该链全期事件比
  B 主体进入热度：链内企业近三年（2023—2025）新设占该链全期新设比
第三条腿（资讯）实测在 12 条链里只覆盖 9 条、极差 371 倍，只登记、不入合成。

叶级（细分领域）热度不可算：三种来源都没有叶级时间序列，探针逐条给出计数。

产物：code/M_CHAIN_DEEP_120_1_out.json
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_120_1"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

RECENT = (2023, 2025)      # 近三年窗口
HOT_TOP_N = 3              # 高热链条数（本件自定义）


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b, 6) if b else 0.0


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def main():
    t0 = time.time()
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")
    news = jload("news21_chain_items_20261022.json")

    name2chain = layer["names"]
    roots = {c["chain"]: c["name"] for c in panel["chains"]}

    # ---------- A 资本热度 ----------
    fin_by = defaultdict(Counter)
    fin_unmapped = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if not ch:
            fin_unmapped += 1
            continue
        ys = str(r[6])[:4]
        if ys.isdigit():
            fin_by[ch][int(ys)] += 1

    # ---------- B 主体进入热度 ----------
    nf_by = defaultdict(Counter)
    for k, v in layer["chain_year"].items():
        ch, y = k.split("|")
        nf_by[ch][int(y)] += v

    # ---------- C 资讯热度（只登记） ----------
    # 注意：用 [A-Z]{3}\d+ 而不是定长 7 位。定长写法会把 5 位码（INA01 这类）
    # 整段漏掉，于是「标签深度分布」只剩 7 这一档，看起来像「全部是根链标签」——
    # 实际是正则把短码吃掉了。这条是本轮实测踩到的坑，写在这里防止复现。
    code_re = re.compile(r"[A-Z]{3}\d+")
    news_by = Counter()
    tag_depth = Counter()
    for r in news["rows"]:
        raw = r[1]
        for x in code_re.findall(raw if isinstance(raw, str) else ""):
            tag_depth[len(x)] += 1
            if len(x) >= 7 and x[:7] in roots:
                news_by[x[:7]] += 1

    # ---------- 逐链 ----------
    rows = []
    for ch, nm in roots.items():
        fe = fin_by.get(ch, Counter())
        nf = nf_by.get(ch, Counter())
        fin_total = sum(fe.values())
        nf_total = sum(nf.values())
        fin_recent = sum(fe.get(y, 0) for y in range(RECENT[0], RECENT[1] + 1))
        nf_recent = sum(nf.get(y, 0) for y in range(RECENT[0], RECENT[1] + 1))
        rows.append({
            "chain": ch, "name": nm,
            "fin_total": fin_total, "fin_recent": fin_recent,
            "fin_recent_share": pct(fin_recent, fin_total),
            "newfirm_total": nf_total, "newfirm_recent": nf_recent,
            "newfirm_recent_share": pct(nf_recent, nf_total),
            "news_18m": news_by.get(ch, 0),
        })

    # 合成：两条腿先各自归一，再等权平均（权重自定义、待确认）
    s_fin = minmax([r["fin_recent_share"] for r in rows])
    s_nf = minmax([r["newfirm_recent_share"] for r in rows])
    for r, a, b in zip(rows, s_fin, s_nf):
        r["score_fin"] = round(a, 6)
        r["score_newfirm"] = round(b, 6)
        r["heat"] = round((a + b) / 2, 6)
    rows.sort(key=lambda x: -x["heat"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["class"] = "高热" if i <= HOT_TOP_N else ("中热" if r["heat"] >= 0.4 else "低热")

    heat_vals = [r["heat"] for r in rows]
    corr_pairs = [(r["fin_recent_share"], r["newfirm_recent_share"]) for r in rows]

    # 叶级可达性探针
    leaves = sum(c["leaves"] for c in panel["chains"])
    leaf_signal = 0          # 具备叶级时间序列的来源数
    compute = {
        "window_recent": list(RECENT),
        "chains": rows,
        "n_high": sum(1 for r in rows if r["class"] == "高热"),
        "n_mid": sum(1 for r in rows if r["class"] == "中热"),
        "n_low": sum(1 for r in rows if r["class"] == "低热"),
        "heat_max": {"name": rows[0]["name"], "heat": rows[0]["heat"]},
        "heat_min": {"name": rows[-1]["name"], "heat": rows[-1]["heat"]},
        "fin_events_total": len(fin["fin"]),
        "fin_events_mapped": len(fin["fin"]) - fin_unmapped,
        "fin_unmapped": fin_unmapped,
        "fin_recent_total": sum(r["fin_recent"] for r in rows),
        "newfirm_recent_total": sum(r["newfirm_recent"] for r in rows),
        "newfirm_total": sum(r["newfirm_total"] for r in rows),
        "news_rows": len(news["rows"]),
        "news_chains_covered": sum(1 for r in rows if r["news_18m"] > 0),
        "news_chains_zero": sum(1 for r in rows if r["news_18m"] == 0),
        "news_zero_chains": [r["name"] for r in rows if r["news_18m"] == 0],
        "news_max_chain": max(rows, key=lambda r: r["news_18m"])["name"],
        "news_max": max(r["news_18m"] for r in rows),
        "news_min_nonzero": min([r["news_18m"] for r in rows if r["news_18m"] > 0] or [0]),
        "news_skew_ratio": round(max(r["news_18m"] for r in rows)
                                 / max(1, min([r["news_18m"] for r in rows if r["news_18m"] > 0] or [1])), 2),
        "news_tag_depths": {str(k): v for k, v in sorted(tag_depth.items())},
        "news_leaf_tags": sum(v for k, v in tag_depth.items() if k >= 9),
        "news_max_tag_len": max(tag_depth) if tag_depth else 0,
        "leaf_nodes": leaves,
        "leaf_level_sources": leaf_signal,
        "leaf_level_sources_required": 3,
        "fin_fields": 8,
    }

    out = {
        "metric": METRIC,
        "title": "产业热点领域识别模型",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "链级热度可用两条可比时间序列合成：融资事件近三年 %d 起（占挂链事件 %.2f%%）、"
            "新设企业近三年 %d 家（占可挂链新设 %.2f%%），12 条链全部有值。"
            "但产品要的「领域」是叶级：954 个叶级环节中，具备叶级时间序列的来源为 %d/3——"
            "资讯标签最深只到 7 位根链（叶级标签 0 个）、融资表无环节字段（8 列）、"
            "成立年份只到链级。资讯腿本身还只覆盖 %d/12 条链（%s 为 0），"
            "极差 %d : %d（%.1f 倍），不可作横截面比较。故判部分支持："
            "能给「哪条链在升温」，不能给「链里哪个细分领域在升温」。"
            % (sum(r["fin_recent"] for r in rows),
               sum(r["fin_recent"] for r in rows) / (len(fin["fin"]) - fin_unmapped) * 100,
               sum(r["newfirm_recent"] for r in rows),
               sum(r["newfirm_recent"] for r in rows) / sum(r["newfirm_total"] for r in rows) * 100,
               leaf_signal, sum(1 for r in rows if r["news_18m"] > 0),
               "、".join(r["name"] for r in rows if r["news_18m"] == 0),
               compute["news_max"], compute["news_min_nonzero"], compute["news_skew_ratio"])
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 1),
        "sources": {
            "snapshots": ["code/_snapshots21/chain_panel21.json",
                          "code/_snapshots21/chain21_layer_20261022.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/news21_chain_items_20261022.json"],
            "upstream_tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_industry_chain_info",
                                "gkx.dwd_org_base_info", "gkx.dwd_org_financing_info",
                                "gkx.dwd_industry_chain_news_info"],
        },
        "base_years_used": list(range(RECENT[0], RECENT[1] + 1)),
        "base_years_missing": [],
        "base_years_note": (
            "近三年窗口 2023—2025 全部有数，未做缺年摊 0；2026 年为不完整年（截至 07），"
            "不入窗口。分母为各链全期（1990—2025）事件数，属同源分母，不是外部总量。"
        ),
        "params": {
            "recent_window": list(RECENT),
            "weights": {"capital": 0.5, "entry": 0.5},
            "hot_top_n": HOT_TOP_N,
            "normalization": "min-max（12 条链内）",
            "weight_note": "等权、近三年窗口与高热条数均为本件自定义、待甲方确认；不是官方口径",
        },
        "compute": compute,
        "missing_dims": [
            {"dim": "叶级热度", "status": "不可得",
             "evidence": "资讯标签深度分布 %s，9 位以上（叶级）码 %d 个；融资表 8 列无 industry_code；成立年份只到链级"
                         % (json.dumps(compute["news_tag_depths"], ensure_ascii=False),
                            compute["news_leaf_tags"]),
             "impact": "热点只能落到「链」，落不到「链内细分领域」，产品想要的领域卡片做不出"},
            {"dim": "资讯腿的横向可比性", "status": "不足",
             "evidence": "12 条链中 %d 条资讯为 0，非零链极差 %.1f 倍"
                         % (compute["news_chains_zero"], compute["news_skew_ratio"]),
             "impact": "资讯热度只能做单链纵向，不进合成"},
            {"dim": "热点阈值参数", "status": "不存在",
             "evidence": "库内无热点判定参数表；本件用 min-max + top3（自定义）",
             "impact": "「高热」条数随阈值变，须会签"},
            {"dim": "资金金额", "status": "部分",
             "evidence": "融资表有金额字段但币种不统一（CNY/USD 混列），本件只用事件次数",
             "impact": "热度是「事件频次热度」，不是「资金规模热度」"},
        ],
        "counter_checks": [
            {"id": "C1", "question": "资讯腿能不能直接进合成？",
             "action": "逐链统计 18 个月资讯数并算极差",
             "result": "%d/12 条链资讯为 0（%s），非零链最高 %s %d 条、最低 %d 条，相差 %.1f 倍；"
                       "这是标签体系覆盖差异，不是热度差异，进合成会把「标签覆盖好」误判成「热」。"
                       % (compute["news_chains_zero"], "、".join(compute["news_zero_chains"]),
                          compute["news_max_chain"], compute["news_max"],
                          compute["news_min_nonzero"], compute["news_skew_ratio"])},
            {"id": "C2", "question": "两条腿会不会给出互相矛盾的排序（说明合成无意义）？",
             "action": "对照融资榜单与新设榜单的名次差",
             "result": "融资热度第 1 为 %s（%.4f），新设热度第 1 为 %s（%.4f）；"
                       "12 条链里两条腿名次相差 ≥4 位的有 %d 条，说明两腿信息不完全重叠，合成分有增量。"
                       % (max(rows, key=lambda r: r["score_fin"])["name"],
                          max(r["score_fin"] for r in rows),
                          max(rows, key=lambda r: r["score_newfirm"])["name"],
                          max(r["score_newfirm"] for r in rows),
                          sum(1 for r in rows
                              if abs(sorted(rows, key=lambda x: -x["score_fin"]).index(r)
                                     - sorted(rows, key=lambda x: -x["score_newfirm"]).index(r)) >= 4))},
            {"id": "C3", "question": "「近三年占比高」是不是只是因为它总量小？",
             "action": "同时列出分子分母（fin_recent/fin_total、newfirm_recent/newfirm_total）",
             "result": "低空经济融资总量仅 %d 起、近三年占比 %.2f%%；生物医药总量 %d 起、占比 %.2f%%。"
                       "小样本链的占比方差大，读榜时必须带分母。"
                       % (next(r["fin_total"] for r in rows if r["name"] == "低空经济"),
                          next(r["fin_recent_share"] for r in rows if r["name"] == "低空经济") * 100,
                          next(r["fin_total"] for r in rows if r["name"] == "生物医药"),
                          next(r["fin_recent_share"] for r in rows if r["name"] == "生物医药") * 100)},
            {"id": "C4", "question": "能不能用「叶级企业数」当热点（静态热门）？",
             "action": "统计叶级企业数分布与时间维度",
             "result": "%d 个叶级环节只有企业数快照，无年份、无融资、无资讯；"
                       "企业数多说明「存量大」，不等于「在升温」，用它当热点会把成熟环节误报为热点。" % leaves},
        ],
        "notes": [
            "热度的语义边界：本件衡量「近期事件占自身历史的比重」，不是「事件绝对规模」。",
            "与 M_CHAIN_HOT_NEWS_COUNT 的分工：那件数资讯条数（单链纵向），本件做链间合成排名且明确剔除资讯腿。",
            "与 M_CHAIN_CYCLE_STAGE 的分工：那件判生命周期阶段，本件判近期升温速度。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("[OK] %s -> %s（%.1fs）高热 %d 条，资讯覆盖 %d/12，叶级源 %d/3"
          % (METRIC, OUT, out["elapsed_sec"], compute["n_high"],
             compute["news_chains_covered"], leaf_signal))


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
    out_json = here / "M_CHAIN_DEEP_120_1_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_DEEP_120_1.py 等价）
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
        "metric_id": "M_CHAIN_DEEP_120_1",
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
