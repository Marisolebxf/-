# DEMO-CHAIN-PY-JOB-PANORAMA-L01 · 产业链 Python — 全景改条件 Job chain:panorama:graph

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-PANORAMA-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 第 5/7 条 / §6 PANORAMA  
> 决策：[`DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-PANORAMA-产业链全景图谱/DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813.md)  
> 依赖：[`DEMO-CHAIN-PY-JOB-RUNTIME-L01.md`](./DEMO-CHAIN-PY-JOB-RUNTIME-L01.md) · [`DEMO-CHAIN-PY-GRAPH-L01.md`](./DEMO-CHAIN-PY-GRAPH-L01.md) · [`DEMO-CHAIN-PY-SYNC-L01.md`](./DEMO-CHAIN-PY-SYNC-L01.md)

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
| 说明 | 未用 YAGNI 跳过发布语义、诚实空、失败不写、七键隔离、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 CYCLE/REGIONAL/SHENZHEN。未改 Java / SEARCH / SYNC 秒开 / KEY-LINK / BOTTLENECK / GRAPH project。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 DEC 全景条件任务 / SYNC handoff / Demo PanoramaPage 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

默认进页秒开走 **SYNC** 已发布快照（`created_task=false`）。本 Job 只服务「改了产业/链/数据截至后点开始分析」：`task_type=chain:panorama:graph` / `panorama.graph.v1`。

把 RUNTIME stub `GRAPH_STUB_PENDING_PANORAMA` **替换**为三节点菜谱（对齐 Demo `PANORAMA_TASK_STAGES`）。仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`；菜谱在 `lumen_common.algorithms.chain.panorama`。厨房 `job_runtime.py` 本身不 INSERT。

| 段 | stage_code | stage_label | 本单 |
|---|---|---|---|
| N1 | `freeze` | 确认产业与产业链范围 | 校验 `chain_id` + `as_of`；不写 ADS |
| N2 | `assemble` | 加载全景图谱快照 | 按条件读 Demo DWD 节点/边/主体；可选 Nebula 计数 fail-soft；**不**调用 `project_graph` |
| N3 | `publish` | 对齐数据截至时间 | **成功才** INSERT `industry_chain_graph_snapshot`（`publish_status=published`）+ 相邻 `graph_diff`；失败 Complete(failed) 不提交 |

**与 SYNC 秒开的分工**

| 路径 | 谁 | 行为 |
|---|---|---|
| 无脏条件进页 | SYNC `GET /internal/v1/chain/sync/snapshot` | 读最新 published；`created_task=false`；不 Execute |
| 改产业/链/截至后「开始分析」 | 本 Job Execute | 组装并**新发布** snapshot；Complete 只交 `result_payload`，不自签 `result_snapshot_id` |
| 查看分析结果 | 前端/Java wait_view | 本页无「查看报告」「查看分析记录」字段 |

**发布表写入规则**

- 闸门：`assert_demo_mysql_targets()`；非 `demo_` 库名拒绝。只写 `demo_gkxlumenx_ads`。
- 成功：`industry_chain_graph_snapshot.publish_status=published`；`effective_at` ≡ 输入 `as_of`；payload 为整图 JSON（节点属性+边+布局坐标），禁止只存 ID。
- 同日 `effective_at` 再发：旧 published 标 `deprecated`，新 `snapshot_id`。不同截至保留多版本供演进。
- `graph_diff`：相对该链上一 published 预计算 `node_add` / `node_exit` / `edge_change` / 可选 `entity_change`；`confirm_status=pending`；**禁止** `tech_replace`。
- **禁止**把七键 Result（`high_end_index` / `bottleneck_score` / `is_key_node` / `cycle_stage` 等）写入 snapshot payload。
- **禁止**报告阅读器字段（`查看报告` / `查看分析记录` / `report_url`）。
- 失败：不 commit；Complete(`failed`)。
- LLM：无密钥则跳过叙述；有密钥也不得改节点/边。可选 Nebula 读失败不挡发布。

**复用（禁止第二套注册表）**

```python
from lumen_common.algorithms.chain.job_runtime import GRAPH_REGISTRY, execute_chain_job
from lumen_common.algorithms.chain.panorama import node_freeze, node_assemble, node_publish
```

## 偏离

| 项 | 说明 |
|---|---|
| 过程壳 3 段 | Demo `PANORAMA_TASK_STAGES` 为 3 句中文；本单 Graph 三节点对齐，未扩成七键五段。 |
| Nebula | 组装真源是 DWD；Nebula 只做可选 segment 计数。不在本 Job 写图（投影仍只走 GRAPH `POST /graph/project`）。 |
| 实写后回滚 | pytest 与联调探针均向 demo ADS INSERT 再 DELETE 隔离行（`as_of=2099-12-31`），未改 seed `snap:INB130301:mock_20260814_append`。 |
| LLM | 默认无密钥跳过；摘要仍用链名+节点/边计数，不造报告。 |

## 产物清单

- 代码：`lumen-algo-py` `cac856068fdeca3cbd7c6bbe75828b365149c95c`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC 秒开语义 / KEY-LINK / BOTTLENECK / GRAPH `project_graph`；未写正式库；未 CREATE 表；未做 CYCLE/REGIONAL/SHENZHEN

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_panorama.py tests/test_chain_job_runtime.py tests/test_chain_sync.py tests/test_chain_graph.py --tb=short
```

输出摘要：

- 全量：`196 passed, 1 warning`（Starlette TestClient deprecation，与本单无关；此前约 187 绿）
- PANORAMA：stub 文案消失；成功路径发布 published snapshot；失败 freeze/assemble 不调用 publish；七键 payload 拒写；SYNC `created_task` 仍恒 false；厨房 `job_runtime.py` 无 INSERT；`project_graph(` 未出现在菜谱

Demo ADS 实写（隔离后回滚）：

| 项 | 结果 |
|---|---|
| Execute `chain:panorama:graph` `chain_id=INB130301` `as_of=2099-12-31` | Complete `succeeded`；`node_count=12`（对齐 DWD）；`created_task=false` |
| 新 snapshot | 曾写入 `snap:INB130301:p:20991231:…` / `publish_status=published` |
| 七键 | `honesty.seven_key_in_snapshot=false` |
| seed `snap:INB130301:mock_20260814_append` | **仍 published**（不同截至，未 deprecate） |
| 回滚后 `industry_chain_graph_snapshot` | **10 未变**；无 `chain-panorama:%` 残留 |
| 正式库 | 未写 |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| 段 C Java | Create/互斥/Complete Schema / 签发 `result_snapshot_id` / wait_view；Python 只交 result_payload |
| 布局 | 按上中下游分层的确定性坐标；基线继承上一 published `layout_baseline_id` |
| Q062 / 技术替代 | diff 不做 `tech_replace` |
| CYCLE/REGIONAL/SHENZHEN | 明确不做 |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`cac856068fdeca3cbd7c6bbe75828b365149c95c`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径已挂 `panorama.graph.v1`
- 本地：pytest 196 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：Execute body 或 `current_trace_id()` 写入 Stage/Complete
- 未第二套中间件

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只经已有 `POST /internal/v1/chain/jobs/execute`；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本 Job 不写 space；可选只读计数 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL 出 Java |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只 INSERT 已有 snapshot/diff；闸门 demo_* |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ 本页不造市场规模；诚实空布局/投入产出；七键不进 snapshot |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/panorama.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_panorama.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 175000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.05 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`175000 × (0.75×3 + 0.25×15) / 1e6 = 1.05`。

## 联调确认

**联调通过 / 联调确认**：pytest 196 绿；stub 文案消失；成功才发布 demo ADS snapshot（探针 12 节点后已回滚，seed 10 行未变）；失败不写发布态；七键 payload 不进 snapshot 表；SYNC 默认秒开仍 `created_task=false`。本 agent **不**把任务标 `done`（feature → `integration`）。
