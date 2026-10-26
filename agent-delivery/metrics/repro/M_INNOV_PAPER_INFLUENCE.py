#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文影响力（M_INNOV_PAPER_INFLUENCE）——A-22 批复现脚本。

口径来源：
  - seed `cfg_metric-INNOV-seed.yaml`：definition =「论文被引次数 / 影响因子」，
    formula = `pending_cosign: human:唐绍祖（未签）`，source_tables = `pending_ods`（未登记实体表）。
    即**没有已签口径**，本报告给的是推测定义（见 MD §1.6），不冒充王惠定版。

本报告落地的两维（缺测维重归一）：
  D1 被引次数   dwd_zh_paper_citation.citation_num（第三方被引记录，2 万篇样本）
  D2 期刊影响因子 dwd_zh_journal.impact_score（**整列为空**，0/2,796）

取数：本脚本**零 SQL**，只读 2026-10-22 的快照（code/_probe_infl_data.py 与
code/_probe_infl_data2.py 一次性拉取，单表均 ≤10 万行、限时 60 秒）：
  zh_paper.json / zh_paper_citation.json / zh_paper_doi.json /
  zh_paper_ref.json / en_paper.json / en_paper_cited_by.json
另有两条整列体检结论直接引用同批探针（download_num 全 0、impact_score 全空），
与 _snapshots21/city_family_probe_20261021.json 的 paper_download / journal_impact 两条一致。

产物：code/M_INNOV_PAPER_INFLUENCE_out.json
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from _innov_gkx21_common import dist, norm01, pct, write_out

METRIC = "M_INNOV_PAPER_INFLUENCE"
SNAP = HERE / "_snapshots21"
PROBE = SNAP / "probe_infl_20261022"


def load(name):
    d = json.loads((PROBE / f"{name}.json").read_text(encoding="utf-8"))
    return d["rows"], {c: i for i, c in enumerate(d["columns"])}, d


def main():
    papers, px, pmeta = load("zh_paper")
    cites, cx, cmeta = load("zh_paper_citation")
    dois, dx, _ = load("zh_paper_doi")
    refs, rx, _ = load("zh_paper_ref")
    enp, ex, _ = load("en_paper")
    encb, bx, _ = load("en_paper_cited_by")

    pid2year = {r[px["id"]]: str(r[px["cover_year_start"]] or "")[:4] for r in papers}
    pid2jrn = {r[px["id"]]: (r[px["publication_zh_name"]] or "") for r in papers}
    doi2id = {}
    for r in dois:
        d = (r[dx["doi"]] or "").strip().lower()
        if d:
            doi2id[d] = r[dx["id"]]

    # ---------------- 1. 论文语料 ----------------
    year_cnt = {}
    for r in papers:
        y = str(r[px["cover_year_start"]] or "")[:4]
        if y.isdigit():
            year_cnt[y] = year_cnt.get(y, 0) + 1
    year_cnt = dict(sorted(year_cnt.items()))
    corpus = {
        "rows": pmeta["n"],
        "distinct_id": len(pid2year),
        "doi_nonnull": sum(1 for r in dois if (r[dx["doi"]] or "").strip()),
        "doi_distinct": len(doi2id),
        "year_min": min(year_cnt), "year_max": max(year_cnt),
        "year_series": year_cnt,
        "batch_break_note": ("2024 年入库 32,379 篇，是 2023 年（6,651）的 4.87 倍，"
                             "为采集批次断点而非真实产出跃升；2025/2026 为残年"),
    }

    # ---------------- 2. 被引副表 ----------------
    cnum = [int(r[cx["citation_num"]] or 0) for r in cites]
    cids = [r[cx["id"]] for r in cites]
    idlen = [r[cx["id_list_len"]] or 0 for r in cites]
    matched = [i for i in cids if i in pid2year]
    citation_dim = {
        "rows": cmeta["n"],
        "distinct_id": len(set(cids)),
        "citation_num": {"nonnull": len(cnum), "gt0": sum(1 for c in cnum if c > 0),
                         "sum": sum(cnum), "mean": round(statistics.mean(cnum), 3),
                         "median": statistics.median(cnum), "max": max(cnum),
                         "p90": pct(cnum, 0.90), "p99": pct(cnum, 0.99),
                         "n_distinct": len(set(cnum))},
        "citation_id_list_len": {"nonnull": sum(1 for x in idlen if x), "max": max(idlen),
                                 "mean": round(statistics.mean(idlen), 2)},
        "linked_to_corpus": len(set(matched)),
        "linked_rate_of_citation_rows": round(len(set(matched)) / len(set(cids)), 4),
        "corpus_coverage": round(len(set(matched)) / len(pid2year), 6),
    }

    # 分年被引覆盖
    by_year_total, by_year_linked = {}, {}
    mset = set(matched)
    for r in papers:
        y = str(r[px["cover_year_start"]] or "")[:4]
        if not y.isdigit():
            continue
        by_year_total[y] = by_year_total.get(y, 0) + 1
        if r[px["id"]] in mset:
            by_year_linked[y] = by_year_linked.get(y, 0) + 1
    year_cov = {y: {"papers": by_year_total[y], "with_citation": by_year_linked.get(y, 0),
                    "rate": round(by_year_linked.get(y, 0) / by_year_total[y], 5)}
                for y in sorted(by_year_total) if y >= "2010"}

    # ---------------- 3. 库内引文网络（用参考文献反查入度） ----------------
    ref_rows = len(refs)
    ref_with_doi = sum(1 for r in refs if (r[rx["ref_doi"]] or "").strip())
    ref_papers = len({r[rx["paper_id"]] for r in refs})
    indeg = {}
    self_cite = 0
    for r in refs:
        d = (r[rx["ref_doi"]] or "").strip().lower()
        if not d:
            continue
        tid = doi2id.get(d)
        if not tid:
            continue
        if tid == r[rx["paper_id"]]:
            self_cite += 1
        else:
            indeg[tid] = indeg.get(tid, 0) + 1
    network = {
        "reference_rows": ref_rows,
        "reference_with_doi": ref_with_doi,
        "reference_doi_rate": round(ref_with_doi / ref_rows, 4),
        "papers_with_any_reference": ref_papers,
        "papers_with_reference_rate": round(ref_papers / pmeta["n"], 4),
        "edges_to_corpus": sum(indeg.values()),
        "papers_cited_by_corpus": len(indeg),
        "self_citations": self_cite,
        "max_in_degree": max(indeg.values()) if indeg else 0,
        "in_degree_dist": {str(k): v for k, v in
                           sorted({n: list(indeg.values()).count(n) for n in set(indeg.values())}.items())},
        "conclusion": ("库内 196,619 条参考文献只有 102,811 条带 DOI，其中命中库内论文 DOI 的仅 "
                       "166 条（165 篇被引、最大入度 2）。库内自算引文网络实质上不存在，"
                       "不能拿「参考文献数」当被引次数。"),
    }

    # ---------------- 4. 整列体检（同批探针，直接引用） ----------------
    probe = json.loads((SNAP / "city_family_probe_20261021.json").read_text(encoding="utf-8"))["probes"]
    download = probe["paper_download"]["rows"][0]
    journal = probe["journal_impact"]["rows"][0]
    dead_cols = {
        "download_num": {"rows": int(download[0]), "gt0": int(download[1]), "sum": int(download[2]),
                         "source": "city_family_probe_20261021.json → paper_download"},
        "journal_impact_score": {"rows": int(journal[0]), "nonnull": int(journal[1]),
                                 "source": "city_family_probe_20261021.json → journal_impact"},
    }

    # ---------------- 5. 打分 ----------------
    # 王惠式（推测）：S=100*(0.70*norm(被引)+0.30*norm(影响因子))；影响因子整列空 →
    # 缺测维重归一 → S=100*norm(被引次数)。仅在可挂接的 782 篇上可解释。
    linked_pairs = [(i, int(r[cx["citation_num"]] or 0)) for i, r in zip(cids, cites) if i in pid2year]
    vals = [v for _, v in linked_pairs]
    n_linked = norm01(vals) if vals else []
    score_linked = [100 * x for x in n_linked]
    top_linked = sorted(
        [{"id": i, "year": pid2year[i], "journal": pid2jrn.get(i, ""),
          "citation_num": v, "score": round(100 * s, 2)}
         for (i, v), s in zip(linked_pairs, n_linked)],
        key=lambda x: (-x["citation_num"], x["id"]))[:10]

    # 未挂接的 2 万件只能给出「样本分布」，没有题录、无法解释
    score_sample = [100 * x for x in norm01(cnum)]

    # ---------------- 6. 英文论文（旁证） ----------------
    en_ids = {r[ex["id"]] for r in enp}
    encb_ids = [r[bx["id"]] for r in encb]
    en = {
        "en_paper_rows": len(enp),
        "en_cited_by_rows": len(encb),
        "en_cited_by_distinct": len(set(encb_ids)),
        "overlap": len(set(encb_ids) & en_ids),
        "overlap_rate_of_cited_by": round(len(set(encb_ids) & en_ids) / len(set(encb_ids)), 6),
        "citation_count_dist": {str(k): v for k, v in
                                sorted({c: [r[bx["citation_count"]] for r in encb].count(c)
                                        for c in {r[bx["citation_count"]] for r in encb}}.items())[:8]},
        "note": "英文被引表 77,144 条与英文论文主表 1,387 条仅 5 条交集，同样是断开的外部样本",
    }

    payload = {
        "metric_id": METRIC,
        "metric_name": "论文影响力",
        "support_judgment": "部分支持",
        "run_at": "2026-10-22",
        "db": "gkx@183.240.141.251:3318（只读快照，脚本零 SQL）",
        "corpus": corpus,
        "citation_dim": citation_dim,
        "year_coverage": year_cov,
        "in_corpus_network": network,
        "dead_columns": dead_cols,
        "en_side": en,
        "score": {
            "formula_inferred": ("S=100*(0.70*norm(被引次数)+0.30*norm(期刊影响因子))，"
                                 "缺测维重归一（影响因子整列为空 → 实跑 S=100*norm(被引次数)）"),
            "formula_status": "推测定义：seed formula 为 pending_cosign（唐绍祖未签），非王惠定版",
            "linked_782": {"stats": dist(score_linked), "top10": top_linked},
            "sample_20031_unlabeled": {"stats": dist(score_sample)},
            "n_linked": len(score_linked),
        },
        "coverage_chain": {
            "citation_rows_vs_corpus": round(cmeta["n"] / pmeta["n"], 4),
            "linked_vs_corpus": round(len(mset) / pmeta["n"], 6),
            "note": "被引副表 2 万条 → 能挂到论文主表的 782 篇 → 占 100,900 篇语料 0.775%。",
        },
        "base_years_used": [y for y in year_cnt if "2015" <= y <= "2023" and year_cnt[y] >= 1000],
        "base_years_missing": ["2024", "2025", "2026"],
        "base_years_note": ("论文年度序列 1980—2026 真实存在，但 2024 是采集批次断点（32,379 篇，"
                            "为 2023 年的 4.87 倍）、2025/2026 为残年；任何「前 N 年基线/CAGR」"
                            "只能用 2015—2023 这段，2024 起三年不得按真实增长处理，更不得按 0 摊入分母。"),
        "gaps": [
            "被引副表 20,031 条中只有 782 篇能与论文主表 id 对上（3.90%），主库 100,900 篇论文"
            "有被引记录的比例仅 0.775%。",
            "dwd_zh_paper.download_num 整列为 0（100,900 行，SUM=0），不能当下载量；"
            "dwd_zh_journal.impact_score 整列为空（0/2,796），影响因子维缺测。",
            "库内参考文献表只能构造出 166 条入边，覆盖 165 篇论文（0.16%），无法自算被引网络。",
            "dwd_scholar_papers 738,106 行无被引列；dwd_scholar_paper_relation 1,065,385 行只是"
            "学者-论文关系，同样无被引数。",
            "英文侧 dwd_en_paper_cited_by_info 77,144 条与 dwd_en_paper 1,387 条仅 5 条交集。",
        ],
    }
    p = write_out(METRIC, payload)
    print(json.dumps({"wrote": str(p), "citation": payload["citation_dim"],
                      "coverage": payload["coverage_chain"],
                      "network_edges": network["edges_to_corpus"],
                      "score_linked": payload["score"]["linked_782"]["stats"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
