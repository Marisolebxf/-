# -*- coding: utf-8 -*-
"""SCI-INT-C05 采集：扫前序产物里 structure_escalation=true 的卡片与顶层块，输出原始提法清单。

用法：python C05-collect.py [--dump]   -> 写 _work/C05-raw-mentions-late.yaml（不覆盖已有 C05-raw-mentions.yaml）
原始提法 raw_id = {task}:{int_id 或 顶层路径}
"""
import sys, io, pathlib, yaml, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ["SCI-INT-B01", "SCI-INT-C01", "SCI-INT-C02", "SCI-INT-C03", "SCI-INT-C04",
       "SCI-INT-A01", "SCI-INT-A02", "SCI-INT-A03", "SCI-INT-A04", "SCI-INT-A05",
       "SCI-INT-A06", "SCI-INT-A07", "SCI-INT-A08", "SCI-INT-A09", "SCI-INT-A10",
       "SCI-INT-A11", "SCI-INT-A12", "SCI-INT-A13", "SCI-INT-A14", "SCI-INT-A15",
       "SCI-INT-B02", "SCI-INT-B03", "SCI-INT-B04", "SCI-INT-B05", "SCI-INT-B06",
       "SCI-INT-B07", "SCI-INT-B08", "SCI-INT-B09"]


def walk(node, path, out):
    """顶层块中任何带 structure_escalation: true 的 dict 都算一条提法。"""
    if isinstance(node, dict):
        if node.get("structure_escalation") is True:
            out.append((path, node))
        for k, v in node.items():
            if k == "cards":
                continue
            walk(v, f"{path}.{k}" if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)


def collect():
    rows = []
    for t in SRC:
        d = yaml.safe_load((ROOT / f"{t}.yaml").read_text(encoding="utf-8"))
        for c in d.get("cards", []) or []:
            if c.get("structure_escalation") is True:
                rows.append({"raw_id": f"{t}:{c['int_id']}", "task": t, "kind": "card", "node": c})
        top = []
        walk({k: v for k, v in d.items() if k != "cards"}, "", top)
        for p, n in top:
            rows.append({"raw_id": f"{t}:{p}", "task": t, "kind": "top", "node": n})
    return rows


if __name__ == "__main__":
    rows = collect()
    by = {}
    for r in rows:
        by.setdefault(r["task"], [0, 0])[0 if r["kind"] == "card" else 1] += 1
    for t in SRC:
        print(t, "cards/top =", by.get(t, [0, 0]))
    print("TOTAL raw mentions:", len(rows))
    if "--dump" in sys.argv:
        out = ROOT / "_work" / "C05-raw-mentions-late.yaml"
        slim = []
        for r in rows:
            n = r["node"]
            slim.append({
                "raw_id": r["raw_id"],
                "kind": r["kind"],
                "keys": sorted(n.keys()),
                "gaps": n.get("gaps"),
                "risks": n.get("risks"),
                "conflicts": n.get("conflicts"),
                "downstream": (n.get("call_chain") or {}).get("downstream") if isinstance(n.get("call_chain"), dict) else None,
                "other": {k: v for k, v in n.items() if k not in ("gaps", "risks", "conflicts", "call_chain", "test_points", "status", "srs", "contract_draft")},
            })
        out.write_text(yaml.safe_dump(slim, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
        print("dumped ->", out)
