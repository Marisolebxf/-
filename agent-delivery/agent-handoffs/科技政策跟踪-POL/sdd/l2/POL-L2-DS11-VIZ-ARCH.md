# POL-L2-DS11-VIZ-ARCH · 政策分析评价 · 政策分析报告可视化呈现

- 任务：`POL-L2-DS11-VIZ-ARCH`
- 日期：2026-11-03
- 状态：2026-11-03 返工后第二轮，架构、算法、数据、产品四角色同意。待 `human:淮政玮` 签收。不标 done
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-DS11-VIZ-ARCH-SEQ`（本叶新图，源文件无 frontmatter，记 `draft`）

本叶只定政策分析评价二级「政策分析报告可视化呈现」的实现架构和整体流程。SRS 序号 **219–222**。用户故事 `US-DS-POL-05`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-DS11-VIZ-API`。

上游只引用，不改写：`政策分析评价.md` 219–222、说明书第 2 节 DS-11、第 6 节评价三条路径、第 11.2 节、`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 的 `evaluation/counts`、`evaluation/jobs`、`evaluation/shells`、`sdd/指标与501.md` 219–222。不新造 `metric_id`，不改 D4。

签收标准沿说明书第 11 节：可实现才签收。真算、真查或真模型做不到时，只接受新建表、把 mock 写入表、接口读表。不允许接口直接返回 mock，也不用 501 充当这四叶的功能。本叶按这个标准写迁移之后的架构。

调研和指标分册把 219、220、222 记为 501，意思是没有已注册模型，也没有专属 `metric_id`。那个判定保留在指标分册，本叶不改字。迁移后的读法是查表，无行则空。

## 1. 范围

四叶都在政策分析评价页的可视化区里完成，不另开页。评价页路径仍是说明书第 6 节的三条，本叶不增加第 4 条。

| 序号 | 叶子 | 需规摘要 | 本叶流程 |
|---|---|---|---|
| 219 | 多维指标趋势图 | 按时间、区域、类别切换，组合选取评估指标，看绩效趋势，并标出重点和波动 | 没有趋势模型。读缺项表。不借用全景时序 |
| 220 | 分区/群体对比分析图 | 用柱状图、热力图看地区、行业或目标群体的政策效果，并可筛资源投向 | 没有分区模型。读另一张缺项表。不挂全景分布 |
| 221 | 多维结构关联图 | 弦线图、关系网展示政策要素关联和效果传导，可追踪影响路径 | 跨项。只消费第 7 项已有子图。不建表，不新开资源 |
| 222 | 报告模板定制与批量导出 | 选模板、汇报周期、分析维度、图表类型，批量生成 PDF、Excel，并归档操作日志 | 交互壳。模板选用读本叶的 `gapfill_policy_eval_template`。不读解读壳表。不灌文件，不灌假日志 |

219、220 的行是灌入的 mock，D4 仍是 `mock`。本叶不把 mock 写成已上线。`GDF-POLICY-MOCK-GATE-L01` 与这两张缺项表无关，本叶不改那道闸门。

## 2. 实现架构

浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。

| 叶子 | 资源 | 迁移后的读法 |
|---|---|---|
| 219 | `POST /display/v1/policy/evaluation/jobs` | 种类为趋势。一次请求不带其他种类。不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。无行则图空 |
| 220 | 另一次 `jobs` | 种类为分区。不与趋势放在同一次请求里。不建任务。`gkxlumen-element` 只读 `gapfill_policy_eval_partition`。无行则图空 |
| 221 | 不设 `/display/v1/policy` 资源 | 只消费第 7 项已有子图。挂接可空。不委托专题门面 `/graph` |
| 222 | `GET /display/v1/policy/evaluation/shells` | 种类为模板选用。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_template`。表和灌数都在本叶，灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01`。无行则模板空 |

`counts` 只服务短板条数和机遇条数，序号不在 219–222。本叶不读 `counts`，也不把趋势点或分区对照数写进那次响应。

`jobs` 一次请求只带一种类。本叶只有两种：219 只要趋势，element 只读 `gapfill_policy_eval_trend`；220 只要分区，element 只读 `gapfill_policy_eval_partition`。这两种都不建任务，不进 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。不在同一次请求里既同步填趋势或分区，又转发异步。切时间、区域、类别不自动起任务。

焦点和摘要的异步键由解读稿定，只有 `policy_focus_ads` 和 `policy_text_parse`。序号 229 的路径与风险由方案稿定：不进异步，读 `gapfill_policy_eval_scheme`。效能得分不在 219–222，本叶不改它的读法。本叶不把 229 和效能得分写成仍走异步。

`shells` 一次请求只带一种类。222 只读模板表。解读稿的 `gapfill_policy_eval_shell` 只服务 224、225，行种类只有解读条目和多媒体条目。方案稿的互动意见和方案报告读 `gapfill_policy_eval_scheme`。

```mermaid
flowchart LR
  fe["评价页 · 可视化 219-222"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display"]
  el["gkxlumen-element"]
  gap["gkxlumenx_gapfill"]
  graph["第 7 项已有子图"]
  fe --> gw --> bff
  bff -->|"219 趋势、220 分区：不建任务"| el --> gap
  bff -->|"221：只消费，可空"| graph
  bff -->|"222：shells 读模板表"| el
```

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。`E-E7-POLICY-M1-L06` 不是本页路径。

## 3. 各图的输入条件

条件只来自需规原文。下表是用户要提交的选择，不是参数名，也不是响应字段。参数名留给 `POL-L2-DS11-VIZ-API`。未列出的条件不收。少了必选条件时，该块空，不补一套默认对象。

| 序号 | 用户要选 | 必选 | 闭集 | 落到哪次读取 |
|---|---|---|---|---|
| 219 | 时间、区域、类别里的切换；一组评估指标 | 至少一维，且至少一项指标 | 切换只有时间、区域、类别。指标名只来自缺项表里已有的名称，不另编词表 | `jobs` 的趋势段按所选维和指标名查 `gapfill_policy_eval_trend` |
| 220 | 看地区、行业还是目标群体；图种；可选的资源投向 | 对象三选一。图种可不选 | 对象只有地区、行业、目标群体。图种只有柱状、热力。投向不在本叶编目，只接受缺项表里已有的值 | 图种不选则柱和热力都出。`jobs` 的分区段查 `gapfill_policy_eval_partition`。投向对不上行则该图空 |
| 221 | 看弦线图还是关系网 | 图种可不选 | 只有弦线图、关系网。传导链路是同一张子图上的路径查看，不是第三套数据 | 不发政策资源。子图没有则两图都空，路径也空 |
| 222 | 一套已有模板；汇报周期；分析维度；图表类型；是否导出以及格式 | 模板必选。周期、维度、图表类型不齐则该次导出空 | 格式只有 PDF、Excel。图表类型只有趋势、柱状、热力、弦线、关系网。维度只用 219 的三维和 220 的三类对象 | `shells` 按模板读 `gapfill_policy_eval_template`。不选格式则只看选用行，不生成文件 |

219 未勾选的维不读。220 未选的对象不读。222 未勾选的图表类型不进该次导出。221 不接受演示页上的节点 id 作为政策组的新参数。

### 3.1 条件从哪来

对照了两处 demo 和现网 lumen。展示原型 `demo-ui-science` 的政策分析页不调接口。算法中台 `demo-ui-system-test` 的政策页调的是 `/v1/policy/**`，没有这四叶的趋势、分区、模板窗口。lumen 已接通的政策门面是 `gkxlumen-topic-policy` 上的检索、选项、指标、正文和专题侧 `/graph`。浏览器仍只打 `/display/v1/policy/**`。不把 `/v1/policy/**`、`/topic/v1/policy/graph` 和 `policyData.js` 迁进来。展示仓里还没有评价页的 display 控制器，本叶不补代码。

| 条件 | demo 里实际从哪取 | lumen 里哪条接口能提供 | 本叶怎么用 |
|---|---|---|---|
| 219 的时间、区域、类别和指标 | `PolicyAnalysis.jsx` 读 `policyData.js` 的 `trendAnalysisData`、`evaluationMetrics`。七年件数、类别占比、六地区分数、五维雷达都是页内常量 | 无评价趋势接口。全景时序是 `M_POLICY_TIMESERIES`，不挂本叶。`polan.eval.effect.run` 写的是 `ads.policy_effect` 和效果分，需求来源不在 219 | 维和指标名只从 `gapfill_policy_eval_trend` 的行里读出。表空则下拉空。不迁 2020–2026 的序列，不迁五维雷达 |
| 220 的对象、图种、资源投向 | `RegionGroupCompare.jsx` 读 `regionGroupCompareData`。地区五市、行业五领域、群体，以及资金、人才、平台、税收，都是页内常量 | 无分区接口。全景的全国分布、类型分布、级别分布不挂本叶 | 对象和投向只从 `gapfill_policy_eval_partition` 的行里读出。不迁那四类投向常量和城市名单。图种保持上表闭集，不调接口 |
| 221 的图种和路径 | `StructureLinkPanel.jsx` 读 `chordMatrixData`、`policyElementCorrelation`、`policyKnowledgeGraph`、`effectTransmissionPaths` | 专题门面有 `GET /topic/v1/policy/graph`，下游 `/internal/policy/graph`。算法中台另有 `GET /v1/policy/graph`。都不是展示浏览器地址 | 不调这两条。只消费第 7 项已有子图。子图读不到则空。不迁弦线矩阵和三条演示路径 |
| 222 的模板、周期、维度、图表类型、格式 | `ReportTemplateExport.jsx` 读 `reportTemplates`。周期是近 1 年、近 3 年、近 5 年。图表另有饼图和散点。导出是页内定时下载 | 无模板接口。核增 `report/jobs` 和全景 `benchmark-report` 不是这条 | 模板名只从 `gapfill_policy_eval_template` 的选用行读出。不迁两套演示模板，不迁三年周期，不收饼图和散点。格式保持 PDF、Excel |

## 4. 整体流程

1. 用户看趋势。前端向 `jobs` 提交，只要趋势。展示服务不建任务。`gkxlumen-element` 按所选的时间、区域或类别，以及所选指标名，读 `gapfill_policy_eval_trend`。无行则图空。重点和波动只标在读到的点上，不另算一条指标。
2. 用户看分区或群体。同一次入口，只要分区。展示服务不建任务。element 按地区、行业或群体读 `gapfill_policy_eval_partition`。图种不选则柱和热力都用这些行。投向对不上则该图空。
3. 用户看结构关联。本叶不发新的政策资源。子图能读到则只消费第 7 项已有结果，弦线图和关系网用同一份结果。读不到则该块空。传导路径没有单独的数据来源，子图里没有路径则路径空。
4. 用户选模板或导出。前端调 `shells`，种类为模板选用。element 只读 `gapfill_policy_eval_template`。行不齐则不能导出。要文件时，从这次读到的行生成 PDF 或 Excel，响应里不内嵌一份写死的文件。操作日志不灌。没有真实导出记录则日志空。

某一块读失败，不清空同页已经返回的短板条数和机遇条数。那两条不在本叶。

## 5. 分叶

### 5.1 219 多维指标趋势图 · 读缺项表

没有多维效能趋势模型。`M_POLICY_EFFECT_SCORE` 写入 `ads.policy_effect`。`M_POLICY_IMPLEMENTATION_EFFECT` 写入 `ads.policy_metric_timeseries`。效果分的需求来源在推演。这两条都不挂本叶，本叶也不调用 `effect.run`。全景时序 `M_POLICY_TIMESERIES` 不改挂到 219。

- 库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_trend`。不写入 ODS、DWD、ADS。
- 一行是一个趋势点：时间、区域或类别上的位置，评估指标名，一个对照值。列由 `POL-L2-DS11-VIZ-DATA` 定。
- 灌数是独立脚本，不是请求处理。执行单 `POL-L2-DS11-VIZ-GAPFILL-L01`。
- 浏览器仍提交 `jobs`。`gkxlumen-display` 不直连库，由 `gkxlumen-element` 只读这张表。不把查询转到 Python 现造一个点。
- 条件对不上行则图空，不在接口里补一段曲线。

### 5.2 220 分区/群体对比分析图 · 读缺项表

没有分区效果模型。全景分布类 STAT 不挂本叶。

- 表 `gapfill_policy_eval_partition`。不写入 ODS、DWD、ADS。
- 一行是一个对象上的对照：地区、行业或群体，以及一个对照数。资源投向若要筛，值写在行里，不另造指标。
- 同一张灌数单。本叶不执行。
- 柱和热力读同一批行。不建第三张可视化表。
- 表无行则图空。不返回演示矩阵。

### 5.3 221 多维结构关联图 · 跨项读图

本序号没有专属 `metric_id`。不挂 `M_POLICY_GRAPH_107_1`，不挂 `M_POLICY_RELATION_DEGREE`。前者留在全景区域差异，后者留在推演关联。

流程：不新开 `/display/v1/policy` 资源。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示只消费第 7 项已有子图，Java 不写 nGQL。挂接可空。

不做什么：不走 `E-E7-POLICY-M1-L06`。不把专题门面的 `/graph` 或算法中台的 `/v1/policy/graph` 改成展示浏览器地址。不重做抽取，不重开 GDF。不把共词网络写成新算法，不新造图指标。不把演示页的弦线矩阵和三条路径灌进缺项表。

### 5.4 222 报告模板定制与批量导出 · 读模板表

没有导出模型。核增研报 `report/jobs`（614–618）和全景 `benchmark-report` 不是这条资源。

模板选用不进 `gapfill_policy_eval_shell`。已会签的解读稿规定那张壳表只服务 224、225，行种类只有解读条目和多媒体条目，灌数单 `POL-L2-DS11-READ-GAPFILL-L01` 不灌模板。说明书第 11.2 节把模板选用写在解读 222–226 那一行。解读稿已收窄，本叶不把那一行再当作灌数依据，也不改写说明书和解读稿。

- 库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_template`。本叶建立。不写入 ODS、DWD、ADS。不把模板行拆进趋势表或分区表。
- 一行是一条模板选用：模板名，以及该模板可用的汇报周期、分析维度、图表类型。值落在第 3 节闭集里。列由 `POL-L2-DS11-VIZ-DATA` 定。
- 灌数单是 `POL-L2-DS11-VIZ-GAPFILL-L01`，与 219、220 同一张单。本叶不执行。不拿 224、225 的解读条目或多媒体条目充当模板行。
- 浏览器读 `GET shells`，种类为模板选用。`gkxlumen-element` 只读这张表。
- 没有选用行时，模板区空。不返回一套写死的模板。
- 导出要文件时，从这次读到的行生成。不写对象存储。不灌 PDF，不灌 Excel。
- 操作日志是用户自己的记录。不建日志缺项表，不灌假日志。没有真实导出则日志空。

`shells` 上的多媒体、互动意见、方案报告不在本二级展开。222 这一段为空时，不得用模板正文把整条 `shells` 填满。

## 6. 点名排除

| 资源或序号 | 不纳入本二级的原因 |
|---|---|
| `evaluation/counts` | 短板条数、机遇条数。序号不在 219–222 |
| `jobs` 上的焦点、摘要 | 解读二级。异步键只有 `policy_focus_ads`、`policy_text_parse`。不是趋势图 |
| `jobs` 上的路径与风险 | 序号 229。方案二级同步读 `gapfill_policy_eval_scheme`。不进异步。不是趋势图 |
| 效能得分 | 不在 219–222。本叶不改它的读法 |
| 224、225、227–231 | 解读和方案。224、225 的壳表行不是模板选用。230、231 读方案表。本叶只定 222 |
| `M_POLICY_TIMESERIES`、全景分布 | 指标分册写明不借给 219、220 |
| `M_POLICY_EFFECT_SCORE` | 需求来源在推演。不挂趋势图 |
| `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 不挂 221 |
| `compare/jobs`、`report/jobs`、`benchmark-report` | 核增对比、核增研报、全景对标报告 |

## 7. 明确不做

- 不写 OpenAPI 字段表。
- 不新造 `metric_id`。不改 D4。不改指标分册里 219、220、222 的「无模型」判定。
- 不增加 `/display/v1/policy` 的第 4 条路径。浏览器不改打专题 URL。
- 不重开 GDF，不写 nGQL。不加 ODS、DWD、ADS 表。本叶建立第 9 节的三张 `gapfill_` 表：趋势、分区、模板选用。不建立、不灌 `gapfill_policy_eval_shell`。
- 不在本叶展开参数名。输入条件只到第 3 节的闭集。
- 不在本叶改 Python 或 Java。
- 不允许接口函数直接返回 mock。不允许用 501 充当四叶的画面。
- 2026-11-03 首轮不同意。返工后第二轮四角色同意。待 `human:淮政玮` 签收。不把本单标 done。

## 8. 签收条件：可实现

四叶都有一条现在就能照着做的链路。写成「以后再选算法」，或者接口直接返回写死的曲线、矩阵、弦线或 PDF，本单不可签收。

| 序号 | 可实现的做法 | 现在就能用的代码或表 |
|---|---|---|
| 219 | 建 `gapfill_policy_eval_trend`。`jobs` 在只要趋势时不建任务，element 只查这张表 | 无趋势模型。效果评估和全景时序都不改挂 |
| 220 | 建 `gapfill_policy_eval_partition`。同一条入口的分区段只查这张表 | 无分区模型。不挂全景分布 |
| 221 | 不新开资源。有子图则只消费第 7 项，没有则该块空 | `E-E7-POLICY-M1-L02` 已完成。展示不写 nGQL |
| 222 | 建 `gapfill_policy_eval_template`。灌数单写入模板选用行。`shells` 按种类只查这张表。文件从行生成。不灌日志 | 无导出模型。不读解读壳表，不用 224、225 的行充当模板 |

迁移边界：算法中台页面留在 `demo-ui-system-test`。展示不嵌效果评估页，不打 `/v1/policy/graph`。专题 `/graph` 继续给专题自己用。展示不把 `effect.py` 抄进 Java，也不把 `policyData.js` 的常量写进接口。

## 9. 表与要灌的 mock

界面上要出现、而真实趋势、分区对照、模板选用还没有的内容，先写入表。接口只查询。D4 保持 mock。字段级 DDL 由数据分册定。本叶不执行灌数。

| 序号 | 库表 | 新建于本叶灌数单 | 要灌的 mock | 不灌 |
|---|---|---|---|---|
| 219 | `gkxlumenx_gapfill.gapfill_policy_eval_trend` | 是。`POL-L2-DS11-VIZ-GAPFILL-L01` | 时间、区域或类别上的趋势点，含指标名 | 全景时序、效果分、五维雷达、写死曲线 |
| 220 | `gkxlumenx_gapfill.gapfill_policy_eval_partition` | 是。同一张灌数单 | 地区、行业或群体的对照数。投向写在行里 | 全景分布、演示城市名单、新的效果指标 |
| 221 | 已有政策子图 | 否 | 不建表。无子图则空 | 弦线矩阵、演示路径、新的图指标 |
| 222 | `gkxlumenx_gapfill.gapfill_policy_eval_template` | 是。同一张 `POL-L2-DS11-VIZ-GAPFILL-L01` | 模板选用行：模板名，以及该行允许的汇报周期、分析维度、图表类型 | PDF、Excel、假操作日志、两套演示模板、解读条目、多媒体条目 |

缺项表的行要能按第 3 节的条件拣出来：219 按切换维和指标名，220 按对象和图种，投向有值时再按投向。222 按模板选用。条件对不上的行不返回。

`POL-L2-DS11-VIZ-GAPFILL-L01` 的执行人是 `data-agent`，监管 `human:淮政玮`，状态 backlog。它依赖本架构和 `POL-L2-DS11-VIZ-DATA`。这一张单覆盖 219、220、222 三张表。不灌 `gapfill_policy_eval_shell`。查询请求不灌数。
