# 科技数据资源 · API 接口需求清单

> 版本：V1.1 · 2026-11-12  
> 用途：明确科技信息展示系统「科技数据资源」模块所依赖的 **R-01 ~ R-24 共 24 条接口** 的业务背景、输入参数与输出字段要求

---

## 0. 项目背景与整体说明

### 0.1 业务背景

科技信息展示系统是国际科技信息中心的核心展示平台，面向管理者与决策层提供科技数据的接入、管理与应用全貌。其中「科技数据资源」模块包含 **四个视窗**：

| 视窗 | 需规序号 | 说明 |
|---|---|---|
| 总体视窗（DS-17） | seq 330–346 | 资源接入总览、来源分析、关联图谱、接口健康监控、应用主体与调用趋势 |
| 接入视窗（DS-18） | seq 347–367 | 接入完成度、渠道分析、分区详情、历史归集、问题资源台账 |
| 主题视窗（DS-19） | seq 368–375 | 主题库分类浏览、元数据详情、表结构查询、关联关系、智能检索 |
| 应用视窗（DS-20） | seq 376–399 | 数据应用排行、使用详情、主题/供应方/需求方/业务应用调用统计与导出 |

### 0.2 调用架构

```text
用户浏览器
  → 科技信息展示系统前端（不直连任何外部数据提供方）
    → 展示后端聚合服务（BFF）
      → 本清单所列 R-01 ~ R-24 接口
```

- 前端不直连外部数据提供方，所有数据经展示后端聚合服务组装后，以四个固定 GET 路径对外提供（见 §0.4）。
- 本清单所列 24 条接口为 **BFF 背后要消费的上游能力**，无需按我方四个 GET 路径暴露。
- 可以选择：按 R-01 ~ R-24 暴露 HTTP OpenAPI，或提供等价的库表由我方拉取；验收以 **字段覆盖** 为准。

### 0.3 共性约定（所有接口须遵守）

| 类别 | 要求 |
|---|---|
| 鉴权 | 约定鉴权方式（Token / API Key / mTLS 等），并提供调用审计能力 |
| 限流 | 须约定单 IP / 单 Key 的 QPS 上限与超限行为（返回码 + 重试建议） |
| 时区 | 所有时间字段统一 UTC 或 +08:00，清单中 `updated_at` 为标准更新时间戳 |
| 主键 | 资源 ID（`resource_id`）、主题库 ID（`theme_id`）须跨接口稳定可关联，**禁止**与论文/专利/项目实体 ID 混用 |
| 分页 | 列表类接口建议支持 `page` + `size` 参数与 `total` 返回，便于批量拉取 |
| 时间窗 | 列表类接口建议支持时间范围筛选（`start_time` / `end_time`），便于增量拉取 |
| 空态 | 无数据时返回空集合 / 零值，**禁止**用 404 表示无数据；响应体结构须与有数据时一致 |
| 错误码 | 须提供错误码字典与含义，我方按码做降级或提示 |
| 性能 | 单接口 P99 响应 ≤ 3s；核心统计接口 P99 ≤ 5s |
| 交付物 | OpenAPI / Swagger 文档、字段字典、≥20 条样例数据、刷新频率说明、错误码说明 |
| **调用频率口径（业务展示类接口）** | **1 次 = 1 个唯一调用方（caller_identity）× 1 个 API × 1 次成功请求**。五条规则：① 批量参数按 1 次计（传 50 个 resource_ids 仍计 1）；② 失败重试不计入（只有 `result=success` 的请求计入）；③ **业务调用账写入封顶 1000 次 / 调用方 / API / 自然日**（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）；④ BFF 缓存命中不计入上游；⑤ R-07 探针、R-19 实时监控基线等**机器轮询接口不计入业务调用账**。R-07 自身的运维监控字段（call_freq / fail_rate / success_rate / avg_response_ms）继续用每次 HTTP 请求 = 1 次的**原始口径** |

### 0.4 我方已冻结的消费路径（供参考，非接口提供方义务路径）

以下四个 GET 是展示后端对外暴露的固定接口，**接口提供方不必实现**：

| GET 路径 | 消费的上游接口 | 页面 |
|---|---|---|
| `/display/v1/data-ops/overview/dataset` | R-01 ~ R-08 | 总体视窗 |
| `/display/v1/data-ops/access/dataset` | R-09 ~ R-13 | 接入视窗 |
| `/display/v1/data-ops/theme/dataset` | R-14 ~ R-18 | 主题视窗 |
| `/display/v1/data-ops/application/dataset` | R-19 ~ R-24 | 应用视窗 |

### 0.5 三套分类枚举（须对齐或书面声明映射）

| 枚举套 | 取值 | 用在哪 |
|---|---|---|
| `srs_source`（来源五类） | 国内数据库、国外数据库、科研院所、企业、开源平台 | 来源分布、来源分析 |
| `org_activity`（机构活跃度） | 科研机构、高等院校、企业单位、政府部门、国际组织 | 总体视窗活跃度 |
| `ingest_method`（接入方式） | API接口、文件传输、数据库同步、人工录入、物联网采集 | 完成度、历史接入、问题渠道 |

---

## 1. 总体视窗（DS-17）· R-01 ~ R-08

| 项 | 内容 |
|---|---|
| **需规序号** | 主 330；支撑 333、334 |
| **业务描述** | 返回当前已接入资源的类型分布、总量、年度接入趋势、来源机构活跃度，用于运营驾驶舱一键全局 |
| **输入参数** | |
| 必填 | 无（默认返回全量快照） |
| 选填 | `start_time`（统计起点）、`end_time`（统计终点）、`granularity`（时间粒度：year/month） |
| **输出字段（响应）** | |
| 资源类型分布 | `resource_type`（类型名称）、`type_count`（数量）、`total_volume`（体量）、`share_pct`（占比）、`color`（展示用颜色） |
| 主题分布 | `theme_name`、`theme_count`、`avg_quality`（平均质量分）、`share_pct` |
| 年度接入趋势 | `year`、`annual_added`（当年新增）、`total`（累计总量）、`yoy`（同比，首年可空） |
| 来源机构活跃度 | `org_type`（对应 `org_activity` 枚举）、`org_name`、`activity_score`（活跃度评分）、`status`（活跃/休眠） |
| 其他 | 资源总量汇总数字（**目录口径，禁止把论文/专利/项目实体存量计入**） |
| **验收关注点** | 资源总量口径明确；年度趋势支持跨年；机构活跃度有分级 |

---

### R-02 · 资源来源分析接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 331 |
| **业务描述** | 按来源类型归纳结构与变化，判断数据质量与来源可靠性 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `source_type`（对应 `srs_source` 枚举）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 来源结构 | `srs_source`（来源类型）、`resource_count`（资源条数）、`share_pct`（占比）、`change_pct`（相对上期变化） |
| 质量信息 | `reliability`（可靠性提示）、`avg_quality`（平均质量分）、`reliability_hint`（一句话说明） |
| 结构趋势 | `period`（月/季）、各期 `share_pct` 序列 |
| 分类运行统计 | `classify_type`（自动/人工归类）、`count`、`summary`（摘要） |
| 来源明细列表 | `resource_id`、`name`、`source`（来源方）、`region`（区域）、`data_type`、`collected_at`（采集时间）、`quality_level`（质量等级）、`reliability_level`（可靠性等级）、`discipline`（领域）、`related_project`（关联项目）、`tags`（标签数组） |
| **验收关注点** | 来源类型覆盖全部 `srs_source` 枚举；结构趋势至少 6 期以上；明细可下钻 |

---

### R-03 · 接入资源详情查询接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 332 |
| **业务描述** | 单条 / 批量资源元数据查询，定位和筛选所需数据资源 |
| **输入参数** | |
| 必填 | 单条查询时须带 `resource_id`；批量查询时须带 `resource_ids`（数组） |
| 选填 | `keyword`（关键词）、`page`、`size`、`discipline`（学科领域）、`srs_source`（来源过滤） |
| **输出字段（响应）** | |
| 核心标识 | `resource_id`（稳定主键）、`name`（资源名称）、`resource_type`（类型）、`category`（类别） |
| 来源信息 | `srs_source`（对应 `srs_source` 枚举）、`channel`（接入渠道）、`source_name`（数据来源机构）、`region`（区域） |
| 时间信息 | `collected_at`（采集时间）、`update_freq`（更新频率，如"每日/每周/月/手动"）、`last_update_at`（最近更新时间） |
| 规模信息 | `record_count`（记录量）、`volume`（体量标签，如"10.2TB"）、`status`（状态：在用/归档/异常） |
| 质量与关联 | `quality_score`（质量分 0–100）、`related_project`（关联项目名）、`discipline`（学科领域）、`tags`（关键词数组） |
| **验收关注点** | 支持关键词模糊匹配；`resource_id` 稳定不可变；分页规范 |

---

### R-04 · 主题库与资源中心目录接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 335 |
| **业务描述** | 返回主题库分类结构与大数据资源中心概览 |
| **输入参数** | |
| 必填 | 无（默认返回完整目录树） |
| 选填 | `category`（分类，如"科技要素库"/"领域主题库"）、`discipline_tag`（领域/技术类型标签） |
| **输出字段（响应）** | |
| 分类概览 | `category`（分类名）、`category_desc`（分类说明）、`theme_count`（主题库数量）、`table_count`（表总数）、`record_count`（记录量标签）、`storage`（存储量标签）、`update_status`（更新状态） |
| 主题库骨架 | `theme_id`（主题库 ID）、`theme_name`、`tags`（技术领域标签数组）、`resource_count`（资源条目数） |
| 中心介绍 | `center_name`、`center_desc`（大数据资源中心介绍文案）、`overview_stats`（库数/表数/记录数/存储量汇总） |
| **验收关注点** | 分类树完整；主题库骨架至少包含 ID + 名称 + 标签；支持分类筛选 |

---

### R-05 · 资源详情深度浏览接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 336 |
| **业务描述** | 单资源深度信息与更新动态流，用于详情页 / 抽屉 |
| **输入参数** | |
| 必填 | `resource_id`（须唯一定位） |
| 选填 | 无 |
| **输出字段（响应）** | |
| 完整属性 | `resource_id`、`name`、`resource_type`、`category`、`discipline`、`tech_type`（技术类型）、`update_freq`、`structure_summary`（结构摘要，如"23 张表，含企业注册信息、专利引用关系"） |
| 规模与质量 | `record_count`、`volume_label`、`quality_score`、`growth_7d`（近 7 日增长）、`activity_level`（活跃度） |
| 关联信息 | `related_resources[]`（关联资源 ID + 名称）、`related_projects[]`、`tags[]`、`keywords[]` |
| 更新动态流 | `feed[]`，每条含 `action_time`（时间）、`action`（动作，如"采集/更新/清洗/归档"）、`increment`（增量记录量）、`status`（成功/失败）、`note`（备注） |
| **验收关注点** | 更新动态流至少 10 条以上历史；字段完整度覆盖详情抽屉所有展示位 |

---

### R-06 · 资源关联关系查询接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 339～342；支撑 337、338 |
| **业务描述** | 返回目录级资源间关联图与语义主题聚合（**非全要素图谱验收**） |
| **输入参数** | |
| 必填 | 无（允许空挂接：无图数据时返回空点边） |
| 选填 | `resource_id`（围绕某资源展开局部图）、`theme_id`（围绕某主题库展开局部图） |
| **输出字段（响应）** | |
| 节点 | `nodes[]`，每条含 `node_id`、`node_name`、`category`（节点类别）、`color`（展示色）、`size`（与规模挂钩）、`desc_text`（描述文案） |
| 边 | `edges[]`，每条含 `src_id`、`dst_id`、`relation`（关系类型，如"引用/衔接/主题交叉"）、`strength`（关系强度，0–1） |
| 节点详情 | `node_details[]`，每条含 `node_id` + 可选的 `record_count` / `quality` / `source` / `user_count` / `call_count` 等详情 |
| 图例分类 | `legend[]`，用于前端绘制图例 |
| 语义主题聚合 | `semantic_clusters[]`，每条含 `cluster_name`（语义簇名）、`member_names[]`（簇内成员）、`score`（融合趋势分） |
| **验收关注点** | 节点详情**不要**多出 `parentDB` 字段；允许空图返回；语义簇可空态 |

---

### R-07 · 应用系统与接口状态监控接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 343、344 |
| **业务描述** | 返回各接口/系统的可用性、响应时延、告警情况与调用健康度 |
| **输入参数** | |
| 必填 | 无（默认返回最近一次探针结果） |
| 选填 | `probe_start_time`、`probe_end_time`（探针时间窗） |
| **输出字段（响应）** | |
| 接口状态条 | `interfaces[]`，每条含 `interface_name`、`availability`（可用性标签：正常/降级/不可用）、`probed_at`（最近探针时间） |
| 健康指标（四数字） | `avg_response_ms`（平均响应时延 ms）、`alert_count`（告警总数）、`critical_alert_count`（严重告警数）、`success_rate`（成功率 %） |
| 调用频率日志 | `call_freq`（调用频率）、`fail_rate`（失败率）、`active`（是否活跃） |
| **验收关注点** | **禁止**在响应中多出 `totalCalls` 字段；四健康指标为纯数字，不带描述；时间戳统一格式；call_freq / fail_rate / success_rate / avg_response_ms 采用**运维原始口径**（每次 HTTP 请求 = 1 次），不受业务展示类每日上限约束 |

---

### R-08 · 应用主体与调用趋势接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 345、346 |
| **业务描述** | 返回调用资源的应用主体清单，以及自上线以来的累计调用与趋势 |
| **输入参数** | |
| 必填 | 无（无调用账时允许返回空集合） |
| 选填 | `period_type`（统计周期：周/月/季）、`subject_type`（主体类型：机构/项目/用户） |
| **输出字段（响应）** | |
| 应用主体清单 | `subject_id`、`subject_name`（名称）、`subject_type`（机构/项目/用户/应用系统）、`resource_type`（用的资源类型）、`usage`（用途）、`call_count`（调用次数）、`value_share`（价值占比）、`is_key_user`（是否重点用户） |
| 累计调用分析 | 总累计调用次数、覆盖资源数、日均调用、高峰时段（一天中的时段）、热度与生命周期提示（如"上升期/稳定期/衰退期"） |
| 调用趋势序列 | `trend[]`，每条含 `period_label`（周/月/季标签）、`cumulative_count`（累计调用）、`current_count`（当期调用）、按资源类型的拆分占比 |
| **验收关注点** | 无调用账时整包返回空数组 / 空对象；趋势序列至少 12 期（月）以上；call_count / cumulative_count 等调用类字段采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |

---

## 2. 接入视窗（DS-18）· R-09 ~ R-13

### R-09 · 接入完成度与归集量统计接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 347、349；支撑 350 |
| **业务描述** | 返回接入任务完成度、归集数据量与多粒度趋势 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `start_time`、`end_time`、`granularity`（year/month/week/day）、`ingest_method`（接入方式，对应 `ingest_method` 枚举） |
| **输出字段（响应）** | |
| 接入任务完成度 | `status_counts`：`done`（已完成计数）、`running`（进行中）、`pending`（待处理）；按 `ingest_method` 拆分的完成态 |
| 归集数据量 KPI | `total_collection_volume`（累计归集量）、`current_period_volume`（本期新增量）、`resource_count`（接入资源数） |
| 归集趋势 | `trend[]`，每条含 `period_label`、`metric`（added/updated/volume）、`ingest_method`（接入方式）、`value` |
| **验收关注点** | 归集量口径 **≠** 论文/专利/项目实体存量；趋势支持多粒度；接入方式覆盖全部 `ingest_method` 枚举 |

---

### R-10 · 来源渠道分析接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 348、351～355 |
| **业务描述** | 按接入渠道返回归集体量、成功率、结构趋势与明细行 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `channel_name`（渠道名）、`biz_type`（业务类型）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 渠道汇总 | `channel_name`、`channel_code`、`total_volume`（归集体量）、`item_count`（条数）、`share_pct`（占比）、`success_rate`（成功率）、`color`（展示用颜色）、`biz_type`（业务类型标签） |
| 渠道结构序列 | `period_label`（月/季）、各期 `volume` / `success_rate` / `share_pct` 序列 |
| 业务类型交叉 | `biz_type` × `channel_name` 的交叉计数 |
| 渠道明细行（可导出） | `resource_id`、`resource_name`、`channel`、`data_type`、`collected_at`、`quality_level`、`quality_score`、`related_project`、`discipline`、`volume_label`、`ingest_method` |
| **验收关注点** | 结构序列至少 6 期；明细行可直接导出；渠道覆盖全场景 |

---

### R-11 · 接入资源分区详情接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 356～359 |
| **业务描述** | 按区域 / 分库 / 来源机构的分区返回资源清单与结构 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `region`（区域）、`db_partition`（分库名）、`source_org`（来源机构）、`theme` / `discipline`（主题/学科过滤） |
| **输出字段（响应）** | |
| 分区汇总 | `partition_type`（区域/分库/来源机构）、`partition_value`、`resource_count`、`data_volume`、`avg_quality`、`structured_type_distribution`（结构化类型分布） |
| 下属机构列表 | `orgs[]`：`org_name`、`resource_count`、`avg_quality`、`representative_resources[]`（代表资源名数组） |
| 分区说明 | `partition_desc`（分区介绍文案） |
| 主题库列表骨架 | 与 R-04 共用的主题库骨架行（`theme_id`、`theme_name`、`table_count` 等） |
| **验收关注点** | 分区支持至少三种维度；机构分区可带代表资源名；主题归类信息完整 |

---

### R-12 · 历史接入与更新周期接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 360～363 |
| **业务描述** | 返回历史归集记录、仪表盘汇总、更新周期统计 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `channel`（渠道）、`table_name`（表名）、`anomaly_type`（异常类型）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 历史归集行 | `channel_name`、`table_name`、`access_date`（接入日期）、`row_count`（数据条数）、`volume_label`（体量）、`update_cycle`（更新周期，如"日更/周更"）、`last_update_at`（上次更新时间）、`status`（成功/失败/部分成功）、`anomaly_type`（异常类型，无异常则为空）、`anomaly_note`（异常说明） |
| 仪表盘汇总 | `archive_count`（归档次数）、`channel_count`（涉及渠道数）、`table_count`（涉及表数）、`anomaly_count`（异常总数）、`success_rate`（成功率） |
| 趋势序列 | 分月的 `access_volume`（接入量）、`success_rate`、`anomaly_count` 序列 |
| 异常分布 | `anomaly_distribution[]`：`anomaly_type`、`count`、`color` |
| 更新周期统计 | `update_cycle_distribution[]`：`update_cycle`（周期）、`count`（表数）、`avg_success_rate`（平均成功率）、`trend`（趋势说明） |
| **验收关注点** | 历史记录至少 12 个月；异常类型有分级；更新周期统计按渠道聚合 |

---

### R-13 · 问题资源清单与统计接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 364～367 |
| **业务描述** | 返回被识别为有质量问题的资源清单与分级统计 |
| **输入参数** | |
| 必填 | 无（无质量源时允许返回空列表 + 空统计） |
| 选填 | `issue_type`（问题类型）、`level`（级别：紧急/重要/普通）、`status`（处理状态）、`channel`（渠道） |
| **输出字段（响应）** | |
| 问题资源行 | `resource_id`、`resource_name`、`table_name`、`resource_type`、`category`、`data_cluster`（数据集群）、`level`（紧急/重要/普通）、`status`（处理状态：待处理/处理中/已解决）、`found_at`（发现时间）、`channel`、`detail`（问题详情描述）、`suggestion`（处理建议） |
| 分级 / 分类统计 | 按类别、集群、类型、级别、渠道的 `count`（计数） |
| 趋势 | 按月的 `total_issues`（问题总量）与 `resolved_count`（已解决量）序列 |
| **验收关注点** | 问题级别枚举待甲方确认；明细行可直接导出 |

---

## 3. 主题视窗（DS-19）· R-14 ~ R-18

### R-14 · 主题库分类与资源分布接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 368、370 |
| **业务描述** | 返回主题库总数、各主题库列表头信息与资源分布，供主题页顶部四张卡与分类浏览 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `category`（分类过滤）、`tag`（标签过滤） |
| **输出字段（响应）** | |
| 顶部四张卡数字 | `themeDatabaseCount`（主题库总数）、`tableCount`（表总数）、`recordCountLabel`（记录量标签，纯数字字符串，如"10.2"）、`storageLabel`（存储量标签，纯数字字符串，如"18.6"） |
| 主题库列表头 | 每条含：`theme_id`（主题库 ID）、`theme_name`、`category`（分类）、`resource_type`、`publish_date`（发布时间）、`record_yi`（记录量，亿条）、`storage_tb`（存储量 TB）、`update_time`、`description`（描述）、`source_name`（来源）、`region`（区域）、`partition`（分区）、`contact_person`（联系人）、`collected_at`、`update_freq`、`data_structure`（数据结构说明）、`related_project`、`tags[]`、`table_count`、`quality_score` |
| 资源分布可视化 | 按主题库的数量 / 结构分布切片 |
| **验收关注点** | 顶部四卡数字为纯字符串，不含单位；涨跌文案由前端本地写，**上游不必出涨跌字段**；主题库列表覆盖全部分类 |

---

### R-15 · 数据集元数据详情接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 371、372 |
| **业务描述** | 返回单个主题库 / 数据集的完整元属性 |
| **输入参数** | |
| 必填 | `theme_id`（主题库 ID）或 `resource_id` / `dataset_id`（数据集稳定 ID），二选一须能唯一定位 |
| 选填 | 无 |
| **输出字段（响应）** | |
| 基础属性 | `dataset_name`（数据集名称）、`parent_theme`（所属主题库）、`resource_type`（类型）、`data_volume`（数据量） |
| 来源与时间 | `source_org`（来源单位）、`collected_at`（采集时间）、`update_time`、`update_freq`（更新频率） |
| 质量与关联 | `quality_score`（质量分）、`related_project`（关联项目）、`responsible_person`（维护责任人，可空） |
| 补充元属性 | 学科 / 领域标签、数据版本号、数据格式说明、权限级别 |
| **验收关注点** | 责任人字段可空但键须存在；主题库 ID 与 R-14 的 `theme_id` 一致 |

---

### R-16 · 数据表结构查询接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 373 |
| **业务描述** | 返回主题库下各表的表结构（字段级） |
| **输入参数** | |
| 必填 | `theme_id`（主题库 ID）或 `dataset_id`（数据集 ID） |
| 选填 | `table_name`（只查一张表时指定） |
| **输出字段（响应）** | |
| 表列表 | `tables[]`，每条含 `table_name`（表名）、`table_comment`（表注释 / 业务含义） |
| 表下字段 | 每表下 `fields[]`，每条含 `field_name`（字段名）、`field_type`（字段类型，如 varchar/bigint/datetime）、`business_meaning`（业务含义 / 字段描述）、`required_flag`（是否必填，布尔值） |
| **验收关注点** | 字段描述须是**业务含义**而非纯技术注释；`field_type` 与 R-20 `column_type` 一致 |

---

### R-17 · 数据集关联关系接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 374 |
| **业务描述** | 返回数据集间目录级关联关系（引用 / 衔接 / 主题交叉），不升格为全要素图谱 |
| **输入参数** | |
| 必填 | 无（允许空图） |
| 选填 | `theme_id`（局部关系） |
| **输出字段（响应）** | |
| 节点 | `nodes[]`，每条含 `dataset_id` / `theme_id`、`name`、`category`（类别）、`description`（描述）、`record_count`（规模） |
| 边 | `edges[]`，每条含 `src_id`、`dst_id`、`relation`（关系类型，如"引用/衔接/主题交叉"）、`strength`（关系强度 0–1） |
| **验收关注点** | 允许空图返回；不要求图谱实体检索 |

---

### R-18 · 主题库检索接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 369、375 |
| **业务描述** | 主题库 / 数据集的关键词 + 多维筛选检索 |
| **输入参数** | |
| 必填 | 无（整包目录到位后由前端筛选，可不调用） |
| 选填 | `keyword`（关键词）、`category`（类别）、`start_time`、`end_time`、`theme`、`page`、`size` |
| **输出字段（响应）** | |
| 检索结果 | `items[]`，每条含 `theme_id` / `dataset_id`、`name`、`category`、`summary`（摘要）、`update_time` |
| 分页信息 | `total`（总命中数）、`page`、`size` |
| **验收关注点** | **非 NL2SQL、非图谱实体检索**；如只有检索能力、没有全量目录，须书面通知我方调整消费策略 |

---

## 4. 应用视窗（DS-20）· R-19 ~ R-24

> **整窗依赖「资源调用账」**。无调用账时允许各接口返回空集合。

### R-19 · 数据应用排行与资产总览接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 376～379 |
| **业务描述** | 返回数据资产 / 应用排行、基本情况汇总与调用趋势基线 |
| **输入参数** | |
| 必填 | 无（无调用账允许空） |
| 选填 | `start_time`、`end_time`、`sort_dimension`（排序维度：调用量/主体/领域） |
| **输出字段（响应）** | |
| 应用侧 KPI | 如 `total_call_count`（总调用）、`app_system_count`（应用系统数）、`asset_count`（资产数） |
| 资产 / 应用排行 | 每条含：`asset_id`、`asset_name`（名称）、`category`（类别）、`department`（所属部门）、`data_type`（数据类型）、`app_subject`（应用主体）、`deploy_location`（部署位置）、`usage_cycle`（使用周期）、`biz_type`（业务类型）、`usage_unit`（使用单位）、`last_active_date`（最近活跃日）、`call_count`（调用次数）、`user_count`（用户数）、`growth`（增长率 %）、`biz_module`（业务模块） |
| 调用趋势基线 | `usage_call_trend[]`：每条含 `date`、`call_count`（调用次数）、`active_user_count`（活跃用户数），作为页面"实时监控"跳动基线 |
| **验收关注点** | 无调用账时整包空数组；排行至少 Top 20；趋势至少 30 天；call_count 等调用类字段采用**业务展示口径**；usage_call_trend 为"实时监控跳动基线"，其底层数据来自机器轮询，**不计入业务调用账**，仅用作前端视觉抖动的序列源 |

---

### R-20 · 数据资源使用详情接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 380～383 |
| **业务描述** | 返回字段级使用详情（列名、来源部门、使用频率）与可视化趋势 |
| **输入参数** | |
| 必填 | 无（无使用账允许空） |
| 选填 | `table_name`（表名）、`source_dept`（来源部门）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 字段使用明细 | `columns[]`，每条含：`table_name`、`column_name`（列名）、`column_type`（列类型）、`column_desc`（列描述 / 业务含义）、`source_dept`（来源部门）、`app_name`（应用名）、`last_usage_time`（最近使用时间）、`usage_count`（使用次数）、`subscription_count`（订阅数） |
| 使用详情趋势 | `usage_detail_trend[]`：按月（或等价粒度）的 `total_usage_count` 序列 |
| **验收关注点** | 表名/列名可有，但**使用频率**依赖调用账；`column_type` 与 R-16 一致；usage_count / subscription_count 采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |

---

### R-21 · 主题调用统计与趋势接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 384～387 |
| **业务描述** | 返回各主题被调用的基本信息、多线趋势与用户 / 应用系统追踪 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `theme_name`、`granularity`（日/周/月）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 主题调用基本信息 | 每条含：`theme_name`、`call_time`、`call_frequency`（调用频率）、`api_name`（调用接口）、`app_system`（业务系统） |
| 主题调用趋势 | `theme_call_trend[]`：多线序列（每条线对应一个主题库），横轴 `period_label`（日/周/月），纵轴 `call_count` |
| 调用用户与应用系统追踪 | `call_tracking[]`，每条含：`user_name`（用户）、`dept`（部门）、`app_system`、`theme_name`、`last_call_time`（最近调用时间）、`client_ip`、`call_count` |
| **验收关注点** | 趋势至少 12 期（月）；追踪数据可下钻到用户级；call_frequency / call_count / tracking.call_count 等调用类字段采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |

---

### R-22 · 供应方调用统计接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 388～391 |
| **业务描述** | 返回供应方归集、区域分组、调用明细与多线趋势 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `region`（区域）、`period_type`（统计周期）、`supplier_name`（供应方名称） |
| **输出字段（响应）** | |
| 供应方归集 | `supplier_dept`（名称）、`department`、`region`（区域）、`resource_count`（资源数）、`cumulative_call_count`（**累计调用次数**）、`share_pct`（占比） |
| 区域分组 | `supplier_region_groups[]`：每条含 `region`、`supplier_count`（供应方数）、`resource_count`、`cumulative_call_count`（累计调用）、该区域下的 `supplier_list` |
| 调用明细（须含累计调用） | `supplier_call_details[]`：每条含 `supplier_dept` × `data_product` × `biz_type` × `period` 的 `cumulative_call_count` |
| 周期枚举 | `period_enum[]`（如"日/周/月/季"） |
| 供应方调用趋势 | `supplier_call_trend[]`：多线，每条线对应一个供应方，横轴 `period_label`，纵轴 `call_count` |
| **验收关注点** | **累计调用字段必须有**；与 R-07 禁止出站的 `totalCalls` 不是同一处；明细行可直接导出；cumulative_call_count / supplier_call_trend 等调用类字段采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |

---

### R-23 · 需求方调用统计接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 392～395 |
| **业务描述** | 返回需求方归集、累计调用与行为分布 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `department`、`biz_type`（业务类型）、`project_group`（项目组） |
| **输出字段（响应）** | |
| 需求方归集 | `demander_name`（名称）、`department`、`biz_type`、`project_group`、`cumulative_call_count`（累计调用）、`active_days`（活跃天数）、`avg_daily_call`（日均调用） |
| 调用趋势 / 行为分布 | `demander_call_trend[]`：多线或行为分布序列 |
| **验收关注点** | 无调用账时空集合；支持部门 / 业务类型 / 项目组多维筛选；cumulative_call_count / avg_daily_call / demander_call_trend 等调用类字段采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |

---

### R-24 · 业务应用调用明细与导出接口

| 项 | 内容 |
|---|---|
| **需规序号** | 主 396～399 |
| **业务描述** | 返回业务应用归集、部门分组、调用明细日志与多线趋势 |
| **输入参数** | |
| 必填 | 无 |
| 选填 | `app_name`（应用名称）、`source_dept`（来源部门）、`start_time`、`end_time` |
| **输出字段（响应）** | |
| 业务应用归集 | `app_name`（名称）、`source_dept`（来源部门）、`biz_type`（业务类型）、`status`（状态）、`app_count`（应用数）、`call_count`（累计调用量） |
| 部门分组 | `business_application_dept_groups[]`：每条含 `source_dept`、`app_list`（部门下应用列表 + 累计调用） |
| 调用明细日志（可导出） | `business_application_call_logs[]`，每条含：`app_name`、`department`、`biz_type`、`user_name`、`resource_name`（调用的资源）、`call_time`（调用时间）、`result`（成功/失败）、`latency_ms`（耗时 ms）、`call_count`（次数） |
| 业务应用调用趋势 | `business_call_trend[]`：多线，横轴 `period_label`，纵轴 `call_count` |
| **验收关注点** | **不要求单独"导出文件流"接口**；日志列齐即可导出；导出频控由我方前端 / 网关控制；call_count / business_call_logs.call_count / business_call_trend 等调用类字段采用**业务展示口径**（1 次 = 1 个唯一调用方 × 1 个 API × 1 次成功请求，业务调用账写入封顶 1000（仅影响前端展示数字，不影响接口真实可用性，也不是网关限流）） |
