#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_DEVELOPMENT_MILESTONE_COUNT 产业链发展里程碑数（W14-C2，零 DB）。

calc-logic 的真源是 `industry_chain_milestone_event`（按 milestone_type 三类：
重大技术突破 / 政策出台 / 龙头入驻，阈值判定的重大事件去重计数）。
gkx 侧没有这张表（280 表里 milestone/event 相关只有 20 行的 dwd_event），
live 侧同名表也不存在。本件按「可复算布尔规则」重建两类，第三类如实置空：

  A 政策出台里程碑：链 × 年 的政策命中数 >= 5 → 记 1 个里程碑
     源：policy_industry_20261023.json 的 year_chain_t0（T0 精确链名命中）
  B 龙头入驻里程碑：2021—2026 年、金额 >= 5 亿元、名称可映射到链的融资事件
     源：chain21_fin_degree_20261022.json + chain_firm_index_20261023.json
     金额文本解析（万/亿/人民币；外币与空值剔除）
  C 重大技术突破：不可算 —— 无事件表、资讯表无 event_type/level 列、
     专利表无「技术突破」标签，本件不给代理值（null），只留否定性证据

里程碑数（主值）= A + B；C 单列 null。阈值 5 条/5 亿元为本件自定义，
另给 3/10 条与 1/10 亿元敏感性。

纯快照复算，不连库。
"""
from __future__ import annotations

import json
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
POLICY_MIN = 5
FIN_WAN = 50000.0          # 5 亿元 = 50,000 万元
FIN_YEARS = range(2021, 2027)
AMOUNT = re.compile(r"^\s*([\d.]+)\s*(万|亿)?\s*(人民币|美元|港元|欧元|元)?\s*$")
FIN_EXCLUDE = re.compile(r"(保险|证券|银行|信托|基金|资管|资产管理|金融|期货|人寿|财险)")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as fh:
        return json.load(fh)


def parse_wan(text):
    """融资额文本 → 万元（仅人民币/无币种）。外币、空值、无法解析返回 None。"""
    if not text or not str(text).strip():
        return None
    m = AMOUNT.match(str(text))
    if not m:
        return None
    cur = m.group(3) or ""
    if cur not in ("", "人民币", "元"):
        return None
    v = float(m.group(1))
    unit = m.group(2)
    if unit == "亿":
        return v * 10000.0
    if unit == "万":
        return v
    return v / 10000.0


def main() -> None:
    tree = load("chain_tree_20261021.json")
    idx = load("chain_firm_index_20261023.json")
    policy = load("policy_industry_20261023.json")
    fin = load("chain21_fin_degree_20261022.json")["fin"]
    probe = load("chain_live_result_probe_20261023.json")

    roots = sorted(n["industry_code"] for n in tree if len(n["industry_code"]) == 7)
    chain_name = idx["chain_name"]
    name_chain = idx["name_chain"]

    # ---------- A 政策出台 ----------
    year_cells = []
    for y, d in policy["year_chain_t0"].items():
        for ch, n in d.items():
            if ch in chain_name:
                year_cells.append({"year": int(y), "chain_code": ch, "policies": n})
    year_cells.sort(key=lambda x: (x["year"], x["chain_code"]))
    pol_events = {ch: 0 for ch in roots}
    pol_years = {ch: [] for ch in roots}
    for c in year_cells:
        pol_events[c["chain_code"]] += c["policies"]
        if c["policies"] >= POLICY_MIN:
            pol_years[c["chain_code"]].append(c["year"])
    pol_milestones = {ch: len(pol_years[ch]) for ch in roots}

    # ---------- B 龙头入驻（重大投融资代理）----------
    parsed = {"cnys": 0, "foreign": 0, "blank": 0, "unparsed": 0}
    mapped_events = []
    fin_excluded = 0
    for r in fin:
        nm, amt_text, d = r[1], r[4], r[6]
        y = (d or "")[:4]
        ch = name_chain.get(nm)
        wan = parse_wan(amt_text)
        if not str(amt_text or "").strip():
            parsed["blank"] += 1
        elif wan is None:
            m = AMOUNT.match(str(amt_text))
            if m and (m.group(3) or "") in ("美元", "港元", "欧元"):
                parsed["foreign"] += 1
            else:
                parsed["unparsed"] += 1
        else:
            parsed["cnys"] += 1
        if FIN_EXCLUDE.search(nm or ""):
            fin_excluded += 1
            continue
        if not ch or wan is None or not y.isdigit() or int(y) not in FIN_YEARS:
            continue
        mapped_events.append({
            "event_id": r[0],
            "company": nm,
            "credit_code": r[2],
            "round": r[3],
            "amount_text": amt_text,
            "amount_wan": wan,
            "amount_yi": round(wan / 10000.0, 4),
            "date": d,
            "year": int(y),
            "investor": r[7],
            "chain_code": ch,
            "chain_name": chain_name[ch],
        })

    # 源表 event_id 是「企业级」而非「轮次级」：25,654 行只有 6,503 个 id，且没有一个 id
    # 跨企业。若按 calc-logic 字面的 COUNT(DISTINCT event_id)，同一企业多轮融资会被压成 1 条。
    # 本件改用 (event_id, date, amount_wan) 复合键：保留不同轮次，剔除重复落库行；
    # 该偏离已写入 gaps，供甲方确认。
    seen_ev = set()
    dedup_events = []
    for e in mapped_events:
        k = (e["event_id"], e["date"], e["amount_wan"])
        if k in seen_ev:
            continue
        seen_ev.add(k)
        dedup_events.append(e)
    fin_rows_unique = len(dedup_events)
    mapped_events = dedup_events

    fin_milestones = {ch: 0 for ch in roots}
    fin_firms = {ch: set() for ch in roots}
    fin_amount = {ch: 0.0 for ch in roots}
    big_events = []
    for e in mapped_events:
        if e["amount_wan"] < FIN_WAN:
            continue
        fin_milestones[e["chain_code"]] += 1
        fin_firms[e["chain_code"]].add(e["credit_code"] or e["company"])
        fin_amount[e["chain_code"]] += e["amount_wan"]
        big_events.append(e)

    # ---------- 汇总 ----------
    rows = []
    for ch in roots:
        a, b = pol_milestones[ch], fin_milestones[ch]
        rows.append({
            "chain_code": ch,
            "chain_name": chain_name[ch],
            "policy_milestones": a,
            "policy_years": pol_years[ch],
            "policy_events_all_years": pol_events[ch],
            "investment_milestones": b,
            "investment_firms": len(fin_firms[ch]),
            "investment_amount_yi": round(fin_amount[ch] / 10000.0, 2),
            "tech_breakthrough_milestones": None,
            "milestone_total": a + b,
        })
    total = sum(r["milestone_total"] for r in rows)
    rows.sort(key=lambda r: -r["milestone_total"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    # ---------- 敏感性 ----------
    pol_sens = {}
    for th in (3, POLICY_MIN, 10):
        cnt = sum(1 for c in year_cells if c["policies"] >= th)
        pol_sens[str(th)] = cnt
    fin_sens = {}
    for th_yi in (1, 5, 10):
        fin_sens[str(th_yi)] = sum(1 for e in mapped_events if e["amount_wan"] >= th_yi * 10000.0)

    by_year_pol = {}
    for c in year_cells:
        by_year_pol[str(c["year"])] = by_year_pol.get(str(c["year"]), 0) + c["policies"]
    by_year_fin = {}
    for e in big_events:
        by_year_fin[str(e["year"])] = by_year_fin.get(str(e["year"]), 0) + 1
    by_year_events = {}
    for c in year_cells:
        if c["policies"] >= POLICY_MIN:
            by_year_events[str(c["year"])] = by_year_events.get(str(c["year"]), 0) + 1

    out = {
        "metric_id": "M_CHAIN_DEVELOPMENT_MILESTONE_COUNT",
        "metric_name": "产业链发展里程碑数",
        "support_judgment": "部分支持",
        "verdict_kind": "positive_evidence",
        "judgment_reason": (
            "calc-logic 的真源 industry_chain_milestone_event 两库均无（gkx 280 表 milestone 零命中，"
            "唯一事件表 dwd_event 只有 20 行且无链键；live 同名表不存在）。三类里程碑里，"
            "政策出台可用政策×链×年命中重建、龙头入驻可用大额融资事件代理，两类都能按链汇总并下钻到事件；"
            "重大技术突破既无事件表、资讯表也没有 event_type/level 字段、专利表无突破标签，"
            "无法用可核口径识别，只能置 null 并留否定性证据。三类缺一类，故判部分支持。"
        ),
        "base_years_used": [2021, 2022, 2023, 2024, 2025],
        "base_years_missing": [],
        "base_years_note": (
            "融资侧窗口 2021—2026（2026 只到 10 月，属残年，按事件实际发生计，不做年化外推）；"
            "政策侧政策表的 publish_year 最新只到 2022，2023 及以后零条，故政策里程碑只用 2001—2022 的"
            "真实年份，不把缺失年按 0 摊进任何分母。base_years_used 列融资主窗口 2021—2025。"
        ),
        "sources": [
            "code/_snapshots21/chain_tree_20261021.json",
            "code/_snapshots21/chain_firm_index_20261023.json",
            "code/_snapshots21/policy_industry_20261023.json",
            "code/_snapshots21/chain21_fin_degree_20261022.json",
            "code/_snapshots21/chain_live_result_probe_20261023.json",
        ],
        "rule": {
            "policy": f"链 × 年 政策命中数 >= {POLICY_MIN} 记 1 个政策里程碑（T0 精确链名命中）",
            "investment": f"2021—2026 年金额 >= {int(FIN_WAN / 10000)} 亿元人民币、名称可映射到链的融资事件记 1 个",
            "tech": "不可算：无事件表 / 无 event_type / 无突破标签，不给代理值",
            "total": "milestone_total = policy_milestones + investment_milestones；tech 单列 null",
            "amount_parse": "只认人民币（含无币种）；美元/港元/欧元与空值剔除，不换算汇率",
            "fin_exclude": "剔除名称含 保险/证券/银行/信托/基金/资管/金融/期货 的主体（金融机构增资不是产业入驻）",
            "dedupe": "按 (event_id, date, amount_wan) 复合键去重；企业家数按 credit_code 去重",
        },
        "params": {
            "policy_min": POLICY_MIN,
            "fin_threshold_wan": FIN_WAN,
            "fin_threshold_yi": FIN_WAN / 10000.0,
            "fin_years": list(FIN_YEARS),
            "policy_sensitivity": pol_sens,
            "investment_sensitivity": fin_sens,
        },
        "population": {
            "chains": len(roots),
            "policy_rows": policy["rows"],
            "policy_year_cells": len(year_cells),
            "policy_events_all_years": sum(pol_events.values()),
            "fin_rows": len(fin),
            "fin_amount_parsed_cny": parsed["cnys"],
            "fin_amount_foreign": parsed["foreign"],
            "fin_amount_blank": parsed["blank"],
            "fin_amount_unparsed": parsed["unparsed"],
            "fin_excluded_financial_rows": fin_excluded,
            "fin_mapped_events_2021_2026": len(mapped_events),
            "name_chain_names": len(name_chain),
        },
        "headline": {
            "milestone_total": total,
            "policy_milestones": sum(pol_milestones.values()),
            "investment_milestones": sum(fin_milestones.values()),
            "tech_milestones": None,
            "chain_avg": round(total / len(roots), 1),
            "chain_max": rows[0]["milestone_total"],
            "chain_max_name": rows[0]["chain_name"],
            "chain_min": rows[-1]["milestone_total"],
            "chain_min_name": rows[-1]["chain_name"],
            "chains_with_policy": sum(1 for ch in roots if pol_milestones[ch] > 0),
            "chains_with_investment": sum(1 for ch in roots if fin_milestones[ch] > 0),
            "by_year_policy": dict(sorted(by_year_pol.items())),
            "by_year_policy_milestones": dict(sorted(by_year_events.items())),
            "by_year_investment": dict(sorted(by_year_fin.items())),
        },
        "by_chain": rows,
        "milestone_events": {
            "policy": [c for c in year_cells if c["policies"] >= POLICY_MIN],
            "investment": sorted(big_events, key=lambda e: -e["amount_wan"])[:40],
        },
        "tech_breakthrough_evidence": {
            "verdict": "不可算（不是 0，是未测/无源）",
            "gkx_tables_total": 280,
            "milestone_table_hits": 0,
            "event_tables": {"dwd_event": 20},
            "news_columns": ["pk_id", "industry_code", "industry_name", "title", "publish_date", "source"],
            "missing_fields": ["event_type", "milestone_type", "event_level", "is_milestone"],
            "note": "资讯表只有标题与发布日期，要判「重大技术突破」必须自造阈值+文本分类，"
                    "而 calc-logic 的阈值与事件识别参数未给出；按 v6 §七 负结论必须留证据，"
                    "此处不给代理分，避免把关键词命中冒充技术突破。",
        },
        "live_probe": {k: probe[k] for k in (
            "gkx_has_result_face", "gkx_chain_related_tables", "live_table_rows",
            "live_usable", "live_unusable_reason", "verdict")},
        "gaps": [
            "源表 event_id 为企业级：25,654 行仅 6,503 个 id、且无跨企业复用，按 DISTINCT event_id 会把多轮融资压成 1 条；本件用 (event_id, date, amount_wan) 复合键，窗口内去重后 %d 个事件" % fin_rows_unique,
            "industry_chain_milestone_event 两库均无（gkx 0 表，live 0 表）",
            "chain_roadmap / chain_investment 两库均无，无法读 total_events 或投资事件链键",
            "政策命中只覆盖 2001—2022，2023 及以后政策表零条（不按 0 摊入）",
            "政策 T0 精确命中仅 145/20,000 条（0.725%），链级政策里程碑覆盖薄",
            "重大技术突破无事件识别真源，本件置 null，未用资讯关键词硬凑",
            "融资额 16,828 行为空、502 行为外币，只按人民币解析，事件数偏保守",
        ],
        "checks": {
            "sum_policy_milestones": sum(pol_milestones.values()),
            "sum_investment_milestones": sum(fin_milestones.values()),
            "sum_total": sum(r["milestone_total"] for r in rows),
            "total_matches_headline": total == sum(pol_milestones.values()) + sum(fin_milestones.values()),
            "policy_years_subset_events": all(len(set(pol_years[ch])) <= pol_events[ch] + 1 for ch in roots),
            "big_events_count": len(big_events),
            "parse_total": parsed["cnys"] + parsed["foreign"] + parsed["blank"] + parsed["unparsed"],
            "parse_total_equals_rows": parsed["cnys"] + parsed["foreign"] + parsed["blank"] + parsed["unparsed"] == len(fin),
        },
    }
    path = os.path.join(HERE, "M_CHAIN_DEVELOPMENT_MILESTONE_COUNT_out.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"[ok] M_CHAIN_DEVELOPMENT_MILESTONE_COUNT total={total} "
          f"(policy {sum(pol_milestones.values())} invest {sum(fin_milestones.values())}) "
          f"top={rows[0]['chain_name']}")


if __name__ == "__main__":
    main()
