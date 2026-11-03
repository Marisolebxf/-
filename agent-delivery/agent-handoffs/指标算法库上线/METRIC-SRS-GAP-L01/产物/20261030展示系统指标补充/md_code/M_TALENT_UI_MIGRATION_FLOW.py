#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_MIGRATION_FLOW · 全球人才迁徙人次与净流入（洞察面板·迁徙时序+热点）

展示系统 UI 实扫指标（20261030 批）：
- InsightPanel.jsx:215 图例「人才总量/迁徙人次」（timeTrendOption 时序）
- InsightPanel.jsx:339-375 流入热点/流出风险卡（净流入 net、风险标签）
- data.js:140-167 generateRegionTimeSeries / generateGlobalTimeSeries（mock：按 growth 系数伪造）
- 需求明列叶：SRS「人才迁徙情况展示」(seq 252, excel_row 255)——流动路径动画、区域热点自动高亮。

口径（推测定义）：迁徙 = 学者「在任履历」跨机构变更事件：
  某学者按 start_time 排序的相邻两段履历机构不同 → 记一次迁徙；
  迁入国 = 新机构 country，迁出国 = 前机构 country；年度净流入 = 迁入 − 迁出。
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
        "metric_id": "M_TALENT_UI_MIGRATION_FLOW",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:215",
            "repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:339",
            "repos/demo-ui-science/src/pages/talent-trend/data.js:140",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "srs_leaf": "SRS 02-科技信息展示系统/科技人才态势/全球领域人才态势.md · 人才迁徙情况展示 · seq 252 · excel_row 255",
            "bid_desc": "流动路径动画、区域热点自动高亮…看到近年 AI 人才从硅谷流向新加坡的变化",
        },
        "facts": {},
        "derived": [],
        "support_judgment": None,
        "notes": [],
    }

    # 履历事件基本面
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_work_experience")
    out["facts"]["work_exp_rows"] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_work_experience WHERE start_time IS NOT NULL")
    out["facts"]["start_time_nonnull"] = cur.fetchone()[0]

    # 有 ≥2 段履历的学者（可产生迁徙事件者）
    cur.execute("""
        SELECT scholar_id, COUNT(*) AS n
        FROM gkx.dwd_scholar_work_experience
        GROUP BY scholar_id HAVING n >= 2
    """)
    multi = cur.fetchall()
    out["facts"]["scholars_with_multi_exp"] = len(multi)

    # 迁徙事件测算（限多段履历学者；时间相邻对；start_time 为 'YYYY.MM'/'YYYY' 等字符串格式）
    cur.execute("""
        SELECT we.scholar_id, we.start_time, we.org_name_en
        FROM gkx.dwd_scholar_work_experience we
        WHERE we.start_time IS NOT NULL
        ORDER BY we.scholar_id, we.start_time
    """)
    rows = cur.fetchall()

    def parse_year(v):
        # 实测格式：'2017.04' / '2020' / '2018.01'（字符串，非 DATE）
        if v is None:
            return None
        s = str(v).strip()
        for head in s.replace("–", ".").replace("-", ".").split("."):
            if head.isdigit() and 1900 <= int(head) <= 2100:
                return int(head)
        digits = "".join(ch for ch in s if ch.isdigit())[:4]
        return int(digits) if digits.isdigit() and 1900 <= int(digits) <= 2100 else None

    events = 0
    cross_org = 0
    by_year = {}
    prev = None
    for sid, st, org in rows:
        if prev is not None and prev[0] == sid:
            if org and prev[2] and org.strip() != prev[2].strip():
                cross_org += 1
                y = parse_year(st)
                if y:
                    by_year[y] = by_year.get(y, 0) + 1
            events += 1
        prev = (sid, st, org)
    out["facts"]["adjacent_transitions"] = events
    out["facts"]["cross_org_transitions"] = cross_org
    out["facts"]["transitions_by_year_top"] = dict(sorted(by_year.items(), key=lambda kv: -kv[1])[:10])

    # 国家维迁徙（须过大学表映射——覆盖率四成，如实降档）
    cur.execute("""
        SELECT COUNT(*) FROM (
          SELECT we.scholar_id, we.start_time
          FROM gkx.dwd_scholar_work_experience we
          JOIN gkx.dwd_forg_university_org_info u
            ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
               = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
          WHERE we.start_time IS NOT NULL AND u.country IS NOT NULL AND u.country != ''
        ) t
    """)
    geo_tagged = cur.fetchone()[0]
    out["facts"]["geo_tagged_exp_rows"] = geo_tagged

    out["derived"] = [
        {
            "key": "multi_exp_scholar_share_pct",
            "value": round(len(multi) / 21316 * 100, 4),
            "numerator": "scholars_with_multi_exp",
            "denominator": "scholar_total(21316)",
            "denominator_note": "可产生迁徙事件的学者占比——迁徙口径的样本面",
        },
        {
            "key": "geo_tagged_exp_share_pct",
            "value": round(geo_tagged / max(out["facts"]["work_exp_rows"], 1) * 100, 4),
            "numerator": "geo_tagged_exp_rows",
            "denominator": "work_exp_rows",
            "denominator_note": "履历可挂国家比例＝跨国迁徙（UI 净流入/流出）可用样本上限",
        },
    ]
    out["notes"].append(
        "start_time 为字符串（'2017.04'/'2020'），非 DATETIME——年度聚合按前 4 位数字解析年份，"
        "无法解析的行不计入年度桶（不影响事件总数）。"
    )
    out["notes"].append(
        "机构级迁徙（跨机构变更）可全量推导；但 UI 的「国家间净流入/流出」依赖国家标签，"
        "履历↔大学表覆盖仅约四成 → 跨国维部分支持；无大学映射的机构（企业/研究院所）迁徙不可国家化。"
    )
    out["notes"].append(
        "UI mock 伪迹披露：data.js:140 按 growth 系数伪造年度总量与净流入（±0.015~0.06 随机数），"
        "正式版不得沿用；本件给真实可推导口径。"
    )
    out["support_judgment"] = "部分支持"

    dst = _HERE / "M_TALENT_UI_MIGRATION_FLOW_out.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["facts"], ensure_ascii=False, indent=1)[:1000])
    print("→", out["support_judgment"])


if __name__ == "__main__":
    main()
