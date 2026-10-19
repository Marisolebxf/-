# -*- coding: utf-8 -*-
"""SCI-INT-D04 自检：15 叶、号段 600–799、trace / 降级 / 性能。"""
import re
from pathlib import Path

import yaml

text = Path(__file__).resolve().parent.parent.joinpath("SCI-INT-D04.yaml").read_text(encoding="utf-8")
assert "tbd" not in text.lower(), "TBD"
assert "九新" not in text

data = yaml.safe_load(text)
assert data["scope_count"] == 15 and data["card_count"] == 15
assert data["gap"] == []
cards = data["cards"]
assert len(cards) == 15

leaves = [c["source_leaf"] for c in cards]
assert leaves == [f"A{i:02d}" for i in range(1, 16)], leaves

ids = []
for card in cards:
    m = re.fullmatch(r"INT-D-X-(\d{3})", card["int_id"])
    assert m, card["int_id"]
    n = int(m.group(1))
    assert 600 <= n <= 799, n
    ids.append(n)
    assert card["layer"] == "test"
    assert card["page_ref"]
    assert card["source_int_id"]
    assert card["integration_pattern"]
    tp = "\n".join(card["trace_points"])
    assert "前端" in tp and "Java" in tp, card["int_id"]
    assert "空态" in card["degrade"], card["int_id"]
    assert "待确认" in card["performance"], card["int_id"]
    assert "待确认" in card["timeout_budget"], card["int_id"]
    cc = card["call_chain"]
    chain = "\n".join(
        ["" if cc.get(k) is None else str(cc.get(k)) for k in ("fe_route", "java", "python", "downstream")]
        + list(card["trace_points"])
    )
    if "demo-" in chain:
        assert "禁止" in chain, card["int_id"]

assert ids == list(range(600, 615)), ids
assert len(set(leaves)) == 15
print("OK")
