# DEMO-CHAIN-PY-METRIC-L01 · 产业链 Python — DWD v5 → ADS v2 指标引擎（M_CHAIN_*）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-METRIC-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 / §6 METRIC  
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
| 说明 | 未用 YAGNI 跳过 D9 8 件套信封、诚实空、handoff、pytest、只写 demo_*。复用 SHARED `make_envelope` / `honesty_for` / `assert_demo_mysql_targets`，未另开第二套 chain 包。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求必读全文禁止用压缩摘要代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

从 demo DWD `industry_chain_*` 计算并 **replace** 写入 demo ADS v2 **指标相关 6 表**。写入前 `assert_demo_mysql_targets`。指标 ID 以 `cfg_metric-CHAIN-seed.yaml` 60 条 `M_CHAIN_*` 为准。

**复用 SHARED（禁止第二套包）**

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

本单增量仍在 `lumen_common.algorithms.chain`：`metric_catalog.py` / `metric_engine.py` / `ChainWriteDB`。

| 表 | 本单 |
|---|---|
| `industry_chain_metric_fact` | 60 × 10 链 = 600 行（能算写值，不能算 NULL） |
| `industry_chain_metric_series` | 资讯/新增企业分年 49 行 |
| `industry_chain_metric_dist` | 0（DWD `model_result_detail` 空，不造瓶颈分布） |
| `industry_chain_region_dist` | 15 行城市分布 |
| `industry_chain_region_scorecard` | 0（无模型四力，不造假分） |
| `industry_chain_topn` | 222 行（key_enterprise / hot_news） |
| `industry_chain_conclusion` / `narrative` | **不写** |
| `industry_chain_graph_snapshot` / `graph_diff` | **不写**（现网 snapshot=10 未变） |
| 旧 `ads.chain_*` 十一表 | **不维护** |

硬约束：

- `M_CHAIN_MARKET_SIZE` / `M_CHAIN_MARKET_GROWTH` 按 **Q056 空值**（段 A 曾写入 574340.561，本单已替换为 NULL）
- `M_CHAIN_INVEST_COUNT` / `M_CHAIN_INVEST_TOTAL` 按 **QC07**：DWD 投融资 `source_system=mock`（12 行），ADS **不写假数**
- 不建 DWD/ADS 业务表；replace 仅限 demo ADS 上述 6 表（DELETE+INSERT，非 TRUNCATE）
- 就绪度只从 `metric-readiness-matrix-CHAIN.yaml` `attach_readiness_from_catalog`，禁止改绿

## 偏离

| 项 | 说明 |
|---|---|
| NODE/EDGE | cfg_metric 写 Nebula pending；本单按 DWD `industry_chain_node` / `node_rel` 结构计数（GRAPH 单另做投影，不造图分数） |
| 投融资 | DWD 有 mock 合成行，按 QC07 **忽略**，不把 mock 金额灌 ADS |
| 市场规模 | 不跑 ENT 年报加总（与 ads_v2 `_try_market_size` 对照后按 Q056 否决） |
| scorecard / dist | 表有写入路径但本批 0 行（无模型明细）；不是漏接 |

## 产物清单

- 代码：`lumen-algo-py` `b136cb609894b2a738befd14f0edb46e89099099`（`origin/dev`）
- 本 handoff
- 未改 `demo-algo-science` / Java / 前端；未写 SEARCH/GRAPH/RUNTIME/SYNC

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
python -m pytest -q tests/test_chain_shared.py tests/test_chain_metric.py --tb=short
python -m lumen_common.algorithms.chain.metric_engine --self-check
```

输出摘要：

- 全量：`132 passed, 1 warning in 1.91s`（Starlette TestClient deprecation，与本单无关）
- SHARED 闸门 + METRIC：`16 passed`（正式库名拒绝；Q056/QC07 单测空值）
- `--self-check`：batch `chain-metric:20260814T031657`

写入行数：

| 表 | 行数 |
|---|---:|
| `industry_chain_metric_fact` | 600 |
| `industry_chain_metric_series` | 49 |
| `industry_chain_metric_dist` | 0 |
| `industry_chain_region_dist` | 15 |
| `industry_chain_region_scorecard` | 0 |
| `industry_chain_topn` | 222 |

诚实空（ADS `metric_value` 全 NULL，有事实行可被 SYNC 读取）：

| metric_id | 原因 | 行数 | filled |
|---|---|---:|---:|
| `M_CHAIN_MARKET_SIZE` | Q056 | 10 | 0 |
| `M_CHAIN_MARKET_GROWTH` | Q056 | 10 | 0 |
| `M_CHAIN_INVEST_COUNT` | QC07 / DWD mock | 10 | 0 |
| `M_CHAIN_INVEST_TOTAL` | QC07 / DWD mock | 10 | 0 |

能算示例：`M_CHAIN_ENTERPRISE_COUNT` 10 行全部非空。其余 pending_algorithm 指标（周期/瓶颈/四力等）因 `model_result_detail=0` 写 NULL 事实行，不造假分。

正式库抽查（写入前后）：

| 项 | 结果 |
|---|---|
| `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** |
| `gkxlumenx_dwd.chain` | **8 未变** |
| demo `industry_chain_graph_snapshot` | **10 未变** |
| 本单 DDL | 未 CREATE / 未 TRUNCATE |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| SEARCH / GRAPH / RUNTIME / SYNC | 按总派单另单；本会话停 |
| QC07 真源 | 供应方投融资 ODS 到位且 `source_system!=mock` 后可计算 |
| Q056 | 正式市场源/甲方口径闭合前保持空值 |
| K8s | 未改 `k8s/api.yaml` 企业评估正式库 env；CHAIN 默认走 yaml `chain.*` |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`b136cb609894b2a738befd14f0edb46e89099099`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；METRIC 为 CLI/模块，无新用户面路由
- 本地：pytest 132 绿；`--self-check` 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `ext_json.trace_id`：复用 `current_trace_id()`
- 未新增第二套 Trace 中间件；未挂 search/jobs 路由

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 未新增用户面路由；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；未写 graph_snapshot |
| 4 | 可观测 | ✅ 复用 OTel `current_trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `b136cb6` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science；未整包搬 chainan |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只写 demo_* 指标 6 表；DDL 闸门仍拒 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ catalog→`make_envelope`；Q056/QC07 诚实空；就绪度只读矩阵 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/metric_catalog.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/metric_engine.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/demo_guard.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/metric_envelope.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/tests/test_chain_metric.py`
- `repos/lumen-algo-py/tests/test_chain_shared.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 155000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.93 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

## 联调确认

**联调通过 / 联调确认**：pytest 132 绿；闸门测试仍绿（正式库名拒绝）；`--self-check` 写入 demo ADS v2 指标表；Q056/QC07 `metric_value` 全 NULL；正式 `gkxlumenx_ods.dwd_org_industry_tags=20000`、`gkxlumenx_dwd.chain=8` 未变。本 agent **不**把任务标 `done`（feature → `integration`）。
