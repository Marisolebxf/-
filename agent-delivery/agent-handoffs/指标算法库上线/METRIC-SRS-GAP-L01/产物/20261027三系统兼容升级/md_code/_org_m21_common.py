#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORG 六件（154 / INDUSTRY_COVER / PERF_QUERY / SZ_ADVANTAGE / TECH_LAYOUT /
TECH_SCORE）共用取数层（20261022 自建，只读快照，零 SQL）。

为什么新建而不是复用 `_org_graph_common`：那个 helper 模块级 `import _devdb`，
连的是演示库，已随 M_ORG_DEEP_154_1 旧版一起隔离到 `_quarantine/20261022_demo_helper/`。
本文件的每一条数据都来自 gkx 时代落盘的快照或 `gkx` 直读：

  _snapshots21/org_family_panel_20261021.json   2,074 家机构 × 论文/专利/项目/学者/受让/政策
  _snapshots21/patent_ipc4_by_name_20261021.json 581,585 行 [ipc4, 申请人, 件数]
  _snapshots21/patent_panel_innov_20261021.json  app_year（**仅 2021—2024**，见下）
  _snapshots21/base_20261021.json               189,116 家企业底册 name→city（判「深圳企业」）
  _snapshots21/org_reg_gkx21.json               2,074 家机构登记字段（注册资本/登记日期）
  _snapshots21/papers_city_year_gkx21.json      论文作者城市（11 城白名单，仅都市圈）

口径要点（写进各件正文，不许省略）：
  1. `app_year` 的构造窗口是 WINDOW=(2021, 2024)（见 `_build_patent_panel_innov.py`），
     所以「机构 × 年」专利序列**只到 2024**；2025/2026 必须写 None 而不是 0。
  2. `papers_year` 的 2024 年是采集口径尖峰（32,379 篇，其他年 6,000 上下），
     任何年度趋势都必须标注，不能读成「2024 年论文爆发」。
  3. 底册 2,074 家 100% 在广东省（深圳 1,014 / 广州 822 / 东莞 127 / 惠州 111），
     省外机构一条都没有——这是 154 候选池与 SZ_ADVANTAGE 全国对标的硬边界。
"""
from __future__ import annotations

import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_deep21_common as OC  # noqa: E402  （纯读快照，无 DB）

SNAP = os.path.join(HERE, "_snapshots21")
PANEL = os.path.join(SNAP, "org_family_panel_20261021.json")
IPC = os.path.join(SNAP, "patent_ipc4_by_name_20261021.json")
PANEL_INNOV = os.path.join(SNAP, "patent_panel_innov_20261021.json")
BASE = os.path.join(SNAP, "base_20261021.json")
REG = os.path.join(SNAP, "org_reg_gkx21.json")
PAPER_CITY = os.path.join(SNAP, "papers_city_year_gkx21.json")

# IPC 八个部（WIPO 官方部名）。这是「技术部类」，不是「产业领域」——
# 产业口径需要 IPC→国民经济行业/深圳 20+8 链字典，库内没有（见各件 §三）。
SECTIONS = ["A", "B", "C", "D", "E", "F", "G", "H"]
SECTION_NAMES = {
    "A": "人类生活必需（农/食/医/日用）",
    "B": "作业运输（分离/成型/输送/机床）",
    "C": "化学冶金（化工/材料/生物化学）",
    "D": "纺织造纸",
    "E": "固定建筑（土木/建筑/采矿）",
    "F": "机械工程（动力/照明/加热/武器）",
    "G": "物理（测量/光学/控制/计算）",
    "H": "电学（电子/通信/电池）",
}
DOMAINS = OC.DOMAINS


# ------------------------------------------------------------------ 加载

def load_panel():
    return OC.load_panel()


def load_ipc():
    """{机构名: {ipc4: 件数}}，只保留底册内机构名（精确匹配）。"""
    return OC.load_ipc_by_name()


def load_app_year():
    """{机构名: {年(str): 件数}}，来自面板 app_year（该面板窗口 2021—2024）。"""
    panel = load_panel()
    names = {i["name"] for i in panel["institutions"]}
    raw = OC.load_json(PANEL_INNOV)["app_year"]
    out = defaultdict(dict)
    for k, c in raw.items():
        y, nm = k.split("|", 1)
        if nm in names:
            out[nm][y] = out[nm].get(y, 0) + int(c)
    return dict(out)


def load_reg():
    """{机构名: 登记字段}。该快照由 `_build_org_reg_gkx21.py` 一条 SQL 拉取并写入 source。"""
    doc = OC.load_json(REG)
    return doc, {r["name"]: r for r in doc["rows"]}


def load_base_city():
    """{企业名: 城市}。189,116 行 / 189,069 个不同名，重名取首见（仅用于判「是否深圳企业」）。"""
    rows = OC.load_json(BASE)
    out = {}
    dup = 0
    for r in rows:
        nm, city = r[2], r[4]
        if nm in out and out[nm] != city:
            dup += 1
            continue
        out.setdefault(nm, city)
    return out, dup


def load_paper_city():
    return OC.load_json(PAPER_CITY)


# ------------------------------------------------------------------ 派生

def section_of(ipc4: str) -> str:
    s = (ipc4 or "")[:1].upper()
    return s if s in SECTIONS else "?"


def section_counter(vec: dict) -> Counter:
    c = Counter()
    for k, n in vec.items():
        s = section_of(k)
        if s != "?":
            c[s] += int(n)
    return c


def hhi(counter: Counter) -> float:
    tot = sum(counter.values())
    return round(sum((v / tot) ** 2 for v in counter.values()), 4) if tot else 0.0


def entropy_norm(counter: Counter, k: int = 8) -> float:
    """香农熵按 ln(k) 归一（0=单一部类，1=八部类均分）。"""
    tot = sum(counter.values())
    if not tot or k <= 1:
        return 0.0
    e = -sum((v / tot) * math.log(v / tot) for v in counter.values() if v > 0)
    return round(e / math.log(k), 4)


def minmax_log(vals):
    """log1p 后 min-max 到 0—100。用于「有大量 0 的计数维」（如与深合著篇次）。"""
    if not vals:
        return []
    ls = [math.log1p(max(v, 0)) for v in vals]
    lo, hi = min(ls), max(ls)
    if hi <= lo:
        return [0.0 for _ in vals]
    return [round((x - lo) / (hi - lo) * 100, 1) for x in ls]


def minmax(vals):
    if not vals:
        return []
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return [0.0 for _ in vals]
    return [round((x - lo) / (hi - lo) * 100, 1) for x in vals]


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


def sz_and_candidates(inst):
    sz = [x for x in inst if x["city"] == "深圳市"]
    cand = [x for x in inst if x["city"] != "深圳市"]
    return sz, cand


def coauthor_sz(panel, city_by_name, base_city):
    """候选机构与深圳的合著（论文侧两条边）。

    返回 (inst_hits, comp_hits, detail)：
      inst_hits[候选] = 与深圳**科研机构**的合著篇次（panel.pairs，两端都在底册内）
      comp_hits[候选] = 与深圳**企业**的合著篇次（panel.inst_company_pairs 第二列企业名，
                        经 base_20261021 的 name→city 判定是否深圳）
    只算「非深候选」一侧，深圳内部互著不计。
    """
    inst_hits, comp_hits = Counter(), Counter()
    inst_detail, comp_detail = defaultdict(list), defaultdict(list)
    for a, b, n in panel.get("pairs") or []:
        ca, cb = city_by_name.get(a), city_by_name.get(b)
        if ca == "深圳市" and cb and cb != "深圳市":
            inst_hits[b] += int(n)
            inst_detail[b].append([a, int(n)])
        elif cb == "深圳市" and ca and ca != "深圳市":
            inst_hits[a] += int(n)
            inst_detail[a].append([b, int(n)])
    for a, b, n in panel.get("inst_company_pairs") or []:
        ca = city_by_name.get(a)
        if ca and ca != "深圳市" and base_city.get(b) == "深圳市":
            comp_hits[a] += int(n)
            comp_detail[a].append([b, int(n)])
    detail = {"inst": {k: v[:5] for k, v in inst_detail.items()},
              "company": {k: v[:5] for k, v in comp_detail.items()}}
    return inst_hits, comp_hits, detail


def dist(vals):
    return OC.dist(vals)


def write_out(obj, mid):
    return OC.write_out(obj, mid)


def base_years(used, missing, note):
    return OC.base_years(used, missing, note)


def pct_rank(vals):
    return OC.pct_rank(vals)
