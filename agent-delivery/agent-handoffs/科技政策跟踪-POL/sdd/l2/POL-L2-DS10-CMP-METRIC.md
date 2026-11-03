# POL-L2-DS10-CMP-METRIC · 科创政策全景 · 政策重点比对 · 后台指标设计

- 任务：`POL-L2-DS10-CMP-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（已认领，本叶不再认领，不改任务状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-04`
- 上游：`sdd/l2/POL-L2-DS10-CMP-ARCH.md`（2026-11-03 已签收，签收人 human:淮政玮，本叶读面以该稿为准）
- 会签态：未会签。本叶不代签，不标 done
- 查询：2026-11-03 经 MCP `metric-get`。未读 seed、矩阵 YAML，未改注册表，未改 D4

本叶只写科创政策全景二级「政策重点比对」的指标挂接。SRS 序号 **213–218**。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-CMP-ARCH.md`、`sdd/指标与501.md` 全景表 213–218 行、说明书第 2 节 DS-10 同序号、`sdd/l2/POL-L2-DS10-QRY-METRIC.md` 与 `sdd/l2/POL-L2-DS10-SENT-METRIC.md`（分册结构）。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

六叶都在全景比对工作区里完成。指标身份沿说明书第 2 节与 `指标与501.md` 已有 `metric_id`。读面沿已签收的 `POL-L2-DS10-CMP-ARCH`。本叶不改那几份文件。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 213 | 政策新旧对比 | 未见 `metric_id`；判定列 501 | 不新注册，不写公式。页面读 `gapfill_policy_version_diff` 的行。行内文字不是指标结果 |
| 214 | 政策详情对比 | `M_POLICY_INTENSITY_SCORE`；MODEL；D4=`mock`；判定列 501 | 只挂这一条。走 `jobs`。未接通则该格空，不补演示分。不挂力度指数 |
| 215 | 部门政策对比 | `M_POLICY_TOTAL_COUNT`；STAT；D4=`mock`；可接统计读面 | 只挂这一条。部门件数留在缺项表，不登记成新指标 |
| 216 | 标杆比对功能 | `M_POLICY_SUPPORT_STRENGTH`；COMPUTE；D4=`mock`；可接统计读面 | 只挂这一条。同步 `stats`，不进 Job。金额档缺失则该维空 |
| 217 | 对标报告生成与导出 | 未见 `metric_id`；判定列 501 | 不新注册，不写公式。页面读 `gapfill_policy_benchmark_report` 的行。行内文字不是指标结果 |
| 218 | 对标结果可视化展示 | `M_POLICY_INTENSITY_SCORE`；MODEL；D4=`mock`；判定列 501 | 只挂这一条。走 `jobs`。未接通则图空，不补演示分。不挂力度指数 |

215、216 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

## 2. 本二级用到的已有 metric_id

挂接去重后 3 条，落在 214、215、216、218。213、217 不在此表。全部 `metric-get` 为 `found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D4 都是 `mock`。中文名、`algorithm_type` 以 MCP 为准。

| metric_id | 中文名（MCP） | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_INTENSITY_SCORE` | 政策力度评分 | MODEL | mock | 214、218 |
| `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | mock | 215 |
| `M_POLICY_SUPPORT_STRENGTH` | 支持力度 | COMPUTE | mock | 216 |

这 3 条之外，本二级不新造 `metric_id`。

叶子名与注册中文名不一致的，以 MCP 为准，挂接 id 不变：

- 214、218 的叶子名是「政策详情对比」「对标结果可视化展示」。注册中文名是「政策力度评分」。
- 216 的叶子名是「标杆比对功能」。注册中文名是「支持力度」。类型仍是 COMPUTE。214 不把这一条改挂进来，也不把 214 改判成统计读面。

`M_POLICY_TOTAL_COUNT` 在检索叶序号 197、舆情叶序号 207 上已有挂接。本叶只在 215 使用它，不拆掉那两处，也不改 `srs_refs`。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

源系统三条相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_INTENSITY_SCORE` | 政策力度评分 | MODEL | `dwd_bid_`、`dwd_global_policy_base`、`dwd_global_policy_base_bak_20260923`、`dwd_policy_base`、`dwd_policy_base_bak_20260923` | weekly |
| `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_SUPPORT_STRENGTH` | 支持力度 | COMPUTE | `dwd_bid_`、`dwd_policy_base` | weekly |

三条注册公式都是同一类过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/<metric_id>.py` 为准。注册指针分别为 `metrics/calc-logic/POLICY/M_POLICY_INTENSITY_SCORE.md`、`metrics/calc-logic/POLICY/M_POLICY_TOTAL_COUNT.md`、`metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md`。本叶不手抄、不展开成可执行式，也不另写一条能算出数的式子。

口径按 `metric-get` 的 `kit.definition` 摘录，不改写。政策总数的摘录与 `POL-L2-DS10-QRY-METRIC` 第 3 节相同。

| metric_id | 口径 |
|---|---|
| `M_POLICY_INTENSITY_SCORE` | 五项子指标要 `implementation_date`、`policy_support.support_way`、`policy_support.support_object`、`policy_support.support_behavior`，外加 `district`。前四个全部为空，只有 `district` 有值。效果维与成本维整块空，覆盖维不完整。按正本「缺维不进平均」，可进平均的维为 0，分数不存在。注册判定为完全不支持。口径标记 QPOL-02，本叶不改口径，不闭合 |
| `M_POLICY_TOTAL_COUNT` | 政策总数就是底表行数。主键 `id` 无重复，`is_deleted` 全 0，`COUNT(*)` 与 `COUNT(DISTINCT id)` 相等。库内没有现成汇总表，由一条聚合生成。注册判定为完全转换支持 |
| `M_POLICY_SUPPORT_STRENGTH` | 三维里「扶持力度档位」要金额或档位字段。政策表没有金额类列，`policy_support` 全为 JSON null。政策层级与政策数量两维可从 `rank`、`city` 算。三维缺金额档这一维。注册判定为部分支持。口径标记 QPOL-02，本叶不改口径，不闭合，不补档位 |

214、218 的展示读数不在接口里重算，也不替换上表的注册公式。已签收架构指认仓库里已有的 `lumen-algo-py/vendor/entan-py/polan/eval/intensity.py` 的 `run()`，写入 `ads.policy_intensity`。本叶不重写该函数，不抄公式进 Java。

`extras.algo_server_location` 指向 demo 仓 `polan/metrics/metrics.py` 与 `polan_metric_routes.py`。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。D1 都是 `aligned`，D2 都是 `partial` 且 `d2_assessed=provisional`（待核验），D4 都是 `mock`。本叶不改任何一维。D2 的 provisional 保留「待核验」，不在本叶改绿。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_INTENSITY_SCORE` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_TOTAL_COUNT` | aligned | partial，待核验 | full | mock |
| `M_POLICY_SUPPORT_STRENGTH` | aligned | partial，待核验 | partial | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。本叶不改 D4。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_INTENSITY_SCORE` | 展示 02/214 政策详情对比；展示 02/218 对标结果可视化展示；专题 05/167 政策力度评估模型 | 214 与 218。同一条力度评分，不拆成按图种的新指标 |
| `M_POLICY_TOTAL_COUNT` | 展示 02/215 部门政策对比；专题 05/100 基础指标 | 只挂 215。197、207 的复用留在原叶，本叶不改 `srs_refs` |
| `M_POLICY_SUPPORT_STRENGTH` | 展示 02/216 标杆比对功能；专题 05/167 政策力度评估模型 | 只挂 216。不改挂到 214 或 218 |

## 5. 214、215、216、218 怎么读

读面沿架构稿，不新开路径，不新造指标。

### 5.1 214 政策详情对比

只挂 `M_POLICY_INTENSITY_SCORE`。MCP：中文名「政策力度评分」，MODEL，D4=`mock`，QPOL-02。

力度分走 Job，与舆情叶的效果、匹配同一条管道，`sub_type=policy_intensity`：

1. 浏览器提交 `POST /display/v1/policy/panorama/jobs`。
2. `gkxlumen-display` 调用已有 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`。display 不打分，也不直接调 `jobs/execute`。
3. 已有 `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`。Python 调用已有 `polan.eval.intensity.run`，再按所选政策读 `ads.policy_intensity` 的力度分。

申报时间、受理部门、产业类别读专题门面已有正文。这三列不是本条指标，也不进缺项表。受理部门不是 215 的实施部门。

申报条件、申报材料读 `gkxlumenx_gapfill.gapfill_policy_detail_compare`。浏览器仍走 `GET /display/v1/policy/panorama/{id}/detail`，这两列由 `gkxlumen-element` 只读带出。行内文字是缺项正文，不是指标结果。本叶不给这两列补 `metric_id`，也不写一条条件分或材料分。

`sub_type` 尚未放行，或 `run()` 因缺维写不出力度分时，该格空。不补演示分。D4 保持 mock。QPOL-02 的权重保持待确认。

### 5.2 215 部门政策对比

只挂 `M_POLICY_TOTAL_COUNT`。MCP：中文名「政策总数」，STAT，D4=`mock`，D3=`full`。

总件数走已有 `GET /display/v1/policy/panorama/stats`，由 `gkxlumen-display` 委托已有 `gkxlumen-topic-policy`。本叶不另建一条总数查询。无行则该统计空，不造 0。D4 保持 mock。

区域走已有地区分布。项目类别、技术类别走已有政策类型和产业节点。这三段是目录条件，没有独立 `metric_id`。

实施部门、方面、部门件数、清单标题在 `gapfill_policy_impl_dept`。`gkxlumen-element` 在同一次 `stats` 里把这些行带出。部门件数是缺项行上的字段，不登记成新指标，也不改挂成 `M_POLICY_TOTAL_COUNT`。清单标题是行内文字，不是指标结果。表无行则部门对比空。门户扶持十条不是本页任务。

### 5.3 216 标杆比对功能

只挂 `M_POLICY_SUPPORT_STRENGTH`。MCP：中文名「支持力度」，COMPUTE，D4=`mock`，QPOL-02。

同步读，不进 Job：

- 浏览器读 `GET /display/v1/policy/panorama/stats`。
- `gkxlumen-element` 只读 `ads.policy_intensity` 里已经写下的支持力度。
- 写入仍由已有 `intensity.run()` 完成。这次统计请求不现算，也不把这一行放进 `POL-L2-DS10-CMP-GAPFILL-L01`。

对标范围、对标对象、勾选字段是这次查询的条件。金额档缺失则该维空，不补档位。无行则该卡空。对标报告正文在 217，不在本叶生成。D4 保持 mock。

### 5.4 218 对标结果可视化展示

只挂 `M_POLICY_INTENSITY_SCORE`，与第 5.1 节同一条。MODEL，D4=`mock`。

雷达、柱、热力走与 214 相同的 `jobs`，`sub_type=policy_intensity`，读 `ads.policy_intensity` 上该指标已写入的力度分。不建 `gapfill_policy_benchmark_viz`。`sub_type` 尚未放行或表无行时，图空，不返回演示序列。D4 保持 mock。

216 的支持力度仍只挂在 216。本行不把 `M_POLICY_SUPPORT_STRENGTH` 改挂进来。图上若只画件数，沿架构稿用 215 的目录命中，不把件数改挂成力度分，也不把本行改判成 STAT。`指标与501` 写「另见序号 197」，本叶不改那份文件。

## 6. 213、217 没有已挂指标

213、217 在说明书第 2 节和 `指标与501` 里 `metric_id` 为未见。本叶不新注册，不写能算出数的公式。页面读缺项表行。行内文字不是指标结果。

### 6.1 213 政策新旧对比

没有已挂 `metric_id`。没有版本对比模型。

读面是 `GET /display/v1/policy/panorama/version-diff`。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_version_diff`。一行是同一政策的一个变更：两个发布时间、变更类型（新增、修改、删除）、一句摘要。时点就是该政策的发布时间。

页面展示这些行。增、改、删和摘要是行上的文字。本叶不把行数、变更类型或摘要写成指标结果，也不新造「变化统计」指标。两个发布时间对不上行则对比空。本叶不灌数。灌数单 `POL-L2-DS10-CMP-GAPFILL-L01` 本叶不认领。

### 6.2 217 对标报告生成与导出

没有已挂 `metric_id`。没有对标报告模型。

读面是 `GET /display/v1/policy/panorama/benchmark-report`。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_benchmark_report`。一行有对标对象、对照字段、差异、优劣、借鉴建议、报告正文。

差异、优劣、借鉴和正文是行内文字，不是指标结果。本叶不把这些句子写成评分或新指标。无行则报告空。导出若要文件，从这次读到的行生成。本叶不写对象存储，不把核增研报 `report/jobs`（614–618）或序号 211 的评估报告写成这一叶。

## 7. 点名不挂

`M_POLICY_INTENSITY_INDEX` 已用 `metric-get` 核对，本二级不挂。`found.seed=true`，`found.matrix=true`，`found.srs_map=true`。本叶不改它的 D4。

| metric_id | 注册身份（metric-get） | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_INTENSITY_INDEX` | 政策力度指数；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02；注册判定完全不支持。需求来源只有专题 05/167，`page_ids` 为 `E7-POLICY`，`systems` 为专题。注册 `ui_mount` 写到政策分析页力度排名和城市政策对比雷达图 | 214、218 只挂 `M_POLICY_INTENSITY_SCORE`。雷达图不改挂这条指数。本叶不闭合 QPOL-02，不改 D4 |

下列边界沿架构稿与 `指标与501`，本叶不改挂：

| 对象 | 本叶 |
|---|---|
| `M_POLICY_SUPPORT_STRENGTH` 对 214、218 | 支持力度只挂 216。214 保持 MODEL，不改判成统计读面 |
| `M_POLICY_INTENSITY_SCORE` 对 216 | 216 只挂支持力度。力度评分留在 214、218 |
| 215 缺项表上的部门件数 | 不登记成新指标，不改挂成政策总数 |
| 门户扶持十条 | 不是部门件数，不是本页任务 |
| 序号 211 的评估报告、核增研报 614–618 | 不是 217 |
| `指标与501` 第 6 节序号 610 | 该行写明不采用力度评分、支持力度。本叶不把 213–218 的挂接扩到核增对比 |

## 8. 偏离

任务 DoD 写「未注册模型保持 501」。这句话相对 2026-11-03 已签收的 `POL-L2-DS10-CMP-ARCH` 已经过时。

说明书第 2 节和 `指标与501.md` 仍把 213、217 写成 501，把 214、218 的判定列写成 501、页面空态，同时挂着已有 MODEL。说明书第 11.2 节仍把「重点比对 213–218」放在未开工二级。已签收架构改为：213、217 以及 214 的条件与材料、215 的实施部门读 `gkxlumenx_gapfill` 的 `gapfill_` 表；214 与 218 的力度分走 `jobs` 读 `ads.policy_intensity`；216 同步读同一张表，不进 Job。无行或未接通则空。本叶按签收写挂接。

213、217 仍然没有 `metric_id`。本叶不新注册，不把缺项行内文字说成指标结果，也不把 501 写成一条能算出数的公式。214、218 的判定列仍按 `指标与501` 保留为已注册 MODEL 的页面空态记录；读面改为 Job，未接通时空，不补演示分。本叶不回头改 `指标与501.md`，也不改说明书。

215、216 的三档与说明书第 2 节一致：可接统计读面，D4 仍是 mock。216 的调用链按架构稿定为同步 `stats`，不进 Job。金额档缺失则该维空。

本叶未会签。不把本单标 done。不改任务状态。

## 9. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式，不把 `intensity.py` 重写成新公式，不把演示分写成展示返回值。
- 不挂 `M_POLICY_INTENSITY_INDEX`。
- 不把 `M_POLICY_SUPPORT_STRENGTH` 挂到 214 或 218，不把 `M_POLICY_INTENSITY_SCORE` 挂到 216。
- 不把部门件数登记成新指标，不把缺项件数改挂成政策总数。
- 不给 213、217 以及 214 的条件、材料写能算出数的公式。行内文字不是指标结果。
- 216 不进 Job。金额档缺失不补档位。
- `sub_type=policy_intensity` 未接通时，214 与 218 保持空，不补演示分。
- 不闭合 QPOL-02，不把 D2 provisional 改绿。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓与 vendor 里的计算文件。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不改说明书、`指标与501.md`、架构稿、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。不写代码。
- 不会签。不把本单标 done。不改任务状态。
