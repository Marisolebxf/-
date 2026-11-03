# POL-L2-DS11-PLAN-API · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计

- 任务：`POL-L2-DS11-PLAN-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（本单派令：已签收）。会签对照 `sdd/l2/会签/POL-L2-DS11-PLAN-SIGNOFF-ARCH.md`。本分册以这两份为准，不改它们

本分册只定政策分析评价二级「推荐方案报告交互展示」的后台接口。SRS 序号 **227–231**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名、格式名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-PLAN-ARCH` 为准。契约输入清单里评价页的 `evaluation/jobs`、`evaluation/shells` 只作资源名对照。清单把 `jobs` 整条写成 Job，并把多方案、参数模拟、实施路径、互动意见、方案归档的空态写在「501 时页面空态」列。清单里的 Job 和 501 不覆盖本分册。本分册不改那份清单。

签收口径：做不到的只允许缺项表灌 mock 后由接口读表。五叶只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。不允许接口直接返回写死的方案、分数、路径、意见或文件，也不用 501 充当这五叶的画面。

指标分册 `POL-L2-DS11-PLAN-METRIC` 把五叶的三档判定保持为 501。那是指标身份。本分册不改它，也不改 `指标与501.md`。三档 501 不覆盖接口返回：这五叶 HTTP 成功，对不上或无行则该块空，不返回 501。

## 偏离

调用链第 3 节仍把方案对比、参数模拟、实施路径写在 Job，并写「模型未注册则 501」。本分册按已签收架构改走缺项表只读。资源名仍用已有 `jobs` / `shells`，不建任务行。本分册不改写调用链文件。

本二级 DoD 里「不复用 `/topic/v1/policy`」指浏览器不改打专题政策 URL。这五叶也不提交 `gkxlumen-topic-async-service`。浏览器仍只打 `/display/v1/policy/**`。对外不把 `/topic/v1/policy`、`/v1/policy/**` 或 `/topicAsync/**` 写成入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。

## 1. 公开资源

前缀 `/display/v1/policy/`。五叶都在政策分析评价的推荐方案工作区里完成，不另开页，不另开路径。本分册不新开资源。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 227 | `POST /display/v1/policy/evaluation/jobs` | 同步。不是 Job。种类为方案对照。element 只读 `gapfill_policy_eval_scheme` 的方案对照行。请求内不重算。对不上或少于两行则对比空 |
| 228 | 同一条 `POST /display/v1/policy/evaluation/jobs` | 同步。不是 Job。种类为参数模拟。同一张表按方案和参数档拣行。请求内不重算。对不上则该块空 |
| 229 | 同一条 `POST /display/v1/policy/evaluation/jobs` | 同步。不是 Job。种类为路径与风险。同一张表按方案拣路径节点和风险。请求内不重算。对不上则该块空 |
| 230 | `GET /display/v1/policy/evaluation/shells` | 同步。不是 Job。种类为互动意见。只读同一张表的意见行。请求不插入新意见。无行则列表空 |
| 231 | 同一条 `GET /display/v1/policy/evaluation/shells` | 同步。不是 Job。读法为方案报告，不单独占表种类。只读同一张表的正文行和意见行。从当次读到的行生成文件。不灌导出文件。没有正文行则导出空 |

正文行就是方案对照行：名称、一句说明、对照维度和数值、优劣结论、实施建议。230、231 只读意见行和正文行，不读参数模拟行，不读路径与风险行。

`evaluation/jobs`、`evaluation/shells` 在契约输入清单里还挂着其它叶子。本分册只定上表这些读法。不能把整条 `jobs` 或整条 `shells` 都改成只读这张缺项表。

序号 219–226 不进本分册。`evaluation/counts` 上的短板条数、机遇条数不在这里重写。同一条 `jobs` 上的焦点、效能得分、摘要、趋势、分区、解读，同一条 `shells` 上的模板选用、多媒体、分析报告份数，都不是这五叶。

用户提交时要区分的种类只有四种：方案对照、参数模拟、路径与风险、互动意见。231 的读法叫方案报告，不另占一种类。种类的参数名、枚举字面量和导出格式名留给 `BE-POL-CONTRACT-01`。本分册不冻结这些名字，不冻结第二份 API-POL。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。

`gkxlumen-display` 不直连 Python，不直连库，不写算法，不算指数，不写 nGQL。不打算法中台 `/v1/policy/**`。不调用任何 `demo-*` 服务。不嵌中台页。不调用 `polan.text.simulate`。不调用 `POST /internal/analysis/policy/simulate`。

| 公开资源 | 内部委托 |
|---|---|
| `evaluation/jobs`（本分册只定 227–229） | `gkxlumen-display` 不直连库，不提交异步任务。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。227 取方案对照行，228 按方案和参数档取参数模拟行，229 按方案取路径与风险行。请求内不重算。对不上则该块空 |
| `evaluation/shells`（本分册只定 230–231） | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读同一张表的意见行和正文行。230 取意见行。231 取正文行和意见行，从当次读到的行生成文件。不灌导出文件。请求不插入新意见 |

五叶都不进 `gkxlumen-topic-async-service`，不建任务行，不走 SSE，不加 `policy_scheme`。`PolicyAnalysisTypes` 现有白名单是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`。本分册不把方案五叶塞进其中任何一项，也不改白名单代码。

`gkxlumen-display` 若还没有评价控制器，实现时按契约补 `evaluation/jobs` 与 `evaluation/shells`。补上之后，本二级的种类仍由 element 读缺项表。路径虽叫 `jobs`，227–229 仍是同步读，不是 Job。

切条件不自动起任务。这五叶本来就不建任务。用户换参数是再提交一次 `jobs`，仍是同步查表。某一块读失败，不清空 `evaluation/counts` 已经返回的短板条数和机遇条数，也不清空其他种类已经返回的区块。

trace 沿既有展示链。display 往 element 带 traceId。本分册不新设计观测点。

## 3. 227 多方案对比展示 · jobs

公开资源：`POST /display/v1/policy/evaluation/jobs`。同步。不是 Job。种类为方案对照。

没有方案生成模型。没有专属已挂指标。不挂 `M_POLICY_LAYOUT_REC_COUNT`。不新造 `metric_id`。

`gkxlumen-display` 不直连库，不直连 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 里的方案对照行。雷达和 KPI 的数就是这些行上的对照值。

不选方案则读出全部方案对照行。条件对不上的行不返回。剩下少于两行则对比空，不造第二个方案，不补演示分。对不上则该块空。请求内不重算。Java 不生成方案。HTTP 成功。不返回 501。查询函数自己不拼对照值。

不调用 `polan.text.simulate`。不把展示原型 `policyData.js` 的三条常量迁进接口。

灌数是独立脚本（`POL-L2-DS11-PLAN-GAPFILL-L01`），不是请求处理。本分册不写 DDL，不执行灌数。列由 `POL-L2-DS11-PLAN-DATA` 定。

## 4. 228 方案参数自定义模拟 · jobs

公开资源仍是 `POST /display/v1/policy/evaluation/jobs`。同步。不是 Job。种类为参数模拟。与 227 同一条路径。

没有方案参数模型。`polan.text.simulate.run` 写的是省级力度情景，指标是 `M_POLICY_SIMULATE`，表是 `ads.policy_simulate`。本序号不挂这条推演指标，不读那张表，不调用 `polan.text.simulate`。

同一张 `gapfill_policy_eval_scheme`。一行挂在一个方案上：参数档、评估结果、一句趋势、一条归档说明。用户换参数就是再查一次。对得上的行原样返回。对不上则该块空，预览和趋势都空。请求内不按弹性公式现算。Java 不算，这次请求里的 Python 也不算。

方案必选。少了必选条件则该块空，不补一套默认方案。采纳不插入新行。归档只来自已经灌入的行。

HTTP 成功。不返回 501。不返回写死的评估结果。

## 5. 229 实施路径与风险辅助 · jobs

公开资源仍是 `POST /display/v1/policy/evaluation/jobs`。同步。不是 Job。种类为路径与风险。

指标 `M_POLICY_DS_11_POLICY_EVAL_015`，GRAPH，D4=mock。口径是路径与风险的生成结果，不是在线读图。现有函数不产出这条指标。行上的 `metric_id` 用已有这一条。不新注册，不改 D4，不把读到的行写成已上线。

同一张表。一行挂在一个方案上：节点名称、时间进度、一句节点说明、风险标题、一句风险说明。一个方案可以有多行。

方案必选。该方案没有路径行，或条件对不上，则路径和风险都空。请求内不重算。不返回推演曲线来顶替。不写 nGQL，不读政策子图。不接收改期回写。不调用 `polan.text.simulate`。

`M_POLICY_SIMULATE` 不写进这些行。序号 241 的政策实施路径预测在推演页，不顶替本序号。

HTTP 成功。不返回 501。查询函数自己不拼节点。

## 6. 230 互动意见收集与专家参与 · shells

公开资源：`GET /display/v1/policy/evaluation/shells`。同步。不是 Job。种类为互动意见。与 231 同一条。

没有意见采集服务，也没有意见指标。按签收标准，交互壳同样读缺项表，不用 501 充当这块功能。

同一张 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。`gkxlumen-element` 只读意见行：主体、分类、意见正文、时间。分类只用评价、评论、建议，写在行上。不读参数模拟行，不读路径与风险行。

不选方案则意见列表空。无行则列表空，不造一条专家意见。请求不插入、不更新、不删除。用户在页面上新打的评价留在浏览器，直到另有采集单。本分册不建那张单。

不把序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成方案意见。

HTTP 成功。不返回 501。

## 7. 231 方案报告导出与归档 · shells

公开资源仍是 `GET /display/v1/policy/evaluation/shells`。同步。不是 Job。与 230 同一条。

没有方案报告模型和导出 Job。核增研报 `report/jobs`（614–618）和评价页序号 222 的分析报告模板不是这条资源。

不另建报告行，不另建文件表，不单独占种类。element 只读同一张表里当次范围内的正文行和意见行。

导出文件从当次读到的这些行生成。不另开导出路径。不灌导出文件。响应里不内嵌一份预先写死的 PDF 或 Word。不写对象存储。不新建桶。前端不直连 RustFS。格式名留给 `BE-POL-CONTRACT-01`，本分册不冻结。

没有方案对照行则导出空。HTTP 成功。不返回 501。不返回写死的文件。

## 8. 空态对照

五叶的签收读法都是查缺项表。对不上或无行则该块空。不用 501 充当这五叶的画面。不返回写死的方案、分数、路径、意见或文件。请求内不重算。

| 序号 | 资源 | 是不是 Job | 无数据 |
|---|---|---|---|
| 227 | `POST evaluation/jobs` · 方案对照 | 否。同步读 | 对不上的行不返回。少于两行则对比空，不造第二个方案。不返回 501 |
| 228 | `POST evaluation/jobs` · 参数模拟 | 否。同步读 | 方案未选或参数档对不上则该块空。请求内不重算，不调用 `polan.text.simulate`。不返回 501 |
| 229 | `POST evaluation/jobs` · 路径与风险 | 否。同步读 | 方案未选或没有路径行则路径和风险都空。对不上则该块空。不返回推演曲线。不返回 501 |
| 230 | `GET evaluation/shells` · 互动意见 | 否。同步读 | 未选方案或没有意见行则列表空。请求不插入新意见。不返回 501 |
| 231 | `GET evaluation/shells` · 方案报告 | 否。同步读 | 没有正文行则导出空。文件只从当次读到的正文行和意见行生成。不灌导出文件。不返回 501 |

序号 219–226 不在上表。`counts` 上的短板条数和机遇条数不在上表。

## 9. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名、格式名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不改 `PolicyAnalysisTypes` 白名单。不加 `policy_scheme`。
- 不新开资源。浏览器只打 `/display/v1/policy/**`。不把 `/topic/v1/policy`、`/v1/policy/**`、`/topicAsync/**` 写成浏览器入口。
- 五叶不进 `gkxlumen-topic-async-service`。不调用 `polan.text.simulate`。`gkxlumen-display` 不直连 Python，不直连库。
- 不用 501 充当 227–231 的画面。对不上或无行则该块空。接口不直接返回写死的 mock。
- 不改 `POL-L2-DS11-PLAN-ARCH`、会签页，以及说明书、WBS、契约输入清单、调用链与边界、指标与 501、调研分册。
- 不改兄弟分册。219–226 不进本分册。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。
- 不新造 `metric_id`。不改 D4。229 沿用 `M_POLICY_DS_11_POLICY_EVAL_015`。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不挂 `M_POLICY_SIMULATE`、`M_POLICY_LAYOUT_REC_COUNT`。不读 `ads.policy_simulate`。
- 不把 `counts`、`compare/jobs`、`report/jobs`、`panorama/jobs`、`simulation/jobs` 写成这五叶。
- 230 的请求不插入新意见。231 不灌导出文件，不写对象存储。
- 查询不灌数。缺项表的建表与灌数不在本分册执行。
- 不改 `FE-POL-02A`，不新建前端单。契约冻结前前端继续 mock。
- 不会签。不把本单标 done。
