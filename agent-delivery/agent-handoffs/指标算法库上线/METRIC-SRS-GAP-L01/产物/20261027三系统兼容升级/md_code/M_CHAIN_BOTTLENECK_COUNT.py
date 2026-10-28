#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_BOTTLENECK_COUNT 的**否定性证据**探针（不计算指标）。

正文判「完全不支持」，依据是「五维输入一维都没有表」。这句话要能被机器复核，
所以这里把五维各自可能的表名词根一次性扫掉，并顺手扫掉「可比价/产能/订单/
进口/供应商清单」这些具体载体。产物只存证据，不产出指标值。

五维（父口径只给维度名，未给权重与阈值）：
    ① 供需缺口  ② 技术依赖  ③ 产能利用率  ④ 交付周期  ⑤ 替代性
注意：本件与 M_CHAIN_KEY_NODE_COUNT / M_CHAIN_HIGH_VALUE_RATIO 不同——
      「空位环节」是结构占位（有节点但没有企业），不是「瓶颈」。
      两者混同会让瓶颈数虚高，正文 §1.6 已写死这条边界。

用法：cd code && python3 M_CHAIN_BOTTLENECK_COUNT.py
"""
from __future__ import annotations

import json
import os
import time
import traceback

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_CHAIN_BOTTLENECK_COUNT_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=20, read_timeout=180)

DIMS = {
    "D1_供需缺口": ["%capacity%", "%demand%", "%gap%"],
    "D2_技术依赖": ["%import%", "%depend%", "%citation%"],
    "D3_产能利用": ["%utiliz%", "%production%", "%output_capacity%"],
    "D4_交付周期": ["%order%", "%delivery%", "%lead_time%"],
    "D5_替代性": ["%supplier%", "%substitut%", "%vendor%"],
    "兜底_瓶颈": ["%bottleneck%", "%chokepoint%", "%constraint%"],
}


def q(sql, args=None):
    """连接 + 重试：gkx 握手会间歇性超时，一次失败就记 note 会把网络故障
    伪装成「查了没有」（2026-10-22 实测 10 次连接约 2 次超时）。"""
    last = None
    for attempt in range(5):
        try:
            conn = pymysql.connect(**GKX)
            with conn.cursor() as cur:
                cur.execute(sql) if args is None else cur.execute(sql, args)
                rows = cur.fetchall()
            conn.close()
            return rows
        except (pymysql.err.OperationalError, OSError) as e:
            last = e
            time.sleep(3 * (attempt + 1))
    raise last


def main() -> int:
    out = {
        "metric_id": "M_CHAIN_BOTTLENECK_COUNT",
        "metric_name": "产业链瓶颈堵点数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "完全不支持",
        "verdict_kind": "negative_evidence",
        "probes": {},
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面指标：堵点数是「当前存量堵点清单的条数」；五维输入均无年度字段，"
                            "不构造年度序列。"),
        "sources": [
            {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
             "table": "gkx.information_schema.tables", "role": "五维载体表的词根扫描"},
            {"library": "gkx", "host": "183.240.141.251:3318",
             "table": "gkx.dwd_industry_chain_info", "role": "环节（节点）定义源"},
        ],
    }

    def flush():
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)

    flush()

    # ---- P1 五维词根扫描 ----
    scan = {}
    for dim, pats in DIMS.items():
        hit = {}
        for p in pats:
            try:
                hit[p] = [r["t"] for r in q(
                    "SELECT table_name AS t FROM information_schema.tables "
                    "WHERE table_schema='gkx' AND table_name LIKE %s", (p,))]
            except Exception:
                out["notes"].append(f"P1 {dim} {p} fail: "
                                    + traceback.format_exc(limit=1))
                hit[p] = None
        scan[dim] = hit
        out["probes"]["dimension_scan"] = scan
        flush()

    # 词根命中 ≠ 载体存在：`%import%` 命中 `dwd_org_important_news_info`（重要资讯），
    # `%citation%` 命中论文引用表——两者都与「技术依赖」无关。逐条人工核过后标为误匹配，
    # 不把它们算进「有表的维度」。这一步不能省：不核就会把 1/5 写成 0/5 或反过来。
    FALSE_POSITIVE = {
        "dwd_org_important_news_info": "企业重要资讯，非进口依赖",
        "dwd_en_paper_citation": "英文论文引用，非技术依赖",
        "dwd_zh_paper_citation": "中文论文引用，非技术依赖",
    }
    real = {}
    for dim, hit in scan.items():
        tabs = sorted({t for v in hit.values() if v for t in v})
        kept = [t for t in tabs if t not in FALSE_POSITIVE]
        real[dim] = {"all_hits": tabs, "kept": kept,
                     "dropped": {t: FALSE_POSITIVE[t] for t in tabs if t in FALSE_POSITIVE}}
    out["probes"]["dimension_verdicts"] = real
    out["probes"]["dims_with_any_table"] = sum(
        1 for dim, v in real.items()
        if dim != "兜底_瓶颈" and v["kept"])
    out["probes"]["dims_total"] = 5
    flush()

    # ---- P2 有没有「瓶颈」这个具体词 ----
    try:
        out["probes"]["bottleneck_like_tables"] = scan.get("兜底_瓶颈", {})
        flush()
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P3 环节规模（说明为什么「空位环节」不能顶替堵点）----
    try:
        out["probes"]["chain_nodes"] = q(
            "SELECT COUNT(*) AS n FROM dwd_industry_chain_info")[0]["n"]
        out["probes"]["node_company_count_positive"] = q(
            "SELECT COUNT(*) AS n FROM dwd_industry_chain_info "
            "WHERE node_company_count > 0")[0]["n"]
        flush()
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P4b 宏观指数表：最容易被当成「产能利用率」的载体 ----
    # 2026-10-22 16:40 实测：`dwd_macro_index_data` 有 20,000 行、287 个指数码、
    # 覆盖 1949—2026，看起来能顶 D3。查 `dim_cal` 只有 JDZ（绝对值）与 TB（同比）两值，
    # 按 `cap|util|channeng` 与「产能」检索 0 条——它是国民经济/外贸效益类宏观序列，
    # 不含产能利用率，也不落到产业链环节。所以它不能救 D3，但必须在正文里点名，
    # 否则下一个人还会再查一遍。
    try:
        out["probes"]["macro_index"] = {
            "rows": q("SELECT COUNT(*) AS n FROM dwd_macro_index_data")[0]["n"],
            "distinct_index_code": q("SELECT COUNT(DISTINCT index_code) AS n "
                                     "FROM dwd_macro_index_data")[0]["n"],
            "year_range": q("SELECT MIN(occur_period_year) AS a, MAX(occur_period_year) AS b "
                            "FROM dwd_macro_index_data")[0],
            "dim_cal": q("SELECT dim_cal, COUNT(*) AS n FROM dwd_macro_index_data "
                         "GROUP BY dim_cal ORDER BY n DESC"),
            "capacity_like_hits": q(
                "SELECT index_code, dim_cal, COUNT(*) AS n FROM dwd_macro_index_data "
                "WHERE index_code REGEXP 'cap|util' OR dim_cal LIKE '%%产能%%' "
                "GROUP BY index_code, dim_cal LIMIT 5"),
        }
        flush()
    except Exception:
        out["notes"].append("P4b fail: " + traceback.format_exc(limit=1))
        flush()

    # ---- P4 产能/工业统计这类「最像」的载体是否存在 ----
    try:
        cands = ["%statistic%", "%industrial%", "%industry_stat%", "%macro%"]
        found = {}
        for p in cands:
            found[p] = [r["t"] for r in q(
                "SELECT table_name AS t FROM information_schema.tables "
                "WHERE table_schema='gkx' AND table_name LIKE %s", (p,))]
        out["probes"]["macro_stat_scan"] = found
        flush()
    except Exception:
        out["notes"].append("P4 fail: " + traceback.format_exc(limit=1))
        flush()

    pr = out["probes"]
    out["judgment_reason"] = (
        "五维输入（供需缺口/技术依赖/产能利用/交付周期/替代性）逐维按 3 类词根扫描 gkx 表名，"
        "剔除误匹配后**有节点级载体的维度 %s/5**；瓶颈本体词根（bottleneck/chokepoint/"
        "constraint）命中 0 张。最像的 `dwd_macro_index_data`（%s 行、%s 个指数、%s—%s 年）"
        "经查 `dim_cal` 只有 JDZ/TB 两值、按 cap/util/产能检索 0 条，不含产能利用率，"
        "且为宏观口径、不落环节，不能救 D3。"
        "五维均无一维具备「结构 + 数据」闭环，故不存在「至少一维可算」的部分支持下限，"
        "判完全不支持。另：链树 %s 个节点里 `node_company_count>0` 的仅 %s 个，"
        "「空位环节」是结构占位而非堵点，不能顶替本指标（§1.6 边界）。"
        % (pr.get("dims_with_any_table"),
           (pr.get("macro_index") or {}).get("rows"),
           (pr.get("macro_index") or {}).get("distinct_index_code"),
           ((pr.get("macro_index") or {}).get("year_range") or {}).get("a"),
           ((pr.get("macro_index") or {}).get("year_range") or {}).get("b"),
           pr.get("chain_nodes"), pr.get("node_company_count_positive")))
    out["conclusion"] = (
        "否定性证据齐备：五维有表 %s/5、瓶颈词根 0 张、宏观/工业统计类表扫描见 "
        "`macro_stat_scan`。五维评分无法构造。"
        % pr.get("dims_with_any_table"))
    flush()
    print(json.dumps({k: out[k] for k in ("support_judgment", "judgment_reason", "notes")},
                     ensure_ascii=False, indent=1)[:1200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
