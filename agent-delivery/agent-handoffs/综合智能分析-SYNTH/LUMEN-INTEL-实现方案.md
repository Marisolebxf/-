# 综合智能分析实现方案

- 日期：2026-10-28
- 读者：要开工实现三叶（活力 / 要素 / 协同）的人
- 本文件是实现顺序。行级明细不在这里复写，按下面的索引回查。口径未闭合的项不在这里拍板。功能验收缺项按架构基线 D16、血缘规约 §2.4，本方案 §6.1。

## 0. 分析索引

三张单都是只读，认领人 `human:淮政玮`，状态 `ready_to_sign`。全文在同目录。

| 任务 | 回答什么 | 交接 | 分析正文 | 认领改记 |
|---|---|---|---|---|
| `LUMEN-INTEL-MOCK-INV-L01` | 专题 mock 有哪些注册键、路径、结果字段、metric 挂在哪 | [LUMEN-INTEL-MOCK-INV-L01.md](LUMEN-INTEL-MOCK-INV-L01.md) | `409b5b14` | `2fc37a6f` |
| `LUMEN-INTEL-IMPL-XREF-L01` | 这些行在 system-ui-test 和算法 preview 里是对应、部分对应，还是没有 | [LUMEN-INTEL-IMPL-XREF-L01.md](LUMEN-INTEL-IMPL-XREF-L01.md) | `db9b6a9c` | `94a1c692` |
| `LUMEN-INTEL-METRIC-XREF-L01` | 挂载的 metric_id 在指标库里在不在、D1/D4、中文名是否一致 | [LUMEN-INTEL-METRIC-XREF-L01.md](LUMEN-INTEL-METRIC-XREF-L01.md) | `ca85fc71` | `524a1d18` |

相关、但不是这三张单的产物：

| 文档 | 用途 |
|---|---|
| [API-SYNTH-INTEL-REPLICA-PLAN.md](API-SYNTH-INTEL-REPLICA-PLAN.md) | 前端复刻时写的接口需求。本方案若与它对不上，以三张单的实测为准，并在偏离里说明 |
| `LUMEN-INTEL-BE-1` | 已有 backlog：Java 白名单、跑批 404、报告模板。本方案第 9 节是它的施工顺序 |

行主键全文件统一，定义在清单单：`注册键或 analysisType + 字段路径`。后两张单的每一行都用这个键。实现时改字段名，先改清单单再改装包，不要三处各写一套。

## 1. 建议

沿现有专题分析任务做，不要新造「综合智能服务」，也不要接 `demo-ui-system-test` 或算法 preview。

专题页要的是两件事：

1. 默认条件秒开一份快照。
2. 改条件后走「开始分析」，五阶段，结果 JSON 与快照同构。

第 2 件的壳已经在跑：`lumen-ui-topic` 调 `gkxlumen-topic-async-service` 的 `#102–#109`。政策、产业链、产业服务都是「白名单 + 一个 Adapter + Feign Python `/internal/*`」。综合智能照这个加六个 `analysisType`。

第 1 件可以晚一步。没有快照时前端已经会进「开始分析」。第一期 Python 对跑批接口返回 404 即可。

算分只在 `lumen-algo-py` 的 `vendor/entan-py`。那里已有 `POST /v1/synth-metric/metric/{metric_id}/compute`。Java 不算指数、不写 nGQL。浏览器不直打这条 `/v1`。

这个顺序是三张单合在一起才成立的：

- 清单单说明专题要的是「快照 JSON = 任务结果 JSON」，不是产业综合页上的另一套 KPI。
- 实现对照单说明 system-ui-test 和算法 preview **没有一条「对应」**。能借用的只有 5 个已经 `available` 的 compute，而且它们返回的是单指标，不是三叶整包。
- 指标库单说明 21 个 id 可以沿用，但 D4 仍是 `mock`，前端种子的 missing/draft 不能当成「库里没有」。

## 1.1 三单合在一起后必须守住的结论

### 来自清单单

- 跑批只有三键：`synthVitalityBatch`、`synthElementBatch`、`synthCollabBatch`。仅「深圳 × 全国重点城市 × 最近3年」有快照，其余 404。页面秒开目前不走这三键，而是进程内直调 `get*BatchSnapshot()`。
- 改条件复用任务中心九个注册键（`analysisTaskCreate` 到 `analysisTaskDelete`）。三叶只多六个 `analysisType`：三个分析键 + 三个 `*_report`。报告成功体只有 `{ format: 'pdf', parent_task_id }`。
- 结果形状三份：`VitalityResult`、`ElementResult`、`CollabResult`。22 个统计数字的挂载点以清单单第 3 节那张表为准。`deltaVsCompare`、`yoy`、`trend`、优劣势、协同的点边集群没有自己的 metric_id。
- 窗有两套字：页面「最近1年 / 最近3年 / 最近5年」，URL `1y|3y|5y`。mock 用中文窗判断是不是默认三元组。

### 来自实现对照单

判定只有三档，全表在 xref 交接里。汇总：

| 判定 | 哪些行 | 实现时怎么用 |
|---|---|---|
| 对应 | 无 | 没有现成接口可以原样接进专题 |
| 部分对应 | 三键快照、三个分析 `analysisType`、绝大多数结果字段 | 只借用业务名字和少数 compute。路径、入参、数字都不要抄 |
| 无对应 | 整组 `#102–#109`、三个 `*_report`、`dimScores.weight`、`evaluationDimensions` | 这些必须在专题链上新做，或保持缺失。preview 里没有可抄的实现 |

部分对应里，数字也不能混用。system-ui-test 活力指数假数是 76.4，专题默认快照是 84.6。要素在中台拆成 type/layer/domain/synthesis 四页，专题是一叶。层次页讲的是基础/支撑/应用，专题是七结构成熟度。

算法 preview 里已经 `java_api` / `available`、实现时可以调用的只有：

| endpoint | 路径 | 能填进专题的位置 |
|---|---|---|
| `comp.tech-outcome.m_synth_182_1` | `POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute` | 活力科技维的上游，不是活力整包 |
| `comp.talent-outcome.m_synth_184_1` | 同模式 `M_SYNTH_184_1` | 活力人才维的上游 |
| `comp.policy-outcome.m_synth_185_1` | 同模式 `M_SYNTH_185_1` | 活力政策维的上游 |
| `comp.element-synthesis.m_synth_elem_contrib` | 同模式 `M_SYNTH_ELEM_CONTRIB` | 要素 `contributions`。它不是 `contributions[]` 整表 |
| `comp.synergy.m_synth_191_1` | 同模式 `M_SYNTH_191_1` | 协同密度的上游。不能拿它的返回值充当 `collabIndex` |

`M_SYNTH_183_1` 在 preview 里只有未发布的 GET，没有 compute。产业维不要标成已换源。`comp.graph.*` 是另一张图，第一期不要拿来填协同 `nodes/edges`。

专题 Java 仍走 `/internal/*`，不让浏览器去打上表的 `/entan/v1`。

### 来自指标库单

查法是 `metric-query domain=SYNTH`（46 条）加 `metric-get M_SYNTH_ELEM_FOUR_DIM_SCORE`（不在库）。

- 种子 22 个 id，21 个 seed 与 matrix 都有。库侧 D1 全是 `aligned`，D4 全是 `mock`，`algorithm_type` 没有 `UNKNOWN`。
- 前端种子仍是 missing 或 draft。这是镜像旧，不是库缺条。实现不要按种子把接口砍掉，也不要在页面上改绿。
- 中文名不一致的四条，id 仍各是一条：`M_SYNTH_VIT_WEIGHT`、`M_SYNTH_COLLAB_CENTRALITY`、`M_SYNTH_COLLAB_RELATION_INPUT`、`M_SYNTH_COLLAB_OUTPUT_CORR`。装包和 ⓘ 用 id，展示名以指标库为准。
- 库有、三叶 mock 未挂、但和三叶相邻的模型号：`M_SYNTH_186_1` 到 `M_SYNTH_191_1`。装包时作为整模型入口，不在页面上再挂一套平行数字。
- 同域但不是这三叶的（`M_SYNTH_182_1`–`185_1` 里 182/184/185 只当维的上游，183 未换源；以及 `GRAPHAPI`、`DS_21_*`、`DS_23_*`）不要挂进三叶页面。

## 2. 现网里已经有什么

```text
lumen-ui-topic
  → 网关 /topicAsync/topic/v1/analysis/tasks     （#102–#109，三叶页面已接）
  → gkxlumen-topic-async-service
       AnalysisAdapterRegistryImpl 按 analysisType 选 Adapter
       政策样板：PolicyAnalysisTypes + PolicyAnalysisAdapterImpl
                → Feign http://gkxlumen-platform-entan-py:8000/internal/policy/jobs/execute
  → lumen-algo-py / vendor/entan-py
       /v1/synth-metric/catalog|metric|compute     （算法 preview 已挂，专题 Java 未接）
```

对照结论的行级表在 §0 的三份交接里，合在一起的用法在 §1.1。这里只留架构落点：

| 面 | 事实 |
|---|---|
| 专题前端 | 三叶页面和结果形状已在。秒开仍是进程内 `get*BatchSnapshot()`，没有 `defineApi`。`registerApiMock('synth*Batch')` 没有调用方。 |
| 任务中心 | 路径和 mock 有。Java 白名单还没有 `region_innovation_*`。未知类型会被 Adapter 注册表拒绝。 |
| 算法 preview / system-ui-test | 产业综合页是另一套契约（`M_COMP_*`、`/comp/v1/...`）。主 GET 是 `local_mock` 且 `unavailable`。不能当专题后端。 |
| 指标计算 | catalog 约 23 条。`TABLE_MAP` 为空，缺表的走 mock 占位。`SPEC_REGISTRY` 里真正换源计算的只有 `M_SYNTH_182_1`、`M_SYNTH_184_1`、`M_SYNTH_185_1`、`M_SYNTH_191_1`、`M_SYNTH_ELEM_CONTRIB`。 |
| 指标库 | 三叶种子 22 个 id 有 21 个在库，D1=`aligned`、D4=`mock`。库里没有 `M_SYNTH_ELEM_FOUR_DIM_SCORE`。 |
| 已有单 | `LUMEN-INTEL-BE-1`（backlog）范围就是白名单、跑批 404、报告模板。本方案是它的上文，不另起服务名。 |

调用链铁律：

```text
lumen-ui-topic
  → gkxlumen-platform-gateway
  → gkxlumen-topic-async-service（任务）或 gkxlumen-topic（只读快照，第二期）
  → /internal/* 
  → gkxlumen-platform-entan-py（lumen-algo-py）
```

禁止浏览器、Java Feign、helm 指到 `demo-algo-ent-analysis`、`demo-ui-system-test`、`demo-platform-entan-py`。

## 3. 明确不做

- 不把产业综合十个模型页迁进专题，也不把 `M_COMP_*` 填进专题数字。
- 不在 Java 里加权、排序、算密度。
- 不新建 Python 服务。综合智能计算留在 `entan-py`。
- 第一期不建 ADS 宽表，不把 mock 占位说成已接入。
- 不在前端把种子 `def_status` 改成和指标库一样的 `aligned`。镜像同步是 data-agent 的事。
- 不登记新指标来补 `M_SYNTH_ELEM_FOUR_DIM_SCORE`。四维得分继续走现有缺失态，等 data-agent 决定是否入库。
- 不把未写进客户决策清单的口径当成默认。活力这一叶按 §6.2 的默认方案实算，不等 `Q-SYNTH-*` 升绿。
- 不把缺项表写进 ODS / DWD / ADS / 供应方库。缺项补齐并实算完成之前，不把 D4 提前改成 live。

## 4. 目标形态

三叶共用一个结果包。快照接口的 `data.result` 与任务 `#105` 的 `resultData` 同构，形状就是现在的 `VitalityResult` / `ElementResult` / `CollabResult`（字段表见清单 handoff）。

```text
秒开
  GET /topic/v1/synth/{leaf}/batch-snapshot?region&compare&window
  有预计算 → 200 + result
  没有 → 404，前端引导「开始分析」

改条件
  POST /topicAsync/topic/v1/analysis/tasks
    analysisType = region_innovation_{vitality|elements|collaboration}
    params = { region, compare, window }
    analysis_fp = region|compare|window
  过程：现有 #104 #108 #109 #107
  成功：#105 resultData = 同一 LeafResult，source=task

报告
  analysisType = region_innovation_{leaf}_report
  第一期结果仍是 { format, parent_task_id }，模板号 synth-{leaf}-report-v1
  不在这一期生成真正的 PDF 排版
```

`leaf` 只用 `vitality` | `elements` | `collaboration`。

窗参数：页面中文是「最近1年 / 最近3年 / 最近5年」，URL 是 `1y|3y|5y`。Java 收到任一写法都先归一成中文窗再交给 Python。不要把 `3y` 原样送进计算。

## 5. 分步

### 第一步：任务能创建并跑完（对应 `LUMEN-INTEL-BE-1` 的主路径）

Java，`lumen-svc-platform` 的 `gkxlumen-topic-async-service`：

- 新增 `SynthAnalysisTypes`，六个键，无别名。样板是 `PolicyAnalysisTypes`。
- 新增 `SynthAnalysisAdapterImpl implements AnalysisTypeAdapter`。`analysisTypes()` 返回这六个键。注册表按 Spring 注入自动挂上，不要再写一套扫描。
- 报告三键走现有产物阅读器，父类型去掉 `_report`。第一期不新做排版。
- 分析三键 Feign `http://gkxlumen-platform-entan-py:8000`，路径只用 `/internal/v1/synth/jobs/execute`。配置方式照 `topic-async` 里政策的 `algo-base-url`，默认值禁止 `demo-platform-*`。
- 五阶段文案用前端 mock 里已经写死的中文（清单 handoff 第 2 节）。缺一阶段或改字，过程页会对不上。
- Adapter 校验失败或 Python 失败：任务 `failed`，不要把演示 JSON 写进正式结果。

Python，`lumen-algo-py/vendor/entan-py`：

- 新增 `/internal/v1/synth/jobs/execute`。入参：`task_id`、`leaf`、`region`、`compare`、`window`。
- 出参：`result` 为对应 LeafResult，外加 `methodVersion`。
- 实现方式：进程内调用已有 `compute_metric`，再装成叶子 JSON。不要在这个接口里重写公式。
- 装包规则见第 6 节。某条 compute 返回 mock / blocked 时，字段照样放入，并在结果里带 `metric_id` 与 `confidence`，让前端 ⓘ 仍能指向该 id。不要用随机数填空。
- 现有 `POST /v1/synth-metric/.../compute` 保持给算法 preview。专题 Java 不调用 `/v1`。

前端，`lumen-ui-topic`：

- `USE_MOCK=false` 时，创建任务已经走 `#102`。确认六个 type 不再被 Java 拒绝即可，不必改页面结构。
- 秒开仍可暂时留在本地函数。切真实快照放到第二步，避免半截请求把默认页打成白屏。

这一步完成的标志：非默认三元组点「开始分析」，任务从排队到成功，`#105` 的 JSON 能被现有结果页渲染，五阶段文案与现在一致。

### 第二步：默认三元组秒开

- Python 增加 `GET /internal/v1/synth/{leaf}/batch-snapshot`。
- 只为「深圳 × 全国重点城市 × 最近3年」准备一份结果。来源是第一步同一个装包函数跑出来的 JSON，写入 Python 侧一份只读快照（文件或表均可，第一版用进程内常量也行，但必须标明不是 ADS）。
- 其他组合返回 404。
- Java 同步读放在 `gkxlumen-topic`（或 async 服务上的只读 Controller，二选一，不要两个都做）。对外路径保持总纲的 `GET /topic/v1/synth/{leaf}/batch-snapshot`。网关加这一条，不要复用 `/topicAsync`。
- 前端用 `defineApi` 接上 `synthVitalityBatch` / `synthElementBatch` / `synthCollabBatch`，删掉工作台对 `get*BatchSnapshot()` 的直连。`USE_MOCK=false` 且 404 时进入已有的 no_batch，禁止再用 fixture 填数。

没有这一步，系统仍然可用，只是默认条件也要点「开始分析」。

### 第三步：算分从占位变成查表

不在本方案里展开每条公式。顺序只定这一条：

1. data-agent 按 `metrics/calc-logic/SYNTH/` 把源表补进 `TABLE_MAP` 或 `SPEC_REGISTRY`。
2. `compute_metric` 从 mock 占位换成查表后，叶子装包函数不用改字段名。
3. 前端就绪度镜像由 data-agent 从矩阵生成。页面不得手写改绿。

现在就能进装包、且不是纯占位的，只有 §1.1 列出的 5 个 compute。`M_SYNTH_183_1` 在 catalog 里，不在 `SPEC_REGISTRY` 里，产业维不要假装已换源。

模型号 `M_SYNTH_186_1`–`M_SYNTH_191_1` 是叶子的「整模型」id（指标库单：库有、mock 未挂）。装包时指数位优先用叶子 id（`M_SYNTH_VIT_INDEX` 等）。186 与活力指数同核，实现时调用一处，不要算两遍再对打。

## 6. 叶子怎么装

装包函数按叶子调用下表。行主键、页面挂载见清单单第 3 节；system-ui-test / preview 的判定见实现对照单；D1、D4、中文名见指标库单。计算失败的格子保留 null，并带上该 `metric_id`。不要补 0。

活力 `vitality`：

| 结果字段 | metric_id | 现在的计算 |
|---|---|---|
| `vitalityIndex` | `M_SYNTH_VIT_INDEX` | mock 占位。同核参考 `M_SYNTH_186_1`（四维等权，维分来自 182/183/184/185，缺维不进平均） |
| `dimScores` | `M_SYNTH_VIT_DIM_SCORE` | mock 占位 |
| `dimScores.weight` | `M_SYNTH_VIT_WEIGHT` | mock 占位。库内中文名是「活力指数权重配置与权重弹性」，id 不变 |
| `indicators` | `M_SYNTH_VIT_INDICATOR` | mock 占位 |
| `ranks` | `M_SYNTH_VIT_RANK` | mock 占位。对比范围不是单个城市，按 `compare` 的城市集合排序 |

要素 `elements`：

| 结果字段 | metric_id | 现在的计算 |
|---|---|---|
| `compositeIndex` | `M_SYNTH_ELEM_INDEX` | mock。同核 `M_SYNTH_190_1` |
| `typeIndex` / `typeScores` | `M_SYNTH_ELEM_TYPE_INDEX` / `M_SYNTH_ELEM_TYPE_SCORE` | mock。同核 `M_SYNTH_187_1` |
| `levelIndex` / `levelScores` | `M_SYNTH_ELEM_LEVEL_INDEX` / `M_SYNTH_ELEM_LEVEL_SCORE` | mock。同核 `M_SYNTH_188_1` |
| `domainIndex` | `M_SYNTH_ELEM_DOMAIN_INDEX` | mock。同核 `M_SYNTH_189_1` |
| `indicators` | `M_SYNTH_ELEM_INDICATOR` | mock |
| `lensWeights` | `M_SYNTH_ELEM_WEIGHT` | mock |
| `contributions` | `M_SYNTH_ELEM_CONTRIB` | 已有 SPEC 计算，优先走它 |
| `ranks` | `M_SYNTH_ELEM_RANK` | mock |
| `evaluationDimensions` | `M_SYNTH_ELEM_FOUR_DIM_SCORE` | 指标库无此 id。装包可给演示结构，但 `confidence=blocked`，前端继续显示缺失，不编一个新 id |

协同 `collaboration`：

| 结果字段 | metric_id | 现在的计算 |
|---|---|---|
| `collabIndex` | `M_SYNTH_COLLAB_INDEX` | mock |
| `completeness` | `M_SYNTH_COLLAB_COMPLETENESS` | mock |
| `centrality` | `M_SYNTH_COLLAB_CENTRALITY` | mock。库内中文名多了「平均点度中心性」 |
| `density` | `M_SYNTH_COLLAB_DENSITY` | mock。`M_SYNTH_191_1` 已有 SPEC，密度位调用它，指数不要改用 191 的返回值冒充 |
| `relationInput` | `M_SYNTH_COLLAB_RELATION_INPUT` | mock。库内中文名是「协同关系输入统计」 |
| `effectEval` | `M_SYNTH_COLLAB_OUTPUT_CORR` | mock。样本少于 3 不出系数，与现在的前端规则一致 |
| `nodes` / `edges` | 无单独 id | 第一期允许空数组。不要从 `comp.graph.*` 或演示图硬拷 |

`deltaVsCompare`、`yoy`、`trend`、`strengths`、`weaknesses` 没有独立 metric_id。由装包函数从指数和分维结果推导；推导不了就空数组 / null。协同的集群、孤立点、策略文案同样允许空，不要写死营销句。

区域入参和 compute 现用的 `province/city/year` 不是同一套词。Adapter 里做一张显式映射（深圳 → 城市编码，窗 → 年份闭区间，对比范围 → 城市编码列表），映射表放在 Python 常量里并写进接口说明。映射没有的区域直接失败，不要默默改成深圳。

## 6.1 功能验收时缺项怎么补

全系统规则是架构基线 **D16**、血缘规约 **§2.4**：只在库 `gkxlumenx_gapfill` 建 `gapfill_` 开头的表，由 Python 用 LLM 或其他方式灌入**计算逻辑里已经写明的缺项**。Java 和前端不建表、不灌数。生产配置不读这个库。活力这一叶的灌数任务是 `LUMEN-INTEL-VIT-GAPFILL-DATA-L01`（data-agent）；建表和读路径是 `LUMEN-INTEL-VIT-GAPFILL-L01`。

综合智能按这个办，不另造一套：

- 灌数之前，缺项必须能在 `metrics/calc-logic/SYNTH/{metric_id}.md` 里点到。文档没写的字段保持 null，不补 0，不用随机数填。
- 每行带上 `metric_id`、`gap_item`、`fill_method`、`fill_model`（LLM 时）、`gapfill_batch_id`、`generated_at`。装包结果里对应格子仍带原 `metric_id`，并加 `confidence=gapfill`，让 ⓘ 能看出这格来自缺项表。
- 写出的 ADS 批次号以 `gapfill_` 开头。缺项尚未接入公式时 D4 仍是 mock。按 §6.2 补齐并实算完成后，D4 改为 live，界面去掉 🧪。
- 真源该列有了可用值之后，计算停读对应表，缺项行不并进 DWD。

## 6.2 活力默认方案

`Q-SYNTH-01`、`Q-SYNTH-V-01`、`Q-SYNTH-V-02` 仍是 🟡。本批不另开会，锁定客户决策清单里已经写下的临时默认，五张实现单都按这个算：

| 项 | 默认 |
|---|---|
| 区域 × 对比 × 时间 | 深圳 × 全国重点城市 × 最近3年 |
| 权重 | 四维等权，各 0.25。与 `M_SYNTH_186_1` 同核，只调用一处。0.30/0.30/0.20/0.20 与熵权只作对照，不作为默认主数 |
| 归一 | 对比集合内极值归一 |
| 缺维 | 分母收缩，不补 0 |
| 缺项 | `LUMEN-INTEL-VIT-GAPFILL-L01` 建表并接入公式。`LUMEN-INTEL-VIT-GAPFILL-DATA-L01` 灌行。灌齐并实算完成前，对应指标 D4 不得改成 live |
| 完成态 | 活力五条挂载（`M_SYNTH_VIT_INDEX`、`M_SYNTH_VIT_DIM_SCORE`、`M_SYNTH_VIT_WEIGHT`、`M_SYNTH_VIT_INDICATOR`、`M_SYNTH_VIT_RANK`）不再走 mock 占位。灌数单把 D4 改为 live，`source_systems` 写明 `gapfill_` 批次。五张单都交接后，本功能可提测 |

ⓘ 可以保留「待甲方确认」。数本身按上表计算，不退回占位 JSON。

第一批缺项表（细稿 §3.3）：

| 缺项 | 表 | 现在的源况 |
|---|---|---|
| 新产品销售收入占比 | `gapfill_synth_new_product_sales_ratio` | `a77234` 0 行；营业收入分母几乎全空 |
| 研发人员数量 | `gapfill_synth_rd_employee` | `development_employee` 整列空 |
| 政策实施效果指数 | `gapfill_synth_policy_effect` | 日期为 `0000-00-00` |

人才维、政策维的半维（学历结构、年龄结构等）同样只补细稿写明缺的子项，表名继续 `gapfill_synth_`。`M_SYNTH_ELEM_FOUR_DIM_SCORE` 库中无此 id，不建缺项表来顶这个号。

## 7. 前端还要动的点

只在第二步切秒开时改这些，第一步不要为了「接真接口」重做页面：

- `elementResultSource.ts` 以及活力、协同的同类文件：秒开改为 `defineApi`，404 走现有 no_batch。
- 去掉对 `getVitalityBatchSnapshot` / `getElementBatchSnapshot` / `getCollabBatchSnapshot` 的页面直连。mock 模式仍可由 `registerApiMock` 提供同一形状。
- `USE_MOCK=false` 时禁止 import 这些函数来填数。
- ⓘ 继续用现有 `IntelMetricMount` 和种子。不在这次把 21 条 missing/draft 改成 aligned。
- 活力五条在 D4 改为 live 之后去掉 🧪。`confidence=gapfill` 只出现在 ⓘ 的来源说明里。前端不读 `gkxlumenx_gapfill`。

## 8. 验收

1. 六个 `analysisType` 能创建；第七个任意字符串被拒绝。
2. 默认三元组：第二步之前，快照 404，页面可开始分析；第二步之后，200 且 `source=batch`。
3. 非默认组合：快照 404；任务成功后结果页字段与默认快照同一套键。
4. 浏览器网络里没有 `demo-*`，没有 `/v1/synth-metric`，没有 `/comp/v1`。
5. Java 仓库里没有指数公式。公式只出现在 `entan-py`。
6. 五阶段中文与清单 handoff 一致，过程页不出现百分比。
7. `M_SYNTH_ELEM_FOUR_DIM_SCORE` 仍表现为库中不存在，不出现伪 8 件套。
8. 活力五条在缺项补齐并按 §6.2 实算完成之后，D4 为 live，页面没有 🧪。灌数行只在 `gkxlumenx_gapfill.gapfill_*`，不在 ODS/DWD/供应方库。

## 9. 建议的施工顺序

| 顺序 | 仓 | 内容 | 和现有单的关系 |
|---|---|---|---|
| 1 | `lumen-algo-py` | `LUMEN-INTEL-VIT-PY-L01`：活力装包，按 §6.2 默认口径实算 | 不实现要素、协同 |
| 2 | `lumen-svc-platform` | `LUMEN-INTEL-VIT-BE-L01`：只登记活力两键 | 不并行改 `LUMEN-INTEL-BE-1` 去加要素/协同 |
| 3 | `lumen-ui-topic` | `LUMEN-INTEL-VIT-FE-L01`：只接活力页 | 等 1 和 2 的交接 |
| 4 | `lumen-algo-py` | `LUMEN-INTEL-VIT-GAPFILL-L01`：建三张缺项表，并把读路径接进公式 | 不灌业务行，不改 D4 |
| 5 | `lumen-algo-py` | `LUMEN-INTEL-VIT-GAPFILL-DATA-L01`：data-agent 灌 `gapfill_` 行；实算成功后五条活力指标 D4 改为 live，`source_systems` 写明 `gapfill_` 批次 | 等 1、2、3、4 都交接。灌齐并实算完成前不得改 live |

1 和 2 可以并行。3 等 1 和 2 的交接。4 等 1 的装包函数。5 等前四张单交接后再灌数、再改 D4。

五张单都交接之后，区域创新活力分析可提测：`USE_MOCK=false`，默认条件深圳 × 全国重点城市 × 最近3年，开始分析走真实任务，结果按 §6.2 实算，五条 D4 为 live，页面没有 🧪。缺任何一张都不提测。不另开测试单。五张单的监管人都是唐绍祖。派单说明在 `agent-handoffs/综合智能分析-SYNTH/派单说明/`。

WBS 索引在 `工程过程/02-策划与监控/02-智树工作计划/02-进度/01-自研模块WBS.md` 的「区域创新活力分析」行。
