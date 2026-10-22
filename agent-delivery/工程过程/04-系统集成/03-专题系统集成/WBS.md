# WBS 草案 · 专题系统集成

> 2026-10-22 梳理。方案任务 `系统集成技术方案_专题系统集成` **未建、未签收**。  
> 基础数据管理的叶 **已经在 registry**，状态为当日快照。本表收录进行中的叶（`integration` / `ready_to_sign`），不新开 ID，不把未建的方案任务追进它们的 `depends_on`。`backlog` 与已 `done` 的设计单不计入。  
> 内容管理、可视化仍是签收后才建的叶。菜单配置写进那些叶的完成条件。内容菜单名称未收口前，用定稿规约的来稿用词。  
> 表中「仓」只是建议，最终由该行监管人决定。已经在 registry 里的叶，仓以注册表现状为准。

方案要先写死两句，再允许建下面「待建」叶：四个内容菜单与现网用词的对应；可视化四菜单和门户四块展示页是不是同一套页面。若是同一套，删掉第 4 项里重复的四叶，只保留门户挂载条件。

## 技术方案

| 草案号       | 子项                       | 监管人 | 仓                   | 依赖                          | 可对端                                         |
| --------- | ------------------------ | --- | ------------------- | --------------------------- | ------------------------------------------- |
| WBS-03-00 | 技术方案设计：`系统集成技术方案_专题系统集成` | 淮政玮 | `gkx-orchestration` | 无。已开工的基础数据叶不回退，也不把本行追进它们的依赖 | 五段写在 [技术方案](./技术方案.md)。草案，未签收。内容管理和可视化叶仍等签收 |

## 基础数据管理（进行中，已有任务）

技术链、科研机构、人才不在本块。专家知识、全要素图谱 overlay、门户回写不在本表。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 |
|---|---|---|---|---|---|
| WBS-03-09 | overlay 边界与落库。`CMS-JX-OVERLAY-A5-L01`（ready_to_sign）、`CMS-JX-OVERLAY-DDL-L01`（ready_to_sign） | 徐滕强 | A5 在 `gkx-orchestration`；DDL 在 `lumen-svc-platform` | 保持注册表现状 | 读写边界和独立 schema 可签收。写侧叶继续依赖 DDL，不另做一套库 |
| WBS-03-10 | 企业。写侧 `CMS-JX-ENT-CRUD-L01`、`CMS-JX-ENT-NEWS-L01`、`CMS-JX-ENT-SZ-L01`；只读 `CMS-JX-ENT-LIST-L01`、`CMS-JX-ENT-PRODUCT-L01`。均 integration | 徐滕强（LIST、PRODUCT、CRUD 已填）。NEWS、SZ 本次注册表未返回监管人 | `lumen-svc-platform` | 写侧依赖 `CMS-JX-OVERLAY-DDL-L01` | 对端能按集群内接口做企业读写。列表、详情、资讯、深圳专项可调 |
| WBS-03-11 | 产品链。写侧 `CMS-JX-PROD-CRUD-L01`、`CMS-JX-IND-CUSTOM-L01`、`CMS-JX-PROD-NEWS-L01`、`CMS-JX-PROD-SZ-L01`；只读 `CMS-JX-IND-TREE-L01`、`CMS-JX-IND-LINK-L01`。均 integration | 分类树、环节只读为徐滕强。四条写侧本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能读标准分类与环节，能写产品、自定义分类、产业资讯、区域名录 |
| WBS-03-12 | 政策。写侧 `CMS-JX-POL-CRUD-L01`；只读 `CMS-JX-POL-EXPIRED-L01`。均 integration | 已失效列表为徐滕强。写侧本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能写政策条目并查已失效列表。列表/详情仍在 backlog，不在本叶 |
| WBS-03-13 | 产业服务机构。写侧 `CMS-JX-SVC-CRUD-L01`、`CMS-JX-SVC-NEWS-L01`、`CMS-JX-SVC-SZ-L01`；只读 `CMS-JX-SVC-LIST-L01`。均 integration | LIST、NEWS 为徐滕强。CRUD、SZ 本次未返回监管人 | `lumen-svc-platform` | 写侧依赖 DDL | 对端能做服务机构列表与写侧、资讯、深圳专项 |
| WBS-03-14 | 跨对象批量只读。`CMS-JX-BULK-L01`（integration） | 徐滕强 | `lumen-svc-platform` | 保持注册表现状 | 对端能按一批实体取基础信息 |

基础数据是接口，不单开菜单叶。菜单若挂在内容管理上，随 WBS-03-01～04 配置。

## 内容管理（智树前端 + 智树后端）

`PORTAL-CMS-FIELD-API-L01`（in_progress，监管淮政玮）是字段和读接口的定义单。它已触发指标核对与四条回写定义，那些单不把本单写成前置。契约原文写「任欢维护正文」。按 2026-10-22 定稿，这些菜单的页面和接口都由智树做，不再交给久新做前端。

定义单保持原 ID 和状态。下面是草稿细项，今天不新建 registry 任务。方案未签收前不派编码。确认时按 [规约 §7](../../../系统集成整体过程规约.md) 合并过细的行：确认后一行一个任务。快照分别调研设计与开发，再给出这一级工作包的整体百分比。基础数据写侧（WBS-03-10～14）不充当这些菜单。

有 CMS 正文的菜单（WBS-03-01a、03-02a、03-03a）共用下一行的控件和表单框架，不各做一套编辑页。政策扶持没有 CMS 字段，不走这套表单。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 |
|---|---|---|---|---|---|
| WBS-03-15 | 前端架构：CMS 公共控件选型、设计、开发；CMS 字段增删改查表单编辑页的通用框架 | 孔东 | `lumen-ui-topic` | 方案任务。控件用仓内 Arco，不另引组件库。字段形状以四份门户 CMS 契约为准 | 企业、产业全景、专题服务的正文编辑都套这个框架：列表、新建、编辑、发布。富文本、名单、时间线、按产业切换能复用。政策扶持不做出 CMS 表单 |

### WBS-03-01 企业发展

契约 [PORTAL-CMS-企业发展.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-企业发展.md) 已确认。页面：`overview`、`key-pano`、`star`、`shenzhen`。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 |
|---|---|---|---|---|---|
| WBS-03-01a | 运营正文。CMS：`star_roster_item`、`star_selection_standard`、`star_product_panorama`、`star_tech_narrative`、`star_team_strength`、`star_scientist_ratio`、`star_story`、`key_chain_structure`、`key_enterprise_set`、`sz_enterprise_intro`、`sz_focus_set`、`display_name_alias`。`overview` 无 CMS | 徐滕强 | `lumen-ui-topic`、专题 Java | 方案任务。WBS-03-15。字段以已确认契约为准 | 智树页面可编、可发、可读已发布块。编辑页套通用表单框架。法定名称走主数据，别名标明非法定名。专利数和研发占比不写进 HTML。菜单相对路径进统一用户中心 |
| WBS-03-01b | 指标区块。已对齐：`M_ENT_TOTAL_COUNT`、`M_ENT_REGIONAL_COUNT`、`M_ENT_RESEARCHER_COUNT`、`M_ENT_KEY_NODE_COUNT`、`M_ENT_KEYPANO_QUAL_DISTRIBUTION`、`M_ENT_KEYPANO_DOMAIN_SUMMARY`、`M_ENT_KEY_TOTAL`、`M_ENT_STAR_ENTERPRISE_COUNT`、`M_ENT_RD_INVESTMENT_RATIO`、`M_ENT_SZ_COUNT`。缺口：历年总数趋势、专利数、深圳历年趋势、领域个数、规模、上市数、国企数 | 徐滕强 | 同上，算法在 `lumen-algo-py` | `PORTAL-CMS-METRIC-COVER-L01` 企业段（claimed，监管唐绍祖）。核对未完成前缺口保持空态 | 已有 ID 走指标服务。缺口不手填进 CMS，不用相邻指标顶替 |
| WBS-03-01c | 非 CMS 生成。链上瓶颈解读、生态合作摘要走大模型。图谱边不从 CMS 画 | 徐滕强 | 专题前端、`lumen-algo-py` | 契约 §1.2、§1.3。边的正式口径仍是 Q040 | 生成失败只隐藏文案。不补假节点，不设 `star_ecosystem_note` |
| WBS-03-01d | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-ENT-L01`（ready_to_sign）所列 12 个 content_type | 徐滕强 | 定义单在 `gkx-orchestration`。实现等会签后定仓 | 该定义单 `done` 且架构师会签允许写入 DWD。指标、LLM 摘要、图谱边不回写 | 只落 `publish_status=published`。没有现成表的保持缺口，不新编表名 |

### WBS-03-02 产业全景

契约文件名是专题全景，[PORTAL-CMS-专题全景.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题全景.md) 仍是草案。页面：`panorama`、`news`、`overview`。菜单用词先按本行，不把「产业概况」另开一叶。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 |
|---|---|---|---|---|---|
| WBS-03-02a | 运营正文。`pano_industry_intro`、`pano_dev_history`、`pano_sz_feature`、`pano_cluster_effect`、`pano_competitive_position`。节点简介和市场规模文案本轮不进 CMS | 李伟 | `lumen-ui-topic`、专题 Java | 方案任务。WBS-03-15。契约草案确认前不改字段 | 智树页面可编已发布正文。编辑页套通用表单框架。正文不内嵌企业数。菜单相对路径进统一用户中心 |
| WBS-03-02b | 指标与图谱数字。`M_CHAIN_ENTERPRISE_COUNT`、`M_CHAIN_INSTITUTION_COUNT`、`M_CHAIN_NODE_COUNT`、`M_CHAIN_SZ_ENTERPRISE_COUNT`、`M_CHAIN_SZ_INSTITUTION_COUNT`、`M_CHAIN_GLOBAL_REGION_COUNT`、`M_CHAIN_NATIONAL_REGION_COUNT`。深圳各区计数是缺口。节点和边不进 CMS | 李伟 | 同上，算法在 `lumen-algo-py`。读图主路径不在本叶 | `PORTAL-CMS-METRIC-COVER-L01` 专题全景段 | 已有 ID 走指标服务。区级缺口空态。读图归 WBS-03-06 与第 7 项 |
| WBS-03-02c | 产业资讯。不进 CMS。读 `dwd_industry_chain_news_info`，按 `industry_code` 过滤 | 李伟 | 专题 Java 只读 | 客户决策清单 2026-08-25 该表「禁止业务使用」未解除则不上屏 | 有记录则按发布时间倒序。无记录事件线为空，不从其他产业补，不用大模型生成 |
| WBS-03-02d | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-CHAIN-L01`（ready_to_sign）五个 `pano_*`。资讯表禁止用 CMS 覆盖 | 徐滕强（回写定义单监管人。页面仍归李伟，不两人共管一叶） | 定义单在 `gkx-orchestration` | 该定义单 `done` 且架构师会签 | 只回写已发布的五个正文块。不改 2026-08-25 对资讯表的记录 |

### WBS-03-03 专题服务

契约 [PORTAL-CMS-专题服务.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题服务.md) 仍是草案。页面：`global`、`industry`、`region`、`tech`、`shenzhen`。CMS 只有业务介绍一处。

| 草案号        | 子项                                                                                                                 | 监管人                   | 仓                        | 依赖                                                        | 可对端                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------ | --------------------------------------------------------- | ----------------------------------------------- |
| WBS-03-03a | 运营正文。仅 `svc_business_domain.body_html`，绑定 `org_id` 与 `industry_id`                                                 | 徐滕强                   | `lumen-ui-topic`、专题 Java | 方案任务。WBS-03-15。契约草案确认前不改字段                                 | 智树页面只编这一处 HTML。编辑页套通用表单框架。法定名称、领导人、名次、分数不进正文。菜单相对路径进统一用户中心 |
| WBS-03-03b | 指标与主数据。全球总数/类型/规模，环节机构数，区域分布，技术力前 30（`M_SVC_ORG_TECH_SCORE`），深圳总数/类型/领域/区域，重点机构规模。历年趋势无单独 ID，记缺口。名称、成立时间、领导人走机构主数据 | 徐滕强                   | 同上，算法在 `lumen-algo-py`   | `PORTAL-CMS-METRIC-COVER-L01` 专题服务段。技术力权重仍是 Q-SVCCHAIN-01 | 已有 ID 走指标服务。CMS 不另维护重点名单，不覆盖法定名称                |
| WBS-03-03c | 已发布正文回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-SVC-L01`（ready_to_sign），只回写 `svc_business_domain`                        | 徐滕强（回写定义单监管人。页面仍归侯佳伟） | 定义单在 `gkx-orchestration` | 该定义单 `done` 且架构师会签                                        | 只落已发布的业务介绍。数量、类型、规模、区域、技术力、重点名单不回写              |

### WBS-03-04 政策扶持

契约 [PORTAL-CMS-政策扶持.md](../../../agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md) 写明没有 CMS 字段。页面：`stats`、`map`、`coverage`、`rank`、`news`、`shenzhen`。

| 草案号 | 子项 | 监管人 | 仓 | 依赖 | 可对端 |
|---|---|---|---|---|---|
| WBS-03-04a | 确认无 CMS、无正文读接口、不回写 DWD。定义单 `PORTAL-CMS-DWD-WRITEBACK-POL-L01`（claimed） | 淮政玮 | `gkx-orchestration` | 该定义单收口。不新造政策富文本 | 可对端是这份确认。不另做内容管理后台 |
| WBS-03-04b | 指标页。力度排名用 `M_POLICY_INTENSITY_SCORE`。全国/省/市数量与连续性、发布密度、节点覆盖、深圳数量/趋势/各区/节点覆盖都是缺口。`M_POLICY_OPPORTUNITY_COUNT` 不顶替数量 | 淮政玮 | `lumen-ui-topic`、专题 Java、`lumen-algo-py` | `PORTAL-CMS-METRIC-COVER-L01` 政策段 | 有 ID 的走指标服务。缺口空态，CMS 不填名次和分数。菜单相对路径进统一用户中心 |
| WBS-03-04c | 最新政策与深圳最新政策。走政策主数据：`policy_id`、`title`、`publish_time`、`region_name`、`source_url` | 淮政玮 | 专题 Java 只读 | 列表/详情/失效仍是基础数据接口。本叶不重做 WBS-03-12，也不把 backlog 的政策列表算进来 | 时间线有记录或为空。不新造运营导语 |

## 可视化（待建，方案签收后）

| 草案号       | 子项           | 监管人 | 仓                                        | 依赖                                 | 可对端                             |
| --------- | ------------ | --- | ---------------------------------------- | ---------------------------------- | ------------------------------- |
| WBS-03-05 | 企业发展可视化（前后端） | 徐滕强 | `lumen-ui-topic`、专题 Java、`lumen-algo-py` | 方案任务。不复用基础数据写侧，也不复用 WBS-03-01 的运营页 | 该可视化菜单主路径可点，缺数为空态。菜单相对路径进统一用户中心 |
| WBS-03-06 | 产业全景可视化（前后端） | 李伟  | 同上                                       | 同上                                 | 同上                              |
| WBS-03-07 | 专题服务可视化（前后端） | 黄敬洲 | 同上                                       | 同上                                 | 同上                              |
| WBS-03-08 | 政策扶持可视化（前后端） | 淮政玮 | 同上                                       | 同上                                 | 同上                              |

不进本表：专家知识、全要素图谱 overlay、基础数据里仍为 backlog 的只读与回调（政策列表、企业档案、各类 TopN、全景包、名录、政策统计、失效通知）。可视化不再拆给久新做前端。
