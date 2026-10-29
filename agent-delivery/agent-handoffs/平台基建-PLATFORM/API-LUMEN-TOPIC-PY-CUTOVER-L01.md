# API-LUMEN-TOPIC-PY-CUTOVER-L01 · Java 企业检索/AI 切到 lumen-topic-py

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12-DEBT-TOPIC-PY 第 3 叶。前置：Python 仓 pipeline 5026 含 deploy 全绿。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改 helm URL / Nacos 样例 / Feign 默认服务名；不新造客户端。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 切流改配置，不依赖 Headroom。 |

## 问题清单

- 现网 Nacos 若已被人改过，helm 发布后以 git 中 DataId 为准；若 init 未覆盖，需确认 `gkxlumen-topic-enterprise-biz-dev.yml` / `gkxlumen-topic-async-service-biz-dev.yml`。
- Pod env `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL` / `GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL` 可压过旧 Nacos 空串回落。
- 网关主路径 200：**已验证** `POST /enterprise/topic/v1/search/meta/filters` → 200 / `code=0`。

## 修改内容

| 配置 | 旧（demo 回落） | 新（lumen-topic-py） |
|------|-----------------|----------------------|
| `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL` | `http://demo-platform-search-py:8080` | `http://gkxlumen-platform-search-py:8080` |
| `python-base-url`（enterprise Nacos） | 同上 | 同上 |
| `python-ai-base-url`（async Nacos） | `""` → 发现 `gkx-ai-service` | `http://gkxlumen-platform-ai-py:8081` |
| `GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL` | （无） | `http://gkxlumen-platform-ai-py:8081` |
| Feign `name` / 默认 service-name | `gkx-ai-service` | `gkxlumen-ai-service`（直连 URL 优先） |

删除 demo-platform-search-py / demo-platform-ai-py 作为正式回落。`demo-svc-topic-py` 仓未改。

## 测试结果

- 前置 Python：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026 全绿（含 3 个 deploy）
- 本仓 commit：`1ceb8e3` 已 push `origin/dev`
- 本仓 pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5027
- 网关回归：`POST http://10.50.69.111:30899/enterprise/topic/v1/search/meta/filters` → **HTTP 200** `code=0`（含 listing_statuses / operating_statuses 等字典，2026-08-14）

## 遗留风险

- D12-DEBT-INNOV-PY / D12-DEBT-ENTAN-PY 仍在（innov-py / entan-py 仍是 demo 制品）。
- DWD 仍 `demo_gkxlumenx_dwd`。
- 关闭 D12-DEBT-TOPIC-PY 条件：**已满足**（helm 绿 + 企业检索 filters 200）。

## CI/CD（必填）

- 分支：`dev`
- commit：`1ceb8e3`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5027
- 部署 namespace：`dev`
- K8s rollout：**success** `helm:deploy` [#21542](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21542) · `deploy:topic-enterprise` [#21544](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21544) · `deploy:topic-async-service` [#21545](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21545)
- dev 测试 URL：`POST http://10.50.69.111:30899/enterprise/topic/v1/search/meta/filters` → **200** `code=0`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-enterprise-biz` / `gkxlumen-topic-async-service-biz`（未改）
- 下游 Python：`gkxlumen-search-service` / `gkxlumen-ai-service`

## 涉及文件

- `helm/gkxlumen-platform/values.yaml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-enterprise-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-async-service-biz-dev.yml`
- `gkxlumen-topic-async-service/.../TopicAsyncPythonProperties.java`
- `gkxlumen-topic-async-service/.../RemoteTopicAsyncAiPythonClient.java`
- `gkxlumen-topic-async-service/.../TopicAsyncAiPythonRoutingClient.java`
- `ENT-JAVA-ANALYSIS-CORE-Nacos配置.md`
- `ENT-JAVA-ANALYSIS-ARTIFACT-Nacos配置.md`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ Java 只改 URL |
| 2 调用链 | ✅ Java → lumen-topic-py `/internal` |
| 3 Nebula | ✅ 未改图谱 |
| 4 可观测 | ✅ 服务名未拆 |
| 5 CI/CD | ✅ `1ceb8e3` → 5027 |
| 6 禁止 merge demo | ✅ |
| 7 共享聚合 | ✅ |
| 8 数据 | ✅ 未切库 |
| 9–11 D8/D9/D10 | N/A |
| 12 D12 | ✅ 删除 demo-platform-search-py / gkx-ai-service 回落 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.30 |
| cost_warn | green |
