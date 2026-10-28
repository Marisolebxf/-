#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ORG_PERF_QUERY 查询结果·科研机构绩效
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ORG_PERF_QUERY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_ORG_PERF_QUERY · 查询结果·科研机构绩效（QUERY 层）

需求锚点：智慧服务门户/专题查询 ——「按机构名/类型/时间检索其绩效结果」。
需求没有给公式（查询态），要的是「查得到、返回快、字段稳定」。

本件做什么：库内没有预计算绩效结果表（`_snapshots21/probe_org_perf_tables_20261022.json`
实测 gkx 的 75 张机构相关表里没有任何 perf/score/rank 结果面），所以本件把
「机构 × 年 × 维度」离线物化成一张查询宽表，再用内存索引模拟查询接口，
并把每次查询的返回字段、缺失标记、耗时写进产物。

口径（零 SQL，只读快照）：
  产出·专利  = 面板 app_year，**只有 2021—2024**（面板窗口 2021—2024），2025/2026 记 null
  产出·论文  = panel.papers_year，查询窗取 2021—2025；2024 是采集口径尖峰（须标注）
  产出·项目  = panel.projects_year，查询窗取 2021—2025；项目表实际覆盖到 2022，
               2023—2025 记 null（不是 0）
  人才       = scholars / h_mean / academicians / people（学者库只命中 29 家）
  转化       = transfer_in / transfer_out（专利受让）
  影响       = policy_mentions / news
  对标       = 在 325 家「有信号」机构池内的分位

关键：本件是**即席物化 + 查询契约**，不是「已有结果面」。
"""
from __future__ import annotations

import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _org_m21_common as M  # noqa: E402

MID = "M_ORG_PERF_QUERY"
PATENT_YEARS = [2021, 2022, 2023, 2024]          # app_year 面板窗口
PAPER_YEARS = [2021, 2022, 2023, 2024, 2025]
PROJECT_YEARS = [2021, 2022, 2023, 2024, 2025]
QUERY_POOL_MIN_SIGNAL = 1


def as_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def build_rows(panel, app_year, prog):
    rows = []
    for x in panel["institutions"]:
        nm = x["name"]
        sig = sum(1 for k in ("patents", "papers", "projects", "scholars") if x[k])
        if sig < QUERY_POOL_MIN_SIGNAL:
            continue
        ay = app_year.get(nm, {})
        pat_series = {str(y): ay.get(str(y)) for y in PATENT_YEARS}
        pap_series = {str(y): as_int((x.get("papers_year") or {}).get(str(y))) for y in PAPER_YEARS}
        proj_series = {str(y): as_int((x.get("projects_year") or {}).get(str(y))) for y in PROJECT_YEARS}
        # 项目表覆盖到 2022：2023—2025 的 None 是「源不覆盖」，不是「没有项目」
        for y in ("2023", "2024", "2025"):
            if x.get("projects_year") and max((int(k) for k in x["projects_year"] if str(k).isdigit()),
                                              default=0) < int(y):
                proj_series[y] = None
        rows.append({
            "name": nm, "city": x["city"], "org_type": x["org_type"],
            "inc_year": x.get("inc_year"),
            "patents": x["patents"], "patent_grant": x["patent_grant"],
            "papers": x["papers"], "projects": x["projects"],
            "scholars": x["scholars"], "h_mean": x["h_mean"],
            "academicians": x["academicians"], "people": x["people"],
            "fund_wan": round(float(x.get("project_fund") or 0), 1),
            "transfer_in": x["transfer_in"], "transfer_out": x["transfer_out"],
            "policy_mentions": x["policy_mentions"], "news": x["news"],
            "discipline_top": x.get("discipline_top"), "kw_top": x.get("kw_top") or [],
            "patent_series": pat_series, "paper_series": pap_series,
            "project_series": proj_series,
            "signals": sig,
        })
    return rows


def pct_in_pool(rows):
    for key in ("patents", "papers", "projects", "scholars"):
        sub = [r for r in rows if r[key] > 0]
        pr = M.pct_rank([r[key] for r in sub])
        for r, v in zip(sub, pr):
            r[key + "_pct"] = round(v, 1)
    for r in rows:
        for key in ("patents", "papers", "projects", "scholars"):
            r.setdefault(key + "_pct", None)


def card(r):
    return {
        "identity": {"name": r["name"], "city": r["city"], "org_type": r["org_type"],
                     "inc_year": r["inc_year"]},
        "output": {
            "patents_total": r["patents"], "patent_grant": r["patent_grant"],
            "papers_total": r["papers"], "projects_total": r["projects"],
            "patent_series": r["patent_series"], "paper_series": r["paper_series"],
            "project_series": r["project_series"],
            "fund_wan": r["fund_wan"],
        },
        "talent": {"scholars": r["scholars"], "h_mean": r["h_mean"],
                   "academicians": r["academicians"], "people": r["people"]},
        "transfer": {"in": r["transfer_in"], "out": r["transfer_out"]},
        "influence": {"policy_mentions": r["policy_mentions"], "news": r["news"]},
        "structure": {"discipline_top": r["discipline_top"], "kw_top": r["kw_top"][:8]},
        "percentile_in_pool": {"patents": r["patents_pct"], "papers": r["papers_pct"],
                               "projects": r["projects_pct"], "scholars": r["scholars_pct"]},
        "data_flags": {
            "patent_series_years": "2021—2024（app_year 面板窗口；2025/2026 为 null，不是 0）",
            "paper_series_years": "2021—2025（2024 为采集口径尖峰）",
            "project_series_years": "2021—2022 有值，2023—2025 为 null（源表不覆盖）",
            "finance": "无（年报财务表对底册 2,074 家命中 0 行）",
            "scholars": "29/2,074 家有学者记录" if r["scholars"] else "该机构无学者记录",
        },
    }


def build_audit(rows):
    """查询层两处硬缺陷的实测：年度序列缺口、同名未消歧。"""
    no_series = [r for r in rows if r["patents"] and not any(r["patent_series"].values())]
    inner, parent = [], []
    seen = set()
    for a in rows:
        for b in rows:
            if a is b or (b["name"], a["name"]) in seen:
                continue
            if len(a["name"]) >= 6 and a["name"] in b["name"]:
                seen.add((a["name"], b["name"]))
                rec = {"short": a["name"], "short_patents": a["patents"],
                       "long": b["name"], "long_patents": b["patents"],
                       "same_city": a["city"] == b["city"]}
                # 短名是长名的前缀 → 母体与下属所，不是重复；短名嵌在中间 → 同一实体的另一种写法
                (parent if b["name"].startswith(a["name"]) else inner).append(rec)
    inner.sort(key=lambda d: -d["long_patents"])
    parent.sort(key=lambda d: -d["long_patents"])
    return {
        "patents_without_series": {
            "n": len(no_series),
            "patents": sum(r["patents"] for r in no_series),
            "share_of_all_patents": round(sum(r["patents"] for r in no_series)
                                          / sum(r["patents"] for r in rows), 4),
            "examples": [{"name": r["name"], "patents": r["patents"]} for r in
                         sorted(no_series, key=lambda r: -r["patents"])[:6]],
            "note": ("累计专利数与年度序列走两条匹配链：前者按申请人名命中，后者要求同时命中"
                     "面板的 app_year 口径。因此出现「有累计、无年份」的机构，页面不能把年度序列"
                     "画成 0 线。"),
        },
        "name_duplicates": {
            "n_inner": len(inner),
            "inner_examples": inner[:6],
            "n_parent_child": len(parent),
            "parent_child_note": ("短名是长名前缀的 36 对里绝大多数是母体与下属所"
                                  "（如「广东省科学院」是「广东省科学院新材料研究所」的前缀），"
                                  "不是重复实体，查询层不应合并，只应给出上卷关系。"),
            "note": ("`n_inner` 才是真重复候选：短名嵌在长名中间（如「深圳先进技术研究院」与"
                     "「中国科学院深圳先进技术研究院」），同一机构两种写法、两套数字，"
                     "查询层必须提示合并。"),
        },
    }


def query(rows, name=None, city=None, org_type=None, min_patents=0, limit=50):
    t0 = time.perf_counter()
    hit = rows
    if name:
        hit = [r for r in hit if name in r["name"]]
    if city:
        hit = [r for r in hit if r["city"] == city]
    if org_type:
        hit = [r for r in hit if r["org_type"] == org_type]
    if min_patents:
        hit = [r for r in hit if r["patents"] >= min_patents]
    hit = sorted(hit, key=lambda r: (-r["patents"], -r["papers"]))
    dt = (time.perf_counter() - t0) * 1000
    return hit[:limit], round(dt, 3), len(hit)


def main() -> None:
    panel = M.load_panel()
    app_year = M.load_app_year()
    reg_doc, reg = M.load_reg()
    prog = None

    rows = build_rows(panel, app_year, prog)
    pct_in_pool(rows)
    by_name = {r["name"]: r for r in rows}

    pool = {
        "n": len(rows),
        "by_city": dict(Counter(r["city"] for r in rows).most_common()),
        "by_type": dict(Counter(r["org_type"] for r in rows).most_common()),
        "with_patents": sum(1 for r in rows if r["patents"]),
        "with_papers": sum(1 for r in rows if r["papers"]),
        "with_projects": sum(1 for r in rows if r["projects"]),
        "with_scholars": sum(1 for r in rows if r["scholars"]),
        "with_transfer": sum(1 for r in rows if r["transfer_in"] or r["transfer_out"]),
        "with_policy": sum(1 for r in rows if r["policy_mentions"]),
        "with_patent_series": sum(1 for r in rows if any(v for v in r["patent_series"].values())),
        "with_finance": 0,
    }

    # ---- 三个示例查询：一个综合大学、一个国家所、一个医院 ----
    demo_names = ["深圳大学", "中国科学院深圳先进技术研究院", "深圳市人民医院"]
    samples = []
    for nm in demo_names:
        hits, ms, n = query(rows, name=nm)
        samples.append({"query": {"name": nm}, "hits": n, "ms": ms,
                        "card": card(hits[0]) if hits else None})
    # 位置兜底：万一底册里名字变了，至少给出模糊匹配样本
    if not any(s["card"] for s in samples):
        hits, ms, n = query(rows, city="深圳市", min_patents=50, limit=3)
        samples.append({"query": {"city": "深圳市", "min_patents": 50}, "hits": n, "ms": ms,
                        "card": card(hits[0]) if hits else None})

    # ---- 过滤查询：深圳专利 ≥50 的机构 ----
    big, ms_big, n_big = query(rows, city="深圳市", min_patents=50, limit=50)
    # ---- 类型查询：事业单位中论文 ≥20 ----
    pap, ms_pap, n_pap = [r for r in rows if r["org_type"] == "事业单位" and r["papers"] >= 20], 0.0, 0
    pap = sorted(pap, key=lambda r: -r["papers"])

    out = {
        "metric_id": MID,
        "metric_name": "查询结果·科研机构绩效",
        "domain": "QUERY / 科研机构绩效结果查询（门户查询层）",
        "formula_owner": "AI-20261022（推测定义，wanghui=false）",
        "support_judgment": "部分支持",
        **M.base_years(
            [2021, 2022, 2023, 2024, 2025], [2017, 2018, 2019, 2020],
            "查询窗 2021—2025。专利序列只到 2024（面板 app_year 窗口 2021—2024，2025/2026 记 null）；"
            "论文序列到 2025（2024 为采集口径尖峰）；项目序列只到 2022（源表不覆盖 2023 以后）。"
            "2017—2020 在专利库内零行，不按 0 摊入；2026 为残年，不进查询窗。"),
        "inputs": {
            "panel": "_snapshots21/org_family_panel_20261021.json（2,074 家）",
            "patent_year": "_snapshots21/patent_panel_innov_20261021.json 的 app_year（窗口 2021—2024）",
            "table_scan": "_snapshots21/probe_org_perf_tables_20261022.json（gkx 机构相关表 75 张的清单）",
        },
        "result_face_status": {
            "available": False,
            "evidence": ("gkx 中与 org/institut/perf/score/rank 相关的表共 75 张，"
                         "没有任何「机构绩效结果」宽表或得分表；live ADS 的 score 类表是样例级"
                         "（DATA_FACTS §3.3），不可作结果面。"),
            "substitute": "本件物化 325 家「有信号」机构的机构×年×维度宽表，作为即席查询的落地形态。",
        },
        "query_contract": {
            "filters": ["name（子串）", "city（等值）", "org_type（等值）",
                        "min_patents（下限）"],
            "returns": ["identity", "output（年度序列 + 累计）", "talent", "transfer",
                        "influence", "structure", "percentile_in_pool", "data_flags"],
            "null_rule": "源不覆盖的年份返回 null，不返回 0；前端必须把 null 显示为「无数据」。",
            "pool": "325 家有信号机构（专利/论文/项目/学者至少一项 >0）",
        },
        "pool": pool,
        "sample_queries": samples,
        "filter_queries": [
            {"query": {"city": "深圳市", "min_patents": 50}, "hits": n_big, "ms": ms_big,
             "rows": [{"name": r["name"], "patents": r["patents"],
                       "patent_grant": r["patent_grant"], "papers": r["papers"],
                       "projects": r["projects"], "scholars": r["scholars"]}
                      for r in big]},
            {"query": {"org_type": "事业单位", "min_papers": 20}, "hits": len(pap),
             "rows": [{"name": r["name"], "papers": r["papers"], "city": r["city"]}
                      for r in pap[:20]]},
        ],
        "pool_stats": {
            "patents": M.dist([r["patents"] for r in rows if r["patents"]]),
            "papers": M.dist([r["papers"] for r in rows if r["papers"]]),
            "projects": M.dist([r["projects"] for r in rows if r["projects"]]),
            "scholars": M.dist([r["scholars"] for r in rows if r["scholars"]]),
            "fund_wan": M.dist([r["fund_wan"] for r in rows if r["fund_wan"]]),
        },
        "year_series_coverage": {
            "patent": {str(y): sum(1 for r in rows if r["patent_series"].get(str(y))) for y in PATENT_YEARS},
            "paper": {str(y): sum(1 for r in rows if r["paper_series"].get(str(y))) for y in PAPER_YEARS},
            "project": {str(y): sum(1 for r in rows if r["project_series"].get(str(y))) for y in PROJECT_YEARS},
            "note": ("patent 2025/2026 缺（面板窗口）；project 2023—2025 缺（源表止于 2022）；"
                     "paper 2024 的机构数 162 是采集尖峰，不是产出翻倍。"),
        },
        "audit": build_audit(rows),
        "fact_table": [{"name": r["name"], "city": r["city"], "org_type": r["org_type"],
                        "patents": r["patents"], "patent_grant": r["patent_grant"],
                        "papers": r["papers"], "projects": r["projects"],
                        "scholars": r["scholars"], "fund_wan": r["fund_wan"],
                        "transfer_in": r["transfer_in"], "transfer_out": r["transfer_out"],
                        "policy_mentions": r["policy_mentions"],
                        "patent_series": r["patent_series"],
                        "paper_series": r["paper_series"],
                        "project_series": r["project_series"]}
                       for r in sorted(rows, key=lambda r: (-r["patents"], -r["papers"]))],
        "limits": [
            "没有预计算绩效结果表；本件是离线物化 + 内存查询，不是线上结果面。",
            "专利年度序列只到 2024（app_year 窗口 2021—2024），2025/2026 为 null；"
            "任何「2025 年专利产出」的查询都不可答。",
            "论文 2024 年 32,379 篇是采集口径尖峰（其他年 6,000 上下），不能读成产出爆发。",
            "项目序列只到 2022，2023 年以后 null；项目经费是项目全周期累计，不是年度投入。",
            "无营业收入/研发投入/研发人员：年报财务表对底册 2,074 家命中 0 行（DATA_FACTS §3.10）。",
            "学者只 29 家 / 145 人，h 均值与院士标记只对少数机构有值。",
            "机构名未消歧（同一机构多种写法会返回多条命中），查询层需在前端做「同名合并」提示。",
        ],
    }
    path = M.write_out(out, MID)
    print("wrote", path, "pool", pool["n"])
    print("samples", [(s["query"], s["hits"], s["card"]["identity"]["name"] if s["card"] else None) for s in samples])
    print("big", n_big, "paper20", len(pap), "ms", ms_big)


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
    out_json = here / "M_ORG_PERF_QUERY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ORG_PERF_QUERY.py 等价）
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
        "metric_id": "M_ORG_PERF_QUERY",
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
