# DEMO-CHAIN-PY-SYNC-L01 · 产业链 Python — 门户 KPI / 全景发布快照 / 对象目录同步读

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-SYNC-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §2 Overview/Panorama / §6 SYNC  
> 依赖：[`DEMO-CHAIN-PY-METRIC-L01.md`](./DEMO-CHAIN-PY-METRIC-L01.md) · [`DEMO-CHAIN-PY-SHARED-L01.md`](./DEMO-CHAIN-PY-SHARED-L01.md) · [`DEMO-CHAIN-PY-SEARCH-L01.md`](./DEMO-CHAIN-PY-SEARCH-L01.md)

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
| 说明 | 未用 YAGNI 跳过 D9 信封/诚实空、handoff、pytest、只读 demo_*。复用 SHARED `make_envelope` / `honesty_for` / `assert_demo_mysql_targets` / `connect_chain_readonly` 与 SEARCH `load_search_records`，未另开第二套 chain 包，未创建全景 task。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求必读全文禁止用压缩摘要代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

只读 `/internal/v1/chain/sync/**`：门户 KPI、已发布全景快照秒开、对象 Select 目录。不创建 `chain:panorama:graph` task，不调 Job execute，不写 Job Result / CMS / ADS `narrative`/`conclusion`。

**复用 SHARED（禁止第二套包）**

```python
from lumen_common.algorithms.chain import (
    assert_demo_mysql_targets,
    connect_chain_readonly,
    make_envelope,
    honesty_for,
    current_trace_id,
    sync_kpi,
    sync_snapshot,
    sync_objects,
    sync_news,
)
```

本单增量：`lumen_common/algorithms/chain/sync.py`；路由挂在已有 `lumen_algo_service.views.chain` 同一前缀。

### 写死的 /internal 路径

| 方法 | 路径 | 读面 |
|---|---|---|
| GET | `/internal/v1/chain/sync/kpi` | 门户 KPI + D9 信封 + series/topn/regionPoints/news |
| GET | `/internal/v1/chain/sync/snapshot` | ADS `graph_snapshot` 发布态 + `graph_diff`；对齐 `IndustryPanoramaDataset` |
| GET | `/internal/v1/chain/sync/objects` | 产业 L0 / 该产业下产业链 L1 Select（复用 SEARCH MySQL 目录） |
| GET | `/internal/v1/chain/sync/news` | DWD `industry_chain_news_event` 只读；无表则空列表 |

查询参数兼容 camelCase / snake_case：`objectId`/`object_id`、`chainId`/`chain_id`、`industryId`/`industry_id`、`asOf`/`as_of`。默认无参 = 第一个可用 L0 + 其下第一条 L1，**`created_task=false`**。

| 项 | 本单 |
|---|---|
| KPI | ADS `industry_chain_metric_fact`（及 series/topn/region_dist）；每个数字带 catalog `make_envelope` 8 件套 + honesty |
| Q056 / QC07 | `M_CHAIN_MARKET_SIZE`/`GROWTH`、`M_CHAIN_INVEST_COUNT`/`TOTAL` 强制 `value=null`，禁止假市场/投融资 |
| 快照 | 仅 `publish_status=published`；缺该列 → 诚实空（`snapshot=null`，`honesty.published=false`），不假成功 |
| 对象目录 | SEARCH `load_search_records`；形状对齐 `IndustryAnalysisSelectOption`（value/label/objectType/disabled） |
| 资讯 | 只读 `industry_chain_news_event`（无短名 `news_event` 表）；形状对齐 `IndustryNewsEvent` |
| Job Result | **不写**；七键结果不写入 `graph_snapshot` |
| CMS | 介绍/历程 **不写** ADS narrative/conclusion |
| 闸门 | 非 `demo_` 库名 422；只读；不 CREATE 表 |

## 偏离

| 项 | 说明 |
|---|---|
| 资讯表名 | 派单写 DWD `news_event`；现网表为 `industry_chain_news_event`。短名不存在则空列表，不建表。 |
| 快照 payload | 段 A 发布包节点只有 `id/name/description` 与边 `source/target/type`；映射到 Demo `PanoramaNode/Edge` 时 `stage/status/inputs/...` 诚实空串/空数组，不灌 Demo mock 图谱。 |
| `evolutionStates` | `graph_diff=0`；无半年度历史则只返回当前发布态一条，不伪造 8 个半年快照。 |
| region lat/lng | ADS `region_dist` 无经纬度，返回 `null`，不编造坐标。 |
| `object_type` | ADS fact 为 `industry`/`chain`；Select 对外仍用 Demo `industry`/`industry_chain`。 |

## 产物清单

- 代码：`lumen-algo-py` `03c6c58fa407862777aadb7879a7f84e8224d2f2`（`origin/dev`）
- 本 handoff
- 未改 METRIC 引擎 / SEARCH 行为 / Nebula / Job Runtime / Java / 前端；未写正式库；未 CREATE 表

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_sync.py tests/test_chain_search.py tests/test_chain_shared.py --tb=short
```

输出摘要：

- 全量：`148 passed, 1 warning`（Starlette TestClient deprecation，与本单无关；SEARCH 140 基线 + SYNC 8）
- SYNC：Demo 链 KPI + 信封；Q056/QC07 即使 ADS 有数也置空；snapshot 缺 `publish_status` 不假成功；非 `demo_` 库名 422；`created_task` 恒 false

只读联调（Demo MySQL `192.168.88.43`，未写库）：

| 请求 | 结果 |
|---|---|
| `GET /sync/kpi?objectId=INB1303` | 产业「集成电路」；`enterprises=72`；kpis=10；series=5；topn=25；regionPoints=9；news=20 |
| Q056 `M_CHAIN_MARKET_SIZE` | `value=null`，`pending_ref=Q056` |
| QC07 `M_CHAIN_INVEST_COUNT` | `value=null`，`pending_ref=QC07` |
| `GET /sync/objects?industryId=INB1303` | L0=2；L1=4（设计/晶圆制造/封装测试/设备与材料）；`defaultChainId=INB130301` |
| `GET /sync/snapshot`（无参秒开） | `chainId=INB130301`；`snapshot_id=snap:INB130301:mock_20260814_append`；nodes=12；edges=11；`created_task=false` |
| `GET /sync/snapshot?chainId=NO_SUCH_CHAIN` | `snapshot=null`；`honesty.published=false`；不建 task |
| `GET /sync/news?objectId=INB1303` | 20 条（上限）；无 CMS 历程 |

只读核对（查询前后）：

| 项 | 结果 |
|---|---|
| demo ADS `industry_chain_metric_fact` | **600 未变** |
| demo ADS `industry_chain_graph_snapshot` | **10 未变** |
| 正式 `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** |
| 正式 `gkxlumenx_dwd.chain` | **8 未变** |
| 本单 DDL / 写入 | 无 |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| 段 C Java 门面 | `/topic/v1/industry/**` 同步只读后做；本段可 curl Python |
| PANORAMA Job | 改条件才建 task；本单只读已发布快照 |
| GRAPH 投影 | snapshot 节点属性仍薄；Nebula 投影另单 |
| CMS 介绍/历程 | 仍不走 ADS；前端继续读 CMS |
| K8s | 未改 `k8s/api.yaml` 企业评估正式库 env；CHAIN 默认走 yaml `chain.*` |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`03c6c58fa407862777aadb7879a7f84e8224d2f2`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；sync 已挂入 API 进程同一 router
- 本地：pytest 148 绿；Demo 库只读可查

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：复用 `current_trace_id()` 写入 sync 响应
- 未新增第二套 Trace 中间件；未挂 Graph Runner execute

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只挂 `/internal/v1/chain/sync/**`；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影、不写 snapshot |
| 4 | 可观测 | ✅ 复用 OTel `current_trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `03c6c58` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science；未整包搬 chainan |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；DDL 闸门仍拒 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ KPI 走 `make_envelope`；Q056/QC07 诚实空；缺发布态不假成功 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/sync.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/tests/test_chain_sync.py`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 130000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.78 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：pytest 148 绿；默认同步读秒开已发布快照且 `created_task=false`；KPI 走 ADS fact + D9 信封；Q056/QC07 空；非 demo_ 拒绝；正式库行数未变。本 agent **不**把任务标 `done`（feature → `integration`）。
