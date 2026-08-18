# -*- coding: utf-8 -*-
"""Generate per-L5 prompts from _template.md + 功能清单需规. Skip T11."""
from __future__ import annotations

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
RUN = ROOT / "gkx-orchestration" / "agent-delivery" / "qa" / "total-set" / "KJZTFWXT" / "fp-split-run"
TPL = (RUN / "prompts" / "_template.md").read_text(encoding="utf-8")
L4_TARGETS = ["产业服务链分析", "产业链分析", "企业分析", "政策分析", "综合智能分析"]
SKIP = {"T11"}

# ID, l4, l5, budget
TASKS = [
    ("T01", "产业链分析", "产业链全景图谱", "40–50"),
    ("T02", "产业链分析", "产业周期分析", "32–44"),
    ("T03", "产业链分析", "区域产业指数评价", "32–44"),
    ("T04", "产业链分析", "产业关键环节识别", "34–46"),
    ("T05", "产业链分析", "产业瓶颈堵点识别", "32–44"),
    ("T06", "产业链分析", "深圳产业情况分析对比", "34–46"),
    ("T07", "产业链分析", "深圳产业发展分析", "18–24"),
    ("T08", "产业链分析", "区域产业竞争力评价", "32–44"),
    ("T09", "企业分析", "重点企业类型分析", "36–48"),
    ("T10", "企业分析", "重点企业领域分布分析", "16–22"),
    ("T12", "企业分析", "企业商业力评估对比分析", "32–44"),
    ("T13", "企业分析", "深圳企业现状分析", "32–44"),
    ("T14", "企业分析", "招引企业推荐分析", "36–46"),
    ("T15", "企业分析", "培育企业推荐分析", "34–44"),
    ("T16", "企业分析", "企业供应链关系分析", "36–48"),
    ("T17", "企业分析", "企业发展痛难点分析", "32–44"),
    ("T18", "企业分析", "企业竞争力分析", "32–44"),
    ("T19", "政策分析", "政策时序分析", "32–44"),
    ("T20", "政策分析", "区域政策对比", "32–44"),
    ("T21", "政策分析", "深圳政策现状分析", "40–52"),
    ("T22", "产业服务链分析", "服务机构产业领域分析", "32–44"),
    ("T23", "产业服务链分析", "服务机构新增趋势分析", "32–44"),
    ("T24", "产业服务链分析", "服务机构技术力评估分析", "34–46"),
    ("T25", "产业服务链分析", "服务链短板分析", "36–48"),
    ("T26", "产业服务链分析", "服务链图谱分析", "36–48"),
    ("T27", "产业服务链分析", "引入服务机构推荐分析", "36–46"),
    ("T28", "产业服务链分析", "培育服务机构推荐分析", "36–46"),
    ("T29", "产业服务链分析", "深圳服务链现状分析", "30–42"),
    ("T30", "综合智能分析", "区域创新活力分析", "42–54"),
    ("T31", "综合智能分析", "区域创新要素分析", "42–54"),
    ("T32", "综合智能分析", "区域创新协同分析", "42–54"),
]


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def load_l5() -> dict[tuple[str, str], list[tuple[str, str]]]:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技专题服务系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        if "需规功能描述" in "".join(str(x or "") for x in row[:14]):
            header_idx = i
            break
    cur = [""] * 6
    g: dict[tuple[str, str], list[tuple[str, str]]] = OrderedDict()
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (6, 7, 8, 9, 10, 11)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        if cur[3] not in L4_TARGETS:
            continue
        desc = str(vals[12]).strip() if vals[12] else ""
        if not (cur[4] or cur[5] or desc):
            continue
        g.setdefault((cur[3], cur[4]), []).append((cur[5], desc))
    wb.close()
    return g


def l6_block(items: list[tuple[str, str]]) -> str:
    parts = []
    for i, (l6, desc) in enumerate(items, 1):
        parts.append(f"**L6-{i} {l6}**  \n{desc}")
    return "\n\n".join(parts)


def main() -> None:
    data = load_l5()
    n = 0
    for tid, l4, l5, budget in TASKS:
        if tid in SKIP:
            continue
        items = data.get((l4, l5))
        if not items:
            raise SystemExit(f"missing {l4}/{l5}")
        text = TPL
        text = text.replace("复制为本任务 `prompts/Txx.md`，替换 `{Txx}` `{四级}` `{五级}` `{预算}` `{L6块}` `{重点}`。\n\n", "")
        text = text.replace("{Txx}", tid)
        text = text.replace("{四级}", l4)
        text = text.replace("{五级}", l5)
        text = text.replace("{预算}", budget)
        text = text.replace("{L6块}", l6_block(items))
        text = text.replace(
            "{重点}",
            f"按七层检查与规则层拆本五级全部 {len(items)} 条六级。金样只学拆法，禁止把技术力业务点抄到本五级。",
        )
        text = "# " + tid + " 专用提示词 · " + l5 + "\n\n" + text.lstrip("# 五级功能点拆分 · 共用提示词模板\n\n")
        out = RUN / "prompts" / f"{tid}.md"
        out.write_text(text, encoding="utf-8")
        n += 1
    print(f"wrote {n} prompts")


if __name__ == "__main__":
    main()
