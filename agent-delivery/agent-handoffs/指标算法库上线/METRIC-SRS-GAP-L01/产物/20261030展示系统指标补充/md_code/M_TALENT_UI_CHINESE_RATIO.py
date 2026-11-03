#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_CHINESE_RATIO · 全球华人科技人才占比（洞察面板·华人占比分析）

展示系统 UI 实扫指标（20261030 批）：
- InsightPanel.jsx:39-90「华人占比分析」堆叠柱（chineseRatio 数据：分区 chinese/total）
- 需求明列叶：SRS「华人占比分析」(seq 248, excel_row 251, path …/人才洞察分析/华人占比分析)
  ——分区展示（按国家/地区展示华人占比）+ 机构筛选（顶尖机构华人学者比例）。

口径（推测定义——需求点名功能但未给算法）：
  华人代理判定 = 学者中文名存在（dwd_scholar.name_zh 非空且含 CJK）。
  分区维 = 学者在任履历机构 → 大学表 country 映射；不可映射者入「未映射」桶如实并列。
"""
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")))
from _gkxdb import gkx  # noqa: E402

CJK = re.compile(r"[\u4e00-\u9fff]")


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_CHINESE_RATIO",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:264",
            "repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:39",
            "repos/demo-ui-science/src/pages/talent-trend/data.js:1130 (generateChineseRatio mock)",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "srs_leaf": "SRS 02-科技信息展示系统/科技人才态势/全球领域人才态势.md · 华人占比分析 · seq 248 · excel_row 251",
            "bid_desc": "支持按国家或地区展示全球各领域人才中的华人占比…用户可直观查看不同区域华人科技人才比例",
        },
        "facts": {},
        "derived": [],
        "support_judgment": None,
        "notes": [],
    }

    total = 21_316  # 与共享快照一致；本件重查防漂
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    total = cur.fetchone()[0]
    out["facts"]["scholar_total"] = total

    # 华人代理：中文名含 CJK（MySQL ICU regexp 不支持 \x{} 语法，统一拉列到 Python 判定）
    cur.execute("SELECT name_zh FROM gkx.dwd_scholar WHERE name_zh IS NOT NULL AND name_zh != ''")
    zh_names = [r[0] for r in cur.fetchall()]
    chinese = sum(1 for n in zh_names if CJK.search(n))
    non_cjk_zh = len(zh_names) - chinese
    out["facts"]["name_zh_nonnull"] = len(zh_names)
    out["facts"]["name_zh_with_cjk"] = chinese
    out["facts"]["name_zh_without_cjk"] = non_cjk_zh

    # 分区：在任履历 → 大学表 country（B3：同池=有在任履历且可映射国家的学者）
    cur.execute("""
        SELECT u.country, COUNT(DISTINCT we.scholar_id) AS n
        FROM gkx.dwd_scholar_work_experience we
        JOIN gkx.dwd_forg_university_org_info u
          ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
             = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
        WHERE we.is_current = 1 AND u.country IS NOT NULL AND u.country != ''
        GROUP BY u.country ORDER BY n DESC LIMIT 12
    """)
    region_rows = {str(k): v for k, v in cur.fetchall()}
    out["facts"]["top12_countries_scholars"] = region_rows

    # 机构华人占比（需求第二分句）：大学表覆盖机构 × 该机构学者中文名占比（Top8）
    cur.execute("""
        SELECT u.name_std, u.country,
               COUNT(DISTINCT we.scholar_id) AS scholars,
               COUNT(DISTINCT CASE WHEN s.name_zh REGEXP '[一-龥]' THEN s.scholar_id END) AS cn
        FROM gkx.dwd_scholar_work_experience we
        JOIN gkx.dwd_scholar s ON s.scholar_id = we.scholar_id
        JOIN gkx.dwd_forg_university_org_info u
          ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
             = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
        WHERE we.is_current = 1
        GROUP BY u.name_std, u.country
        HAVING scholars >= 20
        ORDER BY scholars DESC LIMIT 8
    """)
    inst_rows = []
    for name, country, scholars, cn in cur.fetchall():
        inst_rows.append({"institution": name, "country": country,
                          "scholars": scholars, "chinese_name_scholars": cn,
                          "cn_share_pct": round(cn / scholars * 100, 2)})
    out["facts"]["top8_institutions_by_scholars"] = inst_rows
    # 机构华人计数用 REGEXP '[一-龥]' 在库内完成（ICU 支持 U+4E00–U+9FA5 字面区间）；此处不再复算

    # 派生比
    mapped_total = sum(region_rows.values())
    out["derived"] = [
        {
            "key": "chinese_name_share_pct_global",
            "value": round(chinese / total * 100, 4),
            "numerator": "name_zh_with_cjk",
            "denominator": "scholar_total",
            "denominator_note": "全库口径：中文名代理华人，分母=主档全量（无国籍字段，代理口径敏感性见 notes）",
        },
        {
            "key": "mapped_scholars_country_top12",
            "value": mapped_total,
            "numerator": "SUM(top12_countries_scholars)",
            "denominator": "scholars_geo_resolvable_current(=8438, 见共享快照)",
            "denominator_note": "前12国学者数与可映射总盘的对照，非比值，是覆盖计数",
        },
    ]
    out["notes"].append(
        "代理口径敏感性：name_zh 非空 20,420 中含 CJK 者判「华人」——"
        "该代理会把「有中文名的外籍学者」误纳、把「无中文名的华人」漏判；"
        "两向误差方向相反，量级未可从库内闭合，正文须披露。"
    )
    out["notes"].append(
        "地理维缺口：履历机构名↔大学表精确名等值仅约四成命中（共享快照 39.2%/45.2%），"
        "分区展示的全球覆盖不足 → 部分支持。"
    )
    out["support_judgment"] = "部分支持"

    dst = _HERE / "M_TALENT_UI_CHINESE_RATIO_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["facts"], ensure_ascii=False, indent=1)[:1500])
    print("→", out["support_judgment"])


if __name__ == "__main__":
    main()
