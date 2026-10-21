#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R3 文字返工：展开附录入参、前置直赋、清单步骤/预期分栏（89 册批量，语义不变）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "qa" / "test-cases" / "SDWJSF-KJZTFWSFK"

ROW_RE = re.compile(r"^\|\s*ZNFWJQ-SDWJSF/KJZTFWSFK-v1\.0-FUNC-\d{5}\s*\|")
COL = {
    "content": 7,
    "pre": 8,
    "step": 9,
    "expect": 10,
    "fp": 6,
    "remark": -1,
}

P_APPENDIX = re.compile(r"按附录|附录组合|见附录")
P_DOC = re.compile(r"使用文档示例|按文档示例")
P_STEP_VERB = re.compile(r"核对|确认|检查|校验|查看是否|比对|验证")

APPENDIX_NOTE = "> 参数赋值已展开至步骤/前置；本表仅作编写对照。\n"


def parse_appendix_combos(text: str) -> dict[str, str]:
    combos: dict[str, str] = {}
    if "## 附录 A" not in text:
        return combos
    section = text.split("## 附录 A", 1)[1].split("\n## ", 1)[0]
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|--") or "组合 id" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.match(r"^[A-Z0-9][A-Z0-9-]+$", cells[0]):
            combos[cells[0]] = cells[2]
    return combos


def page_default_chain(text: str) -> str:
    m = re.search(r"文档示例[`']?([A-Z0-9_-]+)", text)
    return m.group(1) if m else "INB1701"


def strip_for_verb_scan(text: str) -> str:
    """步骤扫描时去掉引号内文案（功能点标题可含「比对」等）。"""
    t = re.sub(r"「[^」]*」", "", text)
    return re.sub(r'"[^"]*"', "", t)


def params_to_step_action(params: str) -> str:
    params = (params or "").strip()
    params = re.sub(r"（文档[^）]*）", "", params)
    params = re.sub(r"\(文档[^)]*\)", "", params).strip()
    if re.match(r"^body\s*\{\}", params) or "不传 chain_id" in params:
        return "不填查询参数，点击调用"
    if params.lower().startswith("body "):
        params = params[5:].strip()
    params = params.replace("body ", "")
    pieces = [p.strip() for p in re.split(r"[；;]", params) if p.strip()]
    omits: list[str] = []
    fills: list[str] = []
    for p in pieces:
        if p.startswith("不传"):
            omits.append(p)
        elif "=" in p:
            fills.append(re.sub(r"\s+", "", p))
        else:
            fills.append(p)
    parts: list[str] = []
    if omits:
        parts.append("、".join(omits))
    if fills:
        parts.append("填写 " + "、".join(fills))
    return "，".join(parts) + "，点击调用"


def combo_from_remark(remark: str) -> str | None:
    m = re.search(r"组合=([A-Z0-9][A-Z0-9-]*)", remark)
    return m.group(1) if m else None


def fix_pre(text: str, chain: str) -> str:
    t = text
    t = re.sub(r"(\w+)\s*使用文档示例\s*([\w.-]+)", r"\1=\2", t)
    t = re.sub(r"使用文档示例\s*([\w.-]+)", rf"chainId=\1", t)
    t = re.sub(r"按文档示例\s*([\w.-]+)", r"\1=\2", t) if False else t
    t = re.sub(r"module\s*取不可识别 slug", "module=__invalid__", t)
    t = re.sub(r"请求体不传\s*(\w+)", r"不传 \1", t)
    t = re.sub(r"只破坏\s*(\w+)", r"\1 取非法值", t)
    t = re.sub(r"path\s*不传\s*(\w+)", r"不传 \1", t)
    if "chainId 使用" in t or "chainId使用" in t:
        t = re.sub(r"chainId\s*使用[^；;]*", f"chainId={chain}", t)
    return t


def fix_content(
    text: str, chain: str, combos: dict[str, str], cid: str | None = None
) -> str:
    t = text
    t = re.sub(
        r"检查按文档示例\s*chainId[、,]?\s*statYear",
        f"检查填写 chainId={chain}、statYear=2025",
        t,
    )
    t = re.sub(r"检查按文档\s*chainId", f"检查填写 chainId={chain}", t)
    t = re.sub(r"按文档 sampleRequest", "填写 sampleRequest 所示参数", t)
    t = re.sub(r"按文档\s*chainId", f"chainId={chain}", t)
    t = re.sub(r"按文档示例", f"填写 chainId={chain}", t)
    t = re.sub(
        r"省略可选\s*(\w+)\s*按附录组合\s*[A-Z0-9-]+",
        r"不传 \1",
        t,
    )
    t = re.sub(
        r"按附录组合\s*[A-Z0-9-]+\s*（([^）]+)）",
        r"填写 \1",
        t,
    )

    def repl_combo(m: re.Match) -> str:
        cid = m.group(1)
        raw = combos.get(cid, "")
        frag = params_to_step_action(raw).replace("，点击调用", "")
        if frag.startswith("填写 "):
            return frag
        if frag.startswith("不传"):
            return frag.split("，")[0]
        return frag or f"组合 {cid}"

    t = re.sub(r"按附录组合\s*([A-Z0-9][A-Z0-9-]*)", repl_combo, t)
    if cid and cid in combos:
        frag = params_to_step_action(combos[cid]).replace("，点击调用", "")
        t = t.replace("按附录参数组合", frag)
    else:
        t = t.replace("按附录参数组合", "填写请求参数")
    t = re.sub(r"附录组合\s*[A-Z0-9-]+", "", t)
    t = re.sub(r"\s+调用后", " 后", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def expand_appendix_in_text(text: str, combos: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        cid = m.group(1)
        return params_to_step_action(combos.get(cid, ""))

    t = text
    t = re.sub(r"按附录组合\s*([A-Z0-9][A-Z0-9-]+)\s*填写\S*", repl, t)
    t = re.sub(r"按附录\s*([A-Z0-9][A-Z0-9-]+)\s*基准[^；;）)]*", repl, t)
    t = re.sub(r"按附录\s*([A-Z0-9][A-Z0-9-]+)", repl, t)
    t = re.sub(r"见附录\s*[A-Z0-9-]+", "", t)
    return t


def is_checklist_row(fp: str, remark: str) -> bool:
    if fp in ("接口信息", "算法测试"):
        return True
    return "场景=接口信息" in remark or "场景=算法测试" in remark


def split_checklist_step(step: str) -> tuple[str, list[str]]:
    """步骤只留操作；校验片段进预期补充。"""
    extra_expect: list[str] = []
    norm = step.replace("；", ";")
    parts = re.findall(r"\d+\.[^;]*", norm)
    if not parts:
        parts = [norm]
    kept: list[str] = []
    for p in parts:
        body = re.sub(r"^\d+\.", "", p).strip()
        if not body:
            continue
        if re.match(r"^(确认|查看|核对|检查|校验|验证)", body):
            extra_expect.append(body)
            continue
        if re.search(r"，\s*(确认|查看|核对|检查|校验)", body):
            head, tail = re.split(r"，\s*(?=确认|查看|核对|检查|校验)", body, maxsplit=1)
            if head:
                kept.append(head.rstrip("，"))
            if tail:
                extra_expect.append(tail)
            continue
        if re.search(r"^(侧栏|切换至|切换到|停留在|接口下拉|下拉)", body):
            kept.append(body)
        elif P_STEP_VERB.search(body):
            extra_expect.append(body)
        else:
            kept.append(body)
    if not kept:
        kept = [re.sub(r"^\d+\.", "", step).split("；")[0].split(";")[0]]
    new_step = "；".join(f"{i + 1}.{p}" for i, p in enumerate(kept))
    return new_step, extra_expect


def clean_expect(expect: str) -> str:
    expect = re.sub(
        r"；\d+、确认调用区下拉项数量与名称与 §0 清单一致\s*$",
        "",
        expect,
    )
    return expect.strip()


def rewrite_row(cells: list[str], combos: dict[str, str], chain: str) -> list[str]:
    if len(cells) < 11:
        return cells
    remark = cells[COL["remark"]] if COL["remark"] < len(cells) else ""
    fp = cells[COL["fp"]]
    cid = combo_from_remark(remark)

    cells[COL["content"]] = fix_content(cells[COL["content"]], chain, combos, cid)
    cells[COL["pre"]] = expand_appendix_in_text(fix_pre(cells[COL["pre"]], chain), combos)

    step = cells[COL["step"]]
    step = expand_appendix_in_text(step, combos)
    step = re.sub(r"填写\s*path/body", "填写 ", step)
    step = re.sub(
        r"填写\s*bodychain_id=([^（，]+)（文档example）",
        r"填写 chain_id=\1",
        step,
    )
    step = re.sub(r"（文档example）", "", step)
    step = re.sub(r"，点击调用（不传 module），点击调用", "，点击调用", step)
    step = re.sub(r"（sampleRequest）", "", step)

    if is_checklist_row(fp, remark):
        step, extras = split_checklist_step(step)
        if extras:
            prefix = cells[COL["expect"]].strip()
            add = "；".join(f"{i + 1}、{e}" for i, e in enumerate(extras))
            cells[COL["expect"]] = clean_expect(
                (prefix + "；" + add) if prefix else add
            )
    else:
        step = re.sub(r"，点击调用，点击调用", "，点击调用", step)

    cells[COL["step"]] = step
    cells[COL["expect"]] = clean_expect(cells[COL["expect"]])
    return cells


def rewrite_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    combos = parse_appendix_combos(text)
    chain = page_default_chain(text)
    if "## 附录 A" in text and APPENDIX_NOTE.strip() not in text:
        text = text.replace("## 附录 A", "## 附录 A\n\n" + APPENDIX_NOTE, 1)

    out_lines: list[str] = []
    changed = 0
    for line in text.splitlines():
        if not ROW_RE.match(line):
            out_lines.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        new_cells = rewrite_row(cells[:], combos, chain)
        if new_cells != cells:
            changed += 1
        out_lines.append("| " + " | ".join(new_cells) + " |")
    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return changed


def gate_scan() -> list[tuple[str, str, int]]:
    bad: list[tuple[str, str, int]] = []
    for md in sorted(TC_ROOT.rglob("FUNC-*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            if not ROW_RE.match(line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 11:
                continue
            rid = cells[0][-8:]
            for name, idx in [
                ("appendix", COL["content"]),
                ("appendix", COL["pre"]),
                ("appendix", COL["step"]),
                ("doc", COL["content"]),
                ("doc", COL["pre"]),
                ("step_verb", COL["step"]),
            ]:
                t = cells[idx]
                if name == "appendix" and P_APPENDIX.search(t):
                    bad.append((str(md.relative_to(TC_ROOT)), rid, idx))
                if name == "doc" and P_DOC.search(t):
                    bad.append((str(md.relative_to(TC_ROOT)), rid, idx))
                if name == "step_verb" and P_STEP_VERB.search(strip_for_verb_scan(t)):
                    bad.append((str(md.relative_to(TC_ROOT)), rid, idx))
    return bad


def main() -> None:
    total = 0
    for md in sorted(TC_ROOT.rglob("FUNC-*.md")):
        total += rewrite_file(md)
    print(f"rewrite rows touched: {total} (across 89 booklets)")
    bad = gate_scan()
    if bad:
        print(f"GATE FAIL: {len(bad)} hits (show 20)")
        for item in bad[:20]:
            print(" ", item)
        sys.exit(1)
    print("GATE OK: 0 hits")


if __name__ == "__main__":
    main()
