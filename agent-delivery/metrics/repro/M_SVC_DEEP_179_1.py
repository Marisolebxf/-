#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""科技创新服务机构技术力评价模型（M_SVC_DEEP_179_1）—— gkx 口径，自包含。

王惠口径四维（公式照抄旧稿，数据源全部换为 gkx 快照）：
    D1 合作科研机构数 = 联合申请人里高校/院所去重计数 —— gkx 无全量联合申请人明细，
                        仅 2.9 万行抽样，本件只作下界观察、不进合成
    D2 合作企业数     = 投资 + 机构股东 双端在池边（资本型合作代理）
    D3 科技创新成果数 = 第一申请人名称对齐的专利总数 + 发明占比（质量分层）
    D4 技术转化成果数 = 专利转移事件（转出/受让方名称命中）

合成：各维在 INNOV 池内 min-max（内联复制自 M_SVC_DEEP_177_1.py 的 mm），
缺维不补 0、不进平均，等权 ×100。

数据源：
    code/_snapshots21/svc21_facts_20261022.json      （pool/invest/shareholder）
    code/_snapshots21/star_applicant_agg_gkx.json    （dwd_patent GROUP BY first_applicant_name）
    code/_snapshots21/svc21_extra_20261022.json      （dwd_patent_transfer / dwd_org_heis_info）
    code/_snapshots21/collab_inputs21.json           （dwd_patent_applicants 抽样，仅 D1 下界）
    code/_snapshots21/svc21_pt_axis_20261022.json    （20+8 产业标签，辅助画像）
产出：code/M_SVC_DEEP_179_1_out.json
运行：cd code && python3 M_SVC_DEEP_179_1.py
"""
from __future__ import annotations

import json
import os
import statistics
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
FACTS = os.path.join(SNAP, "svc21_facts_20261022.json")
AGG = os.path.join(SNAP, "star_applicant_agg_gkx.json")
EXTRA = os.path.join(SNAP, "svc21_extra_20261022.json")
COLLAB = os.path.join(SNAP, "collab_inputs21.json")
PTAXIS = os.path.join(SNAP, "svc21_pt_axis_20261022.json")
OUT = os.path.join(HERE, "M_SVC_DEEP_179_1_out.json")


def mm(vals: dict) -> dict:
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    if hi - lo <= 1e-12:
        return {k: 0.5 for k, v in vals.items() if v is not None}
    return {k: (v - lo) / (hi - lo) for k, v in vals.items() if v is not None}


def rank_norm(vals: dict) -> dict:
    """分位归一（敏感度对照）：值→[0,1] 的秩百分位，抗极值（华为 81,376 件专利）"""
    if not vals:
        return {}
    order = sorted(vals.items(), key=lambda x: x[1])
    n = len(order)
    return {k: (i / (n - 1) if n > 1 else 0.5) for i, (k, _) in enumerate(order)}


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
    pool = f["pool"]
    inn = [o for o, v in pool.items() if v.get("ptype2") == "INNOV"]
    N = len(inn)
    inn_set = set(inn)

    # ---- D2 合作企业数：双端在池的资本边 -----------------------------------
    coop = defaultdict(set)
    for src, dst, *_ in f["invest_edges"]:
        if dst in inn_set:
            if src in inn_set and src != dst:
                coop[src].add(dst)
                coop[dst].add(src)
    for src, dst, *_ in f["shareholder_edges"]:
        if dst in inn_set:
            if src in inn_set and src != dst:
                coop[src].add(dst)
                coop[dst].add(src)
    d2 = {o: len(s) for o, s in coop.items()}

    # ---- D3 科技成果：专利总量 + 发明占比 ----------------------------------
    agg = json.load(open(AGG, encoding="utf-8"))["agg"]
    d3, inv_share = {}, {}
    for o in inn:
        v = agg.get(pool[o]["name"])
        if v and v[0]:
            d3[o] = int(v[0])
            inv_share[o] = round(v[1] / v[0], 4)

    # ---- D4 技术转化：专利转移事件 -----------------------------------------
    ex = json.load(open(EXTRA, encoding="utf-8"))
    name2org = {}
    for o in inn:
        name2org.setdefault(pool[o]["name"], o)
    d4 = defaultdict(int)
    transfer_years = defaultdict(int)
    for pn, before, after, date in ex["patent_transfer"]:
        y = str(date)[:4]
        hit = set()
        for raw in (before, after):
            try:
                for x in json.loads(raw or "[]"):
                    nm = (x or {}).get("name")
                    if nm in name2org:
                        hit.add(name2org[nm])
            except Exception:
                continue
        for o in hit:
            d4[o] += 1
            transfer_years[y] += 1

    # ---- D1 合作科研机构数：抽样下界（不进合成） ---------------------------
    coll = json.load(open(COLLAB, encoding="utf-8"))
    pn_apps = defaultdict(set)
    for pn, nm in coll.get("patent_applicants", []):
        pn_apps[pn].add(nm)
    heis = set()
    for row in ex["heis"]:
        if row and row[0]:
            heis.add(row[0])
    hei_pat = ("大学", "学院", "研究院", "研究所", "科学院", "实验室", "高等专科", "职业技术")
    coapp_pairs = 0
    d1_sample = defaultdict(set)
    for pn, names in pn_apps.items():
        if len(names) < 2:
            continue
        coapp_pairs += 1
        hs = [n for n in names if n in heis or any(k in n for k in hei_pat)]
        if not hs:
            continue
        for n in names:
            o = name2org.get(n)
            if o:
                for h in hs:
                    if h != n:
                        d1_sample[o].add(h)

    # ---- 合成 --------------------------------------------------------------
    dims = {"coop_firm": mm(d2), "output": mm(d3), "transfer": mm(d4)}
    score, detail = {}, {}
    for o in inn:
        parts = {k: v[o] for k, v in dims.items() if o in v}
        if len(parts) < 2:
            continue
        score[o] = round(sum(parts.values()) / len(parts) * 100.0, 2)
        detail[o] = parts

    # 敏感度：同三维改分位归一
    rdims = {"coop_firm": rank_norm(d2), "output": rank_norm(d3), "transfer": rank_norm(d4)}
    score_alt = {}
    for o in inn:
        parts = {k: v[o] for k, v in rdims.items() if o in v}
        if len(parts) >= 2:
            score_alt[o] = round(sum(parts.values()) / len(parts) * 100.0, 2)
    alt_ranked = sorted(score_alt.items(), key=lambda x: -x[1])

    ranked = sorted(score.items(), key=lambda x: -x[1])
    vals = sorted(score.values())

    def q(p):
        if not vals:
            return None
        i = min(len(vals) - 1, max(0, int(round(p * (len(vals) - 1)))))
        return round(vals[i], 2)

    top = []
    for i, (o, s) in enumerate(ranked[:10]):
        top.append({"rank": i + 1, "org_id": o, "name": pool[o]["name"], "city": pool[o].get("city"),
                    "score": s, "band": band(s), "coop_firm": d2.get(o),
                    "patents": d3.get(o), "inv_share": inv_share.get(o),
                    "transfers": d4.get(o),
                    "dim_scores": {k: round(v, 4) for k, v in detail[o].items()}})

    bands = {"领先": 0, "稳健": 0, "关注": 0, "薄弱": 0}
    for s in vals:
        bands[band(s)] += 1

    # 专利总量口径对照
    pat_total = sum(d3.values())
    pat_orgs = len(d3)
    inv_orgs = len(inv_share)
    tr_orgs = len(d4)
    tr_events = sum(d4.values())

    # 池内专利集中度
    pv = sorted(d3.values(), reverse=True)
    top1pct = sum(pv[: max(1, len(pv) // 100)]) / pat_total * 100 if pat_total else 0

    reason = ("四维里 D2（资本型合作边）、D3（专利 %d 件 / %d 家，含发明占比分层）、"
              "D4（专利转移 %d 件触达 %d 家）三维在 gkx 实测可算并已合成；"
              "D1 合作科研机构数缺全量联合申请人明细——gkx 只导出了 %d 行申请人抽样"
              "（对 293.9 万件专利约 1%%），只能给出稀疏下界，不足以进合成。"
              "四维缺一且缺的是产学研「研」侧，判部分支持；旧稿称本指标可「完全转换支持」，"
              "在 gkx 侧不成立，已如实降档。" %
              (pat_total, pat_orgs, tr_events, tr_orgs, len(coll.get("patent_applicants", []))))

    out = {
        "metric_id": "M_SVC_DEEP_179_1",
        "metric_name": "科技创新服务机构技术力评价模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": reason,
        "main_gap": ("D1 合作科研机构数无全量联合申请人数据（仅 2.9 万行抽样 / 293.9 万件专利）；"
                     "D4 转移表 22,809 行是三方库子集，非全量登记"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.dwd_org_org_product_info(main_activities) + dwd_org_base_info",
             "rows": f["population"]["product_info_all"],
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_patent（GROUP BY first_applicant_name，83 分块）",
             "rows": 2939895, "names": 169226,
             "snapshot": "code/_snapshots21/star_applicant_agg_gkx.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_patent_transfer", "rows": ex["patent_transfer_meta"]["rows"],
             "snapshot": "code/_snapshots21/svc21_extra_20261022.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_patent_applicants（抽样）",
             "rows": len(coll.get("patent_applicants", [])),
             "snapshot": "code/_snapshots21/collab_inputs21.json"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_org_invest_info + dwd_org_shareholder_info",
             "rows": {"invest": len(f["invest_edges"]), "shareholder": len(f["shareholder_edges"])},
             "snapshot": "code/_snapshots21/svc21_facts_20261022.json"},
        ],
        "base_years_used": [2026],
        "base_years_missing": [],
        "base_years_note": ("创新成果与转化按「存量登记」计（专利表无申请年字段入快照，转移表有效年 "
                            "2021—2026 共 %d 个年份有值），故不设滚动窗、也不按年摊平；"
                            "统计年 2026 仅用于口径标注，不做增速。" % len([y for y in transfer_years if y not in ("0", "None", "")])),
        "population": {"type": "INNOV", "n": N, "pool_total": len(pool)},
        "dimension_cover": {
            "D1_coop_hei": {"available": False, "orgs": len(d1_sample),
                            "note": "抽样内可见 %d 家机构有高校/院所共同申请人；样本仅覆盖约 1%% 专利，"
                                    "不进合成" % len(d1_sample)},
            "D2_coop_firm": {"available": True, "orgs": len(d2), "edges": sum(len(v) for v in coop.values()) // 2},
            "D3_output": {"available": True, "orgs": pat_orgs, "patents": pat_total,
                          "invention_orgs": inv_orgs},
            "D4_transfer": {"available": True, "orgs": tr_orgs, "events": tr_events},
        },
        "composite": {"dims": ["coop_firm", "output", "transfer"], "weights": "等权 1/3",
                      "scored_orgs": len(score), "unscored_orgs": N - len(score),
                      "rule": "维数 <2 不入排序；缺维不补 0"},
        "score_dist": {"n": len(vals), "mean": round(statistics.mean(vals), 2) if vals else None,
                       "median": round(statistics.median(vals), 2) if vals else None,
                       "p90": q(0.90), "p99": q(0.99),
                       "max": round(vals[-1], 2) if vals else None,
                       "min": round(vals[0], 2) if vals else None, "bands": bands},
        "top10": top,
        "sensitivity_rank_norm": {
            "note": "极值归一（旧稿口径）在华为 81,376 件的极值下把 99% 机构压到 5 分以下，"
                    "本块给出同三维改分位归一的对照，用于判断排序是否稳健而非替换口径",
            "top10": [{"rank": i + 1, "name": pool[o]["name"], "score": s_,
                       "patents": d3.get(o), "coop_firm": d2.get(o), "transfers": d4.get(o)}
                      for i, (o, s_) in enumerate(alt_ranked[:10])],
            "scored_orgs": len(score_alt),
        },
        "patent_facts": {"orgs_matched": pat_orgs, "match_rate_pct": round(pat_orgs / N * 100, 2),
                         "patents": pat_total, "top1pct_share_pct": round(top1pct, 2),
                         "median_per_matched": int(statistics.median([d3[o] for o in d3])) if d3 else 0},
        "transfer_facts": {"rows": ex["patent_transfer_meta"]["rows"],
                           "orgs_touched": tr_orgs, "events": tr_events,
                           "year_mix": dict(sorted(transfer_years.items()))},
        "coapp_sample": {"pn_with_multi_applicant": coapp_pairs,
                         "rows": len(coll.get("patent_applicants", [])),
                         "note": "抽样来自 dwd_patent_applicants 首屏 2.9 万行，非随机抽样，"
                                 "不能外推为池级合作高校数"},
        "caliber_note": ("专利按 first_applicant_name 精确名称对齐，不含简称/曾用名归并，故为下界；"
                         "转移事件按 before/after 双方名称精确命中，一次转移同时命中双方时双方各记 1 次"),
        "compute": {"elapsed_sec": round(time.time() - t0, 3), "sql_count": 0},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("INNOV=%d 有分=%d 专利=%d件/%d家 转移=%d件/%d家 合作边=%d家" %
          (N, len(score), pat_total, pat_orgs, tr_events, tr_orgs, len(d2)))
    print("dist", out["score_dist"])
    print("top3", [(t["name"], t["score"], t["patents"], t["coop_firm"]) for t in top[:3]])
    print("->", OUT)


if __name__ == "__main__":
    main()
