# ponytail: one-shot verify for TOPIC-ALGO-GAP-L02; delete after signoff if unused
from collections import Counter
from pathlib import Path

import yaml

root = Path(__file__).resolve().parents[3]
topic = root / "metrics" / "request" / "专题系统"
l01 = yaml.safe_load((topic / "TOPIC-ALGO-GAP-L01.yaml").read_text(encoding="utf-8"))
l02 = yaml.safe_load((topic / "TOPIC-ALGO-GAP-L02.yaml").read_text(encoding="utf-8"))
cat = yaml.safe_load((topic / "A2-GAP-page-catalog.yaml").read_text(encoding="utf-8"))

items = l02["items"]
print("item_count", len(items), "header", l02.get("item_count"))
vc = Counter(i.get("差集判定") for i in items)
print("verdicts", dict(vc))

mapped = [i for i in items if i.get("差集判定") == "mapped"]
missing = [i for i in items if i.get("差集判定") == "missing"]
tp = [i for i in items if i.get("差集判定") == "third_party"]

mapped_no_req = [i["row_id"] for i in mapped if not i.get("A1需规ID")]
mapped_no_leaf = [i["row_id"] for i in mapped if not i.get("A1指标叶ID")]
col14_temp = [
    i["row_id"]
    for i in items
    if str(i.get("metric_id") or "").startswith("TEMP_ALGO_")
]
missing_with_a1 = [i["row_id"] for i in missing if i.get("A1需规ID") or i.get("A1指标叶ID")]
tp_empty = [i["row_id"] for i in tp if not i.get("A1需规ID")]

print("mapped_no_req", mapped_no_req)
print("mapped_no_leaf", mapped_no_leaf)
print("col14_TEMP_ALGO", col14_temp)
print("missing_with_a1", missing_with_a1)
print("missing_ids", sorted(i["row_id"] for i in missing))
print("third_party_empty_a1", tp_empty)

l01_v = Counter(i.get("差集判定") for i in l01["items"])
print("l01_verdicts", dict(l01_v))
print("verdict_row_diff", [
    (a["row_id"], a.get("差集判定"), b.get("差集判定"))
    for a, b in zip(l01["items"], l02["items"])
    if a.get("差集判定") != b.get("差集判定") or a["row_id"] != b["row_id"]
])

opens = []
for p in cat.get("pages", []):
    st = (p.get("metric_open") or {}).get("metric_open_status")
    opens.append((p.get("page_id"), st))
print("catalog_open", opens)
print("present", sum(1 for _, s in opens if s == "present"))

ds = root / "metrics" / "request" / "展示系统" / "DS-ALGO-GAP-L02.yaml"
print("ds_l02_exists", ds.exists())
