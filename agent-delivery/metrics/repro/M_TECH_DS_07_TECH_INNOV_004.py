#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_TECH_DS_07_TECH_INNOV_004 技术创新力综合评估
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_TECH_DS_07_TECH_INNOV_004.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_TECH_DS_07_TECH_INNOV_004 · 技术基础指标模型——领先专利主体机构（王惠口径：技术创新力综合评估）

口径：王惠 M_INNOV_TINN_COMPOSITE（三维等权内子项极值归一；对象 IPC4；0-100）
数据源优先级：gkx 真源（PK 分片抽样）→ 本地快照（tech_d_join / tech_d_metrics / graph2）
输出：code/M_TECH_DS_07_TECH_INNOV_004_out.json

运行：python3 code/M_TECH_DS_07_TECH_INNOV_004.py
"""
import json, os, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots"
OUT = HERE / "M_TECH_DS_07_TECH_INNOV_004_out.json"
SLICES = 10
SLICE_ROWS = 20000


def load_env():
    p = None
    for base in HERE.parents:
        cand = base / "gkx-orchestration/agent-delivery/data/third-party-source/gkx-mysql-raw/.env.local"
        if cand.exists():
            p = cand
            break
    env = {}
    if p is not None:
        for line in p.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def load_patents(live=None):
    """默认读本地快照（既有 out.json 优先复用、禁重跑探针）；--live 时才走 DB PK 分片。"""
    if live is None:
        live = "--live" in sys.argv
    if not live:
        path = SNAP / "tech_d_patent_sample.jsonl"
        return [json.loads(x) for x in path.open(encoding="utf-8")], "snapshot_jsonl"
    env = load_env()
    try:
        import pymysql
        conn = pymysql.connect(host=env.get("GKX_SRC_HOST"), port=int(env.get("GKX_SRC_PORT", 3318)),
                               user=env.get("GKX_SRC_USER"), password=env.get("GKX_SRC_PASSWORD"),
                               database=env.get("GKX_SRC_DB", "gkx"), connect_timeout=8,
                               read_timeout=600, charset="utf8mb4")
        cur = conn.cursor()
        cur.execute("SELECT MIN(dwd_id), MAX(dwd_id) FROM dwd_patent")
        lo, hi = cur.fetchone()
        step = max(1, (int(hi) - int(lo)) // SLICES)
        rows = []
        for i in range(SLICES):
            a = int(lo) + i * step
            cur.execute("""SELECT dwd_id, apdt_year, main_classification_ipcr, further_classification_ipcr,
                                  first_applicant_name, granted_number
                           FROM dwd_patent WHERE dwd_id >= %s AND dwd_id < %s LIMIT %s""",
                        (a, a + step, SLICE_ROWS))
            rows += cur.fetchall()
        conn.close()
        return [dict(zip(("dwd_id", "apdt_year", "main_classification_ipcr",
                          "further_classification_ipcr", "first_applicant_name", "granted_number"), r))
                for r in rows], "gkx_live_slices"
    except Exception as exc:                                    # noqa: BLE001
        print(f"[warn] gkx 不可达（{type(exc).__name__}），回落本地快照：{exc}", file=sys.stderr)
        path = SNAP / "tech_d_patent_sample.jsonl"
        return [json.loads(x) for x in path.open(encoding="utf-8")], "snapshot_jsonl"


def ipc4s(main, further):
    codes = []
    for s in [main] + (json.loads(further) if further and str(further) not in ("[]", "null", "NULL", "") else []):
        s = str(s or "").strip()
        if len(s) >= 4:
            codes.append(s[:4].upper())
    return list(dict.fromkeys(codes))


def main():
    patents, src = load_patents()
    ipc_stat = defaultdict(lambda: {"n": 0, "grant": 0, "width": 0})
    n_with_ipc = 0
    ent_stat = defaultdict(lambda: {"n": 0, "grant": 0, "width": 0, "ipc": Counter()})
    year_stat = Counter()
    for r in patents:
        codes = ipc4s(r.get("main_classification_ipcr"), r.get("further_classification_ipcr"))
        if not codes:
            continue
        n_with_ipc += 1
        g = r.get("granted_number") not in (None, "", "NULL")
        nm = (r.get("first_applicant_name") or "").strip()
        try:
            year_stat[int(r.get("apdt_year"))] += 1
        except Exception:
            pass
        for c in codes:
            s = ipc_stat[c]
            s["n"] += 1; s["grant"] += int(g); s["width"] += len(codes)
        if nm and nm not in ("NULL", "null", "无"):
            e = ent_stat[nm]
            e["n"] += 1; e["grant"] += int(g); e["width"] += len(codes)
            for c in codes[:6]:
                e["ipc"][c] += 1

    join = json.loads((SNAP / "tech_d_join_20261021.json").read_text())
    graph = json.loads((SNAP / "tech_d_graph2_20261021.json").read_text())

    # D1 规模维：申请量/授权量/授权率（域级，样本口径）
    dom = []
    for c, s in sorted(ipc_stat.items(), key=lambda kv: -kv[1]["n"])[:30]:
        dom.append({"ipc4": c, "n_app": s["n"], "n_grant": s["grant"],
                    "grant_rate": round(s["grant"] / s["n"], 4),
                    "width_mean": round(s["width"] / s["n"], 3),
                    "influence_0_100": next((x["influence_0_100"] for x in graph["ipc_influence_top"]
                                             if x["ipc4"] == c), None)})

    # D2 质量维：全局样本（域级 pn 交集近零，不逐域合成）
    quality = {"family_mean_members": join["global"]["family_mean_members"],
               "family_max_members": join["global"]["family_max"],
               "cited_avg": join["global"]["cited_avg"],
               "cited_pos_share": join["global"]["cited_pos_share"],
               "legal_stable_share": join["global"]["legal_stable"],
               "claims_direct": None,
               "domain_level_join": {"pn2ipc": join["join_coverage"]["pn2ipc"],
                                     "legal_joined_ipc": join["join_coverage"]["legal_joined_ipc"]}}

    # D3 市场潜力维：转让（可算）+ 许可/诉讼/质押/开放许可（2,000 抽样近零）
    market = {"transfer_rows": join["join_coverage"]["transfer_rows"],
              "transfer_by_year": graph.get("year_totals"),
              "legal_event_counts_2000": join["global"]["market_event_counts_2000"],
              "distinct_legal_events": join["global"]["distinct_legal_events"]}

    # D4 主体机构维（需求 (8) 阈值法）：量×质双阈值
    ents = []
    for e, s in ent_stat.items():
        if s["n"] < 60:
            continue
        ents.append({"entity": e, "n_app": s["n"], "grant_rate": round(s["grant"] / s["n"], 4),
                     "width_mean": round(s["width"] / s["n"], 3),
                     "top_ipc": s["ipc"].most_common(3)})
    ents.sort(key=lambda x: -x["n_app"])

    thresholds = []
    for n_min in (100, 300, 500, 1000):
        for g_min in (0.30, 0.40, 0.50):
            sel = [x for x in ents if x["n_app"] >= n_min and x["grant_rate"] >= g_min]
            thresholds.append({"n_min": n_min, "grant_min": g_min, "n_leaders": len(sel),
                               "share_of_scored": round(len(sel) / max(1, len(ents)), 4),
                               "top3": [x["entity"] for x in sel[:3]]})

    # 域集中度（HHI，按主体份额）
    hhi = {}
    for tech in ("G06F", "G06N", "H01M"):
        total = sum(c.get(tech, 0) for c in (e["ipc"] and dict(e["ipc"]) for e in ents) if c) if False else None
        shares = []
        for e in ents:
            v = dict(e["top_ipc"]).get(tech, 0)
            shares.append(v)
        tot = sum(shares) or 1
        hhi[tech] = round(sum((v / tot) ** 2 for v in shares if v), 5)

    res = {
        "metric_id": "M_TECH_DS_07_TECH_INNOV_004",
        "metric_name": "技术基础指标模型——领先专利主体机构（王惠口径：技术创新力综合评估）",
        "formula_owner": "王惠",
        "source_used": src,
        "generated_at": "2026-10-21",
        "sample": {"n_patents": len(patents), "n_with_ipc": n_with_ipc,
                   "distinct_ipc4": len(ipc_stat), "n_entities": len(ent_stat),
                   "year_totals": dict(sorted(year_stat.items()))},
        "dim1_scale": dom[:20],
        "dim2_quality": quality,
        "dim3_market": market,
        "dim4_entities": {"n_scored": len(ents), "top": ents[:15], "thresholds": thresholds,
                          "hhi_by_domain_top16_entities": hhi},
        "coverage": {"D1_scale": "full_sampled", "D2_family": "0.70%",
                     "D2_claims": "缺列（claim 表仅 original_text）", "D2_cited": "0.70%",
                     "D2_legal": "0.68%", "D3_transfer": "full_table", "D3_license": "0.1%(2/2000)",
                     "D3_litigation": "0", "D3_pledge": "0.5%(10/2000)", "D3_open_license": "0.05%(1/2000)"},
        "subindicators": {"total": 11, "computable_full": ["专利申请量", "专利授权量", "技术宽度", "转让"],
                          "sample_only": ["家族规模", "被引次数", "法律状态稳定性"],
                          "missing": ["权利要求数", "许可", "诉讼", "质押", "开放许可"]},
        "composite": {"closed": False,
                      "reason": "王惠 11 子项中 4 项全量、3 项 0.7% 抽样、4 项近零/缺列；0-100 综合分缺少 7 子项，不输出闭合分"},
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {"scale_dim_full": True, "width_dim_full": True,
                         "quality_5_sub": {"family": 0.007, "claims": 0.0, "cited": 0.007, "legal": 0.0068,
                                           "width": 1.0},
                         "market_5_sub": {"transfer": 1.0, "license": 0.001, "litigation": 0.0,
                                          "pledge": 0.005, "open_license": 0.0005},
                         "entity_threshold_identified": True,
                         "composite_0_100": "不可闭合（7/11 子项缺）"},
            "note": "四子项全量可算（申请量/授权量/技术宽度/转让）+ 三子项抽样（家族/被引/法律）+ 四子项缺（权利要求/许可/诉讼/质押/开放许可）→ 部分支持"},
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: res[k] for k in ("source_used", "sample", "support_judgment")}, ensure_ascii=False, indent=1))
    print("dim1 top5:", [(x["ipc4"], x["n_app"], x["grant_rate"]) for x in dom[:5]])
    print("thresholds(500/0.4):", next(t for t in thresholds if t["n_min"] == 500 and t["grant_min"] == 0.4))
    print("written:", OUT.name)


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_TECH_DS_07_TECH_INNOV_004_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_TECH_DS_07_TECH_INNOV_004.py 等价）
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
        "metric_id": "M_TECH_DS_07_TECH_INNOV_004",
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
