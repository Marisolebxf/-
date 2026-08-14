# LUMEN-CHAIN-E-FIX-KEYLINK-L01 · 段 E C1 — key_link freeze 失败

> 日期：2026-08-14  
> Task ID：`LUMEN-CHAIN-E-FIX-KEYLINK-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 缺陷包：[`LUMEN-CHAIN-E-QA-SMOKE-L01-defect-US-CHAIN-DIAG-03.md`](./LUMEN-CHAIN-E-QA-SMOKE-L01-defect-US-CHAIN-DIAG-03.md)  
> 规约：[`长任务执行规约.md`](../../长任务执行规约.md) §11.3–11.5  
> 对照：[`DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md`](./DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md) N3

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |
| 说明 | registry 已 claimed；本会话开工即 `in_progress`。bugfix 完工进 `pending_test`，不标 done；未动 E1 `ready_to_sign`。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只去掉 freeze 对 `items[status=ready]` 的硬闸；未另开校验层、未改 Java/前端、未写正式库、未把 Job failed 收成 C3。N3 missing/mock、object 校验、未确认闸门保留。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 缺陷包 + KEY-LINK handoff + freeze 源码短，未 compress。 |

## 问题清单

- 已发布金路径 Create 200，task `CHAIN-20260814-009`，freeze **failed**（约 1s）。期望 succeeded + wait_view 未发生 → 规约 §11.3 必红，§11.4 **C1**（不是 C3）。
- X-Trace-Id=`521c5d529045618049844db2edf4bb11`。Tempo：Java async 对 `/stages` 与 `/complete` 均为 **200**（厨房业务失败，非 5xx）。

## 根因（已用代码+测试核实）

**根因错误码：`VALIDATION_FACTORS_UNAVAILABLE`。**

`node_freeze` 要求 `REQUIRED_FACTORS ⊆ factors.items[status=ready]`。金路径实际 payload：

| 层 | 行为 |
|---|---|
| 前端 `buildChainCreateRequest` | key_link 只设 `factors.user_confirmed=true`（另有 `userConfirmed`/`ready` 布尔），**不传** `factors.items` |
| Java `ChainAnalysisAdapterImpl.validateCreateParams` | 只要 `factors` 存在且 `user_confirmed`；单测 `keyLinkAcceptsConfirmedDraft` 无 items |
| Java `buildExecuteBody` / `ChainJobSnapshotSupport.buildInputPayload` | **有**把 draft `putAll` 进 `input_payload`（含 object + factors）。**不是** Java 掉 payload，本单不 blocked、不派 api-agent |
| Python `key_link.node_freeze`（修前） | 无 ready items → `VALIDATION_FACTORS_UNAVAILABLE`，约 1s Complete(failed) |

缺因子应按 KEY-LINK N3 在 `score_high_end` 出 `status=missing` / 有值则 `mock`，不得在 freeze 挡死金路径。用户未确认仍为 `VALIDATION_FACTORS_NOT_CONFIRMED`。`object.type` 非 `industry_chain` / 无 `chain_id` 仍为 `INPUT_OBJECT_INVALID`。未猜 DDL（不是 C5）。

## 修改内容

- 删除 freeze 的 `REQUIRED_FACTORS ⊆ ready items` 闸门与无用常量。
- `industry_chain` + `chain_id` + `user_confirmed=true` 即可过 freeze；items 缺省/非 ready 则 `factor_values` 空，后续 score missing。
- pytest：`test_freeze_user_confirmed_without_ready_items`（金路径）；`test_freeze_not_confirmed` 仍红。

## 测试结果

```text
python -m compileall -q lumen_algo_service lumen_algo_worker lumen_common
python -m pytest -q -p no:cacheprovider --ignore=vendor
```

- **259 passed**, 1 skipped, 1 warning（Starlette TestClient deprecation，与本单无关）
- 仅 `user_confirmed`、无 items：Complete `succeeded`，`error_code` 非 `VALIDATION_FACTORS_UNAVAILABLE`，五环节 `high_end_index.status=missing`
- `user_confirmed=false` → `VALIDATION_FACTORS_NOT_CONFIRMED` / `failed_stage_code=freeze`
- 错误 object → `INPUT_OBJECT_INVALID`（旧测仍绿）

## 偏离

无。未改 Java/前端；未写 `gkxlumenx_*`；未把失败收成空态。

## 产物清单

- 代码：`lumen-algo-py` `4c6a6a5313c8f8b27e3e7099f432210537407dfb`（已 `git push origin/dev`）
- 本 handoff

## 验收证据

- 本地 pytest 259 绿 + 已 push
- 已发布页仍是旧镜像，**须 E0 再滚 `lumen-algo-py` 后只复测** `US-CHAIN-DIAG-03` → `US-CHAIN-DIAG-04`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| **需要 E0** | **是。** 点名 `lumen-algo-py`（api/worker 镜像）。Java / `lumen-ui-topic` 本单未改，不必为修 freeze 单滚它们 |
| 缺因子 UI | 高端化指数 `missing` + `GAP-CHAIN-DIAG-METRICS`；总控 #4 不允许把 Job failed 当空态，succeeded 后缺分仍是诚实指标，不是 C3 挡 succeded |
| OTLP | algo-py collector DNS 残差未修（不在本单） |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`4c6a6a5313c8f8b27e3e7099f432210537407dfb`
- pipeline：push 后 GitLab `py:test` 接管
- K8s rollout：**需要 E0** 后才上已发布金路径
- 本地：pytest 259 绿

## 可观测性

- OTEL_SERVICE_NAME：`lumen-platform-algo-py`
- 缺陷 Create `X-Trace-Id`：`521c5d529045618049844db2edf4bb11`
- Tempo：Java Complete 200；Python span 可能仍丢（OTLP），本单未改采集

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 未改调用链 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j |
| 4 | 可观测 | ✅ 未拆 OTel；trace_id 仍走厨房 |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `4c6a6a5313c8f8b27e3e7099f432210537407dfb` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-* |
| 7 | Java 不写算法 | ✅ 核实 Java 已传 payload；未改 Java |
| 8 | ADS；不写正式库 | ✅ 无闸门写 `gkxlumenx_*` |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 / 诚实降级 | ✅ 缺因子走 missing/mock，不挡 freeze |
| 12 | D12 | ✅ 未打 demo-* 服务 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/key_link.py`
- `repos/lumen-algo-py/tests/test_chain_key_link.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.59 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 `budget-estimate.md` Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`98000 × (0.75×3 + 0.25×15) / 1e6 = 0.59`。

## 联调确认

**联调通过 / 联调确认**：本地 pytest 259 绿；已 push `origin/dev` `4c6a6a5313c8f8b27e3e7099f432210537407dfb`。未在已发布页复测（须 E0）。本 agent 将本单标 `pending_test`，**不**标 `done`，**不**动 E1。
