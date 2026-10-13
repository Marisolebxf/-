# -*- coding: utf-8 -*-
"""Generate 算法库（旧记 KJZTFWALGO）L01-L60 split prompts. Skip existing gold L31."""
from pathlib import Path
import json
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run"
INV = json.loads((RUN / "_inventory.json").read_text(encoding="utf-8"))

src_dir = Path(r"d:/work/gkx-lumen/原始文档")
src = [f for f in src_dir.glob("*功能清单*.xlsx") if not f.name.startswith("~$")][0]
wb = openpyxl.load_workbook(src, data_only=True, read_only=True)
ws = wb["深度挖掘算法"]
rows = list(ws.iter_rows(values_only=True))


def norm(s):
    return str(s or "").strip()


desc_by_l6 = {}
cur = [""] * 6
for row in rows[3:]:
    vals = list(row) + [None] * 20
    levels = [norm(vals[j]) for j in range(7, 14)]
    for j, v in enumerate(levels[:6]):
        if v:
            cur[j] = v
            for k in range(j + 1, 6):
                cur[k] = ""
    if cur[5]:
        desc_by_l6[cur[5]] = levels[6]
wb.close()

BUDGET = {
    "T01": "40–90",
    "T02": "20–45",
    "T03": "25–45",
    "T04": "25–45",
    "T05": "25–45",
    "T06": "25–45",
    "T07": "25–45",
}
FOCUS = {
    "T01": "基础指标：点名维度的对接/清洗/处理/API/同步有独立验收则分计；规则层仍整模型一套，禁止维度×空态。",
    "T02": "图谱：点名实体/关系类型分计；API 需规写了才拆；不写图可视化控件或点击下钻。",
    "T03": "深度分析：对齐金样 L31 拆法（入参/点名指标/计算/结论/API 输出/模型级规则层）。",
    "T04": "企业深度分析：对齐金样 L31。禁止抄 L31 的技术力指标名到本六级。",
    "T05": "政策深度分析：对齐金样 L31 拆法，对象换成政策。",
    "T06": "产业服务：点名的服务机构类型分计；对齐金样规则层。",
    "T07": "综合评价：点名评价对象/要素分计；对齐金样规则层。",
}

TPL = """# {lid} {l6} · 功能点拆分提示词

子 agent 只做这一条六级。不要拆其他六级，不要写测试步骤，不要生成 Excel，不要合总表。

## 源与非源（必须遵守）

唯一需求源：本提示词里的五级/六级名称 + 需规全文。

不要读取、不要对齐：demo-algo-* / lumen-algo-* / 五件套 / 既有用例 / 其它 Lxx 业务点。

需规怎么写就怎么拆。不写页面操作。规则层挂**整模型一套**，禁止点名维度 × 空态/失败。

## 输出（必须落盘）

1. `d:/work/gkx-lumen/gkx-orchestration/agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run/work/{lid}.md`
2. `d:/work/gkx-lumen/gkx-orchestration/agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run/review/{lid}.md`

金样口径（只对照拆法与表格式，禁止抄金样业务点）：`d:/work/gkx-lumen/gkx-orchestration/agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run/work/L31.md`

原则：`d:/work/gkx-lumen/gkx-orchestration/agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md`

## 范围

- 系统：深度挖掘算法 · 科技专题服务算法库
- 功能模块（三级）：{l3}
- 子功能模块（四级）：{l4}
- 功能项（五级）：{l5}
- 子功能项（六级）：{l6}
- 页面列：填五级名「{l5}」（列约定，不表示有页面）

六级及需规原文（唯一需求源）：

```
__DESC__
```

## 条数预算

本六级合计 **{budget}** 条。不要为凑数灌水，也不要只写动作层。金样 L31 实测 40 条；禁止为冲 67 条/六级灌水。点名对象有独立验收则分计，可以略多。

## 拆法

一条 = 动作 + 对象 + 可验收规则或结果。

七层（算法语义，没有就不拆）：入参 → 指标/参数 → 取数/计算 → 结论 → API/结果结构 → 多级路径（需规未写则不拆）→ 输出（API/SDK/报告/导出/同步，需规写了才拆）。

规则层（模型级）：入参校验、空态、处理中、失败（对接/计算等验收不同才分计）。禁止笛卡尔积。禁止图表控件、点击下钻、打开页面。禁止 LLM 手段单独成点。

规则来源只允许：原文直接 / 原文隐含 / 验收补充。
拆分维度优先：算法 / 字段 / 校验 / 输出 / 状态 / 空态 / 异常。

重点：{focus}

## work/{lid}.md 格式

表头含三级/四级/五级/六级/条数/拆分维度分计/规则来源分计。
先写 `## 需规原文`（本六级全文，表内不要重复），再写四列表：`子功能项 | 功能点 | 拆分维度 | 规则来源`。子功能项填「{l6}」。

## review/{lid}.md 格式

条数与表行一致；表头分计=逐行；只覆盖本六级；无笛卡尔积/界面操作；是否误用原型或算法仓=否；抽 3 条不同验收；结论通过或需返工。
"""

out_dir = RUN / "prompts"
n = 0
skip = 0
for t in INV["tasks"]:
    lid = t["id"]
    dest = out_dir / f"{lid}.md"
    if lid == "L31" and dest.exists():
        skip += 1
        continue
    desc = desc_by_l6[t["l6"]]
    text = TPL.format(
        lid=lid,
        l3=t["l3"],
        l4=t["l4"],
        l5=t["l5"],
        l6=t["l6"],
        budget=BUDGET[t["l5_group"]],
        focus=FOCUS[t["l5_group"]],
    ).replace("__DESC__", desc)
    dest.write_text(text, encoding="utf-8")
    n += 1
print("wrote", n, "skipped_gold", skip)
