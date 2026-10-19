# -*- coding: utf-8 -*-
"""把 A06–A15 / B02–B09 晚到提法补进 SCI-INT-C05.yaml，不重建原 49 张卡。"""
import pathlib
import re
import yaml

BASE = pathlib.Path(__file__).resolve().parents[1]
WORK = pathlib.Path(__file__).resolve().parent
C05 = BASE / "SCI-INT-C05.yaml"
LATE_TASKS = {f"SCI-INT-A{i:02d}" for i in range(6, 16)} | {f"SCI-INT-B{i:02d}" for i in range(2, 10)}
ORIG = [
    "INT-C-TAL-400", "INT-C-TAL-401", "INT-C-TAL-402", "INT-C-TAL-403",
    "INT-C-TAL-404", "INT-C-TAL-405", "INT-C-TAL-406", "INT-C-TAL-407",
    "INT-C-TECH-420", "INT-C-TECH-421", "INT-C-TECH-422", "INT-C-TECH-423",
    "INT-C-TECH-424", "INT-C-TECH-425", "INT-C-TECH-426", "INT-C-TECH-427",
    "INT-C-TECH-428", "INT-C-TECH-429", "INT-C-TECH-430", "INT-C-TECH-431",
    "INT-C-TECH-432", "INT-C-TECH-433", "INT-C-TECH-434",
    "INT-C-ORG-440", "INT-C-ORG-441", "INT-C-ORG-442", "INT-C-ORG-443",
    "INT-C-X-460", "INT-C-X-461", "INT-C-X-462", "INT-C-X-463", "INT-C-X-464",
    "INT-C-X-465", "INT-C-X-466", "INT-C-X-467", "INT-C-X-468", "INT-C-X-469",
    "INT-C-X-470", "INT-C-X-471", "INT-C-X-472", "INT-C-X-474", "INT-C-X-475",
    "INT-C-X-476", "INT-C-X-477", "INT-C-X-478", "INT-C-X-480", "INT-C-X-481",
    "INT-C-X-482", "INT-C-X-490",
]


def M(to, also=()):
    return (to, list(also))


# 主映射 to；also 只挂已有或本次新卡，不另造表
MAP = {
    "SCI-INT-A06:INT-A-ORG-500": M("INT-C-ORG-496", ["INT-C-ORG-440"]),
    "SCI-INT-A06:INT-A-ORG-501": M("INT-C-ORG-440"),
    "SCI-INT-A06:INT-A-X-507": M("INT-C-ORG-443"),
    "SCI-INT-A06:INT-A-X-510": M("INT-C-X-471"),
    "SCI-INT-A06:INT-A-X-515": M("INT-C-X-471"),
    "SCI-INT-A06:INT-A-TECH-516": M("INT-C-X-471", ["INT-C-TECH-421"]),
    "SCI-INT-A06:INT-A-X-517": M("INT-C-X-471"),
    "SCI-INT-A06:INT-A-X-521": M("INT-C-X-497"),
    "SCI-INT-A06:INT-A-X-526": M("INT-C-X-471", ["INT-C-X-497"]),
    "SCI-INT-A07:INT-A-X-601": M("INT-C-X-475"),
    "SCI-INT-A07:INT-A-TECH-602": M("INT-C-X-466"),
    "SCI-INT-A07:INT-A-TECH-607": M("INT-C-X-480", ["INT-C-X-466"]),
    "SCI-INT-A07:INT-A-X-610": M("INT-C-X-480"),
    "SCI-INT-A07:INT-A-X-618": M("INT-C-X-471", ["INT-C-X-480"]),
    "SCI-INT-A07:INT-A-X-619": M("INT-C-X-480", ["INT-C-X-472"]),
    "SCI-INT-A07:INT-A-X-631": M("INT-C-X-472"),
    "SCI-INT-A08:INT-A-X-701": M("INT-C-X-475", ["INT-C-X-474"]),
    "SCI-INT-A08:INT-A-ORG-702": M("INT-C-ORG-440"),
    "SCI-INT-A08:INT-A-ORG-704": M("INT-C-ORG-496"),
    "SCI-INT-A08:INT-A-X-705": M("INT-C-X-471"),
    "SCI-INT-A08:INT-A-X-708": M("INT-C-X-472"),
    "SCI-INT-A08:INT-A-X-717": M("INT-C-X-466", ["INT-C-TECH-421"]),
    "SCI-INT-A08:INT-A-TECH-733": M("INT-C-TECH-421", ["INT-C-TECH-422"]),
    "SCI-INT-A08:INT-A-X-727": M("INT-C-X-497"),
    "SCI-INT-A08:INT-A-TAL-728": M("INT-C-X-497", ["INT-C-TAL-400"]),
    "SCI-INT-A10:INT-A-X-900": M("INT-C-X-491"),
    "SCI-INT-A10:INT-A-TAL-910": M("INT-C-TAL-400", ["INT-C-X-480"]),
    "SCI-INT-A10:INT-A-X-912": M("INT-C-X-491"),
    "SCI-INT-A10:INT-A-X-913": M("INT-C-X-491"),
    "SCI-INT-A10:INT-A-TAL-914": M("INT-C-TAL-404", ["INT-C-X-480"]),
    "SCI-INT-A10:INT-A-X-920": M("INT-C-X-491"),
    "SCI-INT-A10:INT-A-X-924": M("INT-C-X-491"),
    "SCI-INT-A11:INT-A-X-1007": M("INT-C-X-498"),
    "SCI-INT-A11:INT-A-X-1009": M("INT-C-X-498"),
    "SCI-INT-A12:INT-A-TAL-1100": M("INT-C-TAL-405", ["INT-C-X-474"]),
    "SCI-INT-A12:INT-A-TAL-1103": M("INT-C-TAL-402", ["INT-C-X-480"]),
    "SCI-INT-A12:INT-A-TAL-1114": M("INT-C-TAL-400", ["INT-C-TAL-401"]),
    "SCI-INT-A13:INT-A-X-1205": M("INT-C-X-475"),
    "SCI-INT-A14:INT-A-X-1302": M("INT-C-TAL-403", ["INT-C-X-490"]),
    "SCI-INT-A14:INT-A-X-1306": M("INT-C-X-490", ["INT-C-X-480"]),
    "SCI-INT-A14:INT-A-X-1308": M("INT-C-X-490", ["INT-C-X-480"]),
    "SCI-INT-A14:INT-A-X-1320": M("INT-C-X-490"),
    "SCI-INT-A14:INT-A-X-1322": M("INT-C-X-490", ["INT-C-X-480"]),
    "SCI-INT-A14:INT-A-X-1323": M("INT-C-X-490"),
    "SCI-INT-A14:INT-A-X-1324": M("INT-C-X-490"),
    "SCI-INT-A14:INT-A-X-1326": M("INT-C-X-490", ["INT-C-X-480"]),
    "SCI-INT-A14:INT-A-X-1327": M("INT-C-X-490"),
    "SCI-INT-B02:INT-B-TAL-100": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-101": M("INT-C-TAL-402", ["INT-C-X-480", "INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-102": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-103": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-104": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-105": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-106": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-107": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-108": M("INT-C-TAL-402", ["INT-C-X-480", "INT-C-X-481"]),
    "SCI-INT-B02:INT-B-TAL-109": M("INT-C-X-480", ["INT-C-X-481"]),
    "SCI-INT-B03:INT-B-TAL-200": M("INT-C-TAL-400"),
    "SCI-INT-B03:INT-B-TAL-201": M("INT-C-TAL-401"),
    "SCI-INT-B03:INT-B-TAL-207": M("INT-C-TAL-402"),
    "SCI-INT-B05:INT-B-TECH-403": M("INT-C-TECH-421", ["INT-C-X-480"]),
    "SCI-INT-B05:INT-B-TECH-404": M("INT-C-TECH-421", ["INT-C-X-480"]),
    "SCI-INT-B05:INT-B-TECH-410": M("INT-C-TECH-421", ["INT-C-X-480"]),
    "SCI-INT-B06:INT-B-TECH-504": M("INT-C-TECH-492"),
    "SCI-INT-B06:INT-B-TECH-508": M("INT-C-TECH-492"),
    "SCI-INT-B06:INT-B-TECH-509": M("INT-C-TECH-492"),
    "SCI-INT-B06:INT-B-TECH-510": M("INT-C-TECH-492"),
    "SCI-INT-B07:INT-B-TECH-600": M("INT-C-X-493", ["INT-C-X-480"]),
    "SCI-INT-B07:INT-B-TECH-601": M("INT-C-X-493", ["INT-C-X-480"]),
    "SCI-INT-B07:INT-B-TECH-602": M("INT-C-X-493", ["INT-C-X-480"]),
    "SCI-INT-B07:INT-B-TECH-603": M("INT-C-TECH-494"),
    "SCI-INT-B07:INT-B-TECH-604": M("INT-C-TECH-494"),
    "SCI-INT-B07:INT-B-TECH-605": M("INT-C-TECH-494"),
    "SCI-INT-B07:INT-B-TECH-606": M("INT-C-TECH-494"),
    "SCI-INT-B08:INT-B-ORG-700": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-701": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-702": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-703": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-704": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-705": M("INT-C-X-480"),
    "SCI-INT-B08:INT-B-ORG-706": M("INT-C-X-480"),
    "SCI-INT-B09:INT-B-ORG-814": M("INT-C-ORG-495"),
}

NOTES = {
    "INT-C-TAL-400": "补归并：A12 INT-A-TAL-1114 与 B03 SE-B03-01 的 dwd_talent_master 挂本主档，A10 学术力只作对照，不另造第二张人才主表。",
    "INT-C-TAL-401": "补归并：B03 SE-B03-02 的 dwd_person_id_map 即本映射；A12 INT-A-TAL-1114 同时引用，不另造。",
    "INT-C-TAL-402": "补归并：A12 INT-A-TAL-1103 与 B02 SE-B02-02（INT-B-TAL-101/108）及 B03 INT-B-TAL-207 的 dwd_talent_flow 即本流动边，不另立表。",
    "INT-C-TAL-403": "补归并：A14 INT-A-X-1302 写回走本人工层再投影，不直接写 Nebula，不另造表。",
    "INT-C-TAL-404": "补归并：A10 INT-A-TAL-914 的论文/项目参与挂本关系边，不另造参与主表。",
    "INT-C-TAL-405": "补归并：A12 INT-A-TAL-1100 的 ads_talent_geo_agg 即本地区×领域×年度聚合，不另起表。",
    "INT-C-TECH-421": "补归并：B05 SE-B05-01 的 dim_tech_domain 与 A08 INT-A-TECH-733 并入本领域维，不另造第二张。",
    "INT-C-TECH-422": "补归并：A08 INT-A-TECH-733 的 IPC/行业映射挂本锚点桥，不另造映射主表。",
    "INT-C-ORG-440": "补归并：A06/A08 的 dim_carrier 作机构子类型挂本主数据（CF-C05-17），不另造载体主表。",
    "INT-C-ORG-443": "补归并：A06 INT-A-X-507 载体成果计数复用本机构基础指标，不另造聚合主表。",
    "INT-C-X-466": "补归并：A07 成果地理落点 ads_gba_achievement_geo 与 A08 ads_sz_domain_geo 并入本落点表，不另造地理事实表。",
    "INT-C-X-471": "补归并：A06/A08 订阅、监测配置与推送记录并入本用户订阅/推送表，不另造订阅主表。",
    "INT-C-X-472": "补归并：A07 年鉴 ads_gba_city_stat_yearly 与 A08 深圳指标看板并入本 KPI 聚合，不另造年鉴主表。",
    "INT-C-X-474": "补归并：A08 街道级区划与 A12 人才地理维仍用本 code_region 扩展，不新建地理主数据。",
    "INT-C-X-475": "补归并：A07 dim_gba_city（湾区 11 市）与 A08 园区/校区、A13 INT-A-X-1205 深圳区/园区/载体同属本 region_scope 扩展，不另造三张地理表。",
    "INT-C-X-480": "补归并：B02 SE-B02-01 的 ads_sci_result_snapshot 为共享快照；B08 SE-B08-01 ads_sci_org_deep_snapshot 用 kind/分区并入本表；B07 与湾区快照只引用，不另开快照产品。",
    "INT-C-X-481": "补归并：B02 SE-B02-01 的适配层缓存即本 jx_api_cache，不另造缓存表。",
    "INT-C-X-490": "补归并：A14 的 talent / talent_coop 只引用 C04 图谱 schema，不为未建标签另造 ADS 主表。",
}


def card(int_id, kind, kind_cn, name, physical, fields, pk, refresh, writer, *, dim, pattern, ours,
         pages, metrics, consumers, sources, prim, also, gaps, tests, note):
    return {
        "int_id": int_id,
        "layer": "data",
        "srs": {"ref": "见 merged_from 原卡 srs"},
        "page_ref": pages,
        "dimension": dim,
        "dep_kind": ["data"],
        "metric_ids": metrics,
        "metric_domain_other": [],
        "algorithm_type": "n/a（结构卡；指标算法类型见原卡 / MCP）",
        "integration_pattern": pattern,
        "ours": ours,
        "counterpart": "none",
        "delivery_form": "table",
        "jiuxin_row_id": None,
        "call_chain": {
            "fe_route": None,
            "java": "lumen-svc-platform（gkxlumen-* Java 门面，只读）",
            "python": "lumen-algo-py /internal/*（写者）",
            "downstream": physical,
        },
        "contract_draft": {
            "request": [],
            "response_key_fields": fields[:6],
            "granularity": {"pk": pk},
            "freshness": "T+1",
        },
        "status": {"demo": "无（三要素标准层未建）", "lumen": "未建", "d1_d4": "n/a（结构卡）"},
        "gaps": gaps,
        "conflicts": [],
        "decision_needed": ["DDL 与是否单独立表 → human:李伟"],
        "structure_escalation": True,
        "risks": [],
        "test_points": tests,
        "confidence": "medium",
        "canonical": {
            "kind": kind,
            "kind_cn": kind_cn,
            "name": name,
            "physical": physical,
            "existence": "missing",
            "fields_draft": fields,
            "primary_key": pk,
            "refresh": refresh,
            "writer": writer,
            "read_by": "lumen-svc-platform（gkxlumen-* Java 门面，只读）",
            "escalate_to": "human:李伟",
            "note": note,
        },
        "source_cards": sources,
        "consumer_cards": consumers,
        "merged_from": prim,
        "merged_also": also,
    }


def src_meta(raw_ids):
    pages, metrics, consumers = [], [], []
    cache = {}
    for rid in raw_ids:
        task, key = rid.split(":", 1)
        if task not in cache:
            cache[task] = yaml.safe_load((BASE / f"{task}.yaml").read_text(encoding="utf-8"))
        hit = next(c for c in cache[task].get("cards") or [] if c.get("int_id") == key)
        pr = hit.get("page_ref")
        for p in ([pr] if isinstance(pr, str) else list(pr or [])):
            if p not in pages:
                pages.append(p)
        for m in hit.get("metric_ids") or []:
            if m not in metrics:
                metrics.append(m)
        if key not in consumers:
            consumers.append(key)
    return pages, metrics, consumers


def prim_of(int_id):
    return [r for r, (t, _) in MAP.items() if t == int_id]


def also_of(int_id):
    return [r for r, (_, a) in MAP.items() if int_id in a]


def build_new():
    specs = []

    def add(**kw):
        pages, metrics, consumers = src_meta(kw.pop("raws"))
        kw["pages"], kw["metrics"], kw["consumers"] = pages, metrics, consumers
        iid = kw["int_id"]
        specs.append(card(prim=prim_of(iid), also=also_of(iid), **kw))

    add(int_id="INT-C-X-491", kind="snapshot", kind_cn="快照",
        name="科技指数家族 sci_index（排名快照 / 指数值 / 趋势 / 指标树，同卡）",
        physical="gkxlumenx_ads.sci_index_rank_snapshot（家族同卡：sci_index_value / sci_index_trend；指标树 gkxlumenx_dim.sci_index_indicator）",
        fields=["period_id", "board", "object_id", "indicator_key", "index_value", "rank", "weight_version", "parent_indicator_id", "level", "as_of"],
        pk="(period_id, board, object_id, indicator_key, weight_version)",
        refresh="按期次追加；保留期数待确认", writer="lumen-algo-py 指数 Job（单写者）",
        dim=["TAL", "TECH", "ORG"], pattern="IP-01/IP-11", ours=["etl", "python_internal"],
        sources=[], gaps=["A10 四类指数对象（指标树/指数值/趋势/排名快照）只此一张家族卡，不拆四张主表"],
        tests=["同一 (period_id, board, object_id, weight_version) 不重复", "正式库 gkxlumenx_ads / gkxlumenx_dim，不写 demo 库"],
        note="逻辑名 ads_sci_index_rank_snapshot；value/trend/indicator 用 kind 区分",
        raws=prim_of("INT-C-X-491"))
    add(int_id="INT-C-TECH-492", kind="ads", kind_cn="ADS",
        name="技术图节点指标 ads_tech_graph_node_metric",
        physical="gkxlumenx_ads.sci_tech_graph_node_metric",
        fields=["technology_id", "metric_id", "metric_value", "as_of", "version"],
        pk="(technology_id, metric_id, as_of)",
        refresh="T+1 / 异步 Job 回写", writer="lumen-algo-py 图指标 Job（单写者）",
        dim=["TECH"], pattern="IP-05", ours=["python_internal"],
        sources=["INT-C-TECH-180"],
        gaps=["技术主数据只引用 C02 INT-C-TECH-180（C05 INT-C-TECH-420），不新造 technology 主表", "与 INT-C-TECH-429 图指标快照不同名；是否合并由 human:李伟 定，本叶不拆四张"],
        tests=["technology_id 必须能在 technology_master 找到", "不出现第二张技术点主表"],
        note="SE-B06-01。中心度/关键节点/优先级/影响力用 metric_id 区分",
        raws=prim_of("INT-C-TECH-492"))
    add(int_id="INT-C-X-493", kind="ads", kind_cn="ADS",
        name="异步分析任务 ads_sci_async_task",
        physical="gkxlumenx_ads.sci_async_task",
        fields=["task_id", "metric_id", "owner", "status", "result_snapshot_id", "created_at", "updated_at"],
        pk="task_id",
        refresh="事件驱动", writer="lumen-algo-py 任务登记（单写者）",
        dim=["TECH"], pattern="IP-04", ours=["python_internal"],
        sources=[],
        gaps=["结果快照不新造，result_snapshot_id 引用 INT-C-X-480（SE-B02-01 ads_sci_result_snapshot）", "不替代存量 lumen_analysis_task（INT-C-TECH-433）；是否并表由 human:李伟 定"],
        tests=["同一用户同一条件至多一条在跑（产品口径另见分析工作区）", "完成行的 result_snapshot_id 在 sci_result_snapshot 中存在"],
        note="SE-B07-01。逻辑名 ads_sci_async_task",
        raws=prim_of("INT-C-X-493"))
    add(int_id="INT-C-TECH-494", kind="ads", kind_cn="ADS",
        name="技术 STAT 预聚合家族（热度/投资额/规模/论文专利量，同卡）",
        physical="gkxlumenx_ads.sci_tech_stat_preagg（家族同卡：ads_tech_query_term_tf / ads_tech_invest_amount / ads_tech_output_scale / ads_tech_paper_patent_cnt）",
        fields=["kind(query_term_tf|invest_amount|output_scale|paper_patent_cnt)", "technology_id", "stat_year", "metric_id", "value", "as_of"],
        pk="(kind, technology_id, metric_id, stat_year, as_of)",
        refresh="T+1", writer="GDF/ETL（单写者）",
        dim=["TECH"], pattern="IP-01", ours=["etl"],
        sources=["INT-C-TECH-180"],
        gaps=["SE-B07-02 四张候选 STAT 只此一张家族卡，不拆四张互不相关的主表", "不替代 C02 技术点主数据，不另造桥接表"],
        tests=["kind 只允许四枚举", "technology_id 引用 technology_master"],
        note="四逻辑名用 kind 区分，物理上一张预聚合家族",
        raws=prim_of("INT-C-TECH-494"))
    add(int_id="INT-C-ORG-495", kind="ads", kind_cn="ADS",
        name="机构绩效查询 ads_org_perf_query",
        physical="gkxlumenx_ads.sci_org_perf_query",
        fields=["org_key（引用 INT-C-ORG-240 / INT-C-ORG-440 主键，本表不另造 org_uid）", "metric_id", "stat_year", "value", "as_of"],
        pk="(org_key, metric_id, stat_year, as_of)",
        refresh="T+1", writer="GDF/ETL（单写者）",
        dim=["ORG"], pattern="IP-01", ours=["etl"],
        sources=["INT-C-ORG-240"],
        gaps=["机构键只引用已有主数据 INT-C-ORG-240（C05 卡 INT-C-ORG-440），不造第二张机构主表"],
        tests=["org_key 都能连到 research_org", "本表字段清单无独立 org_uid 列"],
        note="SE-B09-01",
        raws=prim_of("INT-C-ORG-495"))
    add(int_id="INT-C-ORG-496", kind="ads", kind_cn="ADS",
        name="载体指数 ads_carrier_index（含权重，不另造载体主表）",
        physical="gkxlumenx_ads.sci_carrier_index",
        fields=["org_key（引用 INT-C-ORG-440）", "index_value", "weight_version", "stat_period", "as_of"],
        pk="(org_key, weight_version, stat_period)",
        refresh="T+1 / 周", writer="lumen-algo-py 载体指数 Job（单写者）",
        dim=["ORG"], pattern="IP-04", ours=["python_internal"],
        sources=["INT-C-ORG-240"],
        gaps=["dim_carrier 不单独立表，载体作机构子类型见 INT-C-ORG-440（CF-C05-17）", "cfg 权重作本表 weight_version，不另造 cfg 主表"],
        tests=["org_key 都能连到 research_org", "正式库 gkxlumenx_ads"],
        note="逻辑名 ads_carrier_index。demo 库里的 carrier 只作风险参照，不是落点",
        raws=prim_of("INT-C-ORG-496"))
    add(int_id="INT-C-X-497", kind="ads", kind_cn="ADS",
        name="城市指数 ads_city_index",
        physical="gkxlumenx_ads.sci_city_index",
        fields=["region_code(code_region)", "index_score", "rank_domestic", "rank_global", "weight_version", "stat_period", "as_of"],
        pk="(region_code, weight_version, stat_period)",
        refresh="周 / 年（待确认）", writer="lumen-algo-py 城市指数 Job（单写者）",
        dim=["ORG", "TAL"], pattern="IP-04", ours=["python_internal"],
        sources=[],
        gaps=["不并入 A10 科技指数家族；城市排名与深圳人才指数 tab 同此一张", "地理码引用 code_region / region_scope，不新建地理主数据"],
        tests=["region_code 都能在 code_region 或 region_scope 找到", "正式库 gkxlumenx_ads"],
        note="A06 城市指数与 A08 城市/人才指数 tab",
        raws=prim_of("INT-C-X-497"))
    add(int_id="INT-C-X-498", kind="ads", kind_cn="ADS",
        name="创新空间预聚合家族（密度 / 用地效益，同卡）",
        physical="gkxlumenx_ads.sci_innov_spatial（家族同卡：ads_innov_spatial_density / ads_innov_land_benefit）",
        fields=["kind(spatial_density|land_benefit)", "region_code", "domain_code", "stat_year", "value", "as_of"],
        pk="(kind, region_code, domain_code, stat_year, as_of)",
        refresh="T+1", writer="GDF/ETL（单写者）",
        dim=["TECH"], pattern="IP-01", ours=["etl"],
        sources=[],
        gaps=["A11 密度与用地效益共一张家族卡，不拆两张主表", "地理码引用已有维，不新建地理主数据"],
        tests=["kind 只允许两枚举", "region_code 引用 code_region"],
        note="DS-09 两条共核指标",
        raws=prim_of("INT-C-X-498"))
    return specs


def insert_items(block, key, items):
    if not items:
        return block
    lines = block.split("\n")
    add = [f"  - {x}" for x in items]
    inline = next((i for i, ln in enumerate(lines) if ln == f"  {key}: []"), None)
    if inline is not None:
        lines[inline:inline + 1] = [f"  {key}:"] + add
        return "\n".join(lines)
    idx = next(i for i, ln in enumerate(lines) if ln == f"  {key}:")
    j = idx + 1
    while j < len(lines) and lines[j].startswith("  - "):
        j += 1
    lines[j:j] = add
    return "\n".join(lines)


def main():
    late_rows = yaml.safe_load((WORK / "C05-raw-mentions-late.yaml").read_text(encoding="utf-8"))
    late_ids = [r["raw_id"] for r in late_rows if r["raw_id"].split(":", 1)[0] in LATE_TASKS]
    assert len(late_ids) == len(set(late_ids))
    missing, extra = set(late_ids) - set(MAP), set(MAP) - set(late_ids)
    if missing or extra:
        raise SystemExit(f"map diff missing={sorted(missing)} extra={sorted(extra)}")

    doc = yaml.safe_load(C05.read_text(encoding="utf-8"))
    have = [c["int_id"] for c in doc["cards"]]
    assert have == ORIG, (set(ORIG) - set(have), set(have) - set(ORIG))

    new_cards = build_new()
    new_ids = [c["int_id"] for c in new_cards]
    assert new_ids == [
        "INT-C-X-491", "INT-C-TECH-492", "INT-C-X-493", "INT-C-TECH-494",
        "INT-C-ORG-495", "INT-C-ORG-496", "INT-C-X-497", "INT-C-X-498",
    ]
    assert all(400 <= int(i.rsplit("-", 1)[1]) <= 499 for i in new_ids)

    text = C05.read_text(encoding="utf-8")
    cut = text.index("\ndedup_map:\n")
    head, tail = text[:cut], text[cut:]
    chunks = re.split(r"\n(?=- int_id: )", head)
    assert chunks[1].startswith("- int_id: "), chunks[1][:40]
    by_id = {}
    for ch in chunks[1:]:
        m = re.match(r"- int_id: (\S+)", ch)
        by_id[m.group(1)] = ch
    assert list(by_id) == ORIG

    touched = set()
    for rid, (to, also) in MAP.items():
        touched.add(to)
        touched.update(also)
    for iid in sorted(touched):
        if iid not in by_id:
            continue
        block = by_id[iid]
        block = insert_items(block, "merged_from", [r for r, (t, _) in MAP.items() if t == iid])
        block = insert_items(block, "merged_also", [r for r, (_, a) in MAP.items() if iid in a])
        if iid in NOTES and "supplement_note:" not in block:
            block = block.rstrip("\n") + "\n  supplement_note: " + NOTES[iid] + "\n"
        by_id[iid] = block

    new_yaml = yaml.safe_dump(new_cards, allow_unicode=True, sort_keys=False, width=200).rstrip() + "\n"
    head2 = chunks[0] + "\n" + "\n".join(by_id[i] if not by_id[i].endswith("\n") else by_id[i][:-1] for i in ORIG) + "\n" + new_yaml

    # header counts
    head2 = head2.replace("scope_count: 80\n", "scope_count: 162\n", 1)
    head2 = head2.replace("card_count: 49\n", "card_count: 57\n", 1)
    head2 = head2.replace(
        "scope_note: scope_count = C05-collect 采集的原始 structure_escalation 提法数（B01/C01–C04/A01–A05）；card_count = 归并后的规范结构卡数\n",
        "scope_note: scope_count = C05-collect 采集的原始 structure_escalation 提法数（开工 B01/C01–C04/A01–A05 共 80 + 晚到 A06–A15/B02–B09）；card_count = 归并后的规范结构卡数\n",
        1,
    )
    old_sum = """summary:
  raw_mentions: 80
  raw_by_kind:
    card: 72
    top: 8
  canonical_by_kind:
    ads: 15
    es: 2
    dim: 5
    snapshot: 4
    dwd_master: 3
    map_bridge: 7
    override: 3
    cfg: 3
    user_own: 4
    ods: 1
    cache: 1
    nebula_schema: 1
  structure_escalation: 47
  conflicts: 19
"""
    new_sum = """summary:
  raw_mentions: 162
  raw_by_kind:
    card: 154
    top: 8
  canonical_by_kind:
    ads: 22
    es: 2
    dim: 5
    snapshot: 5
    dwd_master: 3
    map_bridge: 7
    override: 3
    cfg: 3
    user_own: 4
    ods: 1
    cache: 1
    nebula_schema: 1
  structure_escalation: 55
  conflicts: 19
  supplement:
    late_mentions: 82
    merged_into_existing: 58
    new_cards: 8
"""
    if old_sum not in head2:
        raise SystemExit("summary block not found")
    head2 = head2.replace(old_sum, new_sum, 1)

    dedup_lines = []
    for rid, (to, also) in MAP.items():
        dedup_lines.append(f"- raw_id: {rid}")
        dedup_lines.append("  kind: card")
        dedup_lines.append(f"  to: {to}")
        if also:
            dedup_lines.append("  also:")
            dedup_lines.extend(f"  - {x}" for x in also)
        else:
            dedup_lines.append("  also: []")
    if "\ngeo_dim_plan:\n" not in tail:
        raise SystemExit("geo_dim_plan anchor missing")
    tail = tail.replace("\ngeo_dim_plan:\n", "\n" + "\n".join(dedup_lines) + "\ngeo_dim_plan:\n", 1)
    tail = tail.replace("\nstructure_escalation: 47\n", "\nstructure_escalation: 55\n", 1)

    C05.write_text(head2 + tail, encoding="utf-8")

    items = []
    for rid, (to, also) in MAP.items():
        row = {"raw_id": rid, "also": also}
        if to in ORIG:
            row["merged_into"] = to
        else:
            row["new_int_id"] = to
        items.append(row)
    sup = {
        "late_count": len(items),
        "merged_into_existing": sum(1 for x in items if "merged_into" in x),
        "new_card_mentions": sum(1 for x in items if "new_int_id" in x),
        "new_cards": [
            {"int_id": c["int_id"], "name": c["canonical"]["name"], "physical": c["canonical"]["physical"]}
            for c in new_cards
        ],
        "unmapped": [],
        "items": items,
    }
    (WORK / "C05-supplement.yaml").write_text(
        yaml.safe_dump(sup, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print("late", len(items), "merged", sup["merged_into_existing"], "new_mentions", sup["new_card_mentions"], "cards", len(new_cards))


if __name__ == "__main__":
    main()
