#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS-L2-DS09-SEED-L01 · 科技发展规划（DS-09）28+1 表灌数脚本（Python 一次性，D18）

对应数据流图 TS-DS09-OV-DATAFLOW-01 的「种子提取脚本 → ADS」链路：
  extract_seed.mjs（node import 事实源 dump JSON）→ 本脚本转换 → gkxlumenx_ads 28 张 ts_plan_* 表
  + gkxlumenx 主库 sys_user_planning_push_record（只建表，0 行，不 TRUNCATE 不 INSERT）

行数契约（三份分册实测冻结）：
  OV  8 表 244 行：hot_tech 8 / series 128 / metric_system 30 / tracking_event 8 /
                   tracking_point 35 / local_adv 19 / talent_flow 16 / direction_warning 0（禁灌）
  KEY 9 表  61 行：key_area 3 / carrier 22 / carrier_type 6 / district_baseline 6 /
                   competitiveness 5 / dimension 5 / benchmark 5 / land 6 / plan 3
  RES 11 表 70 行：field 5 / company 7 / overlap 6 / overlap_rule 3 / time_factor 3 /
                   grade 4 / overlap_benchmark 3 / graph_node 14 / graph_edge 13 /
                   insight 4 / report_template 8

用法：
  python seed_ts_plan.py --dry-run        # 只构建行+跑断言+打印行数与 NULL 分布，不落库
  python seed_ts_plan.py --apply-ddl      # 先 DROP+CREATE 全部 29 表（幂等重建），再灌数
  python seed_ts_plan.py                  # 直接 TRUNCATE+INSERT（幂等）
  python seed_ts_plan.py --re-extract     # 强制重跑 node 提取（seed_dump.json 缺失时自动跑）

连接：环境变量 INNOV_MYSQL_* / GKX_MYSQL_*（真源 agent-handoffs/算法库联调-ALGO-LIB/
algo-mysql-connection-info.md；密码不进脚本，必须经 INNOV_MYSQL_PASSWORD/GKX_MYSQL_PASSWORD）。
禁灌铁律（断言）：direction_warning 0 行；overlap 恰 6 行（15 对中 9 空对不灌）；
图谱专家类节点 0；carrier 22 行 land_benefit 全 NULL；grade threshold_low 80/65/45/0
且 is_draft=1；insight plan_id 序列 a/b/c/b。
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime

BASE = pathlib.Path(__file__).resolve().parent
GKX_ROOT = pathlib.Path(os.environ.get("GKX_ROOT") or str(BASE.parents[2]))
SEED_DUMP = BASE / "seed_dump.json"
DDL_ADS = BASE / "ddl" / "01_gkxlumenx_ads_ts_plan.sql"
DDL_PUSH = BASE / "ddl" / "02_gkxlumenx_sys_user_planning_push_record.sql"

ADS_DB = os.environ.get("TS_PLAN_ADS_DB", "gkxlumenx_ads")
MAIN_DB = os.environ.get("TS_PLAN_MAIN_DB", "gkxlumenx")

# 只灌数的 28 张表（direction_warning 与 push_record 不在其中：零行表零语句）
ADS_TABLES = [
    # OV
    "ts_plan_hot_tech", "ts_plan_hot_tech_series", "ts_plan_metric_system",
    "ts_plan_tracking_event", "ts_plan_tracking_point", "ts_plan_local_adv",
    "ts_plan_talent_flow",
    # KEY
    "ts_plan_key_area", "ts_plan_key_area_carrier", "ts_plan_key_area_carrier_type",
    "ts_plan_key_area_district_baseline", "ts_plan_key_area_competitiveness",
    "ts_plan_key_area_dimension", "ts_plan_key_area_benchmark",
    "ts_plan_key_area_land", "ts_plan_key_area_plan",
    # RES
    "ts_plan_research_field", "ts_plan_research_company", "ts_plan_research_overlap",
    "ts_plan_research_overlap_rule", "ts_plan_research_time_factor",
    "ts_plan_research_grade", "ts_plan_research_overlap_benchmark",
    "ts_plan_research_graph_node", "ts_plan_research_graph_edge",
    "ts_plan_research_insight", "ts_plan_research_report_template",
]
EXPECTED_COUNTS = {
    "ts_plan_hot_tech": 8, "ts_plan_hot_tech_series": 128, "ts_plan_metric_system": 30,
    "ts_plan_tracking_event": 8, "ts_plan_tracking_point": 35, "ts_plan_local_adv": 19,
    "ts_plan_talent_flow": 16,
    "ts_plan_key_area": 3, "ts_plan_key_area_carrier": 22,
    "ts_plan_key_area_carrier_type": 6, "ts_plan_key_area_district_baseline": 6,
    "ts_plan_key_area_competitiveness": 5, "ts_plan_key_area_dimension": 5,
    "ts_plan_key_area_benchmark": 5, "ts_plan_key_area_land": 6,
    "ts_plan_key_area_plan": 3,
    "ts_plan_research_field": 5, "ts_plan_research_company": 7,
    "ts_plan_research_overlap": 6, "ts_plan_research_overlap_rule": 3,
    "ts_plan_research_time_factor": 3, "ts_plan_research_grade": 4,
    "ts_plan_research_overlap_benchmark": 3, "ts_plan_research_graph_node": 14,
    "ts_plan_research_graph_edge": 13, "ts_plan_research_insight": 4,
    "ts_plan_research_report_template": 8,
}

# KEY §0.2 / §4.3：7 载体未挂集群白名单（反查结果 ≠ 白名单即报错回滚，防种子漂移）
UNCLUSTERED_WHITELIST = {"L001", "L004", "P003", "P005", "I003", "I004", "A002"}
# KEY §2.6 / §3：dim_label → dim_key 映射（U8-1 建议键，M0+数据侧拍板不同则改映射不改表）
DIM_KEY_MAP = {
    "创新资源": "innovation_resources", "科研产出": "research_output",
    "产业竞争力": "industry_competitiveness", "人才支撑": "talent_support",
    "开放协同": "open_collaboration",
}
# RES §2-6：grade threshold_low U3 建议值（80/65/45/0），is_draft=1 待 M0 终冻
GRADE_THRESHOLD_LOW = {"lead": 80, "advantage": 65, "catching": 45, "potential": 0}
# RES 图谱类别：demo category → (category_key, category_label)；demo「专家」(4) 名实不符取实义=专利
GRAPH_CATEGORY = {
    0: ("enterprise", "企业"), 1: ("institution", "机构"), 2: ("tech_field", "技术领域"),
    3: ("literature", "文献"), 4: ("patent", "专利"),
}
GRAPH_CENTER_NAME = "深圳先进技术研究院"
# OV §2.1：rendered_note U5 口径整句（行源=契约 §3.2 caliber_note 原文，逐字）
HOT_TECH_RENDERED_NOTE = "热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）"
HOT_TECH_METRIC_IDS = ["M_INNOV_PLAN_HEAT", "M_INNOV_PLAN_GROWTH"]
# KEY §2.6：dimension.rendered_note 定稿句（v2 item 2：用户可读、零内部编号）
KEY_DIMENSION_RENDERED_NOTE = "本页竞争力五维得分与指标值为演示数据，五维构成与评估权重口径待定稿后更新"
# OV §0.4 / S-3 裁定：reference 行契约草案示例值逐字
LOCAL_ADV_REFERENCE = {"hotspots": 72, "carriers": 1240, "capacity": 215.4,
                       "source": "全球公开数据库（示例抽样）"}


class SeedError(Exception):
    pass


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SeedError(f"ASSERT FAIL: {msg}")


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def split_unit(value: str):
    """OV §2.3：metric_unit 从 value 机械拆分（尾部非数字符号段），可空。"""
    m = re.match(r"^[+-]?[\d,]+(?:\.\d+)?(.*)$", value)
    unit = m.group(1) if m else ""
    return unit or None


# =====================================================================
# 行构建（转换规则逐条对应分册 §4）
# =====================================================================

def build_rows(seed: dict) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {t: [] for t in ADS_TABLES}

    # ---------------- OV §2.1 hot_tech（8） ----------------
    space_json = jdump(seed["technologyTrendSpaceRegions"])
    caliber_json = jdump(seed["technologyHeatTrendDefinition"])
    metric_ids_json = jdump(HOT_TECH_METRIC_IDS)
    for t in seed["hotTechData"]:
        rows["ts_plan_hot_tech"].append(dict(
            tech_id=t["id"], name=t["name"], category=t["category"], heat=t["heat"],
            growth=t["growth"], hot_trend=t["trend"], patents=t["patents"],
            papers=t["papers"], description=t["description"],
            spatial_distribution=space_json, caliber_def=caliber_json,
            rendered_note=HOT_TECH_RENDERED_NOTE, metric_ids=metric_ids_json,
            source="demo_seed",
        ))

    # ---------------- OV §2.2 hot_tech_series（128） ----------------
    series_by_range = seed["technologyTrendSeriesByRange"]
    tech_ids = [t["id"] for t in seed["hotTechData"]]
    for range_key in ("3m", "6m", "12m"):
        block = series_by_range[range_key]
        for tech_id in tech_ids:
            values = block["series"][tech_id]
            check(len(values) == len(block["xAxis"]),
                  f"series 长度与 xAxis 不一致: {range_key}/{tech_id}")
            for idx, period_label in enumerate(block["xAxis"]):
                rows["ts_plan_hot_tech_series"].append(dict(
                    tech_id=tech_id, range_key=range_key, period_label=period_label,
                    period_order=idx + 1, heat_value=values[idx], source="demo_seed",
                ))

    # ---------------- OV §2.3 metric_system（30） ----------------
    for cat_order, cat in enumerate(seed["multidimensionalIndicatorCategories"], start=1):
        linked_json = jdump(cat["linked"])
        for sort_order, metric in enumerate(cat["metrics"], start=1):
            rows["ts_plan_metric_system"].append(dict(
                category_key=cat["key"], category_label=cat["label"],
                metric_label=metric["label"], metric_value=metric["value"],
                metric_unit=split_unit(metric["value"]),
                metric_change=metric["change"], linked_json=linked_json,
                category_order=cat_order, sort_order=sort_order, source="demo_seed",
            ))

    # ---------------- OV §2.4 tracking_event（8 = 1 meta + 7 事件） ----------------
    timeline = seed["timeline"]
    rows["ts_plan_tracking_event"].append(dict(
        row_kind="timeline_meta", title=timeline["title"],
        current_year=str(timeline["currentYear"]), range_label=timeline["rangeLabel"],
        years_json=jdump([str(y) for y in timeline["years"]]),
        event_date=None, event_year=None, region=None, event_text=None,
        event_order=None, source="demo_seed",
    ))
    for order, ev in enumerate(timeline["events"], start=1):
        rows["ts_plan_tracking_event"].append(dict(
            row_kind="event", title=None, current_year=None, range_label=None,
            years_json=None, event_date=ev["date"], event_year=ev["date"][:4],
            region=ev["region"], event_text=ev["text"], event_order=order,
            source="demo_seed",
        ))

    # ---------------- OV §2.5 tracking_point（35 = 7 点 × 5 层） ----------------
    # mapRegions：demo buildMapRegions 逐字投影；position=[lat,lng] 入库拆列
    for mr in seed["mapRegions"]:
        lat, lng = mr["position"][0], mr["position"][1]
        for result_type in mr["layerKeys"]:
            rows["ts_plan_tracking_point"].append(dict(
                result_type=result_type, source_id=mr["source_id"], name=mr["name"],
                region=mr["name"], lng=lng, lat=lat, score=mr["score"],
                source="demo_seed",
            ))

    # ---------------- OV §2.6 local_adv（19 = 18 维度 + 1 reference） ----------------
    local_blocks = [
        ("field", "领域", "demo_seed", seed["localAdvantageChart"]),
        ("capability", "能力", "lumen_seed", seed["localAdvantageInnovation"]),  # S-2：capability←innovation
        ("output", "产出", "lumen_seed", seed["localAdvantageOutput"]),
    ]
    for dim_key, dim_label, source, block in local_blocks:
        for order, name in enumerate(block["yAxis"], start=1):
            rows["ts_plan_local_adv"].append(dict(
                row_kind="dimension", dimension_key=dim_key, dimension_label=dim_label,
                indicator_name=name, local_score=block["local"][order - 1],
                global_score=block["globalAvg"][order - 1], indicator_order=order,
                base_region="深圳", compare_to="全球", metric_id="M_INNOV_PLAN_LOCAL_ADV",
                reference_json=None, source=source,
            ))
    rows["ts_plan_local_adv"].append(dict(
        row_kind="reference", dimension_key=None, dimension_label=None,
        indicator_name=None, local_score=None, global_score=None, indicator_order=None,
        base_region="深圳", compare_to="全球", metric_id="M_INNOV_PLAN_LOCAL_ADV",
        reference_json=jdump(LOCAL_ADV_REFERENCE), source="contract_draft_sample",
    ))

    # ---------------- OV §2.7 talent_flow（16 = 6 stats + 5 机构 + 5 record） ----------------
    od_nodes_json = jdump(seed["talentDirectionNodes"])
    stat_key_by_name = {
        "学术界": "node_academia", "产业界": "node_industry",
        "政府/科研院所": "node_gov", "其他": "node_other",
    }
    talent_metric = "M_INNOV_PLAN_TALENT_FLOW"
    stat_rows = []
    for node in seed["talentDirectionNodes"]:
        name = node["name"]
        color = node["itemStyle"]["color"]
        region = person_count = trend_pct = None
        stat_key = stat_key_by_name.get(name)
        if stat_key is None:
            # OD 行：'深圳|18,932人|↑21.7%' → 拆 region/person_count/trend_pct
            parts = name.split("|")
            check(len(parts) == 3, f"OD 节点标签形态异常: {name}")
            stat_key = "od_shenzhen" if parts[0] == "深圳" else "od_external"
            region = parts[0]
            person_count = int(parts[1].replace(",", "").rstrip("人"))
            trend_pct = float(parts[2].replace("↑", "").rstrip("%"))
        stat_rows.append((stat_key, dict(
            row_kind="stats", stat_key=stat_key, label=name.split("|")[0] if "|" in name else name,
            color=color, region=region, person_count=person_count, trend_pct=trend_pct,
            od_nodes=od_nodes_json, metric_id=talent_metric, source="demo_seed",
        )))
    # 按 DDL stat_key 枚举序输出（od_shenzhen/od_external/node_*）
    order_pref = ["od_shenzhen", "od_external", "node_academia", "node_industry",
                  "node_gov", "node_other"]
    stat_rows.sort(key=lambda kv: order_pref.index(kv[0]))
    check(len({k for k, _ in stat_rows}) == 6, "talent stats 行 stat_key 必须唯一×6")
    rows["ts_plan_talent_flow"].extend(r for _, r in stat_rows)

    for r in seed["talentInstitutionFlowRows"]:
        rows["ts_plan_talent_flow"].append(dict(
            row_kind="institution_flow", stat_key=None, label=None, color=None,
            region=None, person_count=None, trend_pct=None, od_nodes=None,
            institution=r["institution"],
            net_inflow=int(r["netInflow"].replace(",", "").replace("+", "")),
            flow_direction="in" if r["trend"] == "up" else "out",
            metric_id=talent_metric, source="demo_seed",
        ))

    flow_type_map = {"academia-to-industry": "学术→产业",
                     "industry-to-academia": "产业→学术"}
    for r in seed["talentFlowData"]:
        # U6：name/avatar 提取阶段即丢弃（不进任何行/中间文件）
        rows["ts_plan_talent_flow"].append(dict(
            row_kind="record", stat_key=None, label=None, color=None, region=None,
            person_count=1, trend_pct=None, od_nodes=None, institution=None,
            net_inflow=None, flow_direction=None, flow_id=f"tf-{r['id']}",
            from_org=r["from"], to_org=r["to"], from_type=r["fromType"],
            to_type=r["toType"], field=r["field"],
            flow_type=flow_type_map[r["flowType"]],
            risk_level=r.get("riskLevel"), updated_at=r["date"],
            metric_id=talent_metric, source="demo_seed",
        ))

    # ---------------- KEY §2.1 key_area（3） + §2.2 carrier（22） ----------------
    clusters = seed["industryClusters"]
    carrier_ids_all = [c["id"] for c in seed["carrierLocations"]]
    carrier_id_set = set(carrier_ids_all)
    rev_cluster: dict[str, str] = {}
    for cl in clusters:
        for cid in cl["carrierIds"]:
            check(cid in carrier_id_set, f"集群 {cl['key']} 引用未知载体 {cid}")
            check(cid not in rev_cluster, f"载体 {cid} 被多个集群引用")
            rev_cluster[cid] = cl["key"]
    unclustered = carrier_id_set - set(rev_cluster)
    check(unclustered == UNCLUSTERED_WHITELIST,
          f"未挂集群载体集合 ≠ 白名单: {sorted(unclustered)} vs {sorted(UNCLUSTERED_WHITELIST)}")

    for sort_no, cl in enumerate(clusters, start=1):
        rows["ts_plan_key_area"].append(dict(
            cluster_id=cl["key"], cluster_name=cl["label"],
            industry_category=cl["industryCategory"],
            technology_field=cl["technologyField"],
            default_map_layer=cl["mapLayer"], carrier_ids=jdump(cl["carrierIds"]),
            metric_id="M_INNOV_KEYD_SPATIAL", sort_no=sort_no, source="demo_seed",
        ))
    for sort_no, c in enumerate(seed["carrierLocations"], start=1):
        rows["ts_plan_key_area_carrier"].append(dict(
            carrier_id=c["id"], name=c["name"], carrier_type=c["type"],
            district=c["district"], lng=c["lng"], lat=c["lat"], level=c["level"],
            cluster_id=rev_cluster.get(c["id"]),  # 7 行 NULL（诚实空）
            land_benefit=None,  # V1 全 NULL：demo 无逐载体土地数据，禁编造
            metric_id=None, sort_no=sort_no, source="demo_seed",
        ))

    # ---------------- KEY §2.3–2.9 其余 7 表 ----------------
    for sort_no, ct in enumerate(seed["carrierTypes"], start=1):
        rows["ts_plan_key_area_carrier_type"].append(dict(
            type_key=ct["key"], type_name=ct["name"], carrier_count=ct["count"],
            color=ct["color"], sort_no=sort_no, metric_id=None, source="demo_seed",
        ))
    for sort_no, db_ in enumerate(seed["districtCarrierBaselines"], start=1):
        rows["ts_plan_key_area_district_baseline"].append(dict(
            district=db_["district"], total_carriers=db_["total"],
            leading_type=db_["leadingType"], metric_id=None, sort_no=sort_no,
            source="demo_seed",
        ))
    for sort_no, m in enumerate(seed["keyAreaCompetitivenessMetrics"], start=1):
        rows["ts_plan_key_area_competitiveness"].append(dict(
            metric_key=m["key"], label=m["label"], value=m["value"],
            change_pct=m["change"],
            metric_id="M_INNOV_KEYD_POTENTIAL" if m["key"] == "potential"
            else "M_INNOV_KEYD_COMPETITIVENESS",
            sort_no=sort_no, source="demo_seed",
        ))
    for order, d in enumerate(seed["keyAreaDimensionScores"], start=1):
        rows["ts_plan_key_area_dimension"].append(dict(
            dim_key=DIM_KEY_MAP[d["label"]], dim_label=d["label"], score=d["percent"],
            metric_id="M_INNOV_KEYD_COMPETITIVENESS",
            rendered_note=KEY_DIMENSION_RENDERED_NOTE, dim_order=order,
            source="demo_seed",
        ))
    for b in seed["keyAreaBenchmarkRows"]:
        rows["ts_plan_key_area_benchmark"].append(dict(
            region=b["region"], score=b["score"], rank_no=b["rank"],
            metric_id="M_INNOV_KEYD_COMPETITIVENESS", source="demo_seed",
        ))
    for sort_no, lu in enumerate(seed["landUseData"], start=1):
        rows["ts_plan_key_area_land"].append(dict(
            district=lu["area"], land_type=lu["type"], area_sqm=lu["area_sqm"],
            efficiency=lu["efficiency"], status=lu["status"], land_benefit=None,
            metric_id="M_INNOV_KEYD_LAND", sort_no=sort_no, source="demo_seed",
        ))
    for sort_no, p in enumerate(seed["keyAreaScenarioPlans"], start=1):
        rows["ts_plan_key_area_plan"].append(dict(
            plan_id=p["id"], plan_name=p["name"], title=p["title"],
            priority=p["priority"], expected_effect=p["expectedEffect"],
            resource_gap=p["resourceGap"], actions=jdump(p["actions"]),
            primary_action=p["primaryAction"], secondary_action=p["secondaryAction"],
            detail_action=p["detailAction"], metric_id=None, sort_no=sort_no,
            source="demo_seed",
        ))

    # ---------------- RES §2-1 field（5）/ §2-2 company（7） ----------------
    field_key_by_label = {"人工智能": "ai", "量子科技": "quantum", "合成生物学": "synbio",
                          "集成电路": "ic", "新能源": "newenergy"}
    for sort_no, label in enumerate(seed["researchFieldOptions"], start=1):
        rows["ts_plan_research_field"].append(dict(
            field_key=field_key_by_label[label], field_label=label, sort_no=sort_no,
            metric_id=None, updated_at=None,
        ))
    rows["ts_plan_research_company"].append(dict(
        company_id="C-TARGET", name=seed["targetSubject"], role="target", color=None,
        level_tag=None, sort_no=0, metric_id=None, updated_at=None,
    ))
    for idx, c in enumerate(seed["companies"], start=1):
        rows["ts_plan_research_company"].append(dict(
            company_id=f"C-{idx:02d}", name=c["name"], role="compare", color=c["color"],
            level_tag=c["level"], sort_no=idx, metric_id="M_INNOV_RES_CI_LEVEL",
            updated_at=None,
        ))

    # ---------------- RES §2-3 overlap（6；15 对中 9 空对不灌） ----------------
    company_names = [c["name"] for c in seed["companies"]]
    all_pairs = {frozenset(p) for p in itertools.combinations(company_names, 2)}
    seed_pairs = {frozenset((o["companyA"], o["companyB"])) for o in seed["overlapMatrix"]}
    check(seed_pairs <= all_pairs, "overlapMatrix 存在六企之外的对手名")
    skipped = all_pairs - seed_pairs
    check(len(all_pairs) == 15 and len(skipped) == 9,
          f"15 对中应恰 9 空对：all={len(all_pairs)} skipped={len(skipped)}")
    for o in seed["overlapMatrix"]:
        rows["ts_plan_research_overlap"].append(dict(
            company_a=o["companyA"], company_b=o["companyB"],
            overlap_score=o["overlap"], level=o["level"],
            related_fields=jdump(o["relatedFields"]),
            metric_id="M_INNOV_RES_OVERLAP", updated_at=None,
        ))

    # ---------------- RES §2-4/2-5/2-6/2-7 规则/时间/等级/基准 ----------------
    for sort_no, rp in enumerate(seed["overlapRuleProfiles"], start=1):
        th = rp["levelThresholds"]
        rows["ts_plan_research_overlap_rule"].append(dict(
            rule_key=rp["key"], label=rp["label"], prompt=rp["prompt"],
            threshold_high=th["high"], threshold_medium=th["medium"],
            threshold_low=th["low"], rule_source=rp["ruleSource"],
            scope_text=rp["scopeText"], sort_no=sort_no, metric_id=None,
            updated_at=None,
        ))
    scope_key_by_label = {"近1年": "1y", "近3年": "3y", "近5年": "5y"}
    for sort_no, (label, factor) in enumerate(seed["overlapTimeScopeFactor"].items(), start=1):
        rows["ts_plan_research_time_factor"].append(dict(
            scope_key=scope_key_by_label[label], scope_label=label, factor=factor,
            sort_no=sort_no, metric_id=None, updated_at=None,
        ))
    for sort_no, gc in enumerate(seed["researchLevelCards"], start=1):
        rows["ts_plan_research_grade"].append(dict(
            grade_key=gc["key"], grade_label=gc["label"], description=gc["description"],
            threshold_low=GRADE_THRESHOLD_LOW[gc["key"]], is_draft=1,
            patent=int(gc["patent"].replace(",", "")),
            papers=int(gc["papers"].replace(",", "")),
            top_papers=int(gc["topPapers"].replace(",", "")),
            score=gc["score"], metric_id="M_INNOV_RES_GRADE", sort_no=sort_no,
            updated_at=None,
        ))
    for sort_no, bm in enumerate(seed["researchOverlapBenchmarks"], start=1):
        rows["ts_plan_research_overlap_benchmark"].append(dict(
            name=bm["name"], score=bm["value"], sort_no=sort_no,
            metric_id="M_INNOV_RES_OVERLAP", updated_at=None,
        ))

    # ---------------- RES §2-8/2-9 图谱节点（14）/ 星型边（13） ----------------
    node_id_by_name: dict[str, str] = {}
    for idx, n in enumerate(seed["researchGraphNodes"], start=1):
        node_id = f"N-{idx:02d}"
        node_id_by_name[n["name"]] = node_id
        cat_key, cat_label = GRAPH_CATEGORY[n["category"]]
        rows["ts_plan_research_graph_node"].append(dict(
            node_id=node_id, node_name=n["name"], category_key=cat_key,
            category_label=cat_label, symbol_size=n["symbolSize"], x=n["x"], y=n["y"],
            sort_no=idx, metric_id=None, updated_at=None,
        ))
    center_id = node_id_by_name[GRAPH_CENTER_NAME]
    edge_no = 0
    for n in seed["researchGraphNodes"]:
        if n["name"] == GRAPH_CENTER_NAME:
            continue
        edge_no += 1
        rows["ts_plan_research_graph_edge"].append(dict(
            source=center_id, target=node_id_by_name[n["name"]], relation="关联",
            sort_no=edge_no, metric_id=None, updated_at=None,
        ))

    # ---------------- RES §2-10 insight（4；plan_id 固化 resolveStrategyPlan） ----------------
    plan_ids = {p["id"] for p in seed["keyAreaScenarioPlans"]}
    for sort_no, r in enumerate(seed["regionalPlanningInsightRows"], start=1):
        if r["priority"] == "高":
            plan_id = "a"
        elif "追赶" in r["competition"]:
            plan_id = "b"
        else:
            plan_id = "c"
        check(plan_id in plan_ids, f"plan_id {plan_id} 不在方案键集")
        rows["ts_plan_research_insight"].append(dict(
            field=r["field"], competition=r["competition"], priority=r["priority"],
            evidence=r["evidence"], regional_insight=r["regionalInsight"],
            action=r["action"], plan_id=plan_id, sort_no=sort_no, metric_id=None,
            updated_at=None,
        ))

    # ---------------- RES §2-11 report_template（8 = 报告 3 + 建议 3 + 系统 2） ----------------
    # 报告 3 节：demo buildResearchIntelligenceReport（model L460–490）逐字，占位符化
    # 建议 3 节：ResearchTab 企业发展战略建议 Modal（demo L3358–3375）逐字
    templates = [
        ("overlap_section", "研究领域重叠情况", False, 1,
         "{target}与比对主体在{field}上的重叠结果：{overlap_text}。规则口径为{rule_label}。"),
        ("advantage_section", "竞争优势与劣势", False, 2,
         "优势：{target}在{field}方向综合得分{lead_score}，核心专利{lead_patent}、高被引论文{lead_papers}，"
         "相对比对主体保持领先布局。劣势：追赶级方向综合得分{catching_score}，"
         "与{compare}等高重叠主体相比，工程验证平台和产业承接仍偏弱。"),
        ("suggestion_section", "发展建议", False, 3,
         "{field}：{action}（取情报行前 3 条）"),
        ("tech_route", "技术路线", False, 4, "{action}。{regional_insight}"),
        ("resource_config", "资源配置", False, 5,
         "建议动作：{action}。对应方案「{plan_title}」可缓解资源缺口 {resource_gap}，"
         "预期效果 {expected_effect}。"),
        ("cooperation", "合作机会", False, 6,
         "比对主体 {compare} 中，重叠较高的可协作对象：{benchmark_list}。"),
        # 系统行：page_caliber 文案沿 KEY dimension.rendered_note 先例（用户可读、零内部编号）
        ("page_caliber", "整页口径", True, 7,
         "本页研究领域重叠度、等级划分与竞争情报数据为演示数据，重叠规则阈值与等级阈值口径待定稿后更新"),
        # U9 阈值（RES-ARCH：超 100 节点/300 边走 M2），JSON 物理行源；
        # follow_up 键 = U9 降级跳转语义（RES-API §3：超限 graph 块 follow_up="M2 §3.1"，FE 懒加载 M2 §3.1 图谱接口）
        ("graph_limit", "图谱规模阈值", True, 8,
         '{"node_limit":100,"edge_limit":300,"follow_up":"M2 §3.1"}'),
    ]
    for key, label, is_system, sort_no, text in templates:
        rows["ts_plan_research_report_template"].append(dict(
            section_key=key, section_label=label, template_text=text,
            is_system=int(is_system), sort_no=sort_no, metric_id=None, updated_at=None,
        ))

    return rows


# =====================================================================
# 行级断言（灌数前对构建行执行；对应三份分册 §4 验收）
# =====================================================================

def assert_rows(rows: dict[str, list[dict]]) -> None:
    # 1) 逐表行数
    for table, expected in EXPECTED_COUNTS.items():
        check(len(rows[table]) == expected,
              f"{table} 行数 {len(rows[table])} ≠ {expected}")

    # 2) OV 断言（OV-DATA §4.4）
    ht1 = next(r for r in rows["ts_plan_hot_tech"] if r["tech_id"] == "1")
    check(ht1["heat"] == 98 and ht1["growth"] == 45.2, "hot_tech tech 1 heat=98/growth=45.2")
    s12m8 = [r for r in rows["ts_plan_hot_tech_series"]
             if r["range_key"] == "12m" and r["tech_id"] == "8"]
    check(max(s12m8, key=lambda r: r["period_order"])["heat_value"] == 76,
          "12m 区间 tech 8 末期 heat=76")
    check(any(r["category_key"] == "technology" and r["metric_label"] == "热度指数"
              and r["metric_value"] == "98" for r in rows["ts_plan_metric_system"]),
          "metric_system 含「热度指数=98」")
    check(all("口径待 M0 定稿" in r["rendered_note"] for r in rows["ts_plan_hot_tech"]),
          "hot_tech 各行 rendered_note 含「口径待 M0 定稿」")
    pt = next(r for r in rows["ts_plan_tracking_point"]
              if r["source_id"] == "tdp-global-robot" and r["result_type"] == "hotspot")
    check(pt["score"] == 94, "point(tdp-global-robot, hotspot) score=94")
    check(len({r["source_id"] for r in rows["ts_plan_tracking_point"]}) == 7,
          "tracking_point 7 点")
    od_sz = next(r for r in rows["ts_plan_talent_flow"] if r["stat_key"] == "od_shenzhen")
    check(od_sz["person_count"] == 18932 and float(od_sz["trend_pct"]) == 21.7,
          "talent od_shenzhen person_count=18932/trend=21.7")
    check(len(json.loads(od_sz["od_nodes"])) == 6, "od_nodes 六节点齐")
    od_ext = next(r for r in rows["ts_plan_talent_flow"] if r["stat_key"] == "od_external")
    check(od_ext["person_count"] == 12458 and float(od_ext["trend_pct"]) == 16.2,
          "talent od_external 12458/16.2")
    check(sum(1 for r in rows["ts_plan_talent_flow"] if r["row_kind"] == "record"
              and "张明远" not in json.dumps(r, ensure_ascii=False)) == 5,
          "record 行不得携带任何个人姓名")
    ref = [r for r in rows["ts_plan_local_adv"] if r["row_kind"] == "reference"]
    check(len(ref) == 1 and ref[0]["source"] == "contract_draft_sample",
          "local_adv reference 行 1 条 contract_draft_sample")
    cap = [r for r in rows["ts_plan_local_adv"] if r["dimension_key"] == "capability"]
    check(len(cap) == 6 and all(r["source"] == "lumen_seed" for r in cap),
          "capability 维 6 行 lumen_seed")

    # 3) KEY 断言（KEY-DATA §4.4）
    carriers = rows["ts_plan_key_area_carrier"]
    check(all(r["land_benefit"] is None for r in carriers),
          "carrier 22 行 land_benefit 全 NULL（禁编造容积率/亩产）")
    null_cluster = {r["carrier_id"] for r in carriers if r["cluster_id"] is None}
    check(null_cluster == UNCLUSTERED_WHITELIST and len(null_cluster) == 7,
          f"cluster_id IS NULL 恰 7 行: {sorted(null_cluster)}")
    check(next(r for r in carriers if r["carrier_id"] == "L001")["cluster_id"] is None,
          "L001 cluster_id NULL")
    check(next(r for r in carriers if r["carrier_id"] == "A001")["cluster_id"] == "ai",
          "A001 cluster_id='ai'")
    ai = next(r for r in rows["ts_plan_key_area"] if r["cluster_id"] == "ai")
    check(len(json.loads(ai["carrier_ids"])) == 6 and ai["default_map_layer"] == "产业热度",
          "cluster ai: carrier_ids 6 元素 / default_map_layer=产业热度")
    all_row = next(r for r in rows["ts_plan_key_area_carrier_type"] if r["type_key"] == "all")
    check(all_row["carrier_count"] == 2856, "carrier_type all 行 count=2856")
    ns = next(r for r in rows["ts_plan_key_area_district_baseline"] if r["district"] == "南山区")
    check(ns["total_carriers"] == 276, "district_baseline 南山 total=276")
    comp = next(r for r in rows["ts_plan_key_area_competitiveness"]
                if r["metric_key"] == "composite")
    check(float(comp["value"]) == 78.5 and comp["change_pct"] == "12.3%",
          "competitiveness composite 78.5 / change_pct='12.3%'")
    pot = next(r for r in rows["ts_plan_key_area_competitiveness"]
               if r["metric_key"] == "potential")
    check(pot["metric_id"] == "M_INNOV_KEYD_POTENTIAL", "potential 行挂 POTENTIAL")
    dim1 = next(r for r in rows["ts_plan_key_area_dimension"] if r["dim_label"] == "创新资源")
    check(dim1["score"] == 92 and dim1["dim_key"] == "innovation_resources",
          "dimension 创新资源 92 / innovation_resources")
    check(len({r["rendered_note"] for r in rows["ts_plan_key_area_dimension"]}) == 1,
          "dimension 5 行 rendered_note 同值")
    b1 = next(r for r in rows["ts_plan_key_area_benchmark"] if r["rank_no"] == 1)
    check(b1["region"] == "南山区" and float(b1["score"]) == 78.5, "benchmark rank1 南山区 78.5")
    land1 = next(r for r in rows["ts_plan_key_area_land"]
                 if r["district"] == "南山区" and r["land_type"] == "研发用地")
    check(land1["area_sqm"] == 125000 and land1["efficiency"] == 92
          and land1["status"] == "good", "land 南山研发用地 125000/92/good")
    check(all(r["land_benefit"] is None for r in rows["ts_plan_key_area_land"]),
          "land 6 行 land_benefit 全 NULL")
    plan_a = next(r for r in rows["ts_plan_key_area_plan"] if r["plan_id"] == "a")
    check(plan_a["expected_effect"] == "+18.6%" and len(json.loads(plan_a["actions"])) == 3,
          "plan a 行 expected_effect='+18.6%' / actions 3 元素")

    # 4) RES 断言（RES-DATA §5）+ 任务 DoD 禁灌清单
    overlaps = rows["ts_plan_research_overlap"]
    check(len(overlaps) == 6, "overlap 恰 6 行（15 对中 9 空对不灌）")
    check(all(45 <= float(o["overlap_score"]) <= 72 for o in overlaps),
          "overlap 值域 45–72")
    check(all(r["category_key"] != "expert" and r["category_label"] != "专家"
              for r in rows["ts_plan_research_graph_node"]),
          "图谱专家类节点 0（demo 名实不符，专家类留位不灌）")
    grade_order = ["lead", "advantage", "catching", "potential"]
    grades = {r["grade_key"]: r for r in rows["ts_plan_research_grade"]}
    check([float(grades[k]["threshold_low"]) for k in grade_order] == [80.0, 65.0, 45.0, 0.0],
          "grade threshold_low 依次 80/65/45/0")
    check(all(r["is_draft"] == 1 for r in rows["ts_plan_research_grade"]),
          "grade is_draft=1（U3 建议值未拍板）")
    insight_seq = [r["plan_id"] for r in
                   sorted(rows["ts_plan_research_insight"], key=lambda x: x["sort_no"])]
    check(insight_seq == ["a", "b", "c", "b"],
          f"insight plan_id 序列 a/b/c/b，实际 {insight_seq}")
    templates = rows["ts_plan_research_report_template"]
    check(len(templates) == 8 and sum(r["is_system"] for r in templates) == 2,
          "report_template 8 行（含 2 系统行）")
    gl = next(r for r in templates if r["section_key"] == "graph_limit")
    gl_json = json.loads(gl["template_text"])
    check(gl_json.get("node_limit") == 100 and gl_json.get("edge_limit") == 300
          and gl_json.get("follow_up") == "M2 §3.1",
          "graph_limit 模板行须含 node_limit=100/edge_limit=300/follow_up='M2 §3.1'（U9 降级语义，RES-API §3）")

    # 5) direction_warning 禁灌铁律：本脚本对其零语句（不进 ADS_TABLES 即零 INSERT/TRUNCATE）
    check("ts_plan_direction_warning" not in ADS_TABLES,
          "ts_plan_direction_warning 不得出现在灌数清单（V1 零行，禁灌假预警）")


def assert_column_lengths(rows: dict[str, list[dict]]) -> None:
    """离线预检：解析 DDL 的 varchar/char 上限，校验构建行字符长度（防 1406 上库才爆）。

    例外：`signal` 等保留字列名在 DDL 中带反引号，正则兼容。
    """
    ddl_text = DDL_ADS.read_text(encoding="utf-8")
    limits: dict[str, dict[str, int]] = {}
    for block in re.finditer(
            r"CREATE TABLE `?(\w+)`?\s*\((.*?)\)\s*ENGINE", ddl_text, re.S):
        table, body = block.group(1), block.group(2)
        cols: dict[str, int] = {}
        for m in re.finditer(r"^\s*`?(\w+)`?\s+(?:varchar|char)\((\d+)\)",
                             body, re.M | re.I):
            cols[m.group(1)] = int(m.group(2))
        limits[table] = cols
    for table, table_rows in rows.items():
        col_limits = limits.get(table, {})
        for r in table_rows:
            for col, value in r.items():
                limit = col_limits.get(col)
                if limit is not None and isinstance(value, str) and len(value) > limit:
                    raise SeedError(
                        f"ASSERT FAIL: {table}.{col} 值超长（{len(value)} > varchar({limit})）:"
                        f" {value[:50]}…")


def print_dry_run(rows: dict[str, list[dict]]) -> None:
    print("=" * 96)
    print(f"DRY-RUN · 待写行数与 NULL 分布（{ADS_DB}）")
    print("=" * 96)
    total = 0
    for table in ADS_TABLES:
        table_rows = rows[table]
        total += len(table_rows)
        null_cols = []
        for col in table_rows[0].keys():
            n = sum(1 for r in table_rows if r[col] is None)
            if n:
                null_cols.append(f"{col}={n}")
        dist = (" | NULL: " + ", ".join(null_cols)) if null_cols else ""
        status = "OK" if len(table_rows) == EXPECTED_COUNTS[table] else \
            f"MISMATCH(expect {EXPECTED_COUNTS[table]})"
        print(f"  {table:<42} {len(table_rows):>4} 行  [{status}]{dist}")
    print("-" * 96)
    print(f"  合计 OV 244 + KEY 61 + RES 70 = 375 行；实际 {total} 行"
          f"  [{'OK' if total == 375 else 'MISMATCH'}]")
    print(f"  零行表（只建表不灌）：ts_plan_direction_warning（ADS）、"
          f"sys_user_planning_push_record（{MAIN_DB}）")
    print("  全部行级断言通过，未写库。")


# =====================================================================
# MySQL 执行层
# =====================================================================

def mysql_conf() -> dict:
    password = (os.environ.get("INNOV_MYSQL_PASSWORD")
                or os.environ.get("GKX_MYSQL_PASSWORD"))
    if not password:
        raise SystemExit("缺少 INNOV_MYSQL_PASSWORD / GKX_MYSQL_PASSWORD"
                         "（连接真源：agent-handoffs/算法库联调-ALGO-LIB/algo-mysql-connection-info.md）")
    return dict(
        host=os.environ.get("INNOV_MYSQL_HOST", "10.50.11.76"),
        port=int(os.environ.get("INNOV_MYSQL_PORT", "3306")),
        user=os.environ.get("INNOV_MYSQL_USER", "gkxlumenx"),
        password=password,
        charset="utf8mb4",
        connect_timeout=15,
        autocommit=False,
    )


def split_statements(sql_text: str) -> list[str]:
    """按分号切分 DDL 语句（无存储过程/触发器，安全）。"""
    stmts, buf = [], []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or stripped.startswith("/*"):
            continue
        buf.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(buf).strip().rstrip(";").strip()
            if stmt:
                stmts.append(stmt)
            buf = []
    tail = "\n".join(buf).strip().rstrip(";").strip()
    if tail:
        stmts.append(tail)
    return stmts


def table_of(stmt: str) -> str | None:
    m = re.search(r"CREATE TABLE (IF NOT EXISTS )?`?(\w+)`?", stmt, re.IGNORECASE)
    return m.group(2) if m else None


def apply_ddl(conn, cur) -> None:
    for db, ddl_file in ((ADS_DB, DDL_ADS), (MAIN_DB, DDL_PUSH)):
        cur.execute(f"USE `{db}`")
        for stmt in split_statements(ddl_file.read_text(encoding="utf-8")):
            table = table_of(stmt)
            if table:
                cur.execute(f"DROP TABLE IF EXISTS `{table}`")
            cur.execute(stmt)
            conn.commit()
            print(f"  DDL {db}.{table}: created")


def insert_rows(cur, db: str, table: str, table_rows: list[dict],
                chunk: int = 64) -> None:
    if not table_rows:
        return
    cols = list(table_rows[0].keys())
    # updated_at 由脚本显式写灌数时间戳（RES 组 DDL 无默认值）
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    placeholders = ", ".join(["%s"] * len(cols))
    sql = (f"INSERT INTO `{db}`.`{table}` (`" + "`, `".join(cols) + "`) "
           f"VALUES ({placeholders})")
    payload = [tuple(now if c == "updated_at" and r[c] is None else r[c] for c in cols)
               for r in table_rows]
    # 分块 executemany：内网链路偶发 2013 断连，缩小单包体积降低整批重试成本
    for i in range(0, len(payload), chunk):
        cur.executemany(sql, payload[i:i + chunk])


def seed_one_table(conf: dict, db: str, table: str, table_rows: list[dict],
                   attempts: int = 3) -> None:
    """单表幂等灌数：TRUNCATE + 分块 INSERT + commit；断连类错误整表重试（重建连接）。"""
    import pymysql
    last_err = None
    for attempt in range(1, attempts + 1):
        conn = None
        try:
            conn = pymysql.connect(**conf)
            cur = conn.cursor()
            cur.execute(f"USE `{db}`")
            cur.execute(f"TRUNCATE TABLE `{table}`")  # 隐式提交
            insert_rows(cur, db, table, table_rows)
            conn.commit()
            print(f"  seed {db}.{table}: {len(table_rows)} rows")
            return
        except pymysql.err.OperationalError as e:
            last_err = e
            code = e.args[0] if e.args else 0
            retryable = code in (2006, 2013, 2003)  # 断连/查询中断/无法连接
            print(f"  [warn] {db}.{table} attempt {attempt}: OperationalError {code}"
                  f"{'，重连重试' if retryable and attempt < attempts else '，不可重试'}")
            if not retryable or attempt == attempts:
                raise
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    raise last_err  # pragma: no cover


def verify_db(cur) -> None:
    print("\n" + "=" * 96)
    print("落库后逐表行数验证")
    print("=" * 96)
    cur.execute(f"USE `{ADS_DB}`")
    total = 0
    for table in ADS_TABLES + ["ts_plan_direction_warning"]:
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        n = cur.fetchone()[0]
        total += n
        expect = EXPECTED_COUNTS.get(table, 0)
        status = "OK" if n == expect else f"MISMATCH(expect {expect})"
        print(f"  {ADS_DB}.{table:<42} {n:>4} 行  [{status}]")
        check(n == expect, f"{table} 落库行数 {n} ≠ {expect}")
    cur.execute(f"SELECT COUNT(*) FROM `{MAIN_DB}`.`sys_user_planning_push_record`")
    n = cur.fetchone()[0]
    print(f"  {MAIN_DB}.sys_user_planning_push_record  {n:>4} 行  [{'OK' if n == 0 else 'MISMATCH(expect 0)'}]")
    check(n == 0, "sys_user_planning_push_record 初始必须 0 行（真实推送产生）")
    check(total == 375, f"ADS 28+1 表合计应 375，实际 {total}")

    # DB 级禁灌/抽样断言（复跑行级关键项于库上）
    cur.execute("SELECT COUNT(*) FROM ts_plan_key_area_carrier WHERE land_benefit IS NOT NULL")
    check(cur.fetchone()[0] == 0, "DB: carrier land_benefit 非 NULL 行应为 0")
    cur.execute("SELECT COUNT(*) FROM ts_plan_key_area_carrier WHERE cluster_id IS NULL")
    check(cur.fetchone()[0] == 7, "DB: carrier cluster_id NULL 行应为 7")
    cur.execute("SELECT COUNT(*) FROM ts_plan_research_overlap")
    check(cur.fetchone()[0] == 6, "DB: overlap 恰 6 行")
    cur.execute("SELECT COUNT(*) FROM ts_plan_research_graph_node "
                "WHERE category_key='expert' OR category_label='专家'")
    check(cur.fetchone()[0] == 0, "DB: 图谱专家类节点 0")
    cur.execute("SELECT threshold_low FROM ts_plan_research_grade "
                "ORDER BY FIELD(grade_key,'lead','advantage','catching','potential')")
    check([float(x[0]) for x in cur.fetchall()] == [80.0, 65.0, 45.0, 0.0],
          "DB: grade threshold_low 80/65/45/0")
    cur.execute("SELECT COUNT(*) FROM ts_plan_research_grade WHERE is_draft<>1")
    check(cur.fetchone()[0] == 0, "DB: grade is_draft 全 1")
    cur.execute("SELECT plan_id FROM ts_plan_research_insight ORDER BY sort_no")
    check([x[0] for x in cur.fetchall()] == ["a", "b", "c", "b"],
          "DB: insight plan_id 序列 a/b/c/b")
    cur.execute("SELECT COUNT(*) FROM ts_plan_hot_tech WHERE rendered_note "
                "NOT LIKE '%口径待 M0 定稿%'")
    check(cur.fetchone()[0] == 0, "DB: hot_tech rendered_note 全含「口径待 M0 定稿」")
    print("  DB 级禁灌/抽样断言：全部通过")


def main() -> int:
    parser = argparse.ArgumentParser(description="TS-L2-DS09-SEED-L01 灌数")
    parser.add_argument("--dry-run", action="store_true", help="只构建+断言+打印，不落库")
    parser.add_argument("--apply-ddl", action="store_true",
                        help="先 DROP+CREATE 全部 29 表（幂等重建）再灌数")
    parser.add_argument("--re-extract", action="store_true",
                        help="强制重跑 node 种子提取")
    args = parser.parse_args()

    if args.re_extract or not SEED_DUMP.exists():
        print(f"[extract] 运行 node {BASE / 'extract_seed.mjs'} ...")
        subprocess.run(["node", str(BASE / "extract_seed.mjs")], check=True)

    seed = json.loads(SEED_DUMP.read_text(encoding="utf-8"))
    rows = build_rows(seed)
    assert_rows(rows)  # 行级断言失败即中止，不落库
    assert_column_lengths(rows)  # 离线列长预检（防 1406 上库才爆）
    print(f"[build] 28 表行构建完成，全部行级断言+列长预检通过"
          f"（{sum(len(v) for v in rows.values())} 行）")

    if args.dry_run:
        print_dry_run(rows)
        return 0

    try:
        import pymysql
    except ImportError:
        raise SystemExit("ERROR: 需要 pymysql — pip install pymysql")

    conf = mysql_conf()
    print(f"[mysql] connect {conf['host']}:{conf['port']} as {conf['user']} ...")
    conn = pymysql.connect(**conf)
    try:
        cur = conn.cursor()
        if args.apply_ddl:
            print("[ddl] DROP+CREATE 29 表（幂等重建）")
            apply_ddl(conn, cur)
        # 幂等灌数：逐表 TRUNCATE + INSERT，单表单事务（OV §4.1 / KEY §4.1 / RES §5）
        # 零行表（direction_warning / push_record）无任何语句；
        # 每表独立连接+断连重试，适配内网链路偶发 2013
        for table in ADS_TABLES:
            seed_one_table(conf, ADS_DB, table, rows[table])
        cur.execute(f"USE `{ADS_DB}`")
        verify_db(cur)
    finally:
        conn.close()
    print("\nDONE · TS-L2-DS09-SEED-L01 灌数完成（幂等可重跑；未 push，DDL 变更归 Java 实现单复核）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
