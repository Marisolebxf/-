#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_09_RESEARCH_002 研究领域等级划分 — 20261021 换源复现脚本

口径（王惠，calc-logic/INNOV/M_INNOV_RES_GRADE.md）：
  复用 M_INNOV_RES_OVERLAP 的企业对合成重叠度，按 P70 / P30 分高/中/低。
  重叠度 = 三维 Jaccard 的可用维等权：IPC4 集合 / 关键词集合 / 学者集合。

数据面（20261021）：**三方库 gkx**（`183.240.141.251:3318`），经 `_gkxdb.gkx()` 连接。
原 20261020 版读旧开发库（现以停用、不再使用）；gkx 与其逐表镜像（`dwd_patent` 2,939,895、
`dwd_scholar` 21,316、`dwd_zh_author` 62,002 均一致），故本脚本只换数据面、不改公式。

取数：`_inn_res21_build.py` 已把 294 万行宽表的重扫结果落到
`code/_snapshots21/research_*_20261021.json`，本脚本读缓存计算，不再扫专利表。

产物：M_INNOV_DS_09_RESEARCH_002_out.json
      _snapshots21/research_feature_cache_20261021.json（供 003 / 004 复用）
"""
import json
import time
from itertools import combinations
from pathlib import Path
from statistics import mean, median

import _inn_res21_common as C

HERE = Path(__file__).parent
MID = "M_INNOV_DS_09_RESEARCH_002"
DB = "gkx@183.240.141.251:3318"
CACHE_NAME = "research_feature_cache_20261021.json"


def load_all():
    nm = C.load_cache("research_names_20261021.json")
    names = nm["u2"]["names"]
    ipc = C.load_cache("research_ipc_union_20261021.json")["sets"]
    kww = C.load_cache("research_kw_002_20261021.json")
    sch = C.load_cache("research_scholar_sets_20261021.json")["sets"]
    edges = C.load_cache("research_paper_edges_20261021.json")
    fill = C.load_cache("research_fill_20261021.json")
    return nm, names, ipc, kww, sch, edges, fill


def main():
    t0 = time.time()
    nm, names, ipc_raw, kww, sch_raw, edges, fill = load_all()
    ipc = {n: set(ipc_raw.get(n, [])) for n in names}
    kw = {n: set(kww["sets"].get(n, [])) for n in names}
    sch = {n: set(sch_raw.get(n, [])) for n in names}
    papers = {n: edges["papers"].get(n, []) for n in names}
    pk = edges["paper_keywords"]

    # 论文关键词并入关键词维（王惠口径「专利与论文关键词」）
    n_paper_kw_used = 0
    for n in names:
        for pid in papers[n]:
            toks = pk.get(str(pid))
            if toks:
                kw[n] |= set(toks)
                n_paper_kw_used += 1

    out = {"metric_id": MID, "name": "研究领域等级划分",
           "formula_owner": "王惠", "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
           "db": DB, "probes": {}, "universe": [], "thresholds": {}, "grades": {},
           "distribution": {}, "pairs": [], "disclosures": [], "support_judgment": None}

    # ---------- 1. 行数探针（库存）+ 填充率（一次聚合落盘） ----------
    p = {"dwd_patent": fill["rows"]["dwd_patent"],
         "dwd_org_base_info": fill["rows"]["dwd_org_base_info"],
         "dwd_scholar": fill["rows"]["dwd_scholar"],
         "dwd_zh_author": fill["rows"]["dwd_zh_author"],
         "dwd_zh_paper": fill["rows"]["dwd_zh_paper"],
         "dwd_zh_paper_classification": fill["rows"]["dwd_zh_paper_classification"],
         "dwd_scholar_coauthor": fill["rows"]["dwd_scholar_coauthor"],
         "dwd_patent_with_ipc": fill["patent"]["rows_with_ipc"],
         "dwd_patent_with_keywords": "未重扫（全表非空 2,939,760，20261020 同表实测；"
                                     "本批只逐家统计 66 家入集机构 486,827 件）",
         "dwd_zh_author_with_institution": fill["dwd_zh_author_with_institution"],
         "dwd_scholar_with_org": fill["dwd_scholar_with_org"],
         "candidate_applicants": nm["u2"].get("candidate_n", 120),
         "matched_to_org_base": nm["u2"].get("matched", len(names)),
         "universe_size": len(names)}
    out["probes"] = p
    print("probes", p, flush=True)

    # ---------- 2. 入集企业画像 ----------
    org = nm.get("u2_org", {})
    for n in names:
        o = org.get(n) or {}
        out["universe"].append({
            "name": n, "patents": nm["u2"]["patents"].get(n), "org_id": o.get("org_id"),
            "city": o.get("city"), "industry_l2": None,
            "n_ipc4": len(ipc[n]), "n_kw": len(kw[n]), "n_scholar": len(sch[n]),
            "n_paper": len(papers[n])})

    # ---------- 3. 两两重叠度 ----------
    pairs = []
    for a, b in combinations(names, 2):
        ji = C.jac(ipc[a], ipc[b])
        jk = C.jac(kw[a], kw[b])
        js = C.jac(sch[a], sch[b])
        dims = [x for x in (ji, jk, js) if x is not None]
        ov = sum(dims) / len(dims) if dims else None
        pairs.append({"a": a, "b": b, "ipc_jac": None if ji is None else round(ji, 4),
                      "kw_jac": None if jk is None else round(jk, 4),
                      "scholar_jac": None if js is None else round(js, 4),
                      "n_dims": len(dims), "overlap": None if ov is None else round(ov, 4)})
    valid = [x["overlap"] for x in pairs if x["overlap"] is not None]
    zero_share = sum(1 for v in valid if v == 0) / len(valid) if valid else None

    # ---------- 4. 阈值：全样本 P70/P30 + 仅正重叠子集 ----------
    pos = [v for v in valid if v > 0]
    out["thresholds"] = {
        "p70_all_pairs": round(C.pct(valid, 0.70), 4) if valid else None,
        "p30_all_pairs": round(C.pct(valid, 0.30), 4) if valid else None,
        "p70_positive_only": round(C.pct(pos, 0.70), 4) if pos else None,
        "p30_positive_only": round(C.pct(pos, 0.30), 4) if pos else None,
        "n_pairs": len(valid), "n_positive": len(pos),
        "zero_share": round(zero_share, 4) if zero_share is not None else None,
        "note": "全样本阈值在零膨胀时退化（P70 可能为 0 → 全部判高）；"
                "故同时给出仅正重叠子集阈值作稳健性对照。"}

    p70 = out["thresholds"]["p70_all_pairs"]
    p30 = out["thresholds"]["p30_all_pairs"]
    grade = {"高": 0, "中": 0, "低": 0, "缺失": 0}
    for x in pairs:
        if x["overlap"] is None:
            x["grade"] = "缺失"
        elif x["overlap"] >= p70:
            x["grade"] = "高"
        elif x["overlap"] >= p30:
            x["grade"] = "中"
        else:
            x["grade"] = "低"
        grade[x["grade"]] += 1
    out["grades"] = grade

    p70p = out["thresholds"]["p70_positive_only"]
    p30p = out["thresholds"]["p30_positive_only"]
    gp = {"高": 0, "中": 0, "低": 0}
    if p70p is not None:
        for x in pairs:
            if not x["overlap"]:
                continue
            if x["overlap"] >= p70p:
                gp["高"] += 1
            elif x["overlap"] >= p30p:
                gp["中"] += 1
            else:
                gp["低"] += 1
    out["grades_positive_only"] = gp

    out["distribution"] = {
        "min": min(valid) if valid else None, "max": max(valid) if valid else None,
        "mean": round(mean(valid), 4) if valid else None,
        "median": round(median(valid), 4) if valid else None,
        "p90": round(C.pct(valid, 0.90), 4) if valid else None,
        "p99": round(C.pct(valid, 0.99), 4) if valid else None,
        "n_dims_mean": round(mean([x["n_dims"] for x in pairs]), 2)}
    out["pairs"] = sorted([x for x in pairs if x["overlap"] is not None],
                          key=lambda z: -z["overlap"])[:25]
    out["pairs_zero_examples"] = [x for x in pairs if x["overlap"] == 0][:5]

    # ---------- 5. 覆盖统计 ----------
    out["paper_link"] = {
        "rule": "dwd_zh_author.institution LIKE '企业名%'（前缀匹配，覆盖院系后缀）",
        "exact_papers": edges["exact_papers"],
        "prefix_papers": edges["prefix_papers"],
        "n_firms_with_paper": edges["n_firm_with_paper"],
        "paper_keywords_linked": n_paper_kw_used,
    }
    out["feature_coverage"] = {
        "n_universe": len(names),
        "n_with_ipc": sum(1 for n in names if ipc[n]),
        "n_with_kw": sum(1 for n in names if kw[n]),
        "n_with_scholar": sum(1 for n in names if sch[n]),
        "n_with_paper": sum(1 for n in names if papers[n]),
        "ipc4_mean_set_size": round(mean([len(ipc[n]) for n in names]), 2),
        "kw_mean_set_size": round(mean([len(kw[n]) for n in names]), 2),
        "scholar_mean_set_size": round(mean([len(sch[n]) for n in names]), 2),
        "kw_sample_patents_per_firm": kww["sample_per_firm"],
        "kw_json_parse_ok": kww["json_ok"], "kw_json_parse_bad": kww["json_bad"],
        "papers_linked": edges["prefix_papers"],
        "paper_keywords_linked": len(pk),
        "paper_kw_tokens_added": n_paper_kw_used,
        "paper_classification_rows": fill["rows"]["dwd_zh_paper_classification"],
        "paper_classification_delimiter": "逗号分隔文本（非 JSON 数组）→ 按 JSON 解析命中 0 篇，"
                                          "论文关键词实际未进入关键词维",
    }

    su = fill["scholar_universe"]
    out["disclosures"] = [
        "企业入集依赖 first_applicant_name 与 dwd_org_base_info.name_cn 的精确同名匹配，未做名称归一化；"
        "同一集团多法人、简称/全称并存会漏配",
        "dwd_org_base_info 99.82% 集中在广东（深圳 9.56 万 / 广州 4.96 万），本指标的企业集是深圳都市圈样本，"
        "不代表全国企业竞争格局",
        "关键词维按每家企业前 LIMIT %d 件专利抽样，IPC4 维为全量；抽样率见 feature_coverage"
        % kww["sample_per_firm"],
        "论文→企业的机构边按 dwd_zh_author.institution 前缀匹配企业名（覆盖院系后缀），"
        "但仍受机构名书写不规范影响（exact 命中 %d 篇 → 前缀命中 %d 篇）"
        % (edges["exact_papers"], edges["prefix_papers"]),
        "dwd_patent.keywords 存在字面字符串 'null'（JSON null），按缺失处理；本批对入集 66 家的"
        "全部 %d 件专利逐行解析，成功 %d / 缺失 %d / 解析失败 %d（失败率 %.2f%%）"
        % (fill["patent"]["kw_ok_of_universe"] + fill["patent"]["kw_null_of_universe"]
           + fill["patent"]["kw_bad_of_universe"], fill["patent"]["kw_ok_of_universe"],
           fill["patent"]["kw_null_of_universe"], fill["patent"]["kw_bad_of_universe"],
           100.0 * fill["patent"]["kw_bad_of_universe"] /
           (fill["patent"]["kw_ok_of_universe"] + fill["patent"]["kw_null_of_universe"]
            + fill["patent"]["kw_bad_of_universe"])),
        "学者宇宙双基线：dwd_scholar %d 位，dwd_scholar_talent_flag %d 位，二者 scholar_id 交集仅 %d 位"
        "（%.2f%%）。本指标的学者维**只用 dwd_scholar，分母固定写 %d**，不与人才标签宇宙混算；"
        "任何『学者覆盖率』引用都必须写明分母，禁止拿一张表的分子除另一张表的分母"
        % (su["dwd_scholar"], su["dwd_scholar_talent_flag"], su["intersect"],
           su["intersect_pct"] * 100, su["dwd_scholar"]),
        "dwd_scholar.scholar_org_id 全表 %d 行全为空串，学者—机构只能靠机构名字符串对齐，"
        "这是学者维覆盖低的结构性原因" % fill["dwd_scholar_org_id_empty"],
        "`dwd_zh_paper_classification.keywords` 实测是**逗号分隔文本**（`中药鉴定学,综合能力,教学改革`），"
        "不是 JSON 数组；旧版解析器按 JSON 解析、失败即返回空集，所谓「并入 348 篇」实际是 348 个空集，"
        "本版已如实记为 0 个词条。若甲方确认要把论文关键词真正并入 D2，需把该列按逗号切分后重算，"
        "届时 002/003/004 的分值与阈值会整体右移，属口径变更、需先签认",
        "全部取值来自三方库 gkx 的真实表（dwd_patent / dwd_org_base_info / dwd_scholar / "
        "dwd_zh_author / dwd_zh_paper_classification），未引用任何 mock_* / demo_* 面",
    ]

    # ---------- 6. 四档判定（机判） ----------
    out["support_judgment"] = {
        "level": "部分支持",
        "reason": "三维重叠度均可算（IPC4/关键词/学者），但学者维覆盖率仅 "
                  + str(out["feature_coverage"]["n_with_scholar"]) + "/" + str(len(names))
                  + "，论文→企业机构边仅 " + str(edges["prefix_papers"])
                  + " 篇，且等级阈值在零膨胀下退化（zero_share="
                  + str(out["thresholds"]["zero_share"]) + "）——始终有一维数据不足。",
    }

    # ---------- 7. 特征缓存（供 003 / 004 复用） ----------
    cache = {"names": names,
             "patents": {n: nm["u2"]["patents"].get(n) for n in names},
             "org": {n: {"org_id": (org.get(n) or {}).get("org_id"),
                         "city": (org.get(n) or {}).get("city"),
                         "industry_l2": None} for n in names},
             "ipc": {n: sorted(ipc[n]) for n in names},
             "kw": {n: sorted(kw[n]) for n in names},
             "scholar": {n: sorted(sch[n]) for n in names},
             "papers": {n: len(papers[n]) for n in names},
             "pairs": pairs,
             "thresholds": out["thresholds"],
             "disclosures": out["disclosures"],
             "built_at": out["run_at"]}
    C.save_cache(CACHE_NAME, cache)

    out["runtime_sec"] = round(time.time() - t0, 1)
    dest = C.write_out(MID, out)
    print("saved", dest, "runtime", out["runtime_sec"], "grade", grade)


if __name__ == "__main__":
    main()
