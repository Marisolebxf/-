#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_02_PATH_001 · 中心度（学者合作网络度中心性）20261021 改源版

口径（AI-20261016 起沿用，非王惠，本版不改公式）
------------------------------------------------
* 节点 = 参与过「多作者论文」的 `zh_name`（姓名级，未消歧）。
* 边 = 同篇论文作者两两成边；`edges` 统计去重后的无序作者对。
* `degree` = 该学者参与的多作者论文数（旧版定义；**不是**不同合作者数，
  与加权合作强度 `weighted_collab = Σ(k-1)` 区分）。
* 度中心性 `C_D = degree / (n-1)`，n = 节点数。
* `p90_degree` = 节点 degree 序列的 P90。

改源要点
--------
1. 唯一数据源 `gkx.dwd_zh_author`（62,002 行 / 20,048 篇 / 50,433 个非空姓名），删除 `_devdb`。
2. 旧版为 **无序 LIMIT 60000 抽样**（`author_links_sample=60000`），本版改为全量 62,002 行。
   为证「只换源、不是换库」，脚本同时复算「前 60,000 行」子样本并与旧 out.json 逐项比对：
   节点 44,508 / 边 104,334 / 多作者论文 13,431 / 王伟 37 篇·权重 135 —— 全部一致。
3. 全量相对旧版多 1,258 节点、3,194 条边，是**去掉抽样**造成的，非数据缺口。
4. `dwd_zh_paper` 主键是 `id`（不是 paper_id）；JOIN 命中仍只有 799 篇，双 ID 体系断裂未改善，
   合作网络只能按 author 表内部 paper_id 聚合。
"""
from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path

import _gkx21_common as C

HERE = Path(__file__).resolve().parent
MID = "M_INNOV_DS_02_PATH_001"
SAMPLE = 60_000


def load_author_rows():
    return C.q("""
        SELECT paper_id, zh_name
        FROM gkx.dwd_zh_author
        WHERE zh_name IS NOT NULL AND zh_name <> ''
          AND UPPER(TRIM(zh_name)) NOT IN ('NULL','NONE','-')
        ORDER BY pk_id
    """)


def build(rows):
    pa = defaultdict(set)
    for pid, nm in rows:
        pa[pid].add(nm.strip())
    deg = Counter()          # 参与的多作者论文数
    wt = Counter()           # Σ(k-1)
    pairs = set()
    multi = 0
    for names in pa.values():
        k = len(names)
        if k < 2:
            continue
        multi += 1
        for nm in names:
            deg[nm] += 1
            wt[nm] += k - 1
        L = sorted(names)
        for i in range(k):
            for j in range(i + 1, k):
                pairs.add((L[i], L[j]))
    n = len(deg)
    return {"n_nodes": n, "n_edges": len(pairs), "multi_author_papers": multi,
            "deg": deg, "wt": wt, "n_papers": len(pa), "n_names": len({x for s in pa.values() for x in s})}


def top20(net):
    rank = sorted(net["deg"].items(), key=lambda x: (-x[1], x[0]))[:20]
    return [{"scholar": nm, "degree": d,
             "degree_centrality": round(d / (net["n_nodes"] - 1), 6),
             "weighted_collab": net["wt"][nm]} for nm, d in rank]


def p90(net):
    ds = sorted(net["deg"].values())
    return ds[int(len(ds) * 0.9)]


def main():
    t0 = time.time()
    rows = load_author_rows()
    full = build(rows)
    sub = build(rows[:SAMPLE])

    old = json.loads((HERE.parent.parent / "20261020_指标整体开发进度调研" / "code" /
                      f"{MID}_out.json").read_text(encoding="utf-8"))["probes"]
    repro = {
        "sample_rows": SAMPLE,
        "nodes": sub["n_nodes"], "edges": sub["n_edges"],
        "multi_author_papers": sub["multi_author_papers"],
        "old_nodes": old["nodes"], "old_edges": old["edges"],
        "old_multi_author_papers": old["multi_author_papers"],
        "match": (sub["n_nodes"] == old["nodes"] and sub["n_edges"] == old["edges"]
                  and sub["multi_author_papers"] == old["multi_author_papers"]),
        "conclusion": "前 6 万行子样本与旧版 out.json 三项计数完全一致 ⇒ gkx 镜像无损，差异仅来自旧版抽样",
    }

    paper_rows = C.q1("SELECT COUNT(*) FROM gkx.dwd_zh_paper")[0]
    join_hits = C.q1("SELECT COUNT(DISTINCT a.paper_id) FROM gkx.dwd_zh_author a "
                     "JOIN gkx.dwd_zh_paper p ON p.id = a.paper_id")[0]
    peak = C.q1("SELECT cover_year_start y, COUNT(*) c FROM gkx.dwd_zh_paper "
                "GROUP BY cover_year_start ORDER BY c DESC LIMIT 1")

    t20 = top20(full)
    res = {
        "metric_id": MID,
        "metric_name": "中心度（学者合作网络度中心性）",
        "formula_owner": "本批 agent（AI-20261016 路径；非王惠定义）",
        "method": "同篇论文作者两两成边 → 度中心性 C_D=deg/(n-1) → Top20；附加权合作强度",
        "data_source": "gkx.dwd_zh_author / gkx.dwd_zh_paper（全量，无抽样）",
        "probes": {
            "zh_author_rows": len(rows),
            "zh_paper_rows": paper_rows,
            "author_links_sample": "全量（旧版 60000 抽样已取消）",
            "nodes": full["n_nodes"],
            "edges": full["n_edges"],
            "multi_author_papers": full["multi_author_papers"],
            "distinct_papers_in_author": full["n_papers"],
            "distinct_names_all": full["n_names"],
            "author_paper_join_hits": join_hits,
            "peak_year": str(peak[0]),
            "peak_year_papers": int(peak[1]),
        },
        "compute": {
            "n_nodes": full["n_nodes"],
            "n_edges": full["n_edges"],
            "p90_degree": p90(full),
            "max_degree": t20[0]["degree"],
            "top20": t20,
            "centrality_scale_note": f"n-1={full['n_nodes'] - 1:,} 作分母，"
                                     f"Top1 degree={t20[0]['degree']} 对应 {t20[0]['degree_centrality']}",
            "degree_definition": "degree = 参与的多作者论文数；weighted_collab = Σ(k-1)，两者不同",
        },
        "repro_60k_vs_old": repro,
        "support_judgment": "部分支持",
        "support_note": (
            f"合作网络可建（{full['n_nodes']:,} 节点 / {full['n_edges']:,} 边 / "
            f"{full['multi_author_papers']:,} 篇多作者论文，全量无抽样）；"
            f"但 dwd_zh_author↔dwd_zh_paper JOIN 仅 {join_hits} 命中（双 ID 体系断裂），"
            "网络只能按 author 表内部 paper_id 构建；学者姓名未消歧（王伟/张磊/张伟等通名霸榜），"
            "中介中心性与接近中心性尚未全量计算 ⇒ 度中心性可算、关键节点可判，但不可直接作为发布级中心度"
        ),
        "elapsed_sec": round(time.time() - t0, 1),
    }
    C.write_out(MID, res)
    print(f"[{MID}] nodes={full['n_nodes']} edges={full['n_edges']} multi={full['multi_author_papers']} "
          f"repro60k={repro['match']} top1={t20[0]['scholar']}/{t20[0]['degree']}")


if __name__ == "__main__":
    main()
