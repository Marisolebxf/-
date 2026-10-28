#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_SUPPLY_CHAIN_RISK —— 断链风险等级（W13-E4）

口径正本（gkx-orchestration/.../calc-logic/ENT/M_ENT_SUPPLY_CHAIN_RISK.md）：
  韧性指数 = Σ_{j=1..4} w_j × 指标得分_j，再按 70/40 分档映射低/中/高风险。
  四个二级维度及本库可得性：
    D1 应收账款与收入比的自然对数（逆向）—— 现库无应收账款字段
    D2 前五大客户中非新出现客户数 ÷ 5（正向）—— 现库无客户关系表
    D3 库存周转率（正向）—— 现库无存货余额字段
    D4 经济绩效敏感性指数（逆向）—— gkx.dwd_org_stock_finance_info 有营收/利润/期次

本件判「部分支持」：D1—D3 三个维度无承载，D4 可真算。等级（低/中/高）因为四维缺三、
权重与归一化总体都无法成立，本件不出等级，只交付 D4 单维得分与其不可比性说明。

运行：cd code && python3 M_ENT_SUPPLY_CHAIN_RISK.py
产物：code/M_ENT_SUPPLY_CHAIN_RISK_out.json
"""
from __future__ import annotations

import json
import os
import statistics as st
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_ENT_SUPPLY_CHAIN_RISK_out.json")

MIN_PERIODS = 4          # 少于 4 期的企业不参与波动性计算（2 期也能算，但波动无意义）
WINDOW = 8               # 取最近 8 期（季度口径 ≈ 2 年）


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def scan_roots(roots):
    """在列字典里搜维度所需的词根，返回命中列与表数。"""
    cols = load("gkx_columns_20261023.json")["tables"]
    out = {}
    for r in roots:
        hits = [(t, c) for t, v in cols.items() for c, _ in v["columns"]
                if r in c.lower()]
        out[r] = {"n_columns": len(hits), "n_tables": len({t for t, _ in hits}),
                  "columns": [f"{t}.{c}" for t, c in hits[:6]]}
    return out


def fetch_fin():
    """拉 dwd_org_stock_finance_info 的窄投影（40,239 行，可直接进内存）。"""
    from _gkxdb import gkx
    cur = gkx()
    cur.execute("SET SESSION max_execution_time=180000")
    cur.execute("SELECT org_id, name_cn, stock_code, occur_period, "
                "operating_revenue, total_profit "
                "FROM gkx.dwd_org_stock_finance_info "
                "WHERE occur_period IS NOT NULL")
    rows = []
    for org_id, name, code, period, rev, prof in cur.fetchall():
        rows.append({"org_id": org_id, "name": name, "stock_code": code,
                     "period": str(period), "revenue": rev, "profit": prof})
    return rows


def cv(values):
    """变异系数：标准差 / 平均绝对值。均值为 0 或样本不足返回 None。"""
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None
    mean_abs = sum(abs(v) for v in vals) / len(vals)
    if mean_abs <= 0:
        return None
    return st.pstdev(vals) / mean_abs


def main():
    fam = load("supply_family_20261023.json")
    vocab = fam["vocab_scan"]
    rows = fetch_fin()

    by_org = {}
    for r in rows:
        by_org.setdefault(r["org_id"], []).append(r)

    per_org = []
    for org_id, rs in by_org.items():
        rs.sort(key=lambda x: x["period"])
        tail = rs[-WINDOW:]
        revs = [x["revenue"] for x in tail]
        profs = [x["profit"] for x in tail]
        n_rev = sum(1 for v in revs if v is not None)
        n_prof = sum(1 for v in profs if v is not None)
        if n_rev < MIN_PERIODS and n_prof < MIN_PERIODS:
            continue
        cv_rev = cv(revs) if n_rev >= MIN_PERIODS else None
        cv_prof = cv(profs) if n_prof >= MIN_PERIODS else None
        parts = [x for x in (cv_rev, cv_prof) if x is not None]
        if not parts:
            continue
        vol = sum(parts) / len(parts)      # 经济绩效敏感性指数（未归一化）
        per_org.append({
            "org_id": org_id,
            "name": tail[-1]["name"],
            "stock_code": tail[-1]["stock_code"],
            "n_periods_used": len(tail),
            "n_revenue": n_rev,
            "n_profit": n_prof,
            "cv_revenue": round(cv_rev, 6) if cv_rev is not None else None,
            "cv_profit": round(cv_prof, 6) if cv_prof is not None else None,
            "volatility_raw": vol,
            "last_period": tail[-1]["period"],
            "last_revenue": tail[-1]["revenue"],
            "last_profit": tail[-1]["profit"],
        })

    # 极值归一化：D4 是逆向指标（波动越大越差）→ score = (max - x)/(max - min) × 100
    vals = [p["volatility_raw"] for p in per_org]
    vmin, vmax = (min(vals), max(vals)) if vals else (0.0, 0.0)
    for p in per_org:
        if vmax > vmin:
            p["score_d4"] = round((vmax - p["volatility_raw"]) / (vmax - vmin) * 100, 2)
        else:
            p["score_d4"] = None

    per_org.sort(key=lambda p: p["volatility_raw"], reverse=True)
    scored = [p for p in per_org if p["score_d4"] is not None]
    scores = [p["score_d4"] for p in scored]
    mean_score = round(sum(scores) / len(scores), 2) if scores else None

    def band(lo, hi):
        return sum(1 for s in scores if lo <= s <= hi)

    out = {
        "metric_id": "M_ENT_SUPPLY_CHAIN_RISK",
        "metric_name": "断链风险等级",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_dimension_missing",
        "judgment_reason": (
            "四维韧性指数中 D1 应收账款、D2 前五大客户、D3 存货周转三个维度在 gkx 与开发库均无字段/无表；"
            "仅 D4 经济绩效敏感性（营收/利润波动）可由 gkx.dwd_org_stock_finance_info 真算，"
            "覆盖 972 家上市公司。等级需要四维加权 + 归一化总体，缺三维不可出，故判部分支持、只交付 D4 单维得分。"),
        "formula_calc_logic": (
            "score_j = (x_j - min)/(max - min)*100（逆向指标取反）；"
            "resilience_i = Σ w_j*score_j（j=1..4）；"
            "level_i = 低风险[70,100] / 中风险[40,69] / 高风险[0,39]"),
        "dimension_availability": [
            {"code": "D1", "dim": "供应链抵抗力 / 资金关系",
             "metric": "应收账款与收入比的自然对数", "direction": "逆向",
             "required": "应收账款余额", "found": 0,
             "evidence": "gkx 全库搜 receivable / 应收：receiv 仅命中 dwd_safety.receive_date"
                         "（领用日期）2 列，应收 0 列；dwd_org_stock_finance_info 27 列无应收科目",
             "status": "不可得"},
            {"code": "D2", "dim": "供应链抵抗力 / 供需稳固",
             "metric": "前五大客户中非新出现客户数 ÷ 5", "direction": "正向",
             "required": "客户关系表 + 客户新增标记", "found": 0,
             "evidence": "gkx 全库搜 customer / 客户 / 前五大 → 0 列；无客户关系边表",
             "status": "不可得"},
            {"code": "D3", "dim": "供应链恢复力 / 产品流动",
             "metric": "库存周转率", "direction": "正向",
             "required": "存货余额 / 营业成本", "found": 0,
             "evidence": "gkx 全库搜 inventory / 存货 / 库存 → 0 列；营业成本仅在"
                         "dwd_main_business_composition_area.core_biz_cost（主营构成）有，"
                         "缺存货余额，周转率仍不可算",
             "status": "不可得"},
            {"code": "D4", "dim": "供应链恢复力 / 绩效波动",
             "metric": "经济绩效敏感性指数", "direction": "逆向",
             "required": "营业收入 + 利润总额 + 期次", "found": 3,
             "evidence": "dwd_org_stock_finance_info：40,239 行 / 972 家 / "
                         "occur_period 198912—202603；operating_revenue 非空 39,826、"
                         "total_profit 非空 40,144",
             "status": "可算（本件已算）"},
        ],
        "vocab_evidence": {k: {"n_columns": vocab[k]["n_columns"],
                               "n_tables": vocab[k]["n_tables"]}
                           for k in ("customer", "inventory", "存货", "库存", "upstream",
                                     "downstream", "supply", "supplier")},
        "vocab_evidence_extra": scan_roots(["receiv", "应收", "cost", "营业成本"]),
        "d4": {
            "definition": (
                "volatility = mean(CV_revenue, CV_profit)，CV = 总体标准差 / 平均绝对值，"
                f"取最近 {WINDOW} 期、要求至少 {MIN_PERIODS} 期；"
                "score_d4 = (max - volatility)/(max - min) × 100（逆向）"),
            "population": {"rows": len(rows), "orgs_all": len(by_org),
                           "orgs_scored": len(scored)},
            "volatility_range": {"min": round(vmin, 6), "max": round(vmax, 6)},
            "score_stats": {"mean": mean_score,
                            "n_low_risk_band_70_100": band(70, 100),
                            "n_mid_risk_band_40_69": band(40, 69),
                            "n_high_risk_band_0_39": band(0, 39)},
            "top10_most_volatile": [
                {"name": p["name"], "stock_code": p["stock_code"],
                 "org_id": p["org_id"], "n_periods_used": p["n_periods_used"],
                 "cv_revenue": p["cv_revenue"], "cv_profit": p["cv_profit"],
                 "volatility_raw": round(p["volatility_raw"], 4),
                 "score_d4": p["score_d4"]} for p in per_org[:10]],
            "bottom10_least_volatile": [
                {"name": p["name"], "stock_code": p["stock_code"],
                 "org_id": p["org_id"], "n_periods_used": p["n_periods_used"],
                 "cv_revenue": p["cv_revenue"], "cv_profit": p["cv_profit"],
                 "volatility_raw": round(p["volatility_raw"], 4),
                 "score_d4": p["score_d4"]} for p in per_org[-10:]],
            "not_comparable_note": (
                "D4 的归一化总体是 972 家上市公司，而产业链上还有约 170 万家非上市链上企业；"
                "把 D4 得分当作『断链风险』与全量企业横比会系统性偏高或偏低。"),
        },
        "level_output": {
            "produced": False,
            "why": ("等级 = 四维加权后的韧性指数分档。D1—D3 无字段，权重（等权 25% 或熵值法）"
                    "无法在四维上成立；若只用 D4×1.0 代替，等价于把『财务波动』改名为『断链风险』，"
                    "属改名换义，故不产出。"),
            "what_would_unblock": [
                "财务报表补应收账款、存货、营业成本三个科目（可从年报附注或三方财务库接入）",
                "客户关系边表（企业→前五大客户，含客户首次出现期次）",
                "供应链边表（source_org_id, target_org_id, relation_type），用于把关联企业风险信号挂到链上",
            ],
        },
        "risk_signal_side": {
            "tables": fam["risk_signals"],
            "note": ("calc-logic 还要求统计『供应链关联企业中经营异常/违法/处罚的占比』，"
                     "这一步依赖供应链边表；边表缺失，风险信号只能按企业自身统计，不能按链上关联企业统计。"),
        },
        "base_years_used": ["1989—2026（occur_period 实际覆盖，D4 取各企业最近 8 期）"],
        "base_years_missing": ["2026 年后续季度（库内止于 202603）"],
        "base_years_note": (
            "D4 不用固定自然年窗口，而是每家取最近 8 个有值期次（季度），避免早年稀疏年份被当成 0；"
            "occur_period 为 YYYYMM 文本，198912 起有值，202603 为库内最新期。"
            "没有把缺失年份按 0 摊入分母：期次不足 4 期的企业直接不进样本。"),
        "sources": {
            "db": "gkx @ 183.240.141.251:3318",
            "tables": ["gkx.dwd_org_stock_finance_info"],
            "snapshots": ["code/_snapshots21/supply_family_20261023.json",
                          "code/_snapshots21/gkx_columns_20261023.json"],
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"judgment": out["support_judgment"],
                      "orgs_scored": len(scored),
                      "mean_score": mean_score,
                      "bands": out["d4"]["score_stats"]}, ensure_ascii=False))
    print("top3", [(p["name"], round(p["volatility_raw"], 3), p["score_d4"])
                   for p in per_org[:3]])
    print("saved", OUT)


if __name__ == "__main__":
    main()
