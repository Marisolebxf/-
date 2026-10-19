# -*- coding: utf-8 -*-
"""SCI-INT-D02 自检：对端源卡恰好覆盖一次，号段、契约/降级、无 TBD、demo- 须带禁止。"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "SCI-INT-D02.yaml"
EMPTY = (None, "none", "", "null")
FILES = [f"SCI-INT-A{i:02d}.yaml" for i in range(1, 16)] + [
    f"SCI-INT-B{i:02d}.yaml" for i in range(2, 10)
]
CASES = ["正常", "空数据", "字段缺失", "超时降级", "鉴权失败"]


def source_cards():
    picked = []
    for name in FILES:
        data = yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))
        for card in data.get("cards") or []:
            if card.get("counterpart") in EMPTY:
                continue
            picked.append(card)
    return picked


def main():
    sources = source_cards()
    src_by_id = {}
    for card in sources:
        iid = card["int_id"]
        assert iid not in src_by_id, iid
        src_by_id[iid] = card
    assert len(src_by_id) == 273, len(src_by_id)

    text = OUT.read_text(encoding="utf-8")
    assert "tbd" not in text.lower(), "TBD"
    assert "九新" not in text
    assert text.startswith("# 由 D02-build.py 生成")

    data = yaml.safe_load(text)
    assert data["scope_count"] == 273
    assert data["card_count"] == 273
    assert data["gap"] == []
    cards = data["cards"]
    assert len(cards) == 273

    nums = []
    covered = []
    for card in cards:
        assert card["layer"] == "test"
        num = int(card["int_id"].removeprefix("INT-D-X-"))
        assert 100 <= num <= 399, card["int_id"]
        nums.append(num)
        sid = card["source_int_id"]
        assert sid in src_by_id, sid
        covered.append(sid)
        src = src_by_id[sid]
        assert card["dimension"] == src.get("dimension")
        assert card["integration_pattern"] == src.get("integration_pattern")
        assert card["counterpart"] == src.get("counterpart")
        assert card["jiuxin_row_id"] == src.get("jiuxin_row_id")
        assert card["metric_ids"] == src.get("metric_ids")
        assert card["call_chain"] == src.get("call_chain")
        assert card["contract_draft"] == src.get("contract_draft")
        points = card["test_points"]
        assert isinstance(points, list) and len(points) >= 2
        assert points[0].startswith("契约：")
        assert points[1].startswith("降级：")
        blob = "\n".join(points)
        assert sid in blob
        mids = src.get("metric_ids") or []
        if mids:
            for mid in mids:
                assert str(mid) in blob, (sid, mid)
        else:
            assert "metric_id 无" in blob
        assert "trace" in blob
        assert "已通过" not in blob
        pattern = card["integration_pattern"]
        cases = card["applicable_cases"]
        assert set(cases) <= set(CASES)
        if pattern == "IP-08":
            assert cases == CASES
        elif pattern == "IP-10":
            assert "正常" not in cases
        elif pattern == "IP-09":
            assert "鉴权失败" not in cases
        chain = yaml.safe_dump(card["call_chain"], allow_unicode=True)
        combined = chain + "\n" + blob
        if "demo-" in combined:
            assert "禁止" in combined, sid

    assert len(nums) == len(set(nums))
    assert nums == list(range(100, 100 + len(nums))), nums[:3]
    assert covered == list(src_by_id), "source order or gap"
    assert set(covered) == set(src_by_id)
    print(f"覆盖数 {len(covered)}")
    print("OK")


if __name__ == "__main__":
    main()
