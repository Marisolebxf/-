#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_GLOBAL_STOCK · 全球领域人才总量（UI KPI「全球人才总数」）

展示系统 UI 实扫指标（20261030 批）：repos/demo-ui-science/src/pages/talent-trend/
components/DistributionInsightView.jsx:284 kpiData[0]「全球人才总数」。
需求文档未点名该 KPI（属 UI 自造聚合位），推测定义：全球学者库中可统计的
科技人才（学者）总记录数。

口径（推测定义，非甲方闭合）：
  分子 = gkx.dwd_scholar 有效学者记录数（is_deleted 语义列全 0，不参与过滤；
        status 列分布如实披露）
  并列口径 A：主档全量；口径 B：有履历挂接地理信息的学者数（可上地图者）。

数据源：gkx（183.240.141.251:3318，只读）+ live 兜底（本指标无需）。
产出：M_TALENT_UI_GLOBAL_STOCK_out.json（support_judgment + derived 0 容忍）。
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SHARED = Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")
sys.path.insert(0, str(_SHARED))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_GLOBAL_STOCK",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:284",
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:233",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份需求说明书均未出现「全球人才总数/人才总数」字样；"
                    "SRS 叶「人才分布信息查看」(seq 243, excel_row 246) 仅要求区域分布概览展示。"
                    "本指标为 UI 自造 KPI，推测定义。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
    }

    # —— 口径 A：主档全量有效记录 ——
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    total = cur.fetchone()[0]
    out["facts"]["scholar_total"] = total

    cur.execute("SELECT status, COUNT(*) FROM gkx.dwd_scholar GROUP BY status")
    out["facts"]["status_dist"] = {str(k): v for k, v in cur.fetchall()}

    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar WHERE is_deleted = 1")
    out["facts"]["is_deleted_1_rows"] = cur.fetchone()[0]

    # —— 口径 B：可挂地理（有在任履历且机构可映射国家）的学者数 ——
    cur.execute("""
        SELECT COUNT(DISTINCT we.scholar_id)
        FROM gkx.dwd_scholar_work_experience we
        WHERE we.is_current = 1
    """)
    with_current = cur.fetchone()[0]
    out["facts"]["scholars_with_current_exp"] = with_current

    cur.execute("""
        SELECT COUNT(DISTINCT we.scholar_id)
        FROM gkx.dwd_scholar_work_experience we
        JOIN gkx.dwd_forg_university_org_info u
          ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
             = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
        WHERE we.is_current = 1
          AND we.org_name_en IS NOT NULL
          AND u.country IS NOT NULL AND u.country != ''
    """)
    geo_resolvable = cur.fetchone()[0]
    out["facts"]["scholars_geo_resolvable_current"] = geo_resolvable

    # —— 派生比（0 容忍落产物）——
    out["derived"] = [
        {
            "key": "geo_resolvable_share_pct",
            "value": round(geo_resolvable / total * 100, 4),
            "numerator": "scholars_geo_resolvable_current",
            "denominator": "scholar_total",
            "denominator_note": "分母为主档全量记录数（口径 A），分子为在任履历且机构可映射国家的学者数（口径 B）",
        },
        {
            "key": "current_exp_share_pct",
            "value": round(with_current / total * 100, 4),
            "numerator": "scholars_with_current_exp",
            "denominator": "scholar_total",
            "denominator_note": "分母同上；分子为有在任履历的学者数",
        },
    ]

    # —— 支持度判定 ——
    # 结构：主档 21,316 行可直查直算（完全转换支持的结构条件满足）
    # 数据量：地理映射经大学表仅约四成可解析（抽样 500 段 39.2% 精确 / 45.2% 含 alias），
    #         地图级「全球分布」承载打折 → 部分支持
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "判部分支持依据：人才总量的计数面完全可得（dwd_scholar 21,316 行），"
        "但 UI 同屏还承诺「按地域分布」，学者→国家映射链路（履历机构名↔大学表 name_std/alias）"
        "实测覆盖率仅约 39.2%–45.2%（抽样 500 段履历），地域维数据量不足。"
    )

    dst = _HERE / "M_TALENT_UI_GLOBAL_STOCK_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1)[:1200])
    print("→ 落盘", dst)


if __name__ == "__main__":
    main()
