#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""政策覆盖率词表与命中函数（20261021 版，纯本地计算，不连库）

口径出处：`calc-logic/CHAIN/M_CHAIN_REG_POLICY_COVERAGE.md` v0.2.0（徐滕强 2026-10-14）
  Cov(c,r) = Σ_i hit_i/(hit_i+5) / |L1(c)| × 100%
  政策池 = city=r 的有效政策 ∪ (city 空 ∧ 国家级政策)
环节词表是**算法侧维护载体**（非库表），12 条链 44 个 L1 环节的实体词显式写死以便复现；
阶段词/泛词环节（基础层/技术层/零部件…）单独作命中词会误判，回退链级领域词并标注
token_source = chain_fallback。本文件只保留词表与命中函数，数据行由调用方从 gkx 现取。
"""
from __future__ import annotations

CHAIN_TOKENS = {
    "INB1306": ["软件", "信息服务"],
    "INB1309": ["人工智能"],
    "INB1333": ["智能终端", "消费电子"],
    "INB1502": ["数字创意", "数字文化", "文化创意"],
    "INB2505": ["合成生物", "生物制造"],
    "INB1204": ["机器人"],
    "INB1303": ["集成电路", "半导体", "芯片"],
    "INB1323": ["传感器"],
    "INB1354": ["具身智能", "人形机器人"],
    "INB1209": ["智能网联汽车", "新能源汽车", "车联网"],
    "INB1236": ["低空经济", "低空", "无人机"],
    "INB2503": ["生物医药", "创新药", "医疗器械"],
}

GENERIC_L1 = {
    "基础层", "技术层", "应用层", "平台层", "工具层", "核心元器件与零部件", "零部件", "原材料",
    "软件", "本体制造", "整机集成", "生产制造", "产品设计", "整车制造", "AI应用",
    "核心零部件", "应用", "服务",
}

LINK_SPECIFIC = {
    "软件产品": ["软件产品"],
    "信息技术服务": ["信息技术"],
    "信息安全软件与服务": ["信息安全"],
    "数字文化创意活动": ["数字文化", "文化创意"],
    "规划设计服务": ["规划设计", "工业设计"],
    "半导体材料": ["半导体材料"],
    "EDA/IP核": ["EDA", "电子设计自动化"],
    "半导体设备": ["半导体设备"],
    "晶圆制造": ["晶圆"],
    "Fabless设计": ["芯片设计", "集成电路设计"],
    "封测": ["封装测试", "封测"],
    "智能网联汽车零部件": ["智能网联汽车", "车联网"],
    "智能网联相关服务": ["智能网联", "车联网"],
    "低空基建与信息服务": ["低空", "通用航空"],
    "低空制造业": ["低空", "无人机"],
    "低空运营业": ["低空", "无人机"],
    "低空配套业": ["低空", "通用航空"],
    "传感器生产专用装备": ["传感器"],
    "医学研发服务": ["医学研发", "临床试验"],
    "药品制造": ["创新药", "药品"],
    "具身智能数据服务": ["具身智能"],
    "具身智能体": ["具身智能"],
}


def policy_pool(rows, city):
    out = []
    for r in rows:
        c = r["city"] or ""
        if c == city:
            out.append(r)
        elif c == "" and r["rank"] and "国家级" in r["rank"]:
            out.append(r)
    return out


def tokens_for(chain, l1_name, strict=False):
    if l1_name in GENERIC_L1:
        if strict:
            return [], "strict_none"
        return CHAIN_TOKENS[chain], "chain_fallback"
    if l1_name in LINK_SPECIFIC:
        return LINK_SPECIFIC[l1_name], "link"
    return CHAIN_TOKENS[chain], "chain_fallback"


def hit_count(pool, tokens):
    if not tokens:
        return 0
    n = 0
    for r in pool:
        t = r["title"] or ""
        if any(tok and tok in t for tok in tokens):
            n += 1
    return n


def coverage_cell(policy_rows, chain, l1_links, tree, city, strict=False):
    pool = policy_pool(policy_rows, city)
    links = []
    for code in l1_links:
        name = (tree.get(code) or {}).get("name") or ""
        toks, src = tokens_for(chain, name, strict=strict)
        h = hit_count(pool, toks)
        links.append({"code": code, "name": name, "tokens": toks, "token_source": src,
                      "hits": h, "contribution": round(h / (h + 5), 4) if toks else 0.0})
    n = len(links)
    cov = 100.0 * sum(l["contribution"] for l in links) / n if n else 0.0
    binary = 100.0 * sum(1 for l in links if l["hits"] > 0) / n if n else 0.0
    return {
        "coverage_pct": round(cov, 2),
        "binary_coverage_pct": round(binary, 2),
        "n_links": n,
        "n_links_hit": sum(1 for l in links if l["hits"] > 0),
        "total_hits": sum(l["hits"] for l in links),
        "policy_pool_size": len(pool),
        "links": links,
    }
