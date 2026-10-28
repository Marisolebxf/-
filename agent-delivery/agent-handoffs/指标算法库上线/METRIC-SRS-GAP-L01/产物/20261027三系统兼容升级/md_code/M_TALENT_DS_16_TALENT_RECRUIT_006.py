#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_TALENT_DS_16_TALENT_RECRUIT_006 —— 文化融合风险评估。

需求：评估国际人才来深后的文化适应/融合风险（宗教、族群、语言、生活习惯、社会网络）。
判定：**完全不支持**。全库对「文化」这一对象的字段覆盖是 0，不是覆盖不足：
  1. 280 张表里，列名含 religio/ethnic/race/belief 的 **0 列**；
  2. 表名含 religio/ethnic/culture/community/assimilat/cross_cultural 的 **0 张**；
  3. 列名含 nationality/visa/passport/residence_permit/migrant 的 **0 列**
     ——连「外籍身份」都无法识别，「跨文化」就失去主语；
  4. `dwd_forg_base_info` 名字像「境外人才」，实为境外**企业**底册（20000 行，
     company_type/incorporation_year/stock_code/registered_capital），`country` 去重数 **0**；
  5. `dwd_scholar.bio_zh` 提到「华裔」2 条、「外籍」1 条、「海外」10 条，占比 <0.06%，
     且无任何适应/融入结果。

因此本脚本不产出风险分数、不产出名单——只落证据与修复路径。
零 SQL：读 `code/_snapshots21/zero_source_probe_20261022.json`（含 source）。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_006_out.json`。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_006"
PROBE = HERE / "_snapshots21" / "zero_source_probe_20261022.json"


def main() -> None:
    p = json.loads(PROBE.read_text(encoding="utf-8"))
    rel = p["columns"]["religion_ethnic"]
    nat = p["columns"]["nationality_visa"]
    bio = p["bio"]
    n_bio = bio["nonempty"]
    hits = bio["keyword_hits"]
    pct = {k: round(100 * v / n_bio, 4) for k, v in hits.items()}

    payload = {
        "metric": METRIC,
        "title": "文化融合风险评估",
        "support_judgment": "完全不支持",
        "support_reason": (
            "宗教/族群字段 0 列、文化/社区类表 0 张、国籍/签证字段 0 列；"
            "`dwd_forg_base_info` 是境外企业底册而非境外人才，country 列去重为 0；"
            "bio 提到华裔/外籍合计 3 条。既无「外籍身份」也無「融合结果」，无法构建风险评分。"
        ),
        "dimensions": [
            {"dim": "宗教 / 族群 / 文化背景", "verdict": "无",
             "evidence": "religio|ethnic|race|belief 命中 0 列；culture/religion/community 表 0 张",
             "needed": "人才主档补国籍、母语、族群/宗教（敏感字段需授权）或问卷量表"},
            {"dim": "国籍 / 签证 / 居留身份", "verdict": "无",
             "evidence": "nationality|visa|passport|residence_permit|migrant 命中 0 列",
             "needed": "接入出入境/外专局居留许可数据，或在人才主档补 nationality"},
            {"dim": "文化适应结果（留存/满意度/冲突）", "verdict": "无",
             "evidence": "无 survey/satisfaction/turnover/conflict 类表；`dwd_scholar` 只有成果与引用",
             "needed": "入湖人才服务问卷、离职原因、团队冲突记录"},
            {"dim": "境外经历代理", "verdict": "弱",
             "evidence": "海外学历 628 人、海外履历 896 人（可作「跨文化暴露」，不是「融合风险」）",
             "needed": "暴露度与风险方向相反：经历越多通常适应越好，不能反推"},
        ],
        "evidence": {
            "religion_ethnic_columns": rel["n_columns"],
            "nationality_visa_columns": nat["n_columns"],
            "culture_religion_tables": p["tables"]["culture_religion"],
            "forg_base_info_rows": p["forg"]["rows"],
            "forg_country_distinct": p["forg"]["country_distinct"],
            "forg_note": p["forg"]["note"],
            "bio_rows": bio["rows"], "bio_nonempty": n_bio,
            "bio_keyword_hits": {k: hits[k] for k in ("华裔", "外籍", "海外", "留学")},
            "bio_keyword_pct": {k: pct[k] for k in ("华裔", "外籍", "海外", "留学")},
            "overseas_edu": 628, "overseas_work": 896,
        },
        "no_score_declaration": (
            "本件不输出风险分数与风险名单。可计算维度为 0；若以「海外经历」代替「融合风险」，"
            "方向相反（经历越多通常适应越好），会得到反向结论，属于误用。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("纯截面判定，且不存在可用时间序列：身份、宗教、融合结果字段均无；"
                            "履历表的 start_time/end_time 只记机构任期，不是适应过程。"),
        "probes": {"sql_count": 0, "probe_sql_total": p.get("sql_count"),
                   "probe_snapshot": "_snapshots21/zero_source_probe_20261022.json",
                   "source": "gkx @ 183.240.141.251:3318"},
        "reused_from": "code/_snapshots21/zero_source_probe_20261022.json（由 code/_probe_zero_source.py 生成）",
    }
    C.write(METRIC, payload)
    print("judgment", payload["support_judgment"])
    print("religion cols", rel["n_columns"], "nationality cols", nat["n_columns"],
          "culture tables", len(p["tables"]["culture_religion"]))
    print("bio 华裔/外籍", hits["华裔"], hits["外籍"])


if __name__ == "__main__":
    main()
