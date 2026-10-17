# -*- coding: utf-8 -*-
"""Generate by-api prompts L01–L60. Does not write work tables. Stdlib only."""
from __future__ import annotations

import json
import re
from pathlib import Path

AD = Path(__file__).resolve().parents[1]
ORCH = AD.parent
GKX_ROOT = ORCH.parent
RUN = AD / "qa/total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-run"
OLD_WORK = AD / "qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run/work"
INV = json.loads(
    (AD / "qa/total-set/SDWJSF-KJZTFWSFK/fp-split-run/_inventory.json").read_text(
        encoding="utf-8"
    )
)
CAT = GKX_ROOT / "repos" / "lumen-ui-algo-apiview" / "src" / "catalog"
MAP = RUN / "_l6-to-catalog-map.yaml"
TPL = (RUN / "prompts/_template.md").read_text(encoding="utf-8")

# v0.2 原则 4A：L05–L12 不挂 endpoint 列
GRAPH_DELEGATE_L6 = {f"L{i:02d}" for i in range(5, 13)}

FOCUS = {
    "T01": "v0.2 字段级：chain/entan/policy/svc.basic 各 endpoint 按 params+responseFields 拆行；禁止九维 × 空态笛卡尔积。",
    "T02": "4A：若本 ID 为 L05–L12，只写需规语义行，接口扩展列空，review「契约见 L13」。L13 挂图谱 endpoint 封闭清单。",
    "T03": "一页一模型；按本页 catalog endpoint.id 字段拆；弱挂六级不抄兄弟 path。",
    "T04": "企业深度：按本页 catalog 字段拆；禁止抄其它企业六级业务点。",
    "T05": "政策：同能力多 path 仍按 endpoint.id+field_key 分行，全库 3c 去重。",
    "T06": "服务机构：共用 path 时靠 endpoint.id/入参 field_key 区分验收。",
    "T07": "综合：local_mock → catalog_status=mock；仍字段级拆 catalog 已声明字段。",
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
        "| endpoint_id | method | path | status | runtime | title |",
        "|---|---|---|---|---|---|",
    ]
    seen = set()
    for e in page.get("endpoints") or []:
        eid = e.get("id") or ""
        key = eid or f"{e.get('method', 'GET')} {e.get('path') or ''}"
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| `{eid}` | {e.get('method', 'GET')} | `{e.get('path') or '（空 path）'}` | "
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
        if lid in GRAPH_DELEGATE_L6:
            接口块 = (
                "**原则 4A**：本六级（L05–L12）**不挂** catalog endpoint。"
                " work/review 中 `endpoint_id`/`METHOD`/`path`/`field_key` 留空；"
                "review 须写「契约见 L13」。仅按需规写可验收语义行，`catalog_status=req_only`。"
            )
        elif ep_blocks:
            接口块 = "\n".join(ep_blocks)
        else:
            接口块 = (
                "（本六级无 catalog 页：按需规拆行，接口扩展列空，`catalog_status=req_only`，"
                "review 记 catalog 缺口）"
            )
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
                text = (
                    f"# {lid} {t['l6']} · 功能点拆分提示词（by-api v0.2）\n\n"
                    + text[idx:]
                )
        (out_dir / f"{lid}.md").write_text(text, encoding="utf-8")
        n += 1
    print(f"wrote {n} prompts under {out_dir}")


if __name__ == "__main__":
    main()
