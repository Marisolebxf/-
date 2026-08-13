# -*- coding: utf-8 -*-
"""从企业分析 FUNC 用例生成 R0 测试记录 Excel 空壳（只拷用例列，结果列留空待填）。"""
from __future__ import annotations

from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = Path(r"d:\work\gkx-lumen")
CASE = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "科技专题战略分析-v1.3"
    / "6.国际科技信息中心项目_企业分析_测试用例.xlsx"
)
TPL = ROOT / "原始文档" / "7.国际科技信息中心项目_xx_测试记录.xlsx"
OUT = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "科技专题战略分析-v1.3"
    / "7.国际科技信息中心项目_企业分析_测试记录-R0.xlsx"
)

TASK_ID = "QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01"
ENV_URL = "http://111.198.38.90:50892/"
ROUND = "R0"

# 用例 → 记录：拷贝这些列
CASE_COPY = [
    "用例编号", "功能模块", "子功能模块", "功能项", "子功能项", "页面", "功能点",
    "测试内容", "前置条件", "测试步骤", "预期结果", "优先级",
    "用户故事编号", "USM验收场景编号", "原始需求文件", "原始需求章节号",
    "功能点ID", "TRACE引用", "路由route", "交付口径tier", "备注",
]

RECORD_HEADERS = [
    "用例编号", "功能模块", "子功能模块", "功能项", "子功能项", "页面", "功能点",
    "测试内容", "前置条件", "测试步骤", "预期结果", "优先级",
    "是否通过", "测试工程师", "测试时间", "审核员", "测试截图", "实际结果",
    "用户故事编号", "USM验收场景编号", "原始需求文件", "原始需求章节号",
    "功能点ID", "TRACE引用", "路由route", "交付口径tier", "关联任务ID",
    "BUG编号", "traceId", "复测轮次", "阻塞/跳过原因", "备注",
]

BUG_HEADERS = [
    "BUG编号", "关联用例", "严重级别", "标题", "发现日", "状态", "截图", "备注",
]


def load_cases() -> list[dict]:
    wb = openpyxl.load_workbook(CASE, data_only=True, read_only=True)
    ws = wb["功能测试用例"]
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(h).strip() if h else "" for h in rows[1]]
    out = []
    for row in rows[2:]:
        if not row or not row[0]:
            continue
        d = {headers[i]: row[i] if i < len(row) else None for i in range(len(headers))}
        out.append(d)
    wb.close()
    return out


def main():
    cases = load_cases()
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试记录"]
    ws["A1"] = (
        f"智能服务集群-科技专题服务系统测试记录（科技专题战略分析-企业分析）·{ROUND}　"
        f"环境：{ENV_URL}　任务：{TASK_ID}　是否通过仅填：通过/不通过；未测填跳过并写原因"
    )
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    for col, h in enumerate(RECORD_HEADERS, start=1):
        cell = ws.cell(2, col, h)
        cell.font = Font(bold=True)
    align = Alignment(wrap_text=True, vertical="top")
    for i, c in enumerate(cases, start=3):
        row = {k: (c.get(k) or "") for k in CASE_COPY}
        row["是否通过"] = ""
        row["测试工程师"] = ""
        row["测试时间"] = ""
        row["审核员"] = ""
        row["测试截图"] = ""
        row["实际结果"] = ""
        row["关联任务ID"] = TASK_ID
        row["BUG编号"] = ""
        row["traceId"] = ""
        row["复测轮次"] = ROUND
        row["阻塞/跳过原因"] = ""
        for col, key in enumerate(RECORD_HEADERS, start=1):
            cell = ws.cell(i, col, row.get(key, ""))
            cell.alignment = align
    for col in range(1, len(RECORD_HEADERS) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["J"].width = 40
    ws.column_dimensions["K"].width = 40

    if "BUG清单" in wb.sheetnames:
        wsb = wb["BUG清单"]
        wb.remove(wsb)
    wsb = wb.create_sheet("BUG清单", 1)
    wsb["A1"] = f"BUG 清单 · {ROUND} · {TASK_ID} · 编号 BUG-ZNFWJQ-KJZTFWXT-YYYYMMDD-nnn"
    for col, h in enumerate(BUG_HEADERS, start=1):
        wsb.cell(2, col, h).font = Font(bold=True)

    for name in list(wb.sheetnames):
        if name not in ("功能测试记录", "BUG清单", "规则 -0529"):
            # 保留规则 sheet；清空其它样例行以免误用
            wso = wb[name]
            if wso.max_row > 2 and "记录" in name:
                wso.delete_rows(3, wso.max_row - 2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    wb.close()
    print(f"cases={len(cases)} -> {OUT}")


if __name__ == "__main__":
    main()
