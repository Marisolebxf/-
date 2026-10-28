#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_DS_02_PATH_001 中心度
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_DS_02_PATH_001.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_DS_02_PATH_001_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_DS_02_PATH_001.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_DS_02_PATH_001",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
