# -*- coding: utf-8 -*-
"""
SYSINT-TOPIC-CHAIN-ALIGN-02-L01（WBS-02-11）· 版本二：久新版视角的三要素指标对照表
输入：../_work/prepared.json（由 ../_work/prepare_data.py 生成，只读真源）
输出：本目录 三要素指标对照-久新版-20261031.xlsx
红线：只出记录。不改 seed、不写 ADS、不灌数；「库内有行」≠「已对齐」；归属一律「待三分清单」。
"""
import json
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(HERE), "_work")
OUT_XLSX = os.path.join(HERE, "三要素指标对照-久新版-20261031.xlsx")

HEADERS = [
    "久新 metric_id", "久新指标名", "域", "algorithm_type", "D1", "D4",
    "挂靠久新交付行（51 行包）", "久新模型名", "九新口径证据（CMP 对照原文）",
    "候选表（130 表实测·有行）", "候选表行数（实测）", "候选表字段数（实测）",
    "关键候选字段（节选）", "库内支持", "口径是否等于指标库",
    "我方 573 版对应件", "我方调研文件", "我方计算 py 文件", "我方适用系统",
    "归属判定", "备注",
]
COL_W = [26, 22, 8, 13, 8, 8, 26, 24, 30, 36, 12, 12, 40, 10, 16, 24, 26, 30, 22, 12, 26]

HDR_FILL = PatternFill("solid", fgColor="7B2D26")
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
LINK_FONT = Font(color="0563C1", underline="single")
THIN = Border(*[Side(style="thin", color="D9D9D9")] * 4)
DOMAIN_FILL = {"技术": PatternFill("solid", fgColor="DEEBF7"), "人才": PatternFill("solid", fgColor="FFF2CC"),
               "机构": PatternFill("solid", fgColor="E2EFDA")}


ORCH = os.path.abspath(os.path.join(WORK, "../", "../", "../", "../", "../", "../"))  # _work → 主仓根


def _abs(p):
    return os.path.join(ORCH, p) if p and not p.startswith("/") else (p or "")


def main():
    d = json.load(open(os.path.join(WORK, "prepared.json"), encoding="utf-8"))
    tables_by_name = {t["表"]: t for t in d["tables"]}
    fields_by_table = d["fields_by_table"]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "久新版对照"

    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill, cell.font, cell.border = HDR_FILL, HDR_FONT, THIN
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = COL_W[c - 1]
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "C2"

    order = {"技术": 0, "人才": 1, "机构": 2}
    rows = sorted(d["jiuxin"], key=lambda r: (order.get(r["domain"], 9), r["metric_id"]))
    r_i = 1
    n_link = 0
    for rec in rows:
        r_i += 1
        # 候选表实测信息（取第一张候选表字段节选，最多 6 个）
        cand_tables = [t.strip() for t in rec["candidate_tables"].replace("、", ",").split(",") if t.strip()]
        t0 = cand_tables[0] if cand_tables else ""
        tinfo = tables_by_name.get(t0)
        flds = fields_by_table.get(t0, [])
        key_fields = "；".join(f"{f['field']}" for f in flds[:6]) + ("…" if len(flds) > 6 else "")

        vals = [
            rec["metric_id"], rec["name_cn"], rec["domain"], rec["algorithm_type"], rec["d1"], rec["d4"],
            rec["jiuxin_rows"], rec["jiuxin_model"], rec["jiuxin_evidence"],
            rec["candidate_tables"],
            tinfo["行数"] if tinfo else "",
            tinfo["字段数"] if tinfo else "",
            key_fields,
            rec["db_support"],
            "还没有（调研原文，不标已对齐）",
            rec["metric_id"] if rec["ours_exists"] else "（573 版无同 ID 件）",
            _abs(rec["ours_md"]) or None,
            _abs(rec["ours_py"]) or None,
            "、".join(rec["ours_sheets"]),
            "待三分清单",
            "" if rec["ours_exists"] else "同 ID 件在 573 表外（如族内 _ZT/_ZS 或未注册点位），另见版本一",
        ]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r_i, column=c, value=v)
            cell.border = THIN
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if c == 3 and rec["domain"] in DOMAIN_FILL:
                cell.fill = DOMAIN_FILL[rec["domain"]]
            if c in (17, 18) and v:
                label = os.path.basename(v)
                cell.value = label
                cell.hyperlink = "file://" + v
                cell.font = LINK_FONT
                n_link += 1

    # 说明 sheet
    ws2 = wb.create_sheet("说明")
    notes = [
        ["任务", "SYSINT-TOPIC-CHAIN-ALIGN-02-L01（WBS-02-11）· 调研草稿（依赖 WBS-02-10 未收口，终稿以会签后为准）"],
        ["视角", "久新侧设计为主线：三要素 93 指标（技术 39 / 人才 32 / 机构 22）× 130 张 ADS 表字段级实测证据"],
        ["范围", "久新指标库三要素全集 93 条（调研记录 2026-10-22：这 93 条即三域全部，非抽样）；挂靠 51 行交付包 + 包外 19 条"],
        ["候选表/字段", "130 表字段级只读调研（表清单.csv / 字段清单.csv，schema 5.11.0）：行数、字段数、字段节选均为实测"],
        ["九新口径证据", "SYSINT-CMP-02-L01 对照表 sheet2 原文（2026-10-26），未加工"],
        ["口径是否等于指标库", "调研原文均「还没有」；「结果表在/原料在」≠「已对齐」，不判已接入"],
        ["我方 573 版对应件", "同 metric_id 直挂；超链接 → calc-logic md / repro py（与 20261028 表同源）"],
        ["归属判定", "三分清单未到，一律「待三分清单」，不判归属"],
        ["对版本一", "同 metric_id 见 ../01-我方版/三要素指标对照-我方573版-20261031.xlsx（我方视角：95 域件 + 14 链页点名件）"],
        ["上游真源", "gkx-orchestration/agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/*；agent-handoffs/系统集成-SYSINT/SYSINT-CMP-02-L01/*"],
        ["生成脚本", os.path.basename(os.path.abspath(__file__)) + "（数据准备见 ../_work/prepare_data.py）"],
    ]
    for i, (k, v) in enumerate(notes, 1):
        ws2.cell(row=i, column=1, value=k).font = Font(bold=True)
        ws2.cell(row=i, column=2, value=v)
    ws2.column_dimensions["A"].width = 20
    ws2.column_dimensions["B"].width = 110

    wb.save(OUT_XLSX)
    print("已生成:", OUT_XLSX)
    print("行数:", r_i - 1, "；我方 md/py 超链接数:", n_link)

    # 验证超链接
    wb2 = openpyxl.load_workbook(OUT_XLSX)
    bad = []
    for w in wb2.worksheets:
        for row in w.iter_rows():
            for cell in row:
                if cell.hyperlink and cell.hyperlink.target.startswith("file://"):
                    p = cell.hyperlink.target[7:]
                    if not os.path.exists(p):
                        bad.append(p)
    print("超链接验证:", "全部存在" if not bad else f"缺失 {len(bad)} 个: {bad[:5]}")


if __name__ == "__main__":
    main()
