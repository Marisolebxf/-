# -*- coding: utf-8 -*-
"""SCI-INT-D03 自检：93 张源卡 metric 恰好覆盖一次，号段 400–599。"""
import yaml
from pathlib import Path

PROD = Path(__file__).resolve().parent.parent


def metric_id_of(card):
    if card.get("metric_id"):
        return card["metric_id"]
    mids = card.get("metric_ids") or []
    if len(mids) != 1:
        raise SystemExit(f"metric_id count {card.get('int_id') or card.get('source_int_id')} {mids}")
    return mids[0]


def main():
    sources = []
    for number in range(2, 10):
        doc = yaml.safe_load((PROD / f"SCI-INT-B{number:02d}.yaml").read_text(encoding="utf-8"))
        sources.extend(doc["cards"])
    text = (PROD / "SCI-INT-D03.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    cards = data["cards"]
    assert data["scope_count"] == 93 and data["card_count"] == 93
    assert data["gap"] == []
    assert len(sources) == len(cards) == 93

    src_ids = [metric_id_of(card) for card in sources]
    out_ids = [metric_id_of(card) for card in cards]
    assert len(src_ids) == len(set(src_ids)) == 93
    assert src_ids == out_ids, "差集不为 0"
    assert "tbd" not in text.lower(), "TBD"
    assert "九新" not in text
    assert "select " not in text.lower()

    seen = []
    unable = 0
    for src, card in zip(sources, cards):
        number = int(card["int_id"].rsplit("-", 1)[1])
        assert card["int_id"].startswith("INT-D-X-")
        assert 400 <= number <= 599
        assert number not in seen
        seen.append(number)
        assert card["layer"] == "test"
        assert card["source_int_id"] == src["int_id"]
        assert card["integration_pattern"] == src["integration_pattern"]
        assert card["algorithm_type"] == src["algorithm_type"]
        assert card["jiuxin_row_id"] == src.get("jiuxin_row_id")
        reconcile = card["reconcile"]
        assert isinstance(reconcile, dict)
        method = reconcile.get("method")
        assert isinstance(method, str) and method.strip()
        if method == "无法对账":
            unable += 1
            assert reconcile.get("reason"), card["int_id"]
        for physical in reconcile.get("physical") or []:
            low = str(physical).lower()
            assert "demo_" not in low and "demo-" not in low, physical
        readiness = reconcile["readiness"]
        d4 = readiness.get("d4") if isinstance(readiness, dict) else None
        d3 = readiness.get("d3") if isinstance(readiness, dict) else None
        if d4 == "mock":
            assert reconcile["result_stage"] != "live"
        if d3 == "none":
            assert reconcile["conclusion"] == "排除"
        assert reconcile["upgrade_path"] == "mock→ingesting→live"
        assert reconcile["id_hit_rate"]["definition"] == "能对上主数据键的记录 / 抽样记录"
        assert reconcile["id_hit_rate"]["threshold"] == "待确认"
    assert seen == list(range(400, 493)), seen
    for line in text.splitlines():
        low = line.lower()
        if "demo_" in low or "demo-" in low:
            assert "不得作为通过条件" in line, line
    assert unable == sum(
        1 for card in sources
        if card.get("integration_pattern") == "IP-10" or not (card.get("metric_id") or card.get("metric_ids"))
    )
    print("OK")


if __name__ == "__main__":
    main()
