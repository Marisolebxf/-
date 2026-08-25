# -*- coding: utf-8 -*-
import re
from pathlib import Path

print("=== LUMEN menu ===")
text = Path(r"E:/gkx-lumen/repos/lumen-ui-topic/src/router/menu.ts").read_text(encoding="utf-8")
for m in re.finditer(r"title:\s*'([^']+)',\s*\n\s*key:\s*'([^']+)'", text):
    print(f"GROUP {m.group(2)}: {m.group(1)}")
for m in re.finditer(r"navItem\('([^']+)',\s*'([^']+)',\s*'([^']+)'", text):
    print(f"  MENU {m.group(1)}/{m.group(2)}: {m.group(3)}")
for m in re.finditer(r"title:\s*'([^']+)',\s*\n\s*path:\s*'([^']+)'", text):
    print(f"  ROUTE {m.group(2)}: {m.group(1)}")

print("\n=== LUMEN views ===")
root = Path(r"E:/gkx-lumen/repos/lumen-ui-topic/src/views")
for v in sorted(root.rglob("*.vue")):
    print(" ", v.relative_to(root).as_posix())

print("\n=== DEMO sidebar/nav config candidates ===")
demo = Path(r"E:/gkx-lumen/repos/demo-ui-topic/src")
for p in sorted(demo.rglob("*")):
    if p.is_file() and any(k in p.name.lower() for k in ("nav", "menu", "sidebar", "perm")):
        print(" ", p.relative_to(demo).as_posix())

# Extract Chinese labels from demo routes handle comments and PlaceholderPage titles
routes = (demo / "app/routes.tsx").read_text(encoding="utf-8")
print("\n=== DEMO route path lines (canonical) ===")
for line in routes.splitlines():
    if 'path: "' in line or "path: '" in line:
        if any(x in line for x in ("enterprise", "industry", "policy", "service", "techchain", "development", "personal", "maintenance", "org", "chain")):
            print(line.strip()[:180])

# Try find menu definition with Chinese titles
for cand in [
    "app/config",
    "app/perms",
    "app/components",
]:
    d = demo / cand
    if d.exists():
        for f in d.rglob("*.{ts,tsx}".replace("{ts,tsx}", "*")):
            if f.suffix in {".ts", ".tsx"} and any(k in f.name.lower() for k in ("menu", "nav", "sidebar", "ia")):
                print("CAND", f)

# Search for MENU_ENT labels
print("\n=== DEMO MENU_* label map snippets ===")
for f in demo.rglob("*.ts*"):
    try:
        t = f.read_text(encoding="utf-8")
    except Exception:
        continue
    if "MENU_ENT_SEARCH" in t and ("企业查询" in t or "label" in t or "title" in t):
        print("FILE", f.relative_to(demo).as_posix())
        for line in t.splitlines():
            if "MENU_" in line and ("企业" in line or "产业" in line or "政策" in line or "机构" in line or "维护" in line or "title" in line or "label" in line):
                if len(line.strip()) < 200:
                    print(" ", line.strip())
