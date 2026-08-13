# DEMO-CHAIN-PY-JOB-REGIONAL-L01 · 产业链 Python — 区域指数 + 竞争力两键 Graph

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-REGIONAL-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §4 REGIONAL  
> 契约：[`DESIGN-LANDING-regional_index.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/DESIGN-LANDING-regional_index.v0.md) · [`DESIGN-LANDING-regional_competitiveness.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/DESIGN-LANDING-regional_competitiveness.v0.md) · [`ISOMORPH-chain-analysis-jobs.v0.md`](../产品整体定义/E2-产业链分析/ISOMORPH-chain-analysis-jobs.v0.md) §3.3  
> GRAPH 补声明：[`GRAPH-regional_index.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/GRAPH-regional_index.v0.md) · [`GRAPH-regional_competitiveness.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/GRAPH-regional_competitiveness.v0.md)  
> Demo：`demo-ui-topic` `IndustryRegionalPage.tsx`（`maxObjects=5`）  
> 依赖：[`DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md`](./DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md) · [`DEMO-CHAIN-PY-JOB-RUNTIME-L01.md`](./DEMO-CHAIN-PY-JOB-RUNTIME-L01.md)

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock | 24h（coordinator 开工写入） |
| 说明 | 已 claimed + in_progress 后本会话落地；feature 完工进 `integration`，不标 done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过两键分菜谱、对象上限 maxObjects=5、诚实空、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 SHENZHEN。未改 Java、未改 PANORAMA 发布 / CYCLE / KEY-LINK / BOTTLENECK 菜谱行为。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求两份 DESIGN-LANDING / ISOMORPH §3.3 / RegionalPage 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

同一厨房、**两道菜谱、两个 Bid 叶子，禁止合并**：

| task_type | graph_version | 口诀 |
|---|---|---|
| `chain:regional:index` | `regional_index.graph.v1` | 产业×区域 + 加权指数排名；LLM 不作分数真源 |
| `chain:regional:competitiveness` | `regional_competitiveness.graph.v1` | 竞争力三维，不与指数四力混用 |

仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`。对象栏校验在 `regional_common.py`；配置/打分隔离在各自模块。

### Graph 声明（本单补；未另开架构单）

LANDING §13 原「GRAPH 待建」。本单写入上述两份 GRAPH md，并绑定厨房。

| 段 | stage_code | 指数 | 竞争力 | LLM？ |
|---|---|---|---|---|
| N1 | `freeze` | 对象+模板+计入项+权重 | 对象+三维权重=100% | 否 |
| N2 | `load_base_scores` | 底分就绪 | 同/简化 | 否 |
| N3 | `score` | 四力加权+排名 | 三维合成+排名 | 否 |
| N4 | `gap_explain` | 规则短板；LLM 只叙述 | 同 | 可选轻 |
| N5 | `validate_assemble` | KPI+排名+四力+叶子 | 柱状+热力+GIS 条件+明细 | 否 |

硬约束落地：

- 对象 `industry × region`：1 产业×1～5 区域，或 2～5 产业×1 区域；超 `maxObjects=5` → freeze `OBJECT_LIMIT_EXCEEDED`
- 指数四力（产业力/创新力/学术力/支撑力，QC11 临时）≠ 竞争力三维（产业基础/学术生态/创新生态）；竞争力权重含四力键 → `VALIDATION_DIM_MIXED`
- 配置即时汇总不在本 Graph；Execute 才冻结权重/计入项
- 缺底分 → `BASE_SCORE_MISSING` 或 `incomparable`；Q056/QC07 不作分数
- LLM 关仍有规则短板 + 计算分；LLM 回写分数/排名被丢弃
- Complete 成功只交 `result_payload`；厨房仍剥离 `result_snapshot_id`
- 不写 `industry_chain_graph_snapshot`

### result_payload 要点

**指数** `chain.regional_index.result_payload.v1`：`kpi.composite_index` 锚定第 1 名主体；`sections.ranking_comparison` / `dimension_scores` / `leaf_contributions` / `advantage_gap` / `config_honesty`。

**竞争力** `chain.regional_competitiveness.result_payload.v1`：`kpi.composite_competitiveness`；`bar_ranking` / `heatmap_matrix` / `heatmap_gis`（multi-industry 省略）/ `dimension_comparison` 同源 `art.score_bundle`。

## 偏离

| 项 | 说明 |
|---|---|
| QC11 四力文案 | LANDING 用产业力/创新力；Demo 页为商业力/技术力。Python Result 用 LANDING 键，输入接受 Demo 别名；诚实条写 QC11 |
| 竞争力三维文案 | LANDING 产业基础/学术生态/创新生态；Demo 企业能力/学术生态/配套生态力。Result 用 LANDING 键，Demo 别名仅输入映射 |
| 底分 | ADS `industry_chain_region_scorecard` 可读则读；缺表/缺行不造 Demo 页假分。测试经 `base_scores` 注入，status=`mock`+`GAP-CHAIN-REG-METRICS` |
| Execute 仍同步跑完再 202 | 与 RUNTIME 厨房一致；未改 BackgroundTasks |
| 无 jsonschema 依赖 | 不变量用 Python 断言；未新增 pip 包 |

## 产物清单

- 代码：`lumen-algo-py` `0b44a46489d239f4af99f38af35cde9032d565bc`（`origin/dev`）
- GRAPH 补声明两份（见文首）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC 语义；未写 ADS graph_snapshot；未做 SHENZHEN；未改 CYCLE/PANORAMA/KEY-LINK/BOTTLENECK 菜谱节点

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**215 passed**, 1 skipped, 1 warning in 6.82s（Starlette TestClient deprecation，与本单无关；本单前约 204 绿）
- 两 graph 均注册并经 Execute 实跑五段
- `maxObjects=5`：6 区域 freeze `OBJECT_LIMIT_EXCEEDED`，未查 ADS
- 两键 result 形状可区分（指数无 `bar_ranking`；竞争力无 `leaf_contributions`/四力键）
- LLM 关仍有规则/计算分（深圳综合指数 75.0）
- LLM 叙述不改分数/排名
- 厨房 Complete 无 `result_snapshot_id`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| QC05 / QC11 / GAP-CHAIN-REG-METRICS | 口径未甲方确认；UI 须带 🟡 |
| 底分 ADS | scorecard 未灌数时须注入或失败，禁止静默假市场 |
| 真 LLM | 需 `LUMEN_ALGO_CHAIN_LLM_API_KEY` + `LUMEN_ALGO_CHAIN_LLM_URL`；默认规则短板 |
| SHENZHEN | 本单明确不做 |
| 段 C Java | Snapshot 签发 / wait_view / Complete schema 门禁（Java 已白名单两键，本单未改 Java） |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`0b44a46489d239f4af99f38af35cde9032d565bc`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径仍挂在原 API
- 本地：pytest 215 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：Execute body 或 `current_trace_id()` 写入 Stage/Complete
- 未第二套中间件

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只经已有 Execute；回调 Java；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `0b44a46489d239f4af99f38af35cde9032d565bc` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_* scorecard；不写 graph_snapshot |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ `M_CHAIN_REGION_INDEX` / `M_CHAIN_COMPETITIVENESS_INDEX` + QC11/GAP；禁止假市场/Q056 当分数 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/regional_common.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/regional_index.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/regional_competitiveness.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_regional.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`
- `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/GRAPH-regional_index.v0.md`
- `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/GRAPH-regional_competitiveness.v0.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 240000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.44 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`240000 × (0.75×3 + 0.25×15) / 1e6 = 1.44`。

## 联调确认

**联调通过 / 联调确认**：pytest 215 绿；两 graph 五段 ReportStage 实跑；maxObjects=5 超限 freeze 失败；两键 result 形状可区分；LLM 无密钥时规则/计算分仍在；Complete 无自造 `result_snapshot_id`；缺底分诚实失败；Q056 不作指数分；SEARCH/SYNC 路由仍在。本 agent **不**把任务标 `done`（feature → `integration`）。
