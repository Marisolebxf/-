#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KEYPANO 五件套共用件（2026-10-23）

五件（ENTERPRISE_LIST / MATCH_COUNT / QUAL_DISTRIBUTION / REGIONAL_COUNT /
REGIONAL_DISTRIBUTION）读同一份快照 `code/_snapshots21/keypano_base_20261023.json`，
只在 GROUP BY 的键上不同。共用的是：链名、链位中文、区域键解析、六类资质码、
百分比口径、产物落盘格式。放一处，避免五个脚本各写一遍导致口径漂移。

设计原则：本模块**不连库**。快照由 `_build_keypano_base_20261023.py`（连库一次）
与 `_enrich_keypano_base_20261023.py`（离线补维）产出，五件套只读盘。
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
BASE = SNAP / "keypano_base_20261023.json"
TREE = SNAP / "chain_tree_20261021.json"
ADMIN = SNAP / "admin_area_20261022.json"

QUAL_CODES = ("foreign", "high_tech", "sme", "listed", "little_giant", "little_giant_pro")
QUAL_CN = {
    "foreign": "外资",
    "high_tech": "高新",
    "sme": "小微（科技型中小企业代理）",
    "listed": "上市",
    "little_giant": "专精特新",
    "little_giant_pro": "小巨人",
}
QUAL_FIELD = {
    "foreign": "foreign_proxy",
    "high_tech": "high_tech",
    "sme": "sme",
    "listed": "listed_proxy",
    "little_giant": "little_giant",
    "little_giant_pro": "little_giant_pro",
}
STAGE_CN = {"up": "上游", "mid": "中游", "down": "下游"}
SCOPE_CN = {"gba": "粤港澳大湾区", "yrd": "长三角", "jjj": "京津冀"}


def load_base() -> dict:
    return json.loads(BASE.read_text(encoding="utf-8"))


def chain_names() -> dict:
    t = json.loads(TREE.read_text(encoding="utf-8"))
    return {r["industry_code"]: r["industry_name"] for r in t}


def admin_names() -> tuple:
    """返回 (省码→省名, 市码→市名, 区县码→区县名)。码取前 2/4/6 位。"""
    rows = json.loads(ADMIN.read_text(encoding="utf-8"))["rows"]
    p, c, a = {}, {}, {}
    for r in rows:
        if r.get("province_code"):
            p.setdefault(r["province_code"][:2], r.get("province_name") or "")
        if len(r.get("city_code") or "") >= 4:
            c.setdefault(r["city_code"][:4], r.get("city_name") or "")
        if len(r.get("area_code") or "") >= 6:
            a.setdefault(r["area_code"][:6], r.get("area_name") or "")
    return p, c, a


def key_kind(k: str) -> str:
    """区域键类型：prov / city / area / scope。"""
    if k.startswith("scope:"):
        return "scope"
    code = k.split(":", 1)[1]
    return {2: "prov", 4: "city", 6: "area"}.get(len(code), "unknown")


def key_label(k: str, p: dict, c: dict, a: dict) -> str:
    kind = key_kind(k)
    if kind == "scope":
        return SCOPE_CN.get(k.split(":", 1)[1], k)
    code = k.split(":", 1)[1]
    if kind == "prov":
        return p.get(code, code)
    if kind == "city":
        return c.get(code, code)
    if kind == "area":
        return a.get(code, code)
    return k


def parent_key(k: str) -> str | None:
    """区域键的上一级：区县→市→省→None。复合区域无上级。"""
    kind = key_kind(k)
    code = k.split(":", 1)[1] if ":" in k else ""
    if kind == "area":
        return "admin:" + code[:4]
    if kind == "city":
        return "admin:" + code[:2]
    return None


def pct(a: float, b: float, nd: int = 4) -> float:
    """同母体百分比。分母为 0 时返回 0.0，绝不返回 None（下游按数读）。"""
    if not b:
        return 0.0
    return round(a / b * 100, nd)


def tag_of(firm: dict, code: str) -> bool:
    return bool(firm.get(QUAL_FIELD[code]))


def matched_firms(base: dict) -> list:
    """上链企业（有 chain_code），链级统计的母体。"""
    return [f for f in base["firms"] if f.get("chains")]


def member_rows(base: dict) -> list:
    """成员行 (org_id, chain, stage)。链位来自一级环节映射，无链位不上成员表。"""
    rows = []
    for f in base["firms"]:
        for chain, stages in (f.get("chain_stages") or {}).items():
            for st in stages:
                rows.append({"org_id": f["org_id"], "name": f["name"],
                             "chain_code": chain, "node_stage": st,
                             "province": f.get("province"), "city": f.get("city"),
                             "area": f.get("area"), "credit_code": f.get("credit_code")})
    return rows


def shared_base_block(base: dict) -> dict:
    st = base["stats"]
    return {
        "snapshot": "code/_snapshots21/keypano_base_20261023.json",
        "roster_n": st["roster_n"],
        "roster_rule": base["roster_rule"],
        "in_chain_n": st["in_chain_n"],
        "in_chain_pct": st["in_chain_pct"],
        "with_stage_n": st["with_stage_n"],
        "chain_n": len(st["chain_firm_n"]),
        "chain_stage_cell_n": st["chain_stage_cell_n"],
        "member_row_n": st["chain_stage_pair_n"],
        "scan_rows": st["scan_rows"],
        "scan_bad_credit_rows": st["scan_bad_credit_rows"],
    }


def base_years_block() -> dict:
    return {
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、"
            "区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。"
            "不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。"
        ),
    }


def dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print(f"[ok] {path.name}  {path.stat().st_size / 1024:.1f} KB")
