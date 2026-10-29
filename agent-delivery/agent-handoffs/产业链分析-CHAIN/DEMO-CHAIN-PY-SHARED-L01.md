# DEMO-CHAIN-PY-SHARED-L01 · 产业链 Python 地基（Demo 库闸门 / ADS·DWD 只读 / 指标信封）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-SHARED-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 / §6 SHARED

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
| 说明 | 未用 YAGNI 跳过 D9 指标信封、OTel `trace_id` 复用、架构铁律、handoff、pytest 闸门。未实现 search/jobs/METRIC 引擎。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求必读全文禁止用压缩摘要代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

只做 SHARED 共用地基，后续 13 张 B 单必须 import 本包，不得再拆第二套路径。

**包路径（写死）**

| 用途 | 路径 |
|---|---|
| 闸门 / 只读连接 / 信封 | `lumen_common.algorithms.chain`（`lumen_common/algorithms/chain/`） |
| 内部路由 | `lumen_algo_service.views.chain`（`/internal/v1/chain/health`） |

后续 METRIC/GRAPH/SEARCH/SYNC/RUNTIME import：

```python
from lumen_common.algorithms.chain import (
    assert_demo_mysql_targets,
    chain_target_names,
    connect_chain_readonly,
    make_envelope,
    honesty_for,
    attach_readiness_from_catalog,
    current_trace_id,
)
```

实现要点：

1. **Demo 库闸门**：`is_demo_mysql_name` / `assert_demo_mysql_targets` 对齐段 A（库名不以 `demo_` 开头直接 `NonDemoMysqlTargetError`）。默认目标 `demo_gkxlumenx_ods/dwd/ads`。
2. **只读**：`ChainReadDB.query`；`forbid_business_ddl` 拒绝 CREATE/DROP/ALTER/TRUNCATE TABLE\|DATABASE\|SCHEMA。未建 DWD/ADS 业务表。
3. **D9 信封**：8 件套 `metric_id / metric_name_zh / definition / formula / source_tables / source_systems / update_freq / version` + `honesty`（empty_ok / forbid_fabricate / wave0_behavior / pending_ref / pending_hint / gap_id）。`make_envelope` 拒绝自带就绪度；只允许 `attach_readiness_from_catalog(..., source=矩阵路径)` 只读挂载，禁止改绿。
4. **诚实空**：`M_CHAIN_MARKET_SIZE`→Q056；`M_CHAIN_INVEST_COUNT` / `M_CHAIN_INVEST_TOTAL`→QC07。
5. **trace_id**：复用已有 `TraceHeaderMiddleware`；新增 `current_trace_id()` 供 chain 路由读取，未第二套中间件。
6. **views**：仅 `GET /internal/v1/chain/health`。无 search / jobs。未使用 `/gdf/tasks` 当 CHAIN Job。

## 偏离

| 项 | 说明 |
|---|---|
| 配置键 | 未改全局 `db.dwd_db=gkxlumenx_dwd`（企业评估仍读正式库）。CHAIN 独立 `conf/settings.yaml#chain` + `LUMEN_ALGO_CHAIN_MYSQL_{ODS,DWD,ADS}_DB`。闸门仍拒绝非 `demo_` 名。 |
| ADS 表名 | Demo ADS 现网无 `metric_fact` 短名；段 A 指标事实表为 `industry_chain_metric_fact`。本单不建表、不改名。 |
| 未搬 chainan | 对照段 A 闸门语义后按本仓结构新写，未复制 `demo-algo-science/chainan`。 |

## 产物清单

- 代码：`lumen-algo-py` `db7ee9faad91dceeb838486c7ec9fb3b8b1fecee`（`origin/dev`）
- 本 handoff
- 未改 `demo-algo-science` / Java / 前端；未把 `DEMO-CHAIN-UI-SEED-ODS-L01` 标 done

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_shared.py --tb=short
```

输出摘要：

- 全量：`127 passed, 1 warning in 2.22s`（Starlette TestClient deprecation，与本单无关）
- SHARED 闸门：`11 passed`（`demo_` 通过；`gkxlumenx_dwd/ads/ods` 拒绝；缺 8 件套失败；health 200；无 search/jobs；trace 复用）

只读联调（Demo MySQL `10.50.11.76`，未写库）：

| 项 | 结果 |
|---|---|
| 闸门目标 | `demo_gkxlumenx_ods/dwd/ads` |
| demo ODS `dwd_org_industry_tags` | 128 |
| demo DWD `industry_chain` | 10 |
| 正式 `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** |
| 正式 `gkxlumenx_dwd.chain` | **8 未变** |
| 本单 DDL | 未 CREATE 业务表 |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| METRIC/GRAPH/SEARCH | 按总派单依赖 SHARED 后另单；本会话不停开 |
| Job | 禁止 `/gdf/tasks`；RUNTIME 另单 |
| 就绪度改绿 | 信封不写 D1–D4；METRIC 只读矩阵 |
| K8s | 未改 `k8s/api.yaml` 企业评估正式库 env；CHAIN 默认走 yaml `chain.*` |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`db7ee9faad91dceeb838486c7ec9fb3b8b1fecee`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；health 路径已挂入 API 进程
- 本地：pytest 127 绿；Demo 库只读可连

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `X-Trace-Id`：现有 `TraceHeaderMiddleware`（OTel span）
- chain：`current_trace_id()` 同模块导出，health 响应可带 `trace_id`（无活跃 span 时为 null）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只挂 `/internal/v1/chain/health`；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影 |
| 4 | 可观测 | ✅ 复用 OTel Trace 中间件 |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `db7ee9f` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science；未把 demo 包搬进 lumen |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；DDL 闸门 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ 信封模块；禁止自填改绿 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/demo_guard.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/metric_envelope.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/lumen_algo_service/main.py`
- `repos/lumen-algo-py/lumen_common/observability.py`
- `repos/lumen-algo-py/conf/settings.yaml`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 75000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.45 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：pytest 闸门绿；配置指向 `demo_*` 可连可跑；指向正式库名拒绝；只读核对正式库行数未变；未创建 DWD/ADS 业务表。本 agent **不**把任务标 `done`（feature → `integration`）。
