# -*- coding: utf-8 -*-
"""V1.1 总集用例生成：扩非通用至~1300、总~1700，并结合设计方案具体化描述。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment

ROOT = Path(r"d:\work\gkx-lumen")
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
BID = ROOT / "gkx-orchestration" / "agent-delivery" / "bid-reference" / "科技信息展示系统和科技专题服务系统.md"
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
OUT_DIR = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "科技专题战略分析-v1.1"
)

L3 = "科技专题战略分析"
L4_TARGETS = ["综合智能分析", "政策分析", "企业分析", "产业链分析", "产业服务链分析"]
PLATE, SYSTEM, VERSION, TEST_TYPE = "ZNFWJQ", "KJZTFWXT", "v1.0", "FUNC"

# 目标：非通用 ~1300，总 ~1700（通用保留并略补）
TARGET_NON_GENERIC = 1300
TARGET_TOTAL = 1700
GENERIC_PER_MODULE = 6  # 入口/权限/加载/空态/异常/结果一致性


def norm(s: str) -> str:
    if s is None:
        return ""
    return re.sub(r"\s+", "", str(s).strip())


def load_function_tree():
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技专题服务系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        if "需规功能描述" in "".join(str(x or "") for x in row[:14]):
            header_idx = i
            break
    i1, i2, i3, i4, i5, i6, i_desc = 6, 7, 8, 9, 10, 11, 12
    cur = [""] * 6
    items = []
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (i1, i2, i3, i4, i5, i6)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        if cur[2] != L3 or cur[3] not in L4_TARGETS:
            continue
        desc = str(vals[i_desc]).strip() if vals[i_desc] else ""
        if not (cur[4] or cur[5] or desc):
            continue
        items.append(
            {
                "l4": cur[3],
                "l5": cur[4] or "/",
                "l6": cur[5] or "/",
                "desc": desc,
            }
        )
    wb.close()
    return items


def parse_bid_design() -> dict:
    """Parse 1.1.1.2.4.2 科技专题战略分析 into title -> {body, children}."""
    text = BID.read_text(encoding="utf-8")
    # Restrict to strategic analysis section until 1.1.1.2.4.3
    m_start = re.search(r"1\.1\.1\.2\.4\.2\.\s*\*\*科技专题战略分析\*\*", text)
    m_end = re.search(r"######\s*1\.1\.1\.2\.4\.3\.", text)
    if not m_start:
        return {}
    chunk = text[m_start.start() : m_end.start() if m_end else m_start.start() + 80000]

    # Heading lines like 1.1.1.2.4.2.3.1.1. 产业与企业类型筛选 or **重点企业类型分析**
    heading_re = re.compile(
        r"^(?P<num>\d+(?:\.\d+)*)\.?\s*(?:\*\*)?(?P<title>[^\*\n]{2,40}?)(?:\*\*)?\s*$",
        re.M,
    )
    matches = list(heading_re.finditer(chunk))
    index = {}
    for i, m in enumerate(matches):
        title = norm(m.group("title"))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(chunk)
        body = chunk[start:end].strip()
        # strip images and empty
        body = re.sub(r"!\[.*?\]\(.*?\)", "", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if not title:
            continue
        # keep longest body if duplicate titles
        if title not in index or len(body) > len(index[title]["body"]):
            index[title] = {"num": m.group("num"), "body": body, "title": m.group("title").strip()}
    return index


def lookup_design(index: dict, l5: str, l6: str) -> str:
    """Find best matching design paragraph for L5/L6."""
    keys = [norm(l6), norm(l5)]
    for k in keys:
        if k in index and index[k]["body"]:
            return index[k]["body"]
    # fuzzy contains
    for k, v in index.items():
        if k and (k in norm(l6) or norm(l6) in k or k in norm(l5) or norm(l5) in k):
            if v["body"]:
                return v["body"]
    return ""


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[。；;\n]+", text.replace("\r", "\n"))
    out = []
    for p in parts:
        p = p.strip(" 、，,")
        # skip junk that is only sibling titles leaked
        if len(p) < 8:
            continue
        if p.startswith("http") or p.startswith("file:"):
            continue
        out.append(p)
    return out


def extract_ui_hints(design: str) -> list[str]:
    hints = []
    patterns = [
        (r"雷达图", "结果区出现雷达图对比"),
        (r"热力图", "结果区出现热力图"),
        (r"柱状图", "结果区出现柱状图"),
        (r"知识图谱|交互式图谱|图谱形式", "出现可交互图谱/网络可视化"),
        (r"流程图|时间轴", "以流程图或时间轴呈现阶段"),
        (r"下钻", "支持逐级下钻且下钻后数据刷新"),
        (r"自定义|赋权|权重", "可配置指标/权重并重新计算"),
        (r"导出", "支持导出报告或结果文件"),
        (r"推荐名单|推荐列表", "输出推荐名单且含依据/指标"),
        (r"空态|无数据", "无数据时有可读空态"),
        (r"筛选", "筛选条件生效且摘要可读"),
        (r"对标|对比", "多对象/多区域对比视图可用"),
        (r"评分|得分|指数", "输出量化评分/指数且可读"),
        (r"报告", "可查看或生成分析报告"),
    ]
    for pat, hint in patterns:
        if re.search(pat, design):
            hints.append(hint)
    return hints


def atoms_from_text(text: str, l5: str, l6: str, source_tag: str) -> list[dict]:
    atoms = []
    for sent in split_sentences(text):
        # parenthetical enums
        for group in re.findall(r"[（(]([^）)]{2,40})[）)]", sent):
            for tag in re.split(r"[、,/，]", group):
                tag = tag.strip()
                if 2 <= len(tag) <= 12 and not tag.isdigit():
                    atoms.append(
                        {
                            "功能项": "选项覆盖",
                            "子功能项": tag,
                            "功能点": f"{tag}可选或可识别",
                            "测试内容": f"[{source_tag}] 界面提供或识别「{tag}」（出处：{sent[:50]}）",
                            "source": sent,
                            "kind": "biz",
                        }
                    )
        for pat in [
            r"(允许用户[^，。；]{4,50})",
            r"(支持[^，。；]{4,50})",
            r"(提供[^，。；]{4,50})",
            r"(展示[^，。；]{4,50})",
            r"(计算[^，。；]{4,50})",
            r"(生成[^，。；]{4,50})",
            r"(识别[^，。；]{4,50})",
            r"(对比[^，。；]{4,50})",
            r"(筛选[^，。；]{4,50})",
            r"(下钻[^，。；]{4,50})",
            r"(配置[^，。；]{4,50})",
            r"(输出[^，。；]{4,50})",
            r"(评估[^，。；]{4,50})",
            r"(推荐[^，。；]{4,50})",
            r"(构建[^，。；]{4,50})",
            r"(标注[^，。；]{4,50})",
            r"(采集[^，。；]{4,50})",
            r"(关联[^，。；]{4,50})",
            r"(可视化[^，。；]{4,40})",
        ]:
            for m in re.finditer(pat, sent):
                frag = m.group(1).strip(" ：:")
                atoms.append(
                    {
                        "功能项": l6 if l6 != "/" else l5,
                        "子功能项": frag[:18],
                        "功能点": frag[:32],
                        "测试内容": f"[{source_tag}] {frag}",
                        "source": sent,
                        "kind": "biz",
                    }
                )
        # full sentence as主路径（跳过过短/纯列举标题）
        title_like = sent.count("、") >= 3 and len(sent) < 60 and "该功能" not in sent
        if not title_like:
            fp = sent[:30]
            if sent.startswith("该功能"):
                fp = sent[3:33]
            elif sent.startswith("本功能"):
                fp = sent[3:33]
            atoms.append(
                {
                    "功能项": l6 if l6 != "/" else l5,
                    "子功能项": "需规/设计主路径",
                    "功能点": fp.strip("：:，,")[:40],
                    "测试内容": f"[{source_tag}] {sent[:160]}",
                    "source": sent,
                    "kind": "biz",
                }
            )
    return atoms


def enrich_case(atom: dict, l5: str, l6: str, design: str) -> dict:
    src = atom.get("source") or atom["测试内容"]
    hints = extract_ui_hints(design or src)
    hint_txt = "；".join(hints[:4]) if hints else "关键控件与结果区可读"

    steps = (
        f"1.登录系统，进入「科技专题战略分析」→「{l5}」→「{l6}」\n"
        f"2.按功能点「{atom['功能点']}」准备输入（筛选/对象/参数等，按页面实际控件）\n"
        f"3.执行查询/应用/计算/打开视图等主操作\n"
        f"4.核验界面结果：{hint_txt}\n"
        f"5.对照需求要点核对：{src[:90]}"
    )
    expect = (
        f"1、页面可达且模块定位正确（{l5}/{l6}）\n"
        f"2、功能点「{atom['功能点']}」可完成：{atom['测试内容'][:110]}\n"
        f"3、结果表现具体可观察：{hint_txt}\n"
        f"4、无白屏/未捕获异常；空数据有空态，失败有可读提示\n"
        f"5、不越权展示其他四级模块专属结论"
    )
    return {
        "功能项": str(atom["功能项"])[:30],
        "子功能项": str(atom["子功能项"])[:30],
        "功能点": str(atom["功能点"])[:40],
        "测试内容": atom["测试内容"][:180],
        "前置条件": "1、系统正常；2、已登录且具备本模块权限；3、测试数据可用（允许 Mock，须可辨）；4、可访问科技专题战略分析",
        "测试步骤": steps,
        "预期结果": expect,
        "优先级": atom.get("优先级", "P1"),
        "页面": f"{l5}/{l6}",
        "kind": atom.get("kind", "biz"),
    }


GENERIC_TEMPLATES = [
    ("入口可达", "模块入口与导航", "可从专题导航进入本子模块", "P0"),
    ("权限控制", "访问权限", "无权限不可操作受控功能", "P1"),
    ("加载态", "数据加载反馈", "请求中有加载反馈且完成后消失", "P1"),
    ("空数据态", "无数据空态", "无命中时可读空态、不伪装业务数", "P1"),
    ("异常态", "接口失败提示", "失败时可读错误且不崩溃", "P1"),
    ("结果一致性", "统计与列表一致", "汇总与明细口径一致或差异可解释", "P1"),
]


def generic_cases(l5: str, l6: str) -> list[dict]:
    out = []
    for name, sub, content, pri in GENERIC_TEMPLATES[:GENERIC_PER_MODULE]:
        steps = {
            "入口可达": f"1.从侧栏进入科技专题战略分析\n2.打开{l5}/{l6}\n3.确认标题与模块一致",
            "权限控制": "1.无权限账号访问\n2.有权限账号访问\n3.对比入口与操作可用性",
            "加载态": "1.触发列表/图表加载\n2.观察加载指示\n3.等待完成",
            "空数据态": "1.构造无命中条件\n2.观察结果区",
            "异常态": "1.模拟失败或断网刷新\n2.观察提示与可恢复性",
            "结果一致性": "1.记录汇总数字\n2.核对列表条数或抽样明细",
        }[name]
        expect = {
            "入口可达": f"1、成功打开{l6}\n2、无整页白屏",
            "权限控制": "1、无权限隐藏或明确提示\n2、有权限可进入",
            "加载态": "1、有加载反馈\n2、完成后展示内容或空态",
            "空数据态": "1、空态可读\n2、无伪造业务指标",
            "异常态": "1、可读错误\n2、页面不崩溃",
            "结果一致性": "1、汇总与明细一致或有说明",
        }[name]
        out.append(
            {
                "功能项": "通用质量属性",
                "子功能项": sub,
                "功能点": name,
                "测试内容": content,
                "前置条件": "1、系统正常；2、账号与权限已准备",
                "测试步骤": steps,
                "预期结果": expect,
                "优先级": pri,
                "页面": f"{l5}/{l6}",
                "kind": "generic",
            }
        )
    return out


def expand_biz_atoms(atoms: list[dict], l5: str, l6: str, design: str, need: int) -> list[dict]:
    """Expand business atoms to `need` with design-derived extras (not generic)."""
    seen = set()
    uniq = []
    for a in atoms:
        k = a["功能点"]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(a)

    extras = [
        ("主界面布局", "页面结构", f"核验{l6}主工作区含筛选/结果/图表或列表等核心区块"),
        ("默认进入态", "初始状态", f"首次进入{l6}有默认条件或引导，非空白无提示"),
        ("条件摘要", "当前条件可读", "已选条件/对象/时间在页面有摘要展示"),
        ("重新计算", "参数变更刷新", "修改关键参数后可重新计算并刷新结果"),
        ("对象选择", "分析对象选择", "可选择企业/区域/产业等分析对象并生效"),
        ("多选对比", "多对象对比入口", "支持选择多个对象进入对比（若设计含对比）"),
        ("明细下钻", "从汇总到明细", "点击统计/节点可下钻到明细列表或详情"),
        ("返回保留", "上下文保留", "从详情返回后筛选与分页上下文可解释保留"),
        ("指标卡", "关键指标展示", "页面展示与本模块相关的关键指标卡/得分数值"),
        ("图例可读", "可视化图例", "图表有图例/轴标签，含义可辨"),
        ("排序切换", "结果排序", "列表或排名支持按关键字段排序"),
        ("分页浏览", "列表分页", "结果超一页时可分页且页码正确"),
        ("搜索定位", "关键词检索", "有搜索时可用关键词定位对象"),
        ("导出入口", "结果导出", "有导出则可用或给出权限/上限提示"),
        ("报告打开", "分析报告", "可打开/生成与本模块相关的报告结构"),
        ("本地化口径", "区域聚焦", "涉及深圳/区域时，地域口径在界面可辨"),
        ("模型说明", "评价模型可读", "模型/指标构成有说明入口或评审态说明"),
        ("推荐依据", "推荐理由", "推荐类结果附带依据或关键指标"),
        ("风险提示", "瓶颈/风险标识", "识别类结果对堵点/风险有标识与说明"),
        ("时间维度", "时间范围", "支持时间范围时切换后结果刷新"),
        ("产业维度", "产业选择", "支持产业选择时切换后结果刷新"),
        ("类型标签", "类型过滤", "类型标签过滤生效且可清除"),
        ("地图或区域", "空间呈现", "含地理维度时有地图/区域列表呈现"),
        ("节点详情", "节点信息面板", "图谱/流程节点点击后出现详情信息"),
        ("横向对标", "区域对标", "对标分析展示对比对象与差异"),
        ("清单操作", "名单可用性", "推荐/筛选名单可浏览、可进入对象"),
        ("权重生效", "自定义权重", "调整权重后得分变化可解释"),
        ("数据来源提示", "数据范围提示", "页面提示数据范围或更新时间（若有）"),
    ]

    # design UI hints as atoms
    for h in extract_ui_hints(design):
        extras.insert(0, (h[:16], "设计方案界面要点", f"[设计] {h}"))

    i = 0
    while len(uniq) < need and i < len(extras) * 3:
        name, sub, content = extras[i % len(extras)]
        i += 1
        fp = name if name not in seen else f"{name}-{i}"
        if fp in seen:
            continue
        seen.add(fp)
        uniq.append(
            {
                "功能项": l6 if l6 != "/" else l5,
                "子功能项": sub,
                "功能点": fp[:40],
                "测试内容": content.format(l5=l5, l6=l6) if "{l6}" in content else content,
                "source": content,
                "kind": "biz",
            }
        )
    return uniq[:need]


def allocate_non_generic(n_modules: int, weights: list[int]) -> list[int]:
    """Distribute TARGET_NON_GENERIC across modules by weight (desc+design length)."""
    total_w = sum(max(1, w) for w in weights) or n_modules
    base = [max(15, int(TARGET_NON_GENERIC * max(1, w) / total_w)) for w in weights]
    # clamp 15-30 then fix sum
    base = [min(30, max(15, x)) for x in base]
    s = sum(base)
    # adjust to target
    i = 0
    while s < TARGET_NON_GENERIC and i < 10000:
        idx = i % n_modules
        if base[idx] < 30:
            base[idx] += 1
            s += 1
        i += 1
    while s > TARGET_NON_GENERIC and i < 20000:
        idx = i % n_modules
        if base[idx] > 15:
            base[idx] -= 1
            s -= 1
        i += 1
    return base


def build_cases(items: list[dict], design_index: dict) -> dict:
    """Return {l4: [cases...]}"""
    groups = defaultdict(list)
    for it in items:
        groups[(it["l4"], it["l5"], it["l6"])].append(it)

    # prepare weights
    keys = sorted(groups.keys(), key=lambda x: (L4_TARGETS.index(x[0]), x[1], x[2]))
    weights = []
    meta = []
    for l4, l5, l6 in keys:
        rows = groups[(l4, l5, l6)]
        desc = "；".join(r["desc"] for r in rows if r["desc"])
        design = lookup_design(design_index, l5, l6)
        weights.append(len(desc) + len(design) // 2 + 40)
        meta.append((l4, l5, l6, desc, design))

    quotas = allocate_non_generic(len(meta), weights)
    by_l4 = defaultdict(list)

    for (l4, l5, l6, desc, design), need in zip(meta, quotas):
        atoms = []
        atoms.extend(atoms_from_text(desc, l5, l6, "需规"))
        if design:
            # use first ~800 chars of design for atom extraction to avoid explosion, plus full for hints
            atoms.extend(atoms_from_text(design[:1200], l5, l6, "设计"))
        atoms = expand_biz_atoms(atoms, l5, l6, design, need)

        for idx, a in enumerate(atoms):
            a["优先级"] = "P0" if idx < 5 else ("P1" if idx < 14 else "P2")
            case = enrich_case(a, l5, l6, design)
            by_l4[l4].append(case)

        for g in generic_cases(l5, l6):
            by_l4[l4].append(g)

    # assign IDs per l4
    result = {}
    for l4 in L4_TARGETS:
        cases = by_l4.get(l4, [])
        numbered = []
        for i, c in enumerate(cases, 1):
            numbered.append(
                {
                    "用例编号": f"{PLATE}-{SYSTEM}-{VERSION}-{TEST_TYPE}-{i:05d}",
                    "功能模块": c["页面"].split("/")[0] if "/" in c["页面"] else "",
                    "子功能模块": c["页面"].split("/")[1] if "/" in c["页面"] else "",
                    "功能项": c["功能项"],
                    "子功能项": c["子功能项"],
                    "页面": c["页面"],
                    "功能点": c["功能点"],
                    "测试内容": c["测试内容"],
                    "前置条件": c["前置条件"],
                    "测试步骤": c["测试步骤"],
                    "预期结果": c["预期结果"],
                    "优先级": c["优先级"],
                    "是否通过": "",
                    "测试工程师": "",
                    "测试时间": "",
                    "审核员": "",
                    "测试截图": "",
                    "kind": c["kind"],
                }
            )
        # fix 功能模块/子功能模块 from page
        for c in numbered:
            parts = c["页面"].split("/", 1)
            c["功能模块"] = parts[0]
            c["子功能模块"] = parts[1] if len(parts) > 1 else "/"
        result[l4] = numbered
    return result


def write_workbook(l4: str, cases: list[dict], out_path: Path):
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    ws["A1"] = f"智能服务集群-科技专题服务系统测试用例（{L3}-{l4}）·v1.1"
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    headers = [
        "用例编号", "功能模块", "子功能模块", "功能项", "子功能项", "页面", "功能点",
        "测试内容", "前置条件", "测试步骤", "预期结果", "优先级", "是否通过",
        "测试工程师", "测试时间", "审核员", "测试截图",
    ]
    align = Alignment(wrap_text=True, vertical="top")
    for i, case in enumerate(cases, start=3):
        for col, key in enumerate(headers, start=1):
            cell = ws.cell(i, col, case.get(key, ""))
            cell.alignment = align
    for sheet_name in ["兼容性测试用例", "集成测试用例", "性能测试用例"]:
        if sheet_name not in wb.sheetnames:
            continue
        wso = wb[sheet_name]
        if wso["A1"].value and "测试用例" in str(wso["A1"].value):
            wso["A1"] = f"智能服务集群-科技专题服务系统{sheet_name}（{L3}-{l4}）·v1.1"
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    wb.close()


def main():
    items = load_function_tree()
    design_index = parse_bid_design()
    print(f"function leaves={len(items)}, design titles={len(design_index)}")
    # sample match
    for sample in ["产业与企业类型筛选", "产业链全景图谱", "深圳政策对标"]:
        print(" match", sample, "->", "YES" if norm(sample) in design_index else "NO",
              "body", len(design_index.get(norm(sample), {}).get("body", "")))

    by_l4 = build_cases(items, design_index)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = non_g = gen = 0
    print(f"{'四级':<12}{'用例':>6}{'非通用':>8}{'通用':>6}")
    for l4 in L4_TARGETS:
        cases = by_l4[l4]
        ng = sum(1 for c in cases if c["kind"] != "generic")
        g = len(cases) - ng
        total += len(cases)
        non_g += ng
        gen += g
        out = OUT_DIR / f"6.国际科技信息中心项目_{l4}_测试用例.xlsx"
        # strip kind before write already not in headers
        write_workbook(l4, cases, out)
        print(f"{l4:<12}{len(cases):>6}{ng:>8}{g:>6} -> {out.name}")

    print(f"{'合计':<12}{total:>6}{non_g:>8}{gen:>6}")
    print(f"target non≈{TARGET_NON_GENERIC}, total≈{TARGET_TOTAL}")

    readme = OUT_DIR / "README.md"
    readme.write_text(
        f"""# 科技专题战略分析 · 总集功能测试用例 v1.1

> 基于 v1.0 复制扩展；非通用用例扩至约 {non_g}，总用例 {total}（含通用质量属性 {gen}）  
> 描述完善：功能清单「需规功能描述」全覆盖 + `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2  
> 编号：`ZNFWJQ-KJZTFWXT-v1.0-FUNC-#####`（每四级文件独立起编）  
> 生成：`agent-delivery/scripts/_gen_zt_testcases_v11.py`

| 四级功能 | 用例数 | 非通用 | 通用 |
|----------|--------|--------|------|
"""
        + "\n".join(
            f"| {l4} | {len(by_l4[l4])} | {sum(1 for c in by_l4[l4] if c['kind']!='generic')} | {sum(1 for c in by_l4[l4] if c['kind']=='generic')} |"
            for l4 in L4_TARGETS
        )
        + f"\n| **合计** | **{total}** | **{non_g}** | **{gen}** |\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
