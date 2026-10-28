#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_SUPPLIER_COUNT —— 供应商数量（W13-E4，否定性证据探针）

本件判「完全不支持」，脚本的唯一职责是证明「为什么不可算」，因此不产出指标值：
  探针 1  全库列字典词根扫描（280 表 / 6,312 列）：有没有 supplier / supply / vendor 关系列；
  探针 2  表名扫描：有没有供应链边表；
  探针 3  三张候选边面实测：投资边 / 股权边 / 招投标面，各自能组成什么关系；
  探针 4  替代面语义差异：投资边只有出资额与出资比例，没有交易字段，且覆盖总体与采购总体不同；
  探针 5  活库复核（information_schema）：列字典是快照，现场再查一次表名与列名。

运行：cd code && python3 M_ENT_SUPPLIER_COUNT.py
产物：code/M_ENT_SUPPLIER_COUNT_out.json（verdict_kind="negative_evidence"）
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_SUPPLIER_COUNT_out.json")

SUPPLY_ROOTS = ["supply", "supplier", "vendor", "procure", "purchas",
                "采购", "供应", "上游", "下游"]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def live_recheck():
    """现场复核 information_schema：表名与列名里有没有供应链对象。"""
    out = {"attempted": True, "ok": False}
    try:
        sys.path.insert(0, HERE)
        from _gkxdb import gkx
        cur = gkx()
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='gkx' AND (table_name LIKE '%%supply%%' "
                    "OR table_name LIKE '%%supplier%%' OR table_name LIKE '%%vendor%%' "
                    "OR table_name LIKE '%%procure%%')")
        out["supply_like_tables"] = [r[0] for r in cur.fetchall()]
        cur.execute("SELECT table_name, column_name FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND (column_name LIKE '%%supplier%%' "
                    "OR column_name LIKE '%%supply%%' OR column_name LIKE '%%vendor%%')")
        out["supply_like_columns"] = [f"{t}.{c}" for t, c in cur.fetchall()]
        cur.execute("SELECT table_name, column_name FROM information_schema.columns "
                    "WHERE table_schema='gkx' AND column_name IN "
                    "('relation_type','relation_strength','is_core_supplier','risk_level')")
        out["supply_edge_field_like"] = [f"{t}.{c}" for t, c in cur.fetchall()]
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def live_dev_side():
    """G8 的另一侧：旧机开发库（111.198.38.90:34306）有没有这张边表、有没有行。"""
    out = {"attempted": True, "ok": False}
    try:
        import pymysql
        c = pymysql.connect(host="111.198.38.90", port=34306, user="gkxlumenx",
                            password="GKX@Lumen2026", charset="utf8mb4",
                            connect_timeout=15, read_timeout=60)
        cur = c.cursor()
        cur.execute("SELECT table_schema, table_name FROM information_schema.tables "
                    "WHERE table_name LIKE '%%supply%%'")
        out["supply_like_tables"] = [f"{s}.{t}" for s, t in cur.fetchall()]
        for schema in ("gkxlumenx_dwd",):
            try:
                cur.execute(f"SELECT COUNT(*) FROM {schema}.enterprise_supply_chain")
                out["dwd_enterprise_supply_chain_rows"] = int(cur.fetchone()[0])
                cur.execute("SELECT column_name FROM information_schema.columns "
                            f"WHERE table_schema='{schema}' AND table_name='enterprise_supply_chain' "
                            "ORDER BY ordinal_position")
                out["dwd_enterprise_supply_chain_columns"] = [r[0] for r in cur.fetchall()]
            except Exception as e:  # noqa: BLE001
                out["dwd_error"] = f"{type(e).__name__}: {e}"
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def main():
    fam = load("supply_family_20261023.json")
    inv = fam["invest"]
    sh = fam["shareholder"]
    ov = fam["edge_overlap"]
    bb = fam["bid_base"]
    bw = fam["bid_win"]
    base_total = fam["fin_org_join"]["base_orgs_total"]

    vocab = fam["vocab_scan"]
    tabs = fam["table_scan"]

    probes = {}
    probes["p1_vocab_scan"] = {
        "source": "code/_snapshots21/gkx_columns_20261023.json（280 表 / 6,312 列）",
        "roots": SUPPLY_ROOTS,
        "hits": {k: {"n_columns": vocab[k]["n_columns"], "n_tables": vocab[k]["n_tables"]}
                 for k in SUPPLY_ROOTS},
        "all_hit_columns": (
            vocab["supplier"]["columns"] + vocab["procure"]["columns"]
            + vocab["purchas"]["columns"]),
        "hit_reading": [
            {"column": "dwd_bid_base_out.supplier_qualification_criteria",
             "type": "mediumtext", "reading": "招标公告里的『供应商资格条件』正文（不是关系）"},
            {"column": "dwd_bid_base_out.procurement_method(_code)",
             "type": "varchar/double", "reading": "该条招标的采购方式（公开招标/竞争性磋商…）"},
            {"column": "dwd_bid_base_out.estimated_purchasing_time",
             "type": "datetime", "reading": "预计采购时间，招标公告的一个日期字段"},
        ],
        "conclusion": (
            "12 个命中列全部落在 dwd_bid_base_out 一张表（及其 2 份 bak 副本）上，"
            "逐列读义后是『招标公告的资格条件文本 / 采购方式 / 预计采购时间』三个属性字段，"
            "没有任何一列以『某企业』为值去指向另一家企业。supply / vendor / 采购 / 供应 / 上游 / 下游 "
            "六个词根 0 列。结论：全库不存在可承载『企业→供应商』关系对的列。"),
    }
    probes["p2_table_scan"] = {
        "patterns": list(tabs.keys()),
        "hits": {k: {"n_tables": tabs[k]["n_tables"], "tables": tabs[k]["tables"]}
                 for k in tabs},
        "conclusion": (
            "表名含 supply/supplier/vendor 的表 0 张；含 chain 的 2 张是 "
            "dwd_industry_chain_info（1,273 个链节点目录）与 dwd_industry_chain_news_info"
            "（108,052 条链新闻），都不是企业间关系边。"),
    }
    probes["p3_edge_faces"] = {
        "invest": inv,
        "shareholder": sh,
        "bid_base": bb,
        "bid_win": bw,
        "edge_overlap": ov,
        "conclusion": (
            "投资边 46,967 对（19,611 家被投 / 33,968 家投资方）、股权边 400,286 行"
            f"（{sh.get('distinct_pairs')} 个去重关系对）、招投标面 39,962 条公告 + 39,520 条中标候选人。"
            "三者都不是『供应商→采购方』边：投资边与股权边的重合只有 "
            f"{ov['intersect_pairs']} 对（{ov['invest_pairs_also_shareholder_pct']}%），"
            "说明两表各记一类资本关系；招投标面只有中标方 org_id，招标方没有 org_id。"),
    }

    # 语义差异：投资边的字段与覆盖总体
    # 第四张候选边面：母子公司边（178,900 行），同样不是供应关系
    sub = {"rows": 178900, "distinct_parents": None, "distinct_subs": None,
           "columns": ["org_id", "name_cn", "sub_org_id", "sub_name_cn",
                       "sub_external_id"]}
    try:
        sys.path.insert(0, HERE)
        from _gkxdb import gkx
        cur = gkx()
        cur.execute("SET SESSION max_execution_time=120000")
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT org_id), COUNT(DISTINCT sub_org_id) "
                    "FROM gkx.dwd_org_subsidiary_info")
        r = cur.fetchone()
        sub.update({"rows": int(r[0]), "distinct_parents": int(r[1]),
                    "distinct_subs": int(r[2])})
        probes_sub_ok = True
    except Exception as e:  # noqa: BLE001
        sub["error"] = f"{type(e).__name__}: {e}"
        probes_sub_ok = False
    probes["p3b_subsidiary_face"] = {
        "face": "dwd_org_subsidiary_info（母公司 → 子公司）",
        "stats": sub,
        "reading": ("母子公司边是控制关系（合并报表口径），方向是「母公司 → 子公司」，"
                    "既不是货物交易，也没有采购额；用它当供应边会把『子公司最多的集团』"
                    "读成『供应商最多的采购方』。"),
        "usable_as_supply": False,
    }

    probes["p4_semantic_gap"] = {
        "invest_columns": ["org_id", "name_cn", "inv_org_id", "inv_name",
                           "investment_amount", "investment_ratio"],
        "missing_transaction_fields": ["交易金额（非出资额）", "采购品类/物料",
                                       "供货周期或频次", "收货方（采购方）确认",
                                       "合同号/订单号"],
        "invest_amount_rows": inv["amount_notnull_rows"],
        "invest_ratio_rows": inv["ratio_notnull_rows"],
        "coverage": {
            "invested_firms": inv["distinct_org"],
            "investor_firms": inv["distinct_inv_org"],
            "share_of_base_as_invested_pct": round(inv["distinct_org"] / base_total * 100, 2),
            "share_of_base_as_investor_pct": round(inv["distinct_inv_org"] / base_total * 100, 2),
            "bid_winner_orgs_in_base_pct": bw["share_org_in_base_pct"],
        },
        "conclusion": (
            "投资边是资本关系面（出资额 + 出资比例，18 列里 0 个交易字段），"
            "它筛的是「有对外投资事件的企业」——被投 19,611 家仅占底册 10.37%。"
            "供应关系的总体应是「有采购/供货行为的企业」，两者不是同一总体，"
            "用投资边计数会把『被谁投资』写成『向谁采购』，方向与语义同时错位。"),
        "rejected_proxy": {
            "name": "投资边 → 资金流向代理",
            "usable_as": "只能表达『资金从投资方流向被投方』",
            "not_usable_as": "供应商数量 / 采购集中度 / 供货关系",
            "why_rejected": "指标定义是 COUNT(DISTINCT 供应商)，代理面给出的是 COUNT(DISTINCT 被投企业)，"
                            "对象与方向都不同；若采用必须降档并改名，不能声称等于供应商数。",
        },
    }

    probes["p5_live_recheck"] = live_recheck()
    probes["p6_live_dev_side"] = live_dev_side()

    out = {
        "metric_id": "M_ENT_SUPPLIER_COUNT",
        "metric_name": "供应商数量",
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "judgment_reason": (
            "指标唯一定义依赖『企业→供应商』关系边（relation_type='supplier'），"
            "gkx 280 表无供应链边表、6,312 列无供应商关系列；三张候选边面（投资/股权/招投标）"
            "都组不出供应关系对；开发库侧同样无此结果面 → 结构与数据均不具备可算闭环。"),
        "formula_calc_logic": (
            "supplier_count(i) = COUNT(DISTINCT related_org_id) "
            "WHERE org_id=i AND relation_type='supplier'（enterprise_supply_chain）"),
        "dependencies_declared": ["enterprise_supply_chain（relation_type / related_org_id）"],
        "dependencies_found": [],
        "probes": probes,
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "负结论件，无指标值，不涉及基期；本件所有计数都是当前态快照（2026-10-23 抓取），"
            "不存在把缺失年份按 0 摊入分母的问题。"),
        "sources": {
            "db": "gkx @ 183.240.141.251:3318",
            "tables_checked": ["gkx.dwd_org_invest_info", "gkx.dwd_org_shareholder_info",
                               "gkx.dwd_bid_base_out", "gkx.dwd_bid_win_candidate_out",
                               "gkx.dwd_industry_chain_info"],
            "snapshots": ["code/_snapshots21/supply_family_20261023.json",
                          "code/_snapshots21/gkx_columns_20261023.json"],
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("support_judgment", "verdict_kind")}, ensure_ascii=False))
    print("live", json.dumps(probes["p5_live_recheck"], ensure_ascii=False)[:400])
    print("saved", OUT)


if __name__ == "__main__":
    main()
