# -*- coding: utf-8 -*-
"""从三方 MySQL gkx 按英文表名回填「数据行数」，并更新报告 MD。"""
from __future__ import annotations

import sys
from pathlib import Path as _Path

_SCRIPT_DIR = _Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import re
import time
from datetime import datetime
from pathlib import Path

import pymysql

from gen_gkx_report import extract_all, generate_md, order_libs
from _yuansuku_paths import ENV_PATH, excel_base, prev_search_dirs, report_dir

NOW = datetime.now()
TODAY_COMPACT = NOW.strftime("%Y%m%d-%H%M")
TODAY_ISO = NOW.strftime("%Y-%m-%d %H:%M")
BASE = excel_base()
OUT = report_dir() / f"GKX数据源表及行数报告-{TODAY_COMPACT}.MD"

# Excel 英文名 -> 库内实际表名（已知差异）
MANUAL_ALIASES = {
    "dwd_org_heis_info": "dwd_org_hels_info",  # 源表拼写 heis / 库表 hels
    "dws_zck_policy": "dwd_zck_policy",
    "hycy_pelagic_fishery_enterprises_performance_evaluation_results": (
        "dwd_hycy_pelagic_fishery_enterprise_eval_results"
    ),
    "hycy_shanghai_domestic_water_transportation_trading_directory": (
        "dwd_hycy_shanghai_domestic_water_transport_directory"
    ),
    "dwd_patent_cited": "ods_patent_cited",
    "dwd_bid_base_out": "ods_org_bid_base",
}


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def connect(env: dict[str, str]):
    return pymysql.connect(
        host=env["GKX_ODS_MYSQL_HOST"],
        port=int(env["GKX_ODS_MYSQL_PORT"]),
        user=env["GKX_ODS_MYSQL_USER"],
        password=env["GKX_ODS_MYSQL_PASSWORD"],
        database=env["GKX_ODS_MYSQL_DB"],
        charset="utf8mb4",
        connect_timeout=30,
        read_timeout=600,
        write_timeout=60,
        autocommit=True,
    )


def list_db_tables(conn) -> dict[str, dict]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT TABLE_NAME, TABLE_ROWS
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_TYPE = 'BASE TABLE'
        """
    )
    tables: dict[str, dict] = {}
    for name, approx in cur.fetchall():
        tables[name.lower()] = {
            "name": name,
            "approx_rows": int(approx or 0),
            "has_is_deleted": False,
        }

    cur.execute(
        """
        SELECT TABLE_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND COLUMN_NAME = 'is_deleted'
        """
    )
    for (name,) in cur.fetchall():
        key = name.lower()
        if key in tables:
            tables[key]["has_is_deleted"] = True
    cur.close()
    return tables


def resolve_physical_table(en_name: str, db_tables: dict[str, dict]) -> tuple[str | None, str]:
    """返回 (物理表名, 匹配方式)。"""
    en = (en_name or "").strip()
    if not en or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", en):
        return None, "invalid"

    key = en.lower()
    if key in MANUAL_ALIASES:
        alias = MANUAL_ALIASES[key]
        if alias.lower() in db_tables:
            return db_tables[alias.lower()]["name"], "manual_alias"

    if key in db_tables:
        return db_tables[key]["name"], "exact"

    # 已是 dwd_/dws_ 前缀：仅在同前缀内查找，避免静默落到 ods_*
    if key.startswith("dwd_") or key.startswith("dws_"):
        stem = key[4:]
        cand = f"dwd_{stem}"
        if cand in db_tables:
            return db_tables[cand]["name"], "prefix"
        return None, "missing"

    # 无前缀名：优先 dwd_，再 ods_
    for cand, how in ((f"dwd_{key}", "prefix"), (f"ods_{key}", "prefix")):
        if cand in db_tables:
            return db_tables[cand]["name"], how

    return None, "missing"


def exact_count(conn, table_name: str, has_is_deleted: bool) -> tuple[int, int | None]:
    """返回 (业务行数, 全表行数或 None)。"""
    if not re.fullmatch(r"[A-Za-z0-9_]+", table_name):
        raise ValueError(f"非法表名: {table_name}")
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    total = int(cur.fetchone()[0])
    if has_is_deleted:
        cur.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE `is_deleted` = 0")
        alive = int(cur.fetchone()[0])
        cur.close()
        return alive, total
    cur.close()
    return total, None


def collect_english_names(all_libs) -> list[str]:
    names = []
    seen = set()
    for tables in all_libs.values():
        for (_cn, en), _info in tables.items():
            en = (en or "").strip()
            if not en:
                continue
            key = en.lower()
            if key in seen:
                continue
            seen.add(key)
            names.append(en)
    return names


def format_count(n: int) -> str:
    return f"{n:,}"


def parse_row_number(raw: str) -> int | None:
    """从报告单元格解析业务行数；无法解析为数字时返回 None。"""
    raw = (raw or "").strip()
    if not raw or raw in {"未提供", "库中无此表"}:
        return None
    match = re.match(r"^([\d,]+)", raw)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def parse_report_inventory(path: Path) -> tuple[str | None, dict[str, dict]]:
    """解析报告表清单，返回 (生成日期, {en_lower: info})。"""
    text = path.read_text(encoding="utf-8")
    date_m = re.search(r"> 生成日期：(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)", text)
    report_date = date_m.group(1) if date_m else None

    if "## 表清单（按要素库分组）" not in text:
        return report_date, {}
    section = text.split("## 表清单（按要素库分组）", 1)[1]
    if "## 表字段明细" in section:
        section = section.split("## 表字段明细", 1)[0]

    tables: dict[str, dict] = {}
    current_lib = ""
    for line in section.splitlines():
        if line.startswith("### "):
            current_lib = line[4:].strip()
            continue
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 5:
            continue
        if cols[0] in {"序号", ":---:"} or cols[0].startswith(":"):
            continue
        cn_cell, en_cell, row_cell, field_cell = cols[1], cols[2], cols[3], cols[4]
        cn_m = re.search(r"\[([^\]]+)\]", cn_cell)
        cn = cn_m.group(1) if cn_m else cn_cell
        en = en_cell.strip().strip("`")
        if not en:
            continue
        try:
            field_count = int(field_cell.replace(",", ""))
        except ValueError:
            continue
        tables[en.lower()] = {
            "lib": current_lib,
            "cn": cn,
            "en": en,
            "rows": parse_row_number(row_cell),
            "rows_raw": row_cell,
            "fields": field_count,
        }
    return report_date, tables


def find_previous_report(base: Path, current: Path) -> Path | None:
    """选取除当前文件外、最近修改的历史报告（含旧目录快照）。"""
    search_dirs = [base]
    for d in prev_search_dirs():
        if d not in search_dirs:
            search_dirs.append(d)

    candidates = []
    seen = set()
    for directory in search_dirs:
        if not directory.exists():
            continue
        for pattern in ("GKX数据源表及行数报告*.MD", "GKX数据源表及行数报告*.md"):
            for p in directory.glob(pattern):
                resolved = p.resolve()
                if resolved == current.resolve() or resolved in seen:
                    continue
                seen.add(resolved)
                candidates.append(p)
    if not candidates:
        return None
    candidates.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return candidates[0]


def delta_text(old: int | None, new: int | None) -> str:
    if old is None and new is None:
        return "-"
    if old is None:
        return "首次计数"
    if new is None:
        return "本次缺失"
    diff = new - old
    if diff == 0:
        return "0"
    return f"+{diff:,}" if diff > 0 else f"{diff:,}"


def build_comparison_section(
    prev_path: Path | None,
    curr_tables: dict[str, dict],
    curr_date: str,
    curr_name: str,
) -> list[str]:
    if prev_path is None or not prev_path.exists():
        return [
            "## 与上次对比",
            "",
            "> 未找到可对比的历史报告文件。",
            "",
        ]

    prev_date, prev_tables = parse_report_inventory(prev_path)

    all_keys = sorted(
        set(prev_tables) | set(curr_tables),
        key=lambda k: (
            (curr_tables.get(k) or prev_tables.get(k) or {}).get("lib", ""),
            (curr_tables.get(k) or prev_tables.get(k) or {}).get("en", k),
        ),
    )

    changed_rows: list[dict] = []
    changed_fields: list[dict] = []
    added: list[dict] = []
    removed: list[dict] = []
    unchanged = 0

    for key in all_keys:
        old = prev_tables.get(key)
        new = curr_tables.get(key)
        if old and not new:
            removed.append(old)
            continue
        if new and not old:
            added.append(new)
            continue
        assert old is not None and new is not None
        old_missing = old["rows_raw"] == "库中无此表"
        new_missing = new["rows_raw"] == "库中无此表"
        row_changed = (old["rows"] != new["rows"]) or (old_missing != new_missing)
        field_changed = old["fields"] != new["fields"]
        if not row_changed and not field_changed:
            unchanged += 1
            continue
        item = {
            "lib": new["lib"] or old["lib"],
            "cn": new["cn"] or old["cn"],
            "en": new["en"] or old["en"],
            "old_rows": old["rows"],
            "new_rows": new["rows"],
            "old_rows_raw": old["rows_raw"],
            "new_rows_raw": new["rows_raw"],
            "old_fields": old["fields"],
            "new_fields": new["fields"],
        }
        if row_changed:
            changed_rows.append(item)
        if field_changed:
            changed_fields.append(item)

    def fmt_rows(v: int | None, raw: str | None = None) -> str:
        if v is None:
            return raw or "—"
        return f"{v:,}"

    lines = [
        "## 与上次对比",
        "",
        f"> 对比基准：`{prev_path.name}`"
        + (f"（生成日期 {prev_date}）" if prev_date else "")
        + f" → 本次 `{curr_name}`（生成日期 {curr_date}）",
        "",
        "### 对比总览",
        "",
        "| 指标 | 数量 |",
        "|:---|---:|",
        f"| 上次表数 | {len(prev_tables)} |",
        f"| 本次表数 | {len(curr_tables)} |",
        f"| 行数变化表 | {len(changed_rows)} |",
        f"| 字段数变化表 | {len(changed_fields)} |",
        f"| 新增表 | {len(added)} |",
        f"| 删除表 | {len(removed)} |",
        f"| 无变化表 | {unchanged} |",
        "",
    ]

    lines.extend(
        [
            "### 行数变化明细",
            "",
        ]
    )
    if not changed_rows:
        lines.append("*无行数变化*")
        lines.append("")
    else:
        # 变化量大的优先
        changed_rows.sort(
            key=lambda x: abs((x["new_rows"] or 0) - (x["old_rows"] or 0)),
            reverse=True,
        )
        lines.append(
            "| 序号 | 要素库 | 表中文名 | 英文表名 | 上次行数 | 本次行数 | 行数变化 |"
        )
        lines.append("|:---:|:---|:---|:---|---:|---:|---:|")
        for i, item in enumerate(changed_rows, 1):
            lines.append(
                f"| {i} | {item['lib']} | {item['cn']} | `{item['en']}` | "
                f"{fmt_rows(item['old_rows'], item['old_rows_raw'])} | "
                f"{fmt_rows(item['new_rows'], item['new_rows_raw'])} | "
                f"{delta_text(item['old_rows'], item['new_rows'])} |"
            )
        lines.append("")

    lines.extend(
        [
            "### 字段数变化明细",
            "",
        ]
    )
    if not changed_fields:
        lines.append("*无字段数变化*")
        lines.append("")
    else:
        changed_fields.sort(
            key=lambda x: abs(x["new_fields"] - x["old_fields"]),
            reverse=True,
        )
        lines.append(
            "| 序号 | 要素库 | 表中文名 | 英文表名 | 上次字段数 | 本次字段数 | 字段变化 |"
        )
        lines.append("|:---:|:---|:---|:---|---:|---:|---:|")
        for i, item in enumerate(changed_fields, 1):
            lines.append(
                f"| {i} | {item['lib']} | {item['cn']} | `{item['en']}` | "
                f"{item['old_fields']} | {item['new_fields']} | "
                f"{delta_text(item['old_fields'], item['new_fields'])} |"
            )
        lines.append("")

    if added:
        lines.extend(["### 新增表", ""])
        lines.append("| 序号 | 要素库 | 表中文名 | 英文表名 | 本次行数 | 字段数 |")
        lines.append("|:---:|:---|:---|:---|---:|---:|")
        for i, item in enumerate(added, 1):
            lines.append(
                f"| {i} | {item['lib']} | {item['cn']} | `{item['en']}` | "
                f"{fmt_rows(item['rows'], item['rows_raw'])} | {item['fields']} |"
            )
        lines.append("")

    if removed:
        lines.extend(["### 删除表", ""])
        lines.append("| 序号 | 要素库 | 表中文名 | 英文表名 | 上次行数 | 字段数 |")
        lines.append("|:---:|:---|:---|:---|---:|---:|")
        for i, item in enumerate(removed, 1):
            lines.append(
                f"| {i} | {item['lib']} | {item['cn']} | `{item['en']}` | "
                f"{fmt_rows(item['rows'], item['rows_raw'])} | {item['fields']} |"
            )
        lines.append("")

    return lines


def main() -> None:
    env = load_env(ENV_PATH)
    print("连接 MySQL gkx ...")
    conn = connect(env)
    cur = conn.cursor()
    cur.execute("SELECT VERSION(), DATABASE(), CURRENT_USER()")
    print("OK:", cur.fetchone())
    cur.close()

    db_tables = list_db_tables(conn)
    print(f"库内 BASE TABLE: {len(db_tables)}")

    print("提取 Excel 要素库表清单 ...")
    all_libs, source_files = extract_all(BASE)
    all_libs = order_libs(all_libs)
    en_names = collect_english_names(all_libs)
    print(f"报告英文表名去重: {len(en_names)}")

    stats = {
        "matched": 0,
        "missing": 0,
        "exact_name": 0,
        "aliased": 0,
        "nonzero": 0,
    }
    missing: list[str] = []
    alias_notes: list[str] = []
    row_map: dict[str, str] = {}
    physical_map: dict[str, str] = {}

    for i, en in enumerate(en_names, 1):
        key = en.lower()
        physical, how = resolve_physical_table(en, db_tables)
        if not physical:
            stats["missing"] += 1
            missing.append(en)
            row_map[key] = "库中无此表"
            print(f"[{i}/{len(en_names)}] MISS {en}")
            continue

        meta = db_tables[physical.lower()]
        t0 = time.time()
        alive, total = exact_count(conn, physical, meta["has_is_deleted"])
        elapsed = time.time() - t0
        stats["matched"] += 1
        if how == "exact":
            stats["exact_name"] += 1
        else:
            stats["aliased"] += 1
            alias_notes.append(f"`{en}` → `{physical}` ({how})")
        if alive > 0:
            stats["nonzero"] += 1

        if meta["has_is_deleted"] and total is not None and total != alive:
            display = f"{format_count(alive)}（全表 {format_count(total)}）"
        else:
            display = format_count(alive)
        if how != "exact":
            display = f"{display}〔={physical}〕"

        row_map[key] = display
        physical_map[key] = physical
        print(
            f"[{i}/{len(en_names)}] OK {en} -> {physical} [{how}]: "
            f"{display} ({elapsed:.1f}s)"
        )

    for tables in all_libs.values():
        for (_cn, en), info in tables.items():
            key = (en or "").strip().lower()
            info["row_count"] = row_map.get(key, "未提供")

    generate_md(all_libs, source_files, OUT)
    text = OUT.read_text(encoding="utf-8")
    old_note = (
        "- **数据行数**：源「要素库」工作表未提供统一的表级行数字段时，记为「未提供」。"
    )
    new_note = (
        "- **数据行数**：按英文表名对齐三方 MySQL 库 `gkx`（`183.240.141.251:3318`）"
        " 实测 `COUNT(*)`；存在 `is_deleted` 时默认统计 `is_deleted=0`"
        "（若与全表不一致则括号标注全表行数）；"
        "名称经 `dwd_`/`ods_` 前缀或已知别名映射时，以〔=物理表名〕标注；"
        "库中无对应表记为「库中无此表」。"
    )
    if old_note in text:
        text = text.replace(old_note, new_note)
    text = re.sub(
        r"> 生成日期：\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?",
        f"> 生成日期：{TODAY_ISO}\n"
        "> 行数来源：三方 MySQL `gkx` 实测（英文表名对齐，含前缀/别名映射）",
        text,
        count=1,
    )

    nonzero_tables: list[tuple[str, str, str, str]] = []
    for lib_name, tables in all_libs.items():
        for (cn, en), info in tables.items():
            row_count = info.get("row_count", "")
            match = re.match(r"^([\d,]+)", row_count)
            if match and int(match.group(1).replace(",", "")) > 0:
                nonzero_tables.append((lib_name, cn, en, row_count))

    nonzero_summary = [
        "## 有数据表汇总",
        "",
        "> 仅展示实测数据行数大于 0 的表；0 行及库中无对应表不展示。",
        "",
        "| 序号 | 要素库 | 表中文名 | 英文表名 | 数据行数 |",
        "|:---:|:---|:---|:---|---:|",
    ]
    for index, (lib_name, cn, en, row_count) in enumerate(nonzero_tables, 1):
        nonzero_summary.append(
            f"| {index} | {lib_name} | {cn} | `{en}` | {row_count} |"
        )
    nonzero_summary.append("")

    text = re.sub(
        r"(\| 字段总数 \| \d+ \|)",
        rf"\1\n| 有数据表数 | {len(nonzero_tables)} |",
        text,
        count=1,
    )
    text = text.replace(
        "## 表清单（按要素库分组）",
        "\n".join(nonzero_summary) + "\n## 表清单（按要素库分组）",
        1,
    )

    # 与上次报告对比（基于表清单中的行数/字段数）
    curr_tables: dict[str, dict] = {}
    for lib_name, tables in all_libs.items():
        for (cn, en), info in tables.items():
            en_key = (en or "").strip().lower()
            if not en_key:
                continue
            row_raw = info.get("row_count", "")
            curr_tables[en_key] = {
                "lib": lib_name,
                "cn": cn,
                "en": en,
                "rows": parse_row_number(row_raw),
                "rows_raw": row_raw,
                "fields": len(info.get("fields", [])),
            }

    prev_report = find_previous_report(BASE, OUT)
    comparison = build_comparison_section(
        prev_report, curr_tables, TODAY_ISO, OUT.name
    )
    text = text.replace(
        "## 表清单（按要素库分组）",
        "\n".join(comparison) + "\n## 表清单（按要素库分组）",
        1,
    )

    appendix = [
        "## 行数回填说明",
        "",
        f"- 对齐英文表名：{len(en_names)}",
        f"- 库中匹配并完成计数：{stats['matched']}（其中原名精确匹配 {stats['exact_name']}，别名/前缀映射 {stats['aliased']}）",
        f"- 行数 > 0 的表：{stats['nonzero']}",
        f"- 库中无此表：{stats['missing']}",
        "",
    ]
    if prev_report:
        appendix.insert(
            5,
            f"- 对比基准文件：`{prev_report.name}`",
        )
    if alias_notes:
        appendix.append("### 名称映射")
        appendix.append("")
        for note in alias_notes:
            appendix.append(f"- {note}")
        appendix.append("")
    if missing:
        appendix.append("### 库中未找到的英文表名")
        appendix.append("")
        for name in missing:
            appendix.append(f"- `{name}`")
        appendix.append("")

    text = text.rstrip() + "\n\n" + "\n".join(appendix) + "\n"
    OUT.write_text(text, encoding="utf-8")

    conn.close()
    print("\n==== SUMMARY ====")
    print(stats)
    print("missing:", missing)
    print("updated:", OUT)


if __name__ == "__main__":
    main()
