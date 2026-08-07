# 产业链域（CHAIN）DWD 表设计 — 业务需求驱动版（v5）

> 任务：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 责任人：`[human:李伟]`（架构师）  
> 执行角色：`architect-agent`  
> 日期：2026-07-31  
> 最近修订：2026-08-07（对齐门户 L0/L1、历程阶段、诊断 severity；修订模型结果指纹）  
> 状态：设计草案（**Q053 已冻结**）；待数据 Lead / 指标 Owner 会签后可作结构灌数依据；完整生产仍受资讯/投融资/ENT 营收等缺口约束  
> 需求真源：`catalog-topic-industry.yaml`（IC-01～IC-43）及两份 `bid-reference` Markdown  
> 产品对齐：`DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806`、`DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806`、`DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807`  
> 设计口径：只考虑业务需求和合理分层，不以当前 ODS 字段及数据量限制目标结构  
> 数据链路：**ODS → DWD → ADS**，无独立 DWM 库；介绍/历程另走 **CMS**

---

## 1. v5 结论

### 1.1 相对 v4 的修正

v5 保留 v4 的标准实体、关系、事件和原子事实设计方向，并完成以下修正：

1. 删除全部 DWM 设计和引用，统一为 `ODS → DWD → ADS`；
2. 将区域统计、企业统计、同比、环比、排名和页面快照明确放入 ADS；
3. 七要素关系扩展为产业链、企业、科研机构、服务机构、人才、技术、政策，并兼容产品、专利；
4. 新增事件指标观测表，支撑浏览量、评论量、转发量等热点原始数据；
5. 新增实体/关系抽取结果表，保存 mention、span、三元组、模型版本和证据；
6. 将单一模型结果表拆为模型运行主表与模型结果明细表；
7. 明确投融资参与方是通用事件实体关系的扩展，禁止双写；
8. 补充表粒度、唯一键、更新策略、数据质量规则和 ODS 映射预期；
9. 将“完全覆盖”改为可验证的分层覆盖结论，不把 API、CMS、报告和推荐文案算作 DWD 能力。

### 1.1.1 2026-08-07 设计修订（相对 08-06）

1. `industry_chain` 增加 L0 产业挂载键 `industry_id` 与对象层级 `chain_tier`，对齐门户顶部产业选择器；
2. `industry_chain_milestone_event` 增加 `phase_*`（可选结构化旁路）；**门户发展历程以 CMS 为准**；
3. `industry_chain_model_result_detail` 增加 `severity_level`，承载诊断「瓶颈 ∧ severity=高 → 卡脖子」；
4. `result_fingerprint` 在 `result_type=rank` 时纳入 `rank_no`，避免同 run 多条排名撞防重键；
5. 明确图谱演进快照元数据归 ADS、节点简介读 DWD `node.description`、事件关系可冗余 `event_kind`；
6. **Q053 冻结**：平台 `chain_id`/`node_id`/`industry_id` = 供应方 INB 原文（见 `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md`）；
7. **产业市场规模**：平台默认为链下企业年报营收加总（仅企业），落 ADS；与 DWD 外部市场观测表分轨；
8. **产业介绍 / 产业发展历程**：门户真源均为 **CMS 录入**，非 ODS→DWD 灌数。

### 1.2 覆盖结论

v5 的目标是：

> 对 IC-01～IC-41 所需的产业链标准明细数据、关系、原子观测、事件、模型运行和模型原子结果提供结构基础；IC-42～IC-43 归业务库/CMS，不进入 DWD。

但“DWD 表结构具备承载能力”不等于“业务功能已经完成”。以下能力仍依赖其他层：

- API、消息队列、下载和前端查询：ADS + Java；
- 图结构分析：NebulaGraph + Python；
- 指标口径、阈值、权重、模型参数：`gkx_cfg`；
- 推荐文案、解决方案、报告正文：ADS/业务库/对象存储；
- 专题介绍和门户内容：CMS（**含产业介绍、发展历程**）；
- 企业、机构、人才、技术、政策主体属性：对应权威数据域。

---

## 2. 分层边界

### 2.1 DWD 应承载

- 产业链和节点标准实体（含 L0 `industry_id` / `chain_tier`）；
- 节点间上下游、供需、依赖、替代和协同关系；
- 产业链/节点与外部实体的标准关系；
- **外部导入**的市场原子观测（研报/市调等；不含平台默认「企业营收加总」市场规模）；
- 投融资、资讯事件（有源时）；
- **可选**结构化里程碑（门户历程正文在 CMS，不强制进 DWD）；
- 事件与实体关系；
- 资讯互动量等事件时序观测；
- 实体识别和关系抽取的可审计结果；
- 模型运行元数据；
- 模型评分、标签、排名、预测和因素贡献等原子结果。

### 2.2 ADS 应承载

- 企业数、机构数、人才数等聚合值；
- **产业市场规模（平台默认）**：Σ 链下企业年报营收（仅企业）→ `M_CHAIN_MARKET_SIZE`；不进 DWD `market_observation`；
- 全球、全国、深圳及各区分布；
- 同比、环比、增长率、占比和排名；
- 页面卡片和趋势图查询结构；
- 区域对比和综合评价结果；
- 机遇、布局和跃升路径推荐结果；
- 瓶颈解决方案和政策建议；
- 报告摘要及页面解释；
- **图谱结构快照与演进 diff 查询面**（`snapshot_id`、`chain_id`/`industry_id`、`valid_at`、nodes/edges 引用）；DWD 三张关系表仍为关系真源，ADS 不得另建永久边真源。

### 2.3 业务库/CMS 应承载

- **产业介绍**（产业链/L0 产业介绍正文、图文）：**CMS 录入为唯一真源**；
- **产业发展历程**（阶段划分、历程条目、图文时间轴）：**CMS 录入为门户展示真源**；
- 专题介绍和门户其他图文块；
- 人工发布、审核和内容版本；
- 专家知识录入和维护；
- 实体人工确认、消歧、合并、拆分和纠错审计；
- 分析任务状态和审批流；
- 报告正文、文件地址和下载记录；
- 用户收藏、订阅、评论及浏览记录；
- 模型参数编辑和策略配置。

禁止把 CMS 已录入的「产业介绍 / 发展历程」长文案再写入 DWD 形成双真源；DWD 至多保留结构化事件键或 CMS 外键引用（若后续对接需要），不得以 ODS 灌数覆盖 CMS 正文。

### 2.4 图数据库应承载

NebulaGraph 保存最终图查询结构。以下 DWD 表是关系型权威来源：

- `industry_chain_node_rel`
- `industry_chain_entity_rel`
- `industry_chain_event_entity_rel`

Python 负责从 DWD 投影到 NebulaGraph；不得同时维护第二套永久 MySQL 图谱边真源。

### 2.5 模型原子结果与 ADS 的判定边界

`industry_chain_model_result_detail` 只保存**单次模型运行、单个对象、单个指标或维度**的可复算原子结果。满足以下任一条件的输出不得进入 DWD：

1. 跨 `run_id` 汇总、跨对象 TopN 或面向页面的二次排序；
2. 已按产品阈值形成“推荐/不推荐”“重点招商”等页面结论；
3. 完整自然语言建议、解决方案、报告段落或页面解读；
4. 为单一 API、卡片或图表定制的宽表结构。

上述内容统一进入 ADS/业务库；ADS 必须保留 `run_id`、`result_id`、`metric_id`、`metric_version` 和 `calc_batch_id`，能够反向追溯到 DWD 原子结果。

---

## 3. 命名、主键和治理规范

### 3.1 表命名

物理数据库已经是 `gkxlumenx_dwd` 时，表名不重复添加 `dwd_` 前缀，统一使用 `industry_chain_*`。

### 3.2 稳定业务主键

| 对象 | 主键 | 规则 |
|---|---|---|
| 产业（L0） | `industry_id VARCHAR(64)` | **INB 根码原文**（如 `INB1303`）；与门户/对比篮一致；见 Q053 / `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md` |
| 产业链 | `chain_id VARCHAR(64)` | **INB 升格为平台主键**；L0 与 `industry_id` 同值；与 `chain_code` 同值（Wave1）；L0 行可满足 `industry_id = chain_id` |
| 节点 | `node_id VARCHAR(64)` | **节点 INB 原文**（如 `INB130301`）；与 `node_code` 同值 |
| 企业 | `enterprise_code VARCHAR(64)` | ENT 域权威键 |
| 机构 | `org_uid VARCHAR(64)` | ORG/SVC 域权威键 |
| 区域 | `region_code VARCHAR(20)` | 国标区划编码 |
| 指标 | `metric_id VARCHAR(64)` | 指标注册中心 ID |
| 模型 | `model_id VARCHAR(64)` | 模型注册中心 ID |
| 事件 | `event_id VARCHAR(64)` | 全域唯一；建议使用 `news:`、`invest:`、`milestone:` 前缀 |

供应方自增 ID 只能写入 `source_record_id`，不得直接作为平台跨表业务键。

跨域实体类型与权威键统一如下：

| `entity_type` | 权威键 | 权威数据域 |
|---|---|---|
| `chain` | `chain_id` | CHAIN |
| `enterprise` | `enterprise_code` | ENT |
| `institution` | `org_uid` | ORG |
| `service_institution` | `org_uid` | SVC/ORG |
| `talent` | `talent_uid` | TALENT（待平台主键表补登记） |
| `technology` | `tech_uid` | TECH（待平台主键表补登记） |
| `policy` | `policy_id` | POLICY |
| `product` | `product_uid` | PRODUCT（待平台主键表补登记） |
| `patent` | `patent_uid` | PATENT（待平台主键表补登记） |

`talent_uid`、`tech_uid`、`product_uid`、`patent_uid` 在平台主键表正式冻结前均属于开放项，不得用供应方自增 ID 替代。

临时数据仅允许使用带类型前缀的 Mock 键（例如 `talent:mock:*`），并在 `source_system='mock'` 下流转；不得将临时键用于生产跨域关联、Nebula VID 或对外 API。四类主键必须经平台架构评审后补入 `gkx-platform-business-keys.md`，再解除生产阻塞。

### 3.3 公共治理字段

所有 DWD 表统一包含：

| 字段 | 中文注释 | 类型 | 必填 | ODS 映射预期 |
|---|---|---|---|---|
| `id` | 物理自增主键 | `BIGINT` | 是 | 系统生成；不映射 ODS |
| `source_system` | 来源系统标识 | `VARCHAR(64)` | 是 | 来源系统标识；高置信 |
| `source_table` | 来源表名 | `VARCHAR(128)` | 是 | 来源表名；高置信 |
| `source_record_id` | 来源记录业务键或行键 | `VARCHAR(128)` | 是 | 来源记录业务键或行键；中置信 |
| `etl_batch_id` | 数据加工批次号 | `VARCHAR(64)` | 是 | 数据工厂批次；系统生成 |
| `data_version` | 来源数据或平台版本 | `VARCHAR(32)` | 是 | 来源数据版本或平台版本；中置信 |
| `valid_from` | 记录生效时间 | `DATETIME` | 是 | 来源业务有效期或平台接收时间；中置信 |
| `valid_to` | 记录失效时间 | `DATETIME` | 否 | 来源失效时间；低置信，可为空 |
| `is_deleted` | 逻辑删除标记 | `TINYINT` | 是 | 来源删除标记或 CDC 推导；低置信 |
| `created_time` | 平台创建时间 | `DATETIME` | 是 | 平台创建时间；系统生成 |
| `updated_time` | 平台更新时间 | `DATETIME` | 是 | 平台更新时间；系统生成 |
| `ext` | 扩展属性 JSON | `JSON` | 否 | 未预见字段；不得替代正式建模 |

Mock 数据必须为四个追溯字段提供显式占位值，例如：

- `source_system='mock'`
- `source_table='mock:<generator_name>'`
- `source_record_id='mock:<table>:<business_key>'`
- `etl_batch_id='mock_<date>_<batch>'`

禁止使用空字符串代替可追溯信息。

每个业务字段的 `ods_mapping_expectation` 以字段表中的“预期来源”和“置信度”表示。当前处于 ODS 未稳定阶段，统一标记：

```yaml
mapping_status: pending_ods
source_systems:
  - 待甲方 ODS 稳定
```

字段表中的映射列按以下规则序列化为血缘规约要求的结构；“映射备注”未单列时默认空字符串：

```yaml
ods_mapping_expectation:
  expected_from: "<字段表.预期来源>"
  confidence: "<字段表.置信度：高=high / 中=medium / 低=low / 系统=system>"
  note: ""
```

已知无直接 ODS 来源的模型、人工配置和系统生成字段，`expected_from` 必须明确写成“模型生成”“人工配置”或“系统生成”，不得伪造 ODS 表字段。

所有进入 `industry_chain_market_observation`、`industry_chain_event_metric_observation` 和 `industry_chain_model_result_detail` 的 `metric_id`，以及 `industry_chain_extraction_result.target_metric_id`，必须先在 `cfg_metric` 登记 D9 八件套：`metric_id`、中文名、口径定义、公式、源表、源系统、更新频率、版本。未登记或版本不匹配的记录必须被入库校验阻断。

算法及抽取结果表的公共追溯字段按以下规则填写：

| 表 | `source_system` | `source_table` | `source_record_id` | `valid_from` |
|---|---|---|---|---|
| `industry_chain_model_run` | `gkx-algorithm-platform` | `cfg_model_registry` | `run_id` | `started_time` |
| `industry_chain_model_result_detail` | 继承运行记录 | `industry_chain_model_run` | `result_id` | `COALESCE(completed_time, started_time)` |
| `industry_chain_extraction_result` | 输入文档所属系统 | 输入文档所在 DWD 表 | `document_id` | `COALESCE(completed_time, started_time)` |

模型多源输入的完整行级集合由 `industry_chain_model_run.input_snapshot_ref` 指向，不把多来源强行拼入单值 `source_table`。

---

## 4. v5 DWD 表总览

v5 推荐 14 张 DWD 表：

| 序号 | 表名 | 中文表名（表注释） | 用途简述 | 粒度 |
|---|---|---|---|---|
| 1 | `industry_chain` | 产业链标准信息表 | 保存 L0 产业与 L1+ 子链名录及基础属性（`industry_id`/`chain_tier`），作为统一挂载点 | 一条标准产业链/产业对象 |
| 2 | `industry_chain_node` | 产业链节点信息表 | 保存某条产业链包含的环节或节点，支撑全景图和上中下游展示 | 产业链内一个标准节点 |
| 3 | `industry_chain_node_rel` | 产业链节点关系表 | 保存节点之间的上下游、供需、依赖、替代等结构关系 | 一条节点间关系 |
| 4 | `industry_chain_entity_rel` | 产业链实体关系表 | 保存产业链或节点与企业、机构、人才、技术、政策、产品、专利等外部实体的归属或参与关系 | 产业链/节点与一个外部实体的一条关系 |
| 5 | `industry_chain_market_observation` | 产业链市场指标观测表 | 仅存外部导入的销量/价格/产值等原子观测；**平台「产业市场规模」为企业年报营收加总，落 ADS，不进本表** | 某链/节点/区域/指标/统计期的一次外部市场观测 |
| 6 | `industry_chain_investment_event` | 产业链投融资事件表 | 保存投融资、并购等资本事件本身，不含参与方角色明细 | 一次投融资事件 |
| 7 | `industry_chain_investment_participant` | 投融资事件参与方扩展表 | 保存投融资参与方的金额等扩展信息，角色关系复用事件实体关系表 | 投融资事件中的一个参与方扩展 |
| 8 | `industry_chain_news_event` | 产业链资讯事件表 | 保存产业资讯主数据，支撑热点资讯列表和资讯事件线 | 一条产业资讯事件 |
| 9 | `industry_chain_milestone_event` | 产业链里程碑事件表 | 可选结构化里程碑；**门户发展历程以 CMS 录入为准**，本表不承担历程正文 | 一条结构化里程碑事件（可选） |
| 10 | `industry_chain_event_entity_rel` | 产业事件实体关系表 | 保存事件与企业、机构、投资方、作者等实体之间的关系 | 一个事件与一个实体的一条关系 |
| 11 | `industry_chain_event_metric_observation` | 产业事件指标观测表 | 保存资讯浏览量、评论量、转发量、点赞量等时序互动观测 | 某事件/指标/观测时点的一次互动量观测 |
| 12 | `industry_chain_extraction_result` | 产业链实体关系抽取结果表 | 保存 NLP 从文档中识别出的实体、关系、属性及证据，支持复审和追溯 | 一次实体识别或关系抽取明细 |
| 13 | `industry_chain_model_run` | 产业链模型运行记录表 | 保存某次模型运行的模型版本、参数、输入快照和运行状态，支撑结果可复现 | 一次模型运行 |
| 14 | `industry_chain_model_result_detail` | 产业链模型结果明细表 | 保存模型对对象、指标、维度输出的评分、标签、排名、预测和因素贡献等原子结果 | 一次模型运行的一个对象/指标/维度结果 |

---

## 5. 表结构设计

本节各表只列业务字段和表特有生成字段；每张表均必须同时包含 §3.3 的公共治理字段。

### 5.1 `industry_chain`

**中文表名**：产业链标准信息表。  
**用途简述**：保存平台标准产业链名录与基础属性，作为所有产业链数据的统一挂载点；只描述“链是什么”，不保存企业数、市场规模等统计结果。同时承载门户 L0 产业对象与 L1+ 子链名录（见 `chain_tier`）。  
**粒度**：一条标准产业链或产业对象（L0 / L1 / L2+）。  
**业务唯一键**：`UK(chain_id)`；当前编码辅助唯一键 `UK(chain_code)`；L0 辅助唯一键 `UK(industry_id)`（仅 `chain_tier='L0'` 行强制）。  
**更新策略**：采用 SCD1 当前快照；按 `chain_id` Upsert，修订时递增 `data_version`，不在本表保存多行历史。`valid_from` 表示当前版本生效时间，`valid_to` 固定为空；完整变更历史由 ETL 审计日志保留。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `chain_id` | 产业链归一主键 | `VARCHAR(64)` | 是 | 产业链归一编码或平台生成 | 中 |
| `industry_id` | L0 产业对象主键 | `VARCHAR(64)` | 是 | 门户产业选择器 / 企业所属产业归一键；平台生成或配置库 | 中 |
| `chain_code` | 产业链来源编码 | `VARCHAR(64)` | 是 | 来源产业链编码 | 高 |
| `chain_name` | 产业链标准名称 | `VARCHAR(200)` | 是 | 产业链名称 | 高 |
| `chain_short_name` | 产业链简称 | `VARCHAR(100)` | 否 | 产业链简称 | 低 |
| `parent_chain_id` | 上级产业链主键 | `VARCHAR(64)` | 否 | 上级产业链编码归一；L0 行为空 | 中 |
| `chain_tier` | 产业对象层级 | `VARCHAR(8)` | 是 | `L0` / `L1` / `L2+`；与权限 persona 无关 | 中 |
| `chain_level` | 来源/树形数值层级 | `INT` | 是 | 来源层级或层次计算；可与 `chain_tier` 并存 | 高 |
| `chain_category` | 产业链分类 | `VARCHAR(64)` | 否 | 产业分类字段 | 中 |
| `future_industry_flag` | 未来产业标记 | `TINYINT` | 是 | 八大未来产业标记或平台配置 | 低 |
| `description` | 产业链说明 | `TEXT` | 否 | 可选短摘要；**门户「产业介绍」正文以 CMS 为准，不读本字段作真源** | 低 |
| `status` | 产业链有效状态 | `VARCHAR(20)` | 是 | 来源状态或平台默认 | 中 |

**L0 / L1 约定**（对齐 `DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806`）：

1. 门户顶部选择器与对比篮写入 **`industry_id`（L0）**，不写入子链 `chain_id`；
2. `chain_tier='L0'` 行表示产业对象；建议 `industry_id = chain_id`，便于兼容旧 `chain_id` 只读解析；
3. `chain_tier IN ('L1','L2+')` 行必须填写可解析的 `industry_id` 指向所属 L0，并用 `parent_chain_id` 表达子链父子；
4. 全景默认首屏渲染当前 L0 下的 L1 子链；更深结构由节点表与关系表承载，不在本表堆工艺叶子。

禁止在本表保存企业数、机构数、市场规模、投资总额和增长率。  
**产业介绍真源**：门户/专题「产业介绍」一律读 **CMS 已发布内容**（按 `industry_id`/`chain_id` 挂载）；本表 `description` 不得与 CMS 双写长文。

### 5.2 `industry_chain_node`

**中文表名**：产业链节点信息表。  
**用途简述**：保存某条产业链包含的环节或节点，支撑全景图、上中下游展示和节点筛选；节点通过 `chain_id` 归属到产业链。  
**粒度**：产业链内一个标准节点。  
**业务唯一键**：`UK(chain_id, node_id)`；当前编码辅助唯一键 `UK(chain_id, node_code)`。  
**更新策略**：采用 SCD1 当前快照；属性修订时递增 `data_version` 并 Upsert。节点撤销设置 `is_deleted=1`；多行历史不在本表保存。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `node_id` | 产业链节点归一主键 | `VARCHAR(64)` | 是 | 来源节点 ID 或平台归一 | 高 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链编码归一 | 高 |
| `node_code` | 节点来源编码 | `VARCHAR(64)` | 是 | 节点编码 | 高 |
| `node_name` | 节点标准名称 | `VARCHAR(200)` | 是 | 节点名称 | 高 |
| `parent_node_id` | 父节点主键 | `VARCHAR(64)` | 否 | 父节点编码归一 | 高 |
| `node_level` | 节点层级 | `INT` | 是 | 来源层级 | 高 |
| `stage_code` | 上中下游阶段编码 | `VARCHAR(32)` | 否 | 上游/中游/下游标签或规则生成 | 中 |
| `node_type` | 节点业务类型 | `VARCHAR(32)` | 否 | 环节、工艺、产品、技术等；诊断五环节（研发/设计/制造/销售/服务）经 `gkx_cfg` 枚举映射到本字段或模型 `dimension_code`，不另建 DWD 表 | 中 |
| `importance_level` | 来源明确的节点重要等级 | `VARCHAR(20)` | 否 | 来源或人工维护的重要性标记 | 低 |
| `sort_no` | 同级节点排序号 | `INT` | 否 | 来源排序或平台生成 | 中 |
| `node_path` | 节点层级路径 | `TEXT` | 否 | 来源节点路径或父子关系递归生成 | 中 |
| `description` | 节点说明 | `TEXT` | 否 | 节点说明 | 中 |
| `status` | 节点有效状态 | `VARCHAR(20)` | 是 | 来源状态或平台默认 | 中 |

算法识别的关键节点、重要性得分和高价值指数统一进入 `industry_chain_model_result_detail`，不得回写本表形成双轨口径。`importance_level` 仅允许 ODS 来源或人工维护批次写入；算法批次写入必须被 ETL 拒绝。

**节点简介真源**：门户 / 全景「节点简介」统一读取本表 `description`；本轮 CMS **不**维护节点简介正文，避免双真源（门户 CMS 五文案块仍只管专题介绍类内容）。

### 5.3 `industry_chain_node_rel`

**中文表名**：产业链节点关系表。  
**用途简述**：保存同一产业链内两个节点之间的上下游、供需、依赖、替代、协同等结构关系，支撑拓扑图和传导分析。  
**粒度**：产业链内两个节点之间的一条标准关系。  
**业务唯一键**：`UK(relation_id)`；关系防重键 `UK(chain_id, source_node_id, target_node_id, relation_type, valid_from)`。  
**更新策略**：关系演化使用有效期，禁止覆盖历史；`valid_from` 必填，来源无业务时间时使用平台首次确认时间。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `relation_id` | 节点关系主键 | `VARCHAR(64)` | 是 | 平台关系 ID，建议使用 `node-rel:` 前缀 | 系统 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链编码 | 高 |
| `source_node_id` | 关系起点节点主键 | `VARCHAR(64)` | 是 | 源节点编码 | 高 |
| `target_node_id` | 关系终点节点主键 | `VARCHAR(64)` | 是 | 目标节点编码 | 高 |
| `relation_type` | 节点关系类型编码 | `VARCHAR(32)` | 是 | 上下游、供需、依赖、替代、协同 | 中 |
| `relation_direction` | 关系方向 | `VARCHAR(16)` | 是 | 来源方向或规则生成 | 中 |
| `relation_weight` | 来源明确的关系权重 | `DECIMAL(18,6)` | 否 | 来源明确给出的关系强度或人工确认值 | 低 |
| `confidence` | 关系识别置信度 | `DECIMAL(8,6)` | 否 | 抽取或规则置信度 | 低 |
| `evidence_ref` | 关系证据引用 | `VARCHAR(512)` | 否 | 来源文档/抽取结果引用 | 中 |

算法计算的关系强度、关键性和影响力统一写入 `industry_chain_model_result_detail`，不得回写 `relation_weight`。

### 5.4 `industry_chain_entity_rel`

**中文表名**：产业链实体关系表。  
**用途简述**：保存产业链或节点与企业、机构、人才、技术、政策、产品、专利等外部实体的归属或参与关系；只存关系键，不复制主体完整属性。  
**粒度**：产业链或节点与一个外部实体的一条关系。  
**业务唯一键**：`UK(relation_id)`；关系防重键 `UK(chain_id, node_scope_key, entity_type, entity_id, relation_type, valid_from)`。  
**更新策略**：关系演化使用有效期；`valid_from` 必填，来源无业务时间时使用平台首次确认时间。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `relation_id` | 产业链实体关系主键 | `VARCHAR(64)` | 是 | 平台关系 ID，建议使用 `chain-entity-rel:` 前缀 | 系统 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链编码归一 | 高 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 产业链节点编码 | 中 |
| `node_scope_key` | 链级或节点级关系去重键 | `VARCHAR(64)` | 是 | 生成列：`COALESCE(node_id, '__CHAIN__')` | 系统 |
| `entity_type` | 外部实体类型 | `VARCHAR(32)` | 是 | 来源主体类型或平台归类 | 中 |
| `entity_id` | 外部实体权威业务键 | `VARCHAR(64)` | 是 | 对应权威数据域业务键 | 中 |
| `entity_subtype` | 外部实体细分类别 | `VARCHAR(32)` | 否 | 科研机构、服务机构、政策类型等 | 中 |
| `relation_type` | 实体与链或节点的关系类型 | `VARCHAR(32)` | 是 | 所属、参与、服务、研发、生产、适用等 | 中 |
| `role_type` | 实体在产业链中的角色 | `VARCHAR(32)` | 否 | 链主、供应商、科研主体、服务方等 | 低 |
| `importance_level` | 来源明确的关系重要等级 | `VARCHAR(20)` | 否 | 来源或人工维护的关系重要性 | 低 |
| `confidence` | 关系可信度或抽取置信度 | `DECIMAL(8,6)` | 否 | 来源可信度或关系抽取置信度 | 低 |
| `is_primary` | 是否主要归属关系 | `TINYINT` | 否 | 主要归属标记 | 低 |
| `evidence_ref` | 关系证据引用 | `VARCHAR(512)` | 否 | 关系证据引用 | 中 |

`entity_type` 至少支持：

- `chain`
- `enterprise`
- `institution`
- `service_institution`
- `talent`
- `technology`
- `policy`
- `product`
- `patent`

机构主体仍使用 `org_uid`；科研机构与服务机构通过 `entity_type/entity_subtype` 区分。企业、机构、人才、技术和政策完整主体属性由各权威数据域维护。

`node_scope_key` 只用于 MySQL 唯一键和去重，不作为业务字段输出；产业链级关系使用 `__CHAIN__`，节点级关系使用真实 `node_id`，避免 MySQL 唯一键中 `NULL` 可重复的问题。

`chain_score`、`participation_depth`、关键程度等算法计算属性统一写入 `industry_chain_model_result_detail`，通过 `object_type=chain_entity_relation`、`object_id=relation_id` 关联，禁止同时回写本表形成双轨口径。

`entity_subtype` 是实体分类快照，不是关系区分维度，因此不进入关系防重键；同一实体需要多种关系语义时必须使用不同 `relation_type`。

### 5.5 `industry_chain_market_observation`

**中文表名**：产业链市场指标观测表。  
**用途简述**：仅保存**外部导入**的市场原子观测（如行业研报口径的销量、价格、产值、外购市场规模等）；同比、环比由 ADS 基于本表或指标引擎计算。  
**粒度**：某产业链/节点/区域/指标/统计期的一次原子市场观测。  
**业务唯一键**：`UK(observation_scope_key)`。  
**更新策略**：同源修订按 `data_version` 保留；不覆盖历史口径。

#### 与「产业市场规模」平台计算口径的分轨（强制）

| 口径 | 落层 | 计算/来源 | 是否写入本表 |
|---|---|---|---|
| **产业市场规模（平台默认，IC-03）** | **ADS / 指标引擎**（`M_CHAIN_MARKET_SIZE`） | 取该产业链下全部关联**企业**的年报营收求和；**只计企业，不计**机构/人才/其他主体 | **否** — 禁止把加总结果当 ODS 观测灌入本表 |
| 外部市场观测（研报/市调等） | 本表 DWD | 供应方或采购源的原子观测值 | 是（有源时） |

平台默认市场规模公式（团队口径，2026-08-07 `human:李伟`）：

```text
M_CHAIN_MARKET_SIZE(chain_id, stat_year)
  = SUM( enterprise_annual_revenue )
  WHERE enterprise 经由 industry_chain_entity_rel
        关联到该 chain_id（及授权下钻的 node 范围）
        AND entity_type = 'enterprise'
```

输入依赖：

1. CHAIN：`industry_chain_entity_rel`（企业—链/节点关系，可由本轮 tags 灌入）；  
2. ENT：企业年报营收权威字段（ENT 域 DWD，不在本轮 4 张 ODS 内）。

因此：**产业市场规模不是「4 表直灌」问题，而是跨域计算问题**；本表不承担该指标的落库。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `observation_id` | 市场观测主键 | `VARCHAR(64)` | 是 | 来源观测 ID 或平台生成 | 中 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链标签或映射 | 中 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 节点标签或映射 | 低 |
| `region_code` | 观测区域编码 | `VARCHAR(20)` | 否 | 国家/省/市/区编码归一 | 中 |
| `metric_id` | 观测指标编码 | `VARCHAR(64)` | 是 | 指标注册中心 | 系统 |
| `metric_version` | 指标口径版本 | `VARCHAR(32)` | 是 | 指标口径版本 | 系统 |
| `stat_period` | 统计周期类型 | `VARCHAR(16)` | 是 | 年、季、月、日 | 高 |
| `period_start` | 统计期开始日期 | `DATE` | 是 | 统计期开始 | 中 |
| `period_end` | 统计期结束日期 | `DATE` | 是 | 统计期结束 | 中 |
| `stat_date` | 统计基准日期 | `DATE` | 是 | 统计基准日期 | 高 |
| `observation_value` | 原子市场观测值 | `DECIMAL(30,8)` | 是 | 来源观测值 | 高 |
| `unit` | 观测值单位 | `VARCHAR(32)` | 是 | 来源单位归一 | 高 |
| `currency` | 金额观测币种 | `VARCHAR(16)` | 否 | 币种 | 中 |
| `price_basis` | 价格统计口径 | `VARCHAR(32)` | 否 | 当年价、不变价等 | 低 |
| `market_scope` | 市场范围 | `VARCHAR(32)` | 否 | 全球、全国、区域 | 中 |
| `extraction_id` | 文本抽取结果主键 | `VARCHAR(64)` | 否 | FK → `industry_chain_extraction_result.extraction_id` | 系统 |
| `extraction_run_id` | 文本抽取运行主键 | `VARCHAR(64)` | 否 | FK → `industry_chain_model_run.run_id`，且 `run_type=extraction` | 系统 |
| `observation_scope_key` | 市场观测防重指纹 | `CHAR(64)` | 是 | 按下方规范化字段清单计算 SHA-256 | 系统 |

销售额、销量、价格、产值等观测类型统一由 `metric_id` 表达，不再维护与指标注册重复的 `indicator_code`。

`observation_scope_key` 的规范化输入固定为：

```text
chain_id
| COALESCE(node_id, '__ALL_NODE__')
| COALESCE(region_code, '__ALL_REGION__')
| metric_id
| metric_version
| stat_period
| period_start
| period_end
| stat_date
| COALESCE(market_scope, '__ALL_SCOPE__')
| source_system
| source_record_id
| data_version
```

字段按 UTF-8、去除首尾空白并替换固定哨兵后，依次编码为 `UTF8字节长度:字段值`，按字段顺序直接拼接并计算 SHA-256；禁止使用易产生分隔符歧义的普通字符串拼接，禁止不同 ETL 自行定义。

由文本属性抽取生成市场观测时，`extraction_id` 与 `extraction_run_id` 必须同时填写，且两者必须指向同一次抽取运行；直接来源于结构化数据的观测允许两字段均为空。

### 5.6 `industry_chain_investment_event`

**中文表名**：产业链投融资事件表。  
**用途简述**：保存投融资、并购等资本事件本身，包括金额、轮次、日期；参与方角色和金额扩展分别写入事件实体关系表与参与方扩展表。  
**粒度**：一次投融资、并购或资本事件。  
**业务唯一键**：`UK(event_id)`。  
**更新策略**：采用 SCD1 当前快照；事件按 `event_id` Upsert，金额和状态修订时递增 `data_version`，不在本表保存多行历史。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `event_id` | 投融资事件全域主键 | `VARCHAR(64)` | 是 | 平台统一事件 ID，使用 `invest:` 前缀 | 系统 |
| `source_investment_id` | 来源投融资事件 ID | `VARCHAR(128)` | 否 | 来源投融资事件业务 ID | 中 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链标签或映射 | 中 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 节点标签或映射 | 低 |
| `investment_type` | 投融资事件类型 | `VARCHAR(32)` | 是 | 投资、融资、并购等资本事件类型 | 高 |
| `financing_round` | 融资轮次 | `VARCHAR(32)` | 否 | 融资轮次 | 高 |
| `amount` | 事件总金额 | `DECIMAL(30,8)` | 否 | 事件总金额 | 高 |
| `currency` | 事件金额币种 | `VARCHAR(16)` | 否 | 币种 | 高 |
| `event_date` | 事件发生日期 | `DATE` | 是 | 事件日期 | 高 |
| `region_code` | 事件关联区域编码 | `VARCHAR(20)` | 否 | 事件区域 | 中 |
| `description` | 事件说明 | `TEXT` | 否 | 事件说明 | 中 |
| `evidence_ref` | 事件证据引用 | `VARCHAR(512)` | 否 | 公告或报道地址 | 中 |

融资企业、投资机构及其他参与方统一写入 `industry_chain_event_entity_rel`；融资主体使用 `relation_type=financing_subject`，事件主表不重复保存 `enterprise_code`。

`amount` 非空时 `currency` 必填。

### 5.7 `industry_chain_investment_participant`

**中文表名**：投融资事件参与方扩展表。  
**用途简述**：保存投融资参与方的金额等专属扩展信息；参与方角色关系必须先写入 `industry_chain_event_entity_rel`，本表不重复保存角色。  
**粒度**：投融资事件中的一个参与方扩展。  
**业务唯一键**：`UK(relation_id)`。  
**权威规则**：参与方基础关系必须先写 `industry_chain_event_entity_rel`；本表只保存投融资专属扩展字段，禁止重复保存第二份参与方关系。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `participant_record_id` | 投融资参与方扩展记录主键 | `VARCHAR(64)` | 是 | 平台生成 | 系统 |
| `relation_id` | 事件实体关系主键 | `VARCHAR(64)` | 是 | FK → `industry_chain_event_entity_rel.relation_id` | 系统 |
| `participation_amount` | 单个参与方金额 | `DECIMAL(30,8)` | 否 | 参与金额 | 低 |
| `currency` | 参与方金额币种 | `VARCHAR(16)` | 否 | 币种 | 中 |

参与方角色和领投标记只使用父行 `industry_chain_event_entity_rel.relation_type`，本表不得重复保存角色字段。`participation_amount` 非空时 `currency` 必填。

### 5.8 `industry_chain_news_event`

**中文表名**：产业链资讯事件表。  
**用途简述**：保存产业资讯主数据，包括标题、摘要、来源和发布时间，支撑热点资讯列表和资讯事件线；浏览量和热点得分不写入本表。  
**粒度**：一条产业资讯事件。  
**业务唯一键**：`UK(event_id)`；业务防重键 `UK(news_dedup_key)`。  
**更新策略**：标题、摘要、分类可修订；互动量不得覆盖在本表，进入事件指标观测表。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `event_id` | 资讯事件全域主键 | `VARCHAR(64)` | 是 | 平台统一事件 ID，使用 `news:` 前缀 | 系统 |
| `source_news_id` | 来源资讯业务 ID | `VARCHAR(128)` | 否 | 来源资讯业务 ID | 高 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链标签或映射 | 中 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 节点标签或映射 | 低 |
| `title` | 资讯标题 | `VARCHAR(500)` | 是 | 资讯标题 | 高 |
| `summary` | 资讯摘要 | `TEXT` | 否 | 来源摘要或 NLP 摘要 | 中 |
| `news_type` | 资讯类型 | `VARCHAR(32)` | 否 | 政策、技术、市场、企业等 | 中 |
| `source_name` | 来源媒体名称 | `VARCHAR(200)` | 否 | 来源媒体 | 高 |
| `author_name` | 原文署名作者或机构 | `VARCHAR(200)` | 否 | 来源资讯署名作者或发布机构原文署名 | 中 |
| `source_url` | 原始资讯链接 | `VARCHAR(1000)` | 否 | 原始报道地址 | 高 |
| `source_url_hash` | 规范化资讯链接哈希 | `CHAR(64)` | 否 | 规范化 URL 的 SHA-256 生成列 | 系统 |
| `news_dedup_key` | 资讯业务防重指纹 | `CHAR(64)` | 是 | 按下方降级规则生成的资讯防重指纹 | 系统 |
| `publish_time` | 资讯发布时间 | `DATETIME` | 是 | 发布时间 | 高 |
| `region_code` | 资讯关联区域编码 | `VARCHAR(20)` | 否 | 关联区域 | 低 |

NLP 情感、热点标签及热点得分统一写入 `industry_chain_model_result_detail`，不回写资讯事件主表。

`author_name` 只保存来源原文署名，不作为人才主数据。若作者已归一为平台人物或机构，使用 `industry_chain_event_entity_rel` 建立 `relation_type=author` 或 `publisher` 的标准实体关系。

`news_dedup_key` 生成规则按优先级选择第一组可用字段：

1. 有 URL：`source_system | canonical_url`；
2. 无 URL但有来源 ID：`source_system | source_news_id`；
3. 两者均无：`source_system | COALESCE(source_name,'__UNKNOWN__') | publish_time | normalized_title`。

`canonical_url` 统一小写协议和主机名、移除 fragment、移除 `utm_*` 等跟踪参数、按参数名排序并删除末尾 `/`；`normalized_title` 统一 Unicode NFKC、转小写、压缩连续空白。最终按 UTF-8 拼接并计算 SHA-256。

### 5.9 `industry_chain_milestone_event`

**中文表名**：产业链里程碑事件表。  
**用途简述**：可选的结构化里程碑明细（供算法/图谱引用）；**门户「产业发展历程」以 CMS 录入为展示真源**，本表不承担门户历程正文灌数。  
**粒度**：一条结构化产业发展里程碑或重大事件。  
**业务唯一键**：`UK(event_id)`。  
**更新策略**：若从资讯/政策结构化抽取或人工结构化补录，保留证据和版本；**不得**用本轮 ODS 4 表直灌覆盖 CMS 历程。

#### 与 CMS「产业发展历程」的分轨（强制）

| 口径 | 落层 | 说明 |
|---|---|---|
| **产业发展历程（门户 Tab）** | **CMS** | 阶段、条目、图文、排序由运营在 CMS 录入/发布；前端读 CMS |
| 结构化里程碑（可选） | 本表 DWD | 仅当需要可计算的事件键、与资讯/投融资关联或算法引用时使用；可通过 `source_event_id` / `ext.cms_block_id` 回指 CMS |

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `event_id` | 里程碑事件全域主键 | `VARCHAR(64)` | 是 | 平台统一事件 ID，使用 `milestone:` 前缀 | 系统 |
| `source_milestone_id` | 来源里程碑业务 ID | `VARCHAR(128)` | 否 | 来源里程碑业务 ID | 低 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 产业链标签 | 高 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 产业链节点 | 低 |
| `event_name` | 里程碑事件名称 | `VARCHAR(500)` | 是 | 重大事件标题 | 高 |
| `milestone_type` | 里程碑事件类型 | `VARCHAR(32)` | 是 | 政策、技术突破、产业化、危机等 | 中 |
| `phase_id` | 发展阶段编码 | `VARCHAR(64)` | 否 | 门户历程 Tab 阶段分组键；配置库或 CMS phase 块键 | 中 |
| `phase_name` | 发展阶段名称 | `VARCHAR(100)` | 否 | 发展阶段展示名快照；正式名以配置库为准 | 低 |
| `phase_sort_no` | 发展阶段排序号 | `INT` | 否 | 阶段在历程轴上的排序 | 中 |
| `event_date` | 里程碑发生日期 | `DATE` | 是 | 事件日期 | 高 |
| `event_level` | 里程碑重要等级 | `VARCHAR(20)` | 否 | 事件重要程度 | 低 |
| `source_event_type` | 来源事件类型 | `VARCHAR(32)` | 否 | news、policy、manual 等来源事件类型 | 中 |
| `source_event_id` | 来源事件业务 ID | `VARCHAR(64)` | 否 | 来源资讯、政策或人工记录 ID | 中 |
| `description` | 里程碑事件说明 | `TEXT` | 否 | 事件说明 | 中 |
| `region_code` | 事件关联区域编码 | `VARCHAR(20)` | 否 | 事件区域 | 中 |
| `evidence_ref` | 里程碑证据引用 | `VARCHAR(512)` | 否 | 来源证据 | 高 |

`milestone_type` 描述事件业务类型；`phase_*` 若填写，仅作结构化分组，**门户历程阶段名称与长文案以 CMS 为准**，DWD 不复制 CMS 阶段正文。

影响方向、影响评分和趋势判断属于模型原子结果，统一写入 `industry_chain_model_result_detail`。

### 5.10 `industry_chain_event_entity_rel`

**中文表名**：产业事件实体关系表。  
**用途简述**：保存投融资、资讯、里程碑等事件与企业、机构、投资方、作者等实体之间的关系，回答“这个事件关联了谁”。  
**粒度**：一个产业事件与一个实体的一条关系。  
**业务唯一键**：`UK(relation_id)`；关系防重键 `UK(event_id, entity_type, entity_id, relation_type, valid_from)`。  
**更新策略**：事件 ID 必须全域唯一；关系变化通过有效期维护；`valid_from` 必填。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `relation_id` | 事件实体关系主键 | `VARCHAR(64)` | 是 | 平台关系 ID，建议使用 `event-entity-rel:` 前缀 | 系统 |
| `event_id` | 关联事件全域主键 | `VARCHAR(64)` | 是 | 对应事件业务键 | 高 |
| `event_kind` | 事件域冗余分类 | `VARCHAR(16)` | 是 | `invest` / `news` / `milestone`；与 `event_id` 前缀一致，降低多态路由错误 | 系统 |
| `entity_type` | 关联实体类型 | `VARCHAR(32)` | 是 | 企业、机构、人才、技术、政策等 | 中 |
| `entity_id` | 关联实体权威业务键 | `VARCHAR(64)` | 是 | 权威数据域业务键 | 中 |
| `relation_type` | 事件与实体关系类型 | `VARCHAR(32)` | 是 | 配置库登记的标准关系编码 | 中 |
| `confidence` | 关系识别置信度 | `DECIMAL(8,6)` | 否 | 抽取或规则置信度 | 低 |
| `evidence_ref` | 关系证据引用 | `VARCHAR(512)` | 否 | 来源证据 | 中 |

投融资关系编码统一为 `financing_subject`、`investor`、`lead_investor`、`follow_investor`；资讯署名关系使用 `author`、`publisher`。字段只保存 snake_case 编码，中文名称由配置库提供。`event_kind` 由 ETL 根据 `event_id` 前缀写入，禁止与前缀不一致。

### 5.11 `industry_chain_event_metric_observation`

**中文表名**：产业事件指标观测表。  
**用途简述**：保存资讯浏览量、评论量、转发量、点赞量等时序互动观测，支撑热点排序和互动趋势复算。  
**粒度**：某事件、某指标、某观测时点的一次原子观测。  
**业务唯一键**：`UK(metric_observation_scope_key)`。  
**用途**：支撑 IC-09/IC-19 的热点阈值、变化趋势和可复算性。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `observation_id` | 事件指标观测主键 | `VARCHAR(64)` | 是 | 来源观测 ID 或平台生成 | 中 |
| `event_id` | 被观测事件全域主键 | `VARCHAR(64)` | 是 | 资讯或事件 ID | 高 |
| `metric_id` | 事件互动指标编码 | `VARCHAR(64)` | 是 | 浏览量、评论量、转发量、点赞量指标 | 系统 |
| `metric_version` | 指标口径版本 | `VARCHAR(32)` | 是 | 指标口径版本 | 系统 |
| `observed_time` | 指标采集时间 | `DATETIME` | 是 | 采集时间 | 高 |
| `metric_value` | 事件指标原子观测值 | `DECIMAL(30,8)` | 是 | 来源互动量 | 高 |
| `unit` | 指标单位 | `VARCHAR(32)` | 是 | 次、条等 | 高 |
| `metric_observation_scope_key` | 事件指标防重指纹 | `CHAR(64)` | 是 | 对事件/指标/观测时间/来源规范化后计算 SHA-256 | 系统 |

`metric_observation_scope_key` 的规范化输入固定为：

```text
event_id
| metric_id
| metric_version
| observed_time
| source_system
| source_record_id
| data_version
```

字段按 UTF-8、去除首尾空白并替换固定哨兵后，依次编码为 `UTF8字节长度:字段值`，按字段顺序直接拼接并计算 SHA-256；公共追溯字段均为必填，不允许使用 NULL 绕过唯一约束。

### 5.12 `industry_chain_extraction_result`

**中文表名**：产业链实体关系抽取结果表。  
**用途简述**：保存 NLP 从资讯、政策、专利等文档中识别出的实体、关系、属性及证据，支撑复审、消歧和结果追溯；由本项目算法生成，不从供应方 ODS 直接复制。  
**粒度**：一次实体识别或关系抽取明细。  
**业务唯一键**：`UK(extraction_id)`；防重键 `UK(run_id, result_fingerprint)`。  
**用途**：支撑 IC-13/IC-14 的实体识别、关系抽取、模型复审和证据追溯。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `extraction_id` | 抽取结果主键 | `VARCHAR(64)` | 是 | 模型生成 | 系统 |
| `run_id` | 所属抽取运行主键 | `VARCHAR(64)` | 是 | FK → `industry_chain_model_run.run_id`，且运行类型为 extraction | 系统 |
| `result_type` | 抽取结果类型 | `VARCHAR(16)` | 是 | entity、relation 或 attribute | 系统 |
| `document_id` | 输入文档统一主键 | `VARCHAR(64)` | 是 | 来源文档统一主键 | 中 |
| `document_type` | 输入文档类型 | `VARCHAR(32)` | 是 | news、policy、patent、report、paper、web 等文档类型 | 中 |
| `document_version` | 输入文档内容版本 | `VARCHAR(64)` | 是 | 输入文档内容版本或完整 SHA-256 内容哈希 | 中 |
| `sentence_id` | 来源句段主键 | `VARCHAR(64)` | 否 | 来源句段 ID | 低 |
| `mention_text` | 实体原始提及文本 | `VARCHAR(500)` | 否 | 实体原始文本 | 高 |
| `char_start` | 实体提及起始字符位置 | `INT` | 否 | 起始字符位置 | 高 |
| `char_end` | 实体提及结束字符位置 | `INT` | 否 | 结束字符位置 | 高 |
| `entity_type` | 识别实体类型 | `VARCHAR(32)` | 否 | 识别实体类型 | 模型 |
| `normalized_entity_id` | 归一实体业务键 | `VARCHAR(64)` | 否 | 归一实体业务键 | 模型 |
| `candidate_entities` | 实体消歧候选列表 | `JSON` | 否 | 消歧候选实体 ID、类型和得分列表 | 模型 |
| `subject_entity_type` | 关系主语实体类型 | `VARCHAR(32)` | 否 | 关系主语实体类型 | 模型 |
| `subject_entity_id` | 关系主语归一实体键 | `VARCHAR(64)` | 否 | 关系主语实体 | 模型 |
| `subject_mention_text` | 关系主语原始文本 | `VARCHAR(500)` | 否 | 关系主语原始文本 | 模型 |
| `subject_char_start` | 主语起始字符位置 | `INT` | 否 | 主语起始字符位置 | 模型 |
| `subject_char_end` | 主语结束字符位置 | `INT` | 否 | 主语结束字符位置 | 模型 |
| `predicate_code` | 标准关系谓词编码 | `VARCHAR(64)` | 否 | 关系谓词 | 模型 |
| `object_entity_type` | 关系宾语实体类型 | `VARCHAR(32)` | 否 | 关系宾语实体类型 | 模型 |
| `object_entity_id` | 关系宾语归一实体键 | `VARCHAR(64)` | 否 | 关系宾语实体 | 模型 |
| `object_mention_text` | 关系宾语原始文本 | `VARCHAR(500)` | 否 | 关系宾语原始文本 | 模型 |
| `object_char_start` | 宾语起始字符位置 | `INT` | 否 | 宾语起始字符位置 | 模型 |
| `object_char_end` | 宾语结束字符位置 | `INT` | 否 | 宾语结束字符位置 | 模型 |
| `attribute_code` | 标准属性编码 | `VARCHAR(64)` | 否 | 标准属性编码 | 模型/配置 |
| `attribute_value` | 属性抽取值 | `JSON` | 否 | 属性提取值，按 `attribute_value_type` 解释 | 模型 |
| `attribute_value_type` | 属性值数据类型 | `VARCHAR(16)` | 否 | string、number、date、boolean、json | 模型 |
| `attribute_unit` | 属性值单位 | `VARCHAR(32)` | 否 | 属性单位 | 模型/配置 |
| `target_metric_id` | 属性对应指标编码 | `VARCHAR(64)` | 否 | 属性归一后的指标 ID | 模型/配置 |
| `target_metric_version` | 属性对应指标口径版本 | `VARCHAR(32)` | 否 | 属性归一指标的口径版本 | 模型/配置 |
| `confidence` | 抽取结果置信度 | `DECIMAL(8,6)` | 是 | 模型置信度 | 模型 |
| `evidence_text` | 支撑抽取结果的原文证据 | `TEXT` | 否 | 关系证据文本 | 高 |
| `result_fingerprint` | 抽取结果防重指纹 | `CHAR(64)` | 是 | 按下方规范化字段清单计算 SHA-256 | 系统 |

抽取模型、版本、参数及输入快照统一从 `industry_chain_model_run` 获取，不在结果表重复保存。

`document_id` 必须解析到平台文档注册表或对应权威域的文档 DWD；CHAIN 域不复制新闻、政策、专利、报告和论文全文。公共字段 `source_system/source_table/source_record_id` 必须指向该权威文档记录，`document_version` 必须与运行输入快照中的版本一致。无法解析权威文档或版本的抽取结果禁止进入正式 DWD。

`result_fingerprint` 的规范化输入固定为：

```text
result_type
| document_id
| document_type
| document_version
| COALESCE(sentence_id, '__NO_SENTENCE__')
| COALESCE(normalized_mention_text, '__NO_MENTION__')
| COALESCE(char_start, -1)
| COALESCE(char_end, -1)
| COALESCE(entity_type, '__NO_ENTITY_TYPE__')
| COALESCE(normalized_entity_id, '__NO_ENTITY__')
| COALESCE(subject_entity_type, '__NO_SUBJECT_TYPE__')
| COALESCE(subject_entity_id, '__NO_SUBJECT__')
| COALESCE(normalized_subject_mention, '__NO_SUBJECT_MENTION__')
| COALESCE(subject_char_start, -1)
| COALESCE(subject_char_end, -1)
| COALESCE(predicate_code, '__NO_PREDICATE__')
| COALESCE(object_entity_type, '__NO_OBJECT_TYPE__')
| COALESCE(object_entity_id, '__NO_OBJECT__')
| COALESCE(normalized_object_mention, '__NO_OBJECT_MENTION__')
| COALESCE(object_char_start, -1)
| COALESCE(object_char_end, -1)
| COALESCE(attribute_code, '__NO_ATTRIBUTE__')
| COALESCE(canonical_attribute_value, '__NO_ATTRIBUTE_VALUE__')
| COALESCE(attribute_value_type, '__NO_ATTRIBUTE_TYPE__')
| COALESCE(target_metric_id, '__NO_TARGET_METRIC__')
| COALESCE(target_metric_version, '__NO_TARGET_METRIC_VERSION__')
```

`normalized_mention_text`、`normalized_subject_mention`、`normalized_object_mention` 采用 Unicode NFKC、转小写、压缩连续空白；`canonical_attribute_value` 使用 JSON Canonicalization Scheme 序列化。字段按上述顺序使用长度前缀编码后计算 SHA-256。`run_id` 已在防重键外层，不重复进入指纹。

按 `result_type` 执行条件必填：

| `result_type` | 必填字段 |
|---|---|
| `entity` | `mention_text`、`char_start`、`char_end`、`entity_type` |
| `relation` | `subject_entity_type`、`subject_mention_text`、`subject_char_start`、`subject_char_end`、`predicate_code`、`object_entity_type`、`object_mention_text`、`object_char_start`、`object_char_end` |
| `attribute` | `normalized_entity_id`、`attribute_code`、`attribute_value`、`attribute_value_type`；数值属性还必须填写 `attribute_unit` 或关联带单位的 `target_metric_id`；填写 `target_metric_id` 时必须同时填写 `target_metric_version` |

### 5.13 `industry_chain_model_run`

**中文表名**：产业链模型运行记录表。  
**用途简述**：保存某次模型运行的模型版本、参数、输入快照、运行时间和状态，支撑分析结果可复现和血缘追溯；不保存 Java 异步任务工作流状态。  
**粒度**：一次产业链模型运行。  
**业务唯一键**：`UK(run_id)`。  
**说明**：本表保存分析运行的可复现元数据，不保存 Java 异步任务工作流状态。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `run_id` | 模型运行主键 | `VARCHAR(64)` | 是 | 算法平台生成 | 系统 |
| `run_type` | 模型运行类型 | `VARCHAR(32)` | 是 | extraction、analysis、forecast 等运行类型 | 系统 |
| `model_id` | 模型注册编码 | `VARCHAR(64)` | 是 | 模型注册中心 | 系统 |
| `model_version` | 模型版本 | `VARCHAR(32)` | 是 | 模型版本 | 系统 |
| `parameter_version` | 模型参数或权重版本 | `VARCHAR(32)` | 是 | 参数/权重版本 | 系统 |
| `calc_batch_id` | 模型计算批次号 | `VARCHAR(64)` | 是 | 计算批次 | 系统 |
| `chain_id` | 分析产业链主键 | `VARCHAR(64)` | 是 | 分析产业链 | 高 |
| `region_code` | 分析区域编码 | `VARCHAR(20)` | 否 | 分析区域 | 中 |
| `benchmark_scope` | 对标分析范围 | `VARCHAR(64)` | 否 | 全国、全球或自定义对标组 | 系统 |
| `scenario_id` | 情景模拟主键 | `VARCHAR(64)` | 否 | 情景模拟 ID | 系统 |
| `forecast_horizon` | 预测期长度 | `VARCHAR(32)` | 否 | 预测期长度 | 系统 |
| `stat_date` | 分析基准日期 | `DATE` | 是 | 分析基准日 | 系统 |
| `started_time` | 模型运行开始时间 | `DATETIME` | 是 | 运行开始时间 | 系统 |
| `completed_time` | 模型运行完成时间 | `DATETIME` | 否 | 运行完成时间 | 系统 |
| `run_status` | 模型运行状态 | `VARCHAR(20)` | 是 | success、failed、partial | 系统 |
| `input_snapshot_ref` | 输入数据快照引用 | `VARCHAR(512)` | 否 | 输入数据快照引用 | 系统 |
| `model_card_ref` | 模型卡引用 | `VARCHAR(512)` | 否 | 模型卡或模型注册详情引用 | 系统 |

### 5.14 `industry_chain_model_result_detail`

**中文表名**：产业链模型结果明细表。  
**用途简述**：保存模型对链、节点、关系、事件、区域等对象输出的评分、标签、排名、预测和因素贡献等原子结果；完整推荐文案和解决方案正文不进入本表。  
**粒度**：一次模型运行针对一个对象、指标、维度和预测时点的一条原子结果。  
**业务唯一键**：`UK(result_id)`；防重键 `UK(run_id, result_fingerprint)`。  
**用途**：支撑周期、阶段、关键环节、瓶颈、区域指数、优势问题、推荐指数等模型原子结果。

| 字段 | 中文注释 | 类型 | 必填 | 预期来源 | 置信度 |
|---|---|---|---|---|---|
| `result_id` | 模型结果主键 | `VARCHAR(64)` | 是 | 算法生成 | 系统 |
| `run_id` | 所属模型运行主键 | `VARCHAR(64)` | 是 | FK → `industry_chain_model_run.run_id` | 系统 |
| `object_type` | 分析对象类型 | `VARCHAR(32)` | 是 | chain、node、node_relation、chain_entity_relation、event_entity_relation、news_event、investment_event、milestone_event、region、enterprise 等 | 系统 |
| `object_id` | 分析对象业务键 | `VARCHAR(64)` | 是 | 分析对象业务键 | 系统 |
| `chain_id` | 所属产业链主键 | `VARCHAR(64)` | 是 | 所属产业链 | 系统 |
| `node_id` | 所属节点主键 | `VARCHAR(64)` | 否 | 所属节点 | 系统 |
| `region_code` | 分析对象区域编码 | `VARCHAR(20)` | 否 | 对象区域 | 系统 |
| `benchmark_id` | 对标对象或对标组主键 | `VARCHAR(64)` | 否 | 对标对象或对标组 | 系统 |
| `metric_id` | 结果指标编码 | `VARCHAR(64)` | 是 | 指标 ID | 系统 |
| `metric_version` | 指标口径版本 | `VARCHAR(32)` | 是 | 指标口径版本 | 系统 |
| `dimension_code` | 分析维度编码 | `VARCHAR(64)` | 否 | 技术、人才、市场、资金、政策等维度 | 系统 |
| `contribution_level` | 贡献结果层级 | `VARCHAR(16)` | 否 | dimension 或 feature | 模型 |
| `feature_code` | 模型特征编码 | `VARCHAR(128)` | 否 | 特征编码 | 模型/配置 |
| `result_type` | 模型结果类型 | `VARCHAR(32)` | 是 | score、label、rank、forecast、contribution、cause | 系统 |
| `result_value` | 数值型模型结果 | `DECIMAL(30,8)` | 否 | 数值结果 | 模型 |
| `result_label` | 标签或短原因编码 | `VARCHAR(128)` | 否 | 注册标签编码或短原因编码；禁止保存完整建议文案 | 模型/配置 |
| `unit` | 数值结果单位 | `VARCHAR(32)` | 否 | 分、百分比、元、个等结果单位 | 模型/指标配置 |
| `currency` | 金额结果币种 | `VARCHAR(16)` | 否 | 金额类结果币种 | 模型/指标配置 |
| `rank_no` | 模型结果排名 | `INT` | 否 | 单次 run 内、同一对象/维度下的原子排名；禁止跨对象 TopN | 模型 |
| `contribution_value` | 维度或特征贡献值 | `DECIMAL(30,8)` | 否 | 因素贡献值 | 模型 |
| `forecast_date` | 预测结果日期 | `DATE` | 否 | 预测结果日期 | 模型 |
| `priority_level` | 问题或机会优先级编码 | `VARCHAR(20)` | 否 | 问题或机会优先级 | 模型 |
| `severity_level` | 严重度等级编码 | `VARCHAR(20)` | 否 | `high` / `medium` / `low`；诊断瓶颈严重度 | 模型/配置 |
| `confidence` | 模型结果置信度 | `DECIMAL(8,6)` | 否 | 结果置信度 | 模型 |
| `uncertainty_type` | 不确定性度量类型 | `VARCHAR(32)` | 否 | standard_error、interval、probability 等 | 模型 |
| `uncertainty_value` | 单值不确定性度量 | `DECIMAL(30,8)` | 否 | 不确定性度量值 | 模型 |
| `uncertainty_lower` | 不确定性区间下界 | `DECIMAL(30,8)` | 否 | 区间型不确定性下界 | 模型 |
| `uncertainty_upper` | 不确定性区间上界 | `DECIMAL(30,8)` | 否 | 区间型不确定性上界 | 模型 |
| `evidence_ref` | 模型解释或证据引用 | `VARCHAR(512)` | 否 | 特征贡献、证据或解释引用 | 模型 |
| `result_fingerprint` | 模型结果防重指纹 | `CHAR(64)` | 是 | 按下方规范化字段清单计算 SHA-256 | 系统 |

`object_type` 为关系类型时必须使用细分枚举，不允许使用模糊值 `relation`；`object_id` 分别关联对应关系表的 `relation_id`。事件级模型结果必须使用 `news_event`、`investment_event` 或 `milestone_event`，`object_id` 对应事件表的 `event_id`，不得使用模糊值 `event`。

`result_fingerprint` 的规范化输入固定为：

```text
object_type
| object_id
| chain_id
| COALESCE(node_id, '__ALL_NODE__')
| COALESCE(region_code, '__ALL_REGION__')
| COALESCE(benchmark_id, '__NO_BENCHMARK__')
| metric_id
| metric_version
| COALESCE(dimension_code, '__TOTAL__')
| COALESCE(contribution_level, '__NO_CONTRIBUTION_LEVEL__')
| COALESCE(feature_code, '__NO_FEATURE__')
| result_type
| COALESCE(CASE WHEN result_type IN ('label','cause') THEN normalized_result_label END, '__NO_RESULT_LABEL__')
| COALESCE(CASE WHEN result_type = 'rank' THEN CAST(rank_no AS CHAR) END, '__NO_RANK__')
| COALESCE(forecast_date, '1000-01-01')
```

字段按 UTF-8、去除首尾空白并替换固定哨兵后，依次编码为 `UTF8字节长度:字段值`，按字段顺序直接拼接并计算 SHA-256。`normalized_result_label` 使用 Unicode NFKC、转小写、压缩连续空白；仅 `label/cause` 将短编码纳入指纹，允许同一对象和维度输出多个不同标签或原因。`result_type=rank` 时必须将 `rank_no` 纳入指纹，保证同 run 多条排名不撞防重键。数值型 `result_value` 默认不进入指纹，使同一逻辑数值结果可以在同一运行内按业务规则 Upsert；若需保留修订前后两版 score，应新开 `run_id` 或递增结果版本策略（由算法契约约定）。

按 `result_type` 执行条件必填约束：

| `result_type` | 必填字段 |
|---|---|
| `score` | `result_value`、`unit` |
| `label` | `result_label` |
| `rank` | `rank_no`；若同时保存 `result_value`，则 `unit` 必填 |
| `forecast` | `result_value`、`unit`、`forecast_date` |
| `contribution` | `dimension_code`、`contribution_level`、`contribution_value`、`unit`；当 `contribution_level=feature` 时还必须填写 `feature_code` |
| `cause` | `dimension_code`、`result_label`、`evidence_ref` |

**诊断瓶颈 / 卡脖子**（对齐 `DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806`）：

1. 健康分档（稳健/关注/薄弱）与是否瓶颈，分别用已登记的 `result_label` / `metric_id` 表达，禁止三词平级混写；
2. **卡脖子 = 已判定为瓶颈 ∧ `severity_level='high'`**；正式阈值与枚举以算法模型卡为准，入库前须在配置库登记；
3. `severity_level` 仅表示单次运行的原子严重度，不得直接写成页面「重点招商」等结论。

当 `uncertainty_type=interval` 时，`uncertainty_lower` 与 `uncertainty_upper` 必填且下界不得大于上界；其他不确定性类型使用 `uncertainty_value`。

`result_label`、`priority_level`、`severity_level` 和 `feature_code` 必须来自模型卡或配置库登记的编码；特征展示名、标签展示名和完整自然语言解释由 ADS 按编码、`evidence_ref` 和指标口径组装。`priority_level` 仅表示单次运行输出的原子等级编码，不得直接作为页面推荐结论。

正式 DDL 使用 `CHECK` 约束；若目标 MySQL 版本或 ETL 工具无法可靠执行 CHECK，则由入库校验脚本阻断不合规记录。

布局建议、解决方案、推荐文案和报告正文不进入 DWD；ADS/业务库通过 `run_id/result_id` 引用本表的原子结果。

---

## 6. IC-01～IC-43 覆盖矩阵

### 6.1 DWD 直接提供结构基础

| 需求 | 主要承载 |
|---|---|
| IC-03 市场规模 | **ADS 指标** `M_CHAIN_MARKET_SIZE`：Σ 链下企业年报营收（仅企业）；输入 = `industry_chain_entity_rel` + ENT 年报。**不**由 `market_observation` 直灌；该表仅承载外购/研报类原子观测 |
| IC-06 投融资 | `industry_chain_investment_event` + `industry_chain_investment_participant` |
| IC-09/19 热点资讯 | `industry_chain_news_event` + `industry_chain_event_metric_observation` + 模型结果 |
| IC-12 全要素图谱 | 三张 `industry_chain_*_rel` 关系表 + 其他权威数据域 + Nebula |
| IC-13/14 实体与关系抽取 | `industry_chain_extraction_result` |
| IC-15 十三类模型总包 | `industry_chain_model_run` + `industry_chain_model_result_detail` + 基础事实/关系 |
| IC-16/17 产业链全景 | `industry_chain`（含 `industry_id`/`chain_tier`）+ `industry_chain_node` + 两张结构关系表 |
| IC-18 发展历程 | **CMS 录入**（门户真源）；DWD `milestone_event` 仅可选结构化旁路，本轮 4 表不灌 |
| IC-20～28 九类分析模型 | `industry_chain_model_run` + `industry_chain_model_result_detail` |
| IC-29 综合能力总包 | DWD 原子数据 + cfg + Python + ADS + Nebula |
| IC-30～37 综合分析 | DWD 原子数据 + cfg + Python + ADS；瓶颈/卡脖子见 `result_label` + `severity_level` |
| IC-39 全景图 | `industry_chain` + `industry_chain_node` + 两张结构关系表 |
| IC-40 资讯事件线 | 两张事件主表 + `industry_chain_event_entity_rel` |

### 6.2 依赖其他权威数据域

| 需求 | 依赖 |
|---|---|
| IC-01/02 七类指标体系 | ENT/ORG/TALENT/TECH/POLICY/SVC DWD + `gkx_cfg` |
| IC-04 企业规模 | ENT 域企业主体和注册时间 |
| IC-05 机构规模 | ORG/SVC 域机构主体和注册时间 |
| IC-07/08/10/11 区域分布 | 主体权威域的地址历史 + `dim_region` |
| IC-12 全要素图谱 | 各数据域提供跨实体标准关系 |
| IC-17/20/26/27/28/35/36 深圳分析 | 深圳区域编码和全国/全球对标数据 |

### 6.3 不属于 DWD

| 需求 | 归属 |
|---|---|
| IC-02/03～11 的 API、消息队列和下载 | ADS + Java + 消息基础设施 |
| IC-24/26/27/28/34/36 的建议和推荐文案 | ADS/业务库 |
| IC-31/32 的参数编辑、自定义权重 | `gkx_cfg` + 业务配置库 |
| IC-38 专题入口和介绍 | **CMS**（含产业介绍正文）+ ADS 入口聚合 |
| IC-41 页面统计展示 | ADS |
| IC-42/43 内容管理 | CMS 业务库（含产业介绍、发展历程维护） |

### 6.4 覆盖判断

v5 在表结构层面补齐了 v4 已识别的 14 项结构缺口，但最终验收仍需满足：

1. 各权威数据域提供稳定业务键和主体历史；
2. `cfg_metric` 完成指标八件套和版本治理；
3. `cfg_model_registry` 完成模型注册和参数版本；
4. ADS 契约覆盖页面聚合、推荐和报告结果；
5. NebulaGraph schema 与 DWD 关系投影一致；
6. ODS 稳定后完成逐字段 Mapping 验证。

因此，本设计可以表述为：

> **DWD 目标结构已覆盖 IC-01～IC-41 所需的产业链域明细数据类型；完整业务能力仍依赖跨域 DWD、配置库、Python 模型、ADS、NebulaGraph、Java 和 CMS。**

不能表述为：

> “14 张 DWD 表单独完成全部 IC-01～IC-43。”

---

## 7. 数据质量规则

### 7.1 通用规则

1. 业务主键非空率必须为 100%；
2. 业务唯一键重复率必须为 0；
3. `source_system/source_table/source_record_id/etl_batch_id` 可追溯率必须为 100%；
4. 三张指标结果表的 `metric_id + metric_version` 必须存在于 `cfg_metric` 且版本匹配；`extraction_result.target_metric_id` 非空时，`target_metric_id + target_metric_version` 同样必须匹配；
5. `model_id/model_version` 必须存在于模型注册中心；
6. `region_code` 必须存在于 `dim_region`；
7. Mock 批次必须使用 `mock_` 前缀；
8. `confidence` 值域为 `[0,1]`；
9. `result_value` 和 `contribution_value` 等业务度量值必须明确 `unit`；仅金额类结果必须同时填写 `currency`，排名序号无需单位；
10. 逻辑删除记录不得出现在默认 ADS 查询结果。

### 7.2 关系规则

1. `source_node_id` 和 `target_node_id` 必须存在；
2. 节点关系禁止无业务说明的自环；
3. `entity_id` 必须能在对应权威数据域解析；
4. 同一关系在同一有效期内不得重复；
5. 投融资参与方的 `relation_id` 必须存在于 `industry_chain_event_entity_rel`；
6. Nebula 投影边数必须与有效 DWD 关系数可对账。
7. 三张关系表的 `valid_from` 必须非空。
8. `event_id` 必须以 `news:`、`invest:` 或 `milestone:` 等已注册事件前缀开头。
9. `event_entity_rel.event_id` 不建立跨三张事件表的物理多态 FK；ETL 必须按事件前缀路由到对应事件表并校验存在性；`event_kind` 必须与前缀一致（`invest`/`news`/`milestone`）。
10. 关系变更采用半开区间 `[valid_from, valid_to)`：先将当前有效行 `valid_to` 更新为新版本的 `valid_from`，再插入新行；删除时插入 `is_deleted=1` 的墓碑行，默认查询只取 `valid_to IS NULL AND is_deleted=0`。
11. 投融资参与方引用的事件关系必须满足 `event_id LIKE 'invest:%'`，且 `relation_type` 属于 `financing_subject`、`investor`、`lead_investor`、`follow_investor`；物理 FK 使用 `ON DELETE RESTRICT`。
12. `industry_chain.chain_tier` 只能取 `L0` / `L1` / `L2+`；`L0` 行建议 `industry_id = chain_id` 且 `parent_chain_id IS NULL`；`L1`/`L2+` 行的 `industry_id` 必须能解析到有效 L0 行。

### 7.3 模型结果规则

1. 成功运行至少产生一条结果明细；
2. 结果明细的 `run_id` 必须对应成功或 partial 的模型运行；
3. 抽取结果的 `run_id` 必须对应 `run_type=extraction` 的模型运行；
4. 各 `result_type` 的条件必填字段严格以 §5.14 条件必填表为准；
5. 对比类模型在运行级必须填写 `model_run.benchmark_scope`；需要逐对象对比时，结果行还必须填写 `model_result_detail.benchmark_id`；
6. `run_type=forecast` 的模型运行必须填写 `forecast_horizon`；仅 `result_type=forecast` 的结果明细必须填写 `forecast_date`；
7. 自定义权重模型必须填写 `parameter_version`；
8. `cause` 结果必须填写 `evidence_ref`；
9. 其他重要结论必须有 `evidence_ref` 或对应的因素贡献结果。
10. `object_type` 为关系类型时只能取 `node_relation`、`chain_entity_relation`、`event_entity_relation`，且 `object_id` 必须能在对应关系表解析。
11. `result_label`、`priority_level`、`severity_level`、`feature_code` 必须存在于模型卡或配置库枚举，不得写入未登记的自由文本建议或展示名称。
12. 抽取结果的 `document_id + document_version` 必须能在权威文档域解析，并与 `model_run.input_snapshot_ref` 对账。
13. **禁止**将跨 `run_id`、跨对象 TopN 或页面排序结果写入 DWD；`rank_no` 仅允许单次 run 内原子排名。
14. 卡脖子判定不得单独造词入库：必须同时满足「瓶颈类 `result_label`/`metric_id`」与 `severity_level='high'`。

---

## 8. 索引和性能建议

必须建立以下查询索引：

- 产业链：`industry_id + chain_tier`、`parent_chain_id`、`chain_level`；
- 节点关系：`chain_id`、`source_node_id`、`target_node_id`；
- 产业链实体关系：`chain_id`、`node_id`、`entity_type + entity_id`；
- 市场观测：`chain_id + metric_id + stat_date`、`region_code + stat_date`；
- 事件表：`chain_id + event_date/publish_time`、`region_code`；里程碑另加 `chain_id + phase_id + event_date`；
- 事件关系：`event_id`、`event_kind`、`entity_type + entity_id`；
- 事件指标：`event_id + metric_id + observed_time`；
- 抽取结果：`run_id`、`document_id`、`normalized_entity_id`；
- 模型运行：`run_type`、`model_id + chain_id + stat_date`；
- 模型结果：`run_id`、`chain_id + metric_id`、`region_code + metric_id`、`forecast_date`、`severity_level`；
- 唯一指纹：`observation_scope_key`、`metric_observation_scope_key`、两处 `result_fingerprint`。

所有指纹字段必须调用统一 `fingerprint_v1` 公共函数：字段完成各自规范化和空值哨兵替换后，以 `UTF8字节长度:字段值` 逐字段编码，按字段清单顺序拼接并计算 SHA-256。若使用 MySQL 生成列，必须采用 `STORED GENERATED` 并与 ETL 公共函数运行同一组黄金样例，禁止各任务自行实现哈希规则。`news_dedup_key` 属资讯去重规则，不复用 `fingerprint_v1`。

大规模时序观测表可按 `stat_date/observed_time` 年或月分区；是否启用物理分区由数据 Lead 根据实际量级评审。

---

## 9. 开放项

| 开放项 | 状态 | 影响 |
|---|---|---|
| Q053：INB 与国标产业编码方案 | **🟢 已冻结**（2026-08-07 `human:李伟`；`DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md`） | 平台主键 = INB；国标仅可选对照表 |
| Q054：投融资 ODS 空表 | 待供应方确认 | 投融资真实数据接入 |
| Q055：机构主体源表数据不足 | 待供应方确认 | 机构规模、分布和图谱 |
| `industry_id` 与企业域「所属产业」码表对齐 | 待架构/数据 Lead；v5 已加字段 | 门户选择器、对比篮、跨模块路由 |
| 诊断 severity / 瓶颈 label 正式枚举 | 待算法 Lead 模型卡；v5 已加 `severity_level` | IC-33/34 卡脖子判定 |
| 价值链五环节（研发/设计/制造/销售/服务）枚举 | 待 `gkx_cfg`；映射到 `node_type` 或诊断 `dimension_code` | 关键环节/瓶颈页 |
| 图谱演进快照 ADS 契约（Q062 类） | 待后续 ADS 任务；DWD 关系表仍为真源 | 全景演进 diff |
| 指标八件套未逐项冻结 | 待指标语义 Owner；v5 已明确入库门禁 | 市场、区域、模型结果口径 |
| 模型参数和权重版本未冻结 | 待算法 Lead | IC-20～37 可复现性 |
| ADS 契约未随 v5 重做 | 待后续任务；v5 已冻结最小追溯字段 | 页面和 API 完整覆盖 |
| `talent_uid/tech_uid/product_uid/patent_uid` 未冻结 | 待平台架构评审；生产关联保持阻塞 | 全要素关系和图谱实体解析 |
| 跨域文档统一主键/版本契约未冻结 | 待平台架构和数据 Lead 评审；v5 已定义解析门禁 | IC-13/14 多源抽取追溯 |

---

## 10. 后续步骤

1. 由李伟和架构师 Lead 评审 14 张表的边界（含 2026-08-07 字段增补）；
2. 数据 Lead 评审粒度、唯一键、历史策略、索引和 DQ；
3. 指标语义 Owner 评审 `metric_id`、公式和口径版本；
4. 算法 Lead 评审模型运行与结果明细能否覆盖 13 类深度模型，并冻结 severity/瓶颈枚举；
5. 将 IC-01～IC-43 细化到字段级 TRACE；
6. 按 v5 重做 ADS 契约（含图谱快照），不再引用 DWM；
7. **Q053 已冻结（INB）**后，由 GDF/data-agent 按方案 A 完成 ODS→DWD 结构子集映射与灌数；
8. Mapping 验证后输出正式 DDL 和迁移方案；
9. 经人类会签且 P0 开放项闭合前，本文件不得作为生产建表或对甲方承诺依据。
