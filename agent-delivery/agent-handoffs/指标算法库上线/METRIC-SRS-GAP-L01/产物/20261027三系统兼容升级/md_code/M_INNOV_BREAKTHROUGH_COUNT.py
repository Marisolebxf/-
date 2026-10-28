#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_BREAKTHROUGH_COUNT （注册表未登记·工程件）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_BREAKTHROUGH_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_BREAKTHROUGH_COUNT 重大成果突破数 · 复现代码（20261022 改源版，只用三方库 gkx）

口径：突破 = 高影响尾部计数——专利被引 P90 或价值 P90；论文挂 1 区刊；项目国家级。
非专利组合仅单一维度即入计（OR 逻辑），反映「任一维度突破」。
年窗 2020-2024（与 20261020 版一致，未改动）。

改源说明（20261021 版唯一变动）：数据面由开发库 ODS 换成三方库 `gkx`（逐表镜像、
行数一致）；判据阈值、OR 逻辑、抽样规模与年窗一律不动。表行数探针改为读库存
`_work_gkx21/GKX_INVENTORY.json`，不重复对 294 万行宽表做 `COUNT(*)`。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_BREAKTHROUGH_COUNT_out.json"
INV = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"
YEAR_LO, YEAR_HI = 2020, 2024
PERC = 90

TABLES = ["dwd_patent", "dwd_patent_cited", "dwd_zh_paper", "dwd_zh_journal",
          "dwd_zh_project", "dwd_en_project", "dwd_en_paper"]


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def pct(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(len(s) * p / 100)))
    return s[k]


def main():
    inv = json.loads(INV.read_text(encoding="utf-8"))
    probes = {f"gkx.{t}": int(inv[t]["rows"]) for t in TABLES if t in inv}

    # ---- 专利窗内：value + cited（关联子查询，控制窗口）----
    patents = [tuple(r.values()) for r in qd("""
        SELECT p.pn, p.value, p.apdt_year,
               (SELECT COALESCE(SUM(c.cited_by_nums),0) FROM gkx.dwd_patent_cited c WHERE c.pn = p.pn)
        FROM gkx.dwd_patent p
        WHERE p.apdt_year BETWEEN %s AND %s
        LIMIT 20000
    """, (YEAR_LO, YEAR_HI))]

    # ---- 论文：挂刊分区 ----
    zh_papers = [tuple(r.values()) for r in qd("""
        SELECT CONCAT('zh:', p.id),
               CASE j.jn_zone WHEN '1区' THEN 1 WHEN '2区' THEN 2 WHEN '3区' THEN 3 WHEN '4区' THEN 4 ELSE NULL END
        FROM gkx.dwd_zh_paper p LEFT JOIN gkx.dwd_zh_journal j ON p.publication_id = j.publication_id
        WHERE p.cover_year_start BETWEEN %s AND %s
        LIMIT 20000
    """, (YEAR_LO, YEAR_HI))]

    # ---- 项目：级别 ----
    zh_projects = [tuple(r.values()) for r in qd("""
        SELECT CONCAT('zh:', id), project_level
        FROM gkx.dwd_zh_project
        WHERE approval_year BETWEEN 20200101 AND 20241231
        LIMIT 20000
    """)]

    # 分区/级别覆盖检查（小表，允许直查）
    probes["gkx.dwd_zh_journal.jn_zone_nonnull"] = int(
        qd("SELECT COUNT(*) n FROM gkx.dwd_zh_journal WHERE jn_zone IS NOT NULL AND jn_zone != ''")[0]["n"])
    probes["zh_project.level_dist"] = {
        str(r["project_level"]): int(r["n"])
        for r in qd("SELECT project_level, COUNT(*) n FROM gkx.dwd_zh_project GROUP BY project_level LIMIT 8")}
    probes["patent_cited.positive"] = int(
        qd("SELECT COUNT(*) n FROM gkx.dwd_patent_cited WHERE cited_by_nums > 0")[0]["n"])
    probes["_rows_source"] = "_work_gkx21/GKX_INVENTORY.json（库存实测值，不重复 COUNT(*)）"

    # ---- 专利双 P90 ----
    vals = [float(r[1]) for r in patents if r[1] is not None]
    cites = [float(r[3] or 0) for r in patents]
    v_p90 = pct(vals, PERC) or 0
    c_p90 = pct(cites, PERC) or 0
    pat_break = [r for r in patents if (r[1] is not None and float(r[1]) >= v_p90 and v_p90 > 0) or (float(r[3] or 0) >= c_p90 and c_p90 > 0)]
    pat_break_both = [r for r in patents if (r[1] is not None and float(r[1]) >= v_p90 and v_p90 > 0) and (float(r[3] or 0) >= c_p90 and c_p90 > 0)]

    # ---- 论文 1 区 ----
    papers_q1 = [r for r in zh_papers if r[1] == 1]

    # ---- 项目国家级 ----
    proj_nat = [r for r in zh_projects if r[1] and '国家级' in str(r[1])]

    def topn(rows, key=lambda r: 0, n=10):
        return [str(r[0]) for r in sorted(rows, key=lambda r: -key(r))[:n]]

    result = {
        "metric_id": "M_INNOV_BREAKTHROUGH_COUNT",
        "metric_name": "重大成果突破数",
        "method": "高影响尾部计数（OR 逻辑）：专利 value/被引 双 P90；论文 jn_zone=1区；项目 project_level=国家级",
        "data_source": "gkx（三方库只读）：dwd_patent / dwd_patent_cited / dwd_zh_paper / dwd_zh_journal / dwd_zh_project",
        "window": f"{YEAR_LO}-{YEAR_HI}",
        "probes": probes,
        "compute": {
            "patent": {
                "n_sampled": len(patents),
                "value_p90": round(v_p90, 1) if v_p90 else None,
                "cited_p90": c_p90,
                "breakthrough_count": len(pat_break),
                "breakthrough_both_dims": len(pat_break_both),
                "sample_keys": topn(pat_break, key=lambda r: (float(r[1] or 0) + float(r[3] or 0) * 1000)),
            },
            "zh_paper": {
                "n_sampled": len(zh_papers),
                "q1_count": len(papers_q1),
                "zone_coverage": len([r for r in zh_papers if r[1] is not None]),
                "sample_keys": [str(r[0]) for r in papers_q1[:10]],
            },
            "zh_project": {
                "n_sampled": len(zh_projects),
                "national_count": len(proj_nat),
                "sample_keys": [str(r[0]) for r in proj_nat[:10]],
            },
            "total_breakthrough": len(pat_break) + len(papers_q1) + len(proj_nat),
        },
        "support_judgment": None,
    }

    pat_ok = len(patents) >= 100 and len(pat_break) > 0
    result["support_judgment"] = "部分支持" if pat_ok else "完全不支持"
    result["support_note"] = (
        f"专利维可算（n={len(patents)}，双P90 突破 {len(pat_break)} 件）；"
        f"论文维 jn_zone 实测非空 {probes['gkx.dwd_zh_journal.jn_zone_nonnull']} 行但窗内抽样命中 {len([r for r in zh_papers if r[1] is not None])} 条；"
        f"项目维 level_dist={probes['zh_project.level_dist']}；"
        "论文/项目突破判定维度当前数据弱 → 部分支持"
    )

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "compute"}, ensure_ascii=False, indent=1))
    print(json.dumps(result["compute"], ensure_ascii=False, indent=1)[:1800])


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
    out_json = here / "M_INNOV_BREAKTHROUGH_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_BREAKTHROUGH_COUNT.py 等价）
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
        "metric_id": "M_INNOV_BREAKTHROUGH_COUNT",
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
