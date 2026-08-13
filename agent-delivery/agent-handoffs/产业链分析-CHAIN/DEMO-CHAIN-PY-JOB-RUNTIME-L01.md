# DEMO-CHAIN-PY-JOB-RUNTIME-L01 · 产业链 Python — Analysis Job Graph Runner（Execute/Stage/Complete）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-RUNTIME-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 第 6 条 / §6 RUNTIME  
> 契约：[`系统设计说明书-Analysis-Job-Runtime.v0.md`](../产品整体定义/E2-产业链分析/系统设计说明书-Analysis-Job-Runtime.v0.md) · [`CONTRACT-Java-Python-Analysis-Job-v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/CONTRACT-Java-Python-Analysis-Job-v0.md)  
> 依赖：[`DEMO-CHAIN-PY-SHARED-L01.md`](./DEMO-CHAIN-PY-SHARED-L01.md)

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
| 说明 | 未用 YAGNI 跳过失败路径、回调契约、handoff、pytest、demo_ 闸门。未实现七键算法本体 / Nebula 投影 / Java Snapshot。复用 SHARED 包，未另开第二套 chain 路径。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 Runtime/CONTRACT 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

厨房 Graph Runner：权威 Job 状态机仍在段 C Java。Python 一次跑完传入 Graph，回调 ReportStage / Complete，**不自签** `result_snapshot_id`，**不**把 `succeeded` 伪装成已查看（wait_view 留给 Java）。

**复用 SHARED（禁止第二套包）**

```python
from lumen_common.algorithms.chain import (
    assert_demo_mysql_targets,
    current_trace_id,
    execute_chain_job,
    GRAPH_REGISTRY,
    register_graph,
)
```

本单增量：`lumen_common/algorithms/chain/job_runtime.py`；路由挂在已有 `lumen_algo_service.views.chain` 同一前缀。SEARCH/SYNC 行为未改。

### Execute / 回调路径

```text
Java  POST /internal/v1/chain/jobs/execute
        body: task_id, task_type, analysis_key, input_snapshot_id,
              input_payload, schema_version, graph_version,
              callback{stage_url, complete_url}（或 callbacks 别名 / job_callback_base_url）
        ← 202 {accepted, task_id, input_snapshot_id, trace_id}  不含 result_payload

Python 按 GRAPH_REGISTRY[graph_version] 线性节点：
        POST {stage_url}   ReportStage  started → succeeded|failed
        POST {complete_url} Complete     outcome=succeeded|failed
        成功 Complete 只交 result_payload + 状态语义，禁止 result_snapshot_id
```

| 项 | 本单 |
|---|---|
| 入口 | `POST /internal/v1/chain/jobs/execute`；202；结果只走 Complete |
| 注册表 | code-as-graph：`echo.graph.v1` / `fail.graph.v1` / `key_link.graph.v1` / `panorama.graph.v1`；`register_graph` 可插拔 |
| 预留键 | `chain:diagnosis:key_link` → 五段 Bid stage，诚实降级空 payload（无假分数） |
| 预留键 | `chain:panorama:graph` → freeze+assemble  stub，**不写** ADS `graph_snapshot` |
| 成功路径 | `echo.graph.v1` 回显 object，`honesty.degraded=false` |
| 失败路径 | `fail.graph.v1` / `kitchen_force_fail` → Complete(`failed`) + `error_code` + `failed_stage_code` |
| 回调 URL | Execute `callback` 优先；兼容 `callbacks`；否则 `chain.job_callback_base_url` / `LUMEN_ALGO_CHAIN_JOB_CALLBACK_BASE_URL` |
| Worker 锁 | 同 `task_id` 进程内互斥 → 409 `JOB_ALREADY_RUNNING` |
| 闸门 | Execute 入口 `assert_demo_mysql_targets()`；非 `demo_` 库名 422 |
| 禁止 | `/gdf/tasks`、`lumen_analysis_task`、自签 snapshot、wait_view、七键算法、Nebula |

## 偏离

| 项 | 说明 |
|---|---|
| Execute 同步跑完再 202 | 契约写「立即 202、Worker 异步」。厨房 Graph 为 stub，请求内一次跑完再 202，**仍不**把业务结果放进 Execute 响应。KEY-LINK 后单可改 BackgroundTasks，回调契约不变。 |
| OpenAPI `stage_total: const 5` | 按实际 Graph 长度上报（echo=2，key_link=5）。key_link 五段文案与 Bid 对齐。 |
| `callback` / `callbacks` | OpenAPI 字段为 `callback`；Runtime 示例为 `callbacks`。两者都收。`limits.timeout_sec` 与 `job_timeout_sec` 同收。 |
| 预留键无算法肉 | `key_link` / `panorama` 返回诚实降级空 payload，不造高端化指数 / 关键数 / 全景快照。算法本体归后单。 |
| Worker 锁 | 进程内集合（单副本天花板）。Java 仍拥有 Job 互斥；多副本升级路径见代码 `ponytail:` 注释。 |

## 产物清单

- 代码：`lumen-algo-py` `45d12e5bd32566eb69b71a401077781afc3ed0f1`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC 语义；未写 ADS graph_snapshot；未用企业评估任务表

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：`161 passed, 1 warning in 2.43s`（Starlette TestClient deprecation，与本单无关；此前 148 绿）
- RUNTIME：成功 echo 回调、fail Complete(failed)、key_link 五段降级空、panorama 不写 snapshot、非 demo_ 422、缺 callback 400、未知 graph 400、同 task 409、不用 `/gdf/tasks`

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| KEY-LINK / BOTTLENECK 等 | 后单往 `GRAPH_REGISTRY` 换节点函数；本单 stub 必须被替换后才能出真分数 |
| PANORAMA 发布快照 | `DEMO-CHAIN-PY-JOB-PANORAMA-L01`；本单 Complete 成功也不写 ADS |
| 段 C Java | Create/互斥/Complete Schema 门禁/签发 `result_snapshot_id`/wait_view |
| 多副本 Worker 锁 | 进程内；靠 Java 互斥兜底 |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`45d12e5bd32566eb69b71a401077781afc3ed0f1`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径已挂入 API 进程
- 本地：pytest 161 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：Execute body 或 `current_trace_id()` 写入 Stage/Complete
- 未第二套中间件

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py；七键本体未做 |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只挂 `/internal/v1/chain/jobs/execute`；回调 Java；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `45d12e5bd32566eb69b71a401077781afc3ed0f1` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 闸门 demo_*；不写 graph_snapshot |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ 预留键 payload 带 honesty/gap；禁止假分数 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/conf/settings.yaml`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 185000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.11 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`185000 × (0.75×3 + 0.25×15) / 1e6 = 1.11`。

## 联调确认

**联调通过 / 联调确认**：pytest 成功/失败/降级路径绿；Execute 202 后 mock HTTP 可见 ReportStage + Complete；Complete 无自造 `result_snapshot_id`；非 `demo_` 库名拒绝；SEARCH/SYNC 路由仍在；未使用 `/gdf/tasks` 与 `lumen_analysis_task` 存 CHAIN Job。本 agent **不**把任务标 `done`（feature → `integration`）。
