# POL-L2-DS10-SENT-DATA · 科创政策全景 · 政策舆情评估 · 数据落点

- 任务：`POL-L2-DS10-SENT-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-03`
- 上游架构：`POL-L2-DS10-SENT-ARCH`（2026-11-03 human:淮政玮签收，第 8 节）。本单只写数据落点，不改那份架构，不改图。

本叶只定科创政策全景二级「政策舆情评估」的数据落点。SRS 序号 **207–212**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-SENT-ARCH.md` 第 8 节、`sdd/l2/POL-L2-DS10-QRY-DATA.md`、`sdd/科技政策跟踪-系统详细设计说明书.md` 第 11.1 节舆情两行、`storage/POLICY/stores/mysql/ads.md` 里已登记的 `policy_effect`、`policy_metric_timeseries`、`policy_match`。指标沿用已有 `metric_id`。不新造 `metric_id`，不改 D4。

## 1. 范围

六叶都在全景里完成。浏览器只打 `/display/v1/policy/**`。查询只读表。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 207 | 政策查询与对比 | 正式行沿用检索叶。无正式行时读 `gkxlumenx_gapfill` | 正式：检索叶已定的统计表与 `policy_base_info`。无正式行：`gapfill_policy_qry_doc`、`gapfill_policy_qry_stat` | 不另建缺项表，不第二套灌数 |
| 208 | 区域政策差异性分析 | 不建表 | 无 | 只消费第 7 项已有子图。空允许 |
| 209 | 政策实施效果跟踪 | 已有政策 ADS，`ads.md` 登记名 `demo_gkxlumenx_ads` | `policy_effect`、`policy_metric_timeseries` | 不加列，不改公式 |
| 210 | 政策受众反馈收集 | `gkxlumenx_gapfill` | `gapfill_policy_audience_feedback` | 本单定列。建表与灌数在灌数单 |
| 211 | 政策效果评估报告 | `gkxlumenx_gapfill` | `gapfill_policy_assessment_report` | 本单定列。建表与灌数在灌数单 |
| 212 | 政策匹配与推送 | 与 209 同一已有 ADS | `policy_match` | 不加列，不改打分 |

207 的 D4 仍是 `mock`。209、212 的 D4 仍是 `mock`。210、211 没有已挂指标，行是灌入的 mock，D4 不因缺项表而改绿。`GDF-POLICY-MOCK-GATE-L01` 仍未解开。本叶不把 mock 写成已上线。

209、212 的物理库沿用 `ads.md` 已登记、且 `polan.eval.effect.run`、`polan.text.match.run` 已经在写的那个 ADS。本叶不把这三张表再放到 `gkxlumenx_ads` 或 `gkxlumenx_gapfill`，也不把行写入 `gkxlumenx_ods`、`gkxlumenx_dwd`、供应方库。查询读 `run()` 写入的同一张表。

## 2. 207 政策查询与对比

不另建缺项表。与检索叶同一条资源：`panorama/stats`、`panorama/search`、`panorama/{id}/detail`。链路与检索叶相同：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python `/internal/policy`。

| 读什么 | 正式表有行 | 正式表没有行 |
|---|---|---|
| `stats`：`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST` | 检索叶已定的 `gkxlumenx_ads` 统计结果 | `gkxlumenx_gapfill.gapfill_policy_qry_stat` |
| `search`：类型、地域、时期，落在目录查询上 | `gkxlumenx_dwd.policy_base_info` | `gkxlumenx_gapfill.gapfill_policy_qry_doc` |
| `{id}/detail`：按条读正文 | 同一条正式目录 | 同一张 `gapfill_policy_qry_doc` |

这两张缺项表的列和灌数属于检索叶，灌数单是 `POL-L2-DS10-QRY-GAPFILL-L01`。本叶不改那些列，不执行那张灌数单，不再建第三张目录表或统计表。不读 `gapfill_policy_qry_rank`。

正式表和这两张缺项表都没有行时，统计卡、列表或正文空，不造 0。D4 保持 mock。

## 3. 208 区域政策差异性分析

不建表。不写 nGQL。不重开 GDF。不把 `policy_graph_node`、`policy_graph_edge` 写成这叶的落点。

读已有指标 `M_POLICY_GRAPH_107_1`（GRAPH，D4 仍是 mock）。展示只消费第 7 项已有政策子图。子图没有结果时，该块空。空是允许结果。

地区件数若只画统计，仍走检索叶已有的全国分布、深圳分布，经第 2 节同一条 `stats`。那不把 208 改成新的统计表。支持力度、实施条件不在本行落列。

## 4. 209 政策实施效果跟踪

不另建表，不加列，不改 `polan.eval.effect.run` 的公式。灌数单 `POL-L2-DS10-SENT-MOCK-ADS` 只跑这份已有 `run()`。本单不执行。

粒度：`policy_effect` 一行是一个区域，`scope_type` 固定 `region_effect`，`scope_code` 用 `run()` 已有的省级代码。`policy_metric_timeseries` 一行是该区域在一次计算日上的落地实效，只读 `metric_id = M_POLICY_IMPLEMENTATION_EFFECT` 的行。

社会维、环境维是受控代理。执行维按政策侧算出后，与这两维写在同一行已有的 `ext` 里。本叶不新增 `is_mock` 列。行上已有约定：

| 已有位置 | 本叶怎么读 |
|---|---|
| `policy_effect.scope_type` | 只取 `region_effect` |
| `policy_effect.scope_code`、`scope_name` | 区域代码和名称 |
| `policy_effect.impl_effect` | 该区域落地实效 |
| `policy_effect.ext` | JSON。`is_mock` 为真，`pending` 为 `QPOL-02`。`dims.execution` 是执行维，`dims.socio_economic` 是社会维，`dims.environment` 是环境维。`data_gap` 保留待采购说明 |
| `policy_effect.effect_score`、`metric_id` | 同一次 `run()` 会写入，行上 `metric_id` 为已有 `M_POLICY_EFFECT_SCORE`。本叶不改挂这条 |
| `policy_effect.shortboard_cnt`、`layout_rec_cnt` | 表上已有。本叶不填，也不把它们当成社会影响或评估报告 |
| `policy_metric_timeseries.metric_id` | 只读 `M_POLICY_IMPLEMENTATION_EFFECT` |
| `policy_metric_timeseries.region_code`、`stat_date`、`metric_value` | 区域、计算日、落地实效值 |
| `policy_metric_timeseries.dim_key` | `run()` 现写 `落地实效性` |
| `policy_metric_timeseries.ext` | 同一行带 `is_mock` 与 `pending = QPOL-02` |
| `industry_code`、`yoy` | 保持 `run()` 现有写法，本叶不补 |

无行则 Job 查询结果空，不造 0，不在接口里写区域列表或分数。D4 保持 mock。这张区域表不是序号 211 的评估报告。

> **2026-11-07 变更（POL-L2-DS10-SRCMON-SYNTH-L01）**：LLM 合成政策写完后，原样调用一次已有 `polan.eval.effect.run()`，让合成政策计入各省落地实效；「删除所有 Mock 数据」后也重算一次。公式、列、表都不改。历史版 `expire_date` 设为新版发布日前一天，`run()` 按已有的 `policy_open` 判它无效，不抬高有效率。

## 5. 210 政策受众反馈收集

库 `gkxlumenx_gapfill`，表 `gapfill_policy_audience_feedback`。一行是一条受众意见：一个反馈主体、一个渠道、一段意见正文、可选评分、可选关联政策、一个反馈时间。一行不是一份问卷，不是一次征集活动，不是一个文件。

渠道只允许三个值：`问卷`、`在线评价`、`意见征集`。渠道取「问卷」只表示这条 mock 意见的来源类别。不灌假问卷当真实采集，不建问卷表、题目表、答卷表。

`gkxlumen-display` 不直连库。`GET /display/v1/policy/panorama/feedback` 由 `gkxlumen-element` 只读这张表。不写入 ODS、DWD、ADS、供应方库。

下列是必要列。建表语句由灌数单 `POL-L2-DS10-SENT-MOCK-210` 落地。本单不执行该单，也不在这里给出可执行脚本。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `subject_name` | varchar(256) | 否 | 反馈主体。名称写在行上，不挂企业登记主数据 |
| `channel` | varchar(32) | 否 | `问卷`、`在线评价`、`意见征集` 三者之一 |
| `opinion_text` | text | 否 | 意见正文 |
| `score` | decimal(10,2) | 是 | 可选评分。没有评分就空，不用 0 占位 |
| `policy_id` | text | 是 | 关联政策。没有关联就空。不建外键 |
| `feedback_at` | datetime | 否 | 这条意见上的时间 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。本叶没有已挂指标，不新注册 |
| `gap_item` | varchar(128) | 否 | 固定 `210 政策受众反馈收集` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间，与 `feedback_at` 分开 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。政策只在方法为 `llm` 时要求模型名。

表空则反馈列表空。查询不插入行。

> **2026-11-07 变更（POL-L2-DS10-SRCMON-SYNTH-L01，用户当次对话选定）**：LLM 合成政策时，新版和 `-H1` 历史版每条顺带写 2～3 条受众反馈入本表。`policy_id` 填合成政策 id，渠道仍限三选一，评分 1～5 可空；`feedback_at` 由代码落在该政策实施期内（新版：发布日到昨天；旧版：发布日到 `expire_date`）。这些行 `fill_method=llm-synth`，`gapfill_batch_id` 为合成批次号，`is_mock=1`。本表没有 `fill_model` 列，模型名不入行，由批次号追溯到合成作业。「删除所有 Mock 数据」按合成 `policy_id` 加 `fill_method=llm-synth` 删除。原有 6 条 `manual` 行不动。

## 6. 211 政策效果评估报告

库 `gkxlumenx_gapfill`，表 `gapfill_policy_assessment_report`。一行是一份效果评估报告：范围、达成度、社会影响、问题、建议、报告正文都在这一行。达成度是报告里的一段表述，不是新指标，不写入 ADS。

不灌序号 217 的对标报告，不灌核增研报文件。不新建对象存储桶，不写桶名和对象键。下载内容从读到的这一行生成，文件字节不进 MySQL，也不进对象存储。

`GET /display/v1/policy/panorama/assessment-report` 由 `gkxlumen-element` 只读这张表。不写入 ODS、DWD、ADS、供应方库。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `scope_text` | text | 否 | 评估范围。不是 209 的 `scope_code` |
| `achievement_text` | text | 否 | 达成度表述 |
| `social_impact` | text | 否 | 社会影响 |
| `problem_text` | text | 否 | 问题 |
| `suggestion_text` | text | 否 | 建议 |
| `report_body` | text | 否 | 报告正文 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。不新注册 |
| `gap_item` | varchar(128) | 否 | 固定 `211 政策效果评估报告` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

同样不设 `fill_model`。表空则报告空。查询不插入行。这张表不读 `policy_effect`。

## 7. 212 政策匹配与推送

不另建表，不加列，不改 `polan.text.match.run` 的打分。与 209 同一张灌数单 `POL-L2-DS10-SENT-MOCK-ADS`，只跑这份已有 `run()`。本单不执行。

粒度：一行是一个受控主体对一条政策的一条匹配。同一 `subject_id` 内 `rank_no` 从 1 起，至多 8，与 `run()` 现有 Top 8 一致。主体画像由 `run()` 在内存中生成，列是已有的 `subject_type`、`subject_id`、`subject_name`。不另建主体表，不把画像写成企业登记主数据。

| 已有列 | 本叶怎么读 |
|---|---|
| `subject_type`、`subject_id`、`subject_name` | 受控主体 |
| `policy_id`、`policy_title` | 命中的政策 |
| `match_score` | 匹配分。只来自表上的查询结果 |
| `match_reasons` | 匹配理由 |
| `rank_no` | 该主体内名次 |
| `metric_id` | 已有 `M_POLICY_MATCH` |
| `model_version`、`calc_batch_id` | 保持 `run()` 现有写法 |

`M_POLICY_INDUSTRY_FIT` 读同一张 `policy_match`、同一批行。不另写一套分，不把行上的 `metric_id` 改成第二条指标。

不灌假通知，不灌假邮件。不建通知表、邮件表、外发台账。没有发信通道时，查询只返回匹配列表。通知和邮件不走序号 202 的分享，也不走序号 204 的订阅。

该主体无行则列表空，不返回演示分。D4 保持 mock。

## 8. 灌数单

三张灌数单都依赖本单。本单只点名，不执行，不建库，不插入行。

| 灌数单 | 做什么 | 本单 |
|---|---|---|
| `POL-L2-DS10-SENT-MOCK-ADS` | 只跑已有 `polan.eval.effect.run` 与 `polan.text.match.run`，写入第 4 节、第 7 节的已有表 | 不执行。不改公式，不另建 ADS 表 |
| `POL-L2-DS10-SENT-MOCK-210` | 按第 5 节建 `gapfill_policy_audience_feedback` 并灌 mock 行 | 不执行 |
| `POL-L2-DS10-SENT-MOCK-211` | 按第 6 节建 `gapfill_policy_assessment_report` 并灌 mock 行 | 不执行 |
| `POL-L2-DS10-QRY-GAPFILL-L01` | 检索叶的目录与统计缺项 | 207 只消费。本叶不执行，不第二套灌数 |

查询请求不调用以上任何一单。空表返回空。

## 9. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| 197–202 | 207 复用其 `stats` / `search` / `detail` 与两张已定缺项表。不读 `gapfill_policy_qry_rank`，不建历史、收藏、导出 |
| 203、204 | 入库与订阅。不是 210 的反馈，也不是 212 的推送 |
| 205、206 | 时序、热力、热点与深度报告。不是 209 |
| 213–218 | 新旧对比、详情力度、部门件数、标杆力度、对标报告与对标可视化。211 不读对标报告 |
| 216 | `M_POLICY_SUPPORT_STRENGTH` 不进 208 |
| 614–618 | 核增研报。211 不灌研报文件 |
| `M_POLICY_EFFECT_SCORE` | `run()` 会写在 `policy_effect.metric_id`。本叶不改挂 |
| `M_POLICY_DEEP_168_1` | 不挂到 209 或 211 |

## 10. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑 `run()`。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不加已有 ADS 列。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。
- 不把 210、211 的行写入 ODS、DWD、ADS、供应方库。
- 不灌假问卷、假通知、假邮件、对标报告、研报文件。不新建对象存储桶。
- 不把接口直接返回的 mock、算法库页面上的柱和演示分写成存储。
- 不改架构稿、说明书、WBS、检索叶、动向叶、`ads.md`、注册表。
- 不把本单标成 done。会签态记 `draft`。
