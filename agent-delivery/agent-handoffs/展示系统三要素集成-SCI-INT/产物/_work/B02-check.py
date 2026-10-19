# SCI-INT-B02：10 个 metric_id 全覆盖、差集 0、卡号 100–199、无 TBD
# 运行：python 产物/_work/B02-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B02-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B02.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))
nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-TAL-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 100 <= n <= 199:
        raise SystemExit(f"卡号越界: {c['int_id']}")
    nums.append(n)

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")

assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 10
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 10 and got == expect
assert len(set(nums)) == 10
assert all(c["layer"] == "metric" for c in cards)
assert all(c["integration_pattern"] == "IP-08" for c in cards)
assert all(c["algorithm_type"] == "third_party" for c in cards)
assert all(c["execution"] == "异步" for c in cards)
sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("OK")
