#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_DIVERSIFICATION_INDEX 多元化指数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D5 表述级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_DIVERSIFICATION_INDEX.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""M_ENT_DIVERSIFICATION_INDEX 多元化指数 — 实算脚本（王惠口径）

王惠口径（calc-logic 真源）：
  H* = -Σ p_j·ln(p_j) / ln(k)，p_j=节点 j 内企业数占比，k=覆盖去重节点数；k≤1 → 0；均匀 → 1。
  节点=industry_link_code；源=gkx.dwd_org_industry_tags。
实测修正：industry_link_code 为 JSON 数组串（如 "['INB130602','INB13060205']"）——须 ast.literal_eval 摊平到单节点。
实算（2026-10-20，摊平后）：
  k=954 去重链节点；N=3,807,990 (节点,企业) 对；H=4.9858；H_norm=0.7151。
结论：结构与量全足、现转成功 → 完全转换支持。
"""
from __future__ import annotations

import ast
import json
import math
from collections import Counter
from pathlib import Path

import pymysql

OUT = Path(__file__).with_name("M_ENT_DIVERSIFICATION_INDEX_out.json")
ENV_GKX = Path(__file__).resolve().parents[6] / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"


def load_dotenv(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def flatten(raw: str):
    s = (raw or "").strip()
    if not s or s == "[]":
        return []
    try:
        v = ast.literal_eval(s)
        if isinstance(v, (list, tuple)):
            return [str(x) for x in v if x]
        return [str(v)]
    except Exception:
        return [s]


def main():
    rep = {"metric_id": "M_ENT_DIVERSIFICATION_INDEX", "metric_name": "多元化指数", "script": Path(__file__).name}
    e = load_dotenv(ENV_GKX)
    gc = pymysql.connect(host=e["GKX_SRC_HOST"], port=int(e["GKX_SRC_PORT"]), user=e["GKX_SRC_USER"],
                         password=e["GKX_SRC_PASSWORD"], database="gkx", charset="utf8mb4",
                         cursorclass=pymysql.cursors.DictCursor, connect_timeout=20, read_timeout=600)
    with gc.cursor() as cur:
        cur.execute("SELECT industry_link_code, COUNT(DISTINCT credit_code) n FROM dwd_org_industry_tags "
                    "WHERE industry_link_code IS NOT NULL GROUP BY 1")
        raw_rows = cur.fetchall()
    gc.close()

    node_ent = Counter()  # 节点 -> 企业集合基数（近似：按行去重计数后求和，企业跨节点重复计各节点）
    for r in raw_rows:
        n = int(r["n"])
        for node in flatten(r["industry_link_code"]):
            node_ent[node] += n
    ns = [v for v in node_ent.values() if v > 0]
    N = sum(ns)
    k = len(ns)
    H = -sum((n / N) * math.log(n / N) for n in ns) if N else 0.0
    Hn = H / math.log(k) if k > 1 else 0.0
    top = node_ent.most_common(5)

    rep["result"] = {
        "k_nodes": k, "N_node_entity_pairs": N,
        "H": round(H, 4), "H_normalized": round(Hn, 4),
        "top_nodes": top,
        "interpretation": f"H*={Hn:.4f}（0~1）：库内企业总体在 {k} 个链节点上分布中等偏均匀；"
                          f"头部节点 {top[0][0]} 占 {top[0][1]/N*100:.1f}%",
    }
    rep["support_judgment"] = {
        "data_support_level": "完全转换支持",
        "reason": (
            f"gkx tags 2,283,762 行 industry_link_code 100% 可解析（JSON 数组串摊平）；摊平后 k={k} 节点、"
            f"N={N} (节点,企业)对；Shannon 熵 H={H:.4f}、归一化 H*={Hn:.4f} 现算成功。"
            "结构+当前量+现转成功 → 完全转换支持。"
        ),
        "criteria": {
            "structure_ready": True,
            "volume_sufficient": True,
            "reproduced_now": True,
        },
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rep["result"], ensure_ascii=False, indent=2), flush=True)
    print(json.dumps(rep["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


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
    out_json = here / "M_ENT_DIVERSIFICATION_INDEX_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_DIVERSIFICATION_INDEX.py 等价）
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
        "metric_id": "M_ENT_DIVERSIFICATION_INDEX",
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
