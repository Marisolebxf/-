# -*- coding: utf-8 -*-
"""
SYSINT-TOPIC-CHAIN-ALIGN-02-L01 · 中间数据准备
从既有真源（只读）抽取两版对照表所需的结构化数据，输出 JSON 到本 _work/ 目录。
不连库、不改 seed、不写 ADS。上游真源：
  1. gkx-orchestration/agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx（我方 573 版底账）
  2. gkx-orchestration/agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv（久新 93 条库内支持）
  3. gkx-orchestration/agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv / 字段清单.csv（130 表字段级）
  4. gkx-orchestration/agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-CMP-02-L01/九新三要素93指标对照表-20261026.xlsx（久新↔本地映射真源）
"""
import csv
import json
import os
import re
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
def _rel(link):
    """超链接统一存主仓内相对路径（自包含）。"""
    if not link:
        return ""
    p = link.replace("file://", "")
    i = p.find("agent-delivery/")
    return p[i:] if i >= 0 else p

ORCH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "../", "../", "../", "../", "../"))  # _work → 产物 → 任务目录 → 系统集成-SYSINT → agent-handoffs → agent-delivery → 主仓根  # 主仓根（本文件已在主仓内）
XLSX_573 = os.path.join(ORCH, "agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx")
CSV_SUPPORT = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv")
CSV_TABLES = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv")
CSV_FIELDS = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/字段清单.csv")
XLSX_CMP = os.path.join(ORCH, "agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-CMP-02-L01/九新三要素93指标对照表-20261026.xlsx")

# 缺口清单（专题-产业链分析-三要素对接需求.md §3）点名的页内 metric_id → 页面/垂向
GAP_NAMED = OrderedDict([
    ("M_CHAIN_STAGE_SCORE",            ("产业周期分析", "技术（技术成熟度）")),
    ("M_CHAIN_REG_PATENT",             ("区域产业指数评价", "技术（专利）")),
    ("M_CHAIN_REG_TECH_MATURITY",      ("区域产业指数评价", "技术（技术成熟度）")),
    ("M_CHAIN_REG_RESEARCH_ORG",       ("区域产业指数评价", "科研机构")),
    ("M_CHAIN_REG_TECH_BARRIER",       ("区域产业指数评价", "技术（技术壁垒·可选）")),
    ("M_CHAIN_REG_TALENT_STRUCTURE",   ("区域产业指数评价", "人才（人才结构·可选）")),
    ("M_CHAIN_STRATEGIC_IMPORTANCE",   ("产业关键环节识别", "技术（技术壁垒）")),
    ("M_CHAIN_BOTTLENECK_TYPE_DIST",   ("产业瓶颈堵点识别", "技术+人才（五维演示位）")),
    ("M_CHAIN_SZ_PATENT",              ("深圳产业对比", "技术（专利）")),
    ("M_CHAIN_SZ_TALENT",              ("深圳产业对比", "人才")),
    ("M_CHAIN_REG_COMP_ACADEMIC",      ("区域产业竞争力评价", "科研机构（学术生态·待产品拆清）")),
    ("M_CHAIN_ACADEMIC_POWER",         ("区域产业竞争力评价", "科研机构（学术生态·待产品拆清）")),
    # 瓶颈·人才维：缺口清单 §2.4 五维统一挂 TYPE_DIST 演示位；本件有 md 但未入 573 表（如实标注）
    ("M_CHAIN_BOTTLENECK_TALENT",      ("产业瓶颈堵点识别", "人才（人才维·未独立注册）")),
])
# 未独立注册件的手工链接补充（calc-logic md 存在、repro py 无 → 如实）
UNREGISTERED_LINKS = {
    "M_CHAIN_BOTTLENECK_TALENT": (
        "agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_BOTTLENECK_TALENT.md",
        "",  # repro 无独立 py（573 表 README 已知边界第 4 条：BOTTLENECK 族留旧骨架）
    ),
}
# 页内件缺独立注册时的说明（调研记录：M_CHAIN_SZ_PATENT/_TALENT 在 573 表中存在；
# M_CHAIN_BOTTLENECK_TALENT 无独立件，由 BOTTLENECK_TYPE_DIST 演示位统一挂）


def load_573():
    """读 20261028 三系统表：按指标ID聚合（跨表单去重），保留每表单行数据与超链接。"""
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_573)
    metrics = OrderedDict()
    for ws in wb.worksheets:
        hdr = [c.value for c in ws[1]]
        idx = {h: i for i, h in enumerate(hdr)}
        for row in ws.iter_rows(min_row=2):
            vals = [c.value for c in row]
            mid = vals[idx["指标ID"]]
            if not mid:
                continue
            md_cell = row[idx["指标调研文件"]] if "指标调研文件" in idx else None
            py_cell = row[idx["指标计算 py 文件"]] if "指标计算 py 文件" in idx else None
            rec = metrics.setdefault(mid, {
                "id": mid,
                "name": vals[idx["指标名称"]],
                "sheets": [],
                "rows": [],
            })
            rec["sheets"].append(ws.title)
            rec["rows"].append({
                "sheet": ws.title,
                "name": vals[idx["指标名称"]],
                "algo_type": vals[idx["算法类型"]] if "算法类型" in idx else "",
                "support": vals[idx["数据支持度"]] if "数据支持度" in idx else "",
                "m1": vals[idx["一级模块"]] if "一级模块" in idx else "",
                "m2": vals[idx["二级模块"]] if "二级模块" in idx else "",
                "m3": vals[idx["三级模块"]] if "三级模块" in idx else "",
                "md_link": _rel(md_cell.hyperlink.target) if (md_cell and md_cell.hyperlink) else "",
                "py_link": _rel(py_cell.hyperlink.target) if (py_cell and py_cell.hyperlink) else "",
                "src_tables": vals[idx["源表字段"]] if "源表字段" in idx else "",
                "ui_mount": vals[idx["UI 挂载"]] if "UI 挂载" in idx else "",
                "jiuxin_flag": vals[idx["是否归了久新"]] if ("是否归了久新" in idx and ws.title == "科技专题算法库") else "",
            })
    return metrics


def load_support():
    with open(CSV_SUPPORT, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_tables():
    with open(CSV_TABLES, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_fields():
    with open(CSV_FIELDS, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    by_table = {}
    for r in rows:
        by_table.setdefault(r["表"], []).append({"field": r["字段"], "comment": r["注释"]})
    return rows, by_table


def load_cmp_sheet2():
    """CMP 对照表 sheet2：93 行逐指标对照（久新模型名/口径证据/候选表/集成模式）。"""
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_CMP, read_only=True)
    ws = wb["2-逐指标对照"]
    it = ws.iter_rows(values_only=True)
    hdr = list(next(it))
    out = []
    for vals in it:
        if not vals or not vals[1]:
            continue
        d = dict(zip(hdr, vals))
        out.append({k: (v if v is not None else "") for k, v in d.items()})
    return out


def main():
    m573 = load_573()
    support = load_support()
    tables = load_tables()
    fields_all, fields_by_table = load_fields()
    cmp2 = load_cmp_sheet2()

    # ---- 版本一（我方 573 版）行集 ----
    tri_prefix = ("M_TECH_", "M_TALENT_", "M_ORG_")
    ours = []
    for mid, rec in m573.items():
        if mid.startswith(tri_prefix):
            ours.append({"kind": "三要素域件", "page": "", "vertical": ""})
            ours[-1].update(rec)
    for mid, (page, vert) in GAP_NAMED.items():
        fam = [m for m in m573 if m == mid or m.startswith(mid + "_")]
        if not fam:
            md_l, py_l = UNREGISTERED_LINKS.get(mid, ("", ""))
            ours.append({"kind": "页内点名件（未独立注册）", "page": page, "vertical": vert,
                         "id": mid, "name": "", "sheets": [], "rows": [{
                             "md_link": _rel(md_l),
                             "py_link": _rel(py_l),
                             "name": "", "algo_type": "", "support": "", "m1": "", "m2": "", "m3": "",
                             "src_tables": "", "ui_mount": "", "sheet": "",
                         }]})
            continue
        for m in fam:
            ours.append({"kind": "页内点名件", "page": page, "vertical": vert})
            ours[-1].update(m573[m])
    # 支持信息挂接
    sup_by_id = {r["metric_id"]: r for r in support}
    for row in ours:
        s = sup_by_id.get(row["id"])
        row["jiuxin_support"] = s if s else None

    # ---- 版本二（久新版）行集 ----
    cmp_by_id = {}
    for r in cmp2:
        cmp_by_id[r["metric_id"]] = r
    jiuxin = []
    for s in support:
        mid = s["metric_id"]
        c = cmp_by_id.get(mid, {})
        ours_rec = m573.get(mid)
        jiuxin.append({
            "metric_id": mid,
            "domain": s["域"],
            "name_cn": s["中文名"],
            "jiuxin_rows": c.get("挂靠九新行", ""),
            "jiuxin_model": c.get("九新模型名", ""),
            "jiuxin_evidence": c.get("九新口径证据", ""),
            "candidate_tables": s["有行的候选表"],
            "db_support": s["库内支持"],
            "algorithm_type": s["algorithm_type"],
            "d1": s["D1"], "d4": s["D4"],
            "note": s["说明"],
            "ours_exists": ours_rec is not None,
            "ours_sheets": ours_rec["sheets"] if ours_rec else [],
            "ours_md": ours_rec["rows"][0]["md_link"] if ours_rec and ours_rec["rows"] else "",
            "ours_py": ours_rec["rows"][0]["py_link"] if ours_rec and ours_rec["rows"] else "",
        })

    out = {
        "meta": {
            "gen_date": "2026-10-31",
            "task": "SYSINT-TOPIC-CHAIN-ALIGN-02-L01（WBS-02-11）草稿数据",
            # 主仓内相对路径（自包含，不含本机绝对路径）
            "upstreams": [XLSX_573.replace(ORCH + "/", ""), CSV_SUPPORT.replace(ORCH + "/", ""),
                          CSV_TABLES.replace(ORCH + "/", ""), CSV_FIELDS.replace(ORCH + "/", ""),
                          XLSX_CMP.replace(ORCH + "/", "")],
        },
        "count_573": len(m573),
        "count_support": len(support),
        "count_tables": len(tables),
        "count_fields": len(fields_all),
        "ours": ours,
        "jiuxin": jiuxin,
        "fields_by_table": fields_by_table,
        "tables": tables,
    }
    with open(os.path.join(HERE, "prepared.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("573 全量:", len(m573))
    print("版本一行数（我方视角）:", len(ours), "（三要素域件", sum(1 for r in ours if r['kind'] == '三要素域件'), "+ 页内点名", sum(1 for r in ours if r['kind'].startswith('页内点名')), "）")
    print("版本二行数（久新视角）:", len(jiuxin))
    print("130 表:", len(tables), "；字段:", len(fields_all))
    missing_md = [r["id"] for r in ours if r["rows"] and not r["rows"][0]["md_link"]]
    print("版本一缺 md 链接的已注册件:", missing_md)


if __name__ == "__main__":
    main()
