# SYSINT-SCHEME-07-L04 · 燕大七要素上图对照

> **任务**：`SYSINT-SCHEME-07-L04`（WBS-07-00C）
> **监管人 / 认领人**：human:郭万迎
> **完成日期要求**：2026-11-09（WBS-07-00 出门日）
> **创建时间**：2026-10-27

## 一、目的与口径

### 1.1 本文件是什么

本文件是**燕大侧七要素完整台账**。以七个要素为轴，从燕大快照（2026-10-26）中逐一抽取每个要素的：实体 TAG、关系 EDGE、源数据表、抽取链路、量级锚点、现状判定。

它回答的问题是：**「每个七要素在燕大图谱侧到底有什么、从哪张表来、怎么上图、量级多少」**。

### 1.2 与 L02 的边界区分

| 维度 | L02 对齐轴 | L04 本文件 |
|---|---|---|
| 视角 | **需求侧 14 实体 ↔ 燕大 17 TAG 双向对齐** | **燕大侧七要素单向盘点** |
| 输出形式 | 对齐判定表（✅/🔶/🔴） | 要素台账（TAG + EDGE + 源表 + 量级） |
| 谁对谁 | 需求实体 → 燕大 TAG | 燕大要素 → 完整清单 |
| L05 角色 | 对齐基准（告诉 L05 哪些实体/关系是"同一个东西"） | 减数基准（告诉 L05 燕大侧已有哪些实体/关系） |

### 1.3 事实基准

- **唯一事实源**：`2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md`
- **不验证代码入口**：L04 只认快照原文，不需要像 L03 那样去 repo 里翻代码
- **不改快照原文**：本文件只做整理和结构化，不修订上游

### 1.4 燕大全局规模（快照实测）

| 项 | 数量 | 来源 |
|---|---:|---|
| 实体 TAG | 17（业务 15 + 治理 2） | 快照 1.3-① |
| 关系 EDGE | 33（挂脚本 29 + 改道/未绑 4） | 快照 1.3-① |
| 抽取脚本 | 46 | 快照 1.3-① |
| 来源绑定 | 155 | 快照 1.3-① |
| 属性总数 | 867 | 快照 1.3-① |
| 图空间 | `gkx_local_1` / `gkx_full_1`（平台 Schema 注册） | 快照 1.3-① |

---

## 二、要素 1 · 产业

> 快照 1.2 节判定：**✅ 已实现**

### 2.1 实体 TAG

| TAG | 中文名 | 源数据表 | 字段 | 量级锚点 |
|---|---|---|---|---|
| `IndustryChain` | 产业链 | `dwd_industry_chain_info`（7 位链行） | industry_code（→chain_code）、chain_name | gkx 样例 **12 条链** |
| `IndustryNode` | 产业链节点 | `dwd_industry_chain_info`（9–21 位节点行） | node_id、node_name、node_type、level、node_seq、node_imp_level、node_stage、node_path | gkx 样例 **1,261 节点**（后 5 列 gkx 源为 NULL 占位） |
| `News`（产业资讯子集） | 新闻资讯 | `dwd_industry_chain_news_info` | news_id、title、summary、relaese_date | gkx 样例 1.78M（与企业资讯共享 TAG） |

### 2.2 关系 EDGE

| EDGE | 方向 | 起→终 | 逻辑 | 量级 |
|---|---|---|---|---|
| `HAS_NODE` 链包含节点 | IndustryChain → IndustryNode | 同表按编码位数拆链行/节点行后互连 | 直接映射 | 1,261 边 |
| `CHILD_OF` 节点上下级 | IndustryNode → IndustryNode | 父节点 industry_link_code | 直接映射 | 1,261 边 |
| `DOWNSTREAM_OF` 产业上下游 | IndustryNode → IndustryNode | 源无下游数据 | **0 边**（SQL 恒空） |
| `BELONGS_TO_NODE` 企业归属节点 | Organization → IndustryNode | org_id ↔ node_id / 链编码（机构-产业标签 JSON 按位炸开） | 非直连 | 外部 gkx **≈116,180 边** / 本地历史跑数 2,943 |
| `COVERS_CHAIN` 资讯报道链 | News → IndustryChain | news_id × chain_code（JSON_OVERLAPS） | 非直连 | 94,560 边 |

### 2.3 上图逻辑

走统一抽取链（Temporal workflow `kg.schema.extract`），实体链 `IndustryChain` + `IndustryNode` 先行 → 关系链串行。产业域无特殊挂实体改道或消歧逻辑，全部直接映射或 JSON 炸开。

### 2.4 关键观察

- 产业上下游（DOWNSTREAM_OF）**恒空 0 边**，源无下游数据
- `BELONGS_TO_NODE` 把企业（Organization）连到产业节点，本地实际无 `dwd_org_industry_chain_dtl` 表，用 `dwd_org_industry_tags` 替代
- 产业资讯 News 与企业资讯 News **共享同一个 TAG**，靠源表区分（`dwd_industry_chain_news_info` vs `dwd_org_important_news_info`）

---

## 三、要素 2 · 企业

> 快照 1.2 节判定：**✅ 已实现（无「企业」专属枚举，见 1.3-③）**

### 3.1 核心难点（来自快照 1.3-③）

> Organization 单 TAG + org_kind 7 值枚举中**没有「企业」也没有「服务机构」专属值**。内地企业主体全落默认桶 `domestic_organization`；`org_type` 本地实测基本为空（3,689 行中 3,639 NULL），连文本区分都不可用。

### 3.2 实体 TAG

| TAG | 中文名 | org_kind 枚举值 | 源数据表 | 量级锚点 |
|---|---|---|---|---|
| `Organization` | 机构（企业主体，默认桶） | `domestic_organization` | `dwd_org_base_info`（企业主表）、`dwd_org_org_product_info`、`dwd_stock_base`、`dwd_forg_base_info`、`dwd_forg_product_info` | — |
| `Organization`（港澳台） | 机构 | `hongkong_company` / `taiwan_company` / `macao_company` | `dwd_special_hongkong/taiwan/aomen_company` | — |
| `Organization`（海外） | 机构 | `foreign_organization` | `dwd_forg_base_info`、`dwd_forg_product_info` | — |
| `Product` | 产品 | — | `org_base_info.main_products`、`org_org_product_info.main_prod`、`forg_product_info.main_products` | gkx 样例 **47,956** |
| `Event`（工商事件子集） | 事件 | — | 15 张工商表（annual_financial、changerecord、financing、recruit、stock_finance、company_abnormal、company_punish、company_illegal、risk_tax_punish、opt_judicial_case、risk_shixin、risk_zhixing、bankruptcy_public_cases、bid_base_out、bid_target_item_out） | 源 ≈16M 行，图内**封顶 124,999** |
| `News`（企业资讯子集） | 新闻资讯 | — | `dwd_org_important_news_info` | 与产业资讯共享 TAG |

### 3.3 关系 EDGE（企业域 11 类工商治理边）

| EDGE | 方向 | 起→终 | 逻辑 | 特殊处理 |
|---|---|---|---|---|
| `LEGAL_REP_OF` 法定代表 | Person → Organization | lerep / legal_person → org_id | 非直连（人名按公式生成 person vid，词表过滤机构类） | — |
| `EXECUTIVE_OF` 高管任职 | Person → Organization | executives_name → org_id | 同上 | executives_position 已建模 |
| `SHAREHOLDER_OF` 股东持股 | Person/Organization → Organization | owners_name / inv_org_id → org_id | 非直连（owners_type 词表判自然人/机构） | ownership_percentage 已建模 |
| `ACTUAL_CONTROLLER_OF` 实际控制 | Person → Organization | entity_name → org_id | **外部 gkx 源库缺表 → 0 边** | direct_pct / total_pct 已建模 |
| `BENEFICIAL_OWNER_OF` 最终受益 | Person → Organization | bo_name → org_id | **外部 gkx 源库缺表 → 0 边** | 三级持股比例已建模 |
| `SUBSIDIARY_OF` 子公司 | Organization → Organization | affiliates_company_id / affiliates_name → org_id | 直接映射（ID 缺失时名匹配） | 外部 gkx 换源修复 |
| `INVESTS_IN` 对外投资 | Organization → Organization | org_id → inv_org_id | 直接映射 | investment_amount / investment_ratio |
| `ACQUIRES` 收购 | Organization → Organization | acquiring_org_id → acquired_org_id | 直接映射 | ma_amount / currency_code |
| `PRODUCES` 生产产品 | Organization → Product | main_prod / main_products（= product vid 键） | 直接映射（产品名即终点键） | tech_product_seq |
| `HAS_NEWS` 企业资讯 | Organization → News | org_id → 新闻行稳定键 | 直接映射（一行新闻一条边） | — |
| `INVOLVED_IN` 涉风险事件 | Organization → Event | 各事件表 org_id / u_id → 事件主键 | 直接映射（17 表规格驱动） | role=当事方角色 |

### 3.4 上图逻辑

Organization 多表同构列补空（工商同构列覆盖所有子集表），Product 依附 Organization 存在（缺机构 ID 整行跳过），Event 封顶 124,999 行，SHAREHOLDER_OF 走机构/自然人分流逻辑。两条 0 边（ACTUAL_CONTROLLER_OF / BENEFICIAL_OWNER_OF）因外部 gkx 源库缺表，本地是否有替代表需另行验证。

---

## 四、要素 3 · 技术（论文）

> 快照 1.2 节判定：**✅ 已实现**

> 本要素是燕大图谱中实体和关系最密集的要素，涵盖论文域、专利域、项目域、关键词本体四个子域。

### 4.1 实体 TAG

| TAG | 中文名 | 源数据表 | 量级锚点 |
|---|---|---|---|
| `Paper` | 论文 | `dwd_zh_paper`、`dwd_en_paper` | — |
| `Journal` | 期刊 | `dwd_zh_journal`、`dwd_en_journal` | — |
| `Patent` | 专利（基础绑定 A）+（富集绑定 B） | `dwd_patent` | gkx 样例 **2.69M 行** |
| `PatentFamily` | 专利同族 | `dwd_patent.simple_family_number` | 按同族号聚合 |
| `Report` | 科技成果 | `dwd_zh_report`、`dwd_en_report` | — |
| `Keyword` | 技术主题（关键词本体） | `dwd_zh/en_paper_classification`、`dwd_patent.keywords`、`dwd_zh/en_project.keywords`、`dwd_scholar_research_direction` | gkx 样例 **237,552 词**（中英归一化） |
| `Project` | 项目 | `dwd_zh_project`、`dwd_en_project` | — |

### 4.2 关系 EDGE（论文域 9 类 + 项目域 2 类）

| EDGE | 方向 | 起→终 | 逻辑 | 量级 | 特殊处理 |
|---|---|---|---|---|---|
| `AUTHORED_BY` 论文署名 | Paper → Person | dwd_zh/en_author.paper_id → author_id | 直接映射 | — | author_sequence / is_corresponding 已建模；兜底绑定 dwd_scholar_paper_relation |
| `PUBLISHED_IN` 论文发表 | Paper → Journal | paper.publication_id = journal 主键 | 直接映射 | — | 英文侧 publication_id 全空 → **0 边** |
| `CITES` 论文引用 | Paper → Paper | citation/related 表 paper_id → 被引 DOI | 非直连 | zh 引用 ≈**20,031 边** | 无 DOI 桩点 → paper_ref_* 待 SAME_AS 认领 |
| `HAS_KEYWORD` 论文主题 | Paper → Keyword | paper_classification.id → 关键词 | 非直连 | — | 专利/项目关键词已入 Keyword 点；NFKC+casefold→md5 归一 |
| `REFERENCED_BY` 论文-报告 | Paper → Report | dwd_zh_report_paper.paper_id → report_id | 直接映射 + JSON 数组展开 | — | — |
| `MEMBER_OF_FAMILY` 专利同族 | Patent → PatentFamily | patent_id → simple_family_number | 直接映射 | — | — |
| `INVENTED_BY` 专利发明人 | Patent → Person | patent_id → inventors（人名列表） | **挂实体改道** | — | pendingReview 实体 + 边暂存 → 人裁后补写；sequence 已建模 |
| `APPLIED_BY` 专利申请方 | Patent → Organization | patent_id → 申请人字段 | 同上挂实体改道 | — | role / sequence / resolution_status 已建模 |
| `OWNED_BY` 专利权利人 | Patent → Organization | patent_id → 权利人字段 | 同上挂实体改道 | — | is_current 已建模 |
| `HAS_OUTPUT` 项目产出 | Project → Paper/Patent/Report | project_output.project_id → outputs JSON | 非直连 | — | 匹配链 paper=DOI / patent=号码 / report=title|year；ambiguous/not_found 进复核 |
| `OUTPUT_OF` 成果归属 | Project → 成果实体 | — | **未绑脚本** | — | 跨域 dwd_rel_project_* 只写报告分类，不建边 |

### 4.3 上图逻辑

技术要素是上图链中最复杂的部分：
- **9 类 EDGE 中 3 类走挂实体改道**（INVENTED_BY / APPLIED_BY / OWNED_BY）——专利发明人/申请方/权利人均走 pendingReview 队列，人裁后补写边
- **CITES 依赖 SAME_AS 向量对齐**——无 DOI 桩点待后续认领
- **HAS_OUTPUT 用多策略匹配**——DOI → title|year → title 三档降级
- **PUBLISHED_IN 英文侧 0 边**——源数据 publication_id 全空

---

## 五、要素 4 · 人才

> 快照 1.2 节判定：**✅ 已实现**

### 5.1 实体 TAG

| TAG | 中文名 | 源数据表 | 量级锚点 |
|---|---|---|---|
| `Person` | 科技专家（scholar 子集） | `dwd_scholar`（status=1，聚合 SQL） | gkx 样例 **21,308 人** |
| `Person` | 科技专家（论文作者子集） | `dwd_zh_author`、`dwd_en_author` | vid = person_{author_id} |
| `Person` | 机构角色人员子集 | `dwd_org_shareholder_info`、`dwd_org_executive_info`、`dwd_forg_executive_info`、各机构主表 lerep | vid = person_{md5(kind\|org\|name\|birth\|country)}；词表过滤机构类不出 Person |
| `ScholarOrganization` | 学者任职机构 | `dwd_scholar_work_experience` | 2026-10-15 引入，修复 AFFILIATED_WITH 悬挂端点 |

### 5.2 关系 EDGE（人才域 8 类中的人才相关 + 工商治理域中的 Person 端点）

| EDGE | 方向 | 起→终 | 逻辑 | 量级 |
|---|---|---|---|---|
| `COAUTHOR_WITH` 专家合著 | Person ↔ Person | scholar_id ↔ co_scholar_id | 直接映射（status=1） | 源 ≈**1.19M 行** |
| `AFFILIATED_WITH` 任职 | Person → Organization | scholar_id → org_name_zh/en（机构名，无机构 ID） | 非直连（机构名消歧，confidence ≥0.6 写桩点；旧口径 scholar_org_id 直连=1.0 优先） | 2026-10-15 换源修复悬挂端点 |
| `STUDIED_AT` 就读院校 | Person → Organization | scholar_id → education_background_institution | 非直连（中→英、精确→小写双跳匹配） | 不中则弃，不建桩机构 |
| `LEADS` 项目负责人 | Project → Person | project.id → project_host（负责人姓名） | 非直连（图匹配器——人名 vs 图内 Person） | 依赖实体链先入库 |
| `HAS_PARTICIPANT` 项目参加人 | Project → Person | project.id → participants（参与人列表） | 同上匹配器 | — |
| `FUNDED_BY` 项目资助方 | Project → Organization | project.id → funded_institution / participating_institution | 非直连（机构名候选 vs 机构名池） | 两列全空/0 命中 → 0 边 |
| `LEGAL_REP_OF` / `EXECUTIVE_OF` / `SHAREHOLDER_OF` | Person → Organization | （同企业要素 3.3 节） | 非直连 | 词表过滤机构类不出 Person |

### 5.3 关键观察

- Person TAG 承载了**三类完全不同的人**：学术 scholar、论文 author、企业高管/股东/法人——靠 vid 生成公式区分（scholar_id / author_id / md5 混合键）
- `ScholarOrganization` 是 2026-10-15 新增的轻量 TAG，专门修复 AFFILIATED_WITH 悬挂端点问题（之前 Person 直接连 Organization，机构名匹配不上时边就挂了）
- Person 侧有三条 0 边风险：ACTUAL_CONTROLLER_OF / BENEFICIAL_OWNER_OF（源库缺表）、STUDIED_AT 匹配不中则弃（不建桩机构）

---

## 六、要素 5 · 科研机构

> 快照 1.2 节判定：**✅ 已实现**

### 6.1 核心机制

> 科研机构**不是独立 TAG**，而是 Organization 单 TAG 下靠 **org_kind 枚举值**区分的子集。

| org_kind 值 | 含义 | 源数据表 |
|---|---|---|
| `domestic_university` | 高校 | `dwd_org_heis_info`（univ_type 字段实测：理工类/医药类/综合类） |
| `domestic_research_institute` | 科研院所 | `dwd_research_institute_base_info`（org_type 实测：科研事业单位） |

### 6.2 实体 TAG

| TAG | 中文名 | 源数据表 |
|---|---|---|
| `Organization`（高校子集） | 机构 | `dwd_org_heis_info`（工商同构列 + univ_type） |
| `Organization`（科研院所子集） | 机构 | `dwd_research_institute_base_info`（工商同构列 + org_type） |
| `ScholarOrganization` | 学者任职机构 | `dwd_scholar_work_experience`（与人才要素共享 TAG） |

### 6.3 关系 EDGE

科研机构作为端点出现在多个跨要素关系中：

| EDGE | 方向 | 起→终 | 逻辑 |
|---|---|---|---|
| `AFFILIATED_WITH` 任职 | Person → Organization（含科研机构） | （同人才要素 5.2 节） |
| `STUDIED_AT` 就读院校 | Person → Organization（含高校） | （同人才要素 5.2 节） |
| `FUNDED_BY` 项目资助方 | Project → Organization（含科研机构） | （同技术要素 4.2 节） |
| `APPLIED_BY` 专利申请方 | Patent → Organization | 挂实体改道（含科研机构申请专利场景） |
| `OWNED_BY` 专利权利人 | Patent → Organization | 同上 |

### 6.4 关键观察

- 科研机构要素**边界清晰**：高校 `domestic_university` + 科研院所 `domestic_research_institute` 两个 org_kind 值完整覆盖，不像企业和服务机构落默认桶
- 但 Organization 是单 TAG，查询时**必须加 org_kind 过滤**才能拿到科研机构子集——图数据库本身不做类型隔离

---

## 七、要素 6 · 政策

> 快照 1.2 节判定：**⚠ 未实现（蓝图+源表已备）**

### 7.1 现状

**无 Policy TAG、无政策相关 EDGE、无抽取脚本**。

快照原文（1.2 节）：
> | 6     | 政策     | —                                                | ⚠ 未实现（蓝图+源表已备）                |

### 7.2 蓝图与源表（快照未展开，待燕大确认）

| 信息 | 状态 |
|---|---|
| 政策源表 | 已备（具体表名快照未列出） |
| 抽取脚本 | 未编写 |
| Policy TAG | 未注册 |
| 政策相关 EDGE | 未定义 |
| 量级锚点 | 无 |

### 7.3 对需求侧的影响

这是 **P0 GAP**，直接阻塞需求清单中：
- `policy` 实体
- `publish` 关系（institution→policy）
- `policy_relate` 关系（policy↔policy）
- `policy_apply_to` 关系（policy→field/enterprise/person/institution）

### 7.4 待燕大确认事项

1. 政策源表的具体名称和字段
2. Policy TAG 注册排期
3. 三条政策关系的 EDGE 定义
4. 是否需要支持政策版本管理（政策条款包概念）

---

## 八、要素 7 · 服务机构

> 快照 1.2 节判定：**⚠ 无独立口径（Organization 默认桶混装）**

### 8.1 现状

与企业要素完全相同的困境：**Organization 默认桶 `domestic_organization` 同时装了企业和服务机构**，无 org_kind 枚举值可区分。

快照原文（1.2 节）：
> | 7     | 服务机构   | Organization（默认桶混装）                              | ⚠ 无独立口径                       |

### 8.2 问题细节

| 区分手段 | 可用性 | 证据 |
|---|---|---|
| org_kind 枚举 | ❌ 不可用 | 7 值枚举（domesticuniversity / domesticresearchinstitute / hongkongcompany / taiwancompany / macaocompany / foreignorganization / domesticorganization）中**无服务机构专属值** |
| org_type 文本字段 | ❌ 基本为空 | 本地实测 3,689 行中 3,639 NULL |
| 独立 TAG | ❌ 不存在 | 无 ServiceOrganization 或类似 TAG |

### 8.3 对需求侧的影响

需求清单**未单列服务机构实体**，但展示系统「科技服务全景」模块隐含需要区分科技服务机构（孵化器、检测机构、中介等）与普通企业。当前燕大图谱层面无法做这个区分。

---

## 九、治理层辅助 TAG（不属于七要素）

> 快照 1.2 节列出 17 TAG，上面七要素共覆盖了 15 个业务 TAG，剩余 2 个是治理层辅助 TAG，不属于业务要素：

| TAG | 中文名 | 用途 |
|---|---|---|
| `OrganizationBase` | 机构基础信息（桩） | 论文域 14 表内联机构名列建占位点，供后续对齐认领；溯源混入 TAG，**非业务实体** |
| `DataSource` | 数据来源（治理占位） | Schema 治理层元数据（id / 表中文名 / tier / library），用于溯源；**非业务实体** |

---

## 十、跨要素引用关系汇总

燕大图谱中，七要素之间靠以下 EDGE 互连（整理自快照第三章）：

| 从 | 到 | EDGE | 涉及要素组合 |
|---|---|---|---|
| Person | Organization（含企业/科研机构/服务机构） | AFFILIATED_WITH / STUDIED_AT / LEGAL_REP_OF / EXECUTIVE_OF / SHAREHOLDER_OF | 人才↔企业/科研机构 |
| Organization（企业） | Organization（企业） | SUBSIDIARY_OF / INVESTS_IN / ACQUIRES | 企业↔企业 |
| Organization（企业） | Product | PRODUCES | 企业↔产品 |
| Organization（企业） | Event | INVOLVED_IN | 企业↔工商事件 |
| Organization（企业） | News | HAS_NEWS | 企业↔企业资讯 |
| Organization | IndustryNode | BELONGS_TO_NODE | 企业↔产业 |
| Person | Person | COAUTHOR_WITH | 人才↔人才 |
| Paper | Person | AUTHORED_BY | 论文↔人才 |
| Paper | Paper | CITES | 论文↔论文 |
| Paper | Journal | PUBLISHED_IN | 论文↔期刊 |
| Paper | Keyword | HAS_KEYWORD | 论文↔关键词 |
| Paper | Report | REFERENCED_BY | 论文↔科技成果 |
| Patent | Person | INVENTED_BY | 专利↔人才（挂实体改道） |
| Patent | Organization | APPLIED_BY / OWNED_BY | 专利↔机构（挂实体改道） |
| Patent | PatentFamily | MEMBER_OF_FAMILY | 专利↔专利同族 |
| Project | Person | LEADS / HAS_PARTICIPANT | 项目↔人才 |
| Project | Organization | FUNDED_BY | 项目↔机构 |
| Project | Paper/Patent/Report | HAS_OUTPUT | 项目↔技术成果 |
| IndustryChain | IndustryNode | HAS_NODE | 产业链↔产业节点 |
| IndustryNode | IndustryNode | CHILD_OF | 产业节点↔产业节点 |
| News | IndustryChain | COVERS_CHAIN | 产业资讯↔产业链 |

---

## 十一、全局抽取链（快照第四章摘要）

> 全要素统一走 Temporal workflow `kg.schema.extract`：
> 
> ```
> 来源绑定分批读取 → @step 转换脚本（子进程）→ 写前消歧/改写 VID
>   → nGQL 批量 INSERT VERTEX / INSERT EDGE → 逐行失败进审核
>   → 批级实体索引 upsert → 水位推进 → 链尾 SUBMIT JOB STATS
> ```
> 
> - 部署形态：**实体链（17）先行 → 关系链 A/B（1413）串行**
> - 读取模式：三模式（querySql + keyset/timeColumn 水位 / LIMITOFFSET）
> - 消歧逻辑：≥0.85 并入 / 0.65–0.85 灰区审核 / <0.65 新实体
> - 写链长度：单 Schema 抽取（extract）与多 Schema 串行链（chain，2–20 个严格串行）
> - 失败处理：逐行失败进 TEXTRACTFAIL 审核队列；可按 pkCursor 定点重抽
> - 验证驱动：`gkx_dwd_local_e2e.py`（prepare → purge → run → verify）

### 各要素链路复杂度对比

| 要素 | 实体链数 | 关系链数 | 复杂度 | 特殊处理 |
|---|---:|---:|---|---|
| 产业 | 2（IndustryChain + IndustryNode） | 5 | 低 | DOWNSTREAM_OF 恒空 0 边 |
| 企业 | 4（Organization + Product + Event + News） | 11 | 高 | ACTUAL_CONTROLLER_OF / BENEFICIAL_OWNER_OF 0 边；SHAREHOLDER_OF 机构/自然人分流 |
| 技术 | 7（Paper + Journal + Patent + PatentFamily + Report + Keyword + Project） | 11 | 极高 | INVENTED_BY / APPLIED_BY / OWNED_BY 挂实体改道；CITES SAME_AS 对齐；PUBLISHED_IN 英文侧 0 边 |
| 人才 | 2（Person + ScholarOrganization） | 6 | 中 | Person 三类子集 vid 生成公式不同 |
| 科研机构 | 3（Organization 两子集 + ScholarOrganization） | 5（共享人才/技术域边） | 中 | 靠 org_kind 枚举过滤，非独立 TAG |
| 政策 | — | — | — | **蓝图已备，无任何代码** |
| 服务机构 | —（Organization 默认桶） | — | — | **无独立口径** |

---

## 十二、与 L05 GAP 差集的衔接说明

L05 的差集公式：**GAP = 需求清单 −（L03 算法中台已实现 ∪ L04 燕大已实现）**

本文件（L04）提供 L05 减数的「燕大侧已有」部分：

| L05 减数项 | 本文件对应章节 |
|---|---|
| 燕大已有实体 TAG | 各要素 2.1 / 3.2 / 4.1 / 5.1 / 6.2 节 |
| 燕大已有关系 EDGE | 各要素 2.2 / 3.3 / 4.2 / 5.2 节 |
| 燕大已实现的量级锚点 | 各要素实体表中的量级列 |
| 燕大已实现但需求清单未显式要求的边 | 第十章跨要素引用关系汇总 |
| 燕大完全空白的要素 | 第七章（政策）+ 第八章（服务机构无独立口径） |

**重要**：L05 用 L02 对齐轴判断「需求实体/关系到底对应燕大哪个 TAG/EDGE」，用本文件判断「燕大侧是否真的实现了这个 TAG/EDGE」——两份文件配合完成减数。

---

## 十三、输入材料索引

| 材料 | 路径 | 版本 |
|---|---|---|
| 燕大七要素现状快照 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/对端/2026-10-26-科创要素知识图谱-七要素数据维度与上图逻辑现状快照.md` | **2026-10-26**（唯一事实源） |
| 致燕大需求清单 v1.0 | `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` | v1.0（发燕大版） |
| SYSINT-SCHEME-07-L02 对齐轴 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/我方/SYSINT-SCHEME-07-L02-对齐轴.md` | v1.0（为本文件的前置依赖） |
| WBS-07 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS.md` | 2026-10-26 |
