# POL-L2-DS11-PLAN-DATA · 政策分析评价 · 推荐方案报告交互展示 · 数据落点

- 任务：`POL-L2-DS11-PLAN-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游架构：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md` 第 9 节。该稿 2026-11-03 两轮四角色同意，文件头写明待 `human:淮政玮` 签收。本单按第 9 节定列，不改那份架构，不改图。
- 对照：同目录 `POL-L2-DS11-READ-DATA.md`。本单不改那份解读分册。

本叶只定政策分析评价二级「推荐方案报告交互展示」的数据落点。SRS 序号 **227–231**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`POL-L2-DS11-PLAN-ARCH` 第 9 节、同目录解读数据分册的壳表边界。不新造 `metric_id`，不改 D4。

## 1. 范围

五叶都在政策分析评价的推荐方案工作区里完成。浏览器只打 `/display/v1/policy/**`。查询只读表。查询请求不灌数。表里没有行就返回空。接口不直接返回写死的 mock。

本二级不读已有 ADS，也不读已经落库的推演结果。`ads.policy_simulate` 继续只服务推演键 `M_POLICY_SIMULATE`。仓库里没有已落库的方案、参数档、路径节点或专家意见可以复用。五叶只读将由灌数单新建的这一张缺项表。表还没建、或建了但没有对得上的行时，对应块返回空。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 227 | 多方案对比展示 | `gkxlumenx_gapfill` | `gapfill_policy_eval_scheme` 的方案对照行 | 本单定列。建表与灌数在灌数单 |
| 228 | 方案参数自定义模拟 | 同一张缺项表 | 同一张表的参数模拟行 | 与 227 同一张表，不另建 |
| 229 | 实施路径与风险辅助 | 同一张缺项表 | 同一张表的路径与风险行 | 与 227 同一张表，不另建 |
| 230 | 互动意见收集与专家参与 | 同一张缺项表 | 同一张表的互动意见行 | 与 227 同一张表，不另建 |
| 231 | 方案报告导出与归档 | 同一张缺项表 | 不另占种类，不另建行 | 导出读取方案对照行和互动意见行 |

路径与风险行引用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。该指标的 D4 保持 `mock`。方案对照、参数模拟、互动意见没有已挂指标，不因此新注册，也不把 D4 改绿。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

本叶唯一新建的表是 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。库只允许 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头。本单只定列，不建库，不插入。不写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`，不写供应方库。

`gkxlumen-display` 不直连库。`gkxlumen-element` 按种类只读这张表。227、228、229 走 `POST /display/v1/policy/evaluation/jobs`。230、231 走 `GET /display/v1/policy/evaluation/shells`。Java 不生成方案，不按公式现算，不插入意见，不插入采纳行。

## 2. 唯一新表

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`。227、228、229、230 共用这一张。不拆成四张表。231 不另建报告行，不另建文件表。

一行是一个方案，或挂在某个方案上的一档参数、一个路径节点、一条意见。一行不是一份 PDF，不是一份 Word，不是一份 Excel，不是一条推演曲线，不是政策子图上的一个点。

`row_kind` 只有四个值：

| 值 | 序号 | 这一行放什么 |
|---|---|---|
| `方案对照` | 227，并供 231 取正文 | 一个方案：名称、一句说明、对照维度和数值、优劣结论、实施建议 |
| `参数模拟` | 228 | 挂在一个方案上的一档：参数档、评估结果、一句趋势、一条归档说明 |
| `路径与风险` | 229 | 挂在一个方案上的一个节点：节点、时间进度、一句说明、风险标题、一句风险 |
| `互动意见` | 230，并供 231 取点评 | 挂在一个方案上的一条意见：主体、分类、意见正文、时间 |

没有第五个值。231 不写入 `row_kind`。与解读分册壳表 `gapfill_policy_eval_shell` 的 `entry_kind` 不是同一列。壳表不写入本表，本表不写入壳表。

下列是必要列。建表语句由灌数单 `POL-L2-DS11-PLAN-GAPFILL-L01` 落地。本单不执行该单，也不在这里给出可执行脚本。这张列清单不是可执行 SQL。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `row_kind` | varchar(16) | 否 | `方案对照`、`参数模拟`、`路径与风险`、`互动意见` 四者之一 |
| `scheme_name` | varchar(256) | 否 | 方案名称。四种行都填。方案对照行之间名称不重复。其余三种行的名称必须对得上某一条方案对照行 |
| `summary_text` | text | 是 | 方案对照行必填：一句说明。其余行空 |
| `compare_items` | text | 是 | 方案对照行必填：若干组维度名和数值，组数不固定。其余行空 |
| `verdict_text` | text | 是 | 方案对照行必填：优劣结论。其余行空 |
| `advice_text` | text | 是 | 方案对照行必填：实施建议。其余行空 |
| `param_band` | varchar(256) | 是 | 参数模拟行必填：参数档。同一方案下参数档不重复。其余行空 |
| `eval_result` | text | 是 | 参数模拟行必填：评估结果原文。其余行空 |
| `trend_text` | text | 是 | 参数模拟行必填：一句趋势。其余行空 |
| `archive_text` | text | 是 | 参数模拟行必填：一条归档说明。其余行空 |
| `node_name` | varchar(256) | 是 | 路径与风险行必填：节点名称。其余行空 |
| `schedule_text` | varchar(256) | 是 | 路径与风险行必填：时间进度，展示原文。其余行空 |
| `node_text` | text | 是 | 路径与风险行必填：一句节点说明。其余行空 |
| `risk_title` | varchar(256) | 是 | 路径与风险行必填：风险标题。其余行空 |
| `risk_text` | text | 是 | 路径与风险行必填：一句风险说明。其余行空 |
| `sort_no` | int | 是 | 路径与风险行必填：同一方案内的节点顺序，彼此不重复。其余行空。读取按 `sort_no` 从小到大，不按时间进度原文排序 |
| `actor_name` | varchar(128) | 是 | 互动意见行必填：主体。其余行空 |
| `opinion_kind` | varchar(16) | 是 | 互动意见行必填：`评价`、`评论`、`建议` 三者之一。其余行空 |
| `opinion_text` | text | 是 | 互动意见行必填：意见正文。其余行空 |
| `opinion_at` | datetime | 是 | 互动意见行必填：意见上的时间。与 `generated_at` 不是同一列。其余行空 |
| `is_mock` | tinyint | 否 | 每行必须为 1。D4 仍是 mock |
| `metric_id` | varchar(64) | 是 | 路径与风险行固定 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种留空，写 NULL，不写空字符串 |
| `gap_item` | varchar(128) | 否 | 序号加叶子名。见下表 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写，本单不生成 |

`gap_item` 按种类固定：

| `row_kind` | `gap_item` |
|---|---|
| `方案对照` | `227 多方案对比展示` |
| `参数模拟` | `228 方案参数自定义模拟` |
| `路径与风险` | `229 实施路径与风险辅助` |
| `互动意见` | `230 互动意见收集与专家参与` |

231 没有行，因此没有 `gap_item`。

`fill_method` 固定 `manual`，因此不设 `fill_model`。政策只在方法为 `llm` 时要求模型名。

D16 行级列就是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。外加 `is_mock=1`，避免把缺项行读成已上线。谁写这张表：灌数单里的 Python 脚本。Java 与前端不建表、不灌数。谁读：仅功能验收链路上的 `gkxlumen-element`。生产配置不读 `gkxlumenx_gapfill`。本叶不把读到的行写入 ADS，因此不产生 `gapfill_` 前缀的 `calc_batch_id`。

拣行只用 `row_kind`、`scheme_name`，参数模拟再加 `param_band`。条件对不上的行不返回。查询不插入行来凑数。

## 3. 227 方案对照

粒度：一行一个方案。名称在 `scheme_name`。一句说明在 `summary_text`。对照维度和数值在 `compare_items`。优劣结论在 `verdict_text`。实施建议在 `advice_text`。

`compare_items` 是文本，内容是若干组「维度名、数值」。组数不固定。雷达和 KPI 的数就是这些组。维度名不做成闭集。不单列资金、人才、平台、ROI。不抄展示原型里那三条方案常量的原文。

`metric_id` 留空。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DEEP_171_1`，不挂 `M_POLICY_SIMULATE`。

`jobs` 的方案对照只读 `row_kind=方案对照`。用户未指定方案时读出全部方案对照行。用户指定了方案时按 `scheme_name` 拣。返回行少于两行则对比空，本表不补第二个方案，Java 不补演示分。

## 4. 228 参数模拟

粒度：一行挂在一个方案上的一档参数。方案在 `scheme_name`。参数档在 `param_band`。评估结果在 `eval_result`。一句趋势在 `trend_text`。归档说明在 `archive_text`。

参数档是一行上的一段文字，不是资金、人才、平台三个滑块列。同一方案、同一参数档只保留一行。`eval_result` 是已灌入的原文。查询原样返回。请求内不调用 `polan.text.simulate.run`，不按弹性公式现算。

`metric_id` 留空。不把 `M_POLICY_SIMULATE` 写入这些行。不把省级力度情景、基线、变化率、逐年曲线灌进本表。`ads.policy_simulate` 的行不复制到这里。

`jobs` 的参数模拟按 `scheme_name` 和 `param_band` 拣 `row_kind=参数模拟`。方案必选。对不上则该次预览、趋势和归档都空。采纳不写库。归档只来自已经灌入的 `archive_text`。切参数不自动起任务，也不插入新行。

## 5. 229 路径与风险

粒度：一行挂在一个方案上的一个节点，节点和风险写在同一行。一个方案可以有多行。方案在 `scheme_name`。节点名称在 `node_name`。时间进度在 `schedule_text`。一句节点说明在 `node_text`。风险标题在 `risk_title`。一句风险说明在 `risk_text`。顺序在 `sort_no`。

`metric_id` 固定为已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不新注册，不改这条指标的 D4，不把读到的行写成已上线。口径仍是路径与风险的生成结果。本叶不读政策子图，不写 nGQL。现有推演函数不产出这条指标，本叶不改那个函数，也不把这次读取挂到 `M_POLICY_SIMULATE`。

`jobs` 的路径与风险按 `scheme_name` 拣 `row_kind=路径与风险`，按 `sort_no` 从小到大返回。方案必选。无行则路径和风险都空。不返回推演曲线来顶替。用户在页面上改期不回写这张表。

序号 241 的政策实施路径预测在推演页。那些行不写入本表，也不顶替本种类。

## 6. 230 互动意见

粒度：一行挂在一个方案上的一条意见。方案在 `scheme_name`。主体在 `actor_name`。分类在 `opinion_kind`，只用 `评价`、`评论`、`建议`。正文在 `opinion_text`。意见时间在 `opinion_at`。

没有意见指标。`metric_id` 留空。不把 `M_POLICY_DS_11_POLICY_EVAL_015` 抄到意见行上。

`shells` 的互动意见按 `scheme_name` 拣 `row_kind=互动意见`。方案未选则列表空，不返回全部意见。无行则列表空，不造一条专家意见。

请求处理不插入、不更新、不删除。用户在页面上新打的评价留在浏览器，直到另有采集单。本叶不建那张单。不把序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成方案意见，不把问卷行复制进本表。

## 7. 231 从已有行生成导出

不另建种类，不另建行，不另建文件表，不设文件地址、对象键、文件字节列。

`shells` 的方案报告读取本次范围内的方案对照行，以及 `scheme_name` 落在这些方案上的互动意见行。方案对照行取出 `scheme_name`、`summary_text`、`verdict_text`、`advice_text`、`compare_items`。互动意见行取出 `actor_name`、`opinion_kind`、`opinion_text`、`opinion_at`。导出正文从这些已读列生成。

参数模拟行和路径与风险行不进入这份导出。没有方案对照行则导出空。不返回一份写死的 PDF、Word 或 Excel。不写对象存储，前端不直连 RustFS。核增研报 `report/jobs` 不写入本表。

范围怎么传到接口，留给 `POL-L2-DS11-PLAN-API`。本单不写请求体和响应体。

## 8. 灌数单

灌数单 `POL-L2-DS11-PLAN-GAPFILL-L01` 依赖本单和 `POL-L2-DS11-PLAN-ARCH`。执行人是 `data-agent`，监管是 `human:淮政玮`。本单只点名，不认领，不执行，不建库，不插入行，不改那张任务的注册字段。

该单当前仍是 `backlog`。它的 DoD 已经指向这一张表：在 `gkxlumenx_gapfill` 建 `gapfill_policy_eval_scheme`，独立脚本灌入方案对照、参数模拟结果、路径节点与风险、专家意见条目，不灌导出文件，不改 D4，不新造 `metric_id`。本分册把「专家意见条目」收成 `row_kind=互动意见`。不另建意见表。执行时列按第 2 节，行按第 3 至第 6 节，231 按第 7 节不灌。

灌数单要灌的最少内容，沿架构第 9 节，本单仍不执行：

| 种类 | 灌数单以后要灌 | 不灌 |
|---|---|---|
| 方案对照 | 至少两个方案。每个有名称、一句说明、对照维度和数值、优劣结论、实施建议 | 布局建议条数、演示分、demo 那三条常量的原文 |
| 参数模拟 | 每个方案至少一行。含参数档、评估结果、一句趋势、一条归档说明 | 省级力度情景、弹性公式现算、采纳时新插入的行 |
| 路径与风险 | 每个方案若干节点。含节点、时间进度、一句说明、风险标题和一句风险。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 推演曲线、子图、用户改期 |
| 互动意见 | 挂到方案上的若干条。含主体、分类（评价、评论、建议）、意见正文、时间 | 页面当场提交的新意见、序号 210 的问卷 |
| 231 | 不灌 | PDF、Word、Excel、对象存储、核增研报 |

四种业务行都带第 2 节的 D16 列，`fill_method=manual`，`is_mock=1`。其余三种的 `metric_id` 留空。

查询请求不调用这张灌数单。空表返回空。本单不写示例行。

## 9. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `ads.policy_simulate`、`M_POLICY_SIMULATE`、`polan.text.simulate.run` | 推演键。省级力度情景不灌进本表。228、229 不改挂这条指标 |
| `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` | 布局推荐键。不写入方案对照行 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 只出现在路径与风险行。不改 D4。不挂到另外三种行。不为此读图 |
| `evaluation/counts` | 短板条数、机遇条数。本表不读、不写 |
| 219–222 | 趋势、分区、结构关联、报告模板。不读本表 |
| 223–226 | 焦点、短板、解读、多媒体、摘要。读面在解读分册。不读本表，不把壳表行复制进来 |
| `gapfill_policy_eval_shell` | 解读二级的壳表。与本表不是同一张，列不混用 |
| `gapfill_policy_audience_feedback` | 序号 210 的受众反馈。不复制进互动意见行 |
| 序号 241 | 推演页的实施路径预测。不顶替 229 |
| `report/jobs` | 核增研报。不是 231，不写入本表 |
| `panorama/jobs` | 全景的效果、匹配、力度。不是评价页方案 |
| `GDF-POLICY-MOCK-GATE-L01` | 仍是 blocked。本单不把它写成已解开 |

## 10. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑推演函数。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不写供应方库。
- 不把本表拆成四张。不把 231 建成第五种行或文件表。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。
- 不把推演情景、弹性曲线、`ads.policy_simulate` 的行灌进本表。
- 不灌 PDF、Word、Excel，不写对象存储，不设文件列。
- 不把页面上新打的意见、采纳动作、改期写回本表。
- 查询不插入。列清单不是可执行 SQL。
- 不改说明书、WBS、`指标与501.md`、解读分册、架构稿、注册表里的灌数单。
- 不认领 `POL-L2-DS11-PLAN-GAPFILL-L01`。
- 不把本单标成 done 或 ready_to_sign。
