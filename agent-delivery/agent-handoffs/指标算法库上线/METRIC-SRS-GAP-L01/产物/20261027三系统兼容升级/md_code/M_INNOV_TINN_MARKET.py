#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_TINN_MARKET · 技术市场潜力（判：完全不支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_TINN_MARKET.md`（V1.5-20260901）
五维：转让 / 许可 / 诉讼 / 质押 / 开放许可；一行一个 IPC4，0—100，本批领域内极值归一。

为什么判完全不支持
------------------
1. 转让：`dwd_patent_transfer` 22,809 行（覆盖 0.78%），只有 `pn`，**没有 patent_id、没有 IPC**；
   主表 pn 无索引，按号回连即 294 万行扫描（DATA_FACTS §3.6）。22,809 行里 20,000 个不同 pn，
   无法归属到任何 IPC4。
2. 许可/质押/开放许可/诉讼：只能从 `dwd_patent_legal.legal_events` 解析，20,000 行（0.68%）；
   全局 LIKE 计数为 许可 56、开放许可 6、质押 104、诉讼或无效 **0**——诉讼维整列为 0，
   许可维 0.28%、质押 0.52%，即使不拆 IPC4 也已退化。
3. `dwd_market` 15 行、所有度量列（market_share / measure_code / time_period / obs_status）
   全为 NULL，且只有国家代码，没有任何技术领域字段，不能作为市场维兜底。
4. 三条按 IPC4 归属的回连查询（family/cited/legal）各跑满 60 秒被中断，复现 3 次。

运行：python3 code/M_INNOV_TINN_MARKET.py（零 SQL）
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402

MID = "M_INNOV_TINN_MARKET"
MAIN = 2_939_895


def main() -> None:
    pr = T.tail()
    tp = T.tinn()
    legal = T.rows_of(pr, "legal_agg")[0]
    ev = T.rows_of(pr, "legal_event_kw")[0]
    tr = T.rows_of(pr, "transfer_agg")[0]
    tr_year = T.rows_of(pr, "transfer_year")
    market = T.rows_of(pr, "market_rows")
    joins = {k: tp.get(k) for k in ("family_join", "cited_by_ipc4", "legal_by_ipc4")}

    null_cols = {}
    if market:
        cols = pr["market_rows"]["cols"]
        for i, c in enumerate(cols):
            if c in ("market_name", "market_share", "pharmaceutical_category", "measure_code",
                     "unit_measure", "time_period", "obs_status"):
                null_cols[c] = sum(1 for r in market if r[i] not in (None, "", 0))

    res = {
        "metric_id": MID,
        "metric_name": "技术市场潜力",
        "support_judgment": "完全不支持",
        "object": "技术领域（IPC 主分类前 4 位）",
        "verdict_reason": (
            "五维里四维只能来自 20,000 行（0.68%）的 legal_events，且诉讼命中 0 条、开放许可 6 条、"
            "许可 56 条；转让维 22,809 行只有 pn、无 patent_id 与 IPC，主表 pn 无索引，归属不到 IPC4；"
            "dwd_market 15 行全空。五维均无法在 IPC4 粒度闭环，故不产出任何领域分"),
        "data_source": "gkx.dwd_patent_transfer / dwd_patent_legal / dwd_market（均不足以建域级结果）",
        "sql_count": 0,
        "sql_note": "本脚本零 SQL；探针阶段 legal/transfer/market 三表各查 1 次，回连主表 3 次超时",
        "probe": {
            "patent_main_rows": MAIN,
            "transfer_rows": int(tr[0]),
            "transfer_distinct_pn": int(tr[1]),
            "transfer_date_parseable": int(tr[2]),
            "transfer_coverage_pct": round(100 * int(tr[0]) / MAIN, 4),
            "transfer_has_patent_id": False,
            "transfer_has_ipc": False,
            "legal_rows": int(legal[0]),
            "legal_coverage_pct": round(100 * int(legal[0]) / MAIN, 4),
            "legal_license_hits": int(ev[0]),
            "legal_open_license_hits": int(ev[2]),
            "legal_pledge_hits": int(ev[3]),
            "legal_litigation_hits": int(ev[5]),
            "market_rows": len(market),
            "market_nonnull_by_col": null_cols,
            "return_join_timeouts": {k: (v or {}).get("ok") for k, v in joins.items()},
            "return_join_timeout_count": sum(1 for v in joins.values() if v and not v.get("ok")),
        },
        "dimension_status": {
            "D1_转让": {
                "formula": "转移专利数 / 专利数",
                "rows": int(tr[0]),
                "coverage_pct": round(100 * int(tr[0]) / MAIN, 4),
                "status": "不可用：只有 pn 与生效日；无 patent_id / IPC4，主表 pn 无索引，无法归属领域",
            },
            "D2_许可": {
                "formula": "legal_events 含「许可」且不含「开放许可」/ 专利数",
                "rows": int(legal[0]),
                "hits": int(ev[0]),
                "status": "退化：20,000 行里仅 56 条命中（0.28%），且无法拆到 IPC4",
            },
            "D3_诉讼": {
                "formula": "legal_events 含「诉讼」「无效宣告」/ 专利数",
                "rows": int(legal[0]),
                "hits": int(ev[5]),
                "status": "整列为 0：全表 0 条命中，该维在任何领域都恒等于 0，不构成区分度",
            },
            "D4_质押": {
                "formula": "legal_events 含「质押」/ 专利数",
                "rows": int(legal[0]),
                "hits": int(ev[3]),
                "status": "退化：104 条命中（0.52%），无法拆到 IPC4",
            },
            "D5_开放许可": {
                "formula": "legal_events 含「开放许可」/ 专利数",
                "rows": int(legal[0]),
                "hits": int(ev[2]),
                "status": "退化：6 条命中（0.03%），无法拆到 IPC4",
            },
        },
        "transfer_year": {str(r[0]): int(r[1]) for r in tr_year},
        "market_table_dump": [
            {"id": r[1], "market_name": r[2], "market_share": r[3], "measure_code": r[5],
             "time_period": r[7], "obs_status": r[8]} for r in market[:15]
        ],
        "base_years_used": [],
        "base_years_missing": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_year_block": T.base_year_block(
            [], [2021, 2022, 2023, 2024, 2025, 2026],
            "转让表有生效年（2021—2026 六档），但无法按 IPC4 归属；其他四维无年度字段，"
            "故不构造任何年度分母"),
        "gaps": [
            "转让表无 patent_id / IPC，主表 pn 无索引，领域归属断路",
            "legal_events 仅 20,000 行（0.68%），诉讼命中 0、开放许可 6、许可 56、质押 104",
            "dwd_market 15 行、度量列全空，且无技术领域字段",
            "三条 IPC4 回连查询各 60 秒超时（family/cited/legal），复现 3 次",
        ],
        "repair_requirements": [
            "dwd_patent_transfer 增加 patent_id + ipc4 + apdt_year 三列，或给主表 pn 建索引并允许分块",
            "dwd_patent_legal 扩到全量并冗余 ipc4 / apdt_year，并把四类事件预拆成布尔列",
            "dwd_market 补技术领域键（IPC4 或产业链码）与度量值，当前 15 行全空不足以兜底",
        ],
    }
    T.write_out(MID, res)
    print(json.dumps(res["probe"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
