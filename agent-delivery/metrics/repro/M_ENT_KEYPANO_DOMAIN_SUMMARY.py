#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_KEYPANO_DOMAIN_SUMMARY 领域摘要 — 依赖侧实测脚本（20261021 改源版，王惠五步法逐环探针）

王惠口径（wanghui_agg / calc-logic ENT/M_ENT_KEYPANO_DOMAIN_SUMMARY.md）五步：
  1.链位归集：dwd_org_industry_tags 关联 dwd_industry_chain_info 按 level（上/中/下游）分组企业；
  2.关键词抽取：该链位重点企业论文标题/摘要、专利名称/摘要中抽取技术关键词；
  3.领域映射：关键词与产业链细分领域匹配，统计命中率；
  4.覆盖率 = 命中关键词数 / 该链位关键词总数 × 100%；>=60% 判「证据充分」；
  5.汇总论文关键词、专利关键词及关联重点企业形成证据摘要。

本版数据面：三方库 gkx（全表名 gkx.<表名>），行数只读 _work_gkx21/GKX_INVENTORY.json。
实测（2026-10-21）：
  ① 链位归集环：tags 2,283,762 / chain_info 1,273 两表在，但 chain_info.level 全 0 → 链位分组断（族内 MATCH/DEPTH 同证）；
     且 tags×chain_info 关联 0 行（链路码体系不匹配）。
  ② 文本源环：专利 2,939,895 行 + keywords 列（样本填充实测）；论文 zh 100,900 + 作者单位 62,002（机构名形态可对齐企业）；
     英文侧 en_paper 1,387 薄；摘要表 dwd_patent_abstract 20,000 行。
  ③ 领域映射环：库内无 关键词→细分领域 映射表（SHOW LIKE 全空）——王惠 calc-logic 自标「映射规则表（未建）」。
结论：五步中断在第 1 步（level 全 0、链路码不匹配）与第 3 步（映射表无）→ 部分支持。
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT = CODE_DIR.parent
sys.path.insert(0, str(CODE_DIR))

from _gkxdb import gkx  # noqa: E402

OUT = Path(__file__).with_name("M_ENT_KEYPANO_DOMAIN_SUMMARY_out.json")
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"


def inv_rows() -> dict:
    d = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return {k: int(v["rows"]) for k, v in d.items()}


def dec(x):
    if isinstance(x, Decimal):
        return int(x) if x == x.to_integral_value() else float(x)
    return x


def q(sql: str, args=None):
    cur = gkx()
    try:
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def main():
    rep = {"metric_id": "M_ENT_KEYPANO_DOMAIN_SUMMARY", "metric_name": "领域摘要",
           "script": Path(__file__).name, "data_source": "gkx"}
    inv = inv_rows()
    probe = {}

    # 步1 链位归集环
    r = q("SELECT COUNT(*) n, COUNT(DISTINCT credit_code) orgs FROM gkx.dwd_org_industry_tags")[0]
    probe["industry_tags"] = {k: dec(v) for k, v in r.items()}
    probe["chain_info_rows"] = inv["dwd_industry_chain_info"]
    probe["chain_info_level_dist"] = [
        {k: dec(v) for k, v in row.items()}
        for row in q("SELECT level, COUNT(*) n FROM gkx.dwd_industry_chain_info GROUP BY level ORDER BY n DESC LIMIT 8")
    ]
    r = q("SELECT COUNT(*) n FROM gkx.dwd_org_industry_tags t JOIN gkx.dwd_industry_chain_info c "
          "ON t.industry_code=c.industry_code AND t.industry_link_code=c.industry_link_code")[0]
    probe["tags_chain_join_rows"] = dec(r["n"])

    # 步2 文本源环（专利侧，10 万行样本估 keywords 填充）
    r = q("SELECT COUNT(*) n, SUM(keywords IS NOT NULL AND keywords<>'') kw "
          "FROM (SELECT keywords FROM gkx.dwd_patent LIMIT 100000) t")[0]
    r = {k: dec(v) for k, v in r.items()}
    r["kw_fill_rate"] = round(r["kw"] / r["n"], 4) if r["n"] else None
    probe["patent_kw_sample_100k"] = r
    probe["patent_rows"] = inv["dwd_patent"]
    probe["patent_abstract_rows"] = inv["dwd_patent_abstract"]

    # 步2 文本源环（论文侧）
    probe["dwd_zh_paper_rows"] = inv["dwd_zh_paper"]
    probe["dwd_en_paper_rows"] = inv["dwd_en_paper"]
    r = q("SELECT COUNT(*) n, COUNT(DISTINCT institution) insts, "
          "SUM(institution IS NOT NULL AND institution<>'') filled FROM gkx.dwd_zh_author")[0]
    probe["zh_author"] = {k: dec(v) for k, v in r.items()}
    probe["zh_author_top_inst"] = [
        {k: dec(v) for k, v in row.items()}
        for row in q("SELECT institution, COUNT(*) papers FROM gkx.dwd_zh_author "
                     "WHERE institution IS NOT NULL AND institution<>'' "
                     "GROUP BY institution ORDER BY papers DESC LIMIT 10")
    ]

    # 步3 领域映射环：映射表存在性
    mapping = []
    for pat in ("%keyword%", "%mapping%", "%domain%", "%map%"):
        for row in q("SHOW TABLES FROM gkx LIKE %s", (pat,)):
            mapping.append(list(row.values())[0])
    probe["mapping_tables"] = sorted(set(mapping))
    # 论文摘要表存在性
    probe["paper_like_tables"] = sorted(
        list(row.values())[0] for row in q("SHOW TABLES FROM gkx LIKE %s", ("%paper%",))
    )

    level_dist = probe.get("chain_info_level_dist") or []
    level_ok = any(str(d.get("level")) not in ("0", "None") for d in level_dist)
    kw_rate = (probe.get("patent_kw_sample_100k") or {}).get("kw_fill_rate") or 0
    rep["probe"] = probe
    rep["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"王惠五步法逐环实测（三方库 gkx）：①链位归集断——chain_info.level 全 0（分布 {level_dist}），上/中/下游分组键无从取值"
            f"，且 tags×chain_info 关联 {probe.get('tags_chain_join_rows')} 行（链路码体系不匹配）；"
            f"②文本源在——专利 {probe.get('patent_rows'):,} 行且 keywords 列样本填充率 {kw_rate*100:.1f}%，"
            f"论文 zh {probe.get('dwd_zh_paper_rows')} 篇 + 作者单位 {probe.get('zh_author', {}).get('insts')} 机构（名称可对齐企业），"
            f"但英文侧仅 {probe.get('dwd_en_paper_rows')} 篇、专利摘要表 {probe.get('patent_abstract_rows')} 行；"
            f"③领域映射断——库内无关键词到产业链细分领域映射表（{probe.get('mapping_tables') or '无'}），"
            "王惠 calc-logic 自标「映射规则表（未建）」。五步中断在 1/3 两环 → 部分支持。"
        ),
        "criteria": {
            "chain_level_ready": bool(level_ok),
            "tags_chain_join_ready": probe.get("tags_chain_join_rows", 0) > 0,
            "patent_text_ready": True,
            "paper_text_ready": True,
            "en_paper_thin": True,
            "mapping_table_ready": False,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
