# DR-RES-MOCK-LOAD-L01
# ponytail: full
# 只写 MySQL demo_gkxlumenx_ads。重复执行先按本脚本的 calc_batch_id 删除再插入。
# 密码从本机配置读取，不写进本文件。禁止写 gkxlumenx_ads / ODS / DWD / 久新 / gkxlumenx_gapfill。
# 年度 total = grain=year 且 metric=volume、渠道/表名/业务类型都空的最后一年 row_count。
# 该数必须等于 slice_kind=structure 的 value 之和。
# 主题库行数、问题行数、status=pending 任务数分别对应主题库数量、问题资源数、待处理任务。

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import pymysql

WRITE_DB = "demo_gkxlumenx_ads"
MYSQL_HOST = "10.50.11.76"
MYSQL_PORT = 3306
MOCK_BATCH = "mock_dr_res_load_l01"
SNAP_BATCH = "snap_dr_res_load_l01"
FILL = "manual"

HERE = Path(__file__).resolve()
ORCH = HERE.parents[3]
GKX = ORCH.parent
YML = GKX / "repos" / "lumen-svc-platform" / "gkxlumen-element" / "src" / "main" / "resources" / "application-local.yml"
DORIS_README = (
    ORCH / "agent-delivery" / "data" / "GDF" / "派单包" / "技术节点产业映射" / "GDF-TECH-NODE-WORKPACK" / "README.md"
)

TABLES = (
    "gapfill_dr_type_slice",
    "gapfill_dr_source_channel",
    "gapfill_dr_catalog_item",
    "gapfill_dr_ingest_task",
    "gapfill_dr_collection_fact",
    "gapfill_dr_theme_library",
    "gapfill_dr_theme_column",
    "gapfill_dr_quality_issue",
    "gapfill_dr_usage_subject",
    "gapfill_dr_usage_series",
    "gapfill_dr_call_event",
    "gapfill_dr_api_probe",
    "gapfill_dr_graph_node",
    "gapfill_dr_resource_link",
    "gapfill_dr_block_json",
    "gapfill_dr_entity_year",
    "gapfill_dr_column_catalog",
)

STRUCTURE = (
    ("结构化数据", 12580, "#165dff", "高热", "成熟期"),
    ("非结构化数据", 8932, "#36cfc9", "高热", "成长期"),
    ("半结构化数据", 5641, "#9254de", "中热", "成长期"),
    ("实时流数据", 3245, "#ff7a45", "升温", "导入期"),
)
THEMES_SLICE = (
    ("基础科学", 4230, 92),
    ("工程技术", 3890, 88),
    ("医学健康", 3156, 95),
    ("农业科技", 2845, 86),
    ("能源环境", 2634, 84),
    ("信息技术", 2456, 91),
    ("材料科学", 1987, 89),
)
YEAR_TOTAL = sum(item[1] for item in STRUCTURE)
ADDED_LAST = 3678
YEAR_PREV = YEAR_TOTAL - ADDED_LAST
MONTHS_6 = ("2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05")
MONTHS_12 = tuple(f"2026-{i:02d}" for i in range(1, 13))

SRS = (
    ("domestic_db", "国内数据库", (980, 1050, 1120, 1180, 1260), 6820, 186, 22.4, 14.2, 93, 91, "#165dff", ("CNKI", "万方", "国家科技报告"), "权威库占比高，元数据规范，更新周期稳定"),
    ("foreign_db", "国外数据库", (620, 680, 720, 760, 820), 4560, 98, 15.0, 8.6, 96, 94, "#722ed1", ("Web of Science", "Scopus", "PubMed"), "国际主流库，引用链完整，许可合规需持续关注"),
    ("institute", "科研院所", (1180, 1250, 1320, 1400, 1480), 8234, 245, 27.1, 12.5, 95, 93, "#36cfc9", ("中科院", "行业所", "重点实验室"), "实验与观测数据为主，溯源清晰，字段标准待统一"),
    ("enterprise", "企业", (680, 740, 820, 920, 1020), 5234, 168, 17.2, 18.3, 82, 86, "#ff7a45", ("龙头企", "专精特新", "产业联盟"), "产业场景丰富，部分接口稳定性与脱敏规则需复核"),
    ("opensource", "开源平台", (520, 580, 660, 780, 920), 5550, 142, 18.3, 22.1, 78, 84, "#00b42a", ("GitHub", "Kaggle", "HuggingFace"), "创新活跃、增速快，版本与许可证变更需定期巡检"),
)
ORGS = (
    ("research", "科研机构", 1286, 96, "活跃"),
    ("university", "高等院校", 1048, 88, "活跃"),
    ("company", "企业单位", 836, 76, "活跃"),
    ("government", "政府部门", 432, 58, "一般"),
    ("intl", "国际组织", 186, 36, "较低"),
)

# 最新月 volume 用来源快照（饼图），前 5 个月用结构趋势。同一 volume 列不能同时当存量和月增量。
# ponytail: 趋势末点被快照存量替换；要拆开需另加列，本表没有第二个体量列。

ADDED_M = (450, 520, 480, 620, 580, 720, 680, 750, 820, 780, 850, 920)
UPDATED_M = (320, 380, 420, 450, 480, 520, 560, 590, 620, 680, 720, 780)
WEEK_A = (118, 132, 125, 148, 156, 142, 168, 175)
WEEK_U = (86, 92, 98, 105, 112, 108, 120, 128)
DAY_A = (22, 28, 19, 31, 26, 24, 29)
DAY_U = (15, 18, 14, 21, 19, 17, 20)
DAY_LABELS = ("2026-05-16", "2026-05-17", "2026-05-18", "2026-05-19", "2026-05-20", "2026-05-21", "2026-05-22")
CHANNEL_M = {
    "科研院所": (2100, 2300, 2500, 2800, 3100, 3450),
    "企业": (1400, 1550, 1700, 1900, 2100, 2320),
    "第三方平台": (900, 1000, 1100, 1250, 1400, 1580),
}

TASK_PLAN = (
    ("API接口", "done", 6),
    ("API接口", "running", 1),
    ("API接口", "pending", 1),
    ("文件传输", "done", 3),
    ("文件传输", "running", 1),
    ("文件传输", "pending", 1),
    ("数据库同步", "done", 2),
    ("数据库同步", "running", 1),
    ("数据库同步", "pending", 1),
    ("人工录入", "done", 1),
    ("人工录入", "pending", 1),
    ("物联网采集", "running", 1),
)

ISSUE_NAMES = (
    "基因测序数据_批次20250615",
    "气象观测数据_深圳站",
    "工程图纸_桥梁设计",
    "临床试验数据_二期",
    "卫星遥感数据_华南区",
    "专利数据_电子工程",
    "论文元数据_ScienceDirect",
    "水质监测数据_长江流域",
    "作物长势栅格_华北样带",
    "工业时序_产线A3",
    "开源权重镜像_批次7",
    "纳米表征谱图_沪区",
    "海洋站温盐_东海",
    "人才名录_重复主键",
    "政策全文_编码异常",
    "能耗小时表_缺测",
    "影像序列_UID冲突",
    "工艺参数_单位混用",
    "土壤墒情_延迟三日",
    "引文索引_空标题",
    "传感器心跳_中断",
    "学位论文_缺作者",
    "靶点活性_超范围",
    "图纸版本_双活",
    "排放口_时钟漂移",
    "代码仓索引_许可证空",
    "蛋白结构_坐标缺失",
    "农情月报_迟到",
    "威胁情报_字段错位",
    "材料硬度_重复批次",
)
ISSUE_TYPES = (
    ("完整性异常", "#ff4d4f"),
    ("时效性延迟", "#ff7a45"),
    ("格式不兼容", "#faad14"),
    ("准确性存疑", "#9254de"),
    ("更新中断", "#165dff"),
    ("内容冲突", "#36cfc9"),
)
ISSUE_CATS = ("医学健康", "能源环境", "基础科学", "信息技术", "工程技术", "材料科学", "农业科技")
ISSUE_CLUSTERS = ("生命科学数据群", "环境观测数据群", "基础科研数据群", "工程制造数据群", "网络安全数据群")
ISSUE_LEVELS = ("紧急", "重要", "普通")
ISSUE_STATUS = ("pending", "processing", "resolved")
INGEST = ("API接口", "文件传输", "数据库同步", "人工录入", "物联网采集")

THEMES = (
    {
        "name": "基础研究主题库",
        "category": "基础科学",
        "resource_type": "结构化数据",
        "tags": ["文献计量", "实验数据", "基础学科"],
        "table_count": 156,
        "record_yi": 2.3,
        "storage_tb": 4.5,
        "quality": 94,
        "source_name": "中科院",
        "region": "华北",
        "update_freq": "每周",
        "related_project": "基础学科协同研究计划",
        "description": "涵盖数学、物理、化学等基础学科研究数据",
        "tables": (
            ("exp_raw_data", "实验原始数据表", (("sample_id", "VARCHAR(64)", "样本唯一标识", 1), ("experiment_date", "DATE", "实验采集日期", 1), ("raw_payload", "JSON", "原始实验读数", 1))),
            ("lit_metadata", "文献元数据表", (("paper_id", "VARCHAR(48)", "文献唯一编号", 1), ("title", "VARCHAR(512)", "论文题名", 1), ("pub_year", "INT", "发表年份", 1))),
        ),
    },
    {
        "name": "工程技术主题库",
        "category": "工程技术",
        "resource_type": "半结构化数据",
        "tags": ["智能制造", "工艺参数", "工程设计"],
        "table_count": 234,
        "record_yi": 1.8,
        "storage_tb": 3.2,
        "quality": 91,
        "source_name": "清华大学",
        "region": "华北",
        "update_freq": "每日",
        "related_project": "智能制造工艺优化专项",
        "description": "包含机械、电子、土木等工程领域数据",
        "tables": (
            ("eng_drawing", "工程设计图纸表", (("drawing_id", "VARCHAR(64)", "图纸编号", 1), ("format_type", "VARCHAR(16)", "文件格式", 1))),
            ("process_param", "制造工艺参数表", (("param_id", "VARCHAR(48)", "工艺参数记录 ID", 1), ("line_code", "VARCHAR(32)", "产线编码", 1))),
        ),
    },
    {
        "name": "医学健康主题库",
        "category": "医学健康",
        "resource_type": "非结构化数据",
        "tags": ["精准医疗", "影像组学", "基因组学"],
        "table_count": 189,
        "record_yi": 1.5,
        "storage_tb": 5.8,
        "quality": 96,
        "source_name": "北京大学医学部",
        "region": "华北",
        "update_freq": "每日",
        "related_project": "精准医疗联合攻关",
        "description": "汇集临床、影像、基因等医学研究数据",
        "tables": (
            ("clinical_case", "临床病例结构化表", (("case_id", "VARCHAR(64)", "病例唯一 ID", 1), ("diagnosis_code", "VARCHAR(16)", "ICD 诊断编码", 1))),
            ("gene_variant", "基因变异记录表", (("variant_id", "VARCHAR(64)", "变异位点 ID", 1), ("chromosome", "VARCHAR(4)", "染色体编号", 1))),
        ),
    },
    {
        "name": "农业科技主题库",
        "category": "农业科技",
        "resource_type": "结构化数据",
        "tags": ["智慧农业", "产量评估", "气象"],
        "table_count": 128,
        "record_yi": 0.9,
        "storage_tb": 2.1,
        "quality": 88,
        "source_name": "中国农科院",
        "region": "华东",
        "update_freq": "每月",
        "related_project": "智慧农业示范县建设",
        "description": "覆盖种植、养殖、农产品等农业数据",
        "tables": (("crop_growth", "作物生长监测表", (("plot_id", "VARCHAR(32)", "地块编号", 1), ("crop_type", "VARCHAR(64)", "作物品种", 1))),),
    },
    {
        "name": "能源环境主题库",
        "category": "能源环境",
        "resource_type": "实时流数据",
        "tags": ["碳排放", "环境监测", "新能源"],
        "table_count": 112,
        "record_yi": 0.76,
        "storage_tb": 3.0,
        "quality": 86,
        "source_name": "能源研究所",
        "region": "华南",
        "update_freq": "实时",
        "related_project": "碳达峰监测评估工程",
        "description": "汇集新能源、环境监测、气候等数据",
        "tables": (("emission_monitor", "排放监测实时表", (("site_id", "VARCHAR(32)", "监测点位 ID", 1), ("co2_ppm", "DECIMAL(8,2)", "二氧化碳浓度", 1))),),
    },
    {
        "name": "信息技术主题库",
        "category": "信息技术",
        "resource_type": "非结构化数据",
        "tags": ["人工智能", "大数据", "网络安全"],
        "table_count": 145,
        "record_yi": 0.68,
        "storage_tb": 2.8,
        "quality": 92,
        "source_name": "华为公司",
        "region": "华南",
        "update_freq": "每周",
        "related_project": "网络安全态势感知平台",
        "description": "覆盖 AI、大数据、网络安全等方向",
        "tables": (("net_sec_event", "网络安全事件表", (("event_id", "VARCHAR(64)", "安全事件 ID", 1), ("severity", "VARCHAR(16)", "威胁等级", 1))),),
    },
    {
        "name": "材料科学主题库",
        "category": "材料科学",
        "resource_type": "半结构化数据",
        "tags": ["纳米材料", "表征分析", "新材料"],
        "table_count": 98,
        "record_yi": 0.45,
        "storage_tb": 1.8,
        "quality": 90,
        "source_name": "上海交大",
        "region": "华东",
        "update_freq": "每两周",
        "related_project": "新材料研发专项",
        "description": "纳米材料、复合材料等研发数据",
        "tables": (("material_property", "材料性能测试表", (("material_id", "VARCHAR(48)", "材料样本 ID", 1), ("test_method", "VARCHAR(64)", "测试方法标准", 1))),),
    },
    {
        "name": "海洋与地球主题库",
        "category": "地球与海洋",
        "resource_type": "结构化数据",
        "tags": ["海洋调查", "温盐", "深海"],
        "table_count": 64,
        "record_yi": 0.32,
        "storage_tb": 0.9,
        "quality": 87,
        "source_name": "海洋一所",
        "region": "华东",
        "update_freq": "每月",
        "related_project": "深海探测工程",
        "description": "海洋调查与地球观测主题数据",
        "tables": (("ocean_station", "海洋站观测表", (("station_id", "VARCHAR(32)", "站点编号", 1), ("obs_time", "DATETIME", "观测时间", 1), ("salinity", "DECIMAL(6,3)", "盐度", 0))),),
    },
)


def j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def blocks() -> dict:
    return {
        "overview_classify": {
            "totalResources": 839,
            "autoTagged": 812,
            "manualReview": 27,
            "accuracy": 96.8,
            "lastRun": "2026-05-22 08:30",
        },
        "semantic_theme": {
            "clusters": [
                {"id": "stc-001", "theme": "精准医疗·多组学", "features": ["基因变异", "影像组学", "个体化诊疗"], "cohesion": 0.93, "resourceCount": 3, "resources": [{"id": "rad-002", "name": "基因变异数据库", "category": "医学健康", "similarity": 0.96}, {"id": "kg-n6", "name": "医学影像库", "category": "医学健康", "similarity": 0.91}]},
                {"id": "stc-002", "theme": "智能制造·数字孪生", "features": ["工艺参数", "设备传感", "质量闭环"], "cohesion": 0.89, "resourceCount": 2, "resources": [{"id": "rad-003", "name": "智能制造工艺参数库", "category": "工程技术", "similarity": 0.95}, {"id": "ds-iot", "name": "工业物联网时序库", "category": "信息技术", "similarity": 0.86}]},
                {"id": "stc-003", "theme": "绿色低碳·环境监测", "features": ["大气组分", "排放溯源", "气候响应"], "cohesion": 0.87, "resourceCount": 2, "resources": [{"id": "rad-004", "name": "大气环境监测数据", "category": "能源环境", "similarity": 0.94}, {"id": "ds-energy", "name": "清洁能源出力库", "category": "能源环境", "similarity": 0.85}]},
                {"id": "stc-004", "theme": "新材料·表征发现", "features": ["纳米结构", "性能表征", "高通量筛选"], "cohesion": 0.91, "resourceCount": 2, "resources": [{"id": "rad-006", "name": "纳米材料表征库", "category": "材料科学", "similarity": 0.97}, {"id": "ds-ht", "name": "高通量材料实验库", "category": "材料科学", "similarity": 0.89}]},
            ],
            "fusionTrends": [
                {"id": "ft-001", "themes": ["医学健康", "信息技术"], "strength": 0.91, "direction": "AI辅助精准诊疗", "insight": "基因与影像特征共现，跨主题检索热度上升。", "relatedClusterIds": ["stc-001"]},
                {"id": "ft-002", "themes": ["工程技术", "信息技术"], "strength": 0.86, "direction": "工业大模型驱动的工艺优化", "insight": "工艺参数与时序传感语义簇重合。", "relatedClusterIds": ["stc-002"]},
                {"id": "ft-003", "themes": ["能源环境", "基础科学"], "strength": 0.84, "direction": "陆海统筹气候韧性评估", "insight": "大气监测与海洋调查特征融合增强。", "relatedClusterIds": ["stc-003"]},
                {"id": "ft-004", "themes": ["材料科学", "基础科学"], "strength": 0.88, "direction": "极端条件材料发现", "insight": "表征库与高能实验数据语义邻近度提升。", "relatedClusterIds": ["stc-004"]},
            ],
        },
        "partition": {
            "byRegion": [
                {"name": "华北", "resourceCount": 8560, "dataVolume": "6.8TB", "avgQuality": 93.2, "orgs": ["中科院", "清华大学", "北京大学"], "trend": [8200, 8450, 8560]},
                {"name": "华东", "resourceCount": 7845, "dataVolume": "5.4TB", "avgQuality": 91.5, "orgs": ["上海交大", "浙江大学"], "trend": [7500, 7680, 7845]},
                {"name": "华南", "resourceCount": 6342, "dataVolume": "4.2TB", "avgQuality": 90.8, "orgs": ["华为公司", "深圳市政府"], "trend": [6100, 6250, 6342]},
                {"name": "华西", "resourceCount": 4523, "dataVolume": "2.9TB", "avgQuality": 89.1, "orgs": ["四川大学", "西安交大"], "trend": [4300, 4410, 4523]},
                {"name": "其他", "resourceCount": 3128, "dataVolume": "1.5TB", "avgQuality": 87.6, "orgs": ["东北大学", "厦门大学"], "trend": [3000, 3080, 3128]},
            ],
            "byDatabase": [
                {"name": "文献计量数据库", "resourceCount": 6850, "dataVolume": "5.2TB", "avgQuality": 92.4, "trend": [6500, 6700, 6850]},
                {"name": "领域主题数据库", "resourceCount": 8420, "dataVolume": "6.1TB", "avgQuality": 91.0, "trend": [8000, 8200, 8420]},
                {"name": "科技情报数据库", "resourceCount": 7230, "dataVolume": "4.8TB", "avgQuality": 90.2, "trend": [6900, 7100, 7230]},
                {"name": "科技要素数据库", "resourceCount": 7898, "dataVolume": "4.7TB", "avgQuality": 89.6, "trend": [7500, 7700, 7898]},
            ],
            "byInstitution": [
                {"name": "科研院所", "resourceCount": 8234, "dataVolume": "6.2TB", "avgQuality": 93.1, "topResource": "高能物理实验数据集", "trend": [7900, 8100, 8234]},
                {"name": "高等院校", "resourceCount": 6856, "dataVolume": "5.1TB", "avgQuality": 91.2, "topResource": "基础研究主题库", "trend": [6500, 6700, 6856]},
                {"name": "政府部门", "resourceCount": 5634, "dataVolume": "3.4TB", "avgQuality": 89.5, "topResource": "环境监测数据", "trend": [5400, 5550, 5634]},
                {"name": "企业单位", "resourceCount": 4234, "dataVolume": "2.8TB", "avgQuality": 88.3, "topResource": "智能制造参数库", "trend": [4000, 4120, 4234]},
                {"name": "国际组织", "resourceCount": 1245, "dataVolume": "0.9TB", "avgQuality": 90.6, "topResource": "全球气候数据集", "trend": [1100, 1180, 1245]},
            ],
        },
        "big_data_center": {
            "overview": {"totalDatabases": 28, "totalTables": 1248, "totalRecords": "10.2亿", "totalStorage": "18.6TB"},
            "categories": [
                {"key": "element", "name": "科技要素数据库", "count": 9, "tables": 412, "records": "3.5亿", "description": "专利、论文、项目、人才等科技要素基础库", "updateStatus": "updated", "fields": ["人工智能", "生物医药", "新材料"], "techTypes": ["结构化", "半结构化"]},
                {"key": "theme", "name": "领域主题数据库", "count": 8, "tables": 380, "records": "2.9亿", "description": "按学科领域整合的专题数据", "updateStatus": "updated", "fields": ["基础科学", "工程技术", "能源环境"], "techTypes": ["结构化", "非结构化"]},
                {"key": "intel", "name": "科技情报数据库", "count": 11, "tables": 456, "records": "3.8亿", "description": "科技动态、技术趋势、竞争情报", "updateStatus": "syncing", "fields": ["信息技术", "医学健康", "农业科技"], "techTypes": ["结构化", "实时流"]},
            ],
            "resources": [
                {"id": "bdc-001", "name": "全球专利文献库", "categoryKey": "element", "category": "科技要素数据库", "dataType": "专利", "field": "人工智能", "techType": "结构化", "updateTime": "2026-08-24 06:00", "recordCount": "1.28亿", "quality": 94, "status": "updated"},
                {"id": "bdc-002", "name": "科技论文引用库", "categoryKey": "element", "category": "科技要素数据库", "dataType": "论文", "field": "基础科学", "techType": "结构化", "updateTime": "2026-08-24 02:30", "recordCount": "2.15亿", "quality": 96, "status": "updated"},
                {"id": "bdc-004", "name": "基因序列主题库", "categoryKey": "theme", "category": "领域主题数据库", "dataType": "实验数据", "field": "生物医药", "techType": "非结构化", "updateTime": "2026-08-23 22:00", "recordCount": "9600万", "quality": 93, "status": "updated"},
                {"id": "bdc-007", "name": "AI 竞争情报库", "categoryKey": "intel", "category": "科技情报数据库", "dataType": "情报", "field": "人工智能", "techType": "半结构化", "updateTime": "2026-08-25 08:15", "recordCount": "实时流", "quality": 92, "status": "syncing"},
            ],
            "growthTrend": {"days": ["08-19", "08-20", "08-21", "08-22", "08-23", "08-24", "08-25"], "series": [{"name": "科技要素库", "data": [118, 121, 124, 128, 132, 136, 141]}, {"name": "领域主题库", "data": [96, 98, 101, 103, 107, 110, 114]}, {"name": "科技情报库", "data": [72, 75, 79, 82, 88, 94, 101]}]},
            "updateFeed": [
                {"id": "uf-01", "time": "2026-08-25 08:15", "resource": "AI 竞争情报库", "action": "实时接入", "delta": "+12.6万条", "status": "syncing"},
                {"id": "uf-04", "time": "2026-08-24 06:00", "resource": "全球专利文献库", "action": "增量更新", "delta": "+18万条", "status": "updated"},
            ],
        },
    }


CATALOG = (
    ("overview_source", "CNKI 科技文献题录库", "中国知网", "结构化数据", "国内数据库", "基础科学", "2026-05-20", 94, "高", "文献计量分析", "1280", ["文献", "题录", "中文"]),
    ("overview_source", "Web of Science 引文索引", "Clarivate", "结构化数据", "国外数据库", "基础科学", "2026-05-18", 96, "高", "国际对标研究", "980", ["引文", "SCI"]),
    ("overview_source", "中科院高能所实验数据仓", "中科院高能物理研究所", "半结构化数据", "科研院所", "基础科学", "2026-05-16", 93, "高", "粒子物理前沿", "1560", ["实验", "粒子物理"]),
    ("overview_source", "龙头企业工艺参数开放集", "某装备制造集团", "半结构化数据", "企业", "工程技术", "2026-05-14", 87, "中", "智能制造示范", "720", ["制造", "工艺"]),
    ("overview_source", "HuggingFace 模型权重镜像", "HuggingFace", "非结构化数据", "开源平台", "信息技术", "2026-05-12", 85, "中", "大模型评测", "640", ["开源", "NLP"]),
    ("overview_source", "PubMed 生物医学摘要库", "NCBI", "结构化数据", "国外数据库", "医学健康", "2026-05-10", 95, "高", "精准医疗计划", "1120", ["医学", "摘要"]),
    ("overview_source", "国家科技报告服务系统", "科技部", "非结构化数据", "国内数据库", "信息技术", "2026-05-08", 92, "高", "科技投入监测", "860", ["报告", "政务"]),
    ("overview_source", "Kaggle 竞赛数据集汇聚", "Kaggle", "结构化数据", "开源平台", "信息技术", "2026-05-06", 83, "中", "算法基准评测", "540", ["竞赛", "CSV"]),
    ("overview_source", "某行业研究所监测时序库", "中国气象科学研究院", "实时流数据", "科研院所", "能源环境", "2026-05-04", 91, "高", "气候韧性评估", "1320", ["监测", "时序"]),
    ("overview_source", "专精特新企业专利开放语料", "某新材料企业", "非结构化数据", "企业", "材料科学", "2026-05-02", 81, "中", "知识产权情报", "420", ["专利", "文本"]),
    ("access_source", "高能物理实验数据集", "科研院所", "结构化数据", "科研院所", "基础科学", "2026-05-10", 95, "优", "粒子物理前沿研究", "2300", None),
    ("access_source", "基因变异数据库", "高等院校", "非结构化数据", "高等院校", "医学健康", "2026-05-08", 93, "优", "精准医疗计划", "1800", None),
    ("access_source", "智能制造工艺参数库", "企业", "半结构化数据", "企业", "工程技术", "2026-05-06", 89, "良", "工业4.0示范线", "1500", None),
    ("access_source", "开源气象观测集", "第三方平台", "实时流数据", "第三方平台", "能源环境", "2026-05-05", 91, "优", "气候韧性评估", "920", None),
    ("access_source", "大气环境监测数据", "政府部门", "实时流数据", "政府部门", "能源环境", "2026-05-04", 88, "良", "蓝天保卫战监测", "860", None),
    ("access_source", "作物生长模型数据", "科研院所", "结构化数据", "科研院所", "农业科技", "2026-04-28", 87, "良", "智慧农业示范", "1100", None),
    ("access_source", "企业专利开放语料", "企业", "非结构化数据", "企业", "信息技术", "2026-04-25", 82, "中", "知识产权情报", "640", None),
    ("access_source", "开源蛋白结构库镜像", "第三方平台", "结构化数据", "第三方平台", "基础科学", "2026-04-20", 94, "优", "生物大分子解析", "2100", None),
    ("access_source", "高校论文元数据仓", "高等院校", "半结构化数据", "高等院校", "基础科学", "2026-04-18", 80, "中", "文献计量分析", "720", None),
    ("access_source", "政务科技统计年报", "政府部门", "结构化数据", "政府部门", "信息技术", "2026-04-15", 92, "优", "科技投入监测", "480", None),
    ("access_source", "工业物联网时序库", "企业", "实时流数据", "企业", "工程技术", "2026-04-12", 86, "良", "产线数字孪生", "980", None),
    ("access_source", "开源遥感切片库", "第三方平台", "非结构化数据", "第三方平台", "能源环境", "2026-04-08", 85, "良", "国土空间监测", "1320", None),
    ("access_detail", "高能物理实验数据集", "中科院高能所", "结构化数据", "文件传输", "基础科学", "2026-05-10", 95, "active", "粒子物理前沿研究", "5800万条", ["高能物理", "粒子碰撞"]),
    ("access_detail", "基因变异数据库", "北大医学部", "非结构化数据", "API接口", "医学健康", "2026-05-08", 93, "active", "精准医疗计划", "1200万条", ["基因变异"]),
    ("access_detail", "智能制造工艺参数库", "华为公司", "半结构化数据", "数据库同步", "工程技术", "2026-05-06", 89, "active", "工业4.0示范线", "3500万条", ["智能制造"]),
    ("access_detail", "大气环境监测数据", "环保部监测中心", "实时流数据", "物联网采集", "能源环境", "2026-05-05", 91, "active", "蓝天保卫战监测", "实时流", ["大气监测"]),
    ("access_detail", "作物生长模型数据", "中国农科院", "结构化数据", "文件传输", "农业科技", "2026-04-28", 87, "active", "智慧农业示范", "820万条", ["作物模型"]),
    ("access_detail", "纳米材料表征库", "上海交大", "半结构化数据", "API接口", "材料科学", "2026-04-25", 90, "review", "新材料研发专项", "2100万条", ["纳米材料"]),
    ("access_detail", "网络安全威胁情报", "国家互联网应急中心", "非结构化数据", "API接口", "信息技术", "2026-04-20", 94, "active", "网络安全态势感知", "实时流", ["漏洞情报"]),
    ("access_detail", "海洋科学调查数据", "海洋一所", "结构化数据", "数据库同步", "基础科学", "2026-04-15", 88, "active", "深海探测工程", "9600万条", ["海洋调查"]),
)

SUBJECTS = (
    ("app_subject", "中科院计算技术研究所", None, None, 312000, None, 10.9, None, None),
    ("app_subject", "华为中央研究院", None, None, 268000, None, 9.4, None, None),
    ("app_subject", "精准医疗专项攻关组", None, None, 196000, None, 6.9, None, None),
    ("app_subject", "清华大学交叉信息院", None, None, 178000, None, 6.2, None, None),
    ("asset", "基础研究主题库", "科技管理部", None, 856000, 1234, None, 15.2, "基础科学"),
    ("asset", "医学影像数据集", "医疗健康部", None, 642000, 987, None, 22.5, "医学健康"),
    ("asset", "工程设计规范库", "工程建设部", None, 534000, 756, None, 8.3, "工程技术"),
    ("supplier", "中科院", "科技管理部", "华北", 1250000, None, 43.8, None, None),
    ("supplier", "清华大学", "工程建设部", "华北", 680000, None, 23.8, None, None),
    ("demander", "研发中心A", "科技研发部", None, 256000, None, None, None, None),
    ("demander", "实验室B", "实验研究部", None, 189000, None, None, None, None),
    ("business", "科研项目评估", "科技管理", None, 523000, 45, None, None, None),
    ("business", "人才评价体系", "人力资源", None, 412000, 32, None, None, None),
    ("region", "华北", None, "华北", 2088000, None, None, None, None),
    ("region", "华南", None, "华南", 768000, None, None, None, None),
)

PROBES = (
    ("conn_activity", "连接活跃度", 92.4, "good"),
    ("call_frequency", "调用频率", 88.6, "good"),
    ("fail_rate", "失败率", 0.8, "good"),
    ("total_calls", "调用总量", 2856000, "good"),
    ("avg_response_ms", "平均响应", 245, "good"),
    ("success_rate", "成功率", 99.2, "good"),
    ("alarm_count", "异常告警", 12, "warn"),
    ("alarm_critical", "严重告警", 2, "warn"),
)

KG_CAT = {"数据库": "database", "数据表": "table", "应用系统": "app", "应用": "app", "主题领域": "theme", "主题": "theme"}
KG_COLOR = {"database": "#165dff", "table": "#36cfc9", "app": "#9254de", "theme": "#ff7a45", "org": "#00b42a", "文献计量": "#165dff", "领域主题": "#36cfc9", "科技情报": "#9254de", "科技要素": "#ff7a45"}
KG_NODES = (
    ("n1", "基础研究库", "数据库", 80, "涵盖数学、物理、化学等基础学科研究数据", "2.3亿", 94, "中科院", None, None, ["n2", "n3", "n10"]),
    ("n2", "基因测序", "数据表", 50, "人类基因组测序数据表", "3500万", 93, "北大医学部", None, None, ["n1", "n4"]),
    ("n3", "蛋白质结构", "数据表", 45, "蛋白质三维结构及功能注释", "1200万", 91, "中科院", None, None, ["n1", "n5"]),
    ("n4", "临床试验", "应用系统", 60, "临床试验数据管理系统", None, None, None, "156", "120万次/月", ["n2", "n5"]),
    ("n5", "药物研发", "主题领域", 70, "药物发现到临床试验", None, None, None, None, None, ["n3", "n4"]),
    ("n6", "医学影像库", "数据库", 75, "多模态影像数据", "1.5亿", 96, "北大医学部", None, None, ["n7", "n8"]),
    ("n7", "CT扫描", "数据表", 40, "CT扫描影像及结构化报告", "4500万", 95, "北大医学部", None, None, ["n6", "n9"]),
    ("n8", "MRI数据", "数据表", 42, "核磁共振影像及分析标注", "3200万", 94, "北大医学部", None, None, ["n6", "n9"]),
    ("n9", "诊断系统", "应用系统", 55, "AI辅助影像诊断系统", None, None, None, "234", "85万次/月", ["n7", "n8", "n10"]),
    ("n10", "精准医疗", "主题领域", 65, "基因组学和影像组学个体化诊疗", None, None, None, None, None, ["n1", "n9"]),
)
KG_LINKS = (
    ("n1", "n2", "包含", None),
    ("n1", "n3", "包含", None),
    ("n2", "n4", "支撑", None),
    ("n3", "n5", "支撑", None),
    ("n4", "n5", "服务于", None),
    ("n6", "n7", "包含", None),
    ("n6", "n8", "包含", None),
    ("n7", "n9", "支撑", None),
    ("n8", "n9", "支撑", None),
    ("n9", "n10", "服务于", None),
    ("n1", "n10", "关联", None),
)
DS_NODES = (
    ("ds1", "基础研究库", "文献计量", 80, "涵盖数理化基础学科文献数据"),
    ("ds2", "基因序列库", "领域主题", 70, "人类基因组变异及注释数据"),
    ("ds3", "蛋白质结构库", "领域主题", 65, "PDB蛋白质三维结构数据"),
    ("ds4", "临床病例库", "科技情报", 75, "多中心临床病例信息数据"),
    ("ds5", "药物研发库", "领域主题", 60, "化合物活性及药物靶点数据"),
    ("ds6", "医学影像库", "科技情报", 72, "CT/MRI/X射线影像数据"),
    ("ds7", "工程设计库", "领域主题", 68, "建筑工程设计图纸及规范"),
    ("ds8", "材料性能库", "领域主题", 58, "材料物理化学性能测试数据"),
    ("ds9", "AI训练库", "科技要素", 66, "机器学习训练数据集"),
    ("ds10", "能源统计库", "科技情报", 62, "能源生产消费统计数据"),
    ("ds11", "环境监测库", "科技要素", 64, "大气、水质、土壤环境监测"),
    ("ds12", "农业产量库", "领域主题", 55, "主要农作物产量及气候关联"),
    ("ds13", "专利文献库", "文献计量", 78, "全球专利文献及法律状态"),
    ("ds14", "论文引用库", "文献计量", 73, "科技论文引用关系网络"),
    ("ds15", "人才信息库", "科技要素", 56, "科技人才基本信息及成果"),
)
DS_LINKS = (
    ("ds1", "ds14", "文献引用", 0.9),
    ("ds2", "ds3", "基因-蛋白关联", 0.85),
    ("ds3", "ds5", "靶点发现", 0.8),
    ("ds4", "ds5", "临床试验", 0.75),
    ("ds2", "ds4", "基因-疾病关联", 0.7),
    ("ds6", "ds4", "影像诊断", 0.82),
    ("ds7", "ds8", "材料选型", 0.65),
    ("ds9", "ds6", "AI辅助诊断", 0.78),
    ("ds10", "ds11", "能源-环境影响", 0.88),
    ("ds11", "ds12", "气候-产量关联", 0.72),
    ("ds13", "ds14", "专利引用", 0.86),
    ("ds1", "ds13", "文献-专利交叉", 0.6),
    ("ds15", "ds14", "人才产出", 0.55),
    ("ds9", "ds7", "智能设计", 0.5),
    ("ds5", "ds9", "AI药物发现", 0.68),
    ("ds8", "ds9", "材料-计算", 0.58),
)

# 年份列名以 DR-RES-A0-L01 为准。查询前再用 SHOW FULL COLUMNS 核对，对不上则整批 snap 失败。
ENTITY_SPECS = (
    ("paper.publication_year", "ads_paper_profile", "publication_year"),
    ("patent.application_year", "ads_patent_profile", "application_year"),
    ("patent.publication_year", "ads_patent_profile", "publication_year"),
    ("project.start_year", "ads_project_profile", "start_year"),
)
CATALOG_TABLES = ("ads_paper_profile", "ads_patent_profile", "ads_project_profile")


def redact(text: str, secrets: list[str]) -> str:
    out = text
    for secret in secrets:
        if secret:
            out = out.replace(secret, "***")
    return out[:800]


def mysql_auth() -> tuple[str, str]:
    text = YML.read_text(encoding="utf-8")
    user = re.search(r"(?m)^\s*username:\s*(\S+)\s*$", text)
    password = re.search(r"(?m)^\s*password:\s*(\S+)\s*$", text)
    if not user or not password or user.group(1) != "gkxlumenx":
        raise SystemExit("application-local.yml 里没有用户名 gkxlumenx")
    return user.group(1), password.group(1)


def doris_password() -> str:
    env = os.environ.get("JX_ADS_PASSWORD", "").strip()
    if env:
        return env
    file_path = os.environ.get("JX_ADS_PASSWORD_FILE", "").strip()
    if file_path and Path(file_path).is_file():
        return Path(file_path).read_text(encoding="utf-8").strip()
    home = Path.home() / ".gkx" / "jx_ads_password"
    if home.is_file():
        return home.read_text(encoding="utf-8").strip()
    if DORIS_README.is_file():
        raw = DORIS_README.read_text(encoding="utf-8")
        hit = re.search(r"\|\s*密码\s*\|\s*`([^`]+)`", raw)
        if hit:
            return hit.group(1).strip()
    return ""


def expect_shape() -> None:
    tasks = [(m, s) for m, s, n in TASK_PLAN for _ in range(n)]
    assert len(STRUCTURE) == 4
    assert len(THEMES_SLICE) == 7
    assert YEAR_PREV > 0 and YEAR_TOTAL == YEAR_PREV + ADDED_LAST
    assert len(CATALOG) == 30
    assert len(tasks) == 20
    assert sum(1 for _, status in tasks if status == "pending") == 4
    assert len(ISSUE_NAMES) == 30
    assert len(THEMES) == 8
    assert all(item["tables"] for item in THEMES)
    assert len(SUBJECTS) == 15
    assert len(PROBES) >= 3
    assert KG_NODES and KG_LINKS and DS_NODES and DS_LINKS
    assert set(blocks()) == {"overview_classify", "semantic_theme", "partition", "big_data_center"}
    assert MOCK_BATCH.startswith("mock_") and SNAP_BATCH.startswith("snap_")
    assert WRITE_DB == "demo_gkxlumenx_ads"


def ins(cur, table: str, cols: tuple[str, ...], rows: list[tuple]) -> None:
    if table not in TABLES:
        raise RuntimeError(table)
    if not rows:
        return
    sql = "INSERT INTO `{}` ({}) VALUES ({})".format(table, ",".join(cols), ",".join(["%s"] * len(cols)))
    cur.executemany(sql, rows)


def delete_batch(cur, batch: str, tables=TABLES) -> None:
    for table in tables:
        cur.execute("DELETE FROM `{}` WHERE calc_batch_id=%s".format(table), (batch,))


def load_mock(cur, now: datetime) -> None:
    b, f = MOCK_BATCH, FILL
    delete_batch(cur, b)
    ins(
        cur,
        "gapfill_dr_type_slice",
        ("calc_batch_id", "generated_at", "fill_method", "slice_kind", "name", "value", "color", "avg_quality", "heat", "lifecycle"),
        [(b, now, f, "structure", name, value, color, None, heat, life) for name, value, color, heat, life in STRUCTURE]
        + [(b, now, f, "theme", name, value, None, quality, None, None) for name, value, quality in THEMES_SLICE],
    )
    channel_rows = []
    for code, name, trend, volume, count, share, change, reliability, quality, color, tags, hint in SRS:
        for idx, month in enumerate(MONTHS_6):
            last = idx == len(MONTHS_6) - 1
            channel_rows.append(
                (b, now, f, "srs_source", code, name, month, volume if last else trend[idx], count if last else None, share if last else None, change if last else None, "rise" if last else None, reliability if last else None, quality if last else None, color if last else None, None, None, j(list(tags)) if last else None, hint if last else None)
            )
    for code, name, count, activity, status in ORGS:
        for idx, month in enumerate(MONTHS_6):
            last = idx == len(MONTHS_6) - 1
            back = (len(MONTHS_6) - 1 - idx) * 40
            channel_rows.append((b, now, f, "org_activity", code, name, month, count if last else max(1, count - back), None, None, None, None, None, None, None, activity if last else max(1, activity - (len(MONTHS_6) - 1 - idx) * 2), status, None, None))
    ins(
        cur,
        "gapfill_dr_source_channel",
        ("calc_batch_id", "generated_at", "fill_method", "channel_group", "channel_code", "channel_name", "stat_month", "volume", "item_count", "share_pct", "change_pct", "trend", "reliability", "avg_quality", "color", "activity", "status", "sample_tags", "reliability_hint"),
        channel_rows,
    )
    ins(
        cur,
        "gapfill_dr_catalog_item",
        ("calc_batch_id", "generated_at", "fill_method", "list_code", "name", "source_name", "item_type", "channel_name", "domain_name", "collect_time", "quality_score", "reliability", "related_project", "volume_label", "tags"),
        [(b, now, f, *row[:11], j(row[11]) if row[11] else None) for row in CATALOG],
    )
    tasks = [(m, s) for m, s, n in TASK_PLAN for _ in range(n)]
    ins(cur, "gapfill_dr_ingest_task", ("calc_batch_id", "generated_at", "fill_method", "ingest_method", "status"), [(b, now, f, method, status) for method, status in tasks])

    facts = [
        (b, now, f, "year", "2025", "volume", None, None, None, None, YEAR_PREV, None, None, None, None, None),
        (b, now, f, "year", "2026", "volume", None, None, None, None, YEAR_TOTAL, None, None, None, None, None),
        (b, now, f, "year", "2025", "added", None, None, None, None, 4860, None, None, None, None, None),
        (b, now, f, "year", "2026", "added", None, None, None, None, ADDED_LAST, None, None, None, None, None),
    ]
    for year, scale in (("2025", 0.8), ("2026", 1)):
        for idx, (added, updated) in enumerate(zip(ADDED_M, UPDATED_M), start=1):
            label = f"{year}-{idx:02d}"
            facts.append((b, now, f, "month", label, "added", None, None, None, None, int(added * scale), None, None, None, None, None))
            facts.append((b, now, f, "month", label, "updated", None, None, None, None, int(updated * scale), None, None, None, None, None))
    for idx, (added, updated) in enumerate(zip(WEEK_A, WEEK_U), start=1):
        label = f"2026-W{idx:02d}"
        facts.append((b, now, f, "week", label, "added", None, None, None, None, added, None, None, None, None, None))
        facts.append((b, now, f, "week", label, "updated", None, None, None, None, updated, None, None, None, None, None))
    for label, added, updated in zip(DAY_LABELS, DAY_A, DAY_U):
        facts.append((b, now, f, "day", label, "added", None, None, None, None, added, None, None, None, None, None))
        facts.append((b, now, f, "day", label, "updated", None, None, None, None, updated, None, None, None, None, None))
    for name, series in CHANNEL_M.items():
        for month, volume in zip(MONTHS_6, series):
            facts.append((b, now, f, "month", month, "volume", None, name, None, None, volume, None, None, None, None, None))
    history = (
        ("2026-05-22", "API接口", "sci_papers", 12500, "2.3GB", "每日", "success", None, None),
        ("2026-05-21", "文件传输", "engineering_designs", 8900, "5.6GB", "每周", "success", None, None),
        ("2026-05-20", "数据库同步", "medical_images", 34500, "12.8GB", "每日", "partial", "同步延迟", "3个分表同步延迟4小时"),
        ("2026-05-19", "人工录入", "patent_records", 1200, "156MB", "每月", "success", None, None),
        ("2026-05-18", "物联网采集", "sensor_climate", 87600, "1.2GB", "实时", "success", None, None),
        ("2026-05-17", "API接口", "gene_sequences", 5600, "3.4GB", "每日", "failed", "接口错误", "源接口返回503，已重试3次"),
        ("2026-05-15", "文件传输", "agri_yield_data", 45600, "890MB", "每两周", "success", None, None),
        ("2026-05-14", "数据库同步", "material_properties", 18900, "4.2GB", "每周", "success", None, None),
        ("2026-05-13", "API接口", "env_monitor_data", 67800, "2.1GB", "实时", "partial", "数据缺失", "部分传感器数据缺失"),
        ("2026-05-12", "文件传输", "ai_training_set", 2300, "15.7GB", "每月", "success", None, None),
        ("2026-05-10", "数据库同步", "clinical_trials", 9800, "3.1GB", "每日", "failed", "格式异常", "目标表字段类型不匹配"),
        ("2026-05-08", "物联网采集", "factory_iot_stream", 125000, "2.8GB", "实时", "partial", "同步延迟", "边缘网关断连"),
    )
    for period, channel, table, rows, size, cycle, status, anomaly, note in history:
        facts.append((b, now, f, "day", period, "volume", channel, channel, table, None, rows, size, cycle, status, anomaly, note))
    for biz, rows in (("基础研究", 5200), ("产业应用", 4200), ("开源汇聚", 2800), ("政务统计", 600)):
        facts.append((b, now, f, "year", "2026", "volume", None, None, None, biz, rows, None, None, None, None, None))
    ins(
        cur,
        "gapfill_dr_collection_fact",
        ("calc_batch_id", "generated_at", "fill_method", "grain", "period_label", "metric", "ingest_method", "channel_name", "table_name", "biz_type", "row_count", "size_label", "update_cycle", "status", "anomaly_type", "anomaly_note"),
        facts,
    )

    theme_ids = {}
    for item in THEMES:
        cur.execute(
            "INSERT INTO gapfill_dr_theme_library (calc_batch_id, generated_at, fill_method, name, category, resource_type, tags, table_count, record_yi, storage_tb, quality, source_name, region, update_freq, related_project, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (b, now, f, item["name"], item["category"], item["resource_type"], j(item["tags"]), item["table_count"], item["record_yi"], item["storage_tb"], item["quality"], item["source_name"], item["region"], item["update_freq"], item["related_project"], item["description"]),
        )
        theme_ids[item["name"]] = cur.lastrowid
    col_rows = []
    for item in THEMES:
        for table_name, table_comment, fields in item["tables"]:
            for field_name, field_type, meaning, required in fields:
                col_rows.append((b, now, f, theme_ids[item["name"]], table_name, table_comment, field_name, field_type, meaning, required))
    ins(cur, "gapfill_dr_theme_column", ("calc_batch_id", "generated_at", "fill_method", "theme_id", "table_name", "table_comment", "field_name", "field_type", "meaning", "required_flag"), col_rows)

    issue_rows = []
    for i, name in enumerate(ISSUE_NAMES):
        kind, color = ISSUE_TYPES[i % len(ISSUE_TYPES)]
        issue_rows.append((b, now, f, name, f"t_{i+1:02d}", kind, ISSUE_CATS[i % len(ISSUE_CATS)], ISSUE_CLUSTERS[i % len(ISSUE_CLUSTERS)], ISSUE_LEVELS[i % len(ISSUE_LEVELS)], ISSUE_STATUS[i % len(ISSUE_STATUS)], f"2026-05-{(i % 22) + 1:02d} 09:00", INGEST[i % len(INGEST)], f"{name}需核对后重新入库", "对照源端复核后重跑该批次", color))
    ins(
        cur,
        "gapfill_dr_quality_issue",
        ("calc_batch_id", "generated_at", "fill_method", "name", "table_name", "issue_type", "category", "data_cluster", "level", "status", "found_at", "ingest_method", "detail", "suggestion", "color"),
        issue_rows,
    )
    ins(
        cur,
        "gapfill_dr_usage_subject",
        ("calc_batch_id", "generated_at", "fill_method", "subject_type", "name", "department", "region_name", "call_count", "user_count", "share_pct", "growth_pct", "theme_name"),
        [(b, now, f, *row) for row in SUBJECTS],
    )
    series = []
    call_users = (3100, 3200, 3280, 3350, 3420, 3456)
    call_vals = (1860000, 2010000, 2140000, 2380000, 2650000, 2856000)
    for i, (label, calls, users) in enumerate(zip(MONTHS_6, call_vals, call_users), start=1):
        series.append((b, now, f, "usage_call", "调用", label, i, calls, users, None))
    detail_vals = (1180000, 1240000, 1310000, 1380000, 1450000, 1520000, 1580000, 1650000, 1720000, 1780000, 1850000, 1920000)
    for i, (label, calls) in enumerate(zip(MONTHS_12, detail_vals), start=1):
        series.append((b, now, f, "usage_detail", "使用详情", label, i, calls, None, None))
    theme_series = {
        "基础科学": (72000, 75000, 78000, 82000, 85000, 83000, 80000, 84000, 87000, 89000, 91000, 94000),
        "医学健康": (58000, 60000, 62000, 65000, 68000, 66000, 64000, 67000, 70000, 72000, 74000, 76000),
        "工程技术": (45000, 47000, 49000, 52000, 54000, 53000, 51000, 55000, 57000, 59000, 61000, 63000),
        "农业科技": (32000, 34000, 36000, 38000, 40000, 39000, 37000, 41000, 43000, 45000, 47000, 49000),
        "能源环境": (28000, 30000, 31000, 33000, 35000, 34000, 32000, 36000, 38000, 40000, 42000, 44000),
    }
    for sname, values in theme_series.items():
        for i, (label, calls) in enumerate(zip(MONTHS_12, values), start=1):
            series.append((b, now, f, "theme_call", sname, label, i, calls, None, None))
    for code, packs in (
        ("supplier_call", (("中科院", (180000, 192000, 205000, 218000, 235000, 250000)), ("清华大学", (98000, 105000, 112000, 120000, 130000, 145000)))),
        ("demander_call", (("研发中心A", (35000, 38000, 42000, 46000, 49000, 52000)), ("实验室B", (28000, 30000, 32000, 35000, 37000, 40000)))),
        ("business_call", (("科研项目评估", (72000, 78000, 83000, 89000, 95000, 102000)), ("人才评价体系", (58000, 62000, 66000, 70000, 75000, 80000)))),
    ):
        for sname, values in packs:
            for i, (label, calls) in enumerate(zip(MONTHS_6, values), start=1):
                series.append((b, now, f, code, sname, label, i, calls, None, None))
    for i, (label, calls) in enumerate(zip(MONTHS_6, call_vals), start=1):
        series.append((b, now, f, "cumulative", "累计调用", label, i, calls, None, calls))
    ins(cur, "gapfill_dr_usage_series", ("calc_batch_id", "generated_at", "fill_method", "series_code", "series_name", "period_label", "sort_no", "call_count", "user_count", "cumulative_count"), series)

    events = []
    app_logs = (
        ("张明华", "科技管理", "科研项目评估", "基础科学", "GET /api/theme/basic", "2026-05-22 15:30:12", 12, "成功"),
        ("李建国", "人力资源", "人才评价体系", "信息技术", "GET /api/theme/basic", "2026-05-22 15:15:08", 8, "成功"),
        ("陈伟强", "产业促进", "成果转换分析", "工程技术", "GET /api/theme/engineering", "2026-05-22 14:50:33", 15, "成功"),
        ("赵雪梅", "政策研究", "政策效果评估", "能源环境", "GET /api/theme/energy", "2026-05-22 14:40:21", 6, "成功"),
        ("孙志远", "战略规划", "创新环境监测", "农业科技", "GET /api/theme/agriculture", "2026-05-22 14:30:05", 9, "成功"),
        ("周晓燕", "法务部", "知识产权管理", "材料科学", "GET /api/theme/basic", "2026-05-22 14:20:44", 4, "成功"),
        ("吴国栋", "科技管理", "科研项目评估", "基础科学", "GET /api/theme/basic", "2026-05-22 13:55:17", 3, "超时重试"),
        ("李建国", "人力资源", "人才评价体系", "医学健康", "GET /api/theme/medical", "2026-05-22 13:40:02", 11, "成功"),
        ("陈伟强", "产业促进", "成果转换分析", "工程技术", "GET /api/theme/engineering", "2026-05-21 18:12:40", 7, "成功"),
        ("周晓燕", "法务部", "知识产权管理", "材料科学", "GET /api/theme/basic", "2026-05-20 09:48:55", 1, "失败"),
    )
    for row in app_logs:
        events.append((b, now, f, "app_log", row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], None))
    for supplier, product, period, calls in (
        ("中科院", "基础研究主题库", "2026-05", 92000),
        ("中科院", "基础研究主题库", "2026-04", 88000),
        ("中科院", "材料性能库", "2026-05", 42000),
        ("清华大学", "工程设计规范库", "2026-05", 68000),
        ("清华大学", "工程设计规范库", "2026-04", 64000),
        ("清华大学", "农业科技数据库", "2026-05", 28000),
        ("中科院", "基础研究主题库", "2026-03", 85000),
        ("清华大学", "工程设计规范库", "2026-03", 61000),
        ("中科院", "材料性能库", "2026-04", 39000),
        ("清华大学", "农业科技数据库", "2026-04", 26000),
    ):
        events.append((b, now, f, "supplier_detail", supplier, None, None, product, None, period, calls, None, None))
    for field, app, dept, calls, when in (
        ("paper_id", "科研项目评估", "科技管理部", 125600, "2026-05-22 14:30"),
        ("publish_date", "科研项目评估", "科技管理部", 98200, "2026-05-21 13:15"),
        ("talent_name", "人才评价体系", "人力资源部", 156300, "2026-05-22 15:00"),
        ("research_field", "人才评价体系", "人力资源部", 134200, "2026-05-20 14:45"),
        ("patent_no", "成果转换分析", "法务部", 89600, "2026-05-19 12:30"),
        ("filing_date", "成果转换分析", "法务部", 78400, "2026-05-18 11:20"),
        ("policy_content", "政策效果评估", "政策研究部", 67800, "2026-05-17 10:45"),
        ("pm25_value", "创新环境监测", "环保部", 567800, "2026-05-22 15:20"),
        ("station_code", "创新环境监测", "环保部", 489600, "2026-05-16 15:15"),
        ("gene_symbol", "科学研究平台", "医疗健康部", 234500, "2026-05-15 14:10"),
        ("citation_count", "科研项目评估", "科技管理部", 71200, "2026-05-14 09:40"),
        ("inventor", "知识产权管理", "法务部", 54300, "2026-05-13 16:05"),
    ):
        events.append((b, now, f, "column_usage", None, dept, app, None, None, when, calls, None, field))
    for user, dept, app, theme, when, calls in (
        ("张明华", "科技管理部", "科研项目评估", "基础科学", "2026-05-22 15:30", 1256),
        ("李建国", "人力资源部", "人才评价体系", "信息技术", "2026-05-22 15:15", 983),
        ("王丽芳", "医疗健康部", "医学研究平台", "医学健康", "2026-05-22 15:05", 1523),
        ("陈伟强", "产业促进部", "成果转换分析", "工程技术", "2026-05-22 14:50", 867),
        ("赵雪梅", "政策研究部", "政策效果评估", "能源环境", "2026-05-22 14:40", 645),
        ("孙志远", "战略规划部", "创新环境监测", "农业科技", "2026-05-22 14:30", 534),
        ("周晓燕", "法务部", "知识产权管理", "材料科学", "2026-05-22 14:20", 432),
        ("吴国栋", "数字创新部", "AI开发平台", "信息技术", "2026-05-22 14:10", 1890),
    ):
        events.append((b, now, f, "user_track", user, dept, app, theme, None, when, calls, None, None))
    assert len(events) == 40
    ins(cur, "gapfill_dr_call_event", ("calc_batch_id", "generated_at", "fill_method", "event_kind", "subject_name", "department", "app_name", "theme_name", "api_name", "event_time", "call_count", "result_text", "field_name"), events)
    ins(cur, "gapfill_dr_api_probe", ("calc_batch_id", "generated_at", "fill_method", "metric_code", "label", "value_num", "status", "probed_at"), [(b, now, f, code, label, value, status, now) for code, label, value, status in PROBES])

    node_rows = []
    for node_id, name, category, size, desc, records, quality, source, users, calls, related in KG_NODES:
        key = KG_CAT[category]
        node_rows.append((b, now, f, "overview_kg", node_id, name, category, key, KG_COLOR[key], size, desc, records, quality, source, users, calls, j(related)))
    for node_id, name, category, size, desc in DS_NODES:
        node_rows.append((b, now, f, "theme_relation", node_id, name, category, category, KG_COLOR[category], size, desc, None, None, None, None, None, None))
    ins(cur, "gapfill_dr_graph_node", ("calc_batch_id", "generated_at", "fill_method", "graph_code", "node_id", "name", "category", "category_key", "color", "size", "desc_text", "record_label", "quality", "source_name", "user_label", "call_label", "related_nodes"), node_rows)
    link_rows = [(b, now, f, "overview_kg", src, dst, relation, strength) for src, dst, relation, strength in KG_LINKS]
    link_rows += [(b, now, f, "theme_relation", src, dst, relation, strength) for src, dst, relation, strength in DS_LINKS]
    ins(cur, "gapfill_dr_resource_link", ("calc_batch_id", "generated_at", "fill_method", "graph_code", "src_id", "dst_id", "relation", "strength"), link_rows)
    ins(cur, "gapfill_dr_block_json", ("calc_batch_id", "generated_at", "fill_method", "block_code", "payload_json"), [(b, now, f, code, j(payload)) for code, payload in blocks().items()])


def assert_mock(cur) -> dict:
    b = MOCK_BATCH
    cur.execute("SELECT COALESCE(SUM(value),0) FROM gapfill_dr_type_slice WHERE calc_batch_id=%s AND slice_kind='structure'", (b,))
    structure_sum = int(cur.fetchone()[0])
    cur.execute(
        "SELECT row_count FROM gapfill_dr_collection_fact WHERE calc_batch_id=%s AND grain='year' AND metric='volume' AND channel_name IS NULL AND table_name IS NULL AND biz_type IS NULL ORDER BY period_label DESC LIMIT 1",
        (b,),
    )
    year_total = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_theme_library WHERE calc_batch_id=%s", (b,))
    theme_n = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_quality_issue WHERE calc_batch_id=%s", (b,))
    issue_n = int(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_ingest_task WHERE calc_batch_id=%s AND status='pending'", (b,))
    pending_n = int(cur.fetchone()[0])
    if structure_sum != year_total:
        raise SystemExit(f"structure sum {structure_sum} != year total {year_total}")
    if theme_n != len(THEMES) or issue_n != len(ISSUE_NAMES) or pending_n != 4:
        raise SystemExit(f"kpi counts theme={theme_n} issue={issue_n} pending={pending_n}")
    cur.execute(
        "SELECT t.id FROM gapfill_dr_theme_library t LEFT JOIN gapfill_dr_theme_column c ON c.theme_id=t.id AND c.calc_batch_id=t.calc_batch_id WHERE t.calc_batch_id=%s GROUP BY t.id HAVING COUNT(c.id)=0",
        (b,),
    )
    if cur.fetchall():
        raise SystemExit("theme missing columns")
    cur.execute("SELECT block_code, COUNT(*) FROM gapfill_dr_block_json WHERE calc_batch_id=%s GROUP BY block_code", (b,))
    got = {row[0]: int(row[1]) for row in cur.fetchall()}
    if got != {"overview_classify": 1, "semantic_theme": 1, "partition": 1, "big_data_center": 1}:
        raise SystemExit(f"block_code {got}")
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_type_slice WHERE calc_batch_id=%s AND slice_kind='theme'", (b,))
    if int(cur.fetchone()[0]) != 7:
        raise SystemExit("theme slices")
    cur.execute("SELECT channel_group, COUNT(DISTINCT stat_month), COUNT(DISTINCT channel_name) FROM gapfill_dr_source_channel WHERE calc_batch_id=%s GROUP BY channel_group", (b,))
    groups = {row[0]: (int(row[1]), int(row[2])) for row in cur.fetchall()}
    if groups.get("srs_source", (0, 0))[0] < 3 or groups.get("srs_source", (0, 0))[1] != 5:
        raise SystemExit(f"srs {groups}")
    if groups.get("org_activity", (0, 0))[0] < 3 or groups.get("org_activity", (0, 0))[1] != 5:
        raise SystemExit(f"org {groups}")
    for table, expect in (
        ("gapfill_dr_catalog_item", 30),
        ("gapfill_dr_ingest_task", 20),
        ("gapfill_dr_usage_subject", 15),
        ("gapfill_dr_call_event", 40),
    ):
        cur.execute(f"SELECT COUNT(*) FROM `{table}` WHERE calc_batch_id=%s", (b,))
        if int(cur.fetchone()[0]) != expect:
            raise SystemExit(table)
    cur.execute("SELECT graph_code, COUNT(*) FROM gapfill_dr_graph_node WHERE calc_batch_id=%s GROUP BY graph_code", (b,))
    nodes = {row[0]: int(row[1]) for row in cur.fetchall()}
    cur.execute("SELECT graph_code, COUNT(*) FROM gapfill_dr_resource_link WHERE calc_batch_id=%s GROUP BY graph_code", (b,))
    links = {row[0]: int(row[1]) for row in cur.fetchall()}
    if nodes.get("overview_kg", 0) < 1 or nodes.get("theme_relation", 0) < 1 or links.get("overview_kg", 0) < 1 or links.get("theme_relation", 0) < 1:
        raise SystemExit("graphs")
    cur.execute("SELECT COUNT(DISTINCT LEFT(period_label,4)) FROM gapfill_dr_collection_fact WHERE calc_batch_id=%s AND grain='year'", (b,))
    if int(cur.fetchone()[0]) < 2:
        raise SystemExit("collection years")
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_usage_series WHERE calc_batch_id=%s AND series_code='usage_call'", (b,))
    if int(cur.fetchone()[0]) < 1:
        raise SystemExit("usage series")
    cur.execute("SELECT COUNT(*) FROM gapfill_dr_api_probe WHERE calc_batch_id=%s", (b,))
    if int(cur.fetchone()[0]) < 1:
        raise SystemExit("probes")
    for table in TABLES:
        cur.execute(f"SELECT COUNT(*) FROM `{table}` WHERE calc_batch_id=%s AND fill_method<>%s", (b, FILL))
        if int(cur.fetchone()[0]):
            raise SystemExit(f"fill_method {table}")
    return {
        "structure_sum": structure_sum,
        "year_total": year_total,
        "theme_count": theme_n,
        "issue_count": issue_n,
        "pending_count": pending_n,
        "equal_structure_and_year": structure_sum == year_total,
    }


def doris_read(cur, sql: str, args=None):
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "SHOW"):
        raise RuntimeError("doris write blocked")
    cur.execute(sql, args)


def fetch_doris(password: str) -> tuple[list[tuple], list[tuple]]:
    conn = pymysql.connect(
        host=os.environ.get("JX_ADS_HOST", "47.93.119.170"),
        port=int(os.environ.get("JX_ADS_PORT", "29030")),
        user=os.environ.get("JX_ADS_USER", "test2"),
        password=password,
        database=os.environ.get("JX_ADS_DATABASE", "gkx_technology_analysis_dev"),
        connect_timeout=20,
        read_timeout=180,
        charset="utf8mb4",
    )
    try:
        cur = conn.cursor()
        doris_read(cur, "SELECT DATABASE()")
        db = cur.fetchone()[0]
        if db != "gkx_technology_analysis_dev":
            raise RuntimeError("doris database mismatch")
        columns = {}
        for table in CATALOG_TABLES:
            if not re.fullmatch(r"[A-Za-z0-9_]+", table):
                raise RuntimeError("bad table")
            doris_read(cur, f"SHOW FULL COLUMNS FROM `{table}`")
            desc = [item[0] for item in cur.description]
            columns[table] = [dict(zip(desc, row)) for row in cur.fetchall()]
            if not columns[table]:
                raise RuntimeError(f"no columns {table}")
        entity = []
        for entity_type, table, year_col in ENTITY_SPECS:
            names = {str(col.get("Field")) for col in columns[table]}
            if year_col not in names or not re.fullmatch(r"[A-Za-z0-9_]+", year_col):
                raise RuntimeError(f"year column missing {table}.{year_col}")
            doris_read(cur, f"SELECT `{year_col}` AS y, COUNT(*) AS c FROM `{table}` GROUP BY `{year_col}`")
            for year, count in cur.fetchall():
                if year is None:
                    continue
                entity.append((entity_type, int(year), int(count)))
        catalog = []
        for table, cols in columns.items():
            for ordinal, col in enumerate(cols, start=1):
                catalog.append((table, str(col.get("Field")), ordinal, None if col.get("Type") is None else str(col.get("Type"))[:64], None if col.get("Comment") is None else str(col.get("Comment"))[:512]))
        if not catalog:
            raise RuntimeError("empty column catalog")
        return entity, catalog
    finally:
        conn.close()


def clear_snap(conn) -> None:
    cur = conn.cursor()
    try:
        delete_batch(cur, SNAP_BATCH, ("gapfill_dr_entity_year", "gapfill_dr_column_catalog"))
        conn.commit()
    finally:
        cur.close()


def write_snap(conn, now: datetime, entity: list[tuple], catalog: list[tuple]) -> None:
    cur = conn.cursor()
    try:
        delete_batch(cur, SNAP_BATCH, ("gapfill_dr_entity_year", "gapfill_dr_column_catalog"))
        ins(cur, "gapfill_dr_entity_year", ("calc_batch_id", "generated_at", "fill_method", "entity_type", "stat_year", "row_count"), [(SNAP_BATCH, now, FILL, *row) for row in entity])
        ins(cur, "gapfill_dr_column_catalog", ("calc_batch_id", "generated_at", "fill_method", "table_name", "column_name", "ordinal", "data_type", "column_comment"), [(SNAP_BATCH, now, FILL, *row) for row in catalog])
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()


def counts(cur) -> dict:
    out = {}
    for table in TABLES:
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        out[table] = int(cur.fetchone()[0])
    return out


def main() -> int:
    expect_shape()
    user, password = mysql_auth()
    secrets = [password]
    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=user, password=password, database=WRITE_DB, charset="utf8mb4", autocommit=False, connect_timeout=20)
    now = datetime.now().replace(microsecond=0)
    result = {"mock_batch": MOCK_BATCH, "snap_batch": SNAP_BATCH, "fill_method": FILL}
    try:
        cur = conn.cursor()
        cur.execute("SELECT DATABASE()")
        db = cur.fetchone()[0]
        if db != WRITE_DB:
            raise SystemExit("refusing database")
        load_mock(cur, now)
        result["equality"] = assert_mock(cur)
        conn.commit()
        cur.close()
        dpassword = doris_password()
        if dpassword:
            secrets.append(dpassword)
        if not dpassword:
            clear_snap(conn)
            result["snap"] = {"written": False, "reason": "未找到久新只读口令，快照表保持空"}
        else:
            try:
                entity, catalog = fetch_doris(dpassword)
                write_snap(conn, now, entity, catalog)
                result["snap"] = {"written": True, "entity_rows": len(entity), "column_rows": len(catalog), "reason": ""}
            except Exception as exc:
                clear_snap(conn)
                result["snap"] = {"written": False, "reason": redact(str(exc), secrets)}
        cur = conn.cursor()
        result["counts"] = counts(cur)
        cur.close()
    except Exception as exc:
        conn.rollback()
        print(redact(str(exc), secrets), file=sys.stderr)
        return 1
    finally:
        conn.close()
    print(j(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
