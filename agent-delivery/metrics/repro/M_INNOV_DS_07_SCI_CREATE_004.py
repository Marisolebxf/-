#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_07_SCI_CREATE_004 科学创造力趋势预测（王惠口径复现 · 20261021 改源版）

口径（王惠 calc-logic/INNOV/M_INNOV_SCI_FORECAST.md）：
  按题名关键词入集领域论文；三维 = 论文数量 / 网络中心性（作者单位去重）/ 科学研究前沿性（当年新单位）；
  对逐年件数 Holt 外推，输出点预测与约 80% 区间。

数据源（20261021 版）：**只读三方库 gkx**
   gkx.dwd_zh_paper（100,900 篇）/ gkx.dwd_en_paper（1,387 篇）/ gkx.dwd_patent（对照）
   —— gkx 与旧开发库 ods 同名表逐表镜像（DATA_FACTS §2），故本脚本与旧版逐字同算法，
      读数应完全一致；脚本内不再出现任何 demo schema，连接入口统一走 `_gkxdb`。
"""
import json
import os
import re
import time
from collections import Counter, defaultdict

import _innov_gkx21_common as ic

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "M_INNOV_DS_07_SCI_CREATE_004_out.json")

# 领域的题名关键词（可扩展；本脚本取语料量最大的 3 个作演示，其余保留计数）
DOMAINS = {
    "人工智能": ["人工智能", "深度学习", "神经网络", "机器学习", "智能算法"],
    "医学临床": ["临床", "患者", "疗效", "诊断", "病例"],
    "新材料": ["材料", "合金", "复合材料", "涂层", "陶瓷"],
    "电力能源": ["电网", "电力", "储能", "光伏", "新能源"],
    "通信网络": ["通信", "5G", "无线", "网络切片", "物联网"],
    "中医药": ["中药", "中医", "方剂", "针灸", "药理学"],
}
YEARS = list(range(2015, 2027))
FIT_YEARS = list(range(2015, 2024))   # 拟合窗（2024 语料回填峰不入拟合）


def main():
    t0 = time.time()
    out = {"metric_id": "M_INNOV_DS_07_SCI_CREATE_004", "probes": {}, "domains": {}, "compute": {}}
    bag = {"bad_json": 0}

    # 行数只读库存 json（GKX_INVENTORY.json），不重复 COUNT(*) 千万级表
    out["probes"]["dwd_zh_paper"] = ic.count("dwd_zh_paper")
    out["probes"]["dwd_en_paper"] = ic.count("dwd_en_paper")
    out["probes"]["dwd_patent"] = ic.count("dwd_patent")

    # ---- 单遍扫描：领域 → 年 → 论文 / 机构边 / 机构首现 ----
    dom_year_cnt = defaultdict(Counter)             # dom -> year -> n_paper
    dom_year_inst = defaultdict(lambda: defaultdict(Counter))   # dom -> year -> inst -> n
    dom_year_edge = defaultdict(lambda: defaultdict(Counter))   # dom -> year -> (i,j) -> n
    dom_first_year = defaultdict(dict)              # dom -> inst -> first year
    inst_all_year_share = defaultdict(Counter)      # 全语料机构年分布（披露用）
    year_papers = Counter()
    med_inst = 0
    inst_instances = 0
    papers_total = 0
    papers_with_inst = 0

    for p in ic.iter_papers(bag):
        y = p["year"]
        try:
            y = int(str(y)[:4])
        except Exception:
            continue
        papers_total += 1
        year_papers[y] += 1
        if not p["insts"]:
            continue
        papers_with_inst += 1
        insts = sorted(p["insts"])
        inst_instances += len(insts)
        med_inst += sum(1 for i in insts if ic.MED_RX.search(i))
        for i in insts:
            inst_all_year_share[i][y] += 1
        title = p["title"] or ""
        for dom, kws in DOMAINS.items():
            if not any(k.lower() in title.lower() for k in kws):
                continue
            dom_year_cnt[dom][y] += 1
            for i in insts:
                dom_year_inst[dom][y][i] += 1
                if i not in dom_first_year[dom]:
                    dom_first_year[dom][i] = y
            for a in range(len(insts)):
                for b in range(a + 1, len(insts)):
                    dom_year_edge[dom][y][(insts[a], insts[b])] += 1

    # ---- 英文论文（体量极小，作中英双源披露） ----
    en_rows = ic.q("SELECT cover_year_start y, zh_name, en_name FROM gkx.dwd_en_paper")
    en_dom = Counter()
    for r in en_rows:
        try:
            y = int(str(r[0])[:4])
        except Exception:
            continue
        if y not in YEARS:
            continue
        title = (r[1] or r[2] or "")
        for dom, kws in DOMAINS.items():
            if any(k.lower() in title.lower() for k in kws):
                en_dom[(dom, y)] += 1

    out["probes"].update({
        "papers_with_institution": papers_with_inst, "papers_total_scanned": papers_total,
        "bad_json": bag["bad_json"],
        "year_papers_2015_2026": {str(y): year_papers.get(y, 0) for y in YEARS},
        "distinct_institutions_all": len(inst_all_year_share),
        "medical_institution_instance_share": round(med_inst / max(inst_instances, 1), 4),
        "author_institution_instances": inst_instances,
        "en_papers_total": len(en_rows),
        "en_papers_in_window": sum(en_dom.values()),
    })

    # ---- 选域：按窗口内篇数 ----
    rank = sorted(DOMAINS, key=lambda dm: -sum(dom_year_cnt[dm].get(y, 0) for y in YEARS))
    out["compute"]["domain_volume_rank"] = [
        {"domain": dm, "papers_2015_2026": sum(dom_year_cnt[dm].get(y, 0) for y in YEARS)}
        for dm in rank]
    picked = rank[:3]

    for dom in picked:
        ser = []
        n_inst_by_year = {}
        for y in YEARS:
            n = dom_year_cnt[dom].get(y, 0)
            insts = dom_year_inst[dom].get(y, {})
            k = len(insts)
            n_inst_by_year[y] = k
            edges = dom_year_edge[dom].get(y, {})
            deg = Counter()
            for (i, j), w in edges.items():
                deg[i] += w
                deg[j] += w
            centrality = (sum(deg.values()) / max(k - 1, 1) / max(k, 1)) if k > 1 else 0.0
            new_n = sum(1 for i in insts if dom_first_year[dom].get(i) == y)
            frontier = new_n / k if k else 0.0
            new_3y = sum(1 for i in insts if (dom_first_year[dom].get(i) or 0) >= y - 2)
            frontier3 = new_3y / k if k else 0.0
            ser.append({"year": y, "papers": n, "papers_en": en_dom.get((dom, y), 0),
                        "institutions": k, "coauthor_edges": len(edges),
                        "net_centrality": round(centrality, 4),
                        "new_institutions": new_n, "frontier_ratio": round(frontier, 4),
                        "new_inst_3y": new_3y, "frontier_ratio_3y": round(frontier3, 4)})
        fit = [s for s in ser if s["year"] in FIT_YEARS]
        nv = ic.norm01([s["papers"] for s in fit])
        nc = ic.norm01([s["net_centrality"] for s in fit])
        nf = ic.norm01([s["frontier_ratio"] for s in fit])
        nf3 = ic.norm01([s["frontier_ratio_3y"] for s in fit])
        comp = [(nv[i] + nc[i] + nf[i]) / 3 for i in range(len(fit))]
        comp3 = [(nv[i] + nc[i] + nf3[i]) / 3 for i in range(len(fit))]
        for i, s in enumerate(fit):
            s["composite"] = round(comp[i], 4)
            s["composite_frontier3y"] = round(comp3[i], 4)
        fc_comp = ic.holt_fit(comp, h=2)
        fc_comp3 = ic.holt_fit(comp3, h=2)
        fc_paper = ic.holt_fit([s["papers"] for s in fit], h=2)
        # 用 2024/2025 实际值做外推校验
        actual = {s["year"]: s for s in ser}
        valid = []
        for k, yy in enumerate([FIT_YEARS[-1] + 1, FIT_YEARS[-1] + 2]):
            if yy in actual:
                a = actual[yy]["papers"]
                pred = fc_paper["point"][k]
                valid.append({"year": yy, "actual_papers": a, "pred_papers": pred,
                              "in_80ci": fc_paper["lo80"][k] <= a <= fc_paper["hi80"][k],
                              "ape": round(abs(a - pred) / max(a, 1), 4)})
        out["domains"][dom] = {
            "series": ser, "fit_years": FIT_YEARS,
            "forecast_composite_2024_2025": fc_comp,
            "forecast_composite_frontier3y_2024_2025": fc_comp3,
            "forecast_papers_2024_2025": fc_paper,
            "validation": valid,
            "weights": {"papers": 1 / 3, "centrality": 1 / 3, "frontier": 1 / 3},
            "weights_source": "王惠写「加权平均」未给数值；本实现取等权并在 §2.6.1 披露，属代理权重",
        }

    out["compute"]["fit_window"] = {"from": FIT_YEARS[0], "to": FIT_YEARS[-1],
                                   "excluded_2024_note": "2024 年论文数 32,379 为语料回填形成的孤峰（2015-2023 均值约 5,090），不入拟合窗"}
    out["compute"]["corpus_2024_spike"] = {"2023": year_papers.get(2023, 0), "2024": year_papers.get(2024, 0),
                                           "2025": year_papers.get(2025, 0), "2026": year_papers.get(2026, 0)}
    out["elapsed_s"] = round(time.time() - t0, 1)
    out["data_source"] = {"schema": "gkx", "host": "183.240.141.251:3318",
                          "tables": ["gkx.dwd_zh_paper", "gkx.dwd_en_paper", "gkx.dwd_patent"],
                          "row_counts_from": "_work_gkx21/GKX_INVENTORY.json"}

    # ---- 支持度机判：结构 + 当前量 + 现转成功 ----
    ok = (out["probes"]["dwd_zh_paper"] > 50000 and bag["bad_json"] == 0
          and any(v["forecast_papers_2024_2025"] for v in out["domains"].values()))
    out["support_judgment"] = "完全转换支持" if ok else "部分支持"
    out["support_reason"] = (
        "无现成「科学创造力趋势预测」结果面（三方库 gkx 与 live 开发库均无该指标物化表）；"
        "但王惠三维所需字段（论文题名、发表年、作者机构）在 gkx.dwd_zh_paper 全量 100,900 篇、零坏 JSON 下齐备，"
        "且已现算出三维年度序列与 Holt 点预测+80% 区间，故判完全转换支持。"
        if ok else "论文语料与机构字段不足以支撑三维现算。")
    out["disclosures"] = [
        "dwd_en_paper 仅 1,387 篇，中英双源实为「中文为主 + 英文极少量」，英文维权重实际可忽略。",
        "2024 年论文数 32,379 为语料回填孤峰（相邻年约 6.1-6.9k），拟合窗取 2015-2023，2024/2025 仅作外推校验。",
        "机构名未做消歧：71,118 个不同写法（含学院/实验室层级），网络中心性对名称粒度敏感。",
        f"论文语料医学偏斜：按篇内去重机构实例统计，医疗类机构占 {out['probes']['medical_institution_instance_share']:.2%}"
        "（MOCK_TABLE_REGISTRY §9.2 按作者-机构实例口径为 36.6%，两口径差异已在正文说明）。",
        "三维权重为等权「代理权重」：王惠只写「加权平均」未给数值，甲方签认前不得当作正式口径。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: out[k] for k in ["probes", "compute"]}, ensure_ascii=False, indent=1)[:4500])
    for dm, v in out["domains"].items():
        print("\n==", dm, "papers fit:", [(s["year"], s["papers"], s["composite"]) for s in v["series"] if s["year"] in FIT_YEARS])
        print("   fc_paper:", v["forecast_papers_2024_2025"])
        print("   fc_comp:", v["forecast_composite_2024_2025"])
        print("   valid:", v["validation"])
    print("\nsupport:", out["support_judgment"], "elapsed", out["elapsed_s"])


if __name__ == "__main__":
    main()
