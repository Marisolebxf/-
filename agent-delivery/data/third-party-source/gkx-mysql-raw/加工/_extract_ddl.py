# -*- coding: utf-8 -*-
"""One-shot: extract gkx MySQL DDL from Cursor transcript into this sandbox."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\hzw\.cursor\projects\e-gkx-lumen-gkx-orchestration"
    r"\agent-transcripts\1f32dbcf-d513-40f5-821f-ee2c7be0473f"
    r"\1f32dbcf-d513-40f5-821f-ee2c7be0473f.jsonl"
)
OUT_DIR = Path(__file__).resolve().parent
MARKER = "CREATE TABLE `dwd_author_affiliation`"


def collect_texts(obj: object) -> list[str]:
    texts: list[str] = []
    if not isinstance(obj, dict):
        return texts
    msg = obj.get("message")
    if isinstance(msg, dict):
        content = msg.get("content")
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and "text" in c:
                    texts.append(str(c["text"]))
                elif isinstance(c, str):
                    texts.append(c)
    content = obj.get("content")
    if isinstance(content, str):
        texts.append(content)
    elif isinstance(content, list):
        for x in content:
            if isinstance(x, dict) and "text" in x:
                texts.append(str(x["text"]))
            elif isinstance(x, str):
                texts.append(x)
    for k in ("text", "user_query", "query"):
        v = obj.get(k)
        if isinstance(v, str):
            texts.append(v)
    return texts


def extract_ddl() -> str:
    chunks: list[str] = []
    for line in TRANSCRIPT.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        for t in collect_texts(obj):
            if MARKER in t:
                chunks.append(t)

    if not chunks:
        raw = TRANSCRIPT.read_text(encoding="utf-8", errors="replace")
        idx = raw.find(MARKER)
        if idx < 0:
            raise SystemExit("FAILED: marker not found in transcript")
        chunk = raw[idx:]
        chunk = chunk.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')
        chunks.append(chunk)

    ddl = max(chunks, key=len)
    start = ddl.find("-- gkx.dwd_author_affiliation")
    if start < 0:
        start = ddl.find(MARKER)
    if start > 0:
        ddl = ddl[start:]
    for stopper in ("\n</user_query>", "\nAs data-agent", "\n作为data-agent"):
        p = ddl.find(stopper)
        if p > 0:
            ddl = ddl[:p]
    # trim trailing JSON noise after last ); that looks like end of CREATE
    last = ddl.rfind(");")
    if last > 0:
        ddl = ddl[: last + 2] + "\n"
    return ddl


def analyze(ddl: str) -> dict:
    names = re.findall(r"CREATE TABLE `([^`]+)`", ddl)
    uniq = list(dict.fromkeys(names))
    prefixes = Counter()
    bak = []
    for n in uniq:
        if "_bak_" in n or n.endswith("_bak"):
            bak.append(n)
        if n.startswith("dwd_"):
            prefixes["dwd_*"] += 1
        elif n.startswith("ods_"):
            prefixes["ods_*"] += 1
        else:
            prefixes["other"] += 1
    return {
        "table_count": len(uniq),
        "duplicate_create_stmts": len(names) - len(uniq),
        "prefix_counts": dict(prefixes),
        "bak_count": len(bak),
        "tables": uniq,
        "bak_tables": bak,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ddl = extract_ddl()
    ddl_path = OUT_DIR / "gkx_schema_ddl.sql"
    header = (
        "-- ============================================================================\n"
        "-- Isolated sandbox: third-party MySQL schema dump for database `gkx`\n"
        "-- Source: user paste (Navicat/DBeaver style `-- gkx.<table> definition`)\n"
        "-- Purpose: structure analysis ONLY — do NOT load into demo_gdf_data /\n"
        "--          algo POC (117.50...) / production ADS pipelines.\n"
        "-- Extracted-from-transcript: 1f32dbcf-d513-40f5-821f-ee2c7be0473f\n"
        "-- ============================================================================\n\n"
    )
    ddl_path.write_text(header + ddl, encoding="utf-8")

    stats = analyze(ddl)
    inventory_path = OUT_DIR / "table_inventory.md"
    lines = [
        "# gkx（三方 MySQL）表清单 — 隔离沙箱",
        "",
        "> 仅结构盘点；不写生产、不灌 demo/算法库。",
        "",
        "## 统计",
        "",
        f"- CREATE TABLE 表数（去重）: **{stats['table_count']}**",
        f"- 重复 CREATE 语句: {stats['duplicate_create_stmts']}",
        f"- `dwd_*`: **{stats['prefix_counts'].get('dwd_*', 0)}**",
        f"- `ods_*`: **{stats['prefix_counts'].get('ods_*', 0)}**",
        f"- other: {stats['prefix_counts'].get('other', 0)}",
        f"- `*_bak_*` 备份表: **{stats['bak_count']}**",
        "",
        "## 分层说明（本项目口径）",
        "",
        "- 供应方表名大量叫 `dwd_*`，在本项目数据分层中应视为 **ODS 贴源层原料**，",
        "  不要与自建 DWD（如 `dwd.enterprise*`）混淆。",
        "- `ods_*` 为贴源侧镜像/上游表；`*_bak_20260710` 为历史备份，分析时可排除。",
        "",
        "## 全量表名",
        "",
    ]
    for i, n in enumerate(stats["tables"], 1):
        tag = " *(bak)*" if n in stats["bak_tables"] else ""
        lines.append(f"{i}. `{n}`{tag}")
    inventory_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # machine-readable list
    (OUT_DIR / "table_list.txt").write_text(
        "\n".join(stats["tables"]) + "\n", encoding="utf-8"
    )

    print(f"wrote {ddl_path} ({ddl_path.stat().st_size} bytes)")
    print(f"tables={stats['table_count']} dwd={stats['prefix_counts'].get('dwd_*')} "
          f"ods={stats['prefix_counts'].get('ods_*')} bak={stats['bak_count']}")


if __name__ == "__main__":
    main()
