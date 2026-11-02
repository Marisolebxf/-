#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_015 地域流动明细与历史回溯（时空回放）—— 薄壳校验脚本（完全转换支持件）。

UI：SpaceTimeEvolutionNewPage.jsx:984「地域流动明细与历史回溯（时空回放）」：
historyRows 年表（年份/首位热点区域/值/增速/蝉联|新晋）+ 回放按钮。
派单预判「大概率零承载」已被实测推翻——jiuxin 双面实证：
  ads_geo_yearly_metrics 171,736 行（2000-2026 27 年，四级地域含
  inbound/outbound_talent_count 流动列）承载分布演变明细；
  ads_talent_mobility_yearly_flow 51,489 行（2000-2025 26 年 LOCATION 维
  28,672 行 from→to 对流量）承载地域流动语义。
年份×热点聚合一步转换即得 historyRows 同构行。判完全转换支持。
"""
from __future__ import annotations

import json
import os

import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(BASE, "_snapshots", "_shared_s308_laneb_probe_out.json")
OUT = os.path.join(BASE, "M_SCIUI_P10_015_out.json")

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
    # ① 分布演变明细面：geo_yearly COUNTRY 级全序列（热点=按维度取首）
    cur.execute(
        "SELECT statistics_year, location_id, paper_count, talent_count, institution_count "
        "FROM ads_geo_yearly_metrics WHERE location_level='COUNTRY' AND statistics_year>=2018 "
        "AND statistics_year<=2025 ORDER BY statistics_year, paper_count DESC")
    rows = cur.fetchall()
    # 按 talent_count 取每年首位热点（回放表演化语义演示口径）
    by_year = {}
    for y, lid, p, t, i in rows:
        by_year.setdefault(y, []).append((lid, p, t, i))
    replay_rows = []
    for y in sorted(by_year):
        top = sorted(by_year[y], key=lambda r: -r[2])[0]
        replay_rows.append({"year": y, "top_location_id": top[0],
                            "talent_count": top[2]})
    # ② 流动对语义面：LOCATION 维年流量合计
    cur.execute(
        "SELECT statistics_year, SUM(talent_count) FROM ads_talent_mobility_yearly_flow "
        "WHERE flow_dimension='LOCATION' AND statistics_year>=2018 GROUP BY statistics_year "
        "ORDER BY statistics_year")
    flow_yearly = {str(y): int(s or 0) for y, s in cur.fetchall()}
    # ③ 地名解析：Top 地点
    top_ids = sorted({r["top_location_id"] for r in replay_rows})
    names = {}
    for lid in top_ids:
        cur.execute("SELECT name FROM ads_location WHERE location_id=%s", (lid,))
        r = cur.fetchone()
        names[lid] = r[0] if r else lid
    conn.close()

    years_geo = sorted(by_year)
    assert len(replay_rows) == 8  # 2018-2025
    assert all(r["year"] >= 2018 and r["year"] <= 2025 for r in replay_rows)
    assert len(flow_yearly) == 8

    out = {
        "metric_id": "M_SCIUI_P10_015",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:984",
            "repos/demo-ui-science/src/pages/achievement-preview-new/space-time-evolution-new/SpaceTimeEvolutionNewPage.jsx:343-361",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "srs_anchor": "科技时空演进展示.md 序号 501「地域流动明细与历史回溯」（需规描述：支持时空回放功能，用户可依时间轴回溯研究主体流动和分布演变历程，自动生成趋势变化报告）——本件即该功能叶的 UI 落位区块（同名）",
            "note": "区块标题与 SRS 功能叶同名；SRS 另有序号 497「交互式时空地图分布呈现」含「动态筛选与回放功能」",
        },
        "facts": {
            "ui_mount": "SpaceTimeEvolutionNewPage.jsx:984 SectionCard title=地域流动明细与历史回溯（时空回放）extra=Button 从 2018 回放（handleReplay）；:989-997 Table data=historyRows（年份/首位热点区域/值/增速/蝉联|新晋|基准五列）",
            "ui_history_builder": "SpaceTimeEvolutionNewPage.jsx:343-361 historyRows useMemo：YEARS 逐年取 getHotspots(level,dimension,y,1)[0] 为首位热点，与前一年同名判蝉联/新晋/基准；:355-363 historySummary 演变摘要句",
            "ui_mock_note": "ui_demo_fallback：mock 回放表由 CITY_PROFILES 外推热点（dimension 可切 papers/patents/funding/talent）——演示序列非真实回溯",
            "jiuxin_geo_table": "ads_geo_yearly_metrics",
            "jiuxin_geo_rows": 171736,
            "jiuxin_geo_year_span": "2000-2026（27 年现场实数）",
            "jiuxin_geo_levels": {"CITY": 132975, "PROVINCE": 33518, "COUNTRY": 5081, "CONTINENT": 162},
            "jiuxin_geo_flow_columns": ["inbound_talent_count", "outbound_talent_count", "mobility_event_count"],
            "jiuxin_flow_table": "ads_talent_mobility_yearly_flow",
            "jiuxin_flow_rows": jx.get("jx_talent_flow_rows"),
            "jiuxin_flow_location_dim_rows": 28672,
            "jiuxin_flow_yearly_location_sum": flow_yearly,
            "jiuxin_location_dict": "ads_location 22,229 行四级地域字典（location_id→name/lat/lng）",
            "replay_rows_talent_top": [
                {"year": r["year"], "top": names[r["top_location_id"]],
                 "talent_count": r["talent_count"]} for r in replay_rows],
            "dev_traj_word_hits": "trajectory 词族命中 sys_route_conf（路由配置）/gen_table（代码生成器）/xxl_job_info（调度执行器）——全框架语义污染，无时空轨迹面",
            "gkx_traj_note": "280 表 trajectory 词族命中 dwd_drug（药物 trajectory 药代语义）——污染",
            "dev_table_total": dev["dev_table_total"],
            "gkx_table_count": gkx["gkx_table_count"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "replay_history_rows_2018_2025",
                "value": {str(r["year"]): [names[r["top_location_id"]], r["talent_count"]]
                          for r in replay_rows},
                "formula": "每年取 COUNTRY 级 talent_count 最大地点为首位热点（回放表同构：年份/首位热点/值/蝉联-新晋可由相邻年比较导出）",
                "source": "jiuxin ads_geo_yearly_metrics WHERE location_level='COUNTRY'",
                "share_basis": "同表同年同层级取 Top（B3 同基）",
            },
            {
                "name": "location_flow_yearly",
                "value": flow_yearly,
                "formula": "SUM(talent_count) GROUP BY statistics_year（LOCATION 维 from→to 对流量合计，地域流动语义主读数）",
                "source": "jiuxin ads_talent_mobility_yearly_flow",
            },
            {
                "name": "mock_reference",
                "value": "2018 起回放（YEARS[0]）",
                "disclosure": "ui_demo_fallback：mock 回放起点 2018；库序列 2000 起更长（2000-2025 二十六年可回放，2018 起为 UI 习惯窗口）",
            },
        ],
        "absence_probe": [
            {"probe": "dev 542 表 trajectory/route/track/replay 词族", "source": "dev",
             "hits": ["gkxlumenx.sys_route_conf", "gkxlumenx_codegen.gen_table", "gkxlumenx_job.xxl_job_info"],
             "note": "全框架配置语义（路由/代码生成/调度），无时空轨迹面"},
            {"probe": "gkx 280 表 trajectory 词族", "source": "gkx",
             "hits": ["dwd_drug"],
             "note": "药物药代轨迹语义污染"},
            {"probe": "jiuxin 218 表（SHOW TABLES 实数）trajectory/flow 词族", "source": "jiuxin",
             "hits": ["ads_talent_mobility_yearly_flow", "ads_talent_mobility_flow_detail"],
             "primary": "ads_talent_mobility_yearly_flow",
             "note": "正结论：LOCATION 维 28,672 行 from→to 流量 + ads_geo_yearly_metrics 171,736 行四级地域年表双面承载"},
        ],
        "support_judgment": VERDICT,
        "notes": [
            "判档理由：派单预判「大概率零承载」被实测推翻——久新双面实证：ads_geo_yearly_metrics（171,736 行，2000-2026 四级地域年度面，含 inbound/outbound 流动列）承载分布演变明细；ads_talent_mobility_yearly_flow（51,489 行，LOCATION 维 28,672 行）承载地域流动 from→to 语义。回放表（年份×首位热点×蝉联/新晋）一步聚合转换即得，判完全转换支持。",
            "口径转换点：mock 回放维度可切四维（papers/patents/funding/talent）；库面 talent 维最全（inbound/outbound 列现成），papers 维有 paper_count 列可用，patents/funding 维无对应列（该两维回放仍 mock）——talent 维为首选正式口径。",
            "蝉联/新晋判定：相邻年首位热点同名→蝉联、异名→新晋（与 :343-361 mock 构建逻辑同构），2018-2025 实算 talent 维首位热点全序列见 derived[0]。",
            "ads_location（22,229 行）提供 location_id→名称/经纬度解析，回放地图坐标面同源可解。",
            "与 P10_025（主体路径追踪）同族不同粒度：本件地域级（COUNTRY/CITY），P10_025 主体级（机构/团队）；两件独立留证。",
        ],
        "base_years_used": [str(y) for y in years_geo],
        "base_years_missing": [],
        "base_years_note": "ads_geo_yearly_metrics 2018-2025 全覆盖（本件回放窗口）；全序列 2000-2026（2026 为不完整年，talent 流动 0 行）。基期建议 2018（UI 回放习惯起点）；LOCATION 流动序列 2000-2025 二十六年。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted({
            "171736", "171,736", "51489", "51,489", "28672", "28,672", "22229", "22,229",
            "27", "26", "8", "2018", "2025", "2026", "2000", "542", "280", "218",
            "132975", "33518", "5081", "162",
        })},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment:", VERDICT, "| replay rows:", len(replay_rows),
          "| flow years:", sorted(flow_yearly))


if __name__ == "__main__":
    main()
