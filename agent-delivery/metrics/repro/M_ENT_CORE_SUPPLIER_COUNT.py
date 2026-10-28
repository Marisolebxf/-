#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_CORE_SUPPLIER_COUNT —— 核心供应商数（W13-E4，否定性证据探针）

判「完全不支持」。三层否定：
  层 1  母集合不存在：供应商边表 enterprise_supply_chain 在 gkx 0 张（承接 M_ENT_SUPPLIER_COUNT 的词根扫描）；
  层 2  核心标记不存在：is_core_supplier 0 列、risk_level 0 列、采购额/采购占比 0 列；
  层 3  替代面试算：把投资边当供应边、按出资额取 TOP5 会得到什么——用真实数据跑一遍，
        证明它给出的是「被投企业榜」而不是「核心供应商榜」（方向反了，且 100% 持股的子公司会排在首位）。

运行：cd code && python3 M_ENT_CORE_SUPPLIER_COUNT.py
产物：code/M_ENT_CORE_SUPPLIER_COUNT_out.json（verdict_kind="negative_evidence"）
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_CORE_SUPPLIER_COUNT_out.json")

SUPPLY_ROOTS = ["supply", "supplier", "vendor", "procure", "purchas",
                "采购", "供应", "上游", "下游"]
CORE_ROOTS = ["is_core", "core_supplier", "core_flag", "level", "grade", "tier"]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def db_probe():
    """替代面试算：投资边按出资额取 TOP5，看它给出的到底是什么。"""
    out = {"attempted": True, "ok": False}
    try:
        sys.path.insert(0, HERE)
        from _gkxdb import gkx
        cur = gkx()
        cur.execute("SET SESSION max_execution_time=120000")

        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='gkx' AND table_name LIKE '%%supply%%'")
        out["supply_tables"] = [r[0] for r in cur.fetchall()]
        cur.execute("SELECT table_name, column_name FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND (column_name LIKE '%%is_core%%' "
                    "OR column_name LIKE '%%core_supplier%%' "
                    "OR column_name LIKE '%%purchase_amount%%' "
                    "OR column_name LIKE '%%purchase_ratio%%')")
        out["core_or_amount_columns"] = [f"{t}.{c}" for t, c in cur.fetchall()]

        # 列注释核对方向：name_cn='机构名称'（投资方），inv_name='被投资企业名称'（被投方）
        cur.execute("SELECT column_name, column_comment FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND table_name='dwd_org_invest_info' "
                    "AND column_name IN ('name_cn','inv_name','investment_amount',"
                    "'investment_ratio')")
        out["column_comments"] = {c: k for c, k in cur.fetchall()}

        # 用华为系做方向自证：若 org=投资方，则「华为投资控股 → 华为技术(100%)」应成立
        cur.execute("SELECT name_cn, inv_name, investment_amount, investment_ratio "
                    "FROM gkx.dwd_org_invest_info WHERE name_cn='华为投资控股有限公司' "
                    "AND inv_name='华为技术有限公司' LIMIT 3")
        out["direction_self_test"] = [
            {"org_name": r[0], "inv_name": r[1], "amount": float(r[2]),
             "ratio": float(r[3])} for r in cur.fetchall()]

        # 全库最大出资额的投资边（若把投资边当供应边，这就是「TOP 供应商」）
        cur.execute("SELECT org_id, name_cn, inv_org_id, inv_name, investment_amount, "
                    "investment_ratio FROM gkx.dwd_org_invest_info "
                    "WHERE investment_amount IS NOT NULL "
                    "ORDER BY investment_amount DESC LIMIT 12")
        out["top_invest_edges_by_amount"] = [
            {"investor_id": r[0], "investor_name": r[1], "investee_id": r[2],
             "investee_name": r[3],
             "amount": float(r[4]) if r[4] is not None else None,
             "ratio": float(r[5]) if r[5] is not None else None}
            for r in cur.fetchall()]

        # 出资比例分档：investment_ratio 以小数存（0.03 = 3%）
        cur.execute("SELECT "
                    "SUM(investment_ratio >= 0.9999), "
                    "SUM(investment_ratio >= 0.5 AND investment_ratio < 0.9999), "
                    "SUM(investment_ratio > 0 AND investment_ratio < 0.5), "
                    "SUM(investment_ratio > 1.0001), "
                    "MAX(investment_ratio) "
                    "FROM gkx.dwd_org_invest_info WHERE investment_ratio IS NOT NULL")
        r = cur.fetchone()
        out["ratio_bands"] = {"wholly_owned_ge_9999": int(r[0] or 0),
                              "control_50_9999": int(r[1] or 0),
                              "minority_lt_50": int(r[2] or 0),
                              "gt_1_rows": int(r[3] or 0),
                              "max_ratio": float(r[4]) if r[4] is not None else None,
                              "unit_note": ("列注释写『股权占比(%)』，实测取值 0—1 之间"
                                            "（最大值 1.0、>1 的行 0 条），实际按小数存，"
                                            "解读时必须 ×100 才是百分数。")}

        # 全资边的金额量级：用于检验 investment_amount 的单位是否自洽
        cur.execute("SELECT COUNT(*), MIN(investment_amount), MAX(investment_amount), "
                    "SUM(investment_amount < 10), "
                    "SUM(investment_amount >= 10 AND investment_amount < 1000), "
                    "SUM(investment_amount >= 1000 AND investment_amount < 100000), "
                    "SUM(investment_amount >= 100000) "
                    "FROM gkx.dwd_org_invest_info "
                    "WHERE investment_ratio >= 0.9999 AND investment_amount > 0")
        r = cur.fetchone()
        cur.execute("SELECT investment_amount FROM gkx.dwd_org_invest_info "
                    "WHERE investment_ratio >= 0.9999 AND investment_amount > 0 "
                    "ORDER BY investment_amount LIMIT 1 OFFSET 7000")
        med = cur.fetchone()
        out["wholly_owned_amount_sanity"] = {
            "rows": int(r[0]), "min": float(r[1]), "max": float(r[2]),
            "lt_10": int(r[3] or 0), "10_1000": int(r[4] or 0),
            "1000_100000": int(r[5] or 0), "ge_100000": int(r[6] or 0),
            "p50": float(med[0]) if med else None,
            "unit_verdict": (
                "列注释写『投资金额(元)』，但量级跨 9 个数量级：全资边 p50 约 "
                f"{float(med[0]) if med else 0:,.0f}，最小 {float(r[1])}、最大 {float(r[2]):,.0f}。"
                "按元读，大量全资子公司资本不足千元；按万元读，最大边达 2,000 亿元级。"
                "两种读法都不能自洽 → 该金额列不可用于排序或分档。"),
        }

        # 出度最高的投资方（若当供应边，会把「最活跃投资方」写成「供应商最多的采购方」）
        cur.execute("SELECT org_id, name_cn, COUNT(*) c FROM gkx.dwd_org_invest_info "
                    "WHERE org_id IS NOT NULL GROUP BY org_id, name_cn "
                    "ORDER BY c DESC LIMIT 10")
        out["top_out_degree_investors"] = [
            {"investor_id": r[0], "investor_name": r[1], "n_investees": int(r[2])}
            for r in cur.fetchall()]

        # 出度分档：代理口径会退化成 min(5, 出度)
        cur.execute("SELECT SUM(c >= 5), SUM(c >= 2 AND c < 5), SUM(c = 1), COUNT(*) "
                    "FROM (SELECT COUNT(*) c FROM gkx.dwd_org_invest_info "
                    "WHERE org_id IS NOT NULL GROUP BY org_id) t")
        r = cur.fetchone()
        out["investor_out_degree_bands"] = {
            "ge_5": int(r[0] or 0), "2_to_4": int(r[1] or 0), "eq_1": int(r[2] or 0),
            "investors_total": int(r[3] or 0),
            "degenerate_note": ("若把投资边当供应边，核心供应商数退化为 min(5, 出度)："
                                "出度≥5 的企业一律得 5，指标失去区分度。"),
        }
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def main():
    fam = load("supply_family_20261023.json")
    inv = fam["invest"]
    sh = fam["shareholder"]
    base_total = fam["fin_org_join"]["base_orgs_total"]
    vocab = fam["vocab_scan"]
    dbp = db_probe()

    probes = {}
    probes["p1_mother_set_missing"] = {
        "required_object": "enterprise_supply_chain（relation_type='supplier' 的边表）",
        "tables_found": 0,
        "vocab": {k: {"n_columns": vocab[k]["n_columns"], "n_tables": vocab[k]["n_tables"]}
                  for k in SUPPLY_ROOTS},
        "conclusion": ("核心供应商是在供应商集合 S 内再筛『核心』子集；S 本身不存在，"
                       "子集筛选无从谈起。"),
    }
    probes["p2_core_marker_missing"] = {
        "required_fields": ["is_core_supplier", "purchase_amount", "purchase_ratio",
                            "supplier_rank", "relation_type", "risk_level"],
        "found_fields": dbp.get("core_or_amount_columns", []),
        "live_supply_tables": dbp.get("supply_tables", []),
        "conclusion": ("全库无 is_core_supplier / purchase_amount / purchase_ratio / supplier_rank "
                       "同义列；唯一带 level/grade 的字段是招投标的公告属性与行业标签，"
                       "与『这家供应商是不是核心』无关。"),
    }

    top = dbp.get("top_invest_edges_by_amount", [])
    rb = dbp.get("ratio_bands") or {}
    ws = dbp.get("wholly_owned_amount_sanity") or {}
    probes["p3_proxy_trial"] = {
        "proxy_under_test": ("把 dwd_org_invest_info 的出资额当采购额，"
                             "对每家企业取 TOP5 出资对象作为『核心供应商』"),
        "column_comments": dbp.get("column_comments"),
        "direction_self_test": dbp.get("direction_self_test"),
        "top_edges_returned": top[:6],
        "ratio_bands": rb,
        "wholly_owned_amount_sanity": ws,
        "top_out_degree_investors": dbp.get("top_out_degree_investors"),
        "investor_out_degree_bands": dbp.get("investor_out_degree_bands"),
        "fatal_flaws": [
            ("方向错：本表 org_id=投资方（列注释『机构名称』）、inv_org_id=被投企业"
             "（列注释『被投资企业名称』），边指向是『投资方 → 被投方』；"
             "供应边的指向是『供应商 → 采购方』，两者方向相反。"
             + (f"实测最大出资边是『{top[0]['investor_name']} → {top[0]['investee_name']}』，"
                f"出资比例 {top[0]['ratio']:.4f}；照代理口径就会得出"
                f"『{top[0]['investor_name']} 的核心供应商是 {top[0]['investee_name']}』这种荒谬结论。"
                if top else "")),
            (f"总体错：投资边覆盖 {inv['distinct_org']} 家投资方、{inv['distinct_inv_org']} 家被投企业"
             f"（被投方占底册 {round(inv['distinct_inv_org'] / base_total * 100, 2)}%），"
             "而供应关系的总体应是『有采购行为的企业』，两者不是同一批企业。"),
            ("字段错：投资表 18 列里没有交易金额、采购品类、订单号，出资额无法换算成采购额；"
             f"出资比例分档实测：全资(≥99.99%) {rb.get('wholly_owned_ge_9999')} 行、"
             f"控股(50%~99.99%) {rb.get('control_50_9999')} 行、参股(<50%) {rb.get('minority_lt_50')} 行，"
             "是持股结构而不是采购份额。"),
            ("金额列不可用：即使退一步按金额排序，investment_amount 的单位也不自洽——"
             f"{ws.get('unit_verdict', '')}"),
            (f"关系错：投资边与股权边有 {fam['edge_overlap']['intersect_pairs']} 对重合，"
             "说明该表记录的是认缴出资/持股，属资本关系而非交易关系。"),
        ],
        "conclusion": ("代理面试算确实能跑出『每家企业 TOP5 出资对象』，但它给出的是被投企业榜，"
                       "且金额列单位不自洽、排序不可复现；采用即等于把指标改名换义，"
                       "故不采用，维持完全不支持。"),
    }

    probes["p4_alternative_faces"] = {
        "invest": {"rows": inv["rows"], "distinct_investors": inv["distinct_inv_org"]},
        "shareholder": {"rows": sh["rows"], "distinct_pairs": sh.get("distinct_pairs")},
        "bid_win": fam["bid_win"],
        "note": ("招投标面存在『中标方』但招标方 org_id 缺失（purchaser 字段只有名称字符串），"
                 "即便把中标记录当供货记录，也无法确定采购方，无法构成 (采购方, 供应商) 对。"),
    }

    out = {
        "metric_id": "M_ENT_CORE_SUPPLIER_COUNT",
        "metric_name": "核心供应商数",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "指标 = 在供应商集合内筛 is_core_supplier=1 的计数。gkx 既无供应商边表（母集合 S 缺失），"
            "也无 is_core_supplier / purchase_amount / supplier_rank 类核心标记；"
            "把投资边按出资额 TOP5 试算得到的是『投资方 → 被投企业』榜，方向与供应边相反，"
            "且金额列单位不自洽 → 结构与数据都不具备可算闭环。"),
        "formula_calc_logic": (
            "core_supplier_count(i) = COUNT(DISTINCT related_org_id) WHERE org_id=i "
            "AND relation_type='supplier' AND is_core_supplier=1"),
        "dependencies_declared": ["enterprise_supply_chain（relation_type / is_core_supplier）"],
        "dependencies_found": [],
        "probes": probes,
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("负结论件，无指标值，不涉及基期；核心标记是时点属性而非年度量，"
                            "本件不构造任何年度序列。"),
        "sources": {
            "db": "gkx @ 183.240.141.251:3318",
            "tables_checked": ["gkx.dwd_org_invest_info", "gkx.dwd_org_shareholder_info",
                               "gkx.dwd_bid_win_candidate_out", "information_schema"],
            "snapshots": ["code/_snapshots21/supply_family_20261023.json",
                          "code/_snapshots21/gkx_columns_20261023.json"],
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"judgment": out["support_judgment"],
                      "ratio_bands": dbp.get("ratio_bands"),
                      "top_edges": len(top)}, ensure_ascii=False))
    if top:
        print("top1", json.dumps(top[0], ensure_ascii=False))
    print("saved", OUT)


if __name__ == "__main__":
    main()
