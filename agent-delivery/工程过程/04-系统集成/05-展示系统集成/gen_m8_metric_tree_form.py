"""生成 M8 科技指标树 · 算法工程师填写表"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = r"e:\work\上达通\项目\深圳GKX\gkx-lumen\gkx-orchestration\agent-delivery\工程过程\04-系统集成\05-展示系统集成\M8科技指标树-算法填写表.xlsx"

# ---- 样式 ----
HEADER_FILL = PatternFill("solid", fgColor="1E5BB8")
HEADER_FONT = Font(name="微软雅黑", bold=True, color="FFFFFF", size=11)
ZEBRA_1 = PatternFill("solid", fgColor="FFFFFF")
ZEBRA_2 = PatternFill("solid", fgColor="F7F9FC")
LV1_FILL = PatternFill("solid", fgColor="E8F0FE")
THIN = Side(style="thin", color="D9DEE7")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="left")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

HEADERS = [
    "层级\n(level)", "一级指标", "二级指标", "三级指标\n(叶节点)", "节点ID\n(node_id)",
    "父节点ID\n(parent_id)", "权重\n(weight)", "指标版本\n(version)", "赋权依据\n(weight_basis)",
    "指标描述\n(description)", "计算公式/方法\n(calculation)", "指标意义\n(significance)",
    "metric_id\n(叶节点必填)", "计量单位\n(unit)", "数据类型\n(data_type)", "所属领域\n(domain)",
    "数据源表\n(source_tables)", "源系统\n(source_systems)", "更新频率\n(update_freq)",
    "就绪状态\n(mapping_status)", "待确认项\n(pending_ref)", "BID引用\n(bid_ref)",
    "验收单元ID\n(acceptance_unit_id)", "备注",
]

# 示例数据（来源 demo mockData.js，算法工程师可覆盖/补充）
# 列顺序: level, 一级, 二级, 三级, node_id, parent_id, weight, version, weight_basis,
#         description, calculation, significance, metric_id, unit, data_type, domain,
#         source_tables, source_systems, update_freq, mapping_status, pending_ref, bid_ref, acceptance_unit_id, 备注
ROWS = [
    # level1
    [1, "科技创新能力", "", "", "1", "", 0.40, "v2024-01",
     "综合评价的核心维度。专家组判定创新能力对科技指数贡献最高，一级赋权40%。",
     "衡量区域/机构科技创新综合能力的核心指标，反映科技创新的基础实力和核心竞争力",
     "加权求和二级指标得分：科研投入×0.5 + 创新产出×0.5",
     "反映科技创新主体在研发投入和创新产出方面的综合实力，是科技评价的核心维度",
     "", "分", "float", "COMP", "", "", "", "✅已就绪", "", "§1.1.1.1.4.1", "TI-01", "示例行"],
    # level2
    [2, "", "科研投入", "", "1-1", "1", 0.50, "v2024-01",
     "投入是产出的前置条件，与创新产出等权，体现「有投入才有产出」的评价共识。",
     "衡量科技创新资源投入强度的指标",
     "R&D经费投入×0.6 + 研发人员占比×0.4",
     "体现对科技创新的资金支持力度和人才投入强度",
     "", "分", "float", "COMP", "", "", "", "✅已就绪", "", "§1.1.1.1.4.1.1", "TI-01-1", "示例行"],
    # level3
    [3, "", "", "R&D经费投入", "1-1-1", "1-1", 0.60, "v2024-01",
     "经费强度是国际可比的核心投入口径，同级中权重最高（60%）。",
     "年度研发投入经费总额占GDP比例",
     "R&D经费/GDP×100%",
     "反映区域/机构对科技创新的资金投入强度",
     "M_TI_RD_INVEST_RATIO", "%", "float", "COMP",
     "dwd.enterprise.rd_investment <- ods: dwd_org_annual_financial_info",
     "统计年鉴/企业年报", "annual", "⚠️待确认", "Q010", "§1.1.1.1.4.1.1.1", "TI-01-1-1", "示例行，可覆盖"],
    [3, "", "", "研发人员占比", "1-1-2", "1-1", 0.40, "v2024-01",
     "人才投入作为经费的配套项，赋权40%，避免只看资金不看队伍。",
     "研发人员占从业人员总数的比例",
     "研发人员数/从业人员总数×100%",
     "反映科技创新的人力资源配置水平",
     "", "%", "float", "COMP", "", "", "", "🔧算法待实现", "", "", "", "示例行，可覆盖"],
    # level2
    [2, "", "创新产出", "", "1-2", "1", 0.50, "v2024-01",
     "用专利、论文、转化三类产出刻画创新结果，与科研投入等权。",
     "衡量科技创新成果产出水平的指标",
     "专利申请量×0.4 + 论文发表量×0.35 + 成果转化数×0.25",
     "体现科技创新的实际产出效果",
     "", "分", "float", "COMP", "", "", "", "✅已就绪", "", "§1.1.1.1.4.1.2", "TI-01-2", "示例行"],
    [3, "", "", "专利申请量", "1-2-1", "1-2", 0.40, "v2024-01",
     "发明专利最能反映技术创新活跃度，同级赋权40%。",
     "年度专利申请数量（发明专利为主）",
     "发明专利申请量×1.5 + 实用新型×0.5 + 外观设计×0.2",
     "反映技术创新的活跃程度",
     "", "件", "int", "TECH", "", "", "", "🔧算法待实现", "", "", "", "示例行，可覆盖"],
    # level1
    [1, "科技影响力", "", "", "2", "", 0.30, "v2024-01",
     "衡量成果辐射能力，是创新能力的外溢结果，一级赋权30%。",
     "衡量科技创新成果产生的影响力和辐射能力的指标",
     "学术影响力×0.6 + 产业影响力×0.4",
     "反映科技创新成果在学术界和产业界的影响力",
     "", "分", "float", "COMP", "", "", "", "✅已就绪", "", "§1.1.1.1.4.2", "TI-02", "示例行"],
    [2, "", "学术影响力", "", "2-1", "2", 0.60, "v2024-01",
     "学术影响是科技评价的传统主轴，二级赋权60%。",
     "衡量学术成果影响力的指标",
     "论文被引次数×0.5 + H指数×0.3 + 国际合作论文×0.2",
     "反映学术研究的国际影响力和学术地位",
     "", "分", "float", "COMP", "", "", "", "✅已就绪", "", "§1.1.1.1.4.2.1", "TI-02-1", "示例行"],
    [3, "", "", "论文被引次数", "2-1-1", "2-1", 0.50, "v2024-01",
     "被引次数直接度量成果被同行使用的程度，同级赋权50%。",
     "发表论文被引用的总次数",
     "年度论文被引总次数",
     "反映学术成果的影响力和认可度",
     "", "次", "int", "TECH", "", "", "", "🔧算法待实现", "", "", "", "示例行，可覆盖"],
    [3, "", "", "H指数", "2-1-2", "2-1", 0.30, "v2024-01",
     "H指数兼顾数量与质量，赋权30%。",
     "高被引论文数量指标",
     "有h篇论文被引至少h次的最大值",
     "综合反映学术产出数量和质量",
     "", "", "int", "TECH", "", "", "", "🔧算法待实现", "", "", "", "示例行，可覆盖"],
]

wb = Workbook()
ws = wb.active
ws.title = "指标树填写表"

# 表头
for col, h in enumerate(HEADERS, 1):
    c = ws.cell(row=1, column=col, value=h)
    c.fill = HEADER_FILL
    c.font = HEADER_FONT
    c.alignment = CENTER
    c.border = BORDER

# 数据行
for r_idx, row in enumerate(ROWS, 2):
    for c_idx, val in enumerate(row, 1):
        c = ws.cell(row=r_idx, column=c_idx, value=val)
        c.border = BORDER
        c.alignment = WRAP if c_idx >= 6 else CENTER
        level = row[0]
        if level == 1:
            c.fill = LV1_FILL
            c.font = Font(name="微软雅黑", bold=True)
        else:
            c.fill = ZEBRA_1 if (r_idx % 2 == 0) else ZEBRA_2
            c.font = Font(name="微软雅黑")

# 列宽
widths = [8, 16, 16, 18, 12, 12, 8, 12, 30, 34, 36, 30, 20, 10, 10, 10, 36, 16, 12, 14, 14, 18, 14, 18]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 36
for r in range(2, len(ROWS) + 2):
    ws.row_dimensions[r].height = 48

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(ROWS)+1}"

# ---- 版本历史 sheet ----
ws_hist = wb.create_sheet("版本历史")
HIST_HEADERS = ["节点ID", "指标名称", "版本号", "生效日期", "权重", "变更说明"]
hist_rows = [
    ["1", "科技创新能力", "2024-v1", "2024-01-01", 0.40, "权重上调5%"],
    ["1", "科技创新能力", "2023-v2", "2023-06-01", 0.35, "口径修订（权重不变）"],
    ["1", "科技创新能力", "2023-v1", "2023-01-01", 0.35, "权重上调5%"],
    ["1", "科技创新能力", "2022-v1", "2022-01-01", 0.30, "延续上一版"],
    ["1", "科技创新能力", "2021-v1", "2021-01-01", 0.30, "初始版本"],
    ["1-1", "科研投入", "2024-v1", "2024-01-01", 0.50, "优化权重分配"],
    ["1-1", "科研投入", "2023-v1", "2023-01-01", 0.45, "初始版本"],
    ["2", "科技影响力", "2024-v1", "2024-01-01", 0.30, "新增产业影响力维度"],
    ["2", "科技影响力", "2023-v1", "2023-01-01", 0.25, "初始版本"],
]
for col, h in enumerate(HIST_HEADERS, 1):
    c = ws_hist.cell(row=1, column=col, value=h)
    c.fill = HEADER_FILL
    c.font = HEADER_FONT
    c.alignment = CENTER
    c.border = BORDER
for r_idx, row in enumerate(hist_rows, 2):
    for c_idx, val in enumerate(row, 1):
        c = ws_hist.cell(row=r_idx, column=c_idx, value=val)
        c.border = BORDER
        c.alignment = CENTER if c_idx <= 5 else WRAP
        c.fill = ZEBRA_1 if (r_idx % 2 == 0) else ZEBRA_2
        c.font = Font(name="微软雅黑")
hist_widths = [12, 18, 14, 14, 10, 40]
for i, w in enumerate(hist_widths, 1):
    ws_hist.column_dimensions[get_column_letter(i)].width = w
ws_hist.row_dimensions[1].height = 30
ws_hist.freeze_panes = "A2"

# ---- 赋权方法说明 sheet ----
ws_ws = wb.create_sheet("赋权方法说明")
ws_ws.cell(row=1, column=1, value="字段").fill = HEADER_FILL
ws_ws.cell(row=1, column=1).font = HEADER_FONT
ws_ws.cell(row=1, column=1).alignment = CENTER
ws_ws.cell(row=1, column=1).border = BORDER
ws_ws.cell(row=1, column=2, value="内容").fill = HEADER_FILL
ws_ws.cell(row=1, column=2).font = HEADER_FONT
ws_ws.cell(row=1, column=2).alignment = CENTER
ws_ws.cell(row=1, column=2).border = BORDER
weighting_rows = [
    ("赋权方法名称 (method)", "层次分析法（AHP）结合德尔菲专家赋权"),
    ("方法说明 (methodDetail)",
     "同级指标由专家组两两比较构造判断矩阵，计算特征向量后归一化；一致性比率 CR < 0.1 方可通过。两轮德尔菲修订后定稿，同级权重之和为 100%。"),
    ("赋权步骤 (steps)", "1. 组建科技评价专家组，按一级/二级/三级分层赋权\n2. 同级指标两两比较，构造 AHP 判断矩阵\n3. 求特征向量并归一化，检验一致性比率 CR < 0.1\n4. 两轮德尔菲反馈修订后发布当期权重"),
    ("总体依据 (overallBasis)",
     "一级指标突出科技创新能力（40%）与科技影响力（30%），科技发展潜力（20%）与科技保障能力（10%）作为支撑项，对标国家创新调查制度及科技评价通行做法。"),
    ("注意事项 (note)", "演示口径（Mock）。正式环境以指标委员会赋权纪要为准。"),
]
for r_idx, (k, v) in enumerate(weighting_rows, 2):
    ws_ws.cell(row=r_idx, column=1, value=k).font = Font(name="微软雅黑", bold=True)
    ws_ws.cell(row=r_idx, column=1).fill = LV1_FILL
    ws_ws.cell(row=r_idx, column=1).alignment = WRAP
    ws_ws.cell(row=r_idx, column=1).border = BORDER
    ws_ws.cell(row=r_idx, column=2, value=v).font = Font(name="微软雅黑")
    ws_ws.cell(row=r_idx, column=2).alignment = WRAP
    ws_ws.cell(row=r_idx, column=2).border = BORDER
ws_ws.column_dimensions["A"].width = 26
ws_ws.column_dimensions["B"].width = 90
for r in range(2, len(weighting_rows) + 2):
    ws_ws.row_dimensions[r].height = 60
ws_ws.row_dimensions[1].height = 28

# ---- 填写说明 sheet ----
ws2 = wb.create_sheet("填写说明")
notes = [
    ("M8 科技指标树 · 算法工程师填写表", ""),
    ("", ""),
    ("【用途】", "科技发展态势 M8 页面「指标展示」Tab 的完整数据来源，请算法工程师填写以下四个 sheet，支撑指标树、指标详情、权重展示、版本历史的全部展示内容。"),
    ("", ""),
    ("【四个 Sheet 对应展示内容】", "1) 指标树填写表 → 左侧指标树 + 右侧指标详情（名称/层级/权重/描述/计算/意义）\n2) 版本历史 → 每个指标的版本变更记录（权重变化趋势图、版本明细、变更历程）\n3) 赋权方法说明 → 全局赋权方法与总体依据（指标详情中的权重展示卡片 + 底部说明）\n4) 填写说明 → 本说明"),
    ("", ""),
    ("【整体结构】", "固定三级结构：一级(level=1) → 二级(level=2) → 三级(level=3, 叶节点)。前端按 level 缩进渲染。"),
    ("", ""),
    ("【赋权方法】", "AHP 主观权重 × 熵权法客观权重 等比合成（算法公共约定）；权重一律落配置表，不硬编码。"),
    ("", ""),
    ("字段填写说明：", ""),
    ("层级 (level)", "必填。1=一级指标，2=二级指标，3=三级指标(叶节点)。"),
    ("一级/二级/三级指标", "按所属层级填写指标中文名称，其余层级列留空。"),
    ("节点ID (node_id)", "必填。层级编码，如 1 / 1-1 / 1-1-1，需唯一。版本历史 sheet 通过此字段关联。"),
    ("父节点ID (parent_id)", "必填（一级节点留空）。落库建表必备字段，用于构建树结构和按父节点查询子节点。如 1-1 的 parent_id 为 1。"),
    ("权重 (weight)", "必填。0~1 之间的小数；同一父节点下所有子节点权重之和须 = 1。"),
    ("指标版本 (version)", "必填。当前指标的版本号，如 v2024-01。支持版本化查询与历史版本切换。"),
    ("赋权依据 (weight_basis)", "本指标权重的赋权理由，展示在指标详情的「指标权重展示」卡片中。如暂无依据可填「由同级专家赋权归一化得到」。"),
    ("指标描述 (description)", "指标的业务定义/口径说明。"),
    ("计算公式/方法 (calculation)", "可复现的计算公式或算法步骤。"),
    ("指标意义 (significance)", "该指标的业务含义与价值。"),
    ("metric_id", "仅三级(叶节点)必填，需在指标目录(/metrics/v1/catalog)已登记；未登记则留空并在「就绪状态」标❌，前端将显示红问号(D1 missing)。非叶节点禁止填写。"),
    ("计量单位 (unit)", "指标数值的单位，如 %、万元、件、次、分等。非数值型指标可留空。"),
    ("数据类型 (data_type)", "落库字段类型：int / float / string / boolean 等。"),
    ("所属领域 (domain)", "指标所属领域分类，如 COMP(综合) / TECH(技术) / TALENT(人才) / ENT(企业) / CHAIN(产业链) / POLICY(政策) / ORG(科研机构) / SVC(服务机构)。"),
    ("数据源表 (source_tables)", "指标 8 件套：源表及字段血缘，如 dwd.enterprise.rd_investment <- ods: dwd_org_annual_financial_info"),
    ("源系统 (source_systems)", "数据来源系统/库，如 统计年鉴、企业年报、NebulaGraph 图谱等。"),
    ("更新频率 (update_freq)", "daily / weekly / monthly / quarterly / annual。"),
    ("就绪状态 (mapping_status)", "✅已就绪 / ⚠️待确认(口径待甲方确认) / 🔧算法待实现 / ❌数据缺失。"),
    ("待确认项 (pending_ref)", "如存在未决口径，填写决策清单编号，如 Q010、Q-TINDEX-02、QPOL-02。"),
    ("BID引用 (bid_ref)", "指标 8 件套追溯字段：对应 BID 文档中的章节编号，如 §1.1.1.1.4.1.1.1。"),
    ("验收单元ID (acceptance_unit_id)", "指标 8 件套追溯字段：验收单元编号，如 TI-01-1-1。"),
    ("备注", "其他需要说明的事项。"),
    ("", ""),
    ("【版本历史 sheet 说明】", "每个指标的版本变更记录。同一节点ID可有多行（按时间倒序）。字段：节点ID、指标名称、版本号、生效日期、权重、变更说明。如无历史版本可只填当前版本一行。"),
    ("", ""),
    ("【赋权方法说明 sheet 说明】", "全局赋权方法，整份表只需填一份。字段：赋权方法名称、方法说明、赋权步骤、总体依据、注意事项。"),
    ("", ""),
    ("【示例行】", "各 sheet 中已预填 demo 示例数据，仅供参考填写格式，可直接覆盖或删除。"),
    ("", ""),
    ("【提交要求】", "1) 指标树填写表：每一行一个指标节点，叶节点需有 metric_id 或标缺失，权重同级加总=1，parent_id 必须正确指向父节点；\n2) 版本历史：当前版本必填，历史版本可选；\n3) 赋权方法说明：必填，全表一份；\n4) 未决口径务必填 pending_ref；\n5) node_id、version、domain、metric_id 为落库查询关键字段，不可留空（叶节点 metric_id 缺失除外）。"),
    ("", ""),
    ("【落库与查询说明】", "本表字段对齐接口契约 ts_ti_indicator_tree 表结构。后端落库后可支持：\n- 按 version 查询指定版本的完整指标树\n- 按 parent_id 递归查询子节点构建树结构\n- 按 domain 筛选领域指标\n- 按 metric_id 关联指标 8 件套目录\n- 按 mapping_status 过滤就绪/缺失指标"),
]
for r, (k, v) in enumerate(notes, 1):
    ws2.cell(row=r, column=1, value=k).font = Font(name="微软雅黑", bold=True)
    ws2.cell(row=r, column=2, value=v).font = Font(name="微软雅黑")
    ws2.cell(row=r, column=2).alignment = WRAP
ws2.column_dimensions["A"].width = 26
ws2.column_dimensions["B"].width = 90
for r in range(1, len(notes) + 1):
    ws2.row_dimensions[r].height = 30

wb.save(OUT)
print(f"生成成功: {OUT}")
