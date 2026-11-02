#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_KGIND_002/KGSVC_001/002/004 复现入口（薄壳校验型）——计算与产物产出在合算脚本 M_SCIUI_KGIND_002_KGSVC_001_002_004.py
（幂等可重跑：`python3 M_SCIUI_KGIND_002_KGSVC_001_002_004.py` 逐件落 _out.json，约 11 秒）。本壳做存在性+判档+基期三键校验。"""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "M_SCIUI_KGIND_002_KGSVC_001_002_004.py")
for mid in ("M_SCIUI_KGIND_002", "M_SCIUI_KGSVC_001", "M_SCIUI_KGSVC_002", "M_SCIUI_KGSVC_004"):
    out_path = os.path.join(HERE, mid + "_out.json")
    if not os.path.exists(out_path):
        sys.exit(f"产物缺失——请先跑 python3 {RUNNER}")
    out = json.load(open(out_path, encoding="utf-8"))
    for k in ("support_judgment", "base_years_used", "base_years_missing", "base_years_note"):
        assert k in out, f"{mid} 产物缺 {k}"
    print(mid, "verified:", out["support_judgment"], "| 复现入口:", os.path.basename(RUNNER))
