#!/usr/bin/env python3
"""live 版 OpenAPI 与代码实况对账：所有 live 端点必须有 Controller 代码支撑。
用法: python3 check_live_contract.py  · 退出码 0=全部对上"""
import glob
import json
import re
import sys

LIVE = "CMS-JX-OpenAPI-v1.0-live.json"
CTRL = "/Users/xutengqiang/Desktop/xtq/projects/gdf/projects/repos/lumen-svc-platform/gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/controller"

spec = json.load(open(LIVE, encoding="utf-8"))

# 从 Controller 代码重建完整端点集（RequestMapping 前缀 + PostMapping）
code_paths = set()
for f in glob.glob(f"{CTRL}/*.java"):
    src = open(f, encoding="utf-8").read()
    m = re.search(r'@RequestMapping\("([^"]+)"\)', src)
    pre = m.group(1) if m else ""
    for mp in re.findall(r'@PostMapping\("([^"]+)"\)', src):
        code_paths.add(pre + mp)

def norm(p: str) -> str:
    """归一化：{x} 段→{}，去前缀"""
    return re.sub(r"\{[^}]+\}", "{}", p).replace("/api/open/cms/v1", "")

code_norm = {norm(p) for p in code_paths}
bad = [p for p in spec["paths"] if norm(p) not in code_norm]

print(f"live 端点 {len(spec['paths'])} 个，代码端点 {len(code_paths)} 个，无代码支撑 {len(bad)} 个")
for b in bad:
    print("  ✗", b)
sys.exit(1 if bad else 0)
