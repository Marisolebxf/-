#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DS_07_TECH_INNOV_002 · 专利质量评估（20261022 三方库版）

口径（单一）：
  对象 = IPC4 技术领域（一行一个域），五维 = 家族规模 / 权利要求数 / 被引次数 /
  技术宽度 / 法律状态稳定性，域内极值归一后等权合成 0—100。
  本件结论：五维都无法落到 IPC4，故不产出任何领域分；只交付覆盖率证据与样本级画像。

为什么判「完全不支持」（全部可复核，零 SQL，读已落盘探针）：
  1. 五张价值附表各约 2 万行，对 2,939,895 行主表覆盖 0.68%—0.70%；
  2. 附表无 IPC4/申请年字段，按 patent_id 回连主表三条查询各跑满 60 秒被服务端中断（3 次复现）；
  3. 主表 other_Versions 前缀 3,000 行 0 行非空；claims 正文为 mediumtext；
  4. 技术宽度依赖附加分类，面板只采主分类；全表聚合实测 600 秒断连；
  5. 被引表只有 475 件能回连主表（0.0162%）。

运行：python3 code/M_TECH_DS_07_TECH_INNOV_002.py（零 SQL）
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_DS_07_TECH_INNOV_002"
MAIN = 2_939_895


def main():
    tinn = json.load(open(S.SNAP / "probe_tinn21_20261022.json", encoding="utf-8"))
    tail = json.load(open(S.SNAP / "probe_tail21_20261022.json", encoding="utf-8"))
    a26 = json.load(open(S.SNAP / "probe_a26_20261022.json", encoding="utf-8"))
    a25 = json.load(open(S.SNAP / "a25_facts.json", encoding="utf-8"))

    fam = a25["family"][0]
    cited = a25["cited_rows"][0]
    claim = tinn["claim_cover"]["rows"][0]
    legal = tail["legal_agg"]["rows"][0]
    status = tail["legal_status"]["rows"]
    ov = a26["other_versions_prefix"]["rows"][0]
    joins = {k: tinn[k] for k in ("family_join", "cited_by_ipc4", "legal_by_ipc4")}
    prior = json.load(open(S.CODE / "M_INNOV_TINN_PATENT_QUALITY_out.json", encoding="utf-8"))

    granted = next((int(n) for s, n in status if s == "授权"), 0)
    terminated = sum(int(n) for s, n in status if s and ("终止" in s or "放弃" in s or "撤回" in s))
    stable_est = max(0, granted - terminated)

    cov = {
        "family": round(100 * fam["n"] / MAIN, 4),
        "claim": round(100 * claim[0] / MAIN, 4),
        "cited": round(100 * cited["n"] / MAIN, 4),
        "legal": round(100 * legal[0] / MAIN, 4),
        "cited_joinable": round(100 * prior["probe"]["cited_joinable_to_main"] / MAIN, 4),
    }

    payload = {
        "metric_id": MID,
        "metric_name": "专利质量评估",
        "caliber": {
            "对象": "IPC4 技术领域，一行一个域，0—100 分",
            "五维": "家族规模 / 权利要求数 / 被引次数 / 技术宽度 / 法律状态稳定性",
            "本件产出": "不产出领域分；只产出覆盖率与样本级画像（证据）",
        },
        "base_years_used": [],
        "base_years_missing": [2021, 2022, 2023, 2024, 2025, 2026],
        "base_years_note": "价值附表无申请年字段且无法回连主表，任何年度分母都不成立；"
                           "本件是截面覆盖率核验，不设基期。",
        "sql_count": 0,
        "probe": {
            "patent_main_rows": MAIN,
            "family": {"rows": fam["n"], "distinct_pn": fam["pn_uniq"]},
            "claim": {"rows": claim[0], "distinct_patent_id": claim[1], "distinct_pn": claim[2],
                      "lang": [[r[0], int(r[1])] for r in tinn["claim_lang"]["rows"]]},
            "cited": {"rows": int(cited["n"]), "positive_rows": int(cited["pos"]),
                      "positive_share": round(int(cited["pos"]) / int(cited["n"]), 4),
                      "sum": int(round(float(cited["av"]) * int(cited["n"]))), "max": int(cited["mx"]),
                      "avg": float(cited["av"])},
            "legal": {"rows": legal[0], "distinct_pn": legal[1], "distinct_patent_id": legal[2],
                      "legal_events_filled": int(legal[3]), "status_filled": int(legal[4]),
                      "expiration_filled": int(legal[5])},
            "other_versions_prefix": {"sampled_rows": int(ov[0]), "nonempty": int(ov[1] or 0)},
            "legal_status_dist": [[s, int(n)] for s, n in status],
            "coverage_pct_vs_main": cov,
            "return_join_timeouts": {
                k: {"ok": v.get("ok"), "sec": v.get("sec"),
                    "error": (v.get("error") or "")[:90],
                    "sql": (v.get("sql") or "")[:180]}
                for k, v in joins.items()
            },
            "return_join_timeout_count": sum(1 for v in joins.values() if not v.get("ok")),
            "cited_joinable_to_main": prior["probe"]["cited_joinable_to_main"],
        },
        "sample_profile": {
            "note": "以下是把 2 万行价值附表当「样本」看的描述统计，不是 IPC4 领域分，"
                    "也不得用于排名或对外发布",
            "family_members_per_pn": round(fam["n"] / fam["pn_uniq"], 4),
            "claim_rows_per_pn": round(claim[0] / claim[2], 4),
            "cited_per_row": float(cited["av"]),
            "cited_positive_share": round(int(cited["pos"]) / int(cited["n"]), 4),
            "legal_granted_share": round(granted / legal[0], 4),
            "legal_stable_est_share": round(stable_est / legal[0], 4),
            "width": "不可算（附加分类未入缓存，主分类每件只有 1 个 IPC4）",
        },
        "dimension_status": {
            "D1_家族规模": {"rows": fam["n"], "coverage_pct": cov["family"], "status": "不可用（无域键 + 主表 other_Versions 全空）"},
            "D2_权利要求数": {"rows": claim[0], "coverage_pct": cov["claim"], "status": "不可用（正文 mediumtext，无域键）"},
            "D3_被引次数": {"rows": int(cited["n"]), "coverage_pct": cov["cited"], "status": "不可用（可回连主表仅 475 件）"},
            "D4_技术宽度": {"rows": None, "coverage_pct": None, "status": "不可用（附加分类未入缓存）"},
            "D5_法律状态稳定性": {"rows": legal[0], "coverage_pct": cov["legal"], "status": "不可用（无域键，回连超时）"},
        },
        "gaps": [
            "五张价值附表各约 2 万行，对 294 万行主表覆盖 0.68%—0.70%",
            "附表无 IPC4 / 申请年字段，按 patent_id 回连主表三条查询各 60 秒超时（3 次复现）",
            "主表 other_Versions 前缀 3,000 行 0 行非空",
            "dwd_patent_claim.original_text 为 mediumtext，全量取文本 60 秒超时",
            "dwd_patent_cited 只有 475 件可回连主表（0.0162%）",
            "技术宽度依赖 further_classification_ipcr，主表面板未采该列；全表聚合 600 秒断连",
        ],
        "repair_requirements": [
            "五张附表扩到全量，并在表内直接冗余 ipc4 / apdt_year，避免回连主表",
            "或给 dwd_patent 的 patent_id / pn 建可用索引，允许按主键分块聚合",
            "补 dwd_patent.other_Versions（同族）与 further_classification_ipcr（附加分类）",
            "权利要求项数改为入库时预计算的整数列（claim_nums），不要每次解析 mediumtext",
        ],
        "source": {
            "probe": "code/_snapshots21/probe_tinn21_20261022.json、probe_tail21_20261022.json、probe_a26_20261022.json、a25_facts.json",
            "prior": "code/M_INNOV_TINN_PATENT_QUALITY_out.json（同一五维口径的前批结论，可交叉复核）",
        },
        "support_judgment": {
            "data_support_level": "完全不支持",
            "criteria": {
                "D1_家族规模": False,
                "D2_权利要求数": False,
                "D3_被引次数": False,
                "D4_技术宽度": False,
                "D5_法律状态稳定性": False,
                "domain_level_join": False,
            },
            "note": "五维没有任何一维能在 IPC4 粒度闭环；样本 0.68% 且无域键，"
                    "不是「分低」，是「算不出」，故不产出任何领域分",
        },
    }
    S.write_out(MID, payload)

    print(json.dumps({"coverage": cov, "timeouts": payload["probe"]["return_join_timeout_count"],
                      "sample": payload["sample_profile"]}, ensure_ascii=False, indent=1))
    print("legal status top3", status[:3])


if __name__ == "__main__":
    main()
