# DEMO-CHAIN-PY-JOB-CYCLE-L01 · 产业链 Python — chain:diagnosis:cycle

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-CYCLE-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 / §6 CYCLE  
> 契约：[`DESIGN-LANDING-cycle.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-cycle.v0.md) · [`ISOMORPH-chain-analysis-jobs.v0.md`](../产品整体定义/E2-产业链分析/ISOMORPH-chain-analysis-jobs.v0.md) §3.1  
> 样板：[`DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md`](./DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md) · [`DEMO-CHAIN-PY-JOB-RUNTIME-L01.md`](./DEMO-CHAIN-PY-JOB-RUNTIME-L01.md)  
> Demo：`demo-ui-topic` `IndustryDiagnosisPage.tsx` cycle Tab

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
| 说明 | 未用 YAGNI 跳过对象纪律、规则判相、检索降级诚实、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 REGIONAL/SHENZHEN。未改 Java、未改 PANORAMA 发布 / SYNC 秒开 / KEY-LINK / BOTTLENECK 菜谱行为。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 DESIGN-LANDING-cycle / ISOMORPH §3.1 / DiagnosisPage 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

同构扩展：`task_type=chain:diagnosis:cycle`，`graph_version=cycle.graph.v1`。仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`；菜谱在 `lumen_common.algorithms.chain.cycle`。

口诀：换对象（**industry**，不是 industry_chain）+ 规则判相 + LLM 只解释。

### Graph 声明（本单补；未另开架构单）

无独立 `GRAPH-cycle.v0.md`。以下按 DESIGN-LANDING-cycle §5 钉死，并写入 `CYCLE_LABELS` + `cycle.py` 模块头。

| 段 | stage_code | Bid / DiagnosisPage 可见文案 | LLM？ | 主 Artifact |
|---|---|---|---|---|
| N1 | `freeze` | 任务提交与参数冻结 | 否 | `art.context` |
| N2 | `retrieve` | 整合产业参数与联网检索的历史与市场数据 | 否（检索可降级） | `art.retrieval_bundle` |
| N3 | `diagnose_stage` | 大语言模型推理与周期阶段判断（诊断） | 是（只解释） | `art.phase_diagnosis` |
| N4 | `forecast` | 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点 | 是（只归纳） | `art.forecast_bundle` |
| N5 | `validate_assemble` | 结果可信性校验与分析报告组装 | 否 | `art.result_payload` |

`stage_code` = Graph 过程步。业务相位用 `cycle_phase`（introduction/growth/maturity/decline）及中文导入/成长/成熟/衰退。禁止混用。

**复用（禁止第二套注册表）**

```python
from lumen_common.algorithms.chain.job_runtime import GRAPH_REGISTRY, execute_chain_job
from lumen_common.algorithms.chain.cycle import (
    node_freeze, node_retrieve, node_diagnose_stage,
    node_forecast, node_validate_assemble,
)
```

硬约束落地：

- N1：`object.type/object_type=industry`；拒绝 `industry_chain`；四参数区间 + `source` 枚举；`time_range.start < end`
- N2：ADS 主序列缺失/未覆盖时间窗 → `ADS_SERIES_UNAVAILABLE` 硬失败；检索旁路缺失 → `honesty.retrieval.mode=replay_snapshot|unavailable` 继续；**禁止** `mode=live` 与「全网检索完成」
- N3：**规则**产出非空 `candidates[]` 与 `primary_phase`；`cycle_phase` 始终等于规则主选；LLM 越权换相被拒，`phase_source=rule_fallback_after_llm`
- N4：`series_hist` 只复制 N2；预测 = 确定性线性外推；LLM 只写 drivers/拐点/决策摘要，改写序列点被丢弃
- N5：`result_payload` 对齐 `chain.cycle.result_payload.v1`；顶栏仅相位/判定；不自签 `result_snapshot_id`；不写 `graph_snapshot`
- Complete 成功只交 `result_payload`；厨房仍剥离 snapshot id
- Execute 入口仍 `assert_demo_mysql_targets`

### result_payload 要点（成功路径）

- `object.object_type=industry`
- `sections.diagnosis.cycle_phase ∈ {introduction,growth,maturity,decline}` 且 ∈ `candidates`
- `kpi.current_phase_label` 与相位中文一致（成长/导入/成熟/衰退）
- `honesty.retrieval.mode ∈ {replay_snapshot, unavailable}`；`live_claimed=false`
- payload 无「全网检索完成」/「已完成实时全网检索」
- 无 LLM：`phase_source=rule_primary`，规则相位仍在
- 用户覆盖参数 → `honesty.params.overridden=true`

## 偏离

| 项 | 说明 |
|---|---|
| GRAPH md | 无独立 `GRAPH-cycle.v0.md`；本单在代码模块头 + 本 handoff 声明五段，不另开架构单 |
| LLM 换相 | DESIGN §5.3 步骤 4 允许白名单内确认换相。本单按派单口诀「LLM 只解释、不得改 cycle_phase」：即使 LLM 返回其它 candidate 也不改相位 |
| QC03 公式 | 临时规则分（增长率/成熟度/利润率/序列斜率）；`rule_pack_version=temp.qc03.cycle_phase.v1` + honesty；不标 `ok` |
| 主序列 | Demo ADS 市场规模走 Q056 空值，禁止当 hist；测试注入 `series_hist`；实库无覆盖序列则硬失败 |
| Execute 仍同步跑完再 202 | 与 RUNTIME / KEY-LINK 厨房一致 |
| 无 jsonschema 依赖 | 不变量用 Python 断言；未新增 pip 包 |
| 未改 KEY-LINK / BOTTLENECK / PANORAMA 节点 | 只增 `cycle.graph.v1` 绑定 |

## 产物清单

- 代码：`lumen-algo-py` `8fce5ab013efb8ded6eee07747e38c43e69b81ad`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC / PANORAMA 发布 / KEY-LINK / BOTTLENECK；未写 ADS graph_snapshot；未做 REGIONAL/SHENZHEN

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**204 passed**, 1 skipped, 1 warning in 6.84s（Starlette TestClient deprecation，与本单无关；此前约 196 绿）
- 注册表含 `cycle.graph.v1`；默认 `chain:diagnosis:cycle`
- `object.type=industry` 才过 freeze；`industry_chain` → Complete(failed) `INPUT_OBJECT_INVALID`
- 相位由规则产出（成功路径 `growth` / 成长）；LLM 返回 `decline` 不改相位
- 检索降级 `mode=unavailable` 仍成功；payload 无「全网检索完成」
- 无主序列 → `ADS_SERIES_UNAVAILABLE`；厨房禁 `result_snapshot_id`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| QC03 / QC10 / Q056 | 周期口径与对标未甲方确认；市场规模正式空；UI 须带 🟡 |
| 正式 GRAPH md / JSON Schema / Prompt Pack md | 待从本声明抽出；实现以 Git 注册表为准 |
| 真 LLM | 需 `LUMEN_ALGO_CHAIN_LLM_API_KEY` + `LUMEN_ALGO_CHAIN_LLM_URL`；默认跳过 |
| REGIONAL / SHENZHEN | 本单未实现 |
| 段 C Java | Snapshot 签发 / wait_view / Complete schema 门禁（cycle 已白名单，本单未改 Java） |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`8fce5ab013efb8ded6eee07747e38c43e69b81ad`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径仍挂在原 API
- 本地：pytest 204 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：Execute body 或 `current_trace_id()` 写入 Stage/Complete
- 未第二套中间件

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只经已有 Execute；回调 Java；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；未改 `graph/project` |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `8fce5ab013efb8ded6eee07747e38c43e69b81ad` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；不写 graph_snapshot；Q056 序列不拿来假周期 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ `M_CHAIN_CYCLE_STAGE` / `M_CHAIN_PHASE_DETERMINATION` + QC03/Q056 gap；禁止假全网检索 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/cycle.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_cycle.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 230000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.38 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`230000 × (0.75×3 + 0.25×15) / 1e6 = 1.38`。

## 联调确认

**联调通过 / 联调确认**：pytest 204 绿；`cycle.graph.v1` 五段 ReportStage 实跑；仅 `industry` 过 freeze；相位由规则产出；LLM 不得改 `cycle_phase`；检索降级字段诚实且 payload 无「全网检索完成」；Complete 无自造 `result_snapshot_id`；未写 ADS graph_snapshot；KEY-LINK / BOTTLENECK / PANORAMA / SEARCH / SYNC 测试仍绿。本 agent **不**把任务标 `done`（feature → `integration`）。
