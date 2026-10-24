#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DS_16_TALENT_RECRUIT_005 —— 沟通障碍智能检测。

需求：识别国际科技人才在跨语言/跨文化沟通上的障碍，输出可量化、可解释的沟通障碍信号。
判定：**完全不支持**。理由不是「数据少」，而是「检测对象不存在」：
  1. 全库 280 张表没有任何「个人语言能力」字段。13 个 language 列全部是论文/文档/
     政策语种（`dwd_zh_paper.language_classify` 全表只有 1 个取值 1），不是人的能力等级。
  2. 没有访谈、语音、会议、邮件、即时通讯类文本，无法做「沟通行为」层面的检测。
     唯一的大文本是论文摘要（中文 268,315 条），它是书面学术语体，不含沟通障碍标签。
  3. `dwd_scholar.bio_zh` 19,109 条非空，但「提到英语」只有 28 条（0.15%）、
     「提到留学」4 条；且是自述文本、无等级、无证书、无场景，不能变成分数。
  4. `dwd_scholar_talent_flag` 只有 academician 一列，没有语言/国际化标签。

因此本脚本不产出任何「沟通障碍分数」——产出分数就是造数。只落证据计数。
零 SQL：证据读 `code/_snapshots21/zero_source_probe_20261022.json`（由
`code/_probe_zero_source.py` 从 gkx 拉取并落盘，含 source）。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_005_out.json`。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_005"
PROBE = HERE / "_snapshots21" / "zero_source_probe_20261022.json"


def main() -> None:
    p = json.loads(PROBE.read_text(encoding="utf-8"))
    lang = p["columns"]["language_skill"]
    bio = p["bio"]
    n_bio = bio["nonempty"]
    hits = bio["keyword_hits"]
    pct = {k: round(100 * v / n_bio, 4) for k, v in hits.items()}

    payload = {
        "metric": METRIC,
        "title": "沟通障碍智能检测",
        "support_judgment": "完全不支持",
        "support_reason": (
            "全库无个人语言能力字段（13 个 language 列全部指向论文/文档语种），无访谈/语音/"
            "会议/邮件语料，无沟通障碍标签；bio 文本里提到英语的仅 28/19,109（0.15%），"
            "是自述且无等级。检测对象（沟通行为）与标签（障碍程度）双双缺席，任何打分都是造数。"
        ),
        "dimensions": [
            {"dim": "语言能力等级（听说读写）", "verdict": "无",
             "evidence": "language 列 13 个 / 11 表，全部为论文语言、文档语言、政策语种；无 proficiency/TOEFL/IELTS 字段",
             "needed": "人才主档增加语言能力分级字段（CET/TOEFL/IELTS/面试评级），或接入语言测评机构结果"},
            {"dim": "沟通行为语料（访谈/语音/会议/邮件）", "verdict": "无",
             "evidence": "280 表中无 speech/interview/meeting/email/chat 类表；唯一大文本为论文摘要（中文 268,315 条）",
             "needed": "接入面试录音转写、跨文化团队协作日志或问卷量表"},
            {"dim": "沟通障碍标签（结果面）", "verdict": "无",
             "evidence": "无任何 barrier/difficulty/communication_score 类字段或结果表",
             "needed": "设计问卷或专家评分，形成 1—5 级障碍标签"},
            {"dim": "跨文化经历代理", "verdict": "弱",
             "evidence": "海外学历 628 人、海外履历 896 人、国际合著 1,824 人（可作暴露度，不是障碍）",
             "needed": "只能证明「接触过境外」，不能证明「沟通有障碍」"},
        ],
        "evidence": {
            "language_columns_total": lang["n_columns"],
            "language_tables_total": lang["n_tables"],
            "language_columns": lang["items"],
            "bio_rows": bio["rows"], "bio_nonempty": n_bio,
            "bio_keyword_hits": hits, "bio_keyword_pct": pct,
            "zh_abstract_nonempty": 268315,
            "paper_language_distinct": {"1": 100900},
            "talent_flag_columns": ["scholar_id", "academician"],
            "culture_religion_tables": p["tables"]["culture_religion"],
        },
        "no_score_declaration": (
            "本件不输出分数、不输出分档、不输出名单。原因：可计算维度为 0，"
            "若用「海外经历」代替「沟通障碍」，方向相反（有海外经历通常意味着障碍更低），"
            "会得到系统性反向的结论。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("纯截面判定，且不存在可计算的时间序列：语言能力字段与沟通语料均无，"
                            "故无基期。论文摘要覆盖 1980—2026，但与本指标语义无关，不纳入。"),
        "probes": {"sql_count": 0, "probe_sql_total": p.get("sql_count"),
                   "probe_snapshot": "_snapshots21/zero_source_probe_20261022.json",
                   "source": "gkx @ 183.240.141.251:3318"},
        "reused_from": "code/_snapshots21/zero_source_probe_20261022.json（由 code/_probe_zero_source.py 生成）",
    }
    C.write(METRIC, payload)
    print("judgment", payload["support_judgment"])
    print("lang cols", lang["n_columns"], "bio", n_bio, "english hits", hits["英语"], pct["英语"])


if __name__ == "__main__":
    main()
