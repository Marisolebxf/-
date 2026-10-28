#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SZ-CHAIN 族共享工具：读矩阵缓存 + 标准化 + 分档机判。"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
MATRIX = HERE / "_snapshots" / "sz_chain_matrix_20261021.json"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]


def load_matrix() -> dict:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def chains(m: dict):
    return [(c["code"], c["name"]) for c in m["chains"]]


def minmax(vals: dict):
    """对标集合 min-max 到 0–100；全体相同按王惠口径取 50。返回 (scores, meta)。"""
    xs = {k: float(v) for k, v in vals.items()}
    lo, hi = min(xs.values()), max(xs.values())
    if hi - lo <= 1e-12:
        return {k: 50.0 for k in xs}, {"min": lo, "max": hi, "constant": True}
    return {k: round(100 * (v - lo) / (hi - lo), 2) for k, v in xs.items()}, {"min": lo, "max": hi, "constant": False}


def stats(vals):
    v = sorted(float(x) for x in vals)
    if not v:
        return {}
    return {"n": len(v), "min": v[0], "max": v[-1],
            "median": round(statistics.median(v), 2),
            "mean": round(statistics.mean(v), 2),
            "n_zero": sum(1 for x in v if x == 0),
            "n_pos": sum(1 for x in v if x > 0)}


def spearman(a, b):
    def rank(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return round(num / den, 4) if den else None


def write_out(metric_id: str, payload: dict):
    out = HERE / f"{metric_id}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("wrote", out)
    return out
