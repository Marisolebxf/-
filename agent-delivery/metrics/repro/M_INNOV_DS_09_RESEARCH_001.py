#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_09_RESEARCH_001 研究领域重叠度（王惠口径＝三维 Jaccard）— 20261021 换源版

王惠口径（calc-logic/INNOV/M_INNOV_RES_OVERLAP.md）：
  选定企业入集；三维 = IPC 重叠 / 关键词重叠 / 学者重叠（均为 Jaccard |A∩B|/|A∪B|），
  可用维等权平均得 0—1 重叠度。

数据面（20261021）：**三方库 gkx**（`183.240.141.251:3318`），经 `_gkxdb.gkx()`。
  原版读旧开发库（20261021 起已停用、不再使用）；gkx 与其逐表镜像（`dwd_patent` 2,939,895、
  `dwd_zh_paper` 100,900、`dwd_scholar` 21,316 一致），本版只换数据面、不改公式。

取数：`_inn_res21_build.py` 已把专利宽表重扫结果落到 `code/_snapshots21/`，
本脚本读缓存计算。

产物：M_INNOV_DS_09_RESEARCH_001_out.json
"""
import json
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import _inn_res21_common as C

HERE = Path(__file__).parent
MID = "M_INNOV_DS_09_RESEARCH_001"
DB = "gkx@183.240.141.251:3318"
KW_TOP = 80
GRADES = [(0.8, "极高"), (0.6, "高"), (0.4, "中"), (0.2, "低"), (0.0, "极低")]


def grade(v):
    for th, g in GRADES:
        if v >= th:
            return g
    return "极低"


def main():
    t0 = time.time()
    nm = C.load_cache("research_names_20261021.json")
    names = nm["u1"]["names"]
    ipc_raw = C.load_cache("research_ipc_union_20261021.json")["sets"]
    kww = C.load_cache("research_kw_001_20261021.json")
    pa = C.load_cache("research_paper_authors_20261021.json")
    fill = C.load_cache("research_fill_20261021.json")

    out = {"metric_id": MID, "probes": {}, "compute": {},
           "db": DB, "run_at": time.strftime("%Y-%m-%d %H:%M:%S")}

    out["probes"]["dwd_patent"] = fill["rows"]["dwd_patent"]
    out["probes"]["dwd_zh_paper"] = fill["rows"]["dwd_zh_paper"]
    out["probes"]["dwd_scholar"] = fill["rows"]["dwd_scholar"]
    out["probes"]["n_companies"] = len(names)

    # ---------- 入集机构（深圳 + 专利 >=30，按专利量 Top40） ----------
    comp_rows = [{"name": n, "patents": nm["u1"]["patents"][n]} for n in names]
    companies = [r["name"] for r in comp_rows]
    out["compute"]["companies"] = comp_rows

    # ---------- D1：IPC4 集合 ----------
    ipcs = {n: set(ipc_raw.get(n, [])) for n in companies}

    # ---------- D2：关键词集合（词频 Top80） ----------
    kw_sets = {n: {t for t, _ in (kww["top"].get(n) or [])[:KW_TOP]} for n in companies}
    out["probes"]["kw_companies"] = sum(1 for n in companies if kw_sets.get(n))
    out["probes"]["kw_sample_per_firm"] = kww["sample_per_firm"]

    # ---------- D3：学者集合（企业署名论文作者，代理口径） ----------
    sets = pa["sets"]
    scholar_sets = {}
    for n in companies:
        s = set(sets.get(n, []))
        if s:
            scholar_sets[n] = s
    out["probes"]["companies_with_scholar_set"] = len(scholar_sets)
    out["probes"]["paper_company_affiliations"] = pa["instances"]
    out["probes"]["bad_json"] = pa["bad_json"]
    out["probes"]["distinct_authors_in_company_papers"] = (
        len(set().union(*scholar_sets.values())) if scholar_sets else 0)

    # ---------- 两两 Jaccard ----------
    pairs = []
    for a, b in combinations(companies, 2):
        j_ipc = C.jac(ipcs[a], ipcs[b])
        j_kw = C.jac(kw_sets.get(a, set()), kw_sets.get(b, set()))
        j_sc = C.jac(scholar_sets.get(a), scholar_sets.get(b)) if (
            a in scholar_sets and b in scholar_sets) else None
        dims = [x for x in (j_ipc, j_kw, j_sc) if x is not None]
        if not dims:
            continue
        ov = sum(dims) / len(dims)
        dims2 = [x for x in (j_ipc, j_kw) if x is not None]
        ov2 = sum(dims2) / len(dims2) if dims2 else None
        pairs.append({"a": a, "b": b,
                      "j_ipc": None if j_ipc is None else round(j_ipc, 4),
                      "j_keyword": None if j_kw is None else round(j_kw, 4),
                      "j_scholar": None if j_sc is None else round(j_sc, 4),
                      "n_dims": len(dims), "overlap": round(ov, 4), "grade": grade(ov),
                      "overlap_2d": None if ov2 is None else round(ov2, 4),
                      "grade_2d": None if ov2 is None else grade(ov2),
                      "patents_a": {"patents": nm["u1"]["patents"][a]},
                      "patents_b": {"patents": nm["u1"]["patents"][b]}})
    pairs.sort(key=lambda x: -x["overlap"])
    out["compute"]["n_pairs"] = len(pairs)
    out["compute"]["pairs_with_3_dims"] = sum(1 for p in pairs if p["n_dims"] == 3)
    out["compute"]["pairs_with_2_dims"] = sum(1 for p in pairs if p["n_dims"] == 2)
    out["compute"]["grade_dist"] = dict(Counter(p["grade"] for p in pairs))
    out["compute"]["grade_dist_2d"] = dict(Counter(p["grade_2d"] for p in pairs))
    out["compute"]["stats_overlap_2d"] = C.stats([p["overlap_2d"] for p in pairs
                                                 if p["overlap_2d"] is not None])
    for dim in ["overlap", "j_ipc", "j_keyword", "j_scholar"]:
        vals = [p[dim] for p in pairs if p[dim] is not None]
        out["compute"]["stats_" + dim] = C.stats(vals)
    out["compute"]["top15_pairs"] = pairs[:15]
    out["compute"]["median_pairs"] = pairs[len(pairs) // 2:len(pairs) // 2 + 5]

    ok = (len(pairs) >= 100 and out["compute"]["stats_j_ipc"]["max"] > 0
          and out["compute"]["stats_j_keyword"]["max"] > 0)
    full = ok and out["probes"]["companies_with_scholar_set"] >= 0.8 * len(companies)
    out["support_judgment"] = "完全转换支持" if full else ("部分支持" if ok else "完全不支持")
    out["support_reason"] = (
        f"IPC 重叠与关键词重叠两维在 {len(companies)} 家深圳专利头部机构上全覆盖并算出 "
        f"{len(pairs)} 对企业对；"
        f"学者重叠维仅 {out['probes']['companies_with_scholar_set']}/{len(companies)} 家机构能取到"
        f"「企业署名论文作者」集合（企业署名论文共 {out['probes']['paper_company_affiliations']:,} 个机构名），"
        "第三维覆盖不足，故判部分支持。")
    su = fill["scholar_universe"]
    out["disclosures"] = [
        "学者重叠维的代理口径：以 dwd_zh_paper.author_info_list 中 institution 含企业名的记录取作者姓名集合；"
        "无论文署名的机构（本批 %d/%d 家）该维记缺失、不记 0，避免把「无学术产出」误判为「领域不重叠」。"
        % (len(companies) - out["probes"]["companies_with_scholar_set"], len(companies)),
        "作者姓名为原文直取、未做消歧（同名不同人风险），Jaccard 可能高估学者重叠。",
        "关键词集合取每家机构专利关键词频次 Top%d；专利量超 %d 件的机构按 %d 件截断取样。"
        % (KW_TOP, kww["sample_per_firm"], kww["sample_per_firm"]),
        "dwd_zh_paper_classification 与论文主表 JOIN 命中率极低（旧批实测 799 篇 / 0.79%），"
        "因此未把「论文关键词」并入关键词维，仅用专利关键词。",
        "机构入集限定为 dwd_org_base_info 中 city=深圳 且专利≥30 件，故结论只覆盖深圳专利头部机构，"
        "不代表全库企业。",
        "学者宇宙双基线：dwd_scholar %d 位 vs dwd_scholar_talent_flag %d 位，交集仅 %d 位（%.2f%%）；"
        "本指标的学者维是「论文署名作者」代理，既不是 dwd_scholar 也不是人才标签宇宙，"
        "引用其覆盖率时必须写明分母是本批 %d 家入集机构"
        % (su["dwd_scholar"], su["dwd_scholar_talent_flag"], su["intersect"],
           su["intersect_pct"] * 100, len(companies)),
        "全部取值来自三方库 gkx 真实表（dwd_patent / dwd_org_base_info / dwd_zh_paper），"
        "未引用任何 mock_* / demo_* 面",
    ]
    out["elapsed_s"] = round(time.time() - t0, 1)
    dest = C.write_out(MID, out)
    print(json.dumps(out["probes"], ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in out["compute"].items() if k.startswith("stats_")},
                     ensure_ascii=False, indent=1))
    print(json.dumps(out["compute"]["grade_dist"], ensure_ascii=False))
    for p in pairs[:8]:
        print(p["a"], "|", p["b"], p["j_ipc"], p["j_keyword"], p["j_scholar"],
              p["overlap"], p["grade"])
    print("support", out["support_judgment"], out["elapsed_s"])


if __name__ == "__main__":
    main()
