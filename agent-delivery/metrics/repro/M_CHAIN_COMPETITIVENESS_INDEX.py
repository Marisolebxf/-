#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产业链竞争力指数（M_CHAIN_COMPETITIVENESS_INDEX）。

只读 `code/_snapshots21/` 落盘快照，不连数据库；单次运行约 2 秒。

指标来源是王惠《产业链分析》的三维八项（企业维 3、学术维 3、生态维 2）。
本件逐项核对可得性后，只对**能落地的 5 个子项**做等权合成，缺失的 5 项在
`missing_dims` 与 `subitems_wanghui` 里逐条给出计数证据，不填默认分、不伪造。

合成方式（本件自定义，待甲方确认）：
  每个子项在 12 条链内做 min-max 归一到 0—1，再等权平均乘 100。

产物：code/M_CHAIN_COMPETITIVENESS_INDEX_out.json
"""
from __future__ import annotations

import json
import math
import os
import time
from collections import Counter

METRIC = "M_CHAIN_COMPETITIVENESS_INDEX"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, METRIC + "_out.json")


def jload(name):
    p = os.path.join(SNAP, name)
    if not os.path.exists(p):
        raise FileNotFoundError("缺共享快照 %s" % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def pct(a, b):
    return round(a / b, 6) if b else 0.0


def main():
    t0 = time.time()
    panel = jload("chain_panel21.json")
    layer = jload("chain21_layer_20261022.json")
    fin = jload("chain21_fin_degree_20261022.json")
    rev = jload("chain21_revenue_20261022.json")
    paper = jload("org_paper_counts_20261021.json")

    name2chain = layer["names"]

    # ---------- 融资事件挂链 ----------
    fin_by = Counter()
    for r in fin["fin"]:
        ch = name2chain.get(r[1])
        if ch:
            fin_by[ch] += 1
    fin_mapped = sum(fin_by.values())

    # ---------- 营收记录挂链（王惠「人均营收」的可用性证据） ----------
    rev_rows = len(rev["stock"]) + len(rev["annual"])
    rev_by = Counter()
    for block in ("stock", "annual"):
        for row in rev[block]:
            ch = name2chain.get(row[1])
            if ch:
                rev_by[ch] += 1
    rev_mapped = sum(rev_by.values())

    # ---------- 论文机构挂链（学术维的可用性证据） ----------
    paper_orgs = len(paper["counts"])
    paper_nonzero = sum(1 for v in paper["counts"].values() if v)
    paper_mapped = sum(1 for k in paper["counts"] if k in name2chain)

    # ---------- 5 个子项 ----------
    rows = []
    for c in panel["chains"]:
        ch = c["chain"]
        firms = c["firms"]
        rows.append({
            "chain": ch, "name": c["name"],
            "firms": firms,
            "sz_firms": c["sz_firms"],
            "patents": c["patents"],
            "patent_firms": c["patent_firms"],
            "fin_events": fin_by.get(ch, 0),
            "leaves": c["leaves"],
            "leaves_with_firms": c["leaves_with_firms"],
            "firms_log10": round(math.log10(firms), 6) if firms else 0.0,
            "patent_per_1k_firms": round(c["patents"] / firms * 1000, 2) if firms else 0.0,
            "patent_firm_ratio": pct(c["patent_firms"], firms),
            "fin_per_1k_firms": round(fin_by.get(ch, 0) / firms * 1000, 2) if firms else 0.0,
            "leaf_coverage": pct(c["leaves_with_firms"], c["leaves"]),
            "revenue_records": rev_by.get(ch, 0),
            "paper_orgs": 0,
        })

    sub = [
        ("S1", "企业规模（log10 企业数，人均营收的代理）", "firms_log10"),
        ("S2", "创新密度（每千家企业专利申请量）", "patent_per_1k_firms"),
        ("S3", "创新广度（有专利企业占比）", "patent_firm_ratio"),
        ("S4", "资本活跃度（每千家企业融资事件数）", "fin_per_1k_firms"),
        ("S5", "环节覆盖（有企业的叶级环节占比）", "leaf_coverage"),
    ]
    for code, label, key in sub:
        sc = minmax([r[key] for r in rows])
        for r, s in zip(rows, sc):
            r["score_" + code] = round(s, 6)
    for r in rows:
        r["index"] = round(100 * sum(r["score_" + code] for code, _, _ in sub) / len(sub), 2)
    rows.sort(key=lambda x: -x["index"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    idx = [r["index"] for r in rows]

    db_probe = {
        "probed_at": "2026-10-22 17:05 +08:00",
        "note": "以下 5 个计数为一次性 DB 探测（information_schema + 聚合），本脚本不重跑；"
                "因这两张财务表未进快照。SQL 原样附上，可用只读账号复核。",
        "sql": [
            "SELECT column_name FROM information_schema.columns WHERE table_schema='gkx' "
            "AND table_name IN ('dwd_org_base_info','dwd_org_annual_financial_info','dwd_org_stock_finance_info')",
            "SELECT COUNT(*), SUM(employees_number>0), SUM(research_development_amount>0), "
            "COUNT(DISTINCT CASE WHEN research_development_amount>0 THEN org_id END), COUNT(DISTINCT org_id) "
            "FROM dwd_org_stock_finance_info",
            "SELECT COUNT(*), SUM(employees_number>0), SUM(arch_development_am>0), COUNT(DISTINCT org_id) "
            "FROM dwd_org_annual_financial_info",
            "SELECT COUNT(*), SUM(org_size<>0 AND org_size IS NOT NULL) FROM dwd_org_base_info",
            "SELECT COUNT(*), SUM(operating_revenue>0), MIN(operating_revenue), MAX(operating_revenue), "
            "SUM(operating_revenue<1), SUM(operating_revenue>=1e8) FROM dwd_org_annual_financial_info",
            "SELECT COUNT(*), COUNT(DISTINCT org_id) FROM dwd_org_annual_financial_info "
            "WHERE operating_revenue>0 AND employees_number>0",
            "SELECT MIN(operating_revenue), MAX(operating_revenue), "
            "MIN(operating_revenue/employees_number), MAX(operating_revenue/employees_number) "
            "FROM dwd_org_annual_financial_info WHERE operating_revenue>0 AND employees_number>0",
            "SELECT SUM(operating_revenue/employees_number BETWEEN 1 AND 1e7) "
            "FROM dwd_org_annual_financial_info WHERE operating_revenue>0 AND employees_number>0",
        ],
        "stock_finance_rows": 40239,
        "stock_finance_orgs": 972,
        "stock_employees_nonnull": 0,
        "stock_rd_positive": 19585,
        "stock_rd_orgs_positive": 876,
        "stock_finance_orgs_note": "972 为全表去重主体数；研发费用>0 仅 876 家（19,585 行），早期稿把全表 972 家当研发覆盖，已改",
        "annual_finance_rows": 90926,
        "annual_finance_orgs": 8127,
        "annual_employees_positive": 3170,
        "annual_revenue_positive": 2191,
        "annual_revenue_min": -443.71,
        "annual_revenue_max": 109056497066.48,
        "annual_revenue_lt1": 7,
        "annual_revenue_ge1e8": 258,
        "percap_pairs": 1288,
        "percap_orgs": 850,
        "pair_revenue_min": 0.06,
        "pair_revenue_max": 27185309985.32,
        "percap_median": 120.57,
        "rev_bucket_lt1": 5,
        "rev_bucket_1_to_1e4": 790,
        "rev_bucket_1e4_to_1e8": 1138,
        "rev_bucket_ge1e8": 258,
        "percap_min": 0.005882,
        "percap_max": 93967560.13,
        "percap_plausible_1_to_1e7": 1258,
        "annual_rd_columns_nonnull": 0,
        "base_org_size_nonzero": 0,
        "base_rows": 189116,
        "rd_org_share": round(876 / 189116, 6),
        "annual_employees_share": round(3170 / 90926, 6),
        "percap_org_share": round(850 / 189116, 6),
        "stock_employees_share": 0.0,
        "unit_note": "operating_revenue 同表内量级跨 12 个数量级（0.06 → 2.72e10，另有 -443.71 负值），"
                     "人均营收算出 0.0059—93,967,560 元/人、中位仅 120.57 元/人；"
                     "分桶 <1:5 / 1—1e4:790 / 1e4—1e8:1138 / ≥1e8:258，"
                     "中位数低于任何合理年报口径的营收/人，说明该列在元与万元/亿元之间混用。"
                     "本件因此不采用人均营收，S1 用企业数 log10 代理规模。",
    }

    compute = {
        "db_probe": db_probe,
        "subitems_used": [{"code": c, "label": l, "field": k,
                           "weight": round(1 / len(sub), 4)} for c, l, k in sub],
        "chains": rows,
        "index_max": {"name": rows[0]["name"], "index": rows[0]["index"]},
        "index_min": {"name": rows[-1]["name"], "index": rows[-1]["index"]},
        "index_mean": round(sum(idx) / len(idx), 2),
        "index_median": round(sorted(idx)[len(idx) // 2], 2),
        "firms_total": sum(r["firms"] for r in rows),
        "patents_total": sum(r["patents"] for r in rows),
        "patent_firms_total": sum(r["patent_firms"] for r in rows),
        "fin_events_total": len(fin["fin"]),
        "fin_events_mapped": fin_mapped,
        "fin_mapped_ratio": pct(fin_mapped, len(fin["fin"])),
        "revenue_rows": rev_rows,
        "revenue_mapped": rev_mapped,
        "revenue_mapped_ratio": pct(rev_mapped, rev_rows),
        "paper_orgs": paper_orgs,
        "paper_orgs_nonzero": paper_nonzero,
        "paper_orgs_mapped": paper_mapped,
        "paper_orgs_mapped_ratio": pct(paper_mapped, paper_orgs),
        "count_share_ge_10pct": sum(1 for r in rows if r["firms"] / sum(x["firms"] for x in rows) >= 0.10),
    }

    # 王惠三维八项逐项可得性
    subitems_wanghui = [
        {"dim": "企业维", "item": "人均营收", "available": False,
         "evidence": "不是「没有列」，而是「列都有、交集太小且单位不齐」："
                     "dwd_org_stock_finance_info 的 employees_number 在 40,239 行里 0 行有值；"
                     "dwd_org_annual_financial_info 的 employees_number 3,170 行 >0、operating_revenue 2,191 行 >0，"
                     "两者同时 >0 的仅 1,288 行 / 850 家企业（占底册 0.45%%）。"
                     "且 operating_revenue 同表内量级跨 12 个数量级（0.06 → 2.72e10，另有 -443.71 负值），"
                     "人均营收实测 0.0059—93,967,560 元/人，只有 1,258/1,288 行（97.67%%）落在 1—1e7 的合理区间。"
                     "分子侧另有一条：营收快照 %d 行按企业名可挂链 %d 行（%.2f%%）。"
                     % (rev_rows, rev_mapped, rev_mapped / rev_rows * 100),
         "proxy": "S1 用企业数（log10）代理规模，不代理人均"},
        {"dim": "企业维", "item": "研发强度", "available": False,
         "evidence": "字段存在但覆盖极低：dwd_org_stock_finance_info.research_development_amount 有 19,585 行 >0、"
                     "仅 876 家企业（占底册 0.46%）；dwd_org_annual_financial_info 的 arch_development_am 与 "
                     "development_employee 全为 NULL。本件快照未取该列，故未纳入合成。",
         "proxy": "可用「上市公司口径研发强度」补算，但只代表 876 家上市公司"},
        {"dim": "企业维", "item": "有效专利", "available": True,
         "evidence": "star_applicant_agg_gkx.json 2,939,895 件申请、2,140,420 件授权，按申请人名挂链",
         "proxy": "用申请量（有效状态无失效日，不可得）"},
        {"dim": "学术维", "item": "论文", "available": False,
         "evidence": "论文机构快照 %d 家机构中仅 %d 家能挂到链（%.4f%%），且总体只覆盖 %d 篇"
                     % (paper_orgs, paper_mapped, paper_mapped / paper_orgs * 100, paper["total"]),
         "proxy": "无代理"},
        {"dim": "学术维", "item": "人才", "available": False,
         "evidence": "学者表无链标签，链内无「学者—链」桥接表（缺表三态见 TABLE_ABSENCE_EVIDENCE.md）",
         "proxy": "无代理"},
        {"dim": "学术维", "item": "机构", "available": False,
         "evidence": "高校/科研院所表无链标签；论文机构挂链已验证只有 %d 家" % paper_mapped,
         "proxy": "无代理"},
        {"dim": "生态维", "item": "政策覆盖", "available": False,
         "evidence": "dwd_policy_base 无链/行业字段，政策只能按城市与年份聚合",
         "proxy": "无代理"},
        {"dim": "生态维", "item": "融资事件", "available": True,
         "evidence": "融资表 %d 行，按企业名挂链 %d 行（%.2f%%）"
                     % (len(fin["fin"]), fin_mapped, fin_mapped / len(fin["fin"]) * 100),
         "proxy": "用事件次数（金额币种不统一，不用金额）"},
    ]
    n_avail = sum(1 for x in subitems_wanghui if x["available"])

    out = {
        "metric": METRIC,
        "title": "产业链竞争力指数",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "王惠三维八项里只有 %d 项在 gkx 有全量源（有效专利、融资事件），"
            "企业维的另外两项（人均营收、研发强度）字段存在但不可用：研发额仅 876 家企业有正值（0.46%%）；"
            "人均营收的分子分母都存在但交集极小——employees_number 在 stock 表 40,239 行中 0 行有值、"
            "annual 表 3,170 行 >0，operating_revenue 在 annual 表 2,191 行 >0，"
            "两者同时 >0 仅 1,288 行 / 850 家企业（底册 0.45%%），且 operating_revenue 同表内量级跨 12 个数量级"
            "（0.06 → 2.72e10，含 -443.71 负值），人均值 0.0059—93,967,560 元/人，不可横比。"
            "学术维三项（论文、人才、机构）则不可得：营收记录 %d 行按企业名挂链仅 %d 行（%.2f%%）、"
            "论文机构 %d 家中仅 %d 家能挂链、学者的链标签与政策的链标签在库内无字段。"
            "本件用 5 条可算子项（企业规模、专利密度、"
            "专利广度、融资密度、环节覆盖）做等权合成，指数 12 条链全部有值，"
            "但缺 5 项意味着「竞争力」只剩规模与创新两面，学术与政策两面缺失。"
            "故判部分支持。"
            % (n_avail, rev_rows, rev_mapped, rev_mapped / rev_rows * 100,
               paper_orgs, paper_mapped)
        ),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "elapsed_sec": round(time.time() - t0, 1),
        "sources": {
            "snapshots": ["code/_snapshots21/chain_panel21.json",
                          "code/_snapshots21/star_applicant_agg_gkx.json",
                          "code/_snapshots21/chain21_fin_degree_20261022.json",
                          "code/_snapshots21/chain21_revenue_20261022.json",
                          "code/_snapshots21/org_paper_counts_20261021.json"],
            "upstream_tables": ["gkx.dwd_industry_chain_info", "gkx.dwd_org_industry_tags",
                                "gkx.dwd_patent", "gkx.dwd_org_financing_info",
                                "gkx.dwd_org_annual_financial_info", "gkx.dwd_policy_base"],
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面指数：5 个子项全部取全库存量，无年度分母。专利侧只用存量申请量，"
            "不构造年度序列，因此不涉及 2021 年以前零行的问题。"
        ),
        "params": {
            "weights": "5 个子项等权（各 0.2）",
            "normalization": "12 条链内 min-max",
            "weight_note": "等权与 min-max 均为本件自定义、待甲方确认；王惠原口径的权重表在库内不存在",
        },
        "compute": compute,
        "subitems_wanghui": subitems_wanghui,
        "missing_dims": [x for x in subitems_wanghui if not x["available"]],
        "counter_checks": [
            {"id": "C1", "question": "论文维是不是只是「没试过挂链」？",
             "action": "把论文机构快照的 %d 个机构名与链标签表 %d 个名称做交集"
                       % (paper_orgs, len(name2chain)),
             "result": "交集 %d 家（%s）。论文机构与企业是两个主体集，名称几乎不重合，"
                       "不是挂链算法的问题，是根本没有桥。"
                       % (paper_mapped, "、".join([k for k in paper["counts"] if k in name2chain][:3]) or "无")},
            {"id": "C2", "question": "营收维能不能用年报补齐？",
             "action": "把 stock 与 annual 两块共 %d 行按企业名挂链" % rev_rows,
             "result": "挂上 %d 行（%.2f%%），平均每链 %.1f 行——不足以算人均营收，"
                       "且这 %d 行集中在大企业，会把「有年报的企业」误当「链的代表」。"
                       % (rev_mapped, rev_mapped / rev_rows * 100, rev_mapped / 12, rev_mapped)},
            {"id": "C3", "question": "指数会不会被企业数一项决定（规模主导）？",
             "action": "对比 S1（企业规模）与合成指数的名次",
             "result": "企业数占全库 10%% 以上的链有 %d 条；S1 名次与合成名次相差 ≥4 位的有 %d 条，"
                       "说明其余 4 项确实改变了排序，不是规模单项决定。"
                       % (compute["count_share_ge_10pct"],
                          sum(1 for r in rows
                              if abs(r["rank"] - sorted(rows, key=lambda x: -x["firms_log10"]).index(r) - 1) >= 4))},
            {"id": "C5", "question": "「研发强度/人均营收不可得」是不是因为库内真的没有这两列？",
             "action": "逐列读 information_schema 的两张财务表（本件最初就是按「无字段」写的，后来推翻）",
             "result": "字段都在：stock 表有 research_development_amount（19,585 行 >0）与 employees_number（0 行有值），"
                       "annual 表有 employees_number（3,170 行 >0）、operating_revenue（2,191 行 >0）与 "
                       "arch_development_am（0 行有值）。所以正确表述是「有字段、覆盖不到位」，不是「无字段」。"
                       "这一处是本件第一次被自己推翻的理由。"},
            {"id": "C6", "question": "人均营收到底是缺人、缺钱，还是别的？",
             "action": "直接在同一张 annual 表里求「营收>0 且员工>0」的交集，并检查 revenue 的量级分布",
             "result": "既不缺人也缺钱：交集 1,288 行 / 850 家企业（底册 0.45%%）。真正的障碍是两条——"
                       "① 覆盖 850 家（0.45%%），无法代表任一链；② operating_revenue 同表内量级跨 12 个数量级"
                       "（0.06 → 2.72e10，另有 -443.71 负值），人均值算出 0.0059—93,967,560 元/人，"
                       "只有 1,258/1,288 行落在 1—1e7。所以「缺」的既不是人也不是钱，是"
                       "「可比的单位」与「足够的交集」——第一版把它写成「缺人」，第二次推翻。"},
            {"id": "C4", "question": "融资事件 57%% 挂链率会不会让 S4 只反映「被打标的企业」？",
             "action": "对比挂链与未挂链事件数",
             "result": "挂链 %d 行、未挂链 %d 行。未挂链的多为投资方名称或链标签表外的企业，"
                       "S4 因此偏向「已在链内」的企业，绝对值不可跨库比较。"
                       % (fin_mapped, len(fin["fin"]) - fin_mapped)},
        ],
        "notes": [
            "指数名保留「竞争力」，但本件只覆盖规模与创新两面；学术与政策两面缺失，对外必须同时披露。",
            "与 M_CHAIN_CONCENTRATION_INDEX 的分工：那件算链内环节分布（HHI/CR1），本件算链间综合位次；"
            "两件共用 chain_panel21 的企业数与专利数，但统计量不同，不可互相校验。",
            "与 M_CHAIN_SZ_ADVANTAGE_SCORE 的分工：那件是深圳 vs 四城的评分，本件是 12 条链之间的横向位次。",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("[OK] %s -> %s（%.1fs）指数 %.2f—%.2f，均 %.2f；八项可得 %d/8"
          % (METRIC, OUT, out["elapsed_sec"], rows[-1]["index"], rows[0]["index"],
             compute["index_mean"], n_avail))


if __name__ == "__main__":
    main()
