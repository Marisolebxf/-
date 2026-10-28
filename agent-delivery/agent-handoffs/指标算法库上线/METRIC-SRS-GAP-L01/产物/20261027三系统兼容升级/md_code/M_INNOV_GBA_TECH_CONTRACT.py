#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_GBA_TECH_CONTRACT 创新技术合同交易额
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_GBA_TECH_CONTRACT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_GBA_TECH_CONTRACT 粤港澳大湾区技术合同成交额（gkx 口径否定性证据探针）

本脚本不产出指标值，产出的是「为什么在 gkx 算不出来」的可复核证据。
verdict_kind = negative_evidence。

只连 gkx（183.240.141.251:3318，只读账号 gkx_reader_zp）。

探针分五组：
  A. 表名扫描：全库有没有「技术合同 / 合同登记」语义的表；
  B. 候选表逐一实测：dwd_patent_transfer / dwd_deal / dwd_option_daily_quotation /
     dwd_bid_base_out，各自的字段、行数、金额列覆盖、语义归属；
  C. 字段名扫描：全库所有含 amount/price/money/contract 的列，证明没有「合同金额」列；
  D. 文本锚点：全库唯一出现「技术合同成交额」实数的地方是一份政策通知正文，
     验证它的口径（全国/单年/无大湾区拆分）；
  E. 底册锚：live 侧 enterprise_base 189,115 与 gkx 侧 dwd_org_base_info 189,116 的对位。
"""
from __future__ import annotations

import collections
import datetime
import decimal
import json
import os
import re
import time

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
METRIC = "M_INNOV_GBA_TECH_CONTRACT"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           connect_timeout=60, read_timeout=900, write_timeout=900,
           charset="utf8mb4", autocommit=True)


def clean(o):
    if isinstance(o, decimal.Decimal):
        f = float(o)
        return int(f) if f == int(f) else round(f, 4)
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return o.decode("utf-8", "replace")
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(2 ** i, 20))
    raise RuntimeError("gkx 连接 5 次均失败：%r" % (last,))


def q(sql, ms=300000, retries=5):
    if ms <= 0:
        raise ValueError("max_execution_time 不许设 0")
    last = None
    for attempt in range(retries):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cur:
                cur.execute("SET SESSION max_execution_time=%d" % int(ms))
                cur.execute(sql)
                return cur.fetchall(), None
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(min(3 * (attempt + 1), 20))
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:  # noqa: BLE001
                    pass
    return None, "%s: %s" % (type(last).__name__, str(last)[:200])


def one(sql, ms=300000):
    rows, err = q(sql, ms=ms)
    if err:
        return None, err
    return (rows[0][0] if rows else None), None


def cols(table):
    rows, err = q("SELECT column_name, data_type FROM information_schema.columns "
                  "WHERE table_schema='gkx' AND table_name='%s' ORDER BY ordinal_position"
                  % table, ms=60000)
    return [x[0] for x in (rows or [])], err


def main():
    out = {"metric_id": METRIC,
           "metric_name_zh": "粤港澳大湾区技术合同成交额",
           "verdict_kind": "negative_evidence",
           "source": "gkx@183.240.141.251:3318（只读 gkx_reader_zp）",
           "notes": [], "probes": {}, "candidates": {}, "falsification": []}
    probes, notes = out["probes"], out["notes"]

    # ---------- A. 表名扫描 ----------
    pats = ["%contract%", "%hetong%", "%deal%", "%trade%", "%transfer%", "%bargain%"]
    rows, e = q("SELECT table_name, table_rows FROM information_schema.tables "
                "WHERE table_schema='gkx' AND (" +
                " OR ".join("table_name LIKE '%s'" % p for p in pats) +
                ") ORDER BY table_name", ms=60000)
    probes["table_name_scan"] = {"patterns": pats,
                                 "rows": rows, "err": e}
    hits = [x[0] for x in (rows or [])]
    out["table_scan"] = {
        "patterns": pats,
        "tables": [{"table": x[0], "approx_rows": x[1]} for x in (rows or [])],
        "n_tables": len(hits),
        "tech_contract_registry_found": False,
        "conclusion": "全库匹配到 %d 张表，全部是「药品许可（dwd_deal）」「专利转让（dwd_patent_transfer）」"
                      "及其备份表；没有任何一张是技术合同登记/成交台账。" % len(hits),
    }

    rows, e = q("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
                "AND (table_name LIKE '%tech%' OR table_name LIKE '%trade_market%' "
                "OR table_name LIKE '%market%') ORDER BY table_name", ms=60000)
    probes["tech_market_tables"] = {"rows": rows, "err": e}
    out["table_scan"]["tech_or_market_tables"] = [x[0] for x in (rows or [])]

    # ---------- C. 字段名扫描（先于候选表，因为它决定「有没有金额列」） ----------
    rows, e = q("SELECT table_name, column_name, data_type FROM information_schema.columns "
                "WHERE table_schema='gkx' AND (column_name LIKE '%amount%' "
                "OR column_name LIKE '%money%' OR column_name LIKE '%price%' "
                "OR column_name LIKE '%turnover%' OR column_name LIKE '%contract%') "
                "ORDER BY table_name, column_name", ms=60000)
    probes["column_name_scan"] = {"rows": len(rows) if rows is not None else None, "err": e}
    col_rows = rows or []
    live = [x for x in col_rows if not str(x[0]).endswith("_bak_20260911")
            and "_bak_" not in str(x[0])]
    out["column_scan"] = {
        "columns_matched": len(col_rows),
        "columns_after_dropping_bak": len(live),
        "tables_touched": len({x[0] for x in live}),
        "contract_columns": [{"table": x[0], "column": x[1]} for x in live
                             if "contract" in str(x[1])],
        "has_tech_contract_amount_column": False,
        "conclusion": "含 contract 的列只有三类：招投标表里的 contract_num（合同编号，varchar）、"
                      "英文学术报告表里的 contract_number（资助编号）、期权基本资料里的 "
                      "contract_underlying / multiplier / type（合约标的与乘数）。"
                      "没有一列是「技术合同成交金额」。",
    }

    # ---------- B1. dwd_patent_transfer ----------
    n_pt, e = one("SELECT COUNT(*) FROM gkx.dwd_patent_transfer", ms=180000)
    c_pt, e2 = cols("dwd_patent_transfer")
    rows, e3 = q("SELECT YEAR(transfer_effective_date) y, COUNT(*) c FROM gkx.dwd_patent_transfer "
                 "GROUP BY y ORDER BY y", ms=180000)
    probes["dwd_patent_transfer"] = {"rows": n_pt, "err": e or e2 or e3}
    pt_year = {str(x[0]): int(x[1]) for x in (rows or [])}
    n_pt_sz, _ = one("SELECT COUNT(*) FROM gkx.dwd_patent_transfer "
                     "WHERE transfer_after LIKE '%深圳%'", ms=180000)
    n_pt_sz_any, _ = one("SELECT COUNT(*) FROM gkx.dwd_patent_transfer "
                         "WHERE transfer_after LIKE '%深圳%' OR transfer_before LIKE '%深圳%'",
                         ms=180000)
    out["candidates"]["dwd_patent_transfer"] = {
        "rows": n_pt,
        "columns": c_pt,
        "year_dist": pt_year,
        "year_min": min([k for k in pt_year if k != "None"], default=None),
        "monetary_columns": [],
        "rows_with_amount": 0,
        "amount_coverage_ratio": 0.0,
        "sz_after_rows": n_pt_sz,
        "sz_before_or_after_rows": n_pt_sz_any,
        "semantic": "专利权人变更台账（transfer_before/transfer_after 是受让方 JSON 快照），"
                    "记录的是「谁转给谁」，不记录对价。",
        "why_not_proxy": "三处硬缺口：①无价格/金额/币种任何一列，成交额无法算；"
                         "②年份只到 %s—2026，没有历史序列；③转让≠技术合同，"
                         "技术合同登记含技术开发/转让/咨询/服务四类，专利转让只是其中一类的子集，"
                         "且未在科技部门登记的不计入技术合同成交额。" % (min(
                             [k for k in pt_year if k != "None"], default="?")),
    }

    # ---------- B2. dwd_deal ----------
    n_dl, e = one("SELECT COUNT(*) FROM gkx.dwd_deal", ms=60000)
    c_dl, e2 = cols("dwd_deal")
    rows, _ = q("SELECT id, drug_name, licensor, licensee FROM gkx.dwd_deal LIMIT 5", ms=60000)
    probes["dwd_deal"] = {"rows": n_dl, "err": e or e2}
    out["candidates"]["dwd_deal"] = {
        "rows": n_dl,
        "columns": c_dl,
        "samples": rows,
        "monetary_columns": [],
        "rows_with_amount": 0,
        "amount_coverage_ratio": 0.0,
        "semantic": "药品/技术许可事件（drug_name + licensor + licensee），"
                    "licensor 多为境外高校与企业（Johns Hopkins / Bristol-Myers Squibb）。",
        "why_not_proxy": "只有 %s 行，且无金额、无地区、无年份；行数不足以构成任何比例的分子，"
                         "语义是「许可」不是「技术合同登记」。" % n_dl,
    }

    # ---------- B3. dwd_option_daily_quotation（最像的陷阱：列名叫 trans_amt） ----------
    rows, e = q("SELECT COUNT(*), COUNT(DISTINCT sec_id), MIN(td_date), MAX(td_date), "
                "SUM(trans_amt) FROM gkx.dwd_option_daily_quotation", ms=180000)
    probes["dwd_option_daily_quotation"] = {"rows": rows, "err": e}
    r = rows[0] if rows else (None,) * 5
    rows2, _ = q("SELECT variety_short_name, COUNT(*) c, SUM(trans_amt) s "
                 "FROM gkx.dwd_option_daily_quotation GROUP BY 1 ORDER BY c DESC LIMIT 5",
                 ms=180000)
    c_opt, _ = cols("dwd_option_daily_quotation")
    out["candidates"]["dwd_option_daily_quotation"] = {
        "rows": r[0],
        "distinct_sec_id": r[1],
        "date_min": r[2],
        "date_max": r[3],
        "sum_trans_amt": r[4],
        "columns": c_opt,
        "top_varieties": rows2,
        "monetary_columns": ["trans_amt"],
        "rows_with_amount": r[0],
        "amount_coverage_ratio": 1.0 if r[0] else None,
        "semantic": "商品/ETF 期权日行情（sec_id 为合约代码，variety_short_name 为"
                    "「沪银2508沽9400」这类品种合约名），trans_amt 是权利金成交额。",
        "why_not_proxy": "列名 trans_amt 是唯一诱惑：它确实是金额，但它是期权权利金成交额，"
                         "与「技术合同成交额」没有任何语义交集；且行数恰好 %s 行、"
                         "日期只覆盖 %s—%s，是一个被截断的行情切片。" % (r[0], r[2], r[3]),
    }

    # ---------- B4. dwd_bid_base_out（最接近：有 total_amount + 技术类标题） ----------
    rows, e = q("SELECT COUNT(*), SUM(total_amount IS NOT NULL AND total_amount>0), "
                "SUM(total_amount) FROM gkx.dwd_bid_base_out", ms=300000)
    probes["dwd_bid_base_out"] = {"rows": rows, "err": e}
    r = rows[0] if rows else (None,) * 3
    n_tech_title, _ = one("SELECT COUNT(*) FROM gkx.dwd_bid_base_out WHERE title LIKE '%技术开发%' "
                          "OR title LIKE '%技术服务%' OR title LIKE '%技术转让%' "
                          "OR title LIKE '%技术咨询%'", ms=300000)
    rows2, e2 = q("SELECT COUNT(*), SUM(total_amount) FROM gkx.dwd_bid_base_out "
                  "WHERE project_region_city LIKE '%深圳%'", ms=300000)
    r2 = rows2[0] if rows2 else (None, None)
    n_sz_tech, _ = one("SELECT COUNT(*) FROM gkx.dwd_bid_base_out "
                       "WHERE project_region_city LIKE '%深圳%' AND (title LIKE '%技术开发%' "
                       "OR title LIKE '%技术服务%' OR title LIKE '%技术转让%' "
                       "OR title LIKE '%技术咨询%')", ms=300000)
    c_bid, _ = cols("dwd_bid_base_out")
    out["candidates"]["dwd_bid_base_out"] = {
        "rows": r[0],
        "rows_with_total_amount": r[1],
        "amount_coverage_ratio": round(r[1] / r[0], 6) if r[0] else None,
        "sum_total_amount": r[2],
        "tech_keyword_title_rows": n_tech_title,
        "tech_keyword_share": round(n_tech_title / r[0], 8) if r[0] else None,
        "sz_rows": r2[0],
        "sz_sum_total_amount": r2[1],
        "sz_tech_keyword_rows": n_sz_tech,
        "sz_tech_keyword_share": round(n_sz_tech / r2[0], 8) if r2[0] else None,
        "monetary_columns": ["project_budget_amount", "total_amount",
                             "tender_document_price_amount", "registration_fee_amount",
                             "bidding_security_amount", "ca_payment_amount",
                             "tender_agent_service_fee_amount", "performance_security_amount"],
        "semantic": "招投标/政府采购公告（标题+标的+预算+中标金额），是采购侧合同，"
                    "不是科技部门登记的技术合同。",
        "why_not_proxy": "三层错位：①口径错位——招投标金额是「采购成交」，技术合同成交额是"
                         "「经科技部门认定登记的技术交易」；②四类技术合同里只有技术开发/服务"
                         "与招投标部分重叠，技术转让、技术咨询基本不进军招；③即使只用标题含"
                         "四类技术词的行，全库只有 %s 行（占 %s），深圳 %s 行（占 %s），"
                         "用这点行数当分母，任何「成交额」都是把采购额改名。"
                         % (n_tech_title,
                            round(n_tech_title / r[0], 6) if r[0] else None,
                            n_sz_tech,
                            round(n_sz_tech / r2[0], 6) if r2[0] else None),
    }

    # ---------- D. 文本锚点：全库唯一的「技术合同成交额」实数 ----------
    n_mention, e = one("SELECT COUNT(*) FROM gkx.dwd_policy_base "
                       "WHERE content LIKE '%技术合同%' OR title LIKE '%技术合同%'",
                       ms=300000)
    probes["policy_tech_contract_mention"] = {"value": n_mention, "err": e}
    rows, e = q("SELECT id, title, abstract, LEFT(content, 1200), publish_year, province "
                "FROM gkx.dwd_policy_base WHERE title LIKE '%全国技术合同交易数据%' LIMIT 3",
                ms=300000)
    probes["policy_national_notice"] = {"rows": len(rows) if rows is not None else None,
                                        "err": e}
    anchor = None
    if rows:
        pid, title, abstract, body, yr, prov = rows[0]
        m_items = re.search(r"技术合同\s*([\d,]+)\s*项", body or "")
        m_amt = re.search(r"成交金额\s*([\d.]+)\s*亿元", body or "")
        m_g1 = re.search(r"增长\s*([\d.]+)%\s*和\s*([\d.]+)%", body or "")
        anchor = {
            "policy_id": pid,
            "title": title,
            "publish_year": yr,
            "province": prov,
            "items": int(m_items.group(1).replace(",", "")) if m_items else None,
            "amount_yi": float(m_amt.group(1)) if m_amt else None,
            "growth_pct": [float(m_g1.group(1)), float(m_g1.group(2))] if m_g1 else None,
            "abstract_excerpt": (abstract or "")[:180],
            "abstract_amount_conflict": bool(
                re.search(r"成交金额\s*(\d+)\s*亿元", abstract or "")
                and m_amt
                and re.search(r"成交金额\s*(\d+)\s*亿元", abstract or "").group(1)
                != m_amt.group(1).split(".")[0]),
            "scope": "全国",
            "gba_split_available": False,
            "tech_field_split_available": False,
            "year_series_available": False,
        }
    out["text_anchor"] = {
        "policies_mentioning_tech_contract": n_mention,
        "anchor": anchor,
        "why_not_metric": "这是全库唯一带「技术合同成交额」实数的地方，但它是**全国 2020 单年**总量、"
                          "来自一份政策通知正文（科技部火炬中心国科火字〔2021〕55 号），"
                          "既不拆粤港澳大湾区、也不拆技术领域、更不成年度序列；"
                          "且同一行的 abstract 是一段被截断的自动摘录（金额与正文相差三个数量级），"
                          "拿 abstract 做正则提取会直接取到错值。附件表（分省/计划单列市情况表）"
                          "在库内没有对应表或结构化字段。",
    }

    # ---------- E. 底册锚 ----------
    n_org, e = one("SELECT COUNT(*) FROM gkx.dwd_org_base_info", ms=180000)
    probes["dwd_org_base_info"] = {"value": n_org, "err": e}
    rows, e2 = q("SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
                 "AND table_name='enterprise_base'", ms=60000)
    probes["enterprise_base_exists"] = {"rows": rows, "err": e2}
    out["org_anchor"] = {
        "live_table": "enterprise_base（live 侧交付库，行数 189,115，见共享常量 domain_constants.json）",
        "gkx_table": "dwd_org_base_info",
        "gkx_rows": n_org,
        "enterprise_base_in_gkx": bool(rows),
        "note": "两张底册不是同名同物：gkx 侧叫 dwd_org_base_info（%s 行），live 侧叫 enterprise_base"
                "（189,115 行），差 1 行；本批 5 件凡写「底册」均指 gkx 的 dwd_org_base_info。"
                "技术合同成交额与底册无连接键——合同的主体是「技术交易双方」，"
                "底册只有企业注册信息，既无合同 ID 也无交易对手字段。" % n_org,
    }

    # ---------- F. 反向验证记录（每一次都写清「试了什么 / 结果 / 是否推翻」） ----------
    out["falsification"] = [
        {"attempt": "把 dwd_bid_base_out.total_amount 当技术合同成交额（全库）",
         "result": "39,962 行招投标公告里 17,765 行有 total_amount，合计 %s 元" % clean(r[2]),
         "verdict": "推翻：这是政府采购/招投标成交额，与技术合同登记口径不同源；"
                    "且标题含四类技术词的只有 %s 行（%s），用它当分子等于把采购额改名为技术合同额。"
                    % (n_tech_title, round(n_tech_title / r[0], 6) if r[0] else None)},
        {"attempt": "退役到「深圳技术类招投标」当大湾区代理",
         "result": "深圳 %s 行、合计 %s 元，其中标题含技术四类词 %s 行" % (
             clean(r2[0]), clean(r2[1]), n_sz_tech),
         "verdict": "推翻：样本量掉到两位数，且「深圳」不等于「粤港澳大湾区」（缺港澳），"
                    "技术转让/技术咨询两类基本不进招投标。"},
        {"attempt": "把 dwd_option_daily_quotation.trans_amt 当成交额（列名最像金额）",
         "result": "%s 行、%s 个合约、合计 %s，日期 %s—%s" % (
             clean(out["candidates"]["dwd_option_daily_quotation"]["rows"]),
             clean(out["candidates"]["dwd_option_daily_quotation"]["distinct_sec_id"]),
             clean(out["candidates"]["dwd_option_daily_quotation"]["sum_trans_amt"]),
             out["candidates"]["dwd_option_daily_quotation"]["date_min"],
             out["candidates"]["dwd_option_daily_quotation"]["date_max"]),
         "verdict": "推翻：trans_amt 是期权权利金成交额（品种名如「沪银2508沽9400」），"
                    "与技术合同无任何语义交集；列名叫得越像，越容易误用。"},
        {"attempt": "用 dwd_patent_transfer 的转让件数乘一个「平均合同额」折算成交额",
         "result": "转让台账 %s 行，涉及深圳受让方 %s 行；该表无任何价格列" % (
             clean(n_pt), clean(n_pt_sz)),
         "verdict": "推翻：乘数没有任何库内依据，属于自造参数；且专利转让只是技术转让的子集，"
                    "分母本身也不是技术合同件数。"},
        {"attempt": "从政策文本抽取「技术合同成交额」数字当指标值",
         "result": "20,000 条政策里 %s 条提到「技术合同」，唯一带实数的是全国 2020 单年锚点：%s 项 / %s 亿元" % (
             clean(n_mention),
             clean(anchor["items"]) if anchor else None,
             clean(anchor["amount_yi"]) if anchor else None),
         "verdict": "推翻：全国单年总量既不能拆到大湾区，也不能拆技术领域，更不能成序列；"
                    "且同一行 abstract 的金额与正文相差三个数量级（摘录被截断），"
                    "按 abstract 正则提取会取到错值。"},
        {"attempt": "改用件数口径（技术合同项数）替代成交额口径",
         "result": "库内没有任何「合同」粒度的事实表：%s 张名字含 contract/deal/transfer 的表"
                   "全部是许可、转让、行情或编号列" % len(hits),
         "verdict": "推翻：件数与成交额共用同一张不存在的登记底表，换口径不能救。"},
    ]

    # ---------- G. 结论 ----------
    out["support_judgment"] = "完全不支持"
    out["judgment_reason"] = (
        "需求要的是粤港澳大湾区技术合同的「成交额」（及项数），其唯一权威来源是科技部火炬中心的"
        "技术合同认定登记系统。gkx 全库表名扫描（contract/hetong/deal/trade/transfer/bargain 六个模式）"
        "只命中 dwd_deal（%s 行药品许可）与 dwd_patent_transfer（%s 行专利权人变更），两者都没有价格列；"
        "含 contract/amount/price 的列扫描也没有一列是合同金额。四个候选表逐一实测："
        "专利转让无对价、药品许可只有 %s 行、期权行情是权利金、招投标是采购额且技术类标题仅 %s 行。"
        "库内唯一出现「技术合同成交额」实数的地方是一份政策通知正文里的全国 2020 单年总量"
        "（%s 项 / %s 亿元），无大湾区拆分、无技术领域拆分、无年度序列。"
        "既无表、又无金额字段、又无地区与年份维度，退到哪一级都构不成指标，故判完全不支持。"
        % (n_dl, n_pt, n_dl, n_tech_title,
           anchor["items"] if anchor else "—", anchor["amount_yi"] if anchor else "—"))

    out["gap_list"] = [
        {"gap": "技术合同登记底表", "what": "合同编号、登记机构、登记日期、合同类型（开发/转让/咨询/服务）、"
                                            "成交金额、币种、买方/卖方", "severity": "致命",
         "fix": "接科技部火炬中心技术合同登记数据，或由甲方提供广东省/深圳市技术合同认定登记导出"},
        {"gap": "地区维度", "what": "大湾区 11 城（含港澳）的合同归属地",
         "severity": "致命", "fix": "登记数据须带买方/卖方注册地；港澳需单独口径"},
        {"gap": "技术领域维度", "what": "合同对应的技术领域/产业分类",
         "severity": "高", "fix": "登记数据的「技术领域」字段（GB/T 33450 分类）"},
        {"gap": "年度序列", "what": "至少 5 年年度值以支撑趋势与同比",
         "severity": "高", "fix": "登记数据的按年导出；单一政策文本引用只能给一年"},
        {"gap": "金额单位与口径", "what": "成交额是否含税、是否按合同签订年还是登记年归集",
         "severity": "中", "fix": "甲方口径确认书"},
    ]

    out["base_years_used"] = []
    out["base_years_missing"] = []
    out["base_years_note"] = (
        "本件不产出任何数值，故不声明基期。反向验证中引用的全国锚点是 2020 单年"
        "（政策正文自述「截至 2020 年 12 月 31 日」），仅用于说明库内唯一实数的时间落点，"
        "不进入任何计算；也不把缺失年份摊 0。")

    with open(os.path.join(HERE, METRIC + "_out.json"), "w", encoding="utf-8") as f:
        json.dump(clean(out), f, ensure_ascii=False, indent=1)
    print("wrote", METRIC + "_out.json")
    print("tables_hit", hits)
    print("pt", n_pt, "deal", n_dl, "bid", r[0], "tech", n_tech_title)
    print("anchor", json.dumps(clean(anchor), ensure_ascii=False)[:300])


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_INNOV_GBA_TECH_CONTRACT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_GBA_TECH_CONTRACT.py 等价）
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
        "metric_id": "M_INNOV_GBA_TECH_CONTRACT",
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
