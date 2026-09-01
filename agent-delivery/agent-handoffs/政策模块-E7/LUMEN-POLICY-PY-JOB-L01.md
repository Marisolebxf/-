# LUMEN-POLICY-PY-JOB-L01 · /internal search + 分析 Job 只调 harness

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-PY-B-总派单.md`](./LUMEN-POLICY-PY-B-总派单.md)  
> 前序：[`LUMEN-POLICY-PY-HARNESS-L01.md`](./LUMEN-POLICY-PY-HARNESS-L01.md)（`dispatch` / `policy_*` worker）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新读面/Job 薄封装；复用 `polan.harness.dispatch` 与 DWD `connect()`；未改算子 `run()` / 打分 / 抽词；未另起厨房 Graph |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | HTTP 薄封装 + 假任务单测，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。产品链补 `/internal/policy/search` 读 DWD、`/internal/policy/jobs/execute` 只调 harness。灌数仍可调原 `run()` |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 偏离说明

- Job HTTP 挂在现网 `/internal/policy/**`（entan-py `policy_routes`），与已有 graph/status 同进程，便于专题 C Feign 一条前缀。未在 `lumen_algo_service` 再开第二套 `/internal/v1/policy`。
- 与 worker 对齐同一套 `sub_type` / `harness_mode` / `items`：`POST /internal/policy/jobs/execute` 进程内 `dispatch`；`/gdf/tasks/create-and-start` 仍由 worker `_run_policy_node` 调同一 `dispatch`。不是两套算子。
- 详情同时提供 `GET /internal/policy/docs/{id}` 与兜底 `GET /internal/policy/{id}`（静态段 search/graph/status 优先）。

## 产物清单

- 代码：`lumen-algo-py` `ea3acc39c215740560f9f64479ed352a87e75f22` → `origin/dev`
- 检索：`vendor/entan-py/polan/search.py`
- Job：`vendor/entan-py/polan/job.py` → `polan.harness.dispatch`
- 路由：`vendor/entan-py/api/policy_routes.py`
- worker 结果：`lumen_common/tasks/executor.py` 剥离 `result_snapshot_id`
- 流图：`storage/POLICY/01-data-flow.md` amendment_note（拓扑未改）
- 本文 handoff

## 新增 /internal 路径

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/internal/policy/search` | DWD `policy_base_info` 检索；空态诚实；非 `/v1/mock` |
| GET | `/internal/policy/docs/{id}` | 详情 |
| GET | `/internal/policy/{id}` | 详情兜底（避开 graph/status/search） |
| POST | `/internal/policy/jobs/execute` | 分析 Job，202，只调 harness |
| GET | `/internal/policy/metrics` | 与 `/v1/policy/metrics` 对称 |
| GET | `/internal/policy/indicators` | 与 `/v1/policy/indicators` 对称 |
| GET | `/internal/policy/graph` | 已有；Nebula 失败 `source≠nebula` |

已有未改：`/internal/policy/status` · `/models/registry` · `/run-pipeline` · `/sync-ods` · graph 写。

## Job 如何调 harness

1. 请求 `sub_type` ∈ `policy_timeseries` / `policy_regional` / `policy_shenzhen` / `policy_focus`（及 `policy_shard`）；别名 `timeseries` 等可映射。
2. `items` 或 `policy_ids`（与 `/gdf/tasks` 同字段）；`harness_mode` 默认 `auto`。
3. `execute_policy_job` → `polan.harness.dispatch`（sync / threadpool / fanin）。禁止 `eval.*.run()`。
4. `industry_vid` 仅 `chain:` / `segment:`（例 `chain:INB170101`）；拒绝 `INB1303` / 中文名。
5. ≥40000 条拒绝。Python **不**写 `result_snapshot_id`。
6. Worker 路径未拆：`TaskExecutor._run_policy_node` 仍只调 `dispatch`。

## 验收证据

- `python -m pytest -q tests/test_policy_job.py` → **10 passed**
- 连同 harness：`tests/test_policy_job.py tests/test_policy_harness.py` → **20 passed**
- search 空/有命中/DB 异常均 HTTP 200 不 5xx
- Job HTTP 202 且 `dispatch` 被调用；VID 非法 400
- graph Nebula 失败 `source != nebula`
- eval/basic/graph/text/models 本叶 **无 diff**

## 范围与实现

- 检索读 `demo_gkxlumenx_dwd.policy_base_info`（列表不拉 `content` LONGTEXT）；mysql 非 `demo_` 前缀拒绝。
- 专题 C-SEARCH Feign 本 search；禁止把 `/v1/policy/mock` 当专题路径。
- 灌数批处理仍走原 `eval/*.run()`，本叶未碰。

## 修改内容

| 路径 | 动作 |
|------|------|
| `vendor/entan-py/polan/search.py` | 新增 DWD 检索/详情 |
| `vendor/entan-py/polan/job.py` | 新增 Job 入口 → harness.dispatch |
| `vendor/entan-py/api/policy_routes.py` | search / jobs / metrics / indicators / 详情 |
| `lumen_common/tasks/executor.py` | 政策结果剥离 snapshot 键 |
| `tests/test_policy_job.py` | 空态、Job、VID、graph source |
| `storage/POLICY/01-data-flow.md` | amendment_note |

## 测试结果

```text
python -m pytest -q tests/test_policy_job.py
# 10 passed

python -m pytest -q tests/test_policy_job.py tests/test_policy_harness.py
# 20 passed
```

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`
- commit：`ea3acc39c215740560f9f64479ed352a87e75f22`
- pipeline：push 后 GitLab `dev`；`image:api` / entan 制品随 origin/dev
- 部署：`gkxlumen-platform-entan-py` 吃到 `/internal/policy/search|jobs/execute`
- 本叶未改 helm JDBC、未 CREATE SPACE、未写 `gkx_chain`

## 可观测性

- OTEL_SERVICE_NAME：entan-api `gkxlumen-entan-py-api`；worker `lumen-platform-algo-py-worker`
- Job 计算 span 仍在 harness：`gkx.polan.policy.harness`
- 算子内部 span 未改

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 前端→Java→Python `/internal/*` | ✅ 专题路径仅 `/internal/policy/**`，未给前端 `/v1` |
| 图谱 Nebula `demo_gkx_chain` | ✅ 未 CREATE `gkx_policy`、未写 `gkx_chain`；失败 source 诚实 |
| 可观测 | ✅ 复用 harness span |
| CI/CD | ✅ 推 `origin/dev`；禁 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ 未改正式 JDBC |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改口径 |
| D12 lumen 不调 demo **服务** | ✅ |
| I2-12 不自签 snapshot | ✅ |
| 挂接 VID 只用图上链码 | ✅ |
| 禁止一次 load 4 万+ | ✅ |
| 禁止改算子方法 | ✅ |

## 遗留风险

- 现网 search 依赖 Demo DWD 有行；空库返回 `honesty.empty=true`，专题 C 需按空态渲染。
- `jobs/execute` 在 entan-api 进程内跑 harness；万级仍应走 `/gdf/tasks` + worker fan-in（同一 `dispatch`）。
- Java C-SEARCH / C-TASK 尚未 Feign；联调闸门等 C 叶。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 96000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.64 |
| cost_warn | green |
