# -*- coding: utf-8 -*-
"""SCI-INT-C01 人才（TAL）三方源入站盘点：卡片数据 → 产物/SCI-INT-C01.yaml（总派单 §2 schema + data_source 扩展块）。
只读：不连库；行数引用仓内快照。运行：python 产物/_work/C01-build.py
"""
import pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "SCI-INT-C01.yaml"

RAW = "data/third-party-source/gkx-mysql-raw/"
R1010 = RAW + "加工/GKX数据源表及行数报告-20261010-1055-估数.MD（TABLE_ROWS 估数，未过滤 is_deleted）"
R0831 = RAW + "加工/GKX数据源表及行数报告-20260831-1559.MD（精确 COUNT；人才 8 表各 20,000 行=样例）"
P0803 = RAW + "_live_dwd_enterprise_probe_2026-08-03.json（approx_rows）"
P0810 = RAW + "_live_dwd_enterprise_probe_2026-08-10.json（approx_rows）"
P0819 = RAW + "_live_dwd_enterprise_probe_2026-08-19.json（approx_rows）"
DDL = RAW + "gkx_schema_ddl.sql（DDL 沙箱 2026-07-15）"
SRC = RAW + "SOURCE-TABLES.md"
FREQ_UNK = "unknown（供应方未书面给出；多次快照行数有增减，说明在持续加工）"
GKX_SYS = "gkx_mysql_raw（甲方三方库 MySQL gkx @183.240.141.251:3318，只读 gkx_reader_zp）"
SAMPLE_GAP = "2026-08-31 精确 COUNT 时人才 8 表各恰 20,000 行（样例），10-10 估数虽已增长，全量覆盖范围（全球/中国/深圳）供应方未书面说明"

# ---- 指标 → 页面（MCP srs_refs.page_ids ∪ metrics/request/展示系统/pages DS-13～16 mapped 行；专题指标 srs_refs 无页的记模块级） ----
TOPIC_MOD = "TOPIC-TALENT（模块级；MCP srs_refs 无 page_id）"
PAGES = {
    "M_TALENT_BASE_98_1": ["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION", "DS-26-ECO", "TOPIC-TALENT-05"],
    "M_TALENT_GRAPH_110_1": ["DS-13-TALENT-GLOBAL", "DS-15-TALENT-PROFILE", "DS-16-TALENT-RECRUIT", "TOPIC-TALENT-05"],
    "M_TALENT_GRAPH_111_1": ["DS-13-TALENT-GLOBAL", "DS-15-TALENT-PROFILE", "DS-16-TALENT-RECRUIT", "DS-26-ECO", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_156_1": ["DS-15-TALENT-PROFILE", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_157_1": ["DS-13-TALENT-GLOBAL", "DS-14-TALENT-REGION", "DS-26-ECO", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_158_1": ["TOPIC-TALENT-05"],
    "M_TALENT_DEEP_159_1": ["TOPIC-TALENT-05"],
    "M_TALENT_DEEP_160_1": ["DS-15-TALENT-PROFILE", "DS-16-TALENT-RECRUIT", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_161_1": ["TOPIC-TALENT-05"],
    "M_TALENT_DEEP_162_1": ["DS-01-FACTORS", "DS-08-VIZ", "DS-13-TALENT-GLOBAL", "DS-15-TALENT-PROFILE", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_163_1": ["DS-15-TALENT-PROFILE", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_164_1": ["DS-13-TALENT-GLOBAL", "DS-16-TALENT-RECRUIT", "TOPIC-TALENT-05"],
    "M_TALENT_DEEP_165_1": ["TOPIC-TALENT-05"],
    "M_TALENT_ACADEMIC_SCORE": [TOPIC_MOD],
    "M_TALENT_ATTRACT_SCORE": [TOPIC_MOD],
    "M_TALENT_CULTIVATE_SCORE": [TOPIC_MOD],
    "M_TALENT_INDUSTRY_SCORE": [TOPIC_MOD],
    "M_TALENT_FLOW_TRACK": [TOPIC_MOD],
    "M_TALENT_ORG_DIST": [TOPIC_MOD],
    "M_TALENT_REGIONAL_DIST": [TOPIC_MOD],
    "M_TALENT_RELATION_NET": [TOPIC_MOD],
    "M_TALENT_SUPPLY_STRUCT": [TOPIC_MOD],
    "M_TALENT_SZ_STATUS": [TOPIC_MOD],
    "M_TALENT_SZ_SUPPLY_DEMAND": [TOPIC_MOD],
    "M_TALENT_UNIV_NEW": [TOPIC_MOD],
    "M_TALENT_STRUCT_QUERY": ["TOPIC-QUERY（当次查询结果集；口径禁止消费 DS-13～16）"],
    **{f"M_TALENT_DS_16_TALENT_RECRUIT_{n}": ["DS-16-TALENT-RECRUIT"] for n in ("005", "006", "007", "010", "013", "025")},
}


def atype(mid):
    return "STAT" if mid == "M_TALENT_STRUCT_QUERY" else "third_party"


def T(n):
    return f"INT-C-TAL-{n:03d}"


# ---- 指标覆盖：metric → (源卡列表, binding, 说明) ----
# binding: kit_declared=MCP kit.source_tables 点名（本域 32 条全部 pending_ods，故为 0）；candidate=本叶据口径推断的候选原料（未核验）；
#          jiuxin_pending=久新交付（51 行之一，全部待确认）；no_source=无任何可识别源
DS16_NOTE = "A2 missing、05 算法库无专叶；JIUXIN minutes 附录明确「不向久新索要假 API」；三方库 206 张 dwd_* 无{x}数据 → 原料与生产方均未定"
COV = {
    "M_TALENT_BASE_98_1": ([T(40), T(1), T(2), T(3), T(4), T(5), T(6), T(8), T(70)], "jiuxin_pending", "久新交 SQL-98（STAT），在我方入站人才 8 表上跑；表名映射未给"),
    "M_TALENT_GRAPH_110_1": ([T(41), T(1), T(10), T(11), T(12), T(13), T(16), T(17), T(18), T(19), T(20), T(60), T(72)], "jiuxin_pending",
                             "久新 Python-110 人才实体识别/消歧：把论文作者、报告作者、发明人、项目主持人对齐到 scholar_id"),
    "M_TALENT_GRAPH_111_1": ([T(42), T(2), T(6), T(8), T(14), T(15), T(61)], "jiuxin_pending", "久新 Python-111 抽人才关系（合作/任职/项目/报告）→ Nebula"),
    "M_TALENT_DEEP_156_1": ([T(43), T(1), T(4), T(6), T(7)], "jiuxin_pending", "API-156；原料=学者指标（h_index/引用）+ 院士标记"),
    "M_TALENT_DEEP_157_1": ([T(44), T(2), T(71), T(24), T(25), T(26)], "jiuxin_pending", "API-157；流动边 DDL 无（SYNTH-P0-3），只能由任职履历派生（INT-C-TAL-071），地理需机构→区划"),
    "M_TALENT_DEEP_158_1": ([T(45), T(3), T(2), T(24)], "jiuxin_pending", "API-158；高校毕业→任职，教育背景无机构 ID"),
    "M_TALENT_DEEP_159_1": ([T(46), T(1), T(24), T(26)], "jiuxin_pending", "API-159；深圳切片须机构 city 归一"),
    "M_TALENT_DEEP_160_1": ([T(47), T(8), T(14), T(61)], "jiuxin_pending", "API-160；合作网 coauthor + 项目共参"),
    "M_TALENT_DEEP_161_1": ([T(48), T(1), T(3)], "jiuxin_pending", "API-161；供给侧有学者库，需求侧（岗位/招聘）三方库无源 → 见 OI-C01-07"),
    "M_TALENT_DEEP_162_1": ([T(49), T(6), T(7), T(1)], "jiuxin_pending", "API-162；展示 DS-08-VIZ-001 H 指数 / 004 活跃度同挂此行"),
    "M_TALENT_DEEP_163_1": ([T(50), T(19), T(20), T(22), T(23), T(14)], "jiuxin_pending", "API-163；专利发明人/项目/高管只有姓名，须经 072 映射到 scholar_id"),
    "M_TALENT_DEEP_164_1": ([T(51), T(1), T(5), T(71)], "jiuxin_pending", "API-164；需人才领域码（TALENT-P0-2）"),
    "M_TALENT_DEEP_165_1": ([T(52), T(3), T(5), T(24)], "jiuxin_pending", "API-165"),
    "M_TALENT_ACADEMIC_SCORE": ([T(49)], "jiuxin_pending", "对照 seq 162 学术力"),
    "M_TALENT_INDUSTRY_SCORE": ([T(50)], "jiuxin_pending", "对照 seq 163 产业力"),
    "M_TALENT_ATTRACT_SCORE": ([T(51)], "jiuxin_pending", "对照 seq 164 招入推荐"),
    "M_TALENT_CULTIVATE_SCORE": ([T(52)], "jiuxin_pending", "对照 seq 165 培育布局"),
    "M_TALENT_FLOW_TRACK": ([T(44), T(71), T(2)], "jiuxin_pending", "对照 seq 157；流动边待派生"),
    "M_TALENT_ORG_DIST": ([T(43), T(1), T(2), T(24)], "jiuxin_pending", "重点人才（156 产出）× 当前所属机构；scholar_org_id 为空，需名称归一（TALENT-P1-4）"),
    "M_TALENT_REGIONAL_DIST": ([T(43), T(24), T(26)], "jiuxin_pending", "重点人才 × 机构区划；学者表无地理列（TALENT-P1-5）"),
    "M_TALENT_RELATION_NET": ([T(47), T(61), T(8)], "jiuxin_pending", "对照 seq 160 关系链"),
    "M_TALENT_SUPPLY_STRUCT": ([T(48), T(3), T(1)], "jiuxin_pending", "对照 seq 161；学历有 degree，职称/年龄无列（TALENT-P1-3）"),
    "M_TALENT_SZ_STATUS": ([T(46)], "jiuxin_pending", "对照 seq 159"),
    "M_TALENT_SZ_SUPPLY_DEMAND": ([T(48), T(26)], "jiuxin_pending", "对照 seq 161 深圳切片"),
    "M_TALENT_UNIV_NEW": ([T(45), T(3)], "jiuxin_pending", "对照 seq 158"),
    "M_TALENT_STRUCT_QUERY": ([T(1), T(3)], "candidate", "我方 STAT：查询结果集内按学历/职称/年龄分箱；学历取 education_background.degree，职称/年龄三方库无列（TALENT-P1-3），只能部分覆盖"),
    "M_TALENT_DS_16_TALENT_RECRUIT_005": ([], "no_source", DS16_NOTE.format(x="语言/沟通行为")),
    "M_TALENT_DS_16_TALENT_RECRUIT_006": ([], "no_source", DS16_NOTE.format(x="文化背景/适应")),
    "M_TALENT_DS_16_TALENT_RECRUIT_007": ([], "no_source", DS16_NOTE.format(x="签证/出入境/国别政策")),
    "M_TALENT_DS_16_TALENT_RECRUIT_010": ([], "no_source", DS16_NOTE.format(x="引进阻力因子")),
    "M_TALENT_DS_16_TALENT_RECRUIT_013": ([], "no_source", DS16_NOTE.format(x="薪酬/安家/引才成本") + "；DS-16 页 316 成本数据采集为 other_system"),
    "M_TALENT_DS_16_TALENT_RECRUIT_025": ([], "no_source", DS16_NOTE.format(x="团队组成") + "；coauthor 只能给合作关系，不等于团队组合评估"),
}
assert len(COV) == 32 and set(COV) == set(PAGES)

COMMON_GAPS = ["kit.source_tables=pending_ods（D3 pending_ods），本卡对应关系为候选，未经 data-agent 正式化"]
LUMEN_NONE = "无（lumen-etl-es-py / lumen-svc-platform / lumen-ui-science-pc 未引用 dwd_scholar*）"


def gkx(nnn, table, cn, *, keys, pk, align, coverage, rows, rows_ref=R1010, as_of="2026-10-10", freq=FREQ_UNK, dims=("TAL",), dep=("data",),
        gaps=(), conflicts=(), decision=(), risks=(), esc=False, conf="medium", tests=(), lumen=LUMEN_NONE, share=None, ours=("etl",)):
    return dict(nnn=nnn, sys=GKX_SYS, table=table, cn=cn, keys=keys, pk=pk, align=align, coverage=coverage, rows=rows, rows_ref=rows_ref, as_of=as_of,
                freq=freq, dims=list(dims), dep=list(dep), gaps=list(gaps), conflicts=list(conflicts), decision=list(decision), risks=list(risks), esc=esc,
                conf=conf, tests=list(tests), lumen=lumen, share=share, counterpart="gkx_mysql_raw", form="table", jx=None, ours=list(ours))


NAME_ONLY = "只有姓名、无人员 ID：须经人名消歧（姓名中英变体 + 机构归一 + 共现）对齐到 scholar_id（INT-C-TAL-072）"
CARDS = [
    # ---- 人才要素库 8 表（来源 Excel「版权人才、企业机构、政策数据汇总表.xlsx」） ----
    gkx(1, "dwd_scholar", "人才要素库·学者基本信息",
        keys=["id", "scholar_id", "name_zh", "name_en", "scholar_org_name_zh/en（多机构分号拼接）", "scholar_department_name_zh/en", "scholar_org_id",
              "orc_id", "bio / bio_zh", "paper_nums", "citation_nums", "reference_nums", "h_index", "status", "update_time"],
        pk="scholar_id（varchar32，业务唯一；物理 id 自增）",
        align="人才实体：scholar_id 为唯一业务 ID；辅助键 orc_id、name_zh/name_en；机构：scholar_org_id 暂为空串 → 只能用 scholar_org_name_* 名称归一到 org_id（C03）",
        coverage="unknown（学者库，含中外学者；全球/中国/深圳范围供应方未说明）", rows="16,933",
        gaps=[SAMPLE_GAP, "无性别/国籍/出生年/学历层级/职称列（DS-13 257 等需求的结构维缺）", "无地理区划码、无人才领域码（TALENT-P0-2/P1-5）",
              "scholar_org_id 为空串，当前机构稳定码缺（TALENT-P1-4）", "scholar_id 稳定性（是否跨批次不变）未获书面确认（TALENT-P0-1 / SYNTH-P2-1）"],
        conflicts=["2026-08-31 报告：库侧 69 列 vs Excel 20 列；09-11 摘要称多出业务列已消失，以 live 为准"],
        decision=["人才主数据是否以 dwd_scholar.scholar_id 为准（见 master_data_conclusion）"], conf="high",
        tests=["契约：scholar_id 非空且唯一", "对账：与 Excel 20 列字段集一致", "覆盖：orc_id / scholar_org_name 非空率"],
        lumen="lumen 未接入；lumen-algo-py vendor/innov-py 有 mock ods_scholar(scholar_id) 作 INNOV 图节点（mockgen，非本表）"),
    gkx(2, "dwd_scholar_work_experience", "人才要素库·学者工作履历",
        keys=["scholar_id", "seq_no", "start_time / end_time（YYYY 或 YYYY.MM）", "is_current", "org_name_zh/en", "department", "position_zh/en"],
        pk="(scholar_id, seq_no)", align="经 scholar_id；org_name_* 只有名称，需归一到 org_id 后才能派生机构/区域流动", coverage="随 dwd_scholar",
        rows="56,295", dep=("data", "algorithm"),
        gaps=[SAMPLE_GAP, "无机构 ID 与地理列", "时间粒度混用 YYYY / YYYY.MM"],
        decision=["人才流动是否以任职履历相邻两段的机构变更派生（口径待甲方确认）"], conf="high",
        tests=["契约：同一 scholar_id 的 is_current 至多 1 条", "对账：start_time ≤ end_time"]),
    gkx(3, "dwd_scholar_education_background", "人才要素库·学者教育背景",
        keys=["scholar_id", "seq_no", "start_time / end_time", "org_name_zh/en", "degree_zh/en", "major_zh/en"], pk="(scholar_id, seq_no)",
        align="经 scholar_id；毕业院校名称需归一到高校 org_id", coverage="随 dwd_scholar", rows="42,837",
        gaps=[SAMPLE_GAP, "degree 为自由文本，学历分箱需映射表（TALENT-P1-3）", "无院校 ID"], conf="high"),
    gkx(4, "dwd_scholar_talent_flag", "人才要素库·学者人才标记", keys=["scholar_id", "academician（是否院士）"], pk="scholar_id",
        align="经 scholar_id", coverage="随 dwd_scholar", rows="16,400",
        gaps=[SAMPLE_GAP, "只有院士标记，无杰青/长江/海外高层次等人才称号", "DS-13 264 荣誉为 other_system，非本表"], conf="high"),
    gkx(5, "dwd_scholar_research_direction", "人才要素库·学者研究方向", keys=["scholar_id", "fields（longtext，中文分号分隔）"], pk="scholar_id（live 另有 id）",
        align="fields 为自由文本，需归一到技术领域码（C02 INT-C-TECH-181）", coverage="随 dwd_scholar", rows="19,466", dims=("TAL", "TECH"),
        dep=("data", "algorithm"), gaps=[SAMPLE_GAP, "非编码，领域码缺（TALENT-P0-2）"], share="C02 INT-C-TECH-119 记技术链用法；本卡为主卡"),
    gkx(6, "dwd_scholar_paper_relation", "人才要素库·学者-论文关系",
        keys=["scholar_id", "paper_id（→ dwd_scholar_papers.id）", "related_paper_id", "year", "citations", "publish_time", "publication_id"],
        pk="unknown（建议 (scholar_id, paper_id)）", align="学者↔论文显式边；学术力/活跃度原料", coverage="随 dwd_scholar", rows="887,927",
        dep=("data", "metric"), gaps=[SAMPLE_GAP + "（08-31 精确 20,000 → 10-10 估数 887,927）"],
        conflicts=["08-19 探针 approx 1,928,994 vs 10-10 估数 887,927，估数波动大，需精确 COUNT"], conf="medium"),
    gkx(7, "dwd_scholar_papers", "人才要素库·学者论文信息",
        keys=["id / paper_id", "zh_name", "en_name", "authors", "doi", "cover_date_start", "publication_en_name", "zh_abstract / en_abstract"], pk="id（paper_id）",
        align="与论文要素库 dwd_zh_paper / dwd_en_paper 无共同主键，只能 doi 对齐", coverage="全球（学者库论文）", rows="597,513", dims=("TAL", "TECH"),
        gaps=[SAMPLE_GAP, "与论文要素库可能重复计数"], share="C02 INT-C-TECH-118 记技术链用法；本卡为主卡"),
    gkx(8, "dwd_scholar_coauthor", "人才要素库·学者合作者",
        keys=["scholar_id", "co_scholar_id", "co_scholar_name", "co_scholar_org_name", "co_scholar_org_id（空）", "co_paper_count"],
        pk="(scholar_id, co_scholar_id)", align="学者↔学者合作边；co_scholar_id 是否全部落在 dwd_scholar 内未知", coverage="随 dwd_scholar",
        rows="1,028,293", dep=("data", "graph"),
        gaps=[SAMPLE_GAP, "co_scholar_org_id 为空", "co_scholar_id 在 dwd_scholar 中的命中率未核（悬挂边风险）"],
        conflicts=["行数 1,272,117（上次估数）→ 1,028,293（10-10 估数）"], tests=["对账：co_scholar_id ∈ dwd_scholar.scholar_id 命中率"]),
    # ---- 文献作者 / 关联（次级人员源，须对齐到 scholar_id） ----
    gkx(10, "dwd_zh_author", "中文论文要素库·作者信息",
        keys=["paper_id", "author_sequence", "author_id（varchar32）", "zh_name（覆盖 97.82%）", "en_name", "email", "correspond", "institution", "affiliation（json）"],
        pk="(paper_id, author_sequence)；author_id 为供应方作者 ID", align="author_id 与 scholar_id 是否同一套未知；email / 姓名+机构可作消歧辅助键",
        coverage="中国（中文期刊）", rows="63,260", dep=("data", "algorithm"),
        gaps=["author_id 与 scholar_id 映射缺（TALENT-P0-1）"], decision=["author_id 是否承诺与 scholar_id 同一 ID 空间"]),
    gkx(11, "dwd_en_author", "外文论文要素库·作者信息", keys=["paper_id", "author_sequence", "author_id", "en_name", "email", "institution", "affiliation（json）"],
        pk="(paper_id, author_sequence)", align="同 INT-C-TAL-010", coverage="全球（外文）——量极小", rows="1,367", dep=("data", "algorithm"),
        gaps=["10-10 首次计数仅 1,367 行，与英文论文 1,356 行同量级", "author_id 与 scholar_id 映射缺"], conf="medium"),
    gkx(12, "dwd_author_info + dwd_author_*_rel 族", "作者主表（Scopus 风格）及作者-论文/项目/报告/专利/机构关联",
        keys=["auid", "orcid", "姓名变体", "asjc 学科码", "current_affiliations", "author_id ↔ paper/project/report/global_patent/org_base_info/foreign_org_base_info"],
        pk="auid（dwd_author_info）；rel 表 (author_id, 目标 id)", align="auid / orcid 可作跨库消歧强键；若有数据，author_*_rel 是人才↔机构/专利的显式边",
        coverage="unknown", rows="0", rows_ref=P0803 + "：dwd_author_info 与 author_* rel 各表均为 0；结构见 " + DDL, as_of="2026-08-03",
        dep=("data",), gaps=["当前 0 行，不可用；供应方是否计划灌数未知", "10-10 行数报告未覆盖本族，需只读 COUNT 复核"],
        decision=["若供应方灌数，auid/orcid 是否作为 scholar 对齐强键"], conf="low"),
    gkx(13, "dwd_author_affiliation", "作者-机构归属（含地理）", keys=["auid", "affiliation_id", "city", "state", "country", "country_tag"],
        pk="(auid, affiliation_id)", align="唯一带 city/country 的人员归属表；auid→scholar_id 映射缺", coverage="unknown", rows="1,619", rows_ref=P0810,
        as_of="2026-08-10", dep=("data",), gaps=["行数小且为 08-10 探针 approx；auid 体系与 scholar_id 无对应"], conf="low"),
    gkx(14, "dwd_rel_project_scholar", "项目-学者关联（算法绑定后的学者 ID）", keys=["project_source", "project_id", "scholar_id"], pk="pk_id",
        align="DDL 注释「算法绑定后的学者ID」→ 直接是 scholar_id，项目主持/参与人已消歧", coverage="unknown", rows="unknown",
        rows_ref="不在 20 要素库行数报告与 08 月探针覆盖内；结构见 " + DDL + " 与 " + SRC, as_of=None, dep=("data", "graph"),
        gaps=["行数 unknown，需只读 COUNT", "「算法绑定」由谁执行、口径未知（SYNTH-P2-1）"], conf="low"),
    gkx(15, "dwd_rel_report_scholar", "报告-学者关联（算法绑定后的学者 ID）", keys=["report_source", "report_id", "scholar_id"], pk="pk_id",
        align="同 INT-C-TAL-014", coverage="unknown", rows="unknown", rows_ref="不在 20 要素库行数报告与 08 月探针覆盖内；结构见 " + DDL, as_of=None,
        dep=("data", "graph"), gaps=["行数 unknown，需只读 COUNT"], conf="low"),
    gkx(16, "dwd_zh_report_scholar", "中文报告-学者关联", keys=["report_id", "scholar_id / 作者姓名（结构本叶未逐列核）"], pk="unknown",
        align="报告作者→学者", coverage="中国", rows="1,956", rows_ref=P0810, as_of="2026-08-10", dep=("data",),
        gaps=["结构未逐列核实；与 dwd_rel_report_scholar 是否重复未知"], conf="low"),
    gkx(17, "dwd_zh_report_author", "中文报告要素库·作者", keys=["report_id", "author_id", "author_name", "author_unit"], pk="unknown",
        align="author_id 与 scholar_id 映射缺；author_unit 名称需机构归一", coverage="中国（国自然与部分智库）", rows="4,092", dep=("data", "algorithm"),
        gaps=["作者覆盖率 0.55，仅国自然与部分智库报告有作者"]),
    gkx(18, "dwd_en_report_author", "外文报告要素库·作者", keys=["report_id", "authors_id", "authors_name", "authors_unit"], pk="unknown",
        align="同 INT-C-TAL-017", coverage="全球（外文）", rows="18,961", dep=("data", "algorithm"), gaps=["authors_id 与 scholar_id 映射缺"], conf="low"),
    gkx(19, "dwd_patent（inventors 列）", "全球专利要素库·专利发明人", keys=["patent_id", "inventors.sequence", "inventors.name", "first_inventor_name", "applicants"],
        pk="patent_id", align=NAME_ONLY, coverage="全球", rows="2,690,167", dims=("TAL", "TECH"), dep=("data", "algorithm"),
        gaps=["发明人无 ID，消歧成本高、误合并风险大"], share="C02 INT-C-TECH-100 为主卡；本卡只记发明人用法", conf="medium"),
    gkx(20, "dwd_zh_project（project_host / participants）", "国内项目要素库·项目主持人/参与人",
        keys=["id", "project_host", "participants（json 姓名）", "funded_institution", "funded_province", "discipline_code", "approval_year"],
        pk="pk_id（业务 id）", align=NAME_ONLY + "；若 dwd_rel_project_scholar 有数据优先用显式边", coverage="中国（funded_province 省级）", rows="46,455",
        dims=("TAL", "TECH"), dep=("data", "algorithm"), share="C02 INT-C-TECH-120 为主卡；本卡只记人员用法"),
    gkx(21, "dwd_quantum_frontier_talent", "量子专题·前沿人才", keys=["person_name", "organization_name", "research_direction"], pk="unknown（无稳定人员 ID）",
        align="只有姓名+机构名", coverage="量子专题切片", rows="unknown",
        rows_ref=SRC + " 有此表；10-10 报告对应 ods_quantum_frontier_talent 为「库中无此表」", as_of=None,
        gaps=["dwd 行数 unknown；ods 侧库中无表", "领域切片，不可作全域人才主数据"], conf="low"),
    gkx(22, "dwd_org_executive_info", "国内机构要素库·高管信息", keys=["org_id", "高管姓名", "职务"], pk="unknown（本叶未逐列核）",
        align=NAME_ONLY + "；org_id 现成", coverage="中国（企业/机构高管）", rows="385,630", dims=("TAL", "ORG"),
        gaps=["高管是否计入「人才」口径未定（企业不算 ORG，但人员维边界未定）"], decision=["企业高管是否纳入人才产业力/人才库口径"], conf="low"),
    gkx(23, "dwd_forg_executive_info", "国外机构要素库·高管信息", keys=["org_id", "高管姓名", "职务"], pk="unknown", align="同 INT-C-TAL-022",
        coverage="全球（国外机构）", rows="19,920", dims=("TAL", "ORG"), gaps=["同 INT-C-TAL-022"], conf="low"),
    gkx(24, "dwd_org_base_info", "国内机构要素库·机构基本信息（人才所属机构归一 + 深圳切片）",
        keys=["org_id", "name_cn", "external_id（统一社会信用代码）", "city", "province", "reg_status"], pk="org_id",
        align="scholar_org_name / work_experience.org_name / education.org_name → org_id（归一规则归 C03）；city/province 提供区域/深圳切片",
        coverage="中国", rows="192,464", dims=("TAL", "ORG"), share="C03 主卡；本卡只记人才用法", gaps=["高校/科研院所在本表的覆盖率未核"]),
    gkx(25, "dwd_forg_base_info", "国外机构要素库·机构基本信息（海外任职/流入流出）", keys=["org_id", "name_en", "country"], pk="org_id",
        align="海外机构名称归一", coverage="全球（国外）", rows="19,549", dims=("TAL", "ORG"), share="C03 主卡", conf="low"),
    dict(nnn=26, sys="我方项目维表（ddl/，非三方库）", table="dim_code_region / dim_code_country / dim_region_scope(_g20)", cn="地理区划与国家维表",
         keys=["region_code", "region_name", "parent_code", "level", "country_code"], pk="region_code / country_code",
         align="机构 city/province/country → 区划码；人才区域分布/流动经机构二跳", coverage="中国区划 + 国家", rows="unknown",
         rows_ref="agent-delivery/data/ddl/（仅 DDL，本叶未查行数）", as_of=None, freq="版本化，低频", dims=["TAL", "ORG"], dep=["data"],
         gaps=["人才本身无地理码，只能经机构归属推（TALENT-P1-5）"], conflicts=[], decision=[], risks=["多机构任职时区域归属规则未定"], esc=False, conf="medium",
         tests=[], lumen="无", share="C03 共用", counterpart="none", form="table", jx=None, ours=["etl"]),
]

# ---- 久新人才 15 行（JIUXIN-TECH-ORG-TALENT-L01 对人主表；全部待确认） ----
JX_COMMON_GAP = ["久新交付形态与数据底座一律待确认（JIUXIN 清单 51 行 0 确认；minutes 2026-08-24 会前清单，尚未开会）",
                 "返回人才 ID 是否为 scholar_id 未知（见 id_alignment_draft.jiuxin）"]


def jx(nnn, name, rows_ids, form, note, dep, out_fields, fresh="unknown", extra_gaps=(), decision=(), esc=False):
    return dict(nnn=nnn, sys="北京久新（对端；交付待确认）", table=name, cn=name, keys=out_fields, pk="unknown（建议 scholar_id + as_of + version）",
                align="入参/出参须用 scholar_id；若用久新自有人才 ID 须附映射表", coverage="unknown（久新数据底座未知）", rows="unknown", rows_ref="对端交付物，无快照",
                as_of=None, freq=fresh, dims=["TAL"], dep=list(dep), gaps=JX_COMMON_GAP + list(extra_gaps), conflicts=[], decision=list(decision),
                risks=["久新若以其自有人才库计算，结果与我方入站 dwd_scholar 不同源，下钻/对账断裂"], esc=esc, conf="low", tests=[],
                lumen="无（lumen-algo-py 无 /internal/jiuxin/* 适配层）", share=note, counterpart="jiuxin", form=form, jx=rows_ids,
                ours=["python_internal", "etl"])


CARDS += [
    jx(40, "久新 SQL-98 人才基础指标模型", ["SRS-98"], "SQL", "人才计数/占比/排名", ["data", "metric"],
       ["scholar_id / 分组键", "talent_cnt", "share", "rank", "as_of"], fresh="T+1（由我方调度，草案）",
       extra_gaps=["SQL 须能在我方入站 dwd_scholar* / 项目 DWD 上运行；表名映射未给"]),
    jx(41, "久新 Python-110 人才实体识别产出（人才实体集 + 消歧映射）", ["SRS-110"], "Python", "人才主数据底稿 / 作者→scholar_id 映射候选生产者",
       ["scholar_id", "name_variants", "org_id", "source_person_refs（author_id/auid/inventor/host）", "confidence"], ["data", "algorithm", "graph"],
       fresh="offline（离线 Job，频率待定）", extra_gaps=["脚本输入/依赖未知；须并入 lumen-algo-py 离线 Job，依赖不得超出仓栈"], esc=True,
       decision=["110 消歧产出是否作为我方人才 ID 映射表（INT-C-TAL-072）的正式来源"]),
    jx(42, "久新 Python-111 人才关系抽取产出（合作/任职/项目/报告边）", ["SRS-111"], "Python", "人才图谱边", ["data", "algorithm", "graph"],
       ["src_scholar_id", "dst_id", "dst_type", "rel_type", "weight", "evidence"], fresh="offline", extra_gaps=["关系类型枚举未知；写 Nebula 的 edge 清单归 C04"], esc=True),
    jx(43, "久新 API-156 重点人才识别结果集", ["SRS-156"], "API", "重点人才名单（ORG_DIST / REGIONAL_DIST 的分母口径）", ["data", "metric"],
       ["scholar_id", "is_key", "score", "reasons", "as_of"], decision=["「重点人才」判定口径（Q-MO-TALENT-01 相关）"]),
    jx(44, "久新 API-157 人才流动追踪结果集", ["SRS-157"], "API", "流动轨迹/流入流出", ["data", "metric"],
       ["scholar_id", "from_org_id", "to_org_id", "from_region", "to_region", "year", "as_of"], extra_gaps=["三方库无流动边（TALENT-P1-2 / SYNTH-P0-3）"]),
    jx(45, "久新 API-158 高校学院新培育人才结果集", ["SRS-158"], "API", "高校/学院维新培育人才", ["data", "metric"], ["univ_org_id", "college", "new_talent_cnt", "as_of"]),
    jx(46, "久新 API-159 深圳重点人才优势短板结果集", ["SRS-159"], "API", "深圳优势/短板", ["data", "metric"], ["domain_code", "strength / weakness", "score", "as_of"],
       extra_gaps=["依赖人才领域码（TALENT-P0-2）"]),
    jx(47, "久新 API-160 人才关系链结果集", ["SRS-160"], "API", "关系链子图", ["data", "metric", "graph"], ["scholar_id", "nodes[]", "edges[]", "as_of"]),
    jx(48, "久新 API-161 人才供需分析评价结果集", ["SRS-161"], "API", "供给/需求/缺口", ["data", "metric"], ["domain_code", "region_code", "supply", "demand", "gap", "as_of"],
       extra_gaps=["需求侧原料（岗位/招聘）三方库无"]),
    jx(49, "久新 API-162 人才学术力评估结果集（含展示 DS-08-VIZ-001/004）", ["SRS-162", "DS-08-VIZ-001", "DS-08-VIZ-004"], "API", "学术力 / H 指数排行 / 活跃度",
       ["metric", "data"], ["scholar_id", "academic_score", "h_index", "activity", "as_of"],
       decision=["H 指数直接取 dwd_scholar.h_index（我方 STAT）还是久新模型产出"]),
    jx(50, "久新 API-163 人才产业力评估结果集", ["SRS-163"], "API", "产业力", ["data", "metric"], ["scholar_id", "industry_score", "dims", "as_of"]),
    jx(51, "久新 API-164 招入人才推荐结果集", ["SRS-164"], "API", "招入推荐名单", ["data", "metric"], ["scholar_id", "recommend_rank", "reasons", "as_of"],
       extra_gaps=["推荐对象含海外人才，涉及个人信息出境/展示的脱敏口径未定"]),
    jx(52, "久新 API-165 培育人才布局结果集", ["SRS-165"], "API", "培育布局", ["data", "metric"], ["domain_code", "org_id", "layout_score", "as_of"]),
]

# ---- TRSGraph 与我方待建结构 ----
CARDS += [
    dict(nnn=60, sys="trsgraph（NebulaGraph TRSGraph graphd 10.50.75.136:9669）", table="TAG scholar / person（人才顶点）", cn="Nebula 人才顶点",
         keys=["vid", "name", "org", "props"], pk="VID 规则 unknown（SYNTH 协同图草案用 scholar_id）", align="VID 须为稳定 scholar_id", coverage="unknown", rows="unknown",
         rows_ref="本叶未连 Nebula；live 点数由 C04 核", as_of=None, freq="unknown", dims=["TAL"], dep=["graph"],
         gaps=["live 是否已有人才顶点、数量与 VID 规则 unknown（C04）"], conflicts=[], decision=[], risks=["若用姓名作 VID，同名合并错误会污染关系链"], esc=True,
         conf="low", tests=["图谱一致性：人才顶点数 = 人才主档行数"], lumen="无", share=None, counterpart="trsgraph", form="table", jx=None, ours=["graph_load"]),
    dict(nnn=61, sys="trsgraph（NebulaGraph TRSGraph）", table="人才相关 EDGE（合作 / 任职 / 毕业 / 项目共参 / 流动）", cn="Nebula 人才边",
         keys=["src_vid", "dst_vid", "rel_type", "weight", "start_year / end_year"], pk="(src, dst, rank)", align="端点 scholar_id / org_id", coverage="unknown",
         rows="unknown", rows_ref="本叶未连 Nebula；C04 核", as_of=None, freq="unknown", dims=["TAL", "ORG"], dep=["graph"],
         gaps=["边类型清单未在 schema 落地", "机构端点依赖 C03 org_id 归一"], conflicts=[], decision=[], risks=[], esc=True, conf="low", tests=[], lumen="无",
         share=None, counterpart="trsgraph", form="table", jx=None, ours=["graph_load"]),
    dict(nnn=70, sys="我方项目自建（待建）", table="人才主档（建议 dwd/ads talent_master，名待定）", cn="人才主数据",
         keys=["scholar_id", "name_zh", "name_en", "orc_id", "current_org_id", "region_code", "domain_code[]", "degree_level", "title_level", "is_key", "version"],
         pk="scholar_id（沿用三方 scholar_id；稳定性待确认）", align="全部人才维数据的对齐锚点；Nebula VID 用 scholar_id",
         coverage="随 dwd_scholar", rows="0（不存在）", rows_ref="本叶检索 data/、ddl/、lumen-etl-es-py、lumen-svc-platform 均无人才表", as_of=None,
         freq="T+1（随入站，草案）", dims=["TAL"], dep=["data", "graph"], gaps=["表不存在", "region/domain/学历/职称维须补齐（三方库无列）"], conflicts=[],
         decision=["人才主数据持有方（三方 scholar_id 直用 / 我方代理键 / 久新）"], risks=[], esc=True, conf="medium",
         tests=["契约：scholar_id 唯一；current_org_id 命中 org 主数据率"], lumen="无", share=None, counterpart="none", form="none", jx=None, ours=["etl"]),
    dict(nnn=71, sys="我方项目自建（待建，派生）", table="人才流动/任职变迁边表（建议 dwd talent_flow，名待定）", cn="人才流动边",
         keys=["scholar_id", "from_org_id", "to_org_id", "from_region_code", "to_region_code", "move_year", "method（work_exp_diff|jx157）"],
         pk="(scholar_id, move_year, from_org_id, to_org_id)", align="由 work_experience 相邻段机构变更派生，机构经 C03 归一、区划经 026",
         coverage="随 dwd_scholar", rows="0（不存在）", rows_ref="三方 DDL 无流动边（SYNTH-P0-3 / TALENT-P1-2）", as_of=None, freq="T+1（草案）",
         dims=["TAL", "ORG"], dep=["data", "algorithm"], gaps=["表不存在", "履历时间粒度混用"], conflicts=[], decision=["流动口径：机构变更 / 城市变更 / 国别变更"],
         risks=["机构名归一失败会产生伪流动"], esc=True, conf="medium", tests=["对账：派生流动数 vs 久新 157 产出抽样"], lumen="无", share=None,
         counterpart="none", form="none", jx=None, ours=["etl", "python_internal"]),
    dict(nnn=72, sys="我方项目自建（待建）", table="人员 ID 映射表（建议 dwd person_id_map，名待定）", cn="次级人员源 → scholar_id 映射",
         keys=["src_system", "src_person_key（author_id|auid|inventor_name+patent_id|project_host+project_id|exec_name+org_id）", "scholar_id", "method", "confidence", "version"],
         pk="(src_system, src_person_key, version)", align="人名消歧结果落表；来源=久新 110 或我方 Python 规则", coverage="随各次级源", rows="0（不存在）",
         rows_ref="同 INT-C-TAL-070", as_of=None, freq="随 110 Job", dims=["TAL"], dep=["data", "algorithm"], gaps=["表不存在"], conflicts=[],
         decision=["消歧置信度阈值与人工复核流程"], risks=["同名异人误合并（中文姓名高频）"], esc=True, conf="medium",
         tests=["对账：已知 scholar（rel_project_scholar 显式边）回测命中率"], lumen="无", share=None, counterpart="none", form="none", jx=None,
         ours=["etl", "python_internal"]),
]


def metrics_of(card_id):
    return sorted(m for m, (ids, _, _) in COV.items() if card_id in ids)


def pages_of(mids):
    return sorted({p for m in mids for p in PAGES[m]})


def build_card(c):
    cid = T(c["nnn"])
    mids = metrics_of(cid)
    is_gkx = c["counterpart"] == "gkx_mysql_raw"
    downstream = {
        "gkx_mysql_raw": f"gkx.{c['table']} → 项目 DWD（data 层 ETL）→ ADS / ES（C05）/ Nebula（C04）",
        "jiuxin": "久新 " + c["form"] + "（待确认）→ Python 适配/Job → 结果快照 ADS（metric_id + as_of + version）",
        "trsgraph": "Nebula TRSGraph space（C04 定）",
        "none": "项目 DWD / ADS（新表或我方维表）",
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
                       else "POST /internal/jiuxin/talent/*（draft，适配层归 B01 模式）"),
            "downstream": downstream,
        },
        "contract_draft": {
            "request": ([] if c["counterpart"] != "jiuxin" else ["scholar_id", "org_id", "region_code", "domain_code", "time_range", "as_of"]),
            "response_key_fields": c["keys"],
            "granularity": {"time": "year（履历 start/end、论文 year）" if is_gkx else "unknown",
                            "geo": "经机构归属：country / province / city（深圳切片）" if is_gkx else "unknown"},
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
            "rows": {"value": c["rows"], "as_of": c["as_of"], "ref": c["rows_ref"]},
            "pages": pages_of(mids),
            "shared_with": c["share"],
        },
        "status": {
            "demo": "demo-* 人才页（DS-13～16 / 专题人才）为 Mock，未以 dwd_scholar* 接入（未逐页核）",
            "lumen": c["lumen"],
            "d1_d4": {"d1": "draft", "d4": "mock"} if mids else None,
        },
        "gaps": (COMMON_GAPS if mids else []) + c["gaps"],
        "conflicts": c["conflicts"],
        "decision_needed": c["decision"],
        "structure_escalation": c["esc"],
        "risks": c["risks"],
        "test_points": c["tests"] or ["契约：关键字段非空率/主键唯一", "降级：源缺失时页面空态 + 角标，不填 0"],
        "confidence": c["conf"],
    }


MASTER = {
    "conclusion": "人才实体主数据候选 = 甲方三方库 gkx 人才要素库 dwd_scholar.scholar_id（INT-C-TAL-001）：它是三方库中唯一同时具备稳定业务 ID、履历、教育、研究方向、论文、合作者的人员表，"
                  "且 dwd_rel_project_scholar / dwd_rel_report_scholar 已用「算法绑定后的 scholar_id」挂接。草案：我方人才主档（INT-C-TAL-070）沿用 scholar_id 作主键，"
                  "论文/报告作者 author_id、Scopus auid、专利发明人、项目主持人、机构高管等次级人员源一律经人员 ID 映射表（INT-C-TAL-072）对齐到 scholar_id；久新接口以 scholar_id 交互。",
    "status": "待确认（scholar_id 稳定性与全量覆盖未获书面确认；新建主档/映射/流动边为结构项 → structure_escalation，升级 human:李伟）",
    "evidence": [
        "SOURCE-TABLES.md + 2026-10-10 行数报告：人才要素库 8 表（dwd_scholar 16,933 / work_experience 56,295 / education 42,837 / talent_flag 16,400 / research_direction 19,466 / paper_relation 887,927 / papers 597,513 / coauthor 1,028,293，TABLE_ROWS 估数）",
        "2026-08-31 精确 COUNT：人才 8 表各恰 20,000 行（样例）→ 全量范围未知",
        "DDL：dwd_rel_project_scholar / dwd_rel_report_scholar 注释「算法绑定后的学者ID」",
        "dwd_author_info 及 author_*_rel 族 08-03 探针为 0 行；dwd_zh_author/en_author/report_author 只有供应方 author_id 或姓名；专利发明人、项目主持人只有姓名",
        "TALENT-SUPPLIER-QUESTIONS（DATA-SUPPLIER-Q-TALENT-L01，2026-09-04 现行 7 题）：TALENT-P0-1 人才库主键稳定性、P0-2 领域码、P1-2 流动边、P1-3 分箱键、P1-4 机构码、P1-5 区划码均待供应方回复",
        "SYNTH-SUPPLIER-QUESTIONS：SYNTH-P2-1 rel_project_scholar.scholar_id 是否与人才库主键同一套；SYNTH-P0-3 DDL 无人才流动边",
        "lumen-* 未接入任何 dwd_scholar*；lumen-algo-py vendor/innov-py 仅有 mock ods_scholar",
    ],
    "candidates": [
        {"option": "A 沿用三方 scholar_id 作人才主键（推荐草案）", "pros": "已有履历/论文/合作/项目报告绑定，零重编码",
         "cons": "主键稳定性依赖供应方；样例规模，全量未知；缺地理/领域/机构码需我方补维"},
        {"option": "B 我方代理键 talent_id + scholar_id 映射", "pros": "不受供应方 ID 变更影响", "cons": "多一层映射；图谱/ES/ADS 均需改用代理键"},
        {"option": "C 久新持有人才主数据（110 产出）、我方存映射", "pros": "我方工作量小", "cons": "主数据在对端，与入站数据不同源，违背 Java 只读 ADS 闭环"},
    ],
}

ID_ALIGN = {
    "scholar_id": {
        "primary": "dwd_scholar.scholar_id（varchar32）；Nebula 人才 VID = scholar_id（C04 定前缀）",
        "strong_aux_keys": ["orc_id / ORCID（dwd_scholar.orc_id、dwd_author_info.orcid）", "email（dwd_zh_author / dwd_en_author）", "Scopus auid（dwd_author_info，当前 0 行）"],
        "versioning": "合并/拆分保留旧 ID → 新 ID 映射，快照按 version 回放（同 C02 规则）",
    },
    "person_disambiguation": {
        "table": "INT-C-TAL-072",
        "steps": [
            "强键直连：orc_id / email / auid 精确匹配",
            "显式边优先：dwd_rel_project_scholar / dwd_rel_report_scholar（已绑定 scholar_id）",
            "姓名规范化：中文全半角/空白，英文姓名 First/Last 顺序与缩写变体（name_zh / name_en）",
            "姓名 + 机构归一后 org_id + 共现（DOI 论文共作、项目共参）打分合并",
            "低置信度进人工复核（不自动合并）",
        ],
        "sources": {"zh_paper": "dwd_zh_author.author_id", "en_paper": "dwd_en_author.author_id", "zh_report": "dwd_zh_report_author.author_id",
                    "en_report": "dwd_en_report_author.authors_id", "patent": "dwd_patent.inventors.name + patent_id", "project": "dwd_zh_project.project_host / participants + id",
                    "executive": "dwd_org_executive_info 姓名 + org_id"},
        "decision": "置信度阈值、是否允许跨语言自动合并 → decision_needed（OI-C01-05）",
    },
    "org_normalize": {
        "rule": "scholar_org_name_*（分号拼接多机构）/ work_experience.org_name_* / education.org_name_* → dwd_org_base_info.org_id（国外 dwd_forg_base_info）；规则与别名表归 C03",
        "multi_org": "多机构任职时「当前所属机构」取 is_current=1 的履历段，仍多条时规则待定",
    },
    "geo": "人才无地理列：区域/深圳切片 = 机构 org_id → city/province/country → dim_code_region / dim_code_country（INT-C-TAL-026）",
    "domain": "研究方向 fields 自由文本 → 共用 C02 技术领域维表（INT-C-TECH-181）的 domain_code；禁止用产业链 INB* 冒充（TALENT-P0-2）",
    "jiuxin": {"rule": "久新 SQL/脚本/API 入参出参统一 scholar_id / org_id / domain_code；若久新用自有人才 ID，须交映射表 jx_person_id→scholar_id，D03 按命中率对账（阈值待定）",
               "status": "待确认（郭万迎主谈）"},
    "privacy": "人才为自然人：email、个人履历、头像属个人信息，入 ADS 与展示前需字段分级与脱敏（架构级初稿 §3），口径 decision_needed（OI-C01-08）",
}

OPEN_ITEMS = [
    {"id": "OI-C01-01", "item": "人才主数据持有方与 scholar_id 稳定性（TALENT-P0-1 / SYNTH-P2-1）；新建人才主档 / 人员 ID 映射 / 流动边三张结构", "owner": "human:李伟（结构）+ 供应方/久新",
     "kind": "structure_escalation + 供应方回复", "blocking": "P0"},
    {"id": "OI-C01-02", "item": "人才要素库全量覆盖范围：08-31 各表恰 20,000 行为样例，10-10 已增长但全球/中国/深圳范围与目标规模未书面说明", "owner": "human:郭万迎 → 供应方",
     "kind": "数据完整性", "blocking": "P0"},
    {"id": "OI-C01-03", "item": "久新人才 15 行（SRS-98/110/111/156–165 + DS-08-VIZ-001/004）交付形态与数据底座（用我方入站 dwd_scholar 还是其自有人才库）", "owner": "human:郭万迎",
     "kind": "对端确认", "blocking": "P0"},
    {"id": "OI-C01-04", "item": "供应方人才 7 题未回：TALENT-P0-1/P0-2/P1-1/P1-2/P1-3/P1-4/P1-5（2026-09-04 现行，只引用不改）", "owner": "human:郭万迎（监管 DATA-SUPPLIER-Q-TALENT-L01）",
     "kind": "供应方回复", "blocking": "P0"},
    {"id": "OI-C01-05", "item": "人名消歧规则：置信度阈值、跨语言自动合并、人工复核流程；作者/发明人/主持人/高管归入 scholar_id 的口径", "owner": "PM → 甲方 / algorithm-agent",
     "kind": "decision_needed", "blocking": "P1"},
    {"id": "OI-C01-06", "item": "DS-16 六条 no_source（005/006/007/010/013/025）：库无专叶、三方无原料，是否保留功能、降级或由甲方提供数据", "owner": "PM → 甲方",
     "kind": "decision_needed（客户决策清单草案）", "blocking": "P1"},
    {"id": "OI-C01-07", "item": "人才供需（161 / SUPPLY_STRUCT / SZ_SUPPLY_DEMAND）需求侧原料（岗位/招聘）三方库无源", "owner": "PM → 甲方 / 久新",
     "kind": "源缺口", "blocking": "P1"},
    {"id": "OI-C01-08", "item": "个人信息字段分级与脱敏（email/履历/头像；招入推荐涉海外人才）", "owner": "architect + PM → 甲方", "kind": "decision_needed", "blocking": "P1"},
    {"id": "OI-C01-09", "item": "人才结构维缺列：性别/国籍/出生年/职称/学历层级（DS-13 257、STRUCT_QUERY、SUPPLY_STRUCT）", "owner": "供应方（TALENT-P1-3）",
     "kind": "源缺口", "blocking": "P1"},
    {"id": "OI-C01-10", "item": "「人才」口径边界：企业高管（dwd_org/forg_executive_info）、论文作者、发明人是否计入人才库/分母", "owner": "PM → 甲方",
     "kind": "decision_needed", "blocking": "P1"},
    {"id": "OI-C01-11", "item": "行数 unknown 需只读 COUNT：dwd_rel_project_scholar / dwd_rel_report_scholar / dwd_quantum_frontier_talent / dwd_author_info 族（08-03 为 0）/ dwd_zh_report_scholar 结构",
     "owner": "data-agent（下次快照）", "kind": "核验", "blocking": "P2"},
    {"id": "OI-C01-12", "item": "估数波动：paper_relation 08-19 approx 1,928,994 vs 10-10 887,927；coauthor 1,272,117 → 1,028,293；需精确 COUNT", "owner": "data-agent",
     "kind": "核验", "blocking": "P2"},
    {"id": "OI-C01-13", "item": "供应方各表更新频率未书面给出（默认 T+1 仅为草案）", "owner": "供应方", "kind": "供应方回复", "blocking": "P1"},
    {"id": "OI-C01-14", "item": "TRSGraph 现有人才顶点/边数量与 VID 规则（C04 交接）", "owner": "C04", "kind": "交接", "blocking": "P1"},
    {"id": "OI-C01-15", "item": "H 指数排行（DS-08-VIZ-001）直接用 dwd_scholar.h_index（我方 STAT）还是久新 162 模型产出", "owner": "PM / human:郭万迎", "kind": "decision_needed",
     "blocking": "P2"},
]


def main():
    cards = [build_card(c) for c in CARDS]
    coverage = [{"metric_id": m, "algorithm_type": atype(m), "source_cards": ids if ids else "no_source", "binding": b, "note": note, "pages": PAGES[m]}
                for m, (ids, b, note) in sorted(COV.items())]
    doc = {
        "task_id": "SCI-INT-C01",
        "layer": "data",
        "element": "TAL（人才）",
        "generated_by": "产物/_work/C01-build.py",
        "as_of": "2026-10-18",
        "note": "对端正名「久新」；引用旧路径 metrics/request/九新-技术机构人才/ 保留原名。指标 8 件套/D1–D4 取自 MCP metric-registry（metric-query domain=TALENT fields=full，2026-10-18）；"
                "行数引用仓内快照，未连库、未执行 SQL。data_source 为本叶对 §2 schema 的扩展块（派单要求的源系统/主键/覆盖/频率/行数）。",
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
            "binding_legend": {"kit_declared": "MCP kit.source_tables 点名（本域 32 条 kit 均 pending_ods，故无）", "candidate": "本叶据口径推断的候选原料（未核验）",
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
