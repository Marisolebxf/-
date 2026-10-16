#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KJZTFWXT 交付 Excel · B∪A 切点投影（功能测试 sheet）。

口径（as-built/prompts/_submit.md）：
- 输入：各册 coverage-fp.md 中「已覆盖 / 部分覆盖」功能点行 + 源 B 线场景用例
- 一行 = 一个功能点；测试内容/步骤/预期按点切片（禁止全文复制场景充多行）
- 未覆盖不投影；政策/综合智能等无 B 册矩阵的 A 线段本波不纳入
- 优先复用 A 线 v8 拆分表用例编号；匹配失败则从 code-registry next_seq 取新号

产出：
- qa/delivery/KJZTFWXT/6.…_测试用例.xlsx（覆盖功能 sheet）
- qa/delivery/KJZTFWXT/ab-merge-manifest.md（投影对账）
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
import yaml

ORCH = Path(__file__).resolve().parents[1]
QA = ORCH / "qa"
TC_ROOT = QA / "test-cases" / "KJZTFWXT"
V8 = QA / "total-set" / "KJZTFWXT" / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v8.xlsx"
TPL = Path("/Users/roy/data/projects/zhipu/gkx/参考文档/测试模板-v2/6.国际科技信息中心项目_xx_测试用例.xlsx")
OUT = QA / "delivery" / "KJZTFWXT" / "6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx"
MANIFEST = QA / "delivery" / "KJZTFWXT" / "ab-merge-manifest.md"
REGISTRY = QA / "code-registry.yaml"

STATUS_OK = ("已覆盖", "部分覆盖")
ROW_RE = re.compile(r"^\|\s*ZNFWJQ-KJZTFWXT-v1\.0-FUNC-(\d{5})\s*\|")


def load_v8() -> tuple[list[dict], dict[tuple[str, str], dict], dict[str, list[dict]]]:
    wb = openpyxl.load_workbook(V8, read_only=True, data_only=True)
    ws = wb["功能测试用例"]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    # R1 title, R2 header, R3+ data
    data = []
    by_sub_fp: dict[tuple[str, str], dict] = {}
    by_fp: dict[str, list[dict]] = defaultdict(list)
    for r in rows[2:]:
        if not r or not r[0]:
            continue
        item = {
            "id": str(r[0]).strip(),
            "功能模块": str(r[1] or "").strip(),
            "子功能模块": str(r[2] or "").strip(),
            "功能项": str(r[3] or "").strip(),
            "子功能项": str(r[4] or "").strip(),
            "页面": str(r[5] or "").strip(),
            "功能点": str(r[6] or "").strip(),
        }
        data.append(item)
        by_sub_fp[(item["子功能项"], item["功能点"])] = item
        by_fp[item["功能点"]].append(item)
    return data, by_sub_fp, by_fp


def parse_func_book(md: Path) -> dict[str, list[str]]:
    """短号 00387 / 全号 → 主表 cells（至少 17 列）。"""
    out: dict[str, list[str]] = {}
    for line in md.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 17:
            continue
        full = cells[0]
        short = m.group(1)
        out[full] = cells
        out[short] = cells
        out[short.lstrip("0") or "0"] = cells
    return out


def classify_status(cell: str) -> str | None:
    c = cell.strip()
    if c.startswith("未覆盖"):
        return "未覆盖"
    if c.startswith("部分覆盖"):
        return "部分覆盖"
    if c.startswith("已覆盖"):
        return "已覆盖"
    return None


def parse_coverage_fp(path: Path) -> list[dict]:
    """Parse main matrix rows from coverage-fp.md."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"A 线状态：\s*N/A|不做 v8 功能点覆盖", text):
        return []
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if re.match(r"^\|\s*[-:]+", line):
            continue
        # unescape \| inside cells for split: temporarily protect
        protected = line.replace("\\|", "\x00")
        cells = [c.strip().replace("\x00", "|") for c in protected.strip().strip("|").split("|")]
        if not cells or "功能点键" in cells[:3]:
            continue
        # KEYENT: 功能点键在首列；多数册: # | 功能点键 | …
        key_i = next((i for i, c in enumerate(cells) if re.match(r"^T\d+", c.replace("\\", ""))), None)
        if key_i is None:
            continue
        key = cells[key_i].replace("\\", "")
        # find status cell
        st = None
        st_i = None
        for i, c in enumerate(cells):
            st = classify_status(c)
            if st:
                st_i = i
                break
        if not st or st == "未覆盖":
            continue
        # 对应用例 = 状态前一列（常见）
        case_cell = cells[st_i - 1] if st_i and st_i >= 1 else ""
        note = cells[st_i + 1] if st_i is not None and st_i + 1 < len(cells) else ""
        parts = [p.strip() for p in key.split("|")]
        if len(parts) < 3:
            continue
        t_id, sub, fp = parts[0], parts[1], "|".join(parts[2:])  # 容错：功能点名含 |
        case_ids = re.findall(r"\d{5}", case_cell)
        if not case_ids:
            case_ids = re.findall(r"FUNC-(\d{5})", case_cell)
        rows.append(
            {
                "key": key,
                "t": t_id,
                "子功能项": sub,
                "功能点": fp,
                "status": "部分覆盖" if st.startswith("部分") else "已覆盖",
                "case_shorts": case_ids,
                "note": note,
                "book": path.parent.name,
                "cov_path": str(path.relative_to(QA)),
            }
        )
    return rows


def pick_source(case_shorts: list[str], book_cases: dict[str, list[str]]) -> list[str] | None:
    for s in case_shorts:
        for key in (s, s.zfill(5), s.lstrip("0") or "0"):
            if key in book_cases:
                return book_cases[key]
    return None


def slice_steps(src: list[str], fp: str, status: str, note: str) -> tuple[str, str, str, str]:
    """Return 测试内容, 前置, 步骤, 预期 — 按点切片，不加严。"""
    pre = src[8] if len(src) > 8 else ""
    steps = src[9] if len(src) > 9 else ""
    exp = src[10] if len(src) > 10 else ""
    # 测试内容：一句话对准功能点
    content = f"验证「{fp}」在专题系统中的可判定呈现或行为"
    if status == "部分覆盖" and note:
        content += f"（部分覆盖：{note[:80]}）"
    # 前置：保留源前置，过长则截断
    pre_out = pre if pre else "1、系统正常；2、已登录且可进入本功能页"
    # 步骤：最短进入 + 指向源场景相关验证（不把整段场景步骤原样复制 N 遍的语义：每点只保留与本点相关的最小描述）
    steps_out = (
        f"1.按源场景进入本功能页面并完成必要配置（同源步骤见源用例，本行不重复展开无关分支）\n"
        f"2.定位并执行与功能点「{fp}」直接相关的可见操作或观察\n"
        f"3.记录与本点相关的界面结果（不加严源场景未要求的字段/精确数量）"
    )
    # 若源步骤很短（≤2 步），直接复用并标注聚焦
    if steps and steps.count("\n") <= 1 and len(steps) < 120:
        steps_out = f"1.聚焦验证「{fp}」：{steps}"
    exp_out = (
        f"1、功能点「{fp}」对应的界面呈现或行为可判定成立"
        f"（判定口径不严于源场景预期；部分覆盖时以覆盖矩阵说明为准）"
    )
    if status == "部分覆盖" and note:
        exp_out += f"\n2、已知弱于需规之处：{note[:120]}"
    return content, pre_out, steps_out, exp_out


def match_v8(sub: str, fp: str, by_sub_fp, by_fp) -> dict | None:
    hit = by_sub_fp.get((sub, fp))
    if hit:
        return hit
    cands = by_fp.get(fp) or []
    if len(cands) == 1:
        return cands[0]
    for c in cands:
        if c["子功能项"] == sub or sub in c["子功能项"] or c["子功能项"] in sub:
            return c
    return cands[0] if len(cands) == 1 else (cands[0] if len(cands) > 1 else None)


def main() -> None:
    v8_rows, by_sub_fp, by_fp = load_v8()
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    next_seq = int(reg["next_seq"]["KJZTFWXT"]["FUNC"])

    # collect coverage + cases per book
    projections: list[dict] = []
    stats = Counter()
    unmatched_v8 = 0
    no_source = 0
    used_a_ids: set[str] = set()
    new_ids: list[str] = []

    for cov in sorted(TC_ROOT.rglob("coverage-fp.md")):
        book_dir = cov.parent
        md_files = list(book_dir.glob("FUNC-*.md"))
        if not md_files:
            continue
        book_cases = parse_func_book(md_files[0])
        for row in parse_coverage_fp(cov):
            stats[row["status"]] += 1
            src = pick_source(row["case_shorts"], book_cases)
            if not src:
                no_source += 1
                stats["no_source"] += 1
                continue
            v8 = match_v8(row["子功能项"], row["功能点"], by_sub_fp, by_fp)
            content, pre, steps, exp = slice_steps(src, row["功能点"], row["status"], row["note"])
            if v8 and v8["id"] not in used_a_ids:
                case_id = v8["id"]
                used_a_ids.add(case_id)
                id_source = "A线v8"
            elif v8 and v8["id"] in used_a_ids:
                # rare duplicate key mapping — new id
                case_id = f"ZNFWJQ-KJZTFWXT-v1.0-FUNC-{next_seq:05d}"
                new_ids.append(case_id)
                next_seq += 1
                id_source = "new(dup-A)"
                unmatched_v8 += 0
            else:
                unmatched_v8 += 1
                case_id = f"ZNFWJQ-KJZTFWXT-v1.0-FUNC-{next_seq:05d}"
                new_ids.append(case_id)
                next_seq += 1
                id_source = "new(no-A-match)"

            # module columns: prefer v8, else B source
            功能模块 = (v8 or {}).get("功能模块") or src[1]
            # B books use 企业分析；v8 uses 科技专题战略分析 as 功能模块 — keep v8 for compliance
            子功能模块 = (v8 or {}).get("子功能模块") or src[2]
            功能项 = (v8 or {}).get("功能项") or src[3]
            子功能项 = (v8 or {}).get("子功能项") or row["子功能项"]
            页面 = (v8 or {}).get("页面") or src[5]
            功能点 = row["功能点"]
            pri = src[11] if len(src) > 11 else "P0"
            if pri not in ("P0", "P1", "P2"):
                pri = "P0"

            delivery = [
                case_id,
                功能模块,
                子功能模块,
                功能项,
                子功能项,
                页面,
                功能点,
                content,
                pre,
                steps,
                exp,
                pri,
                "",  # 是否通过
                "",
                "",
                "",
                "",  # 测试截图
            ]
            projections.append(
                {
                    "delivery": delivery,
                    "key": row["key"],
                    "status": row["status"],
                    "src": src[0],
                    "book": row["book"],
                    "id_source": id_source,
                    "note": row["note"],
                }
            )

    # sort: by A-line id numeric when possible
    def sort_key(p):
        m = re.search(r"FUNC-(\d{5})", p["delivery"][0])
        return int(m.group(1)) if m else 10**9

    projections.sort(key=sort_key)
    all_rows = [p["delivery"] for p in projections]

    # write excel from template
    assert TPL.exists(), f"missing template {TPL}"
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    if ws.max_row >= 3:
        ws.delete_rows(3, ws.max_row - 2)
    ws.cell(1, 1).value = "智能服务集群-科技专题服务系统测试用例"
    for i, row in enumerate(all_rows, start=3):
        for c in range(1, 18):
            cell = ws.cell(i, c)
            cell.value = row[c - 1] if row[c - 1] else None
            cell.alignment = openpyxl.styles.Alignment(vertical="center", wrap_text=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    # Manifest
    by_book = Counter(p["book"] for p in projections)
    by_status = Counter(p["status"] for p in projections)
    by_idsrc = Counter(p["id_source"] for p in projections)
    lines = [
        "# KJZTFWXT B∪A 切点投影交付对账",
        "",
        f"> 生成脚本：`scripts/_gen_zt_delivery_func_ab_merge.py`",
        f"> 交付文件：`{OUT.relative_to(ORCH)}`",
        f"> 口径：`as-built/prompts/_submit.md`；未覆盖不投影；政策/综合智能本波不纳入",
        "",
        "## 汇总",
        "",
        f"| 项 | 值 |",
        f"|----|----|",
        f"| 投影行（交付功能 sheet） | **{len(projections)}** |",
        f"| 已覆盖 | {by_status.get('已覆盖', 0)} |",
        f"| 部分覆盖 | {by_status.get('部分覆盖', 0)} |",
        f"| 缺源场景跳过 | {no_source} |",
        f"| 编号来自 A 线 v8 | {by_idsrc.get('A线v8', 0)} |",
        f"| 新号（无 A 匹配/冲突） | {by_idsrc.get('new(no-A-match)', 0) + by_idsrc.get('new(dup-A)', 0)} |",
        f"| A 线 v8 总功能点 | {len(v8_rows)}（含政策/综合等未做 B 册） |",
        "",
        "## 按册",
        "",
        "| 册 | 投影行 |",
        "|----|--------|",
    ]
    for b, n in sorted(by_book.items(), key=lambda x: -x[1]):
        lines.append(f"| `{b}` | {n} |")
    lines.extend(
        [
            "",
            "## 抽样对账（前 30 行）",
            "",
            "| 交付编号 | 功能点 | 状态 | 源场景 | 编号来源 |",
            "|----------|--------|------|--------|----------|",
        ]
    )
    for p in projections[:30]:
        lines.append(
            f"| `{p['delivery'][0]}` | {p['delivery'][6]} | {p['status']} | `{p['src']}` | {p['id_source']} |"
        )
    lines.extend(
        [
            "",
            "## 已知限制（本波）",
            "",
            "1. 步骤/预期为**规则化最小切片**（对准功能点、不加严）；若验收要求人工精炼切片，可按册回炉改投影。",
            "2. 未覆盖功能点未进表；政策 T19–T21、综合智能 T30–T32 无 B 线册，未纳入。",
            "3. 门户/查询/维护/对比篮等 A 线 N/A 册不进本表（无 v8 点可挂）。",
            "4. 非功能 sheet（兼容/集成/性能）仍为模板样例，放行前须清检。",
            "",
        ]
    )
    MANIFEST.write_text("\n".join(lines), encoding="utf-8")

    if new_ids:
        text = REGISTRY.read_text(encoding="utf-8")
        text2, nsub = re.subn(
            r"(KJZTFWXT:\n\s+FUNC:\s+)\d+",
            rf"\g<1>{next_seq}",
            text,
            count=1,
        )
        if nsub:
            REGISTRY.write_text(text2, encoding="utf-8")
        else:
            print("WARN: failed to patch code-registry next_seq; manual=", next_seq)

    # uniqueness check
    ids = [r[0] for r in all_rows]
    assert len(ids) == len(set(ids)), "交付编号重复"

    print(f"OK rows={len(all_rows)} → {OUT}")
    print(f"  已覆盖={by_status.get('已覆盖',0)} 部分覆盖={by_status.get('部分覆盖',0)} no_source={no_source}")
    print(f"  id A线v8={by_idsrc.get('A线v8',0)} new={len(new_ids)} next_seq→{next_seq if new_ids else 'unchanged'}")
    print(f"  manifest → {MANIFEST}")


if __name__ == "__main__":
    main()
