#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创新影响预测（M_INNOV_DS_04_REALTIME_005）—— Holt 外推 · **门槛未过，不发射预测**

王惠口径（calc-logic M_INNOV_IMPACT_FORECAST）：
  输入 = 同一套实体（机构 / IPC 领域）的逐年产出件数序列
  模型 = Holt 线性指数平滑（α=0.5，β=0.3），**满 8 期**，年预 2 期
  输出 = 点预测 + 约 80% 区间 + 贡献度（该实体预测值 / 同类合计预测值），校验 rmse/mae

本件的核心事实（决定了它不能给预测值）：
  `gkx.dwd_patent.apdt_year` 只有 2021—2026。其中
    2021—2024 是完整年（604,512 / 601,893 / 611,811 / 606,468）→ **4 期**；
    2025 入库 440,401 件（比前四年低 27%，含公开滞后）→ 不完整；
    2026 入库 74,810 件 → 残年（采集时点 2026-10，公开滞后叠加）。
  4 期 < 8 期门槛 ⇒ **不外推**，`forecast_emitted=false`。
  把 2021—2025 硬算成 5 期仍然 < 8，结论不变。任何用 4—5 点拟合出来的斜率都不能
  包装成「稳健短期预测」——这正是隔离前旧稿把 `[0,0,0,0,y21..y24]` 喂给 Holt 后
  产出「两年预测 ≈ 八年总产出 67%」的原因（gate_check.py 已把该形态列为 error）。

本件交付的是**可预测性评估**：年序列、门槛判定、缺口与修复路径，以及一个
在合成 8 期序列上跑通的 Holt 实现自检（证明 gate 是门槛判定，不是函数坏了）。

重建背景：原稿读 20261020 目录共享 bundle（演示库 + 2017—2020 补零，DATA_FACTS §3.19）。
本脚本零 SQL、零 bundle。

产物：code/M_INNOV_DS_04_REALTIME_005_out.json
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import _ds04_common as D

METRIC = "M_INNOV_DS_04_REALTIME_005"
ORG_MIN_TOTAL = 50            # 只对「明星级」机构建序列，避免 169,226 条全量输出
TOP_SERIES = 20


def series_of_domain() -> list:
    out = []
    for term, yc in D.ipc_year().items():
        s = {y: yc.get(y, 0) for y in D.PATENT_YEARS}
        out.append({"node": term, "series": s})
    out.sort(key=lambda r: -sum(r["series"].values()))
    return out


def series_of_org() -> list:
    agg = D.applicant_agg()
    oy = D.org_patent_year()
    base = D.base_orgs()
    out = []
    for nm, v in agg.items():
        if int(v[0]) < ORG_MIN_TOTAL:
            continue
        s = {y: oy.get((nm, y), 0) for y in D.PATENT_YEARS}
        out.append({"node": nm, "series": s,
                    "city": (base.get(nm) or {}).get("city"),
                    "in_base": 1 if nm in base else 0})
    out.sort(key=lambda r: -sum(r["series"].values()))
    return out


def observed(series: dict) -> dict:
    """只报观测值，不做任何拟合：末年值、完整期首末比、末年同比、当期占比。"""
    c = [series.get(y, 0) for y in D.COMPLETE_YEARS]
    first, last = c[0], c[-1]
    prev = c[-2] if len(c) > 1 else None
    return {
        "sum_complete": sum(c),
        "last_complete_year": D.COMPLETE_YEARS[-1],
        "last_complete_value": last,
        "first_complete_value": first,
        "ratio_last_over_first": round(last / first, 4) if first else None,
        "yoy_last": round(last / prev - 1, 4) if prev else None,
        "y2025_partial": series.get(2025, 0),
        "y2026_residual": series.get(2026, 0),
    }


def main():
    t0 = time.time()
    dom = series_of_domain()
    org = series_of_org()
    ytot = D.year_total()
    total_complete = sum(ytot.get(y, 0) for y in D.COMPLETE_YEARS)

    n_complete = len(D.COMPLETE_YEARS)                 # 4
    n_if_2025 = n_complete + 1                          # 5
    gate = {
        "required_periods": D.MIN_PERIODS,
        "periods_complete": n_complete,
        "periods_complete_list": list(D.COMPLETE_YEARS),
        "periods_if_2025_counted": n_if_2025,
        "residual_year_excluded": D.RESIDUAL_YEAR,
        "passed": n_complete >= D.MIN_PERIODS,
        "decision": ("不外推：4 期 < 8 期门槛；把 2025 硬算成完整年也只有 5 期，仍不足"),
        "forecast_emitted": False,
    }

    dom_obs = []
    for r in dom[:TOP_SERIES]:
        o = observed(r["series"])
        o["node"] = r["node"]
        o["current_share_2024"] = round(r["series"].get(2024, 0) / max(ytot.get(2024, 0), 1), 6)
        dom_obs.append(o)

    org_obs = []
    for r in org[:TOP_SERIES]:
        o = observed(r["series"])
        o["node"] = r["node"]
        o["city"] = r["city"]
        o["current_share_2024"] = round(r["series"].get(2024, 0) / max(ytot.get(2024, 0), 1), 6)
        org_obs.append(o)

    # Holt 实现自检：合成 8 期序列，只为证明函数可执行；**不是**对真实数据的预测
    synth = [100, 108, 117, 126, 138, 149, 163, 178]
    selftest = D.holt(synth, 0.5, 0.3, 2)
    selftest["label"] = "合成 8 期序列自检（非真实数据、非本库预测）"

    out = {
        "metric_id": METRIC,
        "name": "创新影响预测",
        "vendor_metric": "M_INNOV_IMPACT_FORECAST",
        "formula_owner": "王惠",
        "view": "forecast",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "runtime_sec": None,
        "data_source": ("gkx.dwd_patent IPC 小类×年全量缓存（634 个领域、2,420,915 件）与 "
                        "申请人×年面板（275,135 组）；对应表 dwd_patent.apdt_year 只有 2021—2026"),
        "db": "gkx @ 183.240.141.251:3318（只读，本脚本零 SQL）",
        "definition": ("对同一套机构/领域实体的逐年产出件数做 Holt 线性指数平滑外推"
                       "（α=0.5、β=0.3、满 8 期、年预 2 期），输出点预测、约 80% 区间与贡献度。"),
        "statistical_year": D.T,
        "windows": {"recent": list(D.RECENT), "base_formula": list(D.BASE_FORMULA),
                    "base_used": list(D.BASE_USED_PATENT)},
        "params": {"model": "Holt linear", "alpha": 0.5, "beta": 0.3, "horizon": 2,
                   "min_periods": D.MIN_PERIODS, "interval": 0.8},

        # ---- 硬约束：基期三字段进顶层（本件把「训练期」也写进这三个字段）----
        "base_years_used": list(D.COMPLETE_YEARS),
        "base_years_missing": list(D.BASE_MISSING_PATENT),
        "base_years_note": ("本件的「基期」是训练期：库内完整年只有 2021—2024 四期，"
                            "公式要 8 期；2017—2020 在 dwd_patent.apdt_year 上零行，"
                            "2025 含公开滞后、2026 为残年，均不进训练。"),
        "forecast_emitted": False,
        "gate": gate,
        "forecast": None,
        "interval80": None,
        "contrib": None,

        "family": {
            "group": "M_INNOV_DS_04（科技发展态势·全球创新监测）",
            "this": "REALTIME_005 = 在 REALTIME_004 的节点年序列上做 Holt 外推（本件未发射）",
            "upstream": "M_INNOV_DS_04_REALTIME_004（同一套实体，产出规模序列）",
            "sibling": {
                "M_INNOV_DS_04_MONITOR_001": "词条级突现（列表）",
                "M_INNOV_DS_04_MONITOR_002": "词条级价值（详情）",
            },
            "key_diff": "004 给当期节点得分；005 要给未来 2 期——两者共用实体与年序列，不共用结果",
        },

        "probes": {
            "year_totals": {str(y): n for y, n in sorted(ytot.items())},
            "complete_years": list(D.COMPLETE_YEARS),
            "residual_year": D.RESIDUAL_YEAR,
            "y2025_vs_mean_2021_2024": round(ytot.get(2025, 0) / (total_complete / n_complete), 4),
            "y2026_vs_mean_2021_2024": round(ytot.get(2026, 0) / (total_complete / n_complete), 4),
            "n_domains": len(dom),
            "n_orgs_with_series": len(org),
            "org_min_total": ORG_MIN_TOTAL,
            "domain_panel_window": list(D.PATENT_YEARS),
            "org_panel_window": [2021, 2024],
            "org_panel_note": ("申请人×年面板（patent_panel_innov，275,135 组）的 year 只有 2021—2024，"
                               "因此机构序列里 2025/2026 的 0 是**面板未覆盖**，不是「该年无申请」；"
                               "领域序列的 2021—2026 全部为库内真实年份。"),
            "n_node_total_output": sum(sum(r["series"].values()) for r in dom),
        },
        "compute": {
            "n_domains_series": len(dom),
            "n_orgs_series": len(org),
            "n_forecast_nodes": 0,
            "n_interval_nodes": 0,
            "rmse_train": None,
            "mae_train": None,
            "contrib_method": None,
            "series_fields": ("year_counts（领域 2021—2026 实测，2026 标残年；机构 2021—2024 实测，"
                              "2025/2026 为面板未覆盖的 0）、observed（末年值/首末比/末年同比/当期占比，"
                              "全部为观测值，无拟合）"),
        },
        "series_domain_top": [{"node": r["node"],
                               "year_counts": {str(y): v for y, v in r["series"].items()},
                               **observed(r["series"])} for r in dom[:TOP_SERIES]],
        "series_org_top": [{"node": r["node"], "city": r["city"],
                            "year_counts": {str(y): v for y, v in r["series"].items()},
                            **observed(r["series"])} for r in org[:TOP_SERIES]],
        "observed_domain": dom_obs,
        "observed_org": org_obs,
        "impl_selftest": selftest,
        "repair_path": [
            "补 2017—2020 四年的专利数据（当前 apdt_year 零行）：补 3 年即可到 7 期、"
            "补 4 年才到 8 期，是唯一不降口径的路径；",
            "或取得「公开滞后校正因子」后把 2025 纳入并重定义窗口（例如改用申请年+18 个月口径），"
            "可到 5 期，仍不足 8 期；",
            "或经口径负责人确认把门槛从 8 期降到 5 期，并在指标说明里改公式——属降口径，需书面确认，"
            "本件不自行修改；",
            "论文侧不能补位：中文论文只有 100,900 篇且分类子集 19.87%，英文论文 1,387 篇，"
            "且论文与 IPC 无映射，无法与专利序列拼成同一实体的更长序列。",
        ],
        "quarantine_delta": {
            "why": ("隔离前旧稿把 bundle 的 impact_forecast 段直接当结果，而该 bundle 的训练序列是 "
                    "[0,0,0,0,y2021..y2024]——2017—2020 被 .get(y,0) 补成 0（DATA_FACTS §3.19），"
                    "把趋势斜率顶高，跑出「两年预测≈八年总产出 67%」这种量级失真"),
            "old_vs_new": [
                {"item": "训练期", "old": "2017—2024（n=8，其中 4 个是补的 0）",
                 "new": "2021—2024（n=4，全部为实测完整年）",
                 "cause": "apdt_year 只有 2021—2026，2017—2020 零行，不能补 0 当观测"},
                {"item": "是否发射预测", "old": "是（Top10 两年点预测 + 贡献度）",
                 "new": False,
                 "cause": "4 期 < 8 期门槛，外推不成立"},
                {"item": "两年预测合计", "old": 8385, "new": None,
                 "cause": "旧值出自 H02J7/00 的补零序列；本件不发射，故无此数"},
                {"item": "pred/output 比", "old": 0.67, "new": None,
                 "cause": "同上；该比值是「趋势项被 4 个前导 0 抬高」的直接表现"},
                {"item": "贡献度", "old": "按预测值重算 contrib_forecast",
                 "new": "未产出（只给当期占比 current_share_2024，且不是预测贡献度）",
                 "cause": "无预测即无预测贡献度；用当期占比顶替会把描述当预测"},
                {"item": "区间与训练误差", "old": "均未落库（interval/rmse/mae 为 None）",
                 "new": "未发射，故仍为 None；Holt 实现已在合成 8 期序列上自检通过",
                 "cause": "自检只证明函数可执行，不构成对本库数据的预测"},
            ],
        },
        "support_judgment": "部分支持",
        "support_basis": (
            "年序列这一维可用：634 个 IPC 领域与 %d 个机构（件数≥%d）的 2021—2026 逐年件数都能逐条复核；"
            % (len(org), ORG_MIN_TOTAL) +
            "但公式要求的「满 8 期」在本库只有 4 个完整期（2021—2024），2025 含公开滞后、2026 为残年，"
            "2017—2020 在 apdt_year 上零行。核心输出（Holt 点预测、区间、预测贡献度）因此全部未发射，"
            "按「部分依赖维度无法得到足够数据」判部分支持，不判完全转换支持。"),
        "reasons": [
            "样本期不足是本件唯一的阻断点：4 个完整年 < 8 期门槛，且缺口不是「没采集」而是源表年份就没有；",
            "2025 年 440,401 件只有 2021—2024 年均值的 %s，"
            "把 2025 当完整年会系统性压低末年水平，因此即便凑到 5 期也不等于「更长样本」；"
            % ("%.2f%%" % (100 * ytot.get(2025, 0) / (total_complete / n_complete))),
            "2026 年 74,810 件为残年（采集时点 2026-10 且公开有滞后），任何年度趋势图的末年都不能用它；",
            "论文侧补不了位：分类子集 20,048 篇占 19.87%、英文论文 1,387 篇、且论文与 IPC 无映射，"
            "不能与专利序列拼成同一实体的更长序列；",
            "旧稿的 8 期序列里有 4 个是补出来的 0，这会把 Holt 的初始水平压到 0、"
            "把趋势项推到大正数，于是「预测值远超实际」——本件不重复该写法。",
        ],
        "notes": [
            "本脚本零 SQL、无 reused_from；年序列全部读 code/_snapshots21/ 缓存。",
            "`forecast_emitted=false` 是门槛判定，不是脚本能力缺失：impl_selftest 里 Holt 在 8 期合成序列上正常输出点预测、80% 区间与 rmse/mae。",
            "领域序列的 2021—2026 全部为库内真实年份，年与年之间的 0 是实测 0（全量扫描派生，某年无申请即 0）；"
            "机构序列的 2025/2026 是申请人×年面板（window=2021—2024）未覆盖，不是实测 0，不能当下降读；",
            "库外年份（2017—2020）两侧都不补；不要把 2017—2020 的 0 与 2025/2026 的 0 混为一谈——前者是数据不存在、后者是面板未覆盖。",
            "不要把 current_share_2024 当「贡献度」展示：贡献度定义是预测值占比，本件没有预测值。",
        ],
    }
    out["runtime_sec"] = round(time.time() - t0, 1)

    p = D.write_out(METRIC, out)
    print("written", p)
    print("gate:", gate["passed"], "periods", gate["periods_complete"], "/", gate["required_periods"])
    print("forecast_emitted:", out["forecast_emitted"])
    print("domains", len(dom), "orgs", len(org))
    print("2025 ratio", out["probes"]["y2025_vs_mean_2021_2024"],
          "2026 ratio", out["probes"]["y2026_vs_mean_2021_2024"])
    print("selftest", selftest["forecast"], selftest["rmse_train"], selftest["mae_train"])


if __name__ == "__main__":
    main()
