# DEMO-CHAIN-PY-JOB-SHENZHEN-L01 · 产业链 Python — 深圳对比 + 发展两键 Graph

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-SHENZHEN-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §4 SHENZHEN  
> 契约：[`DESIGN-LANDING-shenzhen_comparison.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/DESIGN-LANDING-shenzhen_comparison.v0.md) · [`DESIGN-LANDING-shenzhen_development.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/DESIGN-LANDING-shenzhen_development.v0.md) · [`ISOMORPH-chain-analysis-jobs.v0.md`](../产品整体定义/E2-产业链分析/ISOMORPH-chain-analysis-jobs.v0.md) §3.4 §3.5  
> GRAPH 补声明：[`GRAPH-shenzhen_comparison.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/GRAPH-shenzhen_comparison.v0.md) · [`GRAPH-shenzhen_development.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/GRAPH-shenzhen_development.v0.md)  
> Demo：`demo-ui-topic` `IndustryShenzhenPage.tsx`  
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
| 说明 | 未用 YAGNI 跳过标杆门禁、发展硬依赖 `source_result_id`、诚实空、路径 `<2` 硬失败、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 REPORT/NER。未改 Java。未改 REGIONAL/CYCLE/PANORAMA/KEY-LINK/BOTTLENECK 菜谱节点行为。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求两份 DESIGN-LANDING / ISOMORPH §3.4–3.5 / ShenzhenPage 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

同一厨房、**两道独立菜谱，禁止自动串联**：

| task_type | graph_version | 口诀 |
|---|---|---|
| `chain:shenzhen:shenzhen_comparison` | `shenzhen_comparison.graph.v1` | 固定深圳 + 1 产业 + 1~5 就绪标杆；四维分开；LLM 轻量可选 |
| `chain:shenzhen:shenzhen_development` | `shenzhen_development.graph.v1` | 显式 `source_result_id`；路径 LLM ≥2；规则校验数字 ⊆ 对比快照 |

仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`。共享常量在 `shenzhen_common.py`；配置/打分/路径隔离在各自模块。

### Graph 声明（本单补；未另开架构单）

LANDING §13 原「GRAPH 待建」。本单写入上述两份 GRAPH md，并绑定厨房。

| 段 | comparison | development | LLM？ |
|---|---|---|---|
| N1 | `freeze` 深圳固定 + 标杆 1~5 就绪 | `freeze` 绑 `source_result_id` + goals 三键 | 否 |
| N2 | `benchmark_ready_check` | `load_source` 只读对比 Result | 否 |
| N3 | `score_dimensions` 四维+矩阵+judgment_fields | `path_generate` ≥2 套路径 | 对比可选轻 / 发展核心 |
| N4 | `narrative` | `path_validate` 完整度+数字一致 | 对比可选 / 发展规则 |
| N5 | `validate_assemble` | `validate_assemble` | 否 |

硬约束落地：

- 对比：主体恒深圳；pending 标杆 Create/freeze 拒绝（`BENCHMARK_NOT_READY` / `NO_BENCHMARK`）
- 四维钉死 产业/专利/政策/人才，**禁止**合并标签；矩阵 `领先`/`相当`/`落后`
- `judgment_fields` 五键原文（技术成熟度/市场前景/技术可行性/发展阶段/阶段描述）；无顶栏「产业发展摘要」KPI
- 对比 Result `may_feed_development=true`，`carry_to_development.auto_run=false`；**不自签** `source_result_id` / `result_snapshot_id`
- 发展：缺 `source_result_id` → freeze `SOURCE_REF_INVALID`；`last_comparison_id` 等静默键不得顶替
- 无对比快照 → `SOURCE_LOAD_FAILED`，禁止空跑路径
- 路径 `<2` → `PATH_COUNT_LT_2`，**禁止**伪造补齐；引用数字 ∉ 源 → `PATH_NUMBER_INCONSISTENT`
- IC-36：`honesty.case_library=unavailable`，不得 `matched`
- Q056/QC07 不得作四维分；Complete 成功只交 `result_payload`；不写 `industry_chain_graph_snapshot`
- Execute 入口仍 `assert_demo_mysql_targets`

### result_payload 要点

**对比** `chain.shenzhen_comparison.result_payload.v1`：`dimension_comparison`（四行分维）/ `advantage_gap_matrix` / `synthesis_judgment` / `judgment_fields` / `carry_to_development`。

**发展** `chain.shenzhen_development.result_payload.v1`：`source_evidence` + 三类建议 + `paths[]`≥2 + `source_ref`。

## 偏离

| 项 | 说明 |
|---|---|
| 四维文案 | LANDING 产业/专利/政策/人才；Demo 页为 企业/专利/政策/人才。Python Result 用 LANDING「产业」，输入接受 `enterprise`/`企业` 别名 |
| 四维分数 | QC08 权重未闭合。无注入则等权 mock + `GAP-CHAIN-SZ-METRICS`，不抄市场规模/投融资假值 |
| 发展 goals | LANDING v0 三键必填；Demo 页允许少勾。Python freeze 要求政策/技术/人才均非空 |
| Execute 仍同步跑完再 202 | 与 RUNTIME 厨房一致；未改 BackgroundTasks |
| 无 jsonschema 依赖 | 不变量用 Python 断言；未新增 pip 包；JSON Schema 文件仍待建 |
| 对比 `source_result_id` | Python 置 `null`，由 Java Complete 签发；禁止自签 snapshot |

## 产物清单

- 代码：`lumen-algo-py` `170205977270cc9d6481c2ed5e931ae0de51fbd2`（`origin/dev`）
- GRAPH 补声明两份（见文首）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC 语义；未写 ADS graph_snapshot；未做 REPORT/NER；未改 REGIONAL/CYCLE/PANORAMA/KEY-LINK/BOTTLENECK 菜谱

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**225 passed**, 1 skipped, 1 warning in 6.84s（Starlette TestClient deprecation，与本单无关；REGIONAL 时 215 绿）
- 对比：四维分开；pending 标杆 freeze 失败；非深圳主体失败；LLM 关仍有矩阵+五字段；厨房无 snapshot id
- 发展：无 `source_result_id`（含 `last_comparison_id` 静默键）freeze `SOURCE_REF_INVALID`
- 发展：有对比 Result + 注入 ≥2 路径才 succeeded
- 发展：LLM 只出 1 条 → `PATH_COUNT_LT_2`，未补齐
- 发展：无快照 → `SOURCE_LOAD_FAILED`；编造 99.9 → `PATH_NUMBER_INCONSISTENT`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| QC08 / GAP-CHAIN-SZ-METRICS | 对标集合与四维权重未甲方确认；UI 须带 🟡 |
| IC-36 案例库 | honesty unavailable；上线前不得宣称匹配 |
| 真 LLM | 发展路径需 `LUMEN_ALGO_CHAIN_LLM_API_KEY` + `LUMEN_ALGO_CHAIN_LLM_URL`；无密钥则路径不足硬失败 |
| JSON Schema / Prompt Pack md | LANDING §13 仍待建；执行以 Python 注册表为准 |
| 段 C Java | Snapshot 签发 / wait_view / 源 Result 授权门禁（Java 已白名单两键，本单未改 Java） |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`170205977270cc9d6481c2ed5e931ae0de51fbd2`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径仍挂在原 API
- 本地：pytest 225 绿

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
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `170205977270cc9d6481c2ed5e931ae0de51fbd2` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 闸门 demo_*；不写 graph_snapshot |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ 四维 `M_CHAIN_SZ_*` + `GAP-CHAIN-SZ-METRICS` / QC08；禁止 Q056/QC07 当四维分 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/shenzhen_common.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/shenzhen_comparison.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/shenzhen_development.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_shenzhen.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`
- `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/GRAPH-shenzhen_comparison.v0.md`
- `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/GRAPH-shenzhen_development.v0.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 255000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.53 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`255000 × (0.75×3 + 0.25×15) / 1e6 = 1.53`。

## 联调确认

**联调通过 / 联调确认**：pytest 225 绿；对比四维分开且 pending 标杆失败；发展无 `source_result_id` freeze 失败、有对比 Result 才过；路径 `<2` 不伪补齐；厨房 Complete 无自造 `result_snapshot_id`；未自动串联两 Job；SEARCH/SYNC 路由仍在。本 agent **不**把任务标 `done`（feature → `integration`）。
