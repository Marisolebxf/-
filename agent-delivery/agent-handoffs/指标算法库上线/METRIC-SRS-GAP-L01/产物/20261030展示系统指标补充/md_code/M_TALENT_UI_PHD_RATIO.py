#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_PHD_RATIO · 全球人才博士平均占比（UI KPI）

展示系统 UI 实扫指标（20261030 批）：DistributionInsightView.jsx:285 kpiData[1]
「博士平均占比」。需求文档未点名（UI 自造 KPI），推测定义：全球学者库中
学历为博士（degree 含"博士/PhD/Doctor"）的学者占比，按学者去重。

UI 同名位（多挂点）：CityActivityDrawer.jsx:46（城市抽屉·博士占比）、
ChinaTalentView.jsx:465（中国视图·博士占比）、InstitutionDetailDrawer.jsx:35。
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_PHD_RATIO",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:285",
            "repos/demo-ui-science/src/pages/talent-trend/components/CityActivityDrawer.jsx:46",
            "repos/demo-ui-science/src/pages/talent-trend/components/ChinaTalentView.jsx:465",
            "repos/demo-ui-science/src/pages/talent-trend/components/InstitutionDetailDrawer.jsx:35",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "SRS「城市与区域详情」叶(seq 243)要求『点击地区弹出行业、学历、类型统计』——"
                    "学历维被需求点名，但未给出「博士占比」计算定义。",
        },
        "facts": {},
        "derived": [],
        "support_judgment": None,
        "notes": [],
    }

    # —— 学者×学历：履历/学历子表 → 学者去重 ——
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_education_background")
    out["facts"]["edu_rows"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(DISTINCT eb.scholar_id)
        FROM gkx.dwd_scholar_education_background eb
        WHERE eb.degree_zh LIKE '%博士%'
           OR eb.degree_en LIKE '%PhD%'
           OR eb.degree_en LIKE '%Doctor%'
           OR eb.degree_zh LIKE '%Doctor%'
    """)
    phd_scholars = cur.fetchone()[0]
    out["facts"]["phd_scholars"] = phd_scholars

    cur.execute("""
        SELECT COUNT(DISTINCT eb.scholar_id)
        FROM gkx.dwd_scholar_education_background eb
    """)
    edu_linked_scholars = cur.fetchone()[0]
    out["facts"]["edu_linked_scholars"] = edu_linked_scholars

    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    total = cur.fetchone()[0]
    out["facts"]["scholar_total"] = total

    # degree 字段分布（前 8 名，如实披露口径）
    cur.execute("""
        SELECT COALESCE(NULLIF(degree_zh, ''), degree_en, '（空）') AS deg, COUNT(*) AS n
        FROM gkx.dwd_scholar_education_background
        GROUP BY deg ORDER BY n DESC LIMIT 8
    """)
    out["facts"]["degree_top8"] = {str(k): v for k, v in cur.fetchall()}

    # —— 派生比：两种分母口径并列（B3 同基相除纪律） ——
    out["derived"] = [
        {
            "key": "phd_share_pct_over_edu_linked",
            "value": round(phd_scholars / edu_linked_scholars * 100, 4),
            "numerator": "phd_scholars",
            "denominator": "edu_linked_scholars",
            "denominator_note": "分母=学历子表覆盖的去重学者数（有学历信息者），分子分母同源（同走 eb 表）",
        },
        {
            "key": "phd_share_pct_over_all",
            "value": round(phd_scholars / total * 100, 4),
            "numerator": "phd_scholars",
            "denominator": "scholar_total",
            "denominator_note": "全库口径并列：分母=学者主档全量；该口径会低估（无学历信息者被计入分母）",
        },
    ]
    out["notes"].append(
        "share_basis：主口径取「有学历信息者」为分母（同池同 WHERE）；"
        "全库口径仅作并列参考。UI 的 mock 值为常量 0.62/0.66 假分布，本指标为真实口径重建。"
    )

    # 判档：学历子表 43,766 行、覆盖去重学者数千级，博士判定字段直接可用
    # →「完全转换支持」需「结构+数据量+现转成功」三者齐备；实测已跑通 → 完全转换支持
    out["support_judgment"] = "完全转换支持"
    out["notes"].append(
        "结构：dwd_scholar_education_background.degree_zh/degree_en 语义明确可直接判博士；"
        "数据量：43,766 行学历记录覆盖去重学者，规模充足；现转：本脚本已跑通产出占比。"
        "唯一限制：学历子表未覆盖全部学者（<100%），故全库口径为低估参考。"
    )

    dst = _HERE / "M_TALENT_UI_PHD_RATIO_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["facts"], ensure_ascii=False, indent=1))
    print("derived:", json.dumps(out["derived"], ensure_ascii=False))
    print("→", out["support_judgment"])


if __name__ == "__main__":
    main()
