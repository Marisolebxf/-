#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_09_COMPREHENSIVE_005 本地特色与优势分析（王惠口径＝区位商 LQ · 20261021 改源版）

王惠口径（calc-logic/INNOV/M_INNOV_PLAN_LOCAL_ADV.md）：
  本地（默认深圳）按 IPC 前 4 位入集；三维 = 专利区位商 / 论文区位商 / 创新资源区位商；LQ>1 为优势领域。

数据源（20261021 版）：**只读三方库 gkx**
  gkx.dwd_patent（IPC4 + first_applicant_name）/ gkx.dwd_org_base_info（name_cn→city）/
  gkx.dwd_zh_paper（author_info_list.institution 判本地；题名词典法定方向）

与旧版唯一的算法差异（属数据陷阱修正，不是换口径）：
  旧版 `LEFT JOIN gkx.dwd_org_base_info ON name_cn = first_applicant_name` 在
  `dwd_org_base_info` 的 **47 个重名**（DATA_FACTS §3.5）上会把同一批专利复制成两行，
  使「带 IPC 专利」合计被抬高。本版改为：按 `(IPC4, first_applicant_name)` 分组后
  在 Python 侧用**按名称去重后的** name→city 映射打属地，天然一专利一行，
  去重规则与冲突明细见 `_innov_gkx21_common.org_name_city()`。
"""
import json
import os
import time
from collections import Counter

import _innov_gkx21_common as ic

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "M_INNOV_DS_09_COMPREHENSIVE_005_out.json")
LOCAL = "深圳"

# 论文方向词典（论文无 IPC，按题名词表定向；与专利 IPC4 分属两套方向体系，故分维报 LQ）
PAPER_DOMAINS = {
    "人工智能": ["人工智能", "深度学习", "神经网络", "机器学习", "智能算法", "大模型"],
    "临床医学": ["临床", "患者", "疗效", "诊断", "病例", "手术"],
    "中医药": ["中药", "中医", "方剂", "针灸", "药理"],
    "材料科学": ["材料", "合金", "复合", "涂层", "陶瓷", "纳米"],
    "电力能源": ["电网", "电力", "储能", "光伏", "新能源", "电池"],
    "通信网络": ["通信", "5G", "无线", "物联网", "光通信", "信号"],
    "建筑工程": ["建筑", "施工", "结构", "桥梁", "隧道", "地铁"],
    "生态环境": ["生态", "环境", "污染", "水质", "碳排放", "大气"],
    "农业食品": ["农业", "水稻", "土壤", "食品", "作物", "养殖"],
    "管理经济": ["管理", "经济", "金融", "商业模式", "绩效", "政策"],
    "机械制造": ["机械", "机器人", "数控", "装备", "加工", "动力学"],
    "生物技术": ["基因", "蛋白", "细胞", "微生物", "发酵", "生物"],
}


def patent_ipc4_by_name():
    """一次扫描：`(IPC4, 第一申请人)` 粒度专利件数，落缓存供复算。

    不 JOIN 机构表——`dwd_org_industry_tags.credit_code` 类无索引问题在这里同样成立，
    `dwd_org_base_info.name_cn` 也无索引；把归属放到 Python 侧既避免 47 个重名复制，
    也避免 294 万行 × 18.9 万行的嵌套循环。
    """
    d = ic.load_cache("patent_ipc4_by_name_20261021.json")
    if d is None:
        rows = ic.q("SELECT LEFT(main_classification_ipcr,4) ipc4, first_applicant_name nm, COUNT(*) c "
                    "FROM gkx.dwd_patent "
                    "WHERE main_classification_ipcr IS NOT NULL AND main_classification_ipcr <> '' "
                    "GROUP BY 1,2")
        d = [[str(r[0]), str(r[1] or ""), int(r[2] or 0)] for r in rows]
        ic.save_cache("patent_ipc4_by_name_20261021.json", d)
    return d


def main():
    t0 = time.time()
    out = {"metric_id": "M_INNOV_DS_09_COMPREHENSIVE_005", "local": LOCAL,
           "probes": {}, "compute": {}, "lq": {}}

    out["probes"]["dwd_patent"] = ic.count("dwd_patent")
    out["probes"]["dwd_org_base_info"] = ic.count("dwd_org_base_info")
    out["probes"]["dwd_zh_paper"] = ic.count("dwd_zh_paper")
    omp = ic.org_name_city()
    city_totals = omp["city_totals"]
    out["probes"]["org_city_sz"] = sum(n for c, n in city_totals.items() if LOCAL in (c or ""))

    # ---------- 专利维 + 创新资源维：IPC4 × 属地 ----------
    nm_city = omp["map"]
    all_pat, sz_pat = Counter(), Counter()
    all_org, sz_org = Counter(), Counter()
    unmatched = Counter()
    dup_names_hit = set()
    for ipc, nm, c in patent_ipc4_by_name():
        all_pat[ipc] += c
        all_org[ipc] += 1
        city = nm_city.get(nm)
        if city is None:
            unmatched[ipc] += c
            continue
        if LOCAL in city:
            sz_pat[ipc] += c
            sz_org[ipc] += 1
    T_all, T_sz = sum(all_pat.values()), sum(sz_pat.values())
    O_all, O_sz = sum(all_org.values()), sum(sz_org.values())
    out["probes"].update({
        "dwd_patent_ipc_nn": T_all,
        "patent_with_ipc_in_scope": T_all, "patent_local": T_sz,
        "patent_local_share": round(T_sz / max(T_all, 1), 4),
        "ipc4_distinct": len(all_pat),
        "applicant_org_instances_all": O_all, "applicant_org_instances_local": O_sz,
        "applicant_names_unmatched_rows": sum(unmatched.values()),
        "applicant_names_unmatched_pct": round(sum(unmatched.values()) / max(T_all, 1), 4),
        "locality_tag_method": "first_applicant_name → 按 name_cn 去重后的 org 名称→城市映射；"
                               "未命中者不计本地（保守口径）",
        "org_name_duplicates": {"total_rows": ic.count("dwd_org_base_info"),
                               "named_rows": omp["n_rows"],
                               "blank_name_rows": ic.count("dwd_org_base_info") - omp["n_rows"],
                               "distinct_names": omp["n_names"],
                               "dup_names": omp["n_rows"] - omp["n_names"],
                               "dup_names_cross_city": len(omp["dup_name_conflicts"]),
                               "rule": "同名取城市出现次数最多者，次数相同取字典序最小；"
                                       "打标在 Python 侧完成，不对机构表做 SQL JOIN（避免重名复制专利行）"},
        "name_join_hit_distinct_100k": 0.9414,
        "name_join_note": "94.14%/86.98% 为 2026-10-20 既有 10 万名称/10 万专利行抽样读数，"
                          "本次未重抽（抽样复现不改变口径），按历史测量沿用",
    })

    lq_pat = {}
    lq_res = {}
    for ipc in all_pat:
        if all_pat[ipc] < 200:
            continue
        lq_pat[ipc] = (sz_pat[ipc] / T_sz) / (all_pat[ipc] / T_all)
        lq_res[ipc] = (sz_org[ipc] / max(O_sz, 1)) / (all_org[ipc] / max(O_all, 1))

    out["lq"]["patent_ipc4"] = {
        "n_directions": len(lq_pat),
        "top15_lq_gt1": sorted(
            [{"ipc4": k, "lq": round(v, 4), "local_patents": sz_pat[k], "all_patents": all_pat[k],
              "local_share": round(sz_pat[k] / max(all_pat[k], 1), 4)}
             for k, v in lq_pat.items() if v > 1], key=lambda x: (-x["lq"], x["ipc4"]))[:15],
        "bottom8": sorted(
            [{"ipc4": k, "lq": round(v, 4), "local_patents": sz_pat[k], "all_patents": all_pat[k]}
             for k, v in lq_pat.items()], key=lambda x: (x["lq"], x["ipc4"]))[:8],
        "distribution": ic.dist(list(lq_pat.values())),
        "n_lq_gt1": sum(1 for v in lq_pat.values() if v > 1),
        "n_lq_gt1_2": sum(1 for v in lq_pat.values() if v > 1.2),
    }
    out["lq"]["innovation_resource_ipc4"] = {
        "n_directions": len(lq_res),
        "top10_lq_gt1": sorted(
            [{"ipc4": k, "lq": round(v, 4), "local_orgs": sz_org[k], "all_orgs": all_org[k]}
             for k, v in lq_res.items() if v > 1], key=lambda x: (-x["lq"], x["ipc4"]))[:10],
        "distribution": ic.dist(list(lq_res.values())),
    }

    # ---------- 论文维：属地＝篇内出现深圳机构；方向＝题名词典 ----------
    bag = {"bad_json": 0}
    sz_dom = Counter()
    all_dom = Counter()
    sz_papers = all_papers = 0
    sz_inst_names = Counter()
    for p in ic.iter_papers(bag):
        title = p["title"] or ""
        insts = p["insts"]
        if not insts:
            continue
        all_papers += 1
        is_sz = any(LOCAL in i for i in insts)
        if is_sz:
            sz_papers += 1
            for i in insts:
                if LOCAL in i:
                    sz_inst_names[i] += 1
        doms = [dm for dm, kws in PAPER_DOMAINS.items() if any(k in title for k in kws)]
        for dm in doms:
            all_dom[dm] += 1
            if is_sz:
                sz_dom[dm] += 1
    lq_paper = {}
    for dm in all_dom:
        if all_dom[dm] < 100:
            continue
        lq_paper[dm] = (sz_dom[dm] / max(sz_papers, 1)) / (all_dom[dm] / max(all_papers, 1))
    out["probes"].update({
        "papers_scoped": all_papers, "papers_local": sz_papers,
        "papers_local_share": round(sz_papers / max(all_papers, 1), 4),
        "distinct_local_institutions_paper": len(sz_inst_names),
        "bad_json": bag["bad_json"],
    })
    out["lq"]["paper_domain"] = {
        "n_directions": len(lq_paper),
        "by_domain": sorted(
            [{"domain": k, "lq": round(v, 4), "local_papers": sz_dom[k], "all_papers": all_dom[k]}
             for k, v in lq_paper.items()], key=lambda x: (-x["lq"], x["domain"])),
        "top5_local_institutions": sz_inst_names.most_common(5),
    }

    # ---------- 三维合成：优势方向排序 ----------
    # 排序键与并列规则：主键 LQ 合成值降序，次键 IPC4 升序（保证全序、可复现）。
    # 名次语义取 competition rank（1,2,2,4）：合成值相同者同名次、后续跳号 —— 与
    # RANK() 语义一致，而非 DENSE_RANK()（1,2,2,3）。理由见 MD §2.6.2。
    comp = []
    for ipc, v in lq_pat.items():
        comp.append({"direction_type": "IPC4", "direction": ipc,
                     "lq_patent": round(v, 4), "lq_resource": round(lq_res.get(ipc, 0), 4),
                     "lq_composite": round((v + lq_res.get(ipc, 0)) / 2, 4),
                     "local_patents": sz_pat[ipc]})
    comp.sort(key=lambda x: (-x["lq_composite"], x["direction"]))
    rank = 0
    prev = None
    for i, x in enumerate(comp, 1):
        if x["lq_composite"] != prev:
            rank, prev = i, x["lq_composite"]
        x["rank_competition"] = rank
    out["compute"]["top20_advantage_ipc4"] = comp[:20]
    out["compute"]["n_directions_scored"] = len(comp)
    out["compute"]["n_patent_lq_gt1"] = sum(1 for x in comp if x["lq_patent"] > 1)
    out["compute"]["n_patent_lq_gt1_2"] = sum(1 for x in comp if x["lq_patent"] > 1.2)
    out["compute"]["tie_structure"] = {
        "n_directions": len(comp),
        "n_distinct_composite": len({x["lq_composite"] for x in comp}),
        "largest_tie_group": max(Counter(x["lq_composite"] for x in comp).values()),
        "rank_rule": "competition rank（同分同名次、后续跳号），次键 IPC4 升序",
    }
    out["compute"]["weight_source"] = {
        "lq_composite": "专利 LQ 与创新资源 LQ 等权平均（0.5/0.5）",
        "provenance": "王惠未给三维权重；等权为本实现自定，属**代理权重**，"
                      "仅用于优势方向排序，不改变「专利 LQ>1 即优势」的判定",
        "not_summed": "论文 LQ 与 IPC4 合成值不合并：两者方向体系不同（12 个题名域 vs 456 个 IPC4），"
                      "直接相加会把不同分类轴的份额混淆",
    }
    out["compute"]["logical_consistency"] = {
        "patent_lq_gt1_and_resource_lq_gt1": sum(
            1 for x in comp if x["lq_patent"] > 1 and x["lq_resource"] > 1),
        "patent_lq_gt1_but_resource_lq_lt1": sum(
            1 for x in comp if x["lq_patent"] > 1 and x["lq_resource"] <= 1),
    }
    out["elapsed_s"] = round(time.time() - t0, 1)
    out["data_source"] = {"schema": "gkx", "host": "183.240.141.251:3318",
                          "tables": ["gkx.dwd_patent", "gkx.dwd_org_base_info", "gkx.dwd_zh_paper"],
                          "row_counts_from": "_work_gkx21/GKX_INVENTORY.json"}

    ok3 = (T_sz > 500000 and len(lq_pat) > 100 and sz_papers > 500)
    # 需求明列的第四维「与全球水平的对比分析」在三方库/开发库均无境外产出语料，属始终缺失的依赖维
    out["three_local_dims_ok"] = bool(ok3)
    out["support_judgment"] = "部分支持"
    out["support_reason"] = (
        "三方库 gkx 与 live 开发库均无「本地特色与优势」结果面；王惠三维所需结构齐备且量足："
        f"专利侧 {T_all:,} 件带 IPC（本地 {T_sz:,} 件）、论文侧 {sz_papers:,} 篇含深圳机构署名，"
        "已现算出 IPC4 专利区位商、创新资源区位商与论文分域区位商。"
        "但需求原文明列第四项输出「提供与全球水平的对比分析」，三方库与开发库均无境外专利/论文的属地可比语料"
        "（gkx.dwd_forg_* 仅为海外机构名录，不含产出），该维无法构建，故判部分支持。")
    out["disclosures"] = [
        "属地打标依赖 first_applicant_name 与 gkx.dwd_org_base_info.name_cn 精确同名（10 万名称抽样命中 94.14%、按专利行 86.98%），"
        "未命中者按「非本地」处理，本地份额为保守下界。",
        "「全域」= 本语料全域（专利公开库 242.09 万件带 IPC、论文 10.09 万篇），非全国统计年鉴口径；"
        "dwd_org_base_info 99.82% 集中于广东，本地/全域对比实为「深圳 vs 含深圳的全国公开库」。",
        "论文方向用题名词典法定向（12 个域），因 gkx.dwd_zh_paper_classification 仅 20,048 行且与论文主表 JOIN 仅命中 799 篇（0.79%），"
        "无法按王惠「中文关键词」原路径定向，属口径替换，需甲方确认。",
        "专利属地打标不再对机构表做 SQL JOIN：改名去重后按名称映射，避免 47 个重名把同一批专利复制成两行"
        "（旧版因此把带 IPC 合计抬高 79 件，见 §2.2）。",
        "论文语料医学偏斜：篇内去重机构实例中医疗类占 22.34%。",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out["probes"], ensure_ascii=False, indent=1))
    print(json.dumps(out["lq"]["paper_domain"]["by_domain"], ensure_ascii=False))
    print(json.dumps(out["compute"]["top20_advantage_ipc4"][:12], ensure_ascii=False, indent=1))
    print(json.dumps(out["lq"]["patent_ipc4"]["top15_lq_gt1"][:10], ensure_ascii=False))
    print(json.dumps(out["lq"]["patent_ipc4"]["distribution"], ensure_ascii=False))
    print(json.dumps(out["compute"]["tie_structure"], ensure_ascii=False))
    print("support", out["support_judgment"], out["elapsed_s"])


if __name__ == "__main__":
    main()
