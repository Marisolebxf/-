# 产业链 ODS → DWD 字段映射复核报告（Step 2）

> 任务：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 责任人：`[human:李伟]`（架构师）  
> 执行角色：`agent:architect-agent`  
> 实时核验：2026-08-03  
> 目标 DWD：`产业链-DWD表设计-业务需求驱动(v5).md`（14 张表）  
> 入站源：MySQL `183.240.141.251:3318/gkx`，只读账号 `gkx_reader_zp`  
> 扫描范围：全部 `dwd_*`，排除表名包含 `_bak_` 的备份表

---

## 1. 扫描口径

供应方库中的 `dwd_*` 表在供应方内部属于清洗结果，但在本项目链路中是 **ODS 入站源**：

```text
供应方 gkx.dwd_* → 本项目 DWD industry_chain_* → ADS → Java/API
```

本报告同时判断两个维度：

- **字段结构匹配**：源表字段是否能够映射到目标 DWD 字段；
- **当前实际可灌**：源表当前是否存在有效数据。

状态定义：


| 状态  | 含义                            |
| --- | ----------------------------- |
| ✅   | 可直接映射                         |
| 🔧  | 可经拆行、关联、标准化或生成映射              |
| 🟡  | 字段存在，但依赖编码/业务键/跨域契约           |
| ❌   | 当前 ODS 无可用字段                  |
| 🧮  | 应由本项目 Python/系统生成，不由 ODS 直接提供 |


---



## 2. 全库扫描结论



### 2.1 表数量


| 项                        | 实时结果      |
| ------------------------ | --------- |
| 有效 `dwd_*` 表（排除 `_bak_`） | **269 张** |
| 直接产业链核心候选表               | 16 张      |
| 当前有直接产业链关联数据的表           | **1 张**   |




### 2.2 直接产业链候选表数据量


| ODS 表                                         | 当前行数    | 用途             |
| --------------------------------------------- | ------- | -------------- |
| `dwd_industry_chain_info`                     | 0       | 产业链、节点、父子层级    |
| `dwd_industry_code`                           | 0       | 产业链、节点、定义、关键环节 |
| `dwd_industry_chain_news_info`                | 0       | 产业资讯           |
| `dwd_org_industry_tags`                       | 0       | 链/节点—企业关系      |
| `dwd_org_industry_product_tags`               | 0       | 链/节点—产品关系      |
| `dwd_org_industry_chain_pat_dtl`              | **888** | 链/节点—专利关系      |
| `dwd_org_financing_info`                      | 0       | 融资事件           |
| `dwd_org_invest_info`                         | 0       | 投资关系           |
| `dwd_org_merger_acquisition_info`             | 0       | 并购事件           |
| `dwd_merger_acquisition_events_info`          | 0       | 并购事件           |
| `dwd_merger_acquisition_events_party_info`    | 0       | 并购参与方          |
| `dwd_industrial_fund_basic_info`              | 0       | 产业基金           |
| `dwd_industrial_fund_investment_project_info` | 0       | 产业基金投资汇总       |
| `dwd_news_base`                               | 0       | 通用资讯           |
| `dwd_org_important_news_info`                 | 0       | 机构重点资讯         |
| `dwd_macro_index_data`                        | 0       | 宏观指标观测         |




### 2.3 唯一直接可用源的质量

`dwd_org_industry_chain_pat_dtl`：


| 指标                  | 结果  |
| ------------------- | --- |
| 总行数                 | 888 |
| 产业链数                | 2   |
| 节点数                 | 11  |
| 专利申请号数              | 888 |
| 缺失 `chain_code`     | 0   |
| 缺失 `node_id`        | 0   |
| 缺失 `apno`           | 0   |
| 缺失 `pat_name`       | 0   |
| 缺失 `current_assign` | 0   |


产业链覆盖：


| `chain_code` | `chain_name` | 行数  |
| ------------ | ------------ | --- |
| `IC0007`     | 集成电路         | 862 |
| `IC9901`     | 低空经济         | 26  |


结论：当前只能可靠产生这 2 条链、11 个节点及 888 条链—专利关系；不能据此认为产业链全域已覆盖。

### 2.4 有数据但缺产业链关联的辅助源


| ODS 表                        | 实际行数   | 可提供             | 为什么不能直接灌 CHAIN DWD                |
| ---------------------------- | ------ | --------------- | --------------------------------- |
| `dwd_org_annual_report_base` | 770000 | 企业信用代码、名称、地址、年度 | 无 `chain_id/node_id`；主体属性应归 ENT 域 |
| `dwd_forg_industry`          | 7569   | 国外企业行业代码        | 行业代码未映射到平台产业链编码                   |
| `dwd_forg_investment`        | 12199  | 国外企业持股关系        | 无事件日期、金额和产业链关系                    |
| `dwd_author_affiliation`     | 1647   | 作者—机构关系、区域      | 无人才—产业链关系                         |
| `dwd_org_innovation_carrier` | 1449   | 创新载体、区域、公告      | 无产业链标签                            |
| `dwd_zh_report_scholar`      | 2000   | 报告—学者关系         | 无报告正文和产业链标签                       |


这些表可作为跨域权威数据或后续算法输入，但不能绕过标准业务键和产业链映射直接写入 CHAIN DWD。

---



## 3. 公共治理字段映射

v5 的 14 张表都包含公共治理字段。供应方多数表有六个技术字段，统一映射如下：


| 目标字段               | ODS 来源                 | 规则                                     |
| ------------------ | ---------------------- | -------------------------------------- |
| `id`               | 无                      | 🧮 本项目生成物理主键                           |
| `source_system`    | 常量                     | 🧮 固定为供应方系统标识                          |
| `source_table`     | 当前源表名                  | 🧮 例如 `dwd_org_industry_chain_pat_dtl` |
| `source_record_id` | `pk_id/id/apno/...`    | 🔧 按各表稳定行键选择                           |
| `etl_batch_id`     | 无                      | 🧮 数据工厂生成                              |
| `data_version`     | `updated_time` 或行内容哈希  | 🔧 无来源版本时由数据工厂生成                       |
| `valid_from`       | 业务日期；其次 `created_time` | 🔧 按表定义                                |
| `valid_to`         | 无                      | 🧮 当前快照为空；历史关系由数据工厂维护                  |
| `is_deleted`       | `is_deleted`           | ✅ 无该字段的源表默认 0，并记录映射说明                  |
| `created_time`     | `created_time`         | ✅                                      |
| `updated_time`     | `updated_time`         | ✅                                      |
| `ext`              | 未正式建模字段                | 🔧 JSON 兜底，不得替代正式字段                    |


特殊情况：`dwd_org_industry_chain_pat_dtl` 没有 `is_deleted/table_data_source`，可用 `data_source` 作为来源标识，`is_deleted` 暂按 0，但必须登记供应方删除同步策略。

算法及抽取表不使用供应方六技术字段，按 v5 特例填写：


| 目标表                                  | `source_system`          | `source_table`             | `source_record_id` | `valid_from`                             |
| ------------------------------------ | ------------------------ | -------------------------- | ------------------ | ---------------------------------------- |
| `industry_chain_model_run`           | `gkx-algorithm-platform` | `cfg_model_registry`       | `run_id`           | `started_time`                           |
| `industry_chain_model_result_detail` | 继承运行记录                   | `industry_chain_model_run` | `result_id`        | `COALESCE(completed_time, started_time)` |
| `industry_chain_extraction_result`   | 输入文档所属系统                 | 输入文档所在权威 DWD 表             | `document_id`      | `COALESCE(completed_time, started_time)` |


---



## 4. 14 张目标 DWD 表逐字段映射



## 4.1 `industry_chain`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `chain_id` | 平台归一产业链主键 | `dwd_industry_chain_info.industry_code`；`dwd_industry_code.industry_code`；`dwd_org_industry_chain_pat_dtl.chain_code` | 🟡 | 需按 Q053 归一；当前可从专利表得到 2 条 |
| `chain_code` | 来源产业链编码 | 同上 | ✅ | 当前 2 个编码 |
| `chain_name` | 产业链标准名称 | `dwd_industry_chain_info.industry_name`；`dwd_industry_code.industry_name`；`dwd_org_industry_chain_pat_dtl.chain_name` | ✅ | 当前可灌 |
| `chain_short_name` | 产业链简称 | 无 | ❌ | ODS 无简称 |
| `parent_chain_id` | 上级产业链主键 | 无可靠字段 | ❌ | `parent_code` 是节点父级，不是上级产业链 |
| `chain_level` | 产业链层级 | `dwd_industry_code.level`（需筛选产业根） | 🔧 | 主源 0 行；专利源只能给默认根层级 |
| `chain_category` | 产业链分类 | `dwd_industry_code.industry_code` 或外部分类映射 | 🟡 | 需确认分类语义 |
| `future_industry_flag` | 八大未来产业标记 | 无 | ❌ | 需配置库/人工标注 |
| `description` | 产业链说明 | `dwd_industry_code.definition` | ✅ | 源表 0 行 |
| `status` | 启用或有效状态 | `is_deleted` 派生 | 🔧 | 专利源无删除标识 |


**当前结论：部分可灌。** 可派生 2 条产业链基础记录，无法完整提供层级、分类、未来产业标识和状态。

## 4.2 `industry_chain_node`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `node_id/node_code` | 节点归一主键/来源编码 | `dwd_industry_chain_info.industry_link_code`；`dwd_industry_code.code`；`dwd_org_industry_chain_pat_dtl.node_id` | ✅ | 当前 11 个节点 |
| `chain_id` | 所属产业链主键 | `industry_code`；`dwd_org_industry_chain_pat_dtl.chain_code` | 🟡 | 需 Q053 归一 |
| `node_name` | 节点标准名称 | `industry_link_name`；`dwd_industry_code.name`；`dwd_org_industry_chain_pat_dtl.node_name` | ✅ | 当前可灌 |
| `parent_node_id` | 父节点主键 | `dwd_industry_chain_info.parent_code`；`dwd_industry_code.parent_code` | ✅ | 两个源表均 0 行 |
| `node_level` | 节点层级 | `dwd_industry_chain_info.level`；`dwd_industry_code.level` | ✅ | 当前专利源没有 |
| `stage_code` | 上中下游阶段编码 | 无 | ❌ | 需节点字典或规则 |
| `node_type` | 环节、工艺、产品或技术类型 | 无直接字段 | ❌ | 需配置/规则分类 |
| `importance_level` | 来源明确的节点重要性 | 无 | ❌ | 不可把算法得分回写节点表 |
| `sort_no` | 同级节点排序号 | 无 | ❌ | 系统生成或配置 |
| `node_path` | 节点层级路径 | `parent_code` 递归派生 | 🔧 | 当前无法从专利源派生 |
| `description` | 节点定义或说明 | `dwd_industry_code.definition` | ✅ | 源表 0 行 |
| `status` | 节点有效状态 | `is_deleted` 派生 | 🔧 | 当前专利源无删除标识 |


**当前结论：部分可灌。** 可得到 11 个节点的编码、名称和所属链，缺父子层级、阶段、类型、路径等。

## 4.3 `industry_chain_node_rel`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `relation_id` | 节点关系稳定主键 | 无 | 🧮 按链、父节点、子节点和有效期生成 |
| `chain_id` | 所属产业链主键 | `dwd_industry_chain_info.industry_code`；`dwd_industry_code.industry_code` | ✅ |
| `source_node_id` | 关系起点节点 | `parent_code` | 🔧 父节点 |
| `target_node_id` | 关系终点节点 | `industry_link_code` 或 `code` | 🔧 子节点 |
| `relation_type` | 上下游、依赖等关系编码 | 常量 `parent_child`/配置映射 | 🧮 |
| `relation_direction` | 关系方向 | 常量 `directed` | 🧮 |
| `relation_weight` | 来源明确的关系强度 | 无 | ❌ |
| `confidence` | 来源或抽取置信度 | 无 | ❌ |
| `evidence_ref` | 关系证据引用 | `source_table + source_record_id` | 🔧 |


**当前结论：结构可派生、当前不可灌。** 两个层级源表均为 0 行，专利源没有父子节点。

## 4.4 `industry_chain_entity_rel`


| 关系类型 | 注解 | 来源表.字段 | 目标字段映射 | 当前状态 |
|---|---|---|---|---|
| 链/节点—企业 | 企业参与产业链或节点 | `dwd_org_industry_tags.industry_code/industry_link_code/credit_code` | `chain_id/node_id/entity_type='enterprise'/entity_id` | 结构匹配，0 行 |
| 链/节点—产品 | 产品归属产业链或节点 | `dwd_org_industry_product_tags.industry_code/industry_link_code/product_name` | `entity_type='product'`，产品 UID 待冻结 | 结构匹配，0 行 |
| 链/节点—专利 | 专利适用于产业链或节点 | `dwd_org_industry_chain_pat_dtl.chain_code/node_id/apno` | `entity_type='patent'`、`entity_id=apno`（临时） | **888 行可用** |
| 量子链—实体 | 量子专题既有实体关系 | `dwd_quantum_chain_link.industry_chain_id/link_code/entity_type/entity_id` | 对应关系字段 | 结构匹配，0 行 |
| 链—人才/技术/政策/机构 | 七要素跨域关系 | 无直接产业链关联表 | 需跨域业务键 + 分类/NLP | ❌ |


其他字段：


| 目标字段 | 字段注解 | 来源/规则 | 状态 |
|---|---|---|---|
| `relation_id` | 实体关系稳定主键 | 业务字段指纹生成 | 🧮 |
| `node_scope_key` | 链级/节点级关系去重键 | `COALESCE(node_id, '__CHAIN__')` | 🧮 目标生成列 |
| `entity_subtype` | 外部实体细分类别 | 产品/专利/机构类型字典 | 🔧 |
| `relation_type` | 实体与链/节点的关系编码 | 企业 `participates_in`、产品 `produces`、专利 `applies_to` 等配置编码 | 🧮 |
| `role_type` | 实体在产业链中的业务角色 | 无稳定来源 | ❌ |
| `importance_level` | 来源明确的关系重要性 | 人工明确来源才可写 | ❌ |
| `confidence` | 规则或抽取置信度 | 规则/NLP 产出 | 🧮 |
| `is_primary` | 是否主要归属关系 | 无 | ❌ |
| `evidence_ref` | 关系证据引用 | `apno/pn/data_source` 或来源记录引用 | 🔧 |


**当前结论：仅链—专利关系可灌。** 当前可形成 888 条候选关系；`patent_uid` 未冻结前不得作为生产跨域键。

## 4.5 `industry_chain_market_observation`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `observation_id` | 市场观测业务主键 | 来源观测业务键；无稳定键时按来源记录生成 | 🔧 |
| `chain_id` | 所属产业链主键 | 各专题固定链映射；通用指标源无直接链编码 | 🟡 |
| `node_id` | 所属节点主键 | 无通用来源 | ❌ |
| `region_code` | 观测区域编码 | `dwd_macro_index_data.area_code`；`dwd_series_metadata.metadata_country_id`；`dwd_quantum_market_scale.region` | 🔧 |
| `metric_id` | 指标注册中心编码 | `dwd_macro_index_data.index_code`；`dwd_series_metadata.metadata_indicators`；专题指标配置 | 🔧 |
| `metric_version` | 指标口径版本 | 无 | 🧮 指标注册中心 |
| `stat_period` | 年、季、月或日统计周期 | `occur_period_t`；`metadata_frequency_id/name`；`stat_year` | 🔧 |
| `period_start/period_end/stat_date` | 统计期起止及基准日 | `occur_period*`；`timepoints_date`；`stat_year` | 🔧 |
| `observation_value` | 原子观测值 | `index_value`；`timepoints_value`；`market_size_100m` | ✅ |
| `unit` | 观测值单位 | `unit_use`；`metadata_unit_name`；专题固定单位 | ✅ |
| `currency` | 金额观测币种 | 指标配置 | 🟡 |
| `price_basis` | 当年价或不变价等价格口径 | 无 | ❌ |
| `market_scope` | 全球、全国或区域市场范围 | 区域/国家字段派生 | 🔧 |
| `extraction_id/extraction_run_id` | 文本抽取结果及运行引用 | 无 | 🧮 结构化源均留空；文本抽取源由 Python 填写 |
| `observation_scope_key` | 市场观测防重指纹 | 目标字段生成 | 🧮 |


候选源 `dwd_macro_index_data`、`dwd_series_metadata/timepoints`、`dwd_quantum_market_scale` 当前均为 0 行，且通用数列缺稳定产业链映射。

**当前结论：字段结构部分匹配，当前不可灌。**

## 4.6 `industry_chain_investment_event`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `event_id` | 平台全域投融资事件主键 | 无 | 🧮 本项目生成 `invest:*` 全域事件键 |
| `source_investment_id` | 来源投融资事件 ID | `dwd_org_financing_info.pk_id`；`dwd_merger_acquisition_events_info.zzzjid` | 🔧 |
| `chain_id/node_id` | 事件所属产业链和节点 | 事件企业 JOIN `dwd_org_industry_tags` | 🟡 |
| `investment_type` | 投资、融资、并购等事件类型 | 融资常量；`dwd_merger_acquisition_events_info.bdlx` | 🔧 |
| `financing_round` | 融资轮次 | `dwd_org_financing_info.funding_round` | ✅ |
| `amount` | 事件总金额 | `funding_amount`；`jyje`；`ma_amount` | ✅ |
| `currency` | 事件金额币种 | `funding_currency_code`；`currency_code`；`mgjgbz` | ✅/🟡 |
| `event_date` | 事件发生或完成日期 | `completion_date`；`ggrq/bgwcsj` | ✅ |
| `region_code` | 事件关联区域编码 | 事件主体 JOIN 主体域地址 | 🔧 |
| `description` | 事件说明 | `bdxq/jyjj/bz` | ✅ |
| `evidence_ref` | 公告或报道证据引用 | 来源记录引用 | 🔧 |


`dwd_org_invest_info` 只有投资双方、金额、股比，没有事件日期和币种，更适合关系辅助，不足以独立形成完整投资事件。

**当前结论：字段结构基本匹配，所有直接事件源均为 0 行，当前不可灌。**

## 4.7 `industry_chain_investment_participant`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `participant_record_id` | 参与方扩展记录主键 | 事件+参与方业务键生成 | 🧮 |
| `relation_id` | 对应事件—实体关系主键 | `industry_chain_event_entity_rel.relation_id` | 🔧 必须复用父关系主键，不得独立生成 |
| 参与方实体 | 父关系中的投资方或融资方，不落本表字段 | `dwd_org_financing_info.external_id/investors_name`；`dwd_merger_acquisition_events_party_info.jgid/dsrmc/dsrlx` | 🔧 |
| `participation_amount` | 单个参与方金额 | 无可靠逐参与方金额；事件表只有总金额 | ❌ |
| `currency` | 参与方金额币种 | 继承事件币种 | 🔧 |


`investors_name` 是文本列表，必须拆分并完成机构归一；角色写入 `industry_chain_event_entity_rel.relation_type`，不得在扩展表重复保存。

**当前结论：部分字段可匹配，当前 0 行且缺逐参与方金额。**

## 4.8 `industry_chain_news_event`


| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `event_id` | 平台全域资讯事件主键 | 无 | 🧮 本项目生成 `news:*` 全域事件键 |
| `source_news_id` | 来源资讯业务 ID | `dwd_industry_chain_news_info.id`；`dwd_news_base.zzzjid`；`dwd_org_important_news_info.pk_id` | ✅/🔧 |
| `chain_id` | 资讯所属产业链 | `dwd_industry_chain_news_info.industry_code` | ✅ |
| `node_id` | 资讯所属产业链节点 | 无直接字段 | ❌ |
| `title` | 资讯标题 | `title`；`dwd_news_base.bt`；`news_title` | ✅ |
| `summary` | 来源摘要或 NLP 摘要 | `abstract`；`dwd_news_base.zy`；`news_content` | ✅ |
| `news_type` | 政策、技术、市场、企业等资讯分类 | `dwd_news_base.lx` 或 NLP 分类 | 🔧 |
| `source_name` | 来源媒体名称 | `source`；`dwd_news_base.lymc` | ✅ |
| `author_name` | 原文署名作者或发布机构 | 无 | ❌ |
| `source_url` | 原始报道链接 | `dwd_news_base.lylj`；`original_textlink` | ✅ |
| `source_url_hash/news_dedup_key` | URL 哈希及资讯防重指纹 | URL/来源 ID/标题生成 | 🧮 |
| `publish_time` | 资讯发布时间 | `publish_date`；`fbsj`；`news_date` | ✅ |
| `region_code` | 资讯关联区域编码 | 关联主体或 NLP 派生 | 🔧 |


**当前结论：字段结构匹配度较高，但三个主要资讯源均为 0 行，当前不可灌。**

## 4.9 `industry_chain_milestone_event`


| 目标字段 | 字段注解 | 候选来源 | 状态 |
|---|---|---|---|
| `event_id` | 平台全域里程碑事件主键 | 系统生成 `milestone:*` | 🧮 |
| `source_milestone_id/source_event_id` | 来源里程碑 ID 及来源事件 ID | 资讯、政策、项目、公告的业务 ID | 🔧 |
| `chain_id/node_id` | 里程碑所属产业链和节点 | 产业链资讯直接映射，其他文档需 NLP/实体关系 | 🟡 |
| `event_name` | 重大事件标题 | 资讯/政策/项目/公告标题 | ✅ |
| `milestone_type/event_level` | 里程碑类型及重要程度 | 阈值、规则或模型识别 | 🧮 |
| `event_date` | 里程碑发生日期 | 发布时间、立项时间、公告时间 | ✅ |
| `source_event_type` | 来源事件类型 | `news/policy/project/announcement` | 🧮 |
| `description` | 里程碑说明 | 摘要、正文、公告 | ✅ |
| `region_code` | 事件关联区域编码 | 来源区域或主体地址 | 🔧 |
| `evidence_ref` | 来源证据引用 | 原文 URL/来源记录 | ✅/🔧 |


候选表包括 `dwd_industry_chain_news_info`、`dwd_zck_policy`、`dwd_zck_intl_policy`、`dwd_zh_project`、`dwd_en_project`、`dwd_org_innovation_carrier`。其中只有创新载体表当前有数据，但没有产业链关联，不能直接生成产业里程碑。

**当前结论：需 Python/NLP 派生，当前无可直接灌记录。**

## 4.10 `industry_chain_event_entity_rel`


| 关系 | 注解 | 来源表.字段 | 当前状态 |
|---|---|---|---|
| 融资主体/投资方 | 投融资事件与融资方、投资方关系 | `dwd_org_financing_info.external_id/investors_name` | 0 行 |
| 并购主体 | 并购事件与收购方、被收购方关系 | `dwd_merger_acquisition_events_party_info.jgid/dsrmc/dsrlx` | 0 行 |
| 机构资讯主体 | 资讯事件关联机构 | `dwd_org_important_news_info.external_id/org_id` | 0 行 |
| 资讯关联企业 | 通用资讯关联企业 | `dwd_news_base.xgqyxx` | 0 行，需解析 |
| 政策发布方 | 政策事件发布机构 | `dwd_zck_policy.pubdeptname` | 0 行，需机构归一 |
| 里程碑影响对象 | 里程碑影响的企业、机构等实体 | 无直接字段 | 模型/NLP |


通用字段 `relation_id/relation_type/confidence/evidence_ref` 均需标准化生成。

**当前结论：结构可映射，当前不可灌。**

## 4.11 `industry_chain_event_metric_observation`


| 目标字段 | 字段注解 | 候选来源 | 状态 |
|---|---|---|---|
| `observation_id` | 事件指标观测主键 | 来源观测业务键；无稳定键时按事件、指标和观测时间生成 | 🔧 |
| `event_id` | 被观测事件主键 | 事件业务键 | 🔧 |
| `metric_id/metric_version` | 互动指标编码及口径版本 | 指标注册中心 | 🧮 |
| `observed_time` | 指标采集时间 | 来源采集时间 | 🔧 |
| `metric_value` | 浏览、评论、转发、点赞等原子值 | 浏览量、评论量、转发量、点赞量 | ❌ |
| `unit` | 指标单位 | 指标配置 | 🧮 |
| `metric_observation_scope_key` | 事件指标防重指纹 | 目标字段生成 | 🧮 |


全库未找到产业资讯浏览量、评论量、转发量、点赞量的可用入站字段。`dwd_zh_paper.download_num` 是论文下载量，且当前 0 行，不能替代产业资讯互动指标。

**当前结论：ODS 不满足，当前不可灌。**

## 4.12 `industry_chain_extraction_result`

该表保存的是本项目模型抽取结果，不应从供应方表直接复制。逐字段来源如下：


| 目标字段 | 字段注解 | 来源/规则 | 状态 |
|---|---|---|---|
| `extraction_id` | 抽取结果主键 | 抽取运行和结果指纹生成 | 🧮 |
| `run_id` | 所属抽取运行主键 | `industry_chain_model_run.run_id` | 🧮 |
| `result_type` | 实体、关系或属性抽取类型 | Python 输出 `entity/relation/attribute` | 🧮 |
| `document_id` | 输入文档统一主键 | `dwd_industry_chain_news_info.id`、`dwd_news_base.zzzjid`、`dwd_zck_policy.id`、论文/项目/报告/专利业务键 | 🔧 |
| `document_type` | 输入文档类型 | 按输入表映射 `news/policy/paper/project/report/patent` | 🧮 |
| `document_version` | 输入文档内容版本 | 输入表 `updated_time` 或规范化内容 SHA-256 | 🔧 |
| `sentence_id` | 文档句段主键 | 文档切分器生成 | 🧮 |
| `mention_text` | 实体原始提及文本 | Python 实体识别输出 | 🧮 |
| `char_start` | 实体提及起始字符位置 | Python 实体识别输出 | 🧮 |
| `char_end` | 实体提及结束字符位置 | Python 实体识别输出 | 🧮 |
| `entity_type` | 识别出的实体类型 | Python + 实体类型配置 | 🧮 |
| `normalized_entity_id` | 归一后的实体业务键 | 跨域实体归一服务返回 | 🧮 |
| `candidate_entities` | 实体消歧候选列表 | Python 消歧候选列表 | 🧮 |
| `subject_entity_type` | 关系主语实体类型 | Python 关系抽取输出 | 🧮 |
| `subject_entity_id` | 关系主语归一实体键 | 跨域实体归一服务返回 | 🧮 |
| `subject_mention_text` | 关系主语原始文本 | Python 关系抽取输出 | 🧮 |
| `subject_char_start` | 主语起始字符位置 | Python 关系抽取输出 | 🧮 |
| `subject_char_end` | 主语结束字符位置 | Python 关系抽取输出 | 🧮 |
| `predicate_code` | 标准关系谓词编码 | 关系谓词配置 + Python 输出 | 🧮 |
| `object_entity_type` | 关系宾语实体类型 | Python 关系抽取输出 | 🧮 |
| `object_entity_id` | 关系宾语归一实体键 | 跨域实体归一服务返回 | 🧮 |
| `object_mention_text` | 关系宾语原始文本 | Python 关系抽取输出 | 🧮 |
| `object_char_start` | 宾语起始字符位置 | Python 关系抽取输出 | 🧮 |
| `object_char_end` | 宾语结束字符位置 | Python 关系抽取输出 | 🧮 |
| `attribute_code` | 标准属性编码 | 属性字典 + Python 输出 | 🧮 |
| `attribute_value` | 属性抽取值 | Python 属性抽取输出 | 🧮 |
| `attribute_value_type` | 属性值数据类型 | Python 按属性类型生成 | 🧮 |
| `attribute_unit` | 属性值单位 | 属性/指标配置 | 🧮 |
| `target_metric_id` | 属性对应指标编码 | `cfg_metric.metric_id` | 🧮 |
| `target_metric_version` | 属性对应指标口径版本 | `cfg_metric.version` | 🧮 |
| `confidence` | 抽取置信度 | Python 模型输出 | 🧮 |
| `evidence_text` | 支撑结果的原文证据 | 输入文档证据片段 | 🧮 |
| `result_fingerprint` | 抽取结果防重指纹 | 本项目统一 `fingerprint_v1` 生成 | 🧮 |


可作为输入文档的 ODS 表包括资讯、政策、论文、项目、报告和专利相关表；但这些候选表目前绝大多数为 0 行，且不存在供应方抽取结果表。

**当前结论：不能直接灌数，必须由 Python 生成。**

## 4.13 `industry_chain_model_run`

全部字段由本项目算法平台生成：

| 目标字段 | 字段注解 | 来源/规则 | 状态 |
|---|---|---|---|
| `run_id` | 模型运行主键 | 算法平台生成 | 🧮 |
| `run_type` | 抽取、分析或预测运行类型 | 算法任务配置 | 🧮 |
| `model_id` | 模型注册中心编码 | `cfg_model_registry` | 🧮 |
| `model_version` | 模型版本 | 模型注册中心 | 🧮 |
| `parameter_version` | 参数和权重版本 | 算法配置 | 🧮 |
| `calc_batch_id` | 模型计算批次 | 算法平台生成 | 🧮 |
| `chain_id` | 分析产业链主键 | 运行输入参数 | 🧮 |
| `region_code` | 分析区域编码 | 运行输入参数 | 🧮 |
| `benchmark_scope` | 全国、全球或自定义对标范围 | 运行输入参数 | 🧮 |
| `scenario_id` | 情景模拟主键 | 情景配置 | 🧮 |
| `forecast_horizon` | 预测期长度 | 预测任务配置 | 🧮 |
| `stat_date` | 分析基准日期 | 运行输入参数 | 🧮 |
| `started_time` | 运行开始时间 | 算法平台 | 🧮 |
| `completed_time` | 运行完成时间 | 算法平台 | 🧮 |
| `run_status` | 成功、失败或部分成功状态 | 算法平台 | 🧮 |
| `input_snapshot_ref` | 输入数据快照引用 | 算法平台生成 | 🧮 |
| `model_card_ref` | 模型卡引用 | 模型注册中心 | 🧮 |

**当前结论：不应从 ODS 灌数。**

## 4.14 `industry_chain_model_result_detail`

全部业务结果字段由 Python 模型生成，ODS 只作为输入：

| 目标字段 | 字段注解 | 来源/规则 | 状态 |
|---|---|---|---|
| `result_id` | 模型结果主键 | Python 生成 | 🧮 |
| `run_id` | 所属模型运行主键 | `industry_chain_model_run.run_id` | 🧮 |
| `object_type` | 链、节点、关系、事件、区域等对象类型 | 模型输出配置 | 🧮 |
| `object_id` | 被分析对象业务键 | 对应权威对象主键 | 🧮 |
| `chain_id` | 所属产业链主键 | 运行输入/对象关系 | 🧮 |
| `node_id` | 所属节点主键 | 对象关系 | 🧮 |
| `region_code` | 对象区域编码 | 对象关系/运行输入 | 🧮 |
| `benchmark_id` | 对标对象或对标组主键 | 运行配置 | 🧮 |
| `metric_id` | 结果指标编码 | `cfg_metric.metric_id` | 🧮 |
| `metric_version` | 指标口径版本 | `cfg_metric.version` | 🧮 |
| `dimension_code` | 技术、人才、市场等分析维度 | 模型配置 | 🧮 |
| `contribution_level` | 维度级或特征级贡献层级 | 模型输出 | 🧮 |
| `feature_code` | 模型特征编码 | 模型卡/配置库 | 🧮 |
| `result_type` | 评分、标签、排名、预测、贡献或原因 | 模型输出 | 🧮 |
| `result_value` | 数值型模型结果 | Python 模型输出 | 🧮 |
| `result_label` | 标签或短原因编码 | 模型卡/配置库 | 🧮 |
| `unit` | 数值结果单位 | 指标/模型配置 | 🧮 |
| `currency` | 金额结果币种 | 指标/模型配置 | 🧮 |
| `rank_no` | 对象在单次运行中的名次 | Python 模型输出 | 🧮 |
| `contribution_value` | 维度或特征贡献值 | Python 模型输出 | 🧮 |
| `forecast_date` | 预测结果日期 | 预测模型输出 | 🧮 |
| `priority_level` | 问题或机会优先级编码 | 模型卡/配置库 | 🧮 |
| `confidence` | 模型结果置信度 | Python 模型输出 | 🧮 |
| `uncertainty_type` | 不确定性度量类型 | Python 模型输出 | 🧮 |
| `uncertainty_value` | 单值不确定性度量 | Python 模型输出 | 🧮 |
| `uncertainty_lower` | 不确定性区间下界 | Python 模型输出 | 🧮 |
| `uncertainty_upper` | 不确定性区间上界 | Python 模型输出 | 🧮 |
| `evidence_ref` | 特征贡献或解释证据引用 | Python 模型输出 | 🧮 |
| `result_fingerprint` | 模型结果防重指纹 | `fingerprint_v1` 生成 | 🧮 |

**当前结论：不应从 ODS 直接灌数。**

---



## 5. 总体可灌性


| 目标 DWD 表                                  | 字段结构         | 当前数据              | 当前可灌结论    |
| ----------------------------------------- | ------------ | ----------------- | --------- |
| `industry_chain`                          | 部分满足         | 888 条专利关系可派生 2 条链 | 🟡 部分     |
| `industry_chain_node`                     | 部分满足         | 可派生 11 个节点        | 🟡 部分     |
| `industry_chain_node_rel`                 | 可由层级源派生      | 层级源 0 行           | ❌         |
| `industry_chain_entity_rel`               | 企业/产品/专利结构匹配 | 仅专利关系 888 行       | 🟡 仅专利    |
| `industry_chain_market_observation`       | 部分匹配         | 候选源 0 行           | ❌         |
| `industry_chain_investment_event`         | 基本匹配         | 事件源 0 行           | ❌         |
| `industry_chain_investment_participant`   | 部分匹配         | 参与方源 0 行          | ❌         |
| `industry_chain_news_event`               | 高度匹配         | 资讯源 0 行           | ❌         |
| `industry_chain_milestone_event`          | 需规则/NLP      | 无直接链级记录           | ❌         |
| `industry_chain_event_entity_rel`         | 部分匹配         | 事件源 0 行           | ❌         |
| `industry_chain_event_metric_observation` | 不满足          | 无互动指标             | ❌         |
| `industry_chain_extraction_result`        | ODS 仅提供输入文档  | 无抽取结果             | 🧮 Python |
| `industry_chain_model_run`                | 不属于 ODS      | —                 | 🧮 系统     |
| `industry_chain_model_result_detail`      | 不属于 ODS      | —                 | 🧮 Python |




### 5.1 最终判断

> **当前** `gkx` **入站库不能满足 v5 的完整 DWD 灌数。**

可以立即形成的只有：

1. 2 条产业链基础记录；
2. 11 个产业链节点基础记录；
3. 888 条链/节点—专利候选关系。

其余业务表虽然多数存在可匹配字段结构，但主要源表为 0 行；事件互动指标完全无源；抽取和模型表必须由本项目 Python/算法平台生成。

### 5.2 核心缺口


| 优先级 | 缺口                                                | 影响             |
| --- | ------------------------------------------------- | -------------- |
| P0  | `dwd_industry_chain_info`、`dwd_industry_code` 0 行 | 链、节点层级和节点关系    |
| P0  | `dwd_org_industry_tags` 0 行                       | 链—企业/机构关系和跨域聚合 |
| P0  | `dwd_industry_chain_news_info` 0 行                | 资讯、热点和里程碑      |
| P0  | 投融资/并购源全部 0 行                                     | 投融资事件和参与方      |
| P0  | 无浏览/评论/转发/点赞字段                                    | 事件指标观测         |
| P1  | `dwd_org_industry_product_tags` 0 行               | 链—产品关系         |
| P1  | 人才、技术、政策无直接链关系表                                   | 七要素图谱          |
| P1  | 市场指标源无稳定 `chain_id` 映射且 0 行                       | 市场观测           |
| P1  | 专利 UID、人才 UID、技术 UID、产品 UID 未冻结                   | 生产跨域关系         |


---



## 6. 后续动作

1. 将本次实时结果同步 Q053～Q055，特别注明当前主链、资讯、企业标签表均为 0 行；
2. 向供应方确认 `dwd_industry_chain_info`、`dwd_industry_code`、`dwd_org_industry_tags`、`dwd_industry_chain_news_info` 和投融资表的数据交付时间；
3. 先用 `dwd_org_industry_chain_pat_dtl` 输出“2 链 + 11 节点 + 888 专利关系”的受限试灌方案，并显式标注不代表全域覆盖；
4. Q053 和跨域 UID 未冻结前，只做字段映射与 Mock/试灌，不形成生产业务键承诺；
5. 数据到位后重新执行字段非空率、唯一性、编码值域和行数核验，再生成正式 Mapping 与 DDL。

---

*实时只读分析 ·* `[human:李伟]` *监管 ·* `agent:architect-agent` *执行 · 2026-08-03 ·* `CHAIN-INST-DATA-ANALYSIS-L01` *Step 2*