# -*- coding: utf-8 -*-
"""生成 SCI-INT-A12.yaml。分析产物，不写业务仓。"""
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
pack = yaml.safe_load((HERE / "_prep" / "A12-pack.yaml").read_text(encoding="utf-8"))
b01 = {m["metric_id"]: m for m in pack["b01_mapping"]}

FE = "/talent/global-talent-situation"
DEMO = "demo-ui-science src/pages/talent-preview/TalentPreviewPage.tsx（有，页键 global）及 src/pages/talent-trend/（有原型）"
LUMEN = "无。lumen-ui-science-pc src/router/menu.ts 仅有菜单 talent/global-talent-situation，resolveNavComponent 落到 DevelopingView.vue，无独立页面与 api"
PAGE = "DS-13-TALENT-GLOBAL"

JAVA_NOTE = "draft；现网无 /situation/v1（B01 R5）；模块归属 DN-07"


def java(path):
    return f"GET {path} ({JAVA_NOTE})"


def card(
    row,
    seq,
    path,
    n,
    pattern,
    algorithm,
    metrics,
    ours,
    counterpart,
    delivery,
    jiuxin,
    call,
    contract,
    d1d4,
    gaps,
    decisions,
    escalation,
    risks,
    tests,
    confidence,
    dep,
    conflicts=None,
    other_metrics=None,
):
    return {
        "int_id": f"INT-A-TAL-{n}",
        "layer": "page",
        "srs": {"excel_row": row, "seq": seq, "path": path},
        "page_ref": PAGE,
        "dimension": ["TAL"],
        "dep_kind": dep,
        "metric_ids": metrics,
        "metric_domain_other": other_metrics or [],
        "algorithm_type": algorithm,
        "integration_pattern": pattern,
        "ours": ours,
        "counterpart": counterpart,
        "delivery_form": delivery,
        "jiuxin_row_id": jiuxin,
        "call_chain": call,
        "contract_draft": contract,
        "status": {"demo": DEMO, "lumen": LUMEN, "d1_d4": d1d4},
        "gaps": gaps,
        "conflicts": conflicts or [],
        "decision_needed": decisions,
        "structure_escalation": escalation,
        "risks": risks,
        "test_points": tests,
        "confidence": confidence,
    }


def chain(j, p, d):
    return {"fe_route": FE, "java": j, "python": p, "downstream": d}


def contract(req, resp, time, geo, fresh):
    return {
        "request": req,
        "response_key_fields": resp,
        "granularity": {"time": time, "geo": geo},
        "freshness": fresh,
    }


D_DRAFT = {"d1": "draft", "d4": "mock"}
D_MISS = {"d1": "missing", "d4": "n/a"}
D_NA = {"d1": "n/a", "d4": "n/a"}
PY_NONE = "在线链路不经 Python（IP-10 不实现，禁止伪数）"
PY_READ = "在线链路不经 Python（读父快照，IP-09）"
PY_SQL = "在线链路不经 Python；离线 lumen-etl-es-py/GDF 执行久新 SQL-98 落 ADS（draft）"
ADS_GEO = "ADS ads_talent_geo_agg（候选，未建；维度 region_code × domain_code × period × talent_type）+ dim_code_region（INT-C-TAL-026）"
BASE_REQ = ["domain_code", "region_code", "geo_level", "time_range", "talent_type"]
BASE_RESP = ["region_code", "region_name", "headcount", "period", "metric_id", "snapshot_id"]

# excel_row -> spec pieces. 路径/seq 从材料包填。
SPEC = {
    246: dict(
        pattern="IP-06", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade", "etl"], counterpart="jiuxin", delivery="SQL", jiuxin="SRS-98",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/distribution"),
            PY_SQL,
            "久新 SQL-98（INT-C-TAL-040）评审后纳入 GDF；原料 dwd_scholar（INT-C-TAL-001，主键未定 P0-1）；" + ADS_GEO,
        ),
        contract=contract(BASE_REQ, BASE_RESP + ["edu_breakdown", "top_orgs"], "year", "country_city", "T+1"),
        d1d4=D_DRAFT, escalation=True, confidence="medium",
        gaps=[
            "人才主键未定：候选 dwd_scholar.scholar_id，卡在供应方 P0-1（INT-C-TAL-001 / OI-C01-01）",
            "城市详情中的学历结构：学历层级缺列（OI-C01-09），该子块置灰，不拿教育经历自由文本硬分层",
            "领域筛选依赖技术领域码，选型未定（OI-C02-02）",
            "区域聚合 ADS 表未建，不能在 Java 里现场 GROUP BY 三方库",
        ],
        decisions=["DN-A12-06", "OI-C01-01", "OI-C01-09", "OI-C02-02"],
        risks=["R-A12-1", "R-A12-6"],
        tests=["国家/城市人数与 ADS 聚合一致，前端不二次计数", "学历层级缺列时子块空态+⚠️，热力人数仍可显示", "USE_MOCK=false 不回落原型假数"],
    ),
    247: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/distribution?geo_level="),
            PY_READ,
            "读 INT-A-TAL-1100 同一 ADS 聚合，按 geo_level / talent_type / time_range 切片；地图缩放只改镜头",
        ),
        contract=contract(BASE_REQ, BASE_RESP, "year", "world_country_province_city", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=["省州层级是否在 dim_code_region 有码未核实（INT-C-TAL-026）", "时间维默认自然年，需规未写死窗口"],
        decisions=["DN-A12-06"],
        risks=["R-A12-1"],
        tests=["切换 geo_level 不新起久新请求", "筛选生物医药只改 domain_code，地图与面板同源"],
    ),
    248: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "service"],
        call=chain(
            java("/situation/v1/talent-global/distribution/focus"),
            PY_READ,
            "城市名走 dim_code_region（INT-C-TAL-026）；机构名待 C03 机构主键与坐标，未定前不编造落点",
        ),
        contract=contract(["q", "q_type"], ["hit_type", "region_code", "org_id", "bbox", "headcount"], "year", "city", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=["机构自动定位依赖机构主键与地理编码（C03，A10 记草案 INT-C-ORG-240），当前无稳定 org_uid", "点击区域后的流动趋势数字不在本叶，见 1103/1109"],
        decisions=["OI-C02-02"],
        risks=["R-A12-1"],
        tests=["城市命中只移动镜头并带上该城聚合", "机构无坐标时提示无法定位，不把字符串哈希成经纬度"],
    ),
    249: dict(
        pattern="IP-08", algorithm="third_party", metrics=["M_TALENT_DEEP_157_1"],
        ours=["frontend", "java_facade", "python_internal"], counterpart="jiuxin", delivery="API", jiuxin="SRS-157",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/migration"),
            "POST /internal/v1/sci/talent/flow (draft；适配久新 API-157；凭据只在 Python)",
            "久新 API-157 结果集（INT-C-TAL-044）；原料候选 dwd_scholar_work_experience（INT-C-TAL-002）；行级边表候选见 INT-C-TAL-071",
        ),
        contract=contract(
            ["domain_code", "time_range", "from_region", "to_region"],
            ["from_region", "to_region", "flow_count", "period", "event_def_version", "snapshot_id"],
            "year", "country_city", "T+1",
        ),
        d1d4=D_DRAFT, escalation=True, confidence="low",
        gaps=[
            "迁徙事件定义未拍板：职位变动、跨国搬迁、机构变动不是同一件事，确认前本图按 IP-10 空态，不把任职履历差分直接当成迁徙",
            "与 A11 excel_row 185「科技人才流动监控」重叠；SCI-INT-A11.yaml 尚未写出，无法引用其 int_id",
            "A11 该叶挂的是 M_INNOV_DS_09_COMPREHENSIVE_006（材料包标 MODEL），与本叶 M_TALENT_DEEP_157_1 不是同一指标",
        ],
        decisions=["DN-A12-02", "DN-01", "DN-09", "OI-C01-03"],
        conflicts=["CF-A12-1", "CF-A12-3"],
        risks=["R-A12-3", "R-A12-7"],
        tests=["event_def_version 为空时响应无 flow_count，前端空态+⚠️", "Java 响应体不含久新域名", "与 1109 读同一 snapshot_id"],
    ),
    250: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "export"],
        call=chain(
            java("/situation/v1/talent-global/distribution/export"),
            PY_READ,
            "弹窗读 INT-A-TAL-1100 聚合；导出文件方案未定，不新建导出任务表",
        ),
        contract=contract(BASE_REQ + ["format"], BASE_RESP + ["job_id"], "year", "country_city", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=["导出格式、权限、水印、是否异步未定，当前不能承诺报告文件", "弹窗学历/行业子块受 OI-C01-09 与领域码约束，缺列则该列空"],
        decisions=["DN-A12-07"],
        risks=["R-A12-1"],
        tests=["导出请求带上当前筛选条件，文件列与面板一致", "方案未定前按钮不可用并说明原因，不返回空文件假装成功"],
    ),
    251: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/chinese-share"),
            PY_NONE,
            "无。三方库无国籍/华人标记列（OI-C01-09）；久新 51 行无华人占比；不从姓名或机构地址推断",
        ),
        contract=contract(
            ["region_code", "org_id", "domain_code"],
            ["reason", "gap_id"],
            "unknown", "country", "unknown",
        ),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:华人占比（分区与机构两个切面）无注册 metric_id，无公式，无源表字段"],
        decisions=["DN-A12-01", "OI-C01-09"],
        conflicts=["CF-A12-2"],
        risks=["R-A12-2"],
        tests=["响应无占比数值字段", "D3 缺口不参与任何排行", "页面空态+⚠️，文案不自造华人定义"],
    ),
    252: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/distribution/insight"),
            PY_READ,
            "同 INT-A-TAL-1100 聚合按大洲/国家/城市与 domain_code、time_range 切片",
        ),
        contract=contract(BASE_REQ, BASE_RESP + ["parent_region_code"], "year", "continent_country_city", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=["结构变化若要学历/类型拆分，受 OI-C01-09 缺列限制，缺的维度不出数", "过去三年窗口是否滚动年未确认（DN-A12-06）"],
        decisions=["DN-A12-06", "OI-C01-09"],
        risks=["R-A12-6"],
        tests=["下钻父区与子区人数可加总关系与口径说明一致（未定前不强制子区之和等于父区）", "筛选条件变化不自动向久新再要一次 SQL"],
    ),
    253: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/orgs/rank"),
            PY_READ,
            "人数切片来自 1100 聚合按 org 分组；机构主数据归 C03；论文量原料 dwd_scholar_papers（INT-C-TAL-007）但本叶无注册指标",
        ),
        contract=contract(["domain_code", "time_range", "top_n"], ["org_id", "org_name", "headcount", "rank"], "year", "org", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=[
            "metric_missing:顶尖机构排名分、近三年论文量无注册 metric_id（人数可挂 M_TALENT_BASE_98_1）",
            "机构主键未定，名称聚合会把同一高校拆成多行",
            "顶尖的入选规则（前 20、榜单来源）未定",
        ],
        decisions=["DN-A12-08", "OI-C02-02"],
        risks=["R-A12-6"],
        tests=["无 org_uid 时不出名次，只出空态", "论文量不在前端用原料现算"],
    ),
    254: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_BASE_98_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-98",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/distribution?org_sector="),
            PY_READ,
            "人数仍是 SQL-98 聚合；产/研标签需机构类型，机构主数据归 C03（dwd_org_base_info / dwd_org_heis_info 尚未并成 org_uid）",
        ),
        contract=contract(BASE_REQ + ["org_sector"], BASE_RESP + ["org_sector", "share"], "year", "country_city", "T+1"),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=["metric_missing:产研人数比例无注册 metric_id", "企业 vs 高校/科研院所的划分口径未定，未定前 org_sector 固定为空、比例字段不返回"],
        decisions=["DN-A12-03"],
        conflicts=["CF-A12-4"],
        risks=["R-A12-6"],
        tests=["口径未确认时切换按钮置灰", "确认后产与研两个视图读同一快照不同 org_sector"],
    ),
    255: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_DEEP_157_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-157",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/migration/hotspots"),
            PY_READ,
            "读 INT-A-TAL-1103 同一 API-157 快照，按流入/流出汇总；不第二路调用久新",
        ),
        contract=contract(
            ["domain_code", "time_range", "direction"],
            ["region_code", "direction", "flow_count", "snapshot_id"],
            "year", "country_city", "T+1",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=["热点阈值（TopN 或绝对人数）未定", "父卡 1103 在事件定义确认前为空态，本叶同步空态", "待 A11 excel_row 185 对齐，避免两套流动预警"],
        decisions=["DN-A12-02"],
        conflicts=["CF-A12-3"],
        risks=["R-A12-7"],
        tests=["hotspots.snapshot_id = migration.snapshot_id", "父卡空态时本叶不显示高亮"],
    ),
    256: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data"],
        call=chain(
            java("/situation/v1/talent-global/activity/bubbles"),
            PY_NONE,
            "无统一人才动态事件流。论文/项目/任职变更是分表原料，不是实时消息；久新无对应行",
        ),
        contract=contract(["region_code", "event_type"], ["reason", "gap_id"], "unknown", "city", "unknown"),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:区域人才动态气泡计数（活跃度）无注册 metric_id，无事件源"],
        decisions=["DN-A12-04"],
        conflicts=["CF-A12-5"],
        risks=["R-A12-4"],
        tests=["不返回气泡条数", "不把论文发表日期伪装成实时消息"],
    ),
    257: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/activity/heat"),
            PY_NONE,
            "无。需规要的是人才动态密度，不是 1100 的人数热力；动态事件无源",
        ),
        contract=contract(["geo_level", "domain_code"], ["reason", "gap_id"], "unknown", "country_city", "unknown"),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:人才动态热力密度无注册 metric_id；禁止用人才人数热力顶替动态热力"],
        decisions=["DN-A12-04"],
        risks=["R-A12-4"],
        tests=["接口与 /distribution 分离，人数接口有数时本接口仍为空", "缩放只改变空态地图层级"],
    ),
    258: dict(
        pattern="IP-09", algorithm="n/a_ops", metrics=[],
        ours=["frontend"], counterpart="none", delivery="none", jiuxin=None,
        dep=["service"],
        call=chain(
            java("/situation/v1/talent-global/activity/focus"),
            PY_READ,
            "镜头定位复用城市维 INT-C-TAL-026；气泡与热力内容随 1110/1111，无内容时只移动地图",
        ),
        contract=contract(["q"], ["region_code", "bbox"], "unknown", "city", "unknown"),
        d1d4=D_NA, escalation=False, confidence="medium",
        gaps=["搜索命中后没有动态可叠加（父叶 IP-10）"],
        decisions=["DN-A12-04"],
        risks=["R-A12-1"],
        tests=["滚轮只改 zoom，不发统计请求", "搜索波士顿只定位，不生成气泡"],
    ),
    259: dict(
        pattern="IP-08", algorithm="third_party", metrics=["M_TALENT_DEEP_157_1"],
        ours=["frontend", "java_facade", "python_internal"], counterpart="jiuxin", delivery="API", jiuxin="SRS-157",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/activity/trends"),
            "POST /internal/v1/sci/talent/flow (draft；与 1103 同一适配，不新开久新接口)",
            "职位流动读 API-157 快照（INT-C-TAL-044）；学术发布、项目启动无事件表",
        ),
        contract=contract(
            ["domain_code", "event_type", "time_range"],
            ["event_type", "period", "flow_count", "snapshot_id"],
            "month", "country", "T+1",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=[
            "metric_missing:学术发布、新项目启动两类动态无注册 metric_id",
            "需规写一周/一月回放，注册流动模型未给月粒度，粒度未确认前不出动画点",
            "事件定义同 DN-A12-02，确认前职位流动也空态",
        ],
        decisions=["DN-A12-02", "DN-A12-04"],
        conflicts=["CF-A12-3", "CF-A12-5"],
        risks=["R-A12-7"],
        tests=["event_type=职位变动且口径未确认时为空", "event_type=学术发布始终为空态，不扫论文表现算"],
    ),
    260: dict(
        pattern="IP-07", algorithm="third_party", metrics=["M_TALENT_GRAPH_110_1"],
        ours=["frontend", "java_facade", "python_internal", "etl"], counterpart="jiuxin", delivery="Python", jiuxin="SRS-110",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}"),
            "POST /internal/v1/sci/talent/ner (draft；久新 Python-110 并入 lumen-algo-py，离线 Job)",
            "在线读 ADS 人才主档投影；实体识别产出 INT-C-TAL-041；主档候选 INT-C-TAL-070，映射 INT-C-TAL-072",
        ),
        contract=contract(
            ["scholar_id"],
            ["scholar_id", "name", "org_name", "title", "field_tags"],
            "offline", "none", "weekly",
        ),
        d1d4=D_DRAFT, escalation=True, confidence="low",
        gaps=[
            "性别、国籍、出生年、职称、学历层级缺列（OI-C01-09），这些字段返回 null+reason，不编造",
            "教育经历原文在 dwd_scholar_education_background（INT-C-TAL-003），没有学历层级码就不能统计",
            "展示前要过个人信息分级（OI-C01-08）",
        ],
        decisions=["DN-A12-01", "OI-C01-01", "OI-C01-08", "OI-C01-09"],
        risks=["R-A12-6", "R-A12-8"],
        tests=["缺列字段键存在但值为 null", "响应不出现 email 等未授权字段", "scholar_id 未定时详情入口不可开"],
    ),
    261: dict(
        pattern="IP-08", algorithm="third_party", metrics=["M_TALENT_DEEP_162_1"],
        ours=["frontend", "java_facade", "python_internal"], counterpart="jiuxin", delivery="API", jiuxin="SRS-162",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/outputs"),
            "POST /internal/v1/sci/talent/academic (draft；适配久新 API-162，含 DS-08-VIZ-001/004，不另开行)",
            "久新 API-162（INT-C-TAL-049）；原料论文 INT-C-TAL-006/007、专利发明人 INT-C-TAL-019、项目参与 INT-C-TAL-014（行数 unknown）",
        ),
        contract=contract(
            ["scholar_id", "time_range"],
            ["paper_count", "patent_count", "project_count", "cited_by", "snapshot_id", "metric_id"],
            "year", "none", "T+1",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=[
            "被引与影响力分值以 162 结果为准，禁止前端用论文表现算",
            "项目参与表行数 unknown（OI-C01-11），162 若不含项目则该格空态",
            "H 指数主源未决（OI-C01-15）：dwd_scholar.h_index 只作降级对照，不在本叶单独开统计",
        ],
        decisions=["OI-C01-15", "OI-C01-03", "DN-09"],
        conflicts=["CF-A12-1"],
        risks=["R-A12-3", "R-A12-9"],
        tests=["论文/专利/项目三格允许部分为 null", "Java 不读 dwd_scholar.h_index 做排序", "快照带 algo_version"],
    ),
    262: dict(
        pattern="IP-09", algorithm="third_party", metrics=["M_TALENT_DEEP_162_1"],
        ours=["frontend", "java_facade"], counterpart="jiuxin", delivery="none", jiuxin="SRS-162",
        dep=["data", "metric"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/influence"),
            PY_READ,
            "读 INT-A-TAL-1115 同一 API-162 快照的 h_index / influence 子字段；学科贡献度无字段则空",
        ),
        contract=contract(
            ["scholar_id", "domain_code"],
            ["h_index", "influence_score", "hindex_source", "snapshot_id"],
            "year", "none", "T+1",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=[
            "metric_missing:学科贡献度无独立 metric_id，162 结果集若无此字段则该格 IP-10",
            "H 指数谁为主见 OI-C01-15，页面只展示 hindex_source，不在前端重算 Hirsch",
        ],
        decisions=["OI-C01-15", "DN-A12-09"],
        conflicts=["CF-A12-1"],
        risks=["R-A12-9"],
        tests=["hindex_source 只允许 jiuxin_162 或 scholar_h_index_fallback", "无学科贡献度字段时不显示 0"],
    ),
    263: dict(
        pattern="IP-07", algorithm="third_party", metrics=["M_TALENT_GRAPH_110_1"],
        ours=["frontend", "java_facade", "python_internal"], counterpart="jiuxin", delivery="Python", jiuxin="SRS-110",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/tags"),
            "POST /internal/v1/sci/talent/ner (draft；与 1114 同一 Python-110 Job)",
            "标签读 ADS 投影；原料 dwd_scholar_research_direction（INT-C-TAL-005）；领域码未定（OI-C02-02）",
        ),
        contract=contract(["scholar_id"], ["scholar_id", "tag", "tag_code", "score", "model_version"], "offline", "none", "weekly"),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=["领域码体系未选定时 tag_code 可空，只回标签文本并标未编码", "NLP 在 lumen-algo-py，Java 不跑模型"],
        decisions=["OI-C02-02", "OI-C01-05"],
        risks=["R-A12-3"],
        tests=["同一 scholar_id 的标签版本与 1114 实体版本一致", "无方向原料时标签为空数组"],
    ),
    264: dict(
        pattern="IP-07", algorithm="third_party", metrics=["M_TALENT_GRAPH_111_1"],
        ours=["frontend", "java_facade", "python_internal", "graph_load"], counterpart="jiuxin", delivery="Python", jiuxin="SRS-111",
        dep=["data", "metric", "algorithm", "graph"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/network"),
            "POST /internal/v1/sci/talent/relations (draft；久新 Python-111 并入 lumen-algo-py；nGQL 只在 Python，图库 TRSGraph)",
            "在线 Java 读 ADS 合作投影；边写入 TRSGraph 人才 EDGE（INT-C-TAL-061）；抽取产出 INT-C-TAL-042；合作原料 dwd_scholar_coauthor（INT-C-TAL-008）",
        ),
        contract=contract(
            ["scholar_id", "depth"],
            ["node_id", "node_name", "edge_type", "org_id", "snapshot_id"],
            "offline", "none", "weekly",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="medium",
        gaps=["TRSGraph 三要素 schema / VID 未确认（OI-C01-14）", "Java 不写 nGQL，也不读 dwm_graph_*", "合作机构名称归一依赖 C03"],
        decisions=["OI-C01-14", "DN-09"],
        risks=["R-A12-10"],
        tests=["响应来自 ADS 投影而非浏览器直连图库", "edge_type 只含合作/任职/毕业/项目共参，流动边不在本叶塞进合作网"],
    ),
    265: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/activities"),
            PY_NONE,
            "无实时动态流。论文见 1115 的存量统计，不能当作最新动态时间线",
        ),
        contract=contract(["scholar_id", "event_type"], ["reason", "gap_id"], "unknown", "none", "unknown"),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:人才最新动态（论文发表、项目申报、学术交流、讲座）无注册 metric_id，无事件表"],
        decisions=["DN-A12-04"],
        conflicts=["CF-A12-5"],
        risks=["R-A12-4"],
        tests=["时间线接口返回空列表与 gap_id", "不从论文表抽最近 N 篇冒充动态"],
    ),
    266: dict(
        pattern="IP-08", algorithm="third_party", metrics=["M_TALENT_DEEP_164_1"],
        ours=["frontend", "java_facade", "python_internal"], counterpart="jiuxin", delivery="API", jiuxin="SRS-164",
        dep=["data", "metric", "algorithm"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/match"),
            "POST /internal/v1/sci/talent/attract (draft；适配久新 API-164)",
            "久新 API-164（INT-C-TAL-051）；需求侧岗位无源（OI-C01-07）。完整引进评估页归 A15，本叶只挂详情入口，A15 产物未出",
        ),
        contract=contract(
            ["scholar_id", "post_id"],
            ["match_score", "risk_flags", "reason", "snapshot_id"],
            "offline", "none", "T+1",
        ),
        d1d4=D_DRAFT, escalation=False, confidence="low",
        gaps=["岗位/招聘需求三方库无源，没有 post_id 时不得产出匹配分", "潜力与风险的分项无本叶注册指标，162/164 未列明的子分展示为空"],
        decisions=["OI-C01-07", "DN-A12-10", "OI-C01-08"],
        conflicts=["CF-A12-1"],
        risks=["R-A12-3", "R-A12-8"],
        tests=["post_id 缺失时 match_score 为 null", "与 A15 共用 API-164 快照键，不各算一套", "海外人才字段按脱敏策略裁剪"],
    ),
    267: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/honors"),
            PY_NONE,
            "无。C01 人才表清单无奖项/荣誉表；久新无对应行",
        ),
        contract=contract(["scholar_id"], ["reason", "gap_id"], "unknown", "none", "unknown"),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:荣誉奖项数量与社会影响力无注册 metric_id，无源表"],
        decisions=["DN-A12-05"],
        risks=["R-A12-4"],
        tests=["不从人才头衔文本拆奖项", "空态+⚠️"],
    ),
    268: dict(
        pattern="IP-10", algorithm="UNKNOWN", metrics=[],
        ours=["frontend", "java_facade"], counterpart="none", delivery="none", jiuxin=None,
        dep=["data"],
        call=chain(
            java("/situation/v1/talent-global/talents/{scholar_id}/visits"),
            PY_NONE,
            "无出访/海外交流表。dwd_rel_project_scholar（INT-C-TAL-014，行数 unknown）只是项目参与，不能当作出访记录",
        ),
        contract=contract(["scholar_id"], ["reason", "gap_id"], "unknown", "none", "unknown"),
        d1d4=D_MISS, escalation=False, confidence="high",
        gaps=["metric_missing:国际合作项目清单、出访记录、海外学术交流无注册 metric_id；出访无源表"],
        decisions=["DN-A12-05", "OI-C01-11"],
        risks=["R-A12-4"],
        tests=["不把合作者国别或项目参与渲染成出访时间线", "空态+⚠️"],
    ),
}


def main():
    leaves = pack["srs"]
    assert [s["excel_row"] for s in leaves] == list(range(246, 269)), "pack rows"
    cards = []
    for i, s in enumerate(leaves):
        spec = SPEC[s["excel_row"]]
        pack_metrics = [m["metric_id"] for m in s.get("metrics") or []]
        for mid in pack_metrics:
            assert mid in spec["metrics"], (s["excel_row"], mid)
            assert b01[mid]["algorithm_type"] == "third_party"
        cards.append(
            card(
                s["excel_row"], s["seq"], s["path"], 1100 + i,
                spec["pattern"], spec["algorithm"], spec["metrics"],
                spec["ours"], spec["counterpart"], spec["delivery"], spec["jiuxin"],
                spec["call"], spec["contract"], spec["d1d4"], spec["gaps"],
                spec["decisions"], spec["escalation"], spec["risks"], spec["tests"],
                spec["confidence"], spec["dep"], spec.get("conflicts"),
            )
        )
    doc = {
        "task_id": "SCI-INT-A12",
        "scope_count": 23,
        "card_count": len(cards),
        "gap": [],
        "chinese_share_verdict": {
            "question": "华人占比（excel_row 251）数据来源",
            "source_class": "无源",
            "conclusion": "三方库无国籍/华人标记列（OI-C01-09：性别/国籍/出生年/职称/学历层级缺列）。久新 51 行没有华人占比。材料包本叶 metrics 为空。不从姓名、机构地址或论文语种推断华人。集成模式 IP-10：空态+⚠️，不出数。华人定义与分母登记 DN-A12-01，不替甲方定口径。",
        },
        "migration_verdict": {
            "question": "迁徙图（excel_row 249、255）数据来源",
            "source_class": "久新",
            "raw_candidate": "dwd_scholar_work_experience（INT-C-TAL-002）只是任职原料，不是迁徙事件",
            "conclusion": "主源是久新 API-157 人才流动追踪（M_TALENT_DEEP_157_1，IP-08，INT-C-TAL-044，行 SRS-157），不是无源。迁徙事件定义（职位变动 / 跨国 / 换机构）未拍板，确认前 1103/1109/1113 按 IP-10 空态降级，禁止用任职履历自行差分。A11 excel_row 185「科技人才流动监控」与本页重叠，但 SCI-INT-A11.yaml 不存在，本页独立出卡；该叶指标是 M_INNOV_DS_09_COMPREHENSIVE_006（材料包标 MODEL），与 DEEP_157 并列待对齐（CF-A12-3）。行级边表候选 INT-C-TAL-071，本页 1103 升结构。",
        },
        "a11_overlap": {
            "a11_yaml": "无",
            "excel_row": 185,
            "seq": 182,
            "name": "科技人才流动监控",
            "a11_metric": "M_INNOV_DS_09_COMPREHENSIVE_006",
            "note": "A11 是科技发展规划中的一叶，不是整叶都等于人才流动。本页不引用尚未写出的 A11 int_id。",
        },
        "cards": cards,
        "summary": {},
    }
    # summary filled after so it matches check
    from collections import Counter
    ids = [c["int_id"] for c in cards]
    by_type = Counter(i.split("-")[2] for i in ids)
    doc["summary"] = {
        "cards_by_type": {k: by_type[k] for k in ("TAL", "TECH", "ORG", "X") if by_type[k]},
        "srs_rows_covered": len({c["srs"]["excel_row"] for c in cards}),
        "jiuxin_rows_referenced": sorted({c["jiuxin_row_id"] for c in cards if c["jiuxin_row_id"]}),
        "jiuxin_new_rows_needed": 0,
        "page_metrics_assignment": {},
        "metric_missing_cards": sorted(c["int_id"] for c in cards if any(g.startswith("metric_missing") for g in c["gaps"])),
        "structure_escalation_cards": sorted(c["int_id"] for c in cards if c["structure_escalation"]),
        "lumen_page": "无",
        "demo_page": "有",
    }
    assign = {}
    for c in cards:
        for m in c["metric_ids"]:
            assign.setdefault(m, []).append(c["srs"]["excel_row"])
    doc["summary"]["page_metrics_assignment"] = {m: sorted(v) for m, v in sorted(assign.items())}
    doc["decision_needed"] = [
        {"id": "DN-A12-01", "owner": "甲方", "item": "华人定义（国籍、华裔、姓名或其他）与占比分母（全球领域人才范围）。确认前 IP-10"},
        {"id": "DN-A12-02", "owner": "甲方", "item": "迁徙事件定义：职位变动、跨国搬迁、机构变动是否都算；与 A11 row 185 是否同一口径。确认前迁徙图空态"},
        {"id": "DN-A12-03", "owner": "甲方", "item": "产与研的机构类型划分（企业 / 高校 / 科研院所），以及一人多机构时怎么归类"},
        {"id": "DN-A12-04", "owner": "甲方", "item": "人才动态事件有哪些类型、是否要求实时。当前无事件流，气泡/动态热力/最新动态走 IP-10"},
        {"id": "DN-A12-05", "owner": "甲方", "item": "荣誉奖项与出访/海外交流是否建设、由谁供数。当前无表"},
        {"id": "DN-A12-06", "owner": "甲方", "item": "分布统计的时间窗（默认自然年）与地图层级（全球/国家/省州/城市）是否都要"},
        {"id": "DN-A12-07", "owner": "产品 + 甲方", "item": "分布数据导出的格式、权限与水印。未定前不交付文件"},
        {"id": "DN-A12-08", "owner": "甲方", "item": "顶尖机构的入选规则与机构榜来源"},
        {"id": "DN-A12-09", "owner": "PM / human:郭万迎", "item": "学科贡献度是否进入 API-162 结果集；不进入则该格保持 IP-10。H 指数主源沿用 OI-C01-15"},
        {"id": "DN-A12-10", "owner": "产品", "item": "详情页匹配度与 A15 人才引进推荐评估的边界：本叶只读 API-164，需求侧岗位仍无源（OI-C01-07）"},
    ]
    doc["decision_referenced"] = [
        "OI-C01-01", "OI-C01-03", "OI-C01-07", "OI-C01-08", "OI-C01-09", "OI-C01-11", "OI-C01-14", "OI-C01-15",
        "OI-C02-02", "DN-01", "DN-07", "DN-09",
    ]
    doc["risks"] = [
        {"id": "R-A12-1", "level": "high", "desc": "lumen 无本页。菜单落到 DevelopingView，/situation/v1 无 Java 实现（B01 R5）", "mitigation": "DN-07 定门面后再按本卡拆端点"},
        {"id": "R-A12-2", "level": "high", "desc": "若用姓名、地址或论文语种计算华人占比，等于替甲方定义华人", "mitigation": "DN-A12-01 确认前 IP-10，接口无数值"},
        {"id": "R-A12-3", "level": "high", "desc": "久新 SRS-98/110/111/157/162/164 交付形态与 SLA 均待确认（B01 R2 / DN-01 / OI-C01-03）", "mitigation": "IP-08 熔断读快照；无快照空态"},
        {"id": "R-A12-4", "level": "high", "desc": "动态气泡、动态热力、最新动态、奖项、出访无源。用人数或论文列表填上会伪闭合", "mitigation": "IP-10，与 distribution 接口分开"},
        {"id": "R-A12-5", "level": "medium", "desc": "/metrics/v1/catalog 仅 ENT，无 D1–D4（B01 R3/C5）。本页 6 个 TAL 指标的 ⓘ 目前会空", "mitigation": "IP-12；catalog 失败时保留 ⓘ 并提示口径加载失败"},
        {"id": "R-A12-6", "level": "high", "desc": "scholar_id 未定（P0-1）时，分布、详情、迁徙的主键都不稳定", "mitigation": "阻塞项沿用 INT-C-TAL-001 / 070 / 072，本页不新造 ID"},
        {"id": "R-A12-7", "level": "medium", "desc": "迁徙图与 A11 row 185 可能各做一套流动预警", "mitigation": "A11 卡写出后对齐；在此之前只保留 API-157 一条快照"},
        {"id": "R-A12-8", "level": "medium", "desc": "详情含履历与匹配，涉及个人信息分级（OI-C01-08）", "mitigation": "未分级字段不出接口"},
        {"id": "R-A12-9", "level": "medium", "desc": "H 指数若在前端或 Java 用 dwd_scholar.h_index 直接排序，会绕过 OI-C01-15", "mitigation": "只展示 162 快照；降级源必须带 hindex_source"},
        {"id": "R-A12-10", "level": "medium", "desc": "合作网络若 Java 写 nGQL 或连非 TRSGraph，违反铁律", "mitigation": "Java 只读 ADS 投影；Python 写 TRSGraph"},
    ]
    doc["conflicts"] = [
        {"id": "CF-A12-1", "desc": "M_TALENT_DEEP_157_1 / 162_1 / 164_1 与 GRAPH_110/111 在材料包 algorithm_type=third_party，久新行侧常标 MODEL/Python（同 B01 C2）。卡片算法类型以材料包为准"},
        {"id": "CF-A12-2", "desc": "需规要求展示华人占比，数据侧无字段、无指标、无久新行。功能保留为空态，不删需求也不造数"},
        {"id": "CF-A12-3", "desc": "A12 迁徙（DEEP_157，third_party，久新 API-157）与 A11 row 185（M_INNOV_DS_09_COMPREHENSIVE_006，材料包标 MODEL）都在描述人才流动，指标与页面不同，口径是否同一未定"},
        {"id": "CF-A12-4", "desc": "产研对比要机构类型，人才主数据没有稳定 org_uid（C03）。人数模型本身不带产/研标签"},
        {"id": "CF-A12-5", "desc": "需规写实时气泡与最新动态，供应与久新都没有事件流，刷新频率默认只是 T+1 草案（OI-C01-13）"},
    ]
    doc["structure_escalation_to"] = "human:李伟"
    header = """# SCI-INT-A12 · 全球领域人才态势 · 页面级系统集成依赖卡片
# 范围：SRS 科技人才态势/全球领域人才态势.md excel_row 246–268（seq 243–265，23 叶）
# 页面：DS-13-TALENT-GLOBAL
# 模板：产物/_card-template.yaml；algorithm_type / d1_d4 取自材料包（MCP 口径：third_party / draft / mock）
# 引用不重分析：C01（dwd_scholar INT-C-TAL-001，P0-1；SQL-98 INT-C-TAL-040；API-157 INT-C-TAL-044；
#   Python-110/111 INT-C-TAL-041/042；API-162 INT-C-TAL-049 含 DS-08-VIZ-001/004；API-164 INT-C-TAL-051；
#   主档/流动边/映射 INT-C-TAL-070/071/072；区划 INT-C-TAL-026；OI-C01-09 缺国籍等列；OI-C01-15 H 指数主源）
# 前端：lumen 无本页（菜单落到 DevelopingView）；demo 有原型。D12：调用链不指向 demo-* 服务
# 迁徙与 A11 row 185 重叠，A11 卡片文件不存在，本页独立出卡

"""
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120)
    out = HERE / "SCI-INT-A12.yaml"
    out.write_text(header + body, encoding="utf-8")
    print(f"wrote {out} cards={len(cards)}")


if __name__ == "__main__":
    main()
