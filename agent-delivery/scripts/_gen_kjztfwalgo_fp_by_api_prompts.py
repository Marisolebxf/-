# -*- coding: utf-8 -*-
"""Generate by-api prompts L01–L60. Does not write work tables. Stdlib only."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "qa/total-set/KJZTFWALGO/fp-split-by-api-run"
OLD_WORK = ROOT / "qa/total-set/KJZTFWALGO/fp-split-run/work"
INV = json.loads((ROOT / "qa/total-set/KJZTFWALGO/fp-split-run/_inventory.json").read_text(encoding="utf-8"))
CAT = Path(r"d:/work/gkx-lumen/repos/lumen-ui-algo-apiview/src/catalog")
MAP = RUN / "_l6-to-catalog-map.yaml"
TPL = (RUN / "prompts/_template.md").read_text(encoding="utf-8")

FOCUS = {
    "T01": "基础指标：开篇点名的统计接口按 path 分计；规则层按接口，禁止九类维度 × 空态。",
    "T02": "图谱：ner/intra/hang 等按 path 分计；与兄弟六级共享 path 时本六级只写本页职责，合表去重。",
    "T03": "产业链分析页：一页一模型；catalog 无独立页的弱挂只拆需规已写且本页列出的 path。",
    "T04": "企业深度：对齐金样 L31 接口级拆法，禁止抄技术力 path 到本六级。",
    "T05": "政策：focus 与 focus-one 同能力变体按 path 去重。",
    "T06": "服务机构：多页共用 `/entan/v1/svc/models` 时按本页 title/入参区分验收，path 合表仍去重。",
    "T07": "综合：整库 local_mock，功能点须标明 Mock/契约未交付。",
}


def extract_spec(text: str) -> str:
    m = re.search(r"## 需规原文\s*\n(.*?)(?=\n\| 子功能项|\n## 绑定接口)", text, re.S)
    return m.group(1).strip() if m else ""


def load_pages() -> dict:
    out = {}
    for name in ("entan", "chain", "policy", "svc", "comp", "innov"):
        for p in json.loads((CAT / f"{name}.json").read_text(encoding="utf-8")):
            out[p["id"]] = p
    return out


def load_map() -> dict:
    text = MAP.read_text(encoding="utf-8")
    rows = {}
    for m in re.finditer(
        r"^\s+(L\d+):\s*\{([^}]+)\}", text, re.M
    ):
        lid, body = m.group(1), m.group(2)
        v_m = re.search(r"v:\s*(\w+)", body)
        pages = re.findall(r"[a-z]+\.[a-z0-9-]+", body)
        note_m = re.search(r'note:\s*(.+)$', body)
        rows[lid] = {
            "v": v_m.group(1) if v_m else "none",
            "pages": pages,
            "note": note_m.group(1).strip() if note_m else "",
        }
    return rows


def fmt_eps(page: dict) -> str:
    lines = [
        f"### `{page.get('id')}` {page.get('title')} (`{page.get('menuPath')}`)",
        "",
        "| method | path | status | runtime | title |",
        "|---|---|---|---|---|",
    ]
    seen = set()
    for e in page.get("endpoints") or []:
        key = f"{e.get('method', 'GET')} {e.get('path') or ''}"
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| {e.get('method', 'GET')} | `{e.get('path') or '（空 path）'}` | "
            f"{e.get('status') or ''} | {e.get('runtime') or ''} | {e.get('title') or ''} |"
        )
        params = e.get("params") or []
        names = [p.get("name") for p in params if p.get("name")]
        if names:
            lines.append(f"| | 入参点名：{'、'.join(names)} | | | |")
        fields = e.get("responseFields") or []
        fnames = [f.get("name") for f in fields if f.get("name")]
        if fnames:
            lines.append(f"| | 顶层结果体：{'、'.join(fnames[:12])}{'…' if len(fnames) > 12 else ''} | | | |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    pages = load_pages()
    mmap = load_map()
    out_dir = RUN / "prompts"
    n = 0
    for t in INV["tasks"]:
        lid = t["id"]
        spec = extract_spec((OLD_WORK / f"{lid}.md").read_text(encoding="utf-8"))
        bind = mmap.get(lid) or {"v": "none", "pages": [], "note": ""}
        titles = []
        ep_blocks = []
        for pid in bind["pages"]:
            p = pages.get(pid)
            if not p:
                ep_blocks.append(f"### `{pid}`（快照中无此页）\n")
                continue
            titles.append(p.get("title") or pid)
            ep_blocks.append(fmt_eps(p))
        page_title = " / ".join(titles) if titles else "整模型（需规-only）"
        page_ids = ", ".join(bind["pages"]) if bind["pages"] else "（无）"
        note = bind.get("note") or ""
        判定 = bind["v"] + (f"（{note}）" if note else "")
        接口块 = "\n".join(ep_blocks) if ep_blocks else "（本六级无 catalog 页，只按需规拆接口语义，并在 review 记 catalog 缺口）"
        text = TPL
        repl = {
            "{Lxx}": lid,
            "{三级}": t["l3"],
            "{四级}": t["l4"],
            "{五级}": t["l5"],
            "{六级}": t["l6"],
            "{页title}": page_title,
            "{页ids}": page_ids,
            "{判定}": 判定,
            "{L6块}": spec,
            "{接口块}": 接口块,
            "{重点}": FOCUS.get(t["l5_group"], ""),
        }
        for k, v in repl.items():
            text = text.replace(k, v)
        # strip the instruction preamble of _template for Lxx files: keep from first 子 agent
        if text.startswith("# 五级"):
            idx = text.find("子 agent 只做")
            if idx > 0:
                text = f"# {lid} {t['l6']} · 功能点拆分提示词（by-api）\n\n" + text[idx:]
        (out_dir / f"{lid}.md").write_text(text, encoding="utf-8")
        n += 1
    print(f"wrote {n} prompts under {out_dir}")


if __name__ == "__main__":
    main()
