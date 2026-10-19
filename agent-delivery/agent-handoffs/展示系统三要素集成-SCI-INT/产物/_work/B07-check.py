# SCI-INT-B07：总派单 16 个 metric_id 全覆盖、差集 0、卡号 600–699、无 TBD
# 运行：python 产物/_work/B07-check.py（任意 cwd）
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((OUT / "_prep" / "B07-pack.yaml").read_text(encoding="utf-8"))
raw = (OUT / "SCI-INT-B07.yaml").read_text(encoding="utf-8")
doc = yaml.safe_load(raw)

expect = [m["metric_id"] for m in pack["metrics"]]
by_id = {m["metric_id"]: m for m in pack["metrics"]}
cards = doc["cards"]
got = [c["metric_id"] for c in cards]
gap = sorted(set(expect).symmetric_difference(got))

MODEL = [
    "M_TECH_DS_07_TECH_INNOV_002",
    "M_TECH_DS_07_TECH_INNOV_004",
    "M_TECH_DS_07_TECH_INNOV_006",
]
MODEL_A09 = {
    "M_TECH_DS_07_TECH_INNOV_002": "INT-A-X-0805",
    "M_TECH_DS_07_TECH_INNOV_004": "INT-A-X-0807",
    "M_TECH_DS_07_TECH_INNOV_006": "INT-A-X-0809",
}
STAT = [
    "M_TECH_HEAT_QUERY",
    "M_TECH_INVEST_AMOUNT",
    "M_TECH_OUTPUT_SCALE",
    "M_TECH_PAPER_PATENT_CNT",
]
PARENT_SEQ = {
    "M_TECH_CONVERT_BOTTLENECK": 136,
    "M_TECH_HEAT_INDEX": 134,
    "M_TECH_LIFE_STAGE": 137,
    "M_TECH_MATURITY_LEVEL": 137,
    "M_TECH_POTENTIAL_SCORE": 135,
    "M_TECH_STAGE_JUDGE": 137,
    "M_TECH_SZ_ASSESS": 138,
    "M_TECH_TOPIC_HEAT": 134,
}


def pages_of(metric_id):
    src = by_id[metric_id]
    pages = []
    for row in src.get("srs_refs_02") or []:
        if row["page"] not in pages:
            pages.append(row["page"])
    for a in pack["a_cards"]:
        if metric_id in (a.get("metric_ids") or []) and a.get("page_ref") not in pages:
            pages.append(a["page_ref"])
    return pages


nums = []
for c in cards:
    m = re.fullmatch(r"INT-B-TECH-(\d+)", c["int_id"])
    if not m:
        raise SystemExit(f"卡号非法: {c['int_id']}")
    n = int(m.group(1))
    if not 600 <= n <= 699:
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
    if src["b01"]["pattern"] != "IP-10" and c["integration_pattern"] == "IP-10":
        raise SystemExit(f"已有模式却标了 IP-10: {c['metric_id']}")
    if c["integration_pattern"] != "IP-10" and not c.get("inputs"):
        raise SystemExit(f"缺输入: {c['metric_id']}")
    if not c.get("outputs"):
        raise SystemExit(f"缺输出: {c['metric_id']}")
    if c["execution"] not in ("同步", "异步"):
        raise SystemExit(f"执行方式未写明: {c['metric_id']}")
    if "D12" not in " ".join(c.get("risks") or []):
        raise SystemExit(f"未记 D12: {c['metric_id']}")
    expect_pages = pages_of(c["metric_id"])
    got_pages = c["used_by"]["pages"]
    if not expect_pages:
        if got_pages != "未挂页":
            raise SystemExit(f"未挂页未写明: {c['metric_id']}")
    elif sorted(got_pages) != sorted(expect_pages):
        raise SystemExit(f"页面与包不一致: {c['metric_id']} {got_pages} != {expect_pages}")
    pat = c["integration_pattern"]
    if pat == "IP-04":
        if c["metric_id"] not in MODEL or c["execution"] != "异步":
            raise SystemExit(f"IP-04 只用于三条 MODEL 且为异步: {c['metric_id']}")
        if c["algorithm_type"] != "MODEL":
            raise SystemExit(f"MODEL 注册值被改: {c['metric_id']}")
        blob = " ".join(c["conflicts"]) + " " + " ".join(c["decision_needed"])
        a09 = MODEL_A09[c["metric_id"]]
        for token in ("MODEL", "missing", "demo-algo-science", "D12", "IP-04", a09, "DN-05"):
            if token not in blob:
                raise SystemExit(f"MODEL 冲突未写全 {token}: {c['metric_id']}")
        if "不改注册" not in blob:
            raise SystemExit(f"未声明不改注册值: {c['metric_id']}")
        if "SE-B07-01" not in c["structure_escalation_id"]:
            raise SystemExit(f"MODEL 未挂任务表: {c['metric_id']}")
    elif pat == "IP-01":
        if c["metric_id"] not in STAT or c["execution"] != "同步":
            raise SystemExit(f"IP-01 只用于四条 STAT 且为同步: {c['metric_id']}")
        if c["algorithm_type"] != "STAT":
            raise SystemExit(f"STAT 注册值被改: {c['metric_id']}")
        if "不经 Python" not in c["call_chain"]["python"]:
            raise SystemExit(f"STAT 未写只读 ADS、不经 Python: {c['metric_id']}")
        if "只读 ADS" not in c["call_chain"]["java"] and "只读 ADS" not in c["execution_note"]:
            raise SystemExit(f"STAT 未写只读 ADS: {c['metric_id']}")
        if "SE-B07-02" not in c["structure_escalation_id"]:
            raise SystemExit(f"STAT 未升新表: {c['metric_id']}")
        if c["structure_escalation_owner"] != "human:李伟":
            raise SystemExit(f"新表未升李伟: {c['metric_id']}")
    elif pat == "IP-09":
        parent = c.get("parent_metric") or {}
        if parent.get("seq") != PARENT_SEQ[c["metric_id"]] or not parent.get("fields"):
            raise SystemExit(f"派生卡缺母指标 seq 或字段: {c['metric_id']}")
        if c["execution"] != "同步":
            raise SystemExit(f"IP-09 应按同步读计: {c['metric_id']}")
        if not c["jiuxin_row_id"]:
            raise SystemExit(f"IP-09 缺久新行: {c['metric_id']}")
    elif pat == "IP-10":
        if c["metric_id"] != "M_TECH_COMPOSITE_SCORE":
            raise SystemExit(f"IP-10 只允许综合分: {c['metric_id']}")
        if c["jiuxin_row_id"] is not None or c["execution"] != "同步":
            raise SystemExit("综合分 IP-10 应无久新行且同步空态")
        if "DN-03" not in " ".join(c["decision_needed"]):
            raise SystemExit("综合分未登记 DN-03")
    else:
        raise SystemExit(f"未预期模式: {pat}")

banned = "TB" + "D"
if banned in raw:
    raise SystemExit("yaml 含禁用占位")

sync = sum(1 for c in cards if c["execution"] == "同步")
async_n = sum(1 for c in cards if c["execution"] == "异步")
assert doc["scope_count"] == doc["card_count"] == len(cards) == len(expect) == 16
assert doc["gap"] == [] and gap == []
assert len(set(got)) == 16 and got == expect
assert nums == list(range(600, 616))
assert doc["execution_count"] == {"sync": sync, "async": async_n} == {"sync": 13, "async": 3}
assert doc["jiuxin_rows"] == ["SRS-134", "SRS-135", "SRS-136", "SRS-137", "SRS-138"]
assert [e["id"] for e in doc["structure_escalations"]] == ["SE-B07-01", "SE-B07-02"]
assert all(e["owner"] == "human:李伟" for e in doc["structure_escalations"])
assert doc["model_owner"]["registry_algorithm_type"] == "MODEL"
assert doc["model_owner"]["a2_status"] == "missing"

print(f"cards={len(cards)} expect={len(expect)} gap={gap}")
print(f"int_ids={min(nums)}-{max(nums)} unique={len(set(nums))}")
print(f"sync={sync} async={async_n}")
print("jiuxin_rows:", doc["jiuxin_rows"])
print("structure_escalation:", [e["id"] for e in doc["structure_escalations"]])
print("OK")
