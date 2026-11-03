# POL-L2-DS11-VIZ-METRIC · 政策分析评价 · 政策分析报告可视化呈现 · 后台指标设计

- 任务：`POL-L2-DS11-VIZ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（已认领，本叶不再认领，不改任务状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`。任务 `POL-L2-DS11-VIZ-ARCH` 经 `task-get` 为 `done`，note 为「淮政玮 2026-11-03 签收。四角色复会签同意。」会签页 `sdd/l2/会签/POL-L2-DS11-VIZ-SIGNOFF-ARCH.md` 复会签结论为「同意」。架构稿抬头仍写「会签未完成。未签收」。本叶不改那份抬头。读面以架构正文和该会签页为准
- 会签态：未会签。本叶不代签，不标 done
- 查询：2026-11-03 经 MCP `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改注册表，未改 D4

本叶只写政策分析评价二级「政策分析报告可视化呈现」的指标挂接。SRS 序号 **219–222**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-VIZ-ARCH.md`、`sdd/l2/会签/POL-L2-DS11-VIZ-SIGNOFF-ARCH.md`、`sdd/指标与501.md` 评价表 219–222 行、说明书第 2 节 DS-11 同序号。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

四叶都在政策分析评价里完成。指标身份沿说明书第 2 节与 `指标与501.md` 已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-VIZ-ARCH`。本叶不改那几份文件。

说明书第 2 节这四叶的拆解列，本叶不改字：

| 序号 | 说明书第 2 节拆解 |
|---|---|
| 219 | 501 |
| 220 | 501 |
| 221 | 跨项索引 |
| 222 | 501（交互壳，调研记未见） |

`指标与501.md` 评价表 219–222 的 `metric_id`、类型、D4、判定、真路径，本叶不改字：

| 序号 | metric_id | algorithm_type | D4 | 判定 | 真路径（原文） |
|---|---|---|---|---|---|
| 219 多维指标趋势图 | 未见 | 未见 | 未见 | 501 | 501，页面空态。不借用 `M_POLICY_TIMESERIES` |
| 220 分区/群体对比分析图 | 未见 | 未见 | 未见 | 501 | 501，页面空态。不挂全景分布类 STAT |
| 221 多维结构关联图 | 未见 | 未见 | 未见 | 跨项索引 | 真图归第 7 项。只索引 `E-E7-POLICY-M1-L02` done、`GDF-POLICY-GRAPH-EXT-L01` backlog。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` |
| 222 报告模板定制与批量导出 | 未见 | 未见 | 未见 | 501 | 501，页面空态。调研交互壳为「未见」。无指标，无导出模型，与核增研报无关 |

| 序号 | 叶子 | 本叶 |
|---|---|---|
| 219 | 多维指标趋势图 | 没有专属已注册模型。判定保持 501。读 `gapfill_policy_eval_trend`。不借用全景时序，不挂效果分。无行则图空 |
| 220 | 分区/群体对比分析图 | 没有专属已注册模型。判定保持 501。读 `gapfill_policy_eval_partition`。不挂全景分布。无行则图空 |
| 221 | 多维结构关联图 | `metric_id` 保持「未见」。判定保持「跨项索引」。只消费第 7 项已有子图。不新造图指标。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE` |
| 222 | 报告模板定制与批量导出 | 没有专属已注册模型。判定保持 501。调研交互壳为「未见」。读壳表里的模板选用行。无选用行则模板区空。不写导出公式 |

219、220、222 没有专属 `metric_id`。221 也没有专属 `metric_id`。本二级挂接 0 条已有指标。

`counts` 上的短板条数和机遇条数序号不在 219–222。本叶不读 `counts`，也不把趋势点或分区对照数写进那次响应。

## 2. 本二级用到的已有 metric_id

挂接去重后 **0** 条。

说明书第 2 节 219–222 没有给出可挂的 `metric_id`。`指标与501` 这四行的 `metric_id` 列都是「未见」。本叶不新造 `metric_id`，也不从全景、推演、页 KPI 或 `counts` 借一条来填这四格。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

本二级没有挂接已有 `metric_id`，因此没有可列的八件套。

第 6 节点名核对过的指标，注册公式都是过程指针：见各自 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄。本叶不手抄、不展开。不把那些指针改写成趋势斜率、分区对照、关联度、弦线或导出文件的计算式。

## 4. 接入状态

接入状态不是八件套。本二级没有挂上的指标，没有本叶要改的 D4。

第 6 节各条的 D4 都仍是 `mock`，`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。本叶不改任何一维，不把 mock 写成已上线。

架构稿写「219、220 的行是灌入的 mock，D4 仍是 `mock`」。这两叶没有专属 `metric_id`。本叶不新造 id 来承接这个 D4，也不把缺项行改成 live。`GDF-POLICY-MOCK-GATE-L01` 与这两张缺项表无关，本叶不改那道闸门。

## 5. 219–222 怎么读

读面沿架构稿与架构会签页，不新开路径，不新造指标。切时间、区域、类别不自动起任务。模型段失败时，不清空已经读到的趋势和分区。无行则空，不写假公式。接口不直接返回写死的 mock，也不用 501 这个词充当画面。

### 5.1 219 多维指标趋势图

没有专属已注册模型。`指标与501` 的判定是 501，真路径是「501，页面空态。不借用 `M_POLICY_TIMESERIES`」。说明书第 2 节拆解是「501」。本叶不改这些字。

没有多维效能趋势模型。全景时序、效果分、落地实效性都不改挂到 219。

读面沿已签收架构，只读缺项表，不在本叶定义怎么算出一个点：

1. 浏览器提交 `POST /display/v1/policy/evaluation/jobs`，只要趋势。
2. `gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python。
3. `gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_trend`。
4. 切换只有时间、区域、类别。指标名只来自缺项表里已有的名称。
5. 重点和波动只标在读到的点上。不另算一条指标。

无行则图空。不返回写死曲线，不用 501 充当一个数。不迁全景时序，不迁五维雷达。缺项行上的对照值不是已注册指标的计算结果。不写入 ODS、DWD、ADS。灌数单 `POL-L2-DS11-VIZ-GAPFILL-L01` 本叶不认领、不执行。列由 `POL-L2-DS11-VIZ-DATA` 定，本叶不写字段。

### 5.2 220 分区/群体对比分析图

没有专属已注册模型。`指标与501` 的判定是 501，真路径是「501，页面空态。不挂全景分布类 STAT」。说明书第 2 节拆解是「501」。本叶不改这些字。

没有分区效果模型。全国分布、类型分布、级别分布、深圳分布都不改挂到 220。效果分不挂本叶。

读面沿已签收架构：

1. 同一条 `POST /display/v1/policy/evaluation/jobs`，只要分区。展示服务不建任务，不调 Python。
2. `gkxlumen-element` 只读 `gapfill_policy_eval_partition`。
3. 对象只有地区、行业、目标群体。图种只有柱状、热力。图种不选则柱和热力都用这些行。
4. 资源投向若要筛，值写在缺项行里。投向对不上则该图空。不另造投向指标。

无行则图空。不返回演示矩阵。不迁全景分布，不迁演示城市名单。同一张灌数单，本叶不执行。不建第三张可视化表。不写入 ODS、DWD、ADS。

### 5.3 221 多维结构关联图

`metric_id` 保持「未见」。判定保持「跨项索引」。真路径保持原文：真图归第 7 项；只索引 `E-E7-POLICY-M1-L02` done、`GDF-POLICY-GRAPH-EXT-L01` backlog；不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。说明书第 2 节拆解是「跨项索引」。本叶不改这些字，也不把 221 改判成 501。

不新造图指标。不把共词网络写成新算法。

流程沿已签收架构：不新开 `/display/v1/policy` 资源。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示只消费第 7 项已有子图。Java 不写 nGQL。挂接可空。子图没有则弦线图、关系网和路径都空。传导路径没有单独的数据来源。

不走 `E-E7-POLICY-M1-L06`。不把专题门面 `/graph` 或算法中台 `/v1/policy/graph` 写成展示浏览器地址。不重做抽取，不重开 GDF。不把演示页的弦线矩阵和三条路径灌进缺项表。

### 5.4 222 报告模板定制与批量导出

没有专属已注册模型。`指标与501` 的判定是 501，真路径是「501，页面空态。调研交互壳为「未见」。无指标，无导出模型，与核增研报无关」。说明书第 2 节拆解是「501（交互壳，调研记未见）」。本叶不改这些字。

没有导出模型。本叶不写导出公式。模板选用行不是指标结果。

读面沿已签收架构：

1. 浏览器读 `GET /display/v1/policy/evaluation/shells`。
2. `gkxlumen-element` 只读 `gapfill_policy_eval_shell` 里的模板选用行。
3. 壳表由解读二级为 224、225 建立。`POL-L2-DS11-READ-GAPFILL-L01` 不灌模板选用。本叶不另建表，不把模板选用加进那张灌数单。
4. 无选用行则模板区空。
5. 要文件时，只沿架构从当次读到的行生成 PDF 或 Excel。响应里不内嵌一份写死的文件。不写对象存储。不灌 PDF，不灌 Excel。
6. 操作日志不灌。没有真实导出记录则日志空。

核增 `report/jobs` 和全景 `benchmark-report` 不是这条资源。`shells` 上的多媒体、互动意见、方案归档、分析报告份数不在本二级展开。222 这一段为空时，不得用模板正文把整条 `shells` 填满。

## 6. 点名不挂

下列 id 已用 `metric-get` 核对。本二级不挂。不改它们的 D4，不改 `srs_refs`，不手抄注册公式。全部 `is_mock=true`。除另行写出的条目外，`found.seed=true`、`found.matrix=true`、`found.srs_map=true`，D1=`aligned`，D2=`partial` 且 `d2_assessed=provisional`（待核验）。

| metric_id | 注册身份（metric-get） | 不挂 219–222 的原因 |
|---|---|---|
| `M_POLICY_TIMESERIES` | 政策时序指标；STAT；D3=`partial`；D4=`mock`。`d1_note` 含 QPOL-07。需求来源是展示 02/205、02/206 与专题 05/100；`page_ids` 为 `DS-10-POLICY-PANORAMA` | 全景时序。`指标与501` 219 的真路径写「不借用 `M_POLICY_TIMESERIES`」。本叶不改这句，不把时序改挂到趋势图 |
| `M_POLICY_EFFECT_SCORE` | 政策效果评分（王惠三维口径 v2 复现）；MODEL；D3=`partial`；D4=`mock`；QPOL-02。需求来源是展示 02/232、02/233 与专题 05/168。05/168 的 `page_ids` 含 `DS-11-POLICY-EVAL`、`DS-12-POLICY-SIM` | 效果分。架构稿写需求来源在推演，不挂趋势图。`指标与501` 把它放在页 KPI，真路径写展示侧需求来源在 232/233。本叶不把 05/168 的页码改成 219 的挂接 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性；MODEL；D3=`partial`；D4=`mock`；QPOL-02。注册判定完全不支持。需求来源是展示 02/209、02/235 与专题 05/168；`page_ids` 为 `DS-10-POLICY-PANORAMA`、`DS-12-POLICY-SIM`、`E7-POLICY` | 架构稿第 5.1 节把它和效果分一起写成效果评估所写的指标。没有多维效能趋势模型。需求来源不是 219。本叶不挂 |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布；STAT；D3=`full`；D4=`mock`。需求来源只有专题 05/100；`page_ids` 为 `DS-10-POLICY-PANORAMA` | 全景分布。架构稿第 3.1 节点名不挂本叶。不改挂到 220 |
| `M_POLICY_TYPE_DIST` | 政策类型分布；STAT；D3=`partial`；D4=`mock`；QPOL-01。需求来源只有专题 05/100；`page_ids` 为 `DS-10-POLICY-PANORAMA` | 全景分布。不改挂到 220 |
| `M_POLICY_LEVEL_DIST` | 政策级别分布；STAT；D3=`full`；D4=`mock`。需求来源只有专题 05/100；`page_ids` 为 `DS-10-POLICY-PANORAMA` | 全景分布。不改挂到 220 |
| `M_POLICY_SZ_DIST` | 深圳政策分布；STAT；D3=`partial`；D4=`mock`。需求来源只有专题 05/100；`page_ids` 为 `DS-10-POLICY-PANORAMA` | 同属全景分布类 STAT。架构稿第 3.1 节点名的是全国、类型、级别；深圳分布经本次 `metric-get` 核对后同样不挂 220 |
| `M_POLICY_GRAPH_107_1` | 政策实体关系抽取；GRAPH；D3=`partial`；D4=`mock`；`pending_ref=GAP-ALGO-TYPE-UNSIGNED`。需求来源是展示 02/208、02/239、02/240、02/549 与专题 05/107。没有 02/221 | 221 的真路径写明不挂这一条。它留在全景区域差异等已有序号。本叶不新造图指标，不签它的公式，Java 不写 nGQL |
| `M_POLICY_RELATION_DEGREE` | 政策关联度；GRAPH；D3=`partial`；D4=`mock`；QPOL-03；注册判定完全不支持。`found.srs_map=false`，`srs_refs` 为空 | 221 的真路径写明不挂这一条。`指标与501` 把它放在推演序号 240。本叶不为此新造图指标，不改 `srs_refs` |
| `M_POLICY_SHORTBOARD_COUNT` | 政策短板清单条数；STAT；D3=`partial`；D4=`mock`；QPOL-02。需求来源只有专题 05/169；`page_ids` 含 `DS-11-POLICY-EVAL`、`E7-POLICY`。没有 219–222 的序号 | `counts` 上的短板条数。`指标与501` 把它放在 223。本叶不读 `counts`，不把短板改挂到趋势或分区 |
| `M_POLICY_OPPORTUNITY_COUNT` | 政策机遇清单条数（王惠机遇计数 v2 全维复现）；STAT；D3=`partial`；D4=`mock`；QPOL-02。需求来源只有专题 05/170；`page_ids` 为 `DS-11-POLICY-EVAL`。没有 219–222 的序号 | `counts` 上的机遇条数。说明书写它没有 219–231 里的序号。本叶不读 `counts`，不把机遇改挂进这四叶 |

`metric-query`（域=政策，关键词「分布」）还返回 `M_POLICY_BASE_100_1`（政策基础指标模型构建；STAT；D4=`mock`；`found.seed=true`，`found.matrix=true`，`found.srs_map=true`）和 `M_POLICY_DEEP_167_1`（政策力度评估模型；MODEL；D4=`mock`；三侧 `found` 同为 true）。说明书第 2 节 219–222 没有这两个 id。本叶不挂，不把这次摘要查询写成八件套。

上述 id 的 `extras.algo_server_location` 指向 demo 仓 `polan/metrics/metrics.py` 与 `polan_metric_routes.py`。那是注册表索引。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

下列边界沿架构稿、架构会签页与 `指标与501`，本叶不改挂。下表 id 的三档以 `指标与501` 已有行为准，本叶不把它们当作 219–222 的挂接对象，因此不在此复述八件套：

| 对象 | 本叶 |
|---|---|
| 序号 223 焦点 `M_POLICY_FOCUS_INDEX` | 不挂。在 `jobs` 的异步段。判定在指标分册仍是 501 |
| 序号 223 短板、页 KPI 机遇 | 见上表。`counts` 不进本叶。某一块读失败，不清空同页已经返回的短板条数和机遇条数 |
| 序号 224、225、227–231 | 不挂。解读和方案不进这四叶。225、230、231 同在 `shells`，本叶只定 222 的模板选用 |
| 序号 226 `M_POLICY_DS_11_POLICY_EVAL_012` | 不挂。摘要在 `jobs` 上，不是趋势图 |
| 序号 229 `M_POLICY_DS_11_POLICY_EVAL_015` | 不挂。实施路径不进 219–222 |
| 页 KPI 效能得分 | 见上表 `M_POLICY_EFFECT_SCORE`。不挂趋势图 |
| `compare/jobs`、`report/jobs`、`benchmark-report` | 核增对比、核增研报、全景对标报告。不是 222 |
| 门户或算法中台的效果评估页、`/v1/policy/graph`、专题 `/graph` | 展示不嵌这些页，不把它们改成浏览器地址 |

QPOL-01、QPOL-02、QPOL-03、QPOL-07 与 `GAP-ALGO-TYPE-UNSIGNED` 本叶都不闭合，都不签公式。D2 的 provisional 保留「待核验」，不在本叶改绿。

## 7. 偏离

任务 DoD 写「未注册模型保持 501」。说明书第 2 节和 `指标与501.md` 对 219、220、222 的判定列就是 501，`metric_id` 列是「未见」。本叶保持这三档，不改字，不写成可算公式。

221 的判定列是「跨项索引」，说明书拆解列也是「跨项索引」。本叶保持这个字。不把 221 改判成 501，也不新造图指标。

已签收架构把 219、220、222 的功能空态收成读表：有行则读，无行则空。221 有子图则只消费，没有则空。接口不直接返回写死的 mock，也不用 501 这个词充当返回值。本叶按签收写读面，同时不把「读表」或「消费子图」写成一条新公式，也不改指标分册的判定列。

- 219：判定保持 501。真路径保持「不借用 `M_POLICY_TIMESERIES`」。无行则图空。
- 220：判定保持 501。真路径保持「不挂全景分布类 STAT」。无行则图空。
- 221：判定保持「跨项索引」。不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。不新造图指标。
- 222：判定保持 501。调研交互壳为「未见」。无指标，无导出模型。无选用行则模板区空。

本叶未会签。不把本单标 done。不改任务状态。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式。不把 219、220、222 的 501 改写成可算公式。221 不新造图指标。无行则空。
- 不借用全景时序 `M_POLICY_TIMESERIES`。不挂效果分 `M_POLICY_EFFECT_SCORE`，不挂 `M_POLICY_IMPLEMENTATION_EFFECT`。
- 不挂全景分布 `M_POLICY_NATIONAL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_SZ_DIST`。
- 不挂 `M_POLICY_GRAPH_107_1`、`M_POLICY_RELATION_DEGREE`。
- `counts` 上的短板 `M_POLICY_SHORTBOARD_COUNT` 和机遇 `M_POLICY_OPPORTUNITY_COUNT` 不进本叶。
- 不闭合 QPOL-01、QPOL-02、QPOL-03、QPOL-07，不签 `GAP-ALGO-TYPE-UNSIGNED`，不把 D2 provisional 改绿。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓与 vendor 里的计算文件。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开，不把 `GDF-POLICY-GRAPH-EXT-L01` 写成已完成。
- 不改说明书、`指标与501.md`、架构稿、会签页、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。不写代码。
- 不会签。不把本单标 done。不改任务状态。
