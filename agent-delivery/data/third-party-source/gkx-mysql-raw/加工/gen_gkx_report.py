# -*- coding: utf-8 -*-
"""从各 Excel『要素库』工作表提取表清单与字段明细，生成 GKX 数据源表及行数报告。"""
from __future__ import annotations

import sys
from pathlib import Path as _Path

_SCRIPT_DIR = _Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import re
import zipfile
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from _yuansuku_paths import excel_base, report_dir

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

HEADER_ALIASES = {
    "序号": "seq",
    "中文表名": "table_cn",
    "英文表名": "table_en",
    "字段中文名称": "field_cn",
    "字段英文名称": "field_en",
    "字段英文名称（json解析）": "field_en_json",
    "数据类型": "dtype",
    "数据长度（精度）": "length",
    "数据长度(精度)": "length",
    "字段描述": "desc",
    "数据样例": "sample",
    "是否有空值": "nullable",
    "是否为空": "nullable",
    "是否为空值": "nullable",
    "是否索引": "indexed",
    "是否为主键": "pk",
    "是否为索引主键": "index_pk",
    "值域": "domain",
    "关联表/字段": "rel",
    "关联类型(一对多以关联表为主)": "rel_type",
    "字段覆盖率（抽样估算）": "coverage",
    "字段完整率（覆盖率）": "coverage",
    "字段覆盖率-PPR": "coverage",
    "字段完整性": "coverage",
    "完整率": "coverage",
    "约束字段": "constraint",
    "备注": "remark",
    "数据行数": "row_count",
    "记录数": "row_count",
    "数据量": "row_count",
}


def norm_header(h: str) -> str:
    return re.sub(r"\s+", "", str(h or ""))


def col_to_idx(col: str) -> int:
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def load_ss(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
    ss: list[str] = []
    for si in sst.findall("m:si", NS):
        texts = [
            t.text or ""
            for t in si.iter(
                "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
            )
        ]
        ss.append("".join(texts))
    return ss


def cell_val(c, ss: list[str]) -> str:
    t = c.get("t")
    v = c.find("m:v", NS)
    if v is None:
        is_elem = c.find("m:is", NS)
        if is_elem is not None:
            texts = [
                t.text or ""
                for t in is_elem.iter(
                    "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                )
            ]
            return "".join(texts)
        return ""
    raw = v.text or ""
    if t == "s":
        try:
            return ss[int(raw)]
        except Exception:
            return raw
    return raw


def read_rows(z: zipfile.ZipFile, target: str, ss: list[str]) -> list[list[str]]:
    root = ET.fromstring(z.read(target))
    rows: list[list[str]] = []
    for row in root.findall("m:sheetData/m:row", NS):
        cells: dict[int, str] = {}
        maxc = -1
        for c in row.findall("m:c", NS):
            ref = c.get("r", "A1")
            col = "".join(ch for ch in ref if ch.isalpha())
            idx = col_to_idx(col)
            cells[idx] = cell_val(c, ss)
            if idx > maxc:
                maxc = idx
        vals = [str(cells.get(i, "") or "").strip() for i in range(maxc + 1)]
        rows.append(vals)
    return rows


def md_escape(s: str) -> str:
    s = str(s or "").replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("|", "\\|").replace("\n", "<br>")
    return s


def looks_like_ident(s: str) -> bool:
    s = (s or "").strip()
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", s))


def has_cjk(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


def normalize_table_names(cn: str, en: str) -> tuple[str, str]:
    """修复源表把中英文表名列写反的情况。"""
    cn = (cn or "").strip()
    en = (en or "").strip()
    # 英文列是中文、中文列是标识符 => 对调
    if has_cjk(en) and looks_like_ident(cn):
        return en, cn
    return cn, en


def anchor(text: str) -> str:
    # GitHub-style-ish anchor for Chinese headings
    a = re.sub(r"\s+", "-", text.strip())
    a = re.sub(r"[^\w\u4e00-\u9fff\-（）()_]", "", a)
    return a


def extract_all(base: Path) -> OrderedDict:
    all_libs: OrderedDict = OrderedDict()
    source_files: OrderedDict = OrderedDict()

    for f in sorted(base.glob("*.xlsx")):
        if f.name.startswith("~$"):
            continue
        with zipfile.ZipFile(f) as z:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            sheets = [(s.get("name"), s.get(R_NS)) for s in wb.findall(".//m:sheet", NS)]
            rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            rid_map = {rel.get("Id"): rel.get("Target") for rel in rels}
            ss = load_ss(z)

            for name, rid in sheets:
                if "要素库" not in (name or ""):
                    continue
                target = rid_map[rid]
                if not target.startswith("xl/"):
                    target = "xl/" + target
                rows = read_rows(z, target, ss)

                header_idx = None
                for i, r in enumerate(rows[:15]):
                    joined = "".join(r)
                    if "中文表名" in joined and "英文表名" in joined:
                        header_idx = i
                        break
                if header_idx is None:
                    print(f"[WARN] 未找到表头: {f.name} / {name}")
                    continue

                header = rows[header_idx]
                colmap: dict[str, int] = {}
                for ci, h in enumerate(header):
                    hn = norm_header(h)
                    for k, v in HEADER_ALIASES.items():
                        if norm_header(k) == hn and v not in colmap:
                            colmap[v] = ci
                            break

                tables: OrderedDict = OrderedDict()
                cur_cn, cur_en = "", ""
                for r in rows[header_idx + 1 :]:
                    if not any(r):
                        continue

                    def get(key: str) -> str:
                        i = colmap.get(key)
                        return r[i] if i is not None and i < len(r) else ""

                    raw_cn = get("table_cn") or cur_cn
                    raw_en = get("table_en") or cur_en
                    cn, en = normalize_table_names(raw_cn, raw_en)
                    field_cn = get("field_cn")
                    field_en = get("field_en")
                    if not cn and not en:
                        continue
                    if not field_cn and not field_en:
                        # 可能是表级行（含行数），尝试捕获
                        row_count = get("row_count")
                        if row_count and (cn or en):
                            key = (cn, en)
                            if key not in tables:
                                tables[key] = {"row_count": row_count, "fields": []}
                            else:
                                tables[key]["row_count"] = row_count
                        continue

                    cur_cn, cur_en = cn, en
                    key = (cn, en)
                    if key not in tables:
                        tables[key] = {"row_count": get("row_count") or "", "fields": []}
                    elif get("row_count") and not tables[key]["row_count"]:
                        tables[key]["row_count"] = get("row_count")

                    tables[key]["fields"].append(
                        {
                            "field_cn": field_cn,
                            "field_en": field_en,
                            "field_en_json": get("field_en_json"),
                            "dtype": get("dtype"),
                            "length": get("length"),
                            "desc": get("desc"),
                            "sample": get("sample"),
                            "nullable": get("nullable"),
                            "indexed": get("indexed"),
                            "pk": get("pk"),
                            "index_pk": get("index_pk"),
                            "domain": get("domain"),
                            "rel": get("rel"),
                            "rel_type": get("rel_type"),
                            "coverage": get("coverage"),
                            "constraint": get("constraint"),
                            "remark": get("remark"),
                        }
                    )

                all_libs[name] = tables
                source_files[name] = f.name
                print(
                    f"[OK] {f.name} / {name}: {len(tables)} 表, "
                    f"{sum(len(t['fields']) for t in tables.values())} 字段"
                )

    return all_libs, source_files


def has_any(tables: OrderedDict, key: str) -> bool:
    for t in tables.values():
        if t.get(key):
            return True
        for f in t["fields"]:
            if f.get(key):
                return True
    return False


def generate_md(all_libs: OrderedDict, source_files: OrderedDict, out_path: Path) -> None:
    lines: list[str] = []
    lines.append("# GKX数据源表及行数报告")
    lines.append("")
    lines.append("> 数据来源：各数据汇总表 Excel 中的「要素库」工作表。")
    lines.append(f"> 生成日期：{datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("说明：")
    lines.append("- **表清单**按要素库分组，列示表中文名、英文名、数据行数、字段数。")
    lines.append(
        "- **数据行数**：源「要素库」工作表未提供统一的表级行数字段时，记为「未提供」。"
    )
    lines.append("- **字段明细**含字段中英文名、数据类型、长度、描述、空值、索引、值域等（以各表实际列为准）。")
    lines.append("")

    total_tables = sum(len(t) for t in all_libs.values())
    total_fields = sum(
        len(info["fields"]) for tables in all_libs.values() for info in tables.values()
    )
    lines.append("## 总览")
    lines.append("")
    lines.append(f"| 指标 | 数量 |")
    lines.append(f"|:---|---:|")
    lines.append(f"| 要素库数 | {len(all_libs)} |")
    lines.append(f"| 数据表数 | {total_tables} |")
    lines.append(f"| 字段总数 | {total_fields} |")
    lines.append("")

    lines.append("## 要素库一览")
    lines.append("")
    lines.append("| 序号 | 要素库 | 来源文件 | 表数量 | 字段总数 |")
    lines.append("|:---:|:---|:---|---:|---:|")
    for i, (lib, tables) in enumerate(all_libs.items(), 1):
        fc = sum(len(t["fields"]) for t in tables.values())
        lines.append(
            f"| {i} | [{lib}](#{anchor(lib)}) | {md_escape(source_files.get(lib, ''))} | {len(tables)} | {fc} |"
        )
    lines.append("")

    # 全量表清单（按要素库）
    lines.append("## 表清单（按要素库分组）")
    lines.append("")
    for lib, tables in all_libs.items():
        lines.append(f"### {lib}")
        lines.append("")
        if not tables:
            lines.append("*（该要素库未提取到表定义）*")
            lines.append("")
            continue
        lines.append("| 序号 | 表中文名 | 英文名 | 数据行数 | 字段数 |")
        lines.append("|:---:|:---|:---|---:|---:|")
        for j, ((cn, en), info) in enumerate(tables.items(), 1):
            row_count = info.get("row_count") or "未提供"
            link = f"[{md_escape(cn) or '-'}](#{anchor(f'{cn}({en})')})"
            lines.append(
                f"| {j} | {link} | `{md_escape(en) or '-'}` | {md_escape(row_count)} | {len(info['fields'])} |"
            )
        lines.append("")

    # 字段明细
    lines.append("---")
    lines.append("")
    lines.append("## 表字段明细（按要素库分组）")
    lines.append("")

    for lib, tables in all_libs.items():
        lines.append(f"# {lib}")
        lines.append("")
        lines.append(f"**来源文件**：{md_escape(source_files.get(lib, ''))}  ")
        lines.append(f"**表数量**：{len(tables)}")
        lines.append("")

        if not tables:
            lines.append("*（无表）*")
            lines.append("")
            continue

        # 动态列：仅展示该库实际出现过的扩展列
        show_pk = has_any(tables, "pk")
        show_index_pk = has_any(tables, "index_pk")
        show_rel = has_any(tables, "rel")
        show_rel_type = has_any(tables, "rel_type")
        show_coverage = has_any(tables, "coverage")
        show_sample = has_any(tables, "sample")
        show_json = has_any(tables, "field_en_json")
        show_constraint = has_any(tables, "constraint")

        for (cn, en), info in tables.items():
            lines.append(f"## {cn}({en})")
            lines.append("")
            row_count = info.get("row_count") or "未提供"
            lines.append(f"- **表中文名**：{md_escape(cn)}")
            lines.append(f"- **英文名**：`{md_escape(en)}`")
            lines.append(f"- **数据行数**：{md_escape(row_count)}")
            lines.append(f"- **字段数**：{len(info['fields'])}")
            if info.get("schema_change"):
                lines.append(f"- **表结构变化**：{md_escape(info['schema_change'])}")
            lines.append("")

            headers = [
                "序号",
                "字段中文名称",
                "英文名称",
            ]
            keys = [
                "field_cn",
                "field_en",
            ]
            if show_json:
                headers.append("英文名称(json解析)")
                keys.append("field_en_json")
            headers.extend(
                [
                    "数据类型",
                    "数据长度",
                    "字段描述",
                    "是否有空值",
                    "是否索引",
                ]
            )
            keys.extend(["dtype", "length", "desc", "nullable", "indexed"])
            if show_pk:
                headers.append("是否主键")
                keys.append("pk")
            if show_index_pk:
                headers.append("是否索引主键")
                keys.append("index_pk")
            headers.append("值域")
            keys.append("domain")
            if show_sample:
                headers.append("数据样例")
                keys.append("sample")
            if show_rel:
                headers.append("关联表/字段")
                keys.append("rel")
            if show_rel_type:
                headers.append("关联类型")
                keys.append("rel_type")
            if show_coverage:
                headers.append("字段覆盖率/完整率")
                keys.append("coverage")
            if show_constraint:
                headers.append("约束字段")
                keys.append("constraint")
            headers.append("备注")
            keys.append("remark")

            lines.append("| " + " | ".join(headers) + " |")
            lines.append("|" + "|".join([":---:" if h == "序号" else ":---" for h in headers]) + "|")
            for n, field in enumerate(info["fields"], 1):
                cells = [str(n)] + [md_escape(field.get(k, "")) for k in keys]
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")

        lines.append("---")
        lines.append("")

    # 统计
    lines.append("## 统计汇总")
    lines.append("")
    lines.append(f"- 共提取 **{total_tables}** 张数据源表")
    lines.append(f"- 共涉及 **{len(all_libs)}** 个要素库")
    lines.append(f"- 字段定义合计 **{total_fields}** 条")
    lines.append("")
    lines.append("| 要素库 | 表数量 | 字段总数 |")
    lines.append("|:---|---:|---:|")
    for lib, tables in all_libs.items():
        fc = sum(len(t["fields"]) for t in tables.values())
        lines.append(f"| {lib} | {len(tables)} | {fc} |")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


LIB_ORDER = [
    "国内机构要素库",
    "国外机构要素库",
    "人才要素库",
    "国内政策要素库",
    "国外政策要素库",
    "金融要素库",
    "宏观行业要素库",
    "行业分析要素库",
    "产业链要素库",
    "医药专题要素库",
    "化学专题要素库",
    "海洋专题要素库",
    "量子专题要素库",
    "中文论文要素库",
    "外文论文要素库",
    "全球专利要素库",
    "国内项目要素库",
    "国外项目要素库",
    "中文报告要素库",
    "外文报告要素库",
]


def order_libs(all_libs: OrderedDict) -> OrderedDict:
    ordered: OrderedDict = OrderedDict()
    for name in LIB_ORDER:
        if name in all_libs:
            ordered[name] = all_libs[name]
    for name, tables in all_libs.items():
        if name not in ordered:
            ordered[name] = tables
    return ordered


def main() -> None:
    base = excel_base()
    out = report_dir() / "GKX数据源表及行数报告.MD"
    all_libs, source_files = extract_all(base)
    all_libs = order_libs(all_libs)
    generate_md(all_libs, source_files, out)
    total = sum(len(t) for t in all_libs.values())
    print(f"Excel 目录: {base}")
    print(f"\n完成: {total} 张表 -> {out}")


if __name__ == "__main__":
    main()
