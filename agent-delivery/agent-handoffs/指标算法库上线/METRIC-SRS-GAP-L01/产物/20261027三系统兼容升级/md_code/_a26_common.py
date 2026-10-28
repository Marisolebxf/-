#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-26 簇公共库（学者影响力 / 产业科学影响力 / 产业技术影响力 / 研究领域重叠度 / 多企业竞争情报比对）。

设计原则
--------
1. **零专利 SQL**：专利侧只读 `_snapshots21/` 已建成缓存（面板、申请人聚合、IPC4×申请人）。
2. **学者/论文只读窄列快照**：`_snapshots21/probe_a26_20261022.json` 由 `_probe_a26.py` 逐条限时
   落盘（dwd_scholar 21,316 行、dwd_zh_paper_citation 20,031 行、dwd_zh_author 62,002 行），
   本模块不再对这两张表发任何 GROUP BY。
3. **行业维本地化**：机构 → 行业只用 `star_base_rows_gkx.json`（189,116 行底册，含 industry_l1/l2），
   不查 `dwd_org_base_info`（无索引，全表 COUNT 实测 87.7 秒）。

所有输出均显式写出覆盖率和缺失维，禁止把「无数据」写成「低分」。
"""
from __future__ import annotations

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"

# ---------------------------------------------------------------- 统计工具


def pct(vals, q: float):
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
    return {"n": len(vals), "min": round(min(vals), 4), "max": round(max(vals), 4),
            "mean": round(statistics.mean(vals), 4), "median": round(statistics.median(vals), 4),
            "p10": pct(vals, 0.10), "p90": pct(vals, 0.90), "p99": pct(vals, 0.99)}


def rank_pct(vals) -> list[float]:
    """百分位 0—100（rank-1/(n-1)，并列取平均秩）。"""
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


def jaccard(a: set, b: set):
    if not a and not b:
        return None
    return round(len(a & b) / len(a | b), 4)


def write_out(metric: str, payload: dict) -> Path:
    out = HERE / f"{metric}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("wrote", out.name)
    return out


def base_year_block(used: list[int], missing: list[int], note: str) -> dict:
    """§3.16 强制字段：分母只允许用库内真实存在的年份。"""
    return {"base_years_used": used, "base_years_missing": missing, "note": note}


_CACHE: dict[str, object] = {}


# ---------------------------------------------------------------- 快照加载


def probe() -> dict:
    if "probe" not in _CACHE:
        _CACHE["probe"] = json.loads((SNAP / "probe_a26_20261022.json").read_text(encoding="utf-8"))
    return _CACHE["probe"]  # type: ignore[return-value]


def scholars() -> list[dict]:
    """21,316 位学者；h_index / citation_nums / paper_nums 三列 100% 非空（本批实测）。"""
    if "sch" not in _CACHE:
        rows = probe()["scholar_dump"]["rows"]
        _CACHE["sch"] = [
            {"scholar_id": r[0], "name": r[1], "org": (r[2] or "").strip(),
             "paper_nums": int(r[3] or 0), "citation_nums": int(r[4] or 0),
             "h_index": int(r[5] or 0), "status": r[6]}
            for r in rows
        ]
    return _CACHE["sch"]  # type: ignore[return-value]


def zh_citations() -> dict[str, int]:
    if "zc" not in _CACHE:
        _CACHE["zc"] = {r[0]: int(r[1] or 0) for r in probe()["zh_citation"]["rows"]}
    return _CACHE["zc"]  # type: ignore[return-value]


def zh_authors() -> dict[str, list[tuple[str, str]]]:
    """paper_id -> [(institution, affiliation)]；62,002 行覆盖 20,048 篇。"""
    if "za" not in _CACHE:
        d: dict[str, list] = defaultdict(list)
        for pid, inst, aff in probe()["zh_author"]["rows"]:
            d[pid].append(((inst or "").strip(), (aff or "").strip()))
        _CACHE["za"] = dict(d)
    return _CACHE["za"]  # type: ignore[return-value]


def base_rows() -> list[list]:
    if "base" not in _CACHE:
        _CACHE["base"] = json.loads((SNAP / "star_base_rows_gkx.json").read_text(encoding="utf-8"))
    return _CACHE["base"]  # type: ignore[return-value]


def org_industry() -> tuple[dict[str, tuple[str, str]], set[str]]:
    """名称 → (industry_l1, industry_l2)；仅保留有行业值的机构。"""
    if "oind" not in _CACHE:
        m: dict[str, tuple[str, str]] = {}
        for r in base_rows():
            nm = (r[1] or "").strip()
            l1 = (r[5] or "").strip()
            l2 = (r[6] or "").strip()
            if nm and l1:
                m[nm] = (l1, l2)
        _CACHE["oind"] = (m, set(m))
    return _CACHE["oind"]  # type: ignore[return-value]


def all_org_names() -> set[str]:
    """底册全部机构名（189,068 个），用于「机构识别」；行业归属另用 org_industry()。"""
    if "onames" not in _CACHE:
        _CACHE["onames"] = {(r[1] or "").strip() for r in base_rows() if (r[1] or "").strip()}
    return _CACHE["onames"]  # type: ignore[return-value]


def match_org_any(inst: str) -> str | None:
    """机构串 → 底册机构名（不限行业是否有值）：先精确，再取最长前缀（4—30 字）。"""
    if not inst:
        return None
    names = all_org_names()
    if inst in names:
        return inst
    for L in range(min(len(inst), 30), 3, -1):
        cand = inst[:L]
        if cand in names:
            return cand
    return None


def match_org(inst: str) -> str | None:
    """机构串 → 底册机构名：先精确，再取最长前缀（4—30 字）。"""
    if not inst:
        return None
    m, names = org_industry()
    if inst in names:
        return inst
    for L in range(min(len(inst), 30), 3, -1):
        cand = inst[:L]
        if cand in names:
            return cand
    return None


_SEP = re.compile(r"[;,；，、/|]+")


def inst_tokens(inst: str) -> list[str]:
    return [t.strip() for t in _SEP.split(inst or "") if t.strip()]


# ---------------------------------------------------------------- 国际合作识别

FOREIGN_CN = [
    "美国", "英国", "日本", "德国", "法国", "加拿大", "澳大利亚", "新加坡", "韩国", "荷兰",
    "瑞典", "瑞士", "意大利", "西班牙", "比利时", "丹麦", "挪威", "芬兰", "奥地利", "以色列",
    "印度", "巴西", "俄罗斯", "马来西亚", "泰国", "越南", "新西兰", "爱尔兰", "波兰", "葡萄牙",
    "捷克", "土耳其", "南非", "墨西哥", "阿根廷", "智利", "沙特", "阿联酋", "伊朗", "埃及",
    "巴基斯坦", "孟加拉", "乌克兰", "希腊", "匈牙利", "罗马尼亚", "印度尼西亚", "菲律宾",
]
FOREIGN_EN = [
    "USA", "United States", "U.S.A", "America", "UK", "U.K.", "United Kingdom", "England",
    "Scotland", "Japan", "Germany", "France", "Canada", "Australia", "Singapore", "Korea",
    "Netherlands", "Sweden", "Switzerland", "Italy", "Spain", "Belgium", "Denmark", "Norway",
    "Finland", "Austria", "Israel", "India", "Brazil", "Russia", "Malaysia", "Thailand",
    "Vietnam", "New Zealand", "Ireland", "Poland", "Portugal", "Czech", "Turkey", "South Africa",
    "Mexico", "Argentina", "Chile", "Saudi", "UAE", "Iran", "Egypt", "Pakistan", "Bangladesh",
    "Ukraine", "Greece", "Hungary", "Romania", "Indonesia", "Philippines",
]


def is_foreign(affiliation: str) -> bool:
    s = affiliation or ""
    if not s:
        return False
    for t in FOREIGN_CN:
        if t in s:
            return True
    low = s.lower()
    for t in FOREIGN_EN:
        if t.lower() in low:
            return True
    return False


# ---------------------------------------------------------------- 专利缓存


def ipc4_year() -> dict[tuple[str, int], list[int]]:
    if "i4y" not in _CACHE:
        rows = json.loads((SNAP / "patent_ipc4_year_20261021.json").read_text(encoding="utf-8"))
        _CACHE["i4y"] = {(r[0], int(r[1])): [int(r[2]), int(r[3])] for r in rows}
    return _CACHE["i4y"]  # type: ignore[return-value]


def ipc4_by_name() -> list[list]:
    if "i4n" not in _CACHE:
        _CACHE["i4n"] = json.loads((SNAP / "patent_ipc4_by_name_20261021.json").read_text(encoding="utf-8"))
    return _CACHE["i4n"]  # type: ignore[return-value]


def applicant_agg() -> dict[str, list[int]]:
    if "agg" not in _CACHE:
        _CACHE["agg"] = json.loads((SNAP / "star_applicant_agg_gkx.json").read_text(encoding="utf-8"))["agg"]
    return _CACHE["agg"]  # type: ignore[return-value]


def roster() -> list[dict]:
    if "roster" not in _CACHE:
        _CACHE["roster"] = json.loads((SNAP / "star_roster_gkx_20261021.json").read_text(encoding="utf-8"))["rows"]
    return _CACHE["roster"]  # type: ignore[return-value]


def enterprise_universe(k: int = 12) -> list[dict]:
    """明星企业池（授权≥50、已剔除非企业主体）按专利件数取 Top K。"""
    rows = [r for r in roster() if r.get("pub_cnt", 0) > 0]
    rows.sort(key=lambda r: (-r["pub_cnt"], r["name_cn"]))
    return rows[:k]


def ipc_sets(names: list[str]) -> dict[str, set]:
    want = set(names)
    out: dict[str, set] = {n: set() for n in names}
    for ipc, nm, _n in ipc4_by_name():
        if nm in want:
            out[nm].add(ipc)
    return out


def scholar_sets(names: list[str]) -> dict[str, set]:
    want = set(names)
    out: dict[str, set] = {n: set() for n in names}
    for s in scholars():
        o = s["org"]
        if o in want:
            out[o].add(s["scholar_id"])
    return out


def author_sets(names: list[str]) -> dict[str, set]:
    """论文作者名集合（dwd_zh_paper.author_info_list 解析缓存，25 家机构有值）。
    仅作「学者重叠」的敏感性对照：作者名不是学者实体，同名不同人无法区分。"""
    p = SNAP / "research_paper_authors_20261021.json"
    d = json.loads(p.read_text(encoding="utf-8"))["sets"]
    return {n: set(d.get(n, [])) for n in names}


def ent_papers() -> dict[str, int]:
    p = SNAP / "probe_a26_ent_papers.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))["papers_by_enterprise"]


# ---------------------------------------------------------------- 重叠度计算


def overlap_bundle(k: int = 12) -> dict:
    """12 家明星企业的三维 Jaccard（IPC / 学者实体 / 论文作者名）。

    * IPC 集合：`patent_ipc4_by_name`（581,585 个 IPC4×申请人 组合）；
    * 学者集合：`dwd_scholar.scholar_org_name_zh` 精确等于企业名（多数企业为 0，见覆盖率）；
    * 作者集合：`dwd_zh_paper.author_info_list` 解析出的作者姓名（同名不可区分，仅作敏感性对照，
      **不进入合成**——它不是口径里的「学者实体」维）。
    合成口径：composite = mean(IPC, 学者)，两维都可用才平均；缺维不补 0。
    学者维只在双方学者集合都非空时才算 Jaccard（一方为空是「没有数据」而不是「不重叠」）。
    """
    ents = enterprise_universe(k)
    names = [e["name_cn"] for e in ents]
    ipc = ipc_sets(names)
    sch = scholar_sets(names)
    auth = author_sets(names)
    papers = ent_papers()

    rows = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            ji = jaccard(ipc[a], ipc[b])
            js = jaccard(sch[a], sch[b]) if (sch[a] and sch[b]) else None
            ja = jaccard(auth[a], auth[b]) if (auth[a] and auth[b]) else None
            dims = [x for x in (ji, js) if x is not None]
            comp = round(sum(dims) / len(dims), 4) if dims else None
            rows.append({"a": a, "b": b, "ipc_jaccard": ji, "scholar_jaccard": js,
                         "author_jaccard": ja, "composite": comp,
                         "n_dims": len(dims),
                         "ipc_inter": len(ipc[a] & ipc[b]), "ipc_union": len(ipc[a] | ipc[b])})

    per_ent = {}
    for n in names:
        vals = [r["composite"] for r in rows if r["composite"] is not None and n in (r["a"], r["b"])]
        best = max((r for r in rows if r["composite"] is not None and n in (r["a"], r["b"])),
                   key=lambda r: r["composite"], default=None)
        per_ent[n] = {
            "n_pairs": len(vals),
            "avg_overlap": round(sum(vals) / len(vals), 4) if vals else None,
            "max_overlap": best["composite"] if best else None,
            "max_partner": (best["b"] if best and best["a"] == n else best["a"]) if best else None,
        }

    matrix = []
    for a in names:
        line = []
        for b in names:
            if a == b:
                line.append(100.0)
            else:
                r = next(x for x in rows if {x["a"], x["b"]} == {a, b})
                line.append(round(100 * r["composite"], 2) if r["composite"] is not None else None)
        matrix.append(line)

    return {"enterprises": ents, "names": names, "ipc_sets": {n: sorted(ipc[n]) for n in names},
            "scholar_sets": {n: sorted(sch[n]) for n in names},
            "author_sets": {n: sorted(auth[n]) for n in names},
            "papers": {n: int(papers.get(n, 0)) for n in names},
            "pairs": rows, "per_enterprise": per_ent, "matrix": matrix}
