# -*- coding: utf-8 -*-
"""在行数报告基础上，追加 Excel vs MySQL 表结构差异。"""
from __future__ import annotations

import sys
from pathlib import Path as _Path

_SCRIPT_DIR = _Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from gen_gkx_report import extract_all, generate_md, md_escape, order_libs
from _yuansuku_paths import ENV_PATH, excel_base, report_dir
from update_row_counts import (
    build_comparison_section,
    collect_english_names,
    connect,
    exact_count,
    find_previous_report,
    format_count,
    list_db_tables,
    load_env,
    parse_row_number,
    resolve_physical_table,
)

NOW = datetime.now()
TODAY_COMPACT = NOW.strftime("%Y%m%d-%H%M")
TODAY_ISO = NOW.strftime("%Y-%m-%d %H:%M")
BASE = excel_base()
OUT = report_dir() / f"GKX数据源表及行数报告-{TODAY_COMPACT}.MD"

TECH_FIELDS = {
    "created_time",
    "updated_time",
    "creater",
    "updater",
    "table_data_source",
    "is_deleted",
    "operator_remarks",
    "insert_remark",
    "dwd_id",
}

IDENT_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


def list_db_columns(conn) -> dict[str, list[str]]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT TABLE_NAME, COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
    )
    cols: dict[str, list[str]] = defaultdict(list)
    for table_name, column_name in cur.fetchall():
        cols[table_name.lower()].append(column_name)
    cur.close()
    return cols


def excel_field_en_names(fields: list[dict]) -> tuple[list[str], list[str]]:
    names: list[str] = []
    seen: set[str] = set()
    no_en: list[str] = []
    for field in fields:
        en = (field.get("field_en") or "").strip()
        cn = (field.get("field_cn") or "").strip()
        if not en:
            if cn:
                no_en.append(cn)
            continue
        if not IDENT_RE.fullmatch(en):
            no_en.append(f"{cn or en}（非标识符 `{en}`）")
            continue
        key = en.lower()
        if key in seen:
            continue
        seen.add(key)
        names.append(en)
    return names, no_en


def split_extra_db(extra_db: list[str]) -> tuple[list[str], list[str]]:
    tech = [c for c in extra_db if c.lower() in TECH_FIELDS]
    biz = [c for c in extra_db if c.lower() not in TECH_FIELDS]
    return tech, biz


def format_schema_change(
    extra_tech: list[str],
    extra_biz: list[str],
    extra_excel: list[str],
    missing: bool,
) -> str:
    if missing:
        return "库中无此表"
    parts: list[str] = []
    if extra_tech:
        parts.append("技术字段多出：" + ", ".join(extra_tech))
    if extra_biz:
        parts.append("业务字段多出：" + ", ".join(extra_biz))
    if extra_excel:
        parts.append("Excel多出（库无）：" + ", ".join(f"-{n}" for n in extra_excel))
    if not parts:
        return "无"
    return "；".join(parts)


def classify_diff(
    extra_tech: list[str],
    extra_biz: list[str],
    extra_excel: list[str],
    missing: bool,
) -> str:
    if missing:
        return "库中无此表"
    if not extra_tech and not extra_biz and not extra_excel:
        return "一致"
    if extra_biz or extra_excel:
        # 业务侧有任一方向差异
        if extra_biz and extra_excel:
            return "业务字段双向差异"
        if extra_biz:
            return "业务字段多出"
        return "Excel字段多出"
    return "仅技术字段多出"


def truncate(text: str, limit: int = 140) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def build_schema_sections(rows: list[dict]) -> list[str]:
    n = len(rows)
    n_ok = sum(1 for r in rows if r["category"] == "一致")
    n_tech_only = sum(1 for r in rows if r["category"] == "仅技术字段多出")
    n_biz_extra = sum(1 for r in rows if r["n_extra_biz"] > 0)
    n_excel_extra = sum(1 for r in rows if r["n_extra_excel"] > 0)
    n_miss = sum(1 for r in rows if r["category"] == "库中无此表")
    n_has_tech = sum(1 for r in rows if r["n_extra_tech"] > 0)
    n_has_biz = sum(1 for r in rows if r["n_extra_biz"] > 0)

    lines = [
        "## 表结构差异总览",
        "",
        "> 对照 Excel「要素库」英文字段名 与 live MySQL `gkx` 物理列名（小写对齐）。",
        "> **技术字段**（九件套）：`created_time` / `updated_time` / `creater` / `updater` / "
        "`table_data_source` / `is_deleted` / `operator_remarks` / `insert_remark` / `dwd_id`。",
        "> **业务字段多出**：库有而 Excel 无、且不属于上述技术字段的列。",
        "> **Excel字段多出**：Excel 有而库无。",
        "",
        "### 总览指标",
        "",
        "| 指标 | 数量 | 说明 |",
        "|:---|---:|:---|",
        f"| 参与对照表 | {n} | 去重英文表名 |",
        f"| 结构一致 | {n_ok} | 英文字段名完全一致 |",
        f"| 含技术字段多出 | {n_has_tech} | 库侧多出技术字段中至少 1 个 |",
        f"| 其中「仅技术字段多出」 | {n_tech_only} | 无业务/Excel 字段差异，仅技术字段多出 |",
        f"| 含业务字段多出 | {n_has_biz} | 库侧多出非技术字段 |",
        f"| 含 Excel 字段多出 | {n_excel_extra} | Excel 有、库无 |",
        f"| 库中无此表 | {n_miss} | 无法拉列对照 |",
        "",
        "### 表级结构差异一览",
        "",
        "| 序号 | 要素库 | 表中文名 | 英文表名 | 物理表 | 数据行数 | Excel字段 | 库字段 | "
        "技术多出数 | 业务多出数 | Excel多出数 | 分类 | 差异摘要 |",
        "|:---:|:---|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|:---|",
    ]
    for i, r in enumerate(rows, 1):
        phys = r["physical"] or "—"
        db_n = "—" if r["db_cols"] is None else str(r["db_cols"])
        lines.append(
            f"| {i} | {md_escape(r['lib'])} | {md_escape(r['cn'])} | `{md_escape(r['en'])}` | "
            f"`{md_escape(phys)}` | {md_escape(r['row_count'])} | {r['excel_fields']} | {db_n} | "
            f"{r['n_extra_tech']} | {r['n_extra_biz']} | {r['n_extra_excel']} | "
            f"{r['category']} | {md_escape(truncate(r['schema_change']))} |"
        )
    lines.append("")

    # 分栏清单：技术 / 业务，便于扫读
    tech_rows = [r for r in rows if r["n_extra_tech"] > 0]
    biz_rows = [r for r in rows if r["n_extra_biz"] > 0]
    excel_rows = [r for r in rows if r["n_extra_excel"] > 0]

    lines.extend(
        [
            f"### 技术字段多出清单（{len(tech_rows)} 表）",
            "",
        ]
    )
    if not tech_rows:
        lines.append("*无*")
        lines.append("")
    else:
        lines.append("| 序号 | 要素库 | 英文表名 | 技术字段多出 |")
        lines.append("|:---:|:---|:---|:---|")
        for i, r in enumerate(tech_rows, 1):
            lines.append(
                f"| {i} | {md_escape(r['lib'])} | `{md_escape(r['en'])}` | "
                f"{md_escape(', '.join(r['extra_tech']))} |"
            )
        lines.append("")

    lines.extend(
        [
            f"### 业务字段多出清单（{len(biz_rows)} 表）",
            "",
        ]
    )
    if not biz_rows:
        lines.append("*无*")
        lines.append("")
    else:
        lines.append("| 序号 | 要素库 | 英文表名 | 业务字段多出 |")
        lines.append("|:---:|:---|:---|:---|")
        for i, r in enumerate(biz_rows, 1):
            lines.append(
                f"| {i} | {md_escape(r['lib'])} | `{md_escape(r['en'])}` | "
                f"{md_escape(', '.join(r['extra_biz']))} |"
            )
        lines.append("")

    lines.extend(
        [
            f"### Excel 字段多出清单（库无，{len(excel_rows)} 表）",
            "",
        ]
    )
    if not excel_rows:
        lines.append("*无*")
        lines.append("")
    else:
        lines.append("| 序号 | 要素库 | 英文表名 | Excel多出（库无） |")
        lines.append("|:---:|:---|:---|:---|")
        for i, r in enumerate(excel_rows, 1):
            lines.append(
                f"| {i} | {md_escape(r['lib'])} | `{md_escape(r['en'])}` | "
                f"{md_escape(', '.join('-' + x for x in r['extra_excel']))} |"
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
    db_columns = list_db_columns(conn)
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
    row_map: dict[str, str] = {}
    physical_map: dict[str, str] = {}
    missing: list[str] = []
    alias_notes: list[str] = []
    no_en_notes: list[str] = []
    overview_rows: list[dict] = []

    for i, en in enumerate(en_names, 1):
        key = en.lower()
        physical, how = resolve_physical_table(en, db_tables)
        if not physical:
            stats["missing"] += 1
            missing.append(en)
            row_map[key] = "库中无此表"
            physical_map[key] = ""
            print(f"[{i}/{len(en_names)}] MISS {en}")
            continue

        meta = db_tables[physical.lower()]
        alive, total = exact_count(conn, physical, meta["has_is_deleted"])
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
        print(f"[{i}/{len(en_names)}] OK {en} -> {physical} [{how}]: {display}")

    seen_en: set[str] = set()
    for lib_name, tables in all_libs.items():
        for (cn, en), info in tables.items():
            key = (en or "").strip().lower()
            info["row_count"] = row_map.get(key, "未提供")
            excel_en, no_en = excel_field_en_names(info.get("fields") or [])
            if no_en:
                no_en_notes.append(
                    f"`{en}` / {cn}：无英文名 {len(no_en)} 个（{', '.join(no_en[:8])}"
                    f"{'…' if len(no_en) > 8 else ''}）"
                )

            physical = physical_map.get(key, "")
            missing_table = not physical
            if missing_table:
                extra_tech: list[str] = []
                extra_biz: list[str] = []
                extra_excel = list(excel_en)
                db_col_count = None
            else:
                db_cols = db_columns.get(physical.lower(), [])
                db_col_count = len(db_cols)
                db_set = {c.lower() for c in db_cols}
                excel_set = {c.lower() for c in excel_en}
                extra_db = [c for c in db_cols if c.lower() not in excel_set]
                extra_excel = [c for c in excel_en if c.lower() not in db_set]
                extra_tech, extra_biz = split_extra_db(extra_db)

            schema_change = format_schema_change(
                extra_tech, extra_biz, extra_excel, missing_table
            )
            category = classify_diff(extra_tech, extra_biz, extra_excel, missing_table)
            info["schema_change"] = schema_change

            if key in seen_en:
                continue
            seen_en.add(key)
            overview_rows.append(
                {
                    "lib": lib_name,
                    "cn": cn,
                    "en": en,
                    "physical": physical,
                    "row_count": info["row_count"],
                    "excel_fields": len(info.get("fields") or []),
                    "db_cols": db_col_count,
                    "extra_tech": extra_tech,
                    "extra_biz": extra_biz,
                    "extra_excel": extra_excel,
                    "n_extra_tech": len(extra_tech),
                    "n_extra_biz": len(extra_biz),
                    "n_extra_excel": len(extra_excel),
                    "category": category,
                    "schema_change": schema_change,
                }
            )

    generate_md(all_libs, source_files, OUT)
    text = OUT.read_text(encoding="utf-8")

    old_note = (
        "- **数据行数**：源「要素库」工作表未提供统一的表级行数字段时，记为「未提供」。"
    )
    new_notes = (
        "- **数据行数**：按英文表名对齐三方 MySQL 库 `gkx`（`183.240.141.251:3318`）"
        " 实测 `COUNT(*)`；存在 `is_deleted` 时默认统计 `is_deleted=0`"
        "（若与全表不一致则括号标注全表行数）；"
        "名称经 `dwd_`/`ods_` 前缀或已知别名映射时，以〔=物理表名〕标注；"
        "库中无对应表记为「库中无此表」。\n"
        "- **表结构变化**：Excel 英文字段名 vs 库列名；"
        "技术字段多出 / 业务字段多出 / Excel多出（库无）分项标注。"
        "字段明细仍为 Excel 提取原文。"
    )
    if old_note in text:
        text = text.replace(old_note, new_notes)
    text = re.sub(
        r"> 生成日期：\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?",
        f"> 生成日期：{TODAY_ISO}\n"
        "> 行数来源：三方 MySQL `gkx` 实测（英文表名对齐，含前缀/别名映射）\n"
        "> 结构对照：Excel 英文字段名 ↔ `information_schema.COLUMNS`",
        text,
        count=1,
    )

    # ---- 有数据表汇总（与原行数报告一致）----
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

    # ---- 与上次行数对比 ----
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

    schema_sections = build_schema_sections(overview_rows)

    # 插入顺序：有数据表汇总 → 与上次对比 → 表结构差异总览 → 表清单
    insert_block = (
        "\n".join(nonzero_summary)
        + "\n"
        + "\n".join(comparison)
        + "\n"
        + "\n".join(schema_sections)
        + "\n## 表清单（按要素库分组）"
    )
    text = text.replace("## 表清单（按要素库分组）", insert_block, 1)

    appendix = [
        "## 行数回填说明",
        "",
        f"- 对齐英文表名：{len(en_names)}",
        f"- 库中匹配并完成计数：{stats['matched']}（其中原名精确匹配 {stats['exact_name']}，别名/前缀映射 {stats['aliased']}）",
        f"- 行数 > 0 的表：{stats['nonzero']}",
        f"- 库中无此表：{stats['missing']}",
        "",
        "## 表结构对照说明",
        "",
        "- 字段对齐键：Excel `字段英文名称` 小写；无英文名不参与差分",
        "- 技术字段九件套：`created_time` / `updated_time` / `creater` / `updater` / "
        "`table_data_source` / `is_deleted` / `operator_remarks` / `insert_remark` / `dwd_id`",
        "- 业务字段多出 = 库多出且不属于上述技术字段",
        "- 各表明细「表结构变化」分项：技术字段多出 / 业务字段多出 / Excel多出（库无）",
        "",
    ]
    if prev_report:
        appendix.insert(
            5,
            f"- 对比基准文件：`{prev_report.name}`",
        )
    if alias_notes:
        appendix.extend(["### 名称映射", ""])
        for note in alias_notes:
            appendix.append(f"- {note}")
        appendix.append("")
    if missing:
        appendix.extend(["### 库中未找到的英文表名", ""])
        for name in missing:
            appendix.append(f"- `{name}`")
        appendix.append("")
    if no_en_notes:
        appendix.extend(["### 未参与差分的无英文字段", ""])
        for note in no_en_notes:
            appendix.append(f"- {note}")
        appendix.append("")

    text = text.rstrip() + "\n\n" + "\n".join(appendix) + "\n"
    OUT.write_text(text, encoding="utf-8")
    conn.close()

    cats: dict[str, int] = defaultdict(int)
    for r in overview_rows:
        cats[r["category"]] += 1
    print("\n==== SUMMARY ====")
    print("row_stats:", stats)
    print("schema_cats:", dict(cats))
    print(
        "tech_tables:",
        sum(1 for r in overview_rows if r["n_extra_tech"] > 0),
        "biz_tables:",
        sum(1 for r in overview_rows if r["n_extra_biz"] > 0),
        "excel_extra_tables:",
        sum(1 for r in overview_rows if r["n_extra_excel"] > 0),
    )
    print("missing:", missing)
    print("updated:", OUT)


if __name__ == "__main__":
    main()
