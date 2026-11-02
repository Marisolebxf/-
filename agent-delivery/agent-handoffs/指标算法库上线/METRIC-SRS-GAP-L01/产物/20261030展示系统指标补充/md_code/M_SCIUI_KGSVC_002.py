#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGSVC_002 复现入口（薄壳校验型）——计算与产物产出在合算脚本 M_SCIUI_KGIND_002_KGSVC_001_002_004.py（幂等可重跑）。
本壳做存在性+判档+基期三键校验，不重复计算、零漂移。"""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(HERE, "M_SCIUI_KGSVC_002_out.json")
if not os.path.exists(out_path):
    sys.exit("产物缺失——请先跑 python3 " + os.path.join(HERE, "M_SCIUI_KGIND_002_KGSVC_001_002_004.py"))
out = json.load(open(out_path, encoding="utf-8"))
for k in ("support_judgment", "base_years_used", "base_years_missing", "base_years_note"):
    assert k in out, f"产物缺 {k}"
print("M_SCIUI_KGSVC_002 verified: ", out["support_judgment"], "| 复现入口: M_SCIUI_KGIND_002_KGSVC_001_002_004.py")
