#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REG5 批共用装配（20261021 改源版）：只读 `gkx` 与 `_snapshots21/` 缓存，零重扫。

链轴/区域轴/统计年与同族 `_gkx21_common` 保持一致：
  12 条链（INB1204…INB2505）× 4 市（深圳/广州/东莞/惠州），统计年 2025，专利完整年 2024。

本文件只做三件事：
  1. 把探针落盘的机构名录、学者表、融资表、企业底册装配成内存索引；
  2. 提供机构名 → 城市的**最长前缀**匹配（论文/学者归属共用同一套）；
  3. 统一统计与写盘函数，保证 5 个指标的 out.json 口径一致。
"""
from __future__ import annotations

import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

SNAP = Path(__file__).parent / "_snapshots21"
CODE = Path(__file__).parent

CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
CHAIN_CN = {
    "INB1306": "软件与信息服务", "INB1309": "人工智能", "INB1333": "智能终端", "INB1502": "数字创意",
    "INB2505": "合成生物", "INB1204": "机器人", "INB1303": "集成电路", "INB1323": "传感器",
    "INB1354": "具身智能", "INB1209": "智能网联汽车", "INB1236": "低空经济", "INB2503": "生物医药",
}
CHAIN_AXIS = list(CHAIN_CN)
STAT_YEAR = 2025
PAT_YEAR_LAST = 2024
CITY_TOKEN = {"深圳": "深圳市", "广州": "广州市", "东莞": "东莞市", "惠州": "惠州市"}


def _load(name, default=None):
    p = SNAP / name
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def probe3():
    return _load("reg5_probe3_20261021.json", {"queries": {}})["queries"]


def base_rows():
    """企业底册 189,116 行：[org_id, credit, name, province, city, year]"""
    return _load("base_20261021.json", [])


def bridge():
    """链上企业桥 35,046 家（credit 唯一）：{nm, cc, p, c, chains, n_row, tags}"""
    return _load("bridge_20261021.json", [])


# ---------------------------------------------------------------- 机构 → 城市
_ORG_CACHE = {}


def org_city_index():
    """机构名 → (city, kind)；含高校、科研院所、企业底册三类，最长前缀匹配。"""
    if "idx" in _ORG_CACHE:
        return _ORG_CACHE["idx"], _ORG_CACHE["by4"]
    p3 = probe3()
    rows = []
    for r in p3.get("heis_names", {}).get("rows", []):
        rows.append((r[0], r[1], "university"))
    for r in p3.get("inst_names", {}).get("rows", []):
        rows.append((r[0], r[1], "institute"))
    for r in base_rows():
        if len(r) > 4 and r[2]:
            rows.append((r[2], r[4], "enterprise"))
    exact, by4 = {}, defaultdict(list)
    for nm, city, kind in rows:
        nm = (nm or "").strip()
        if not nm or not city:
            continue
        if nm not in exact:
            exact[nm] = (city, kind)
        by4[nm[:4]].append(nm)
    for k in by4:
        by4[k] = sorted(set(by4[k]), key=len, reverse=True)
    _ORG_CACHE["idx"] = exact
    _ORG_CACHE["by4"] = by4
    return exact, by4


def match_org(name, exact=None, by4=None):
    """最长前缀匹配；退化为机构名里的城市词（深圳/广州/东莞/惠州）。"""
    if exact is None:
        exact, by4 = org_city_index()
    s = (name or "").strip()
    if not s:
        return None, None
    if s in exact:
        return exact[s]
    for cand in by4.get(s[:4], ()):
        if s.startswith(cand):
            return exact[cand]
    for tok, city in CITY_TOKEN.items():
        if tok in s:
            return city, "city_token"
    return None, None


# ---------------------------------------------------------------- 链 × 城
def cells():
    """返回 (cell_firms, name_cells, credit_chains)。"""
    cf, nc, ec = defaultdict(set), defaultdict(list), {}
    for b in bridge():
        chs = [c for c in (b.get("chains") or []) if c in CHAIN_CN]
        if b.get("cc"):
            ec[b["cc"]] = chs
        if b.get("c") not in CITY4:
            continue
        for ch in chs:
            cf[(ch, b["c"])].add(b["nm"])
            nc[b["nm"]].append((ch, b["c"]))
    return cf, nc, ec


def chain_firms():
    """链 → 企业名列表（跨市，去重）。"""
    out = defaultdict(set)
    for b in bridge():
        for ch in (b.get("chains") or []):
            if ch in CHAIN_CN:
                out[ch].add(b["nm"])
    return {k: sorted(v) for k, v in out.items()}


# ---------------------------------------------------------------- 统计
def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi - lo <= 1e-12:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def stats(vals, nd=4):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], nd), "max": round(s[-1], nd),
            "mean": round(sum(s) / n, nd), "median": round(statistics.median(s), nd),
            "p90": round(s[int(0.9 * (n - 1))], nd),
            "n_zero": sum(1 for x in s if x == 0),
            "n_distinct": len({round(x, 6) for x in s})}


def pct(a, b, nd=2):
    return round(100.0 * a / b, nd) if b else None


def write_out(metric_id, payload):
    p = CODE / f"{metric_id}_out.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


DEGREE_RE = re.compile(r"博士|硕士|学士|本科")


def degree_bucket(ds):
    """一人多学位取最高：博士（含博士后/哲学博士）> 硕士 > 学士/本科 > 其他。"""
    for d in ds:
        if "博士" in (d or ""):
            return "博士"
    for d in ds:
        if "硕士" in (d or ""):
            return "硕士"
    for d in ds:
        if "学士" in (d or "") or "本科" in (d or ""):
            return "学士"
    return "其他"
