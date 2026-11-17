#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把本地 Markdown 写入飞书在线文档；```mermaid 转为「文本绘图」小组件（block_type=40）。

用法：
  python md_to_feishu_docx.py --md <本地.md> --folder-token <目录token> [--title 标题]
  python md_to_feishu_docx.py --md <本地.md> --document-id <已有docx id>   # 追加到已有文档末尾
  正式写入默认执行；加 --dry-run 只解析不写。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://open.feishu.cn/open-apis"
MERMAID_COMPONENT = "blk_631fefbbae02400430b8f9f4"
FENCE = chr(96) * 3  # ```
PREFIXES = ("FEISHU_DRIVE_APP", "LARK_APP", "FEISHU_APP")


def load_creds():
    env_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".env"
    )
    dotenv = {}
    if os.path.isfile(env_path):
        for line in open(env_path, encoding="utf-8", errors="replace"):
            m = re.match(r"\s*([A-Z_]+)\s*=\s*(.*?)\s*$", line)
            if m and m.group(2):
                dotenv.setdefault(m.group(1), m.group(2).strip("\"'"))
    for src in (os.environ, dotenv):
        for p in PREFIXES:
            if src.get(p + "_ID") and src.get(p + "_SECRET"):
                return src[p + "_ID"], src[p + "_SECRET"]
    sys.exit("[x] 缺少 FEISHU_DRIVE_APP_ID / FEISHU_DRIVE_APP_SECRET")


def get_token(app_id, secret):
    req = urllib.request.Request(
        BASE + "/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": secret}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    r = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    if r.get("code") != 0:
        sys.exit("[x] 取令牌失败: %s" % r)
    return r["tenant_access_token"]


def api(method, path, tat, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": "Bearer " + tat,
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8", "replace"))


def plain(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", s)
    return s.replace("**", "").replace("`", "")


def text_block(content, btype=2):
    key = {
        2: "text",
        3: "heading1",
        4: "heading2",
        5: "heading3",
        6: "heading4",
        7: "heading5",
        12: "bullet",
        13: "ordered",
        15: "quote",
    }[btype]
    return {
        "block_type": btype,
        key: {"elements": [{"text_run": {"content": content[:15000]}}]},
    }


def code_block(content, language=39):
    return {
        "block_type": 14,
        "code": {
            "style": {"language": language, "wrap": True},
            "elements": [{"text_run": {"content": content[:15000]}}],
        },
    }


def mermaid_block(src: str):
    src = src.replace("<br/>", "\n").replace("<br>", "\n").strip()
    record = json.dumps(
        {"data": src, "theme": "default", "view": "codeChart"}, ensure_ascii=False
    )
    return {
        "block_type": 40,
        "add_ons": {"component_type_id": MERMAID_COMPONENT, "record": record},
    }


def divider():
    return {"block_type": 22, "divider": {}}


def parse_md(text: str):
    blocks = []
    lines = text.splitlines()
    i = 0
    mermaid_fence = FENCE + "mermaid"
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == mermaid_fence:
            j = i + 1
            buf = []
            while j < len(lines) and lines[j].strip() != FENCE:
                buf.append(lines[j])
                j += 1
            blocks.append(("mermaid", "\n".join(buf)))
            i = j + 1
            continue
        if stripped.startswith(FENCE):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith(FENCE):
                buf.append(lines[j])
                j += 1
            blocks.append(("code", "\n".join(buf)))
            i = j + 1
            continue
        if stripped == "---":
            blocks.append(("hr", ""))
            i += 1
            continue
        if line.startswith("###### "):
            blocks.append(("h5", line[7:].strip()))
            i += 1
            continue
        if line.startswith("##### "):
            blocks.append(("h5", line[6:].strip()))
            i += 1
            continue
        if line.startswith("#### "):
            blocks.append(("h4", line[5:].strip()))
            i += 1
            continue
        if line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
            i += 1
            continue
        if line.startswith("# "):
            blocks.append(("h1", line[2:].strip()))
            i += 1
            continue
        if line.startswith("> "):
            buf = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            blocks.append(("quote", "\n".join(buf)))
            continue
        if re.match(r"^\|.+\|$", stripped) and i + 1 < len(lines) and re.match(
            r"^\|[\s\-:|]+\|$", lines[i + 1].strip()
        ):
            buf = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                buf.append(lines[i])
                i += 1
            rows = []
            for li, raw in enumerate(buf):
                if li == 1 and re.match(r"^\|[\s\-:|]+\|$", raw.strip()):
                    continue
                cells = [plain(c.strip()) for c in raw.strip().strip("|").split("|")]
                rows.append(cells)
            if rows:
                blocks.append(("table", rows))
            continue
        if re.match(r"^\d+\.\s+", line):
            blocks.append(("ol", re.sub(r"^\d+\.\s+", "", line)))
            i += 1
            continue
        if re.match(r"^[-*]\s+", line):
            blocks.append(("ul", re.sub(r"^[-*]\s+", "", line)))
            i += 1
            continue
        if not stripped:
            i += 1
            continue
        buf = [line]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith("#")
            and not lines[i].startswith(">")
            and not lines[i].startswith(FENCE)
            and not lines[i].startswith("|")
            and lines[i].strip() != "---"
            and not re.match(r"^[-*]\s+", lines[i])
            and not re.match(r"^\d+\.\s+", lines[i])
        ):
            buf.append(lines[i])
            i += 1
        blocks.append(("p", "\n".join(buf)))
    return blocks


def to_feishu(kind, content):
    if kind != "mermaid":
        content = plain(content)
    if kind == "h1":
        return text_block(content, 3)
    if kind == "h2":
        return text_block(content, 4)
    if kind == "h3":
        return text_block(content, 5)
    if kind == "h4":
        return text_block(content, 6)
    if kind == "h5":
        return text_block(content, 7)
    if kind == "p":
        return text_block(content, 2)
    if kind == "quote":
        return text_block(content, 15)
    if kind == "ul":
        return text_block(content, 12)
    if kind == "ol":
        return text_block(content, 13)
    if kind == "code":
        return code_block(content, 39)
    if kind == "mermaid":
        return mermaid_block(content)
    if kind == "hr":
        return divider()
    return text_block(content, 2)


def create_doc(tat, title, folder_token):
    out = api(
        "POST",
        "/docx/v1/documents",
        tat,
        {"title": title, "folder_token": folder_token},
    )
    if out.get("code") != 0:
        sys.exit("[x] 创建文档失败: %s" % out)
    return out["data"]["document"]["document_id"]


def append_block(tat, doc_id, block):
    out = api(
        "POST",
        "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, doc_id),
        tat,
        {"children": [block], "index": -1},
    )
    return out


def clear_doc(tat, doc_id):
    out = api("GET", "/docx/v1/documents/%s/blocks/%s" % (doc_id, doc_id), tat)
    if out.get("code") != 0:
        sys.exit("[x] 读文档根失败: %s" % out)
    n = len(out.get("data", {}).get("block", {}).get("children") or [])
    if n == 0:
        return 0
    out = api(
        "DELETE",
        "/docx/v1/documents/%s/blocks/%s/children/batch_delete?document_revision_id=-1"
        % (doc_id, doc_id),
        tat,
        {"start_index": 0, "end_index": n},
    )
    if out.get("code") != 0:
        sys.exit("[x] 清空文档失败: %s" % out)
    print("[i] cleared %d children" % n)
    return n


def fit_column_widths(rows, page_w=880, min_w=72, max_w=480):
    """按单元格内容权重分配列宽（px），贴近飞书正文可读宽度。"""
    ncols = max(len(r) for r in rows)
    weights = []
    for ci in range(ncols):
        mx = 4
        for r in rows:
            if ci >= len(r):
                continue
            # 中文约占 2 单位，英文 1；单格上限避免极长文案撑爆
            w = 0
            for ch in r[ci][:120]:
                w += 2 if ord(ch) > 127 else 1
            mx = max(mx, w)
        weights.append(mx)
    total = float(sum(weights)) or 1.0
    widths = []
    for w in weights:
        px = int(round(page_w * (w / total)))
        widths.append(max(min_w, min(max_w, px)))
    # 微调总和贴近 page_w
    diff = page_w - sum(widths)
    if widths and diff != 0:
        # 把差额摊到最宽列
        i = max(range(len(widths)), key=lambda k: widths[k])
        widths[i] = max(min_w, widths[i] + diff)
    return widths


def set_table_column_widths(tat, doc_id, table_block_id, widths):
    for i, w in enumerate(widths):
        out = api(
            "PATCH",
            "/docx/v1/documents/%s/blocks/%s?document_revision_id=-1" % (doc_id, table_block_id),
            tat,
            {"update_table_property": {"column_index": i, "column_width": int(w)}},
        )
        if out.get("code") != 0:
            print(
                "[x] col_width[%d]=%d fail: %s"
                % (i, w, json.dumps(out, ensure_ascii=False)[:200])
            )
        time.sleep(0.05)


def insert_table(tat, doc_id, rows):
    if not rows:
        return False
    cols = max(len(r) for r in rows)
    norm = []
    for r in rows:
        cells = list(r) + [""] * (cols - len(r))
        norm.append([c[:15000] for c in cells[:cols]])
    nrows, ncols = len(norm), cols
    widths = fit_column_widths(norm)
    # 飞书单次建表过大易失败：超 9 行拆成多表
    chunk = 9
    ok_any = False
    for start in range(0, nrows, chunk):
        part = norm[start : start + chunk]
        if start > 0:
            # 续表带表头
            part = [norm[0]] + part
        out = api(
            "POST",
            "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, doc_id),
            tat,
            {
                "children": [
                    {
                        "block_type": 31,
                        "table": {
                            "property": {
                                "row_size": len(part),
                                "column_size": ncols,
                                "header_row": True,
                                "column_width": widths,
                            }
                        },
                    }
                ],
                "index": -1,
            },
        )
        if out.get("code") != 0:
            # 部分环境不接受创建时带 column_width，降级后再 PATCH
            out = api(
                "POST",
                "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, doc_id),
                tat,
                {
                    "children": [
                        {
                            "block_type": 31,
                            "table": {
                                "property": {
                                    "row_size": len(part),
                                    "column_size": ncols,
                                    "header_row": True,
                                }
                            },
                        }
                    ],
                    "index": -1,
                },
            )
        if out.get("code") != 0:
            print("[x] table create fail: %s" % json.dumps(out, ensure_ascii=False)[:400])
            continue
        table = out["data"]["children"][0]
        table_id = table.get("block_id")
        cell_ids = table.get("children") or table.get("table", {}).get("cells") or []
        for i, cell_id in enumerate(cell_ids):
            ri, ci = divmod(i, ncols)
            if ri >= len(part) or ci >= ncols:
                continue
            txt = part[ri][ci] or " "
            out2 = api(
                "POST",
                "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, cell_id),
                tat,
                {"children": [text_block(txt, 2)], "index": 0},
            )
            if out2.get("code") != 0:
                # 空单元格常已有占位文本；改用追加
                out2 = api(
                    "POST",
                    "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, cell_id),
                    tat,
                    {"children": [text_block(txt, 2)], "index": -1},
                )
            if out2.get("code") != 0:
                print(
                    "[x] cell %s fail: %s"
                    % (cell_id, json.dumps(out2, ensure_ascii=False)[:240])
                )
            time.sleep(0.05)
        if table_id:
            set_table_column_widths(tat, doc_id, table_id, widths)
        ok_any = True
        print(
            "[ok] table %dx%d widths=%s"
            % (len(part), ncols, widths)
        )
        time.sleep(0.2)
    return ok_any


def append_parsed(tat, doc_id, parsed_items):
    ok = 0
    total = len(parsed_items)
    batch = []

    def flush():
        nonlocal ok, batch
        if not batch:
            return
        out = api(
            "POST",
            "/docx/v1/documents/%s/blocks/%s/children" % (doc_id, doc_id),
            tat,
            {"children": batch, "index": -1},
        )
        if out.get("code") != 0:
            for b in batch:
                out2 = append_block(tat, doc_id, b)
                if out2.get("code") != 0:
                    print(
                        "[x] skip type=%s err=%s"
                        % (b.get("block_type"), json.dumps(out2, ensure_ascii=False)[:300])
                    )
                else:
                    ok += 1
                time.sleep(0.1)
        else:
            ok += len(batch)
            print("[ok] inserted %d / ~%d" % (ok, total))
        batch = []
        time.sleep(0.2)

    for kind, content in parsed_items:
        if kind == "table":
            flush()
            if insert_table(tat, doc_id, content):
                ok += 1
            continue
        batch.append(to_feishu(kind, content))
        if len(batch) >= 15:
            flush()
    flush()
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--folder-token", default="")
    ap.add_argument("--document-id", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true", help="清空已有文档再写入（保留链接）")
    ap.add_argument("--mermaid-only", action="store_true", help="只写入标题说明 + 全部文本绘图")
    args = ap.parse_args()
    if not os.path.isfile(args.md):
        sys.exit("[x] 文件不存在: %s" % args.md)
    text = open(args.md, encoding="utf-8").read()
    parsed = parse_md(text)
    n_m = sum(1 for k, _ in parsed if k == "mermaid")
    n_t = sum(1 for k, _ in parsed if k == "table")
    print("[i] parsed blocks=%d mermaid=%d table=%d" % (len(parsed), n_m, n_t))
    if args.dry_run:
        for k, c in parsed:
            if k == "mermaid":
                print("--- mermaid ---\n%s\n" % c[:200])
            if k == "table":
                print("--- table %dx%d ---" % (len(c), len(c[0]) if c else 0))
        return

    tat = get_token(*load_creds())
    title = args.title or os.path.splitext(os.path.basename(args.md))[0]
    if args.document_id:
        doc_id = args.document_id
        if args.replace:
            clear_doc(tat, doc_id)
    else:
        if not args.folder_token:
            sys.exit("[x] 新建文档需要 --folder-token")
        doc_id = create_doc(tat, title, args.folder_token)
        print("[i] created doc", doc_id)

    note = text_block(
        "图用飞书「文本绘图」；表为飞书原生表格。Markdown 真源在编排仓；同目录另有 .md 云空间附件。",
        15,
    )
    if args.mermaid_only:
        items = [("quote", note["quote"]["elements"][0]["text_run"]["content"])]
        # mermaid-only path uses blocks directly
        children = [note]
        for n, (k, c) in enumerate(parsed, 1):
            if k != "mermaid":
                continue
            children.append(text_block("图 %d" % n, 5))
            children.append(mermaid_block(c))
        for b in children:
            append_block(tat, doc_id, b)
            time.sleep(0.1)
    else:
        append_parsed(tat, doc_id, [("quote", "图用飞书「文本绘图」；表为飞书原生表格。Markdown 真源在编排仓；同目录另有 .md 云空间附件。")] + parsed)
    print("[done] https://zhipu-ai.feishu.cn/docx/%s" % doc_id)


if __name__ == "__main__":
    main()
