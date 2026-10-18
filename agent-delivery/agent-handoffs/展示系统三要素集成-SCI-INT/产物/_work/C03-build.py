# -*- coding: utf-8 -*-
"""SCI-INT-C03 生成器：科研机构（ORG）三方源入站盘点 → 产物/SCI-INT-C03.yaml
运行：python 产物/_work/C03-build.py
指标 8 件套/D1–D4 来自 MCP metric-registry（metric-query domain=ORG fields=full，2026-10-18），此处只抄结论不读 registry 文件。
"""
import pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "SCI-INT-C03.yaml"

R1010 = "data/third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20261010-1055-估数.MD（TABLE_ROWS 估数，未过滤 is_deleted）"
R0831 = "data/third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20260831-1559.MD（精确 COUNT，is_deleted=0）"
R0911 = "data/third-party-source/gkx-mysql-raw/加工/GKX数据源表差异分析摘要-20260911.md"
GKX_SYS = "gkx_mysql_raw（甲方三方库 MySQL gkx @183.240.141.251:3318，只读 gkx_reader_zp；供应方=北京久新）"
FREQ_UNK = "unknown（供应方未书面给出；两次快照行数有增减，说明在持续加工）"
KIT_GAP = "kit.source_tables=pending_ods（D3 pending_ods），本卡对应关系为候选，未经 data-agent 正式化"

# ---------- 22 条 ORG 指标（MCP 2026-10-18）----------
STAT = {"M_ORG_PERF_QUERY"}
SRS = {  # extras.srs_refs (book, seq)
    "M_ORG_BASE_99_1": "04:60/64/65/67 · 05:99",
    "M_ORG_DEEP_149_1": "04:62 · 05:149",
    "M_ORG_DEEP_150_1": "05:150",
    "M_ORG_DEEP_151_1": "04:80/81 · 05:151",
    "M_ORG_DEEP_152_1": "04:82/83 · 05:152",
    "M_ORG_DEEP_153_1": "02:153 · 04:70/71 · 05:100/153/167",
    "M_ORG_DEEP_154_1": "04:75/76/77 · 05:154",
    "M_ORG_DEEP_155_1": "04:78/79 · 05:155",
    "M_ORG_GRAPH_114_1": "05:114",
    "M_ORG_GRAPH_115_1": "05:115",
}
D1REF = {
    "M_ORG_ATTENTION_TREND": "Q-MO-ORG-02（Q085）", "M_ORG_ATTRACT_SCORE": "Q-MO-ORG-07（Q090）",
    "M_ORG_COLLAB_CHAIN": "Q-MO-ORG-05（Q088）", "M_ORG_CULTIVATE_SCORE": "Q-MO-ORG-07（Q090）",
    "M_ORG_NEW_TREND": "Q-MO-ORG-01（Q084）", "M_ORG_PERF_QUERY": "Q-MO-QUERY-02（Q104）",
    "M_ORG_SZ_ADVANTAGE": "Q-MO-ORG-08（Q091）", "M_ORG_SZ_PAINPOINT": "Q-MO-ORG-09（Q092）",
    "M_ORG_SZ_STATUS": "Q-MO-ORG-04（Q087）", "M_ORG_TECH_LAYOUT": "Q-MO-ORG-03（Q086）",
    "M_ORG_TECH_SCORE": "Q-MO-ORG-06（Q089）",
}
PAT = {  # SCI-INT-B01 initial_mapping
    "M_ORG_DEEP_149_1": "IP-08", "M_ORG_DEEP_150_1": "IP-08", "M_ORG_DEEP_151_1": "IP-08", "M_ORG_DEEP_152_1": "IP-08",
    "M_ORG_DEEP_153_1": "IP-08", "M_ORG_DEEP_154_1": "IP-08", "M_ORG_DEEP_155_1": "IP-08", "M_ORG_BASE_99_1": "IP-06",
    "M_ORG_GRAPH_114_1": "IP-07", "M_ORG_GRAPH_115_1": "IP-07", "M_ORG_TECH_SCORE": "IP-08", "M_ORG_PERF_QUERY": "IP-01",
}
PAGES = {m: ["SRS-ORG", "TOPIC-ORG-05"] for m in SRS}
PAGES["M_ORG_BASE_99_1"] = ["DS-01-FACTORS", "SRS-ORG", "TOPIC-ORG-05"]
PAGES["M_ORG_GRAPH_114_1"] = ["SRS-ORG"]
PAGES["M_ORG_GRAPH_115_1"] = ["SRS-ORG"]
for m in ("M_ORG_ATTENTION_TREND", "M_ORG_ATTRACT_SCORE", "M_ORG_COLLAB_CHAIN", "M_ORG_CULTIVATE_SCORE", "M_ORG_INDUSTRY_COVER",
          "M_ORG_NEW_TREND", "M_ORG_SZ_ADVANTAGE", "M_ORG_SZ_PAINPOINT", "M_ORG_SZ_STATUS", "M_ORG_TECH_LAYOUT", "M_ORG_TECH_SCORE"):
    PAGES[m] = ["TOPIC-ORG-05"]
PAGES["M_ORG_PERF_QUERY"] = ["TOPIC-QUERY"]

# metric → (source cards, binding, note)
C = lambda *n: [f"INT-C-ORG-{x}" for x in n]
COV = {
    "M_ORG_BASE_99_1": (C(250, 200, 201, 202, 203, 205, 206, 212, 215, 218, 222, 240), "jiuxin_pending",
                        "久新交 SQL-99（待确认），在我方库跑；原料=机构名录 + 论文/专利/项目计数，须经机构主数据与文献-机构桥接"),
    "M_ORG_GRAPH_114_1": (C(251, 200, 201, 204, 205, 206, 211, 213, 215, 218, 219, 220, 221, 230, 241), "jiuxin_pending",
                          "久新交 Python-114（待确认）并入 lumen-algo-py；输入=各表机构名称文本，输出须落我方 org_id"),
    "M_ORG_GRAPH_115_1": (C(252, 210, 211, 215, 216, 218, 230, 242), "jiuxin_pending",
                          "久新交 Python-115（待确认）；机构-机构/机构-文献关系，落 TRSGraph（C04）"),
    "M_ORG_DEEP_149_1": (C(253, 211, 212, 215, 218, 223, 242), "jiuxin_pending", "API-149；技术领域分类码见 ORG-P0-3 / C02 OI-C02-02"),
    "M_ORG_DEEP_150_1": (C(254, 200, 201, 212, 215, 218), "jiuxin_pending", "API-150；成立时间仅 research_institute.incorporation_date；专题 RORG-017 产品走 CMS"),
    "M_ORG_DEEP_151_1": (C(255, 200, 201, 207, 212, 215, 218, 222), "jiuxin_pending", "API-151；成果/经费/人才三维（Q091 默认）"),
    "M_ORG_DEEP_152_1": (C(256, 207, 217, 218, 222, 223), "jiuxin_pending", "API-152；项目/转化/人才/产业合作四维（Q092 默认）"),
    "M_ORG_DEEP_153_1": (C(257, 210, 211, 215, 218, 230, 242), "jiuxin_pending", "API-153；合作边原料只有名称（ORG-P1-5）"),
    "M_ORG_DEEP_154_1": (C(258, 200, 201, 205, 206, 207, 208, 209, 212, 214, 215), "jiuxin_pending", "API-154；学术影响力/科技成果/团队实力"),
    "M_ORG_DEEP_155_1": (C(259, 200, 201, 207, 208, 215, 218, 222), "jiuxin_pending", "API-155；成果/经费效率/人才结构"),
    "M_ORG_ATTENTION_TREND": (C(250, 200, 201, 240), "jiuxin_pending", "B01 IP-09 派生自 SRS-99（TOPIC-RORG-006）；新增判定依赖名录首次入库时间"),
    "M_ORG_ATTRACT_SCORE": (C(258), "jiuxin_pending", "B01 IP-09 派生自 SRS-154（TOPIC-RORG-013）；lumen-algo-py 同名端点口径关系 unknown（B01 C9）"),
    "M_ORG_COLLAB_CHAIN": (C(257, 210, 230, 242), "jiuxin_pending", "B01 IP-09 派生自 SRS-153（TOPIC-RORG-010）；图在 TRSGraph"),
    "M_ORG_CULTIVATE_SCORE": (C(259), "jiuxin_pending", "B01 IP-09 派生自 SRS-155（TOPIC-RORG-014）；lumen-algo-py 同名端点（B01 C9）"),
    "M_ORG_INDUSTRY_COVER": (C(250, 223, 240), "jiuxin_pending",
                             "B01 IP-09 派生自 SRS-99（TOPIC-RORG-002）；科研机构↔产业链无直接边，只能经 credit_code 碰 dwd_org_industry_tags（企业为主，命中率 unknown）"),
    "M_ORG_NEW_TREND": (C(250, 200, 201, 240), "jiuxin_pending", "B01 IP-09 派生自 SRS-99（TOPIC-RORG-005）"),
    "M_ORG_PERF_QUERY": (C(240, 242, 200, 201, 211, 212, 214), "candidate",
                         "STAT 自建（IP-01）：结果集内关联论文数（Q104 默认）；依赖机构主数据 + 文献-机构桥接，不在久新 51 行"),
    "M_ORG_SZ_ADVANTAGE": (C(255), "jiuxin_pending", "B01 IP-09 派生自 SRS-151（TOPIC-RORG-015）"),
    "M_ORG_SZ_PAINPOINT": (C(256), "jiuxin_pending", "B01 IP-09 派生自 SRS-152（TOPIC-RORG-016）"),
    "M_ORG_SZ_STATUS": (C(250, 222), "jiuxin_pending", "B01 IP-09 派生自 SRS-99（TOPIC-RORG-008）；深圳圈定见 ORG-P1-4"),
    "M_ORG_TECH_LAYOUT": (C(253, 242), "jiuxin_pending", "B01 IP-09 派生自 SRS-149（TOPIC-RORG-003）"),
    "M_ORG_TECH_SCORE": (C(260, 242), "jiuxin_pending", "久新无专叶行 TOPIC-RORG-012（待确认）；禁止用 M_SVC_ORG_TECH_SCORE 顶替"),
}
assert len(COV) == 22


def gkx(nnn, table, cn, *, keys, pk, align, coverage, rows, rows_as_of="2026-10-10", rows_ref=R1010, freq=FREQ_UNK,
        gaps=(), conflicts=(), decision=(), risks=(), conf="medium", tests=(), share=None, lumen="无（lumen-etl-es-py / lumen-svc-platform 未读该表）"):
    return dict(nnn=nnn, counterpart="gkx_mysql_raw", sys=GKX_SYS, table=table, cn=cn, keys=list(keys), pk=pk, align=align,
                coverage=coverage, rows=rows, rows_as_of=rows_as_of, rows_ref=rows_ref, freq=freq, gaps=[KIT_GAP] + list(gaps),
                conflicts=list(conflicts), decision=list(decision), risks=list(risks), esc=False, conf=conf,
                tests=list(tests) or ["对账：is_deleted=0 精确 COUNT 与估数比对", "契约：org_id 唯一、名称非空率"],
                share=share, lumen=lumen, form="table", ours=["etl"], jx=None)


CARDS = [
    gkx(200, "dwd_research_institute_base_info", "科研机构基本信息",
        keys=["org_id", "external_id（统一社会信用代码，可空）", "name_cn", "name_en", "org_type（如 事业单位）", "province / city / area（名称，值域 dim_admin_area）",
              "addr_lng / addr_lat", "registration_org", "incorporation_date"],
        pk="org_id", align="org_id 为三方业务键；统一社会信用代码 external_id 可空，非空时作跨表锚点；name_cn 归一兜底；无 GRID/ROR 列",
        coverage="中国（国内科研院所；样例 中科院深圳先进院）；深圳切片可用 city", rows="2,012（估数）；2,074（2026-08-31 精确 COUNT）",
        gaps=["规模仅约 2 千条，国内科研院所全集口径 unknown（需供应方说明是否全量）", "无学科/技术领域、无产业链字段（ORG-P0-2/P0-3）", "无机构类型码表（ORG-P1-3）"],
        conflicts=["SOURCE-TABLES.md 工作面清单未列本表（清单较旧），以 2026-10-10 报告为准"],
        decision=["本表是否作为「科研院所」主名录（vs 711 万国内机构全集中按类型圈定）"], conf="high",
        tests=["对账：is_deleted=0 COUNT ≈ 2,074", "契约：org_id 唯一；external_id 非空率", "深圳切片：city='深圳市' 行数抽样"]),
    gkx(201, "dwd_org_heis_info", "高校基本信息",
        keys=["org_id", "name_cn", "school_code（学校标识码，非空）", "external_id（统一社会信用代码）", "name_en", "univ_type", "comp_dept（主管部门）",
              "school_nature", "province / city / area", "lng / lat"],
        pk="org_id", align="school_code（教育部学校标识码）为最强锚点；external_id 统一社会信用代码次之；无 GRID/ROR",
        coverage="中国高校", rows="3,576（估数）；2026-08-31 精确 COUNT=0；2026-09-11 摘要 2,864",
        gaps=["行数大起大落（2,933→0→回灌 1,819→估 3,576），疑似软删/换批；业务行数需 is_deleted=0 复核", "无学科/技术领域字段"],
        conflicts=["SUPPLIER-LOAD-PROGRESS：711 万国内机构是否含高校未答"],
        risks=["估数含 is_deleted=1 行（09-11 摘要：高校估数>0 多半含软删，不视为业务回灌）"], conf="medium",
        tests=["对账：is_deleted=0 COUNT 复核", "契约：school_code 唯一"]),
    gkx(202, "dwd_org_base_info", "机构基本信息（国内全集，企业为主）",
        keys=["org_id", "name_cn", "external_id（统一社会信用代码）", "province / city / area", "lng / lat", "org_type（工商类型）",
              "industry_l1~l4（国民经济行业 2017）", "org_size"],
        pk="org_id", align="external_id 统一社会信用代码；专利申请人/项目承担单位名称归一的主靶表（C01/C02 指向本表）",
        coverage="中国（工商主体全集，企业为主）", rows="192,464（估数）；2026-08-31 精确 COUNT=50,000（样例上限）",
        gaps=["无「科研机构/高校/新型研发机构」类型码，只有工商 org_type（ORG-P1-3）", "供应方口径 711 万 vs 库内 19 万，是否全量 unknown（Q-SVC-005 / Q055）"],
        conflicts=["三要素口径 ORG 不含企业，但 DS-04/DS-06「载体」含企业/工作室；本表若进 ORG 需甲方拍板"],
        decision=["载体是否等于机构；企业/工作室是否进 ORG 实体"], conf="medium", share="C01/C02 名称归一靶表；C03 为主卡"),
    gkx(203, "dwd_org_tech_tag", "科技型标签",
        keys=["org_id", "org_tag（如 国家级高新技术企业）"], pk="org_id + org_tag",
        align="org_id → dwd_org_base_info.org_id", coverage="中国", rows="196,662（估数）；202,393（2026-08-31 精确 COUNT）",
        gaps=["标签值域未盘点：是否含「新型研发机构 / 重点实验室 / 工程中心 / 孵化器」等载体标签 unknown"],
        decision=["新型研发机构 / 创新载体是否以本表标签圈定"], conf="low",
        tests=["值域：SELECT DISTINCT org_tag 只读盘点（下次快照）"]),
    gkx(204, "dwd_forg_base_info", "海外机构基本信息",
        keys=["org_id（名录唯一标识，如 60704780）", "name_en", "country_code", "external_id（当地注册码）", "industry_code（NAICS）"],
        pk="org_id", align="org_id 仅三方内部；无 GRID/ROR；名称英文归一", coverage="全球（海外工商主体为主）",
        rows="19,549（估数）；2026-08-31 业务行=0", gaps=["业务行在 08-31 为 0，估数多半含软删（09-11 摘要）", "以企业为主，非科研机构名录"],
        risks=["不视为业务回灌，需 is_deleted=0 复核"], conf="low"),
    gkx(205, "dwd_forg_university_org_info", "海外高校基本信息",
        keys=["org_id", "name_std", "org_type（多值：高等教育/科研设施/资助机构/政府/医疗/非营利/企业）", "country", "region", "city", "website",
              "name_alias", "abbreviation", "lat / lng", "information_date"],
        pk="org_id", align="org_id 三方内部；name_std + name_alias + abbreviation 可做英文归一；无 GRID/ROR 列（形态像 ROR/GRID 衍生但未给码）",
        coverage="全球高校", rows="16,790（估数）；2026-08-31 业务行=0（全表 20,000）",
        gaps=["业务行=0，估数含软删", "GRID/ROR 不可用（unknown，需问供应方是否可补）"], risks=["不视为业务回灌"], conf="low"),
    gkx(206, "dwd_forg_research_org_info", "海外科研机构基本信息",
        keys=["org_id", "name_std", "org_type（多值）", "country", "region", "city", "website", "name_alias", "abbreviation", "lat / lng", "information_date"],
        pk="org_id", align="同 INT-C-ORG-205；无 GRID/ROR", coverage="全球科研机构",
        rows="19,902（估数）；2026-08-31 业务行=0（全表 20,000）", gaps=["业务行=0，估数含软删", "GRID/ROR 不可用"],
        risks=["不视为业务回灌"], conf="low"),
    gkx(207, "dwd_scholar", "学者（机构名字段）",
        keys=["scholar_id", "scholar_org_name_zh / scholar_org_name_en（文本，分号拼接多机构）", "scholar_org_id（暂无值时为空字符串）"],
        pk="scholar_id", align="机构只有名称 → 归一到 org_id（INT-C-ORG-241）；scholar_org_id 空", coverage="全球学者",
        rows="16,933（估数）", gaps=["scholar_org_id 为空串，机构-人才边只能靠名称归一"], conf="medium", share="C01 主卡；本卡只记机构团队/人才结构用法"),
    gkx(208, "dwd_scholar_work_experience", "学者工作经历",
        keys=["scholar_id", "org_name_zh / org_name_en", "起止时间"], pk="unknown（报告未标主键）", align="无 org_id，名称归一",
        coverage="全球", rows="56,295（估数）", gaps=["无 org_id"], conf="medium", share="C01 主卡"),
    gkx(209, "dwd_scholar_education_background", "学者教育背景",
        keys=["scholar_id", "机构名称"], pk="unknown", align="无 org_id，名称归一", coverage="全球", rows="42,837（估数）",
        gaps=["无 org_id"], conf="medium", share="C01 主卡"),
    gkx(210, "dwd_scholar_coauthor", "学者合作者",
        keys=["scholar_id", "co_scholar_id", "co_scholar_org_id（为空）", "co_scholar_org_name"], pk="unknown",
        align="机构合作边候选：scholar 机构 × co_scholar_org_name，两端都要名称归一", coverage="全球", rows="1,028,293（估数）",
        gaps=["co_scholar_org_id 为空", "机构-机构合作边需由人-人合作派生，口径待定（ORG-P1-5）"], conf="medium", share="C01 主卡"),
    gkx(211, "dwd_zh_author", "中文论文作者",
        keys=["author_id / paper_id", "institution（文本）", "affiliation（json）"], pk="unknown", align="无机构 ID，institution 文本归一",
        coverage="中国（中文论文）", rows="63,260（估数）", gaps=["无机构 ID / 无地理"], conf="medium", share="C02 文献主卡"),
    gkx(212, "dwd_zh_paper", "中文论文", keys=["id", "title", "year", "keywords", "scope"], pk="id",
        align="论文 → 作者（211）→ 机构名称归一", coverage="中国", rows="89,214（估数）", gaps=["论文表本身无机构字段"], conf="high",
        share="C02 主卡；本卡只记机构产出计数用法"),
    gkx(213, "dwd_en_author", "英文论文作者", keys=["author_id / paper_id", "institution（文本）", "affiliation（json）"], pk="unknown",
        align="无机构 ID，英文名称归一", coverage="全球（英文论文）", rows="1,367（估数）；2026-08-31 库中无此表",
        gaps=["规模过小（C02 OI-C02-06 英文论文仅 1,356 行）"], conf="low", share="C02"),
    gkx(214, "dwd_scholar_papers", "学者论文", keys=["paper_id", "doi", "title", "year"], pk="paper_id",
        align="经 dwd_scholar_paper_relation（887,927）→ scholar → 机构名称；与论文库按 doi 去重", coverage="全球",
        rows="597,513（估数）", gaps=["机构关联须经学者两跳且为名称"], conf="medium", share="C01/C02"),
    gkx(215, "dwd_patent", "全球专利", keys=["patent_id", "applicants.name", "assignees.name", "first_applicant_name", "main_classification_ipcr / cpc", "country_code", "apdt_year"],
        pk="patent_id", align="申请人/权利人只有名称，无信用代码 → 名称归一到 org_id；有 216 显式边时优先",
        coverage="全球", rows="2,690,167（估数）；2026-08-31 精确 COUNT=86,028", gaps=["申请人无稳定码（ORG-P1-6）"],
        conf="high", share="C02 主卡；本卡只记机构成果用法"),
    gkx(216, "dwd_org_base_info_patent_rel", "国内机构-专利关联", keys=["org_id", "base_external_id", "patent_id", "publication_number"], pk="id",
        align="机构↔专利显式边，可替代名称归一", coverage="unknown", rows="unknown", rows_as_of=None,
        rows_ref="不在 20 要素库行数报告覆盖内；见 data/third-party-source/gkx-mysql-raw/加工/table_inventory.md（结构盘点，无行数）",
        gaps=["行数 unknown（C02 OI-C02-07 同项）", "是否覆盖科研院所/高校（还是仅企业）unknown"], conf="low", share="C02 同卡"),
    gkx(217, "dwd_patent_transfer", "专利转移", keys=["patent_id", "转让人 / 受让人（名称）", "转移日期"], pk="unknown",
        align="转让人名称归一到 org_id（成果转化维）", coverage="全球/中国", rows="21,193（估数）", gaps=["当事人只有名称"], conf="medium", share="C02"),
    gkx(218, "dwd_zh_project", "中文科研项目", keys=["id", "funded_institution（名称）", "participating_institution（json）", "funded_province", "经费", "approval_year"],
        pk="id", align="承担/参与单位名称归一到 org_id（经费/项目维）", coverage="中国", rows="46,455（估数）",
        gaps=["无单位 ID"], conf="medium", share="C02"),
    gkx(219, "dwd_en_project", "英文科研项目", keys=["项目索引", "funded_institution", "funded_country"], pk="项目索引",
        align="英文名称归一", coverage="全球", rows="16,281（估数）", gaps=["无单位 ID"], conf="low", share="C02"),
    gkx(220, "dwd_zh_report_org", "中文报告机构", keys=["org_id", "org_name", "org_xydm（统一社会信用代码，覆盖约 70%）"], pk="org_id",
        align="唯一自带信用代码的文献侧机构表：xydm → research_institute/heis/org_base external_id", coverage="中国",
        rows="1,387（估数）", gaps=["规模小；与 200/201/202 的 org_id 是否同一编码体系 unknown"], conf="medium",
        tests=["对账：org_xydm 与 200/201/202 external_id 命中率"]),
    gkx(221, "dwd_en_report_org", "英文报告机构", keys=["org_id", "org_name", "org_country"], pk="org_id", align="英文名称归一",
        coverage="全球", rows="961（估数）", gaps=["无注册码"], conf="low"),
    gkx(222, "dwd_dim_admin_area", "行政区划维", keys=["cur_code（12 位国标）", "province_code / city_code / area_code / street_code", "名称"],
        pk="cur_code", align="机构表 province/city/area 存名称 → 经本表映射 adcode；深圳圈定用 city_code", coverage="中国",
        rows="19,633（估数）", gaps=["机构表存名称不存码，需名称→码映射（ORG-P1-4）", "产业园/园区层级不在本维（DS-06 需要）"], conf="high",
        share="C01 区划卡共用"),
    gkx(223, "dwd_org_industry_tags", "产业关联企业信息", keys=["industry_code（INB*）", "industry_name", "industry_link_code / name", "company_name", "credit_code"],
        pk="credit_code（报告标主键，实为一对多）", align="credit_code ↔ 机构 external_id；节点码对 dwd_industry_chain_info（1,296）",
        coverage="中国", rows="2,197,216（估数）", gaps=["主体为企业，科研机构命中率 unknown（ORG-P0-2 产业链码未答）"],
        decision=["科研机构产业链归属是否允许经信用代码借用企业产业标签"], conf="low", share="CHAIN 域主卡（非三要素）"),
]

CARDS.append(dict(
    nnn=230, counterpart="trsgraph", sys="NebulaGraph TRSGraph（graphd 10.50.75.136:9669）", table="TAG institution（及机构相关边）", cn="图谱机构顶点",
    keys=["VID", "name", "（仅约 4 个属性可灌，见 Q055 备注）"], pk="VID（规则 unknown）", align="VID 须改用我方 org_id（C04 交接）",
    coverage="unknown", rows="unknown", rows_as_of=None, rows_ref="未查图；客户决策清单 Q055 备注「Nebula institution Tag 仅能灌 4 个字段」",
    freq="unknown", gaps=["顶点数、VID 规则、现存边类型 unknown（C04 盘点）"], conflicts=[], decision=[], risks=[], esc=False, conf="low",
    tests=["C04：institution 顶点计数与 VID 抽样"], share="C04 主卡", lumen="lumen-algo-py 未见 institution 读写（未逐文件核）",
    form="graph", ours=["graph_load", "python_internal"], jx=None))

OURS = [
    (240, "dim_research_org（我方科研机构主数据维表，草案）", "科研机构主数据",
     ["org_uid（我方全局 ID）", "src_refs[{system, table, org_id}]", "credit_code", "school_code", "name_cn / name_en / aliases", "org_category（院所/高校/新型研发机构/载体…，码表待定）",
      "adcode / city_code", "lng / lat", "established_date", "status", "version"],
     "org_uid", "合并 200/201/(202 圈定子集)/205/206：优先 credit_code → school_code → 规范化名称+区划", "全球（国内+海外）"),
    (241, "map_org_alias（机构名称归一 / 别名映射，草案）", "机构名称归一表",
     ["raw_name", "lang", "source_table", "org_uid", "match_method（xydm|school_code|exact|fuzzy|ner|manual）", "score", "confirmed_by"],
     "raw_name + source_table", "所有只有机构名称的表（207–219）→ org_uid", "全球"),
    (242, "rel_doc_org（文献-机构桥接，草案）", "文献-机构桥接表",
     ["doc_type（paper|patent|project|report|scholar）", "doc_id", "org_uid", "role（作者单位/申请人/承担/参与/转让）", "source", "version"],
     "doc_type + doc_id + org_uid + role", "由 241 归一结果 + 216 显式边生成", "全球"),
]
for nnn, table, cn, keys, pk, align, cov in OURS:
    CARDS.append(dict(
        nnn=nnn, counterpart="none", sys="我方项目内结构（不存在，提案）", table=table, cn=cn, keys=keys, pk=pk, align=align, coverage=cov,
        rows="n/a（未建）", rows_as_of=None, rows_ref="提案，无快照", freq="T+1（草案，随入站 ETL）",
        gaps=["新表/新结构，未评审"], conflicts=[], decision=["主数据持有方（我方自建 vs 久新 vs 甲方）"], risks=["归一错误会污染全部机构计数与图谱"],
        esc=True, conf="low", tests=["归一抽样准确率（阈值待定）", "重复 org_uid 检测"], share="C01/C02 归一依赖本卡",
        lumen="不存在（lumen-etl-es-py db/dwd_domain_tables.sql 无机构维）", form="table", ours=["etl", "python_internal"], jx=None))

JX = [  # nnn, row_id, 名称, 交付形态, algorithm, 产出字段
    (250, "SRS-99", "科研机构基础指标模型构建", "SQL", "STAT", ["org_uid", "metric_code", "value", "period", "region"]),
    (251, "SRS-114", "科研机构实体识别构建", "Python", "GRAPH", ["raw_name", "org_uid", "score"]),
    (252, "SRS-115", "科研机构实体关系抽取", "Python", "GRAPH", ["src_org_uid", "dst_org_uid / doc_id", "rel_type", "weight"]),
    (253, "SRS-149", "科研机构重点技术领域布局模型", "API", "MODEL", ["org_uid", "domain_code", "count / share", "as_of"]),
    (254, "SRS-150", "科研机构发展历程模型", "API", "MODEL", ["org_uid", "events[{date, type, desc}]"]),
    (255, "SRS-151", "深圳科研机构优势分析模型", "API", "MODEL", ["industry_code", "org_uid", "dims[成果/经费/人才]", "report"]),
    (256, "SRS-152", "深圳科研机构痛难点识别模型", "API", "MODEL", ["industry_code", "org_uid", "dims[项目/转化/人才/产业合作]", "suggestions"]),
    (257, "SRS-153", "科研合作关系链条模型", "API", "MODEL", ["nodes[org_uid]", "edges[src, dst, strength, type]", "centrality"]),
    (258, "SRS-154", "科研机构引入推荐模型", "API", "MODEL", ["org_uid", "score", "dims[学术影响力/科技成果/团队实力]", "reason"]),
    (259, "SRS-155", "科研机构扶持推荐模型", "API", "MODEL", ["org_uid", "score", "dims[成果/经费效率/人才结构]", "plan_text"]),
    (260, "TOPIC-RORG-012", "科研机构技术力评价与对比（05 无专叶）", "API", "MODEL", ["org_uid", "weights_in", "score", "radar_dims"]),
]
for nnn, rid, name, form, at, out in JX:
    CARDS.append(dict(
        nnn=nnn, counterpart="jiuxin", sys="北京久新（对端；交付待确认）", table=f"{form}-{rid.replace('SRS-', '')}", cn=name, keys=out,
        pk="unknown（建议 org_uid + as_of + version）", align="入参/出参须用我方 org_uid；若用久新自有 ID 须附映射表 jx_org_id→org_uid",
        coverage="unknown（久新数据底座未知：用我方入站 gkx 数据还是其自有库）", rows="unknown", rows_as_of=None, rows_ref="对端交付物，无快照",
        freq="unknown", gaps=["久新确认=待确认（JIUXIN-TECH-ORG-TALENT-L01）", "交付形态为沟通起点（非最终）", f"algorithm.type SRS 层暂标 {at}，未签"],
        conflicts=[], decision=["久新返回是否带我方 org_uid"], risks=["久新底座与我方入站数据不同源时，机构计数口径不一致"],
        esc=False, conf="low", tests=["契约：返回 org_uid 命中我方主数据比例", "降级：对端超时空态 + ⚠️"], share=None,
        lumen="无（lumen-algo-py vendor 有 svcan 同名端点 attract/cultivate/tech-score，口径关系 unknown，B01 C9）" if nnn in (258, 259, 260) else "无",
        form=form, ours=["python_internal"] + (["etl"] if form == "SQL" else []), jx=[rid]))


def metrics_of(cid):
    return sorted(m for m, (ids, _, _) in COV.items() if cid in ids)


def build_card(c):
    cid = f"INT-C-ORG-{c['nnn']}"
    mids = metrics_of(cid)
    cp = c["counterpart"]
    pats = sorted({PAT.get(m, "IP-09") for m in mids}) or ["TBD"]
    if cp == "gkx_mysql_raw":
        chain = dict(fe_route=None, java="只读 ADS（draft；Java 不直连三方库、不写 nGQL）", python="lumen-etl-es-py 离线 ETL（draft）",
                     downstream=f"gkx.{c['table']} →（is_deleted=0）项目 DWD → 机构主数据/桥接 → ADS / ES（C05）/ Nebula（C04）")
    elif cp == "trsgraph":
        chain = dict(fe_route=None, java="不直连 Nebula；读 Python 投影的 ADS", python="lumen-algo-py /internal/graph/*（draft）",
                     downstream="NebulaGraph TRSGraph TAG institution")
    elif cp == "jiuxin":
        chain = dict(fe_route=None, java="gkxlumen-* 只调 Python /internal/*（draft）",
                     python="lumen-algo-py 适配层 /internal/org/*（draft）" + ("；SQL 并入 GDF/ETL 跑在我方库" if c["form"] == "SQL" else ""),
                     downstream="久新 " + c["form"] + "（待确认）→ 结果快照表（B01 IP-11）")
    else:
        chain = dict(fe_route=None, java="只读 ADS 投影（draft）", python="lumen-etl-es-py / lumen-algo-py 归一 Job（draft）",
                     downstream="我方 DWD/ADS 新表（未建）")
    rows_val = c["rows"]
    return {
        "int_id": cid, "layer": "data", "srs": None, "page_ref": None, "dimension": ["ORG"],
        "dep_kind": ["data"] + (["algorithm"] if cp == "jiuxin" else []) + (["graph"] if cp == "trsgraph" or c["nnn"] in (251, 252, 257) else []),
        "metric_ids": mids, "metric_domain_other": [],
        "algorithm_type": sorted({"STAT" if m in STAT else "third_party" for m in mids}),
        "integration_pattern": pats if len(pats) > 1 else pats[0],
        "ours": c["ours"], "counterpart": cp, "delivery_form": c["form"], "jiuxin_row_id": c["jx"],
        "call_chain": chain,
        "contract_draft": {"request": [] if cp != "jiuxin" else ["org_uid[]", "industry_code", "region_code", "time_range"],
                           "response_key_fields": c["keys"], "granularity": {"time": "year", "geo": "country / province / city（深圳）"},
                           "freshness": "unknown" if cp != "none" else "T+1"},
        "data_source": {"source_system": c["sys"], "table": c["table"], "table_cn": c["cn"], "key_fields": c["keys"],
                        "primary_key": c["pk"], "entity_align_key": c["align"], "coverage": c["coverage"], "update_freq": c["freq"],
                        "rows": {"value": rows_val, "as_of": c["rows_as_of"], "ref": c["rows_ref"]},
                        "pages": sorted({p for m in mids for p in PAGES[m]}), "shared_with": c["share"]},
        "status": {"demo": "demo-* 科研机构页为 Mock，未以 dwd_* 接入（未逐页核）", "lumen": c["lumen"],
                   "d1_d4": {"d1": "draft", "d4": "mock"} if mids else None},
        "gaps": c["gaps"], "conflicts": c["conflicts"], "decision_needed": c["decision"],
        "structure_escalation": c["esc"], "risks": c["risks"], "test_points": c["tests"], "confidence": c["conf"],
    }


MASTER = {
    "conclusion": "当前没有任何一方持有统一的科研机构实体主数据。甲方三方库 gkx（供应方即久新）把机构拆成多张互不关联的 dwd_*："
                  "国内科研院所 dwd_research_institute_base_info（≈2 千，org_id + 可空统一社会信用代码）、高校 dwd_org_heis_info（school_code + 信用代码，业务行数反复清零/回灌）、"
                  "工商全集 dwd_org_base_info（以企业为主，无科研机构类型码）、海外高校/科研机构 dwd_forg_university_org_info / dwd_forg_research_org_info（只有三方 org_id，无 GRID/ROR，08-31 业务行=0）；"
                  "论文/专利/项目/学者里的机构全部只有名称（唯一例外 dwd_zh_report_org 带 org_xydm）。草案：我方自建科研机构主数据维表 dim_research_org（INT-C-ORG-240，全局 org_uid）"
                  "+ 名称归一表（241）+ 文献-机构桥接表（242），以统一社会信用代码 / 学校标识码 / 三方 org_id 为对齐锚点；久新 11 行交付一律以我方 org_uid 交互。",
    "status": "decision_needed（待甲方 / 久新确认；structure_escalation → human:李伟）",
    "evidence": [
        "2026-10-10 估数报告：机构相关表行号 641 / 835 / 1410 / 1523 / 1545 / 1654 / 1680；字段见各卡 data_source",
        "2026-08-31 精确 COUNT：heis=0、forg_*=0（全表 20,000）、org_base_info=50,000（样例上限）",
        "2026-09-11 差异摘要：国外机构/高校估数>0 多半含 is_deleted=1，不视为业务回灌",
        "ORG-SUPPLIER-QUESTIONS（2026-09-04）P0-1 主表/主键/稳定码 未回，卡住 22 条",
        "客户决策清单 Q055（国内机构库到位时间）🔴 未决",
        "lumen-etl-es-py / lumen-svc-platform 无科研机构维；lumen-algo-py 仅 vendor svcan 同名推荐端点",
    ],
    "candidates": [
        {"option": "A 我方自建主数据（推荐草案）", "pros": "ID 稳定、可审计，与 Nebula/ES/ADS 同源；C01/C02 归一有统一靶", "cons": "新表 + 归一流程（结构升级）"},
        {"option": "B 久新持有主数据、我方存映射", "pros": "我方工作量小；久新本身是三方库供应方", "cons": "主数据在对端，变更不可控；Java 只读 ADS 闭环需额外映射表"},
        {"option": "C 直接用 dwd_research_institute_base_info + dwd_org_heis_info 拼接", "pros": "零建设", "cons": "无海外、无新型研发机构、高校行数不稳；文献侧名称无法挂接"},
    ],
    "carrier_vs_org": {
        "issue": "三要素口径 ORG=科研机构（含高校、新型研发机构），企业归 OTHER；但展示系统 DS-04「载体」=企业/机构，DS-06「载体」=高校/研究机构/企业/工作室",
        "team_default": "🟡 团队临时默认：ORG 主数据只收院所/高校/新型研发机构；企业/工作室载体留在 dwd_org_base_info（INNOV/ENT 域），DS-04/DS-06 载体榜按 org_category 联合两侧",
        "decision_needed": True,
    },
}

ID_ALIGN = {
    "org_uid": {
        "format_draft": "我方代理键（如 ORG-{CN|GL}-{8 位序号} 或 UUID，待定）；Nebula VID = org:{org_uid}",
        "anchor_priority": ["统一社会信用代码（credit_code：200/201/202/220/223 external_id·xydm）", "学校标识码 school_code（201）",
                            "三方 org_id（200/201/202/204/205/206，仅三方内部稳定，跨表是否同体系 unknown）", "规范化名称 + 区划（province/city）", "英文 name_std + name_alias + abbreviation + country（海外）"],
        "normalize": ["全半角/空白/标点/括号规范化", "后缀与简称表（如「中国科学院」「中科院」、「大学」「学院」）", "多机构分号拆分（dwd_scholar.scholar_org_name_*）",
                      "Python 模糊匹配 + 久新 114 NER 产出作候选（待确认）", "人工确认写回（confirmed_by）"],
        "grid_ror": "unknown：三方库无 GRID/ROR 列；海外高校/科研机构表形态类似但未给码，需问供应方（OI-C03-04）",
        "versioning": "合并/拆分保留 redirect（旧 org_uid → 新 org_uid），图谱与快照按 version 回放",
    },
    "org_category": {"draft": "院所 / 高校 / 新型研发机构 / 创新载体（实验室、工程中心、孵化器…）/ 企业（非 ORG）", "source": "200=院所、201=高校、203 标签候选（未盘点）、205/206 org_type 多值",
                     "decision": "码表与新型研发机构认定口径待甲方（OI-C03-02）"},
    "geo": {"rule": "机构表存区划名称 → dwd_dim_admin_area（222）映射 adcode；深圳圈定=city_code 440300（区级 4403xx）", "gap": "产业园/园区层级无源（DS-06）"},
    "cross_leaf": {"C01": "人才 → 机构：scholar_org_name_* / work_experience / education → map_org_alias → org_uid",
                   "C02": "专利申请人 / 项目承担单位 → map_org_alias → org_uid；dwd_org_base_info_patent_rel 有数据时优先",
                   "C04": "TRSGraph institution VID 迁移为 org:{org_uid}"},
    "jiuxin": {"rule": "久新 API 入参/出参使用我方 org_uid；若用自有 ID 须交映射表 jx_org_id→org_uid，按命中率对账（阈值待定）", "status": "待确认（郭万迎主谈）"},
}

OPEN = [
    ("OI-C03-01", "科研机构主数据持有方与全局 org_uid（我方自建 / 久新 / 甲方）", "human:李伟（结构）+ 甲方/久新", "structure_escalation + decision_needed", "P0"),
    ("OI-C03-02", "载体是否等于机构；企业/工作室是否进 ORG；新型研发机构/创新载体认定口径（是否用 dwd_org_tech_tag 圈定）", "PM → 甲方", "decision_needed（客户决策清单草案）", "P0"),
    ("OI-C03-03", "供应方 9 题未回：ORG-P0-1 主表主键稳定码 / P0-2 产业链码 / P0-3 学科码 / P1-1~P1-6（2026-09-04 出题）", "human:郭万迎", "供应方回复", "P0"),
    ("OI-C03-04", "GRID/ROR 是否可由供应方补列（海外高校/科研机构表）", "human:郭万迎", "供应方回复", "P1"),
    ("OI-C03-05", "高校表 dwd_org_heis_info 与海外 forg_* 业务行数（is_deleted=0）需只读 COUNT 复核；估数含软删", "data-agent（下次快照）", "核验", "P1"),
    ("OI-C03-06", "久新科研机构 11 行交付形态与数据底座（用我方 gkx 入站数据还是其自有库）", "human:郭万迎", "对端确认", "P0"),
    ("OI-C03-07", "711 万国内机构是否含高校/科研院所；dwd_research_institute_base_info 是否全量（Q055 / Q-SVC-005）", "供应方 / 甲方", "供应方回复", "P1"),
    ("OI-C03-08", "深圳科研机构圈定规则（注册地 city vs 实际办公地 vs 分支机构）", "PM → 甲方", "decision_needed", "P1"),
    ("OI-C03-09", "dwd_org_tech_tag 标签值域、dwd_org_base_info_patent_rel 行数与覆盖面（只读盘点）", "data-agent（下次快照）", "核验", "P2"),
    ("OI-C03-10", "lumen-algo-py vendor svcan 同名端点（attract/cultivate/tech-score）与 ORG 指标口径关系（B01 C9）", "algorithm-agent（B09）", "owner 未定", "P1"),
    ("OI-C03-11", "架构初稿 §3 写 DS-04 依赖 99/149/153、DS-06 依赖 151/152，但 DS-04-CARRIER-RANK / DS-06-CARRIER 明确禁止挂 99/149/154/155、151/152；以页面映射为准并回改初稿", "architect", "冲突回写", "P2"),
    ("OI-C03-12", "TRSGraph institution 顶点数 / VID 规则 / 可灌属性（Q055 备注仅 4 字段）", "C04", "交接", "P1"),
]


def main():
    cards = [build_card(c) for c in CARDS]
    items = []
    for m in sorted(COV):
        ids, binding, note = COV[m]
        items.append({"metric_id": m, "algorithm_type": "STAT" if m in STAT else "third_party", "source_cards": ids, "binding": binding,
                      "integration_pattern": PAT.get(m, "IP-09"), "srs_refs": SRS.get(m, "[]（未回填）"), "d1_pending_ref": D1REF.get(m, "GAP-ALGO-TYPE-UNSIGNED"),
                      "kit_source_tables": "pending_ods", "note": note, "pages": PAGES[m]})
    no_src = [i["metric_id"] for i in items if i["source_cards"] == "no_source"]
    doc = {
        "task_id": "SCI-INT-C03", "layer": "data", "element": "ORG（科研机构：高校 / 院所 / 新型研发机构 / 创新载体）",
        "generated_by": "产物/_work/C03-build.py", "as_of": "2026-10-18",
        "note": "对端正名「久新」；引用旧路径 metrics/request/九新-技术机构人才/ 保留原名。指标 8 件套/D1–D4 取自 MCP metric-registry（metric-query domain=ORG fields=full，2026-10-18）；"
                "行数引用仓内快照，未连库。scope_count / card_count 按源卡计数；data_source 为本叶对 §2 schema 的扩展块。",
        "scope_count": len(cards), "card_count": len(cards), "gap": [],
        "master_data_conclusion": MASTER, "id_alignment_draft": ID_ALIGN,
        "metric_coverage": {"scope_metrics": 22, "covered": 22 - len(no_src), "no_source": len(no_src), "diff": [],
                            "binding_legend": {"kit_declared": "MCP kit.source_tables 点名（本域 22 条均 pending_ods，无此类）",
                                               "candidate": "本叶据口径推断的候选原料（未核验）", "jiuxin_pending": "久新交付（11 行之一，全部待确认）",
                                               "no_source": "无可识别源"},
                            "items": items},
        "open_items": [dict(id=a, item=b, owner=c, kind=d, blocking=e) for a, b, c, d, e in OPEN],
        "cards": cards,
    }
    OUT.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print(f"wrote {OUT.name}: cards={len(cards)} no_source={len(no_src)}")


if __name__ == "__main__":
    main()
