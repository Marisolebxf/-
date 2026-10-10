# -*- coding: utf-8 -*-
from collections import Counter, defaultdict
from pathlib import Path
import openpyxl

d = Path(r"d:\work\gkx-lumen\gkx-orchestration\agent-delivery\qa\total-set\KJZTFWXT\科技专题战略分析")
files = sorted(d.glob("6.国际科技信息中心项目_*_测试用例.xlsx"))

PAD = {
    "入口可达", "权限控制", "加载态", "空数据态", "异常态", "筛选条件", "条件重置",
    "排序", "分页", "详情下钻", "图表展示", "图表联动", "导出", "指标说明",
    "时间范围", "区域维度", "对比", "搜索", "推荐", "报告生成", "参数配置",
    "图谱交互", "预警提示", "数据时效", "结果一致性",
}

print(
    f"{'四级功能':<14}{'总用例':>6}{'功能项=通用质量属性':>18}"
    f"{'占比':>8}{'六级数':>6}{'通用/模块':>10}{'模板补齐合计':>12}"
)
print("-" * 86)

for fp in files:
    wb = openpyxl.load_workbook(fp, data_only=True)
    ws = wb["功能测试用例"]
    total = generic = pad_all = 0
    per_mod = defaultdict(lambda: [0, 0])
    for r in range(3, ws.max_row + 1):
        mod = (ws.cell(r, 2).value, ws.cell(r, 3).value)
        feat = ws.cell(r, 4).value or ""
        point = str(ws.cell(r, 7).value or "")
        total += 1
        per_mod[mod][0] += 1
        if feat == "通用质量属性":
            generic += 1
            per_mod[mod][1] += 1
        base = point.split("-")[0]
        if feat == "通用质量属性" or base in PAD:
            pad_all += 1
    l4 = fp.name.replace("6.国际科技信息中心项目_", "").replace("_测试用例.xlsx", "")
    nmod = len(per_mod)
    print(
        f"{l4:<14}{total:>6}{generic:>18}{generic/total*100:>7.1f}%"
        f"{nmod:>6}{generic/nmod:>10.1f}{pad_all:>12}"
    )
    dist = Counter(v[1] for v in per_mod.values())
    print(f"  每模块「功能项=通用质量属性」条数分布: {dict(sorted(dist.items()))}")
