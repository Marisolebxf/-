# LUMEN-INTEL-METRIC-XREF-L01

综合智能分析 mock 挂载的 metric_id 与指标库对应关系。只读。未改种子、未改口径、未把 D1 改绿。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 用户要求连续执行。监管人取 `dispatch-rules.yaml` data-agent 默认监管。行主键来自 `LUMEN-INTEL-MOCK-INV-L01`。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 指标对照。查询只走 metric-registry MCP，不读 `metrics/registry` YAML。 |

## 范围与实现

查法：`metric-query` `domain=SYNTH` `limit=80`（返回 46 条，字段含中文名、`algorithm_type`、D1、D4、`found.seed`、`found.matrix`）。种子里有、查询结果里没有的 id，再用 `metric-get` 确认。

种子 22 个 id。21 个在库（seed 与 matrix 都有）。D1 全部是 `aligned`，D4 全部是 `mock`。`algorithm_type` 没有 `UNKNOWN`。

前端种子的 `def_status` 仍是 missing 或 draft。这和指标库当前 D1=`aligned` 不是同一份状态。本单只记下差，不改 `intelMetricSeed.ts` / `synthReadinessSeed.ts`。

### 种子有、库也有

| 行主键 | metric_id | 种子中文名 | 库中文名 | 库 algorithm_type | 库 D1 | 库 D4 | 种子 def_status |
|---|---|---|---|---|---|---|---|
| `synthVitalityBatch + result.vitalityIndex` | `M_SYNTH_VIT_INDEX` | 区域创新活力指数 | 同左 | MODEL | aligned | mock | missing |
| `synthVitalityBatch + result.dimScores` | `M_SYNTH_VIT_DIM_SCORE` | 四维单维评分 | 同左 | MODEL | aligned | mock | draft |
| `synthVitalityBatch + result.dimScores.weight` | `M_SYNTH_VIT_WEIGHT` | 维度权重分布 | 活力指数权重配置与权重弹性 | STAT | aligned | mock | missing |
| `synthVitalityBatch + result.indicators` | `M_SYNTH_VIT_INDICATOR` | 活力分项指标值与得分 | 同左 | MODEL | aligned | mock | draft |
| `synthVitalityBatch + result.ranks` | `M_SYNTH_VIT_RANK` | 对比范围活力排名 | 同左 | STAT | aligned | mock | missing |
| `synthElementBatch + result.compositeIndex` | `M_SYNTH_ELEM_INDEX` | 区域创新要素指数（综合） | 同左 | MODEL | aligned | mock | missing |
| `synthElementBatch + result.typeIndex` | `M_SYNTH_ELEM_TYPE_INDEX` | 区域创新要素类型指数 | 同左 | MODEL | aligned | mock | missing |
| `synthElementBatch + result.typeScores` | `M_SYNTH_ELEM_TYPE_SCORE` | 七要素类型维得分 | 同左 | MODEL | aligned | mock | draft |
| `synthElementBatch + result.levelIndex` | `M_SYNTH_ELEM_LEVEL_INDEX` | 区域创新要素层次指数 | 同左 | MODEL | aligned | mock | missing |
| `synthElementBatch + result.levelScores` | `M_SYNTH_ELEM_LEVEL_SCORE` | 七大结构层次评价 | 同左 | MODEL | aligned | mock | draft |
| `synthElementBatch + result.domainIndex` | `M_SYNTH_ELEM_DOMAIN_INDEX` | 区域创新要素领域指数 | 同左 | MODEL | aligned | mock | missing |
| `synthElementBatch + result.indicators` | `M_SYNTH_ELEM_INDICATOR` | 要素分项指标值与得分 | 同左 | MODEL | aligned | mock | draft |
| `synthElementBatch + result.lensWeights` | `M_SYNTH_ELEM_WEIGHT` | 类型/层次/领域权重分布 | 同左 | STAT | aligned | mock | missing |
| `synthElementBatch + result.contributions` | `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 | 同左 | MIXED | aligned | mock | missing |
| `synthElementBatch + result.ranks` | `M_SYNTH_ELEM_RANK` | 对比范围要素综合排名 | 同左 | STAT | aligned | mock | missing |
| `synthCollabBatch + result.collabIndex` | `M_SYNTH_COLLAB_INDEX` | 区域创新协同指数 | 同左 | MODEL | aligned | mock | missing |
| `synthCollabBatch + result.completeness` | `M_SYNTH_COLLAB_COMPLETENESS` | 协同网络完整度 | 同左 | STAT | aligned | mock | draft |
| `synthCollabBatch + result.centrality` | `M_SYNTH_COLLAB_CENTRALITY` | 协同网络中心度 | 协同网络中心度（平均点度中心性） | GRAPH | aligned | mock | draft |
| `synthCollabBatch + result.density` | `M_SYNTH_COLLAB_DENSITY` | 协同网络密度 | 同左 | GRAPH | aligned | mock | draft |
| `synthCollabBatch + result.relationInput` | `M_SYNTH_COLLAB_RELATION_INPUT` | 合作关系输入构成 | 协同关系输入统计 | STAT | aligned | mock | draft |
| `synthCollabBatch + result.effectEval` | `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联 | 协同—创新产出关联结果 | MODEL | aligned | mock | missing |

中文名不一致的四条：`M_SYNTH_VIT_WEIGHT`、`M_SYNTH_COLLAB_CENTRALITY`、`M_SYNTH_COLLAB_RELATION_INPUT`、`M_SYNTH_COLLAB_OUTPUT_CORR`。id 仍是同一条。

### 种子有、库无

| 行主键 | metric_id | 种子中文名 | 库 |
|---|---|---|---|
| `synthElementBatch + result.evaluationDimensions` | `M_SYNTH_ELEM_FOUR_DIM_SCORE` | 要素评价四维得分 | `metric-get` 返回 Metric not found，无建议 id |

### 库有、三叶 mock 未挂

与三叶直接相邻的模型号（preview 的 compute / 未发布 GET 已引用，专题种子未挂）：

| metric_id | 库中文名 | algorithm_type | D1 | D4 |
|---|---|---|---|---|
| `M_SYNTH_186_1` | 区域创新活力综合分析模型 | MIXED | aligned | mock |
| `M_SYNTH_187_1` | 区域创新要素类型综合评价模型 | MIXED | aligned | mock |
| `M_SYNTH_188_1` | 区域创新要素层次综合评价模型 | MIXED | aligned | mock |
| `M_SYNTH_189_1` | 区域创新要素领域综合评价模型 | MIXED | aligned | mock |
| `M_SYNTH_190_1` | 区域创新要素综合分析模型 | MIXED | aligned | mock |
| `M_SYNTH_191_1` | 区域创新协同分析模型（合作网络密度） | MIXED | aligned | mock |

同域但不是这三叶页面的，种子也不该被要求挂上：`M_SYNTH_182_1`–`M_SYNTH_185_1`（科技/产业/人才/政策成果模型），`M_SYNTH_GRAPHAPI_116_1`，以及 `M_SYNTH_DS_21_*`、`M_SYNTH_DS_23_*` 图谱算法条。本次 `metric-query` 共 46 条，除上表 6 个模型号和种子已挂的 21 条外，其余落在这一组。

## 偏离

无口径改写。前端副本把多条标成 missing，指标库 D1 已是 aligned 且 D4 仍是 mock。两边都保持原样。

## 产物清单

- 本 handoff
- 未改指标种子、就绪度矩阵、前端镜像

## 验收证据

- 2026-10-28 `metric-query domain=SYNTH limit=80`：matched 46
- `metric-get M_SYNTH_ELEM_FOUR_DIM_SCORE`：not found
- 未打开 `cfg_metric-*.yaml` / `metric-readiness-matrix-*.yaml`

## 架构合规自检

- ✅ 调用链：未改接口
- ✅ 算法只在 Python：未改公式实现
- ✅ 图谱：未改 Nebula
- ✅ 可观测：未改埋点
- ✅ CI：文档落编排仓
- ✅ D9：只读消费指标库，未在前端把状态改绿
- ✅ 未把 D1–D4 写成 8 件套字段；表中 D1/D4 与 algorithm_type 分开列
- ✅ 未直读 registry YAML

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 25000 |
| model_used | cursor-grok-4.7 |
| actual_cost | 0.14 |
| cost_warn | green |

单价表无 Grok 行。按 data-agent 比例 0.80/0.20、claude-sonnet-4.5 单价作上限：`25000×0.8×3/1e6 + 25000×0.2×15/1e6 = 0.14`。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：随本 handoff 提交
- pipeline：编排仓无业务 CI
- 部署：无

## 涉及文件

- `repos/lumen-ui-topic/src/mock/intel/intelMetricSeed.ts`（只读）
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/LUMEN-INTEL-MOCK-INV-L01.md`
- 指标库经 MCP，无本地 YAML 改动
