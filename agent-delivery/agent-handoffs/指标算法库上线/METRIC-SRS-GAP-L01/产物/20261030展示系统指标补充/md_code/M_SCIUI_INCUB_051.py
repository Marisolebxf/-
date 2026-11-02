#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_INCUB_051 路径强度变化（较上期）—— 薄壳校验脚本（负结论件）。

UI：spaceTimeEvolutionMock.js:638 图表卡「路径强度变化」（values 32/41/52/67/76）
+ 主要流向排行 strengthChange 变化徽标（SpaceTimeEvolutionPage.jsx:808-810
formatSignedDelta，mock +12/+6/-4）。变化=路径强度双时点差。
探针：同 INCUB_050 根因——区域对路径强度面三源零承载（词族 2+2 表域错位），
双时点强度序列连带无从谈起；无现成「变化」结果面。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_lane_a_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_INCUB_051_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)

    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]
    assert dev["table_total"] == 542 and gkx["table_count"] == 280
    assert jx["table_count_live"] == 218
    assert dev["word_path"] == ["gkxlumenx.sys_route_conf", "gkxlumenx_ads.chain_roadmap"]
    assert gkx["word_path"] == []
    assert jx["word_path"] == ["ads_research_problem_research_path", "ads_technology_evolution_path_step"]

    out = {
        "metric_id": "M_SCIUI_INCUB_051",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:638",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx:808-810",
            "repos/demo-ui-science/src/pages/achievement-preview/modules/space-time-evolution/mock/spaceTimeEvolutionMock.js:319",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「路径强度变化」指标名三份说明书未出现；INCUB 清单 row_01=606（清单语义注同 050 知识图谱域，UI 实挂载=路径强度环比徽标+图表卡）；挂载位=spaceTimeEvolutionMock.js:638（清单定位）。",
        },
        "facts": {
            "ui_mount_chart": "spaceTimeEvolutionMock.js:637-643 charts[1] { key: path-strength, title: 路径强度变化, metric: 76, unit: 条, badge: 高强度 21 条, values: [32,41,52,67,76] }——五点路径计数序列（注：该 charts 数组未被组件直接渲染，活跃渲染链为 buildDistributionCharts 时空事件趋势，:721-729——mock 卡登记为清单挂载位）",
            "ui_mount_badge": "SpaceTimeEvolutionPage.jsx:785-813 主要流向排行（buildFlowRanking :733-748）每项强度旁变化徽标：formatSignedDelta(strengthChange)，tone up/down/flat（:788/:808-810）——路径强度双时点差的真实消费点",
            "ui_status_semantics": "getPathStatusLevel（:482-490）以 strengthChange 符号三态分档：>0=enhanced/<0=declining/=0=stable——变化值驱动路径状态筛选（pathStatusValues）",
            "ui_mock_changes": "mock paths[].strengthChange（:319 南山->宝安 +12 / :360 南山->坪山 +6 / :399 光明->南山 -4）——较上期变化演示值",
            "ui_mock_note": "mock values 32/41/52/67/76（图表五点）与 +12/+6/-4（徽标）为演示常量，不参与支持度结论（ui_demo_fallback）；两处口径不同（图表=路径条数序列/徽标=强度差）",
            "dev_table_total": dev["table_total"],
            "dev_path_word_tables": dev["word_path"],
            "gkx_table_count": gkx["table_count"],
            "gkx_path_word_tables": gkx["word_path"],
            "jiuxin_table_count_live": jx["table_count_live"],
            "jiuxin_path_word_tables": jx["word_path"],
            "jiuxin_path_note": "久新 path 词族 2 表（research_path/evolution_path_step）为技术主题演化域，无区域对与流动语义，无强度时序列——双时点差无从计算",
            "named_in_srs": False,
        },
        "derived": [
            {
                "name": "path_strength_change_period_over_period",
                "value": None,
                "numerator": None,
                "denominator": None,
                "note": "路径强度变化 = strength(t) - strength(t-1)（较上期，区域对路径强度双时点差）。前提=路径强度双时点序列——区域对路径强度面三源零承载（INCUB_050 同根因）→ 序列不存在即变化不可计算，负结论 null 登记",
            },
        ],
        "absence_probe": [
            {"probe": "dev path 词族（542 表）",
             "source": "dev", "sql": "information_schema 表名扫描（快照）",
             "hits": 2,
             "hit_detail": "sys_route_conf（系统路由，语义错位）/chain_roadmap（产业链路线图 0 行，域错位）——无区域对路径强度时序面"},
            {"probe": "gkx path 词族（280 表）",
             "source": "gkx", "sql": "information_schema 表名扫描（快照）",
             "hits": 0, "note": "gkx word_path=[]"},
            {"probe": "久新 path 词族（SHOW TABLES 实数 218 表）",
             "source": "jiuxin", "sql": "SHOW TABLES + 词族扫描（快照）",
             "hits": 2,
             "hit_detail": "ads_research_problem_research_path/ads_technology_evolution_path_step 技术演化域——无区域对、无强度列、无时序双点"},
            {"probe": "现成「变化」结果面（环比字段）",
             "source": "三源", "sql": "词族扫描 + 列语义核（快照）",
             "hits": 0,
             "hit_detail": "三源无 path_strength_change/yoy/环比 同构列；UI strengthChange 为 mock 自设字段"},
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：变化指标的前提是被变化量（路径强度）有双时点序列。区域对路径强度面三源零承载（INCUB_050 已证同根：dev 2 表域错位/gkx 0/久新 2 表技术演化域），强度序列不存在→双时点差无从计算；三源亦无现成环比/变化结果面。前提缺位即变化指标整体从缺。",
            "UI 两处挂载口径不同：mock :638 图表卡「路径强度变化」实为路径条数序列（32→76 条，unit=条）；排行徽标 strengthChange 才是强度差（+12/+6/-4）——清单挂载位（mock :638）与本件语义（较上期变化）以徽标链为准留证。",
            "同族关系：INCUB_050（强度本体）/INCUB_052（抬升幅度）同 mock paths[].score/strengthChange 字段族——三件独立留证，判档同根（完全不支持）。",
            "升档路径：区域对强度面落库（双时点序列）→ 变化=一步差分（完全转换支持）；与 050 共用升档路径。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "变化需双时点强度序列；三源无强度面即无序列；mock 五点（32-76）与徽标（+12/+6/-4）均无年度基期语义。",
        "ctx_refs": {"note": "正文引用型数字登记", "refs": sorted([
            "76", "32", "41", "52", "67", "12", "6", "-4", "21", "542", "280", "218", "2", "0"])},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | 强度序列三源零承载，双时点差无从计算（INCUB_050 同根）")


if __name__ == "__main__":
    main()
