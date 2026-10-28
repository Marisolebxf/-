#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_TINN_PATENT_QUALITY 专利质量
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_TINN_PATENT_QUALITY.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_TINN_PATENT_QUALITY · 专利质量（判：完全不支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_PATENT_QUALITY.md`（V1.5-20260901）
五维：家族规模（other_Versions）/ 权利要求数（claims 项数）/ 被引次数（cited_by_nums）/
技术宽度（IPC4 去重数）/ 法律状态稳定性（授权且未失效）；一行一个 IPC4，0—100。

为什么判完全不支持（本批实测，全部可复核）
----------------------------------------
1. 五张价值附表各只有 2 万行量级，对 2,939,895 行主表覆盖 0.68%—0.70%；
2. 五维要落到 IPC4，必须把附表按 `patent_id` / `pn` 回连主表，而主表除 `PRIMARY(dwd_id)`
   外没有可用索引：本批 3 条回连查询（family / cited / legal）**各跑满 60 秒被服务端中断**，
   复现 3 次（见 `_snapshots21/probe_tinn21_20261022.json`）；
3. 家族规模维在主表侧整列为空（`other_Versions` 前缀 3,000 行 0 行非空，见 POT_TECH_INFL）；
   权利要求维的正文是 mediumtext，全量取文本实测 60 秒超时（`claim_agg` 同批失败）；
4. 被引维只有 475 件能回连主表（0.0162%，见 FACTORS_014 实测）。
结论：五维中没有任何一维能在 IPC4 粒度闭环，故不产出任何领域分，只留覆盖率证据与修复清单。

运行：python3 code/M_INNOV_TINN_PATENT_QUALITY.py（零 SQL，全部读探针缓存与登记簿）
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_PATENT_QUALITY"
MAIN = 2_939_895


def main() -> None:
    pr = T.tail()
    tp = T.tinn()
    inv = json.loads((T.HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json").read_text(encoding="utf-8"))
    fac = json.loads((T.HERE / "M_INNOV_DS_FACTORS_014_out.json").read_text(encoding="utf-8"))
    pot = json.loads((T.HERE / "M_INNOV_POT_TECH_INFL_out.json").read_text(encoding="utf-8"))

    fam = T.rows_of(pr, "family_agg")[0]
    claim = T.rows_of(tp, "claim_cover")[0]
    cited = T.rows_of(pr, "cited_agg")[0]
    legal = T.rows_of(pr, "legal_agg")[0]
    status = T.rows_of(pr, "legal_status")
    ev = T.rows_of(pr, "legal_event_kw")[0]
    ov = T.rows_of(json.loads((T.SNAP / "probe_a26_20261022.json").read_text(encoding="utf-8")),
                   "other_versions_prefix")[0]
    joins = {k: tp[k] for k in ("family_join", "cited_by_ipc4", "legal_by_ipc4") if k in tp}

    cov = {
        "family": round(100 * int(fam[0]) / MAIN, 4),
        "claim": round(100 * int(claim[0]) / MAIN, 4),
        "cited": round(100 * int(cited[0]) / MAIN, 4),
        "legal": round(100 * int(legal[0]) / MAIN, 4),
    }

    res = {
        "metric_id": MID,
        "metric_name": "专利质量",
        "support_judgment": "完全不支持",
        "object": "技术领域（IPC 主分类前 4 位）",
        "verdict_reason": (
            "五维全部无法落到 IPC4：三张价值附表按 patent_id 回连主表各跑满 60 秒被中断（3 次复现），"
            "主表 side 的 other_Versions 整列为空、claims 正文全量读取超时、被引仅 475 件可回连。"
            "不是「分低」，是「算不出」，故不产出任何领域分"),
        "data_source": "gkx.dwd_patent_family / dwd_patent_claim / dwd_patent_cited / "
                       "dwd_patent_legal / dwd_patent（仅主键点查，均失败）",
        "sql_count": 0,
        "sql_note": "本脚本零 SQL；失败的三条回连查询见 code/_probe_tinn21_20261022.py 的落盘记录",
        "probe": {
            "patent_main_rows": MAIN,
            "family_rows": int(fam[0]),
            "family_distinct_patent_id": int(fam[1]),
            "family_json_nonempty": int(fam[3]),
            "claim_rows": int(claim[0]),
            "claim_distinct_patent_id": int(claim[1]),
            "cited_rows": int(cited[0]),
            "cited_positive_rows": int(cited[2]),
            "cited_sum": int(cited[3]),
            "cited_max": int(cited[4]),
            "cited_joinable_to_main": int(fac["probes"]["cited_join_patent_id"]),
            "legal_rows": int(legal[0]),
            "legal_expiration_filled": int(legal[5]),
            "other_versions_prefix_n": int(ov[0]),
            "other_versions_prefix_filled": int(ov[1] or 0),
            "coverage_pct_vs_main": cov,
            "return_join_timeouts": {k: {"ok": v.get("ok"), "sec": v.get("sec"),
                                         "error": (v.get("error") or "")[:80]} for k, v in joins.items()},
            "return_join_timeout_count": sum(1 for v in joins.values() if not v.get("ok")),
        },
        "dimension_status": {
            "D1_家族规模": {
                "formula": "同族成员数合计 / 专利数",
                "table": "dwd_patent.other_Versions / dwd_patent_family",
                "rows": int(fam[0]),
                "coverage_pct": cov["family"],
                "status": "不可用：主表 other_Versions 前缀样本 0/3,000 非空；family 表无 IPC/申请人字段，"
                          "按 patent_id 回连主表 60 秒超时",
            },
            "D2_权利要求数": {
                "formula": "权利要求项数合计 / 专利数",
                "table": "dwd_patent_claim.original_text",
                "rows": int(claim[0]),
                "coverage_pct": cov["claim"],
                "status": "不可用：正文为 mediumtext，20,026 行全量取文本实测 60 秒超时；"
                          "且无 IPC4 字段，回连同样超时",
            },
            "D3_被引次数": {
                "formula": "SUM(cited_by_nums)",
                "table": "dwd_patent_cited.cited_by_nums",
                "rows": int(cited[0]),
                "coverage_pct": cov["cited"],
                "status": "不可用：20,515 行里只有 475 件能按 patent_id 回连主表（0.0162%），"
                          "其余指向不存在的专利号",
            },
            "D4_技术宽度": {
                "formula": "每件 IPC4 去重数合计 / 专利数",
                "table": "dwd_patent(main_classification_ipcr, further_classification_ipcr)",
                "status": "不可用：附加分类只在主表侧，面板只采了主分类；按 IPC4 统计需全表 294 万行聚合，"
                          "实测 600 秒断连（DATA_FACTS §3.6）",
            },
            "D5_法律状态稳定性": {
                "formula": "（授权且未失效）/ 专利数",
                "table": "dwd_patent_legal(status, expiration_year)",
                "rows": int(legal[0]),
                "coverage_pct": cov["legal"],
                "status": "不可用：20,000 行覆盖 0.68%，按 patent_id 回连 60 秒超时；"
                          "status 分布见下，但落不到 IPC4",
            },
        },
        "legal_status_dist": [[r[0], int(r[1])] for r in status],
        "event_keyword_counts": {
            "许可_中文": int(ev[0]), "许可_英文": int(ev[1]), "开放许可": int(ev[2]),
            "质押_中文": int(ev[3]), "质押_英文": int(ev[4]), "诉讼或无效_中文": int(ev[5]),
            "note": "以上是对 20,000 行 legal_events 的全局 LIKE 计数，无法拆到 IPC4，仅作稀疏度证据",
        },
        "base_years_used": [],
        "base_years_missing": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_year_block": T.base_year_block(
            [], [2021, 2022, 2023, 2024, 2025, 2026],
            "价值附表无申请年字段且无法回连主表，任何年度分母都不成立"),
        "gaps": [
            "五张价值附表各约 2 万行，对 294 万行主表覆盖 0.68%—0.70%",
            "主表 side 的 other_Versions 整列为空（前缀样本 0/3,000）",
            "dwd_patent_claim.original_text 为 mediumtext，全量取文本 60 秒超时",
            "dwd_patent_cited 只有 475 件可回连主表（0.0162%）",
            "主表 pn 无索引，按专利号回连即 294 万行扫描",
        ],
        "repair_requirements": [
            "把五张附表扩到全量，并在表内直接冗余 ipc4 / apdt_year，避免回连主表",
            "或给 dwd_patent 的 patent_id / pn 建可用索引，并允许分块聚合",
            "补 dwd_patent.other_Versions（同族）与 further_classification_ipcr（附加分类）",
            "权利要求项数改为入库时预计算的整数列（claim_nums），不要每次解析 mediumtext",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps({"coverage": cov, "joins": res["probe"]["return_join_timeouts"]},
                     ensure_ascii=False, indent=1))


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
    out_json = here / "M_INNOV_TINN_PATENT_QUALITY_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_TINN_PATENT_QUALITY.py 等价）
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
        "metric_id": "M_INNOV_TINN_PATENT_QUALITY",
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
