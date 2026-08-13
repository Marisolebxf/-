# DEMO-CHAIN-PY-JOB-BOTTLENECK-L01 · 产业链 Python — chain:diagnosis:bottleneck

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-BOTTLENECK-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 / §6 BOTTLENECK  
> 契约：[`DESIGN-LANDING-bottleneck.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-bottleneck.v0.md) · [`ISOMORPH-chain-analysis-jobs.v0.md`](../产品整体定义/E2-产业链分析/ISOMORPH-chain-analysis-jobs.v0.md) §3.2 · [`DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806.md)  
> 样板：[`DESIGN-LANDING-key_link.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-key_link.v0.md) · [`DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md`](./DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md)  
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
| 说明 | 未用 YAGNI 跳过同构 Graph 五段、词汇纪律、诚实空、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 CYCLE/REGIONAL/SHENZHEN/PANORAMA。未改 Java、未改 KEY-LINK 菜谱行为、未改 Nebula 投影入口。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 DESIGN-LANDING-bottleneck / ISOMORPH / key_link 样板禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

同构扩展：`task_type=chain:diagnosis:bottleneck`，`graph_version=bottleneck.graph.v1`。仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`；菜谱在 `lumen_common.algorithms.chain.bottleneck`。

口诀：同 `industry_chain` + 健康度确定性 + **规则**标瓶颈/卡脖子 + LLM 只写成因/建议。

### Graph 声明（本单补；未另开架构单）

无独立 `GRAPH-bottleneck.v0.md`。以下按 DESIGN-LANDING §5 钉死，并写入 `BOTTLENECK_LABELS` + `bottleneck.py` 模块头。

| 段 | stage_code | Bid / Wireframe 可见文案 | LLM？ | 主 Artifact |
|---|---|---|---|---|
| N1 | `freeze` | 任务提交与产业链对象冻结 | 否 | `art.context` |
| N2 | `timeseries` | 整合各环节技术/人才/资本/政策等时序数据 | 否 | `art.timeseries_bundle` |
| N3 | `score_health` | 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度 | 否 | `art.link_health_scores` |
| N4 | `annotate_bottleneck` | 瓶颈智能识别与卡脖子环节归因/改进建议生成 | 建议可 LLM | `art.bottleneck_bundle` |
| N5 | `validate_assemble` | 结果可信性校验与靶向方案/报告组装 | 否 | `art.result_payload` |

过程 Steps 含四核心指标词：技术成熟度 / 人才供给量 / 融资事件 / 政策覆盖率。维名展示「资本」。

**复用（禁止第二套注册表）**

```python
from lumen_common.algorithms.chain.job_runtime import GRAPH_REGISTRY, execute_chain_job
from lumen_common.algorithms.chain.bottleneck import (
    node_freeze, node_timeseries, node_score_health,
    node_annotate_bottleneck, node_validate_assemble,
)
```

硬约束落地：

- N1：`object_type=industry_chain`；五维 `user_confirmed`+`ready`（tech/talent/market_demand/capital/policy）；拒绝 `dim_key=资金`
- N2：五环节骨架（rd/design/manufacturing/sales/service）；时序未接通 → `honesty.timeseries.mode=unavailable`，允许继续；骨架不缺
- N3：四核心等权临时健康分；缺任一核心 → `status=missing`，不造假分；有值 → `status=mock` + `gap_ref=GAP-CHAIN-DIAG-METRICS`；L1 `band ∈ {稳健,关注,薄弱}`
- N4：**规则** `薄弱 ∧ 时序 trend=down` 才入 `bottlenecks[]`（故 **薄弱 ≠ 瓶颈**）；`is_choke = 瓶颈 ∧ severity=高`（临时：健康分 < 50 → 高）；LLM 只写成因/建议；无密钥则跳过叙述，规则仍跑
- N5：`result_payload` 对齐 `chain.bottleneck.result_payload.v1`；不自签 `result_snapshot_id`；payload 禁「断链」「资金」
- Complete 成功只交 `result_payload`；厨房仍剥离 snapshot id
- 不写 `industry_chain_graph_snapshot`；Execute 入口仍 `assert_demo_mysql_targets`

### 词汇自检

| 项 | 结果 |
|---|---|
| L1 band | 稳健 / 关注 / 薄弱 |
| L2 瓶颈 | 规则角标；`band=薄弱` 不强制入选（成功路径：服务=薄弱但非瓶颈，制造=薄弱且瓶颈） |
| L2+ 卡脖子 | 瓶颈 ∧ severity=高；计数 ⊆ 瓶颈数 |
| 禁词「断链」 | payload / Complete 体均无 |
| 维名「资本」 | freeze 拒绝「资金」；类型展示用技术/人才/资本/政策 |
| LLM | 即使回写 `is_bottleneck`/`band`/`health_score` 也不落判定 |

### result_payload 要点（成功路径）

- 五环节 `health_graph.nodes` + `link_health` 均有 band
- `kpi.choke_link_count ≤ kpi.bottleneck_count`
- 每个 `is_choke=true` 必有对应瓶颈项且 `severity=高`
- 无 LLM：`honesty.llm=degraded`，`node_details` 成因/建议空，规则瓶颈仍在
- KPI 带 `metric_id`：`M_CHAIN_BOTTLENECK_COUNT` / `SEVERITY` / `TYPE_DIST` / `M_CHAIN_CHOKE_LINK_COUNT`

## 偏离

| 项 | 说明 |
|---|---|
| GRAPH md | 无独立 `GRAPH-bottleneck.v0.md`；本单在代码模块头 + 本 handoff 声明五段，不另开架构单 |
| QC04 公式 | 四核心等权 + 分档阈值 75/60 + 瓶颈=薄弱∧下行 + 卡脖子分<50，均为临时默认 + honesty；不标 `ok` |
| 时序 | Demo 无 ADS 时序表；可注入 `stage_timeseries` 回放，否则 `unavailable` 继续 |
| 市场需求 | 五维包必确认；N3 健康分按 Bid 四核心，不把市场需求并进等权（QC04 未闭合） |
| Execute 仍同步跑完再 202 | 与 RUNTIME / KEY-LINK 厨房一致 |
| 无 jsonschema 依赖 | 不变量用 Python 断言；未新增 pip 包 |
| 未改 KEY-LINK 节点函数 | 只增注册绑定；key_link 测试仍绿 |

## 产物清单

- 代码：`lumen-algo-py` `b14b7b384ffbedbb00a5c79d2941212eb8ed74c1`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC / GRAPH 投影语义；未写 ADS graph_snapshot；未做 CYCLE/REGIONAL/SHENZHEN/PANORAMA

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**187 passed**, 1 warning in 2.46s（Starlette TestClient deprecation，与本单无关；KEY-LINK 时约 179 绿）
- 注册表含 `bottleneck.graph.v1`；默认 `chain:diagnosis:bottleneck`
- 成功路径：五环节健康带；服务薄弱但非瓶颈；制造瓶颈且卡脖子
- 禁词「断链」不出现在 payload
- LLM 关仍有规则瓶颈；厨房禁 `result_snapshot_id`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| QC04 / GAP-CHAIN-DIAG-METRICS | 口径未甲方确认；UI 须带 🟡 |
| 正式 GRAPH md / JSON Schema | 待从本声明抽出；实现以 Git 注册表为准 |
| 真 LLM | 需 `LUMEN_ALGO_CHAIN_LLM_API_KEY` + `LUMEN_ALGO_CHAIN_LLM_URL`；默认跳过 |
| CYCLE / REGIONAL / SHENZHEN | 本单未实现 |
| 段 C Java | Snapshot 签发 / wait_view / Complete schema 门禁 / 五维 Create 门禁 |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`b14b7b384ffbedbb00a5c79d2941212eb8ed74c1`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径仍挂在原 API
- 本地：pytest 187 绿

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
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `b14b7b384ffbedbb00a5c79d2941212eb8ed74c1` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；不写 graph_snapshot |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ KPI 四 metric_id + QC04/METRICS gap；禁止假分；薄弱≠瓶颈 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/bottleneck.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_bottleneck.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.08 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`180000 × (0.75×3 + 0.25×15) / 1e6 = 1.08`。

## 联调确认

**联调通过 / 联调确认**：pytest 187 绿；`bottleneck.graph.v1` 五段 ReportStage 实跑；LLM 无密钥时跳过叙述但规则瓶颈仍在；成功路径五环节健康带且薄弱≠瓶颈；payload 无「断链」；Complete 无自造 `result_snapshot_id`；未写 ADS graph_snapshot；KEY-LINK / RUNTIME / GRAPH 投影测试仍绿。本 agent **不**把任务标 `done`（feature → `integration`）。
