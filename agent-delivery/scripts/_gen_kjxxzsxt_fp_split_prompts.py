# -*- coding: utf-8 -*-
"""Generate KJXXZSXT per-L5 prompts from _template.md + 功能清单需规. Skip T27."""
from __future__ import annotations

import json
import re
from collections import OrderedDict
from pathlib import Path

import openpyxl

ROOT = Path(r"d:\work\gkx-lumen")
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
RUN = ROOT / "gkx-orchestration" / "agent-delivery" / "qa" / "total-set" / "KJXXZSXT" / "fp-split-run"
INV = json.loads((RUN / "_inventory.json").read_text(encoding="utf-8"))
TPL = (RUN / "prompts" / "_template.md").read_text(encoding="utf-8")
SKIP = {"T27"}
IN_SCOPE_MAX = 140
EXCLUDE_L3 = "科技信息展示系统数据需求"
EXCLUDE_L4 = "科技抗疫主题报告（核减需求）"

EVAL_KEYS = ("评估", "对比", "预测", "指数", "推演", "综合")
MAP_KEYS = ("地图操作", "图层", "放大", "拖动", "复位")
MAP_L5 = {"地图操作", "图层配置"}


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def load_l5() -> dict[tuple[str, str, str], list[tuple[str, str]]]:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技信息展示系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:8]):
        if "需规功能描述" in "".join(str(x or "") for x in row[:20]):
            header_idx = i
            break
    cur = [""] * 6
    g: dict[tuple[str, str, str], list[tuple[str, str]]] = OrderedDict()
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (6, 7, 8, 9, 10, 11)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        desc = str(vals[12]).strip() if vals[12] else ""
        l3, l4, l5, l6 = cur[2], cur[3], cur[4], cur[5]
        if EXCLUDE_L3 in l3 or EXCLUDE_L4 in l4:
            continue
        if not (l5 or l6 or desc):
            continue
        g.setdefault((l3, l4, l5), []).append((l6, desc))
    wb.close()
    return g


def budget(l3: str, l5: str, n6: int) -> tuple[str, int, int]:
    if l3.startswith("政策对比"):
        lo, hi = 12, 16
    elif l5 in MAP_L5 or any(k in l5 for k in MAP_KEYS):
        lo, hi = 8, 14
    elif any(k in l5 for k in EVAL_KEYS):
        lo, hi = 12, 16
    else:
        lo, hi = 10, 14
    return f"{lo * n6}–{hi * n6}", lo * n6, hi * n6


def l6_block(items: list[tuple[str, str]], l5: str) -> str:
    parts = []
    for i, (l6, desc) in enumerate(items, 1):
        name = l5 if (not l6 or l6 == "/") else l6
        body = desc or "（功能清单本行需规功能描述为空，仅按五级/六级名称拆，不发明未点名对象。）"
        note = ""
        if not l6 or l6 == "/":
            note = "（本条六级名为 `/`，子功能项列填五级名。）\n"
        parts.append(f"**L6-{i} {name}**  \n{note}{body}")
    return "\n\n".join(parts)


def focus_extra(task: dict) -> str:
    if task["l3"].startswith("政策对比"):
        return "本五级只有 1 条六级（名为 `/`），子功能项填五级名；按该需规做完整七层+规则层，条数取 12–16。"
    if task["l5"] in MAP_L5:
        return "地图/图层类贴近预算下限，但不要掉出下限；放大/缩小分计；不要发明需规未写的收藏/分享/导出。"
    return ""


def render(tid: str, task: dict, items: list[tuple[str, str]], bud: str) -> str:
    extra = focus_extra(task)
    body = TPL
    body = body.replace(
        "复制为本任务 `prompts/Txx.md`，替换 `{Txx}` `{三级}` `{四级}` `{五级}` `{预算}` `{L6块}` `{重点}`。\n\n",
        "",
    )
    body = body.replace("# 五级功能点拆分 · 共用提示词模板（展示系统）\n\n", "")
    body = body.replace("{Txx}", tid)
    body = body.replace("{三级}", task["l3"])
    body = body.replace("{四级}", task["l4"])
    body = body.replace("{五级}", task["l5"])
    body = body.replace("{预算}", bud)
    body = body.replace("{L6块}", l6_block(items, task["l5"]))
    body = body.replace(
        "{重点}",
        (
            f"按七层检查与规则层拆本五级全部 {len(items)} 条六级。"
            "金样只学拆法（work/T27.md），禁止把技术创新力业务点抄到本五级。"
            "「等」「如」只取本提示词需规已写名称。"
            "表头必须写拆分维度分计和规则来源分计，两类合计 = 条数。"
            + extra
        ),
    )
    return f"# {tid} 专用提示词 · {task['l5']}\n\n" + body.lstrip()


def main() -> None:
    data = load_l5()
    n = 0
    lo_sum = 0
    hi_sum = 0
    missing: list[str] = []
    for task in INV["tasks"]:
        tid = task["id"]
        idx = int(tid[1:])
        if idx > IN_SCOPE_MAX or tid in SKIP:
            continue
        key = (task["l3"], task["l4"], task["l5"])
        items = data.get(key)
        if not items:
            missing.append(tid + " " + "/".join(key))
            continue
        bud, lo, hi = budget(task["l3"], task["l5"], len(items))
        lo_sum += lo
        hi_sum += hi
        (RUN / "prompts" / f"{tid}.md").write_text(
            render(tid, task, items, bud), encoding="utf-8"
        )
        n += 1
    if missing:
        raise SystemExit("missing:\n" + "\n".join(missing))
    print(
        f"wrote {n} prompts; remaining budget band {lo_sum}–{hi_sum}; "
        f"plus T27=92 → table {lo_sum + 92}–{hi_sum + 92}"
    )


if __name__ == "__main__":
    main()
