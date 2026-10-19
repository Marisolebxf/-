# SCI-INT-B08：总派单 7 个 metric_id 全覆盖、差集 0、卡号 700–799、无 TBD
# 运行：python 产物/_work/B08-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B08-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B08.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))


def pages_of(metric_id):
    src = by_id[metric_id]
    pages = []
    for row in src.get("srs_refs_02") or []:
        if row["page"] not in pages:
            pages.append(row["page"])
    for a in pack.get("a_cards") or []:
        if metric_id in (a.get("metric_ids") or []) and a.get("page_ref") not in pages:
            pages.append(a["page_ref"])
    return pages


def split_io(metric_id):
    inputs, outputs = [], []
    for c in pack["c_cards"]:
        if metric_id not in (c.get("metric_ids") or []):
            continue
        if c.get("delivery_form") == "API" and c.get("counterpart") == "jiuxin":
            outputs.append(c["int_id"])
        else:
            inputs.append(c["int_id"])
    return inputs, outputs


nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-ORG-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 700 <= n <= 799:
        raise SystemExit(f"卡号越界: {c['int_id']}")
    nums.append(n)
    src = by_id[c["metric_id"]]
    if c["layer"] != "metric":
        raise SystemExit(f"layer 不是 metric: {c['int_id']}")
    if c["integration_pattern"] != src["b01"]["pattern"]:
        raise SystemExit(f"模式与包不一致: {c['metric_id']}")
    if c["algorithm_type"] != src["b01"]["algorithm_type"]:
        raise SystemExit(f"algorithm_type 被改: {c['metric_id']}")
    if c["jiuxin_row_id"] != src["b01"]["jiuxin_row_id"]:
        raise SystemExit(f"久新行被改: {c['metric_id']}")
    if c["jiuxin_row_id"] and c["integration_pattern"] == "IP-10":
        raise SystemExit(f"有久新行却标了 IP-10: {c['metric_id']}")
    if c["integration_pattern"] != "IP-08":
        raise SystemExit(f"未预期模式: {c['integration_pattern']}")
    if c["parent_metric"] is not None:
        raise SystemExit(f"库叶不应写母指标: {c['metric_id']}")
    if c["execution"] != "异步":
        raise SystemExit(f"IP-08 在 SLA 未确认时应按异步计: {c['metric_id']}")
    if not c.get("inputs") or not c.get("outputs"):
        raise SystemExit(f"缺输入或输出: {c['metric_id']}")
    if "D12" not in " ".join(c.get("risks") or []):
        raise SystemExit(f"未记 D12: {c['metric_id']}")
    expect_pages = pages_of(c["metric_id"])
    got_pages = c["used_by"]["pages"]
    if not expect_pages:
        if got_pages != "未挂页":
            raise SystemExit(f"未挂页未写明: {c['metric_id']}")
    elif sorted(got_pages) != sorted(expect_pages):
        raise SystemExit(f"页面与包不一致: {c['metric_id']} {got_pages} != {expect_pages}")
    expect_in, expect_out = split_io(c["metric_id"])
    got_in = [i["c_card"] for i in c["inputs"]]
    missing = sorted(set(expect_in) - set(got_in))
    extra = sorted(set(got_in) - set(expect_in) - {"INT-C-ORG-240"})
    if missing or extra:
        raise SystemExit(f"输入与包不一致: {c['metric_id']} missing={missing} extra={extra}")
    if "INT-C-ORG-240" not in got_in:
        raise SystemExit(f"未引用机构主数据: {c['metric_id']}")
    if expect_out != [c["outputs"]["c_card"]]:
        raise SystemExit(f"输出 API 卡与包不一致: {c['metric_id']} {expect_out}")
    if c["structure_escalation_id"] != ["SE-B08-01"]:
        raise SystemExit(f"未挂 SE-B08-01: {c['metric_id']}")
    if c["structure_escalation_owner"] != "human:李伟":
        raise SystemExit(f"升级负责人不是李伟: {c['metric_id']}")
    if c["metric_id"] == "M_ORG_DEEP_153_1":
        blob = " ".join(c["conflicts"])
        if "INT-A-X-0817" not in blob or "IP-08" not in blob:
            raise SystemExit("153 未写明 A09 纠偏且保持 IP-08")
        if c["integration_pattern"] == "IP-10":
            raise SystemExit("153 被标成 IP-10")

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")
if "INT-C-ORG-240" not in raw or "不另造" not in raw:
    raise SystemExit("未引用 C03 机构主数据或不另造声明缺失")
if doc["a09_correction"]["this_leaf_pattern"] != "IP-08":
    raise SystemExit("153 纠偏未保持 IP-08")
if doc["a09_correction"]["a09_pattern"] != "IP-10":
    raise SystemExit("未记录 A09 的错误标法")

sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")
assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 7
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 7 and got == expect
assert nums == list(range(700, 707))
assert doc["execution_count"] == {"sync": sync, "async": async_n} == {"sync": 0, "async": 7}
assert doc["jiuxin_rows"] == [f"SRS-{n}" for n in range(149, 156)]
assert [e["id"] for e in doc["structure_escalations"]] == ["SE-B08-01"]
assert doc["structure_escalations"][0]["owner"] == "human:李伟"
assert [e["id"] for e in doc["structure_escalation_refs"]][0] == "INT-C-ORG-240"

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("structure_escalation_refs:", [e["id"] for e in doc["structure_escalation_refs"]])
print("pattern_153:", by_id["M_ORG_DEEP_153_1"]["b01"]["pattern"])
print("OK")
