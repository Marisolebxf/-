# -*- coding: utf-8 -*-
"""Count 功能点 vs 用例 per total-set Excel."""
from pathlib import Path
from collections import Counter
import openpyxl

d = Path(r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJZTFWXT\科技专题战略分析")
files = sorted(d.glob("6.国际科技信息中心项目_*_测试用例.xlsx"))

# stable order matching L4_TARGETS
order = ["综合智能分析", "政策分析", "企业分析", "产业链分析", "产业服务链分析"]

def l4_name(fp: Path) -> str:
    return fp.name.replace("6.国际科技信息中心项目_", "").replace("_测试用例.xlsx", "")

rows_out = []
print(f"{'四级功能':<14}{'用例数':>8}{'功能点(行)':>10}{'去重功能点':>10}{'一对多用例':>10}")
print("-" * 56)

tot_cases = tot_fp_rows = tot_fp_uniq = 0
for name in order:
    fps = [f for f in files if l4_name(f) == name]
    if not fps:
        continue
    fp = fps[0]
    wb = openpyxl.load_workbook(fp, data_only=True)
    ws = wb["功能测试用例"]
    points = []
    for r in range(3, ws.max_row + 1):
        p = ws.cell(r, 7).value  # 功能点
        if p is None and ws.cell(r, 1).value is None:
            continue
        points.append(str(p or "").strip())
    cases = len(points)
    uniq = len(set(points))
    # how many 功能点 have >1 case
    c = Counter(points)
    multi = sum(1 for k, v in c.items() if v > 1 and k)
    print(f"{name:<14}{cases:>8}{cases:>10}{uniq:>10}{multi:>10}")
    tot_cases += cases
    tot_fp_rows += cases
    tot_fp_uniq += uniq
    rows_out.append((name, cases, uniq, multi))

print("-" * 56)
print(f"{'合计':<14}{tot_cases:>8}{tot_fp_rows:>10}{tot_fp_uniq:>10}")
print()
print("说明: 当前生成策略为「每功能点通常 1 条用例」，故用例数≈功能点行数；")
print("去重功能点≈用例数（仅当同名功能点重复时会小于用例数）。")
