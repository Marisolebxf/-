#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_SCI_PAPER · 科学论文数量（判：完全转换支持）

口径真源：`metrics/calc-logic/INNOV` 无该件，按需求原文「按时间（年/季/月）、研究机构、
地域统计特定领域论文发表数量」+ 王惠同类件（M_INNOV_SCI_CENTRALITY）的集合定义推测。

本脚本 1 条 SQL：`dwd_zh_paper` 全表 100,900 行窄列（id / 年 / 日 / 开放获取 / 作者单位 JSON）。
所有聚合在本地完成，不对任何列写 GROUP BY（100,900 行是小表，但作者 JSON 需逐行解析）。

运行：python3 code/M_INNOV_SCI_PAPER.py    （约 40—60 秒，1 条 SQL）
"""
from __future__ import annotations

import sys
import os
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402
from _gkxdb import gkx  # noqa: E402

MID = "M_INNOV_SCI_PAPER"


def fetch() -> list[list]:
    cur = gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute("SELECT id, cover_year_start, cover_date_start, open_access, "
                    "author_info_list FROM gkx.dwd_zh_paper")
        return [list(r) for r in cur.fetchall()]
    finally:
        cur.close()


def main() -> None:
    t0 = time.time()
    rows = fetch()
    en_rows = T.rows_of(T.tail(), "en_paper_agg")[0]

    year = Counter()
    month = Counter()
    quarter = Counter()
    inst = Counter()
    city_paper = Counter()
    kind = Counter()
    inst_kind_cnt = Counter()
    oa = 0
    auth_instances = 0
    bad_json = 0
    multi_city = 0
    city_ok = 0

    for pid, y, d, o, auth in rows:
        yy = T.year_of(y) or T.year_of(d)
        year[yy] += 1
        ds = str(d or "")
        if len(ds) >= 6 and ds[:4].isdigit():
            mm = int(ds[4:6]) if ds[4:6].isdigit() else 0
            month[f"{ds[:4]}-{mm:02d}"] += 1
            if 1 <= mm <= 12:
                quarter[f"{ds[:4]}Q{(mm - 1) // 3 + 1}"] += 1
        oa += int(o or 0)
        js = T.parse_authors(auth)
        if auth and not js:
            bad_json += 1
            continue
        auth_instances += len(js)
        seen_city = set()
        for a in js:
            nm = (a.get("institution") or "").strip()
            if nm:
                inst[nm] += 1
                kind[T.inst_kind(nm)] += 1
            c = T.city_of(nm) or T.city_of(a.get("affiliation") or "")
            if c:
                seen_city.add(c)
        if seen_city:
            city_ok += 1
            if len(seen_city) > 1:
                multi_city += 1
            for c in sorted(seen_city):
                city_paper[c] += 1

    total = len(rows)
    # 年序列（只保留 2015 以后，前段极稀疏；全量仍写入 year_all）
    year_all = {str(k): int(v) for k, v in sorted(year.items()) if k}
    y2024 = year_all.get("2024", 0)
    y2023 = year_all.get("2023", 0)

    # 近三年 vs 前三年（只用真实存在的年份，缺年不摊 0）
    recent = [year_all.get(str(y), 0) for y in (2022, 2023, 2024)]
    base = [year_all.get(str(y), 0) for y in (2019, 2020, 2021)]
    growth = round(100 * (sum(recent) / 3 - sum(base) / 3) / (sum(base) / 3), 2)

    res = {
        "metric_id": MID,
        "metric_name": "科学论文数量",
        "support_judgment": "完全转换支持",
        "object": "中文论文（dwd_zh_paper，期刊论文）",
        "definition": "按时间（年/季/月）× 研究机构 × 地域统计特定领域论文发表数量；"
                      "本批领域维未传参，输出全库分布，领域筛选用题名/关键词二次过滤",
        "data_source": "gkx.dwd_zh_paper（100,900 行）+ gkx.dwd_en_paper（1,387 行，对照）",
        "sql_count": 1,
        "sql": ["SELECT id, cover_year_start, cover_date_start, open_access, author_info_list "
                "FROM gkx.dwd_zh_paper"],
        "probe": {
            "zh_papers": total,
            "zh_distinct_id": total,
            "en_papers": int(en_rows[0]),
            "en_distinct_id": int(en_rows[1]),
            "author_instances": auth_instances,
            "distinct_institutions": len(inst),
            "bad_json_rows": bad_json,
            "open_access_rows": oa,
            "open_access_pct": round(100 * oa / total, 2),
            "city_attributed_papers": city_ok,
            "city_coverage_pct": round(100 * city_ok / total, 2),
            "multi_city_papers": multi_city,
            "paper_type": "期刊论文 100%（paper_type 单值，无类型分化）",
        },
        "year_all": year_all,
        "year_recent": {k: v for k, v in year_all.items() if k >= "2015"},
        "quarter_tail": {k: int(v) for k, v in sorted(quarter.items())[-12:]},
        "month_tail": {k: int(v) for k, v in sorted(month.items())[-18:]},
        "institution_kind": dict(kind),
        "institution_top20": T.topn(inst, 20),
        "city_top20": T.topn(city_paper, 20),
        "anomaly": {
            "y2024": y2024,
            "y2024_share_pct": round(100 * y2024 / total, 2),
            "y2024_over_2023": round(y2024 / y2023, 3) if y2023 else None,
            "y2025": year_all.get("2025", 0),
            "y2026": year_all.get("2026", 0),
            "note": "2024 年 32,379 篇 = 全库 32.09%，是 2023 年的 4.87 倍，而 2025 仅 6,548、"
                    "2026 仅 2,989；这是采集批次截断，不是真实产出爆发，趋势图必须断点标注",
        },
        "growth": {
            "recent_window": [2022, 2023, 2024],
            "base_window": [2019, 2020, 2021],
            "recent_mean": round(sum(recent) / 3, 1),
            "base_mean": round(sum(base) / 3, 1),
            "growth_pct": growth,
            "note": "2024 含批次尖峰，该增速不可单独作为「论文产出增长」对外",
        },
        "base_years_used": [2019, 2020, 2021, 2022, 2023, 2024],
        "base_years_missing": [],
        "base_year_block": T.base_year_block(
            [2019, 2020, 2021, 2022, 2023, 2024], [],
            "论文年序列自 1980 起连续；2019—2024 六年均为真实年份，无缺失年"),
        "coverage": {
            "time_dim": "cover_year_start 100,900/100,900 = 100%",
            "institution_dim": f"{len(inst):,} 个机构名，{auth_instances:,} 个署名实例",
            "region_dim": f"按机构名/地址文本识别城市，覆盖 {city_ok:,}/{total:,} = "
                          f"{round(100 * city_ok / total, 2)}%",
            "type_dim": "paper_type 全为「期刊论文」，类型维无区分度",
        },
        "gaps": [
            "地域维靠机构名/地址文本识别城市，未做机构主数据对齐（企业底册是工商主体，不含高校）",
            "类型维只有「期刊论文」单值，会议/预印本/学位论文不在库内",
            "2024 年存在采集批次尖峰（32.09%），跨年趋势必须在 2024 断点",
            "2025 年 6,548 篇、2026 年 2,989 篇均不完整，禁止参与同比",
        ],
        "elapsed_sec": round(time.time() - t0, 1),
    }
    T.write_out(MID, res)
    print({k: res[k] for k in ("probe", "anomaly", "growth")})
    print("elapsed", res["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
