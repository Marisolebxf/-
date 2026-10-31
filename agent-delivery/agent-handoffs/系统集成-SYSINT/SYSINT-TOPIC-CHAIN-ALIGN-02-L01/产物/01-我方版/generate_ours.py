# -*- coding: utf-8 -*-
"""
SYSINT-TOPIC-CHAIN-ALIGN-02-L01（WBS-02-11）· 版本一：我方 573 版视角的三要素指标对照表
输入：../_work/prepared.json（由 ../_work/prepare_data.py 生成，只读真源）
输出：本目录 三要素指标对照-我方573版-20261031.xlsx
红线：只出记录。不改 seed、不写 ADS、不灌数；「库内有行」≠「已对齐」；归属一律「待三分清单」。
"""
import json
import os
import re

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(HERE), "_work")
OUT_XLSX = os.path.join(HERE, "三要素指标对照-我方573版-20261031.xlsx")
XLSX_JIUXIN = os.path.join(os.path.dirname(HERE), "02-久新版", "三要素指标对照-久新版-20261031.xlsx")

# 页内点名件 → 候选久新 metric_id（缺口真源：专题-产业链分析-三要素对接需求.md §3）
GAP_CANDIDATE = {
    "M_CHAIN_STAGE_SCORE": "M_TECH_MATURITY_LEVEL",
    "M_CHAIN_STAGE_SCORE_ZT": "M_TECH_MATURITY_LEVEL",
    "M_CHAIN_STAGE_SCORE_ZS": "M_TECH_MATURITY_LEVEL",
    "M_CHAIN_REG_PATENT": "M_TECH_PAPER_PATENT_CNT 等",
    "M_CHAIN_REG_TECH_MATURITY": "M_TECH_MATURITY_LEVEL",
    "M_CHAIN_REG_RESEARCH_ORG": "M_ORG_INDUSTRY_COVER 等",
    "M_CHAIN_REG_TECH_BARRIER": "（无单独久新 metric，专利类原料）",
    "M_CHAIN_REG_TALENT_STRUCTURE": "M_TALENT_STRUCT_QUERY 等",
    "M_CHAIN_STRATEGIC_IMPORTANCE": "（无单独久新 metric，专利/工艺原料）",
    "M_CHAIN_BOTTLENECK_TYPE_DIST": "M_TECH_MATURITY_LEVEL + M_TALENT_SUPPLY_STRUCT 等",
    "M_CHAIN_SZ_PATENT": "M_TECH_PAPER_PATENT_CNT 等",
    "M_CHAIN_SZ_TALENT": "M_TALENT_SUPPLY_STRUCT 等",
    "M_CHAIN_REG_COMP_ACADEMIC": "M_ORG_*（学术生态待产品拆清）",
    "M_CHAIN_ACADEMIC_POWER": "M_ORG_*（学术生态待产品拆清）",
}

HEADERS = [
    "指标ID", "指标名称", "条目类型", "垂向", "产业链页面", "算法类型", "数据支持度（我方 md）",
    "适用系统（20261028 表）", "指标调研文件", "指标计算 py 文件", "我方源表字段",
    "候选久新 metric_id", "久新候选表（130 表实测）", "库内支持（久新调研）", "字段缺口（调研原文要点）",
    "口径是否同", "归属判定", "备注",
]
COL_W = [30, 20, 16, 14, 18, 12, 16, 22, 26, 30, 34, 26, 34, 14, 40, 12, 12, 30]

HDR_FILL = PatternFill("solid", fgColor="1F4E79")
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
LINK_FONT = Font(color="0563C1", underline="single")
THIN = Border(*[Side(style="thin", color="D9D9D9")] * 4)
KIND_FILL = {
    "三要素域件": PatternFill("solid", fgColor="E2EFDA"),
    "页内点名件": PatternFill("solid", fgColor="FFF2CC"),
    "页内点名件（未独立注册）": PatternFill("solid", fgColor="FCE4EC"),
}


def vert_of(mid, fallback=""):
    if mid.startswith("M_TECH_"):
        return "技术/技术链"
    if mid.startswith("M_TALENT_"):
        return "人才"
    if mid.startswith("M_ORG_"):
        return "科研机构"
    return fallback or ("技术/技术链、人才（混合演示位）" if "BOTTLENECK" in mid else "")


def field_gap_from_note(note):
    """从久新调研说明原文提取字段缺口要点，不加工判断。"""
    if not note:
        return ""
    m = re.search(r"候选表里没有字段名片段[^；。]*", note)
    return m.group(0) if m else ""


def base_id(mid):
    return re.sub(r"_(ZT|ZS)$", "", mid)


def name_from_md(md_path, fallback):
    """名称列若上游为 ID 占位，则从 calc-logic md 抬头「# {ID} · {中文名}」补齐。"""
    if not md_path or not re.fullmatch(r"M_[A-Z0-9_]+", str(fallback or "")):
        return fallback or ""
    try:
        with open(md_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    t = line[2:].strip()
                    # 两种抬头：「# ID · 名」（新批） / 「# 名（ID）」（老批）
                    if "·" in t:
                        return t.split("·", 1)[1].strip()
                    m = re.match(r"(.+?)（M_[A-Z0-9_]+）$", t)
                    return m.group(1).strip() if m else t
    except OSError:
        pass
    return fallback


ORCH = os.path.abspath(os.path.join(WORK, "../", "../", "../", "../", "../", "../"))  # _work → 主仓根


def _abs(p):
    return os.path.join(ORCH, p) if p and not p.startswith("/") else (p or "")


def main():
    d = json.load(open(os.path.join(WORK, "prepared.json"), encoding="utf-8"))
    support_by_id = {r["metric_id"]: r for r in d["jiuxin"]}

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "我方573版对照"

    # 表头
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill, cell.font, cell.border = HDR_FILL, HDR_FONT, THIN
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = COL_W[c - 1]
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "C2"

    rows = sorted(d["ours"], key=lambda r: (0 if r["kind"] == "三要素域件" else 1, r["id"]))
    r_i = 1
    n_link = 0
    for rec in rows:
        r_i += 1
        mid = rec["id"]
        row0 = rec["rows"][0] if rec["rows"] else {}
        kind = rec["kind"]
        # 候选久新：三要素域件用本体 ID（族件去后缀）；页内件用缺口清单映射
        if kind == "三要素域件":
            cand = base_id(mid)
            sup = support_by_id.get(cand)
        else:
            cand = GAP_CANDIDATE.get(mid, "")
            first = cand.split(" ")[0]
            sup = support_by_id.get(first) if (cand and not cand.startswith("（")) else None
        # 未独立注册件：名称从 md 抬头补齐（md 已挂），py 如实留空
        if "未独立注册" in kind and not row0.get("name"):
            row0 = dict(row0)
            row0["name"] = name_from_md(_abs(row0.get("md_link", "")), mid)

        vals = [
            mid,
            name_from_md(_abs(row0.get("md_link", "")), row0.get("name", "")) or rec.get("name", ""),
            kind,
            vert_of(mid, rec.get("vertical", "")),
            rec.get("page", ""),
            row0.get("algo_type", ""),
            row0.get("support", ""),
            "、".join(rec["sheets"]),
            _abs(row0.get("md_link", "")) or None,
            _abs(row0.get("py_link", "")) or None,
            row0.get("src_tables", ""),
            cand,
            sup["candidate_tables"] if sup else ("见调研 CSV（多候选）" if "等" in cand else ""),
            sup["db_support"] if sup else "",
            field_gap_from_note(sup["note"]) if sup else ("未独立注册，无对照记录" if "未独立注册" in kind else ""),
            "未对齐（还没有）" if sup else "",
            "待三分清单",
            ("同名指标族拆分件，候选久新件取本体 " + base_id(mid)) if mid != base_id(mid) else "",
        ]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r_i, column=c, value=v)
            cell.border = THIN
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if kind in KIND_FILL and c == 3:
                cell.fill = KIND_FILL[kind]
            if c in (9, 10) and v:  # md / py 超链接
                label = os.path.basename(v)
                cell.value = label
                cell.hyperlink = "file://" + v
                cell.font = LINK_FONT
                n_link += 1
        if not rec["rows"]:  # 未独立注册件：备注指向缺口清单
            ws.cell(row=r_i, column=18, value="该 metric_id 为缺口清单页内点位，未在 573 版独立注册；供数缺口见缺口清单 §3")

    # 说明 sheet
    ws2 = wb.create_sheet("说明")
    notes = [
        ["任务", "SYSINT-TOPIC-CHAIN-ALIGN-02-L01（WBS-02-11）· 调研草稿（依赖 WBS-02-10 未收口，终稿以会签后为准）"],
        ["视角", "我方 20261028 版 573 指标（= 20261027 批三系统拆分后全集：565 基线 + 8 件 _ZT/_ZS 拆分）"],
        ["范围", "三要素域件 95（M_TECH 39 / M_TALENT 34 / M_ORG 22）+ 产业链页面点名件 14（含族内件）"],
        ["数据支持度", "我方 calc-logic md 抬头四档判定（同 20261028 表口径）"],
        ["库内支持/字段缺口", "久新 130 表实测调研原文（指标支持.csv，2026-10-22，schema 5.11.0），未加工"],
        ["口径是否同", "调研原文均为「还没有/未对齐」；本表不把「有行」写成「已对齐」"],
        ["归属判定", "三分清单（公用/久新/智树自算）未到，一律「待三分清单」，不判归属"],
        ["超链接", "指标调研文件 → calc-logic md；指标计算 py 文件 → repro py（file:// 绝对路径，与 20261028 表一致）"],
        ["对版本二", "同 metric_id 见 ../02-久新版/三要素指标对照-久新版-20261031.xlsx（久新视角：93 指标 × 130 表字段级）"],
        ["上游真源", "gkx-orchestration/agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx；工程过程/04-系统集成/02-对接三要素/调研/*"],
        ["生成脚本", os.path.relpath(os.path.abspath(__file__), HERE) + "（数据准备见 ../_work/prepare_data.py）"],
    ]
    for i, (k, v) in enumerate(notes, 1):
        ws2.cell(row=i, column=1, value=k).font = Font(bold=True)
        ws2.cell(row=i, column=2, value=v)
    ws2.column_dimensions["A"].width = 16
    ws2.column_dimensions["B"].width = 110

    wb.save(OUT_XLSX)
    print("已生成:", OUT_XLSX)
    print("行数:", r_i - 1, "；md/py 超链接数:", n_link)

    # 验证全部超链接指向真实文件
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
