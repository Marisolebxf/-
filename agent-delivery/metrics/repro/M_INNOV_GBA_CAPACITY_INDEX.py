#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_GBA_CAPACITY_INDEX · 粤港澳大湾区创新能力指标（INNOV / DS-05-GBA-CAPACITY）。

王惠口径（calc-logic/INNOV/M_INNOV_GBA_CAPACITY_INDEX.md）：
  湾区 11 城，由「创新资源 / 创新机构 / 创新机制 / 创新环境」四子指数等权合成，取值 0-100。

实现（20261021 版，gkx + 授权缓存）：
  RES  创新资源 = 专利数 + 论文数 + 上市企业研发投入（最新报告期）
  ORG  创新机构 = 机构数 + 高新技术企业数 + 科研院所数
  MECH 创新机制 = 专利转移件数（机构名匹配属地）；联合专利/合作项目两维缺测（见 gaps）
  ENV  创新环境 = 有效政策数 + 高企密度
  各维在「有数据的城市」内 min-max 归一；子指数 = 可用维均值；总指数 = 四子指数等权

零专利 SQL：专利城市维读 `city_patent_year_gkx.json`（面板派生，2021–2026），
**不查 `dwd_patent`**；2017–2020 零行，本指标不涉及「前 N 年基线」，但须在 §四 披露。

输出：code/M_INNOV_GBA_CAPACITY_INDEX_out.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTS = HERE / "_snapshots21" / "innov21_facts_20261021.json"
OUT = HERE / "M_INNOV_GBA_CAPACITY_INDEX_out.json"
METRIC_ID = "M_INNOV_GBA_CAPACITY_INDEX"
GBA = ["广州市", "深圳市", "珠海市", "佛山市", "惠州市", "东莞市",
       "中山市", "江门市", "肇庆市", "香港", "澳门"]
SHORT = {c: c.replace("市", "") for c in GBA}


def minmax(vals):
    lo, hi = min(vals), max(vals)
    return [0.5] * len(vals) if hi == lo else [(v - lo) / (hi - lo) for v in vals]


def main():
    t0 = time.time()
    f = json.load(open(FACTS, encoding="utf-8"))
    base = f["base"]["gba_city_counts"]
    pat = f["patent_city"]["city_totals"]
    pap = f["paper_city"]["by_city"]
    rd = f["rd_city"]["by_city"]
    hq = f["hightech_city"]["by_city"]
    inst = f["institute_city"]
    tr = f["transfer_city"]["by_city"]
    pol = f["policy_city"]

    rows = []
    for c in GBA:
        rows.append({
            "city": c, "city_short": SHORT[c],
            "org_cnt": int(base.get(c, 0)),
            "patent_cnt": int(pat.get(c, 0)),
            "paper_cnt": int(pap.get(c, 0)),
            "rd_latest": round(float(rd.get(c, 0)), 2),
            "hightech_cnt": int(hq.get(c, 0)),
            "institute_cnt": int(inst.get(c, 0)),
            "transfer_cnt": int(tr.get(c, 0)),
            "policy_cnt": int(pol.get(c, 0)),
        })
    avail = [r for r in rows if r["org_cnt"] >= 100]
    missing = [r["city"] for r in rows if r["org_cnt"] < 100]

    if avail:
        n_pat = minmax([r["patent_cnt"] for r in avail])
        n_pap = minmax([r["paper_cnt"] for r in avail])
        n_rd = minmax([r["rd_latest"] for r in avail])
        n_org = minmax([r["org_cnt"] for r in avail])
        n_hq = minmax([r["hightech_cnt"] for r in avail])
        n_inst = minmax([r["institute_cnt"] for r in avail])
        n_tr = minmax([r["transfer_cnt"] for r in avail])
        n_pol = minmax([r["policy_cnt"] for r in avail])
        n_den = minmax([r["hightech_cnt"] / r["org_cnt"] for r in avail])
        for i, r in enumerate(avail):
            r["hightech_density"] = round(r["hightech_cnt"] / r["org_cnt"], 4)
            r["n_patent"] = round(n_pat[i], 4)
            r["n_paper"] = round(n_pap[i], 4)
            r["n_rd"] = round(n_rd[i], 4)
            r["n_org"] = round(n_org[i], 4)
            r["n_hq"] = round(n_hq[i], 4)
            r["n_inst"] = round(n_inst[i], 4)
            r["n_transfer"] = round(n_tr[i], 4)
            r["n_policy"] = round(n_pol[i], 4)
            r["n_density"] = round(n_den[i], 4)
            r["res_index"] = round(100 * (n_pat[i] + n_pap[i] + n_rd[i]) / 3, 1)
            r["org_index"] = round(100 * (n_org[i] + n_hq[i] + n_inst[i]) / 3, 1)
            r["mech_index"] = round(100 * n_tr[i], 1)
            r["env_index"] = round(100 * (n_pol[i] + n_den[i]) / 2, 1)
            r["capacity_index"] = round((r["res_index"] + r["org_index"]
                                         + r["mech_index"] + r["env_index"]) / 4, 1)

    cap_avail = [r["capacity_index"] for r in avail]
    ranking = sorted(avail, key=lambda r: -r["capacity_index"])

    out = {
        "metric_id": METRIC_ID,
        "metric_name": "粤港澳大湾区创新能力指标",
        "domain": "INNOV / DS-05-GBA-CAPACITY",
        "formula_owner": "王惠（四子指数等权，沿用 calc-logic 口径）",
        "generated_at": time.strftime("%Y-%m-%d"),
        "source_db": "gkx",
        "source_detail": {
            "专利城市维": "city_patent_year_gkx.json（面板 app_year × 底册 name→city，零 DB）",
            "论文城市维": "dwd_zh_paper.author_info_list → 底册 name_cn→city（机构名精确匹配）",
            "研发/转移/机构/政策": "gkx 小表聚合（上市财务 40,239 / 转移 22,809 / 院所 2,074 / 政策 20,000）",
        },
        "definition_used": "容量指数 = (RES+ORG+MECH+ENV)/4；子指数内各维在可用城市 min-max 后等权",
        "probes": {
            "dwd_org_base_info": f["table_counts"]["dwd_org_base_info"]["rows"],
            "dwd_patent": f["patent"]["rows"],
            "dwd_zh_paper": f["table_counts"]["dwd_zh_paper"]["rows"],
            "dwd_patent_transfer": f["transfer_city"]["rows"],
            "dwd_research_institute_base_info": f["table_counts"]["dwd_research_institute_base_info"]["rows"],
            "dwd_policy_base": f["table_counts"]["dwd_policy_base"]["rows"],
            "dwd_org_stock_finance_info": f["table_counts"]["dwd_org_stock_finance_info"]["rows"],
            "patent_city_unmapped_rows": f["patent_city"]["unmapped_all_rows"],
            "paper_inst_hit_rate": f["paper_city"]["inst_hit_rate"],
            "transfer_name_hit_rate": f["transfer_city"]["name_hit_rate"],
        },
        "city_universe": {"required": GBA, "available": [r["city"] for r in avail],
                          "missing": missing},
        "city_coverage": {r["city"]: r["org_cnt"] for r in rows},
        "rows": rows,
        "gba_capacity_avg_available": round(sum(cap_avail) / len(cap_avail), 1) if cap_avail else None,
        "ranking": [{"city": r["city"], "capacity_index": r["capacity_index"]} for r in ranking],
        "subindex_composition": {r["city"]: {"res": r.get("res_index"), "org": r.get("org_index"),
                                            "mech": r.get("mech_index"), "env": r.get("env_index")}
                                 for r in avail},
        "gaps": {
            "城市覆盖": f"11 城中仅 {len(avail)} 城有机构底册（{', '.join(r['city'] for r in avail)}）；"
                        "珠海/佛山/中山 ≤1 家、江门/肇庆/香港/澳门 0 家。"
                        "香港/澳门在 dwd_forg_base_info 无有效城市记录（country 大量为空、city 为境外城市）→ 港澳两维整体缺失",
            "联合专利": "dwd_patent 无 applicants 多申请人字段（只有 first_applicant_name 单值）；"
                        "dwd_patent_applicants 仅 28,964 行、覆盖主表 0.99% → 联合专利件数不可算",
            "合作项目": "dwd_zh_project.funded_institution 全空、participating_institution 为单一机构名（非机构列表）"
                        "→ 无法构造「跨机构合作项目」边",
            "政策主题": "dwd_policy_base.theme 字面 NULL 19,998/20,000；status 全为「有效」（20,000/20,000）"
                        "→ 政策主题覆盖与有效性判别均无区分度",
            "研发投入": f"dwd_org_stock_finance_info 仅覆盖上市主体（{f['rd_city']['orgs_with_rd']} 家有研发费用），"
                        "取每机构最新报告期后求和，仍非全市 R&D 口径（全市 R&D 需统计年鉴）",
            "专利城市归属": f"面板派生城市序列未匹配 {f['patent_city']['unmapped_all_rows']:,} 件"
                            f"（占主表 {f['patent_city']['unmapped_all_rows'] / f['patent']['rows'] * 100:.2f}%），"
                            "城市合计 + 未匹配 = 2,939,895；未匹配集中在无底册的中小主体",
            "论文城市归属": f"100,900 篇中仅 {f['paper_city']['papers_with_city']:,} 篇（"
                            f"{f['paper_city']['papers_with_city'] / f['table_counts']['dwd_zh_paper']['rows'] * 100:.2f}%）"
                            f"能按署名机构精确匹配到底册；机构名实例命中率 {f['paper_city']['inst_hit_rate'] * 100:.2f}%",
            "转移城市归属": f"22,809 条转移记录中仅 {f['transfer_city']['edges_matched']:,} 条能匹配到底册城市，"
                            f"权利人名称命中率 {f['transfer_city']['name_hit_rate'] * 100:.2f}%",
            "专利年份": "apdt_year 仅 2021–2026，2017–2020 零行；本指标用存量专利数（非增速），"
                        "但不得把城市序列解释为「历史累计」——它只覆盖 2021 年以来的申请",
            "底册偏斜": "机构底册 99.82% 在广东（深圳 95,600 / 广州 49,605 / 东莞 33,590 / 惠州 9,979），"
                        "省外样本 <0.2%；湾区内比较受影响较小，但「全国/全球湾区对比」不可解释",
            "归一化": "0-100 为「可用 4 城」内 min-max，深圳必然为 100、惠州为 0；"
                      "不可与外部湾区指数直接比较，需补珠海/佛山/中山/港澳后重标定",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure": "四子指数均有字段承载，但 MECH 仅 1/3 维可算（转移），RES 论文维仅 37.2% 论文可归属",
                "volume": f"可用城市 {len(avail)}/11；专利 293.99 万件、论文 10.09 万篇、转移 22,809 件可归属",
                "reproducible": True,
                "all_11_cities": False,
            },
            "note": "四子指数与合成公式可复现且分布非退化，但 11 城中 7 城无数据、港澳整块缺失、"
                    "MECH 两维缺测 -> 部分支持。补齐珠海/佛山/中山底册与港澳机构库后可升级。",
        },
        "elapsed_sec": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({"level": out["support_judgment"]["data_support_level"],
                      "available": out["city_universe"]["available"], "missing": missing,
                      "avg": out["gba_capacity_avg_available"], "ranking": out["ranking"],
                      "sub": out["subindex_composition"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
