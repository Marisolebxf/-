#!/usr/bin/env python3
"""Fill GDF CDC Excel drafts from inventory.json by cloning a template shell."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

WAVE_A_NAME = "1、贴源_预填-DRAFT.xlsx"
WAVE_B_NAME = "2、明细数据_预填-DRAFT.xlsx"
WAVE_A_CALIBRATE = "1、贴源_模板.xlsx"
WAVE_B_CALIBRATE = "2、明细数据_模板.xlsx"
HERE = Path(__file__).resolve().parent
CATALOGS_PATH = HERE / "v1_calibrate_catalogs.json"

V1_MISSING = {"dwd_forg_college_org_info"}
V1_NO_FILTER = {"dwd_org_base_info", "dwd_org_org_product_info"}
V1_APPEND_LAST = ("dwd_org_org_product_info",)
V1_CONVERT = {
    "dwd_org_annual_financial_info": "年报财务信息",
    "dwd_forg_base_info": "国外机构基本信息",
    "dwd_industry_chain_news_info": "产业动态资讯",
}
V1_CONVERSION_ROWS = {
    "年报财务信息": [
        {"A": 1, "B": "year", "C": "year", "D": "yearTime", "E": "DOUBLE", "F": "空", "G": "空"},
    ],
    "国外机构基本信息": [
        {"A": 2, "C": "created_time", "D": "created_time", "E": "DATETIME"},
        {"A": 2, "C": "updated_time", "D": "updated_time", "E": "DATETIME"},
        {"A": 2, "C": "create_time", "D": "create_time", "E": "DATETIME"},
    ],
    "产业动态资讯": [
        {
            "A": 1,
            "B": (
                "CASE \n"
                "  WHEN DATE_FORMAT(`publish_date`, '%Y-%m-%d') = '0000-00-00' THEN NULL\n"
                "  ELSE `publish_date`\n"
                "END"
            ),
            "C": "publish_date",
            "D": "publish_date",
            "E": "DATE",
        },
    ],
}


def load_inv(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_template(workpack: Path, kind: str, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_file():
            raise SystemExit(f"template not found: {p}")
        return p
    local = workpack / "templates"
    names = (
        ["1、贴源_模板.xlsx", "1、贴源_预填-DRAFT.xlsx"]
        if kind == "a"
        else ["2、明细数据_模板.xlsx", "2、明细数据_预填-DRAFT.xlsx"]
    )
    for n in names:
        cand = local / n
        if cand.is_file():
            return cand
    parent = workpack.parent
    for child in sorted(parent.iterdir(), reverse=True):
        er = child / "执行结果"
        if not er.is_dir():
            continue
        for n in names:
            cand = er / n
            if cand.is_file():
                return cand
    raise SystemExit(
        f"no CDC template shell for wave-{kind}. Pass --template or put xlsx in {local} "
        "or sibling WORKPACK 执行结果/"
    )


def sheet_named(wb, *cands: str) -> Worksheet:
    for name in wb.sheetnames:
        if name in cands:
            return wb[name]
    return wb[wb.sheetnames[0]]


def clear_from_row(ws: Worksheet, start: int) -> None:
    if ws.max_row >= start:
        ws.delete_rows(start, ws.max_row - start + 1)


def write_row(ws: Worksheet, row: int, values: dict[str, object]) -> None:
    for col, val in values.items():
        ws[f"{col}{row}"] = val


def fill_wave_a(inv: dict, template: Path, out: Path, missing: set[str]) -> None:
    shutil.copy2(template, out)
    wb = load_workbook(out)
    ws = sheet_named(wb, "索引")
    clear_from_row(ws, 3)
    seq = 0
    for t in inv["wave_a"]:
        if t["name"] in missing:
            continue
        seq += 1
        r = seq + 2
        write_row(
            ws,
            r,
            {
                "A": seq,
                "B": f"#ODS_SCHEMA#.{t['name']}",
                "C": t["cn"],
                "D": "EDW_ODS",
                "E": f"#SRC_SCHEMA#.{t['name']}",
                "F": "GKX_DB",
                "G": "SRC_ENT",
                "H": "全量",
                "I": inv.get("default_filter", "is_deleted = 0") or None,
                "J": "删表重建",
            },
        )
    miss_ws = None
    for name in wb.sheetnames:
        if "没找到" in name:
            miss_ws = wb[name]
            break
    if miss_ws is None:
        miss_ws = wb.create_sheet("没找到的表")
        write_row(miss_ws, 1, {"A": "模板名称", "B": "SRC_DB_CDC_TEMPLATE"})
        write_row(
            miss_ws,
            2,
            {
                "A": "序号",
                "B": "全局标识",
                "C": "中文名称",
                "D": "目标数据源",
                "E": "来源表名",
            },
        )
    clear_from_row(miss_ws, 3)
    by_name = {t["name"]: t for t in inv["wave_a"]}
    seq = 0
    for name in missing:
        t = by_name.get(name, {"name": name, "cn": name})
        seq += 1
        write_row(
            miss_ws,
            seq + 2,
            {
                "A": seq,
                "B": f"#ODS_SCHEMA#.{t['name']}",
                "C": t.get("cn", name),
                "D": "EDW_ODS",
                "E": f"#SRC_SCHEMA#.{t['name']}",
                "J": "清空数据",
            },
        )
    drop = [n for n in wb.sheetnames if n not in (ws.title, miss_ws.title)]
    for n in drop:
        del wb[n]
    wb.save(out)


SRC_HEADER = {"A": "别名", "B": "数据类型", "C": "数据源", "D": "表名", "E": "中文名"}
FIELD_HEADER = {
    "A": "序号",
    "B": "英文名称",
    "C": "中文名称",
    "D": "类型",
    "E": "长度",
    "F": "精度",
    "G": "主键否",
    "H": "可为空",
    "I": "默认值",
    "J": "扩展属性",
}
COL_HEADER = {
    "K": "关联条件",
    "L": "过滤条件",
    "M": "分组统计条件",
    "N": "排序条件",
    "O": "别名",
    "P": "数据类型",
    "Q": "数据源",
    "R": "表名",
    "S": "是否去重",
    "T": "行数限制",
    "U": "中文名",
    "V": "扩展配置",
}
MAP_HEADER = {
    "K": "步骤",
    "L": "映射规则",
    "M": "描述",
    "O": "序号",
    "P": "英文名称",
    "Q": "中文名称",
    "R": "类型",
    "S": "长度",
    "T": "精度",
    "U": "主键否",
    "V": "可为空",
    "W": "默认值",
    "X": "扩展属性",
}
RISK_BY_SRC = {
    "dwd_org_company_abnormal": ("abnormal", "经营异常", "abnormal_id"),
    "dwd_org_company_punish": ("punishment", "行政处罚", "penalty_id"),
    "dwd_org_company_illegal": ("illegal", "严重违法", "illegal_id"),
    "dwd_org_risk_tax_punish": ("tax_punish", "税收违法", "tax_punish_id"),
    "dwd_org_opt_judicial_case": ("judicial_case", "司法案件", "case_id"),
    "dwd_org_risk_shixin": ("dishonest", "失信被执行人", "shixin_id"),
    "dwd_org_risk_zhixing": ("executed", "被执行人", "zhixing_id"),
    "dwd_org_bankruptcy_public_cases": ("bankruptcy", "破产案件", "case_no"),
    "dwd_org_bankruptcy_public_cases_list": ("bankruptcy_party", "破产案件关联人", "id"),
}


def sheet_title_for(dwd: str, cn: str) -> str:
    title = cn or dwd
    title = re.sub(r'[\\/\*\?:\[\]]', "_", title)[:31]
    return title or dwd[:31]


def is_data_result(ws: Worksheet) -> bool:
    return ws["K2"].value == "数据结果" or ws["A2"].value == "来源数据"


def src_cn(inv: dict, name: str) -> str:
    for t in inv.get("wave_a") or []:
        if t["name"] == name:
            return t["cn"]
    return name


def normalize_sources(rec: dict) -> list[str]:
    srcs = list(rec.get("sources") or [])
    dwd = rec["dwd_table"]
    pref: list[str] = []
    if dwd == "enterprise_industry_chain":
        pref = ["dwd_industry_chain_info", "dwd_org_industry_tags", "dwd_org_industry_product_tags"]
    elif dwd == "enterprise_finance_history":
        pref = ["dwd_org_annual_financial_info", "dwd_org_stock_finance_info"]
    elif dwd == "enterprise_bid":
        pref = ["dwd_bid_base_out", "dwd_bid_win_candidate_out"]
    if pref:
        srcs = [s for s in pref if s in srcs] + [s for s in srcs if s not in pref]
    return srcs


def join_k(rec: dict) -> str:
    sources = rec.get("sources") or []
    dwd = rec["dwd_table"]
    if not sources:
        return "T1"
    if dwd == "enterprise_industry_chain" and len(sources) >= 2:
        return (
            "T2\nleft join T1\n"
            "on T2.industry_code = T1.industry_code and T2.industry_link_code = T1.industry_link_code "
            "and T1.is_deleted = 0"
        )
    if len(sources) == 1:
        return "T1"
    key = "u_id" if dwd == "enterprise_bid" or any("bid_" in s for s in sources) else "org_id"
    parts = ["T1"]
    for i in range(2, len(sources) + 1):
        parts.append(f"left join T{i} on T1.{key} = T{i}.{key}")
    return " ".join(parts)


def map_row(j: int, expr: str, en: str, zh: str | None = None, typ: str = "VARCHAR", length=None) -> dict:
    row = {"L": expr, "O": j, "P": en, "Q": zh or en, "R": typ, "U": "否", "V": "是"}
    if length is not None:
        row["S"] = length
    return row


def typed_row(j: int, expr: str, f: dict) -> dict:
    """金融包：目标列类型来自 09（`varchar(255) NULL` / `decimal(20,4) NULL` / `bigint NOT NULL`）。"""
    m = re.match(r"(\w+)\s*(?:\((\d+)(?:,(\d+))?\))?\s*(NOT NULL|NULL)?", f.get("type") or "")
    typ, length, prec, nn = (m.groups() if m else ("VARCHAR", None, None, None))
    row = map_row(j, expr, f["tgt_field"], None, typ.upper(), int(length) if length else None)
    if prec:
        row["T"] = int(prec)
    row["U"] = "是" if f.get("pk") else "否"
    row["V"] = "否" if nn == "NOT NULL" else "是"
    return row


def events_union(inv: dict, rec: dict) -> tuple[list[dict], list[dict]]:
    """多源 UNION ALL：每源一个 IVi 临时视图（同构列）→ IVU 合并 → MainOutput。"""
    sources = rec.get("sources") or []
    fields = rec.get("fields") or []
    cn = rec.get("cn") or rec["dwd_table"]
    left: list[dict] = []
    right: list[dict] = []
    tgts: list[dict] = []
    for f in fields:
        if f["tgt_field"] not in [t["tgt_field"] for t in tgts]:
            tgts.append(f)
    for n, s in enumerate(sources, 1):
        if n > 1:
            right.append(COL_HEADER)
        left += [SRC_HEADER, {
            "A": f"T{n}", "B": "数据表", "C": "EDW_ODS", "D": f"#ODS_SCHEMA#.{s}", "E": src_cn(inv, s),
        }, FIELD_HEADER]
        if n == 1:
            right.append(COL_HEADER)
        right += [{
            "K": f"T{n}", "O": f"IV{n}", "P": "临时视图", "Q": "否", "U": f"{src_cn(inv, s)}清洗",
        }, MAP_HEADER]
        by_tgt = {f["tgt_field"]: f for f in fields if f["src_table"] == s}
        for j, t in enumerate(tgts, 1):
            f = by_tgt.get(t["tgt_field"])
            right.append(typed_row(j, str(f["expr"]) if f else "NULL", t))
    union_sql = "\nUNION ALL\n".join(f"SELECT * FROM IV{n}" for n in range(1, len(sources) + 1))
    right += [COL_HEADER, {
        "K": union_sql, "O": "IVU", "P": "临时视图", "Q": "否", "U": f"{cn}合并",
    }, MAP_HEADER]
    for j, t in enumerate(tgts, 1):
        right.append(typed_row(j, f"IVU.{t['tgt_field']}", t))
    right += [COL_HEADER, {
        "K": "IVU", "O": "MainOutput", "P": "输出表", "Q": "EDW_DWD",
        "R": f"#DWD_SCHEMA#.{rec['dwd_table']}", "U": cn,
    }, MAP_HEADER]
    for j, t in enumerate(tgts, 1):
        right.append(typed_row(j, f"IVU.{t['tgt_field']}", t))
    return left, right


def write_events(ws: Worksheet, left: list[dict], right: list[dict]) -> None:
    n = max(len(left), len(right))
    for i in range(n):
        cells: dict[str, object] = {}
        if i < len(left):
            cells.update(left[i])
        if i < len(right):
            cells.update(right[i])
        write_row(ws, 3 + i, cells)


def events_direct(inv: dict, rec: dict) -> tuple[list[dict], list[dict]]:
    sources = rec.get("sources") or []
    src = sources[0] if sources else ""
    cn = rec.get("cn") or rec["dwd_table"]
    left = [SRC_HEADER, {
        "A": "T1",
        "B": "数据表",
        "C": "EDW_ODS",
        "D": f"#ODS_SCHEMA#.{src}" if src else "",
        "E": src_cn(inv, src) if src else "",
    }, FIELD_HEADER]
    right = [COL_HEADER, {
        "K": join_k(rec),
        "O": "MainOutput",
        "P": "输出表",
        "Q": "EDW_DWD",
        "R": f"#DWD_SCHEMA#.{rec['dwd_table']}",
        "U": cn,
    }, MAP_HEADER]
    for j, f in enumerate(rec.get("fields") or [], 1):
        expr = str(f.get("expr") or f"T1.{f.get('src_field')}").replace("yearTime", "year")
        right.append(typed_row(j, expr, f) if f.get("type") else map_row(j, expr, f["tgt_field"]))
    for i, s in enumerate(sources[1:], 2):
        left += [SRC_HEADER, {
            "A": f"T{i}",
            "B": "数据表",
            "C": "EDW_ODS",
            "D": f"#ODS_SCHEMA#.{s}",
            "E": src_cn(inv, s),
        }, FIELD_HEADER]
    return left, right


def events_finance(inv: dict, rec: dict) -> tuple[list[dict], list[dict]]:
    sources = rec.get("sources") or []
    t1 = sources[0] if sources else "dwd_org_annual_financial_info"
    t2 = sources[1] if len(sources) > 1 else None
    fields = rec.get("fields") or []

    def iv_maps(flist: list[dict], alias: str, lit: str) -> list[dict]:
        maps: list[dict] = []
        seen: set[str] = set()
        for f in flist:
            tgt = f["tgt_field"]
            if tgt in seen:
                continue
            seen.add(tgt)
            expr = str(f.get("expr") or f"{alias}.{f.get('src_field')}").replace("yearTime", "year")
            maps.append(map_row(len(maps) + 1, expr, tgt))
        if "data_source" not in seen:
            maps.append(map_row(len(maps) + 1, f"'{lit}'", "data_source", "数据来源标识"))
        return maps

    a_fields = [f for f in fields if f.get("src_table") == t1] or fields
    s_fields = [f for f in fields if t2 and f.get("src_table") == t2]
    iv1 = iv_maps(a_fields, "T1", "annual")
    left = [SRC_HEADER, {
        "A": "T1",
        "B": "数据表",
        "C": "EDW_ODS",
        "D": f"#ODS_SCHEMA#.{t1}",
        "E": src_cn(inv, t1),
    }, FIELD_HEADER]
    right = [COL_HEADER, {
        "K": "T1",
        "L": "T1.org_id is not null",
        "O": "IV1",
        "P": "临时视图",
        "Q": "否",
        "U": "年报财务清洗",
    }, MAP_HEADER]
    right.extend(iv1)
    if t2:
        iv2 = iv_maps(s_fields, "T2", "stock")
        tgts: list[str] = []
        for m in iv1 + iv2:
            if m["P"] not in tgts:
                tgts.append(m["P"])
        iv3 = []
        for j, tgt in enumerate(tgts, 1):
            if tgt == "data_source":
                expr = "CASE WHEN IV2.org_id IS NOT NULL THEN 'stock' ELSE 'annual' END"
            else:
                expr = f"COALESCE(IV2.{tgt}, IV1.{tgt})"
            iv3.append(map_row(j, expr, tgt))
        right += [COL_HEADER, {
            "K": "T2",
            "L": "T2.org_id is not null",
            "O": "IV2",
            "P": "临时视图",
            "Q": "否",
            "U": "上市财务清洗",
        }, MAP_HEADER]
        right.extend(iv2)
        right += [COL_HEADER, {
            "K": "IV2\nleft join IV1\non IV2.org_id = IV1.org_id and IV2.data_year = IV1.data_year",
            "O": "IV3",
            "P": "临时视图",
            "Q": "否",
            "U": "合并财务历史",
        }, MAP_HEADER]
        right.extend(iv3)
        left += [SRC_HEADER, {
            "A": "T2",
            "B": "数据表",
            "C": "EDW_ODS",
            "D": f"#ODS_SCHEMA#.{t2}",
            "E": src_cn(inv, t2),
        }, FIELD_HEADER]
        main_k, main_from = "IV3", iv3
    else:
        main_k, main_from = "IV1", iv1
    right += [COL_HEADER, {
        "K": main_k,
        "O": "MainOutput",
        "P": "输出表",
        "Q": "EDW_DWD",
        "R": f"#DWD_SCHEMA#.{rec['dwd_table']}",
        "U": rec.get("cn") or "企业财务历史输出",
    }, MAP_HEADER]
    for j, m in enumerate(main_from, 1):
        right.append(map_row(j, f"{main_k}.{m['P']}", m["P"], m.get("Q")))
    return left, right


def events_preagg(inv: dict, rec: dict) -> tuple[list[dict], list[dict]]:
    left = [SRC_HEADER]
    right = [COL_HEADER]
    ivs: list[tuple[str, str]] = []
    n = 0
    for src in rec.get("sources") or []:
        meta = RISK_BY_SRC.get(src)
        if not meta:
            continue
        n += 1
        alias, iv = f"T{n}", f"IV{n}"
        typ, cn, idcol = meta
        if n > 1:
            left.append(SRC_HEADER)
            right.append(COL_HEADER)
        left += [{
            "A": alias,
            "B": "数据表",
            "C": "EDW_ODS",
            "D": f"#ODS_SCHEMA#.{src}",
            "E": src_cn(inv, src),
        }, FIELD_HEADER]
        right += [{
            "K": alias,
            "M": f"{alias}.org_id",
            "O": iv,
            "P": "临时视图",
            "Q": "否",
            "U": f"{cn}预聚合",
        }, MAP_HEADER, map_row(1, f"{alias}.org_id", "org_id", "机构id", "VARCHAR", 64),
            map_row(2, f"COUNT(DISTINCT {alias}.{idcol})", "total_count", "次数", "INT")]
        ivs.append((iv, typ))
    union_sql = "\nUNION ALL\n".join(
        "SELECT org_id, '{typ}' AS risk_type, total_count, total_count AS current_count, "
        "0 AS history_count, CAST(NULL AS DATE) AS latest_date FROM {iv}".format(typ=typ, iv=iv)
        for iv, typ in ivs
    ) or "T1"
    long_cols = [
        ("IV10.org_id", "org_id", "机构id", "VARCHAR", 64),
        ("IV10.risk_type", "risk_type", "风险类型", "VARCHAR", 50),
        ("IV10.total_count", "total_count", "风险总次数", "INT", None),
        ("IV10.current_count", "current_count", "当前次数", "INT", None),
        ("IV10.history_count", "history_count", "历史次数", "INT", None),
        ("IV10.latest_date", "latest_date", "最近发生日期", "DATE", None),
    ]
    right += [COL_HEADER, {
        "K": union_sql,
        "O": "IV10",
        "P": "临时视图",
        "Q": "否",
        "U": "风险汇总长表",
    }, MAP_HEADER]
    for j, (expr, en, zh, typ, length) in enumerate(long_cols, 1):
        right.append(map_row(j, expr, en, zh, typ, length))
    right += [COL_HEADER, {
        "K": "IV10",
        "O": "MainOutput",
        "P": "输出表",
        "Q": "EDW_DWD",
        "R": "#DWD_SCHEMA#.enterprise_risk_summary",
        "U": rec.get("cn") or "企业风险汇总",
    }, MAP_HEADER]
    for j, (expr, en, zh, typ, length) in enumerate(
        long_cols + [("NOW()", "create_time", "创建时间", "DATETIME", None), ("NOW()", "update_time", "更新时间", "DATETIME", None)],
        1,
    ):
        right.append(map_row(j, expr if not expr.startswith("NOW") else expr, en, zh, typ, length))
    return left, right


def assert_risk_summary(wb) -> None:
    if "企业风险汇总" not in wb.sheetnames:
        raise SystemExit("missing sheet 企业风险汇总")
    ws = wb["企业风险汇总"]
    if not is_data_result(ws):
        raise SystemExit("企业风险汇总 is not 数据结果 layout")
    if not any("预聚合" in str(ws[f"U{r}"].value or "") for r in range(1, 16)):
        raise SystemExit("企业风险汇总 missing 预聚合 blocks")
    cols = {ws[f"P{r}"].value for r in range(1, (ws.max_row or 1) + 1)}
    if "risk_type" not in cols or "total_count" not in cols:
        raise SystemExit("企业风险汇总 MainOutput missing long-table columns")


def fill_wave_b(inv: dict, template: Path, out: Path) -> None:
    shutil.copy2(template, out)
    wb = load_workbook(out)
    proto_src = next((n for n in wb.sheetnames if n != "索引" and is_data_result(wb[n])), None)
    if proto_src is None:
        raise SystemExit("template has no 数据结果 proto sheet")
    proto = wb.copy_worksheet(wb[proto_src])
    proto.title = "_proto"
    wipe_values(proto)
    proto["A1"] = "返回"
    proto["A2"] = "来源数据"
    proto["K2"] = "数据结果"
    for name in list(wb.sheetnames):
        if name not in ("索引", "_proto"):
            del wb[name]
    idx = sheet_named(wb, "索引")
    wipe_values(idx)
    write_row(idx, 1, {"A": "模板名称", "B": "DWD_CDC_TEMPLATE"})
    write_row(
        idx,
        2,
        {
            "A": "序号",
            "B": "全局标识",
            "C": "表中文名",
            "D": "业务主题",
            "E": "表初始化方式",
            "F": "自定义清数条件",
            "G": "插入模式",
            "H": "分区配置",
            "I": "数据描述",
            "J": "作业频率",
            "K": "运行区间",
            "L": "数据映射",
            "M": "扩展值Sheet页名称",
        },
    )
    keep = {"索引", "_proto"}
    used: set[str] = set()
    for i, rec in enumerate(inv["wave_b"], 1):
        rec = dict(rec, sources=normalize_sources(rec))
        dwd = rec["dwd_table"]
        cn = rec.get("cn") or dwd
        title = sheet_title_for(dwd, cn)
        if title in used:
            title = dwd[:31]
        used.add(title)
        write_row(
            idx,
            i + 2,
            {
                "A": i,
                "B": f"#DWD_SCHEMA#.{dwd}",
                "C": cn,
                "D": inv.get("subject", "ENT"),
                "E": "删表重建",
                "G": "正常插入",
                "L": title,
            },
        )
        ws = wb.copy_worksheet(proto)
        ws.title = title
        keep.add(title)
        pattern = rec.get("pattern") or "direct"
        if pattern == "union":
            left, right = events_union(inv, rec)
        elif pattern == "preagg" or dwd == "enterprise_risk_summary":
            left, right = events_preagg(inv, rec)
        elif pattern == "finance_iv" or dwd == "enterprise_finance_history":
            left, right = events_finance(inv, rec)
        else:
            left, right = events_direct(inv, rec)
        write_events(ws, left, right)
    for name in list(wb.sheetnames):
        if name not in keep:
            del wb[name]
    del wb["_proto"]
    if "企业风险汇总" in wb.sheetnames:
        assert_risk_summary(wb)
    wb.save(out)


def wipe_values(ws: Worksheet) -> None:
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None:
                c.value = None


def write_cells(ws: Worksheet, cells: dict) -> None:
    for coord, val in cells.items():
        ws[coord] = val


def write_conversion_sheet(ws: Worksheet, title: str) -> None:
    wipe_values(ws)
    write_row(ws, 1, {"A": "字段转换配置"})
    write_row(
        ws,
        2,
        {
            "A": "记录号",
            "B": "表达式",
            "C": "字段名",
            "D": "新字段名",
            "E": "新字段类型",
            "F": "新字段长度",
            "G": "新字段精度",
        },
    )
    for i, rec in enumerate(V1_CONVERSION_ROWS[title], 3):
        write_row(ws, i, rec)


def fill_wave_a_calibrate(inv: dict, template: Path, out: Path) -> None:
    """Index + conversion from 02 + v1 校准规则；先清空壳再写。"""
    shutil.copy2(template, out)
    wb = load_workbook(out)
    for name in list(wb.sheetnames):
        wipe_values(wb[name])
    idx = sheet_named(wb, "索引")
    write_row(idx, 1, {"A": "模板名称", "B": "SRC_DB_CDC_TEMPLATE"})
    write_row(
        idx,
        2,
        {
            "A": "序号",
            "B": "全局标识",
            "C": "中文名称",
            "D": "目标数据源",
            "E": "来源表名",
            "F": "来源数据源",
            "G": "来源系统名称",
            "H": "增量/全量",
            "I": "抽取过滤条件",
            "J": "表初始化方式",
            "K": "自定义清数条件",
            "L": "来源数据描述",
            "M": "作业频率",
            "N": "运行区间",
            "O": "扩展值Sheet页名称",
        },
    )
    miss_ws = None
    for name in wb.sheetnames:
        if "没找到" in name:
            miss_ws = wb[name]
            break
    if miss_ws is None:
        miss_ws = wb.create_sheet("没找到的表")
    write_row(miss_ws, 1, {"A": "模板名称", "B": "SRC_DB_CDC_TEMPLATE"})
    write_row(
        miss_ws,
        2,
        {
            "A": "序号",
            "B": "全局标识",
            "C": "中文名称",
            "D": "目标数据源",
            "E": "来源表名",
            "F": "来源数据源",
            "G": "来源系统名称",
            "H": "增量/全量",
            "I": "抽取过滤条件",
            "J": "表初始化方式",
            "K": "自定义清数条件",
            "L": "来源数据描述",
            "M": "作业频率",
            "N": "运行区间",
            "O": "扩展值Sheet页名称",
        },
    )
    tables = list(inv["wave_a"])
    append = [t for t in tables if t["name"] in V1_APPEND_LAST]
    idx_row = 3
    miss_row = 3
    for seq, t in enumerate(tables, 1):
        if t["name"] in V1_MISSING:
            write_row(
                miss_ws,
                miss_row,
                {
                    "A": seq,
                    "B": f"#ODS_SCHEMA#.{t['name']}",
                    "C": t["cn"],
                    "D": "EDW_ODS",
                    "E": f"#SRC_SCHEMA#.{t['name']}",
                    "F": "GKX_DB",
                    "G": "SRC_ENT",
                    "H": "全量",
                    "I": "is_deleted = 0",
                    "J": "清空数据",
                },
            )
            miss_row += 1
            continue
        if t["name"] in V1_APPEND_LAST:
            continue
        row = {
            "A": seq,
            "B": f"#ODS_SCHEMA#.{t['name']}",
            "C": t["cn"],
            "D": "EDW_ODS",
            "E": f"#SRC_SCHEMA#.{t['name']}",
            "F": "GKX_DB",
            "G": "SRC_ENT",
            "H": "全量",
            "J": "删表重建",
        }
        if t["name"] not in V1_NO_FILTER:
            row["I"] = "is_deleted = 0"
        if t["name"] in V1_CONVERT:
            row["O"] = V1_CONVERT[t["name"]]
        write_row(idx, idx_row, row)
        idx_row += 1
    for t in append:
        seq = next(i for i, x in enumerate(tables, 1) if x["name"] == t["name"])
        row = {
            "A": seq,
            "B": f"#ODS_SCHEMA#.{t['name']}",
            "C": t["cn"],
            "D": "EDW_ODS",
            "E": f"#SRC_SCHEMA#.{t['name']}",
            "F": "GKX_DB",
            "G": "SRC_ENT",
            "H": "全量",
            "J": "删表重建",
        }
        if t["name"] not in V1_NO_FILTER:
            row["I"] = "is_deleted = 0"
        write_row(idx, idx_row, row)
        idx_row += 1
    keep = {idx.title, miss_ws.title}
    for sheet_name in V1_CONVERT.values():
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(sheet_name)
        write_conversion_sheet(ws, sheet_name)
        keep.add(sheet_name)
    for name in list(wb.sheetnames):
        if name not in keep:
            del wb[name]
    wb.save(out)


def fill_wave_b_calibrate(catalogs: dict, template: Path, out: Path) -> None:
    """数据结果页：清空壳后按左右栏事件序列填写。"""
    shutil.copy2(template, out)
    wb = load_workbook(out)
    for name in list(wb.sheetnames):
        wipe_values(wb[name])
    spec_b = catalogs["wave_b"]
    write_cells(wb[sheet_named(wb, "索引").title], spec_b["index"]["cells"])
    keep = set(spec_b["sheet_order"])
    for name in spec_b["sheet_order"]:
        if name == "索引":
            continue
        if name not in wb.sheetnames:
            wb.create_sheet(name)
        ws = wb[name]
        spec = spec_b["sheets"][name]
        if spec.get("a1") is not None:
            ws["A1"] = spec["a1"]
        if spec.get("a2") is not None:
            ws["A2"] = spec["a2"]
        if spec.get("k2") is not None:
            ws["K2"] = spec["k2"]
        for ev in spec["events"]:
            r = ev["row"]
            for side in ("left", "right"):
                block = ev.get(side)
                if not block:
                    continue
                for col, val in block["cells"].items():
                    ws[f"{col}{r}"] = val
    for name in list(wb.sheetnames):
        if name not in keep:
            del wb[name]
    wb.save(out)


def write_report(inv: dict, out_dir: Path, a_path: Path, b_path: Path, missing: set[str]) -> None:
    lines = [
        "# CDC 预填生成报告",
        "",
        f"- 工作包: `{inv['workpack']}`",
        f"- Wave A 表: {inv['counts']['wave_a']}（P0={inv['counts']['p0']}）",
        f"- Wave B 目标表: {inv['counts']['wave_b']}",
        f"- 产出: `{a_path.name}` / `{b_path.name}`",
        "",
        "## 这是 DRAFT",
        "不是 GDF 执行结果。导入、跑批、`05` 回签仍由 GDF 完成。作业频率未填。",
        "",
        "## warnings",
    ]
    for w in inv.get("warnings") or []:
        lines.append(f"- {w}")
    if missing:
        lines += ["", "## --missing（没找到的表）"]
        for n in missing:
            lines.append(f"- `{n}`")
    lines += ["", "## mirror_only（只贴源不洗）"]
    for n in inv.get("mirror_only") or []:
        lines.append(f"- `{n}`")
    (out_dir / "GENERATION-REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("wave", choices=["wave-a", "wave-b", "both"])
    ap.add_argument("--workpack", required=True)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--template", default=None, help="single-wave template; ignored when wave=both")
    ap.add_argument("--template-a", default=None)
    ap.add_argument("--template-b", default=None)
    ap.add_argument("--missing", default="", help="comma-separated src table names")
    ap.add_argument(
        "--calibrate",
        action="store_true",
        help="v1 校准：允许已作废包；只留壳；Wave A 按 02+规则；Wave B 按校准目录事件填写",
    )
    ap.add_argument("--catalogs", default=str(CATALOGS_PATH))
    args = ap.parse_args()
    workpack = Path(args.workpack)
    inv = load_inv(Path(args.inventory))
    if inv.get("status", {}).get("obsolete") and not args.calibrate:
        raise SystemExit("workpack is 已作废; refuse to generate")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    missing = {s.strip() for s in args.missing.split(",") if s.strip()}
    a_path = out_dir / (WAVE_A_CALIBRATE if args.calibrate else WAVE_A_NAME)
    b_path = out_dir / (WAVE_B_CALIBRATE if args.calibrate else WAVE_B_NAME)
    wrote_a = wrote_b = False
    catalogs = None
    if args.calibrate:
        catalogs = json.loads(Path(args.catalogs).read_text(encoding="utf-8"))
    if args.wave in ("wave-a", "both"):
        tmpl_a = args.template_a or (args.template if args.wave == "wave-a" else None)
        tmpl = find_template(workpack, "a", tmpl_a)
        if args.calibrate:
            fill_wave_a_calibrate(inv, tmpl, a_path)
        else:
            fill_wave_a(inv, tmpl, a_path, missing)
        print(f"wrote {a_path}")
        wrote_a = True
    if args.wave in ("wave-b", "both"):
        tmpl_b = args.template_b or (args.template if args.wave == "wave-b" else None)
        tmpl = find_template(workpack, "b", tmpl_b)
        if args.calibrate:
            fill_wave_b_calibrate(catalogs, tmpl, b_path)
        else:
            fill_wave_b(inv, tmpl, b_path)
        print(f"wrote {b_path}")
        wrote_b = True
    if wrote_a or wrote_b:
        write_report(
            inv,
            out_dir,
            a_path if wrote_a else Path("."),
            b_path if wrote_b else Path("."),
            missing,
        )
        print(f"wrote {out_dir / 'GENERATION-REPORT.md'}")


if __name__ == "__main__":
    main()
