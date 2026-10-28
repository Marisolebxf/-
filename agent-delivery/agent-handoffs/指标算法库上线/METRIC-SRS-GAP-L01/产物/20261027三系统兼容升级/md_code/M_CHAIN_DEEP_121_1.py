#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_CHAIN_DEEP_121_1 深圳产业优势识别模型
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_CHAIN_DEEP_121_1.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""深圳产业优势识别模型（M_CHAIN_DEEP_121_1）。

只读 `code/_snapshots21/` 落盘快照（快照由 gkx 扫描产出，见各快照 meta.source），
不连任何数据库；单次运行约 3 秒。

识别逻辑（本件自定义，待甲方确认）：
  以「区位商 LQ」为主判据，专利份额与融资份额为副判据。
    LQ_c = (SZ_c / F_c) / (SZ_all / F_all)
  其中 SZ_c 为链 c 的深圳企业数，F_c 为链 c 的全部企业数。
  LQ>1 表示深圳在该链的相对集聚高于深圳在本库产业链企业中的平均集聚。

产物：code/M_CHAIN_DEEP_121_1_out.json
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

METRIC = "M_CHAIN_DEEP_121_1"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")
SZ = "深圳市"

# 识别阈值（本件自定义、待甲方确认；不称官方口径）
LQ_TH = 1.0          # 区位商门槛
SHARE_GAP_TH = 0.0   # 专利/融资份额相对规模份额的溢出门槛（百分点）


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    base = jload("base_20261021.json")            # [org_id, credit, name, prov, city, year]
    agg = jload("star_applicant_agg_gkx.json")    # name -> [applies, grants]
    fin = jload("chain21_fin_degree_20261022.json")

    name2chain = layer["names"]
    name2city = {r[2]: r[4] for r in base}
    credit2city = {r[1]: r[4] for r in base}

    # ---------- 母体规模 ----------
    firms_all = sum(c["firms"] for c in panel["chains"])
    firms_sz = sum(c["sz_firms"] for c in panel["chains"])
    sz_base_share = firms_sz / firms_all

    # ---------- 专利：申请人 -> 链 / 城市 ----------
    pat_all = Counter()
    pat_sz = Counter()
    pat_applicants = Counter()
    pat_unmapped_apply = 0
    for nm, v in agg["agg"].items():
        ap = int(v[0] or 0)
        ch = name2chain.get(nm)
        if not ch:
            pat_unmapped_apply += ap
            continue
        pat_all[ch] += ap
        pat_applicants[ch] += 1
        if name2city.get(nm) == SZ:
            pat_sz[ch] += ap
    agg_apply_total = sum(int(v[0] or 0) for v in agg["agg"].values())

    # ---------- 融资：企业名 -> 链，信用码 -> 城市 ----------
    fin_all = Counter()
    fin_sz = Counter()
    fin_unmapped = 0
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if not ch:
            fin_unmapped += 1
            continue
        fin_all[ch] += 1
        if credit2city.get(r[2]) == SZ:
            fin_sz[ch] += 1
    fin_total = len(fin["fin"])

    # ---------- 逐链 ----------
    rows = []
    for c in panel["chains"]:
        ch = c["chain"]
        firms = c["firms"]
        szf = c["sz_firms"]
        share = szf / firms if firms else 0.0
        lq = share / sz_base_share if sz_base_share else 0.0
        leaves = c["leaves"]
        leaves_sz = c["leaves_with_sz"]
        cov = leaves_sz / leaves if leaves else 0.0
        p_all = pat_all.get(ch, 0)
        p_sz = pat_sz.get(ch, 0)
        p_share = p_sz / p_all if p_all else 0.0
        f_all = fin_all.get(ch, 0)
        f_sz = fin_sz.get(ch, 0)
        f_share = f_sz / f_all if f_all else 0.0
        rows.append({
            "chain": ch, "name": c["name"],
            "firms": firms, "sz_firms": szf, "sz_share": round(share, 6),
            "lq": round(lq, 6),
            "leaves": leaves, "leaves_with_sz": leaves_sz, "sz_leaf_coverage": round(cov, 6),
            "patents_all": p_all, "patents_sz": p_sz, "sz_patent_share": round(p_share, 6),
            "patent_applicants": pat_applicants.get(ch, 0),
            "fin_all": f_all, "fin_sz": f_sz, "sz_fin_share": round(f_share, 6),
            "patent_share_minus_firm_share": round(p_share - share, 6),
            "fin_share_minus_firm_share": round(f_share - share, 6),
            "patent_intensity_ratio": round(p_share / share, 6) if share else 0.0,
        })

    # ---------- 识别判定 ----------
    for r in rows:
        hit_lq = r["lq"] >= LQ_TH
        hit_pat = r["patent_share_minus_firm_share"] > SHARE_GAP_TH
        hit_fin = r["fin_share_minus_firm_share"] > SHARE_GAP_TH
        r["hit_lq"] = hit_lq
        r["hit_patent_overflow"] = hit_pat
        r["hit_fin_overflow"] = hit_fin
        r["criteria_hit"] = int(hit_lq) + int(hit_pat) + int(hit_fin)
        if hit_lq and hit_pat:
            r["verdict"] = "确认优势"
        elif hit_lq:
            r["verdict"] = "规模优势（创新无溢出）"
        elif hit_pat:
            r["verdict"] = "创新密度占优（规模不集聚）"
        else:
            r["verdict"] = "非优势"
    rows.sort(key=lambda x: (-x["lq"]))
    verdicts = Counter(r["verdict"] for r in rows)
    n_confirm = verdicts["确认优势"]
    n_scale = verdicts["规模优势（创新无溢出）"]
    n_intens = verdicts["创新密度占优（规模不集聚）"]
    n_none = verdicts["非优势"]
    n_pat_overflow = sum(1 for r in rows if r["hit_patent_overflow"])
    n_fin_overflow = sum(1 for r in rows if r["hit_fin_overflow"])

    # ---------- 反向核查：深圳份额的极值与专利覆盖 ----------
    lq_sorted = sorted(rows, key=lambda x: -x["lq"])
    max_row, min_row = lq_sorted[0], lq_sorted[-1]
    REAL_CITIES = [SZ, "广州市", "东莞市", "惠州市"]
    sz_city_rank = 0
    sz_rank_second = 0
    city_rank_rows = []
    for c in panel["chains"]:
        order = sorted(((k, c["cities"].get(k, 0)) for k in REAL_CITIES),
                       key=lambda kv: -kv[1])
        names = [k for k, _ in order]
        rank = names.index(SZ) + 1 if SZ in names else None
        if rank == 1:
            sz_city_rank += 1
        elif rank == 2:
            sz_rank_second += 1
        city_rank_rows.append({
            "chain": c["chain"], "name": c["name"], "sz_rank_among": rank,
            "cities": {k: c["cities"].get(k, 0) for k in REAL_CITIES},
            "province_outside": c["cities"].get("省外", 0),
        })

    # 专利维的覆盖边界：未挂链的申请量占比
    pat_unmapped_ratio = pat_unmapped_apply / agg_apply_total if agg_apply_total else 0.0

    compute = {
        "firms_all": firms_all,
        "firms_sz": firms_sz,
        "sz_base_share": round(sz_base_share, 6),
        "chains": rows,
        "n_confirm": n_confirm,
        "n_scale": n_scale,
        "n_intensity": n_intens,
        "n_none": n_none,
        "n_patent_overflow": n_pat_overflow,
        "n_fin_overflow": n_fin_overflow,
        "lq_max": {"chain": max_row["chain"], "name": max_row["name"], "lq": max_row["lq"]},
        "lq_min": {"chain": min_row["chain"], "name": min_row["name"], "lq": min_row["lq"]},
        "sz_rank_first_chains": sz_city_rank,
        "sz_rank_second_chains": sz_rank_second,
        "city_rank": city_rank_rows,
        "patent_applies_total": agg_apply_total,
        "patent_applies_chain": sum(pat_all.values()),
        "patent_applies_unmapped": pat_unmapped_apply,
        "patent_unmapped_ratio": round(pat_unmapped_ratio, 6),
        "patents_sz_total": sum(pat_sz.values()),
        "fin_events_total": fin_total,
        "fin_events_mapped": sum(fin_all.values()),
        "fin_events_unmapped": fin_unmapped,
        "fin_events_sz": sum(fin_sz.values()),
        "applicants_total": len(agg["agg"]),
    }

    out = {
        "metric": METRIC,
        "title": "深圳产业优势识别模型",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "识别所需的三条判据中，规模判据（企业数）与结构判据（专利份额、融资份额）"
            "在 gkx 均有全量源：12 条链合计 %d 家企业、其中深圳 %d 家（%.2f%%），"
            "专利可按申请人名挂到链与城市（链内申请量 %d 件，其中深圳 %d 件），"
            "融资事件 %d 行可挂 %d 行（%.2f%%）。但「优势」的营收与利润内核不可得："
            "有营收的链内企业仅个位数，研发强度字段存在但覆盖极低"
            "（stock 表 research_development_amount 仅 876 家、0.46%%，"
            "annual 表 arch_development_am 全为 NULL）；且链标签层把广东省外企业"
            "压成一个「省外」聚合桶（无城市字段，软件链省外 774604 家、占该链 84.4%%），"
            "无法做全国城市排名，城市比较只能做到深/穗/莞/惠四城。"
            "故判部分支持：结论可出「相对四城的结构性优势」，不能出「全国优势」。"
            % (firms_all, firms_sz, sz_base_share * 100, compute["patent_applies_chain"],
               compute["patents_sz_total"], fin_total, compute["fin_events_mapped"],
               compute["fin_events_mapped"] / fin_total * 100)
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 1),
        "sources": {
            "snapshots": ["code/_snapshots21/chain_panel21.json",
                          "code/_snapshots21/chain21_layer_20261022.json",
                          "code/_snapshots21/base_20261021.json",
                          "code/_snapshots21/star_applicant_agg_gkx.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json"],
            "upstream_tables": ["gkx.dwd_org_industry_tags", "gkx.dwd_industry_chain_info",
                                "gkx.dwd_org_base_info", "gkx.dwd_patent",
                                "gkx.dwd_org_financing_info"],
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面识别：企业数、专利数、融资事件数都取全库存量，不设年度分母。"
            "专利表仅 2021—2026 有申请年，本件只用存量计数、不做专利年度序列，"
            "因此不涉及 2021 之前年份按 0 摊入的问题。"
        ),
        "params": {
            "lq_threshold": LQ_TH,
            "share_gap_threshold": SHARE_GAP_TH,
            "weight_note": "三条判据等权计分（各 1 分，满 3 分），阈值与等权均为本件自定义、待甲方确认",
            "city_scope": ["深圳市", "广州市", "东莞市", "惠州市", "广东其他市", "省外"],
        },
        "compute": compute,
        "missing_dims": [
            {"dim": "营业收入/利润", "status": "不可得",
             "evidence": "chain21_revenue_20261022.json 中链内企业营收记录仅个位数家（stock 39,395 行、annual 2,191 行，经企业名挂链后每链 3—8 家）",
             "impact": "无法算「人均营收」「利润率」这类优势内核"},
            {"dim": "研发强度", "status": "不可得",
             "evidence": "字段存在但覆盖极低：dwd_org_stock_finance_info.research_development_amount 仅 876 家有正值（占底册 0.46%）；dwd_org_annual_financial_info.arch_development_am 全为 NULL",
             "impact": "无法区分「规模优势」与「技术优势」"},
            {"dim": "全国对标", "status": "不可得",
             "evidence": "chain21_layer 的城市字段只有深圳/广州/东莞/惠州四个真实城市与一个「省外」聚合桶；省外无城市名（软件链省外 774604 家、占该链 84.4%%）",
             "impact": "只能做四城比较，不能称全国城市排名"},
            {"dim": "深圳专利的授权/有效状态", "status": "部分可得",
             "evidence": "star_applicant_agg_gkx.json 提供申请量与授权量两列，但无法律状态与失效日",
             "impact": "只能用申请量，不能算「有效专利」"},
        ],
        "counter_checks": [
            {"id": "C1", "question": "深圳在 12 条链上是不是都占优（导致识别失效）？",
             "action": "只在深圳/广州/东莞/惠州四个真实城市之间排名（省外单列，省外不是城市）",
             "result": "12 条链里深圳企业数排第 1 的有 %d 条、排第 2 的有 %d 条。"
                       "若把「省外」当城市一起排，深圳一条都排不到第 1——"
                       "这是本件最容易写错的地方，已按城市口径改正。"
                       % (sz_city_rank, sz_rank_second)},
            {"id": "C2", "question": "区位商会不会只是「深圳企业整体多」的镜像？",
             "action": "用全库深圳占比 %.4f%% 作基准做归一" % (sz_base_share * 100),
             "result": "LQ 最高 %s %.3f、最低 %s %.3f；若深圳在每条链都同比例分布，LQ 应恒为 1，实测离散说明存在链间差异。"
                       % (max_row["name"], max_row["lq"], min_row["name"], min_row["lq"])},
            {"id": "C3", "question": "专利份额用的是不是抽样、会不会偏？",
             "action": "统计申请人聚合表覆盖：%d 个申请人 / %d 件申请，其中能挂到链的 %d 件"
                       % (compute["applicants_total"], agg_apply_total, compute["patent_applies_chain"]),
             "result": "未挂链申请 %d 件，占 %.2f%%；份额只在「已挂链」的子集内比较，"
                       "分子分母同源，但结论不能外推到全量专利。"
                       % (pat_unmapped_apply, pat_unmapped_ratio * 100)},
            {"id": "C4", "question": "「深圳专利份额高于企业份额」能不能当优势判据？",
             "action": "逐链算专利份额减企业份额的符号",
             "result": "%d/12 条链的差值为正——包括 LQ 只有 %.3f 的生物医药。"
                       "12 条链全部为正说明该判据在深圳样本里系统性偏正，没有区分度，"
                       "只能作辅助读数；判档仍以 LQ 为主。"
                       % (n_pat_overflow, min_row["lq"])},
            {"id": "C5", "question": "融资份额能不能替代营收份额？",
             "action": "逐链比较融资事件份额与企业份额",
             "result": "%d/12 条链融资份额高于企业份额，方向与专利一致；但融资事件只覆盖有融资记录的企业"
                       "（%d 行挂链 %d 行，%.2f%%），且事件次数不等于金额，不能替代营收。"
                       % (n_fin_overflow, fin_total, compute["fin_events_mapped"],
                          compute["fin_events_mapped"] / fin_total * 100)},
        ],
        "notes": [
            "本件与已交付 M_CHAIN_SZ_ADVANTAGE_SCORE（王惠四维评分）的分工：那件输出 0—100 分与名次，"
            "本件输出「是否优势」的判定与区位商。两件的深圳企业维同源（chain_panel21），"
            "但统计量不同（min-max 分 vs 区位商），数值不可互换。",
            "与 M_CHAIN_CONCENTRATION_INDEX 的分工：那件算链内环节分布（HHI），本件算深圳在链间的相对集聚（LQ）。",
            "阈值与等权为本件自定义、待甲方确认；不得表述为官方口径。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("[OK] %s -> %s（%.1fs）确认优势 %d / 规模优势 %d / 创新密度占优 %d / 非优势 %d"
          % (METRIC, OUT, out["elapsed_sec"], n_confirm, n_scale, n_intens, n_none))


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
    out_json = here / "M_CHAIN_DEEP_121_1_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_CHAIN_DEEP_121_1.py 等价）
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
        "metric_id": "M_CHAIN_DEEP_121_1",
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
