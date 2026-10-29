# LUMEN-CHAIN-E-DEVOPS-L01 · 产业链段 E0 — K8s dev 发布门

> 格式参考 `templates/handoff-template.md`；内容按 2026-08-14 集群实测。本单**只检查、不改 helm/CI、不改业务代码**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已为 in_progress；lock 24h。tech_task 完工转 **ready_to_sign**，不标 done。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过可观测 / D12。逐项核对 deploy rollout、已发布 URL（非 localhost）、网关/Feign 是否回落 demo-*、联调库名前缀、OTel endpoint。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本单为集群核对，未挂载 compress。 |

## 结论（给 coordinator）

**PASS**

- 前端已发布 URL：http://10.50.69.111:30892 （`lumen-ui-topic` → deploy `gkx-lumen-topic`，title=深圳国际科技专题服务系统）
- 三个点名 deploy 均为 ready **1/1**，rollout status 成功
- D12：前端 nginx / Java Feign **未**指向 `demo-platform-*` / `demo-svc-*` / `demo-algo-*`；CHAIN 算法下游是 `lumen-platform-algo-py`，不是 `demo-algo-science` / `demo-platform-innov-py`
- 产业链 health 返回联调库 `demo_gkxlumenx_ods/dwd/ads`（只读）

## 点名服务核对

| 点名 | K8s deploy | ready | 镜像 | svc | 备注 |
|------|------------|-------|------|-----|------|
| lumen-ui-topic | `gkx-lumen-topic` | **1/1** | `harbor.htmisoft.net/gkx/gkx-lumen-topic:b0032e17` | NodePort **80:30892** | 与 registry `dev_url` 一致 |
| lumen-svc-platform chain 门面 | `gkxlumen-platform-topic-chain` | **1/1** | `harbor.htmisoft.net/gkx/gkxlumen-topic-chain:474e98a9` | ClusterIP :7095 | `SPRING_APPLICATION_NAME=gkxlumen-topic-chain-biz` |
| lumen-svc-platform async-service | `gkxlumen-platform-topic-async-service` | **1/1** | `harbor.htmisoft.net/gkx/gkxlumen-topic-async-service:474e98a9` | ClusterIP :7094 | algo URL → lumen-algo |
| lumen-algo-py | `lumen-platform-algo-py` | **1/1** | `harbor.htmisoft.net/gkx/gkx-lumen-algo-py-api:9a0342f3` | ClusterIP :8000 | **不是** demo-algo / demo-platform-innov-py |

同 ns 对照（CHAIN **不**走这些）：

- `demo-platform-innov-py` 1/1（demo 算法，禁止冒充 lumen）
- `gkxlumen-platform-innov-py` 1/1（lumen innov-py，CHAIN Feign 未指向它）
- `gkx-demo-ui` NodePort 30889（demo 前端，不是本单 URL）

`kubectl -n dev rollout status --timeout=90s`：

- deployment "gkx-lumen-topic" successfully rolled out
- deployment "gkxlumen-platform-topic-chain" successfully rolled out
- deployment "gkxlumen-platform-topic-async-service" successfully rolled out
- deployment "lumen-platform-algo-py" successfully rolled out

网关（联调入口，非点名但验证调用链）：`gkxlumen-platform-gateway` 1/1，NodePort **9999:30899**，镜像 `gkxlumen-gateway:474e98a9`。ns=dev 无 Ingress。

## 已发布前端 URL

| 项 | 值 |
|----|-----|
| URL | http://10.50.69.111:30892 |
| curl -I | HTTP/1.1 **200 OK** Server: nginx |
| HTML title | 深圳国际科技专题服务系统 |
| 证据性质 | K8s NodePort 已发布页，**不是** localhost / `pnpm dev` |

## D12 结论

**合规（CHAIN 调用链未回落 demo-*）。**

| 检查点 | 结果 |
|--------|------|
| 前端 nginx `proxy_pass` | `http://gkxlumen-platform-gateway:9999/`（`/api/`） |
| 前端静态资源 grep `demo-platform-*` / `demo-svc-*` / `demo-algo-*` | **0 命中** |
| chain Feign | `GKXLUMEN_TOPIC_CHAIN_ALGO_BASE_URL=http://lumen-platform-algo-py:8000` |
| async Feign | `GKXLUMEN_TOPIC_ASYNC_CHAIN_ALGO_BASE_URL=http://lumen-platform-algo-py:8000`；AI URL=`http://gkxlumen-platform-ai-py:8081`（lumen，非 demo AI） |
| Nacos | Java/网关 `NACOS_HOST=gkxlumen-platform-nacos`（非 demo-platform-nacos） |
| 同 ns 的 `DEMO_PLATFORM_*_SERVICE_HOST` | K8s 注入的 Service 发现变量，**不是**应用配置；未作为 Feign/nginx 目标 |

同 ns 并存 demo 栈（`demo-platform-*`）属预期隔离，未当作 lumen 冒烟证据。

## 联调库（不打印密码）

| 组件 | 应用配置 | 判定 |
|------|----------|------|
| topic-chain JDBC | `demo_gkxlumenx_ads` @ 10.50.11.76:3306 | 符合 `demo_gkxlumenx_*` |
| CHAIN health（经网关/前端反代） | `targets.ODS/DWD/ADS = demo_gkxlumenx_ods/dwd/ads`，`readonly=true` | **CHAIN 冒烟库闸门通过** |
| lumen-algo-py env | `LUMEN_ALGO_MYSQL_{DWD,ADS,CFG}_DB=gkxlumenx_*`（无 `demo_` 前缀） | 与 health 返回的 demo_ 目标不一致；health 以 Python 模块口径为准。遗留：env 字面量仍是正式库名 |
| topic-async-service JDBC | `gkxlumenx_topic_enterprise` | 企业模块库名，无 `demo_` 前缀；**CHAIN Feign 不走该库**。登记为残差，本单不改 helm |

CHAIN 冒烟路径实测：

```
curl http://10.50.69.111:30899/chain/topic/v1/industry/health  → HTTP 200, status=ok, module=chain, trace_id 有值
curl http://10.50.69.111:30892/api/chain/topic/v1/industry/health → HTTP 200, 同上
```

## 可观测性

| 组件 | OTEL_SERVICE_NAME | exporter | 判定 |
|------|-------------------|----------|------|
| topic-chain | `gkxlumen-topic-chain-biz` | `http://gkxlumen-platform-otel-collector:4318` + Java Agent | 有 |
| topic-async-service | `gkxlumen-topic-async-service-biz` | 同上 | 有 |
| lumen-algo-py | `lumen-platform-algo-py` | `http://gkx-otel-collector:4318` | ns=dev **无** Service `gkx-otel-collector`（仅有 `gkxlumen-platform-otel-collector` / `demo-platform-otel-collector`）。进程仍报 trace_id，但 OTLP 导出可能丢。本单不改 helm，记残差 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | 通过。未在 Java 侧做算法；CHAIN 下探 lumen-algo-py |
| 2 调用链 前端→Java REST→Python `/internal/*` | 通过。nginx→`gkxlumen-platform-gateway`→topic-chain→`lumen-platform-algo-py:8000` |
| 3 图谱 Nebula | N/A（本单不查图库连通） |
| 4 可观测 | 通过（Java Agent + Python OTEL_SERVICE_NAME）；algo collector DNS 见遗留 |
| 5 CI/CD | 通过。已在 ns=dev 发布；本单未改 pipeline |
| 6 demo2 merge | N/A |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS | 通过。CHAIN health 指向 demo_gkxlumenx_ads |
| 9 D8 Design | N/A（不改 UI） |
| 10 D9 血缘 | N/A |
| 11 D10 交互 | N/A |
| 12 D12 demo/lumen 隔离 | 通过。见 D12 结论 |

## 修改内容

- 无业务代码、无 helm/CI 变更。仅本 handoff。

## 测试结果

- `kubectl -n dev get deploy,svc` + `rollout status`：点名 deploy 1/1
- 前端 30892：200 + lumen 专题系统 title
- 网关 30899 与前端 `/api/chain/...` health：200 + demo_gkxlumenx_* + trace_id
- SSH 入口：MCP ssh-executor serverName=`10.50.69.111`（本机无 kubectl）

## 遗留风险

1. `lumen-platform-algo-py` 的 `OTEL_EXPORTER_OTLP_ENDPOINT` 指向不存在的 `gkx-otel-collector`。下一步（非本单）：helm/k8s 改为 `gkxlumen-platform-otel-collector:4318`。
2. algo-py / async-service 环境变量字面量仍是 `gkxlumenx_*`（无 `demo_`）。CHAIN health 已声明走 `demo_gkxlumenx_*`；若后续 Job/非 health 路径读 env 原值，需算法/Java 再核。不改 helm。
3. 同 ns 仍有完整 demo 栈；冒烟必须钉死 30892 / `gkxlumen-platform-gateway:30899` / `lumen-platform-algo-py`。

## CI/CD

- 分支：未改仓
- commit：无
- pipeline：未触发（只读核对）
- 部署 namespace：`dev`
- K8s rollout：成功（见上表）
- dev 测试 URL：http://10.50.69.111:30892 ；health：http://10.50.69.111:30899/chain/topic/v1/industry/health

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | grok-4.6 |
| actual_cost | 2.40 |
| cost_warn | green |

## 涉及文件

- `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-E-DEVOPS-L01.md`（本文件）
