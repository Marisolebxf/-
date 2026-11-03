# POL-L2-DS11-PLAN-API · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计

- 任务：`POL-L2-DS11-PLAN-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（2026-11-03 架构、算法、数据、产品四角色同意。待 `human:淮政玮` 签收。本分册以它为准，不改它）

本分册只定政策分析评价二级「推荐方案报告交互展示」的后台接口。SRS 序号 **227–231**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-PLAN-ARCH` 为准。契约输入清单里评价页已经点名的 `evaluation/jobs` 与 `evaluation/shells` 只作资源名对照。清单、`指标与501.md`、说明书、WBS、调研里仍写的 501 空态不覆盖本分册。

签收口径：五叶都读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。227–229 各一次 `jobs`，230–231 各一次 `shells`。231 不单独占行种类，导出从当次读到的方案对照行和互动意见行生成。不允许接口直接返回 mock，也不用 501 充当功能。无行则空。

## 偏离

三处与上游 DoD 或仍在架上的旧空态字面不一致。本分册写明，不回头改那些文件。

1. DoD「不复用 `/topic/v1/policy`」在本二级是：浏览器只打 `/display/v1/policy/**`，227–231 的内部委托也不打专题政策 URL，不调用 `POST /topic/v1/analysis/tasks`，不进 `gkxlumen-topic-async-service`。焦点、摘要仍由解读分册走那条内部委托。本分册不把方案五叶写成那条链，也不改解读分册。
2. DoD 完成标准里的「501 空态」，以及 `指标与501.md` 仍把 227–231 写成 501、页面空态。契约输入清单把整条 `evaluation/jobs` 标成 Job，并把多方案、参数模拟、实施路径与风险的空态写在这一条 Job 上。2026-11-03 架构把这五叶改成读 `gapfill_policy_eval_scheme`：227–229 同步，不建任务。本分册按该架构写。空态是空，HTTP 成功，不返回 501。不改 `指标与501.md`、说明书、WBS、调研、契约输入清单，也不改同目录的 VIZ、READ。
3. 不把整条 `jobs` 或整条 `shells` 改成只读方案表。趋势、分区、模板选用留给可视化分册。焦点、摘要留给解读分册。本分册只给 227–231 按种类分发。

## 1. 公开资源

前缀 `/display/v1/policy/`。五叶都在政策分析评价的推荐方案工作区里完成，不另开页，不另开路径。本二级对外只有下面两条，且一次请求只带一种类。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 227 方案对照 | `POST /display/v1/policy/evaluation/jobs` | 同步。种类为方案对照。element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的方案对照行。少于两行则对比空。不建任务。不返回 501 |
| 228 参数模拟 | 同一条 `POST /display/v1/policy/evaluation/jobs` | 同步。种类为参数模拟。同一张表按方案和参数档拣行。对不上则预览空。请求内不重算。不返回 501 |
| 229 路径与风险 | 同一条 `POST /display/v1/policy/evaluation/jobs` | 同步。种类为路径与风险。同一张表按方案拣路径节点和风险。不读图。不返回 501 |
| 230 互动意见 | `GET /display/v1/policy/evaluation/shells` | 同步。种类为互动意见。同一张表按方案拣意见行。请求不插入。不读壳表，不读模板表。不返回 501 |
| 231 方案报告 | 同一条 `GET /display/v1/policy/evaluation/shells` | 同步。种类为方案报告。同一次读取方案对照行和意见行，从这些行生成导出内容。不灌文件，不写对象存储。不读壳表，不读模板表。不返回 501 |

`evaluation/jobs`、`evaluation/shells` 上还有别的二级。本分册不改写那些种类，也不把查方案表的读法套到它们身上。

| 留给谁 | 种类 | 本分册不改的读法 |
|---|---|---|
| 可视化 | `jobs` 的趋势、分区 | 各一次请求。趋势读 `gapfill_policy_eval_trend`，分区读 `gapfill_policy_eval_partition`。都不进异步 |
| 可视化 | `shells` 的模板选用 | 读 `gapfill_policy_eval_template`。不读壳表 |
| 解读 | `jobs` 的焦点、摘要 | 异步键只有 `policy_focus_ads`、`policy_text_parse`。焦点读 `ads.policy_focus`，摘要读 `ads.policy_text_parse.summary` |
| 解读 | `shells` 的解读条目、多媒体条目 | 读 `gapfill_policy_eval_shell` |

效能得分不在这五叶。`evaluation/counts` 上的短板条数、机遇条数不在本二级。本分册不读、不改。

`PolicyAnalysisTypes` 现有白名单是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`。本分册不加 `policy_scheme`，也不把 227–231 塞进其中任何一项。这五叶不进 `POST /internal/policy/jobs/execute`。

种类字段名由 `BE-POL-CONTRACT-01` 冻结。本分册只定种类的中文名和一次一种类。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。不调用任何 `demo-*` 服务。Java 不生成方案，不按弹性公式现算，不拼路径，不插入意见，不拼写死的文件。

| 公开资源 | 内部委托 |
|---|---|
| `jobs` 的方案对照、参数模拟、路径与风险 | `gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 里该次种类的行 |
| `shells` 的互动意见、方案报告 | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读同一张方案表。230 只读互动意见行，请求不写库。231 读方案对照行和互动意见行，导出内容从这些行生成。不读 `gapfill_policy_eval_shell`，不读 `gapfill_policy_eval_template` |

若 `gkxlumen-display` 还没有评价控制器，实现时按契约补 `evaluation/jobs` 与 `evaluation/shells`。补上之后仍按种类分发。不能把整条 `jobs` 或整条 `shells` 都改成只读这张方案缺项表。本分册不补控制器，不写 Java。

五叶都不进异步任务管道。切条件、切参数不自动起任务。某一次 `jobs` 或 `shells` 失败，不清空 `evaluation/counts` 已经返回的短板条数和机遇条数，也不清空其他种类已经返回的区块。

trace 沿既有展示链。display 往 element 带 traceId。本分册不新设计观测点。

表只有四种行种类：方案对照、参数模拟、路径与风险、互动意见。231 不单独占种类。字段级 DDL 由 `POL-L2-DS11-PLAN-DATA` 定。灌数由 `POL-L2-DS11-PLAN-GAPFILL-L01` 执行。二者都不在本分册。查询请求不灌数。库只允许 `gkxlumenx_gapfill`。不进 ODS、DWD、ADS，不写供应方库。

每行都带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，以架构第 9 节为准。路径与风险行的 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。其余三种没有已挂指标，`metric_id` 留空，不新注册。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把 mock 写成已上线，不改 D4。

## 3. 227 多方案对比展示 · jobs · 方案对照

公开资源：`POST /display/v1/policy/evaluation/jobs`。浏览器提交这一次，种类为方案对照。没有方案生成模型。不挂 `M_POLICY_LAYOUT_REC_COUNT`。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的方案对照行。

- 同步。不建任务。不进 `PolicyAnalysisTypes`。不加 `policy_scheme`
- 一行是一个方案：名称、一句说明、若干对照维度和数值、优劣结论、实施建议。雷达和 KPI 的数就是这些行上的对照值
- 用户可以不选方案。不选则读出全部方案对照行。选了则只返回对得上的行
- 表里少于两行则对比空。不造第二个方案。Java 不补演示分
- 需规写的是并排图表上筛选。不把展示原型里优劣、风险、ROI 三个下拉写成闭集
- 不迁 `policyData.js` 的 `recommendationSchemes`

空态：少于两行，或所选方案对不上行，则对比空。HTTP 成功。不返回 501。不在接口函数里返回写死的方案或分数。

## 4. 228 方案参数自定义模拟 · jobs · 参数模拟

公开资源与 227 相同：`POST /display/v1/policy/evaluation/jobs`。浏览器另一次提交，种类为参数模拟。一次请求不带方案对照，也不带路径与风险。

没有方案参数模型。`polan.text.simulate.run` 写的是省级力度情景，指标是 `M_POLICY_SIMULATE`，表是 `ads.policy_simulate`。本分册不调用这个函数，不读这张表，不把 228 改挂到推演键。

链路与第 3 节相同，element 只读同一张方案表里的参数模拟行。

- 方案必选。少了方案则该块空，不补一套默认方案
- 一行挂在一个方案上：参数档、评估结果、一句趋势、一条归档说明
- 用户换参数，就是换一次查询。参数档对得上的行原样返回。对不上则预览和趋势空
- 不在 Java 或 Python 里按弹性公式现算。请求内不重算
- 采纳不插入新行。归档只来自已经灌入的行
- 切参数不自动起任务

空态：方案未选，或参数档对不上行，则预览空、趋势空。HTTP 成功。不返回 501。不返回推演曲线来顶替。不在接口函数里返回写死的评估结果。

## 5. 229 实施路径与风险辅助 · jobs · 路径与风险

公开资源仍是 `POST /display/v1/policy/evaluation/jobs`。浏览器另一次提交，种类为路径与风险。

指标 `M_POLICY_DS_11_POLICY_EVAL_015`，GRAPH，D4=mock。口径是路径与风险的生成结果，不是第 7 项在线读图。现有函数不产出这条指标。行上的 `metric_id` 用这一条。不新注册，不改 D4，不把读到的行写成已上线。

链路与第 3 节相同，element 只读同一张方案表里的路径与风险行。

- 方案必选。少了方案则路径和风险都空
- 一行挂在一个方案上：节点名称、时间进度、一句节点说明、风险标题、一句风险说明。一个方案可以有多行
- 不写 nGQL，不读政策子图。不进第 7 项读图
- 时间进度在路径行里。本分册不接收改期回写
- 不返回 `polan.text.simulate` 的曲线来顶替。`M_POLICY_SIMULATE` 不写进这些行
- 序号 241 的政策实施路径预测在推演页，不顶替本叶

空态：该方案没有路径行则路径和风险都空。HTTP 成功。不返回 501。不在接口函数里返回写死的节点或风险。

## 6. 230 互动意见收集与专家参与 · shells · 互动意见

公开资源：`GET /display/v1/policy/evaluation/shells`。浏览器调这一次，种类为互动意见。

没有意见采集服务，也没有意见指标。调研把它记为交互壳。按架构，交互壳同样读缺项表，不用 501 充当这块功能。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 同一张 `gapfill_policy_eval_scheme` 的互动意见行。

- 同步。不建任务
- 不读 `gapfill_policy_eval_shell`。那张壳表只服务解读的 224、225
- 不读 `gapfill_policy_eval_template`。那张模板表只服务可视化的 222
- 一行挂在一个方案上：主体、分类、意见正文、时间。分类只用评价、评论、建议，写在行上。分类的字段名由契约单冻结
- 用户不选方案则意见列表空。选了则按方案拣行
- 请求处理不插入、不更新、不删除。页面上新打的评价留在浏览器，直到另有采集单。本分册不建那张单
- 不把序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成方案意见

空态：未选方案，或该方案没有意见行，则列表空。HTTP 成功。不造一条专家意见。不返回 501。不在接口函数里返回写死的评论。

## 7. 231 方案报告导出与归档 · shells · 方案报告

公开资源与 230 相同：`GET /display/v1/policy/evaluation/shells`。浏览器另一次调用，种类为方案报告。一次请求不带互动意见种类，也不带模板选用。

没有方案报告模型和导出 Job。核增研报 `report/jobs`（614–618）和评价页序号 222 的分析报告模板不是这条资源。

- 同步。不建任务。不另建报告行，不另建文件表
- 不读壳表，不读模板表
- 这一次读取方案对照行（名称、说明、优劣结论、实施建议、对照值）和互动意见行。两种行都在 `gapfill_policy_eval_scheme`。231 自己不占行种类
- 有方案对照行则导出内容从当次读到的这些行生成。没有方案对照行则导出空
- 不灌文件。响应里不内嵌一份写死的 PDF、Word 或 Excel。不写对象存储，不新建桶，前端不直连 RustFS
- 导出格式名由 `BE-POL-CONTRACT-01` 冻结。本分册不写字段表，不把格式写成实现代码

空态：没有方案对照行则导出空。HTTP 成功。不返回 501。不返回一份写死的文件。

## 8. 空态对照

五叶的签收读法都是查方案缺项表，或从该表当次读到的行生成。无行则空。不用 501 充当功能。接口不直接返回写死的 mock。mock 若存在，只能先由灌数单落入表，再被查询读出来。查询不灌数。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 227 | jobs · 方案对照 | 方案对照行少于两行，或所选方案对不上，则对比空。不造第二个方案。不返回 501。失败不清空 counts 和其他种类 |
| 228 | jobs · 参数模拟 | 未选方案，或参数档对不上行，则预览和趋势空。不现算。不返回 501。失败不清空 counts 和其他种类 |
| 229 | jobs · 路径与风险 | 未选方案，或该方案没有路径行，则路径和风险都空。不读图，不返回推演曲线。不返回 501 |
| 230 | shells · 互动意见 | 未选方案，或没有意见行，则列表空。请求不插入。不读壳表，不读模板表。不返回 501 |
| 231 | shells · 方案报告 | 没有方案对照行则导出空。不灌文件，不写对象存储。不读壳表，不读模板表。不返回 501 |

## 9. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不补评价控制器。
- 不改 `POL-L2-DS11-PLAN-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研分册、VIZ、READ 和任何兄弟分册。
- 不把整条 `jobs` 或整条 `shells` 改成只读 `gapfill_policy_eval_scheme`。
- 趋势、分区、模板选用留给可视化。焦点、摘要、解读条目、多媒体条目留给解读。效能得分、`evaluation/counts` 不在本分册改读法。
- 不加 `policy_scheme`。不把 227–231 写入 `PolicyAnalysisTypes`。五叶不进 `POST /internal/policy/jobs/execute`，不进 `gkxlumen-topic-async-service`。
- 浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 展示不直连 Python，不直连库，不打算法中台。不调用 `demo-*`。不调用 `polan.text.simulate`。不读 `ads.policy_simulate`。
- 不用 501 充当 227–231 的功能。无行则空。对比少于两行不补方案。短板条数和机遇条数不随本二级变空。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不改模型注册表。
- 不读 `gapfill_policy_eval_shell`、`gapfill_policy_eval_template`、`gapfill_policy_audience_feedback`。不读趋势表、分区表。
- 请求不插入、不更新、不删除意见。采纳不写库。不接收路径改期回写。查询不灌数。
- 不返回写死的 PDF、Word、Excel。不新建桶，不写对象存储，前端不直连 RustFS。231 不灌文件。
- 不纳入本分册：219–222、223–226、序号 241、`report/jobs`、`panorama/jobs`、`M_POLICY_SIMULATE`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`。
- 不改 `FE-POL-02A`，不新建前端单。前端 mock 开关不是接口实现。
- 不会签。不把本单标 done，不标 ready_to_sign。
