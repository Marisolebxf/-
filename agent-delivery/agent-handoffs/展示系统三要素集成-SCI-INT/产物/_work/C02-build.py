# -*- coding: utf-8 -*-
"""SCI-INT-C02 技术链三方源入站盘点：卡片数据 → 产物/SCI-INT-C02.yaml（总派单 §2 schema + data_source 扩展块）。
只读：不连库；行数引用仓内快照。运行：python 产物/_work/C02-build.py
"""
import pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "SCI-INT-C02.yaml"

R1010 = "data/third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20261010-1055-估数.MD（TABLE_ROWS 估数，未过滤 is_deleted）"
R0911S = "data/third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20260911-1550-结构.MD（live 列名）"
INV = "data/third-party-source/gkx-mysql-raw/加工/table_inventory.md（2026-07-15 结构盘点，无行数）"
FREQ_UNK = "unknown（供应方未书面给出；两次快照行数有增减，说明在持续加工）"

# ---- 指标 → 页面（MCP srs_refs + metrics/request 各 yaml 命中；DS-0x-* = id-assign/open-loop 只到页级） ----
PAGES = {
    "M_TECH_BASE_96_1": ["DS-01-FACTORS", "DS-02-ENTITY", "DS-07-SCI-CREATE", "DS-07-TECH-INNOV", "TOPIC-TECH-05"],
    "M_TECH_COMPOSITE_SCORE": ["DS-03-RESULT", "DS-07-*"],
    "M_TECH_CONVERT_BOTTLENECK": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_130_1": ["DS-02-TECHGRAPH", "TOPIC-TECH-05"],
    "M_TECH_DEEP_131_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_132_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_133_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_134_1": ["DS-03-RESULT", "DS-07-SCI-CREATE", "DS-09-COMPREHENSIVE", "TOPIC-TECH-05"],
    "M_TECH_DEEP_135_1": ["DS-07-TECH-INNOV", "TOPIC-TECH-05"],
    "M_TECH_DEEP_136_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_137_1": ["DS-03-RESULT", "DS-07-INDUSTRY-POTENTIAL", "TOPIC-TECH-05"],
    "M_TECH_DEEP_138_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_139_1": ["TOPIC-TECH-05"],
    "M_TECH_DEEP_140_1": ["TOPIC-TECH-05"],
    "M_TECH_DS_07_TECH_INNOV_002": ["DS-07-TECH-INNOV"],
    "M_TECH_DS_07_TECH_INNOV_004": ["DS-07-TECH-INNOV"],
    "M_TECH_DS_07_TECH_INNOV_006": ["DS-07-TECH-INNOV"],
    "M_TECH_EDGE_STRENGTH": ["DS-02-*"],
    "M_TECH_ENTITY_INFLUENCE": ["DS-02-*"],
    "M_TECH_ENTITY_REL": ["DS-02-*"],
    "M_TECH_ENTITY_TOP5": ["DS-02-*"],
    "M_TECH_GRAPH_104_1": ["TOPIC-TECH-05"],
    "M_TECH_GRAPH_105_1": ["DS-02-ENTITY", "DS-02-MAINTAIN-ENTITY", "DS-02-TECHGRAPH", "DS-03-RESULT"],
    "M_TECH_GRAPH_STRUCT": ["DS-02-*"],
    "M_TECH_HEAT_INDEX": ["DS-07-*", "DS-09-*", "TOPIC-TECH-05"],
    "M_TECH_HEAT_QUERY": ["DS-09-*", "TOPIC-QUERY"],
    "M_TECH_INVEST_AMOUNT": ["DS-03-RESULT"],
    "M_TECH_LIFE_STAGE": ["DS-03-RESULT", "DS-07-*"],
    "M_TECH_MATURITY_LEVEL": ["DS-03-RESULT", "DS-07-*"],
    "M_TECH_OUTPUT_SCALE": ["DS-03-RESULT"],
    "M_TECH_PAPER_PATENT_CNT": ["DS-02-*", "DS-07-*", "TOPIC-TECH-05"],
    "M_TECH_PATH_CENTRALITY": ["DS-02-*", "DS-07-*"],
    "M_TECH_PATH_KEYNODE": ["DS-02-*"],
    "M_TECH_PATH_PRIORITY": ["DS-02-*"],
    "M_TECH_POTENTIAL_SCORE": ["DS-07-*", "DS-09-*", "TOPIC-TECH-05"],
    "M_TECH_REL_STRENGTH": ["DS-03-RESULT"],
    "M_TECH_STAGE_JUDGE": ["DS-07-*", "TOPIC-TECH-05"],
    "M_TECH_SZ_ASSESS": ["DS-07-*", "TOPIC-TECH-05"],
    "M_TECH_TOPIC_HEAT": ["DS-03-RESULT", "DS-09-*"],
}
STAT = {"M_TECH_HEAT_QUERY", "M_TECH_INVEST_AMOUNT", "M_TECH_OUTPUT_SCALE", "M_TECH_PAPER_PATENT_CNT"}
MODEL = {"M_TECH_DS_07_TECH_INNOV_002", "M_TECH_DS_07_TECH_INNOV_004", "M_TECH_DS_07_TECH_INNOV_006"}


def atype(mid):
    return "STAT" if mid in STAT else "MODEL" if mid in MODEL else "third_party"


# ---- 指标覆盖：metric → (源卡 int_id 列表, binding, 说明) ----
# binding: kit_declared=MCP kit.source_tables 点名；candidate=本叶据口径推断的候选原料（kit 仍 pending_ods，未核验）；
#          jiuxin_pending=久新交付（51 行之一，全部待确认）；no_source=无任何可识别源
COV = {
    "M_TECH_BASE_96_1": (["INT-C-TECH-150", "INT-C-TECH-100", "INT-C-TECH-107", "INT-C-TECH-113", "INT-C-TECH-118", "INT-C-TECH-182"], "jiuxin_pending", "久新交 SQL-96，在我方库跑；原料=论文/专利计数，须经技术点桥接"),
    "M_TECH_COMPOSITE_SCORE": ([], "no_source", "口径写明只读 ADS 已落库字段、分项与权重未冻、不抄 seq 182–191；不在久新 51 行，也无我方 owner → 生产方与原料均未定"),
    "M_TECH_CONVERT_BOTTLENECK": (["INT-C-TECH-158"], "jiuxin_pending", "seq 136 G3 Job 结果"),
    "M_TECH_DEEP_130_1": (["INT-C-TECH-153", "INT-C-TECH-151", "INT-C-TECH-152", "INT-C-TECH-170", "INT-C-TECH-171"], "jiuxin_pending", "API-130 结果；输入依赖技术点实体与关系"),
    "M_TECH_DEEP_131_1": (["INT-C-TECH-153", "INT-C-TECH-128"], "jiuxin_pending", "API-131；深圳切片需机构地理"),
    "M_TECH_DEEP_132_1": (["INT-C-TECH-154"], "jiuxin_pending", "API-132；专题 TOPIC-TECH-015 产品走 CMS"),
    "M_TECH_DEEP_133_1": (["INT-C-TECH-155", "INT-C-TECH-181", "INT-C-TECH-128"], "jiuxin_pending", "API-133；需技术领域码（TECH-P0-2）"),
    "M_TECH_DEEP_134_1": (["INT-C-TECH-156", "INT-C-TECH-181"], "jiuxin_pending", "API-134；需技术领域码"),
    "M_TECH_DEEP_135_1": (["INT-C-TECH-157"], "jiuxin_pending", "API-135"),
    "M_TECH_DEEP_136_1": (["INT-C-TECH-158"], "jiuxin_pending", "API-136"),
    "M_TECH_DEEP_137_1": (["INT-C-TECH-159"], "jiuxin_pending", "API-137"),
    "M_TECH_DEEP_138_1": (["INT-C-TECH-160", "INT-C-TECH-128"], "jiuxin_pending", "API-138；深圳切片"),
    "M_TECH_DEEP_139_1": (["INT-C-TECH-160", "INT-C-TECH-128"], "jiuxin_pending", "API-139；深圳切片"),
    "M_TECH_DEEP_140_1": (["INT-C-TECH-155", "INT-C-TECH-181", "INT-C-TECH-128"], "jiuxin_pending", "API-140；需技术领域码"),
    "M_TECH_DS_07_TECH_INNOV_002": (["INT-C-TECH-100", "INT-C-TECH-101", "INT-C-TECH-102", "INT-C-TECH-128"], "kit_declared", "kit：dwd_patent / _cited / _legal / dwd_org_base_info"),
    "M_TECH_DS_07_TECH_INNOV_004": (["INT-C-TECH-100", "INT-C-TECH-101", "INT-C-TECH-102", "INT-C-TECH-103", "INT-C-TECH-128"], "kit_declared", "kit：dwd_patent / _cited / _legal / _transfer / dwd_org_base_info"),
    "M_TECH_DS_07_TECH_INNOV_006": (["INT-C-TECH-100", "INT-C-TECH-101", "INT-C-TECH-103", "INT-C-TECH-128"], "kit_declared", "kit：dwd_patent / _cited / _transfer / dwd_org_base_info"),
    "M_TECH_EDGE_STRENGTH": (["INT-C-TECH-171", "INT-C-TECH-152"], "jiuxin_pending", "技术–技术边权，口径写随 seq 105"),
    "M_TECH_ENTITY_INFLUENCE": (["INT-C-TECH-170", "INT-C-TECH-171", "INT-C-TECH-182"], "candidate", "A2 missing、05 无专叶；原料只能是技术点图谱+文献桥接，计算 owner 未定"),
    "M_TECH_ENTITY_REL": (["INT-C-TECH-171", "INT-C-TECH-152", "INT-C-TECH-182"], "jiuxin_pending", "消费 seq 105 关系面"),
    "M_TECH_ENTITY_TOP5": (["INT-C-TECH-171", "INT-C-TECH-152", "INT-C-TECH-182"], "jiuxin_pending", "按 105 边权截 Top5（人/机构/论文/专利）"),
    "M_TECH_GRAPH_104_1": (["INT-C-TECH-151", "INT-C-TECH-170", "INT-C-TECH-100", "INT-C-TECH-105", "INT-C-TECH-106", "INT-C-TECH-107", "INT-C-TECH-110", "INT-C-TECH-113", "INT-C-TECH-115", "INT-C-TECH-120", "INT-C-TECH-126", "INT-C-TECH-127"], "jiuxin_pending", "久新 Python-104 在我方入站文本上抽技术点（输入表为候选）"),
    "M_TECH_GRAPH_105_1": (["INT-C-TECH-152", "INT-C-TECH-171"], "jiuxin_pending", "久新 Python-105 抽关系 → Nebula"),
    "M_TECH_GRAPH_STRUCT": (["INT-C-TECH-170", "INT-C-TECH-171", "INT-C-TECH-152"], "jiuxin_pending", "Nebula A 面技术点子图"),
    "M_TECH_HEAT_INDEX": (["INT-C-TECH-156"], "jiuxin_pending", "seq 134 G3 Job"),
    "M_TECH_HEAT_QUERY": (["INT-C-TECH-100", "INT-C-TECH-108", "INT-C-TECH-114", "INT-C-TECH-120", "INT-C-TECH-126"], "candidate", "查询结果集内 term TF；原料=文献 keywords，经 ES 检索（索引归 C05）"),
    "M_TECH_INVEST_AMOUNT": (["INT-C-TECH-120", "INT-C-TECH-122", "INT-C-TECH-131", "INT-C-TECH-132", "INT-C-TECH-133", "INT-C-TECH-182"], "candidate", "政府专项=项目 funded_amount；社会资本=融资/投资事件；三类均无技术键"),
    "M_TECH_LIFE_STAGE": (["INT-C-TECH-159"], "jiuxin_pending", "对照 seq 137"),
    "M_TECH_MATURITY_LEVEL": (["INT-C-TECH-159"], "jiuxin_pending", "对照 seq 137"),
    "M_TECH_OUTPUT_SCALE": (["INT-C-TECH-100", "INT-C-TECH-107", "INT-C-TECH-113", "INT-C-TECH-121", "INT-C-TECH-123", "INT-C-TECH-126", "INT-C-TECH-127", "INT-C-TECH-182"], "candidate", "成果与应用体量；「应用」原料未知，口径禁止拿论文/专利量冒充"),
    "M_TECH_PAPER_PATENT_CNT": (["INT-C-TECH-100", "INT-C-TECH-107", "INT-C-TECH-113", "INT-C-TECH-118", "INT-C-TECH-182"], "candidate", "COUNT DISTINCT paper_id / patent_id，按 technology_id"),
    "M_TECH_PATH_CENTRALITY": (["INT-C-TECH-170", "INT-C-TECH-171"], "candidate", "图算法输入=技术点网；owner 待 B06（初稿建议我方 Python 自研）"),
    "M_TECH_PATH_KEYNODE": (["INT-C-TECH-170", "INT-C-TECH-171"], "candidate", "同上；05 无专叶"),
    "M_TECH_PATH_PRIORITY": (["INT-C-TECH-170", "INT-C-TECH-171"], "candidate", "同上；05 无专叶"),
    "M_TECH_POTENTIAL_SCORE": (["INT-C-TECH-157"], "jiuxin_pending", "seq 135 G3 Job"),
    "M_TECH_REL_STRENGTH": (["INT-C-TECH-171", "INT-C-TECH-152"], "jiuxin_pending", "弦线图线粗，边权随 seq 105"),
    "M_TECH_STAGE_JUDGE": (["INT-C-TECH-159"], "jiuxin_pending", "G3 Job + LLM 未注册"),
    "M_TECH_SZ_ASSESS": (["INT-C-TECH-157", "INT-C-TECH-159", "INT-C-TECH-160", "INT-C-TECH-155", "INT-C-TECH-128"], "jiuxin_pending", "深圳综合评估包，复用潜力/阶段核"),
    "M_TECH_TOPIC_HEAT": (["INT-C-TECH-156", "INT-C-TECH-181"], "jiuxin_pending", "对照 seq 134；需技术领域/话题码"),
}

COMMON_GAPS = ["kit.source_tables=pending_ods（D3 pending_ods），本卡对应关系为候选，未经 data-agent 正式化"]


def gkx(nnn, table, cn, *, keys, pk, align, coverage, rows, rows_ref=R1010, freq=FREQ_UNK, dims=("TECH",),
        dep=("data",), gaps=(), conflicts=(), decision=(), risks=(), esc=False, conf="medium", tests=(), lumen="无（lumen 未读该表）",
        share=None, ours=("etl",)):
    return dict(nnn=nnn, sys="gkx_mysql_raw（甲方三方库 MySQL gkx @183.240.141.251:3318，只读 gkx_reader_zp）", table=table, cn=cn, keys=keys, pk=pk,
                align=align, coverage=coverage, rows=rows, rows_ref=rows_ref, freq=freq, dims=list(dims), dep=list(dep), gaps=list(gaps),
                conflicts=list(conflicts), decision=list(decision), risks=list(risks), esc=esc, conf=conf, tests=list(tests), lumen=lumen,
                share=share, counterpart="gkx_mysql_raw", form="table", jx=None, ours=list(ours))


PAT_SIDE_GAP = "附表行数≈1.6–2.1 万，仅为主表 dwd_patent（≈269 万）的 <1%：法律状态/引用/转移/同族/标题/摘要覆盖面严重不足，需供应方说明是否抽样"
CARDS = [
    gkx(100, "dwd_patent", "全球专利要素库·专利信息表",
        keys=["patent_id", "pn", "publication_number", "kind", "country_code", "apdt / apdt_year", "pbdt / pbdt_year", "applicants / first_applicant_name",
              "assignees / first_current_assignee_name", "inventors", "main_classification_ipcr", "further_classification_ipcr", "main_classification_cpc",
              "further_classification_cpc", "keywords", "claims", "granted_number", "value", "other_Versions"],
        pk="patent_id（live 另有 pn 公布号）", align="技术点：无技术点键，只能经 IPC/CPC 分类号 + keywords 归入技术点/领域（需桥接 INT-C-TECH-182）；机构：first_applicant_name/assignees 只有名称，需归一到 org_id（C03）",
        coverage="全球（country_code 多国）；深圳切片需申请人→机构地理", rows="2,690,167",
        gaps=["无技术点/技术领域稳定码（TECH-P0-1/P0-2 待供应方回复）", "无申请人地址/机构 ID 列，深圳切片要靠名称归一", PAT_SIDE_GAP.replace("附表", "本表的附表")],
        conflicts=["DDL 沙箱 gkx_schema_ddl.sql（2026-07-15）列为 classification_ipcr / application_reference_*；live（2026-09-11 结构报告）为 main_classification_ipcr / apdt_year / pn；以 live 为准，kit 与 live 一致", "行数 2026-09-11=2,892,155 → 2026-10-10=2,690,167（估数波动 −20 万）"],
        tests=["对账：按 country_code / apdt_year 分布与供应方口径抽样", "契约：IPC 主分类非空率、pn 唯一性"], conf="high",
        lumen="lumen-etl-es-py db/dwd_domain_tables.sql 仅有企业维 enterprise_patent_detail（来源 dwd_patent，ENT 域）；无技术维"),
    gkx(101, "dwd_patent_cited", "全球专利要素库·专利引用关系表",
        keys=["patent_id", "pn", "reference_cited_count", "cited_by_nums", "cited_by", "patent_citations", "non_patent_count", "cited_by_date"],
        pk="patent_id（逻辑 id）", align="经 patent_id → dwd_patent → 技术点桥接", coverage="随 dwd_patent（全球）", rows="20,239", rows_ref=R1010 + "；表不在 DDL 沙箱，字段见 " + R0911S,
        gaps=[PAT_SIDE_GAP, "DDL 沙箱（07-15）无此表，结构以 09-11 live 报告为准"], tests=["对账：cited_by_nums 与 dwd_patent.cited_by_nums 一致性"]),
    gkx(102, "dwd_patent_legal", "全球专利要素库·法律状态信息表",
        keys=["patent_id", "status", "legal_events", "anticipated_expiration", "expiration_year"], pk="patent_id",
        align="经 patent_id", coverage="随 dwd_patent", rows="19,071", gaps=[PAT_SIDE_GAP]),
    gkx(103, "dwd_patent_transfer", "全球专利要素库·专利转移信息表",
        keys=["patent_transfer_id", "pn", "country", "transfer_effective_date", "transfer_before", "transfer_after"], pk="patent_transfer_id",
        align="经 pn → dwd_patent；转移前后权利人只有名称，需机构归一", coverage="随 dwd_patent", rows="21,193", rows_ref=R1010 + "；字段见 " + R0911S,
        gaps=[PAT_SIDE_GAP, "DDL 沙箱（07-15）无此表"]),
    gkx(104, "dwd_patent_family", "全球专利要素库·专利家族信息表",
        keys=["patent_id", "simple_family", "simple_family_2（成员国家）", "simple_family_3（成员公开号）"], pk="patent_id",
        align="同族归并用于专利去重（technology_id 下 COUNT DISTINCT 前先并族，口径待定）", coverage="随 dwd_patent", rows="16,235", gaps=[PAT_SIDE_GAP],
        decision=["技术点专利计数是否按简单同族去重（影响 M_TECH_PAPER_PATENT_CNT 口径）"]),
    gkx(105, "dwd_patent_title", "全球专利要素库·专利标题信息表",
        keys=["patent_id", "title_localized", "title_localized_2（英文）"], pk="patent_id", align="技术实体识别（seq 104）文本输入", coverage="随 dwd_patent",
        rows="19,420", dep=("data", "algorithm"), gaps=[PAT_SIDE_GAP + "；标题是 NER 主输入，覆盖不足直接限制技术点抽取"]),
    gkx(106, "dwd_patent_abstract", "全球专利要素库·专利摘要信息表",
        keys=["patent_id", "abstract_localized", "abstract_localized_2（英文）"], pk="patent_id", align="技术实体识别/关系抽取文本输入", coverage="随 dwd_patent",
        rows="19,247", dep=("data", "algorithm"), gaps=[PAT_SIDE_GAP]),
    gkx(107, "dwd_zh_paper", "中文论文要素库·中文论文详情信息",
        keys=["id", "doi", "zh_name", "en_name", "publication_id", "publication_zh_name", "issn", "cover_year_start", "cover_date_start", "language_classify", "paper_url"],
        pk="id", align="无技术点键；经 dwd_zh_paper_classification.keywords/scope 归入技术点/领域；作者机构需 C01/C03 作者-机构关联", coverage="中国为主（中文期刊）",
        rows="89,214", gaps=["无机构/地理列，深圳切片需作者-机构关联（dwd_author_* 归 C01）", "标题/摘要/分类附表仅 1.4–1.9 万行，约为主表 16–22%"], conf="high"),
    gkx(108, "dwd_zh_paper_classification", "中文论文要素库·中文论文分类信息",
        keys=["id", "scope（大类学科）", "scope_zone（细分学科）", "keywords"], pk="id", align="学科 scope/scope_zone 可作技术领域映射锚点之一；keywords 作技术点候选",
        coverage="随 dwd_zh_paper", rows="18,895", dep=("data", "algorithm"),
        gaps=["只覆盖约 21% 中文论文", "scope 为期刊学科，不等于技术领域码，需映射表（INT-C-TECH-181）"]),
    gkx(109, "dwd_zh_paper_title", "中文论文要素库·中文论文标题信息", keys=["id", "标题文本"], pk="id", align="NER 文本输入", coverage="随 dwd_zh_paper",
        rows="19,288", dep=("data", "algorithm"), gaps=["只覆盖约 22% 中文论文（主表 zh_name 可替代）"], conf="low"),
    gkx(110, "dwd_zh_paper_abstract", "中文论文要素库·中文论文摘要信息", keys=["id", "摘要文本"], pk="id", align="NER/关系抽取文本输入",
        coverage="随 dwd_zh_paper", rows="14,254", dep=("data", "algorithm"), gaps=["只覆盖约 16% 中文论文"]),
    gkx(111, "dwd_zh_paper_citation", "中文论文要素库·中文论文引用/被引信息",
        keys=["id", "publication_id", "doi", "zh_name", "publication_zh_name"], pk="id", align="经 id/doi 关联论文；用于技术点影响力/热度候选特征",
        coverage="随 dwd_zh_paper", rows="17,494", conflicts=["2026-10-10 报告中「引用文献信息」「被引用信息」两行同指 dwd_zh_paper_citation（17,494），语义需供应方澄清"]),
    gkx(112, "dwd_zh_paper_reference", "中文论文要素库·中文论文参考文献信息", keys=["id", "参考文献"], pk="id", align="经 id 关联论文；技术演进/引用网络候选",
        coverage="随 dwd_zh_paper", rows="12,914", conf="low"),
    gkx(113, "dwd_en_paper", "外文论文要素库·英文论文详情信息",
        keys=["id", "doi", "en_name", "publication_en_name", "issn_print", "cover_year_start", "language", "data_source"], pk="id",
        align="无技术点键；经 dwd_en_paper_classification 归入", coverage="全球（外文）——但量极小", rows="1,356",
        gaps=["仅 1,356 行，无法支撑「全球」技术态势的论文侧统计", "无机构/国家列"],
        decision=["全球论文侧数据量是否由供应方补足，或甲方接受以专利为全球主口径"], risks=["全球技术热点/前沿若以论文为输入，结果会严重偏向中文文献"]),
    gkx(114, "dwd_en_paper_classification", "外文论文要素库·英文论文分类信息", keys=["id", "scope", "sub_scope", "keywords"], pk="id",
        align="学科锚点 + keywords", coverage="随 dwd_en_paper", rows="1,386", dep=("data", "algorithm"), gaps=["量极小，同 INT-C-TECH-113"]),
    gkx(115, "dwd_en_paper_abstract", "外文论文要素库·英文论文摘要信息", keys=["id", "摘要文本"], pk="id", align="NER 文本输入", coverage="随 dwd_en_paper",
        rows="1,192", dep=("data", "algorithm"), gaps=["量极小"], conf="low"),
    gkx(116, "dwd_en_paper_citation", "外文论文要素库·英文论文引用文献信息", keys=["id", "引用文献"], pk="id", align="经 id", coverage="随 dwd_en_paper",
        rows="1,352", gaps=["量极小"], conf="low"),
    gkx(117, "dwd_en_paper_cited_by", "爱思唯尔外文论文引用关系表", keys=["id", "paper_eid", "citing_eid", "citing_year"], pk="id",
        align="paper_eid 指向 dwd_en_paper（键名 eid 与 id 的对应待核）", coverage="unknown", rows="unknown",
        rows_ref="不在 20 要素库行数报告覆盖内；存在于 " + INV + " 与 SOURCE-TABLES.md",
        gaps=["行数 unknown，需只读 COUNT 核验（见 handoff 只读 SQL 草案）", "eid 与 dwd_en_paper.id 对齐规则未知"], conf="low"),
    gkx(118, "dwd_scholar_papers", "人才要素库·论文信息（学者论文）",
        keys=["paper_id", "zh_name", "en_name", "authors", "doi", "cover_date_start", "publication_en_name", "zh_abstract", "en_abstract"], pk="paper_id",
        align="与 dwd_zh_paper / dwd_en_paper 无共同主键，只能 doi 对齐（去重口径待定）；人才侧由 C01 主盘点", coverage="全球（学者库）", rows="597,513",
        dims=("TECH", "TAL"), gaps=["与两套论文库存在重复计数风险（无统一 paper 主键）"],
        decision=["技术点论文量的论文全集 = zh_paper ∪ en_paper ∪ scholar_papers（按 doi 去重）还是仅论文要素库"], share="C01 主卡，本卡只记技术链用法"),
    gkx(119, "dwd_scholar_research_direction", "人才要素库·学者研究方向", keys=["scholar_id", "fields"], pk="scholar_id（live 另有 id）",
        align="fields 为自由文本研究方向，可作技术点/领域到人才的弱关联", coverage="随 dwd_scholar（16,933 学者）", rows="19,466", dims=("TECH", "TAL"),
        gaps=["fields 非编码，需归一到技术点/领域"], share="C01 主卡"),
    gkx(120, "dwd_zh_project", "国内项目要素库·国内项目信息表",
        keys=["id", "project_number", "title", "project_source", "funded_institution", "funded_amount", "discipline", "discipline_code", "fund_category",
              "funded_province", "approval_year", "keywords", "abstract"], pk="pk_id（业务 id）",
        align="discipline_code 可作领域锚点；keywords/abstract 作技术点候选；funded_institution 名称需机构归一", coverage="中国（funded_province 可做省级）", rows="46,455",
        gaps=["funded_amount 无技术键，作「政府专项投入」需经技术点桥接", "单位（元/万元）需核验"], tests=["对账：approval_year × funded_province 分布"], conf="high"),
    gkx(121, "dwd_zh_project_output", "国内项目要素库·国内项目-产出信息",
        keys=["id", "total_outputs", "journal_articles_count", "patents_count", "products_count", "output_patents", "output_products"], pk="pk_id（业务 id）",
        align="经 id 关联 dwd_zh_project", coverage="随 dwd_zh_project", rows="17,475", gaps=["产出仅给计数与标题文本，无产出主键（不能直接 JOIN 专利/论文）"]),
    gkx(122, "dwd_en_project", "国外项目要素库·国外项目信息表",
        keys=["项目索引", "项目编号", "项目名称", "受资助金额", "学科 / 学科代码", "项目受资助国家", "立项年度", "关键词"], pk="项目索引（英文列名以 live 为准）",
        align="同 INT-C-TECH-120", coverage="全球（国外）", rows="16,281", rows_ref=R1010 + "；表不在 DDL 沙箱，字段见 " + R0911S,
        gaps=["DDL 沙箱无此表；英文列名未在本叶核实", "币种/单位未知"], conf="low"),
    gkx(123, "dwd_en_project_output", "国外项目要素库·国外项目-产出信息", keys=["项目索引", "产出计数/标题"], pk="unknown",
        align="经项目索引", coverage="随 dwd_en_project", rows="17,689", gaps=["结构未在本叶核实"], conf="low"),
    gkx(124, "dwd_rel_project_patent", "项目-专利关联表", keys=["project_source", "project_id", "patent_id"], pk="pk_id",
        align="项目 ↔ 专利显式边，可补技术点桥接", coverage="unknown", rows="unknown", rows_ref="不在 20 要素库行数报告覆盖内；见 " + INV,
        gaps=["行数 unknown，需只读 COUNT"], conf="low"),
    gkx(125, "dwd_rel_project_paper", "项目-论文关联表", keys=["project_source", "project_id", "paper_source", "paper_id"], pk="pk_id",
        align="项目 ↔ 论文显式边", coverage="unknown", rows="unknown", rows_ref="不在 20 要素库行数报告覆盖内；见 " + INV,
        gaps=["行数 unknown，需只读 COUNT"], conf="low"),
    gkx(126, "dwd_zh_report", "中文报告要素库·中文科技报告信息表",
        keys=["report_id", "report_category", "title_cn", "organization", "abstract_cn", "keywords_cn", "preparation_time", "related_projects"], pk="pk_id（业务 report_id）",
        align="keywords_cn 作技术点候选；关联表 dwd_zh_report_paper/_project/_org（5,880/653/1,387 行）", coverage="中国", rows="13,699", dep=("data", "algorithm")),
    gkx(127, "dwd_en_report", "外文报告要素库·外文科技报告信息表", keys=["报告 id", "标题", "摘要", "关键词"], pk="unknown（DDL 沙箱无此表）",
        align="文本作技术点候选", coverage="全球（外文）", rows="10,070", rows_ref=R1010, gaps=["结构未在本叶核实"], conf="low"),
    gkx(128, "dwd_org_base_info", "国内机构要素库·机构基本信息（申请人/承担单位对齐 + 深圳切片）",
        keys=["org_id", "name_cn", "external_id（统一社会信用代码）", "city", "province", "reg_status"], pk="org_id",
        align="专利申请人/项目承担单位名称 → org_id（名称归一规则归 C03）；city/province 提供深圳切片", coverage="中国（国外机构在 dwd_forg_base_info 19,549 行，kit 未列）",
        rows="192,464", dims=("TECH", "ORG"), dep=("data",), share="C03 主卡，本卡只记技术链用法（MODEL×3 kit 点名）",
        gaps=["全球专利申请人对齐国外机构需 dwd_forg_base_info，kit 未列"]),
    gkx(129, "dwd_org_base_info_patent_rel", "国内机构-专利关联表", keys=["org_id", "base_external_id", "patent_id", "publication_number"], pk="id",
        align="机构 ↔ 专利显式边，可替代名称归一", coverage="unknown", rows="unknown", rows_ref="不在 20 要素库行数报告覆盖内；见 " + INV + " 与 SOURCE-TABLES.md",
        dims=("TECH", "ORG"), gaps=["行数 unknown；若有数据，应优先于名称归一（与 C03 协同）"], conf="low"),
    gkx(130, "dwd_org_tech_tag", "国内机构要素库·科技型标签", keys=["org_id", "org_tag", "data_source"], pk="unknown（org_id+org_tag）",
        align="机构资质标签（如高新技术企业类），不是技术点", coverage="中国", rows="196,662", dims=("TECH", "ORG", "OTHER"),
        conflicts=["表名含「科技型标签」，易被误当技术点源；实为机构标签，禁止作技术点主数据"], conf="medium"),
    gkx(131, "dwd_org_financing_info", "国内机构融资事件", keys=["org_id", "name_cn", "funding_round", "funding_amount", "funding_currency_code", "completion_date", "investors_name"],
        pk="pk_id", align="只有机构维，无技术键；技术投资额需 org→技术点（经专利/标签）间接归属", coverage="中国", rows="23,662", dims=("TECH", "OTHER"),
        decision=["「社会资本投入」按融资事件还是投资事件；按机构归属到技术点的分摊规则"], gaps=["无技术键"]),
    gkx(132, "dwd_org_invest_info", "投资事件", keys=["org_id", "inv_org_id", "inv_name", "investment_amount", "investment_ratio"], pk="pk_id",
        align="同 INT-C-TECH-131", coverage="中国", rows="53,758", dims=("TECH", "OTHER"), gaps=["无技术键", "无投资日期列（DDL 沙箱），时间窗口无法切"]),
    gkx(133, "dwd_industrial_fund_investment_project_info", "金融要素库·产业基金投资项目信息", keys=["结构未在本叶核实"], pk="unknown",
        align="产业基金→项目，可能含行业/领域文本", coverage="中国", rows="9,939", rows_ref=R1010 + "；DDL 沙箱无此表", dims=("TECH", "OTHER"),
        gaps=["结构未核实"], conf="low"),
    gkx(134, "dwd_quantum_tech_trend", "量子专题·量子技术趋势",
        keys=["id", "technology_name", "technology_category", "maturity_stage", "application_prospect", "main_orgs", "publish_time"], pk="id",
        align="三方库唯一带 technology_name / maturity_stage 的表，但只覆盖量子领域", coverage="量子专题切片", rows="unknown",
        rows_ref="不在 20 要素库行数报告覆盖内；见 " + INV, gaps=["行数 unknown", "领域切片，不能作全域技术点主数据"],
        risks=["若被当成技术点主表会把全域技术链窄化为量子"], conf="low"),
    gkx(135, "dwd_quantum_rd_progress", "量子专题·量子研发进展", keys=["id", "project_name", "organization_name", "credit_code", "rd_direction", "rd_stage"], pk="id",
        align="rd_direction / rd_stage 为文本", coverage="量子专题切片", rows="unknown", rows_ref="不在 20 要素库行数报告覆盖内；见 " + INV,
        gaps=["行数 unknown"], conf="low"),
    gkx(136, "dwd_industry_code", "产业链环节码表（海洋/量子专题共用）", keys=["code", "name", "parent_code", "industry_code", "industry_name", "level", "is_key_link"],
        pk="code", align="产业链环节码，不是技术领域码", coverage="海洋/量子等专题产业", rows="19,855", dims=("TECH", "OTHER"),
        conflicts=["TECH-SUPPLIER-QUESTIONS 明确：禁止用产业链 INB*/环节码冒充技术领域码"], conf="high"),
    gkx(137, "dwd_org_important_news_info", "国内机构要素库·重点资讯", keys=["org_id", "标题", "正文", "发布时间"], pk="unknown（本叶未核）",
        align="资讯文本可作技术话题热度原料（需 NER 到技术点/话题）", coverage="中国", rows="1,371,863", dims=("TECH", "OTHER"), dep=("data", "algorithm"),
        gaps=["无技术/话题键；SOURCE-TABLES §3.1 裁定可用"], conf="low"),
    gkx(138, "dwd_industry_analysis_*（六表）", "行业分析要素库（documents/companies/industries/topics/content_types/countries）",
        keys=["document_id", "title", "abstract", "body", "creation_date", "language", "topics.*", "industries.*", "countries.*"], pk="document_id（uk）",
        align="topics/industries 为供应方主题维，可作技术话题候选；需映射到技术领域码", coverage="全球（countries 维）", rows="unknown",
        rows_ref="不在 20 要素库行数报告覆盖内；结构见 data/data-design/storage/CHAIN/sources/inventory-industry-analysis.md（gkx live 存在）",
        dims=("TECH", "OTHER"), dep=("data", "algorithm"), gaps=["行数 unknown", "topics 编码与技术领域无对应"], conf="low"),
    gkx(139, "dwd_org_industry_chain_pat_dtl", "产业链关联专利信息", keys=["chain_code", "node_id", "node_name", "apno", "pn", "current_assign"], pk="unknown",
        align="产业链节点 ↔ 专利；节点是产业环节非技术点", coverage="unknown", rows="unknown", rows_ref="不在 20 要素库行数报告覆盖内；见 SOURCE-TABLES.md",
        dims=("TECH", "OTHER"), conflicts=["产业链节点不得当技术点（同 INT-C-TECH-136）"], gaps=["行数 unknown"], conf="low"),
]

# ---- 久新交付（51 行之技术链 25 行）作为源实体 ----
JX_COMMON_GAP = ["久新交付形态与数据底座一律待确认（JIUXIN 清单 51 行 0 确认）", "返回实体 ID 是否为我方 technology_id 未知（见 id_alignment_draft）"]


def jx(nnn, name, rows_ids, form, mids_note, dep, out_fields, fresh="unknown", extra_gaps=(), decision=(), esc=False, conf="low"):
    return dict(nnn=nnn, sys="北京久新（对端；交付待确认）", table=name, cn=name, keys=out_fields, pk="unknown（建议以我方 technology_id + as_of + version 为键）",
                align="入参/出参须用我方 technology_id 与技术领域码；若用久新自有 ID 须附映射表", coverage="unknown（久新数据底座未知）", rows="unknown",
                rows_ref="对端交付物，无快照", freq=fresh, dims=["TECH"], dep=list(dep), gaps=JX_COMMON_GAP + list(extra_gaps), conflicts=[],
                decision=list(decision), risks=["久新若以其自有数据计算，结果与我方入站数据不同源，对账与下钻断裂"], esc=esc, conf=conf, tests=[],
                lumen="无（lumen-algo-py 无 /internal/jiuxin/* 适配层）", share=mids_note, counterpart="jiuxin", form=form, jx=rows_ids,
                ours=["python_internal", "etl"])


CARDS += [
    jx(150, "久新 SQL-96 技术基础指标模型", ["SRS-96"], "SQL", "基础计数（论文量/专利量/增长）", ["data", "metric"],
       ["technology_id", "paper_cnt", "patent_cnt", "growth", "as_of"], fresh="T+1（由我方调度，草案）",
       extra_gaps=["SQL 须能在我方入站 dwd_* / 项目 DWD 上运行；表名映射未给"], decision=["SQL-96 的统计对象是我方技术点还是久新自有技术分类"]),
    jx(151, "久新 Python-104 技术实体识别产出（技术点实体集）", ["SRS-104"], "Python", "技术点主数据候选生产者", ["data", "algorithm", "graph"],
       ["technology_id（待定）", "name", "aliases", "domain_code", "source_doc_refs"], fresh="offline（离线 Job，频率待定）",
       extra_gaps=["脚本输入表/依赖未知；须并入 lumen-algo-py 离线 Job，依赖不得超出仓栈"], esc=True,
       decision=["104 产出的技术点是否作为我方技术点主数据底稿（主数据持有方）"]),
    jx(152, "久新 Python-105 技术实体关系抽取产出（技术–技术 / 实体–技术边）", ["SRS-105"], "Python", "技术点图谱边 + 边权（EDGE/REL_STRENGTH、ENTITY_REL/TOP5 消费）",
       ["src_technology_id", "dst_id", "dst_type", "rel_type", "weight", "evidence_doc_ids"], ["data", "algorithm", "graph"], fresh="offline",
       extra_gaps=["边权口径/关系类型枚举未知；写 Nebula 的 edge 清单归 C04"], esc=True),
    jx(153, "久新 API-130/131 技术链结构结果集（全景 / 深圳）", ["SRS-130", "SRS-131"], "API", "技术链节点/边结构", ["data", "metric", "graph"],
       ["technology_id", "chain_nodes", "chain_edges", "region_scope", "as_of"]),
    jx(154, "久新 API-132 技术发展历程结果集", ["SRS-132"], "API", "历程时间轴", ["data", "metric"], ["technology_id", "events[]", "as_of"],
       decision=["专题 TOPIC-TECH-015 历程走 CMS；久新是否仍提供 API"]),
    jx(155, "久新 API-133/140 深圳细分领域分布 / 重点布局推荐结果集", ["SRS-133", "SRS-140"], "API", "领域维结果（依赖技术领域码）", ["data", "metric"],
       ["domain_code", "share / score", "recommend_rank", "as_of"], extra_gaps=["依赖技术领域码体系（TECH-P0-2）"]),
    jx(156, "久新 API-134 前沿热点识别结果集（含展示 6 行）",
       ["SRS-134", "DS-03-RESULT-001", "DS-03-RESULT-002", "DS-07-SCI-CREATE-003", "DS-09-COMPREHENSIVE-001", "DS-09-COMPREHENSIVE-002", "DS-09-COMPREHENSIVE-004"],
       "API", "热度/增速/话题热度", ["data", "metric"], ["technology_id / topic_id", "heat", "growth", "term", "as_of"],
       decision=["「实时」热点的真实时效（客户决策项草案）"]),
    jx(157, "久新 API-135 产业化潜力结果集（含展示 1 行）", ["SRS-135", "DS-07-TECH-INNOV-003"], "API", "潜力评分", ["data", "metric"],
       ["technology_id", "potential_score", "dims", "as_of"]),
    jx(158, "久新 API-136 转化瓶颈识别结果集", ["SRS-136"], "API", "瓶颈与原因", ["data", "metric"], ["technology_id", "bottlenecks[]", "reasons[]", "as_of"]),
    jx(159, "久新 API-137 技术阶段 / 成熟度结果集（含展示 4 行）",
       ["SRS-137", "DS-03-RESULT-004", "DS-03-RESULT-005", "DS-03-RESULT-006", "DS-07-INDUSTRY-POTENTIAL-002"], "API", "阶段/成熟度", ["data", "metric"],
       ["technology_id", "life_stage", "maturity_level", "as_of"], decision=["生命周期分档是否含「衰退」（QC03 技术成熟度口径）"]),
    jx(160, "久新 API-138/139 深圳技术发展问题 / 机遇识别结果集", ["SRS-138", "SRS-139"], "API", "深圳问题/机遇清单", ["data", "metric"],
       ["technology_id / domain_code", "issues[] / opportunities[]", "as_of"]),
]

# ---- TRSGraph 与我方待建结构 ----
CARDS += [
    dict(nnn=170, sys="trsgraph（NebulaGraph TRSGraph graphd 10.50.75.136:9669）", table="TAG technology（技术点顶点）", cn="Nebula 技术点顶点",
         keys=["vid", "name", "node_type", "weight", "props"], pk="VID 现规则 tech:{名称}（ENT pipeline-to-nebula §79/§105）",
         align="现行 VID 用名称，非稳定 ID；ENT 管线写明「无专题库技术 ID」、无稳定技术点不上图", coverage="unknown", rows="unknown",
         rows_ref="本叶未连 Nebula；live 点数由 C04 核", freq="unknown", dims=["TECH"], dep=["graph"],
         gaps=["live 是否已有技术点顶点、数量 unknown（C04）", "VID 规则 tech:{名称} 无法承接同名异义/别名归一"], conflicts=[],
         decision=[], risks=["若沿用名称 VID，技术点改名/合并会断边"], esc=True, conf="medium", tests=["图谱一致性：顶点数 = 技术点主表行数"],
         lumen="无", share=None, counterpart="trsgraph", form="table", jx=None, ours=["graph_load"]),
    dict(nnn=171, sys="trsgraph（NebulaGraph TRSGraph）", table="技术相关 EDGE（技术–技术、实体–技术；ENT 已定义 produces）", cn="Nebula 技术点边",
         keys=["src_vid", "dst_vid", "rel_type", "weight"], pk="(src, dst, rank)", align="边端点需稳定 technology_id", coverage="unknown", rows="unknown",
         rows_ref="本叶未连 Nebula；C04 核", freq="unknown", dims=["TECH", "ORG", "TAL"], dep=["graph"],
         gaps=["技术–技术边类型（演进/依赖/掌握/应用/产业化，见 srs 04 seq 13）未在 schema 落地", "produces 边现网靠新闻推断（infer_org_produces_tech），无稳定技术点即不上图"],
         conflicts=[], decision=[], risks=["人工维护写回（A03）与 105 自动灌入的优先级未定"], esc=True, conf="low", tests=[], lumen="无", share=None,
         counterpart="trsgraph", form="table", jx=None, ours=["graph_load"]),
    dict(nnn=180, sys="我方项目自建（待建，不在任何现有库）", table="技术点主数据表（建议 dwd/ads technology_master，名待定）", cn="技术点主数据",
         keys=["technology_id", "name_cn", "name_en", "aliases[]", "domain_code", "parent_technology_id", "source（jx104|manual）", "status", "version"],
         pk="technology_id（全局稳定 ID）", align="全部技术维数据的对齐锚点；Nebula VID = tech:{technology_id}", coverage="全球（随文献）", rows="0（不存在）",
         rows_ref="本叶检索 data/、ddl/、lumen-etl-es-py、lumen-algo-py、lumen-svc-platform 均无", freq="随 104 Job + 人工维护",
         dims=["TECH"], dep=["data", "graph", "write_back"], gaps=["表不存在"], conflicts=[],
         decision=["技术点主数据持有方（我方 / 久新 / 甲方）"], risks=[], esc=True, conf="medium", tests=["契约：technology_id 唯一、别名不跨点"],
         lumen="无", share=None, counterpart="none", form="none", jx=None, ours=["etl", "graph_load"]),
    dict(nnn=181, sys="我方项目自建（待建）", table="技术领域分类维表（建议 dim_tech_domain，名待定）", cn="技术领域分类体系",
         keys=["domain_code", "domain_name", "parent_code", "level", "ipc_anchor[]", "discipline_anchor[]", "version"], pk="domain_code",
         align="IPC/CPC、论文 scope、项目 discipline_code 三套映射到同一 domain_code；与久新共用", coverage="全球", rows="0（不存在）",
         rows_ref="ddl/ 仅有地区/国家/产业集群维（gkxlumenx_dim_*），无技术领域维", freq="版本化，低频",
         dims=["TECH"], dep=["data"], gaps=["表不存在", "TECH-P0-2 供应方未回复"], conflicts=["禁止用产业链 INB* / dwd_industry_code 冒充"],
         decision=["技术领域分类体系选型：IPC 派生 / 国家学科分类 / 战略性新兴产业分类 / 甲方自定义"], risks=[], esc=True, conf="medium", tests=[],
         lumen="无", share=None, counterpart="none", form="none", jx=None, ours=["etl"]),
    dict(nnn=182, sys="我方项目自建（待建）", table="技术点↔文献/机构/人才桥接表（建议 dwd technology_doc_rel，名待定）", cn="技术点桥接",
         keys=["technology_id", "doc_type（patent|zh_paper|en_paper|scholar_paper|project|report）", "doc_id", "weight", "method（ipc|keyword|ner）", "version"],
         pk="(technology_id, doc_type, doc_id, version)", align="把 dwd_* 文献主键挂到 technology_id；机构/人才经文献二跳", coverage="随文献", rows="0（不存在）",
         rows_ref="同 INT-C-TECH-180", freq="随 104 Job", dims=["TECH", "ORG", "TAL"], dep=["data", "algorithm"], gaps=["表不存在", "TECH-P1-3 供应方未回复"],
         conflicts=[], decision=[], risks=["归属方法（IPC 规则 vs NER）不同会导致计数差异"], esc=True, conf="medium",
         tests=["对账：同一专利在不同 method 下的技术点命中率"], lumen="无", share=None, counterpart="none", form="none", jx=None, ours=["etl", "python_internal"]),
]


def metrics_of(card_id):
    return sorted(m for m, (ids, _, _) in COV.items() if card_id in ids)


def pages_of(mids):
    return sorted({p for m in mids for p in PAGES[m]})


def build_card(c):
    cid = f"INT-C-TECH-{c['nnn']}"
    mids = metrics_of(cid)
    is_gkx = c["counterpart"] == "gkx_mysql_raw"
    downstream = {
        "gkx_mysql_raw": f"gkx.{c['table']} → 项目 DWD（data 层 ETL）→ ADS / ES（C05）/ Nebula（C04）",
        "jiuxin": "久新 " + c["form"] + "（待确认）→ Python 适配/Job → 结果快照 ADS（metric_id + as_of + version）",
        "trsgraph": "Nebula TRSGraph space（C04 定）",
        "none": "项目 DWD / ADS（新表，结构升级）",
    }[c["counterpart"]]
    return {
        "int_id": cid,
        "layer": "data",
        "srs": None,
        "page_ref": None,
        "dimension": c["dims"],
        "dep_kind": c["dep"],
        "metric_ids": mids,
        "metric_domain_other": [],
        "algorithm_type": sorted({atype(m) for m in mids}),
        "integration_pattern": "TBD",
        "ours": c["ours"],
        "counterpart": c["counterpart"],
        "delivery_form": c["form"],
        "jiuxin_row_id": c["jx"],
        "call_chain": {
            "fe_route": None,
            "java": "只读 ADS（draft；Java 不直连三方库、不写 nGQL）",
            "python": ("lumen-etl-es-py / lumen-algo-py 离线 ETL·Job（draft）" if c["counterpart"] != "jiuxin"
                       else "POST /internal/jiuxin/tech/*（draft，适配层归 B01 模式）"),
            "downstream": downstream,
        },
        "contract_draft": {
            "request": ([] if is_gkx else ["technology_id", "domain_code", "region_scope", "time_range", "as_of"]),
            "response_key_fields": c["keys"],
            "granularity": {"time": "year（apdt_year / cover_year_start / approval_year）" if is_gkx else "unknown", "geo": "country / province（深圳需机构 city）" if is_gkx else "unknown"},
            "freshness": "unknown" if c["freq"].startswith("unknown") else c["freq"],
        },
        "data_source": {
            "source_system": c["sys"],
            "table": c["table"],
            "table_cn": c["cn"],
            "key_fields": c["keys"],
            "primary_key": c["pk"],
            "entity_align_key": c["align"],
            "coverage": c["coverage"],
            "update_freq": c["freq"],
            "rows": {"value": c["rows"], "as_of": "2026-10-10" if c["rows_ref"].startswith(R1010[:40]) else None, "ref": c["rows_ref"]},
            "pages": pages_of(mids),
            "shared_with": c["share"],
        },
        "status": {
            "demo": "demo-* 未以 dwd_* 技术维接入（技术链页为 Mock；未逐页核）",
            "lumen": c["lumen"],
            "d1_d4": {"d1": "draft", "d4": "mock"} if mids else None,
        },
        "gaps": (COMMON_GAPS if mids and any(COV[m][1] == "candidate" for m in mids) else []) + c["gaps"],
        "conflicts": c["conflicts"],
        "decision_needed": c["decision"],
        "structure_escalation": c["esc"],
        "risks": c["risks"],
        "test_points": c["tests"] or ["契约：关键字段非空率/主键唯一", "降级：源缺失时页面空态 + 角标，不填 0"],
        "confidence": c["conf"],
    }


MASTER = {
    "conclusion": "当前没有任何一方持有技术点（technology）实体主数据：甲方三方库 gkx 无技术点表与稳定码，TRSGraph technology 顶点 VID 是名称，久新 104 产出未确认。"
                  "草案建议由我方项目自建「技术点主表 + 技术领域维表」作为主数据（INT-C-TECH-180/181），内容底稿由久新 Python-104（并入 lumen-algo-py 离线 Job）在我方入站文献上抽取，"
                  "人工维护经全景维护页写回；久新 API 一律以我方 technology_id / domain_code 交互。",
    "status": "decision_needed（待甲方 / 久新确认，structure_escalation → human:李伟）",
    "evidence": [
        "SOURCE-TABLES.md 206 张活跃 dwd_* 无技术点/技术主题主表；TECH-SUPPLIER-QUESTIONS TECH-P0-1/P0-2（2026-09-04）待回复",
        "唯一含 technology_name 的 dwd_quantum_tech_trend 是量子专题切片、行数 unknown，不可作全域主数据（INT-C-TECH-134）",
        "dwd_org_tech_tag 为机构资质标签、dwd_industry_code / dwd_org_industry_chain_pat_dtl 为产业链环节，均不是技术点（INT-C-TECH-130/136/139）",
        "技术分类信号只在文献属性：专利 main/further_classification_ipcr/cpc + keywords；论文 scope/scope_zone/keywords；项目 discipline_code/keywords；学者 fields；报告 keywords_cn",
        "data-design/storage/ENT/etl/pipeline-to-nebula.md：TAG technology、VID tech:{名称}、「无专题库技术 ID」「无稳定技术点不上图」",
        "JIUXIN-TECH-ORG-TALENT-L01：SRS-104/105 Python 待确认；jx-tech-topic 两仓 2026-10-15 为空模板（只有 README），无法判断久新数据底座",
        "lumen-algo-py / lumen-etl-es-py / lumen-svc-platform 均无 technology_id",
    ],
    "candidates": [
        {"option": "A 我方自建主表（推荐草案）", "pros": "ID 稳定、可审计、与 Nebula/ES/ADS 同源", "cons": "需新表 + 维表 + 归一流程（结构升级）"},
        {"option": "B 久新持有主数据、我方存映射", "pros": "我方工作量小", "cons": "主数据在对端，命中率与变更不可控；违背 Java 只读 ADS 的数据闭环"},
        {"option": "C 以 IPC 分类号直接充当技术点", "pros": "零建设", "cons": "粒度是分类不是技术点；论文/项目无 IPC；与 SRS「技术点网」语义不符"},
    ],
}

ID_ALIGN = {
    "technology_id": {
        "format_draft": "我方代理键（如 TECH-{domain_code}-{6 位序号} 或 UUID，待定）；Nebula VID = tech:{technology_id}，替换现行 tech:{名称}",
        "normalize": ["名称规范化：全半角/大小写/空白/标点", "别名表 aliases（中/英/缩写）并组", "IPC 锚点 + 文本相似度候选合并（Python）", "人工确认经全景维护页写回（A03 写回链路）"],
        "versioning": "合并/拆分保留旧 ID → 新 ID 映射（redirect），图谱与快照按 version 回放",
    },
    "domain_code": {
        "draft": "以 IPC 小类（如 H01L）为一级锚点，论文 scope/scope_zone、项目 discipline_code 经映射表挂到同一 domain_code；编码与久新共用",
        "forbidden": "禁止用产业链 INB* / dwd_industry_code 环节码冒充",
        "decision": "分类体系选型待甲方拍板（OI-C02-02）",
    },
    "doc_bridge": {
        "table": "INT-C-TECH-182",
        "doc_keys": {"patent": "dwd_patent.patent_id（同族去重用 dwd_patent_family.simple_family）", "zh_paper": "dwd_zh_paper.id", "en_paper": "dwd_en_paper.id",
                     "scholar_paper": "dwd_scholar_papers.paper_id（与论文库按 doi 去重）", "project": "dwd_zh_project.id / dwd_en_project.项目索引", "report": "dwd_zh_report.report_id"},
        "methods": ["ipc 规则（专利）", "keyword 匹配（论文/项目/报告）", "ner（久新 104 产出）"],
    },
    "org_talent": {
        "org": "专利申请人/项目承担单位只有名称 → dwd_org_base_info.org_id（国外 dwd_forg_base_info）；若 dwd_org_base_info_patent_rel 有数据优先用显式边；归一规则由 C03 定",
        "talent": "学者研究方向 fields、学者论文 → scholar_id；人名消歧由 C01 定",
        "geo": "深圳切片 = 机构 city/province（dwd_org_base_info）；中文论文无机构地理，需作者-机构关联（C01/C03）",
    },
    "jiuxin": {
        "rule": "久新 API 入参/出参使用我方 technology_id / domain_code；若久新用自有 ID，须交映射表 jx_tech_id→technology_id，D03 按命中率对账（阈值待定）",
        "status": "待确认（郭万迎主谈）",
    },
}

OPEN_ITEMS = [
    {"id": "OI-C02-01", "item": "技术点主数据持有方与全局 technology_id（我方自建 / 久新 / 甲方）", "owner": "human:李伟（结构）+ 甲方/久新", "kind": "structure_escalation + decision_needed", "blocking": "P0"},
    {"id": "OI-C02-02", "item": "技术领域分类体系选型与编码（与久新共用；TECH-P0-2 供应方未回）", "owner": "PM → 甲方", "kind": "decision_needed（客户决策清单草案）", "blocking": "P0"},
    {"id": "OI-C02-03", "item": "久新技术链 25 行交付形态 + 数据底座（用我方 gkx 入站数据还是其自有数据）", "owner": "human:郭万迎", "kind": "对端确认", "blocking": "P0"},
    {"id": "OI-C02-04", "item": "供应方 5 题未回：TECH-P0-1/P0-2/P1-1/P1-2/P1-3（2026-09-04 出题）", "owner": "human:郭万迎", "kind": "供应方回复", "blocking": "P0"},
    {"id": "OI-C02-05", "item": "专利附表（cited/legal/transfer/family/title/abstract）仅 ≈1.6–2.1 万行 vs 主表 ≈269 万，是否抽样交付", "owner": "供应方", "kind": "数据完整性", "blocking": "P1"},
    {"id": "OI-C02-06", "item": "英文论文仅 1,356 行，全球论文侧覆盖不足；是否补数或以专利为全球主口径", "owner": "供应方 / 甲方", "kind": "decision_needed", "blocking": "P1"},
    {"id": "OI-C02-07", "item": "行数 unknown 表需只读 COUNT：dwd_en_paper_cited_by / dwd_rel_project_patent / dwd_rel_project_paper / dwd_org_base_info_patent_rel / dwd_quantum_* / dwd_org_industry_chain_pat_dtl / dwd_industry_analysis_*", "owner": "data-agent（下次快照）", "kind": "核验", "blocking": "P2"},
    {"id": "OI-C02-08", "item": "DDL 沙箱（2026-07-15）与 live 列名不一致（dwd_patent 等），且缺 dwd_patent_cited/_transfer、dwd_en_project/_report、dwd_org_tech_tag", "owner": "data-agent", "kind": "沙箱刷新", "blocking": "P2"},
    {"id": "OI-C02-09", "item": "供应方各表更新频率未书面给出", "owner": "供应方", "kind": "供应方回复", "blocking": "P1"},
    {"id": "OI-C02-10", "item": "M_TECH_INVEST_AMOUNT：政府专项（项目经费）+ 社会资本（融资/投资）均无技术键，分摊规则与币种单位待定", "owner": "PM → 甲方", "kind": "decision_needed", "blocking": "P1"},
    {"id": "OI-C02-11", "item": "M_TECH_COMPOSITE_SCORE 无源（no_source）：生产方与分项未定", "owner": "algorithm-agent（B07）/ PM", "kind": "owner 未定", "blocking": "P1"},
    {"id": "OI-C02-12", "item": "PATH_CENTRALITY / KEYNODE / PRIORITY / ENTITY_INFLUENCE 是否改判我方 Python+Nebula 自研（B06），原料只能是技术点图谱", "owner": "algorithm-agent（B06）", "kind": "owner 未定", "blocking": "P1"},
    {"id": "OI-C02-13", "item": "MODEL×3（DS-07-TECH-INNOV 002/004/006）入参清单未签（等唐绍祖）；kit 只点名国内机构 dwd_org_base_info，全球申请人需 dwd_forg_base_info", "owner": "human:唐绍祖", "kind": "入参确认", "blocking": "P1"},
    {"id": "OI-C02-14", "item": "「实时」热点/监测的真实时效（默认 T+1）", "owner": "PM → 甲方", "kind": "decision_needed", "blocking": "P2"},
    {"id": "OI-C02-15", "item": "技术点论文全集口径（论文要素库 ∪ 学者论文，doi 去重）与专利同族去重口径", "owner": "PM → 甲方", "kind": "decision_needed", "blocking": "P2"},
    {"id": "OI-C02-16", "item": "TRSGraph 现有 technology 顶点/技术边数量与 VID 规则迁移（tech:{名称}→tech:{technology_id}）", "owner": "C04", "kind": "交接", "blocking": "P1"},
]


def main():
    cards = [build_card(c) for c in CARDS]
    coverage = []
    for m in sorted(COV):
        ids, binding, note = COV[m]
        coverage.append({"metric_id": m, "algorithm_type": atype(m), "source_cards": ids if ids else "no_source", "binding": binding, "note": note, "pages": PAGES[m]})
    doc = {
        "task_id": "SCI-INT-C02",
        "layer": "data",
        "element": "TECH（技术链 / 技术点）",
        "generated_by": "产物/_work/C02-build.py",
        "as_of": "2026-10-18",
        "note": "对端正名「久新」；引用旧路径 metrics/request/九新-技术机构人才/ 保留原名。指标 8 件套/D1–D4 取自 MCP metric-registry（metric-query domain=TECH fields=full，2026-10-18）；"
                "行数引用仓内快照，未连库。data_source 为本叶对 §2 schema 的扩展块（派单要求的源系统/主键/覆盖/频率/行数）。",
        "scope_count": len(cards),
        "card_count": len(cards),
        "gap": [],
        "master_data_conclusion": MASTER,
        "id_alignment_draft": ID_ALIGN,
        "metric_coverage": {
            "scope_metrics": len(COV),
            "covered": sum(1 for v in COV.values() if v[0]),
            "no_source": sum(1 for v in COV.values() if not v[0]),
            "diff": [],
            "binding_legend": {"kit_declared": "MCP kit.source_tables 点名", "candidate": "本叶据口径推断的候选原料（kit 仍 pending_ods，未核验）",
                               "jiuxin_pending": "久新交付（51 行之一，全部待确认）", "no_source": "无可识别源"},
            "items": coverage,
        },
        "open_items": OPEN_ITEMS,
        "cards": cards,
    }
    OUT.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print(f"wrote {OUT.name}: cards={len(cards)} metrics={len(COV)}")


if __name__ == "__main__":
    main()
