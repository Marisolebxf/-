#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_025 科研主体时空流动路径追踪 —— 薄壳校验脚本（部分支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:1374 SectionCard「科研主体时空流动路径追踪」：
RESEARCH_SUBJECTS 选择器（16 主体=10 机构/载体+6 团队）+ WorldEvolutionMap route
+ 迁移路线明细（getSubjectRoute：团队 trajectory 截至某年站点序列）。
SRS 509：用户选择机构或研究团队，自动绘制其地理迁移和学科变迁路线。
数据实况：机构维无迁移（profile 静态单址，经历表 0 个多城市机构）；
团队维无实体表；学者维双向轨迹丰富（experience 地理时序 + event 学科变迁）。
主体选择器语义可由学者/领军人才承载，机构/团队整体迁移从缺 → 部分支持。
"""
from __future__ import annotations

import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_025_out.json")

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev", charset="utf8mb4",
          connect_timeout=15, read_timeout=600)

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=600, write_timeout=600, autocommit=True)

VERDICT = "部分支持"


def main() -> None:
    snap = json.load(open(SNAP, encoding="utf-8"))
    dev, gkx_snap, jx = snap["dev"], snap["gkx"], snap["jiuxin"]

    conn = pymysql.connect(**JX)
    cur = conn.cursor()
    # ① 轨迹承载量：多城市/多机构学者数（地理迁移候选主体）
    cur.execute(
        "SELECT COUNT(*) FROM (SELECT talent_id FROM ads_talent_experience "
        "WHERE city IS NOT NULL AND city<>'' GROUP BY talent_id "
        "HAVING COUNT(DISTINCT city)>=2) t")
    multi_city_talents = int(cur.fetchone()[0])
    cur.execute(
        "SELECT COUNT(*) FROM (SELECT talent_id FROM ads_talent_experience "
        "WHERE institution_id IS NOT NULL AND institution_id<>'' "
        "GROUP BY talent_id HAVING COUNT(DISTINCT institution_id)>=2) t")
    multi_inst_talents = int(cur.fetchone()[0])
    # ② 机构迁移检查：经历表机构→城市聚合，机构级多城市数（应=0，profile 静态单址）
    cur.execute(
        "SELECT COUNT(*) FROM (SELECT institution_id FROM ads_talent_experience "
        "WHERE institution_id IS NOT NULL AND institution_id<>'' AND city IS NOT NULL AND city<>'' "
        "GROUP BY institution_id HAVING COUNT(DISTINCT city)>=2) t")
    multi_city_institutions = int(cur.fetchone()[0])
    # ③ 示例轨迹 A：地理迁移路线（serial mover，站点=城市×年份）
    tid = "tal_a17fdb1ed9c84606bd947d3f7f75f2f2"
    cur.execute(
        "SELECT start_year, end_year, city, institution_name FROM ads_talent_experience "
        "WHERE talent_id=%s AND city IS NOT NULL AND city<>'' "
        "ORDER BY COALESCE(start_year, 9999)", (tid,))
    exp_route = [{"year": int(s) if s else None, "end": int(e) if e else None,
                  "city": c, "institution": i} for s, e, c, i in cur.fetchall()]
    # ④ 示例轨迹 B：学科变迁路线（event 面 RESEARCH_FIELD_CHANGE）
    cur.execute(
        "SELECT e.event_year, ff.name_en, tf.name_en FROM ads_talent_mobility_event e "
        "LEFT JOIN ads_discipline_field ff ON e.from_field_id=ff.field_id "
        "LEFT JOIN ads_discipline_field tf ON e.to_field_id=tf.field_id "
        "WHERE e.talent_id='tal_e2d780a9129748c09ca089218fd7c72b' "
        "AND e.mobility_type='RESEARCH_FIELD_CHANGE' ORDER BY e.event_year")
    field_route = [{"year": int(y), "from": f, "to": t} for y, f, t in cur.fetchall()]
    # ⑤ 事件面类型分布（地理型 vs 学科型覆盖）
    cur.execute("SELECT mobility_type, COUNT(*) FROM ads_talent_mobility_event GROUP BY mobility_type")
    types = {t: int(n) for t, n in cur.fetchall()}
    conn.close()

    assert multi_city_talents == 25434 and multi_inst_talents == 27458
    assert multi_city_institutions == 0  # 机构无迁移——部分支持的核心缺口证据
    assert len(exp_route) == 18 and exp_route[0]["city"] == "Paderborn"
    assert len(field_route) == 10 and field_route[0]["year"] == 2016
    assert types["RESEARCH_FIELD_CHANGE"] == 281117 and types["WORK_TO_WORK"] == 9276

    # gkx 侧复核（学者履历面行数）
    gconn = pymysql.connect(**GKX)
    gcur = gconn.cursor()
    gcur.execute("SET NAMES utf8mb4")
    gcur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar_work_experience")
    gkx_work_exp = int(gcur.fetchone()[0])
    gcur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    gkx_scholar = int(gcur.fetchone()[0])
    gconn.close()
    assert gkx_work_exp == 57117 and gkx_scholar == 21316

    out = {
        "metric_id": "M_SCIUI_P10_025",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1374",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1380",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:1390-1415",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:81-139",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/mockData.js:464-478",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "srs_anchor": "科技时空演进展示.md 序号 509（excel_row 512）「科研主体时空流动路径追踪」：用户选择机构或研究团队，支持基于时间轴自动绘制其地理迁移和学科变迁路线。交互式轨迹图和数据明细一键展示、导出",
            "note": "SRS 正名功能叶（509）；UI 区块同名挂载 :1374；本件为该叶 UI 落位",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:1374 SectionCard title=科研主体时空流动路径追踪；:1380 Select 主体选择器（RESEARCH_SUBJECTS 16 项 label=name（type））；:1390 WorldEvolutionMap route={stops: subjectRoute}；:1397-1415 迁移路线明细（末站红框红 Tag）",
            "ui_subjects": "mockData.js:81-139 RESEARCH_SUBJECTS=16 主体：10 机构/载体（无 trajectory，getSubjectRoute 返 []）+6 团队（sub-11~16 带 trajectory 3-4 站：年份+cityKey+note）",
            "ui_route_builder": "mockData.js:464-478 getSubjectRoute(subject, year)：trajectory.filter(year<=选择年).map(city 坐标+note)——站点={year, cityKey, cityName, lat, lng, note}",
            "ui_mock_note": "ui_demo_fallback：16 主体与站点序列均为 mock 编造（斯坦福 HAI/深智大模型团队等）；机构/载体项无轨迹（返空数组）——UI 自身即只对团队型主体画线",
            "jiuxin_experience_table": "ads_talent_experience（140,887 行；talent_id×experience_type×起止年×institution_id×city——学者地理时序）",
            "jiuxin_event_table": "ads_talent_mobility_event（298,384 行；mobility_type 三类：RESEARCH_FIELD_CHANGE 281,117/EDUCATION_TO_WORK 7,991/WORK_TO_WORK 9,276；from/to institution+location+field 双端）",
            "jiuxin_institution_profile": "ads_institution_profile（83,745 行）——静态单址（location_id/city_location_id 单值列），无迁移历史",
            "gkx_scholar_family": "dwd_scholar（21,316 行）/dwd_scholar_work_experience（57,117 行 org_name×起止时）——学者履历面（无城市列，机构名英文）",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx_snap["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "trajectory_carrier_counts",
                "value": {"multi_city_talents": multi_city_talents, "multi_inst_talents": multi_inst_talents,
                          "multi_city_institutions": multi_city_institutions},
                "formula": "COUNT(DISTINCT city)>=2 / COUNT(DISTINCT institution_id)>=2 分组计数",
                "source": "jiuxin ads_talent_experience / 同表机构粒度",
                "note": "学者维轨迹承载 25,434/27,458 人；机构维多城市=0——主体两维中机构维无迁移承载",
            },
            {
                "name": "sample_geo_route_serial_mover",
                "value": exp_route,
                "formula": "单学者经历按 start_year 排序站点序列（city×institution×年份）",
                "source": "jiuxin ads_talent_experience",
                "note": "示例 tal_a17f...：Paderborn(1991)→Atlanta(2001)→St Louis(2004)→Giessen(2005)→Stanford(2007)→New Haven(2008)→Osnabrück(2008)→Berlin(2011)→Tromsø(2019)→Munich(2020~) 18 行——地理迁移路线可绘制",
            },
            {
                "name": "sample_field_change_route",
                "value": field_route,
                "formula": "单学者 RESEARCH_FIELD_CHANGE 事件按 event_year 排序（from_field→to_field）",
                "source": "jiuxin ads_talent_mobility_event × ads_discipline_field",
                "note": "示例 tal_e2d7...：Chemistry→Agr&Bio(2016)→Engineering(2017)→...→Chemistry(2025) 十跳——学科变迁路线可绘制（SRS 509 双维后一半）",
            },
            {
                "name": "event_type_coverage",
                "value": types,
                "formula": "mobility_type 分组计数",
                "source": "jiuxin ads_talent_mobility_event",
                "note": "学科型事件 281,117 占 94.2%；地理型 WORK_TO_WORK 仅 9,276（from_location 缺失 281,117 行为学科型事件无地理端）",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 trajectory/route/track/replay/flow_path 词族", "source": "dev",
             "hits": ["gkxlumenx.sys_route_conf"],
             "note": "系统路由配置表（技术 route 非主体轨迹）——0 承载"},
            {"probe": "gkx 280 表 trajectory 词族 + 团队/机构迁移面", "source": "gkx",
             "hits": [],
             "note": "轨迹词族 0 命中；dwd_scholar_work_experience 57,117 行为学者履历（可推个体轨迹，无城市列需机构名关联）；无团队实体表"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）trajectory 词族 + 机构迁移历史", "source": "jiuxin",
             "hits": ["ads_talent_experience", "ads_talent_mobility_event"],
             "primary": "ads_talent_experience",
             "note": "正结论：学者维轨迹双面（经历时序+事件流）；负结论：机构 profile 静态单址（多城市机构=0），团队实体表无——主体三分维（机构/团队/学者）仅学者维可承载"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：SRS 509 主体=机构或研究团队。机构维——经历表机构粒度多城市聚合=0（profile 静态单址，机构无迁移历史承载）；团队维——三源无团队实体表（RESEARCH_SUBJECTS 6 团队纯 mock）；学者维——经历面 25,434 多城市学者+事件面 281,117 学科变迁，地理迁移与学科变迁双路线可绘制。三主体维仅一维（学者）齐备，关键维度（机构/团队整体迁移）缺失，判部分支持。",
            "可交付子项：主体选择器可改挂领军人才/多段履历学者（25,434 候选）；地理迁移路线（experience 时序）与学科变迁路线（RESEARCH_FIELD_CHANGE 流）双维均可时间轴绘制——SRS 509 的「地理迁移和学科变迁」双语义在学者粒度全通。",
            "从缺子项：机构整体迁移（如院所迁址）无承载——机构在经历表中的城市为其人才任职城市聚合=0 个多城市机构，profile 无历史地址列；团队整体迁移（如 sub-11 深智团队南迁语义）无实体表。",
            "gkx 备选路径：dwd_scholar_work_experience 57,117 行（21,316 学者）可推个体轨迹但 org_name 英文名无城市列，需先关联机构地理；精度低于 jiuxin 现成 city 列——本件主源 jiuxin。",
            "与 P10_022/023 同根三面；本件为 507 族第三件（主体路径维），与 509 叶一一对应。",
        ],
        "base_years_used": ["1991", "2025"],
        "base_years_missing": [],
        "base_years_note": "轨迹为个体全程时序（示例 1991-2025 全程可追溯）；事件面 2000-2025。基期为主体各自生涯首站，无全局基期——base_years_used 登记示例轨迹起止年。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "140887", "140,887", "298384", "298,384", "281117", "281,117", "9276", "9,276",
            "7991", "7,991", "83745", "83,745", "25434", "25,434", "27458", "27,458",
            "21316", "21,316", "57117", "57,117", "16", "10", "6", "18", "0",
            "1991", "2016", "2025", "542", "280", "218",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| multi_city_talents:", multi_city_talents,
          "| multi_city_institutions:", multi_city_institutions,
          "| exp_route stops:", len(exp_route), "| field_route stops:", len(field_route))


if __name__ == "__main__":
    main()
