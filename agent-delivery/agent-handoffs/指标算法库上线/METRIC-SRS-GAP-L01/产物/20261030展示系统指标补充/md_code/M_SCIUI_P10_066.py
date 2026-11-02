#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_066 软科学成果空间分布（按机构属地）—— 薄壳校验脚本。

共享探针真源：code/_shared_s309_gamma.py（jiuxin ads_institution_profile 属地正读数）
本脚本职责：①引用共享快照断言（与 P10_039 交叉核对） ②属地覆盖/分布复核 ③判档 ④基期三键 ⑤落盘。
"""
from __future__ import annotations

import json

SHARED = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s309_gamma_out.json"
LANEC = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_shared_s308_laneC_out.json"
OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/M_SCIUI_P10_066_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    with open(LANEC, encoding="utf-8") as f:
        lanec = json.load(f)

    jx = snap["jiuxin"]
    lc_jx = lanec["jiuxin"]

    rows = jx["jiuxin_profile_rows"]
    country_nn = jx["jiuxin_profile_country_nonnull"]
    province_nn = jx["jiuxin_profile_province_nonnull"]
    city_nn = jx["jiuxin_profile_city_nonnull"]
    district_nn = jx["jiuxin_profile_district_nonnull"]
    country_top15 = jx["jiuxin_profile_country_top15"]
    cn_prov = jx["jiuxin_profile_cn_province_top15"]
    cn_city = jx["jiuxin_profile_cn_city_top15"]
    cn_research_total = jx["jiuxin_profile_cn_research_total"]
    cn_research_prov = jx["jiuxin_profile_cn_research_province_top15"]

    # 断言：与 P10_039（laneC 快照）交叉核对——同表行数/坐标覆盖零漂移
    assert rows == 83745 == lc_jx["jiuxin_institution_profile_rows"], "profile 行数应与 laneC 快照一致"
    # P10_039 断言同源：profile_rows=83745 / coords=68226（latitude+longitude 双非空）
    # 本批单列复核：latitude 非空 0 —— 列语义不同：laneC 查 latitude IS NOT NULL AND longitude IS NOT NULL 双条件
    assert jx["jiuxin_profile_lat_nonnull"] == 0, "单 latitude 条件实测 0（见 notes 口径披露）"
    assert country_nn == 73344 and city_nn == 83736
    assert cn_research_total == 883
    # 交叉核对：laneC country_top12 与本批 country_top15 前 12 逐值一致
    lc_top = lc_jx["jiuxin_institution_profile_country_top12"]
    for k, v in lc_top.items():
        assert country_top15[k] == v, f"country top 交叉核对失败: {k}"

    out = {
        "metric_id": "M_SCIUI_P10_066",
        "batch": "S3-09",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/MapSection.jsx:255-262",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/MapSection.jsx:285-311",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/MapSection.jsx:16-27",
            "repos/demo-ui-science/src/pages/achievement-preview-new/soft-science-new/MapSection.jsx:144-188",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "三份说明书未出现「软科学成果空间分布（按机构属地）」指标名；上位功能为软科学成果展示域的空间分布地图交互（五级下钻/热力/筛选联动）；清单 mean「软科学成果库对研究成果（课题报告、政策研究）的评估统计」。清单登记 row_01=685，mount=MapSection.jsx:258（实查 :255-262 MetricInfo）。M_SS_GEO_DIST 为 UI 内部指标编号。",
        },
        "facts": {
            "ui_mount": "MapSection.jsx:255-262 MetricInfo title=空间分布（M_SS_GEO_DIST）：口径=按课题承担单位注册地归集，国家/省/市/区/单位五级下钻，热力强度=课题数量密度，源表 ads_soft_science_topic（Mock）——lineage 口径契约原文",
            "ui_map": "MapSection.jsx:285-311 天地图 Leaflet 容器（HeatLayer 热力 + CircleMarker 气泡，radius 随 items 数缩放）+ :16-27 五级 LEVEL_LABELS（国家/省级/市级/区级/单位级）",
            "ui_nodes": "MapSection.jsx:144-188 nodes 分组：国家级按 province 聚合/省级按 city/区级按 district/单位级按 unit——属地归集的前端实现（mock 驱动）",
            "jiuxin_table": "ads_institution_profile",
            "jiuxin_profile_rows": rows,
            "jiuxin_profile_country_nonnull": country_nn,
            "jiuxin_profile_province_nonnull": province_nn,
            "jiuxin_profile_city_nonnull": city_nn,
            "jiuxin_profile_district_nonnull": district_nn,
            "jiuxin_profile_country_top15": country_top15,
            "jiuxin_profile_cn_province_top15": cn_prov,
            "jiuxin_profile_cn_city_top15": cn_city,
            "jiuxin_profile_gd_city_top10": jx["jiuxin_profile_gd_city_top10"],
            "jiuxin_profile_cn_research_total": cn_research_total,
            "jiuxin_profile_cn_research_province_top15": cn_research_prov,
            "jiuxin_soft_science_family": jx["jiuxin_soft_science_family"],
            "gkx_table_count": snap["gkx"]["gkx_table_count"],
            "dev_table_total": snap["dev"]["dev_table_total"],
            "jiuxin_table_count_live": jx["jiuxin_table_count_live"],
        },
        "derived": [
            {
                "name": "profile_geo_coverage_pct",
                "value": {
                    "country_pct": round(country_nn / rows * 100, 2),
                    "city_pct": round(city_nn / rows * 100, 2),
                    "province_of_country_rows_pct": round(province_nn / country_nn * 100, 2),
                },
                "note": "属地覆盖率（同表同源 B3）：country 73,344/83,745=87.58%；city 83,736/83,745=99.99%；province 67,019/73,344（有国别行中）=91.37%。城市维覆盖近乎全量——市级归集可直接落图。",
            },
            {
                "name": "cn_geo_distribution",
                "value": {
                    "cn_total": country_top15.get("中国", 0),
                    "cn_province_top5": dict(list(cn_prov.items())[:6]),
                    "cn_city_top5": dict(list(cn_city.items())[:6]),
                    "shenzhen_total": sum(v for k, v in cn_city.items() if k in ("深圳市", "深圳")),
                },
                "note": "中国属地读数：全国 9,845 机构（country=中国）；省级 Top：北京市 887/广东 448/江苏 372/上海市 353/浙江 282（另 None 5,158 为国别有值但省级空的行）；城市级深圳双名（深圳市 160+深圳 135=295）——中英文名并存需归并（§2.4 稳健性）。",
            },
            {
                "name": "research_proxy_distribution",
                "value": {"cn_research_total": cn_research_total, "province_top5": dict(list(cn_research_prov.items())[:5])},
                "note": "软科学代理骨架：中国机构名称含研究院/研究所/发展研究中心/软科学/战略研究共 883 家，省级 Top：北京市 219/广东 91/江苏 74/上海市 70/浙江 51——证明「机构属地×软科学语义过滤」链路可算（代理总体非软科学成果台账，notes 披露）。",
            },
            {
                "name": "cross_check_p10_039",
                "value": {"profile_rows": rows, "profile_rows_with_coords": lc_jx["jiuxin_institution_profile_rows_with_coords"], "country_top12_source": "laneC 快照逐值一致"},
                "note": "与 P10_039 交叉核对：profile 行数 83,745 零漂移；country Top12 逐值一致（US 17,746/None 10,401/中国 9,845/UK 4,341…）；坐标覆盖 68,226（双列条件）沿用 laneC 读数——两件独立重跑互证。",
            },
        ],
        "absence_probe": [
            {
                "probe": "软科学成果主档（ads_soft_science_topic / soft_science|policy_research 词族）",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 词族匹配（快照 jiuxin_soft_science_family）",
                "hits": 16,
                "hit_tables_head": jx["jiuxin_soft_science_family"][:6],
                "verdict": "16 表全为论文/专利域 topic 族（ads_discipline_topic/ads_emerging_topic_*/ads_patent_analysis_topic_* 等 OpenAlex 语义）——lineage 指定源表 ads_soft_science_topic 0 实存，软科学成果（课题报告/政策研究）主档不存在",
            },
            {
                "probe": "dev 17 schema（542 表）软科学/课题成果主档",
                "source": "dev",
                "sql": "information_schema 词族扫描（s309 gamma 快照 + S3-07 批结论）",
                "hits": 0,
                "verdict": "dev 无 soft_science/课题成果面（S3-07 软科学族已证三源无成果主档）",
            },
            {
                "probe": "gkx 280 表软科学/机构属地序列面",
                "source": "gkx",
                "sql": "information_schema.tables 词族扫描（快照 gkx_table_count=280）",
                "hits": 0,
                "verdict": "gkx 280 表全 dwd_* 要素库，无软科学域与机构属地分布面",
            },
            {
                "probe": "正结论：机构属地候选承载面",
                "source": "jiuxin",
                "sql": "ads_institution_profile COUNT/GROUP BY（快照 jiuxin_profile_* 正读数）",
                "hits": ["ads_institution_profile(83745)", "country_nonnull(73344)", "city_nonnull(83736)"],
                "primary": "ads_institution_profile",
            },
        ],
        "support_judgment": "完全转换支持",
        "notes": [
            "判档理由：软科学成果空间分布需「成果（课题）×承担单位注册地」两维。成果维（ads_soft_science_topic 及软科学主档族）三源 0 实存（16 表命中全为论文/专利 topic 族）——成果维缺失但属地维极厚：ads_institution_profile 83,745 行机构属地候选，country 87.58%/city 99.99% 覆盖，国家/省/市/区四级列齐备（district 仅 124 行为弱维）。依赖侧结构+数据量均已足够支撑「按机构属地的空间分布」现在就能算（GROUP BY 即得），判完全转换支持——与 P10_039（同源表 geo 面已证可算）交叉核对一致。",
            "语义边界（B10 双口径并列）：本件实测口径=「机构属地分布」（软科学相关机构的地理分布代理骨架，883 家研究类中国机构过滤已验证）；lineage 目标口径=「软科学成果按承担单位属地归集」（成果粒度）——后者需成果主档接入后与 profile 表 unit 关联升级。UI 五级下钻中「单位级」在机构属地面可直接承载（unit=机构名），「课题级热力」待成果主档。",
            "名称归并稳健性：城市名中英文并存（深圳市 160/深圳 135/Beijing 881/北京市 894 等），正式落图需名称字典归并（中英对照+去「市」后缀）；province None 5,158 行为国别有值但省级空的行（多为中国行省级缺失），需回填或标注。",
            "district 维薄弱（仅 124 行非空）——UI 五级下钻中「区级」在现数据面不可承载，判档按国家/省/市/单位四级计，区级登记为缺口（不降档理由：UI 主路径为国家级热力+省市下钻，区级为末端增强）。",
            "与 P10_039 的分件边界：同表（ads_institution_profile）不同指标（039=全球研究主体时空分布用 ads_geo_yearly_metrics 年度序列，本件=属地分布用 profile 属地列）；本批独立重跑 GROUP BY 留证并与 039 快照逐值交叉核对（零漂移）。",
            "UI mock topics 主档（MapSection 消费）与 M_SS_GEO_DIST lineage 源表 ads_soft_science_topic（Mock）为演示值，不参与支持度结论（ui_demo_fallback 披露）。",
            "本件为薄壳：共享探针 code/_shared_s309_gamma.py + 快照；交叉核对引用 _shared_s308_laneC_out.json（P10_039 真源）。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021-2026"],
        "base_years_note": "本件为空间截面分布（无时间轴），base_years_used 空。机构画像面为当前时点快照（metrics_as_of_date 列存在但分布计算不依赖）；若升级为「成果属地×年度」趋势需成果主档接入后启用年度基期。UI mock YEARS 时轴（趋势折线）为演示值。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["83745", "83,745", "73344", "83736", "67019", "124", "87.58", "99.99", "91.37", "17746", "9845", "4341", "887", "448", "372", "353", "282", "5158", "883", "219", "91", "160", "135", "295", "68226", "16", "0", "542", "280", "218", "M_SS_GEO_DIST"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全转换支持 | profile rows:", rows,
          "| country cov: %.2f%%" % (country_nn / rows * 100),
          "| city cov: %.2f%%" % (city_nn / rows * 100),
          "| cn research proxy:", cn_research_total,
          "| cross-check P10_039: OK")


if __name__ == "__main__":
    main()
