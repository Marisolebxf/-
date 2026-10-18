# SCI-INT-B01：B01 映射 vs P00-baseline 自检（93=93、差集空、IP 合法、类型一致、久新行合法）
# 运行：python 产物/_work/B01-check.py（任意 cwd）
from collections import Counter
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
p00 = yaml.safe_load((OUT / "P00-baseline.yaml").read_text(encoding="utf-8"))
b01 = yaml.safe_load((OUT / "SCI-INT-B01.yaml").read_text(encoding="utf-8"))

base = {m["metric_id"]: m for m in p00["metrics"]}
rows = b01["initial_mapping"]
ids = [r["metric_id"] for r in rows]
ip_ids = {p["id"] for p in b01["patterns"]}
jx_ids = {j["row_id"] for j in p00["jiuxin_rows"]}

assert len(ids) == len(set(ids)), f"重复: {[k for k, v in Counter(ids).items() if v > 1]}"
missing, extra = set(base) - set(ids), set(ids) - set(base)
bad_ip = [r["metric_id"] for r in rows if r["pattern"] not in ip_ids]
bad_type = [r["metric_id"] for r in rows if r["metric_id"] in base and r["algorithm_type"] != base[r["metric_id"]]["algorithm_type"]]
bad_leaf = [r["metric_id"] for r in rows if r["metric_id"] in base and r["b_leaf"] != base[r["metric_id"]]["leaf"]]
bad_jx = [r["metric_id"] for r in rows if r["jiuxin_row_id"] is not None and r["jiuxin_row_id"] not in jx_ids]

print(f"scope_count={b01['scope_count']} baseline={len(base)} mapped={len(ids)}")
print(f"差集 baseline-mapped={sorted(missing)} mapped-baseline={sorted(extra)}")
print(f"非法IP={bad_ip} 类型不一致={bad_type} 叶不一致={bad_leaf} 非法久新行={bad_jx}")
print("patterns:", sorted(ip_ids))
print("按 IP:", dict(sorted(Counter(r["pattern"] for r in rows).items())))
print("按类型:", dict(Counter(r["algorithm_type"] for r in rows)))
print(f"挂久新行={sum(r['jiuxin_row_id'] is not None for r in rows)} 无久新行={sum(r['jiuxin_row_id'] is None for r in rows)}")
print("未被映射引用的久新行:", sorted(jx_ids - {r["jiuxin_row_id"] for r in rows}))

assert b01["scope_count"] == b01["card_count"] == len(base) == len(ids) == 93
assert not (missing or extra or bad_ip or bad_type or bad_leaf or bad_jx)
assert b01["gap"] == []
print("OK")
