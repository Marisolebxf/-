# 从 _prep/{叶}-pack.yaml 写出卡片骨架，避免子智能体读完材料却不落盘。
# 已有 SCI-INT-{叶}.yaml 的不覆盖。运行：python 产物/_work/PREP-skeleton.py A09 A13
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
PREP = OUT / "_prep"
START = {f"A{i:02d}": (i - 1) * 100 for i in range(1, 16)}


def card(n, srs):
    return {
        "int_id": f"INT-A-X-{n:04d}",
        "layer": "page",
        "srs": {"excel_row": srs["excel_row"], "seq": srs["seq"], "path": srs["path"]},
        "page_ref": srs.get("page_ref"),
        "dimension": ["OTHER"],
        "dep_kind": ["data"],
        "metric_ids": [m["metric_id"] for m in srs.get("metrics") or []],
        "metric_domain_other": [],
        "algorithm_type": "UNKNOWN",
        "integration_pattern": "TBD",
        "ours": ["frontend"],
        "counterpart": "none",
        "delivery_form": "unknown",
        "jiuxin_row_id": None,
        "call_chain": {"fe_route": None, "java": "TBD", "python": "TBD", "downstream": "TBD"},
        "contract_draft": {"request": [], "response_key_fields": [], "granularity": {"time": "TBD", "geo": "TBD"}, "freshness": "TBD"},
        "status": {"demo": "TBD", "lumen": "TBD", "d1_d4": {}},
        "gaps": [],
        "conflicts": [],
        "decision_needed": [],
        "structure_escalation": False,
        "risks": [],
        "test_points": [],
        "confidence": "low",
        "skeleton": True,
    }


def main():
    for leaf in sys.argv[1:]:
        dest = OUT / f"SCI-INT-{leaf}.yaml"
        if dest.exists():
            print(f"skip {leaf}: yaml exists")
            continue
        pack = yaml.safe_load((PREP / f"{leaf}-pack.yaml").read_text(encoding="utf-8"))
        srs = sorted(pack["srs"], key=lambda x: x["excel_row"])
        base = START[leaf]
        cards = [card(base + i, s) for i, s in enumerate(srs)]
        doc = {"task_id": f"SCI-INT-{leaf}", "scope_count": len(srs), "card_count": len(cards),
               "gap": [], "note": "骨架由 PREP-skeleton.py 生成。TBD / skeleton:true 必须补完并删掉 skeleton 字段。",
               "cards": cards}
        dest.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
        print(f"{leaf}: cards={len(cards)} ids={cards[0]['int_id']}..{cards[-1]['int_id']}")


if __name__ == "__main__":
    main()
