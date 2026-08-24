# ponytail: one assert file; fails if 对人主表 counts or bans regress.
from pathlib import Path
import yaml

p = Path(__file__).resolve().parents[1] / "九新-技术机构人才" / "JIUXIN-TECH-ORG-TALENT-L01.yaml"
doc = yaml.safe_load(p.read_text(encoding="utf-8"))
items = doc["items"]
c = doc["counts_对人主表"]
assert c["rows"] == 51 == len(items)
assert c["SQL"] == 3 and c["Python"] == 6 and c["API"] == 42
assert c["待确认"] == 51 and c["确认"] == 0
assert c["库叶"] == 37 and c["无专叶项"] == 1 and c["展示third_party"] == 13
ids = {r["row_id"] for r in items}
assert "TOPIC-RORG-012" in ids
assert not ids & {"ENT-SEARCH-009", "DS-CHAIN-OV-009", "DS-CHAIN-OV-010"}
assert {r["row_id"] for r in items if r["系统"] == "展示"} == {
    "DS-03-RESULT-001",
    "DS-03-RESULT-002",
    "DS-03-RESULT-004",
    "DS-03-RESULT-005",
    "DS-03-RESULT-006",
    "DS-07-INDUSTRY-POTENTIAL-002",
    "DS-07-TECH-INNOV-003",
    "DS-07-SCI-CREATE-003",
    "DS-09-COMPREHENSIVE-001",
    "DS-09-COMPREHENSIVE-002",
    "DS-09-COMPREHENSIVE-004",
    "DS-08-VIZ-001",
    "DS-08-VIZ-004",
}
assert all(r["九新确认"] == "待确认" for r in items)
tal = [r for r in doc["topic_trace"] if r["维度"] == "人才"]
assert len(tal) == 15
assert len(doc["display_talent_mapped"]) == 18
assert len(doc["ds16_missing_appendix"]) == 6
print("ok", c)
