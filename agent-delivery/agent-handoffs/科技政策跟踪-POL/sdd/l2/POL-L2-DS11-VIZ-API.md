# POL-L2-DS11-VIZ-API · 政策分析评价 · 政策分析报告可视化呈现 · 后台接口设计

- 任务：`POL-L2-DS11-VIZ-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`（本单派令：已签收）。会签对照 `sdd/l2/会签/POL-L2-DS11-VIZ-SIGNOFF-ARCH.md`（复会签结论：同意）。本分册以这两份为准，不改它们

本分册只定政策分析评价二级「政策分析报告可视化呈现」的后台接口。SRS 序号 **219–222**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS11-VIZ-ARCH` 为准。契约输入清单里评价页的 `evaluation/counts`、`evaluation/jobs`、`evaluation/shells` 只作资源名对照。清单把趋势图、分区对比、报告模板导出的空态写在「501 时页面空态」列。清单里的 501 列不覆盖本分册。本分册不改那份清单。指标分册里 219、220、222 的「无模型 / 501」字样留在指标分册，本分册不改字。迁移后的读法是查表，或只消费第 7 项已有子图。无行或无子图则空。

签收口径：做不到的只允许缺项表灌 mock 后由接口读表。219 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。220 只读 `gapfill_policy_eval_partition`。221 不建表，只消费第 7 项已有子图。222 只读 `gapfill_policy_eval_shell` 的模板选用行。不允许接口直接返回写死的曲线、矩阵、弦线、PDF 或 Excel，也不用 501 充当这四叶的画面。

## 偏离

评价页只有 `counts`、`jobs`、`shells` 三条。219、220 仍用已有的 `POST /display/v1/policy/evaluation/jobs`，不增加第 4 条路径。这两段是同步读表，不是会写任务行的 Job。只要趋势或只要分区时，不把这两段登记成会写任务行的 `sub_type`。参数名留给 `BE-POL-CONTRACT-01`。

浏览器只打 `/display/v1/policy/**`。本四叶不把 `/topic/v1/policy`、`/topic/v1/policy/graph`、`/v1/policy/**` 或 `/topicAsync/**` 写成入口。219、220、222 不转发 `gkxlumen-topic-async-service`。221 不委托专题门面 `/graph`。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是本页路径。

## 1. 公开资源

前缀 `/display/v1/policy/`。四叶都在政策分析评价页的可视化区里完成，不另开页，不另开路径。本分册不新开资源。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 219 | `POST /display/v1/policy/evaluation/jobs` 的趋势段 | 同步。不是 Job。只要趋势时不建任务，不转发异步服务，不调 Python。element 只读 `gapfill_policy_eval_trend`。无行则图空 |
| 220 | 同一条 `POST /display/v1/policy/evaluation/jobs` 的分区段 | 同步。不是 Job。同样不建任务。element 只读 `gapfill_policy_eval_partition`。无行则图空 |
| 221 | 不设 `/display/v1/policy` 资源 | 不是 Job。只消费第 7 项已有子图。不委托专题 `/graph`。Java 不写 nGQL。无子图则空 |
| 222 | `GET /display/v1/policy/evaluation/shells` | 同步。不是 Job。element 只读 `gapfill_policy_eval_shell` 的模板选用行。无选用行则模板区空 |

`evaluation/counts` 不归本叶。短板条数和机遇条数留在 `counts` 已有读面。本分册不读 `counts`，也不把趋势点或分区对照数写进那次响应。

序号 223–231 不进本分册。`jobs` 上的焦点、效能、摘要、实施路径，以及 `shells` 上的解读条目、多媒体、互动意见、方案归档、分析报告份数，都不是这四叶。同一条路径上其它叶子的读法由它们自己的分册定。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。

`gkxlumen-display` 不直连 Python，不直连库，不写算法，不写 nGQL。不打算法中台 `/v1/policy/**`。不调用任何 `demo-*` 服务。不嵌中台页。

| 公开资源 | 内部委托 |
|---|---|
| `evaluation/jobs` 的趋势段、分区段 | 只要趋势或只要分区时，`gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python，不写任务行，不占并发锁，不发 SSE。`gkxlumen-element` 同步只读缺项表。趋势读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`，分区读 `gapfill_policy_eval_partition` |
| 221 | 不发 `/display/v1/policy` 资源。展示只消费第 7 项已有子图。不委托专题门面 `GET /topic/v1/policy/graph`。不把 `/v1/policy/graph` 写成展示地址。Java 不写 nGQL |
| `evaluation/shells` 的模板选用 | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 里的模板选用行。解读灌数单不灌模板选用 |

`jobs` 上已有的焦点、效能、摘要、实施路径不属于本二级。那些键仍走它们自己的分册，本分册不改它们。请求里若带了趋势或分区，这两段由 element 同步读表填上，不因模型未注册而写成 501。只选趋势或只选分区时，整次请求不写任务行。同一次请求里其它叶子的模型段失败时，不清空已经读到的趋势和分区。切时间、区域、类别不自动起任务。

某一块读失败，不清空同页已经返回的短板条数和机遇条数。那两条不在本叶。

trace 沿既有展示链。同步读在 display 往下带 traceId。本分册不新设计观测点。221 不新开查图任务，不另画查图时序。

## 3. 219 多维指标趋势图 · jobs 趋势段

公开资源：`POST /display/v1/policy/evaluation/jobs` 的趋势段。同步。不是 Job。

没有多维效能趋势模型。全景时序 `M_POLICY_TIMESERIES` 不挂本叶。效果分 `M_POLICY_EFFECT_SCORE` 的需求来源在推演，不挂本叶。不新造 `metric_id`。D4 保持 mock。

只要趋势时，`gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。这张表不写入 ODS、DWD、ADS。不把查询转到 Python 现造一个点。

用户要选的是时间、区域、类别里的切换，以及一组评估指标。至少一维，且至少一项指标。少了必选条件时该块空，不补一套默认对象，不补一段曲线。未勾选的维不读。指标名只来自缺项表里已有的名称，不另编词表。条件对不上行则图空。

重点和波动只标在读到的点上，不另算一条指标。

无行则图空。HTTP 成功。不返回 501。查询函数自己不拼曲线。

灌数是独立脚本（`POL-L2-DS11-VIZ-GAPFILL-L01`），不是请求处理。本分册不写 DDL，不执行灌数。列由 `POL-L2-DS11-VIZ-DATA` 定。`GDF-POLICY-MOCK-GATE-L01` 与这张缺项表无关，本分册不改那道闸门。

## 4. 220 分区/群体对比分析图 · jobs 分区段

公开资源与 219 同一条：`POST /display/v1/policy/evaluation/jobs` 的分区段。同步。不是 Job。

没有分区效果模型。全景的全国分布、类型分布、级别分布不挂本叶。不新造 `metric_id`。D4 保持 mock。

只要分区时，同样不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_partition`。这张表不写入 ODS、DWD、ADS。

用户要选的是看地区、行业还是目标群体，以及图种。对象三选一，必选。图种可不选。对象只有地区、行业、目标群体。图种只有柱状、热力。未选的对象不读。图种不选则柱和热力都用这一批行。柱和热力不建第三张表。

资源投向可选。投向不在本叶编目，只接受缺项表里已有的值。投向对不上行则该图空。

无行则图空。不返回演示矩阵。HTTP 成功。不返回 501。查询函数自己不拼对照数。

灌数与 219 同一张单 `POL-L2-DS11-VIZ-GAPFILL-L01`。查询不灌数。本分册不写 DDL，不执行灌数。

趋势和分区可以出现在同一次 POST 里。两段都由 element 同步读各自的表，都不因此建任务。

## 5. 221 多维结构关联图 · 不设资源

不设 `/display/v1/policy` 资源。本分册不给 221 写路径，也不写方法。不是 Job，也不是新的查图任务。

本序号没有专属 `metric_id`。不挂 `M_POLICY_GRAPH_107_1`，不挂 `M_POLICY_RELATION_DEGREE`。前者留在全景区域差异，后者留在推演关联。

展示只消费第 7 项已有子图。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。挂接可空。Java 不写 nGQL。`gkxlumen-display` 不为此直连库，不直连 Python。

不委托专题门面 `/graph`。不把 `GET /topic/v1/policy/graph` 或 `GET /v1/policy/graph` 写成展示浏览器地址。不走 `E-E7-POLICY-M1-L06`。不重做抽取，不重开 GDF。不把共词网络写成新算法，不新造图指标。不接受演示页上的节点 id 作为政策组的新参数。不把弦线矩阵和演示路径灌进缺项表。

用户要看的是弦线图或关系网。图种可不选。只有这两类。传导链路是同一张子图上的路径查看，不是第三套数据。子图能读到则弦线图和关系网用同一份结果。子图没有则两图都空，路径也空。HTTP 成功意义上的空块。不返回 501。不返回写死的弦线或关系网。

## 6. 222 报告模板定制与批量导出 · shells

公开资源：`GET /display/v1/policy/evaluation/shells`。同步。不是 Job。

没有导出模型。核增研报 `report/jobs` 和全景 `benchmark-report` 不是这条资源。不新造 `metric_id`。

`gkxlumen-display` 不直连库，不直连 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 里的模板选用行。壳表由解读二级为 224、225 建立，只灌解读条目和多媒体条目。`POL-L2-DS11-READ-GAPFILL-L01` 不灌模板选用。本叶不另建表，不把模板选用加进那张灌数单，也不把模板行拆进 `gapfill_policy_eval_trend`。

没有选用行则模板区空。不返回一套写死的模板。HTTP 成功。不返回 501。

模板必选。汇报周期、分析维度、图表类型不齐则该次导出空。格式只有 PDF、Excel。图表类型只有趋势、柱状、热力、弦线、关系网。维度只用 219 的三维和 220 的三类对象。未勾选的图表类型不进该次导出。不选格式则只看选用行，不生成文件。

要文件时，只从当次读到的行生成 PDF 或 Excel。响应里不内嵌一份写死的文件。不写对象存储。不灌 PDF，不灌 Excel。前端不直连 RustFS。不新建桶。

操作日志是用户自己的记录。不建日志缺项表，不灌假日志。没有真实导出记录则日志空。

`shells` 上的多媒体、互动意见、方案归档、分析报告份数不在本二级展开。222 这一段为空时，不得用模板正文把整条 `shells` 填满。解读条目、焦点和摘要归解读二级，本叶不写。

查询不灌数。本分册不写 DDL。壳表的列由解读二级的数据分册定。

## 7. 空态对照

四叶的签收读法都是查表，或只消费已有子图。无行或无子图则空。不用 501 充当这四叶的画面。不返回写死的曲线、矩阵、弦线、模板、PDF 或 Excel。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 219 | `POST evaluation/jobs` 的趋势段。同步，不是 Job | `gapfill_policy_eval_trend` 无行，或条件对不上行，则图空。不补曲线。只要趋势时不建任务，不转发异步服务，不调 Python。不返回 501 |
| 220 | 同一条 `POST evaluation/jobs` 的分区段。同步，不是 Job | `gapfill_policy_eval_partition` 无行则图空。投向对不上则该图空。不返回演示矩阵。同样不建任务。不返回 501 |
| 221 | 不设 `/display/v1/policy` 资源。不是 Job | 第 7 项子图没有则弦线图、关系网和路径都空。不委托专题 `/graph`。Java 不写 nGQL。不返回 501 |
| 222 | `GET evaluation/shells`。同步，不是 Job | 壳表没有模板选用行则模板区空。解读灌数单不灌模板选用。周期、维度、图表类型不齐则该次导出空。要文件只从当次读到的行生成。不灌 PDF、Excel、假日志。不返回 501 |

`counts` 不在上表。短板条数和机遇条数留在 `counts` 已有读面。序号 223–231 不在上表。某一块读失败，不清空已经返回的短板条数和机遇条数。模型段失败时，不清空已经读到的趋势和分区。

## 8. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。
- 不新开资源。浏览器只打 `/display/v1/policy/**`。不增加第 4 条路径。不把 `/topic/v1/policy`、`/topic/v1/policy/graph`、`/v1/policy/**`、`/topicAsync/**` 写成浏览器入口。
- `gkxlumen-display` 不直连 Python，不直连库，不写算法，不写 nGQL。
- 219、220 只要趋势或只要分区时不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python，不写任务行，不占并发锁，不发 SSE。不把这两段登记成会写任务行的 `sub_type`。
- 221 不设 `/display/v1/policy` 资源。只消费第 7 项已有子图。不委托专题 `/graph`。不走 `E-E7-POLICY-M1-L06`。
- 222 只读模板选用行。`POL-L2-DS11-READ-GAPFILL-L01` 不灌模板选用。要文件只从当次读到的行生成。不灌 PDF、Excel、假日志。不写对象存储。
- 不用 501 充当 219–222 的画面。无行或无子图则空。接口不直接返回写死的 mock。
- `counts` 不归本叶。序号 223–231 不进本分册。
- 不改 `POL-L2-DS11-VIZ-ARCH`、会签页，以及说明书、WBS、契约输入清单、调用链与边界、指标与 501、调研分册。
- 不改 `ARCH-DISPLAY-01`。不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不把 `M_POLICY_TIMESERIES`、全景分布、`M_POLICY_EFFECT_SCORE` 挂到 219 或 220。不把 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` 挂到 221。
- 不把 `compare/jobs`、`report/jobs`、`benchmark-report` 写成这四叶。
- 查询不灌数。缺项表的建表与灌数不在本分册执行。221 不建表。222 不另建表。
- 不改 `FE-POL-02A`，不新建前端单。契约冻结前前端继续 mock。
- 不会签。不把本单标 done。
