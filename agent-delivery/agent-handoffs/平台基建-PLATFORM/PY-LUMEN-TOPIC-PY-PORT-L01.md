# PY-LUMEN-TOPIC-PY-PORT-L01 · 对照迁检索/AI/worker

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控：L01 ready_to_sign 即可同仓连续） |
| 说明 | D12-DEBT-TOPIC-PY 第 2 叶。契约路径 `/internal/gkx-search/**` `/internal/gkx-ai/**` 保持。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 同仓对照迁入，不另起模块、不并进 `lumen-algo-py`、不改 demo 仓。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对照迁代码，不依赖 Headroom。 |

## 问题清单

- `tests/test_query_tree_dsl.py::test_meta_query_tree_schema_matches_field_strategy` 本地失败（`name_en` extra）。**对照源 demo 即有**，非本叶 URL 改名引入；未扩修 schema。CI smoke 不含该用例。

## 修改内容

在 `lumen-topic-py` 落地：

- `gkx_search_service` / `gkx_ai_service` / `gkx_ai_worker` / `gkx_common`（对照 demo，禁止 merge）
- 仅 `/internal/*`；算法厨房默认 `http://lumen-platform-algo-py:8000`
- `conf/settings.yaml`：search 本地默认 `127.0.0.1:8080`（不再写死 demo NodePort **30805**）；服务名 `gkxlumen-search-service` / `gkxlumen-ai-service`
- `gkx_ai_service/deps.py`：self-base 注释与默认名切 lumen
- `tests/test_eval_callback_defaults.py`：断言 `gkxlumen-platform-ai-py`

未改 `demo-svc-topic-py`。未把代码并进 `lumen-algo-py`。

## 测试结果

本地 `python -m pytest`（`GKX_MOCK_ENABLED=0`）：

| 文件 | 结果 |
|------|------|
| `test_eval_callback_defaults.py` | pass |
| `test_key_analysis_geo_filter.py` | pass |
| `test_recommend_geo_sources.py` | pass |
| `test_lumen_algo_adaptation.py` | pass |
| `test_no_mock_runtime.py` | pass |
| `test_enum_guards.py` | pass |
| `test_query_tree_dsl.py` | 1 fail（见问题清单） |

合计：**83 passed, 1 failed**（失败项非本叶回归范围）。

## 遗留风险

- 集群冒烟等 CI image + manual deploy。
- Java 仍打 demo search，直到 CUTOVER。

## CI/CD（必填）

- 分支：`dev`
- commit：`5d20411`（与 DEVOPS 同根提交；新仓首包含代码+隔离）
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026 **全绿**（smoke + image + deploy）
- 部署：`gkxlumen-platform-search-py` / `ai-py` / `ai-worker` rollout success
- 本地冒烟：上表

## 可观测性（建议）

- OTEL_SERVICE_NAME：K8s 注入 `gkxlumen-*`；代码 logger 名仍 `gkx-ai-service.*`（与 demo 对照，未为改名而扩 diff）

## 涉及文件

- `repos/lumen-topic-py/gkx_search_service/`
- `repos/lumen-topic-py/gkx_ai_service/`
- `repos/lumen-topic-py/gkx_ai_worker/`
- `repos/lumen-topic-py/conf/settings.yaml`
- `repos/lumen-topic-py/tests/test_eval_callback_defaults.py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 厨房 `lumen-algo-py` |
| 2 调用链 `/internal` | ✅ |
| 3 Nebula | ✅ |
| 4 可观测 | ✅ |
| 5 CI | ✅ 同 5026 |
| 6 禁止 merge demo | ✅ |
| 7 Java 不写算法 | ✅ |
| 8 数据 | ✅ DWD 暂留，已注明 |
| 9–11 D8/D9/D10 | N/A |
| 12 D12 | ✅ 内部 URL 不再指向 30805 / demo-platform-ai-py |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 200000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.80 |
| cost_warn | green |
