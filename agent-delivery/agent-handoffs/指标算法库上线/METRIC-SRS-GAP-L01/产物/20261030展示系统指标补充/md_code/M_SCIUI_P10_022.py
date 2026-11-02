#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_022 科技人员流动动态 —— 薄壳校验脚本（完全转换支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:1089 ElementCard「科技人员流动动态」
（stat = kpis.talent 全球科研人员净流入，人）。
数据：jiuxin ads_talent_mobility_yearly_flow 51,489 行（2000-2025 二十六年）
+ ads_geo_yearly_metrics inbound/outbound_talent_count（净流入=入-出一步转换）
+ ads_talent_mobility_event 298,384 行事件底表——结构+数据均足，判完全转换支持。
"""
from __future__ import annotations

import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_022_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          connect_timeout=15, read_timeout=600)

VERDICT = "完全转换支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    conn = pymysql.connect(**JX)
    cur = conn.cursor()
    # COUNTRY 级年度净流入合计（净流入 = Σ(inbound-outbound)）
    cur.execute(
        "SELECT statistics_year, SUM(inbound_talent_count), SUM(outbound_talent_count) "
        "FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' "
        "AND statistics_year BETWEEN 2018 AND 2025 GROUP BY statistics_year "
        "ORDER BY statistics_year")
    rows = cur.fetchall()
    net_yearly = {}
    for y, ib, ob in rows:
        net_yearly[str(y)] = int(ib or 0) - int(ob or 0)  # COUNTRY 全集合计=0（守恒）
    # 中国净流入（UI mock 语义=区域净流入读数；全集守恒说明必须按区域切）
    cur.execute(
        "SELECT statistics_year, inbound_talent_count-outbound_talent_count "
        "FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' "
        "AND location_id='loc_B56D89F0452662FBF49EAAD21C2A630E' "
        "AND statistics_year BETWEEN 2018 AND 2025 ORDER BY statistics_year")
    cn_net = {str(y): int(n or 0) for y, n in cur.fetchall()}
    # 事件底表跨域标志年度合计（2018-2025）
    cur.execute(
        "SELECT event_year, COUNT(*), SUM(is_cross_country), SUM(is_cross_province), SUM(is_cross_city) "
        "FROM ads_talent_mobility_event WHERE event_year BETWEEN 2018 AND 2025 "
        "GROUP BY event_year ORDER BY event_year")
    ev = [{"year": y, "events": n, "cross_country": cc, "cross_province": cp, "cross_city": ct}
          for y, n, cc, cp, ct in cur.fetchall()]
    conn.close()

    assert jx["jx_talent_flow_rows"] == 51489
    assert len(net_yearly) == 8 and len(cn_net) == 8 and len(ev) == 8
    assert all(v == 0 for v in net_yearly.values())  # 全集守恒断言
    assert cn_net["2024"] == -5  # 中国 2024 净流入（实测；+19 为香港行）
    assert cn_net["2018"] == 115 and cn_net["2020"] == 155

    out = {
        "metric_id": "M_SCIUI_P10_022",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1089",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:680-681",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技时空演进展示.md 序号 507「科技人员流动动态可视化」（需规描述：支持主动跟踪各专业主题下的科技人员流动，智能识别跨区和跨领域流动趋势，展示人才聚集、迁徙热点及高成长区）；另 bid_desc 500 行「科技人员流动等实时动态数据」",
            "note": "要素卡（本件）+可视化区块（P10_023）同挂 507 族语义；本件为总量卡",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:1089 ElementCard title=科技人员流动动态 stat=`${formatNumber(kpis.talent)} 人` desc=全球科研人员净流入 onClick 跳 ste-b-talent；:681 KpiTile label=科研人员净流入 metricId=Q0205",
            "ui_kpis_source": "mockData.js getCityStats→aggregateStats：26 城 base.talent 按 growth*0.8 外推求和（毛存量外推非净流入语义）",
            "ui_mock_note": "ui_demo_fallback：mock talent 值为城市基准外推合计（毛量语义）；UI 标签「净流入」与 mock 计算式（毛存量）本身口径不一致——切真时以库净流入口径为准",
            "jiuxin_flow_table": "ads_talent_mobility_yearly_flow",
            "jiuxin_flow_rows": 51489,
            "jiuxin_flow_year_span": "2000-2025（26 年现场实数，无空年 null_year=0）",
            "jiuxin_flow_dimensions": {"LOCATION": 28672, "INSTITUTION": 17064, "DISCIPLINE": 5753},
            "jiuxin_event_table": "ads_talent_mobility_event",
            "jiuxin_event_rows": 298384,
            "jiuxin_event_columns_30": "30 列含 mobility_type/from-to_institution/location/country/province/city/field/is_cross_country/province/city 标志/assignment_confidence",
            "jiuxin_geo_table": "ads_geo_yearly_metrics（171,736 行，含 inbound_talent_count/outbound_talent_count）",
            "gkx_talent_tables": "dwd_scholar（21,316 行）/dwd_scholar_work_experience/dwd_scholar_education_background（学者履历族——P4 探针已采 57,117 工作经历行）",
            "gkx_talent_note": "gkx 学者履历面为另一条转换路径（履历时序推流动），久新事件面更直接（现成跨域标志列）——本件以久新为主源",
            "dev_talent_word_hits": "scholar 表（gkxlumenx_ods.scholar）+链上 talent 列（chain_bottleneck 等 5 表）——无流动事件面",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "cn_net_inflow_yearly",
                "value": cn_net,
                "formula": "net = inbound_talent_count - outbound_talent_count（COUNTRY 级中国行，2018-2025）",
                "source": "jiuxin ads_geo_yearly_metrics",
                "share_basis": "同表同行两列相减（B3 同基）",
            },
            {
                "name": "cross_border_events_yearly",
                "value": {str(e["year"]): [e["events"], e["cross_country"], e["cross_province"], e["cross_city"]] for e in ev},
                "note": "[events, cross_country, cross_province, cross_city]——跨域流动事件三标志年度序列",
                "source": "jiuxin ads_talent_mobility_event",
            },
            {
                "name": "global_net_conservation_check",
                "value": net_yearly,
                "note": "COUNTRY 全集合计逐年=0（流入=流出守恒）——「全球净流入」全集口径无意义，必须按区域切（中国净流入见 derived[0]）；UI desc「全球科研人员净流入」语义需修正为区域读数",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 talent/personnel/mobility 词族", "source": "dev",
             "hits": ["gkxlumenx_ods.scholar", "gkxlumenx_ads.chain_bottleneck", "gkxlumenx_ads.tech_power"],
             "note": "scholar 学者名录+链上人才列——无流动事件面（0 张）"},
            {"probe": "gkx 280 表 talent 词族", "source": "gkx",
             "hits": ["dwd_scholar", "dwd_scholar_work_experience", "dwd_scholar_education_background", "dwd_scholar_talent_flag"],
             "note": "学者履历面（可转换但需履历时序工程）——非现成流动面"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）talent/mobility 词族", "source": "jiuxin",
             "hits": ["ads_talent_mobility_yearly_flow", "ads_talent_mobility_event", "ads_talent_mobility_flow_detail"],
             "primary": "ads_talent_mobility_yearly_flow",
             "note": "正结论：流动三件套（年度流量 51,489 行/事件底表 298,384 行/明细 65,105 行）+ geo 面 inbound/outbound 列"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：人员流动读数（净流入/流动量）可由久新三面一步转换——ads_geo_yearly_metrics（inbound-outbound 列现成）、ads_talent_mobility_yearly_flow（LOCATION 对流量 2000-2025）、ads_talent_mobility_event（298,384 行含跨域三标志）。结构+数据均足，判完全转换支持。",
            "口径修正点：mock 计算式为毛存量外推（aggregateStats 求和）而 UI 标签写「净流入」——两口径不一致；库净流入=入-出（中国 2018-2025：+115/+95/+155/+158/+96/+28/-5/+21 人；2024 年净流出国 Top 为香港/美国）。切真时按区域净流入口径并对齐标签。",
            "全集守恒断言：COUNTRY 级全球合计逐年=0（流入=流出）——「全球净流入」无意义，desc 需改区域读数（如「中国科研人员净流入」）。",
            "gkx 学者履历面（21,316 学者/57,117 工作经历）为备选路径（履历时序推流动），精度低于久新事件面（assignment_confidence 现成）；本件主源久新。",
            "与 P10_023（可视化区块）同根共享三面；P10_023 聚焦热点/迁徙三标签，本件聚焦总量卡读数——两件独立留证。",
        ],
        "base_years_used": sorted(cn_net),
        "base_years_missing": [],
        "base_years_note": "ads_geo_yearly_metrics 2018-2025 全覆盖（本件读数窗口）；事件面 2000-2025 二十六年更长；2026 为不完整年（geo 面 talent 流动 0 行）截断。基期建议 2018。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "51489", "51,489", "298384", "298,384", "171736", "171,736", "21316", "21,316",
            "57117", "57,117", "28672", "17064", "5753", "26", "0", "19", "8",
            "542", "280", "218", "2018", "2025", "2024", "2000", "419",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| CN net 2018-2025:", cn_net)


if __name__ == "__main__":
    main()
