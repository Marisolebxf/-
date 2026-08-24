# JIUXIN-TECH-ORG-TALENT-L01 · generate yaml+xlsx from A2 pages + 派单包 §6–§7.
# ponytail: one-shot generator; ceiling = A1 type 回填后改 algorithm.type_source.
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[3]
REQ = ROOT / "metrics" / "request"
OUT = REQ / "九新-技术机构人才"
TOPIC_PAGES = REQ / "专题系统" / "pages"
DS_PAGES = REQ / "展示系统" / "pages"

HEADERS = [
    "系统",
    "维度",
    "page_id",
    "row_id",
    "主项/库叶名",
    "SRS seq",
    "algorithm.type",
    "交付形态",
    "九新确认",
    "备注",
]

# 派单包 §5
LAYER_TYPE = {"基础指标": "STAT", "图谱": "GRAPH", "深度": "MODEL", "实现类": "MODEL"}
TYPE_DELIVERY = {"STAT": "SQL", "GRAPH": "Python", "MODEL": "API", "COMPUTE": "Python"}


def leaf(seq, layer, dim, name, topic, display="", extra=""):
    t = LAYER_TYPE[layer]
    d = TYPE_DELIVERY[t]
    note_parts = []
    if topic:
        note_parts.append("专题消费: " + topic)
    if display:
        note_parts.append("展示消费: " + display)
    if extra:
        note_parts.append(extra)
    return {
        "系统": "专题",
        "维度": dim,
        "page_id": {"技术链": "SRS-TECH", "科研机构": "SRS-ORG", "人才": "SRS-TALENT"}[dim],
        "row_id": f"SRS-{seq}",
        "主项/库叶名": name,
        "SRS seq": seq,
        "algorithm.type": t,
        "algorithm.type_source": "SRS层暂标",
        "交付形态": d,
        "交付形态_source": "沟通起点(非最终)",
        "九新确认": "待确认",
        "row_kind": "库叶",
        "srs_layer": layer,
        "备注": "；".join(note_parts),
    }


LEAVES = [
    leaf(96, "基础指标", "技术链", "技术基础指标模型构建", "TOPIC-TECH-003 论文量/专利量", "态势计数读面，非本包 Job"),
    leaf(104, "图谱", "技术链", "技术实体识别构建", "TOPIC-TECH-002 节点下钻"),
    leaf(105, "图谱", "技术链", "技术实体关系抽取", "TOPIC-TECH-001 技术网络边", "DS-03 弦线 mapped，非 third_party"),
    leaf(130, "深度", "技术链", "全景技术链模型", "TOPIC-TECH-001"),
    leaf(131, "深度", "技术链", "深圳技术链模型", "TOPIC-TECH-011"),
    leaf(132, "深度", "技术链", "技术发展历程模型", "TOPIC-TECH-015 产品走 CMS，库叶仍须问九新有无 API", extra="禁止把历程 CMS 当 Job"),
    leaf(133, "深度", "技术链", "深圳细分领域分布模型", "TOPIC-TECH-012 复用"),
    leaf(134, "深度", "技术链", "技术前沿热点领域识别模型", "TOPIC-TECH-004/005", "DS-03-RESULT-001/002；DS-07-SCI-CREATE-003；DS-09-COMPREHENSIVE-001/002/004"),
    leaf(135, "深度", "技术链", "技术产业化潜力识别模型", "TOPIC-TECH-006/007", "DS-07-TECH-INNOV-003"),
    leaf(136, "深度", "技术链", "技术转化瓶颈堵点原因识别模型", "TOPIC-TECH-013/014"),
    leaf(137, "深度", "技术链", "技术阶段分析模型", "TOPIC-TECH-008/009；TOPIC-TECH-012", "DS-03-RESULT-004/005/006；DS-07-INDUSTRY-POTENTIAL-002"),
    leaf(138, "深度", "技术链", "深圳技术发展问题识别模型", "TOPIC-TECH-012"),
    leaf(139, "深度", "技术链", "深圳技术发展机遇识别模型", "TOPIC-TECH-012"),
    leaf(140, "深度", "技术链", "深圳技术发展重点布局领域推荐模型", "TOPIC-TECH-012"),
    leaf(99, "基础指标", "科研机构", "科研机构基础指标模型构建", "TOPIC-RORG-002/005/006/008"),
    leaf(114, "图谱", "科研机构", "科研机构实体识别构建", "机构节点（与选取壳 RORG-001 分开）；A2 标 other_system，库叶仍问"),
    leaf(115, "图谱", "科研机构", "科研机构实体关系抽取", "随合作链；A2 KPI 不挂 115，库叶仍问"),
    leaf(149, "深度", "科研机构", "科研机构重点技术领域布局模型", "TOPIC-RORG-003/008"),
    leaf(150, "深度", "科研机构", "科研机构发展历程模型", "TOPIC-RORG-017 产品走 CMS，库叶仍问"),
    leaf(151, "深度", "科研机构", "深圳科研机构优势分析模型", "TOPIC-RORG-015"),
    leaf(152, "深度", "科研机构", "深圳科研机构痛难点识别模型", "TOPIC-RORG-016"),
    leaf(153, "深度", "科研机构", "科研合作关系链条模型", "TOPIC-RORG-010"),
    leaf(154, "深度", "科研机构", "科研机构引入推荐模型", "TOPIC-RORG-013"),
    leaf(155, "深度", "科研机构", "科研机构扶持推荐模型", "TOPIC-RORG-014"),
    leaf(98, "基础指标", "人才", "人才基础指标模型构建", "TOPIC-TAL-001/002/003", "DS-13/14 分布 mapped"),
    leaf(110, "图谱", "人才", "人才实体识别构建", "TOPIC-TAL-014", "DS-13/15/16 画像 mapped"),
    leaf(111, "图谱", "人才", "人才实体关系抽取", "TOPIC-TAL-015", "DS-15/16 合作网 mapped"),
    leaf(156, "深度", "人才", "重点人才识别模型", "TOPIC-TAL-012", "DS-15 画像 mapped"),
    leaf(157, "深度", "人才", "人才流动追踪模型", "TOPIC-TAL-013", "DS-13/14 迁徙 mapped；禁止轨迹引擎"),
    leaf(158, "深度", "人才", "高校学院新培育人才模型", "TOPIC-TAL-010"),
    leaf(159, "深度", "人才", "深圳重点人才优势和短板分析模型", "TOPIC-TAL-005"),
    leaf(160, "深度", "人才", "人才关系链模型", "TOPIC-TAL-004", "DS-15/16 合作网 mapped"),
    leaf(161, "深度", "人才", "人才供需分析评价模型", "TOPIC-TAL-011"),
    leaf(162, "深度", "人才", "人才学术力评估模型", "TOPIC-TAL-006", "DS-08-VIZ-001 H指数、DS-08-VIZ-004 活跃度 third_party；DS-13/15 mapped"),
    leaf(163, "深度", "人才", "人才产业力评估模型", "TOPIC-TAL-007", "DS-15 画像 mapped"),
    leaf(164, "深度", "人才", "招入人才推荐模型", "TOPIC-TAL-008", "DS-13/16 推荐/画像 mapped"),
    leaf(165, "深度", "人才", "培育人才布局模型", "TOPIC-TAL-009"),
]

RORG012 = {
    "系统": "专题",
    "维度": "科研机构",
    "page_id": "TOPIC-ORG-05",
    "row_id": "TOPIC-RORG-012",
    "主项/库叶名": "科研机构技术力评价与对比（05 无专叶）",
    "SRS seq": None,
    "algorithm.type": "MODEL",
    "algorithm.type_source": "A2 third_party / 无专叶暂标 MODEL",
    "交付形态": "API",
    "交付形态_source": "沟通起点(非最终)",
    "九新确认": "待确认",
    "row_kind": "无专叶项",
    "srs_layer": "实现类",
    "备注": "TOPIC-RORG-012 third_party。禁止用 M_SVC_ORG_TECH_SCORE / seq 174–179 顶替。必须单列问九新。",
}

DISPLAY_TP = [
    ("DS-03-RESULT", "DS-03-RESULT-001", "技术链", "话题热力图展示", 134, "技术评估结果"),
    ("DS-03-RESULT", "DS-03-RESULT-002", "技术链", "技术话题热度", 134, "技术评估结果"),
    ("DS-03-RESULT", "DS-03-RESULT-004", "技术链", "动态气泡图（阶段/成熟度）", 137, "技术评估结果"),
    ("DS-03-RESULT", "DS-03-RESULT-005", "技术链", "技术成熟度", 137, "技术评估结果"),
    ("DS-03-RESULT", "DS-03-RESULT-006", "技术链", "技术发展阶段", 137, "技术评估结果"),
    ("DS-07-INDUSTRY-POTENTIAL", "DS-07-INDUSTRY-POTENTIAL-002", "技术链", "技术产品成熟度评估", 137, "产业发展潜力"),
    ("DS-07-TECH-INNOV", "DS-07-TECH-INNOV-003", "技术链", "技术市场潜力分析", 135, "技术创新力"),
    ("DS-07-SCI-CREATE", "DS-07-SCI-CREATE-003", "技术链", "科学研究前沿性分析", 134, "科学创造力"),
    ("DS-09-COMPREHENSIVE", "DS-09-COMPREHENSIVE-001", "技术链", "全球热点技术捕捉 · 热度", 134, "综合发展规划"),
    ("DS-09-COMPREHENSIVE", "DS-09-COMPREHENSIVE-002", "技术链", "全球热点技术捕捉 · 增速", 134, "综合发展规划"),
    ("DS-09-COMPREHENSIVE", "DS-09-COMPREHENSIVE-004", "技术链", "技术与产业热点动态跟踪", 134, "综合发展规划"),
    ("DS-08-VIZ", "DS-08-VIZ-001", "人才", "专家 H 指数排行", 162, "指数可视化"),
    ("DS-08-VIZ", "DS-08-VIZ-004", "人才", "专家活跃度", 162, "指数可视化"),
]


def display_row(page_id, row_id, dim, name, seq, page_name):
    t = "MODEL"
    return {
        "系统": "展示",
        "维度": dim,
        "page_id": page_id,
        "row_id": row_id,
        "主项/库叶名": name,
        "SRS seq": seq,
        "algorithm.type": t,
        "algorithm.type_source": "SRS层暂标(深度/实现类)",
        "交付形态": "API",
        "交付形态_source": "沟通起点(非最终)；读面跟所挂库叶",
        "九新确认": "待确认",
        "row_kind": "展示third_party",
        "srs_layer": "深度",
        "备注": f"页面={page_name}；A2 third_party；挂库叶 SRS-{seq}；不单独再要一份（与库叶同交）。禁止前端直连九新。",
    }


def load_items(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("page_id"), data.get("items") or []


def parse_seq(item: dict):
    for key in ("A1需规ID", "取数依据", "缺口说明"):
        v = item.get(key)
        if not v:
            continue
        m = re.search(r"(?:seq\s+|DEEP-|GRAPH-|BASE-|SRS-)(\d{2,3})", str(v), re.I)
        if m:
            return int(m.group(1))
    leaf = item.get("algo_lib_leaf") or ""
    return None


TOPIC_FILE = {
    "技术链": "TOPIC-TECH-05.yaml",
    "科研机构": "TOPIC-ORG-05.yaml",
    "人才": "TOPIC-TALENT-05.yaml",
}

SEQ_TO_LEAF = {r["SRS seq"]: r for r in LEAVES}


def topic_trace_rows():
    rows = []
    for dim, fn in TOPIC_FILE.items():
        page_id, items = load_items(TOPIC_PAGES / fn)
        for it in items:
            v = it.get("差集判定")
            if v not in ("mapped", "third_party"):
                continue
            seq = None
            a1 = it.get("A1需规ID") or ""
            m = re.search(r"(\d{2,3})$", str(a1))
            if m:
                seq = int(m.group(1))
            if seq is None:
                seq = parse_seq(it)
            parent = SEQ_TO_LEAF.get(seq) if seq else None
            if it.get("row_id") == "TOPIC-RORG-012":
                parent = RORG012
                seq = None
            delivery = parent["交付形态"] if parent else "API"
            atype = parent["algorithm.type"] if parent else "MODEL"
            rows.append(
                {
                    "系统": "专题",
                    "维度": dim,
                    "page_id": page_id,
                    "row_id": it["row_id"],
                    "主项/库叶名": it.get("主项"),
                    "SRS seq": seq,
                    "algorithm.type": atype,
                    "algorithm.type_source": "继承库叶暂标",
                    "交付形态": delivery,
                    "交付形态_source": "继承库叶沟通起点；不单独向九新再要一份",
                    "九新确认": "待确认",
                    "row_kind": "专题页面行",
                    "a2_verdict": v,
                    "备注": f"A2={v}；回溯→{parent['row_id'] if parent else 'RORG-012' if it.get('row_id')=='TOPIC-RORG-012' else '未挂叶'}。n/a_ops/other_system 未进本表。",
                }
            )
    return rows


DISPLAY_TALENT_MAP = [
    ("DS-13-TALENT-GLOBAL", 98, "人才分布/领域/供给计数"),
    ("DS-13-TALENT-GLOBAL", 110, "人才基础属性/领域 NER"),
    ("DS-13-TALENT-GLOBAL", 111, "合作网薄子图"),
    ("DS-13-TALENT-GLOBAL", 157, "流动（关系+时间，禁止轨迹）"),
    ("DS-13-TALENT-GLOBAL", 162, "成果统计/影响力"),
    ("DS-13-TALENT-GLOBAL", 164, "匹配度只读，不跑 DS-16 Job"),
    ("DS-14-TALENT-REGION", 98, "排行/趋势/结构"),
    ("DS-14-TALENT-REGION", 157, "迁徙图"),
    ("DS-15-TALENT-PROFILE", 156, "重点人才综合评分"),
    ("DS-15-TALENT-PROFILE", 162, "权威度/学术影响力"),
    ("DS-15-TALENT-PROFILE", 163, "贡献度/产业力"),
    ("DS-15-TALENT-PROFILE", 160, "关系链/合作网"),
    ("DS-15-TALENT-PROFILE", 110, "实体属性/关键词"),
    ("DS-15-TALENT-PROFILE", 111, "人才–成果/机构关系"),
    ("DS-16-TALENT-RECRUIT", 164, "招入推荐/匹配/名单"),
    ("DS-16-TALENT-RECRUIT", 160, "过往合作/合作网络"),
    ("DS-16-TALENT-RECRUIT", 111, "合作关系抽取"),
    ("DS-16-TALENT-RECRUIT", 110, "尽调画像档案"),
]


def display_talent_rows():
    rows = []
    for page_id, seq, name in DISPLAY_TALENT_MAP:
        parent = SEQ_TO_LEAF[seq]
        rows.append(
            {
                "系统": "展示",
                "维度": "人才",
                "page_id": page_id,
                "row_id": f"{page_id}-SEQ-{seq}",
                "主项/库叶名": name,
                "SRS seq": seq,
                "algorithm.type": parent["algorithm.type"],
                "algorithm.type_source": "继承库叶暂标",
                "交付形态": parent["交付形态"],
                "交付形态_source": "继承库叶；A2 mapped 非 third_party，沟通时带上",
                "九新确认": "待确认",
                "row_kind": "展示人才mapped",
                "a2_verdict": "mapped",
                "备注": f"A2 无 third_party。回溯→SRS-{seq} {parent['主项/库叶名']}。n/a_ops/报告导出/指数 CMS 不问九新要模型。",
            }
        )
    return rows


EXCLUDED = [
    {
        "系统": "展示",
        "维度": "（非本包）企业",
        "page_id": "ENT-SEARCH",
        "row_id": "ENT-SEARCH-009",
        "主项/库叶名": "市场份额（Q019）",
        "SRS seq": None,
        "algorithm.type": None,
        "交付形态": None,
        "九新确认": "不进本包",
        "row_kind": "排除",
        "备注": "企业展示采购项，不是技术/机构/人才。A2 16 条 third_party 之一。",
    },
    {
        "系统": "展示",
        "维度": "（非本包）投融资",
        "page_id": "CHAIN-PORTAL-OVERVIEW",
        "row_id": "DS-CHAIN-OV-009",
        "主项/库叶名": "投融资总额（QC07）",
        "SRS seq": None,
        "algorithm.type": None,
        "交付形态": None,
        "九新确认": "不进本包",
        "row_kind": "排除",
        "备注": "产业链门户待采购，不是九新技术包。",
    },
    {
        "系统": "展示",
        "维度": "（非本包）投融资",
        "page_id": "CHAIN-PORTAL-OVERVIEW",
        "row_id": "DS-CHAIN-OV-010",
        "主项/库叶名": "投融资事件数（QC07）",
        "SRS seq": None,
        "algorithm.type": None,
        "交付形态": None,
        "九新确认": "不进本包",
        "row_kind": "排除",
        "备注": "产业链门户待采购，不是九新技术包。",
    },
]

DS16_MISSING = [
    ("DS-16-TALENT-RECRUIT-005", "沟通障碍智能检测"),
    ("DS-16-TALENT-RECRUIT-006", "文化融合风险评估"),
    ("DS-16-TALENT-RECRUIT-007", "国际流动壁垒分析"),
    ("DS-16-TALENT-RECRUIT-010", "引进阻力量化评分"),
    ("DS-16-TALENT-RECRUIT-013", "高精度成本模型构建"),
    ("DS-16-TALENT-RECRUIT-025", "团队组合与协同分析"),
]


def public_row(r: dict) -> dict:
    out = {k: r.get(k) for k in HEADERS}
    return out


def write_yaml(items, topic_trace, ds_talent, excluded):
    OUT.mkdir(parents=True, exist_ok=True)
    counts = Counter(r["交付形态"] for r in items)
    conf = Counter(r["九新确认"] for r in items)
    doc = {
        "version": 1,
        "task": "JIUXIN-TECH-ORG-TALENT-L01",
        "updated": "2026-08-24",
        "algorithm_type_source": "SRS层暂标；A1 ALGO-LIB-METRIC-DEPS-L01 交卷后回填，不挡本叶",
        "jiuxin_confirm_rule": "未开会不得写成确认或九新已交；本批全部待确认",
        "forbidden": [
            "前端直连九新",
            "改 cfg_metric-*-seed.yaml",
            "写业务代码",
            "复活 TOPIC/DS-METRIC-INVENTORY/CLASSIFY-L01",
            "混入 ENT-SEARCH-009 / DS-CHAIN-OV-009 / DS-CHAIN-OV-010",
        ],
        "counts_对人主表": {
            "rows": len(items),
            "SQL": counts["SQL"],
            "Python": counts["Python"],
            "API": counts["API"],
            "待确认": conf["待确认"],
            "确认": 0,
            "九新不提供": 0,
            "库叶": 37,
            "无专叶项": 1,
            "展示third_party": 13,
        },
        "items": items,
        "topic_trace": topic_trace,
        "display_talent_mapped": ds_talent,
        "excluded": excluded,
        "ds16_missing_appendix": [
            {
                "row_id": rid,
                "主项": name,
                "note": "我方库缺口 A2 missing；纪要附录：不向九新索要假 API",
            }
            for rid, name in DS16_MISSING
        ],
    }
    path = OUT / "JIUXIN-TECH-ORG-TALENT-L01.yaml"
    path.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    return path, counts, conf


THIN = Border(
    left=Side(style="thin", color="D0D5DD"),
    right=Side(style="thin", color="D0D5DD"),
    top=Side(style="thin", color="D0D5DD"),
    bottom=Side(style="thin", color="D0D5DD"),
)
HDR_FILL = PatternFill("solid", fgColor="165DFF")
HDR_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
BODY_FONT = Font(name="Calibri", size=11)
SQL_FILL = PatternFill("solid", fgColor="E8F3FF")
PY_FILL = PatternFill("solid", fgColor="E8FFEA")
API_FILL = PatternFill("solid", fgColor="FFF7E8")
WAIT_FILL = PatternFill("solid", fgColor="FFF3E8")
SKIP_FILL = PatternFill("solid", fgColor="F2F3F5")
TITLE_FONT = Font(name="Calibri", bold=True, size=14, color="1D2129")


def style_header(ws, ncols):
    for col in range(1, ncols + 1):
        c = ws.cell(1, col)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = Alignment(horizontal="center", vertical="center", wrapText=True)
        c.border = THIN
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}1"
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 22


def write_sheet_rows(ws, rows, title=None):
    for i, h in enumerate(HEADERS, 1):
        ws.cell(1, i, h)
    style_header(ws, len(HEADERS))
    fills = {"SQL": SQL_FILL, "Python": PY_FILL, "API": API_FILL}
    for r_i, row in enumerate(rows, 2):
        for c_i, h in enumerate(HEADERS, 1):
            val = row.get(h)
            cell = ws.cell(r_i, c_i, "" if val is None else val)
            cell.font = BODY_FONT
            cell.alignment = Alignment(vertical="center", wrapText=True)
            cell.border = THIN
            if h == "交付形态" and val in fills:
                cell.fill = fills[val]
            if h == "九新确认" and val == "待确认":
                cell.fill = WAIT_FILL
            if h == "九新确认" and val == "不进本包":
                cell.fill = SKIP_FILL
    widths = [8, 12, 26, 32, 36, 10, 16, 12, 12, 56]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    last = max(2, len(rows) + 1)
    dv1 = DataValidation(type="list", formula1='"SQL,Python,API"', allow_blank=True)
    dv2 = DataValidation(type="list", formula1='"确认,待确认,九新不提供"', allow_blank=True)
    ws.add_data_validation(dv1)
    ws.add_data_validation(dv2)
    dv1.add(f"H2:H{last}")
    dv2.add(f"I2:I{last}")
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{last}"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.print_title_rows = "1:1"
    ws.page_setup.horizontalCentered = True
    ws.oddFooter.left.text = "JIUXIN-TECH-ORG-TALENT-L01 · 未确认不得写成已交"
    ws.oddFooter.right.text = "第 &P 页 / 共 &N 页"


def write_count_sheet(ws, n_items):
    ws["A1"] = "九新交付形态计数（对人主表）"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:C1")
    labels = [
        (3, "SQL"),
        (4, "Python"),
        (5, "API"),
        (6, "待确认"),
        (7, "确认"),
        (8, "九新不提供"),
        (9, "对人主表行数"),
        (11, "库叶"),
        (12, "无专叶项 RORG-012"),
        (13, "展示 third_party"),
    ]
    ws["A2"] = "口径"
    ws["B2"] = "条数"
    ws["C2"] = "公式/说明"
    for col in range(1, 4):
        ws.cell(2, col).fill = HDR_FILL
        ws.cell(2, col).font = HDR_FONT
        ws.cell(2, col).border = THIN
    last = 1 + n_items
    formulas = {
        3: ('=COUNTIF(对人主表!H:H,"SQL")', "沟通起点 STAT→SQL"),
        4: ('=COUNTIF(对人主表!H:H,"Python")', "沟通起点 GRAPH→Python（Nebula，禁止 Neo4j）"),
        5: ('=COUNTIF(对人主表!H:H,"API")', "沟通起点 MODEL / 无专叶 / 展示 third_party"),
        6: ('=COUNTIF(对人主表!I:I,"待确认")', "本批全部待确认；开会后改「确认」或「九新不提供」"),
        7: ('=COUNTIF(对人主表!I:I,"确认")', "必须有纪要签字；禁止 agent 自填"),
        8: ('=COUNTIF(对人主表!I:I,"九新不提供")', "必须有纪要；禁止口头"),
        9: ("=COUNTA(对人主表!D:D)-1", "应=51（37 库叶 + 1 无专叶 + 13 展示）"),
        11: ('=COUNTIF(对人主表!D:D,"SRS-*")', "应=37"),
        12: ('=COUNTIF(对人主表!D:D,"TOPIC-RORG-012")', "应=1"),
        13: ('=COUNTIF(对人主表!A:A,"展示")', "应=13（主表不含 DS-13～16 mapped）"),
    }
    for row, label in labels:
        ws.cell(row, 1, label).font = BODY_FONT
        ws.cell(row, 1).border = THIN
        f, note = formulas[row]
        c = ws.cell(row, 2, f)
        c.font = Font(name="Calibri", size=11, color="000000")
        c.border = THIN
        ws.cell(row, 3, note).font = BODY_FONT
        ws.cell(row, 3).border = THIN
        ws.cell(row, 3).alignment = Alignment(wrapText=True)
    ws["A15"] = "禁止"
    ws["A15"].font = Font(name="Calibri", bold=True, size=12)
    ws["A16"] = "未与北京九新开会不得把 I 列改成「确认」。前端禁止直连九新。不改 seed。不挡 A1。"
    ws.merge_cells("A16:C16")
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 56
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1


def write_xlsx(items, topic_trace, ds_talent, excluded):
    wb = Workbook()
    ws0 = wb.active
    ws0.title = "对人主表"
    write_sheet_rows(ws0, items)
    ws1 = wb.create_sheet("专题回溯")
    write_sheet_rows(ws1, topic_trace)
    ws2 = wb.create_sheet("展示人才mapped")
    write_sheet_rows(ws2, ds_talent)
    ws3 = wb.create_sheet("不进本包")
    write_sheet_rows(ws3, excluded)
    ws4 = wb.create_sheet("计数")
    write_count_sheet(ws4, len(items))
    ws4.sheet_view.showGridLines = False
    path = OUT / "JIUXIN-TECH-ORG-TALENT-L01.xlsx"
    wb.save(path)
    return path


def check(items, topic_trace):
    errs = []
    seqs = [r["SRS seq"] for r in items if r.get("row_kind") == "库叶"]
    if len(seqs) != 37:
        errs.append(f"库叶 {len(seqs)} != 37")
    if len(set(seqs)) != 37:
        errs.append("库叶 seq 重复")
    if not any(r["row_id"] == "TOPIC-RORG-012" for r in items):
        errs.append("缺 RORG-012")
    ds = [r for r in items if r.get("row_kind") == "展示third_party"]
    if len(ds) != 13:
        errs.append(f"展示 third_party {len(ds)} != 13")
    banned = {"ENT-SEARCH-009", "DS-CHAIN-OV-009", "DS-CHAIN-OV-010"}
    ids = {r["row_id"] for r in items}
    if ids & banned:
        errs.append(f"主表混入排除项 {ids & banned}")
    if any(r["九新确认"] == "确认" for r in items):
        errs.append("未开会写成确认")
    tech_m = [r for r in topic_trace if r["维度"] == "技术链"]
    org_m = [r for r in topic_trace if r["维度"] == "科研机构"]
    tal_m = [r for r in topic_trace if r["维度"] == "人才"]
    if len(tal_m) != 15:
        errs.append(f"专题人才 mapped/tp {len(tal_m)} != 15")
    if not any(r["row_id"] == "TOPIC-RORG-012" for r in topic_trace + items):
        errs.append("RORG-012 未入表")
    # TECH mapped 4 + third_party 9 = 13; ORG mapped 10 + tp 1 = 11
    if len(tech_m) != 13:
        errs.append(f"专题技术链 mapped/tp {len(tech_m)} != 13")
    if len(org_m) != 11:
        errs.append(f"专题机构 mapped/tp {len(org_m)} != 11")
    assert not errs, "\n".join(errs)


def main():
    items = list(LEAVES) + [RORG012] + [display_row(*t) for t in DISPLAY_TP]
    topic_trace = topic_trace_rows()
    ds_talent = display_talent_rows()
    check(items, topic_trace)
    ypath, counts, conf = write_yaml(items, topic_trace, ds_talent, EXCLUDED)
    xpath = write_xlsx(items, topic_trace, ds_talent, EXCLUDED)
    print("yaml", ypath)
    print("xlsx", xpath)
    print("items", len(items), dict(counts), dict(conf))
    print("topic_trace", len(topic_trace), "ds_talent", len(ds_talent))


if __name__ == "__main__":
    main()
