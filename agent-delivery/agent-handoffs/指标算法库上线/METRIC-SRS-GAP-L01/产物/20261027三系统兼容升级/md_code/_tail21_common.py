#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INNOV 尾批 8 指标公共库（20261022）。

内容：
  * 快照 / 探针缓存读取（`_snapshots21/probe_tail21_20261022.json`、
    `probe_inn21_texts_20261022.json`、`probe_tinn21_20261022.json`）；
  * 年份、城市、作者单位解析；
  * `write_out` / `base_year_block` 直接复用 A-26 公共库，保持字段一致。
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
sys.path.insert(0, str(HERE))

import _a26_common as C  # noqa: E402

write_out = C.write_out
base_year_block = C.base_year_block
st = C.st
pct = C.pct

_C: dict[str, object] = {}


def load(name: str):
    if name not in _C:
        _C[name] = json.loads((SNAP / name).read_text(encoding="utf-8"))
    return _C[name]


def tail() -> dict:
    return load("probe_tail21_20261022.json")


def texts() -> dict:
    return load("probe_inn21_texts_20261022.json")


def tinn() -> dict:
    return load("probe_tinn21_20261022.json")


def rows_of(d: dict, label: str) -> list[list]:
    v = d.get(label) or {}
    return v.get("rows") or []


_YEAR = re.compile(r"(1[89]\d{2}|20\d{2})")

# 论文机构名里可识别的城市（含直辖市与主要地级市；只做「出现即归属」，不做消歧）
CITIES = [
    "北京市", "上海市", "天津市", "重庆市", "深圳市", "广州市", "东莞市", "惠州市", "珠海市",
    "佛山市", "中山市", "汕头市", "湛江市", "江门市", "肇庆市", "杭州市", "宁波市", "温州市",
    "南京市", "苏州市", "无锡市", "常州市", "徐州市", "武汉市", "长沙市", "株洲市", "成都市",
    "绵阳市", "西安市", "合肥市", "芜湖市", "济南市", "青岛市", "烟台市", "郑州市", "洛阳市",
    "福州市", "厦门市", "泉州市", "南昌市", "昆明市", "贵阳市", "南宁市", "兰州市", "太原市",
    "石家庄市", "唐山市", "沈阳市", "大连市", "鞍山市", "长春市", "吉林市", "哈尔滨市",
    "大庆市", "乌鲁木齐市", "呼和浩特市", "银川市", "西宁市", "拉萨市", "海口市", "三亚市",
    "香港", "澳门", "台北市",
]


def year_of(s) -> int | None:
    if s is None:
        return None
    m = _YEAR.match(str(s).strip())
    return int(m.group(1)) if m else None


def city_of(text: str) -> str | None:
    """从机构名/地址串取城市：先全称（带「市」），再退化到裸名；命中即返回。"""
    if not text:
        return None
    for c in CITIES:
        if c in text:
            return c
    for c in CITIES:
        bare = c[:-1] if c.endswith("市") else c
        if len(bare) >= 2 and bare in text:
            return c
    return None


def parse_authors(raw) -> list[dict]:
    if not raw:
        return []
    try:
        js = json.loads(raw)
        return js if isinstance(js, list) else []
    except Exception:
        return []


ENT_SUFFIX = ("有限公司", "股份", "集团", "公司", "厂", "研究院", "研究所", "大学", "学院",
              "医院", "中心", "实验室", "科学院", "学校")


def inst_kind(name: str) -> str:
    if not name:
        return "未知"
    if any(k in name for k in ("大学", "学院", "学校", "中学")):
        return "高校"
    if any(k in name for k in ("研究院", "研究所", "科学院", "研究中心", "实验室")):
        return "院所"
    if "医院" in name:
        return "医院"
    if any(k in name for k in ("有限公司", "股份", "集团", "公司", "厂")):
        return "企业"
    return "其他"


def topn(counter: Counter, n: int = 20) -> list[list]:
    return [[k, int(v)] for k, v in counter.most_common(n)]
