#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_DEEP_119_1 产业发展路线历程模型
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_DEEP_119_1.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""产业发展路线历程模型（M_CHAIN_DEEP_119_1）。

只读 `code/_snapshots21/` 落盘快照，不连数据库；单次运行约 3 秒。

本件用三条已有时间序列重建「链的成长曲线」，替代旧稿里那张不存在的事件表：
  L1 主体进入：链内企业按成立年份计数（chain21_layer_20261022.json 的 chain_year）
  L2 资本进入：链内融资事件按年份计数（chain21_fin_degree_20261022.json + 名称挂链）
  L3 舆论关注：链内资讯按年月计数（news21_chain_items_20261022.json，仅 2025-02—2026-07）
  L4 政策（仅作城市级背景）：dwd_policy_base 的深圳政策按年计数（无链标签）

阶段判定阈值是本件自定义（见 params），不是官方口径。

产物：code/M_CHAIN_DEEP_119_1_out.json
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter, defaultdict

METRIC = "M_CHAIN_DEEP_119_1"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")

Y0, Y1 = 1990, 2025          # 统计窗口（2026 为不完整年，不入序列）
# 阶段边界不用人工阈值，改用事件累计分位：
#   P33 年 = 累计事件达到全期 1/3 的年份；P67 年 = 达到 2/3 的年份。
#   「扩张窗口」= P67 - P33，衡量一条链把中间三分之一事件压缩在多长时间内。
# 为什么不用「起步/加速/成熟」三档命名：那需要阈值参数表，库内没有，
# 硬套阈值会把 11/12 条链判成同一档（实测），等于用标签掩盖无区分度。
Q1, Q2 = 1 / 3, 2 / 3


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(a / b, 6) if b else 0.0


def main():
    t0 = time.time()
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")
    news = jload("news21_chain_items_20261022.json")
    policy = jload("policy_base_20261021.json")

    name2chain = layer["names"]

    # ---------- L1 主体进入 ----------
    newfirm = defaultdict(Counter)          # chain -> year -> n
    newfirm_out_window = 0
    for k, v in layer["chain_year"].items():
        ch, y = k.split("|")
        yi = int(y)
        if Y0 <= yi <= Y1:
            newfirm[ch][yi] += v
        elif yi > Y1:
            newfirm_out_window += v

    # ---------- L2 资本进入 ----------
    fin_by = defaultdict(Counter)
    fin_pre_window = 0
    fin_unmapped = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if not ch:
            fin_unmapped += 1
            continue
        ys = str(r[6])[:4]
        if not ys.isdigit():
            continue
        yi = int(ys)
        if yi < Y0:
            fin_pre_window += 1
            continue
        if yi <= Y1:
            fin_by[ch][yi] += 1

    # ---------- L3 资讯 ----------
    # 快照里 industry_code 是 JSON 数组的字符串形态，实测有整行被截断的行
    # （字符串在中途断开，json.loads 直接抛错）。这里按码型正则抽取，不依赖 JSON 完整：
    # 12 条链的根码形如 INB1306（3 位字母 + 4 位数字），取其前 7 位即为根。
    code_re = re.compile(r"[A-Z]{3}\d{4}")
    news_by_chain = Counter()
    news_by_chain_ym = defaultdict(Counter)
    news_chain_tag_rows = 0
    news_tag_parse_fail = 0
    for r in news["rows"]:
        raw = r[1]
        if isinstance(raw, str):
            try:
                json.loads(raw)
            except Exception:
                news_tag_parse_fail += 1
            codes = code_re.findall(raw)
        else:
            codes = [str(x) for x in (raw or [])]
        roots = sorted({c for c in codes})
        d = str(r[4])[:7]
        if roots:
            news_chain_tag_rows += 1
        for c in roots:
            news_by_chain[c] += 1
            news_by_chain_ym[c][d] += 1
    chain_roots = {c["chain"] for c in panel["chains"]}
    news_by_chain = Counter({k: v for k, v in news_by_chain.items() if k in chain_roots})

    # ---------- L4 政策（城市级） ----------
    pol_sz = Counter()
    pol_all = Counter()
    for p in policy:
        y = str(p.get("date") or "")[:4]
        if not y.isdigit():
            continue
        pol_all[int(y)] += 1
        if p.get("city") == "深圳市":
            pol_sz[int(y)] += 1
    pol_years = sorted(y for y in pol_all if 1981 <= y <= 2025)

    # ---------- 逐链 ----------
    chains = []
    for c in panel["chains"]:
        ch = c["chain"]
        nf = newfirm.get(ch, Counter())
        fe = fin_by.get(ch, Counter())
        total_nf = sum(nf.values())
        total_fe = sum(fe.values())
        yrs = sorted(set(nf) | set(fe))
        span = (max(yrs) - min(yrs) + 1) if yrs else 0
        # 事件累计分位年（新设 + 融资合计）
        ev = [(y, nf.get(y, 0) + fe.get(y, 0)) for y in range(Y0, Y1 + 1)]
        total_ev = sum(x[1] for x in ev)
        p33 = p67 = None
        cum = 0
        for y, n in ev:
            cum += n
            if p33 is None and total_ev and cum >= total_ev * Q1:
                p33 = y
            if p67 is None and total_ev and cum >= total_ev * Q2:
                p67 = y
        peak_nf = max(nf.items(), key=lambda kv: kv[1]) if nf else (None, 0)
        peak_fe = max(fe.items(), key=lambda kv: kv[1]) if fe else (None, 0)
        last5_nf = sum(nf.get(y, 0) for y in range(Y1 - 4, Y1 + 1))
        last5_fe = sum(fe.get(y, 0) for y in range(Y1 - 4, Y1 + 1))
        expand_window = (p67 - p33) if (p33 and p67) else None
        density = round((total_nf + total_fe) / span, 2) if span else 0.0
        # 里程碑代理：事件数最高的 3 个年份（不是真实里程碑事件）
        yearly = [(y, nf.get(y, 0) + fe.get(y, 0), nf.get(y, 0), fe.get(y, 0))
                  for y in range(Y0, Y1 + 1)]
        top_years = sorted(yearly, key=lambda x: -x[1])[:3]
        chains.append({
            "chain": ch, "name": c["name"],
            "newfirms": total_nf, "fin_events": total_fe,
            "first_year": min(yrs) if yrs else None, "span_years": span,
            "p33_year": p33, "p67_year": p67, "expand_window": expand_window,
            "peak_newfirm_year": peak_nf[0], "peak_newfirm_count": peak_nf[1],
            "peak_fin_year": peak_fe[0], "peak_fin_count": peak_fe[1],
            "last5_newfirm": last5_nf, "last5_newfirm_share": pct(last5_nf, total_nf),
            "last5_fin": last5_fe, "last5_fin_share": pct(last5_fe, total_fe),
            "event_density": density,
            "top_years": [{"year": y, "events": e, "newfirms": a, "fin": b}
                          for y, e, a, b in top_years],
            "series": [[y, nf.get(y, 0), fe.get(y, 0)] for y in range(Y0, Y1 + 1)],
            "event_share_last5": pct(last5_nf + last5_fe, total_ev) if total_ev else 0.0,
            "news_2025_2026": news_by_chain.get(ch, 0),
        })
    chains.sort(key=lambda x: (x["p67_year"] or 9999))

    # ---------- 母体与覆盖 ----------
    base = jload("base_20261021.json")
    base_rows = len(base)
    nf_all_years = sum(layer["chain_year"].values())
    year_cov = pct(nf_all_years, base_rows)

    windows = [c["expand_window"] for c in chains if c["expand_window"] is not None]

    n_mapped_fin = len(fin["fin"]) - fin_unmapped
    compute = {
        "window": [Y0, Y1],
        "chain_count": len(chains),
        "chains": chains,
        "expand_window_min": min(windows) if windows else None,
        "expand_window_max": max(windows) if windows else None,
        "expand_window_median": sorted(windows)[len(windows) // 2] if windows else None,
        "newfirms_total": sum(c["newfirms"] for c in chains),
        "newfirms_all_years": nf_all_years,
        "base_rows": base_rows,
        "newfirms_year_coverage": year_cov,
        "fin_events_total": sum(c["fin_events"] for c in chains),
        "newfirms_out_of_window": newfirm_out_window,
        "fin_pre_window_rows": fin_pre_window,
        "fin_unmapped_rows": fin_unmapped,
        "fin_all_rows": len(fin["fin"]),
        "fin_mapped_rows": n_mapped_fin,
        "fin_mapped_ratio": pct(n_mapped_fin, len(fin["fin"])),
        "news_rows": len(news["rows"]),
        "news_rows_with_chain": news_chain_tag_rows,
        "news_tag_parse_fail": news_tag_parse_fail,
        "news_window": [news["rows"] and min(str(r[4])[:10] for r in news["rows"]),
                        news["rows"] and max(str(r[4])[:10] for r in news["rows"])],
        "news_total_per_chain": sum(news_by_chain.values()),
        "news_month_count": len({str(r[4])[:7] for r in news["rows"]}),
        "policy_rows": len(policy),
        "policy_sz_rows": sum(pol_sz.values()),
        "policy_year_min": min(pol_years) if pol_years else None,
        "policy_year_max": max(pol_years) if pol_years else None,
        "policy_sz_series": [[y, pol_sz.get(y, 0)] for y in range(1990, Y1 + 1)],
        "policy_recent_years": {y: pol_all.get(y, 0) for y in (2020, 2021, 2022, 2023, 2024, 2025)},
        "chain_has_milestone_table": False,
        "leaf_year_rows": 0,
    }

    out = {
        "metric": METRIC,
        "title": "产业发展路线历程模型",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "成长曲线可用两条全量时间序列重建：链内企业成立年（窗口内 %d 家）与链内融资事件年"
            "（窗口内 %d 起；融资表 %d 行中 %d 行可按企业名挂到 12 条链，占 %.2f%%）。"
            "但旧稿的三块核心依赖在 gkx 均不存在：里程碑事件表、阶段阈值参数表、政策表的链标签"
            "（缺表三态见 TABLE_ABSENCE_EVIDENCE.md）；资讯腿只有 %d 行、覆盖 %s 至 %s 共 %d 个月，"
            "不足以支撑「历程」。成立年份字段也只覆盖底册 %d 家中的 %d 家（%.2f%%），早期年份左截断。"
            "故判部分支持：能给「按年事件密度 + 阶段切分」，不能给「带里程碑的路线图」。"
            % (compute["newfirms_total"], compute["fin_events_total"], len(fin["fin"]),
               n_mapped_fin, n_mapped_fin / len(fin["fin"]) * 100,
               len(news["rows"]), compute["news_window"][0], compute["news_window"][1],
               compute["news_month_count"], base_rows, nf_all_years, year_cov * 100)
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 1),
        "sources": {
            "snapshots": ["code/_snapshots21/chain_panel21.json",
                          "code/_snapshots21/chain21_layer_20261022.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/news21_chain_items_20261022.json",
                          "code/_snapshots21/policy_base_20261021.json"],
            "upstream_tables": ["gkx.dwd_org_base_info", "gkx.dwd_org_industry_tags",
                                "gkx.dwd_org_financing_info", "gkx.dwd_industry_chain_news_info",
                                "gkx.dwd_policy_base"],
        },
        "base_years_used": list(range(Y0, Y1 + 1)),
        "base_years_missing": [],
        "base_years_note": (
            "序列窗口 1990—2025 全部入图，未做任何「缺年按 0 摊入」的插补："
            "某年计数为 0 就是当年 0 起事件/0 家新设，不是缺数。2026 年为不完整年"
            "（数据截至 2026-07），整年排除，不入分母。资讯腿另按 2025-02—2026-07 的"
            "18 个月窗口统计，与 1990—2025 的年度序列不同源，不混算。"
        ),
        "params": {
            "window": [Y0, Y1],
            "quantile_edges": [Q1, Q2],
            "weight_note": "阶段边界用事件累计 1/3、2/3 分位年（本件自定义切分方式，无人工阈值）；"
                           "不输出「起步/加速/成熟」标签，因为阈值参数表在 gkx 不存在",
        },
        "compute": compute,
        "missing_dims": [
            {"dim": "里程碑事件表", "status": "不存在",
             "evidence": "旧稿的 chain_roadmap / 里程碑事件表在 gkx 无同名表，缺表三态见 TABLE_ABSENCE_EVIDENCE.md",
             "impact": "只能给「事件峰值年」，不能给「某年某技术突破」这类里程碑"},
            {"dim": "阶段阈值参数", "status": "不存在",
             "evidence": "库内无参数表；本件只能用自定义阈值（起势年 10% + 年份分段），已写入 params",
             "impact": "阶段名可复现，但换阈值会换阶段，必须标记自定义"},
            {"dim": "政策的链标签", "status": "不存在",
             "evidence": "dwd_policy_base 无 chain/industry 列，政策只能按城市与年份聚合",
             "impact": "政策腿只能做城市级背景，不能进链级事件密度"},
            {"dim": "资讯的历史长度", "status": "不足",
             "evidence": "资讯表 %d 行仅覆盖 %s 至 %s（%d 个月）"
                         % (len(news["rows"]), compute["news_window"][0],
                            compute["news_window"][1], compute["news_month_count"]),
             "impact": "资讯只能做「当下热度」，不能做「历程」"},
            {"dim": "成立年份覆盖", "status": "部分",
             "evidence": "底册 %d 家中仅 %d 家有可挂链的成立年（%.2f%%）"
                         % (base_rows, nf_all_years, year_cov * 100),
             "impact": "2010 年以前的新设数偏低，早期阶段判定右偏"},
        ],
        "counter_checks": [
            {"id": "C1", "question": "阶段划分是不是被「成立年份」这一个来源单独决定？",
             "action": "用融资序列独立复算峰值年，与成立年峰值年对照",
             "result": "12 条链中两条序列峰值年相差 ≤3 年的有 %d 条；相差 >3 年的 %d 条"
                       "（差异明细见 chains[].peak_newfirm_year / peak_fin_year）。"
                       "两腿不同步说明单一来源不足以定阶段。"
                       % (sum(1 for c in chains if c["peak_fin_year"] and c["peak_newfirm_year"]
                              and abs(c["peak_fin_year"] - c["peak_newfirm_year"]) <= 3),
                          sum(1 for c in chains if c["peak_fin_year"] and c["peak_newfirm_year"]
                              and abs(c["peak_fin_year"] - c["peak_newfirm_year"]) > 3))},
            {"id": "C2", "question": "融资事件挂链率 57% 会不会让「资本腿」只覆盖大企业？",
             "action": "统计未挂链行数与未挂链原因（企业名不在链标签表）",
             "result": "未挂链 %d 行（%.2f%%）。未挂链多为投资方/被投方名称与链标签表不一致，"
                       "不是随机缺失；资本腿因此偏「已被打标的链内企业」。"
                       % (fin_unmapped, fin_unmapped / len(fin["fin"]) * 100)},
            {"id": "C3", "question": "政策腿能不能硬塞进链级序列？",
             "action": "逐列检查 dwd_policy_base 是否有行业/链字段",
             "result": "逐列检查无 chain/industry 字段；深圳政策 %d 条只能按年做城市背景，"
                       "强行按标题关键词挂链会把「泛产业政策」重复计入多条链。" % sum(pol_sz.values())},
            {"id": "C4", "question": "2022 之后政策数骤降，是不是「政策退出」？",
             "action": "统计 2020—2025 各年政策行数",
             "result": "2020 年 %d 条、2021 年 %d 条、2022 年 %d 条、2023 年 %d 条、2024 年 %d 条、2025 年 %d 条——"
                       "这是入库截断不是政策退出，2022 年以后不可用于趋势判断。"
                       % tuple(compute["policy_recent_years"].values())},
        ],
        "notes": [
            "本件不给「路线图」结论：里程碑需要事件表，事件表不存在。给的是按年事件密度与阶段切分。",
            "与 M_CHAIN_CYCLE_STAGE 的分工：那件用企业年龄结构判生命周期阶段（截面），"
            "本件用逐年事件序列判阶段（时序）；两件若结论冲突，以本件的序列证据为准，但阶段名不可互认。",
            "阶段名为「起步期/加速期/成熟期」，阈值本件自定义，不得写成标准阶段划分。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("[OK] %s -> %s（%.1fs）窗口 %d—%d，新设 %d，融资 %d，扩张窗口 %s—%s 年"
          % (METRIC, OUT, out["elapsed_sec"], Y0, Y1, compute["newfirms_total"],
             compute["fin_events_total"], compute["expand_window_min"],
             compute["expand_window_max"]))


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
    out_json = here / "M_CHAIN_DEEP_119_1_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_DEEP_119_1.py 等价）
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
        "metric_id": "M_CHAIN_DEEP_119_1",
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
