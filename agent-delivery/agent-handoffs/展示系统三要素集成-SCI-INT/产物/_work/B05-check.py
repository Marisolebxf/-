# SCI-INT-B05：11 个 metric_id 全覆盖、差集 0、卡号 400–499、无 TBD
# 运行：python 产物/_work/B05-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B05-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B05.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))
nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-TECH-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 400 <= n <= 499:
        raise SystemExit(f"卡号越界: {c['int_id']}")
    nums.append(n)

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")

assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 11
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 11 and got == expect
assert len(set(nums)) == 11
assert all(c["layer"] == "metric" for c in cards)
assert all(c["integration_pattern"] == c_pack["b01"]["pattern"] == "IP-08"
           for c, c_pack in zip(cards, pack["metrics"]))
assert all(c["algorithm_type"] == "third_party" for c in cards)
assert all(c["integration_pattern"] != "IP-10" for c in cards)
assert all(c["jiuxin_row_id"] for c in cards)
assert all(c["execution"] == "异步" for c in cards)
sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")

by_id = {c["metric_id"]: c for c in cards}
d134 = [r["row"] for r in by_id["M_TECH_DEEP_134_1"]["used_by"]["display_rows"]]
d135 = [r["row"] for r in by_id["M_TECH_DEEP_135_1"]["used_by"]["display_rows"]]
d137 = [r["row"] for r in by_id["M_TECH_DEEP_137_1"]["used_by"]["display_rows"]]
assert d134 == [
    "DS-03-RESULT-001",
    "DS-03-RESULT-002",
    "DS-09-COMPREHENSIVE-001",
    "DS-09-COMPREHENSIVE-002",
    "DS-09-COMPREHENSIVE-004",
]
assert d135 == ["DS-07-TECH-INNOV-003", "DS-07-INDUSTRY-POTENTIAL-002"]
assert d137 == [
    "DS-03-RESULT-004",
    "DS-03-RESULT-005",
    "DS-03-RESULT-006",
    "DS-07-SCI-CREATE-003",
]
assert by_id["M_TECH_DEEP_135_1"]["page_ref"] == "未挂页"
se = [e["id"] for e in doc["structure_escalations"]]
assert se == ["SE-B05-01"]
assert doc["structure_escalations"][0]["owner"] == "human:李伟"
assert doc["tech_point"]["new_master_table"] is False

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", se)
print("OK")
