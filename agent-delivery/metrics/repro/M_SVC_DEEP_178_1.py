#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""咨询服务机构技术力评价模型（M_SVC_DEEP_178_1）—— gkx 口径，自包含。

王惠口径四维（公式照抄旧稿，数据源全部换为 gkx 快照）：
    D1 人才密度   = 研发人员数 / 从业人员数        —— gkx 年报表**无研发人员列**，本件记无源
    D2 行业经验   = 成立年限 + 覆盖产业/技术领域数  —— 主档 inc_year 全量 + 深圳 20+8 产业标签
    D3 成功案例   = 可验证成功案例数               —— 无正式源，资讯条数弱代理（不进正式合成）
    D4 行业声誉   = 荣誉/技术标签 + 资讯声量 − 风险事件 —— 双信号加负向扣减

合成：各维在 CONSULT 池内 min-max（内联复制自 M_SVC_DEEP_177_1.py 的 mm 函数），
      缺维不补 0、不进平均，等权 ×100。

数据源：
    code/_snapshots21/svc21_facts_20261022.json   （pool/finance/tags/news/risk）
    code/_snapshots21/svc21_pt_axis_20261022.json （pool_tags：深圳 20+8 产业标签）
产出：code/M_SVC_DEEP_178_1_out.json
运行：cd code && python3 M_SVC_DEEP_178_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
PTAXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_178_1_out.json")

STAT_YEAR = 2026


def mm(vals: dict) -> dict:
    """min-max（内联复制自 M_SVC_DEEP_177_1.py，不 import 共享模块）"""
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k, v in vals.items() if v is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def band(x):
    if x >= 70:
        return "领先"
    if x >= 55:
        return "稳健"
    if x >= 40:
        return "关注"
    return "薄弱"


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, fin = f["pool"], f["finance"]
    tags, news, risk = f["tags"], f["news"], f["risk"]
    pt = json.load(open(PTAXIS, encoding="utf-8"))
    pool_tags = pt["pool_tags"]

    cons = [o for o, v in pool.items() if v.get("ptype2") == "CONSULT"]
    N = len(cons)

    # ---- D1 人才密度：无研发人员列，只报可观测的从业人员覆盖 ---------------
    emp_orgs = [o for o in cons if any((r or {}).get("emp") for r in (fin.get(o) or {}).values())]
    rd_field_orgs = 0  # gkx.dwd_org_annual_financial_info 全表无研发人员列，实测恒 0

    # ---- D2 行业经验：年限 + 覆盖产业/技术领域数 ---------------------------
    years, breadth = {}, {}
    for o in cons:
        y = pool[o].get("inc_year")
        if y:
            years[o] = max(0, STAT_YEAR - int(y))
        tg = pool_tags.get(o) or []
        if tg:
            breadth[o] = len(set(tg))

    # ---- D3 成功案例：资讯条数弱代理 ---------------------------------------
    case = {o: news[o] for o in cons if o in news}

    # ---- D4 行业声誉：标签 + 声量 − 风险 ----------------------------------
    rep_raw = {}
    for o in cons:
        tag_n = tags.get(o, 0) or 0
        news_n = news.get(o, 0) or 0
        r = risk.get(o) or {}
        risk_n = sum(v for v in r.values() if isinstance(v, (int, float)))
        if tag_n or news_n or risk_n:
            rep_raw[o] = tag_n * 1.0 + min(news_n, 50) * 0.2 - risk_n * 3.0

    # ---- 合成 --------------------------------------------------------------
    dims = {
        "exp_years": mm(years),
        "ind_breadth": mm(breadth),
        "reputation": mm(rep_raw),
    }
    score, detail = {}, {}
    for o in cons:
        parts = {k: v[o] for k, v in dims.items() if o in v}
        if len(parts) < 2:
            continue
        s = sum(parts.values()) / len(parts) * 100.0
        score[o] = round(s, 2)
        detail[o] = parts

    ranked = sorted(score.items(), key=lambda x: -x[1])
    vals = sorted(score.values())

    def q(p):
        if not vals:
            return None
        i = min(len(vals) - 1, max(0, int(round(p * (len(vals) - 1)))))
        return round(vals[i], 2)

    top = []
    for i, (o, s) in enumerate(ranked[:10]):
        d = detail[o]
        top.append({
            "rank": i + 1, "org_id": o, "name": pool[o]["name"],
            "city": pool[o].get("city"), "score": s, "band": band(s),
            "exp_years": years.get(o), "ind_breadth": breadth.get(o),
            "tags": tags.get(o, 0), "news": news.get(o, 0),
            "dims_used": sorted(d), "dim_scores": {k: round(v, 4) for k, v in d.items()},
        })

    bands = {"领先": 0, "稳健": 0, "关注": 0, "薄弱": 0}
    for s in vals:
        bands[band(s)] += 1

    # ---- 池纯度诊断 ---------------------------------------------------------
    # ptype2 规则为「INNOV > IP > FINANCE > HR > MKT > CONSULT，多命中取首个」→ CONSULT 是兜底类，
    # 只要 main_activities 命中「咨询」而没命中前五类就落进来，于是 15% 的建筑/置业/贸易企业混入。
    import re
    noise_pat = re.compile("建筑|工程|建设|置业|房地产|装饰|珠宝|首饰|汽车城|贸易")
    noisy = [o for o in cons if noise_pat.search(pool[o]["name"])]
    clean = set(cons) - set(noisy)
    strict_top = [r for r in ranked if r[0] in clean][:10]
    name_pat = re.compile("咨询|顾问|智库|策划|评估|认证|检测|设计院|研究院|事务所")
    named = [o for o in cons if name_pat.search(pool[o]["name"])]
    named_top = [r for r in ranked if r[0] in set(named)][:5]
    purity = {
        "noise_rule": "名称含 建筑/工程/建设/置业/房地产/装饰/珠宝/首饰/汽车城/贸易 视为疑似误分",
        "noise_orgs": len(noisy), "noise_pct": round(len(noisy) / N * 100, 2),
        "clean_orgs": len(clean),
        "noise_score_mean": round(statistics.mean([score[o] for o in noisy if o in score]), 2)
        if [o for o in noisy if o in score] else None,
        "clean_score_mean": round(statistics.mean([score[o] for o in clean if o in score]), 2)
        if [o for o in clean if o in score] else None,
        "consult_name_orgs": len(named),
        "consult_name_pct": round(len(named) / N * 100, 2),
        "consult_name_top5": [{"name": pool[o]["name"], "score": s_, "exp_years": years.get(o),
                               "ind_breadth": breadth.get(o)} for o, s_ in named_top],
        "note": "CONSULT 是 ptype2 兜底类（INNOV>IP>FINANCE>HR>MKT>CONSULT 取首个命中），"
                "工程/造价咨询类建筑企业会落入本池；全池分照算以保口径，另给剔除后的严格子池榜单",
    }
    strict_rank = []
    for i, (o, s) in enumerate(strict_top):
        d = detail[o]
        strict_rank.append({"rank": i + 1, "org_id": o, "name": pool[o]["name"],
                            "city": pool[o].get("city"), "score": s, "band": band(s),
                            "exp_years": years.get(o), "ind_breadth": breadth.get(o),
                            "tags": tags.get(o, 0), "news": news.get(o, 0),
                            "dim_scores": {k: round(v, 4) for k, v in d.items()}})

    # 覆盖矩阵（逐维）
    cover = {
        "D1_talent_density": {"available": False, "orgs": 0,
                              "note": "gkx 年报无研发人员列（rd_emp 字段不存在），研发人员占比无法构成；"
                                      "仅有从业人员 emp 覆盖 %d/%d 家，单有分母无分子，不强行代理" % (len(emp_orgs), N)},
        "D2_experience": {"available": True, "orgs_years": len(years), "orgs_breadth": len(breadth),
                          "note": "年限侧随主档全量可取；覆盖领域侧用深圳 20+8 产业标签（gkx 产业标签表），"
                                  "非国民经济行业代码，语义为「技术领域覆盖」"},
        "D3_cases": {"available": False, "orgs": len(case),
                     "note": "无 svc_success_case_count；资讯条数只作观察变量，不进正式合成"},
        "D4_reputation": {"available": True, "orgs": len(rep_raw),
                          "note": "技术标签数 + 资讯声量（截顶 50）+ 风险事件负向扣减，三项同池 min-max 前合成"},
    }

    reason = ("四维中 D2（年限全量 + 产业标签覆盖 %d 家）、D4（标签 %d 家 + 资讯 %d 家 + 风险 %d 家）"
              "两维在 gkx 可实测复现，D3 仅有资讯弱代理；但 D1 人才密度维结构性缺分子——"
              "gkx 年报表无研发人员列（全表实测 0 行非空），从业人员 emp 虽有 %d 家也构不成占比，"
              "而人才密度是本模型的第一维、官方标准里权重最高的一维，缺它不能算「完全转换支持」，"
              "故判部分支持。" % (len(breadth), len(tags), len(news), len(risk), len(emp_orgs)))

    out = {
        "metric_id": "M_SVC_DEEP_178_1",
        "metric_name": "咨询服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "main_gap": "D1 人才密度缺研发人员分子（无字段）；D3 成功案例无正式源（仅资讯代理）",
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info(main_activities) + dwd_org_base_info",
             "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info", "rows": f["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_industry_product_tags（20+8 产业标签）",
             "rows": pt["pool_tags_meta"]["rows_matched"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_tech_tag / dwd_org_news / dwd_org_risk_info",
             "rows": {"tags_orgs": f["tags_meta"]["orgs_in_pool"], "news_orgs": f["news_meta"]["orgs_in_pool"],
                      "risk_orgs": f["risk_meta"]["orgs_in_pool"]},
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("统计年取 2026（快照时点）；成立年限 = 2026 − inc_year，inc_year 覆盖 44,132/44,153。"
                            "财务年表覆盖 2007—2025，本件只用其 emp 覆盖做可行性判定、不入合成，故不进基期。"),
        "population": {"type": "CONSULT", "n": N, "pool_total": len(pool)},
        "dimension_cover": cover,
        "composite": {"dims": ["exp_years", "ind_breadth", "reputation"], "weights": "等权 1/3",
                      "scored_orgs": len(score), "unscored_orgs": N - len(score),
                      "rule": "维数 <2 的机构不入排序（缺维不补 0，也不进平均）"},
        "score_dist": {"n": len(vals), "mean": round(statistics.mean(vals), 2) if vals else None,
                       "median": round(statistics.median(vals), 2) if vals else None,
                       "p90": q(0.90), "p99": q(0.99),
                       "max": round(vals[-1], 2) if vals else None,
                       "min": round(vals[0], 2) if vals else None,
                       "bands": bands},
        "top10": top,
        "pool_purity": purity,
        "strict_top10": strict_rank,
        "caliber_note": ("D4 的风险扣减（×3）与资讯截顶（50 条）是演示参数，正式化须由甲方确认；"
                         "D3 未进合成，故本指数实际是「经验 + 声誉」二维，不可对外称四维合成"),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("CONSULT=%d 有分=%d 年限=%d 领域=%d 声誉=%d" % (N, len(score), len(years), len(breadth), len(rep_raw)))
    print("dist", out["score_dist"])
    print("purity", purity["noise_orgs"], purity["noise_pct"], "clean mean", purity["clean_score_mean"])
    print("top3", [(t["name"], t["score"], t["exp_years"], t["ind_breadth"]) for t in top[:3]])
    print("strict3", [(t["name"], t["score"], t["exp_years"]) for t in strict_rank[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
