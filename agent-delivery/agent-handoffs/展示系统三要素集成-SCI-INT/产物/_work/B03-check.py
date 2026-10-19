# SCI-INT-B03：总派单 15 个 metric_id 全覆盖、差集 0、卡号 200–299、无 TBD
# 运行：python 产物/_work/B03-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B03-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B03.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))
nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-TAL-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 200 <= n <= 299:
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
    pat = c["integration_pattern"]
    if pat == "IP-09":
        parent = c.get("parent_metric") or {}
        if not parent.get("seq") or not parent.get("fields"):
            raise SystemExit(f"派生卡缺母指标 seq 或字段: {c['metric_id']}")
        if c["execution"] != "同步":
            raise SystemExit(f"IP-09 应按同步读计: {c['metric_id']}")
        if c["used_by"]["srs_refs_02"] or c["used_by"]["a_cards"]:
            raise SystemExit(f"IP-09 包内无挂页却写了页面: {c['metric_id']}")
        if c["used_by"]["pages"] != "未挂页":
            raise SystemExit(f"未挂页未写明: {c['metric_id']}")
    elif pat == "IP-07":
        if c["parent_metric"] is not None:
            raise SystemExit(f"图谱库叶不应写母指标: {c['metric_id']}")
        if c["execution"] != "异步":
            raise SystemExit(f"IP-07 应按异步 Job 计: {c['metric_id']}")
    elif pat == "IP-06":
        if c["parent_metric"] is not None:
            raise SystemExit("基础库叶不应写母指标")
        if c["execution"] != "同步":
            raise SystemExit("IP-06 应按同步读计")

flow = next(c for c in cards if c["metric_id"] == "M_TALENT_FLOW_TRACK")
if "SE-B02-02" not in flow["structure_escalation_id"]:
    raise SystemExit("流动卡未引用 SE-B02-02")
if "dwd_talent_flow" not in raw:
    raise SystemExit("未引用 dwd_talent_flow")
for banned_table in ("dwd_talent_move", "dwd_talent_flow_edge", "dwd_scholar_flow"):
    if banned_table in raw:
        raise SystemExit(f"另造了流动边表: {banned_table}")

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")

sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")
assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 15
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 15 and got == expect
assert len(set(nums)) == 15
assert doc["execution_count"] == {"sync": sync, "async": async_n}
assert [e["id"] for e in doc["structure_escalations"]] == ["SE-B03-01", "SE-B03-02"]
assert doc["structure_escalation_refs"][0]["id"] == "SE-B02-02"

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("structure_escalation_refs:", [e["id"] for e in doc["structure_escalation_refs"]])
print("OK")
