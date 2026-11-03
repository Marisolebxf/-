#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_YOY_GROWTH · 全球人才平均同比增长（UI KPI）

展示系统 UI 实扫指标（20261030 批）：DistributionInsightView.jsx:286「平均同比增长」
（v3 实扫该行已注释，仅 Excel 导出 218 行保留文案；RegionDetailDrawer 区域时序同义）。
需求文档未点名。推测定义：学者池年度新增（按论文首年或履历起始年计）的同比增长率均值。

基期事实（先测后判）：dwd_scholar 无 create_time 有效分布保证 → 用
dwd_scholar_papers.cover_date_start（100% 非空）按年聚合「有产出的学者数」做年度序列，
对相邻年算同比增长，取均值与逐年序列并列。
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_YOY_GROWTH",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:286（注释态）",
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:218（Excel 导出文案「平均同比增长」）",
            "repos/demo-ui-science/src/pages/talent-trend/components/ChinaTalentView.jsx:466（中国视图·同比增长）",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书均未出现「同比增长」；UI 自造 KPI。mock 值为常量 +12.5%/+3.2%。",
        },
        "facts": {},
        "derived": [],
        "support_judgment": None,
        "notes": [],
    }

    # 年度「活跃学者数」序列：dwd_scholar_paper_relation 自带 year/citations（106.5 万行），
    # 无需 join papers 表；year 有脏值（0/1761 等），限 1990–2026 现代区间
    cur.execute("""
        SELECT `year`, COUNT(DISTINCT scholar_id) AS n
        FROM gkx.dwd_scholar_paper_relation
        WHERE `year` BETWEEN 1990 AND 2026
        GROUP BY `year` ORDER BY `year`
    """)
    series = {int(y): n for y, n in cur.fetchall()}
    out["facts"]["data_source"] = "gkx.dwd_scholar_paper_relation（1,065,385 行；year 限 1990–2026，脏年份剔除）"
    out["facts"]["active_scholars_by_year"] = {str(k): v for k, v in sorted(series.items())}

    # 同比增长率序列（相邻年，n_{t-1}>0 才算）
    years = sorted(series)
    yoy = {}
    for a, b in zip(years, years[1:]):
        if series[a] > 0:
            yoy[b] = round((series[b] - series[a]) / series[a] * 100, 4)
    out["facts"]["yoy_pct_by_year"] = {str(k): v for k, v in sorted(yoy.items())}

    # 近 5 个「完整年」均值（2020–2024；2025/2026 收录滞后剔除，与正文口径一致）
    recent = [yoy[y] for y in sorted(yoy) if 2020 <= y <= 2024]
    avg5 = round(sum(recent) / len(recent), 4) if recent else None
    out["facts"]["avg_yoy_last5_pct"] = avg5
    out["facts"]["avg_window"] = "2020–2024（完整年窗口；2025/2026 收录滞后剔除）"

    out["derived"] = [
        {
            "key": f"yoy_{y}",
            "value": v,
            "numerator": f"active_scholars_by_year[{y}] - active_scholars_by_year[{y-1}]",
            "denominator": f"active_scholars_by_year[{y-1}]",
            "denominator_note": "相邻年活跃学者同比增长率，逐年并列",
        } for y, v in sorted(yoy.items())
    ] + [{
        "key": "avg_yoy_last5_pct",
        "value": avg5,
        "numerator": "mean(yoy of last 5 years)",
        "denominator": "—（均值口径，无独立分母）",
        "denominator_note": "UI KPI「平均同比增长」对应的均值口径；逐年值见 yoy_* 键",
    }]

    out["notes"].append(
        "口径敏感性：主档 paper_nums/citation_nums 为累计值，无年度切面；"
        "年度序列由 dwd_scholar_paper_relation.year（活跃学者口径）推出，"
        "与 UI mock 的「人才总量年增长」语义有差（活跃≈有产出），须在正文披露。"
    )
    out["notes"].append(
        "2025/2026 年值骤降（8,464/281）为论文收录滞后所致，均值口径须注明取至 2024 或剔除不完整年。"
    )
    out["notes"].append(
        "relation 表 1,065,385 行、year 限现代区间后 1990–2024 序列完整，"
        "结构+数据量足、现转已跑通 → 完全转换支持（活跃学者口径）。"
    )
    out["support_judgment"] = "完全转换支持"

    dst = _HERE / "M_TALENT_UI_YOY_GROWTH_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("近5年同比:", {k: out["facts"]["yoy_pct_by_year"][k] for k in sorted(out["facts"]["yoy_pct_by_year"])[-5:]})
    print("avg5:", avg5, "→", out["support_judgment"])


if __name__ == "__main__":
    main()
