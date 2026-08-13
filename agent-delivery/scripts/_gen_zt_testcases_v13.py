# -*- coding: utf-8 -*-
"""V1.3 总集用例：功能清单定数量；八件套出要点；冲突以 demo-ui-topic 原型为准。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import openpyxl
import yaml
from openpyxl.styles import Alignment

ROOT = Path(r"d:\work\gkx-lumen")
ORCH = ROOT / "gkx-orchestration" / "agent-delivery"
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
BID = ORCH / "bid-reference" / "科技信息展示系统和科技专题服务系统.md"
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
QA_DIR = ORCH / "qa" / "total-set" / "KJZTFWXT"
CATALOG = QA_DIR / "prototype-catalog-zt-strategy.yaml"
PACK_INDEX = QA_DIR / "product-pack-index-zt-strategy.yaml"
PACK_ROOT = ORCH / "agent-handoffs" / "产品整体定义"
OUT_DIR = QA_DIR / "科技专题战略分析-v1.3"
# 企业分析 xlsx 若被占用，整包改写到 rev 目录
OUT_DIR_FALLBACK = QA_DIR / "科技专题战略分析-v1.3-rev"

L3 = "科技专题战略分析"
L4_TARGETS = ["综合智能分析", "政策分析", "企业分析", "产业链分析", "产业服务链分析"]
PLATE, SYSTEM, VERSION, TEST_TYPE = "ZNFWJQ", "KJZTFWXT", "v1.0", "FUNC"
TASK_ID = "QA-KJZTFWXT-STRATEGY-TOTALSET-L01"
BID_FILE = "科技信息展示系统和科技专题服务系统.md"
BID_CHAPTER = "1.1.1.2.4.2"
TIER = "DEMO"

TARGET_NON_GENERIC = 1300
GENERIC_PER_MODULE = 6

# 八件套与原型冲突时改写（仅生成器用；不写入用例正文）
PROTO_REWRITE = (
    (r"两个分析类型\s*Tab|分析类型\s*Tab|页内Tab「?类型与区域分析」?|默认选中[“\"]?类型与区域分析[”\"]?", "侧栏「重点企业类型分析」"),
    (r"切换到?[“\"]?领域分布分析[”\"]?\s*Tab|点击[“\"]?领域分布分析[”\"]?\s*Tab", "侧栏「重点企业领域分析」"),
    (r"进入[“\"]?重点企业分析[”\"]?，页面先显示两个分析类型", "从侧栏进入「重点企业类型分析」或「重点企业领域分析」"),
)

PRECOND = "1、测试环境可访问；2、已登录；3、具备本模块权限；4、测试数据可用"


def sanitize_text(text: str) -> str:
    """用例正文用业务语言；编写原则/技术实现细节不进步骤与预期。"""
    if not text:
        return ""
    s = str(text)
    repls = [
        (r"原型或联调环境可访问", "测试环境可访问"),
        (r"原型或联调可访问", "测试环境可访问"),
        (r"原型可访问", "测试环境可访问"),
        (r"打开原型/联调环境", "登录测试环境"),
        (r"登录\s*demo-ui-topic\s*原型（或联调环境）", "登录测试环境"),
        (r"登录\s*demo-ui-topic（或联调）", "登录测试环境"),
        (r"登录原型/联调环境", "登录测试环境"),
        (r"登录\s*demo-ui-topic[^\n]*", "登录测试环境"),
        (r"Mock\s*数据可展示", "测试数据可用"),
        (r"Mock\s*亦可?需有反馈", "有明确反馈"),
        (r"Mock\s*可展示", "测试数据可用"),
        (r"观察结果区/Drawer/URL", "观察结果区"),
        (r"观察结果区/侧滑详情/URL", "观察结果区"),
        (r"与八件套冲突时以原型为准[。；]?", ""),
        (r"与原型交互一致（冲突以原型为准）", ""),
        (r"与原型控件一致（冲突以原型为准）", ""),
        (r"（冲突以原型为准）", ""),
        (r"异常有可读提示，非白屏", ""),
        (r"无整页白屏", "页面正常展示"),
        (r"无白屏；?", ""),
        (r"非白屏", ""),
        (r"无未捕获异常", "结果可观察"),
        (r"对照 Design\.md §14", "对照页面实际展示"),
        (r"\[原型\]\s*", ""),
        (r"\[USM主路径\]\s*", ""),
        (r"\[USM-AC\]\s*", ""),
        (r"\[USM异常\]\s*", ""),
        (r"\[USM\]\s*", ""),
        (r"\[UX\]\s*", ""),
        (r"\[IA\]\s*", ""),
        (r"\[D8/D9\]\s*", ""),
        (r"\[需规\]\s*", ""),
        (r"\[设计\]\s*", ""),
        (r"ContextBar", "顶部筛选"),
        (r"Cascader", "级联选择"),
        (r"Checkbox", "复选框"),
        (r"\bRadio\b", "单选"),
        (r"\bTable\b", "列表"),
        (r"\bDrawer\b", "侧滑详情"),
        (r"ForceGraph", "关系图谱"),
        (r"\bG6\s*", ""),
        (r"MetricSpecCard", "指标说明"),
        (r"MetricCard", "指标卡"),
        (r"emptyGate", "未选对象提示"),
        (r"OrgPickerModal", "机构选择窗"),
        (r"StageDetailDrawer", "环节详情"),
        (r"analysis-rounded-tabs", "圆角分析页签"),
        (r"analysis-tabs", "分析页签"),
        (r"GEO_TARGET", "当前地理范围"),
        (r"enterprise_codes(?:\[\])?", "当前所选企业"),
        (r"Shell\s*", ""),
        (r"aria-current/?", ""),
        (r"\bdisabled\b", "不可用"),
        (r"workspace=type&view=type", "类型分析"),
        (r"workspace=domain&view=domain", "领域分析"),
        (r"workspace=[\w\-]+", "对应分析页"),
        (r"recommendation_tab=[\w\-]+", "对应推荐页签"),
        (r"\?tab=[\w\-]+", ""),
        (r"tab=[\w\-]+", "对应页签"),
        (r"URL\s*同步[^\n；。]*", "筛选与结果同步刷新"),
        (r"路由\s+/[^\s；。]+", "进入对应页面"),
        (r"确认路由/页面壳：[^\n]*", ""),
        (r"记录 route：[^\n]*", ""),
    ]
    for pat, repl in repls:
        s = re.sub(pat, repl, s)
    s = re.sub(r"(?m)^\s*\d+[\.、]\s*确认路由：[^\n]*\n?", "", s)
    s = re.sub(r"(?m)^\s*\d+[\.、]\s*路由：[^\n]*\n?", "", s)
    s = re.sub(r"(?m)^\s*\d+[\.、]\s*记录 route：[^\n]*\n?", "", s)
    s = re.sub(r"(?m)^\s*\d+[\.、]\s*确认 URL/标题[^\n]*\n?", "", s)
    s = re.sub(r"(?m)^\s*\d+[\.、]\s*$", "", s)
    s = re.sub(r"\n{3,}", "\n", s)
    return s.strip()


def renumber_lines(text: str) -> str:
    if not text:
        return ""
    out, n = [], 0
    for line in text.split("\n"):
        m = re.match(r"^(\s*)\d+([\.、])\s*(.*)$", line)
        if m and m.group(3).strip():
            n += 1
            out.append(f"{m.group(1)}{n}{m.group(2)}{m.group(3)}")
        elif line.strip():
            out.append(line)
    return "\n".join(out)


def sanitize_atom(a: dict) -> dict:
    for k in ("前置条件", "测试步骤", "预期结果", "测试内容", "功能项", "子功能项", "功能点"):
        if k in a and a[k]:
            a[k] = sanitize_text(str(a[k]))
    if a.get("测试步骤"):
        a["测试步骤"] = renumber_lines(a["测试步骤"])
    if a.get("预期结果"):
        a["预期结果"] = renumber_lines(a["预期结果"])
    if a.get("前置条件"):
        a["前置条件"] = renumber_lines(a["前置条件"].replace("；", "\n").replace(";", "\n"))
        # 前置保持一行分号风格
        parts = [re.sub(r"^\d+[\.、]\s*", "", x).strip(" ；;") for x in a["前置条件"].split("\n") if x.strip()]
        a["前置条件"] = "；".join(f"{i}、{p}" for i, p in enumerate(parts, 1) if p)
    return a


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
    return {
        "pages": data.get("pages") or {},
        "overlays": data.get("l6_overlays") or {},
        "nav_prefix": data.get("nav_prefix") or {},
    }


def load_pack_index() -> dict:
    data = yaml.safe_load(PACK_INDEX.read_text(encoding="utf-8"))
    return data.get("l5") or {}


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


def apply_proto_rewrite(text: str) -> str:
    out = text or ""
    for pat, repl in PROTO_REWRITE:
        out = re.sub(pat, repl, out)
    return out


def focus_hit(text: str, focus: list[str] | None) -> bool:
    if not focus:
        return True
    return any(k in (text or "") for k in focus)


def resolve_l5_page(catalog: dict, l5: str) -> dict | None:
    pages = catalog["pages"]
    if l5 in pages:
        return pages[l5]
    for k, v in pages.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    extra = EXTRA_L5_PAGES.get(l5)
    if extra:
        return extra
    for k, v in EXTRA_L5_PAGES.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    return None


def build_nav(l4: str, page: dict | None, catalog: dict) -> str:
    prefix = catalog["nav_prefix"].get(l4, f"侧栏「{l4}」")
    if not page:
        return prefix
    menu = page.get("menu") or ""
    parts = [prefix]
    if menu:
        parts.append(f"「{menu}」")
    return " → ".join(parts)


def base_trace(l5: str, l6: str, page: dict | None, extra: dict | None = None) -> dict:
    d = {
        "用户故事编号": "",
        "USM验收场景编号": "",
        "原始需求文件": BID_FILE,
        "原始需求章节号": BID_CHAPTER,
        "功能点ID": "",
        "TRACE引用": "",
        "路由route": (page or {}).get("route", ""),
        "交付口径tier": TIER,
        "关联任务ID": TASK_ID,
        "备注": "",
    }
    if extra:
        d.update({k: v for k, v in extra.items() if v})
    return d


def read_pack_texts(rel_dir: str) -> dict[str, tuple[str, str]]:
    """key → (filename, text)。"""
    folder = PACK_ROOT / rel_dir
    out: dict[str, tuple[str, str]] = {}
    if not folder.exists():
        return out
    for p in folder.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        name = p.name.upper()
        key = ""
        if name.startswith("USM"):
            key = "usm"
        elif name.startswith("TRACE"):
            key = "trace"
        elif name.startswith("IA-") or name.startswith("IA_"):
            key = "ia"
        elif name.startswith("UX-SPEC") or name.startswith("UX_SPEC"):
            key = "ux"
        elif name.startswith("WIRE"):
            key = "wire"
        elif "METRIC" in name:
            key = "metric"
        elif "GAP" in name or "DATA-GAP" in name:
            key = "gap"
        elif "FUNC" in name and "DESIGN" in name:
            key = "func"
        if not key or key in out:
            continue
        out[key] = (p.name, p.read_text(encoding="utf-8", errors="replace"))
    return out


def extract_trace_meta(text: str) -> dict:
    meta = {"route": "", "fp": "", "file": ""}
    if not text:
        return meta
    m = re.search(r"(?m)^\s*route:\s*[`'\"]?(/[^\s`'\"]+)", text)
    if not m:
        m = re.search(r"`(/[a-z0-9\-_/?.=&\[\]]+)`", text, re.I)
    if m:
        meta["route"] = m.group(1).split()[0]
    fps = re.findall(r"\b(E-\d{1,3}|P-\d{1,3}|DS-\d{1,3})\b", text)
    if fps:
        meta["fp"] = "/".join(dict.fromkeys(fps[:4]))
    return meta


def pack_atoms_from_usm(usm: str, fname: str, l5: str, l6: str, focus: list[str] | None, page, catalog, l4) -> list[dict]:
    atoms = []
    nav = build_nav(l4, page, catalog)
    route = (page or {}).get("route", "")
    # 用户故事
    for m in re.finditer(r"^###\s+(US-[\w-]+)\s+(.+)$", usm, re.M):
        uid, title = m.group(1), m.group(2).strip()
        after = usm[m.end() : m.end() + 400]
        para = re.split(r"\n\s*\n", after, maxsplit=1)[0].strip().replace("\n", "")
        blob = title + para
        if not focus_hit(blob + l5 + l6, focus) and not focus_hit(uid, focus):
            continue
        para = apply_proto_rewrite(para)
        atoms.append(
            {
                "功能项": "用户故事",
                "子功能项": uid,
                "功能点": title[:40],
                "测试内容": f"{uid} {title}：{para[:140]}",
                "前置条件": PRECOND,
                "测试步骤": (
                    f"1.登录测试环境\n2.导航：{nav}\n"
                    f"3.按「{title}」完成主任务\n4.观察结果区"
                ),
                "预期结果": f"1、{para[:140] or title}\n2、筛选条件不串用",
                "优先级": "P0",
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "usm-story",
                **base_trace(l5, l6, page, {"用户故事编号": uid, "TRACE引用": fname}),
            }
        )
    # 主路径 walkthrough 步骤
    for hm in re.finditer(r"^###\s+((?:主路径|路径)[^\n]*)\s*$", usm, re.M):
        htitle = hm.group(1).strip()
        nxt = usm.find("\n### ", hm.end())
        block = usm[hm.end() : nxt if nxt > 0 else None]
        if not focus_hit(htitle + block + l5, focus):
            continue
        steps = re.findall(r"^\d+\.\s+(.+)$", block, re.M)
        for i, step in enumerate(steps, 1):
            step = apply_proto_rewrite(step.strip())
            if len(step) < 8:
                continue
            atoms.append(
                {
                    "功能项": htitle[:20],
                    "子功能项": f"步骤{i}",
                    "功能点": step[:40],
                    "测试内容": f"{htitle} 第{i}步：{step[:140]}",
                    "前置条件": PRECOND,
                    "测试步骤": (
                        f"1.登录测试环境\n2.导航：{nav}\n"
                        f"3.执行：{step}\n4.观察结果区"
                    ),
                    "预期结果": f"1、{step[:140]}\n2、当前筛选与浏览位置保持不变",
                    "优先级": "P0" if i <= 4 else "P1",
                    "页面": f"{l5}/{l6}",
                    "kind": "biz",
                    "origin": "usm-walk",
                    **base_trace(l5, l6, page, {"USM验收场景编号": htitle, "TRACE引用": fname}),
                }
            )
    # 验收标准表
    ac_re = re.compile(
        r"^\|\s*([A-Z0-9][\w.-]+)\s*\|\s*([^|]*?)\s*\|\s*([^|]+?)\s*\|",
        re.M,
    )
    in_ac = False
    for line in usm.splitlines():
        if line.startswith("## ") and "验收" in line:
            in_ac = True
            continue
        if in_ac and line.startswith("## "):
            break
        if not in_ac:
            continue
        m = ac_re.match(line)
        if not m or m.group(1) in {"ID", ":---", "---"}:
            continue
        acid, usref, gwt = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if acid.lower() in {"id", "编号"}:
            continue
        blob = acid + usref + gwt
        if usref.strip().upper() != "ALL" and not focus_hit(blob + l5 + l6, focus):
            continue
        gwt = apply_proto_rewrite(gwt)
        us_ids = ",".join(re.findall(r"US-[\w./]+", usref)) or usref.strip()[:40]
        if usref.strip().upper() == "ALL":
            us_ids = "ALL"
        atoms.append(
            {
                "功能项": "验收标准",
                "子功能项": acid,
                "功能点": gwt[:40],
                "测试内容": f"{acid}（{usref}）：{gwt[:160]}",
                "前置条件": PRECOND,
                "测试步骤": (
                    f"1.登录测试环境\n2.导航：{nav}\n"
                    f"3.按验收要点执行：{gwt}\n4.观察结果区"
                ),
                "预期结果": f"1、{gwt}",
                "优先级": "P0",
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "usm-ac",
                **base_trace(
                    l5,
                    l6,
                    page,
                    {"用户故事编号": us_ids, "USM验收场景编号": acid, "TRACE引用": fname},
                ),
            }
        )
    # 异常路径表
    in_ex = False
    for line in usm.splitlines():
        if "异常" in line and line.startswith("## "):
            in_ex = True
            continue
        if in_ex and line.startswith("## "):
            break
        if not in_ex or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0] in {"场景", ":---", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        scene, behavior = cells[0], cells[1] if len(cells) > 1 else ""
        if not focus_hit(scene + behavior + l5, focus):
            continue
        behavior = apply_proto_rewrite(behavior)
        atoms.append(
            {
                "功能项": "异常路径",
                "子功能项": scene[:30],
                "功能点": (scene + "·" + behavior)[:40],
                "测试内容": f"{scene}：{behavior[:120]}",
                "前置条件": "1、测试环境可访问；2、已登录；3、可构造该异常条件",
                "测试步骤": f"1.登录测试环境\n2.导航：{nav}\n3.构造场景：{scene}\n4.观察结果区",
                "预期结果": f"1、{behavior}\n2、不伪造业务数据，用户仍可继续操作",
                "优先级": "P1",
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "usm-ex",
                **base_trace(l5, l6, page, {"TRACE引用": fname}),
            }
        )
    return atoms


def pack_atoms_from_ux_ia(text: str, fname: str, kind: str, l5: str, l6: str, focus, page, catalog, l4) -> list[dict]:
    if not text:
        return []
    atoms = []
    nav = build_nav(l4, page, catalog)
    route = (page or {}).get("route", "")
    tag = "UX" if kind == "ux" else "IA"
    for sent in split_sentences(text[:6000]):
        if not focus_hit(sent + l5 + l6, focus):
            continue
        if sent.startswith("#") or sent.startswith("|") or sent.startswith("- ["):
            continue
        if not re.search(r"(进入|点击|切换|筛选|打开|查看|下钻|对比|导出|空态|Drawer|Tab|地图|图谱)", sent):
            continue
        sent = apply_proto_rewrite(sent)
        atoms.append(
            {
                "功能项": tag,
                "子功能项": fname[:24],
                "功能点": sent[:40],
                "测试内容": sent[:160],
                "前置条件": PRECOND,
                "测试步骤": f"1.登录测试环境\n2.导航：{nav}\n3.按要点操作：{sent[:120]}\n4.观察结果区",
                "预期结果": f"1、{sent[:140]}",
                "优先级": "P1",
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": f"pack-{kind}",
                **base_trace(l5, l6, page, {"TRACE引用": fname}),
            }
        )
    return atoms[:20]


DESIGN14 = [
    ("筛选区不过宽", "顶部筛选", "顶部筛选区宽度适中，不遮挡主工作区", "P1"),
    ("分析页签样式", "分析页签", "二级分析页签为圆角样式，选中态可区分", "P1"),
    ("指标可查说明", "指标说明", "统计数字旁有说明入口，可查看口径", "P0"),
    ("评审标识不泄漏", "评审模式", "业务模式下不展示内部编号；评审标识仅评审模式可见", "P1"),
    ("侧滑可关闭", "侧滑详情", "侧滑详情可用关闭按钮关闭，关闭后页面条件保留", "P2"),
]


def design14_atoms(l5: str, l6: str, page, catalog, l4) -> list[dict]:
    nav = build_nav(l4, page, catalog)
    out = []
    for fp, sub, content, pri in DESIGN14:
        out.append(
            {
                "功能项": "界面规范",
                "子功能项": sub,
                "功能点": fp,
                "测试内容": content,
                "前置条件": PRECOND,
                "测试步骤": f"1.登录测试环境\n2.导航：{nav}\n3.检查：{content}\n4.观察结果区",
                "预期结果": f"1、{content}",
                "优先级": pri,
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "design14",
                **base_trace(l5, l6, page),
            }
        )
    return out


def atoms_from_text(text: str, l5: str, l6: str, source_tag: str, page=None) -> list[dict]:
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
                "子功能项": "需规主路径" if source_tag == "需规" else "设计要点",
                "功能点": fp.strip("：:，,")[:40],
                "测试内容": f"[{source_tag}] {sent[:160]}",
                "source": sent,
                "kind": "biz",
                "origin": "req" if source_tag == "需规" else "bid",
                **base_trace(l5, l6, page),
            }
        )
    return atoms


def zone_to_atom(zone: dict, l5: str, l6: str, nav: str, route: str, pri: str, page) -> dict:
    z, ctrl, act, exp = zone["zone"], zone["control"], zone["action"], zone["expect"]
    fp = f"{z}·{ctrl}"[:40]
    return {
        "功能项": z,
        "子功能项": ctrl[:30],
        "功能点": fp,
        "测试内容": f"{l6}：在「{z}」对「{ctrl}」执行「{act}」",
        "前置条件": PRECOND,
        "测试步骤": (
            f"1.登录测试环境\n2.导航：{nav}\n"
            f"3.在「{z}」找到「{ctrl}」\n4.操作：{act}\n5.观察结果区"
        ),
        "预期结果": (
            f"1、进入「{l5}」，可开展「{l6}」\n"
            f"2、「{ctrl}」可见且可操作\n3、{exp}"
        ),
        "优先级": pri,
        "页面": f"{l5}/{l6}",
        "kind": "biz",
        "origin": "proto",
        **base_trace(l5, l6, page),
    }


def overlay_atoms(catalog: dict, l6: str, l5: str, page) -> list[dict]:
    overlays = catalog["overlays"].get(l6) or {}
    out = []
    for pt in overlays.get("points") or []:
        out.append(
            {
                "功能项": pt.get("功能项", l6),
                "子功能项": pt.get("子功能项", l6),
                "功能点": pt.get("功能点", l6)[:40],
                "测试内容": pt.get("测试内容", "")[:180],
                "前置条件": PRECOND,
                "测试步骤": apply_proto_rewrite(pt.get("步骤", "").replace("\\n", "\n")),
                "预期结果": apply_proto_rewrite(pt.get("预期", "")),
                "优先级": pt.get("优先级", "P0"),
                "页面": f"{l5}/{l6}",
                "kind": "biz",
                "origin": "proto-overlay",
                **base_trace(l5, l6, page),
            }
        )
    return out


def prototype_atoms_for_module(l4, l5, l6, catalog, sibling_l6s) -> list[dict]:
    page = resolve_l5_page(catalog, l5)
    atoms = overlay_atoms(catalog, l6, l5, page)
    if not page:
        return atoms
    route = page.get("route", "")
    nav = build_nav(l4, page, catalog)
    zones = page.get("zones") or []
    for i, zone in enumerate(zones):
        pri = "P0" if i < 4 else "P1"
        atoms.append(zone_to_atom(zone, l5, l6, nav, route, pri, page))
    return atoms


def leftover_pack_pool(all_pack: list[dict], used_fps: set[str]) -> list[dict]:
    return [a for a in all_pack if a["功能点"] not in used_fps]


def dedupe_atoms(atoms: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for a in atoms:
        k = (a.get("origin", ""), a["功能点"], a.get("子功能项", ""), a.get("USM验收场景编号", ""))
        if k in seen:
            continue
        seen.add(k)
        out.append(a)
    return out


def fill_to_quota(atoms, leftover, l5, l6, design14, need) -> list[dict]:
    if len(atoms) >= need:
        return atoms[:need]
    pool = leftover + design14
    seen = {a["功能点"] for a in atoms}
    for a in pool:
        if len(atoms) >= need:
            break
        if a["功能点"] in seen:
            continue
        seen.add(a["功能点"])
        atoms.append(a)
    return atoms[:need]


GENERIC_TEMPLATES = [
    ("入口可达", "模块入口与导航", "可从专题导航进入本子模块", "P0"),
    ("权限控制", "访问权限", "无权限不可操作受控功能", "P1"),
    ("加载态", "数据加载反馈", "请求中有加载反馈且完成后消失", "P1"),
    ("空数据态", "无数据空态", "无命中时可读空态、不伪装业务数", "P1"),
    ("异常态", "接口失败提示", "失败时可读错误且不崩溃", "P1"),
    ("结果一致性", "统计与列表一致", "汇总与明细口径一致或差异可解释", "P1"),
]


def generic_cases(l4, l5, l6, catalog) -> list[dict]:
    page = resolve_l5_page(catalog, l5)
    nav = build_nav(l4, page, catalog)
    route = (page or {}).get("route", "（按 IA 导航）")
    out = []
    for name, sub, content, pri in GENERIC_TEMPLATES[:GENERIC_PER_MODULE]:
        if name == "入口可达":
            steps = f"1.登录测试环境\n2.导航：{nav}\n3.查看页面标题或面包屑是否为「{l5} / {l6}」"
            expect = f"1、成功进入「{l6}」\n2、页面标题或面包屑与模块名称一致"
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
                "前置条件": PRECOND if name != "权限控制" else "1、测试环境可访问；2、已准备有权限与无权限账号",
                "测试步骤": steps,
                "预期结果": expect,
                "优先级": pri,
                "页面": f"{l5}/{l6}",
                "kind": "generic",
                "origin": "generic",
                **base_trace(l5, l6, page),
            }
        )
    return out


def allocate_non_generic(n_modules: int, weights: list[int]) -> list[int]:
    total_w = sum(max(1, w) for w in weights) or n_modules
    base = [max(15, int(TARGET_NON_GENERIC * max(1, w) / total_w)) for w in weights]
    base = [min(40, max(12, x)) for x in base]
    s = sum(base)
    i = 0
    while s < TARGET_NON_GENERIC and i < 10000:
        idx = i % n_modules
        if base[idx] < 40:
            base[idx] += 1
            s += 1
        i += 1
    while s > TARGET_NON_GENERIC and i < 20000:
        idx = i % n_modules
        if base[idx] > 12:
            base[idx] -= 1
            s -= 1
        i += 1
    return base


# catalog 未覆盖时的兜底路由（真源仍以 catalog / routes.tsx 为准）
EXTRA_L5_PAGES = {
    "政策时序分析": {"route": "/policy/overview", "menu": "政策时序分析", "zones": []},
    "区域政策对比": {"route": "/policy/analysis", "menu": "区域政策对比", "zones": []},
    "深圳政策现状分析": {"route": "/policy/recommendation", "menu": "深圳政策现状分析", "zones": []},
}


def enrich_pack_trace(atoms: list[dict], tmeta: dict, trace_name: str):
    for a in atoms:
        if trace_name and not a.get("TRACE引用"):
            a["TRACE引用"] = trace_name
        if tmeta.get("fp") and not a.get("功能点ID"):
            a["功能点ID"] = tmeta["fp"]
        if tmeta.get("route") and not a.get("路由route"):
            a["路由route"] = tmeta["route"]
        # 原型 route 优先
        if a.get("origin", "").startswith("proto") and a.get("路由route"):
            continue


def build_cases(items, design_index, catalog, pack_index) -> dict:
    groups = defaultdict(list)
    for it in items:
        groups[(it["l4"], it["l5"], it["l6"])].append(it)
    l5_siblings = defaultdict(list)
    for l4, l5, l6 in groups:
        if l6 not in l5_siblings[(l4, l5)]:
            l5_siblings[(l4, l5)].append(l6)

    keys = sorted(groups.keys(), key=lambda x: (L4_TARGETS.index(x[0]), x[1], x[2]))
    weights, meta = [], []
    for l4, l5, l6 in keys:
        desc = "；".join(r["desc"] for r in groups[(l4, l5, l6)] if r["desc"])
        design = lookup_design(design_index, l5, l6)
        pmeta = pack_index.get(l5) or {}
        proto_bonus = 80 if resolve_l5_page(catalog, l5) else 0
        overlay_bonus = 40 if l6 in catalog["overlays"] else 0
        pack_bonus = 60 if pmeta.get("dir") else 0
        weights.append(len(desc) + len(design) // 2 + 40 + proto_bonus + overlay_bonus + pack_bonus)
        meta.append((l4, l5, l6, desc, design, pmeta))

    by_l4 = defaultdict(list)
    pack_cache: dict[str, dict] = {}
    built: list[tuple] = []

    for l4, l5, l6, desc, design, pmeta in meta:
        siblings = l5_siblings[(l4, l5)]
        page = resolve_l5_page(catalog, l5)
        focus = pmeta.get("focus")
        rel = pmeta.get("dir") or ""
        if rel and rel not in pack_cache:
            pack_cache[rel] = read_pack_texts(rel)
        files = pack_cache.get(rel) or {}

        usm_name, usm_text = files.get("usm", ("", ""))
        trace_name, trace_text = files.get("trace", ("", ""))
        ux_name, ux_text = files.get("ux", ("", ""))
        ia_name, ia_text = files.get("ia", ("", ""))
        tmeta = extract_trace_meta(trace_text)
        if trace_name:
            tmeta["file"] = trace_name
        # 原型 route 覆盖 TRACE
        if page and page.get("route"):
            tmeta["route"] = page["route"]

        pack_all = []
        if usm_text:
            pack_all.extend(pack_atoms_from_usm(usm_text, usm_name, l5, l6, focus, page, catalog, l4))
        pack_all.extend(pack_atoms_from_ux_ia(ux_text, ux_name, "ux", l5, l6, focus, page, catalog, l4))
        pack_all.extend(pack_atoms_from_ux_ia(ia_text, ia_name, "ia", l5, l6, focus, page, catalog, l4))
        wire_name, wire_text = files.get("wire", ("", ""))
        met_name, met_text = files.get("metric", ("", ""))
        pack_all.extend(pack_atoms_from_ux_ia(wire_text, wire_name, "ia", l5, l6, focus, page, catalog, l4))
        pack_all.extend(pack_atoms_from_ux_ia(met_text, met_name, "ux", l5, l6, focus, page, catalog, l4))
        if not pack_all and usm_text:
            pack_all.extend(pack_atoms_from_usm(usm_text, usm_name, l5, l6, None, page, catalog, l4)[:12])
        enrich_pack_trace(pack_all, tmeta, trace_name)

        atoms = []
        atoms.extend(prototype_atoms_for_module(l4, l5, l6, catalog, siblings))
        atoms.extend(pack_all)
        atoms.extend(atoms_from_text(desc, l5, l6, "需规", page))
        if design:
            atoms.extend(atoms_from_text(design[:2500], l5, l6, "设计", page))
        atoms = dedupe_atoms(atoms)
        order = {
            "proto-overlay": 0,
            "proto": 1,
            "usm-ac": 2,
            "usm-walk": 3,
            "usm-story": 4,
            "usm-ex": 5,
            "pack-ux": 6,
            "pack-ia": 7,
            "req": 8,
            "bid": 9,
            "design14": 10,
        }
        atoms.sort(key=lambda a: order.get(a.get("origin", "req"), 11))
        used = {a["功能点"] for a in atoms}
        extra_pack = [
            x
            for x in pack_atoms_from_usm(usm_text, usm_name, l5, l6, None, page, catalog, l4)
            + pack_atoms_from_ux_ia(ux_text, ux_name, "ux", l5, l6, None, page, catalog, l4)
            + pack_atoms_from_ux_ia(ia_text, ia_name, "ia", l5, l6, None, page, catalog, l4)
            if x["功能点"] not in used
        ]
        enrich_pack_trace(extra_pack, tmeta, trace_name)
        d14 = design14_atoms(l5, l6, page, catalog, l4)
        full = dedupe_atoms(atoms + extra_pack + d14)
        built.append((l4, l5, l6, page, full))

    avail = [len(b[4]) for b in built]
    quotas = allocate_non_generic(len(built), avail)
    for i, q in enumerate(quotas):
        quotas[i] = min(q, avail[i])
    s = sum(quotas)
    j = 0
    while s < TARGET_NON_GENERIC and j < 20000:
        idx = j % len(built)
        if quotas[idx] < avail[idx]:
            quotas[idx] += 1
            s += 1
        j += 1

    for (l4, l5, l6, page, full), need in zip(built, quotas):
        atoms = full[:need]
        for a in atoms:
            a.setdefault("页面", f"{l5}/{l6}")
            a.setdefault("前置条件", "1、系统正常；2、已登录且具备本模块权限；3、测试数据可用")
            if not a.get("测试步骤"):
                nav_hint = build_nav(l4, page, catalog)
                a["测试步骤"] = (
                    f"1.登录测试环境\n2.导航：{nav_hint}\n"
                    f"3.执行「{a['功能点']}」\n4.观察结果区"
                )
            if not a.get("预期结果"):
                a["预期结果"] = f"1、{a['测试内容'][:90]}\n2、结果可观察"
            a.setdefault("优先级", "P1")
            a.setdefault("kind", "biz")
            if page and page.get("route"):
                a["路由route"] = page["route"]
            sanitize_atom(a)
            by_l4[l4].append(a)
        for g in generic_cases(l4, l5, l6, catalog):
            sanitize_atom(g)
            by_l4[l4].append(g)

    result = {}
    gkx_keys = [
        "用户故事编号", "USM验收场景编号", "原始需求文件", "原始需求章节号",
        "功能点ID", "TRACE引用", "路由route", "交付口径tier", "关联任务ID", "备注",
    ]
    for l4 in L4_TARGETS:
        cases = by_l4.get(l4, [])
        numbered = []
        for i, c in enumerate(cases, 1):
            row = {
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
            for k in gkx_keys:
                if k == "备注":
                    row[k] = c.get("origin", "")
                else:
                    row[k] = c.get(k, "")
            numbered.append(row)
        result[l4] = numbered
    return result


HEADERS = [
    "用例编号", "功能模块", "子功能模块", "功能项", "子功能项", "页面", "功能点",
    "测试内容", "前置条件", "测试步骤", "预期结果", "优先级", "是否通过",
    "测试工程师", "测试时间", "审核员", "测试截图",
    "用户故事编号", "USM验收场景编号", "原始需求文件", "原始需求章节号",
    "功能点ID", "TRACE引用", "路由route", "交付口径tier", "关联任务ID", "备注",
]


def write_workbook(l4: str, cases: list[dict], out_path: Path):
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    ws["A1"] = f"智能服务集群-科技专题服务系统测试用例（{L3}-{l4}）·v1.3"
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    # 扩展列标题（总集 17 列 + GKX 右侧）
    for col, h in enumerate(HEADERS, start=1):
        ws.cell(2, col, h)
    align = Alignment(wrap_text=True, vertical="top")
    for i, case in enumerate(cases, start=3):
        for col, key in enumerate(HEADERS, start=1):
            cell = ws.cell(i, col, case.get(key, ""))
            cell.alignment = align
    for sheet_name in ["兼容性测试用例", "集成测试用例", "性能测试用例"]:
        if sheet_name not in wb.sheetnames:
            continue
        wso = wb[sheet_name]
        if wso["A1"].value and "测试用例" in str(wso["A1"].value):
            wso["A1"] = f"智能服务集群-科技专题服务系统{sheet_name}（{L3}-{l4}）·v1.3"
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        wb.save(out_path)
    except OSError:
        alt_dir = OUT_DIR_FALLBACK
        alt_dir.mkdir(parents=True, exist_ok=True)
        alt = alt_dir / out_path.name
        wb.save(alt)
        print(f"LOCKED {out_path.name} -> {alt}")
        out_path = alt
    wb.close()


def main():
    catalog = load_catalog()
    pack_index = load_pack_index()
    items = load_function_tree()
    design_index = parse_bid_design()
    print(f"leaves={len(items)} design={len(design_index)} catalog={len(catalog['pages'])} packs={len(pack_index)}")

    by_l4 = build_cases(items, design_index, catalog, pack_index)
    write_dir = OUT_DIR
    write_dir.mkdir(parents=True, exist_ok=True)

    total = non_g = gen = proto = packn = 0
    print(f"{'四级':<12}{'用例':>6}{'非通用':>8}{'通用':>6}{'原型':>6}{'八件套':>8}")
    origin_pack = {"usm-ac", "usm-walk", "usm-story", "usm-ex", "pack-ux", "pack-ia"}
    for l4 in L4_TARGETS:
        cases = by_l4[l4]
        ng = sum(1 for c in cases if c["kind"] != "generic")
        g = len(cases) - ng
        p = sum(1 for c in cases if str(c.get("origin", "")).startswith("proto"))
        pk = sum(1 for c in cases if c.get("origin", "") in origin_pack)
        total += len(cases)
        non_g += ng
        gen += g
        proto += p
        packn += pk
        out = write_dir / f"6.国际科技信息中心项目_{l4}_测试用例.xlsx"
        write_workbook(l4, cases, out)
        print(f"{l4:<12}{len(cases):>6}{ng:>8}{g:>6}{p:>6}{pk:>8} -> {out.name}")

    print(f"{'合计':<12}{total:>6}{non_g:>8}{gen:>6}{proto:>6}{packn:>8}")

    lines = [
        f"| {l4} | {len(by_l4[l4])} | {sum(1 for c in by_l4[l4] if c['kind']!='generic')} | "
        f"{sum(1 for c in by_l4[l4] if c['kind']=='generic')} | "
        f"{sum(1 for c in by_l4[l4] if str(c.get('origin','')).startswith('proto'))} | "
        f"{sum(1 for c in by_l4[l4] if c.get('origin','') in origin_pack)} |"
        for l4 in L4_TARGETS
    ]
    (write_dir / "README.md").write_text(
        f"""# 科技专题战略分析 · 总集功能测试用例 v1.3

> **相对 v1.2**：功能清单定数量；八件套出要点；编写时与原型冲突以 demo-ui-topic 为准（**不写入用例正文**）。  
> 非通用约 **{non_g}**，总用例 **{total}**（通用 **{gen}**）；原型向 **{proto}**，八件套向 **{packn}**。  
> 索引：`../product-pack-index-zt-strategy.yaml` · 原型：`../prototype-catalog-zt-strategy.yaml`  
> 编号：`ZNFWJQ-KJZTFWXT-v1.0-FUNC-#####`（每四级独立起编）  
> 列：总集 17 列 + 右侧 GKX 扩展列（用户故事 / USM-AC / bid / TRACE / route / 任务ID）  
> 生成：`agent-delivery/scripts/_gen_zt_testcases_v13.py`  
> 任务：`QA-KJZTFWXT-STRATEGY-TOTALSET-L01` · ponytail: full

## 编写原则（v1.3）

1. **数量**：从功能清单 L5/L6 拆分，非通用目标约 1300、总约 1700（含每模块 6 条通用质量属性）
2. **内容**：USM 故事 / 主路径 / 验收标准 / 异常路径 → 用例要点；路由只进扩展列，不进步骤
3. **文案**：前置写测试环境；步骤用业务名称；不写确认路由、Drawer/URL、八件套原则、每条非白屏
4. **填充**：配额不足时用剩余八件套要点 + 界面规范检查，禁止「布局区块-N」
5. **KEYENT P0**：对照 `USM-ENT-KEYENT` AC + 侧栏类型/领域分析

| 四级功能 | 用例数 | 非通用 | 通用 | 原型向 | 八件套向 |
|----------|--------|--------|------|--------|----------|
"""
        + "\n".join(lines)
        + f"\n| **合计** | **{total}** | **{non_g}** | **{gen}** | **{proto}** | **{packn}** |\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
