#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_023 科技人员流动动态可视化 —— 薄壳校验脚本（完全转换支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:1261「科技人员流动动态可视化」区块：
聚集热点（talent 存量 Top3）/迁徙热点（FLOW_PATHS talent 型目的地 Top3）/
高成长区（growth.talent Top3）三标签。
数据：jiuxin 三面齐备——geo 面存量+growth 列、yearly_flow LOCATION 对流量
（迁徙目的地=对流量 to 端 Top）、event 面跨域标志。三标签全部可转换计算。
"""
from __future__ import annotations

import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_023_out.json")

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
    # ① 聚集热点：COUNTRY 级 2024 talent_count Top3
    cur.execute(
        "SELECT g.location_id, g.talent_count, l.name FROM ads_geo_yearly_metrics g "
        "JOIN ads_location l ON g.location_id=l.location_id "
        "WHERE g.location_level='COUNTRY' AND g.statistics_year=2024 "
        "ORDER BY g.talent_count DESC LIMIT 3")
    gather = [{"name": n, "talent": int(t)} for _lid, t, n in cur.fetchall()]
    # ② 迁徙热点：LOCATION 维 2024 入流量（to 端）Top3
    cur.execute(
        "SELECT f.to_entity_id, SUM(f.talent_count) s, l.name "
        "FROM ads_talent_mobility_yearly_flow f "
        "JOIN ads_location l ON f.to_entity_id=l.location_id "
        "WHERE f.flow_dimension='LOCATION' AND f.statistics_year=2024 "
        "GROUP BY f.to_entity_id, l.name ORDER BY s DESC LIMIT 3")
    migrate = [{"name": n, "inflow": int(s)} for _tid, s, n in cur.fetchall()]
    # ③ 高成长区：COUNTRY 级 talent_count 同比增速 Top3（2023→2024）
    cur.execute(
        "SELECT a.location_id, ROUND((b.talent_count-a.talent_count)/a.talent_count*100,1) g, l.name "
        "FROM ads_geo_yearly_metrics a JOIN ads_geo_yearly_metrics b "
        "ON a.location_id=b.location_id AND b.statistics_year=a.statistics_year+1 "
        "JOIN ads_location l ON a.location_id=l.location_id "
        "WHERE a.location_level='COUNTRY' AND a.statistics_year=2023 "
        "AND a.talent_count>1000 "
        "ORDER BY g DESC LIMIT 3")
    rising = [{"name": n, "growth_pct": float(g)} for _lid, g, n in cur.fetchall()]
    # ④ 口径②（tooltip :1282 变体）：近三年净流入合计增速（2021-2023 和 vs 2022-2024 和）
    cur.execute(
        "SELECT location_id, statistics_year, inbound_talent_count-outbound_talent_count "
        "FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' "
        "AND statistics_year IN (2021,2022,2023,2024) AND location_id IN ("
        "SELECT location_id FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' "
        "AND statistics_year=2024 AND talent_count>1000)")
    from collections import defaultdict
    dd = defaultdict(dict)
    for lid, y, n in cur.fetchall():
        dd[lid][int(y)] = int(n or 0)
    variant = []
    for lid, m in dd.items():
        if all(y in m for y in (2021, 2022, 2023, 2024)):
            sp, sn = m[2021] + m[2022] + m[2023], m[2022] + m[2023] + m[2024]
            if sp != 0:
                variant.append({"location_id": lid, "sum_2123": sp, "sum_2224": sn,
                                "chg_pct": round((sn - sp) / abs(sp) * 100, 1)})
    variant.sort(key=lambda r: -r["chg_pct"])
    rising_variant = variant[:3]
    conn.close()

    assert len(gather) == 3 and len(migrate) == 3 and len(rising) == 3
    assert gather[0]["name"] == "China" and gather[0]["talent"] == 69523
    assert migrate[0]["name"] == "China" and migrate[0]["inflow"] == 127
    assert rising[0]["name"] == "South Korea" and rising[0]["growth_pct"] == 26.1

    out = {
        "metric_id": "M_SCIUI_P10_023",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1261",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:534",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:482-502",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技时空演进展示.md 序号 507「科技人员流动动态可视化」——本件即该功能叶的 UI 落位区块（同名，需规描述：智能识别跨区和跨领域流动趋势，展示人才聚集、迁徙热点及高成长区）",
            "note": "区块标题与 SRS 功能叶 507 同名；本件为可视化区块（P10_022 为同族总量卡）",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:1261 SectionCard id=ste-b-talent title=科技人员流动动态可视化 desc=聚集热点/迁徙热点/高成长区；:1268-1276 三 Tag 标签行（红=聚集/orangered=迁徙/绿=高成长）",
            "ui_hotspot_builder": "mockData.js:482-502 getTalentHotspots(year)：gather=城市 talent 存量 Top3；migrate=FLOW_PATHS talent 型按流量排序取 to 端去重 Top3；rising=growth.talent Top3",
            "ui_mock_note": "ui_demo_fallback：mock 热点为 26 城外推（聚集如北京/深圳；迁徙如硅谷/新加坡）；非真实流动识别",
            "jiuxin_geo_table": "ads_geo_yearly_metrics（171,736 行；talent_count 存量列承载聚集、同比增速承载成长）",
            "jiuxin_flow_table": "ads_talent_mobility_yearly_flow（51,489 行；LOCATION 维 to 端入流量承载迁徙目的地）",
            "jiuxin_event_table": "ads_talent_mobility_event（298,384 行；跨域三标志承载「跨区和跨领域流动趋势」语义）",
            "hotspots_2024": {"gather_top3": gather, "migrate_top3": migrate, "rising_top3": rising},
            "geo_level_rows": {"COUNTRY": 5081, "PROVINCE": 33518, "CITY": 132975, "CONTINENT": 162},
            "ads_location_rows": 22229,
            "gkx_note": "学者履历族（dwd_scholar_work_experience 57,117 行）可推热点但需自建聚合；久新三面现成列优先",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "gather_hotspots_top3_2024",
                "value": gather,
                "formula": "COUNTRY 级 talent_count 降序 Top3（聚集=存量规模）",
                "source": "jiuxin ads_geo_yearly_metrics × ads_location",
                "share_basis": "同表同年同层级排序（B3 同基）",
            },
            {
                "name": "migrate_hotspots_top3_2024",
                "value": migrate,
                "formula": "LOCATION 维 SUM(talent_count) 按 to 端分组降序 Top3（迁徙目的地=入流量）",
                "source": "jiuxin ads_talent_mobility_yearly_flow",
            },
            {
                "name": "rising_hotspots_top3_2024",
                "value": rising,
                "formula": "(talent_{2024}−talent_{2023})/talent_{2023}×100 降序 Top3（talent_count>1000 门槛防小基数）",
                "source": "jiuxin ads_geo_yearly_metrics 自关联",
                "note": "同表自关联相除（B3 同基）；分母门槛 1000 人防微基数虚高",
            },
            {
                "name": "rising_variant_tooltip_cagr_top3",
                "value": rising_variant,
                "formula": "口径②（tooltip :1282 变体）：Σ净流入(2022-2024) 对 Σ净流入(2021-2023) 变化率降序 Top3（>1000 人门槛集合内）",
                "source": "jiuxin ads_geo_yearly_metrics inbound-outbound",
                "note": "小基数敏感（净流入绝对量仅几十人级）：Top1 三年和 −6→+2；Hong Kong 18→40（+122.2%）——仅作敏感性披露不参与判档",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 talent/hotspot 词族", "source": "dev",
             "hits": ["gkxlumenx_ods.scholar", "gkxlumenx_ads.chain_hotspot"],
             "note": "scholar 名录+链热点（行业链语义）——非人才流动热点面"},
            {"probe": "gkx 280 表 talent 词族", "source": "gkx",
             "hits": ["dwd_scholar", "dwd_scholar_work_experience"],
             "note": "学者履历面（备选路径，需自建聚合非现成热点列）"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）talent/mobility 词族", "source": "jiuxin",
             "hits": ["ads_talent_mobility_yearly_flow", "ads_talent_mobility_event", "ads_talent_yearly_metrics"],
             "primary": "ads_talent_mobility_yearly_flow",
             "note": "正结论：三面齐备（存量/流量/事件），三标签全部可转换计算"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：三标签逐一对应现成列——聚集=geo 面 talent_count 排序；迁徙=flow 面 to 端入流量排序；高成长=geo 面同比自关联。结构+数据均足（2024 实算三组 Top3 落产物），判完全转换支持。",
            "2024 实算：聚集 Top3=China 69,523/United States 18,891/United Kingdom 5,265 人（数量级远小于 mock 26 城外推设定）；迁徙 Top3 按入流量=China 127/United States 64/Hong Kong 39 人；高成长 Top3 按 2023→2024 同比=South Korea 26.1%/Hong Kong 20.1%/Taiwan 18.0%（门槛>1000 人防微基数）。",
            "「跨区和跨领域流动趋势」（507 需规）由 event 面三跨域标志+DISCIPLINE 维承载（P10_022 已采序列）；本区块三标签为主呈现位。",
            "口径②（tooltip :1282「近三年人才净流入复合增速」变体）可算但小基数敏感（Top3 见 derived[3]：Hong Kong 三年和 18→40=+122.2%）——敏感性披露不参与判档。",
            "层级口径：mock 热点为城市级；库 COUNTRY 级最稳（CITY 132,975 行亦可切，geo 面 location_level 分布 COUNTRY 5,081/PROVINCE 33,518/CITY 132,975/CONTINENT 162；区域字典 ads_location 22,229 行）——层级选择披露为口径参数（默认 COUNTRY）。",
            "与 P10_022（总量卡）同根共享三面；两件独立实算留证。",
        ],
        "base_years_used": ["2023", "2024"],
        "base_years_missing": [],
        "base_years_note": "三标签为时点读数（2024 计算年，含 2023 基准年自关联）；全序列 2000-2025 可复算任意年。基期随 year 选择器联动。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "171736", "171,736", "51489", "51,489", "298384", "298,384",
            "69523", "69,523", "18891", "18,891", "5265", "5,265",
            "127", "64", "39", "26.1", "20.1", "18.0", "122.2",
            "5081", "5,081", "33518", "33,518", "132975", "132,975", "22229", "22,229",
            "57117", "57,117", "3", "1000", "2021", "2023", "2024", "542", "280", "218",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| gather:", gather, "| migrate:", migrate, "| rising:", rising)


if __name__ == "__main__":
    main()
