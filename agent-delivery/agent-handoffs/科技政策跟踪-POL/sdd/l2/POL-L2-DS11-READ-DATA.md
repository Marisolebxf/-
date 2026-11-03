# POL-L2-DS11-READ-DATA · 政策分析评价 · 结果解读报告多维展示 · 数据落点

- 任务：`POL-L2-DS11-READ-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（已认领，状态 `in_progress`，本单不改状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 会签态：本数据叶未会签。上游架构四页已于 2026-11-03 同意。本叶不代签，不标 done
- 上游架构：`POL-L2-DS11-READ-ARCH`（四页会签同意）。表与合规 mock 在该稿第 8 节。该稿没有第 9 节。本单同时对照 `sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-DATA.md` 以及同目录的架构、算法、产品会签页。本单只写数据落点，不改那些稿，不改图。

本叶只定政策分析评价二级「结果解读报告多维展示」的数据落点。SRS 序号 **223–226**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-READ-ARCH.md` 第 4 节和第 8 节、四份会签页、说明书第 11.2 节「评价 · 解读 223–226」那一行、`storage/POLICY/stores/mysql/ads.md` 已登记的 `policy_effect`、`policy_focus`、`policy_text_parse`。指标沿用已有 `metric_id`。不新造 `metric_id`，不改 D4。

## 1. 范围

四叶都在政策分析评价里完成。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python。查询只读表。`counts` 与 `shells` 的查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

新建表只有库 `gkxlumenx_gapfill` 下这一张：

| 表 | 序号 | 灌数方 | 读取方 | 拣行键 |
|---|---|---|---|---|
| `gapfill_policy_eval_shell` | 224 的解读条目；225 的标题和一句说明 | `POL-L2-DS11-READ-GAPFILL-L01` | `gkxlumen-element` | `entry_kind`，并与 `gap_item` 成对 |

这张缺项表只灌两类行：224 的解读条目（专题或指标名、一句结论、一句应用建议），225 的多媒体标题加一句说明。不灌视频，不灌动画，不灌图形文件，不灌 PDF，不灌模板选用。

不建 `gapfill_policy_eval_focus`。不建 `gapfill_policy_eval_summary`。不建 `ads.policy_gap`。不写 ODS、DWD、ADS 新表，不加已有 ADS 列，不写供应方库。不新开 GDF。不写 nGQL。

三张已有表只读，或由已有 `run()` 按原路径写入。本单和灌数单都不往这三张表插入 shell 行。

| 表 | 序号 | 灌数方 | 读取方 | 拣行键 |
|---|---|---|---|---|
| `ads.policy_effect` | 223 短板 | 已有 `polan.eval.gap.run`。不新开灌数单。这次 `counts` 不调用它 | `gkxlumen-element` | `scope_type=region_gap` |
| `ads.policy_focus` | 223 焦点 | 展示 Job 调用已有 `polan.eval.focus.run`。不新开灌数单 | Python `jobs/execute`，`sub_type=policy_focus_ads` | `policy_id` 非空 |
| `ads.policy_text_parse` | 226 | 已有 `polan.text.parse.run` 的解析批次。展示请求不调用它 | Python `jobs/execute`，`sub_type=policy_text_parse` | 现有行，返回列只取 `summary` |

这张缺项表只服务功能验收。生产配置不读 `gkxlumenx_gapfill`。行上带 D16 规定列。缺项表有行也不把 D4 改成 live。`GDF-POLICY-MOCK-GATE-L01` 仍未解开。`QPOL-02` 不在本单闭合。

| 序号 | 叶子 | 库表 | 本单 |
|---|---|---|---|
| 223 短板 | 热点问题分析看板 | 已有 `ads.policy_effect` | 不加列，不进灌数单 |
| 223 焦点 | 热点问题分析看板 | 已有 `ads.policy_focus` | 不建 `gapfill_policy_eval_focus` |
| 224 | 分主题分指标互动解读 | `gkxlumenx_gapfill.gapfill_policy_eval_shell` 的解读行 | 本单定逻辑列 |
| 225 | 多媒体辅助解读 | 同一张 shell 的多媒体行 | 只灌标题和一句说明 |
| 226 | 智能摘要与结论推送 | 已有 `ads.policy_text_parse.summary` | 不建 `gapfill_policy_eval_summary` |

## 2. 已有三张 ADS

表名是 `policy_effect`、`policy_focus`、`policy_text_parse`。架构和接口简称 `ads.<表名>`。代码 SCHEMA 的默认库是 `demo_gkxlumenx_ads`。已有 `run()` 经 `conn.ads` 写入，库名随已有连接。同一张表结构。本叶不复制第三份，不在 `gkxlumenx_gapfill` 再造这三张表，不加列，不改 `run()`。

`ads.md` 把建表登记在 `demo_gkxlumenx_ads`。本单不改 `ads.md`。

D4 保持 mock。无行则该计数、该块或该摘要空，不造 0。

## 3. 223 短板 · 已有 `policy_effect`

不新建表，不加列，不进 `POL-L2-DS11-READ-GAPFILL-L01`。不建 `ads.policy_gap`。

指标 `M_POLICY_SHORTBOARD_COUNT`。粒度：`scope_type=region_gap` 的一行是一个区域。`scope_code` 为区域码，`scope_name` 为区域名。已有 `polan.eval.gap.run` 先删除 `scope_type=region_gap` 再写入。本单不改这个删除范围，不改公式，不改权重。

| 读什么 | 已有列 | 谁写入 | 这次请求 |
|---|---|---|---|
| 短板条数 | `policy_effect.shortboard_cnt`。行条件：`scope_type=region_gap`。行上 `metric_id` 仍是 `M_POLICY_SHORTBOARD_COUNT` | 已有 `gap.run` | `GET /display/v1/policy/evaluation/counts` 不调用 `gap.run`。返回只读表上的条数 |
| 区域 | `scope_code`、`scope_name` | 同上 | 不另建区域列 |
| 分项原因 | `ext.reasons`。`ext` 里已有 `is_mock` 与 `pending=QPOL-02` | 同上 | 不另建原因列 |

`effect_score`、`layout_rec_cnt`、`impl_effect` 留在表上。短板读面不取这三列。本单不补值。

拣行键：`scope_type=region_gap`。对不上的行不返回。无行则计数空，不造 0。查询不把各区域加总登记成新指标。

读取方：`gkxlumen-element`。`gkxlumen-display` 不直连库。这次读取不调用 `gap.run`，也不把 `GDF-POLICY-MDC-STAT-L01` 写成已覆盖本指标。

灌数方：已有 `polan.eval.gap.run`。不新开灌数单。要补批次时只跑这份已有函数。本单不执行。

`scope_type=region_effect` 上的 `M_POLICY_EFFECT_SCORE` 由已有 `effect.run` 写入。那不是本读面。

## 4. 223 焦点 · 已有 `policy_focus`

不新建表，不加列，不进灌数单。不建 `gapfill_policy_eval_focus`。

指标 `M_POLICY_FOCUS_INDEX`。`policy_id` 非空的一行是一条政策。`policy_id` 为空的行是机遇，不在本读面。已有 `polan.eval.focus.run` 只删除 `policy_id IS NOT NULL` 的行再写入，不删除 `policy_id` 为空的机遇行。本单不改这个删除范围，不改公式，不改权重。

| 读什么 | 已有列 | 谁写入 | 这次请求 |
|---|---|---|---|
| 焦点指数 | `policy_focus.focus_score`。行条件：`policy_id` 非空。行上 `metric_id` 仍是 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE` | 已有 `focus.run` | Job 调用这份 `run()` 之后再读。返回只读表上的分 |
| 名称 | `ext.title` | 同上 | 不另建名称列 |
| 一句说明 | `ext.explanation` | 同上 | 不另建说明列 |

`ext` 里已有 `is_mock` 与 `pending`。本单不改。`relation_degree` 留在同一行。本单不把它改挂到 223，不为此写 nGQL，不改 `focus.run` 内部对边镜像的既有读法。

拣行键：`policy_id` 非空。`policy_id` 为空的行不返回。无行则焦点块空，不造 0，不返回写死指数。

读取方：Python `/internal/policy/jobs/execute`，`sub_type=policy_focus_ads`。公开资源是 `POST /display/v1/policy/evaluation/jobs`。`gkxlumen-display` 只提交已有 `POST /topic/v1/analysis/tasks`。接通之后由已有适配器调用已有 `focus.run`，再按拣行键读表。`gkxlumen-display` 不直连库，不直连 Python。`sub_type` 尚未放行时，这次 Job 的焦点结果为空，不返回演示分。

灌数方：同一次 Job 调用的已有 `focus.run`。不新开灌数单。本单不执行。带 items 的既有 `policy_focus` 仍走 harness。展示看板不读 harness 的返回。`focus-one` 不写这张表，本读面不取它。

## 5. 224、225 · `gapfill_policy_eval_shell`

没有专属 `metric_id`，也没有已注册的解读模型或多媒体模型。库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_shell`。一张表两种行，用 `entry_kind` 分开。

解读行（224）：一行是一条解读。内容是专题或指标名、一句结论、一句应用建议。同一专题或指标可以有多行。点选在已经返回的解读行里按 `subject_name` 筛选，不另做查询键，不另起计算。

多媒体行（225）：一行是一条多媒体辅助。内容只有标题和一句说明。不灌视频，不灌动画，不灌图形文件，不灌 PDF。

拣行键：`entry_kind`，并且与 `gap_item` 成对。

- `entry_kind=解读` 且 `gap_item=224 分主题分指标互动解读` 的行是 224。
- `entry_kind=多媒体` 且 `gap_item=225 多媒体辅助解读` 的行是 225。
- 这两列对不上的行不返回。

灌数方：`POL-L2-DS11-READ-GAPFILL-L01`。只灌上面两类行。不灌序号 222 的模板选用。读取方：`gkxlumen-element`，经 `GET /display/v1/policy/evaluation/shells`。同一次读取可以带出两类，调用方按 `entry_kind` 分开。`gkxlumen-display` 不直连库。不写入 ODS、DWD、ADS、供应方库。不写对象存储，前端不直连 RustFS。

下列是逻辑列，不是可执行 DDL。建表由灌数单落地。本单不执行。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `entry_kind` | varchar(16) | 否 | `解读`、`多媒体` 二者之一。拣行键 |
| `subject_name` | varchar(128) | 多媒体行必空 | 解读行必填。专题或指标名。点选筛的是已返回行上的这一列 |
| `conclusion_text` | text | 多媒体行必空 | 解读行必填。一句结论 |
| `suggestion_text` | text | 多媒体行必空 | 解读行必填。一句应用建议 |
| `title` | varchar(200) | 解读行必空 | 多媒体行必填。标题 |
| `caption_text` | text | 解读行必空 | 多媒体行必填。一句说明 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 没有已挂指标则留空。不新注册。多媒体行留空。解读行只有该条目确实指向已经登记的 `metric_id` 才填写该已有号 |
| `gap_item` | varchar(128) | 否 | 解读行固定 `224 分主题分指标互动解读`。多媒体行固定 `225 多媒体辅助解读`。与 `entry_kind` 成对 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`，因此不设 `fill_model`。不设视频、动画、图形、PDF、对象键、模板号、模板正文。不设 `policy_id`。不把 226 的 `summary` 复制进本表。不把 223 的 `ext.title`、`ext.explanation` 复制进本表。

表空则对应块空。只有解读行时，多媒体块空。只有多媒体行时，解读块空。查询不插入行。D4 不因这些行改成 live。224、225 没有专属指标，本单不新造。

## 6. 226 智能摘要 · 已有 `policy_text_parse.summary`

不新建表，不加列，不进灌数单。不建 `gapfill_policy_eval_summary`。不建编辑表。不把用户改过的句子写回。不灌推送记录。

展示读面用已有 `M_POLICY_DS_11_POLICY_EVAL_012`。这是读面身份，不是第二套摘要，也不写进新列。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本单不改这个行上的号。写入 `summary` 的已有 `polan.text.parse.run` 是规则截取。本单不把截取改成大模型，不改截取长度。

`parse.run` 会先清空整张 `policy_text_parse` 再插入。条款结构化写在同一张表的 `structured_elements`。展示请求只查询，避免一次请求把整表清掉。

拣行键：这张表现有的行。返回列只取 `summary`。行上已有 `policy_id`，本单不加筛选列，也不另编摘要编号。无行则摘要空。`summary` 为空的行不补一句。不把 `structured_elements`、`auto_tags`、`title` 当成摘要。不读 `policy_summary`。

读取方：Python `/internal/policy/jobs/execute`，`sub_type=policy_text_parse`。公开资源是 `POST /display/v1/policy/evaluation/jobs`。`gkxlumen-display` 只提交已有 `POST /topic/v1/analysis/tasks`。这条路径只查询，不调用 `parse.run`。`gkxlumen-display` 不直连库，不直连 Python。`sub_type` 尚未放行时，这次 Job 的摘要为空，不返回写死段落。

灌数方：已有 `polan.text.parse.run` 的解析批次。不在展示请求里调用。不新开灌数单。要补批次时只跑这份已有函数，并且知道它会清空整表。本单不执行。

`focus-one`、序号 242 的推演解读、核增研报 `report/jobs` 不写入这张读面。

## 7. 灌数单

只点名，本单不执行，不建库，不插入行，不调用 `run()`。

| 灌数单或已有函数 | 做什么 | 本单 |
|---|---|---|
| `POL-L2-DS11-READ-GAPFILL-L01` | 按第 5 节建 `gapfill_policy_eval_shell`，只灌 224 解读条目和 225 多媒体标题加一句说明。执行人 `data-agent`，监管 `human:淮政玮`。依赖本架构和本数据叶 | 不执行。查询请求不调用它 |
| 已有 `polan.eval.gap.run` | 写入第 3 节的 `policy_effect`（`scope_type=region_gap`）。短板不进灌数单。`counts` 不调用它 | 不执行，不改公式 |
| 已有 `polan.eval.focus.run` | 223 焦点 Job 调用它，写入第 4 节的 `policy_focus`（`policy_id` 非空），再读 | 不执行，不改公式，不改删除范围 |
| 已有 `polan.text.parse.run` | 写入第 6 节的 `policy_text_parse.summary`。展示请求不调用它 | 不执行，不改截取 |

shell 的灌数方是这一张灌数单，读取方是 `gkxlumen-element`。三张已有表的读取方见第 1 节。空表返回空。接口不直接返回写死的 mock。

## 8. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `M_POLICY_OPPORTUNITY_COUNT` | 无 223–226 的序号。写在 `policy_focus` 且 `policy_id` 为空的行。`counts` 上已有的机遇读面本叶不改 |
| `M_POLICY_RELATION_DEGREE` | 留在焦点行的 `relation_degree` 和拼接 `metric_id` 上。本叶不改挂，不写 nGQL |
| `M_POLICY_EFFECT_SCORE` | 在 `policy_effect` 的 `scope_type=region_effect`。不进 223 的短板读面 |
| `M_POLICY_DEEP_169_1` | 仍是 MODEL。不在 223 的同步链上计算 |
| `M_POLICY_TEXT_PARSE` | 留在 `policy_text_parse` 行上。226 的展示读面仍是已有 `M_POLICY_DS_11_POLICY_EVAL_012`，不另造号 |
| `policy_summary` | 不作为 226 的表 |
| 219–221 | 趋势、分区、结构关联另叶。本叶不读 `gapfill_policy_eval_trend`、`gapfill_policy_eval_partition`，不读图 |
| 222 | 报告模板与批量导出。模板选用不写入 shell |
| 227–231 | 方案、参数模拟、实施路径、意见与归档。`M_POLICY_DS_11_POLICY_EVAL_015` 不挂本叶。不读 `gapfill_policy_eval_scheme` |
| 242、`report/jobs` | 推演解读和核增研报。不是 226 的摘要 |
| `focus-one` | 不写 ADS。不充当焦点，也不充当摘要 |
| 既有 `policy_focus` harness | 带 items 的作业保持原样。看板走 `policy_focus_ads` |
| `GDF-POLICY-MOCK-GATE-L01` | 仍未解开。本叶不新开 GDF |

## 9. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑 `gap.run`、`focus.run`、`parse.run`。
- 不重开 GDF，不写 nGQL，不写第二套统计脚本。
- 新表只有第 1 节这一张 `gkxlumenx_gapfill.gapfill_policy_eval_shell`。不建 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary`、`ads.policy_gap`。
- 不写 ODS、DWD、ADS 新表，不加已有 ADS 列，不写供应方库。不把 shell 的行写入这四库。
- 不新造 `metric_id`，不改 D4，不把缺项行或已有 `run()` 的 mock 写成已上线。
- shell 只灌 224 的解读条目和 225 的标题加一句说明。不灌视频、动画、图形文件、PDF、模板选用。
- 不从 shell 反查 223 的焦点或 226 的摘要。不把用户改稿和推送记录写入 `policy_text_parse`。
- 223 的 `counts` 不调用 `gap.run`。226 的展示请求不调用 `parse.run`。
- 不在接口里直接返回写死的短板数、焦点指数、结论、摘要、视频或 PDF。无行则空。
- 不改架构稿、会签页、说明书、WBS、`ads.md`、注册表。
- 不把本单标成 done。会签态记未会签。

## 10. 对照

架构第 7 节写：说明书第 11.2 节把 `gapfill_policy_eval_focus`、`gapfill_policy_eval_summary` 和 shell 写在同一行。当前说明书第 11.2 节「评价 · 解读 223–226」那一行已经只列 `gapfill_policy_eval_shell`，并写明焦点读 `ads.policy_focus`、短板读 `ads.policy_effect`、226 读 `ads.policy_text_parse` 的摘要，不灌 PDF、不灌视频，灌数单是 `POL-L2-DS11-READ-GAPFILL-L01`。本单不改说明书，不改架构稿。表名、要灌的内容和灌数单与该行以及架构第 8 节一致。列和拣行键写在本分册第 3–6 节。
