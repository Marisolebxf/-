# POL-L2-DS11-VIZ-API · 政策分析评价 · 政策分析报告可视化呈现 · 后台接口设计

- 任务：`POL-L2-DS11-VIZ-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`（2026-11-03 返工后第二轮，架构、算法、数据、产品四角色同意。待 `human:淮政玮` 签收。本分册以它为准，不改它，也不把它标 done）

本分册只定政策分析评价二级「政策分析报告可视化呈现」的后台接口。SRS 序号 **219–222**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里写路径、方法、种类、同步或 Job、空态，以及架构第 3 节闭集里的条件字段名。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-VIZ-ARCH` 为准。契约输入清单里评价页已经点名的 `evaluation/jobs`、`evaluation/shells` 只作资源名对照。`evaluation/counts` 不在本二级。清单、`指标与501.md`、说明书、WBS、调研里仍写的 501 空态不覆盖本分册。

签收口径：219、220、222 只允许缺项表灌 mock 后由接口读表。221 不新开政策资源。不允许接口直接返回 mock，也不用 501 充当这四叶的功能。无行则空。

## 偏离

三处与上游字面不一致。本分册写明，不回头改那些文件。

1. DoD 完成标准里的「501 空态」与 `指标与501.md` 仍把 219、220、222 记为 501、无已注册模型。该判定留在指标分册，本分册不改字。2026-11-03 架构把迁移后的读法定为查表：219 读 `gapfill_policy_eval_trend`，220 读 `gapfill_policy_eval_partition`，222 读 `gapfill_policy_eval_template`。空态是空，HTTP 成功，不返回 501。不改 `指标与501.md`、说明书、WBS、调研、契约输入清单。
2. DoD「不复用 `/topic/v1/policy`」在本二级是：浏览器只打 `/display/v1/policy/**`。219、220、222 不进 `gkxlumen-topic-async-service`，不调用 `POST /topic/v1/analysis/tasks`，不调 Python。221 不委托专题门面 `/graph`。对外不暴露 `/topicAsync/**`。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。
3. 说明书第 11.2 节仍把模板选用写在解读 222–226 那一行，表名仍像壳表。已签收解读稿规定 `gapfill_policy_eval_shell` 只服务 224、225。架构第 5.4 节已收窄，本分册按架构读 `gapfill_policy_eval_template`。不改说明书，不改已签收的 `POL-L2-DS11-READ-ARCH` 与 `POL-L2-DS11-READ-API`。

## 1. 公开资源

前缀 `/display/v1/policy/`。四叶都在政策分析评价页的可视化区里完成，不另开页，不增加第 4 条路径。浏览器只打 `/display/v1/policy/**`。

本二级对外只有下面两条已有资源上的三个分支。221 不占资源。

| 序号 | 公开资源 | 种类 | 同步或 Job | 读法 |
|---|---|---|---|---|
| 219 | `POST /display/v1/policy/evaluation/jobs` | 趋势 | 同步。不建任务 | element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。无行则图空。不返回 501 |
| 220 | 另一次 `POST /display/v1/policy/evaluation/jobs` | 分区 | 同步。不建任务 | element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。无行则图空。不返回 501 |
| 221 | 不设 `/display/v1/policy` 资源 | 无 | 无调用 | 只消费第 7 项已有子图。挂接可空。子图没有则两图都空，路径也空 |
| 222 | `GET /display/v1/policy/evaluation/shells` | 模板选用 | 同步。不建任务 | element 只读 `gkxlumenx_gapfill.gapfill_policy_eval_template`。无行则模板空。不返回 501 |

`jobs` 一次请求只带一种类。219 与 220 必须分成两次请求。一次请求不能同时同步填趋势并转发异步，也不能同时读趋势表和分区表。

`shells` 一次请求只带一种类。222 这一次只读模板表。不读 `gapfill_policy_eval_shell`。

`counts` 只服务短板条数和机遇条数，序号不在 219–222。本分册不读 `counts`，也不把趋势点或分区对照数写进那次响应。

`evaluation/jobs`、`evaluation/shells` 上还有解读和方案的种类。本分册不把整条资源改成只服务 219–222，也不改写那些种类。见第 8 节。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。不调用任何 `demo-*` 服务。Java 不拼趋势点、不拼分区对照、不生成写死的 PDF 或 Excel。

| 公开资源 | 种类 | 内部委托 |
|---|---|---|
| `POST evaluation/jobs` | 趋势 | 不建任务。不进 `gkxlumen-topic-async-service`。不调 `POST /internal/policy/jobs/execute`。不调 Python。`gkxlumen-element` 只读 `gapfill_policy_eval_trend` |
| `POST evaluation/jobs` | 分区 | 同左，只读 `gapfill_policy_eval_partition`。与趋势不是同一次请求 |
| `GET evaluation/shells` | 模板选用 | 不建任务。不进异步。`gkxlumen-element` 只读 `gapfill_policy_eval_template`。不读 `gapfill_policy_eval_shell` |
| 221 | 无 | 不新开政策资源，不委托专题门面 `/graph`，不打 `GET /v1/policy/graph` |

219、220、222 不占并发锁，不发 SSE。切时间、区域、类别不自动起任务。这三种类本身也不建任务。

某一块读失败，不清空同页已经返回的短板条数和机遇条数。那两条不在本叶。失败也不清空其他种类已经返回的区块。

trace 沿既有展示链。同步读在 display 往 element 带 traceId。本分册不新设计观测点，不把这三支记到异步任务链上。

条件字段只来自架构第 3 节闭集。未列出的条件不收。少了必选条件时，该块空，不补一套默认对象。闭集外的值不接收，该块空，不替换成另一套图。

同一次 `jobs` 若同时出现本分册的 `kind` 和解读分册的 `sub_type`，该次不建任务，不读趋势表，不读分区表，不转发异步。该块空。HTTP 成功。不返回 501。

## 3. 219 多维指标趋势图 · jobs · 同步

公开资源：`POST /display/v1/policy/evaluation/jobs`。这一次 `kind=趋势`。不建任务。不是 Job。

没有趋势模型。不挂 `M_POLICY_TIMESERIES`，不挂 `M_POLICY_EFFECT_SCORE`，不挂 `M_POLICY_IMPLEMENTATION_EFFECT`。不调用 `effect.run`。不把全景时序改挂到 219。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_trend`。

条件字段只收这三个：

| 字段 | 含义 | 必选 | 闭集 |
|---|---|---|---|
| `kind` | 种类 | 是 | 本请求只能是 `趋势` |
| `switch` | 切换的维 | 至少一维 | 只有 `时间`、`区域`、`类别`。未出现的维不读 |
| `metric` | 评估指标名 | 至少一项 | 只接受该缺项表里已有的名称。不另编词表 |

`switch` 缺省或为空、或 `metric` 缺省或为空：图空。不补默认曲线。

element 按所选维和指标名查表。一行是一个趋势点：时间、区域或类别上的位置，评估指标名，一个对照值。列名由 `POL-L2-DS11-VIZ-DATA` 定，本分册不另造列。重点和波动只标在读到的点上，不另算一条指标。条件对不上行则图空，不在接口里补一段曲线。

建表和灌数不在本分册。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01`（`data-agent`，监管 `human:淮政玮`）不是请求处理。查询请求不灌数。表在 `gkxlumenx_gapfill`，不写入 ODS、DWD、ADS、供应方库。

空态：无行则图空。HTTP 成功。不造一条曲线。不返回写死的 2020–2026 序列，不返回五维雷达。不返回 501。不在接口函数里返回 mock。D4 仍是 mock。行是灌入的 mock，不是已上线实数。`GDF-POLICY-MOCK-GATE-L01` 与这张表无关，本分册不改那道闸门。

## 4. 220 分区/群体对比分析图 · jobs · 同步

公开资源与 219 相同：`POST /display/v1/policy/evaluation/jobs`。这一次 `kind=分区`。必须是另一次请求。不建任务。不是 Job。

没有分区模型。全景的全国分布、类型分布、级别分布不挂本叶。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_partition`。

条件字段只收这四个：

| 字段 | 含义 | 必选 | 闭集 |
|---|---|---|---|
| `kind` | 种类 | 是 | 本请求只能是 `分区` |
| `subject` | 看哪一类对象 | 是，三选一 | 只有 `地区`、`行业`、`目标群体`。未选的对象不读 |
| `chart` | 图种 | 否 | 只有 `柱状`、`热力`。不传则柱和热力都用这些行。闭集外的图种不收，该图空 |
| `allocation` | 资源投向 | 否 | 不在本叶编目。只接受缺项表里已有的值。对不上行则该图空 |

`subject` 缺省，或一次带上两个对象：该块空。不补默认对象。不另造城市名单。

element 按所选对象读表。一行是一个对象上的对照：地区、行业或群体，以及一个对照数。资源投向若要筛，值在行里，不另造指标。柱和热力读同一批行。不建第三张可视化表。列名由 `POL-L2-DS11-VIZ-DATA` 定，本分册不另造列。

灌数与 219 同一张单，本分册不执行。查询请求不灌数。不写入 ODS、DWD、ADS。

空态：表无行则图空。投向对不上则该图空。HTTP 成功。不返回演示矩阵。不返回 501。不在接口函数里返回 mock。D4 仍是 mock。

## 5. 221 多维结构关联图 · 不设资源

本序号没有专属 `metric_id`。不挂 `M_POLICY_GRAPH_107_1`，不挂 `M_POLICY_RELATION_DEGREE`。

不设 `/display/v1/policy` 资源。不新增路径、方法、种类或条件字段。不接受演示页上的节点 id 作为政策组的参数。图种只有弦线图、关系网，是同一张已有子图上的查看，不是第三套数据，也不是本分册的请求参数。传导路径没有单独的数据来源。

展示只消费第 7 项已有子图。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。Java 不写 nGQL。挂接可空。子图读不到则弦线图和关系网都空，路径也空。

不走 `E-E7-POLICY-M1-L06`。不把 `GET /topic/v1/policy/graph` 或 `GET /v1/policy/graph` 写成展示浏览器地址。不重做抽取，不重开 GDF。不把共词网络写成新算法。不把弦线矩阵和演示路径灌进缺项表。不用 501 充当这一叶的画面。

## 6. 222 报告模板定制与批量导出 · shells · 同步

公开资源：`GET /display/v1/policy/evaluation/shells`。这一次 `kind=模板选用`。同步。不建任务。不是 Job。

没有导出模型。核增研报 `report/jobs`（614–618）和全景 `benchmark-report` 不是这条资源。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_template`。

不读 `gapfill_policy_eval_shell`。不用 224、225 的解读条目或多媒体条目充当模板行。不把模板行拆进趋势表或分区表。

条件字段只收这六个：

| 字段 | 含义 | 必选 | 闭集 |
|---|---|---|---|
| `kind` | 种类 | 是 | 本请求只能是 `模板选用` |
| `template` | 一套已有模板 | 是 | 只接受该缺项表里已有的模板名。不另编模板词表 |
| `period` | 汇报周期 | 导出时必填 | 只接受该选用行上已有的周期。不单列近 1 年、近 3 年、近 5 年 |
| `dimension` | 分析维度 | 导出时必填 | 只用 219 的三维和 220 的三类对象：`时间`、`区域`、`类别`、`地区`、`行业`、`目标群体` |
| `chart_type` | 图表类型 | 导出时必填 | 只有 `趋势`、`柱状`、`热力`、`弦线`、`关系网`。未勾选的不进该次导出。不收饼图、散点 |
| `format` | 是否导出以及格式 | 否 | 只有 `PDF`、`Excel`。不传则只返回选用行，不生成文件 |

`template` 缺省或对不上行：模板区空，不生成文件。

`format` 有值，而 `period`、`dimension`、`chart_type` 任一不齐：该次导出空，不生成文件。模板能对上时仍只返回选用行。不拿写死文件补上。

一行是一条模板选用：模板名，以及该模板可用的汇报周期、分析维度、图表类型。值落在第 3 节闭集里。列名由 `POL-L2-DS11-VIZ-DATA` 定，本分册不另造列。

要文件时，从这次读到的行生成 PDF 或 Excel。响应里不内嵌一份写死的文件。不写对象存储。不灌 PDF，不灌 Excel。前端不直连 RustFS。不新建桶。

操作日志是用户自己的记录。不建日志缺项表，不灌假日志。没有真实导出记录则日志空。本分册不把「日志空」写成归档已经做到，也不另开日志资源。

建表和灌数不在本分册。同一张灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 覆盖 219、220、222 三张表。本分册不执行。查询请求不灌数。不写入 ODS、DWD、ADS。

`shells` 上的多媒体、互动意见、方案报告不在本二级展开。222 这一段为空时，不得用模板正文把整条 `shells` 填满，也不得改去读壳表把空段填上。

空态：无选用行则模板区空。HTTP 成功。不返回一套写死的模板。不返回 501。不在接口函数里返回 mock。D4 仍是 mock。

## 7. 空态对照

四叶的签收读法：219、220、222 查缺项表，221 只消费已有子图。无行或挂接为空则空。不用 501 充当功能。接口不直接返回写死的 mock。mock 若存在，只能先由灌数单落进表，再被查询读出来。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 219 | jobs · `kind=趋势` | `gapfill_policy_eval_trend` 无对得上的行，或少了维、少了指标名，则图空。不造曲线。不建任务。不返回 501 |
| 220 | jobs · `kind=分区` | `gapfill_policy_eval_partition` 无对得上的行，或对象不在三选一里，则图空。投向对不上则该图空。不返回演示矩阵。不返回 501 |
| 221 | 无政策资源 | 子图读不到则弦线图、关系网、路径都空。不新开路径去转接。不返回 501 |
| 222 | shells · `kind=模板选用` | `gapfill_policy_eval_template` 无选用行则模板区空。导出条件不齐则不生成文件。无真实导出则日志空。不写对象存储。不返回 501 |

`kind` 与 `sub_type` 同传时，该块空。不建任务，不转发异步，不读本二级的表。HTTP 成功。不返回 501。

## 8. 与解读、方案共享资源的种类分界

`POST /display/v1/policy/evaluation/jobs` 与 `GET /display/v1/policy/evaluation/shells` 是评价页共用资源。一次请求只一种类。实现时按种类分发。本分册只增加第 1 节的三个分支。

### 8.1 jobs

| 种类 | 定稿 | 同步或 Job | 读取 | 本分册 |
|---|---|---|---|---|
| 趋势 | 本分册 | 同步。不建任务 | `gapfill_policy_eval_trend` | 只写这一支 |
| 分区 | 本分册 | 同步。不建任务 | `gapfill_policy_eval_partition` | 只写这一支。与趋势分成两次请求 |
| `policy_focus_ads` | 已签收 `POL-L2-DS11-READ-API` | Job | `ads.policy_focus` 且 `policy_id` 非空 | 不改键，不改白名单例外，不改 `run()` 的删除范围 |
| `policy_text_parse` | 已签收 `POL-L2-DS11-READ-API` | Job | `ads.policy_text_parse.summary` | 不改键。不把序号 229 写进这个异步键 |
| 方案对照 | `POL-L2-DS11-PLAN-API` | 方案稿定为同步读方案表 | `gapfill_policy_eval_scheme` | 留给方案接口分册 |
| 参数模拟 | `POL-L2-DS11-PLAN-API` | 方案稿定为同步读方案表 | 同上 | 留给方案接口分册 |
| 路径与风险（序号 229） | `POL-L2-DS11-PLAN-API` | 方案稿定为同步。不进异步 | 同上 | 留给方案接口分册。本分册不把它写成 Job |
| 效能得分 | 不在 219–222 | 维持原读法 | 本分册不点名新表 | 不改 |

`PolicyAnalysisTypes` 现有异步白名单不增加趋势键、分区键。趋势和分区用 `kind`，不写入 `sub_type`。已签收的两个异步键仍只走解读分册的 Job 链：`gkxlumen-display` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。那条链不是 219、220 的委托。

一次请求不能同时同步填趋势或分区，又转发异步。

### 8.2 shells

| 种类 | 定稿 | 同步或 Job | 读取 | 本分册 |
|---|---|---|---|---|
| 模板选用 | 本分册 | 同步 | `gapfill_policy_eval_template` | 只写这一支。不读壳表 |
| 解读条目 | 已签收 `POL-L2-DS11-READ-API` | 同步 | `gapfill_policy_eval_shell` | 不改 |
| 多媒体条目 | 已签收 `POL-L2-DS11-READ-API` | 同步 | 同上 | 不改。不把模板选用并进这两类行 |
| 互动意见 | `POL-L2-DS11-PLAN-API` | 方案稿定为同步读方案表 | `gapfill_policy_eval_scheme` | 留给方案接口分册 |
| 方案报告 | `POL-L2-DS11-PLAN-API` | 方案稿定为同步读方案表 | 方案对照行和意见行 | 留给方案接口分册 |

222 不读 `gapfill_policy_eval_shell`。解读壳表的行种类仍只有解读条目和多媒体条目。

## 9. 明确不做

- 不另建 API-POL。不冻结枚举、响应列名和 DTO。交给 `BE-POL-CONTRACT-01`。条件字段只到第 3–6 节的表，不超出架构第 3 节闭集。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不补评价页 display 控制器。
- 不改 `POL-L2-DS11-VIZ-ARCH`、`POL-L2-DS11-READ-ARCH`、`POL-L2-DS11-READ-API`、`POL-L2-DS11-PLAN-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研和任何兄弟分册。
- 不改 `policy_focus_ads`、`policy_text_parse`。不把序号 229 写成异步。方案种类留给 `POL-L2-DS11-PLAN-API`。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。
- 浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`。
- 219、220、222 不进 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。
- 一次请求只一种类。不同一次请求里既同步填趋势或分区，又转发异步。
- 不用 501 充当 219–222 的功能。无行则空。接口不直接返回 mock。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不改指标分册里 219、220、222 的「无模型」判定文字。
- 不读 `evaluation/counts`。不把趋势点或分区对照写进 counts。
- 221 不新开 `/display/v1/policy` 资源。不委托 `/graph`。不接受节点 id。
- 222 不读 `gapfill_policy_eval_shell`。不写对象存储。不灌 PDF、Excel、假操作日志。
- 不建立、不灌表。查询不灌数。DDL 在 `POL-L2-DS11-VIZ-DATA`。灌数在 `POL-L2-DS11-VIZ-GAPFILL-L01`。
- 不纳入本分册：223–226 解读、227–231 方案、效能得分、`compare/jobs`、`report/jobs`、`benchmark-report`、`simulation/jobs`。
- 不改 `FE-POL-02A`，不新建前端单。契约冻结前前端继续 mock。
- 不会签。不把本单标 done，不标 ready_to_sign。

## 10. 2026-11-12 增补：DS11-VIZ 七可视化块 · viz · 同步

> 增补来源：监管人 `human:淮政玮` 2026-11-12 03:48 裁定（入口=③独立资源，见 `POL-L2-DS11-VIZ-GAPFILL-L02-DATA` §8.1）；实现 handoff = `POL-L2-DS11-VIZ-GAPFILL-L02-BE`。本节只增补，不改 §1–§9 原文；第 1 节「对外只有三个分支」的口径由本节放宽为四个分支。

七可视化块是 demo 复刻保留块（无 SRS 序号），表与列真源 = `POL-L2-DS11-VIZ-GAPFILL-L02-DATA`。读面挂在既有 `/evaluation` 资源上作子路径扩展，不新开第 4 条路径，不触 VIZ-ARCH「不加第 4 条路径」红线。

公开资源：`GET /display/v1/policy/evaluation/viz?block=<块键>`。同步只读，不建任务，不进 `JOB_SUB_TYPES` 异步白名单，不调 Python。

条件字段只收这一个：

| 字段 | 含义 | 必选 | 闭集 |
|---|---|---|---|
| `block` | 可视化块键 | 是 | 只有 `metric`、`portrait`、`geo`、`region_impl`、`topic_heat`、`topic_sentiment`、`bubble`。闭集外/缺省不查表，该块空 |

内部委托：`gkxlumen-display`（BFF 只读不连库）→ `@NoToken` Feign → `gkxlumen-element` `GET /v1/element/policy/evaluation/viz`（`@Inner`）→ `{gapfill}.gapfill_policy_eval_viz_<block>` 七表一一对应。

响应形状：`R` 包 `data.records`（行内 snake_case 由 `ElementDao` 统一转 camelCase）。空态：闭集外、块无行、表未建、下游失败一律 HTTP 200 + `records: []`，不返回 501。血缘列随行返回（`is_mock=1`，`metric_id` 留空，见 DATA §5）。

拣行语义：七块无用户筛选，一次请求整块读；各表保留的块内拣行键（`region_name` / `topic_name`+`stat_month` / `scope_kind`+`topic_name` / `category`）当前读面不启用（DATA §3）。

本节不改动 219–222 的任何既有分支与闭集；`jobs` / `shells` / `counts` 行为不变。
