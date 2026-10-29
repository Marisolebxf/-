# LUMEN-POLICY-E-DEVOPS-L01 · 政策专题 E0 点名发布

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-E-总派单.md`](./LUMEN-POLICY-E-总派单.md)  
> **本叶不标 done**：四服务已发布绿；tech_task 走 AV → `ready_to_sign`。E1 由 coordinator 收 E0 后再派。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；tech_task；E1 等本叶绿；禁止改 `lumen-ui-topic` 业务代码 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短发布边：helm 装出 + 去重 MYSQL_DB + `deploy:topic-policy` 改 auto-on-dev。未改工厂拓扑、未改正式 JDBC、未改业务代码 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 发布/探活，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 只补 §2.3 发布边（topic-policy:7097 / 网关 `/policy/**` / 政策 HTTP=`gkxlumen-platform-entan-py:8000`）。§1 工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 未改 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 结论：发布绿（四服务均绿）

| 点名 | K8s | ready | 镜像 | CI |
|------|-----|-------|------|-----|
| `lumen-ui-topic` | `gkx-lumen-topic` NodePort **30892** | **1/1** | `gkx-lumen-topic:97963375`（含 POL-04 及 C1 TS 修，`97963375678d7d246ff800824995889901aebbf3`） | [frontend:build 26179](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26179) 绿 · [frontend:image 26180](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26180) 绿。旧 26140 为 C1，已过 |
| `gkxlumen-topic-policy` | `gkxlumen-platform-topic-policy` :7097 | **1/1** | `gkxlumen-topic-policy:7d12b8dd` | [deploy:topic-policy 26171](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26171) success；[helm:deploy 26164](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26164) success |
| `gkxlumen-topic-async-service` | `gkxlumen-platform-topic-async-service` :7094 | **1/1** | `gkxlumen-topic-async-service:7d12b8dd` | [deploy:topic-async-service 26168](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26168) success |
| 政策 HTTP | `gkxlumen-platform-entan-py` :8000 | **1/1** | `gkxlumen-entan-py-api:ea3acc39` | [deploy:entan-api 25779](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/jobs/25779) success。**不是**厨房 `lumen-platform-algo-py` |

Nacos：`FORCE_NACOS_REPUBLISH=true` 已灌（[helm:chart 26080](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26080)）。现网 env `GKXLUMEN_TOPIC_ASYNC_POLICY_ALGO_BASE_URL=http://gkxlumen-platform-entan-py:8000`。helm release `gkxlumen-platform` **rev 33 deployed**。

**发布绿。** 本叶不标 done。E1 不开。`e2e:chain-gold` [26183](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26183) 红（CHAIN #4 wait_view）不是本叶政策 E0 点名，留给 E1/CHAIN。

## 范围与实现

- helm 装出 `gkxlumen-platform-topic-policy`（BOOT 遗留：`deploy:topic-policy` 曾 manual，因 Deployment 未装出会 not found）。
- `values.yaml` 去掉 `topic-policy.env` 重复 `MYSQL_DB`（`platformDb` 已注入；双键导致 helm patch-order 失败）。
- `.gitlab-ci.yml`：`deploy:topic-policy` 与 `topic-svc` 同 **origin/dev 自动** set-image。
- 政策 Job Nacos 新键：`FORCE_NACOS_REPUBLISH=true` 点 `helm:chart`。
- `deploy:entan-api` 把现网滚到含 `/internal/policy` 的 `ea3acc39`（entan-api 制品）。
- JDBC 保持 `demo_gkxlumenx_ads`。禁止改正式 `gkxlumenx_*`。
- 禁止 Feign/服务打 `demo-*`。禁止把 innov / 厨房 deploy 当本轮 E0。

## 偏离说明

- 首发 `helm:chart --reuse-values` 只叠了 `values-lumen.yaml` 的 `{enabled: true}`，新服务缺 `image.repository` / `jarPath` / `springAppName`，出现 `harbor.htmisoft.net/gkx/:57c9a1d9` InvalidImageName。随后 `helm:deploy` 因双 `MYSQL_DB` patch-order 红；去掉重复键后 [26164](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26164) 绿，release 从 failed → **deployed**。
- `lumen-algo-py` pipeline [5881](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5881) 整管线曾因 bridge `e2e:chain-gold` 红；点名 `deploy:entan-api` 本身 success。后续 [26183](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26183) 仍红（CHAIN #4 wait_view），**不修、不挡政策 E0**。

## 产物清单

- 代码：`lumen-svc-platform` `7d12b8dd` → `origin/dev`（CI auto-deploy + helm MYSQL_DB）
- 前端现网：`lumen-ui-topic` `97963375`（C1 修后；本叶未改 UI 业务代码）
- 流图：`storage/POLICY/01-data-flow.md` §2.3 发布边（不改工厂、不翻签）
- 本文 handoff

## 验收证据

探活（网关，非 localhost）：

```text
GET http://10.50.69.111:30899/policy/topic/v1/policy/health
HTTP 200
java.status=up  service=gkxlumen-topic-policy-biz
python.name=lumen-algo-py  pathPrefix=/internal/policy
python.baseUrl=http://gkxlumen-platform-entan-py:8000
degraded=false
```

entan-py：`GET /internal/policy/status` → `backend=mysql`，`policy_focus=47082`。  
JDBC：`demo_gkxlumenx_ads` @ 10.50.11.76:3306。无正式前缀数据面。  
Nacos DataId：`gkxlumen-topic-policy-biz-dev.yml`；async `policy.algo-base-url` → entan-py。  
前端：`http://10.50.69.111:30892` HTTP **200**，镜像 `gkx-lumen-topic:97963375`（≥ POL-04 `5c5caaf`）。

## 修改内容

| 路径 | 动作 |
|------|------|
| `lumen-svc-platform/.gitlab-ci.yml` | `deploy:topic-policy` auto-on-dev |
| `helm/.../values.yaml` | 去掉 topic-policy 重复 `MYSQL_DB` |
| `storage/POLICY/01-data-flow.md` | §2.3 发布边 |

## 测试结果

- `kubectl -n dev rollout status`：`gkx-lumen-topic` / topic-policy / topic-async-service / entan-py 均 1/1。
- 网关 health 200；python 打 entan-py，不打 `lumen-platform-algo-py` / `demo-platform-entan-py`。
- `deploy:topic-policy` 已可自动跑（26171 success）。
- 前端 30892 HTTP 200；`frontend:build` 26179 / `frontend:image` 26180 绿。

## CI/CD（必填）

- 分支：`lumen-svc-platform` / `lumen-algo-py` / `lumen-ui-topic` `origin/dev`（禁止 force）
- commit：Java `7d12b8dd`；Python `ea3acc39`；前端 `97963375678d7d246ff800824995889901aebbf3`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5925 · https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5881 · frontend jobs [26179](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26179) / [26180](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26180)
- namespace：`dev`
- 镜像：`gkx-lumen-topic:97963375` · `gkxlumen-topic-policy:7d12b8dd` · `gkxlumen-topic-async-service:7d12b8dd` · `gkxlumen-entan-py-api:ea3acc39`
- K8s rollout：四服务 **成功**（发布绿）
- helm：`gkxlumen-platform` rev **33 deployed**

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz` / `gkxlumen-topic-async-service-biz`
- Tempo / Loki：随平台 Collector；本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改 Java 算法 |
| 前端→Java→Python `/internal/*` | ✅ health python.pathPrefix=`/internal/policy` |
| 图谱 Nebula | ✅ 未写 nGQL；space 仍 `demo_gkx_chain` |
| 可观测 | ✅ OTEL_SERVICE_NAME + javaagent |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC `demo_gkxlumenx_ads` |
| D8 / D10 | N/A 无 UI 改动 |
| D9 8 件套 | N/A |
| D12 lumen 不调 demo **服务** | ✅ Feign/env 打 `gkxlumen-platform-entan-py`；禁止 `demo-platform-entan-py` |
| 禁止改工厂拓扑 | ✅ |
| 禁止 helm JDBC 改正式前缀 | ✅ |

## 遗留风险

- `e2e:chain-gold` [26183](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26183) 红（CHAIN #4 wait_view）。**不是**政策 E0 点名，本叶不修；分类留给 E1/CHAIN。
- E1 不开，等 coordinator 收 E0 后再派。
- 勿再对未装出的新服务只跑 `helm:chart --reuse-values`；新服务用 `helm:deploy` 或补全 values 后再 chart。

## 回滚命令

```text
# 回滚政策门面 / async 到本叶前 Java SHA（保留 Deployment）
kubectl -n dev set image deploy/gkxlumen-platform-topic-policy app=harbor.htmisoft.net/gkx/gkxlumen-topic-policy:9f403944
kubectl -n dev set image deploy/gkxlumen-platform-topic-async-service app=harbor.htmisoft.net/gkx/gkxlumen-topic-async-service:9f403944

# 回滚前端到 C1 修前（无 POL-04）
kubectl -n dev set image deploy/gkx-lumen-topic nginx=harbor.htmisoft.net/gkx/gkx-lumen-topic:b0d0252d

# 回滚政策 HTTP 到政策 HTTP 前 entan 镜像（无 /internal/policy）
kubectl -n dev set image deploy/gkxlumen-platform-entan-py app=harbor.htmisoft.net/gkx/gkxlumen-entan-py-api:548be2aa

# 整仓 helm 回退到装出政策前（会卸 topic-policy，慎用；须列清单）
# helm rollback gkxlumen-platform 29 -n dev
```

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 185000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.25 |
| cost_warn | green |
