# SCI-INT-B04：7 个 metric_id 全覆盖、差集 0、卡号 300–399、无 TBD
# 运行：python 产物/_work/B04-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B04-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B04.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = []
for c in cards:
    ids = c.get("metric_ids") or []
    if len(ids) != 1:
        raise SystemExit(f"每卡应只绑 1 个 metric_id: {c['int_id']}")
    got.append(ids[0])
gap = sorted(set(expect).symmetric_difference(got))

DS16 = {
    "M_TALENT_DS_16_TALENT_RECRUIT_005",
    "M_TALENT_DS_16_TALENT_RECRUIT_006",
    "M_TALENT_DS_16_TALENT_RECRUIT_007",
    "M_TALENT_DS_16_TALENT_RECRUIT_010",
    "M_TALENT_DS_16_TALENT_RECRUIT_013",
    "M_TALENT_DS_16_TALENT_RECRUIT_025",
}
OWNER = "owner 三选一：久新扩包 / 我方自研 / 范围调整。不写成久新已提供"
nums = []
for c, mid in zip(cards, got):
    m = re.fullmatch(r"INT-B-(?:TAL|TECH|ORG|X)-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 300 <= n <= 399:
        raise SystemExit(f"卡号越界: {c['int_id']}")
    nums.append(n)
    src = by_id[mid]
    if c["layer"] != "metric":
        raise SystemExit(f"layer 不是 metric: {c['int_id']}")
    if c["integration_pattern"] != src["b01"]["pattern"]:
        raise SystemExit(f"模式与包不一致: {mid}")
    if c["algorithm_type"] != src["b01"]["algorithm_type"]:
        raise SystemExit(f"algorithm_type 被改: {mid}")
    if c["jiuxin_row_id"] != src["b01"]["jiuxin_row_id"]:
        raise SystemExit(f"久新行被改: {mid}")
    if c["jiuxin_row_id"] is not None:
        raise SystemExit(f"出现久新行号: {mid}")
    down = (c.get("call_chain") or {}).get("downstream") or ""
    if "SE-B03-01" not in down:
        raise SystemExit(f"主档未引用 SE-B03-01: {mid}")
    if c.get("structure_escalation") is not False:
        raise SystemExit(f"本叶不应新开结构升级: {c['int_id']}")
    if mid in DS16:
        if c["integration_pattern"] != "IP-10" or c["counterpart"] != "none":
            raise SystemExit(f"DS-16 必须 IP-10 且 counterpart none: {mid}")
        if c["delivery_form"] != "none":
            raise SystemExit(f"DS-16 不应有交付物: {mid}")
        if c.get("decision_needed") != [OWNER]:
            raise SystemExit(f"owner 三选一须留在 decision_needed: {mid}")
    if mid == "M_TALENT_STRUCT_QUERY":
        if c["algorithm_type"] != "STAT" or c["integration_pattern"] != "IP-01":
            raise SystemExit("M_TALENT_STRUCT_QUERY 必须是 STAT、IP-01")
    if mid == "M_TALENT_DS_16_TALENT_RECRUIT_013":
        risks = " ".join(c.get("risks") or [])
        if "不建费用表" not in risks:
            raise SystemExit("成本模型须写明不建费用表")
        if c["delivery_form"] != "none":
            raise SystemExit("成本模型不建费用表")

se_ids = sorted(set(re.findall(r"SE-B\d+-\d+", raw)))
if se_ids != ["SE-B03-01"]:
    raise SystemExit(f"主档只能引用 SE-B03-01，实际: {se_ids}")
if re.search(r"SRS-\d+", raw):
    raise SystemExit("yaml 出现久新行号")
for banned_table in ("dwd_talent_cost", "ads_talent_cost", "dwd_cost", "费用明细"):
    if banned_table in raw:
        raise SystemExit(f"成本模型建了费用表: {banned_table}")

placeholder = "TB" + "D"
if placeholder in raw:
    raise SystemExit("yaml 含禁用占位")

assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 7
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 7 and got == expect
assert len(set(nums)) == 7
assert sum(1 for mid in got if mid in DS16) == 6

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print("jiuxin_rows: []")
print("structure_escalation_refs: ['SE-B03-01']")
print("OK")
