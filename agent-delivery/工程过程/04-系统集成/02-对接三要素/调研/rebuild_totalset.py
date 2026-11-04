# -*- coding: utf-8 -*-
"""Regenerate 总集对照.csv from the md-extract sheet CSVs and the fresh scan.

Rules (unchanged from the 2026-10-22 pass):
- Theme mapping only. Same theme = the Jiuxin library has a same-subject table.
- No same-name primary key claim. 同名不等于同一套 ID.
"""
import csv
import io
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSVDIR = Path(__file__).resolve().parents[4] / "data" / "third-party-source" / "doc" / "md-extract" / "_csv"

WORKBOOKS = {
    "市场研究（金融、宏观行业、行业分析、产业链）数据汇总表": ["金融要素库", "宏观行业要素库", "行业分析要素库", "产业链要素库"],
    "版权人才、企业机构、政策数据汇总表": ["国内机构要素库", "国外机构要素库", "人才要素库", "国内政策要素库", "国外政策要素库"],
    "行业专题数据汇总表": ["医药专题要素库", "化学专题要素库", "海洋专题要素库", "量子专题要素库"],
    "论文、专利、项目、报告数据汇总表": ["中文论文要素库", "外文论文要素库", "全球专利要素库", "国内项目要素库", "国外项目要素库", "中文报告要素库", "外文报告要素库"],
}


def theme_match(lib, table_en):
    if lib == "人才要素库":
        return "ads_talent_*", "主题对应", "总集主键在 dwd_scholar，久新主键是 talent_id"
    if lib == "国内机构要素库":
        return "ads_institution_*", "主题对应", "企业、招投标、司法、财务没有进久新机构画像。企业类型是 company，不把企业算成科研机构"
    if lib == "国外机构要素库":
        return "ads_institution_*", "主题对应", "久新不另建国外机构表"
    if lib in ("中文论文要素库", "外文论文要素库"):
        return "ads_paper_* 及论文关系表", "主题对应", "久新论文来自 OpenAlex work，身份列是 openalex_work_id。同名只有 doi、页码、卷期、paper_type。不是同一主键"
    if lib == "全球专利要素库":
        return "ads_patent_*、ads_patent_analysis_*、ads_talent_patent、ads_technology_patent、ads_institution_patent", "主题对应", "久新专利身份是平台 patent_id。同名不等于同一套 ID。新增 ads_patent_analysis_* 23 张是久新自己的分析族"
    if lib == "国内项目要素库":
        return "ads_project_*", "主题对应", "久新上游叫 grant。项目金额列已出现（amount_cny），口径未对齐"
    if lib == "国外项目要素库":
        return "ads_project_*", "主题对应", "久新上游叫 grant"
    if lib == "国内政策要素库":
        return "ads_technology_policy_evidence、ads_research_problem_policy_evidence", "还没有接上", "总集有 dwd_policy_base。技术政策证据表仍 0 行；研究问题政策证据有行但同名字段 0 个"
    if lib == "国外政策要素库":
        return "ads_research_problem_policy_evidence", "还没有接上", "总集有 dwd_global_policy_base。研究问题政策证据有 1,252 行，同名字段 0 个，还没有接上"
    if lib in ("中文报告要素库", "外文报告要素库"):
        return "无", "久新库还没有", "久新库里没有报告主体"
    if lib == "金融要素库":
        return "无", "久新库还没有", "久新没有证券、基金、行情、并购。ads_technology_profile 的投资额是规则模拟，不是已核验市场金额"
    if lib == "宏观行业要素库":
        return "无", "久新库还没有", "总集有指数和行政区划。不是 ads_location"
    if lib == "行业分析要素库":
        return "无", "久新库还没有", "总集有文档表。不是论文，也不是技术节点"
    if lib == "产业链要素库":
        if "news" in (table_en or ""):
            return "无", "久新库还没有", "ads_media_* 是技术媒体分析族，不是产业链资讯表"
        return "无", "久新库还没有", "ads_industry 与 ads_sz_gkx_industry_cluster* 只是分类/集群映射，不是总集产业链图谱、产品、企业标签 4 张表"
    if lib in ("医药专题要素库", "化学专题要素库", "海洋专题要素库", "量子专题要素库"):
        return "无", "久新库还没有", "久新没有这些专题表"
    return "无", "久新库还没有", "总集已有该表。久新库里没有同主题主体。"


def main():
    data = json.loads((HERE / "_raw_schema.json").read_text(encoding="utf-8"))
    tables = {t["table"] for t in data["tables"]}
    rows = []
    for workbook, libs in WORKBOOKS.items():
        for lib in libs:
            path = CSVDIR / f"{workbook}__{lib}.csv"
            if not path.exists():
                print("missing", path.name)
                continue
            seen = {}
            counts = Counter()
            for r in csv.reader(io.open(path, encoding="utf-8-sig")):
                if len(r) < 3 or not r[2]:
                    continue
                en, cn = r[2].strip(), (r[1] or "").strip()
                if en in ("英文表名",) or en.startswith("_col"):
                    continue
                if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", en):
                    continue
                if en not in seen:
                    seen[en] = cn
                counts[en] += 1
            for table_en, table_cn in seen.items():
                ref, verdict, note = theme_match(lib, table_en)
                jiuxin = ref if verdict != "久新库还没有" else (
                    "无" if not any(t in tables for t in re.findall(r"ads_[a-z_0-9]+", ref)) else ref)
                rows.append({
                    "总集工作簿": workbook,
                    "要素库": lib,
                    "总集中文表名": table_cn,
                    "总集英文表名": table_en,
                    "字段数": counts[table_en],
                    "对应": verdict,
                    "久新表": jiuxin,
                    "说明": note,
                })
    out = HERE / "总集对照.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows", dict(Counter(r["对应"] for r in rows)))
    by_lib = {}
    for r in rows:
        by_lib.setdefault(r["要素库"], Counter())[r["对应"]] += 1
    for lib, c in by_lib.items():
        print(lib, dict(c))


if __name__ == "__main__":
    main()
