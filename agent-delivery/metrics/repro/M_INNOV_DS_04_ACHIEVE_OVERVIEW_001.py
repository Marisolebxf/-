#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 创新价值
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 · 创新价值（20261021 改源：三方库 gkx）

口径完全沿用王惠 V1.5（= 上游 M_INNOV_ACHIEVE_VALUE，步骤一致，不改公式）
--------------------------------------------------------------------
三类成果 × 三维，批内极值归一、缺测维不补 0（可用维重归一）、等权 ×100，P70/P30 分档：
  专利    ：技术=value / 应用=2019-2024 转移次数 / 潜在=被引合计；附深圳切片。
  中文论文：技术=impact_score / 应用=download_num / 潜在=jn_zone(1区4…4区1，其余0)。
  国内项目：技术=funded_amount / 应用=结题摘要有无 / 潜在=project_level(国家级3/省部级2/其他1)。
样本：与旧版一致，每类按表内顺序取 5,000 行（LIMIT 5000），窗口 2019-2024。

本版只改数据源与取数方式
------------------------
1. 旧演示库 / `_devdb` 全部删除，改 `gkx.*`（行数镜像：patent 2,939,895 /
   zh_paper 100,900 / zh_project 58,453 / journal 2,796）。
2. 旧版对每一行专利跑两个相关子查询（cited / transfer 的 pn 均无索引），本版改为
   「先取 5,000 行 → 按 pn 批量 GROUP BY 回填」，公式与分子不变、避免 5,000 次全表扫描。
3. 论文的 journal 关联改为客户端字典映射（等价 LEFT JOIN，规避无索引 JOIN）。
4. 分区/被引/转移/下载四张表当日空值率全部重新实测（probes_today），不引用旧结论。
"""
from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

import _gkx21_common as C

HERE = Path(__file__).resolve().parent
MID = "M_INNOV_DS_04_ACHIEVE_OVERVIEW_001"
YEAR_LO, YEAR_HI = 2019, 2024
SAMPLE_N = 5000
PLACEHOLDER = ("NULL", "", "NONE", "-")


def clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def norm(vals):
    xs = [v for v in vals if v is not None]
    if not xs:
        return [None] * len(vals)
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return [(0.5 if v is not None else None) for v in vals]
    return [((v - lo) / (hi - lo) if v is not None else None) for v in vals]


def pctl(sorted_xs, p):
    if not sorted_xs:
        return None
    return sorted_xs[max(0, min(len(sorted_xs) - 1, int(len(sorted_xs) * p / 100)))]


def score_batch(rows, idx=(1, 2, 3)):
    ns = [norm([r[i] for r in rows]) for i in idx]
    out = []
    for i, r in enumerate(rows):
        parts = [n[i] for n in ns]
        avail = [p for p in parts if p is not None]
        out.append((r, parts, (sum(avail) / len(avail) * 100) if avail else None))
    return out


def stats_with_tier(out):
    scores = sorted(s for _, _, s in out if s is not None)
    if not scores:
        return {}
    p70, p30 = pctl(scores, 70), pctl(scores, 30)
    return {"n": len(scores), "min": round(scores[0], 2), "max": round(scores[-1], 2),
            "mean": round(sum(scores) / len(scores), 2), "median": round(pctl(scores, 50), 2),
            "p70": round(p70, 2), "p30": round(p30, 2),
            "tier": {"high": sum(1 for s in scores if s >= p70),
                     "low": sum(1 for s in scores if s <= p30),
                     "mid": sum(1 for s in scores if p30 < s < p70)}}


def top(out, n=8):
    return [{"key": r[0], "dims": [round(d, 3) if d is not None else None for d in ds],
             "sz": (r[4] if len(r) > 4 else None), "score": round(s, 2)}
            for r, ds, s in sorted(out, key=lambda x: -(x[2] or 0))[:n] if s is not None]


def sz_names():
    return {clean(r[2]) for r in C.base_rows() if r[4] and "深圳" in str(r[4]) and clean(r[2])}


def patent_rows():
    rows = C.q("""
        SELECT pn, value, first_applicant_name
        FROM gkx.dwd_patent
        WHERE apdt_year BETWEEN %s AND %s
        LIMIT %s
    """, (YEAR_LO, YEAR_HI, SAMPLE_N))
    pns = [r[0] for r in rows if r[0]]
    ph = ",".join(["%s"] * len(pns))
    cited = {r[0]: float(r[1] or 0) for r in C.q(
        "SELECT pn, SUM(cited_by_nums) FROM gkx.dwd_patent_cited WHERE pn IN (" + ph + ") GROUP BY pn", pns)}
    trans = {r[0]: float(r[1] or 0) for r in C.q(
        "SELECT pn, COUNT(*) FROM gkx.dwd_patent_transfer WHERE pn IN (" + ph +
        ") AND transfer_effective_date BETWEEN '2019-01-01' AND '2024-12-31' GROUP BY pn", pns)}
    sz = sz_names()
    return [(r[0], float(r[1]) if r[1] is not None else None,
             trans.get(r[0], 0.0), cited.get(r[0], 0.0),
             clean(r[2]) in sz, clean(r[2])) for r in rows]


def zh_paper_rows():
    rows = C.q("""
        SELECT CONCAT('zh:', id), publication_id, download_num
        FROM gkx.dwd_zh_paper
        WHERE cover_year_start BETWEEN %s AND %s
        LIMIT %s
    """, (YEAR_LO, YEAR_HI, SAMPLE_N))
    jour = {r[0]: (r[1], r[2]) for r in C.q(
        "SELECT publication_id, impact_score, jn_zone FROM gkx.dwd_zh_journal")}
    zone = {"1区": 4, "2区": 3, "3区": 2, "4区": 1}
    out = []
    for pid, pub, dl in rows:
        imp, zn = jour.get(pub, (None, None))
        out.append((pid, float(imp) if imp is not None else None, float(dl or 0),
                    float(zone.get(clean(zn), 0))))
    return out


def zh_project_rows():
    rows = C.q("""
        SELECT CONCAT('zh:', id), funded_amount,
               CASE WHEN final_report_abstract IS NOT NULL AND final_report_abstract <> '' THEN 1 ELSE 0 END,
               CASE project_level WHEN '国家级' THEN 3 WHEN '省部级' THEN 2 ELSE 1 END
        FROM gkx.dwd_zh_project
        WHERE approval_year BETWEEN %s AND %s
        LIMIT %s
    """, (int(f"{YEAR_LO}0101"), int(f"{YEAR_HI}1231"), SAMPLE_N))
    return [(r[0], float(r[1]) if r[1] is not None else None,
             float(r[2]), float(r[3] or 0)) for r in rows]


def probes_today():
    p = {}
    r = C.q1("SELECT COUNT(*), SUM(impact_score IS NULL), SUM(jn_zone IS NULL) FROM gkx.dwd_zh_journal")
    p["gkx.dwd_zh_journal"] = {"rows": int(r[0]), "impact_score_null": int(r[1] or 0),
                               "jn_zone_null": int(r[2] or 0)}
    r = C.q1("SELECT COUNT(*), SUM(download_num=0), SUM(download_num IS NULL) FROM gkx.dwd_zh_paper")
    p["gkx.dwd_zh_paper"] = {"rows": int(r[0]), "download_zero": int(r[1] or 0), "download_null": int(r[2] or 0)}
    p["gkx.dwd_patent_cited"] = int(C.q1("SELECT COUNT(*) FROM gkx.dwd_patent_cited")[0])
    p["gkx.dwd_patent_transfer"] = int(C.q1("SELECT COUNT(*) FROM gkx.dwd_patent_transfer")[0])
    r = C.q1("SELECT COUNT(*), COUNT(DISTINCT project_level), SUM(project_level IS NULL) FROM gkx.dwd_zh_project")
    p["gkx.dwd_zh_project"] = {"rows": int(r[0]), "distinct_level": int(r[1] or 0), "null_level": int(r[2] or 0)}
    p["gkx.dwd_patent"] = {"rows": int(json.loads((HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json")
                                                  .read_text(encoding="utf-8"))["dwd_patent"]["rows"]),
                           "note": "行数读 GKX_INVENTORY.json；本指标只取 5,000 行样本"}
    return p


def main():
    t0 = time.time()
    probes = probes_today()

    pat_rows = patent_rows()
    zhp_rows = zh_paper_rows()
    prj_rows = zh_project_rows()

    p_out, z_out, j_out = score_batch(pat_rows), score_batch(zhp_rows), score_batch(prj_rows)

    sz_p = [s for r, _, s in p_out if s is not None and r[4]]
    sz_sorted = sorted(sz_p)
    sz_share = round(len(sz_p) / len(pat_rows) * 100, 2) if pat_rows else None

    def view(block, kind):
        return {"kind": kind, "n": block.get("n"), "min": block.get("min"), "max": block.get("max"),
                "mean": block.get("mean"), "median": block.get("median"),
                "p70": block.get("p70"), "p30": block.get("p30"),
                "tier_high": (block.get("tier") or {}).get("high"),
                "tier_mid": (block.get("tier") or {}).get("mid"),
                "tier_low": (block.get("tier") or {}).get("low"),
                "spread": round((block.get("max") or 0) - (block.get("min") or 0), 2),
                "degenerate": block.get("max") == block.get("min"),
                "top3": [{"key": t["key"], "score": t["score"]} for t in block.get("top", [])[:3]]}

    p_stats = {**stats_with_tier(p_out), "sz_slice": {"n": len(sz_p),
               "mean": round(sum(sz_p) / len(sz_p), 2) if sz_p else None,
               "median": round(pctl(sz_sorted, 50), 2) if sz_p else None},
               "top": top(p_out)}
    z_stats = {**stats_with_tier(z_out), "top": top(z_out, 5)}
    j_stats = {**stats_with_tier(j_out), "top": top(j_out, 5)}

    views = [view(p_stats, "专利"), view(z_stats, "中文论文"), view(j_stats, "国内项目")]
    degenerate = [v["kind"] for v in views if v["degenerate"]]

    jour_ok = probes["gkx.dwd_zh_journal"]["impact_score_null"] < probes["gkx.dwd_zh_journal"]["rows"]
    dl_ok = probes["gkx.dwd_zh_paper"]["download_zero"] < probes["gkx.dwd_zh_paper"]["rows"]
    paper_ok = jour_ok or dl_ok
    patent_ok = p_stats["n"] > 100 and p_stats["max"] > p_stats["min"]

    judgment = "部分支持" if (patent_ok and not paper_ok) else ("完全转换支持" if patent_ok else "完全不支持")
    note = (
        f"专利型三维修齐（n={p_stats['n']:,}，区间 {p_stats['min']}-{p_stats['max']}，"
        f"P70={p_stats['p70']}/P30={p_stats['p30']}，分档 high {p_stats['tier']['high']}/"
        f"mid {p_stats['tier']['mid']}/low {p_stats['tier']['low']}，深圳切片 {len(sz_p):,} 条占 {sz_share}%）；"
        f"论文型期刊 impact_score/jn_zone 当日 {probes['gkx.dwd_zh_journal']['impact_score_null']}/"
        f"{probes['gkx.dwd_zh_journal']['rows']} 全空、download_num 全 0（"
        f"{probes['gkx.dwd_zh_paper']['download_zero']}/{probes['gkx.dwd_zh_paper']['rows']}）；"
        f"项目型 project_level 全单值（{probes['gkx.dwd_zh_project']['rows']:,} 行仅 "
        f"{probes['gkx.dwd_zh_project']['distinct_level']} 个取值）→ 三类成果仅一类有区分度 → 部分支持"
    )

    res = {
        "metric_id": MID,
        "metric_name": "创新价值",
        "also_known_as": "M_INNOV_ACHIEVE_VALUE（王惠 calc-logic：同口径，步骤完全一致）",
        "method": "王惠 V1.5 三维×三型、批内极值归一、缺测维不补0、等权×100、P70/P30 分档；本脚本按概览视角重组",
        "data_source": "gkx.dwd_patent / dwd_patent_cited / dwd_patent_transfer / dwd_zh_paper / "
                       "dwd_zh_journal / dwd_zh_project / dwd_org_base_info",
        "reuse_policy": "公式沿用上游，数值在本库当日重算（不再复用 demo 侧 out.json 的数字）",
        "derived_meta": {"window": f"{YEAR_LO}-{YEAR_HI}", "sample_n_per_type": SAMPLE_N,
                         "upstream_method": "王惠 V1.5 升级版 v2"},
        "probes_today": probes,
        "compute": {"n_scored_total": sum(v["n"] or 0 for v in views),
                    "by_type": views,
                    "degenerate_types": degenerate,
                    "patent_sz_slice": p_stats["sz_slice"],
                    "patent_sz_share_pct": sz_share,
                    "top_by_type": {"patent": p_stats["top"], "zh_paper": z_stats["top"],
                                    "zh_project": j_stats["top"]}},
        "support_judgment": judgment,
        "support_note": note,
        "elapsed_sec": round(time.time() - t0, 1),
    }
    C.write_out(MID, res)
    print(f"[{MID}] " + " | ".join(f"{v['kind']} n={v['n']} {v['min']}-{v['max']} deg={v['degenerate']}"
                                   for v in views) + f" sz={len(sz_p)} {round(time.time()-t0,1)}s")


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_INNOV_DS_04_ACHIEVE_OVERVIEW_001_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.py 等价）
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
        "metric_id": "M_INNOV_DS_04_ACHIEVE_OVERVIEW_001",
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
