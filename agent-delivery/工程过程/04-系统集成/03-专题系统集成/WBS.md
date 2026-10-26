# WBS 草案 · 专题系统集成

> 2026-10-22 梳理。方案任务 `SYSINT-SCHEME-03-L01` 于 2026-10-23 由 `human:淮政玮` 签收后，同日改回处理中。范围与可对端以 [技术方案](./技术方案.md) 现稿为准。同日按已写明的人员姓名补建开发任务，任务号回写本表。  
> 基础数据管理的叶 **已经在 registry**，状态为当日快照。本表收录进行中的叶（`integration` / `ready_to_sign`），不新开 ID。`SYSINT-SCHEME-03-L01` 不追进这些已开工叶的 `depends_on`。2026-10-22 晚把两条 backlog 补进行：`CMS-JX-POL-LIST-L01`、`CMS-JX-ENT-PROFILE-L01`，沿用原 ID。其余 backlog 与已 `done` 的设计单不计入。  
> 内容管理、可视化的开发任务已于 2026-10-23 建号，见下表。菜单配置写进那些叶的完成条件。内容菜单名称未收口前，用定稿规约的来稿用词。  
> 表中「仓」只是建议，最终由该行监管人决定。已经在 registry 里的叶，仓以注册表现状为准。  
> 2026-10-22 晚：草稿已确认作建叶底稿。已有监管人即负责人。开始时间注册表没有，写「无开始时间」。完成日期要求取智谱 11 月倒排「科技专题服务系统」功能开发完成日：企业、产业链、统一用户为 2026-10-19；政策、服务链、综合为 2026-11-05。一行跨这两个版本时取较晚的 2026-11-05。不是系统测试、总集验证或上线日。久新行不计入。

2026-10-22 晚拍板：内容管理、可视化管理给运维人员用。第 4 项门户四页给最终普通用户用，不是同一批页面，两边的叶都保留。内容菜单与现网用词仍在方案里收口。

## 技术方案

| 草案号       | 子项                       | 监管人 | 仓                   | 依赖                          | 可对端                                         | 开始时间 | 完成日期要求 |
| --------- | ------------------------ | --- | ------------------- | --------------------------- | ------------------------------------------- | ---- | ------ |
| WBS-03-00 | 技术方案设计：`SYSINT-SCHEME-03-L01` | 淮政玮 | `gkx-orchestration` | 无。已开工的基础数据叶不回退，也不把本行追进它们的依赖 | 五段写在 [技术方案](./技术方案.md)。2026-10-23 改回处理中 | 无开始时间 | 2026-11-05 |

## 基础数据管理（进行中，已有任务）

技术链、科研机构、人才不在本块。专家知识、全要素图谱 overlay、门户回写不在本表。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-09 | overlay 边界与落库。`CMS-JX-OVERLAY-A5-L01`（ready_to_sign）、`CMS-JX-OVERLAY-DDL-L01`（ready_to_sign） | 徐滕强 | A5 在 `gkx-orchestration`；DDL 在 `lumen-svc-platform` | 保持注册表现状 | 读写边界和独立 schema 可签收。写侧叶继续依赖 DDL，不另做一套库 | 无开始时间 | 2026-11-05 |
| WBS-03-10 | 企业。写侧 `CMS-JX-ENT-CRUD-L01`、`CMS-JX-ENT-NEWS-L01`、`CMS-JX-ENT-SZ-L01`；只读 `CMS-JX-ENT-LIST-L01`、`CMS-JX-ENT-PRODUCT-L01`。均 integration | 徐滕强（LIST、PRODUCT、CRUD 已填）。NEWS、SZ 本次注册表未返回监管人 | `lumen-svc-platform` | 写侧依赖 `CMS-JX-OVERLAY-DDL-L01` | 对端能按集群内接口做企业读写。列表、详情、资讯、深圳专项可调 | 无开始时间 | 2026-10-19 |
| WBS-03-11 | 产品链。写侧 `CMS-JX-PROD-CRUD-L01`、`CMS-JX-IND-CUSTOM-L01`、`CMS-JX-PROD-NEWS-L01`、`CMS-JX-PROD-SZ-L01`；只读 `CMS-JX-IND-TREE-L01`、`CMS-JX-IND-LINK-L01`。均 integration | 分类树、环节只读为徐滕强。四条写侧本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能读标准分类与环节，能写产品、自定义分类、产业资讯、区域名录 | 无开始时间 | 2026-10-19 |
| WBS-03-12 | 政策。写侧 `CMS-JX-POL-CRUD-L01`；只读 `CMS-JX-POL-EXPIRED-L01`。均 integration | 已失效列表为徐滕强。写侧本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能写政策条目并查已失效列表。列表/详情仍在 backlog，不在本叶 | 无开始时间 | 2026-11-05 |
| WBS-03-13 | 产业服务机构。写侧 `CMS-JX-SVC-CRUD-L01`、`CMS-JX-SVC-NEWS-L01`、`CMS-JX-SVC-SZ-L01`；只读 `CMS-JX-SVC-LIST-L01`。均 integration | LIST、NEWS 为徐滕强。CRUD、SZ 本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能做服务机构列表与写侧、资讯、深圳专项 | 无开始时间 | 2026-11-05 |
| WBS-03-14 | 跨对象批量只读。`CMS-JX-BULK-L01`（integration） | 徐滕强 | `lumen-svc-platform` | 保持注册表现状 | 对端能按一批实体取基础信息 | 无开始时间 | 2026-11-05 |
| WBS-03-16 | 政策列表 / 详情 / 下拉。`CMS-JX-POL-LIST-L01`（backlog） | 淮政玮 | `lumen-svc-platform` | 保持注册表现状：`CMS-JX-INT-DESIGN-L01`。不并进 WBS-03-12 | 对端能按集群内只读接口查政策列表、详情和关键词下拉。数据源是 DWD 政策真源 | 无开始时间 | 2026-11-05 |
| WBS-03-17 | 企业基础档案。`CMS-JX-ENT-PROFILE-L01`（backlog） | 徐滕强 | `lumen-svc-platform` | 保持注册表现状：`CMS-JX-ENT-LIST-L01`。2026-10-15 笔记写明顺延，本行仍计入，不改成已取消 | 按企业业务 ID 返回基础档案只读字段。集群内暴露，不另开 Ingress | 无开始时间 | 2026-10-19 |

基础数据是接口，不单开菜单叶。菜单若挂在内容管理上，随 WBS-03-01～04 配置。用户权限不写进上面各叶，见文末 WBS-03-18。

## 内容管理（智树前端 + 智树后端）

`PORTAL-CMS-FIELD-API-L01`（in_progress，监管淮政玮）是字段和读接口的定义单。它已触发指标核对与四条回写定义，那些单不把本单写成前置。契约原文写「任欢维护正文」。按 2026-10-22 定稿，这些菜单的页面和接口都由智树做，不再交给久新做前端。

定义单保持原 ID 和状态，不另开第二张回写叶。内容与可视化按技术方案一行一个任务。基础数据写侧（WBS-03-10～14）不充当这些菜单。指标行分别依赖四张核对单：`PORTAL-CMS-METRIC-COVER-ENT-L01`、`PORTAL-CMS-METRIC-COVER-CHAIN-L01`、`PORTAL-CMS-METRIC-COVER-POL-L01`、`PORTAL-CMS-METRIC-COVER-SVC-L01`。原 `PORTAL-CMS-METRIC-COVER-L01` 已 blocked，不再执行。对齐还没有。

有 CMS 正文的菜单（WBS-03-01a、03-02a、03-03a）共用下一行的控件和表单框架，不各做一套编辑页。政策扶持没有 CMS 字段，不走这套表单。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-15 · `SYSINT-03-15-L01` | 前端架构：CMS 公共控件选型、设计、开发；CMS 字段增删改查表单编辑页的通用框架 | 孔东 | `lumen-ui-topic` | 控件用仓内 Arco，不另引组件库。字段形状以四份门户 CMS 契约为准。2026-10-23 去掉对 `SYSINT-SCHEME-03-L01` 的依赖 | 企业、产业全景、专题服务的正文编辑都套这个框架：列表、新建、编辑、发布。富文本、名单、时间线、按产业切换能复用。政策扶持不做出 CMS 表单 | 无开始时间 | 2026-11-05 |

### WBS-03-01 企业发展

契约 [PORTAL-CMS-企业发展.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-企业发展.md) 已确认。页面：`overview`、`key-pano`、`star`、`shenzhen`。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-01a · `SYSINT-03-01A-L01` | 运营正文·前端。CMS：`star_roster_item`、`star_selection_standard`、`star_product_panorama`、`star_tech_narrative`、`star_team_strength`、`star_scientist_ratio`、`star_story`、`key_chain_structure`、`key_enterprise_set`、`sz_enterprise_intro`、`sz_focus_set`、`display_name_alias`。`overview` 无 CMS。页面：列表/编辑/发布，套 WBS-03-15 表单框架 | 孔东（2026-10-23 前端线定孔东） | `lumen-ui-topic` | `SYSINT-SCHEME-03-L01`。WBS-03-15。Java 运营写接口拆 `SYSINT-03-01A-JAVA-L01`（同日拆叶），两叶经 PORTAL-CMS-企业发展.md 已确认契约握手 | 智树页面可编、可发、可读已发布块。法定名称走主数据，别名标明非法定名。专利数和研发占比不写进 HTML。菜单相对路径进统一用户中心 | 无开始时间 | 2026-11-05 |
| WBS-03-01a-JAVA · `SYSINT-03-01A-JAVA-L01` | 运营正文·Java 运营写接口。gkxlumen-cms 新增 12 个 content_type 的 list/create/update/publish；正文落 `gkxlumenx_cms`（徐滕强 2026-10-23 拍板，A5 已冻结库）；真源零写；操作写 cms_op_audit；OpenAPI + 示例入 handoff 供前端叶联调 | 徐滕强 | `lumen-svc-platform`（`gkxlumen-cms`） | `SYSINT-SCHEME-03-L01`。契约 PORTAL-CMS-企业发展.md 已确认 | 对端（前端叶）能按契约完成 12 类正文编辑发布。不复用 `/api/open/cms/v1/*` 机器接口当页面接口 | 无开始时间 | 2026-11-05 |
| WBS-03-01b · `SYSINT-03-01B-L01` | 指标区块。契约点名、COVER 未完成，不算已对齐：`M_ENT_TOTAL_COUNT`、`M_ENT_REGIONAL_COUNT`、`M_ENT_RESEARCHER_COUNT`、`M_ENT_KEY_NODE_COUNT`、`M_ENT_KEYPANO_QUAL_DISTRIBUTION`、`M_ENT_KEYPANO_DOMAIN_SUMMARY`、`M_ENT_KEY_TOTAL`、`M_ENT_STAR_ENTERPRISE_COUNT`、`M_ENT_RD_INVESTMENT_RATIO`、`M_ENT_SZ_COUNT`。缺口：历年总数趋势、专利数、深圳历年趋势、领域个数、规模、上市数、国企数 | 徐滕强 | 同上，算法在 `lumen-algo-py` | `PORTAL-CMS-METRIC-COVER-ENT-L01`（监管唐绍祖）。核对未完成前缺口保持空态 | 已有 ID 走指标服务。缺口不手填进 CMS，不用相邻指标顶替 | 无开始时间 | 2026-10-19 |
| WBS-03-01c · `SYSINT-03-01C-L01` | 非 CMS 生成。链上瓶颈解读、生态合作摘要走大模型。图谱边不从 CMS 画。生成接口路径还没有 | 徐滕强 | 专题前端、`lumen-algo-py` | 契约 §1.2、§1.3。边的正式口径仍是 Q040 | 生成失败只隐藏文案。不补假节点，不设 `star_ecosystem_note` | 无开始时间 | 2026-10-19 |
| WBS-03-01d | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-ENT-L01`（ready_to_sign）所列 12 个 content_type | 徐滕强 | 定义单在 `gkx-orchestration`。实现等会签后定仓 | 该定义单 `done` 且架构师会签允许写入 DWD。指标、LLM 摘要、图谱边不回写 | 只落 `publish_status=published`。没有现成表的保持缺口，不新编表名 | 无开始时间 | 2026-10-19 |

### WBS-03-02 产业全景

契约文件名是专题全景，[PORTAL-CMS-专题全景.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题全景.md) 仍是草案。页面：`panorama`、`news`、`overview`。菜单用词先按本行，不把「产业概况」另开一叶。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-02a · `SYSINT-03-02A-L01`（前端）+ `SYSINT-03-02A-JAVA-L01`（Java，2026-10-24 拆叶） | 运营正文。`pano_industry_intro`、`pano_dev_history`、`pano_sz_feature`、`pano_cluster_effect`、`pano_competitive_position`。节点简介和市场规模文案本轮不进 CMS | 前端孔东、Java 徐滕强（2026-10-24 与李伟沟通，产业链 CMS 需求前端线孔东、后端徐滕强；李伟不再监管） | `lumen-ui-topic`、专题 Java | WBS-03-15。契约 PORTAL-CMS-专题全景.md 2026-10-24 已确认。2026-10-23 去掉对 `SYSINT-SCHEME-03-L01` 的依赖 | 智树页面可编已发布正文。编辑页套通用表单框架。正文不内嵌企业数。菜单相对路径进统一用户中心 | 无开始时间 | 2026-11-05 |
| WBS-03-02b · `SYSINT-03-02B-L01` | 指标与图谱数字。契约点名、对齐还没有：`M_CHAIN_ENTERPRISE_COUNT`、`M_CHAIN_INSTITUTION_COUNT`、`M_CHAIN_NODE_COUNT`、`M_CHAIN_SZ_ENTERPRISE_COUNT`、`M_CHAIN_SZ_INSTITUTION_COUNT`、`M_CHAIN_GLOBAL_REGION_COUNT`、`M_CHAIN_NATIONAL_REGION_COUNT`。深圳各区计数是缺口。节点和边不进 CMS。读图不在本叶新做 | 徐滕强（2026-10-24 与李伟沟通接管；李伟不再监管） | 同上，算法在 `lumen-algo-py`。读图主路径不在本叶 | `PORTAL-CMS-METRIC-COVER-CHAIN-L01` | 已有 ID 走指标服务。区级缺口空态。读图归 WBS-03-06 与第 7 项 | 无开始时间 | 2026-11-05 |
| WBS-03-02c · `SYSINT-03-02C-L01` | 产业资讯。不进 CMS。读 `dwd_industry_chain_news_info`，按 `industry_code` 过滤 | 徐滕强（2026-10-24 与李伟沟通接管；李伟不再监管） | 专题 Java 只读 | 客户决策清单 2026-08-25 该表「禁止业务使用」未解除则不上屏 | 有记录则按发布时间倒序。无记录事件线为空，不从其他产业补，不用大模型生成 | 无开始时间 | 2026-11-05 |
| WBS-03-02d | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-CHAIN-L01`（ready_to_sign）五个 `pano_*`。资讯表禁止用 CMS 覆盖 | 徐滕强（回写定义单监管人） | 定义单在 `gkx-orchestration` | 该定义单 `done` 且架构师会签 | 只回写已发布的五个正文块。不改 2026-08-25 对资讯表的记录 | 无开始时间 | 2026-11-05 |

### WBS-03-03 专题服务

契约 [PORTAL-CMS-专题服务.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题服务.md) 仍是草案。页面：`global`、`industry`、`region`、`tech`、`shenzhen`。CMS 只有业务介绍一处。

| 草案号        | 子项                                                                                                                 | 监管人                   | 仓                        | 依赖                                                        | 可对端                                             | 开始时间 | 完成日期要求 |
| ---------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------ | --------------------------------------------------------- | ----------------------------------------------- | ---- | ------ |
| WBS-03-03a · `SYSINT-03-03A-L01` | 运营正文。仅 `svc_business_domain.body_html`，绑定 `org_id` 与 `industry_id`                                                 | 徐滕强                   | `lumen-ui-topic`、专题 Java | WBS-03-15。契约草案确认前不改字段。2026-10-23 去掉对 `SYSINT-SCHEME-03-L01` 的依赖 | 智树页面只编这一处 HTML。编辑页套通用表单框架。法定名称、领导人、名次、分数不进正文。菜单相对路径进统一用户中心 | 无开始时间 | 2026-11-05 |
| WBS-03-03b · `SYSINT-03-03B-L01` | 指标与主数据。全球总数/类型/规模，环节机构数，区域分布，技术力前 30（`M_SVC_ORG_TECH_SCORE`），深圳总数/类型/领域/区域，重点机构规模。历年趋势无单独 ID，记缺口。名称、成立时间、领导人走机构主数据 | 徐滕强                   | 同上，算法在 `lumen-algo-py`   | `PORTAL-CMS-METRIC-COVER-SVC-L01`。技术力权重仍是 Q-SVCCHAIN-01 | 已有 ID 走指标服务。CMS 不另维护重点名单，不覆盖法定名称                | 无开始时间 | 2026-11-05 |
| WBS-03-03c | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-SVC-L01`（ready_to_sign），只回写 `svc_business_domain`                        | 徐滕强（回写定义单监管人。页面仍归侯佳伟） | 定义单在 `gkx-orchestration` | 该定义单 `done` 且架构师会签                                        | 只落已发布的业务介绍。数量、类型、规模、区域、技术力、重点名单不回写              | 无开始时间 | 2026-11-05 |

### WBS-03-04 政策扶持

契约 [PORTAL-CMS-政策扶持.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md) 写明没有 CMS 字段。页面：`stats`、`map`、`coverage`、`rank`、`news`、`shenzhen`。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-04a | 确认无 CMS、无正文读接口、不回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-POL-L01`（claimed） | 淮政玮 | `gkx-orchestration` | 该定义单收口。不新造政策富文本 | 可对端是这份确认。不另做内容管理后台 | 无开始时间 | 2026-11-05 |
| WBS-03-04b · `SYSINT-03-04B-L01` | 指标页。力度排名用 `M_POLICY_INTENSITY_SCORE`。全国/省/市数量与连续性、发布密度、节点覆盖、深圳数量/趋势/各区/节点覆盖都是缺口。`M_POLICY_OPPORTUNITY_COUNT` 不顶替数量。真实 ADS 未接前允许 mock | 淮政玮 | `lumen-algo-py` | `PORTAL-CMS-METRIC-COVER-POL-L01`（监管淮政玮）。读接口是 `SYSINT-04-05-API-L01`。ADS 需求见 WBS-03-04d，不阻塞 | 有 ID 的走指标服务。缺口空态，CMS 不填名次和分数。契约不改 | 无开始时间 | 2026-11-05 |
| WBS-03-04c · `SYSINT-03-04C-L01` | 最新政策与深圳最新政策的读接口。字段：`policy_id`、`title`、`publish_time`、`region_name`、`source_url`。无主数据时允许 mock | 淮政玮 | 专题 Java 只读 | 不重做 WBS-03-12，也不把 `CMS-JX-POL-LIST-L01` 并进本叶。结果供 `SYSINT-04-05-API-L01` | 有记录或为空。不新造运营导语。契约不改 | 无开始时间 | 2026-11-05 |
| WBS-03-04d · `SYSINT-POL-ADS-REQ-L01` | 政策扶持读数对 ADS 的需求。只写需求，不实现加工。不进门户闭环 | 淮政玮 | `gkx-orchestration` | 无。页面与 `SYSINT-04-05-API-L01` 先 mock | 列出力度排名、十条缺口、时间线五个字段的建议落点。不生成 CDC | 无开始时间 | 还没有 |

## 可视化（运维人员。不是门户四页）

使用人是运维人员。不是第 4 项门户上给普通用户看的那四页。

| 草案号       | 子项           | 监管人 | 仓                                        | 依赖                                 | 可对端                             | 开始时间 | 完成日期要求 |
| --------- | ------------ | --- | ---------------------------------------- | ---------------------------------- | ------------------------------- | ---- | ------ |
| WBS-03-05 · `SYSINT-03-05-L01` | 企业发展可视化（前后端） | 徐滕强 | `lumen-ui-topic`、专题 Java、`lumen-algo-py` | 不复用基础数据写侧，也不复用 WBS-03-01 的运营页。2026-10-23 去掉对 `SYSINT-SCHEME-03-L01` 的依赖 | 该可视化菜单主路径可点，缺数为空态。菜单相对路径进统一用户中心 | 无开始时间 | 2026-10-19 |
| WBS-03-06 · `SYSINT-03-06-L01` | 产业全景可视化（前后端） | 孔东（2026-10-26 前端线字段修正，原移交 note 落字段） | 同上                                       | 同上                                 | 同上                              | 无开始时间 | 2026-10-19 |
| WBS-03-07 · `SYSINT-03-07-L01` | 专题服务可视化（前后端） | 黄敬洲 | 同上                                       | 同上                                 | 同上                              | 无开始时间 | 2026-11-05 |
| WBS-03-08 · `SYSINT-03-08-L01` | 政策扶持可视化（前后端）。指标与需规 93–98 同一套，不另开清单任务 | 淮政玮。注册表监管人为孔东 | 同上                                       | `SYSINT-04-05-API-L01`。允许 mock | 可视化菜单主路径可点，缺数为空态。菜单相对路径进统一用户中心 | 无开始时间 | 2026-11-05 |

## 统一用户中心（2026-10-22 晚补行）

各页开发叶仍写自己的相对路径。本行只做注册和用户权限。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 | 开始时间 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-03-18 · `SYSINT-03-18-L01` | 本项菜单注册与用户权限。内容管理四菜单、可视化四菜单 | 淮政玮。2026-10-22 纪要未点名，2026-10-23 指定 | 统一用户中心配置。业务仓不写主机名 | 各菜单叶负责自己的相对路径。2026-10-23 去掉对 `SYSINT-SCHEME-03-L01` 的依赖 | 八个菜单以相对路径可见，对应用户登录后能进。地址不写 `https://next.itic-sci.com/`。八个菜单的相对路径仍还没有 | 无开始时间 | 2026-11-05 |

不进本表：专家知识、全要素图谱 overlay、基础数据里其余 backlog（各类 TopN、全景包、名录、政策统计、失效通知）。政策列表与企业档案见 WBS-03-16、03-17。可视化不再拆给久新做前端。
