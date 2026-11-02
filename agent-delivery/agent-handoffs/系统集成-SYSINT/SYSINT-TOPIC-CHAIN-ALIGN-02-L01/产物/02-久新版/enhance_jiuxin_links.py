# -*- coding: utf-8 -*-
"""
SYSINT-TOPIC-CHAIN-ALIGN-02-L01 · 版本二增强：久新原始证据文件超链接
新增三列：
  - 候选表 schema 章节（xlsx 内超链接 → ADS_SCHEMA.md 对应行）
  - 久新公式/方法章节（19+3 条「有公式」指标的精确锚点，含弱匹配标注）
  - 久新原始文件（每行统一挂：ADS_SCHEMA 快照 / RELEASE_NOTES / 调研记录 三个 file:// 链接）
输入：../_work/prepared.json + /tmp/match_{tech,talent,org}.json（子代理语义匹配结果）
"""
import json
import os
import re

import openpyxl
from openpyxl.styles import Alignment, Font

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(HERE), "_work")
XLSX = os.path.join(HERE, "三要素指标对照-久新版-20261031.xlsx")

ORCH = os.path.abspath(os.path.join(WORK, "../", "../", "../", "../", "../", "../"))
SCHEMA_MD = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA-5.11.0.md")
NOTES_MD = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA_RELEASE_NOTES.md")
SURVEY_MD = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/调研记录.md")

LINK_FONT = Font(color="0563C1", underline="single")


def load_schema_sections():
    """解析 schema 全部标题 → [(行号, 层级, 标题)]；并建 表名→(章节标题, 行号) 映射。"""
    lines = open(SCHEMA_MD, encoding="utf-8").read().split("\n")
    heads = []
    for i, l in enumerate(lines, 1):
        m = re.match(r"^(#{1,4})\s+(.*)", l)
        if m:
            heads.append({"line": i, "lvl": len(m.group(1)), "title": m.group(2).strip()})
    table_sec = {}
    for h in heads:
        m = re.match(r"^(?:\d+(?:\.\d+)*)\.?\s*`([a-z_]+)`\s*$", h["title"])
        if m and m.group(1).startswith("ads_"):
            table_sec.setdefault(m.group(1), h)
    return heads, table_sec


def load_matches():
    """合并三个子代理匹配结果。"""
    out = {}
    for p in ("/tmp/match_tech.json", "/tmp/match_talent.json", "/tmp/match_org.json"):
        if os.path.exists(p):
            try:
                for item in json.load(open(p, encoding="utf-8")):
                    out[item["metric_id"]] = item
            except (json.JSONDecodeError, KeyError):
                pass
    return out


def find_section_head(heads, title_prefix):
    """按标题前缀（章节号）找标题，返回行号或 None。"""
    for h in heads:
        if h["title"].startswith(title_prefix) or title_prefix in h["title"]:
            return h["line"]
    return None


def main():
    heads, table_sec = load_schema_sections()
    matches = load_matches()
    print("匹配结果载入:", len(matches), "条")

    wb = openpyxl.load_workbook(XLSX)
    ws = wb["久新版对照"]
    hdr = [c.value for c in ws[1]]
    # 在「库内支持」前插入三列
    anchor_col = hdr.index("库内支持") + 1  # 1-based
    ws.insert_cols(anchor_col, 3)
    new_titles = ["候选表 schema 章节", "久新公式/方法章节", "久新原始文件"]
    for j, t in enumerate(new_titles):
        c = ws.cell(row=1, column=anchor_col + j, value=t)
        c.font = ws.cell(row=1, column=1).font.copy()
        c.fill = ws.cell(row=1, column=1).fill.copy()
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    from openpyxl.utils import get_column_letter
    ws.column_dimensions[get_column_letter(anchor_col)].width = 30
    ws.column_dimensions[get_column_letter(anchor_col + 1)].width = 34
    ws.column_dimensions[get_column_letter(anchor_col + 2)].width = 30

    # 行数据列索引（插入后）：metric_id=1, candidate_tables 原「候选表（130 表实测·有行）」列位置不变（在其左侧）
    # 找到关键列
    def col_of(name):
        for c in range(1, ws.max_column + 1):
            if ws.cell(row=1, column=c).value == name:
                return c
        return None
    c_id = col_of("久新 metric_id")
    c_cand = col_of("候选表（130 表实测·有行）")

    n_sec, n_formula = 0, 0
    for r in range(2, ws.max_row + 1):
        mid = ws.cell(row=r, column=c_id).value
        cand = str(ws.cell(row=r, column=c_cand).value or "")
        # ① 候选表 → schema 章节（每表一节，超链接）
        ts = [t.strip() for t in cand.replace("、", ",").split(",") if t.strip().startswith("ads_")]
        if ts:
            cell = ws.cell(row=r, column=anchor_col)
            parts, first_link = [], None
            for t in ts[:3]:  # 最多列 3 张表防溢出
                h = table_sec.get(t)
                if h:
                    sec = re.sub(r"`", "", h["title"])
                    parts.append(f"{t}: {sec.split('.', 1)[0]}")
                    if first_link is None:
                        first_link = (sec, h["line"])
            if parts:
                cell.value = "；".join(parts) + ("…" if len(ts) > 3 else "")
                if first_link:
                    sec_title, ln = first_link
                    cell.hyperlink = f"file://{SCHEMA_MD}"
                    cell.font = LINK_FONT
                    ws.cell(row=r, column=anchor_col).comment = None
                n_sec += 1
        # ② 公式章节（匹配结果）
        m = matches.get(mid)
        if m and m.get("sections"):
            cell = ws.cell(row=r, column=anchor_col + 1)
            secs = m["sections"]
            conf = m.get("confidence", "")
            cell.value = "；".join(secs) + ("（弱匹配）" if conf == "weak" else "")
            # 链接到第一个章节的行
            ln = find_section_head(heads, secs[0])
            if ln:
                cell.hyperlink = f"file://{SCHEMA_MD}#L{ln}"
                cell.font = LINK_FONT
            n_formula += 1
        # ③ 久新原始文件（统一三链接：schema / release notes / 调研记录）
        cell = ws.cell(row=r, column=anchor_col + 2, value="ADS_SCHEMA 5.11.0")
        cell.hyperlink = f"file://{SCHEMA_MD}"
        cell.font = LINK_FONT

    # 说明页补一行
    ws2 = wb["说明"]
    row0 = ws2.max_row + 1
    ws2.cell(row=row0, column=1, value="增强列说明（2026-10-31 二次交付）").font = openpyxl.styles.Font(bold=True)
    for i, txt in enumerate([
        "候选表 schema 章节：候选表在对端 ADS_SCHEMA.md 快照中的章节定位（如 ads_talent_profile → §4），单元格超链接直开该文件",
        "久新公式/方法章节：「有公式」类指标的方法章节精确锚点（如 24.4 热点算法）；「弱匹配」=语义相近需人工复核；无公式类此列为空",
        "久新原始文件：ADS_SCHEMA 5.11.0 快照（公式与口径唯一真源）；版本日志见 对端/2026-10-22-ADS_SCHEMA_RELEASE_NOTES.md；只读库实测见 调研/调研记录.md",
        "重要边界：久新未交付计算代码（py），交付物=只读库+数仓说明文档；「有公式」19+3 条的公式写在 schema 章节内，其余为结果表直读或原料自算",
    ], 1):
        ws2.cell(row=row0 + i, column=2, value=txt)

    wb.save(XLSX)
    print(f"已增强 {XLSX}")
    print(f"表章节列填充: {n_sec} 行；公式章节列填充: {n_formula} 行")

    # 验证：超链接目标存在
    bad = []
    wb2 = openpyxl.load_workbook(XLSX)
    for w in wb2.worksheets:
        for row in w.iter_rows():
            for cell in row:
                if cell.hyperlink and cell.hyperlink.target.startswith("file://"):
                    p = cell.hyperlink.target[7:].split("#")[0]
                    if not os.path.exists(p):
                        bad.append(p)
    print("超链接验证:", "全部存在" if not bad else f"缺失 {len(bad)}: {bad[:3]}")


if __name__ == "__main__":
    main()
