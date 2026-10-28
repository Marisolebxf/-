#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_OUTPUT_VALUE · 创新产值（湾区 11 城）

口径（registry seq 106 / xlsx 49，公式 pending_cosign）：湾区城市高技术产业（制造业）
增加值 / 创新产出价值，年度、亿元。

判定：**完全不支持**。
  库内不存在任何增加值/产值/高技术产业产出表；
  9 张候选表在 gkx 280 表清单（`_work_gkx21/GKX_INVENTORY.json`）中逐一缺席；
  企业财报「营业收入」只有 3,302 家法人（占底册 1.75%），且与区域核算增加值不同量纲。

本脚本只做「缺源取证」：候选表逐一核验 + 替代表覆盖率实测 + 为什么不能替代。
不产出任何产值数字（F4：不许用 SUM(yysr) 冒充增加值）。

数据源：gkx（183.240.141.251:3318）+ 本地企业底册缓存（零 demo 依赖）。
输出：code/M_INNOV_GBA_OUTPUT_VALUE_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gba_gkx_common as C  # noqa: E402
from _gkxdb import gkx  # noqa: E402

T0 = time.time()
MID = "M_INNOV_GBA_OUTPUT_VALUE"
WORK = HERE.parent
INV = json.loads((WORK / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))

CANDIDATES = [
    ("dwd_output_value", "创新产值/产出价值明细"),
    ("dwd_org_output_value", "机构口径产值"),
    ("dwd_high_tech_output", "高技术产业产出"),
    ("dwd_industry_added_value", "行业增加值"),
    ("dwd_gdp", "地区生产总值"),
    ("dwd_region_economy", "区域经济指标"),
    ("dwd_tech_contract", "技术合同成交额"),
    ("dwd_output", "产出总表"),
    ("dwd_industrial_output", "工业总产值"),
]
# 语义相近但实为「项目成果」的表，必须点明不是产值
NEAR_MISS = [("dwd_en_project_output", "英文项目成果表（论文/成果描述，非金额）"),
             ("dwd_zh_project_output", "中文项目成果表（论文/成果描述，非金额）")]

cur = gkx()
cur.execute("SET SESSION max_execution_time=120000")

table_probe = {}
for t, desc in CANDIDATES:
    rec = {"desc": desc, "in_inventory": t in INV, "rows": INV.get(t, {}).get("rows") if t in INV else None}
    try:
        cur.execute("SELECT COUNT(*) FROM gkx." + t)
        rec["exists"] = True
        rec["count"] = int(cur.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        rec["exists"] = False
        rec["error"] = str(e)[:120]
    table_probe[t] = rec

near_probe = {}
for t, desc in NEAR_MISS:
    rec = {"desc": desc, "in_inventory": t in INV, "rows": INV.get(t, {}).get("rows")}
    try:
        cur.execute("SELECT COUNT(*) FROM gkx." + t)
        rec["exists"] = True
        rec["count"] = int(cur.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        rec["exists"] = False
        rec["error"] = str(e)[:120]
    near_probe[t] = rec

# ---- 替代路径实测：企业财报覆盖率与口径 ----
cur.execute("""SELECT COUNT(*) rows_, COUNT(DISTINCT jgid) orgs,
                      SUM(yysr IS NOT NULL AND yysr>0) yysr_pos
               FROM gkx.dwd_org_income_statement""")
fin = cur.fetchone()
fin_rows, fin_orgs, fin_pos = int(fin[0]), int(fin[1]), int(fin[2])

cur.execute("""SELECT COUNT(*) n,
                      SUM(operating_revenue IS NOT NULL AND operating_revenue>0) rev_pos,
                      SUM(arch_development_am IS NOT NULL) arch_nn,
                      SUM(development_employee IS NOT NULL) dev_nn
               FROM gkx.dwd_org_annual_financial_info""")
af = cur.fetchone()
af_rows, af_rev_pos, af_arch_nn, af_dev_nn = (int(af[0]), int(af[1] or 0), int(af[2] or 0), int(af[3] or 0))

cur.execute("""SELECT jgid, SUM(yysr) rev FROM gkx.dwd_org_income_statement
               WHERE yysr IS NOT NULL AND yysr>0 GROUP BY jgid""")
fin_by_org = cur.fetchall()
cur.execute("SELECT MIN(fbrq), MAX(fbrq) FROM gkx.dwd_org_income_statement")
fin_years = cur.fetchone()

base = C.load_base()
_, org_city, dup = C.name_city_maps(base)
agg_city = {}
mapped_orgs = 0
for jgid, rev in fin_by_org:
    c = org_city.get(jgid)
    if not c:
        continue
    mapped_orgs += 1
    a = agg_city.setdefault(c, {"city": c, "orgs": 0, "rev": 0.0})
    a["orgs"] += 1
    a["rev"] += float(rev or 0)
fin_city = sorted(agg_city.values(), key=lambda x: -x["rev"])[:15]

# 底册结构（99.82% 广东）
prov = {}
for row in base:
    prov[row[3]] = prov.get(row[3], 0) + 1
city_cnt = {}
for row in base:
    city_cnt[row[4]] = city_cnt.get(row[4], 0) + 1
gd4 = sum(city_cnt.get(c, 0) for c in C.COVERED)
base_rows = len(base)

out = {
    "metric_id": MID,
    "metric_name": "创新产值",
    "domain": "INNOV / 湾区创新监测（DS-05）",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "window": "无可核算年度（无时间序列表）",
    "unit": "亿元",
    "formula_intended": "output_value(city,y) = 高技术产业（制造业）增加值(city,y)，现价，亿元",
    "formula_actual": None,
    "output_value": None,
    "universe": {
        "documented_cities": 11,
        "computable_cities": 0,
        "cities": C.GBA11,
        "note": "11 城均无区域核算数据；连「有值但不可信」的城都没有。",
    },
    "table_probe": table_probe,
    "near_miss_tables": near_probe,
    "candidate_tables_found": sum(1 for v in table_probe.values() if v["exists"]),
    "existing_substitutes": {
        "dwd_org_income_statement": {
            "rows": fin_rows,
            "orgs": fin_orgs,
            "yysr_positive_rows": fin_pos,
            "org_coverage_of_base": C.pct(fin_orgs, base_rows, 6),
            "report_date_range": [str(fin_years[0]), str(fin_years[1])],
            "orgs_mapped_to_city": mapped_orgs,
            "city_revenue_top": [{"city": r["city"], "orgs": int(r["orgs"]), "revenue_sum": r["rev"]}
                                 for r in fin_city],
            "verdict": "企业营业收入合计 ≠ 区域增加值：覆盖 1.75% 法人、未扣中间投入、"
                       "无行业门类可与《高技术产业（制造业）分类（2017）》对齐。",
        },
        "dwd_org_annual_financial_info": {
            "rows": af_rows,
            "operating_revenue_positive": af_rev_pos,
            "arch_development_am_nonnull": af_arch_nn,
            "development_employee_nonnull": af_dev_nn,
            "verdict": "annual 表营收仅 2,191 行有值；研发费用列（arch_development_am）与研发人员列"
                       "（development_employee）整列为空（DATA_FACTS §3.10），不可用。",
        },
    },
    "base_structure": {
        "rows": base_rows,
        "province_top": sorted(prov.items(), key=lambda x: -x[1])[:5],
        "city_top": sorted(city_cnt.items(), key=lambda x: -x[1])[:6],
        "gd_four_city_share": C.pct(gd4, base_rows, 6),
        "note": "底册 99.82% 集中在深圳都市圈四城（深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979），"
                "任何「湾区 11 城」的区域核算指标都不能靠这张表拼出来。",
    },
    "external_reference_only": {
        "note": "以下为公开统计口径，可用于文档对照，但不能入库计算。",
        "gd_statistical_yearbook": "https://stats.gd.gov.cn/gdtjnj/index.html（分市地区生产总值、规模以上工业）",
        "hk_censtatd_rd": "https://www.censtatd.gov.hk/tc/scode580.html",
        "macau_dsec": "https://www.dsec.gov.mo/zh-CN/Home/Publication/YearbookOfStatistics",
        "nbs_high_tech_classification": "《高技术产业（制造业）分类（2017）》",
    },
    "why_not_substitutable": [
        "核算口径不同：增加值 = 总产出 − 中间投入（或收入法四项），营业收入是总产出侧概念且含非生产性收入。",
        "覆盖不同：企业财报只覆盖 3,302 家法人（1.75%），区域增加值覆盖全部常住单位。",
        "价格不同：增加值需现价/不变价核算，企业营收为现价且含跨区域分支机构合并问题。",
        "行业不同：registry 要求「高技术产业（制造业）」，财报无行业门类字段可与该分类对齐。",
        "时间不同：财报报告期 1989–2026 且非均衡面板，无法构造城市—年度平衡序列。",
    ],
    "structural_missing": [
        "无地区生产总值/行业增加值表（dwd_gdp、dwd_industry_added_value 在 280 表清单中缺席）。",
        "无高技术产业（制造业）分类映射表，无法从企业行业代码聚合到高技术产业。",
        "无港澳产值/增加值数据。",
        "无技术合同成交额表（dwd_tech_contract 不存在），无法用技术合同侧面替代。",
        "dwd_en_project_output / dwd_zh_project_output 是「项目成果」表（论文/成果描述），非金额表，不可顶替。",
    ],
    "support_judgment": {
        "data_support_level": "完全不支持",
        "implementable": False,
        "criteria": {
            "structure": "无表、无字段、无行业映射",
            "volume": "0 行可用增加值数据",
            "reproducible": False,
            "discriminative": False,
        },
        "blocking_gaps": [
            "9 张候选产值/增加值表全部不存在（gkx 280 表清单逐一核验）。",
            "唯一沾边的企业营收表覆盖率 1.75%，且口径不可换算为增加值。",
            "registry 要求城市—年度高技术产业增加值，库内无任何年度区域核算数据。",
        ],
        "recommendation": "标记为「无源指标」，等待统计年鉴/核算数据接入；不得用企业营收冒充。",
    },
    "runtime_sec": round(time.time() - T0, 2),
}

C.write_out(MID, out)
print(f"[{time.time() - T0:.1f}s] candidates existing={out['candidate_tables_found']}/9; "
      f"income orgs={fin_orgs:,} rows={fin_rows:,}; annual rev_pos={af_rev_pos:,}")
print("  output_value = None（完全不支持）")
