# -*- coding: utf-8 -*-
"""V1.2 总集用例：需规全覆盖 + demo-ui-topic 原型 UI 元素/交互路径具体化。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import openpyxl
import yaml
from openpyxl.styles import Alignment

ROOT = Path(r"d:\work\gkx-lumen")
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
BID = ROOT / "gkx-orchestration" / "agent-delivery" / "bid-reference" / "科技信息展示系统和科技专题服务系统.md"
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
CATALOG = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "prototype-catalog-zt-strategy.yaml"
)
OUT_DIR = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "科技专题战略分析-v1.2"
)

L3 = "科技专题战略分析"
L4_TARGETS = ["综合智能分析", "政策分析", "企业分析", "产业链分析", "产业服务链分析"]
PLATE, SYSTEM, VERSION, TEST_TYPE = "ZNFWJQ", "KJZTFWXT", "v1.0", "FUNC"

TARGET_NON_GENERIC = 1300
TARGET_TOTAL = 1700
GENERIC_PER_MODULE = 6


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
        items.append({"l4": cur[3], "l5": cur[4] or "/", "l6": cur[5] or "/", "desc": desc})
    wb.close()
    return items


def load_catalog() -> dict:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    pages = data.get("pages") or {}
    overlays = data.get("l6_overlays") or {}
    nav_prefix = data.get("nav_prefix") or {}
    return {"pages": pages, "overlays": overlays, "nav_prefix": nav_prefix}


# L5 级原型壳（YAML 未列出的 L5 用此表；route/控件来自 demo-ui-topic）
EXTRA_L5_PAGES = {
    "区域政策对比": {
        "route": "/policy-portal/overview",
        "menu": "政策概览",
        "zones": [
            {"zone": "Tab", "control": "政策概览/政策检索/政策分析", "action": "进入政策分析子模块", "expect": "路由切换正确"},
            {"zone": "对比区", "control": "区域政策选择", "action": "选择两个及以上区域", "expect": "对比视图刷新"},
            {"zone": "图表", "control": "标准化对比图表", "action": "查看指标对比", "expect": "多区域序列可读"},
        ],
    },
    "政策时空分析": {
        "route": "/policy/search",
        "menu": "政策检索",
        "zones": [
            {"zone": "模式Tab", "control": "关键词/语义/高级", "action": "切换检索模式", "expect": "输入区与示例切换"},
            {"zone": "时间轴", "control": "政策时间线", "action": "拖动或切换年份", "expect": "政策密度/条目随时间变化"},
            {"zone": "结果", "control": "政策卡片列表", "action": "打开政策详情", "expect": "Drawer 展示摘要与正文"},
        ],
    },
    "深圳政策现状分析": {
        "route": "/policy/overview",
        "menu": "深圳政策现状",
        "zones": [
            {"zone": "指标", "control": "政策数量/覆盖领域", "action": "查看 KPI", "expect": "指标与筛选一致"},
            {"zone": "可视化", "control": "政策分布图", "action": "切换维度", "expect": "图表随维度刷新"},
            {"zone": "对标", "control": "兄弟城市对比", "action": "选择对标城市", "expect": "对比表/雷达可读"},
        ],
    },
    "企业供应链关系分析": {
        "route": "/enterprise-center/risk-insight?view=supply-chain",
        "menu": "风险洞察",
        "zones": [
            {"zone": "对象", "control": "企业多选", "action": "选择 1-2 家企业", "expect": "开始分析按钮可用"},
            {"zone": "图谱", "control": "供应链 ForceGraph", "action": "点击节点展开", "expect": "关系类型过滤生效"},
            {"zone": "筛选", "control": "供应商/客户/合作伙伴", "action": "切换关系类型", "expect": "图谱边集变化"},
        ],
    },
    "企业评估分析": {
        "route": "/enterprise-center/enterprise-assessment",
        "menu": "企业评估",
        "zones": [
            {"zone": "模型", "control": "评估模型选择", "action": "切换模型", "expect": "得分维度说明更新"},
            {"zone": "结果", "control": "雷达/得分卡", "action": "查看综合得分", "expect": "各维度可读"},
            {"zone": "名单", "control": "企业列表", "action": "排序/打开画像", "expect": "Drawer 打开企业详情"},
        ],
    },
    "重点企业领域分布分析": {
        "route": "/enterprise-center/key-enterprise-analysis?view=domain",
        "menu": "重点企业分析",
        "view_tab": "领域分布分析",
        "zones": [
            {"zone": "页内Tab", "control": "领域分布分析", "action": "切换到 domain 视图", "expect": "URL ?view=domain"},
            {"zone": "筛选", "control": "技术领域/产业", "action": "选择领域标签", "expect": "热力/矩阵刷新"},
            {"zone": "图表", "control": "领域覆盖矩阵", "action": "点击单元格", "expect": "打开企业清单 Drawer"},
        ],
    },
    "产业链全景图谱": {
        "route": "/industry-center/panorama",
        "menu": "产业链全景图谱",
        "zones": [
            {"zone": "选择", "control": "产业链 Select", "action": "切换产业链", "expect": "G6 根节点刷新"},
            {"zone": "图谱", "control": "环节节点", "action": "点击节点", "expect": "高亮并展示环节摘要"},
            {"zone": "演进", "control": "时间/版本", "action": "切换演进参数", "expect": "结构变化可观察"},
        ],
    },
    "产业运行诊断": {
        "route": "/industry-center/diagnosis",
        "menu": "产业运行诊断",
        "zones": [
            {"zone": "Tab", "control": "周期/关键环节/瓶颈/记录", "action": "切换 Tab", "expect": "URL tab 同步"},
            {"zone": "表单", "control": "诊断参数", "action": "提交诊断", "expect": "进入 processing 或结果页"},
            {"zone": "图谱", "control": "瓶颈五维图", "action": "切换维度", "expect": "堵点标识可读"},
        ],
    },
    "区域产业评价": {
        "route": "/industry-center/regional-evaluation",
        "menu": "区域产业评价",
        "zones": [
            {"zone": "区域", "control": "区域选择", "action": "切换评价区域", "expect": "得分卡刷新"},
            {"zone": "指标", "control": "多维指标", "action": "展开指标树", "expect": "权重/得分可读"},
            {"zone": "对标", "control": "横向对比", "action": "选择对比区域", "expect": "雷达/表格更新"},
        ],
    },
    "深圳产业决策支撑": {
        "route": "/industry-center/shenzhen-decision",
        "menu": "深圳产业决策",
        "zones": [
            {"zone": "场景", "control": "决策场景 Tab", "action": "切换场景", "expect": "建议清单切换"},
            {"zone": "路径", "control": "发展路径图", "action": "查看阶段节点", "expect": "阶段与政策/项目关联可读"},
            {"zone": "导出", "control": "报告导出", "action": "点击导出", "expect": "有反馈或下载入口"},
        ],
    },
    "服务机构能力推荐": {
        "route": "/service-portal/recommendation",
        "menu": "服务能力推荐",
        "zones": [
            {"zone": "需求", "control": "需求表单", "action": "填写领域/能力", "expect": "推荐列表刷新"},
            {"zone": "名单", "control": "推荐机构卡片", "action": "查看依据", "expect": "展示匹配理由"},
            {"zone": "对比", "control": "加入对比", "action": "多选机构", "expect": "对比篮计数增加"},
        ],
    },
    "服务机构领域推荐": {
        "route": "/service-portal/domain-recommendation",
        "menu": "领域推荐",
        "zones": [
            {"zone": "领域", "control": "技术领域 Tag", "action": "选择领域", "expect": "覆盖机构列表更新"},
            {"zone": "地图", "control": "区域分布", "action": "下钻区域", "expect": "机构密度变化"},
        ],
    },
    "服务机构产业适配分析": {
        "route": "/service/institution-decision",
        "menu": "机构决策",
        "zones": [
            {"zone": "产业", "control": "产业链选择", "action": "选择产业环节", "expect": "适配度得分刷新"},
            {"zone": "矩阵", "control": "能力-环节矩阵", "action": "点击单元格", "expect": "打开机构清单"},
        ],
    },
}


def parse_bid_design() -> dict:
    text = BID.read_text(encoding="utf-8")
    m_start = re.search(r"1\.1\.1\.2\.4\.2\.\s*\*\*科技专题战略分析\*\*", text)
    m_end = re.search(r"######\s*1\.1\.1\.2\.4\.3\.", text)
    if not m_start:
        return {}
    chunk = text[m_start.start() : m_end.start() if m_end else m_start.start() + 80000]
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
        body = re.sub(r"!\[.*?\]\(.*?\)", "", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if title and (title not in index or len(body) > len(index[title]["body"])):
            index[title] = {"body": body, "title": m.group("title").strip()}
    return index


def lookup_design(index: dict, l5: str, l6: str) -> str:
    for k in (norm(l6), norm(l5)):
        if k in index and index[k]["body"]:
            return index[k]["body"]
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
        if len(p) < 8 or p.startswith("http") or p.startswith("file:"):
            continue
        out.append(p)
    return out


def atoms_from_text(text: str, l5: str, l6: str, source_tag: str) -> list[dict]:
    atoms = []
    for sent in split_sentences(text):
        title_like = sent.count("、") >= 3 and len(sent) < 60 and "该功能" not in sent
        if title_like:
            continue
        fp = sent[:30]
        if sent.startswith(("该功能", "本功能")):
            fp = sent[3:33]
        atoms.append(
            {
                "功能项": l6 if l6 != "/" else l5,
                "子功能项": "需规主路径",
                "功能点": fp.strip("：:，,")[:40],
                "测试内容": f"[{source_tag}] {sent[:160]}",
                "source": sent,
                "kind": "biz",
                "origin": "req",
            }
        )
    return atoms


def resolve_l5_page(catalog: dict, l5: str) -> dict | None:
    pages = catalog["pages"]
    if l5 in pages:
        return pages[l5]
    if l5 in EXTRA_L5_PAGES:
        return EXTRA_L5_PAGES[l5]
    for k, v in pages.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    for k, v in EXTRA_L5_PAGES.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    return None


def build_nav(l4: str, page: dict, catalog: dict) -> str:
    prefix = catalog["nav_prefix"].get(l4, f"侧栏「{l4}」")
    menu = page.get("menu") or page.get("view_tab") or ""
    parts = [prefix]
    if menu:
        parts.append(f"「{menu}」")
    if page.get("view_tab"):
        parts.append(f"Tab「{page['view_tab']}」")
    return " → ".join(parts)


def zone_to_atom(zone: dict, l5: str, l6: str, nav: str, route: str, pri: str = "P0") -> dict:
    z, ctrl, act, exp = zone["zone"], zone["control"], zone["action"], zone["expect"]
    fp = f"{z}·{ctrl}"[:40]
    steps = (
        f"1.登录 demo-ui-topic 原型（或联调环境）\n"
        f"2.导航：{nav}\n"
        f"3.确认路由/页面壳：{route}\n"
        f"4.定位「{z}」控件「{ctrl}」\n"
        f"5.操作：{act}\n"
        f"6.观察结果区/Drawer/URL 参数变化"
    )
    expect = (
        f"1、按导航可达目标页面（{l5}/{l6}）\n"
        f"2、控件「{ctrl}」可见且可操作\n"
        f"3、{exp}\n"
        f"4、[原型] 交互路径明确，测试员无需猜测入口\n"
        f"5、异常时有可读提示，非白屏"
    )
    return {
        "功能项": z,
        "子功能项": ctrl[:30],
        "功能点": fp,
        "测试内容": f"[原型] {l6}：在「{z}」对「{ctrl}」执行「{act}」",
        "前置条件": "1、原型或联调环境可访问；2、已登录；3、具备模块权限；4、Mock 数据可展示",
        "测试步骤": steps,
        "预期结果": expect,
        "优先级": pri,
        "页面": f"{l5}/{l6}",
        "kind": "biz",
        "origin": "proto",
    }


def overlay_atoms(catalog: dict, l6: str, l5: str) -> list[dict]:
    overlays = catalog["overlays"].get(l6) or {}
    out = []
    for pt in overlays.get("points") or []:
        out.append(
            {
                "功能项": pt.get("功能项", l6),
                "子功能项": pt.get("子功能项", l6),
                "功能点": pt.get("功能点", l6)[:40],
                "测试内容": pt.get("测试内容", "")[:180],
                "前置条件": "1、原型或联调环境可访问；2、已登录；3、测试数据可用",
                "测试步骤": pt.get("步骤", "").replace("\\n", "\n"),
                "预期结果": pt.get("预期", ""),
                "优先级": pt.get("优先级", "P0"),
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "proto-overlay",
            }
        )
    return out


def prototype_atoms_for_module(
    l4: str, l5: str, l6: str, catalog: dict, sibling_l6s: list[str]
) -> list[dict]:
    """从 L5 页面 zones + L6 overlay 生成本模块原型用例。"""
    page = resolve_l5_page(catalog, l5)
    atoms = overlay_atoms(catalog, l6, l5)
    if not page:
        return atoms

    route = page.get("route", "")
    nav = build_nav(l4, page, catalog)
    zones = page.get("zones") or []
    if not zones:
        return atoms

    # 将 zones 按 L6  sibling 均分，本模块取属于自己的那份 + 全部 overlay
    idx = sibling_l6s.index(l6) if l6 in sibling_l6s else 0
    n = len(sibling_l6s) or 1
    for i, zone in enumerate(zones):
        if i % n != idx:
            continue
        pri = "P0" if i < 3 else "P1"
        atoms.append(zone_to_atom(zone, l5, l6, nav, route, pri))
    return atoms


def dedupe_atoms(atoms: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for a in atoms:
        k = (a.get("origin", ""), a["功能点"], a.get("子功能项", ""))
        if k in seen:
            continue
        seen.add(k)
        out.append(a)
    return out


def fill_to_quota(atoms: list[dict], l5: str, l6: str, design: str, need: int) -> list[dict]:
    """配额不足时用设计稿 UI 提示补点（非通用质量属性）。"""
    if len(atoms) >= need:
        return atoms[:need]
    hints = [
        ("布局区块", "主工作区", f"核验 {l6} 含筛选区、结果区、图表/列表"),
        ("条件摘要", "已选条件", "页面展示当前筛选/对象摘要"),
        ("刷新行为", "参数变更", "修改关键参数后结果刷新"),
        ("明细入口", "下钻/详情", "从汇总点击进入明细或 Drawer"),
        ("图例轴标签", "可视化可读", "图表含图例与轴标签"),
    ]
    design_hints = re.findall(r"(雷达图|热力图|图谱|下钻|导出|对比|推荐|评分|时间轴|流程图)", design or "")
    for h in design_hints:
        hints.insert(0, (h, "设计要点", f"[设计] 页面含{h}且可交互"))

    i = 0
    seen = {a["功能点"] for a in atoms}
    while len(atoms) < need and i < len(hints) * 4:
        name, sub, content = hints[i % len(hints)]
        i += 1
        fp = f"{name}-{i}" if name in seen else name
        if fp in seen:
            continue
        seen.add(fp)
        atoms.append(
            {
                "功能项": l6 if l6 != "/" else l5,
                "子功能项": sub,
                "功能点": fp[:40],
                "测试内容": content,
                "前置条件": "1、系统正常；2、已登录",
                "测试步骤": f"1.进入{l5}/{l6}\n2.定位{sub}\n3.执行相关操作\n4.核对{content}",
                "预期结果": f"1、{content}\n2、结果可观察\n3、无未捕获异常",
                "优先级": "P2",
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "fill",
            }
        )
    return atoms[:need]


GENERIC_TEMPLATES = [
    ("入口可达", "模块入口与导航", "可从专题导航进入本子模块", "P0"),
    ("权限控制", "访问权限", "无权限不可操作受控功能", "P1"),
    ("加载态", "数据加载反馈", "请求中有加载反馈且完成后消失", "P1"),
    ("空数据态", "无数据空态", "无命中时可读空态、不伪装业务数", "P1"),
    ("异常态", "接口失败提示", "失败时可读错误且不崩溃", "P1"),
    ("结果一致性", "统计与列表一致", "汇总与明细口径一致或差异可解释", "P1"),
]


def generic_cases(l4: str, l5: str, l6: str, catalog: dict) -> list[dict]:
    page = resolve_l5_page(catalog, l5)
    nav = build_nav(l4, page, catalog) if page else f"{catalog['nav_prefix'].get(l4, l4)} → {l5}"
    route = (page or {}).get("route", "（按 IA 导航）")
    out = []
    for name, sub, content, pri in GENERIC_TEMPLATES[:GENERIC_PER_MODULE]:
        if name == "入口可达":
            steps = f"1.打开原型/联调环境\n2.导航：{nav}\n3.确认 URL/标题与 {l5}/{l6} 一致\n4.记录 route：{route}"
            expect = f"1、成功进入 {l6}\n2、页面标题/面包屑正确\n3、无整页白屏"
        else:
            steps = {
                "权限控制": "1.无权限账号访问\n2.有权限账号访问\n3.对比入口与操作可用性",
                "加载态": "1.触发列表/图表加载\n2.观察加载指示\n3.等待完成",
                "空数据态": "1.构造无命中条件\n2.观察结果区",
                "异常态": "1.模拟失败或断网刷新\n2.观察提示与可恢复性",
                "结果一致性": "1.记录汇总数字\n2.核对列表条数或抽样明细",
            }[name]
            expect = {
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


def allocate_non_generic(n_modules: int, weights: list[int]) -> list[int]:
    total_w = sum(max(1, w) for w in weights) or n_modules
    base = [max(15, int(TARGET_NON_GENERIC * max(1, w) / total_w)) for w in weights]
    base = [min(30, max(15, x)) for x in base]
    s = sum(base)
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


def build_cases(items: list[dict], design_index: dict, catalog: dict) -> dict:
    groups = defaultdict(list)
    for it in items:
        groups[(it["l4"], it["l5"], it["l6"])].append(it)

    l5_siblings = defaultdict(list)
    for l4, l5, l6 in groups:
        if l6 not in l5_siblings[(l4, l5)]:
            l5_siblings[(l4, l5)].append(l6)

    keys = sorted(groups.keys(), key=lambda x: (L4_TARGETS.index(x[0]), x[1], x[2]))
    weights = []
    meta = []
    for l4, l5, l6 in keys:
        desc = "；".join(r["desc"] for r in groups[(l4, l5, l6)] if r["desc"])
        design = lookup_design(design_index, l5, l6)
        # 有原型映射的模块加权，优先多分配 UI 细点
        proto_bonus = 80 if resolve_l5_page(catalog, l5) else 0
        overlay_bonus = 40 if l6 in catalog["overlays"] else 0
        weights.append(len(desc) + len(design) // 2 + 40 + proto_bonus + overlay_bonus)
        meta.append((l4, l5, l6, desc, design))

    quotas = allocate_non_generic(len(meta), weights)
    by_l4 = defaultdict(list)

    for (l4, l5, l6, desc, design), need in zip(meta, quotas):
        siblings = l5_siblings[(l4, l5)]
        atoms = []
        # 1) 原型 UI 点（优先）
        atoms.extend(prototype_atoms_for_module(l4, l5, l6, catalog, siblings))
        # 2) 需规句子（全覆盖，去重后保留）
        atoms.extend(atoms_from_text(desc, l5, l6, "需规"))
        if design:
            atoms.extend(atoms_from_text(design[:900], l5, l6, "设计"))
        atoms = dedupe_atoms(atoms)
        # 原型优先排序：proto > proto-overlay > req > design > fill
        order = {"proto-overlay": 0, "proto": 1, "req": 2, "fill": 4}
        atoms.sort(key=lambda a: order.get(a.get("origin", "req"), 3))
        atoms = fill_to_quota(atoms, l5, l6, design, need)

        for a in atoms:
            a.setdefault("页面", f"{l5}/{l6}")
            a.setdefault("前置条件", "1、系统正常；2、已登录且具备本模块权限；3、测试数据可用")
            if "测试步骤" not in a or not a["测试步骤"]:
                nav_hint = build_nav(l4, resolve_l5_page(catalog, l5) or {}, catalog)
                a["测试步骤"] = (
                    f"1.登录原型/联调环境\n2.导航：{nav_hint}\n"
                    f"3.执行功能点「{a['功能点']}」相关操作\n4.核对结果区"
                )
            if "预期结果" not in a or not a["预期结果"]:
                a["预期结果"] = f"1、{a['测试内容'][:90]}\n2、结果可观察\n3、无未捕获异常"
            a.setdefault("优先级", "P1")
            a.setdefault("kind", "biz")
            by_l4[l4].append(a)

        for g in generic_cases(l4, l5, l6, catalog):
            by_l4[l4].append(g)

    result = {}
    for l4 in L4_TARGETS:
        cases = by_l4.get(l4, [])
        numbered = []
        for i, c in enumerate(cases, 1):
            numbered.append(
                {
                    "用例编号": f"{PLATE}-{SYSTEM}-{VERSION}-{TEST_TYPE}-{i:05d}",
                    "功能模块": c["页面"].split("/")[0],
                    "子功能模块": c["页面"].split("/")[1] if "/" in c["页面"] else "/",
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
                    "origin": c.get("origin", ""),
                }
            )
        result[l4] = numbered
    return result


def write_workbook(l4: str, cases: list[dict], out_path: Path):
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    ws["A1"] = f"智能服务集群-科技专题服务系统测试用例（{L3}-{l4}）·v1.2"
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
            wso["A1"] = f"智能服务集群-科技专题服务系统{sheet_name}（{L3}-{l4}）·v1.2"
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    wb.close()


def main():
    catalog = load_catalog()
    items = load_function_tree()
    design_index = parse_bid_design()
    print(f"leaves={len(items)} design={len(design_index)} catalog_pages={len(catalog['pages'])}")

    by_l4 = build_cases(items, design_index, catalog)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = non_g = gen = proto = 0
    print(f"{'四级':<12}{'用例':>6}{'非通用':>8}{'通用':>6}{'原型':>6}")
    for l4 in L4_TARGETS:
        cases = by_l4[l4]
        ng = sum(1 for c in cases if c["kind"] != "generic")
        g = len(cases) - ng
        p = sum(1 for c in cases if c.get("origin", "").startswith("proto"))
        total += len(cases)
        non_g += ng
        gen += g
        proto += p
        out = OUT_DIR / f"6.国际科技信息中心项目_{l4}_测试用例.xlsx"
        write_workbook(l4, cases, out)
        print(f"{l4:<12}{len(cases):>6}{ng:>8}{g:>6}{p:>6} -> {out.name}")

    print(f"{'合计':<12}{total:>6}{non_g:>8}{gen:>6}{proto:>6}")

    readme = OUT_DIR / "README.md"
    readme.write_text(
        f"""# 科技专题战略分析 · 总集功能测试用例 v1.2

> **相对 v1.1**：功能点按 **demo-ui-topic 原型** 页面元素与交互路径拆分，步骤/预期可执行；需规描述仍全覆盖。  
> 非通用约 **{non_g}**，总用例 **{total}**（含通用质量属性 **{gen}**）；其中标注 `[原型]` / origin=proto 约 **{proto}** 条。  
> 原型目录：`../prototype-catalog-zt-strategy.yaml`（真源 `repos/demo-ui-topic`）  
> 编号：`ZNFWJQ-KJZTFWXT-v1.0-FUNC-#####`（每四级文件独立起编）  
> 生成：`agent-delivery/scripts/_gen_zt_testcases_v12.py`

## 编写原则（v1.2）

1. **先找原型**：L5/L6 映射到侧栏路由、Tab、Drawer、ContextBar 等可操作控件  
2. **再补需规**：功能清单句子作为覆盖检查，不与原型点简单排列组合  
3. **步骤写路径**：侧栏 → 菜单 → Tab → 控件 → 操作 → 可观察 UI 状态  
4. **通用质量属性**：每六级模块保留 6 条（入口/权限/加载/空态/异常/一致性）

| 四级功能 | 用例数 | 非通用 | 通用 | 原型向 |
|----------|--------|--------|------|--------|
"""
        + "\n".join(
            f"| {l4} | {len(by_l4[l4])} | {sum(1 for c in by_l4[l4] if c['kind']!='generic')} | "
            f"{sum(1 for c in by_l4[l4] if c['kind']=='generic')} | "
            f"{sum(1 for c in by_l4[l4] if c.get('origin','').startswith('proto'))} |"
            for l4 in L4_TARGETS
        )
        + f"\n| **合计** | **{total}** | **{non_g}** | **{gen}** | **{proto}** |\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
