# -*- coding: utf-8 -*-
"""功能点拆分 v1：功能清单 5 个四级 → 总集「功能测试用例」填到功能点，不写用例步骤。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import openpyxl
import yaml
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = Path(r"d:\work\gkx-lumen")
ORCH = ROOT / "gkx-orchestration" / "agent-delivery"
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
QA_DIR = ORCH / "qa" / "total-set" / "KJZTFWXT"
CATALOG = QA_DIR / "prototype-catalog-zt-strategy.yaml"
PACK_INDEX = QA_DIR / "product-pack-index-zt-strategy.yaml"
PACK_ROOT = ORCH / "agent-handoffs" / "产品整体定义"
OUT = QA_DIR / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v1.xlsx"

L4_TARGETS = ["产业服务链分析", "产业链分析", "企业分析", "政策分析", "综合智能分析"]
MODULE = "科技专题战略分析"
TASK_ID = "QA-KJZTFWXT-FUNCLIST-SPLIT-L01"
A1_TITLE = "智能服务集群-科技专题服务系统功能点拆分"

SKIP_PACK = re.compile(
    r"评审模式|内部禁用|Frame|DOM 中|review mount|有效高度|像素|产品解释作为需求|内部禁用词|review_copy"
)
GENERIC_FOCUS = {"区域", "分析", "企业", "选择", "查看", "系统", "页面"}


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def biz_text(s: str) -> str:
    if not s:
        return ""
    t = str(s)
    repls = [
        (r"ContextBar", "顶部筛选"),
        (r"Cascader", "级联选择"),
        (r"Checkbox", "复选框"),
        (r"\bRadio\b", "单选"),
        (r"\bTable\b", "列表"),
        (r"\bDrawer\b", "侧滑详情"),
        (r"ForceGraph", "关系图谱"),
        (r"\bG6\s*", ""),
        (r"OrgPickerModal", "机构选择窗"),
        (r"StageDetailDrawer", "环节详情"),
        (r"emptyGate", "未选对象提示"),
        (r"URL\s*同步[^\n；。]*", "筛选与结果同步刷新"),
        (r"路由\s+/[^\s；。]+", "进入对应页面"),
        (r"workspace=type&view=type", "类型分析"),
        (r"workspace=domain&view=domain", "领域分析"),
        (r"两个分析类型\s*Tab|分析类型\s*Tab|页内Tab「?类型与区域分析」?", "侧栏「重点企业类型分析」"),
        (r"点击[“\"]?领域分布分析[”\"]?\s*Tab", "侧栏「重点企业领域分析」"),
        (r"\[原型\]\s*|\[USM[^\]]*\]\s*|\[需规\]\s*|\[IA\]\s*|\[UX\]\s*", ""),
    ]
    for pat, repl in repls:
        t = re.sub(pat, repl, t)
    return re.sub(r"\s+", " ", t).strip(" ；;、，")


def load_function_tree() -> list[dict]:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技专题服务系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        if "需规功能描述" in "".join(str(x or "") for x in row[:14]):
            header_idx = i
            break
    cur = [""] * 6
    items = []
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (6, 7, 8, 9, 10, 11)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        if cur[3] not in L4_TARGETS:
            continue
        desc = str(vals[12]).strip() if vals[12] else ""
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
    return (yaml.safe_load(PACK_INDEX.read_text(encoding="utf-8")) or {}).get("l5") or {}


def resolve_page(catalog: dict, l5: str) -> dict | None:
    pages = catalog["pages"]
    if l5 in pages:
        return pages[l5]
    for k, v in pages.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    return None


def page_name(catalog: dict, l5: str) -> str:
    p = resolve_page(catalog, l5)
    if p and p.get("menu"):
        return str(p["menu"])
    return l5


def split_desc(desc: str) -> list[str]:
    if not desc:
        return []
    text = desc.replace("\r", "\n")
    chunks = re.split(r"[。；;\n]+", text)
    out = []
    for chunk in chunks:
        chunk = chunk.strip(" 、，,")
        if len(chunk) < 6:
            continue
        pieces = re.split(r"(?:同时，?|并且|以及，?|并支持|还支持)", chunk)
        for p in pieces:
            p = re.sub(r"^(该功能|本功能|此功能|用户可以|用户可|系统将|系统可|系统能够|系统)", "", p)
            p = p.strip(" 、，,")
            if len(p) < 6:
                continue
            out.append(p)
    seen, uniq = set(), []
    for x in out:
        k = norm(x)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(x)
    return uniq


def keyword_score(text: str, key: str) -> int:
    if not key or key in ("/", ""):
        return 0
    t, k = text or "", key
    n = 0
    if k in t:
        n += 3
    for ch in re.findall(r"[\u4e00-\u9fff]{2,}", k):
        if ch in t:
            n += 1
    return n


def pick_l6(l6s: list[str], text: str) -> str:
    if not l6s:
        return "/"
    ranked = sorted(l6s, key=lambda x: keyword_score(text, x), reverse=True)
    if keyword_score(text, ranked[0]) > 0:
        return ranked[0]
    return l6s[0]


def extract_usm_points(md: str) -> list[str]:
    pts = []
    # 验收标准表：| ID | 故事 | Given/When/Then | ...
    for line in md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in ("ID", "用户故事", "场景") or set(cells[0]) <= {"-", ":"}:
            continue
        body = cells[2] if len(cells) >= 3 else ""
        if len(cells) >= 4 and "When" not in cells[1] and len(cells[2]) < 8:
            body = cells[2]
        if SKIP_PACK.search(body):
            continue
        body = biz_text(body)
        if 8 <= len(body) <= 180:
            pts.append(body)
    # 异常表
    in_ex = False
    for line in md.splitlines():
        if re.match(r"^##+\s*异常", line):
            in_ex = True
            continue
        if in_ex and line.startswith("## "):
            in_ex = False
        if not in_ex or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("场景", "---"):
            continue
        body = biz_text(f"{cells[0]}时：{cells[1]}")
        if SKIP_PACK.search(body) or len(body) < 8:
            continue
        pts.append(body)
    return pts


def load_pack_points(l5: str, index: dict) -> list[str]:
    meta = index.get(l5)
    if not meta:
        for k, v in index.items():
            if norm(k) == norm(l5) or k in l5 or l5 in k:
                meta = v
                break
    if not meta:
        return []
    d = PACK_ROOT / meta["dir"]
    if not d.is_dir():
        return []
    pts = []
    focus = [k for k in (meta.get("focus") or []) if k and k not in GENERIC_FOCUS]
    for usm in sorted(d.glob("USM-*.md")):
        text = usm.read_text(encoding="utf-8")
        for p in extract_usm_points(text):
            if focus and not any(k in p for k in focus):
                continue
            pts.append(p)
    seen, uniq = set(), []
    for p in pts:
        k = norm(p)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(p)
    return uniq


def overlay_points(catalog: dict, l6: str) -> list[dict]:
    ov = catalog["overlays"].get(l6) or {}
    out = []
    for p in ov.get("points") or []:
        out.append(
            {
                "功能项": p.get("功能项") or "",
                "子功能项": p.get("子功能项") or l6,
                "功能点": biz_text(p.get("功能点") or ""),
            }
        )
    return out


def build_rows(items: list[dict], catalog: dict, index: dict) -> list[dict]:
    by_l5 = defaultdict(list)
    for it in items:
        by_l5[(it["l4"], it["l5"])].append(it)

    rows = []
    seen = set()

    def add(l4, l5, l6, page, fp):
        fp = biz_text(fp)
        if len(fp) < 4:
            return
        key = (l4, l5, l6, norm(fp))
        if key in seen:
            return
        seen.add(key)
        rows.append(
            {
                "功能模块": MODULE,
                "子功能模块": l4,
                "功能项": l5,
                "子功能项": l6,
                "页面": page,
                "功能点": fp,
            }
        )

    for (l4, l5), group in by_l5.items():
        page = page_name(catalog, l5)
        l6s = [g["l6"] for g in group]
        proto = resolve_page(catalog, l5)
        # 1) 需规（必须包含）
        for g in group:
            clauses = split_desc(g["desc"]) or ([g["desc"]] if g["desc"] else [g["l6"]])
            for c in clauses:
                add(l4, l5, g["l6"], page, c)
            for ov in overlay_points(catalog, g["l6"]):
                add(l4, l5, g["l6"], page, ov["功能点"])
        # 2) 原型页面/按钮/操作/结果
        used_zone = set()
        if proto:
            for z in proto.get("zones") or []:
                blob = " ".join(str(z.get(k) or "") for k in ("zone", "control", "action", "expect"))
                l6 = pick_l6(l6s, blob)
                fp = biz_text(
                    f"{z.get('control') or z.get('zone')}：{z.get('action')}，{z.get('expect')}"
                )
                add(l4, l5, l6, page, fp)
                used_zone.add(norm(blob))
        # 3) 八件套 USM 验收 / 主路径 / 异常
        for p in load_pack_points(l5, index):
            add(l4, l5, pick_l6(l6s, p), page, p)
        _ = used_zone
    return rows


def write_excel(rows: list[dict]) -> None:
    wb = openpyxl.load_workbook(TPL)
    # 只填功能测试用例；其它 sheet 清掉样例行以免误用
    ws = wb["功能测试用例"]
    ws["A1"] = A1_TITLE
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    align = Alignment(wrap_text=True, vertical="top")
    headers = [ws.cell(2, c).value for c in range(1, 18)]
    for i, r in enumerate(rows, start=1):
        row_i = i + 2
        rec = {
            "用例编号": f"ZNFWJQ-KJZTFWXT-v1.0-FUNC-{i:05d}",
            "功能模块": r["功能模块"],
            "子功能模块": r["子功能模块"],
            "功能项": r["功能项"],
            "子功能项": r["子功能项"],
            "页面": r["页面"],
            "功能点": r["功能点"],
        }
        for col, h in enumerate(headers, start=1):
            val = rec.get(h, "") if h else ""
            cell = ws.cell(row_i, col, val)
            cell.alignment = align
            if col == 1:
                cell.font = Font(name="Calibri")
    for col, w in enumerate([36, 18, 16, 22, 22, 20, 48], start=1):
        ws.column_dimensions[get_column_letter(col)].width = w
    for name in wb.sheetnames:
        if name == "功能测试用例":
            continue
        wso = wb[name]
        if name == "规则 -0529":
            continue
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    wb.close()


def main():
    items = load_function_tree()
    catalog = load_catalog()
    index = load_pack_index()
    rows = build_rows(items, catalog, index)
    write_excel(rows)
    by_l4 = defaultdict(int)
    for r in rows:
        by_l4[r["子功能模块"]] += 1
    print(f"src_rows={len(items)} fps={len(rows)} -> {OUT}")
    for k in L4_TARGETS:
        print(f"  {k}: {by_l4.get(k, 0)}")


if __name__ == "__main__":
    main()
