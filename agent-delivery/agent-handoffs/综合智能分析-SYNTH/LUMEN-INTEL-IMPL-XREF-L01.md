# LUMEN-INTEL-IMPL-XREF-L01

综合智能分析 mock 对照 `demo-ui-system-test` 产业综合页与算法 preview（`lumen-ui-algo-apiview` `src/catalog/comp.json`）。只读，未改两个仓。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-28 改由淮政玮本人认领。对照结论未改：三叶 mock 与 system-ui-test、算法 preview 无同路径实现。行主键来自 `LUMEN-INTEL-MOCK-INV-L01`。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 对照文档。不把产业综合十模型整包当成专题三叶的同构实现。 |

## 范围与实现

判定只用三档：

- **对应**：路径或注册键一致，且能返回专题那份结果字段。
- **部分对应**：同一业务叶有页面或 catalog 条目，但路径、入参、metric_id 或运行时不同。
- **无对应**：system-ui-test 与算法 preview 都没有这一调用。

读到的事实：

- `demo-ui-system-test` 没有「综合智能分析」菜单，也没有 `region_innovation_*` / `batch-snapshot`。产业综合在 `src/views/industry-comp/`，菜单 `industryCompMenuConfig.ts`，页内数是 `compModelCatalog.ts` 的 `M_COMP_*` 本地假数。
- 算法 preview `comp.json` 与这些菜单同 slug。三叶相关主 GET 全部 `runtime=local_mock` 且 `status=unavailable`（目录写明 Java/网关/Python 未发布，不发真实请求）。另有几条 `POST .../compute` 是 `runtime=java_api`、`status=available`，指标号不是专题 batch-snapshot。

### 跑批三键与任务壳

| 行主键 | system-ui-test | 算法 preview | 判定 |
|---|---|---|---|
| `synthVitalityBatch` | 页 `/industry-comp/vitality`，模型 `COMP_REGION_VITALITY`，KPI 用 `M_COMP_REGION_VITALITY_INDEX/RANK/YOY/COV`。无 `GET /topic/v1/synth/vitality/batch-snapshot` | `comp.vitality.main` `GET /comp/v1/comp/region-vitality`，`local_mock` / `unavailable`。样例指标含 `M_SYNTH_VIT_INDEX`、`M_SYNTH_186_1`、`M_SYNTH_VIT_DIM_SCORE`、`M_SYNTH_VIT_INDICATOR` | 部分对应 |
| `synthElementBatch` | 拆成四页：`element-type`、`element-layer`、`element-domain`、`element-synthesis`。KPI 是 `M_COMP_ELEMENT_*`，不是 `M_SYNTH_ELEM_*` | 四条主 GET：`/comp/v1/comp/element-type|element-layer|element-domain|element-synthesis`，均 `local_mock` / `unavailable`。另 `comp.element-synthesis.m_synth_elem_contrib` `POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute`，`java_api` / `available` | 部分对应 |
| `synthCollabBatch` | 页 `/industry-comp/synergy`，模型 `COMP_INNOV_SYNERGY`，KPI `M_COMP_INNOV_SYNERGY_INDEX/LINK/CROSS/EFF`。图是本地节点，不是专题 `CollabResult` | `comp.synergy.main` `GET /comp/v1/comp/innov-synergy`，`local_mock` / `unavailable`（样例提到 `M_SYNTH_COLLAB_INDEX`、`M_SYNTH_COLLAB_OUTPUT_CORR`）。另 `comp.synergy.m_synth_191_1` `POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute`，`java_api` / `available` | 部分对应 |
| `analysisTaskCreate` 及 list/detail/result/events/cancel/running/stream/delete | 无 `/topicAsync/topic/v1/analysis/tasks` | catalog 无这组路径 | 无对应 |
| `region_innovation_vitality` | 无该 analysisType。结果语义见活力页 | 无该键。结果语义见 `comp.vitality.main`（未发布） | 部分对应（只在结果语义） |
| `region_innovation_elements` | 无该键。结果语义拆在四页 | 无该键。结果语义拆在四条未发布 GET | 部分对应（只在结果语义） |
| `region_innovation_collaboration` | 无该键。结果语义见 synergy 页 | 无该键。结果语义见 `comp.synergy.main`（未发布） | 部分对应（只在结果语义） |
| `region_innovation_*_report` 三个 | 无报告任务、无 pdf 指针接口 | 无 | 无对应 |

### 字段路径（挂在快照 result 上；任务成功体同路径）

活力：

| 行主键 | system-ui-test | 算法 preview | 判定 |
|---|---|---|---|
| `synthVitalityBatch + result.vitalityIndex` | 页上有「活力指数」`M_COMP_REGION_VITALITY_INDEX`（假数 76.4；专题默认快照是 84.6） | 未发布 GET 的样例含 `M_SYNTH_VIT_INDEX` | 部分对应 |
| `synthVitalityBatch + result.dimScores` | 页有四维条，无 `M_SYNTH_VIT_DIM_SCORE` | 样例含 `M_SYNTH_VIT_DIM_SCORE` | 部分对应 |
| `synthVitalityBatch + result.dimScores.weight` | 无同名权重接口 | 主 GET 未发布，样例未单列 `M_SYNTH_VIT_WEIGHT` | 无对应 |
| `synthVitalityBatch + result.indicators` | 无 12 行分项表契约 | 样例含 `M_SYNTH_VIT_INDICATOR` | 部分对应 |
| `synthVitalityBatch + result.ranks` | 有「活力排名」`M_COMP_REGION_VITALITY_RANK` | 未发布 GET 的样例有城市条，无专题 `ranks[]` 契约 | 部分对应 |

要素：

| 行主键 | system-ui-test | 算法 preview | 判定 |
|---|---|---|---|
| `synthElementBatch + result.compositeIndex` | `element-synthesis` 的 `M_COMP_ELEMENT_SYNTHESIS_INDEX` | `comp.element-synthesis.main` 未发布，样例含 `M_SYNTH_ELEM_INDEX`、`M_SYNTH_190_1` | 部分对应 |
| `synthElementBatch + result.typeIndex` | `element-type` 的 `M_COMP_ELEMENT_TYPE_INDEX` | `comp.element-type.main` 未发布，样例含 `M_SYNTH_ELEM_TYPE_INDEX`、`M_SYNTH_187_1` | 部分对应 |
| `synthElementBatch + result.typeScores` | 类型页有七类展示，id 不是 `M_SYNTH_ELEM_TYPE_SCORE` | 样例含 `M_SYNTH_ELEM_TYPE_SCORE` | 部分对应 |
| `synthElementBatch + result.levelIndex` | `element-layer` 的 `M_COMP_ELEMENT_LAYER_INDEX` | `comp.element-layer.main` 未发布，样例含 `M_SYNTH_ELEM_LEVEL_INDEX`、`M_SYNTH_188_1` | 部分对应 |
| `synthElementBatch + result.levelScores` | 层次页讲基础/支撑/应用，专题是七结构成熟度 | 样例含 `M_SYNTH_ELEM_LEVEL_SCORE` | 部分对应 |
| `synthElementBatch + result.domainIndex` | `element-domain` 的 `M_COMP_ELEMENT_DOMAIN_INDEX` | `comp.element-domain.main` 未发布，样例含 `M_SYNTH_ELEM_DOMAIN_INDEX`、`M_SYNTH_189_1` | 部分对应 |
| `synthElementBatch + result.indicators` | 无专题分项行契约 | 综合页样例含 `M_SYNTH_ELEM_INDICATOR` | 部分对应 |
| `synthElementBatch + result.evaluationDimensions` | 无规模/质量/结构/活跃度四维契约 | 无 `M_SYNTH_ELEM_FOUR_DIM_SCORE` 端点 | 无对应 |
| `synthElementBatch + result.lensWeights` | 综合页饼图是三维权重草案，id 不是 `M_SYNTH_ELEM_WEIGHT` | 无单独权重端点 | 部分对应 |
| `synthElementBatch + result.contributions` | 综合页无贡献路径表 | `POST .../M_SYNTH_ELEM_CONTRIB/compute` 已 `java_api` / `available`。这是指标计算，不是专题快照里的 `contributions[]` | 部分对应 |
| `synthElementBatch + result.ranks` | 各页有「区域排名」假数，id 是 `M_COMP_*_RANK` | 无专题 `ranks[]` 端点 | 部分对应 |

协同：

| 行主键 | system-ui-test | 算法 preview | 判定 |
|---|---|---|---|
| `synthCollabBatch + result.collabIndex` | `M_COMP_INNOV_SYNERGY_INDEX` | 未发布 GET 样例含 `M_SYNTH_COLLAB_INDEX`；另有 `M_SYNTH_191_1` compute（库名是合作网络密度模型，不是专题指数快照） | 部分对应 |
| `synthCollabBatch + result.completeness` | 图标题写到完整度，无同路径字段 | 主 GET 未发布 | 部分对应 |
| `synthCollabBatch + result.centrality` | 图标题写到中心度，无同路径字段 | 主 GET 未发布 | 部分对应 |
| `synthCollabBatch + result.density` | 图标题写到密度，无同路径字段 | `M_SYNTH_191_1` compute 可用，响应不是专题 `density` 字段 | 部分对应 |
| `synthCollabBatch + result.relationInput` | 有「协同链路」`M_COMP_INNOV_SYNERGY_LINK`，不是联合专利/项目/人才流动三分 | 无 `M_SYNTH_COLLAB_RELATION_INPUT` 端点 | 部分对应 |
| `synthCollabBatch + result.effectEval` | 有「协同效果」`M_COMP_INNOV_SYNERGY_EFF`，不是 Pearson 散点 | 未发布 GET 样例提到 `M_SYNTH_COLLAB_OUTPUT_CORR` | 部分对应 |

### 同 catalog 里、但不是这三叶 mock 的实现

这些是 `java_api` / `available`，不要当成专题 batch-snapshot 已落地：

| endpoint id | 路径 | 指标 |
|---|---|---|
| `comp.tech-outcome.m_synth_182_1` | `POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute` | 区域科技创新成果综合评价 |
| `comp.talent-outcome.m_synth_184_1` | `POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute` | 区域产业创新人才综合评价 |
| `comp.policy-outcome.m_synth_185_1` | `POST /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute` | 区域产业创新政策综合评价 |
| `comp.element-synthesis.m_synth_elem_contrib` | `POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute` | 要素贡献 |
| `comp.synergy.m_synth_191_1` | `POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute` | 协同密度模型 |

`comp.industry-outcome.main` 仍是未发布 GET，没有 183 的 compute 条目。`comp.graph.*` 是产业全要素图谱，`local_mock` / `available`，指标 `M_COMP_GRAPH_116_1`，不是三叶快照。

## 偏离

无实现偏离。结论是对照，不把「页面在」写成「接口已实现」。

## 产物清单

- 本 handoff
- 未改 `demo-ui-system-test`、`lumen-ui-algo-apiview`、`lumen-ui-topic`

## 验收证据

- 2026-10-28 读 `industryCompMenuConfig.ts`、`compModelCatalog.ts`，并用脚本抽出 `comp.json` 每条 endpoint 的 id、path、runtime、status、metric 号
- 无业务仓 commit

## 架构合规自检

- ✅ 调用链：只读对照，未新增越层调用
- ✅ 算法只在 Python：未写算法、未改 compute
- ✅ 图谱：未改 Nebula 协议；图谱页只作「非三叶」标注
- ✅ 可观测：未改埋点
- ✅ CI：文档落编排仓
- ✅ demo 不 merge 进 lumen
- ✅ D12：未让 lumen 调 demo-ui-system-test
- ✅ 未把 local_mock/unavailable 标成已实现

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 35000 |
| model_used | cursor-grok-4.7 |
| actual_cost | 0.21 |
| cost_warn | green |

单价表无 Grok 行。按 algorithm-agent 比例 0.75/0.25、claude-sonnet-4.5 单价作上限：`35000×0.75×3/1e6 + 35000×0.25×15/1e6 = 0.21`。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：随本 handoff 提交
- pipeline：编排仓无业务 CI
- 部署：无

## 涉及文件

- `repos/demo-ui-system-test/src/views/industry-comp/industryCompMenuConfig.ts`
- `repos/demo-ui-system-test/src/views/industry-comp/compModelCatalog.ts`
- `repos/lumen-ui-algo-apiview/src/catalog/comp.json`
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/LUMEN-INTEL-MOCK-INV-L01.md`
