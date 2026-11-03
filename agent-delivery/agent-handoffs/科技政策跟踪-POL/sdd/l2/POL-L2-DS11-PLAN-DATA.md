# POL-L2-DS11-PLAN-DATA · 政策分析评价 · 推荐方案报告交互展示 · 数据落点

- 任务：`POL-L2-DS11-PLAN-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（已认领，状态 `in_progress`，本单不改状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 会签态：未会签。本叶不代签，不标 done
- 上游架构：`POL-L2-DS11-PLAN-ARCH`（真源，第 5 节和第 9 节）。本单只写数据落点，不改那份架构，不改图。

本叶只定政策分析评价二级「推荐方案报告交互展示」的数据落点。SRS 序号 **227–231**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL，本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md` 第 3、5、9 节，说明书第 11.2 节「评价 · 方案 227–231」那一行。不新造 `metric_id`，不改 D4，不改 `M_POLICY_DS_11_POLICY_EVAL_015`。

## 1. 范围

五叶都在评价页的推荐方案工作区里完成。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python。查询只读表。查询请求不灌数。表里没有对得上的行就返回空。接口不直接返回写死的 mock。

新建表只有一张：

| 表 | 库 | 灌数方 | 读取方 |
|---|---|---|---|
| `gapfill_policy_eval_scheme` | `gkxlumenx_gapfill` | `POL-L2-DS11-PLAN-GAPFILL-L01` | `gkxlumen-element` |

不拆成四张表。不写 ODS、DWD、ADS 新表，不加已有 ADS 列，不写供应方库。231 不另建报告表，不另建文件表。

这张表只服务功能验收。生产配置不读 `gkxlumenx_gapfill`。行上带 D16 规定列。表里有行也不把 D4 改成 live。`GDF-POLICY-MOCK-GATE-L01` 仍未解开。

| 序号 | 叶子 | 表中的行 | 本单 |
|---|---|---|---|
| 227 | 多方案对比展示 | `row_kind=方案对照` | 定逻辑列。至少灌两个方案 |
| 228 | 方案参数自定义模拟 | `row_kind=参数模拟` | 按方案和参数档拣行。采纳不插入 |
| 229 | 实施路径与风险辅助 | `row_kind=路径与风险` | `metric_id` 只用已有 `M_POLICY_DS_11_POLICY_EVAL_015` |
| 230 | 互动意见收集与专家参与 | `row_kind=互动意见` | 可灌已定意见行。意见请求不插入新行 |
| 231 | 方案报告导出与归档 | 不另建行 | 不灌导出文件。读方案对照行和意见行 |

## 2. 已有 ADS 与已落库结果

本二级不读已有 ADS，也没有可复用的已落库方案结果。五叶的数只来自第 3 节这一张缺项表。

| 已有对象 | 本单 |
|---|---|
| `ads.policy_simulate`、`M_POLICY_SIMULATE`、`polan.text.simulate` | 推演键。228、229 不读、不写、不把该 `metric_id` 放进缺项行 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 已注册。架构写明 D4 为 mock。只出现在路径与风险行的 `metric_id`。本单不改这条指标，不改 D4，不读政策子图 |
| `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` | 布局推荐键。不写入方案对照行 |
| `evaluation/counts` | 短板条数、机遇条数。不进本表，本单不读、不改 |
| `gapfill_policy_audience_feedback` | 序号 210 的受众反馈。不是方案意见 |

某一次 `jobs` 或 `shells` 失败，不清空 `evaluation/counts` 已经返回的短板条数和机遇条数。

## 3. 共用表

库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`。一行只属于一种 `row_kind`。种类只有四种：方案对照、参数模拟、路径与风险、互动意见。231 不占种类。

`scheme_name` 是方案名。方案对照行里各个 `scheme_name` 互不相同。参数模拟、路径与风险、互动意见用同一个 `scheme_name` 挂到该方案上。不另造 `scheme_id`，不建外键。

拣行键：

| 序号 | 拣行键 | 对不上时 |
|---|---|---|
| 227 | `scheme_name`。不选方案则读出全部方案对照行 | 读出的方案对照行少于两行则对比空 |
| 228 | `scheme_name` + `param_band`。方案必选 | 参数档对不上则预览、趋势、归档都空 |
| 229 | `scheme_name`。方案必选。一个方案可以多行 | 该方案没有路径与风险行则路径和风险都空 |
| 230 | `scheme_name`。不选方案则列表空 | 该方案没有意见行则列表空 |
| 231 | 不单独拣种类。按当次方案读方案对照行，再读这些 `scheme_name` 上的互动意见行。没带方案则读全部方案对照行，并读这些方案上的意见行 | 没有方案对照行则导出空。意见行可以没有，点评那一块空 |

条件对不上的行不返回。查询不插入、不更新、不删除。

灌数方：`POL-L2-DS11-PLAN-GAPFILL-L01`（`data-agent`，监管 `human:淮政玮`）。读取方：`gkxlumen-element`，经 `gkxlumen-display` 原样返回。display 不直连库。

| 序号 | 读取资源 |
|---|---|
| 227、228、229 | `POST /display/v1/policy/evaluation/jobs`。按种类只读本表对应行 |
| 230、231 | `GET /display/v1/policy/evaluation/shells`。230 只读互动意见行。231 读方案对照行和互动意见行 |

同一条 `jobs`、同一条 `shells` 上的其他种类不改挂到本表。参数名留给 `POL-L2-DS11-PLAN-API`。本单不写请求体、响应体。

下列是逻辑列，不是可执行 DDL。建表由灌数单落地。本单不执行。不适用本种类的列留空（NULL），不填占位字。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `row_kind` | varchar(16) | 否 | `方案对照`、`参数模拟`、`路径与风险`、`互动意见` 四者之一 |
| `scheme_name` | varchar(128) | 否 | 方案名。全部种类的拣行键。方案对照行上互不相同 |
| `scheme_brief` | text | 是 | 一句说明。方案对照行必填 |
| `compare_dims` | text | 是 | 对照维度和数值。方案对照行必填。同一格内分行，一行一个「维度名：数值」。数值是对照值。不另建维度子表 |
| `pros_cons_text` | text | 是 | 优劣结论。方案对照行必填 |
| `suggestion_text` | text | 是 | 实施建议。方案对照行必填 |
| `param_band` | varchar(128) | 是 | 参数档。参数模拟行必填，并与 `scheme_name` 一起拣行。不拆成资金、人才、平台三列，也不把这三词写成闭集 |
| `eval_result` | text | 是 | 评估结果。参数模拟行必填 |
| `trend_text` | text | 是 | 一句趋势。参数模拟行必填 |
| `archive_note` | text | 是 | 一条归档说明。参数模拟行必填。归档来自已灌行。采纳不插入新行 |
| `node_name` | varchar(128) | 是 | 节点名称。路径与风险行必填 |
| `time_progress` | varchar(64) | 是 | 时间进度。路径与风险行必填。不接收改期回写 |
| `node_note` | text | 是 | 一句节点说明。路径与风险行必填 |
| `risk_title` | varchar(128) | 是 | 风险标题。路径与风险行必填 |
| `risk_note` | text | 是 | 一句风险说明。路径与风险行必填 |
| `opinion_subject` | varchar(128) | 是 | 主体。互动意见行必填 |
| `opinion_class` | varchar(16) | 是 | `评价`、`评论`、`建议` 三者之一。互动意见行必填 |
| `opinion_text` | text | 是 | 意见正文。互动意见行必填 |
| `opinion_at` | datetime | 是 | 意见时间。互动意见行必填 |
| `is_mock` | tinyint | 否 | 每行必须为 1 |
| `metric_id` | varchar(64) | 是 | 路径与风险行固定 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种留空。不新注册，不改这条已有指标 |
| `gap_item` | varchar(128) | 否 | 按种类固定，见下表 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间 |

`fill_method` 固定 `manual`。D16 只在方法为 `llm` 时要求 `fill_model`。本表不设 `fill_model`。

| `row_kind` | `gap_item` |
|---|---|
| 方案对照 | `227 多方案对比展示` |
| 参数模拟 | `228 方案参数自定义模拟` |
| 路径与风险 | `229 实施路径与风险辅助` |
| 互动意见 | `230 互动意见收集与专家参与` |

不设文件列、对象键、版本号。不设 `M_POLICY_SIMULATE`。

同一方案、同一参数档的参数模拟只留一行。路径与风险、互动意见在同一方案上可以多行，用 `id` 区分，不把节点名或意见正文写成唯一约束。

## 4. 227 多方案对比展示

一行是一个方案：名称、一句说明、若干对照维度和数值、优劣结论、实施建议。雷达和 KPI 的数就是 `compare_dims` 里的对照值。Java 不生成方案，不补演示分。

灌数单灌方案对照行，至少两个方案。不灌布局建议条数，不灌演示分，不把展示原型 `recommendationSchemes` 那三条常量的原文写入本表。

读取方：`gkxlumen-element`，`jobs` 的方案对照。少于两行则对比空，不造第二个方案。

## 5. 228 方案参数自定义模拟

一行挂在一个方案上：参数档、评估结果、一句趋势、一条归档说明。用户换参数就是换一次查询。对得上的行原样返回。请求内不按弹性公式现算，不调用 `polan.text.simulate`。

灌数单灌参数模拟行，每个方案至少一行。不灌省级力度情景，不灌弹性公式现算的结果，不在采纳时插入新行。

读取方：`gkxlumen-element`，`jobs` 的参数模拟。方案未给，或参数档对不上，则该块空。

## 6. 229 实施路径与风险辅助

一行挂在一个方案上：节点名称、时间进度、一句节点说明、风险标题、一句风险说明。一个方案可以有多行。

`metric_id` 使用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不新注册，不改该指标，不改 D4，不把读到的行写成已上线。不写 nGQL，不读政策子图。不返回推演曲线来顶替。

灌数单灌路径与风险行，每个方案若干节点。不灌推演曲线，不灌子图，不灌用户改期。

读取方：`gkxlumen-element`，`jobs` 的路径与风险。无行则路径和风险都空。

## 7. 230 互动意见收集与专家参与

一行挂在一个方案上：主体、分类、意见正文、时间。分类只用评价、评论、建议。

没有意见指标。`metric_id` 留空，不新注册。不读 `gapfill_policy_audience_feedback`。

灌数单可灌已定的意见行。意见请求不插入、不更新、不删除。页面上新打的评价留在浏览器，直到另有采集单。本单不建那张单。

读取方：`gkxlumen-element`，`shells` 的互动意见。不选方案，或该方案无行，则列表空，不造一条专家意见。

## 8. 231 方案报告导出与归档

不另建行，不占 `row_kind`，不建文件表。

读取方：`gkxlumen-element`，`shells` 的方案报告。读当次范围的方案对照行（名称、说明、优劣结论、实施建议、对照值）和这些方案上的互动意见行。导出若要文件，从这次读到的行生成。响应里不内嵌写死的 PDF 或 Word。文件字节不进 MySQL，不进对象存储。

灌数单不灌导出文件。不灌 PDF、Word、Excel，不写对象存储，不写核增研报 `report/jobs`。没有方案对照行则导出空。意见行没有时，专家点评那一块空，不因此插入一条意见。

## 9. 灌数单

只点名，本单不执行，不建库，不插入行。

| 灌数单 | 灌什么 | 不灌什么 |
|---|---|---|
| `POL-L2-DS11-PLAN-GAPFILL-L01` | 方案对照行、参数模拟行、路径与风险行、已定意见行。执行人 `data-agent`，监管 `human:淮政玮`。依赖本架构和本数据叶 | 231 的导出文件。意见请求产生的新行。ODS、DWD、ADS、供应方库。省级力度情景、推演曲线、子图、布局建议条数、演示分、demo 三条常量原文、序号 210 的问卷 |

查询请求不调用这张灌数单。空表或对不上的行返回空。

## 10. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| 219–222 | 趋势、分区、结构关联、报告模板。可视化二级。本表不读 |
| 223–226 | 焦点、短板、解读、多媒体、摘要。解读二级。本表不读 |
| `evaluation/counts` | 短板条数、机遇条数。本表不读、不改 |
| `M_POLICY_SIMULATE`、`ads.policy_simulate`、`polan.text.simulate` | 推演键。228、229 不迁 |
| `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` | 布局推荐键。不写入方案对照 |
| 序号 241 | 推演页的实施路径预测。不顶替 229 |
| `report/jobs`（614–618） | 核增研报。不是 231 |
| `panorama/jobs` | 全景的效果、匹配、力度。不是评价页方案 |
| `gapfill_policy_audience_feedback` | 序号 210。不是方案意见 |

## 11. 明确不做

- 不写可执行 SQL，不建库，不灌数。
- 不重开 GDF，不写 nGQL。
- 新表只有 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不写 ODS、DWD、ADS、供应方库。
- 不新造 `metric_id`，不改 D4，不改 `M_POLICY_DS_11_POLICY_EVAL_015`，不把缺项行写成已上线。
- 不把 231 写成第五种行，不灌导出文件。
- 意见请求不插入、不更新、不删除。
- 不在接口里直接返回写死的方案、分数、路径、意见或文件。
- 不改架构稿、说明书、WBS、`POL-L2-DS11-READ-DATA.md`、`POL-L2-DS11-VIZ-DATA.md`、`task-registry.yaml`。
- 不把本单标成 done。会签态记未会签。
