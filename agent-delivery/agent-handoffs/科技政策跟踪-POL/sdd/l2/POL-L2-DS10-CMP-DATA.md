# POL-L2-DS10-CMP-DATA · 科创政策全景 · 政策重点比对 · 数据落点

- 任务：`POL-L2-DS10-CMP-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（已认领，状态 `in_progress`，本单不改状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-04`
- 会签态：未会签。本叶不代签，不标 done
- 上游架构：`POL-L2-DS10-CMP-ARCH`（2026-11-03 human:淮政玮签收，第 5 节和第 9 节）。本单只写数据落点，不改那份架构，不改图。

本叶只定科创政策全景二级「政策重点比对」的数据落点。SRS 序号 **213–218**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-CMP-ARCH.md` 第 5 节和第 9 节、说明书第 11.2 节「重点比对 213–218」那一行、`sdd/l2/POL-L2-DS10-QRY-DATA.md`（分册结构）、`storage/POLICY/stores/mysql/ads.md` 已登记的 `policy_intensity` 与 `policy_metric_timeseries`、`dwd.md` 已登记的 `policy_base_info.publish_date`。指标沿用已有 `metric_id`。不新造 `metric_id`，不改 D4。

说明书第 11.2 节仍把这一二级放在未开工。本叶不改说明书。表名、要灌的内容和灌数单与该行一致。列和拣行键按已签收架构第 9 节写在这里。

## 1. 范围

六叶都在全景比对工作区里完成。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python。查询只读表。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

新建表只有库 `gkxlumenx_gapfill` 下这四张：

| 表 | 序号 | 灌数方 | 读取方 |
|---|---|---|---|
| `gapfill_policy_version_diff` | 213 | `POL-L2-DS10-CMP-GAPFILL-L01` | `gkxlumen-element` |
| `gapfill_policy_version_analysis` | 213-3 演变趋势说明 | `POL-L2-DS10-CMP-213-ANALYSIS-FDE`（seed / LLM enrich） | `gkxlumen-element`（`version-diff` 透传） |
| `gapfill_policy_detail_compare` | 214 的申报条件、申报材料、优点、缺点 | 同上 | `gkxlumen-element` |
| `gapfill_policy_impl_dept` | 215 的实施部门 | 同上 | `gkxlumen-element` |
| `gapfill_policy_benchmark_report` | 217 | 同上 | `gkxlumen-element` |

不建 `gapfill_policy_benchmark_viz`。不写 ODS、DWD、ADS 新表，不加已有 ADS 列，不写供应方库。

`ads.policy_intensity` 已有。支持力度由 `gkxlumen-element` 同步读。力度分由已有 `run()` 写入，请求不现算。216 不进灌数单。218 读这张已有力度表，不另建可视化缺项表。

这四张缺项表只服务功能验收。生产配置不读 `gkxlumenx_gapfill`。行上带 D16 规定列。缺项表有行也不把 D4 改成 live。`GDF-POLICY-MOCK-GATE-L01` 仍未解开。

| 序号 | 叶子 | 库表 | 本单 |
|---|---|---|---|
| 213 | 政策新旧对比 | `gkxlumenx_gapfill.gapfill_policy_version_diff` | 本单定逻辑列。时点来自已有发布时间 |
| 214 | 政策详情对比 | 正文走已有门面。力度读已有 `policy_intensity`。条件、材料、优缺点读 `gapfill_policy_detail_compare` | 缺项表放条件、材料、`pros_text`、`cons_text` |
| 215 | 部门政策对比 | 区域、类别、总件数走已有目录。实施部门读 `gapfill_policy_impl_dept` | 不新造部门指标 |
| 216 | 标杆比对功能 | 已有 `policy_intensity` 所在 ADS。支持力度同步读；「政策类型」列 2026-11-11 起同一次统计读 DWD 文种按省聚合（QPOL-01 临时默认） | 不加列，不进灌数单 |
| 217 | 对标报告生成与导出 | `gkxlumenx_gapfill.gapfill_policy_benchmark_report` | 正文在行里。不灌文件。导出走态势报告链（FE HTML → situation/report → OpenHTMLtoPDF）；禁 trackingExport 打印另存 |
| 218 | 对标结果可视化展示 | 已有力度表 | 不建 `gapfill_policy_benchmark_viz` |

## 2. 已有力度表

表名 `policy_intensity`。架构和接口简称 `ads.policy_intensity`。`ads.md` 把建表登记在 `demo_gkxlumenx_ads.policy_intensity`。已有 `polan.eval.intensity.run()`（`lumen-algo-py/vendor/entan-py`）经 `conn.ads` 写入这张表：政策平面为演示时库名是 `demo_gkxlumenx_ads`，平面为正式时库名是 `gkxlumenx_ads`。同一张表结构。本叶不复制第三份，不在 `gkxlumenx_gapfill` 再造力度表，不加列，不改 `run()`。

粒度：`scope_type=policy` 的一行是一条政策；`scope_code` 为 `policy_id`。`scope_type=province` 的一行是一个省级范围。本叶不改这两档粒度。

| 读什么 | 已有列 | 谁写入 | 这次请求 |
|---|---|---|---|
| 214、218 的力度分 `M_POLICY_INTENSITY_SCORE` | `policy_intensity.intensity_score`。行条件：`scope_type=policy` 且 `metric_id=M_POLICY_INTENSITY_SCORE` | 已有 `run()` | 请求不现算。返回只读表上的分 |
| 216 的支持力度 `M_POLICY_SUPPORT_STRENGTH` | 同一次 `run()` 写在同库已有表 `policy_metric_timeseries`：`metric_id=M_POLICY_SUPPORT_STRENGTH`，`metric_value` 为值，`dim_key` 为「支持力度」，`region_code` 为地区 | 已有 `run()` | `gkxlumen-element` 在 `GET panorama/stats` 上同步读。这次统计请求不调用 `run()` |

`policy_intensity` 的已有列是 `scope_type`、`scope_code`、`scope_name`、`intensity_index`、`intensity_score`、`industry_coverage`、`rank_no`、`metric_id`、`calc_batch_id`、`ext`。其中没有支持力度列。`ads.md` 展示窗口把 `SUPPORT_STRENGTH` 映到 `policy_intensity`，与 `run()` 的实际写入表不一致。本叶不补列，不改 `ads.md`，不改架构稿。element 同步读的是这份 `run()` 已经写下的支持力度，不在统计请求里现算，也不把 216 放进 `POL-L2-DS10-CMP-GAPFILL-L01`。

正文列 `policy_base_info.policy_support` 是清洗字段。支持力度不读这一列。

`M_POLICY_INTENSITY_INDEX` 不挂本页。`run()` 会把省级 `intensity_index` 写在同一张 `policy_intensity` 上，本叶不改挂、不删那一列。QPOL-02 的权重保持待确认。`ext` 里已有 `is_mock` 与 `pending=QPOL-02` 的写法保持不动。三维缺数据、`run()` 写不出力度分时，该格空，不在接口里补一个分数。

214、218 的公开资源是 `POST /display/v1/policy/panorama/jobs`，`sub_type=policy_intensity`。`gkxlumen-display` 只提交已有 `POST /topic/v1/analysis/tasks`。接通之后由已有适配器调用已有 `run()`，再按所选政策或地区读表。`sub_type` 尚未放行时，这次 Job 的力度结果为空，不返回演示分，也不返回演示序列。216 不进这条 Job。

对标对象的候选项从 `policy_intensity` 已有的地区范围（`scope_type=province` 的 `scope_code`、`scope_name`）在同一次读取里带出。没有海外城市。本叶不另建对象表。

D4 保持 mock。无行则该格、该卡或该图空，不造 0。

## 3. 213 政策新旧对比

库 `gkxlumenx_gapfill`，表 `gapfill_policy_version_diff`。一行是同一政策在两个发布时间之间的一条变更：变更类型（新增、修改、删除）和一句摘要。一行不是一个版本号，不是一段高亮 HTML，不是一个 diff 文件。

可选时点不从本表反查。来源是 `policy_base_info` 上成对的两行：新版一行，历史版一行（`policy_id` = 新版 id 加 `-H1`，`status=已废止`，同 `source_plane`）。两个时点就是这两行的 `publish_date`（发文日期）。读取方 `gkxlumen-element`，经 `GET /display/v1/policy/panorama/versions`。没有 `-H1` 行的政策凑不齐两个时点，对比空。本表不补第二个日期，也不用 `publish_year` 编出一个时点。

> **2026-11-07 变更（POL-L2-DS10-SRCMON-SYNTH-L01）**：原写法「时点取同一正文上的 `publish_date`」只有一个日期，产线永远凑不齐两个时点。改为新版加 `-H1` 历史版成对。成对行目前只由 LLM 合成写入：每次合成 10 条，随机挑 5 条再写旧版（旧版发布日早 1～3 年），新旧之间的增改删写本表，`fill_method=llm-synth`，`gapfill_batch_id` 为合成批次号，`is_mock=1`。「删除所有 Mock 数据」会一并删除这些变更行。

拣行键：`policy_id` 加上这两个发布日期。两个日期与查询给出的两个发布时间成对相等，次序不另编版本号。对不上的行不返回。

灌数方：`POL-L2-DS10-CMP-GAPFILL-L01`（手工 5 行），以及 `POL-L2-DS10-SRCMON-SYNTH-L01`（合成政策的历史版本变更行）。读取方：`gkxlumen-element`，经 `GET /display/v1/policy/panorama/version-diff`。`gkxlumen-display` 不直连库。不写入 ODS、DWD、ADS、供应方库。

下列是逻辑列，不是可执行 DDL。建表由灌数单落地。本单不执行。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `policy_id` | varchar(100) | 否 | 政策。与已有正文 `policy_id` 同一业务键。不建外键 |
| `publish_date_a` | date | 否 | 两个发布时间之一。值等于已有 `publish_date`，不另编版本号 |
| `publish_date_b` | date | 否 | 两个发布时间的另一个。与 `publish_date_a` 成对，不表示版本先后编号 |
| `change_type` | varchar(16) | 否 | `新增`、`修改`、`删除` 三者之一 |
| `summary_text` | text | 否 | 一句摘要 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。213 没有已挂指标，不新注册 |
| `gap_item` | varchar(128) | 否 | 固定 `213 政策新旧对比` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。不设 `version_no`。不设高亮 HTML 列，不设文件列。

同一政策、同一对日期可以有多行，按变更类型和摘要分开。查询把对上的行一起返回。表空，或两个日期对不上，则对比空。查询不插入行。

### 3.1 213-3 演变趋势说明（配对级）

库 `gkxlumenx_gapfill`，表 `gapfill_policy_version_analysis`。一行是同一政策、同一对发布时间上的一句演变趋势说明。不是 diff 行摘要，不塞进 `summary_text`。

拣行键：`policy_id` + 两个发布日期（次序对调仍命中）。至多一行。

灌数方：seed（可演样本）与 `POST /internal/policy/version-analysis/enrich`（LLM）。合成历史版路径在写入 diff 后可顺带 enrich。读取方：`gkxlumen-element`，经 `GET /display/v1/policy/panorama/version-diff` 顶层字段 `analysis_text`。不写入 ODS、DWD、ADS。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。自增 |
| `policy_id` | varchar(100) | 否 | 与 diff 表同一业务键 |
| `publish_date_a` | date | 否 | 两个发布时间之一 |
| `publish_date_b` | date | 否 | 另一个发布时间 |
| `analysis_text` | text | 否 | 一句演变趋势说明（含两时点） |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空 |
| `gap_item` | varchar(128) | 否 | 固定 `213 政策新旧对比·分析` |
| `fill_method` | varchar(16) | 否 | `manual`（seed）或 `llm` / `llm-synth` |
| `gapfill_batch_id` | varchar(64) | 否 | 批次 |
| `generated_at` | datetime | 否 | 写入时间 |

唯一约束：同一政策同一对日期一行（实现可用应用层 upsert；DDL 可加唯一索引 `(policy_id, publish_date_a, publish_date_b)` 并在写入前规范化日期次序）。

## 4. 214 政策详情对比

三块落点分开。接口按块读表，不把三块拼成一段写死的对比文案。

申报时间、受理部门、产业类别继续读专题门面已有正文，经 `panorama/search` 与 `{id}/detail` 委托 `gkxlumen-topic-policy`。这三列不进缺项表，本叶不加 DWD 列。受理部门不是第 5 节的实施部门，不读 `gapfill_policy_impl_dept`。

力度分走第 2 节：已有 `run()` 写入 `policy_intensity.intensity_score`，请求不现算。

申报条件、申报材料、优缺点没有字段，也没有模型。库 `gkxlumenx_gapfill`，表 `gapfill_policy_detail_compare`。一行是一条政策的条件、材料与优缺点正文。

拣行键：`policy_id`。一条政策一行。条件对不上的行不返回。详情对比读面同一次带出四列（条件/材料/优缺点）；未勾选条件材料维时仍可读优缺点（COVER-FDE：开始对比即读本表）。

灌数方：`POL-L2-DS10-CMP-GAPFILL-L01`（2026-11-12 扩列）。读取方：`gkxlumen-element`，在同一次 `GET /display/v1/policy/panorama/{id}/detail` 里只读这些列。正文仍走专题门面。display 不直连库，不直连 Python。不写入 ODS、DWD、ADS、供应方库。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `policy_id` | varchar(100) | 否 | 拣行键。与已有正文 `policy_id` 同一业务键。不建外键。灌数时同一 `policy_id` 只留一行 |
| `apply_condition` | text | 否 | 申报条件 |
| `apply_material` | text | 否 | 申报材料 |
| `pros_text` | text | 否 | 优点。多条用换行分隔。无内容写空串，不造接口 mock |
| `cons_text` | text | 否 | 缺点。多条用换行分隔。无内容写空串 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。条件与材料不是 `M_POLICY_INTENSITY_SCORE` |
| `gap_item` | varchar(128) | 否 | 固定 `214 政策详情对比` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

存量库：`ALTER TABLE ... ADD COLUMN pros_text/cons_text` 后由灌数脚本回填。不设 `fill_model`。不设申报时间、受理部门、产业类别、力度分。某一列无行则该列空。查询不插入行。

**优缺点 LLM 补写（2026-11-12，`POL-L2-DS10-CMP-PROS-LLM-L01`）**：`POST /display/v1/policy/panorama/jobs`，`sub_type=policy_detail_pros_cons`。Python 仅当该 `policy_id` 行不存在，或存在但 `pros_text`/`cons_text` 去空白后皆空时写入；`fill_method=llm-synth`，`gap_item` 仍为 `214 政策详情对比`。已有非空优缺点不覆盖。无密钥/失败不造假文。不写入 ODS/DWD/ADS。

## 5. 215 部门政策对比

区域走已有地区分布。项目类别、技术类别走已有政策类型和产业节点。总件数仍是已有 `M_POLICY_TOTAL_COUNT`。这三段不进缺项表，不新灌，不把缺项件数改挂成政策总数。

实施部门在现网收集不到。库 `gkxlumenx_gapfill`，表 `gapfill_policy_impl_dept`。一行是一个区域、一个实施部门、一个方面，带件数和清单标题。方面只有两个取值：`项目类别`、`技术类别`。方面的具体词仍用已有词表里的政策类型或产业节点，不写进本表，也不把 demo 的扶持类、技术类写进本表。

实施部门的候选项只来自本表。区域候选项不从本表反查。目录按发布机构筛不到这些部门。清单标题只在本表。标题对不上已有政策时只显示标题，不编 `policy_id`，不写政策正文。

拣行键：区域、实施部门、方面。三键相同的只留一行。条件对不上的行不返回。

灌数方：`POL-L2-DS10-CMP-GAPFILL-L01`。读取方：`gkxlumen-element`，在同一次 `GET /display/v1/policy/panorama/stats` 里带出。区域、类别、总件数仍委托 `gkxlumen-topic-policy`。display 不直连库。不另开路径。不写入 ODS、DWD、ADS、供应方库。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `region_name` | varchar(64) | 否 | 区域。与用户从已有地区分布里选定的名称对齐。不建外键 |
| `impl_dept` | varchar(128) | 否 | 实施部门。候选项只来自本列 |
| `aspect` | varchar(16) | 否 | `项目类别`、`技术类别` 二者之一 |
| `item_count` | bigint | 否 | 该三键上的件数。不是新指标，不写入 `metric_id` |
| `list_title` | text | 否 | 清单标题。多条标题在同一格内分行。不写政策正文 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。不挂 `M_POLICY_TOTAL_COUNT`，不新注册部门指标 |
| `gap_item` | varchar(128) | 否 | 固定 `215 部门政策对比` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

不设 `fill_model`。不设 `policy_id`。表无行则部门对比空。查询不插入行。D4 保持 mock。

## 6. 216 标杆比对功能

不新建表，不加列，不进 `POL-L2-DS10-CMP-GAPFILL-L01`。

指标 `M_POLICY_SUPPORT_STRENGTH`。读取方是 `gkxlumen-element`，资源是 `GET /display/v1/policy/panorama/stats`，同步，不进 Job。读第 2 节已经由 `run()` 写入的支持力度。这次统计请求不调用 `run()`，请求不现算。

对标范围、对标对象、勾选字段是这次查询的条件，不落新列。范围只有全球科创领先城市、国内先进地区。字段只有政策类型、支持力度、覆盖范围。金额档不是 `policy_intensity` 或 `policy_metric_timeseries` 上的列。金额档缺失时该维空。无行则该卡空，不造 0。

未勾选的字段不进第 7 节的报告，也不进第 8 节的图。对标报告正文不在本叶生成。

**「政策类型」列读法（2026-11-11 增补，`POL-L2-DS10-CMP-PTYPE-FDE`，QPOL-01 临时默认 🟡）**

- 只读已有表：`dwd.policy_base_info` 的 `province`、`policy_type`、`policy_id` 三列（`is_deleted=0`、`source_plane IN ('domestic','global')`）。不建 gapfill 表，不写 ODS/ADS，不灌 mock 行。
- 聚合：`province × policy_type` 去重计件（`COUNT(DISTINCT policy_id)`），SQL GROUP BY 下推库端。每省返回各文种件数与 Top 文种（件数多者；同数取字典序首个）。
- 拣行键：对象→省沿用 `policy_intensity` 省级行的 `scope_code`/`scope_name`；某省无文种行则该省条目缺席，不造 0。
- 口径：DWD 文种是 QPOL-01 增补的**临时默认**，与主口径（ODS `topic_type` 主题分类，`M_POLICY_TYPE_DIST` 已挂）并行不互斥；甲方归一时一并定 216 用文种还是主题分类，切换只改 SELECT 不动链路。UI 带 🟡「待甲方确认」。
- 不新造 `metric_id`：这是对照展示列，不是新统计指标；`M_POLICY_TYPE_DIST` 的全国口径与本列的按省文种口径不互相顶替。D4 判定不变（读 DWD 真列，非 mock 灌行）。

## 7. 217 对标报告生成与导出

没有对标报告模型。库 `gkxlumenx_gapfill`，表 `gapfill_policy_benchmark_report`。一行是一个对标对象在一个已勾字段上的一段对照：差异、优劣、借鉴建议、报告正文都在这一行。

拣行键：对标对象和已勾字段。对象与字段沿用 216 已经选定的那一组。`benchmark_object` 属于这组对象，并且 `compare_field` 属于已勾字段，才返回该行。没有 216 的选择则报告空。未勾选的字段不返回。对标对象的候选项不从本表反查，来自第 2 节力度表已有的地区范围。

灌数方：`POL-L2-DS10-CMP-GAPFILL-L01`。读取方：`gkxlumen-element`，经 `GET /display/v1/policy/panorama/benchmark-report`。display 不直连库。不写入 ODS、DWD、ADS、供应方库。

导出格式只有 PDF、Word，是请求条件，不落列。不选格式则只在线看行。导出文件不进本 gapfill 表；真文件走态势报告链（`situation/report` → topic-async OpenHTMLtoPDF，OSS/`gkx-lumen` 或 local 指针，与态势页同构）。gapfill 表本身不写桶名和对象键。不建邮件。核增研报 `report/jobs`（614–618）和检索分享 `share` 不是这张表。废止仅前端 `trackingExport` 打印另存。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `benchmark_object` | varchar(128) | 否 | 对标对象。拣行键的一截 |
| `compare_field` | varchar(32) | 否 | 已勾字段。只允许 `政策类型`、`支持力度`、`覆盖范围` |
| `difference_text` | text | 否 | 差异 |
| `pros_cons_text` | text | 否 | 优劣 |
| `suggestion_text` | text | 否 | 借鉴建议 |
| `report_body` | text | 否 | 报告正文。写在行里 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 留空。217 没有已挂指标，不新注册 |
| `gap_item` | varchar(128) | 否 | 固定 `217 对标报告生成与导出` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

不设 `fill_model`。不设 PDF、Word、对象键。无行则报告空，也不产生文件。查询不插入行。

## 8. 218 对标结果可视化展示

不建 `gapfill_policy_benchmark_viz`。不写 ODS、DWD、ADS 新表。

雷达、柱、热力的数来自第 2 节已有力度表里 214 已经读到的力度分，以及 216 已经读到的支持力度。公开资源与 214 力度分相同：`POST /display/v1/policy/panorama/jobs`，`sub_type=policy_intensity`。先有已有 `run()` 的写入，再读表。请求不现算，不返回演示序列。

图上若只画件数，仍用 215 的目录命中和已有 `M_POLICY_TOTAL_COUNT`，不改挂成力度分。`M_POLICY_INTENSITY_INDEX` 不挂本页。对象和字段沿用 216。政策视角用 214 已选的政策。表无行或 `sub_type` 未放行则图空。

## 9. 灌数单

只点名，本单不执行，不建库，不插入行，不调用 `run()`。

| 灌数单 | 做什么 | 本单 |
|---|---|---|
| `POL-L2-DS10-CMP-GAPFILL-L01` | 按第 3、4、5、7 节建四张 `gapfill_` 表并灌 mock 行。执行人 `data-agent`，监管 `human:淮政玮`。依赖本架构和本数据叶 | 不执行。查询请求不调用它 |
| 已有 `polan.eval.intensity.run` | 写入第 2 节的 `policy_intensity` 与 `policy_metric_timeseries`。216 不进灌数单 | 不执行，不改公式 |

四张缺项表的灌数方都是这一张灌数单。读取方都是 `gkxlumen-element`。空表返回空。

## 10. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| 197–202 | 213 的时点复用检索叶已有 `publish_date`。本叶不读 `gapfill_policy_qry_doc`、`gapfill_policy_qry_stat`、`gapfill_policy_qry_rank`，不建历史、收藏、导出 |
| 202 `share` | 检索目录导出。不是 217 |
| 207、208 | 深度交叉与区域子图。本叶不读图，不写 nGQL |
| 209–212 | 效果、反馈、评估报告、匹配。211 的 `gapfill_policy_assessment_report` 不是 217 |
| 614–618 `report/jobs` | 核增研报。不是 217，不进本二级落点 |
| `M_POLICY_INTENSITY_INDEX` | `run()` 会写在省级行。本叶不挂到 214 或 218 |
| `M_POLICY_INDUSTRY_COVERAGE` | 同表已有列。本叶不改挂成 216 的覆盖范围字段 |
| 门户扶持十条 | 不得改挂到力度指数、力度评分或产业覆盖率。本叶不把它们写入部门表 |

## 11. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑 `run()`。
- 不重开 GDF，不写 nGQL。
- 新表只有第 1 节四张 `gkxlumenx_gapfill.gapfill_` 表。不建 `gapfill_policy_benchmark_viz`。不写 ODS、DWD、ADS 新表，不加已有 ADS 列。
- 不新造 `metric_id`，不改 D4，不把缺项行或 `run()` 的 `is_mock` 写成已上线。
- 不把四张缺项表的行写入 ODS、DWD、ADS、供应方库。
- 不从缺项表反查 213 的可选时点。不把版本号、高亮 HTML、假 diff 文件写进 213。
- 不把时间、受理部门、产业、力度分写进 214 的缺项表。
- 不把缺项件数登记成 `M_POLICY_TOTAL_COUNT`。不按发布机构去重灌实施部门。
- 不把 216 放进灌数单。统计请求不现算支持力度。Job 的返回不现算力度分。
- 不在接口里直接返回写死的差异、分数、部门名单、报告或 PDF。
- 不改架构稿、说明书、WBS、检索叶、`ads.md`、`dwd.md`、注册表。
- 不把本单标成 done。会签态记未会签。
