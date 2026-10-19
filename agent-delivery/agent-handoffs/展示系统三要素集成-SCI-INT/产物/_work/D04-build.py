# -*- coding: utf-8 -*-
"""从 A01–A15 各抽一张代表卡，生成 SCI-INT-D04 端到端测试卡。"""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "SCI-INT-D04.yaml"

DEGRADE = (
    "超时或上游失败 → 空态 + 角标，禁止伪造数值，"
    "禁止回落 demo-algo-science / demo-svc-* / demo_*。"
)
PERFORMANCE = "待确认。超时预算待确认。"


def nonempty(v):
    if v is None:
        return False
    return str(v).strip() not in ("", "null", "None", "~")


def no_online_python(py):
    if not nonempty(py):
        return True
    s = str(py)
    return ("不经 Python" in s) or ("无 Python" in s) or ("不经过 Python" in s)


def guard_demo(v):
    if not nonempty(v):
        return v
    s = str(v).replace("九新", "久新")
    if re.search(r"demo[-_]", s) and "禁止" not in s:
        s += "（正式用例禁止回落 demo_ 库与 demo- 服务）"
    return s


def checkpoint(text):
    s = "" if text is None else str(text).strip()
    m = re.search(r"(GET|POST|PUT|DELETE)\s+([^\s（(]+)", s)
    if m:
        return f"{m.group(1)} {m.group(2).rstrip('，,;；')}"
    if not s:
        return "未命名"
    return s.split("。")[0][:80]


def python_line(card):
    cc = card.get("call_chain") or {}
    py = cc.get("python")
    if not no_online_python(py):
        return f"Python /internal：检查点 {checkpoint(py)}"
    down = "" if cc.get("downstream") is None else str(cc.get("downstream"))
    if "无 ADS" in down:
        return "Python 检查点=不适用（无在线 /internal，无 ADS 读）"
    return "Python 检查点=不适用，Java 读 ADS"


def timeout_budget(ip):
    if ip == "IP-08":
        return "草案 2s 同步上限然后转异步（待确认）"
    if ip == "IP-04":
        return "异步不设页面同步超时，轮询间隔草案 5s（待确认）"
    return "草案 3s（待确认）"


def trace_points(card):
    cc = card.get("call_chain") or {}
    fe = cc.get("fe_route")
    fe_name = fe if nonempty(fe) else f"{card.get('page_ref')}（路由未登记）"
    py_line = python_line(card)
    return [
        f"前端 observability：检查点 {fe_name}",
        f"Java 网关：检查点 {checkpoint(cc.get('java'))}",
        py_line,
    ]


def pick(cards):
    for card in cards:
        if nonempty((card.get("call_chain") or {}).get("java")):
            return card, False
    return cards[0], True


def one(leaf, seq, cards):
    src, unimplemented = pick(cards)
    cc = src.get("call_chain") or {}
    card = {
        "int_id": f"INT-D-X-{seq:03d}",
        "layer": "test",
        "source_leaf": leaf,
        "source_int_id": src.get("int_id"),
        "page_ref": src.get("page_ref"),
        "integration_pattern": src.get("integration_pattern"),
        "call_chain": {
            "fe_route": guard_demo(cc.get("fe_route")),
            "java": guard_demo(cc.get("java")),
            "python": guard_demo(cc.get("python")),
            "downstream": guard_demo(cc.get("downstream")),
        },
        "trace_points": trace_points(src),
        "timeout_budget": timeout_budget(src.get("integration_pattern")),
        "degrade": DEGRADE,
        "performance": PERFORMANCE,
    }
    if unimplemented:
        card["chain_note"] = "链路未实现"
    return card


def main():
    cards = []
    for i in range(1, 16):
        leaf = f"A{i:02d}"
        path = ROOT / f"SCI-INT-{leaf}.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        cards.append(one(leaf, 600 + i - 1, data["cards"]))
    doc = {
        "task_id": "SCI-INT-D04",
        "scope_count": 15,
        "card_count": 15,
        "gap": [],
        "cards": cards,
    }
    header = (
        "# SCI-INT-D04 端到端链路与非功能（spike）\n"
        "# 15 张 = A01–A15 各 1 条代表链路。号段 INT-D-X-600–614。\n"
        "# 代表卡取该叶第一张 call_chain.java 非空的卡；全空则取第一张并注明链路未实现。\n"
        "# 对端：久新。超时预算与性能均为草案，待确认。\n"
    )
    body = yaml.safe_dump(
        doc, allow_unicode=True, sort_keys=False, width=1000
    ).replace("九新", "久新")
    OUT.write_text(header + body, encoding="utf-8")
    print(f"wrote {OUT.name} cards={len(cards)}")


if __name__ == "__main__":
    main()
