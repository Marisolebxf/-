#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-18/A-19 簇公共库（20261021 版）：只读缓存，零专利 SQL。

数据入口（全部为 20261021 批已建成的共享资产）：
  * `_snapshots21/patent_ipc4_year_20261021.json`   IPC4 × 年 → [件数, 机构数]（全量 2,420,915 件有 IPC）
  * `_snapshots21/patent_panel_innov_20261021.json` 面板主表（年 / 申请人年 / IPC 年）
  * `_snapshots21/patent_ipc4_by_name_20261021.json` IPC4 × 申请人 → 件数
  * `_snapshots21/patent_scan_20261021.pkl`          城市 × 年 × IPC4 → pn 集合
  * `_snapshots21/base_20261021.json`                底册 189,116 行（名称/城市）
  * `_snapshots21/plan_ipc_lexicon_gkx21.json`       跨表术语词典（IPC4 ← 中文术语）
  * `_snapshots21/policy_base_20261021.json`         政策全表 20,000 条

铁律：本模块**不连 gkx.dwd_patent**。专利任何计数一律来自上面的面板/派生缓存。
"""
from __future__ import annotations

import json
import math
import pickle
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"

PANEL_MIN_Y21 = 200
PANEL_MIN_Y24 = 200
CJK = re.compile(r"[\u4e00-\u9fff]")

STOP_TERMS = {
    "工程学", "电子设备", "计算机", "自动化", "智能化", "信息化", "系统", "方法", "装置",
    "设备", "技术", "应用", "研究", "设计", "检测", "控制", "管理", "数据分析", "人工智能",
    "数据库", "软件", "算法", "模型", "传感器", "机器人", "新材料", "生物", "医学",
}

_CACHE: dict[str, object] = {}


# ---------------------------------------------------------------- 专利缓存
def ipc4_year() -> dict[tuple[str, int], list[int]]:
    """{(ipc4, year): [件数, 机构数]}；合计 2,420,915 件（全量有 IPC 部分）。"""
    if "i4y" not in _CACHE:
        rows = json.loads((SNAP / "patent_ipc4_year_20261021.json").read_text(encoding="utf-8"))
        _CACHE["i4y"] = {(r[0], int(r[1])): [int(r[2]), int(r[3])] for r in rows}
    return _CACHE["i4y"]  # type: ignore[return-value]


def panel_ipc4() -> list[str]:
    """258 个面板方向：2021 与 2024 年专利量均 ≥200 件（与 20261020 批同口径）。"""
    if "panel" not in _CACHE:
        d = ipc4_year()
        ips = {k[0] for k in d}
        _CACHE["panel"] = sorted(
            i for i in ips
            if d.get((i, 2021), [0])[0] >= PANEL_MIN_Y21 and d.get((i, 2024), [0])[0] >= PANEL_MIN_Y24
        )
    return _CACHE["panel"]  # type: ignore[return-value]


def year_totals() -> dict[int, int]:
    """年 × 件数（全量，含无 IPC 部分），来自面板主表的 year_all。"""
    if "ytot" not in _CACHE:
        p = json.loads((SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
        _CACHE["ytot"] = {int(k): int(v) for k, v in p["year_all"].items()}
    return _CACHE["ytot"]  # type: ignore[return-value]


def panel_meta() -> dict:
    p = json.loads((SNAP / "patent_panel_innov_20261021.json").read_text(encoding="utf-8"))
    return {"rows": p["rows"], "chunks": p["chunks"], "complete": p["rows"] == 2_939_895}


def ipc4_by_name() -> list[list]:
    if "i4n" not in _CACHE:
        _CACHE["i4n"] = json.loads((SNAP / "patent_ipc4_by_name_20261021.json").read_text(encoding="utf-8"))
    return _CACHE["i4n"]  # type: ignore[return-value]


def city_ipc_pn() -> dict[tuple[str, int, str], set]:
    """(城市短名, 年, IPC4) → pn 集合。只含 6 个可判城市，2021—2024。"""
    if "cip" not in _CACHE:
        with open(SNAP / "patent_scan_20261021.pkl", "rb") as f:
            d = pickle.load(f)
        _CACHE["cip"] = d["ipc_pn"]
        _CACHE["scan_meta"] = {k: d[k] for k in ("row_total", "row_city", "year_dist", "done")}
    return _CACHE["cip"]  # type: ignore[return-value]


# ---------------------------------------------------------------- 企业底册
def name_city() -> tuple[dict[str, str], int]:
    """名称 → 城市（市级全称）；同名跨市记为不判，返回 (map, n_conflict)。"""
    if "nc" not in _CACHE:
        rows = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
        seen: dict[str, set] = defaultdict(set)
        for r in rows:
            nm = (r[2] or "").strip()
            cty = (r[4] or "").strip()
            if nm:
                seen[nm].add(cty)
        m = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
        _CACHE["nc"] = (m, sum(1 for v in seen.values() if len(v) > 1))
    return _CACHE["nc"]  # type: ignore[return-value]


def base_rows() -> list[list]:
    if "base" not in _CACHE:
        _CACHE["base"] = json.loads((SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    return _CACHE["base"]  # type: ignore[return-value]


# ---------------------------------------------------------------- 术语词典桥
def lexicon() -> dict:
    if "lex" not in _CACHE:
        _CACHE["lex"] = json.loads((SNAP / "plan_ipc_lexicon_gkx21.json").read_text(encoding="utf-8"))
    return _CACHE["lex"]  # type: ignore[return-value]


def term_index() -> tuple[dict, dict]:
    """(倒排 term→[(ipc,w)], 2-gram matcher)。"""
    if "inv" not in _CACHE:
        lex = lexicon()["terms_by_ipc"]
        inv: dict[str, list] = defaultdict(list)
        for ipc, terms in lex.items():
            for t, w in terms.items():
                inv[t].append((ipc, float(w)))
        idx: dict[str, list] = defaultdict(list)
        for term in inv:
            for i in range(len(term) - 1):
                idx[term[i:i + 2]].append(term)
        _CACHE["inv"] = dict(inv)
        _CACHE["matcher"] = {k: sorted(set(v)) for k, v in idx.items()}
    return _CACHE["inv"], _CACHE["matcher"]  # type: ignore[return-value]


def assign_fast(text: str, k: int = 3) -> list[tuple[str, float, list]]:
    """文本 → [(ipc4, score, hits)]，2-gram 候选加速，与词典建典时同义。"""
    inv, matcher = term_index()
    if not text:
        return []
    text = str(text)
    cands: set[str] = set()
    for i in range(len(text) - 1):
        hit = matcher.get(text[i:i + 2])
        if hit:
            cands.update(hit)
    score: dict[str, float] = defaultdict(float)
    hits: dict[str, list] = defaultdict(list)
    for term in cands:
        if term in text:
            for ipc, w in inv[term]:
                score[ipc] += w
                hits[ipc].append(term)
    if not score:
        return []
    top = sorted(score.items(), key=lambda kv: -kv[1])[:k]
    return [(ipc, round(sc, 3), hits[ipc][:5]) for ipc, sc in top]


# ---------------------------------------------------------------- 统计助手
def pct(vals, q):
    if not vals:
        return None
    s = sorted(vals)
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return round(s[int(k)], 4)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 4)


def st(vals) -> dict:
    if not vals:
        return {}
    return {
        "n": len(vals), "min": round(min(vals), 4), "max": round(max(vals), 4),
        "mean": round(statistics.mean(vals), 4), "median": round(statistics.median(vals), 4),
        "p10": pct(vals, 0.10), "p90": pct(vals, 0.90),
    }


def rank_pct(vals: list[float]) -> list[float]:
    """百分位（0—100，最小 0、最大 100，rank-1/(n-1)）。"""
    n = len(vals)
    if n <= 1:
        return [50.0] * n
    order = sorted(range(n), key=lambda i: vals[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return [round(100 * x / (n - 1), 2) for x in r]


def spearman(a, b):
    if len(a) < 3:
        return None

    def rk(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    ra, rb = rk(a), rk(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return round(num / den, 4) if den else None


def write_out(metric: str, payload: dict) -> Path:
    # §3.16：base_years_used / base_years_missing 同时提到顶层，便于机检
    bb = payload.get("base_years")
    if isinstance(bb, dict):
        payload.setdefault("base_years_used", bb.get("base_years_used"))
        payload.setdefault("base_years_missing", bb.get("base_years_missing"))
    out = HERE / f"{metric}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("wrote", out.name)
    return out


def base_year_block(used: list[int], missing: list[int], note: str) -> dict:
    """§3.16 强制字段：分母只允许用库内真实存在的年份。"""
    return {"base_years_used": used, "base_years_missing": missing, "note": note}
