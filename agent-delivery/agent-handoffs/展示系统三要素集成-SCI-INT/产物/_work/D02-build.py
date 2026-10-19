# -*- coding: utf-8 -*-
"""SCI-INT-D02：从 A01–A15、B02–B09 里有对端的源卡生成测试卡。"""
from copy import deepcopy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "SCI-INT-D02.yaml"
EMPTY = (None, "none", "", "null")
CASES = ["正常", "空数据", "字段缺失", "超时降级", "鉴权失败"]
FILES = [f"SCI-INT-A{i:02d}.yaml" for i in range(1, 16)] + [
    f"SCI-INT-B{i:02d}.yaml" for i in range(2, 10)
]


def has_counterpart(value):
    return value not in EMPTY


def metric_label(metric_ids):
    if not metric_ids:
        return "无"
    return "、".join(str(item) for item in metric_ids)


def interface_pending(card):
    parts = []
    chain = card.get("call_chain") or {}
    if isinstance(chain, dict):
        parts.extend(str(v) for v in chain.values() if v is not None)
    status = card.get("status") or {}
    if isinstance(status, dict):
        for key in ("lumen", "demo"):
            if status.get(key) is not None:
                parts.append(str(status[key]))
    blob = "\n".join(parts)
    return ("未实现" in blob) or ("draft" in blob.lower())


def applicable_cases(pattern):
    if pattern == "IP-08":
        return list(CASES)
    if pattern == "IP-10":
        # 无来源：不要「正常有数」，也不单列鉴权失败
        return ["空数据", "字段缺失", "超时降级"]
    if pattern == "IP-09":
        # 读父快照，不单列鉴权失败
        return ["正常", "空数据", "字段缺失", "超时降级"]
    return ["正常", "空数据", "字段缺失", "超时降级"]


def field_text(card):
    fields = (card.get("contract_draft") or {}).get("response_key_fields") or []
    if not fields:
        return "（无）"
    return "、".join(str(item) for item in fields)


def contract_point(card, pending):
    iid = card["int_id"]
    mid = metric_label(card.get("metric_ids"))
    fields = field_text(card)
    verdict = "待测" if pending else "按字段核对，不预填通过结论"
    if card.get("integration_pattern") == "IP-10":
        body = (
            f"正常项改为空态，禁止伪造数值，不得把 response_key_fields（{fields}）填成有数"
        )
    else:
        body = f"正常响应带上 response_key_fields：{fields}"
    return f"契约：源卡 {iid}，metric_id {mid}。{body}。判定：{verdict}。trace 可关联。"


def degrade_point(card):
    iid = card["int_id"]
    mid = metric_label(card.get("metric_ids"))
    if card.get("integration_pattern") == "IP-08":
        body = "超时与鉴权失败后空态，凭据不进前端"
    else:
        body = "超时或上游失败后空态加角标"
    return (
        f"降级：源卡 {iid}，metric_id {mid}。{body}，禁止伪造数值，"
        f"禁止回落 demo-algo-science / demo-svc-* / demo_* 库。trace 记录失败。"
    )


def load_sources():
    picked = []
    seen = set()
    for name in FILES:
        data = yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))
        for card in data.get("cards") or []:
            if not has_counterpart(card.get("counterpart")):
                continue
            iid = card["int_id"]
            if iid in seen:
                raise SystemExit(f"duplicate source int_id {iid}")
            seen.add(iid)
            picked.append(card)
    if len(picked) != 273:
        raise SystemExit(f"scope {len(picked)} != 273")
    return picked


def build_card(card, seq):
    return {
        "int_id": f"INT-D-X-{seq:03d}",
        "layer": "test",
        "source_int_id": card["int_id"],
        "dimension": deepcopy(card.get("dimension")),
        "integration_pattern": card.get("integration_pattern"),
        "counterpart": deepcopy(card.get("counterpart")),
        "jiuxin_row_id": deepcopy(card.get("jiuxin_row_id")),
        "metric_ids": deepcopy(card.get("metric_ids")),
        "call_chain": deepcopy(card.get("call_chain")),
        "contract_draft": deepcopy(card.get("contract_draft")),
        "applicable_cases": applicable_cases(card.get("integration_pattern")),
        "test_points": [
            contract_point(card, interface_pending(card)),
            degrade_point(card),
        ],
    }


def main():
    sources = load_sources()
    cards = [build_card(card, 100 + i) for i, card in enumerate(sources)]
    last = int(cards[-1]["int_id"].rsplit("-", 1)[-1])
    if last > 399:
        raise SystemExit(f"id {last} outside 100-399")
    doc = {
        "task_id": "SCI-INT-D02",
        "scope_count": 273,
        "card_count": 273,
        "gap": [],
        "cards": cards,
    }
    body = yaml.safe_dump(
        doc,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=10000,
    )
    header = (
        "# 由 D02-build.py 生成\n"
        "# SCI-INT-D02 契约测试用例集。对端：久新。\n"
        "# 源：A01–A15、B02–B09 中 counterpart 不是 none/null/空；B04 为 0。\n"
    )
    text = header + body
    if "tbd" in text.lower():
        raise SystemExit("generated text contains TBD")
    if "已通过" in text:
        raise SystemExit("generated text contains 已通过")
    if "九新" in text:
        raise SystemExit("generated text contains 九新")
    OUT.write_text(text, encoding="utf-8")
    counts = {}
    for card in cards:
        key = card["integration_pattern"]
        counts[key] = counts.get(key, 0) + 1
    print(f"cards {len(cards)}")
    print(f"ids {cards[0]['int_id']} .. {cards[-1]['int_id']}")
    print("patterns " + " ".join(f"{k}:{counts[k]}" for k in sorted(counts)))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
