# -*- coding: utf-8 -*-
"""SCI-INT-D01 自检：17 张测试卡、号段、模式各一次、调用链无 demo-。"""
import re
from pathlib import Path

text = Path(__file__).resolve().parent.parent.joinpath("SCI-INT-D01.yaml").read_text(encoding="utf-8")
lower = text.lower()
assert "tbd" not in lower, "TBD"
assert "skeleton" not in lower, "skeleton"
assert "九新" not in text

ids = [int(n) for n in re.findall(r"(?m)^  - int_id: INT-D-X-(\d{3})\s*$", text)]
assert ids == list(range(1, 18)), ids

for i in range(1, 14):
    key = f"IP-{i:02d}"
    found = re.findall(rf"(?<![A-Za-z0-9-]){key}(?!\d)", text)
    assert len(found) == 1, (key, len(found))

patterns = re.findall(r"(?m)^    integration_pattern: (.+?)\s*$", text)
assert patterns[:13] == [f"IP-{i:02d}" for i in range(1, 14)], patterns[:13]

blocks = re.split(r"(?m)^  - int_id: ", text)[1:]
assert len(blocks) == 17
for block in blocks:
    tail = block.split("test_points:", 1)[1].split("confidence:", 1)[0]
    pts = re.findall(r"(?m)^      - .+", tail)
    assert pts, block[:40]

chains = []
lines = text.splitlines()
i = 0
while i < len(lines):
    if lines[i].strip() == "call_chain:":
        buf = []
        i += 1
        while i < len(lines) and lines[i].startswith("      "):
            buf.append(lines[i])
            i += 1
        chains.append("\n".join(buf))
        continue
    i += 1
assert len(chains) == 17, len(chains)
for chain in chains:
    assert "demo-" not in chain, chain

try:
    import yaml
except ImportError:
    yaml = None
if yaml is not None:
    data = yaml.safe_load(text)
    assert data["scope_count"] == 17 and data["card_count"] == 17
    assert data["gap"] == []
    assert len(data["cards"]) == 17
    for card in data["cards"]:
        assert card["layer"] == "test"
        assert card["dimension"] == ["NONE_3E"]
        assert isinstance(card["test_points"], list) and card["test_points"]
        assert card["structure_escalation"] is False
        blob = " ".join("" if v is None else str(v) for v in card["call_chain"].values())
        assert "demo-" not in blob

print("OK")
