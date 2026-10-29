# DEMO-CHAIN-PY-SEARCH-L01 · 产业链 Python — 产业查询 MySQL 目录（不走 ES）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-SEARCH-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 裁决第 3 条 / §2 SearchPage / §6 SEARCH  
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
| 说明 | 未用 YAGNI 跳过 `/internal/v1/chain/search`、D9 空态诚实、handoff、pytest。复用 SHARED `assert_demo_mysql_targets` / `connect_chain_readonly` / `current_trace_id`，未另开第二套 chain 包，未引入 ES。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求必读全文禁止用压缩摘要代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

实现 `GET` + `POST /internal/v1/chain/search`：只读 Demo DWD `industry_chain`，LEFT JOIN 同表取 L0 父级名，再读 `industry_chain_node.node_name` 填 tags/keywords。三种 mode 语义对齐 `filterIndustrySearchRecords`（`smart` / `industry` / `advanced`）。响应记录可喂 `IndustrySearchRecord`。

**复用 SHARED（禁止第二套包）**

```python
from lumen_common.algorithms.chain import (
    assert_demo_mysql_targets,
    connect_chain_readonly,
    current_trace_id,
    search_chain,
)
```

本单增量：`lumen_common/algorithms/chain/search.py`；路由挂在已有 `lumen_algo_service.views.chain` 同一前缀。

| 项 | 本单 |
|---|---|
| 引擎 | MySQL 目录，无 Elasticsearch |
| `objectType` | `chain_tier=L0` → `industry`；其余 → `industry_chain` |
| `id` / `stableId` | INB `chain_id` / `{objectType}:{chain_id}`（Q053） |
| `name` | DWD `chain_name`；无名行跳过，禁止编造 |
| `aliases` | `chain_short_name`（现网全空 → `[]`） |
| `parentIndustryId/Name` | L1+ JOIN L0；L0 省略 |
| `domain` / `summary` | `chain_category` / `description`（现网空串，诚实空） |
| `tags` / `keywords` | L1=节点名；L0=子链名 + 子孙节点名 |
| `availability` | `status=active` → `available`，否则 `unavailable` |
| 高筛支撑 | `objectType` / `domain` / `classification` / `focusDirection` / `tags` / `updatedAt` / `industryLevel` / `industryAttribute`（`future_industry_flag`） / `chainParentIndustryId` / `keyChainDirection` / `chainTags` |
| 高筛忽略 | `layoutStatus` / `coveredStage` / `industryParentId`（DWD 无列；仅这些条件时返回空 + `ignored_filters`，不假全命中） |
| Job / snapshot / Bid 叶子 | 未做 |

## 偏离

| 项 | 说明 |
|---|---|
| 夹具产业名 | 未搬 `industrySearchData.ts` 的「新一代信息技术产业」等 mock 名；现网名录是供应方 INB：`集成电路` / `智能机器人` 及 L1 子链 |
| `domain` | DWD `chain_category` 全 NULL，返回 `""`，不伪造「战略性新兴产业」 |
| `summary` | DWD `description` 全 NULL（介绍真源是 CMS），返回 `""` |
| `aliases` | `chain_short_name` 全 NULL → `[]` |
| `availability` | DWD 无权限撤回字段，不会出现 `permission_revoked` |
| `layoutStatus` / `coveredStage` / `industryParentId` | 忽略；单独使用时 `records=[]` 且 `ignored_filters` 可区分 |
| `industryLevel` | L0 映射为「一级产业」（对齐夹具选项，不是编造产业名） |
| `industryAttribute` | 用 `future_industry_flag` 映射未来产业/重点产业，不用空 `domain` 硬猜 |

## 产物清单

- 代码：`lumen-algo-py` `b8a398867ec2fff48452569e76bee50d05cd6d9a`（`origin/dev`）
- 本 handoff
- 未改 METRIC 引擎 / Nebula / Job Runtime / SYNC / Java / 前端；未引入 ES；未搬 `demo-svc-topic-py`

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_search.py tests/test_chain_shared.py --tb=short
```

输出摘要：

- 全量：`140 passed, 1 warning`（Starlette TestClient deprecation，与本单无关）
- SEARCH：关键词命中 / 高筛 / 空命中 / 非 `demo_` 库名 422；源码无 elasticsearch

示例请求（Demo `10.50.11.76` `demo_gkxlumenx_dwd.industry_chain` 10 行）：

| 请求 | 命中 |
|---|---:|
| `POST {"mode":"smart","keyword":"集成电路"}` | **5**（L0 集成电路 + 4 条 L1；子链靠 `parentIndustryName` 命中，对齐 TS） |
| `POST {"mode":"industry","keyword":"智能机器人"}` | **5** |
| `POST {"mode":"advanced","conditions":[{"field":"objectType","operator":"eq","value":"industry"}]}` | **2**（两个 L0） |
| `POST {"mode":"smart","keyword":"不存在的产业词xyz"}` | **0**（诚实空） |
| `GET ?mode=smart&keyword=EDA工具` | **2**（集成电路 + 集成电路设计） |

L1 记录示例字段：`id=INB130301`，`stableId=industry_chain:INB130301`，`name=集成电路设计`，`parentIndustryId=INB1303`，`parentIndustryName=集成电路`，`domain=""`，`summary=""`，`aliases=[]`，`tags/keywords`=节点名（EDA工具、IP核…），`source=llm_ods_demo`，`updatedAt=2026-08-14`，`availability=available`。

只读核对（查询前后）：

| 项 | 结果 |
|---|---|
| demo DWD `industry_chain` | 10 |
| 正式 `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** |
| 正式 `gkxlumenx_dwd.chain` | **8 未变** |
| 本单 DDL / 写入 | 无 |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| Java 门面 | 段 C `/topic/v1/industry/search` 后做；本段可 curl Python |
| `chain_category` / 别名 / CMS 摘要 | 入站后 domain/aliases/summary 才有值 |
| 权限锁态 | DWD 无 `permission_revoked`，US-CHAIN-TOPIC-01-08 需后续权限源 |
| GRAPH / SYNC / RUNTIME / 七键 | 按总派单另单；本会话停 |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`b8a398867ec2fff48452569e76bee50d05cd6d9a`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；search 已挂入 API 进程同一 router
- 本地：pytest 140 绿；Demo 库只读可查

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：复用 `current_trace_id()` 写入 search 响应
- 未新增第二套 Trace 中间件；未挂 `/jobs`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只挂 `/internal/v1/chain/search`；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影 |
| 4 | 可观测 | ✅ 复用 OTel `current_trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `b8a3988` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science；未搬 ES/topic-py |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；DDL 闸门仍拒 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ 缺字段诚实空；不编造产业名；非 demo 库名拒绝 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/search.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/tests/test_chain_search.py`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 105000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.63 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：pytest 140 绿；三种 mode 从 Demo 目录打出记录或诚实空；响应字段对齐 `IndustrySearchRecord`；无 ES 依赖；正式库行数未变。本 agent **不**把任务标 `done`（feature → `integration`）。
