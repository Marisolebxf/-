from collections import Counter
from openpyxl import load_workbook

p = "agent-delivery/metrics/request/专题系统/TOPIC-ALGO-GAP-L02.xlsx"
wb = load_workbook(p, data_only=False)
print("sheets", wb.sheetnames)
ws = wb["清单"]
headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
print("headers", headers)
print("max_row", ws.max_row)
verdicts = []
col14_temp = []
mapped_empty = []
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    vals = {headers[i]: row[i].value for i in range(len(headers))}
    v = vals.get("差集判定")
    if v is None:
        continue
    verdicts.append(v)
    mid = str(vals.get("metric_id") or "")
    if mid.startswith("TEMP_ALGO_"):
        col14_temp.append(vals.get("row_id") or row[0].value)
    if v == "mapped" and not vals.get("A1需规ID"):
        mapped_empty.append(vals.get("row_id") or row[0].value)
print("xlsx_verdicts", dict(Counter(verdicts)), "n", len(verdicts))
print("xlsx_col14_TEMP", col14_temp)
print("xlsx_mapped_empty_a1", mapped_empty)
sc = wb["计数"]
print("B5", sc["B5"].value, "B12", sc["B12"].value)
print("B11", sc["B11"].value, "B13", sc["B13"].value)
bf = wb["回填清单"]
print("回填 max_row", bf.max_row, "headers", [c.value for c in next(bf.iter_rows(min_row=1, max_row=1))])
