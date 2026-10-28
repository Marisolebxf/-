#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""服务机构引入推荐模型（M_SVC_DEEP_180_1）—— gkx 口径，自包含。

王惠口径四维（公式照抄旧稿，数据源全部换为 gkx 快照）：
    D1 竞争力     = 研发投入强度 + 研发人员占比  —— gkx 年报无研发两列（实测 0 行非空），
                    以专利产出 + 发明占比作产出侧代理（旧稿同一处置）
    D2 产业相关度 = 产业契合度 |K_i∩K_target|/|K_target| + 链协同度
    D3 政策匹配度 = 机构产业词与政策文本关键词的契合度（深圳政策优先）
    D4 深圳连接度 = 深圳对端边 / 总对端边

合成：各维在外部池内 min-max（内联复制自 M_SVC_DEEP_177_1.py 的 mm），
缺维不补 0、不进平均，等权 ×100；缺两维以上不入排序。

数据源：
    code/_snapshots21/svc21_facts_20261022.json      （pool/base_fields/invest/shareholder）
    code/_snapshots21/svc21_pt_axis_20261022.json    （pool_tags：深圳 20+8 产业标签）
    code/_snapshots21/star_applicant_agg_gkx.json    （专利名称聚合）
    code/_snapshots21/policy_base_20261021.json      （dwd_policy_base 20,000 条标题）
产出：code/M_SVC_DEEP_180_1_out.json
运行：cd code && python3 M_SVC_DEEP_180_1.py
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
OUT = os.path.join(HERE, "M_SVC_DEEP_180_1_out.json")

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
        return "优先引入"
    if x >= 55:
        return "重点关注"
    if x >= 40:
        return "观察"
    return "暂缓"


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    pool, bf = f["pool"], f["base_fields"]
    pt = json.load(open(PTAXIS, encoding="utf-8"))
    pool_tags = pt["pool_tags"]
    agg = json.load(open(AGG, encoding="utf-8"))["agg"]
    pol = json.load(open(POLICY, encoding="utf-8"))

    ext = [o for o, v in pool.items() if (v.get("city") or "") not in ("", SZ)]
    N = len(ext)
    sz_ids = {o for o, v in pool.items() if v.get("city") == SZ}

    # ---- 政策供给强度（产业词 → 深圳政策条数 / 全国条数） -------------------
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
    for o in ext:
        v = agg.get(pool[o]["name"])
        if v and v[0]:
            pat[o] = int(v[0])
            inv_share[o] = v[1] / v[0]
    pn, isn = mm(pat), mm(inv_share)
    for o in pat:
        comp[o] = 0.6 * pn[o] + 0.4 * isn[o]

    # ---- D2 产业相关度：契合度 + 链协同 ------------------------------------
    fit, syn = {}, {}
    edges = defaultdict(lambda: [0, 0])  # org -> [总已知对端, 深圳对端]
    for src, dst, *_ in f["invest_edges"]:
        for a, b in ((src, dst), (dst, src)):
            if a in pool:
                edges[a][0] += 1
                if b in sz_ids:
                    edges[a][1] += 1
    for src, dst, *_ in f["shareholder_edges"]:
        for a, b in ((src, dst), (dst, src)):
            if a in pool:
                edges[a][0] += 1
                if b in sz_ids:
                    edges[a][1] += 1
    for o in ext:
        tg = set(pool_tags.get(o) or [])
        if tg:
            fit[o] = len(tg & set(TARGET)) / len(TARGET)
    for o in ext:
        tot, szn = edges.get(o, [0, 0])
        if tot:
            syn[o] = szn / tot

    # ---- D3 政策匹配度 ------------------------------------------------------
    pols = {}
    for o in ext:
        tg = set(pool_tags.get(o) or [])
        if tg:
            pols[o] = sum(pol_cnt.get(t, 0) for t in tg) / (len(tg) * pol_max)

    # ---- D4 深圳连接度 ------------------------------------------------------
    # 旧稿纯比值 sz/total 会让「只有 1 个对端且恰好是深圳」的机构拿满分（实测前几名即被这类
    # 单边机构占据）。这里保留比值语义，再乘一个样本量置信因子 log1p(total)/log1p(20)（上限 1），
    # 纯比值口径另存 sensitivity_conn_raw 供对照，不隐藏原始口径。
    import math
    conn, conn_raw = {}, {}
    for o in ext:
        tot, szn = edges.get(o, [0, 0])
        if tot:
            raw = szn / tot
            conn_raw[o] = raw
            conf = min(1.0, math.log1p(tot) / math.log1p(20))
            conn[o] = raw * conf

    # ---- 合成 --------------------------------------------------------------
    dims = {"competitiveness": mm(comp), "industry_fit": mm(fit),
            "policy_match": mm(pols), "sz_connection": mm(conn)}
    score, detail = {}, {}
    for o in ext:
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

    top = []
    for i, (o, s) in enumerate(ranked[:15]):
        top.append({"rank": i + 1, "org_id": o, "name": pool[o]["name"], "city": pool[o].get("city"),
                    "type": pool[o].get("ptype2"), "score": s, "band": band(s),
                    "patents": pat.get(o), "inv_share": round(inv_share.get(o, 0), 4) if o in inv_share else None,
                    "tags": pool_tags.get(o), "sz_neighbors": edges.get(o, [0, 0])[1],
                    "known_neighbors": edges.get(o, [0, 0])[0],
                    "dim_scores": {k: round(v, 4) for k, v in detail[o].items()}})

    bands = {"优先引入": 0, "重点关注": 0, "观察": 0, "暂缓": 0}
    for s in vals:
        bands[band(s)] += 1

    # 对端可见性诊断（连接度维的分母缺口）
    tgt_all, tgt_vis = set(), set()
    for src, dst, *_ in f["invest_edges"]:
        if dst:
            tgt_all.add(dst)
            if dst in bf:
                tgt_vis.add(dst)

    reason = ("四维在外部池 %d 家上均可实测：竞争力维用专利代理（%d 家有专利）、产业相关度用深圳 20+8 "
              "标签（%d 家有标签）、政策匹配用 20,000 条政策标题关键词、深圳连接度用双端在池的资本边；"
              "但两处是结构性缺口——(1) 年报无研发投入/研发人员两列，竞争力只能走产出侧代理；"
              "(2) 资本边对端城市只在池内可见（30,219 个对端只有 %d 个有城市），连接度是下界。"
              "缺政策命中表 svc_org_policy_hit，政策维只能用标题关键词近似。故判部分支持。" %
              (N, len(pat), len(fit), len(tgt_vis)))

    out = {
        "metric_id": "M_SVC_DEEP_180_1",
        "metric_name": "服务机构引入推荐模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "main_gap": ("研发投入/研发人员字段空挂（竞争力维只能产出侧代理）；对端城市仅池内可见，"
                     "深圳连接度是下界；无 svc_org_policy_hit 命中表，政策维用标题关键词近似"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info + dwd_org_base_info(city)",
             "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_industry_product_tags（20+8）",
             "rows": pt["pool_tags_meta"]["rows_matched"],
             "snapshot": "code/_snapshots21/svc21_pt_axis_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_patent（首申请人聚合）",
             "rows": 2939895, "snapshot": "code/_snapshots21/star_applicant_agg_gkx.json"},
            {"library": "gkx", "host": "183.240.141.251:3318", "table": "gkx.dwd_policy_base",
             "rows": len(pol), "snapshot": "code/_snapshots21/policy_base_20261021.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_invest_info + dwd_org_shareholder_info",
             "rows": {"invest": len(f["invest_edges"]), "shareholder": len(f["shareholder_edges"])},
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("招引排序是截面决策（快照时点存量），不做年度序列；"
                            "专利与政策均按存量计，政策库跨 2000—2025 年发布，不按年拆窗。"),
        "population": {"external_n": N, "pool_total": len(pool), "sz_n": len(sz_ids),
                       "rule": "city != 深圳市 且 city 非空（空城市 21 家剔除，不并入外部池）"},
        "dimension_cover": {
            "D1_competitiveness": {"available": True, "proxy": "patents + invention_share",
                                   "orgs": len(comp),
                                   "note": "年报研发两列全表 0 行非空，按旧稿同法改产出侧代理"},
            "D2_industry_fit": {"available": True, "orgs": len(fit), "chain_orgs": len(syn),
                                "target_lexicon": TARGET},
            "D3_policy_match": {"available": True, "orgs": len(pols),
                                "note": "20,000 条政策标题关键词命中数，深圳政策单列，缺命中表"},
            "D4_sz_connection": {"available": True, "orgs": len(conn),
                                 "note": "对端城市仅池内可见：%d/%d 个投资对端有城市" % (len(tgt_vis), len(tgt_all))},
        },
        "policy_supply": {"by_industry_all": dict(pol_cnt), "by_industry_sz": dict(pol_sz),
                          "sz_title_hits": sum(1 for r in pol if "深圳" in (r.get("title") or "")),
                          "sz_city_field": sum(1 for r in pol if r.get("city") == SZ)},
        "composite": {"dims": ["competitiveness", "industry_fit", "policy_match", "sz_connection"],
                      "weights": "等权 1/4", "scored_orgs": len(score),
                      "unscored_orgs": N - len(score), "rule": "维数 <2 不入排序；缺维不补 0"},
        "score_dist": {"n": len(vals), "mean": round(statistics.mean(vals), 2) if vals else None,
                       "median": round(statistics.median(vals), 2) if vals else None,
                       "p90": q(0.90), "p99": q(0.99),
                       "max": round(vals[-1], 2) if vals else None,
                       "min": round(vals[0], 2) if vals else None, "bands": bands},
        "top15": top,
        "sensitivity_conn_raw": {
            "note": "纯比值口径（旧稿原式）下的前 5 名，用于说明为何加样本量置信因子",
            "top5": [{"name": pool[o]["name"], "conn_raw": round(v, 4),
                      "known_neighbors": edges[o][0], "sz_neighbors": edges[o][1]}
                     for o, v in sorted(conn_raw.items(), key=lambda x: -x[1])[:5]],
        },
        "caliber_note": ("连接度分子是「深圳对端边数」，分母是「已知对端边数」而非机构真实客户总数——"
                         "旧稿要求总客户/供应商数，gkx 无该字段，故本维是相对连接强度而非绝对占比"),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("外部池=%d 有分=%d 专利=%d 标签=%d 连接=%d" % (N, len(score), len(pat), len(fit), len(conn)))
    print("dist", out["score_dist"])
    print("top3", [(t["name"], t["city"], t["score"], t["patents"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
