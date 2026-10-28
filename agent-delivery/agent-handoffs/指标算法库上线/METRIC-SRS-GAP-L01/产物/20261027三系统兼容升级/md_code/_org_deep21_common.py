#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORG 149 / 150 / 155 / 114 共用取数层（20261022，本批自建，零 SQL）。

为什么单独建：四件指标共用同一份机构底册（2,074 家）、同一份专利 IPC4 面板、
同一份论文面板。分头各读一次 180MB 论文 json 等于把共享实例打 4 倍。

数据源（全部本地缓存 / 三方库 gkx 的只读快照，零 demo 表）：
  _snapshots21/org_family_panel_20261021.json   2,074 家机构 × 论文/专利/项目/学者/政策/转让
  _snapshots21/patent_ipc4_by_name_20261021.json 581,585 行 [ipc4, 申请人, 件数]
  _snapshots21/plan_ipc_lexicon_gkx21.json       484 个 IPC4 的关键词分布（仅用于领域映射校验）
  _snapshots21/org_deep_probe_20261022.json     本批探针：变更记录/财务表/境外名录
  _snapshots21/a25_paper_panel.json             100,900 篇论文（署名机构串，用于实体识别评测）

本文件不发任何 SQL；只做加载、领域映射与统计函数。指标脚本只读这里，
保证四件的「机构全集 / 领域映射 / 分位口径」完全一致。
"""
from __future__ import annotations

import json
import os
import re
import statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

PANEL = os.path.join(SNAP, "org_family_panel_20261021.json")
IPC_BY_NAME = os.path.join(SNAP, "patent_ipc4_by_name_20261021.json")
PROBE = os.path.join(SNAP, "org_deep_probe_20261022.json")
PAPER = os.path.join(SNAP, "a25_paper_panel.json")

DOMAINS = ["电子信息/AI", "生物医药", "能源材料", "装备制造", "基础科学", "农业生态", "经管人文"]

# 学科 / 关键词 → 七大领域。与 _org_family_common.DISC_MAP 同源，这里保留一份
# 以免四件指标相互 import 时耦合；键按「长键优先」匹配，避免「农」吞掉「农业工程」。
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
_DISC_KEYS = sorted(DISC_MAP, key=len, reverse=True)

# IPC4 → 领域：先按「具体小类前缀」匹配，再按部（A–H）兜底。
# 规则顺序即优先级：H01M（电池）必须先于 H01（电气元件）命中，否则储能会被算进电子信息。
IPC_RULES = [
    ("C12", "生物医药"), ("C07K", "生物医药"), ("C07D", "生物医药"), ("C07H", "生物医药"),
    ("C40", "生物医药"), ("G16", "生物医药"), ("A61", "生物医药"),
    ("A01", "农业生态"), ("A21", "农业生态"), ("A22", "农业生态"),
    ("A23", "农业生态"), ("A24", "农业生态"),
    ("H01M", "能源材料"), ("H01G", "能源材料"), ("H02", "能源材料"),
    ("C", "能源材料"), ("D", "能源材料"),
    ("F", "装备制造"), ("B", "装备制造"), ("E", "装备制造"), ("G10", "装备制造"),
    ("G06", "电子信息/AI"), ("G02", "电子信息/AI"), ("G05", "电子信息/AI"),
    ("G08", "电子信息/AI"), ("G11", "电子信息/AI"), ("G21", "电子信息/AI"),
    ("H03", "电子信息/AI"), ("H04", "电子信息/AI"), ("H05", "电子信息/AI"),
    ("H01", "电子信息/AI"),
    ("G01", "基础科学"), ("G03", "基础科学"), ("G04", "基础科学"),
    ("G09", "经管人文"),
]
IPC_FALLBACK = {"A": "农业生态", "B": "装备制造", "C": "能源材料", "D": "能源材料",
                "E": "装备制造", "F": "装备制造", "G": "基础科学", "H": "电子信息/AI"}


def ipc_domain(ipc4: str) -> str:
    k = (ipc4 or "").upper()
    for pre, dom in IPC_RULES:
        if k.startswith(pre):
            return dom
    return IPC_FALLBACK.get(k[:1], "基础科学")


def text_domain(text: str) -> str | None:
    t = text or ""
    for k in _DISC_KEYS:
        if k in t:
            return DISC_MAP[k]
    return None


# ------------------------------------------------------------------ 加载

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_panel():
    return load_json(PANEL)


def load_ipc_by_name():
    """返回 {机构名: {ipc4: 件数}}，只保留底册内机构名（精确匹配，与面板专利口径一致）。"""
    panel = load_panel()
    names = {i["name"] for i in panel["institutions"]}
    out = defaultdict(dict)
    for ipc4, name, cnt in load_json(IPC_BY_NAME):
        if name in names:
            out[name][ipc4] = int(cnt)
    return dict(out)


def load_probe():
    if not os.path.exists(PROBE):
        return {}
    return load_json(PROBE)


# ------------------------------------------------------------------ 统计

def pct_rank(vals):
    """0–100 分位（并列取平均秩）。长尾分布比 minmax 稳健。"""
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


def share(counter: Counter, total: float | None = None) -> dict:
    tot = total if total is not None else sum(counter.values())
    if not tot:
        return {}
    return {k: round(v / tot, 4) for k, v in counter.most_common()}


def norm_name(s: str) -> str:
    s = re.sub(r"\s+", "", str(s or ""))
    s = s.replace("（", "(").replace("）", ")").replace("，", ",")
    return s.strip(".,;；、")


def strip_paren(s: str) -> str:
    return re.sub(r"\([^()]*\)$", "", norm_name(s))


def build_alias_index(names):
    """机构名字典：规范名 + 去尾括号别名 → 前缀索引（前 4 字）。"""
    alias = {}
    for n in names:
        nn = norm_name(n)
        if not nn:
            continue
        alias[nn] = n
        base = strip_paren(nn)
        if len(base) >= 4:
            alias.setdefault(base, n)
    idx = defaultdict(list)
    for a in alias:
        idx[a[:4]].append(a)
    return alias, idx


_MEMO: dict = {}


def match_org(text, alias, idx, min_len: int = 4):
    """自由文本机构串 → 规范机构名。规则：全等 → 前缀/包含（≥8 字）。"""
    o = norm_name(text)
    if not o:
        return None
    if o in _MEMO:
        return _MEMO[o]
    if o in alias:
        _MEMO[o] = alias[o]
        return _MEMO[o]
    best = None
    for a in idx.get(o[:4], ()):
        if len(a) < min_len:
            continue
        if o.startswith(a) or (len(a) >= 8 and a in o):
            if best is None or len(a) > len(best):
                best = a
    _MEMO[o] = alias[best] if best else None
    return _MEMO[o]


def base_years(used, missing, note):
    """基期三字段（DATA_FACTS §3.16）。used/missing 必须是 list。"""
    return {"base_years_used": list(used),
            "base_years_missing": list(missing),
            "base_years_note": note}


def write_out(obj, mid):
    path = os.path.join(HERE, f"{mid}_out.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return path
