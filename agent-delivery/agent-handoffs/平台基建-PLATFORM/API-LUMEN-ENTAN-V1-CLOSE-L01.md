# API-LUMEN-ENTAN-V1-CLOSE-L01 · lumen 关掉 /v1

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12 余项。不删 vendor `/v1` 源码；demo 网关 `/entan/**` 不动。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 运行时开关 + OpenAPI 过滤；不 fork 删除路由。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 路由门控，不依赖检索。 |

## 问题清单

- lumen git 网关 `gkxlumen-gateway-dev.yml` 与 Nacos 种子 ConfigMap **无** `Path=/entan`。现网 `gkx-gateway-routes` 也无 `/entan`（demo 路由在 `gkx-gateway-dev.yml`）。
- lumen `entan-py` Service 已是 ClusterIP；`values.yaml` 默认曾写 NodePort 30800（与 demo 冲突），已改为 ClusterIP。
- Java 无 Feign 到 `gkxlumen-platform-entan-py`。科技新闻走 `/internal/tech-news/*`。

## 修改内容

| 项 | 做法 |
|----|------|
| `ENTAN_EXPOSE_PUBLIC_API` | 缺省 `1`（demo）；lumen helm `0` |
| `INNOV_EXPOSE_PUBLIC_API` | 缺省 `1`；lumen helm `0`（关 `/v1/chain/**`） |
| 行为 | `/v1` → 404；OpenAPI 去掉 `/v1*`；`/healthz` `/internal/*` 保留 |
| helm 注释 | 删除「网关 `/entan/**` 直达」 |
| 基线 | `architecture-baseline.md` v2.2.4 as-built |

## 测试结果

- `vendor/entan-py/tests/test_public_api_gate.py` **ok**（OpenAPI 无 `/v1/enterprises`，HTTP 404，healthz 200）
- `vendor/innov-py/tests/test_public_api_gate.py` **ok**（OpenAPI 无 `/v1/chain/list`）

## 遗留风险

- vendor 源码仍注册 `/v1` 路由，只是运行时挡掉。demo 对照同步仍可用。
- 需新镜像 + helm 后现网才生效。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev` `9a1889a`；`lumen-svc-platform` `dev` `e62230d`；编排 `e14b5c2`
- 本机自检：`test_public_api_gate.py`（entan + innov）ok
- rollout：push 后等 image:innov / image:entan-api + helm

## 可观测性（建议）

- 未改 OTel

## 涉及文件

- `lumen-algo-py/vendor/entan-py/api/main.py` · `vendor/innov-py/api/main.py`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml` · `values-lumen.yaml` · `templates/entan-py.yaml`
- `agent-delivery/architecture-baseline.md`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| `python_algo.exposes_only: [/internal/*]` | ✅ lumen 运行时；vendor 源码 as-built 注明 |
| demo `/entan` 保留 | ✅ 未改 demo 网关 / demo-ui-system-test |
| D12 不回落 demo | ✅ |
| D8/D9/D10 | N/A 无 UI |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 50000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.5 |
| cost_warn | green |
