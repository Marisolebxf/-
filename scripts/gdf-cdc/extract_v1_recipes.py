#!/usr/bin/env python3
"""Turn v1 执行结果 into structured calibrate catalogs (not a raw xlsx copy)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
DEFAULT_GOLD = Path(
    r"agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/执行结果"
)

LEFT_COLS = list("ABCDEFGHIJ")
RIGHT_COLS = list("KLMNOPQRSTUVWX")


def cell(ws, col: str, row: int):
    return ws[f"{col}{row}"].value


def pack(ws, cols: list[str], row: int) -> dict[str, object]:
    out = {}
    for col in cols:
        v = cell(ws, col, row)
        if v not in (None, ""):
            out[col] = v
    return out


def is_num(v) -> bool:
    if isinstance(v, int):
        return True
    if isinstance(v, float) and v == int(v):
        return True
    return bool(isinstance(v, str) and re.fullmatch(r"\d+", v.strip()))


def classify_left(ws, row: int) -> dict | None:
    a, b = cell(ws, "A", row), cell(ws, "B", row)
    if a == "别名" and b == "数据类型":
        return {"kind": "src_header", "cells": pack(ws, LEFT_COLS, row)}
    if b == "数据表":
        return {"kind": "src_alias", "cells": pack(ws, LEFT_COLS, row)}
    if a == "序号" and b == "英文名称":
        return {"kind": "field_header", "cells": pack(ws, LEFT_COLS, row)}
    if is_num(a) and b:
        return {"kind": "field", "cells": pack(ws, LEFT_COLS, row)}
    packed = pack(ws, LEFT_COLS, row)
    return {"kind": "left_misc", "cells": packed} if packed else None


def classify_right(ws, row: int) -> dict | None:
    k, l, o, p = cell(ws, "K", row), cell(ws, "L", row), cell(ws, "O", row), cell(ws, "P", row)
    if k == "关联条件" and l == "过滤条件":
        return {"kind": "col_header", "cells": pack(ws, RIGHT_COLS, row)}
    if k == "步骤" and l == "映射规则":
        return {"kind": "map_header", "cells": pack(ws, RIGHT_COLS, row)}
    if p in ("输出表", "临时视图") or o == "MainOutput" or (
        isinstance(o, str) and re.fullmatch(r"IV\d+", o)
    ):
        return {"kind": "out_alias", "cells": pack(ws, RIGHT_COLS, row)}
    if p and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", str(p)) and l not in (None, "", "映射规则"):
        return {"kind": "map", "cells": pack(ws, RIGHT_COLS, row)}
    packed = pack(ws, RIGHT_COLS, row)
    return {"kind": "right_misc", "cells": packed} if packed else None


def parse_data_result(ws) -> dict:
    max_r = 1
    for row in ws.iter_rows():
        for c in row:
            if c.value not in (None, "") and c.row > max_r:
                max_r = c.row
    events = []
    for r in range(3, max_r + 1):
        left = classify_left(ws, r)
        right = classify_right(ws, r)
        if left is None and right is None:
            continue
        events.append({"row": r, "left": left, "right": right})
    return {
        "a1": cell(ws, "A", 1),
        "a2": cell(ws, "A", 2),
        "k2": cell(ws, "K", 2),
        "events": events,
    }


def parse_index(ws) -> dict:
    cells = {}
    for row in ws.iter_rows():
        for c in row:
            if c.value not in (None, ""):
                cells[c.coordinate] = c.value
    return {"cells": cells}


def parse_conversion(ws) -> dict:
    return parse_index(ws)


def extract_wave_a(path: Path) -> dict:
    wb = load_workbook(path, data_only=False)
    out = {"index": parse_index(wb["索引"]), "sheets": {}}
    for name in wb.sheetnames:
        if name == "索引":
            continue
        out["sheets"][name] = parse_conversion(wb[name])
    out["sheet_order"] = list(wb.sheetnames)
    return out


def extract_wave_b(path: Path) -> dict:
    wb = load_workbook(path, data_only=False)
    out = {"index": parse_index(wb["索引"]), "sheets": {}, "sheet_order": list(wb.sheetnames)}
    for name in wb.sheetnames:
        if name == "索引":
            continue
        out["sheets"][name] = parse_data_result(wb[name])
    return out


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", default=str(DEFAULT_GOLD))
    ap.add_argument("-o", "--out", default=str(HERE / "v1_calibrate_catalogs.json"))
    args = ap.parse_args()
    gold = Path(args.gold)
    recipes = {
        "_comment": (
            "v1 校准目录：按数据结果页左右栏事件序列重建。"
            "fill --calibrate 克隆壳后先清空再按事件填写；禁止当 v2 施工真源。"
        ),
        "wave_a": extract_wave_a(gold / "1、贴源_模板.xlsx"),
        "wave_b": extract_wave_b(gold / "2、明细数据_模板.xlsx"),
    }
    Path(args.out).write_text(json.dumps(recipes, ensure_ascii=False, indent=2), encoding="utf-8")
    nb = sum(len(s.get("events") or []) for s in recipes["wave_b"]["sheets"].values())
    print(f"wrote {args.out} wave_b_event_rows={nb}")


if __name__ == "__main__":
    main()
