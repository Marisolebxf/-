#!/usr/bin/env python3
"""Parse a GDF workpack into inventory.json for scripts/gdf-cdc/fill.py."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TABLE_LINE = re.compile(
    r"-\s*\{\s*name:\s*(?P<name>[\w]+)\s*,\s*priority:\s*(?P<priority>P[012])\s*,\s*cn:\s*(?P<cn>[^,}+]+?)(?:\s*,\s*mapping:\s*(?P<mapping>wash|mirror_only))?(?:\s*,\s*note:\s*(?P<note>.+?))?\s*\}"
)
GROUP_LINE = re.compile(r"^\s*-\s*id:\s*(?P<id>\S+)\s*$")
TITLE_LINE = re.compile(r"^\s*title:\s*(?P<title>.+?)\s*$")
FENCE = re.compile(r"`([^`]+)`")
SPLIT_TARGETS = re.compile(r"\s*\+\s*|\s*、\s*|\s*/\s*")

# Wave B 索引中文名：v1 CDC 壳已用名优先，v2 新增表补中文。禁止用源表 cn 当目标 Sheet 名。
DWD_CN = {
    "enterprise_base": "企业主数据输出",
    "enterprise_executive": "企业高管信息输出",
    "enterprise_extra": "企业扩展表输出",
    "enterprise_finance_history": "企业财务历史输出",
    "enterprise_industry_chain": "企业产业链关联输出",
    "enterprise_news": "企业资讯输出",
    "enterprise_bid": "企业招投标输出",
    "risk_abnormal": "经营异常",
    "risk_punishment": "行政处罚",
    "risk_illegal": "严重违法",
    "risk_tax_punish": "税收违法",
    "risk_judicial_case": "司法案件",
    "risk_dishonest": "失信被执行人",
    "risk_executed": "被执行人",
    "risk_bankruptcy": "破产案件",
    "risk_bankruptcy_party": "破产案件关联人",
    "enterprise_risk_summary": "企业风险汇总",
    "enterprise_financing": "融资信息",
    "enterprise_invest": "对外投资",
    "enterprise_tag": "企业标签",
    "enterprise_parent_subsidiary": "子公司信息",
    "enterprise_recruit": "招聘信息",
    "enterprise_history_name": "历史名称",
    "enterprise_supply_chain": "供应链",
    "enterprise_patent_detail": "专利明细",
    "enterprise_chain_patent": "产业链专利",
    "enterprise_patent_history": "专利历史汇总",
    "enterprise_region_summary": "区域汇总",
    "enterprise_industry_summary": "产业汇总",
    "enterprise_forg_base": "国外机构基本信息",
    "enterprise_forg_extra": "国外机构扩展",
    "enterprise_forg_executive": "国外高管",
    "enterprise_forg_invest": "国外股东穿透",
    "enterprise_forg_finance_history": "国外年报财务",
    "enterprise_forg_parent_subsidiary": "国外子公司",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_workpack_files(root: Path) -> dict[str, Path | None]:
    files: dict[str, Path | None] = {}
    readme = root / "README.md"
    files["readme"] = readme if readme.exists() else root / "00-派单说明书.md"
    yaml02 = list(root.glob("02-*.yaml"))
    if not yaml02:
        raise SystemExit(f"missing 02-WaveA yaml under {root}")
    files["wave_a"] = yaml02[0]
    files["filter"] = next(iter(root.glob("04-*.md")), None)
    mapping = None
    readme_path = files["readme"]
    if readme_path is not None and readme_path.exists():
        text = read_text(readme_path)
        m = re.search(r"09-[^\s\]]+Mapping明细[^\s\]]*", text)
        if m:
            cand = root / m.group(0).rstrip(")")
            if cand.exists():
                mapping = cand
        if mapping is None:
            m = re.search(r"\((09-[^)]+Mapping明细[^)]+)\)", text)
            if m:
                cand = root / m.group(1)
                if cand.exists():
                    mapping = cand
    if mapping is None:
        hits = [p for p in root.glob("09-*.md") if "明细" in p.name]
        mapping = hits[0] if hits else None
    if mapping is None:
        named = []
        if readme_path is not None and readme_path.exists():
            text = read_text(readme_path)
            for m in re.finditer(r"(09-[^\s\])`]+\.md)", text):
                cand = root / m.group(1).rstrip(")`")
                if cand.exists() and "v4" not in cand.name:
                    named.append(cand)
        if named:
            mapping = named[0]
        else:
            any09 = [p for p in root.glob("09-*.md") if "v4" not in p.name]
            mapping = any09[0] if any09 else None
    if mapping is None:
        raise SystemExit(f"missing Mapping 09 under {root}")
    files["mapping"] = mapping
    files["guide"] = next((p for p in root.glob("09-*.md") if p != mapping), None)
    return files


def workpack_status(readme: Path | None) -> dict:
    text = read_text(readme) if readme is not None and readme.exists() else ""
    return {
        "obsolete": bool(re.search(r"已作废|禁止用于建表", text)),
        "deferred": bool(re.search(r"暂缓投递", text)),
        "readme": str(readme) if readme else None,
    }


def parse_wave_a(path: Path) -> list[dict]:
    rows: list[dict] = []
    group_id = ""
    group_title = ""
    for line in read_text(path).splitlines():
        gm = GROUP_LINE.match(line)
        if gm:
            group_id = gm.group("id")
            continue
        tm = TITLE_LINE.match(line)
        if tm and group_id:
            group_title = tm.group("title").strip().strip('"')
            continue
        m = TABLE_LINE.search(line)
        if not m:
            continue
        note = (m.group("note") or "").strip().strip('"')
        rows.append(
            {
                "name": m.group("name"),
                "cn": m.group("cn").strip(),
                "priority": m.group("priority"),
                "mapping": m.group("mapping") or "wash",
                "note": note,
                "group": group_id,
                "group_title": group_title,
            }
        )
    if not rows:
        raise SystemExit(f"no tables parsed from {path}")
    return rows


def split_dwd_names(cell: str) -> list[str]:
    cell = re.sub(r"（[^）]*）", "", cell)
    cell = re.sub(r"\([^)]*\)", "", cell)
    names: list[str] = []
    for part in SPLIT_TARGETS.split(cell):
        part = part.strip().strip("`").split("（")[0].strip()
        if re.fullmatch(r"[a-z][a-z0-9_]*", part):
            names.append(part)
    return names


def parse_md_tables(text: str) -> list[tuple[str, list[list[str]]]]:
    lines = text.splitlines()
    heading = ""
    out: list[tuple[str, list[list[str]]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if re.match(r"^\|.+\|$", line) and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = [headers]
            while i < len(lines) and re.match(r"^\|.+\|$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append((heading, rows))
            continue
        i += 1
    return out


def cell_ident(cell: str) -> str:
    found = FENCE.findall(cell)
    if found:
        return found[0].strip()
    return cell.strip().strip("`")


def parse_v3_mapping(text: str, overview: dict, fields: list[dict]) -> None:
    """GDF-ENT-WORKPACK-v1 09 v3：DWD 字段 | 映射 | 承诺 ODS。"""
    table_alias = {
        "annual": "dwd_org_annual_financial_info",
        "stock": "dwd_org_stock_finance_info",
        "base_info": "dwd_org_base_info",
        "base_out": "dwd_bid_base_out",
        "win_candidate": "dwd_bid_win_candidate_out",
        "target_item": "dwd_bid_target_item_out",
        "purchase_agency": "dwd_bid_purchase_agency_out",
        "tags": "dwd_org_industry_tags",
        "chain_info": "dwd_industry_chain_info",
        "org_product": "dwd_org_org_product_info",
        "stock_base": "dwd_org_stock_base",
        "org_product_info": "dwd_org_org_product_info",
    }
    for heading, rows in parse_md_tables(text):
        headers = [h.replace(" ", "") for h in rows[0]]
        body = rows[1:]
        joined = "".join(headers)
        if "项目DWD表" in joined and "承诺ODS" in joined:
            di = next(i for i, h in enumerate(headers) if "DWD" in h)
            si = next(i for i, h in enumerate(headers) if "ODS" in h)
            for row in body:
                if len(row) <= max(di, si):
                    continue
                for tgt in split_dwd_names(row[di]):
                    srcs = re.findall(r"dwd_[a-z0-9_]+", row[si])
                    if not srcs:
                        continue
                    bucket = "metric" if tgt.endswith("_summary") else "direct"
                    for src in srcs:
                        overview[bucket].append({"src": src, "dwd": tgt, "note": row[-1] if row else ""})
            continue
        if "项目DWD" in joined and "承诺ODS" in joined and "映射" in joined:
            di = next(i for i, h in enumerate(headers) if "DWD" in h)
            si = next(i for i, h in enumerate(headers) if "ODS" in h)
            for row in body:
                if len(row) <= max(di, si):
                    continue
                tgts = split_dwd_names(row[di]) or re.findall(r"(risk_[a-z0-9_]+|enterprise_[a-z0-9_]+)", row[di])
                if "risk_bankruptcy" in row[di] and "party" in row[di] and "risk_bankruptcy_party" not in tgts:
                    if "risk_bankruptcy" not in tgts:
                        tgts.append("risk_bankruptcy")
                    tgts.append("risk_bankruptcy_party")
                srcs = re.findall(r"dwd_[a-z0-9_]+", row[si])
                if "bankruptcy_public_cases" in row[si] and not srcs:
                    srcs = ["dwd_org_bankruptcy_public_cases", "dwd_org_bankruptcy_public_cases_list"]
                if any("summary" in t for t in tgts) and not srcs:
                    for tgt in tgts:
                        overview["metric"].append({"src": "", "dwd": tgt, "note": row[2] if len(row) > 2 else ""})
                    continue
                for tgt in tgts:
                    bucket = "metric" if "summary" in tgt else "direct"
                    for src in srcs:
                        overview[bucket].append({"src": src, "dwd": tgt, "note": row[2] if len(row) > 2 else ""})
            continue
        dwd_hint = ""
        m = re.search(r"(enterprise_[a-z0-9_]+|risk_[a-z0-9_]+)", heading)
        if m:
            dwd_hint = m.group(1)
        if not dwd_hint:
            continue
        dwd_col = next((h for h in rows[0] if "DWD" in h.replace(" ", "")), None)
        ods_col = next((h for h in rows[0] if "ODS" in h.upper() or "承诺" in h), None)
        if dwd_col is None or ods_col is None:
            continue
        di, oi = rows[0].index(dwd_col), rows[0].index(ods_col)
        mark_i = next((i for i, h in enumerate(rows[0]) if h.strip() in ("映射", "标记")), None)
        note_i = len(rows[0]) - 1
        default_src = ""
        for link in overview["direct"] + overview["metric"]:
            if link["dwd"] == dwd_hint:
                default_src = link["src"]
                break
        for row in body:
            if len(row) <= max(di, oi):
                continue
            mark = row[mark_i] if mark_i is not None and mark_i < len(row) else ""
            if "🟦" in mark and "id" in row[di] and "time" not in row[di]:
                continue
            tgts = re.findall(r"[a-z][a-z0-9_]*", row[di])
            if not tgts:
                continue
            ods = row[oi]
            note = row[note_i] if note_i < len(row) else ""
            src_table, src_field = default_src, ""
            dotted = re.search(r"(dwd_[a-z0-9_]+)\.([a-z0-9_]+)", ods.replace("`", ""))
            if dotted:
                src_table, src_field = dotted.group(1), dotted.group(2)
            else:
                token = re.search(r"\b([a-z][a-z0-9_]*)\.([a-z][a-z0-9_]*)\b", ods)
                if token and token.group(1) in table_alias:
                    src_table, src_field = table_alias[token.group(1)], token.group(2)
                else:
                    ident = cell_ident(ods).split()[0] if ods.strip() not in ("—", "-", "") else ""
                    ident = ident.replace("`", "")
                    if ident in table_alias:
                        src_table = table_alias[ident]
                    elif re.fullmatch(r"[a-z][a-z0-9_]*", ident) and ident not in ("annual", "stock"):
                        src_field = ident
            if "❌" in mark and "无" in (note + mark + ods):
                src_field = ""
            for tgt in tgts:
                if tgt in ("id",):
                    continue
                fields.append(
                    {
                        "dwd": dwd_hint,
                        "src_table": src_table,
                        "src_field": src_field or tgt,
                        "tgt_field": tgt,
                        "kind": mark,
                        "logic": note + " " + ods,
                    }
                )
                if src_table:
                    overview["direct"].append({"src": src_table, "dwd": dwd_hint, "note": ""})


def parse_mapping(path: Path) -> dict:
    text = read_text(path)
    overview: dict[str, list] = {"direct": [], "assoc": [], "metric": [], "foreign": [], "skip": []}
    fields: list[dict] = []
    if "承诺 ODS" in text or "DWD 字段" in text:
        parse_v3_mapping(text, overview, fields)
        risk_srcs = [
            x["src"]
            for x in overview["direct"]
            if str(x.get("dwd", "")).startswith("risk_") and str(x.get("src", "")).startswith("dwd_")
        ]
        expanded: list[dict] = []
        for link in overview["metric"]:
            src = str(link.get("src") or "")
            if link.get("dwd") == "enterprise_risk_summary" and not src.startswith("dwd_"):
                for s in risk_srcs:
                    expanded.append({**link, "src": s})
            else:
                expanded.append(link)
        overview["metric"] = expanded
        return {"overview": overview, "fields": fields}
    for heading, rows in parse_md_tables(text):
        headers = rows[0]
        body = rows[1:]
        has_src = "源表" in headers or "源" in headers
        src_header = "源表" if "源表" in headers else ("源" if "源" in headers else None)
        if has_src and src_header and ("目标表" in headers or "原因" in headers or "2.4" in heading or "暂不" in heading):
            si = headers.index(src_header)
            ti = headers.index("目标表") if "目标表" in headers else None
            bucket = "direct"
            if "2.2" in heading or "关联" in heading:
                bucket = "assoc"
            elif "2.3" in heading or "指标" in heading:
                bucket = "metric"
            elif "2.5" in heading or "国外" in heading:
                bucket = "foreign"
            elif "2.4" in heading or "暂不" in heading or ti is None:
                bucket = "skip"
            for row in body:
                if len(row) <= si:
                    continue
                src_cell = row[si]
                src_names = re.findall(r"dwd_[a-z0-9_]+", src_cell)
                if not src_names:
                    ident = cell_ident(src_cell)
                    src_names = [ident.split()[0]] if ident else []
                if bucket == "skip":
                    overview["skip"].extend(src_names)
                    continue
                if ti is None or len(row) <= ti:
                    continue
                for tgt in split_dwd_names(row[ti]):
                    overview[bucket].append({"src": src_names[0] if src_names else "", "dwd": tgt, "note": row[-1] if row else ""})
            continue
        if "源字段" in headers and "目标字段" in headers:
            sf, tf = headers.index("源字段"), headers.index("目标字段")
            kind_i = headers.index("映射类型") if "映射类型" in headers else None
            logic_i = headers.index("转换逻辑") if "转换逻辑" in headers else None
            dwd_hint = ""
            dwd_hits = re.findall(r"`((?:enterprise_|risk_)[a-z0-9_]*)`", heading)
            if len(dwd_hits) == 1:
                dwd_hint = dwd_hits[0]
            src_table_hint = ""
            sm = re.search(r"`(dwd_[a-z0-9_]+)`", heading)
            if sm:
                src_table_hint = sm.group(1)
            if not dwd_hint:
                continue
            for row in body:
                if len(row) <= max(sf, tf):
                    continue
                src_cell = row[sf].strip()
                tgt_cell = row[tf].strip()
                kind = row[kind_i] if kind_i is not None and kind_i < len(row) else "直接"
                logic = row[logic_i] if logic_i is not None and logic_i < len(row) else ""
                if tgt_cell in ("—", "-", "–") or "不映射" in kind:
                    continue
                if "自增" in kind:
                    continue
                src_table = src_table_hint
                src_field = cell_ident(src_cell).split("/")[0].strip()
                dotted = re.match(r"`?(dwd_[a-z0-9_]+)\.([a-z0-9_]+)`?", src_cell.replace(" ", ""))
                if dotted:
                    src_table, src_field = dotted.group(1), dotted.group(2)
                tgt_field = cell_ident(tgt_cell)
                if not re.fullmatch(r"[a-z][a-z0-9_]*", tgt_field):
                    continue
                if src_field in ("—", "-", ""):
                    continue
                fields.append(
                    {
                        "dwd": dwd_hint,
                        "src_table": src_table,
                        "src_field": src_field,
                        "tgt_field": tgt_field,
                        "kind": kind,
                        "logic": logic,
                    }
                )
    risk_srcs = [x["src"] for x in overview["direct"] if str(x.get("dwd", "")).startswith("risk_") and str(x.get("src", "")).startswith("dwd_")]
    expanded: list[dict] = []
    for link in overview["metric"]:
        src = str(link.get("src") or "")
        if link.get("dwd") == "enterprise_risk_summary" and not src.startswith("dwd_"):
            for s in risk_srcs:
                expanded.append({**link, "src": s})
        else:
            expanded.append(link)
    overview["metric"] = expanded
    return {"overview": overview, "fields": fields}


def expr_for(field: dict, alias_by_table: dict[str, str]) -> str:
    logic = field.get("logic") or ""
    src_table = field.get("src_table") or ""
    alias = alias_by_table.get(src_table, "T1")
    col = field["src_field"]
    base = f"{alias}.{col}"
    if re.search(r"÷\s*10000|/ *10000", logic):
        return f"{base} / 10000.0"
    if "occur_period" in col:
        return f"SUBSTRING({base}, 1, 4)"
    if field["tgt_field"] == "is_listed":
        return (
            f"CASE WHEN {alias}.listing_status LIKE '%上市%' "
            f"OR COALESCE(T2.stock_code, '') <> '' THEN 1 ELSE 0 END"
        )
    return base


def assemble_wave_b(mapping: dict, wave_a: list[dict]) -> tuple[list[dict], list[str]]:
    warnings: list[str] = []
    skip: set[str] = set()
    for s in mapping["overview"]["skip"]:
        ident = re.findall(r"dwd_[a-z0-9_]+", s)
        skip.update(ident or [s])
    a_by_name = {t["name"]: t for t in wave_a}
    targets: dict[str, dict] = {}
    for bucket in ("direct", "assoc", "metric", "foreign"):
        for link in mapping["overview"][bucket]:
            src = link["src"]
            if src in skip:
                continue
            rec = targets.setdefault(
                link["dwd"], {"dwd_table": link["dwd"], "sources": [], "fields": [], "kind": bucket}
            )
            if src and src not in rec["sources"]:
                rec["sources"].append(src)
    for f in mapping["fields"]:
        dwd = f["dwd"]
        if not dwd:
            continue
        rec = targets.setdefault(dwd, {"dwd_table": dwd, "sources": [], "fields": [], "kind": "direct"})
        src_table = f["src_table"]
        if src_table and src_table not in rec["sources"]:
            rec["sources"].append(src_table)
        rec["fields"].append(f)

    wave_b: list[dict] = []
    for dwd, rec in targets.items():
        alias_by_table = {src: f"T{i}" for i, src in enumerate(rec["sources"], 1)}
        out_fields = []
        for f in rec["fields"]:
            if not f.get("src_table") and rec["sources"]:
                f = dict(f, src_table=rec["sources"][0])
            if f.get("src_table") in skip:
                continue
            item = dict(f)
            item["alias"] = alias_by_table.get(item.get("src_table") or "", "T1")
            item["expr"] = expr_for(item, alias_by_table)
            if "待三方确认" in (item.get("logic") or ""):
                warnings.append(f"{dwd}.{item['tgt_field']}: 单位待三方确认，未自动 /10000")
            if item["tgt_field"] == "registered_capital" and "/ 10000" not in item["expr"]:
                item["expr"] = f"{item['alias']}.{item['src_field']} / 10000.0"
                warnings.append(f"{dwd}.registered_capital: 已强制 /10000.0（H2）")
            if item["src_field"] == "yearTime":
                warnings.append(f"{dwd}: illegal yearTime in mapping 明细")
            if item["src_field"] == "year":
                item["expr"] = item["expr"].replace("yearTime", "year")
            out_fields.append(item)
        rec["fields"] = out_fields
        rec["aliases"] = alias_by_table
        cn = ""
        for src in rec["sources"]:
            if src in a_by_name:
                cn = a_by_name[src]["cn"]
                break
        rec["cn"] = DWD_CN.get(dwd) or cn or dwd
        rec["sheet_kind"] = "data_result"
        if dwd == "enterprise_risk_summary":
            rec["pattern"] = "preagg"
            warnings.append(
                f"{dwd}: 预聚合后 MainOutput 为长表 org_id+risk_type；current/history 未按 remove_date 细拆"
            )
        elif dwd == "enterprise_finance_history":
            rec["pattern"] = "finance_iv"
        elif len(rec["sources"]) > 1:
            rec["pattern"] = "join"
        else:
            rec["pattern"] = "direct"
        wave_b.append(rec)
    return wave_b, warnings


def extra_warnings(wave_a: list[dict], mapping: dict, status: dict) -> list[str]:
    w: list[str] = []
    if status["obsolete"]:
        w.append("workpack marked 已作废 — do not generate")
    if status["deferred"]:
        w.append("workpack 暂缓投递 — DRAFT only if user explicitly asked")
    skip: set[str] = set()
    for s in mapping["overview"]["skip"]:
        skip.update(re.findall(r"dwd_[a-z0-9_]+", s))
    for t in wave_a:
        if t["mapping"] == "wash" and t["name"] in skip:
            w.append(f"{t['name']}: 02 mapping=wash but 09 §2.4 暂不映射 — Wave B skipped (09 wins)")
        if t["mapping"] == "mirror_only" and t["name"] not in skip:
            w.append(f"{t['name']}: 02 mirror_only")
    return w


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workpack", required=True)
    ap.add_argument("-o", "--out", default="-")
    args = ap.parse_args()
    root = Path(args.workpack)
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")
    files = find_workpack_files(root)
    status = workpack_status(files["readme"])
    wave_a = parse_wave_a(files["wave_a"])  # type: ignore[arg-type]
    mapping = parse_mapping(files["mapping"])  # type: ignore[arg-type]
    wave_b, map_warn = assemble_wave_b(mapping, wave_a)
    warnings = extra_warnings(wave_a, mapping, status) + map_warn
    inv = {
        "workpack": str(root),
        "status": status,
        "files": {k: str(v) if v else None for k, v in files.items()},
        "wave_a": wave_a,
        "wave_b": wave_b,
        "mirror_only": [t["name"] for t in wave_a if t["mapping"] == "mirror_only"],
        "skip_src": mapping["overview"]["skip"],
        "warnings": warnings,
        "counts": {
            "wave_a": len(wave_a),
            "wave_b": len(wave_b),
            "p0": sum(1 for t in wave_a if t["priority"] == "P0"),
        },
    }
    text = json.dumps(inv, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} wave_a={len(wave_a)} wave_b={len(wave_b)} warnings={len(warnings)}")


if __name__ == "__main__":
    main()
