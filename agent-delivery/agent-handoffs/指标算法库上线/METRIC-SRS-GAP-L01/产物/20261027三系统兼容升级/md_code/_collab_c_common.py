#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_collab_c_common.py —— SYNTH-c（区域创新协同族五件）共用复算模块。

纪律（20261021）：
- 不重跑数据库探针。全部输入取自上一批已落盘的实测缓存：
  * code/M_SYNTH_191_1_out.json                   (2026-10-21 王惠口径 191 实测，含 network_facts/raw_measures)
  * code/_synthb_cache.json                       (2026-10-21 demo ods 行数与城市主档)
  * code/M_SYNTH_COLLAB_RELATION_INPUT_out.json   (2026-10-20 三类边分城统计)
  * code/M_ORG_COLLAB_CHAIN_out.json              (2026-10-21 ORG 域合作链基线，作跨域对比)
- 仅做确定性再计算与序列化，不新增任何 DB 访问。
- 输出统一写入 code/{metric_id}_out.json，保留旧产物的既有字段（覆盖前先读）。
"""
import json
import math
import os

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_ORDER = ["深圳市", "北京市", "上海市", "广州市"]
CITY_SHORT = {"深圳市": "深圳", "北京市": "北京", "上海市": "上海", "广州市": "广州"}


def _load(name, default=None):
    path = os.path.join(CODE_DIR, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_inputs():
    """读取四份已落盘实测产物；缺失即抛错（禁止静默造数）。"""
    m191 = _load("M_SYNTH_191_1_out.json")
    if m191 and "network_facts" not in m191:
        # 20261024 修复：20261021 批 191 产物改版不含 network_facts，回落 20261020 批实测（同源 gkx，含三类边网络事实）
        m191_nf = _load("M_SYNTH_191_1_out.network_facts.json")
        if m191_nf and "network_facts" in m191_nf:
            m191 = m191_nf
    if not m191:
        raise RuntimeError("缺少 M_SYNTH_191_1_out.json（2026-10-21 实测网络事实）")
    cache = _load("_synthb_cache.json", {})
    rel = _load("M_SYNTH_COLLAB_RELATION_INPUT_out.json", {})
    org = _load("M_ORG_COLLAB_CHAIN_out.json", {})
    return m191, cache, rel, org


def build_network(m191):
    """把 191 的 network_facts 展开为统一城市级网络对象。"""
    nf = m191["network_facts"]
    net = {}
    for c in CITY_ORDER:
        org_n = int(nf["org_nodes"].get(c, 0))
        ri_n = int(nf["ri_nodes"].get(c, 0))
        sch_n = int(nf["scholar_org_nodes"].get(c, 0))
        e = nf["edges"][c]
        net[c] = {
            "org_nodes": org_n,
            "ri_nodes": ri_n,
            "scholar_org_nodes": sch_n,
            "n_nodes": org_n + ri_n + sch_n,
            "e_joint_patent": int(e["joint_patent_edges"]),
            "e_coop_project": int(e["coop_project_edges"]),
            "e_talent_flow": int(e["talent_flow_edges"]),
            "m_edges": int(e["edges_total"]),
            "covered_nodes_cached": int(nf["covered_nodes_approx"].get(c, 0)),
        }
    return net


def metrics_for(cell):
    """单城网络的三件套原始量。"""
    n, m = cell["n_nodes"], cell["m_edges"]
    cell["possible_edges"] = n * (n - 1) / 2 if n >= 2 else 0
    cell["density"] = (2.0 * m / (n * (n - 1))) if n >= 2 else None
    cell["deg_avg"] = (2.0 * m / n) if n else None
    # 归一化平均点度中心性 = 平均度/(n-1)，在无向简单图上恒等于密度
    cell["deg_centrality_norm"] = (
        (cell["deg_avg"] / (n - 1)) if n >= 2 else None
    )
    cov = cell["covered_nodes_cached"]
    cell["covered_upper_bound_2m"] = min(cov, 2 * m) if m else 0
    cell["covered_graph_consistent"] = bool(cov <= 2 * m) if m else True
    cell["completeness"] = (cov / n) if n else None
    cell["completeness_upper_bound"] = (cell["covered_upper_bound_2m"] / n) if n else None
    cell["covered_subgraph_avg_deg"] = (2.0 * m / cov) if cov else None
    return cell


def minmax_scores(values):
    """批内极值归一（min-max→0..100），与 191 的 dim_scores 口径一致。"""
    vals = [v for v in values.values() if v is not None]
    if not vals:
        return {k: None for k in values}
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {k: (100.0 if v is not None else None) for k, v in values.items()}
    return {
        k: (round((v - lo) / (hi - lo) * 100.0, 4) if v is not None else None)
        for k, v in values.items()
    }


def describe(values):
    """四城分布描述。"""
    vals = sorted(v for v in values.values() if v is not None)
    if not vals:
        return {}
    n = len(vals)
    mid = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2.0
    return {
        "n": n,
        "min": vals[0],
        "max": vals[-1],
        "mean": sum(vals) / n,
        "median": mid,
        "cv": (std(vals) / (sum(vals) / n)) if sum(vals) else None,
    }


def std(vals):
    mu = sum(vals) / len(vals)
    return math.sqrt(sum((x - mu) ** 2 for x in vals) / len(vals))


def pearson(xs, ys):
    """Pearson r；任一侧零方差返回 None。"""
    n = len(xs)
    if n != len(ys) or n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def baseline(org):
    """ORG 合作链基线（跨域对比，不作本指标分子）。"""
    comp = (org or {}).get("compute", {})
    inst = comp.get("inst_net", {})
    return {
        "metric": "M_ORG_COLLAB_CHAIN（ORG 域，论文合著+专利共申双源）",
        "merged_edges": comp.get("merged_edges"),
        "total_edge_weight": comp.get("total_edge_weight"),
        "inst_inst_edges": comp.get("inst_inst_edges"),
        "inst_nodes_V": inst.get("V"),
        "inst_edges_E": inst.get("E"),
        "inst_density": inst.get("density"),
        "weighted_degree_sum": inst.get("weighted_degree_sum"),
        "note": "边域与 SYNTH 协同网不同（论文合著边在本族不入网），仅作量级与密度基线对比",
    }


def provenance(m191):
    return {
        "probe_date": "2026-10-21",
        "db_probe": "skipped（按任务纪律：已有 out.json 先读复用，禁重跑探针）",
        "inputs": [
            "code/M_SYNTH_191_1_out.json（2026-10-21 王惠口径实测）",
            "code/_synthb_cache.json（demo ods 行数与城市主档）",
            "code/M_SYNTH_COLLAB_RELATION_INPUT_out.json（三类边分城统计）",
            "code/M_ORG_COLLAB_CHAIN_out.json（ORG 域基线）",
        ],
        "source_tables": {
            "dwd_patent_applicants": 28964,
            "dwd_patent": 2939895,
            "dwd_scholar_work_experience": 57117,
            "dwd_zh_project": 58453,
            "dwd_org_base_info": 189116,
            "dwd_research_institute_base_info": 2074,
            "dwd_scholar": 21316,
        },
        "known_gap": "dwd_zh_project.funded_institution 非空 0 行 → 合作项目边 0",
        "m191_support": m191.get("support_judgment"),
    }


def write_out(metric_id, payload):
    """读旧产物 → 合并（新值覆盖同名字段）→ 落盘，保留历史字段。"""
    path = os.path.join(CODE_DIR, metric_id + "_out.json")
    old = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            old = {}
    merged = dict(old)
    merged.update(payload)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    return path
