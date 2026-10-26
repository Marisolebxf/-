#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
