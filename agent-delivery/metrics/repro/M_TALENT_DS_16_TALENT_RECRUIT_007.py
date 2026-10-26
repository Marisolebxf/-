#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_DS_16_TALENT_RECRUIT_007 —— 国际流动壁垒分析。

需求：分析国际科技人才流动的壁垒（签证/居留、学历认证、语言、家庭、学术网络），
      给出可量化的流动壁垒画像。
判定：**部分支持**。
  可算（3 维，全部来自履历/论文的境外信号）：
    O1 海外学历（edu_for>0）628 人；
    O2 海外履历（work_for>0）896 人；
    O3 国际合著（nfor>0）1,824 人，占可锚定学者 13,955 的 13.07%。
  不可算（4 维，全库零字段）：
    签证/居留、国籍、家庭随迁、学历认证结果——`nationality|visa|passport|residence_permit|
    migrant` 命中 0 列（见 `_probe_zero_source.py`）。
  因此本件输出的是「国际流动经历强度」指数（越高=流动能力越强、壁垒越低），
  不是壁垒本身；两者方向相反，正文必须成对读。

口径：
  流动强度 = 100 × (0.35·O1 + 0.35·O2 + 0.30·国际合著占比)，只对 2,446 名
  「至少有一个境外信号」的学者打分；无任何境外信号的 17,974 人记 None（不补 0，
  因为「没查到境外经历」≠「没有境外经历」，子表本身只覆盖 1,795/1,792 人）。
  分档阈值取这 2,446 人内部的 p90/p70/p40。

零 SQL：读 `code/_snapshots21/talent22_panel_20261022.json`。
产物：`code/M_TALENT_DS_16_TALENT_RECRUIT_007_out.json`。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import _talent22_common as C  # noqa: E402

METRIC = "M_TALENT_DS_16_TALENT_RECRUIT_007"


def main() -> None:
    rs = C.rows()
    pool = []
    for r in rs:
        o1 = 1 if r["edu_for"] > 0 else 0
        o2 = 1 if r["work_for"] > 0 else 0
        o3 = 1 if r["nfor"] > 0 else 0
        if not (o1 or o2 or o3):
            continue
        share = (r["nfor"] / r["np"]) if r["np"] > 0 else None
        parts = [(0.35, 100 * o1), (0.35, 100 * o2)]
        if share is not None:
            parts.append((0.30, 100 * share))
        w = sum(p[0] for p in parts)
        pool.append({"r": r, "o1": o1, "o2": o2, "o3": o3,
                     "intl_share": share,
                     "score": round(sum(p[0] * p[1] for p in parts) / w, 4),
                     "dims": len(parts)})

    scores = [x["score"] for x in pool]
    cs = C.cuts(scores)
    tiers = Counter(C.tier(x["score"], cs) for x in pool)
    both = sum(1 for x in pool if x["o1"] and x["o2"])
    sz = [x for x in pool if C.is_sz(x["r"]) or x["r"]["work_sz"] or x["r"]["edu_sz"]]
    ret = [x for x in pool if x["o1"] or x["o2"]]
    ret_keep = [x for x in ret if x["o3"]]
    top = C.top([x["r"] for x in pool], [x["score"] for x in pool], 30,
                extra=lambda j: {"ov_edu": pool[j]["o1"], "ov_work": pool[j]["o2"],
                                 "intl_papers": pool[j]["r"]["nfor"],
                                 "intl_share": pool[j]["intl_share"],
                                 "np": pool[j]["r"]["np"], "dims": pool[j]["dims"]})

    payload = {
        "metric": METRIC,
        "title": "国际流动壁垒分析",
        "support_judgment": "部分支持",
        "support_reason": (
            "海外学历 628 人、海外履历 896 人、国际合著 1,824 人三维可算，能刻画「流动经历强度」；"
            "但壁垒本身——签证/居留、国籍、家庭随迁、学历认证——全库 0 字段，"
            "只能给出壁垒的逆向代理（经历越多=壁垒越低），无法直接测「被什么挡住」。"
        ),
        "method": {
            "pool": f"20,420 名有姓名学者中至少有一个境外信号的 {len(pool):,} 人",
            "formula": "100 × (0.35·海外学历 + 0.35·海外履历 + 0.30·国际合著占比)，缺失维归一",
            "intl_share": "nfor / np，nfor = 作者机构含境外机构的锚定论文数",
            "no_zero_fill": "三项全无者不评分（None），不按 0 计入分母",
            "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
            "direction_warning": "分数越高=流动经历越强=壁垒越低；不可反读为「壁垒越高」",
        },
        "coverage": {
            "scholars": len(rs), "scored": len(pool), "not_scored": len(rs) - len(pool),
            "overseas_edu": sum(1 for x in pool if x["o1"]),
            "overseas_work": sum(1 for x in pool if x["o2"]),
            "both_edu_work": both,
            "intl_coauthor": sum(1 for x in pool if x["o3"]),
            "anchored": 13955, "intl_coauthor_pct_of_anchored": round(100 * 1824 / 13955, 2),
            "returnees_with_intl_paper": len(ret_keep),
            "returnees_with_intl_paper_pct": round(100 * len(ret_keep) / len(ret), 2) if ret else 0,
            "sz_in_pool": len(sz),
        },
        "dist": {"score": C.dist(scores),
                 "intl_share": C.dist([x["intl_share"] for x in pool
                                       if x["intl_share"] is not None])},
        "thresholds": {"p90": cs[0], "p70": cs[1], "p40": cs[2]},
        "tiers": {t: tiers.get(t, 0) for t in "ABCD"},
        "top30": top,
        "zero_dims": [
            {"dim": "签证 / 居留许可", "evidence": "nationality|visa|passport|residence_permit 命中 0 列",
             "needed": "接入外专局/出入境居留许可数据"},
            {"dim": "国籍", "evidence": "同上 0 列；`dwd_forg_base_info` 是境外企业底册，country 去重 0",
             "needed": "人才主档补 nationality"},
            {"dim": "家庭随迁", "evidence": "无 spouse/child/family 类字段",
             "needed": "人才服务问卷"},
            {"dim": "学历认证结果", "evidence": "只有 edu 表机构/学位文本，无认证状态字段",
             "needed": "接入教育部留服认证结果"},
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面口径：海外学历/履历为全时段记录，国际合著为全时段累计，"
                            "无年度窗口，故无基期。履历 start_time 为 varchar(7)，"
                            "本件不按年切分、不做回流年份分布。"),
        "probes": {"sql_count": 0, "patent_sql": 0,
                   "source": "gkx @ 183.240.141.251:3318（快照派生）"},
        "reused_from": "code/_snapshots21/talent22_panel_20261022.json（由 code/_build_talent22_panel.py 生成）",
    }
    C.write(METRIC, payload)
    print("coverage", payload["coverage"])
    print("dist", payload["dist"]["score"], "cuts", cs)
    print("top5", [(x["name"], x["org"], x["score"]) for x in top[:5]])


if __name__ == "__main__":
    main()
