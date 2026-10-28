#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务机构培育推荐模型（M_SVC_DEEP_181_1）—— gkx 口径，自包含。

王惠口径四维（公式照抄旧稿，数据源全部换为 gkx 快照）：
    D1 竞争力     = 研发投入强度 + 研发人员占比 —— 年报无研发两列（实测 0 行非空），
                    以专利产出 + 发明占比作产出侧代理（与 180 同法）
    D2 产业相关度 = 产业契合度（深圳 20+8 标签 ∩ 目标词表）/ |目标词表|
    D3 政策匹配度 = 机构产业词对应的政策供给强度
    D4 发展潜力   = 营业收入 CAGR + 净利润 CAGR（近两年可比年，开方折年）

合成：各维在深圳池内 min-max（内联复制自 M_SVC_DEEP_177_1.py 的 mm），
缺维不补 0、不进平均，等权 ×100；缺两维以上不入排序。
梯度映射照旧稿：潜力高+竞争力低 → 规做精；两维均高 → 优上市；营收低但增速高 → 小升规。

数据源：
    code/_snapshots21/svc21_facts_20261022.json    （pool/base_fields/finance）
    code/_snapshots21/svc21_pt_axis_20261022.json  （pool_tags）
    code/_snapshots21/star_applicant_agg_gkx.json  （专利名称聚合）
    code/_snapshots21/policy_base_20261021.json    （政策标题）
产出：code/M_SVC_DEEP_181_1_out.json
运行：cd code && python3 M_SVC_DEEP_181_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
PTAXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
AGG = os.path.join(SNAP, "star_applicant_agg_gkx.json")
POLICY = os.path.join(SNAP, "policy_base_20261021.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_181_1_out.json")

SZ = "深圳市"
TARGET = ["软件与信息服务", "智能终端", "人工智能", "具身智能", "机器人", "集成电路",
          "数字创意", "传感器", "合成生物", "智能网联汽车", "生物医药", "低空经济"]
POL_KW = {"软件与信息服务": ["软件"], "智能终端": ["智能终端", "终端"], "人工智能": ["人工智能"],
          "具身智能": ["具身智能"], "机器人": ["机器人"], "集成电路": ["集成电路", "芯片"],
          "数字创意": ["数字创意", "文化创意"], "传感器": ["传感器"], "合成生物": ["合成生物"],
          "智能网联汽车": ["智能网联", "新能源汽车"], "生物医药": ["生物医药", "医药"],
          "低空经济": ["低空"]}


def mm(vals: dict) -> dict:
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k, v in vals.items() if v is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def band(x):
    if x >= 70:
        return "优先培育"
    if x >= 55:
        return "重点培育"
    if x >= 40:
        return "观察"
    return "暂缓"


def cagr(series):
    """series: [(year, value)]，取最近两个正值年，开 (t2-t1) 次方折年"""
    pts = [(y, v) for y, v in series if v is not None and v > 0]
    if len(pts) < 2:
        return None, None
    pts.sort()
    (y1, v1), (y2, v2) = pts[-2], pts[-1]
    dt = y2 - y1
    if dt <= 0:
        return None, None
    g = (v2 / v1) ** (1.0 / dt) - 1.0
    return max(-0.95, min(3.0, g)), dt


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, fin = f["pool"], f["finance"]
    pt = json.load(open(PTAXIS, encoding="utf-8"))
    pool_tags = pt["pool_tags"]
    agg = json.load(open(AGG, encoding="utf-8"))["agg"]
    pol = json.load(open(POLICY, encoding="utf-8"))

    sz = [o for o, v in pool.items() if v.get("city") == SZ]
    N = len(sz)
    sz_set = set(sz)

    pol_cnt, pol_sz = Counter(), Counter()
    for r in pol:
        t = r.get("title") or ""
        for ind, kws in POL_KW.items():
            if any(k in t for k in kws):
                pol_cnt[ind] += 1
                if (r.get("city") == SZ) or ("深圳" in t):
                    pol_sz[ind] += 1
    pol_max = max(pol_cnt.values()) if pol_cnt else 1

    # ---- D1 竞争力：专利产出 + 发明占比 ------------------------------------
    pat, inv_share, comp = {}, {}, {}
    for o in sz:
        v = agg.get(pool[o]["name"])
        if v and v[0]:
            pat[o] = int(v[0])
            inv_share[o] = v[1] / v[0]
    pn, isn = mm(pat), mm(inv_share)
    for o in pat:
        comp[o] = 0.6 * pn[o] + 0.4 * isn[o]

    # ---- D2 产业相关度 ------------------------------------------------------
    fit = {}
    for o in sz:
        tg = set(pool_tags.get(o) or [])
        if tg:
            fit[o] = len(tg & set(TARGET)) / len(TARGET)

    # ---- D3 政策匹配度 ------------------------------------------------------
    pols = {}
    for o in sz:
        tg = set(pool_tags.get(o) or [])
        if tg:
            pols[o] = sum(pol_cnt.get(t, 0) for t in tg) / (len(tg) * pol_max)

    # ---- D4 发展潜力：营收 CAGR + 净利 CAGR --------------------------------
    rev_g, np_g, pot = {}, {}, {}
    for o in sz:
        rows = fin.get(o) or {}
        rg, _ = cagr([(int(y), (row or {}).get("rev")) for y, row in rows.items()])
        ng, _ = cagr([(int(y), (row or {}).get("np")) for y, row in rows.items()])
        if rg is not None:
            rev_g[o] = rg
        if ng is not None:
            np_g[o] = ng
    rgn, ngn = mm(rev_g), mm(np_g)
    for o in set(rgn) | set(ngn):
        parts = [d[o] for d in (rgn, ngn) if o in d]
        pot[o] = sum(parts) / len(parts)

    # ---- 合成 --------------------------------------------------------------
    dims = {"competitiveness": mm(comp), "industry_fit": mm(fit),
            "policy_match": mm(pols), "potential": mm(pot)}
    score, detail = {}, {}
    for o in sz:
        parts = {k: v[o] for k, v in dims.items() if o in v}
        if len(parts) < 2:
            continue
        score[o] = round(sum(parts.values()) / len(parts) * 100.0, 2)
        detail[o] = parts

    ranked = sorted(score.items(), key=lambda x: -x[1])
    vals = sorted(score.values())

    def q(p):
        if not vals:
            return None
        i = min(len(vals) - 1, max(0, int(round(p * (len(vals) - 1)))))
        return round(vals[i], 2)

    def advice(o):
        d = detail[o]
        c, p = d.get("competitiveness"), d.get("potential")
        rev = None
        rows = fin.get(o) or {}
        ys = sorted([(int(y), (row or {}).get("rev")) for y, row in rows.items()
                     if (row or {}).get("rev")], key=lambda x: x[0])
        if ys:
            rev = ys[-1][1]
        if c is not None and p is not None:
            if c >= 0.6 and p >= 0.6:
                return "优上市（竞争力与成长性双高，对接上市培育服务）"
            if p >= 0.6 and c < 0.4:
                return "规做精（成长快但技术力弱，给技术升级与研发补贴）"
        if p is not None and p >= 0.6 and (rev is not None and rev < 5000):
            return "小升规（规模小但增速高，给升规纳统与场景资源）"
        if c is not None and c >= 0.6:
            return "稳存量（技术力强、成长性一般，给市场拓展对接）"
        return "常规跟踪（分维证据不足，仅建档监测）"

    top = []
    for i, (o, s) in enumerate(ranked[:15]):
        top.append({"rank": i + 1, "org_id": o, "name": pool[o]["name"], "score": s, "band": band(s),
                    "type": pool[o].get("ptype2"), "patents": pat.get(o),
                    "tags": pool_tags.get(o),
                    "rev_cagr": round(rev_g[o], 4) if o in rev_g else None,
                    "np_cagr": round(np_g[o], 4) if o in np_g else None,
                    "advice": advice(o),
                    "dim_scores": {k: round(v, 4) for k, v in detail[o].items()}})

    bands = {"优先培育": 0, "重点培育": 0, "观察": 0, "暂缓": 0}
    for s in vals:
        bands[band(s)] += 1

    rev_orgs = len([o for o in sz if any((r or {}).get("rev") for r in (fin.get(o) or {}).values())])
    reason = ("四维在深圳池 %d 家上均可实测：竞争力（专利 %d 家）、产业相关度（20+8 标签 %d 家）、"
              "政策匹配（政策标题关键词）、发展潜力（营收 CAGR %d 家 / 净利 CAGR %d 家）；"
              "两处结构性缺口——年报研发两列空挂使竞争力只能产出侧代理；财务覆盖仅 %d/%d 家（%.2f%%），"
              "发展潜力维只在有两年正值序列的子群体成立。判部分支持。" %
              (N, len(pat), len(fit), len(rev_g), len(np_g), rev_orgs, N, rev_orgs / N * 100))

    out = {
        "metric_id": "M_SVC_DEEP_181_1",
        "metric_name": "服务机构培育推荐模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "main_gap": ("财务覆盖薄（营收 %d 家 / 深圳池 %d 家），发展潜力维只在小子群成立；"
                     "研发投入与研发人员字段空挂；政策维缺 svc_org_policy_hit 命中表" % (rev_orgs, N)),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info + dwd_org_base_info(city)",
             "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_annual_financial_info", "rows": f["finance_meta"]["rows_total"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_industry_product_tags（20+8）",
             "rows": pt["pool_tags_meta"]["rows_matched"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_patent（首申请人聚合）",
             "rows": 2939895, "snapshot": "code/_snapshots21/star_applicant_agg_gkx.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_policy_base",
             "rows": len(pol), "snapshot": "code/_snapshots21/policy_base_20261021.json"},
        ],
        "base_years_used": list(range(2007, 2026)),
        "base_years_missing": [2026],
        "base_years_note": ("财务年表覆盖 2007—2025 共 19 年（used 记整段，missing 记 2026：库里无 2026 财务行）；"
                            "增长率用机构自身最近两个正值年做 CAGR，不把缺年按 0 摊入，也不跨机构拉平。"),
        "population": {"sz_n": N, "pool_total": len(pool)},
        "dimension_cover": {
            "D1_competitiveness": {"available": True, "proxy": "patents + invention_share", "orgs": len(comp)},
            "D2_industry_fit": {"available": True, "orgs": len(fit), "target_lexicon": TARGET},
            "D3_policy_match": {"available": True, "orgs": len(pols)},
            "D4_potential": {"available": True, "rev_cagr_orgs": len(rev_g), "np_cagr_orgs": len(np_g),
                             "rev_orgs_any": rev_orgs,
                             "note": "两年正值序列才计 CAGR；负利润年不计净利增速"},
        },
        "policy_supply": {"by_industry_all": dict(pol_cnt), "by_industry_sz": dict(pol_sz)},
        "composite": {"dims": ["competitiveness", "industry_fit", "policy_match", "potential"],
                      "weights": "等权 1/4", "scored_orgs": len(score),
                      "unscored_orgs": N - len(score), "rule": "维数 <2 不入排序；缺维不补 0"},
        "score_dist": {"n": len(vals), "mean": round(statistics.mean(vals), 2) if vals else None,
                       "median": round(statistics.median(vals), 2) if vals else None,
                       "p90": q(0.90), "p99": q(0.99),
                       "max": round(vals[-1], 2) if vals else None,
                       "min": round(vals[0], 2) if vals else None, "bands": bands},
        "top15": top,
        "growth_facts": {
            "rev_cagr_median": round(statistics.median(rev_g.values()), 4) if rev_g else None,
            "np_cagr_median": round(statistics.median(np_g.values()), 4) if np_g else None,
            "rev_cagr_positive_pct": round(sum(1 for v in rev_g.values() if v > 0) / len(rev_g) * 100, 2) if rev_g else None,
            "np_cagr_positive_pct": round(sum(1 for v in np_g.values() if v > 0) / len(np_g) * 100, 2) if np_g else None,
        },
        "advice_mix": dict(Counter(t["advice"].split("（")[0] for t in top)),
        "caliber_note": ("梯度建议只按分维相对位给出，不含政策资格硬门槛（如规上/高企认定）；"
                         "正式化须叠加认定状态过滤，本件不做资格判断"),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("深圳池=%d 有分=%d 专利=%d 标签=%d 营收CAGR=%d 净利CAGR=%d" %
          (N, len(score), len(pat), len(fit), len(rev_g), len(np_g)))
    print("dist", out["score_dist"])
    print("top3", [(t["name"], t["score"], t["rev_cagr"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
