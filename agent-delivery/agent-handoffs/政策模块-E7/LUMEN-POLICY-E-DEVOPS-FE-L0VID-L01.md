# LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01 · 政策专题 E0 · 滚 lumen-ui-topic 至 L0VID 1ce03cc

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01-派单包.md`](./LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01-派单包.md)  
> 前序 C1：[`LUMEN-POLICY-E-C1-FE-L0VID-L01.md`](./LUMEN-POLICY-E-C1-FE-L0VID-L01.md)（`1ce03cc`）  
> 前序前端滚：[`LUMEN-POLICY-E-DEVOPS-C1ROLL-L01.md`](./LUMEN-POLICY-E-DEVOPS-C1ROLL-L01.md)（当时 `006d186d`；其后现网曾是 `c4758206`）  
> **本叶不标 done**：tech_task 走 AV → `ready_to_sign`。禁止宣称金路径已绿。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；tech_task；本轮只滚 `lumen-ui-topic`；禁止改业务代码 / 重滚 innov / 重滚政策 Python |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短发布边：核 origin/dev 自动 CI，未手动点名、未改业务代码、未重滚 innov/Python。未用 YAGNI 跳过 handoff / 30892 探活 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 发布核验，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 无。仅换前端镜像 tag `c4758206` → `1ce03cc4`；发布边（30892 / topic-policy:7097 / 网关 `/policy/**` / 政策 HTTP=`gkxlumen-platform-entan-py:8000`）未改 |
| 会签态 | `approved`（本叶不翻签） |

## 结论：前端已滚到 1ce03cc（自动 CI 绿）

`origin/dev` HEAD = `1ce03cc460ca2803c6bcd423794912ba0b211e72`（含政策 L0VID C1；也含 `c475820`）。push 后 `frontend:build` / `frontend:image` / `deploy:k8s` **已自动跑绿**，无需点名。现网已换掉次要 C2 的 `c4758206`。

| 点名 | K8s | ready | 镜像 | CI（htsvr036 gitlab-runner 实测 job id） |
|------|-----|-------|------|-----|
| `lumen-ui-topic` | `gkx-lumen-topic` NodePort **30892** | **1/1** | `gkx-lumen-topic:1ce03cc4`（≥ 目标 `1ce03cc`；含 C1-FP `006d186` / CHAIN `c475820` / L0VID `1ce03cc`） | [frontend:build 26253](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26253) 绿 · [frontend:image 26254](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26254) 绿 · [deploy:k8s 26256](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26256) 绿。并行 [trivy:frontend 26255](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26255) 绿 |
| `gkxlumen-innov` | 本轮**不重滚** | **1/1** | `gkxlumen-innov:300ad303` | 未点 helm / deploy |
| `gkxlumen-topic-policy` | 本轮不重滚 | **1/1** | `gkxlumen-topic-policy:7d12b8dd` | 未点 |
| 政策 HTTP | 本轮**不重滚** | **1/1** | `gkxlumen-entan-py-api:ea3acc39` | 未点 |

ReplicaSet：现网 `gkx-lumen-topic-594f54559b` 镜像 `1ce03cc4` ready 1（pod `gkx-lumen-topic-594f54559b-5nz85` @ htsvr053，start `2026-09-02T08:49:54Z`）；旧 `66c5dcd68f`=`c4758206` 已 0。Deployment generation 214 / revision 213。

**不要宣称金路径已绿。** 本叶 DoD 只认前端镜像 + HTTP 200。pipeline [5940](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5940) 的 `e2e:chain-gold` [26257](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26257) 与后续 trigger [5944](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5944)/[26305](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26305) 不作为本叶验收；政策金路径留给 E1。

## 范围与实现

- 只核 `lumen-ui-topic` `origin/dev` 自动 CI + K8s 镜像。未改前端业务代码。
- 未改 Java/Python helm、未改 `values` JDBC。现网仍 `demo_gkxlumenx_*`。
- innov 保持 `300ad303`；政策 Python 保持 `ea3acc39`。故未重滚。

## 偏离说明

- 无。CI 已因 `1ce03cc` 自动滚，未手工 `kubectl set image`、未点名 retry。
- `e2e:chain-gold` 按派单不修、不记本叶成败，不宣称金路径已绿。

## 产物清单

- 现网前端：`lumen-ui-topic` `1ce03cc4` @ `http://192.168.88.50:30892`
- 本文 handoff（编排仓；无业务仓 diff）

## 验收证据

```text
kubectl -n dev get deploy gkx-lumen-topic
IMAGE=harbor.htmisoft.net/gkx/gkx-lumen-topic:1ce03cc4  READY=1/1
rollout status: successfully rolled out

GET http://192.168.88.50:30892/
HTTP 200
Content-Length: 456
Last-Modified: Wed, 02 Sep 2026 08:49:19 GMT
```

Pod：`gkx-lumen-topic-594f54559b-5nz85` 1/1 Running @ htsvr053。  
imageID：`harbor.htmisoft.net/gkx/gkx-lumen-topic@sha256:c5698de4f6fe283937ec7bda50f6149f2cb23490c79482c2701103318564531c`  
JDBC 未动。无正式前缀数据面变更。innov / 政策 Python 镜像未变。

## 修改内容

| 路径 | 动作 |
|------|------|
| 业务仓 / helm / JDBC | 无 |
| 本文 handoff | 新增 |

## 测试结果

- `kubectl -n dev`：`gkx-lumen-topic` 1/1，镜像 `1ce03cc4`（≥ 目标 SHA `1ce03cc460ca2803c6bcd423794912ba0b211e72`）。
- 30892 HTTP 200（88.50 与工作站各测一次）。
- innov 仍 `300ad303`；政策 Python 仍 `ea3acc39`；topic-policy 仍 `7d12b8dd`。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`（禁止 force）
- commit：`1ce03cc460ca2803c6bcd423794912ba0b211e72`（一并含 `c475820` CHAIN 全景、`006d186` C1-FP）
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5940 （project=231）
- jobs：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26253 · [26254](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26254) · [26256](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26256)
- namespace：`dev`
- 镜像：`gkx-lumen-topic:1ce03cc4`（已换掉 `c4758206`）
- K8s rollout：`gkx-lumen-topic` **成功**（RS `594f54559b`）
- dev URL：http://192.168.88.50:30892 HTTP **200**

## 可观测性

- 前端静态站，无新 OTEL_SERVICE_NAME。
- 政策门面 OTEL 仍 `gkxlumen-topic-policy-biz`（本叶未改）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改 Java 算法 |
| 前端→Java→Python `/internal/*` | ✅ 未改调用链 |
| 图谱 Nebula | ✅ 未写 nGQL |
| 可观测 | ✅ 未拆平台 Collector |
| CI/CD | ✅ `origin/dev` 自动绿；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 未改 |
| D8 / D10 | N/A 本叶无 UI 改动 |
| D9 8 件套 | N/A |
| D12 lumen 不调 demo **服务** | ✅ 未改 Feign / 网关 |
| 禁止改工厂拓扑 | ✅ |
| 禁止 helm JDBC 改正式前缀 | ✅ 未改 helm |

## 遗留风险

- 本叶不宣称政策金路径已绿。E1 冒烟另派。
- CHAIN `e2e:chain-gold` 不是本叶点名；不挡本叶、不修、不作为本叶成败。

## 回滚命令

```text
# 回滚前端到本叶前（CHAIN 全景 c475820，无政策 L0VID C1）
kubectl -n dev set image deploy/gkx-lumen-topic nginx=harbor.htmisoft.net/gkx/gkx-lumen-topic:c4758206
```

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 42000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.30 |
| cost_warn | green |
