# SCI-INT-A09 card self-check. Stdlib only.
import re
import sys
from pathlib import Path

YAML = Path(__file__).resolve().parents[1] / "SCI-INT-A09.yaml"
text = YAML.read_text(encoding="utf-8")
errors = []

if re.search(r"TBD", text):
    errors.append("含 TBD")
if re.search(r"skeleton", text, re.IGNORECASE):
    errors.append("含 skeleton")

scope = re.search(r"(?m)^scope_count:\s*(\d+)\s*$", text)
card_count = re.search(r"(?m)^card_count:\s*(\d+)\s*$", text)
gap = re.search(r"(?m)^gap:\s*(.*)$", text)
ids = re.findall(r"(?m)^- int_id: INT-A-(?:TAL|TECH|ORG|X)-(\d+)\s*$", text)
rows = [int(x) for x in re.findall(r"(?m)^    excel_row: (\d+)\s*$", text)]

if scope is None or int(scope.group(1)) != 23:
    errors.append("scope_count 不是 23")
if card_count is None or int(card_count.group(1)) != 23:
    errors.append("card_count 不是 23")
if len(ids) != 23:
    errors.append(f"卡片数 {len(ids)} != 23")
if gap is None or gap.group(1).strip() != "[]":
    errors.append(f"差集 gap 不是 []：{gap.group(1).strip() if gap else '缺失'}")

bad_ids = [n for n in ids if not 800 <= int(n) <= 899]
if bad_ids:
    errors.append(f"卡号不在 800–899：{bad_ids}")

want = set(range(139, 162))
got = set(rows)
if len(rows) != 23 or got != want:
    errors.append(
        f"excel 139–161 未全覆盖 missing={sorted(want - got)} extra={sorted(got - want)} n={len(rows)}"
    )

if errors:
    print("FAIL")
    for item in errors:
        print(item)
    sys.exit(1)

print("OK")
