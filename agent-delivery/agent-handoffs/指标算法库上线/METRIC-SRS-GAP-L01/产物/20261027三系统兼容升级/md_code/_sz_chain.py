#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链切片代理：dwd_org_industry_tags（真实行业标签）→ 15 条顶层链的关键词映射。

背景：`dwd_industry_chain_info` 的 15 条顶层链用 INB1701..INB1805 码族；
而 `dwd_org_industry_tags` / `industry_chain_news_event` 用 INB13xx/15xx/25xx 四位数码族，
`dim.industry_cluster_map`(50 行) 只映射 INB17xx/18xx —— 两族之间**没有交叉表**。
故链切片只能用「标签行业名 → 顶层链名」的关键词映射，属代理口径，须披露。
"""
from __future__ import annotations

import json
import re

# 15 条顶层链（INB1701..INB1805）的关键词表；顺序即优先级（长词优先）
CHAIN_KEYWORDS = [
    ("智能网联新能源汽车", ["智能网联", "新能源汽车", "汽车", "车载", "整车"]),
    ("低空经济与空天", ["低空", "无人机", "航空", "航天", "卫星", "运载"]),
    ("新一代信息技术", ["软件", "信息技术", "信息传输", "通信", "集成电路", "智能终端",
                        "信息安全", "人工智能", "大数据", "云计算", "数据服务", "网络", "半导体", "光电"]),
    ("生物", ["生物", "医药", "医疗", "药物", "中药", "医学", "疫苗", "临床", "制药"]),
    ("新能源", ["新能源", "光伏", "储能", "锂电", "电池", "风电", "氢能", "核能"]),
    ("新材料", ["材料", "化工", "金属", "高分子", "陶瓷"]),
    ("高端装备", ["装备", "机器人", "机床", "仪器", "机械", "激光", "具身智能", "智能制造"]),
    ("绿色环保", ["环保", "节能", "资源循环", "污染", "水处理", "固废"]),
    ("海洋", ["海洋", "船舶", "水产", "港口"]),
    ("传统与创意", ["文化", "创意", "影视", "设计", "服装", "食品", "家具", "文旅"]),
    ("未来制造", ["增材", "3D打印", "柔性制造", "智能工厂"]),
    ("未来信息", ["量子", "光通信", "6G", "类脑"]),
    ("未来能源", ["可控核聚变", "氢", "新型储能"]),
    ("未来空间", ["深空", "空间站", "星际"]),
    ("未来健康", ["合成生物", "基因", "细胞", "脑机", "精准医疗"]),
]


def _names(raw):
    if not raw:
        return []
    try:
        v = json.loads(raw)
        if isinstance(v, list):
            return [str(x) for x in v]
        return [str(v)]
    except Exception:  # noqa: BLE001
        return [s.strip() for s in re.split(r"[,，\[\]'\"]", str(raw)) if s.strip()]


def to_chain15(industry_raw: str, link_raw: str = "") -> str | None:
    """把标签行业名（数组串）映射到 15 条顶层链之一；映射不上返回 None。"""
    blob = " ".join(_names(industry_raw) + _names(link_raw))
    if not blob:
        return None
    for chain, kws in CHAIN_KEYWORDS:
        for kw in kws:
            if kw in blob:
                return chain
    return None
