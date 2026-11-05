# LUMEN-INTEL-MOCK-INV-L01

综合智能分析 — lumen-ui-topic 三叶 mock 接口清单。只读，未改业务仓。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-28 改由淮政玮本人认领。清单内容未改：跑批三键、六个 analysisType、22 个 metric 挂载仍以本文表格为准。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 分析文档，不写业务代码。未用 YAGNI 跳过 D9：种子里的 missing/draft 原样抄出。 |

## 范围与实现

盘点 `repos/lumen-ui-topic` 综合智能分析三叶（活力 / 要素 / 协同）的 mock 面。行主键 = `注册键或 analysisType + 字段路径`。

真源文件：

- `src/mock/register.ts`（`synth*Batch` 与 `#102–#109`）
- `src/mock/intel/intelBatchApi.ts`、`vitalityMock.ts`、`elementMock.ts`、`collabMock.ts`
- `src/mock/intel/intelMetricSeed.ts`、`synthReadinessSeed.ts`
- `src/mock/enterprise/analysisTaskStore.ts`
- `src/api/enterprise/analysisTask.ts`、`paths.ts`、`types/analysisTask.ts`
- `src/composables/useSynthCtx.ts`

### 1. 跑批快照（三键）

默认三元组才有快照：`region=深圳`、`compare=全国重点城市`、`window=最近3年`（`isSynthDefaults`）。其余抛 `IntelBatchSnapshotNotFound`（status 404）。URL 窗 `1y|3y|5y` 在 `useSynthCtx` 映射成「最近1年 / 最近3年 / 最近5年」后再判默认。

注册在 `register.ts`，但页面没有 `defineApi({ id: 'synth*Batch' })`。工作台秒开走 `get*BatchSnapshot()` 进程内直调。`elementResultSource.ts` 注释里的 `elementBatchApi.ts` 不存在。

| 行主键 | HTTP（总纲契约，mock 未挂 defineApi） | 入参 | 成功包顶层 | 结果对象顶层字段 | 挂载页 |
|---|---|---|---|---|---|
| `synthVitalityBatch` | `GET /topic/v1/synth/vitality/batch-snapshot` | `region, compare, window` | `snapshotId, computedAt, methodVersion=vDemo-vitality, result` | `VitalityResult`：`batchKey, computedAt, source, vitalityIndex, deltaVsCompare, yoy, gradeNote, dimScores[], indicators[], ranks[], trend[], strengths[], weaknesses[]` | `/intelligence/vitality` |
| `synthElementBatch` | `GET /topic/v1/synth/elements/batch-snapshot` | 同上 | `methodVersion=vDemo-elements` | `ElementResult`：`compositeIndex, typeIndex, levelIndex, domainIndex, evaluationDimensions[], deltaVsCompare, yoy, typeScores[], levelScores[], domainScores[], lensWeights[], indicators[], ranks[], trend[], strengths[], weaknesses[], contributions[], methodDigest[], batchComputedAt, source, snapshotId` | `/intelligence/elements` |
| `synthCollabBatch` | `GET /topic/v1/synth/collaboration/batch-snapshot` | 同上 | `methodVersion=vDemo-collab` | `CollabResult`：`collabIndex, completeness, centrality, density, deltaVsCompare, yoy, relationInput, nodes[], edges[], centralityTop[], clusters[], isolates[], ranks[], trend[], effectEval, strengths[], weaknesses[], strategies[], methodDigest[], batchComputedAt, methodVersion, source, snapshotId` | `/intelligence/collaboration` |

`methodVersion` 包在快照外壳，不在 `VitalityResult` 体内。要素/协同的 `methodVersion` 只在外壳（协同结果体内另有 `methodVersion`）。

### 2. 任务中心（复用 #102–#109，六个 analysisType）

路径前缀 `/topicAsync/topic/v1`（`AnalysisTaskPaths`）。mock 注册键与全专题共用，不是三叶专有路由。

| 注册键 | 方法与路径 | 三叶用途 |
|---|---|---|
| `analysisTaskCreate` | `POST .../analysis/tasks` | 开始分析 / 生成报告 |
| `analysisTaskList` | `POST .../analysis/tasks/list` | 分析记录 |
| `analysisTaskDetail` | `GET .../analysis/tasks/{taskId}` | 过程页详情 |
| `analysisTaskResult` | `GET .../analysis/tasks/{taskId}/result` | 成功后的 resultData |
| `analysisTaskEvents` | `GET .../analysis/tasks/{taskId}/events` | 阶段节点 |
| `analysisTaskCancel` | `POST .../analysis/tasks/{taskId}/cancel` | 排队撤回 |
| `analysisTaskRunning` | `GET .../analysis/tasks/running` | 同条件去重 |
| `analysisTaskStream` | `GET .../analysis/tasks/stream` | 五阶段 SSE |
| `analysisTaskDelete` | `DELETE .../analysis/tasks/{taskId}` | 软删（总纲 #102–#109 未单列，代码已注册） |

`#106` 资产下载按既有规格不注册数据 mock。

创建     入参：`analysisType` + `params.region/compare/window`（活力另可选 `weight_profile`）。  
     指纹：要素/协同 `analysis_fp = region|compare|window`；**活力** `region|compare|window|weight_profile_norm`（缺省归一 `INDEX_MAIN`）。  
     旧三段活力任务：按冻结权重/`methodVersion` 识别档位；无法确认 → `legacy_unknown`，**禁止自动复用**（不得视为 INDEX_MAIN）。  
     快照：`snapshotId`=不可变（含 `calc_batch_id` 或唯一记录 ID）；`cache_key`=条件(+profile) 最新索引。细则 `sdd/l2/SYNTH-L2-VIT-AI-TABLES.md` §3。

| analysisType | 成功 result 顶层 | 过程阶段名 |
|---|---|---|
| `region_innovation_vitality` | 同 `VitalityResult`（`batchKey=task:{taskId}`，`source=task`） | 任务提交与分析条件冻结；校验目标区域×对比范围×时间窗，装载四维专题库快照与权重合计；按科技/产业/人才/政策四维计算区域创新活力指数；生成单维评分、权重分布与优势短板；结果可信性校验与分析报告组装 |
| `region_innovation_elements` | 同 `ElementResult`（`snapshotId=task:{taskId}`） | 任务提交与分析条件冻结；汇聚七类创新要素多源数据与全景快照；计算要素类型指数与层次指数；计算领域指数并量化要素贡献路径；合成要素综合指数、优势短板与分析报告组装 |
| `region_innovation_collaboration` | 同 `CollabResult` | 任务提交与分析条件冻结；装载创新主体与合作关系快照，构建区域协同网络；计算完整度、中心度与密度三项网络指标；合成协同指数，识别高效集群、孤立主体与优势不足；校验横向对比与趋势结果，组装协同效率报告快照 |
| `region_innovation_vitality_report` | `{ format: 'pdf', parent_task_id }` | 无五阶段结果体 |
| `region_innovation_elements_report` | 同上 | 同上 |
| `region_innovation_collaboration_report` | 同上 | 同上 |

报告模板名在总纲里是 `synth-{leaf}-report-v1`，mock 成功体只有 pdf 指针。

### 3. 结果字段 → metric_id

种子 `def_status` 是前端副本，不是指标库结论。missing 的 id 见各叶 `*_MISSING_DEF`。

| 行主键 | metric_id | 种子中文名 | 种子 def_status | 挂载 |
|---|---|---|---|---|
| `synthVitalityBatch + result.vitalityIndex` | `M_SYNTH_VIT_INDEX` | 区域创新活力指数 | missing | 活力工作台指数 |
| `synthVitalityBatch + result.dimScores` | `M_SYNTH_VIT_DIM_SCORE` | 四维单维评分 | draft | 活力四维分 |
| `synthVitalityBatch + result.dimScores.weight` | `M_SYNTH_VIT_WEIGHT` | 维度权重分布 | missing | 活力权重 / 方法抽屉 |
| `synthVitalityBatch + result.indicators` | `M_SYNTH_VIT_INDICATOR` | 活力分项指标值与得分 | draft | 活力分项表 |
| `synthVitalityBatch + result.ranks` | `M_SYNTH_VIT_RANK` | 对比范围活力排名 | missing | 活力排名 |
| `synthElementBatch + result.compositeIndex` | `M_SYNTH_ELEM_INDEX` | 区域创新要素指数（综合） | missing | 要素综合指数 |
| `synthElementBatch + result.typeIndex` | `M_SYNTH_ELEM_TYPE_INDEX` | 区域创新要素类型指数 | missing | 类型指数 |
| `synthElementBatch + result.typeScores` | `M_SYNTH_ELEM_TYPE_SCORE` | 七要素类型维得分 | draft | 七要素得分 |
| `synthElementBatch + result.levelIndex` | `M_SYNTH_ELEM_LEVEL_INDEX` | 区域创新要素层次指数 | missing | 层次指数 |
| `synthElementBatch + result.levelScores` | `M_SYNTH_ELEM_LEVEL_SCORE` | 七大结构层次评价 | draft | 层次评价 |
| `synthElementBatch + result.domainIndex` | `M_SYNTH_ELEM_DOMAIN_INDEX` | 区域创新要素领域指数 | missing | 领域指数 |
| `synthElementBatch + result.indicators` | `M_SYNTH_ELEM_INDICATOR` | 要素分项指标值与得分 | draft | 要素分项 |
| `synthElementBatch + result.evaluationDimensions` | `M_SYNTH_ELEM_FOUR_DIM_SCORE` | 要素评价四维得分 | missing | 规模/质量/结构/活跃度 |
| `synthElementBatch + result.lensWeights` | `M_SYNTH_ELEM_WEIGHT` | 类型/层次/领域权重分布 | missing | 三透镜权重 |
| `synthElementBatch + result.contributions` | `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 | missing | 贡献路径 |
| `synthElementBatch + result.ranks` | `M_SYNTH_ELEM_RANK` | 对比范围要素综合排名 | missing | 要素排名 |
| `synthCollabBatch + result.collabIndex` | `M_SYNTH_COLLAB_INDEX` | 区域创新协同指数 | missing | 协同指数 |
| `synthCollabBatch + result.completeness` | `M_SYNTH_COLLAB_COMPLETENESS` | 协同网络完整度 | draft | 完整度 |
| `synthCollabBatch + result.centrality` | `M_SYNTH_COLLAB_CENTRALITY` | 协同网络中心度 | draft | 中心度 |
| `synthCollabBatch + result.density` | `M_SYNTH_COLLAB_DENSITY` | 协同网络密度 | draft | 密度 |
| `synthCollabBatch + result.relationInput` | `M_SYNTH_COLLAB_RELATION_INPUT` | 合作关系输入构成 | draft | 关系构成 |
| `synthCollabBatch + result.effectEval` | `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联 | missing | 协同—产出关联 |

同一 id 也挂在对应 `region_innovation_*` 的 `#105` resultData 上（字段路径相同，`source=task`）。三个 `*_report` 没有 metric 挂载。

`synthReadinessSeed.ts` 与上表 D1 一致：missing → D2–D4 `n/a`；draft → D4 mock。头注释写明 SYNTH 矩阵当时未由 data-agent 登记，禁止在该文件改绿。

未单独挂 metric_id 的结果字段：`deltaVsCompare`、`yoy`、`trend`、`strengths`、`weaknesses`、协同 `nodes/edges/clusters/isolates/strategies`。它们跟在指数或网络结果旁边，没有自己的种子 id。

## 偏离

- 总纲写 query `window=1y|3y|5y`。mock 判定用中文窗「最近3年」。URL 码只在 `useSynthCtx` 入站时翻译。
- 跑批三键已 `registerApiMock`，页面不经 `defineApi`。`USE_MOCK=false` 时这三键不会被请求打到，秒开直接没有快照。
- 无业务口径偏离需要甲方拍板；本单不改种子。

## 产物清单

- 本 handoff（行主键表）
- 未改 `lumen-ui-topic`

## 验收证据

- 对照阅读上述源文件，2026-10-28
- 无业务仓 commit，无 pipeline
- 下游行主键消费方：`LUMEN-INTEL-IMPL-XREF-L01`、`LUMEN-INTEL-METRIC-XREF-L01`

## 架构合规自检

- ✅ 调用链：只读，未新增前端直连 Python / demo 服务
- ✅ 算法只在 Python：未写算法
- ✅ 图谱：未改 Nebula / 未引入 Neo4j
- ✅ 可观测：未改埋点
- ✅ CI：文档落编排仓，无业务镜像
- ✅ demo 不 merge 进 lumen
- ✅ D12：未让 lumen 调用 demo-* 服务
- ✅ D9：种子 def_status 原样列出，未改绿

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | cursor-grok-4.7 |
| actual_cost | 0.24 |
| cost_warn | green |

单价表无 Grok 行。成本按 frontend-agent 比例 0.80/0.20、用 claude-sonnet-4.5 单价（输入 $3 / 输出 $15 每百万）作上限估算：`45000×0.8×3/1e6 + 45000×0.2×15/1e6 = 0.24`。未接 Console 精确分项。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：随本 handoff 提交
- pipeline：编排仓无业务 CI
- 部署：无
- dev 测试：不适用（只读盘点）

## 涉及文件

- `repos/lumen-ui-topic/src/mock/intel/*`
- `repos/lumen-ui-topic/src/mock/register.ts`
- `repos/lumen-ui-topic/src/mock/enterprise/analysisTaskStore.ts`
- `repos/lumen-ui-topic/src/api/enterprise/analysisTask.ts`
- `repos/lumen-ui-topic/src/api/enterprise/paths.ts`
