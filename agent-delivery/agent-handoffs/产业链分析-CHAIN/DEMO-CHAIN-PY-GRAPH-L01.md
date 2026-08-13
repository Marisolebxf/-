# DEMO-CHAIN-PY-GRAPH-L01 · 产业链 Python — DWD 关系投影 Nebula demo_gkx_chain

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-GRAPH-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 图谱仅 Nebula / §6 GRAPH  
> 依赖：[`DEMO-CHAIN-PY-SHARED-L01.md`](./DEMO-CHAIN-PY-SHARED-L01.md)  
> Schema 指针：`storage/CHAIN/stores/nebula/graph-chain.md`（draft）· `DATA-CHAIN-db-design.md` §7 · DWD v5 `node_rel` / `entity_rel`

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
| 说明 | 未用 YAGNI 跳过失败诚实、Nebula 铁律、Demo space 闸门、handoff、pytest。未自创 Tag/Edge；未改 KEY-LINK 菜谱 / RUNTIME / SEARCH / SYNC；未写 Java。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 storage nebula 稿 / DWD v5 禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

Python 从 Demo DWD `industry_chain` / `industry_chain_node` / `node_rel` / `entity_rel`（及 `event_entity_rel` 计数）投影写入 **Nebula Demo space `demo_gkx_chain`**。

**复用 SHARED（禁止第二套 chain 包）**

```python
from lumen_common.algorithms.chain import (
    assert_demo_mysql_targets,
    assert_demo_nebula_space,
    connect_chain_readonly,
    map_graph,
    project_graph,
)
```

本单增量：`lumen_common/algorithms/chain/graph_project.py`；路由挂在已有 `lumen_algo_service.views.chain` 的 `POST /internal/v1/chain/graph/project`。CLI：`python -m lumen_common.algorithms.chain.graph_project [--self-check|--dry-run]`。

| 项 | 本单 |
|---|---|
| Space | 只写 `demo_gkx_chain`；`gkx_chain` / 非 `demo_*` → 422，禁止无闸门写正式 space |
| Tag | 仅 §7：`chain` / `segment` / `enterprise` / `institution` |
| Edge | 仅 §7：`belongs_to` / `participates` / `supplies` / `depends_on` |
| 客户端 | 仓内原先无 Nebula 驱动；按 `demo-algo-ent-analysis` 连接池模式新写第一套，lazy import `nebula3-python` |
| 失败诚实 | 无客户端 / 连不上 / 鉴权失败 / MySQL 不可达 → `status=failed` 且 `wrote=false`；`enabled=false` → `skipped`；**禁止假成功** |
| 默写图 | search / sync / jobs **不**调用投影 |
| Neo4j | 未引入 |

## 映射表 + 是否升级李伟

**升级 `human:李伟`：是**（graph-chain.md 仍为 draft；下列 OPEN 需结构终裁。能投影的边已投，不能映射的已跳过并计数，**未自创 schema**，故 registry 进 `integration` 而非 `blocked`）。

| DWD | 条件 | Nebula（§7 已列名） | Demo 实投 |
|---|---|---|---|
| `industry_chain` | 全行 | Tag `chain`，vid `chain:{chain_id}` | 10 |
| `industry_chain_node` | 全行 | Tag `segment`，vid `segment:{node_id}` | 96 |
| `industry_chain_node.chain_id` | 环节归属链 | Edge `belongs_to`：segment → chain | 96 |
| `industry_chain_node_rel` | `upstream` / `downstream` / `depends*` / `上下游` / `依赖` | Edge `depends_on`（v1：环节→环节上下游依赖） | 88（现网全是 `upstream`） |
| `industry_chain_node_rel` | `供需` / `替代` / `协同` | **无对应 Edge** | 0；跳过 |
| `industry_chain_entity_rel` | `enterprise` + `belongs_to` / `participates*` / `所属` / `参与` | Tag `enterprise` + Edge `participates` | 点 105 / 边 128 |
| `industry_chain_entity_rel` | `institution` / `service_institution` + 同上 | Tag `institution` + `participates` | 0 |
| `industry_chain_entity_rel` | `product` + `produced_at` | **无 product Tag** | 跳过 208 |
| `industry_chain_event_entity_rel` | 任意（`publisher` / `financing_subject` 等） | **无 event Tag** | 跳过 52 |
| — | 企业→企业供应链 | Edge `supplies` | Demo 无该结构，0，不造边 |

**OPEN（请李伟裁）**

1. DWD `entity_rel.belongs_to`（企业→节点）与 Nebula `belongs_to`（环节→链）撞名；本单把企业归属投到已有 Edge `participates`，未新建边类型。  
2. `product` / `produced_at` 是否补 Tag/Edge，或明确永不入图。  
3. `event_entity_rel` 是否补 event Tag，或事件关系只留 MySQL。  
4. `node_rel` 供需/替代/协同是否扩展 Edge，或确认跳过。  
5. `supplies` 的企业→企业真源表尚未出现在 Demo DWD。  
6. `graph-chain.md` `status=draft` 与 v5 命名终裁。

## 偏离

| 项 | 说明 |
|---|---|
| 仓内无现成 Nebula 客户端 | lumen-algo-py 原先无 nebula3；按 ent-analysis 模式写 CHAIN 第一套驱动，未复制 ENT Tag（`industry`/`talent` 等） |
| `requirements.txt` | 新增 `nebula3-python>=3.4,<3.9`（graph-engine.md 指定；无客户端则投影 `failed` 不假绿） |
| 企业 `belongs_to` → `participates` | 用已有 Edge 名，不是新 schema；待李伟确认是否改投 |
| `event_entity_rel` | 「必要时」已读表，因无 Tag 整表跳过 |
| K8s env | 未改 `k8s/api.yaml`；CHAIN Nebula 默认走 `conf/settings.yaml#chain.nebula` |

## 产物清单

- 代码：`lumen-algo-py` `e6ff8756411cc0644b40529f72b2b4b223f686e6`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / `job_runtime.py` 菜谱 / SEARCH / SYNC / KEY-LINK；未写正式 MySQL；未建 DWD/ADS 表

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_graph.py --tb=short
```

输出摘要：

- 全量：`179 passed, 1 warning`（Starlette TestClient deprecation，与本单无关）
- GRAPH：映射单元测 + 无客户端 `failed` + `enabled=false` → `skipped` + 正式 space 422 + search/sync/jobs 不偷写图

现网实投（`192.168.88.43:9669`，space `demo_gkx_chain`）：

| 项 | 结果 |
|---|---|
| Nebula 连通 | 是 |
| `SHOW TAGS` / `SHOW EDGES` | 4 / 4（仅 §7 名称） |
| `FETCH` `chain:INB1303` | 1 行 |
| vertices_written | **211**（chain 10 + segment 96 + enterprise 105） |
| edges_written | **312**（belongs_to 96 + participates 128 + depends_on 88） |
| skipped | **260**（product 208 + event_entity_rel 52） |
| DWD 行数 | node 96 / node_rel 88 / entity_rel 336 / event_entity_rel 52（与段 A 一致） |
| 正式 space `gkx_chain` | 未写（闸门拒绝） |
| `source` | `nebula` |
| `neo4j` | false |

CLI：

```text
python -m lumen_common.algorithms.chain.graph_project --dry-run
python -m lumen_common.algorithms.chain.graph_project
```

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| 李伟结构终裁 | 见映射表 OPEN；不挡 Demo 联调已投影边 |
| CREATE SPACE 心跳 | 首次建 space 有短等待；重跑幂等 INSERT 覆盖 |
| K8s | 镜像需带 `nebula3-python`；CHAIN space 不要误注入 `GKX_NEBULA_SPACE=gkx_chain` |
| Job | 本单不跑 BOTTLENECK/CYCLE/PANORAMA |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`e6ff8756411cc0644b40529f72b2b4b223f686e6`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；投影入口已挂 API 进程，默认不在 search/sync 写图
- 本地：pytest 179 绿；Demo Nebula 实投 `wrote=true`

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `X-Trace-Id`：现有 `TraceHeaderMiddleware`；投影响应带 `trace_id`
- 投影结果含 `source=nebula|none`，失败不报 `ok`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只挂 `POST /internal/v1/chain/graph/project`；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ space=`demo_gkx_chain`；禁止 Neo4j；Java 不直连 nGQL |
| 4 | 可观测 | ✅ 复用 OTel Trace；响应 `trace_id` / `source` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` |
| 6 | demo 不 merge lumen | ✅ 未把 demo-algo-science 包搬进 lumen；仅对照 fail-soft 语义 |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL 出 Java |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo DWD；未 DDL |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 | N/A 本单不写指标数；未伪造市场规模 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/graph_project.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/conf/settings.yaml`
- `repos/lumen-algo-py/requirements.txt`
- `repos/lumen-algo-py/tests/test_chain_graph.py`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.66 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：pytest 179 绿；无 Nebula 时失败路径不假绿；现网已写入 `demo_gkx_chain`（点 211 / 边 312 / 跳过 260）；正式 space 拒绝；search/sync/jobs 不偷写图；未自创 Tag/Edge，OPEN 升级 `human:李伟`。本 agent **不**把任务标 `done`（feature → `integration`）。
