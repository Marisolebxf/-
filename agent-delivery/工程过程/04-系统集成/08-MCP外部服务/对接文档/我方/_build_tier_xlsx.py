# -*- coding: utf-8 -*-
"""Build Skill/MCP tier annotation workbook from 德金 MCP 清单."""
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "德金提供的参考材料" / "AI战略咨MCP清单.xlsx"
OUT = Path(__file__).resolve().parent / "Skill-MCP一二三阶标注总表-v0.1.xlsx"

ANN = {
    "HV-01": dict(tier="二阶", form="MCP工具", boundary="N", note="汇总态势指标与异常信号，非单对象查询", gkx7="", role="态势入口"),
    "HV-02": dict(tier="二阶", form="MCP工具", boundary="N", note="区域对标与差距结论", gkx7="synth-index（仅区域合成，≠本项）", role="区域对标"),
    "HV-03": dict(tier="二阶", form="MCP工具", boundary="N", note="多政策结构化比较", gkx7="policy-indicators / 部分 search-policy", role="政策差异"),
    "HV-04": dict(tier="二阶", form="MCP工具", boundary="N", note="政策落地研判", gkx7="", role=""),
    "HV-05": dict(tier="二阶", form="MCP工具", boundary="N", note="人才态势+推荐", gkx7="", role=""),
    "HV-06": dict(tier="二阶", form="MCP工具", boundary="N", note="颠覆性技术识别（技术垂向）", gkx7="", role=""),
    "HV-07": dict(tier="二阶", form="MCP工具", boundary="N", note="技术垂向趋势研判", gkx7="", role="趋势研判"),
    "HV-08": dict(tier="二阶", form="MCP工具", boundary="N", note="竞争专题；「报告」不自动升三阶", gkx7="", role="竞争格局"),
    "HV-11": dict(tier="报告装配", form="MCP(被Skill调用)", boundary="Y", note="装配多源结果；待拍板是否并入三阶Skill", gkx7="", role="报告装配"),
    "HV-12": dict(tier="报告装配", form="MCP(被Skill调用)", boundary="Y", note="引用绑定，方法型；同上", gkx7="", role="引用溯源"),
    "HV-13": dict(tier="二阶", form="MCP工具", boundary="N", note="产业垂向结构建模", gkx7="chain-panorama", role="产业链全景"),
    "HV-14": dict(tier="二阶", form="MCP工具", boundary="N", note="产业垂向专题诊断", gkx7="chain-analyze", role="瓶颈识别"),
    "HV-15": dict(tier="二阶", form="MCP工具", boundary="N", note="企业招引推荐", gkx7="ent-recommend", role=""),
    "HV-16": dict(tier="二阶", form="MCP工具", boundary="N", note="企业痛点诊断", gkx7="ent-diagnose", role=""),
    "HV-17": dict(tier="二阶", form="MCP工具", boundary="N", note="企业能力榜单", gkx7="ent-evaluate（同类）", role=""),
    "HV-18": dict(tier="一阶", form="MCP工具", boundary="N", note="企业对象画像/全景取数", gkx7="search-enterprise（入口）", role=""),
    "HV-19": dict(tier="二阶", form="MCP工具", boundary="N", note="合作资源推荐", gkx7="", role=""),
    "HV-20": dict(tier="二阶", form="MCP工具", boundary="N", note="供需匹配", gkx7="svc-analysis / policy-apply", role=""),
    "HV-21": dict(tier="一阶", form="MCP工具", boundary="Y", note="偏监测取数；若定义为研判机会风险则升二阶", gkx7="", role="全球监测"),
    "HV-22": dict(tier="一阶", form="MCP工具", boundary="Y", note="同上", gkx7="", role="湾区监测"),
    "HV-23": dict(tier="一阶", form="MCP工具", boundary="Y", note="同上；下钻仍以查询为主", gkx7="", role="深圳监测"),
    "HV-24": dict(tier="一阶", form="MCP工具", boundary="Y", note="流动监控列表；含预警研判则升二阶", gkx7="", role=""),
    "HV-25": dict(tier="一阶", form="MCP工具", boundary="N", note="分布图查询/展示", gkx7="", role=""),
    "HV-26": dict(tier="二阶", form="MCP工具", boundary="N", note="人才结构与流动研判", gkx7="", role=""),
    "HV-27": dict(tier="一阶", form="MCP工具", boundary="N", note="单个人才画像取数", gkx7="", role=""),
    "HV-28": dict(tier="二阶", form="MCP工具", boundary="N", note="引进评估", gkx7="", role=""),
    "HV-29": dict(tier="二阶", form="MCP工具", boundary="N", note="尽调报告生成（人才垂向）", gkx7="", role=""),
    "HV-30": dict(tier="二阶", form="MCP工具", boundary="N", note="政策匹配推送", gkx7="policy-apply", role=""),
    "HV-31": dict(tier="二阶", form="MCP工具", boundary="N", note="技术链结构，单一垂向", gkx7="", role="技术链全景"),
    "HV-32": dict(tier="一阶", form="MCP工具", boundary="N", note="成长轨迹可视化取数", gkx7="", role=""),
    "HV-33": dict(tier="二阶", form="MCP工具", boundary="N", note="机构排序", gkx7="", role=""),
    "HV-34": dict(tier="二阶", form="MCP工具", boundary="N", note="区域分布分析", gkx7="", role=""),
    "HV-35": dict(tier="二阶", form="MCP工具", boundary="N", note="机构分布分析", gkx7="", role=""),
    "HV-36": dict(tier="二阶", form="MCP工具", boundary="N", note="供给趋势分析", gkx7="", role=""),
    "HV-37": dict(tier="二阶", form="MCP工具", boundary="N", note="关系链分析", gkx7="", role=""),
    "HV-38": dict(tier="二阶", form="MCP工具", boundary="N", note="深圳人才对标", gkx7="", role=""),
    "HV-39": dict(tier="二阶", form="MCP工具", boundary="N", note="学术力评估", gkx7="", role=""),
    "HV-40": dict(tier="二阶", form="MCP工具", boundary="N", note="产业力评估", gkx7="", role=""),
    "HV-41": dict(tier="二阶", form="MCP工具", boundary="N", note="引才推荐", gkx7="", role=""),
    "HV-42": dict(tier="二阶", form="MCP工具", boundary="N", note="培育推荐", gkx7="", role=""),
    "HV-43": dict(tier="二阶", form="MCP工具", boundary="N", note="高校供给预测", gkx7="", role=""),
    "HV-44": dict(tier="二阶", form="MCP工具", boundary="N", note="供需缺口分析", gkx7="", role=""),
    "HV-45": dict(tier="二阶", form="MCP工具", boundary="N", note="区域政策对比", gkx7="", role=""),
    "HV-46": dict(tier="二阶", form="MCP工具", boundary="N", note="服务链短板", gkx7="svc-analysis", role=""),
    "HV-47": dict(tier="二阶", form="MCP工具", boundary="N", note="区域协同分析", gkx7="synth-collab（≠三阶）", role=""),
    "HV-48": dict(tier="一阶", form="MCP工具", boundary="N", note="人才画像底座", gkx7="", role=""),
    "HV-49": dict(tier="二阶", form="MCP工具", boundary="N", note="TOP100筛选排序", gkx7="", role=""),
    "HV-50": dict(tier="支撑能力", form="MCP工具", boundary="N", note="人才池管理，非分析阶", gkx7="", role=""),
    "HV-51": dict(tier="二阶", form="MCP工具", boundary="N", note="分布与趋势分析", gkx7="", role=""),
    "HV-52": dict(tier="二阶", form="MCP工具", boundary="N", note="人才指数计算", gkx7="", role=""),
    "HV-53": dict(tier="一阶", form="MCP工具", boundary="N", note="人才检索入口", gkx7="", role=""),
    "HV-54": dict(tier="一阶", form="MCP工具", boundary="Y", note="驾驶舱聚合展示；若含研判结论可升二阶", gkx7="", role=""),
    "HV-55": dict(tier="一阶", form="MCP工具", boundary="N", note="动态资讯跟踪", gkx7="", role=""),
    "HV-56": dict(tier="二阶", form="MCP工具", boundary="N", note="基础研究问题清单", gkx7="", role=""),
    "HV-57": dict(tier="二阶", form="MCP工具", boundary="N", note="问题趋势分析", gkx7="", role=""),
    "HV-58": dict(tier="二阶", form="MCP工具", boundary="N", note="深圳基础研究部署", gkx7="", role=""),
    "HV-59": dict(tier="二阶", form="MCP工具", boundary="N", note="组织实施分析", gkx7="", role=""),
    "HV-60": dict(tier="底座", form="底座", boundary="N", note="图谱构建底座，非业务分析阶", gkx7="", role=""),
}

FIRST_BATCH = {
    "HV-01", "HV-02", "HV-03", "HV-07", "HV-08", "HV-11", "HV-12",
    "HV-13", "HV-14", "HV-21", "HV-22", "HV-23", "HV-31",
}

ORDER = {
    "HV-21": 1, "HV-22": 2, "HV-23": 3, "HV-01": 4, "HV-02": 5, "HV-03": 6,
    "HV-31": 7, "HV-13": 8, "HV-14": 9, "HV-07": 10, "HV-08": 11,
    "HV-11": 12, "HV-12": 13, "SKILL-SSB-01": 14,
}

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
CELL_FONT = Font(name="Calibri", size=10)
THIN = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")
FILLS = {
    "一阶": PatternFill("solid", fgColor="C6EFCE"),
    "二阶": PatternFill("solid", fgColor="BDD7EE"),
    "三阶": PatternFill("solid", fgColor="FCE4D6"),
    "报告装配": PatternFill("solid", fgColor="E2D5F1"),
    "支撑能力": PatternFill("solid", fgColor="FFF2CC"),
    "底座": PatternFill("solid", fgColor="D9D9D9"),
}
YES_FILL = PatternFill("solid", fgColor="FFEB9C")
BATCH_FILL = PatternFill("solid", fgColor="F8CBAD")


def style_header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(1, c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = THIN


def style_cell(cell, center=False):
    cell.font = CELL_FONT
    cell.alignment = CENTER if center else WRAP
    cell.border = THIN


def main():
    wb_src = load_workbook(SRC)
    ws_src = wb_src["系统高价值功能清单"]
    src_headers = [ws_src.cell(1, c).value for c in range(1, ws_src.max_column + 1)]
    extra_headers = [
        "预标阶", "形态", "是否第一批(固态电池)", "第一批角色", "边界项(待拍板)",
        "标注说明", "对应gkx-7chain工具", "确认阶(11-20填写)", "确认状态", "三阶Skill归属",
    ]
    all_headers = src_headers + extra_headers
    n = len(all_headers)

    wb = Workbook()
    ws = wb.active
    ws.title = "全量阶标注"
    for c, h in enumerate(all_headers, 1):
        ws.cell(1, c, h)
    style_header(ws, n)

    row_idx = 2
    for r in range(2, ws_src.max_row + 1):
        row = [ws_src.cell(r, c).value for c in range(1, ws_src.max_column + 1)]
        hid = row[0]
        if not hid:
            continue
        ann = ANN.get(
            hid,
            dict(tier="二阶", form="MCP工具", boundary="N", note="默认二阶，待复核", gkx7="", role=""),
        )
        is_fb = "是" if hid in FIRST_BATCH else "否"
        skill = "solid-state-battery-strategy" if hid in FIRST_BATCH else ""
        extra = [
            ann["tier"], ann["form"], is_fb, ann.get("role", ""),
            "是" if ann["boundary"] == "Y" else "否",
            ann["note"], ann.get("gkx7", ""), "", "draft", skill,
        ]
        full = row + extra
        for c, v in enumerate(full, 1):
            cell = ws.cell(row_idx, c, v)
            style_cell(cell, center=c not in (3, 4, 5, 6, 7, 10, 20, 21))
        tier_col = len(src_headers) + 1
        t = full[tier_col - 1]
        if t in FILLS:
            ws.cell(row_idx, tier_col).fill = FILLS[t]
        if is_fb == "是":
            ws.cell(row_idx, len(src_headers) + 3).fill = BATCH_FILL
        if extra[4] == "是":
            ws.cell(row_idx, len(src_headers) + 5).fill = YES_FILL
        ws.row_dimensions[row_idx].height = 45
        row_idx += 1

    # 三阶 Skill row
    skill_row = row_idx
    for c in range(1, n + 1):
        style_cell(ws.cell(skill_row, c, ""))
    skill_vals = {
        1: "SKILL-SSB-01",
        2: "跨系统（展示+专题+智库）",
        3: "固态电池发展战略综合分析",
        4: "针对固态电池：科研情况+产业化情况+政策支持情况的综合战略分析与报告",
        5: "产业/技术主题；区域；时间；决策问题",
        6: "综合报告；关键结论；证据清单；数据范围声明",
        7: "第一批唯一三阶，满足「可以少但不能没有」",
        8: "P0",
        9: "solid-state-battery-strategy（Skill名，非MCP工具）",
        10: "GKX-12-02/03；WBS阶的定义；固态电池报告",
        11: "预标",
        12: "综合战略",
        13: "D2–D3（随上游）",
        14: "第一批｜11/10—12/10（预排）",
    }
    for c, v in skill_vals.items():
        ws.cell(skill_row, c, v)
        style_cell(ws.cell(skill_row, c))
    ws.cell(skill_row, len(src_headers) + 1, "三阶").fill = FILLS["三阶"]
    ws.cell(skill_row, len(src_headers) + 2, "Skill")
    ws.cell(skill_row, len(src_headers) + 3, "是").fill = BATCH_FILL
    ws.cell(skill_row, len(src_headers) + 4, "端到端综合分析")
    ws.cell(skill_row, len(src_headers) + 5, "否")
    ws.cell(
        skill_row,
        len(src_headers) + 6,
        "编排 HV-01/02/03/21/22/23 + HV-13/14/31 + HV-07/08 + HV-11/12；不可做成黑盒大工具",
    )
    ws.cell(skill_row, len(src_headers) + 9, "draft")
    ws.cell(skill_row, len(src_headers) + 10, "solid-state-battery-strategy")
    for c in range(1, n + 1):
        style_cell(ws.cell(skill_row, c))
    ws.row_dimensions[skill_row].height = 50

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(n)}{skill_row}"
    ws.row_dimensions[1].height = 32
    widths = {
        1: 12, 2: 18, 3: 22, 4: 36, 5: 28, 6: 28, 7: 24, 8: 10, 9: 36, 10: 28,
        11: 16, 12: 12, 13: 16, 14: 22, 15: 12, 16: 16, 17: 14, 18: 14, 19: 12,
        20: 36, 21: 28, 22: 14, 23: 12, 24: 28,
    }
    for c, w in widths.items():
        ws.column_dimensions[get_column_letter(c)].width = w

    # ===== 第一批 =====
    ws2 = wb.create_sheet("第一批固态电池")
    fb_headers = [
        "功能ID", "系统", "功能名称", "建议MCP/Skill名", "预标阶", "形态",
        "第一批角色", "数据依赖", "边界项", "标注说明", "对应gkx-7chain",
        "编排顺序", "确认阶", "确认状态",
    ]
    for c, h in enumerate(fb_headers, 1):
        ws2.cell(1, c, h)
    style_header(ws2, len(fb_headers))

    fb_src_rows = []
    for r in range(2, skill_row + 1):
        hid = ws.cell(r, 1).value
        if hid in FIRST_BATCH or hid == "SKILL-SSB-01":
            fb_src_rows.append(r)
    fb_src_rows.sort(key=lambda r: ORDER.get(ws.cell(r, 1).value, 99))

    for i, r in enumerate(fb_src_rows, 2):
        hid = ws.cell(r, 1).value
        vals = [
            hid, ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 9).value,
            ws.cell(r, 15).value, ws.cell(r, 16).value, ws.cell(r, 18).value,
            ws.cell(r, 13).value, ws.cell(r, 19).value, ws.cell(r, 20).value,
            ws.cell(r, 21).value, ORDER.get(hid, ""), "", "draft",
        ]
        for c, v in enumerate(vals, 1):
            cell = ws2.cell(i, c, v)
            style_cell(cell)
        if vals[4] in FILLS:
            ws2.cell(i, 5).fill = FILLS[vals[4]]
        if vals[8] == "是":
            ws2.cell(i, 9).fill = YES_FILL
        ws2.row_dimensions[i].height = 40

    ws2.freeze_panes = "C2"
    ws2.auto_filter.ref = f"A1:N{len(fb_src_rows) + 1}"
    for c, w in enumerate([10, 18, 22, 36, 10, 16, 14, 14, 10, 36, 24, 10, 12, 10], 1):
        ws2.column_dimensions[get_column_letter(c)].width = w

    # ===== gkx-7chain =====
    ws3 = wb.create_sheet("gkx-7chain对照")
    h3 = ["现网工具名", "预标阶", "垂向域", "说明", "对应HV(若有)", "是否等于三阶", "确认阶", "确认状态"]
    for c, h in enumerate(h3, 1):
        ws3.cell(1, c, h)
    style_header(ws3, len(h3))
    gkx = [
        ("search-enterprise", "一阶", "企业", "企业查询", "HV-18 入口同类", "否"),
        ("search-industry", "一阶", "产业", "产业/技术点查询", "—", "否"),
        ("search-policy", "一阶", "政策", "政策查询", "HV-03 上游", "否"),
        ("ent-evaluate", "二阶", "企业", "企业能力评估", "HV-17 同类", "否"),
        ("ent-recommend", "二阶", "企业", "企业招引推荐", "HV-15", "否"),
        ("ent-diagnose", "二阶", "企业", "企业痛点诊断", "HV-16", "否"),
        ("chain-panorama", "二阶", "产业链", "产业链全景", "HV-13", "否"),
        ("chain-analyze", "二阶", "产业链", "瓶颈/周期等分析", "HV-14", "否"),
        ("policy-indicators", "二阶", "政策", "政策指标时序/区域", "HV-03 辅助", "否"),
        ("policy-apply", "二阶", "政策", "政策匹配适用", "HV-30", "否"),
        ("svc-analysis", "二阶", "服务链", "服务链分析", "HV-46 同类", "否"),
        ("synth-index", "二阶", "区域合成", "区域创新活力指数；≠综合战略", "HV-02 部分相关", "否（明确≠三阶）"),
        ("synth-collab", "二阶", "区域合成", "区域协同指数；≠综合战略", "HV-47 部分相关", "否（明确≠三阶）"),
    ]
    for i, row in enumerate(gkx, 2):
        for c, v in enumerate(list(row) + ["", "draft"], 1):
            cell = ws3.cell(i, c, v)
            style_cell(cell)
        if row[1] in FILLS:
            ws3.cell(i, 2).fill = FILLS[row[1]]
    ws3.freeze_panes = "B2"
    for c, w in enumerate([18, 10, 12, 28, 22, 18, 12, 10], 1):
        ws3.column_dimensions[get_column_letter(c)].width = w

    # ===== 规则 =====
    ws4 = wb.create_sheet("阶定义与规则")
    ws4["A1"] = "Skill/MCP 一二三阶标注规则（对齐 WBS 阶的定义 · 2026-11-09 淮政玮裁定）"
    ws4["A1"].font = Font(name="Calibri", bold=True, size=14, color="1F4E78")
    ws4.merge_cells("A1:F1")
    rules = [
        ["阶", "定义", "形态", "命名倾向", "例子", "注意"],
        ["一阶", "垂向域的查询", "多为单个 MCP 工具", "search_ / get_ / monitor_", "企业查询、政策查询、技术点查询", "一、二阶是通用能力"],
        ["二阶", "垂向域的专题战略分析", "MCP，或小 Skill + 少量工具", "analyze_ / compare_ / identify_ / recommend_ / evaluate_", "企业能力评估、企业招引、政策对比、瓶颈识别", "「报告」二字不自动升三阶"],
        ["三阶", "综合分析（跨垂向：科研+产业化+政策等）", "必须是 Skill，编排多个一/二阶工具", "Skill 目录名，不另起 MCP 前缀", "固态电池发展战略综合分析", "可以少但不能没有；特定领域"],
        ["报告装配", "多源结果装配 / 引用溯源", "MCP(被 Skill 调用)", "generate_*_report", "HV-11、HV-12", "本身不是分析阶"],
        ["支撑能力", "管理/运营类，非分析", "MCP 工具", "manage_*", "HV-50 人才池管理", "不计入一/二/三阶统计"],
        ["底座", "数据/图谱底座", "底座专项", "—", "HV-60 图谱构建", "不计入业务阶"],
    ]
    for i, row in enumerate(rules, 3):
        for c, v in enumerate(row, 1):
            cell = ws4.cell(i, c, v)
            cell.border = THIN
            cell.alignment = WRAP
            if i == 3:
                cell.fill = HEADER_FILL
                cell.font = HEADER_FONT
            else:
                cell.font = CELL_FONT
                if c == 1 and v in FILLS:
                    cell.fill = FILLS[v]
        ws4.row_dimensions[i].height = 36
    ws4["A11"] = "待拍板（建议 11-20 会上一次过）"
    ws4["A11"].font = Font(name="Calibri", bold=True, size=12)
    for i, t in enumerate(
        [
            "1. HV-21/22/23（及同类 monitor）：一阶还是二阶？",
            "2. HV-11/12：维持「报告装配」，还是并进三阶 Skill、不再单独对外？",
            "3. 首批是否只保留固态电池这一个三阶 Skill？",
            "4. gkx-7chain 的 synth-* 对外是否写明「二阶·区域合成，非综合战略」？",
            "5. HV-54 人才驾驶舱：一阶还是二阶？",
        ],
        12,
    ):
        ws4.cell(i, 1, t).font = CELL_FONT
    ws4["A18"] = "本表真源关系"
    ws4["A18"].font = Font(name="Calibri", bold=True, size=12)
    ws4["A19"] = "德金原表：德金提供的参考材料/AI战略咨MCP清单.xlsx（系统高价值功能清单）"
    ws4["A20"] = "阶定义：08-MCP外部服务/WBS.md §阶的定义"
    ws4["A21"] = "预标注说明 md：对接文档/我方/Skill-MCP一二三阶标注-草稿v0.1.md"
    ws4["A22"] = "第一批范围：GKX-12-02_Skill四批建设计划.md §3"
    ws4["A23"] = "版本：v0.1 · 2026-11-13 · 状态 draft · 11-20 确认后升 confirmed"
    for c, w in enumerate([12, 28, 28, 40, 36, 36], 1):
        ws4.column_dimensions[get_column_letter(c)].width = w

    # ===== 汇总（公式） =====
    ws5 = wb.create_sheet("按阶汇总")
    ws5["A1"] = "按预标阶汇总（公式随「全量阶标注」变动）"
    ws5["A1"].font = Font(name="Calibri", bold=True, size=12, color="1F4E78")
    ws5.merge_cells("A1:D1")
    for c, h in enumerate(["预标阶", "数量", "说明", "第一批数量"], 1):
        cell = ws5.cell(3, c, h)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = THIN
    tiers_sum = [
        ("一阶", "垂向域查询"),
        ("二阶", "垂向域专题战略分析"),
        ("三阶", "综合分析 Skill"),
        ("报告装配", "报告/引用装配"),
        ("支撑能力", "管理运营类"),
        ("底座", "图谱等底座"),
    ]
    last = skill_row
    for i, (t, desc) in enumerate(tiers_sum, 4):
        ws5.cell(i, 1, t).fill = FILLS[t]
        ws5.cell(i, 1).border = THIN
        ws5.cell(i, 1).font = CELL_FONT
        # O = col 15 预标阶; Q = col 17 是否第一批
        formula_cnt = f"=COUNTIF('全量阶标注'!O$2:O${last},A{i})"
        formula_fb = f"=COUNTIFS('全量阶标注'!O$2:O${last},A{i},'全量阶标注'!Q$2:Q${last},\"是\")"
        ws5.cell(i, 2, formula_cnt).border = THIN
        ws5.cell(i, 3, desc).border = THIN
        ws5.cell(i, 3).font = CELL_FONT
        ws5.cell(i, 4, formula_fb).border = THIN
    ws5.cell(10, 1, "合计").font = Font(name="Calibri", bold=True)
    ws5.cell(10, 2, "=SUM(B4:B9)")
    ws5.cell(10, 4, "=SUM(D4:D9)")
    for c in range(1, 5):
        ws5.cell(10, c).border = THIN
        ws5.cell(10, c).font = Font(name="Calibri", bold=True)
    ws5["A12"] = "边界项数量"
    ws5["B12"] = f"=COUNTIF('全量阶标注'!S$2:S${last},\"是\")"
    ws5["A13"] = "第一批能力行数（含三阶Skill）"
    ws5["B13"] = f"=COUNTIF('全量阶标注'!Q$2:Q${last},\"是\")"
    ws5["A15"] = "11-20 DoD"
    ws5["A16"] = "规则冻结 + 第一批全部确认阶 + 至少一个三阶 Skill + gkx-7chain 13 工具确认阶"
    for c, w in enumerate([14, 12, 28, 14], 1):
        ws5.column_dimensions[get_column_letter(c)].width = w

    chart = BarChart()
    chart.type = "col"
    chart.title = "预标阶分布"
    chart.y_axis.title = "数量"
    data = Reference(ws5, min_col=2, min_row=3, max_row=9)
    cats = Reference(ws5, min_col=1, min_row=4, max_row=9)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    chart.width = 15
    chart.height = 8
    ws5.add_chart(chart, "F3")

    # ===== 附录：复制德金其他 sheet =====
    for name in ["功能去重清单", "场景-功能映射", "核对说明"]:
        src_ws = wb_src[name]
        dst = wb.create_sheet(f"附录-{name}")
        for row in src_ws.iter_rows():
            for cell in row:
                nc = dst.cell(cell.row, cell.column, cell.value)
                nc.font = CELL_FONT
                nc.border = THIN
                nc.alignment = WRAP
                if cell.row == 1:
                    nc.fill = HEADER_FILL
                    nc.font = HEADER_FONT
                    nc.alignment = CENTER
        for c in range(1, src_ws.max_column + 1):
            dst.column_dimensions[get_column_letter(c)].width = 22
        dst.freeze_panes = "A2"
        dst.auto_filter.ref = f"A1:{get_column_letter(src_ws.max_column)}{src_ws.max_row}"

    for sheet in wb.worksheets:
        sheet.page_setup.orientation = "landscape"
        sheet.page_setup.fitToPage = True
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0
        sheet.print_title_rows = "1:1"

    wb.save(OUT)
    print("OK", OUT)
    print("HV rows", skill_row - 2, "+ skill row", skill_row)


if __name__ == "__main__":
    main()
