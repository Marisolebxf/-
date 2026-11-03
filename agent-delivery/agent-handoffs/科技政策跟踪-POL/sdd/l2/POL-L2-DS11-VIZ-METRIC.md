# POL-L2-DS11-VIZ-METRIC · 政策分析评价 · 政策分析报告可视化呈现 · 后台指标设计

- 任务：`POL-L2-DS11-VIZ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`（2026-11-03 返工后第二轮，架构、算法、数据、产品四角色同意，待 `human:淮政玮` 签收。本叶以它的读面为准，不代签，不改它）。本叶会签态 `draft`，不标 done
- 查询：未见 metric MCP。本叶未调用 `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改注册表。下文凡未标明出处的身份字段，都不要当成已经查过
- 代码核对：只读。`lumen-algo-py/vendor/entan-py/polan/eval/effect.py` 的写表位置；`lumen-svc-platform` 里 `gkxlumen-topic-async-service` 的 `PolicyAnalysisTypes` 白名单。另核对 `polan/text/simulate.py` 的写入目标，只为确认本叶不调用。不改算法代码

本叶只写政策分析评价二级「政策分析报告可视化呈现」的指标挂接。SRS 序号 **219–222**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`、`sdd/指标与501.md` 评价表 219–222 行、`sdd/l2/POL-L2-DS11-READ-METRIC.md`（篇章样板，不改）。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

四叶都在政策分析评价页的可视化区里完成。挂接沿 `指标与501.md` 评价表 219–222 行。读面沿 `POL-L2-DS11-VIZ-ARCH`。本叶不改那两份文件，也不把调研判定列改写成另一档。

| 序号 | 叶子 | 指标与501 | 本叶 |
|---|---|---|---|
| 219 | 多维指标趋势图 | 未见 `metric_id`；判定列 501。真路径写明不借用 `M_POLICY_TIMESERIES` | 不新注册。没有趋势模型。页面读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。无行则图空。不用 501 充当画面。不挂时序、效果分、落地实效 |
| 220 | 分区/群体对比分析图 | 未见 `metric_id`；判定列 501。真路径写明不挂全景分布类 STAT | 不新注册。没有分区模型。页面读 `gapfill_policy_eval_partition`。无行则图空。不用 501 充当画面。不挂全景分布 |
| 221 | 多维结构关联图 | 未见 `metric_id`；判定列跨项索引。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` | 不新注册。跨项只消费第 7 项已有子图。不建表。子图没有则该块空 |
| 222 | 报告模板定制与批量导出 | 未见 `metric_id`；判定列 501。调研交互壳为「未见」。无指标，无导出模型 | 不新注册。没有导出模型。页面读 `gapfill_policy_eval_template`。无行则模板空。不用 501 充当画面 |

219、220、222 仍无专属模型，也无专属 `metric_id`。`指标与501` 把这三叶的判定列写成「501，页面空态」。那是调研判定。架构规定这三叶读缺项表：有行则读表，无行则空，不用 501 充当这四叶的画面。本叶采用这条读面，不回头改 `指标与501`。221 的判定列是跨项索引，本叶不改成 501，也不改成可接统计读面。

缺项表里灌入的行仍是 mock。本叶不把 mock 写成已上线，也不给这三张表新造一个可改的 D4。`GDF-POLICY-MOCK-GATE-L01` 与趋势表、分区表无关，本叶不改那道闸门。

本二级挂接 0 条已有 `metric_id`。

## 2. 本二级用到的已有 metric_id

没有。219、220、222 在评价表里 `metric_id` 为未见。221 的判定是跨项索引，评价表同样未见专属 `metric_id`。类型和 D4 只转述 `指标与501.md` 已有行，以及架构稿里写明的同一事实。不是 `metric-get` 的返回。

| 序号 | metric_id | 中文名 | algorithm_type | D4 | 挂接 |
|---|---|---|---|---|---|
| 219 | （无） | — | — | 无专属指标，不改 D4 | 不挂 |
| 220 | （无） | — | — | 无专属指标，不改 D4 | 不挂 |
| 221 | （无） | — | — | 无专属指标，不改 D4 | 不挂。只消费子图 |
| 222 | （无） | — | — | 无专属指标，不改 D4 | 不挂 |

这 4 叶之内不把已有号改挂进来。这 4 叶之外，本二级不新造 `metric_id`。

行上的名称不是注册号：

- 219 的评估指标名只来自 `gapfill_policy_eval_trend` 里已有的名称。它是缺项行上的名字，不是新的 `metric_id`。本叶不把这些名字登记成指标。
- 220 的对象和资源投向只来自 `gapfill_policy_eval_partition` 里已有的值。投向写在行里，不另造指标。
- 222 的模板名只来自 `gapfill_policy_eval_template` 的选用行。模板名不是 `metric_id`。

指不到专属 id。不把第 7 节点名排除的号写进这三张缺项表。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进八件套。

本二级没有挂上的 `metric_id`，因此不列八件套全表。不手抄公式，也不另写一条能算出趋势、分区对照、关联或导出文件的式子。

未见 metric MCP。被点名排除的号，下列各项保持注册表原样，本叶不改、不抄、不补：

- 注册中文名
- 口径（`definition`）
- 注册公式
- 注册源表
- 源系统
- 更新频率
- `version`

已定稿架构规定的是读哪张表或哪张子图，不是注册源表。读表只说明展示从哪里取数。无行则空。查询函数自己不拼趋势点、不拼分区对照、不拼弦线、不拼文件。

| 序号 | 本叶能写的身份 | 读面（架构稿，不是注册源表） | 本叶不写的 |
|---|---|---|---|
| 219 | 无专属 `metric_id`。判定列仍是 501，不改。没有可改的 D4 | `gkxlumenx_gapfill.gapfill_policy_eval_trend`。`jobs` 只要趋势，不建任务 | 注册中文名、口径、公式、注册源表、源系统、更新频率、`version` |
| 220 | 同上 | `gapfill_policy_eval_partition`。`jobs` 只要分区，不建任务 | 同上 |
| 221 | 无专属 `metric_id`。判定列仍是跨项索引，不改 | 第 7 项已有子图。不新开 `/display/v1/policy` 资源 | 同上。不新造图指标的公式 |
| 222 | 无专属 `metric_id`。判定列仍是 501，不改。没有可改的 D4 | `gapfill_policy_eval_template`。`shells` 种类为模板选用 | 同上 |

## 4. 接入状态

接入状态不是八件套。未见 metric MCP，本叶不写 D1、D2、D3，也不写 `d2_assessed`、`is_mock` 的注册布尔、`d4_note`、`srs_refs`、`lifecycle_stage`。这些字段没有查到，不能补成 `aligned`、`partial`、`full` 或空引用。

219、220、222 没有专属 `metric_id`。没有可改的 D4。221 也没有专属 `metric_id`，没有可改的 D4。缺项表里灌入的行仍是 mock。本叶不把缺项写成已上线，不把 D4 升成 live。

被排除的号，D4 只转述 `指标与501` 已有行，本叶不改。见第 7 节。它们的 D1–D3 本叶都未用 metric MCP 核对，不补维度。

## 5. 219、220、222 怎么读

读面沿架构稿。三叶都没有专属模型。页面读缺项表。不把 501 当成画面。不调用 `effect.run`，不调用 `simulate.run`。

浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python，不写算法。219、220 走 `POST /display/v1/policy/evaluation/jobs`，一次请求只带一种类：趋势或分区。这两种都不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。222 走 `GET /display/v1/policy/evaluation/shells`，种类为模板选用。参数名留给 `POL-L2-DS11-VIZ-API`，本叶不展开。

### 5.1 219 多维指标趋势图

没有多维效能趋势模型。`指标与501`：未见 `metric_id`，判定列 501，不借用 `M_POLICY_TIMESERIES`。判定列不改。

读面：`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。一行是一个趋势点。条件对不上行则图空，不在接口里补一段曲线。重点和波动只标在读到的点上，不另算一条指标。不写入 ODS、DWD、ADS。

灌数单是 `POL-L2-DS11-VIZ-GAPFILL-L01`。本叶不执行，不认领。查询请求不灌数。

不挂 `M_POLICY_TIMESERIES`。不挂 `M_POLICY_EFFECT_SCORE`。不挂 `M_POLICY_IMPLEMENTATION_EFFECT`。不把全景时序、效果分、五维雷达迁进这张缺项表。

### 5.2 220 分区/群体对比分析图

没有分区效果模型。`指标与501`：未见 `metric_id`，判定列 501，不挂全景分布类 STAT。判定列不改。

读面：同一次 `jobs` 入口，只要分区。`gkxlumen-element` 只读 `gapfill_policy_eval_partition`。柱和热力读同一批行。不建第三张可视化表。表无行则图空，不返回演示矩阵。不写入 ODS、DWD、ADS。

同一张灌数单。本叶不执行。

不挂全景的全国分布、类型分布、级别分布。对应已有号是评价表之外、全景表里已经写下的 `M_POLICY_NATIONAL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`。它们留在全景。本叶不改挂，不改它们的 D4。

### 5.3 222 报告模板定制与批量导出

没有导出模型。`指标与501`：未见 `metric_id`，判定列 501。调研把交互壳记为「未见」，详设没有可调用模型，所以写 501。判定列不改。读面按架构：不用 501 充当这块功能。

读面：`GET shells`，种类为模板选用。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_template`。一行是一条模板选用。没有选用行时模板区空，不返回一套写死的模板。要文件时，从这次读到的行生成 PDF 或 Excel。不写对象存储。不灌 PDF，不灌 Excel。操作日志不灌。没有真实导出记录则日志空。

模板选用不进 `gapfill_policy_eval_shell`。那张壳表只服务 224、225。不拿解读条目或多媒体条目充当模板行。不走核增 `report/jobs`，不走全景 `benchmark-report`。

灌数与 219、220 同一张 `POL-L2-DS11-VIZ-GAPFILL-L01`。本叶不执行。

### 5.4 效果分与落地实效的写表位置

2026-11-03 只读 `vendor/entan-py/polan/eval/effect.py` 的 `run()`。它先按 `scope_type='region_effect'` 删除再插入 `ads.policy_effect`，行上 `metric_id` 为 `M_POLICY_EFFECT_SCORE`。随后按 `metric_id='M_POLICY_IMPLEMENTATION_EFFECT'` 删除再插入 `ads.policy_metric_timeseries`。落地实效在时序表，不在效果分那一行的 `metric_id` 上。

这两处写入都不挂本叶。219 不读这两张 ADS 表来画趋势。220、221、222 也不读。本叶不调用 `effect.run`。不把 `run()` 收成一条新公式，不改它的删除范围。`ext` 里已有的 `is_mock` 与 `QPOL-02` 留在那两次写入上。本叶不闭合 `QPOL-02`，不把 `is_mock` 改成已上线。

`指标与501` 能确认的身份，只转述、不改：

| metric_id | 出处 | algorithm_type | D4 | 本叶 |
|---|---|---|---|---|
| `M_POLICY_EFFECT_SCORE` | 评价表页 KPI · 效能得分。需求来源在推演序号 232/233 | MODEL | mock | 不挂 219–222。不改 D4 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 全景表序号 209 | MODEL | mock | 不挂 219–222。不改 D4 |

页上效能得分不在 219–222。本叶不改它的读法。

### 5.5 `simulate.run` 不调用

2026-11-03 只读 `vendor/entan-py/polan/text/simulate.py` 的 `run()`。它写入 `ads.policy_simulate`，行上 `metric_id` 固定 `M_POLICY_SIMULATE`。`指标与501` 把该号放在推演序号 232、233，并写明需求来源不在序号 219–231 的那些号不进入评价表。本叶不调用 `simulate.run`，不把推演曲线当成 219 的趋势图，不把该号挂进 219–222。

### 5.6 `PolicyAnalysisTypes` 白名单

2026-11-03 只读 `PolicyAnalysisTypes.java`。类在 `lumen-svc-platform` 的 `gkxlumen-topic-async-service`。`CANONICAL` 九键是 `policy_timeseries`、`policy_regional`、`policy_shenzhen`、`policy_focus`、`policy_effect`、`policy_match`、`policy_intensity`、`policy_focus_ads`、`policy_text_parse`。`WHITELIST` 是这九键，加上已有别名 `timeseries`、`regional`、`focus`、`policy:timeseries`、`policy:regional`、`policy:shenzhen`、`policy:focus`、`policy_sz_3d`、`policy:recommendation:policy_sz_3d`。不注册内部 `policy_shard`。

其中没有趋势图、分区对比、模板导出、弦线或关系网。219、220、222 不进入这些键。219、220 的 `jobs` 不建任务、不进异步服务，因此不经过这份白名单。222 走 `shells`，也不进这份白名单。

`policy_effect` 留在白名单里，服务效果分的既有转发。本叶不把它改挂成 219 的趋势键，不调用 `effect.run`，不增删任何键。`policy_timeseries`、`policy_regional` 留给全景时序和区域对比，不借给 219、220。`policy_focus_ads`、`policy_text_parse` 留给解读二级，不借给本四叶。

## 6. 221 跨项只消费子图

221 在 `指标与501` 里 `metric_id` 为未见，判定列跨项索引。真图归第 7 项。本叶不新注册，不改判定列。

没有专属模型，也没有专属 `metric_id`。不挂 `M_POLICY_GRAPH_107_1`，不挂 `M_POLICY_RELATION_DEGREE`。前者留在全景序号 208 区域政策差异性分析。后者留在推演序号 240 政策关联分析。两个号的 D4 本叶都不改。

流程：不新开 `/display/v1/policy` 资源。不建缺项表。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示只消费第 7 项已有子图。Java 不写 nGQL。挂接可空。弦线图和关系网用同一份结果。子图没有则两图都空。传导路径没有单独的数据来源，子图里没有路径则路径空。

不把 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` 写进任何本叶缺项表。不把演示页的弦线矩阵和三条路径灌进缺项表。不把共词网络写成新算法。不新造图指标。不走 `E-E7-POLICY-M1-L06`。不把专题门面 `/graph` 或算法中台 `/v1/policy/graph` 改成展示浏览器地址。不调用 `focus.run` 来给 221 取关联度。

`指标与501` 对这两个号已写下的类型和 D4，本叶只转述：

| metric_id | 出处 | algorithm_type | D4 | 本叶 |
|---|---|---|---|---|
| `M_POLICY_GRAPH_107_1` | 全景表序号 208 | GRAPH | mock | 不挂 221。不改 D4 |
| `M_POLICY_RELATION_DEGREE` | 推演表序号 240 | GRAPH | mock | 不挂 221。不改 D4 |

## 7. 点名不挂

下列号或序号在架构稿或 `指标与501` 里已经出现。本二级不把它们改挂到 219–222，也不改它们的 D4。身份未经过 metric MCP。下表只写本叶能从这两份已有文字，以及第 5 节核对过的写表位置里确认的内容。

| 号或序号 | 已有文字里能确认的 | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_TIMESERIES` | 全景表 198、205、206：STAT，D4=`mock`。205 趋势、206 时间轴挂这一条 | 219 的真路径写明不借用。全景时序不改挂到趋势图 |
| `M_POLICY_EFFECT_SCORE` | 评价表页 KPI：MODEL，D4=`mock`，判定 501。需求来源在推演 232/233。`effect.run` 写入 `ads.policy_effect` 且 `scope_type=region_effect` | 不在 219–222。不挂趋势图。本叶不调用 `effect.run` |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 全景表 209：MODEL，D4=`mock`，判定 501。`effect.run` 写入 `ads.policy_metric_timeseries` | 落地实效不是 219 的趋势点。不挂本四叶 |
| `M_POLICY_NATIONAL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST` | 全景表 197、198 等：STAT，D4=`mock`。架构稿点名全国分布、类型分布、级别分布 | 全景分布类 STAT。不挂 220 |
| `M_POLICY_GRAPH_107_1` | 全景表 208：GRAPH，D4=`mock`，跨项索引 | 留在区域政策差异性分析。不挂 221 |
| `M_POLICY_RELATION_DEGREE` | 推演表 240：GRAPH，D4=`mock`，跨项索引 | 留在政策关联分析。不挂 221。不为此新读图 |
| `M_POLICY_SIMULATE` | 推演表 232、233：MODEL，D4=`mock`。`simulate.run` 写入 `ads.policy_simulate` | 需求来源不在 219–231。本叶不调用 `simulate.run` |
| `policy_effect` 白名单键 | `PolicyAnalysisTypes.EFFECT` | 效果分的既有转发。不改成 219 的键 |
| `policy_timeseries`、`policy_regional` | 白名单已有 | 不借给 219、220 |
| `evaluation/counts` | 短板条数、机遇条数 | 序号不在 219–222 |
| 223–226 | 解读二级 | 不收进本叶。壳表不充当 222 的模板 |
| 227–231 | 方案二级 | 不收进本叶 |
| `compare/jobs`、`report/jobs`、`benchmark-report` | 核增对比、核增研报、全景对标报告 | 不是 222 |

上表各号的 D1–D3 未查。本叶只核对「不改挂、不改 D4」，不展开它们的计算。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不把 219、220、222 的「无模型」改成已有模型。不把 221 的跨项索引改成另一档。
- 不把 501 当成四叶的画面。有行读表，无行则空。221 无子图则空。
- 不挂 `M_POLICY_TIMESERIES`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、全景分布、`M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。
- 不调用 `effect.run`，不调用 `simulate.run`。不把这两处写入收成新公式。
- 不把 `PolicyAnalysisTypes` 加上趋势、分区、导出键。不改白名单。
- 不手抄注册公式。不见 metric MCP 就不填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3、`srs_refs`。
- 不改算法代码，不改 `effect.py`、`simulate.py`、`PolicyAnalysisTypes.java`。
- 不改 `指标与501.md`、`POL-L2-DS11-VIZ-ARCH.md`、`POL-L2-DS11-READ-METRIC.md`、说明书、PLAN、WBS、指标 seed 与矩阵。
- 不写 OpenAPI 字段、请求体、响应体、枚举。
- 不执行 `POL-L2-DS11-VIZ-GAPFILL-L01`。不灌 PDF、Excel、假日志、弦线矩阵。
- 不会签。不把本单标 done，也不标 `ready_to_sign`。
