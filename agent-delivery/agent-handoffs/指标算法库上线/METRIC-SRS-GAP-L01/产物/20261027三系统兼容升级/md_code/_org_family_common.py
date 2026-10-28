#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORG 家族 5 指标共用工具：面板读取、归一化、分布统计、学科→领域映射。

只做纯函数与只读加载，不发任何 SQL。所有指标脚本都从这里取 `load_panel()`。
"""
from __future__ import annotations

import json
import os
import re
import statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "_snapshots21", "org_family_panel_20261021.json")

CITY_ORDER = ["深圳市", "广州市", "东莞市", "惠州市"]

DOMAINS = ["电子信息/AI", "生物医药", "能源材料", "装备制造", "基础科学", "农业生态", "经管人文"]

DISC_MAP = {
    "电子": "电子信息/AI", "计算机": "电子信息/AI", "自动化": "电子信息/AI",
    "人工智能": "电子信息/AI", "信息": "电子信息/AI", "半导体": "电子信息/AI",
    "通信": "电子信息/AI", "光学": "电子信息/AI", "软件": "电子信息/AI",
    "生物": "生物医药", "医学": "生物医药", "药理": "生物医药", "药物": "生物医药",
    "临床": "生物医药", "中医": "生物医药", "遗传": "生物医药", "免疫": "生物医药",
    "神经": "生物医药", "细胞": "生物医药", "生理": "生物医药", "肿瘤": "生物医药",
    "护理": "生物医药", "公共卫生": "生物医药", "口腔": "生物医药",
    "材料": "能源材料", "化学": "能源材料", "化工": "能源材料", "能源": "能源材料",
    "工程热物理": "能源材料", "金属": "能源材料", "高分子": "能源材料", "冶金": "能源材料",
    "机械": "装备制造", "力学": "装备制造", "仪器": "装备制造", "土木": "装备制造",
    "交通": "装备制造", "航空": "装备制造", "矿冶": "装备制造", "水利": "装备制造",
    "建筑": "装备制造", "电气": "装备制造", "动力": "装备制造",
    "数学": "基础科学", "物理": "基础科学", "天文": "基础科学", "地理": "基础科学",
    "地质": "基础科学", "海洋": "基础科学", "大气": "基础科学", "生态": "基础科学",
    "环境": "基础科学", "地球": "基础科学", "遥感": "基础科学", "测绘": "基础科学",
    "农": "农业生态", "园艺": "农业生态", "林": "农业生态", "水产": "农业生态",
    "畜牧": "农业生态", "食品": "农业生态", "植物": "农业生态", "动物": "农业生态",
    "管理": "经管人文", "经济": "经管人文", "政策": "经管人文", "工商": "经管人文",
    "法学": "经管人文", "教育": "经管人文", "文学": "经管人文", "历史": "经管人文",
}


def load_panel():
    with open(PANEL, encoding="utf-8") as f:
        return json.load(f)


def domain_of(text):
    """学科/关键词 → 七大领域；未命中返回 None。"""
    t = text or ""
    for k, v in DISC_MAP.items():
        if k in t:
            return v
    return None


def minmax(vals):
    if not vals:
        return []
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [50.0] * len(vals)
    return [(v - lo) / (hi - lo) * 100.0 for v in vals]


def pct_rank(vals):
    """分位刻度 0–100（并列取平均秩），对长尾比 minmax 稳健。"""
    n = len(vals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: vals[i])
    out = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 / max(n - 1, 1) * 100.0
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def dist(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 2), "p25": round(s[int(n * .25)], 2),
            "median": round(statistics.median(s), 2), "mean": round(sum(s) / n, 2),
            "p75": round(s[int(n * .75)], 2), "p90": round(s[int(n * .9)], 2),
            "max": round(s[-1], 2)}


def spearman(a, b):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** .5
    db = sum((y - mb) ** 2 for y in rb) ** .5
    return round(num / (da * db), 4) if da and db else None


def signal_count(i):
    return sum(1 for k in ("patents", "papers", "scholars", "projects",
                           "transfer_in", "policy_mentions", "people") if i.get(k))


def dedup_name_flags(inst):
    """重名披露：同名不同 org_id 的机构（按 name 计数 >1）。"""
    c = Counter(i["name"] for i in inst)
    return {n: k for n, k in c.items() if k > 1}


def weighted(dims, weights):
    """缺维重归一：dims = {key: (value|None, weight)}。"""
    tot_w = sum(w for v, w in dims.values() if v is not None)
    if tot_w == 0:
        return None, 0
    s = sum(v * w for v, w in dims.values() if v is not None) / tot_w
    return round(s, 2), sum(1 for v, _ in dims.values() if v is not None)


def year_add(counter, start=2014, end=2026):
    """把 {年: 值} 补齐为连续年份序列（缺失年留 None，不按 0 摊）。"""
    return {str(y): counter.get(str(y)) for y in range(start, end + 1)}
