# LUMEN-POLICY-E-DEVOPS-C1ROLL-L01 · 政策专题滚前端至 C1-FP

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-E-DEVOPS-C1ROLL-L01-派单包.md`](./LUMEN-POLICY-E-DEVOPS-C1ROLL-L01-派单包.md)  
> 前序 E0：[`LUMEN-POLICY-E-DEVOPS-L01.md`](./LUMEN-POLICY-E-DEVOPS-L01.md)（当时镜像 `97963375`，本轮已换掉）  
> **本叶不标 done**：tech_task 走 AV → `ready_to_sign`。禁止宣称金路径已绿。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；tech_task；本轮只滚 `lumen-ui-topic`；禁止改业务代码 / 正式 JDBC / Java·Python helm |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短发布边：核 origin/dev 自动 CI，未手动点名、未改业务代码、未改 helm/JDBC、未重滚 Java/Python |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 发布核验，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 无。仅换前端镜像 tag `97963375` → `006d186d`；§2.3 发布边（30892 / topic-policy:7097 / 网关 `/policy/**` / 政策 HTTP=`gkxlumen-platform-entan-py:8000`）未改 |
| 会签态 | `approved`（本叶不翻签） |

## 结论：前端已滚到 006d186（自动 CI 绿）

`origin/dev` HEAD = `006d186dc3ef26671328b7ed54e637b10c261d50`。push 后 `frontend:build` / `frontend:image` / `deploy:k8s` **已自动跑绿**，无需点名。现网已换掉 E0 的 `97963375`。

| 点名 | K8s | ready | 镜像 | CI（htsvr036 gitlab-runner 实测 job id） |
|------|-----|-------|------|-----|
| `lumen-ui-topic` | `gkx-lumen-topic` NodePort **30892** | **1/1** | `gkx-lumen-topic:006d186d`（含 DETAIL `d5ea3f7` / SCOPE `2659503` / C1-FP `006d186`） | [frontend:build 26201](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26201) 绿 · [frontend:image 26202](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26202) 绿 · [deploy:k8s 26204](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26204) 绿（与 RS 于 15:26:42 +08 对齐）。并行 [trivy:frontend 26203](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26203) 绿 |
| `gkxlumen-topic-policy` | 本轮不重滚 | **1/1** | `gkxlumen-topic-policy:7d12b8dd` | 探活仍绿，未点 helm |
| `gkxlumen-topic-async-service` | 本轮不重滚 | **1/1** | `gkxlumen-topic-async-service:7d12b8dd` | 同上 |
| 政策 HTTP | 本轮不重滚 | **1/1** | `gkxlumen-entan-py-api:ea3acc39` | 同上 |

ReplicaSet：现网 `gkx-lumen-topic-666bbc7bb7` 镜像 `006d186d` ready 1；旧 `7454444bc5`=`97963375` 已 0。中间 `d5ea3f7a` / `26595039` 也曾自动滚过，最终被 HEAD 覆盖。Harbor rag runner 本地 tag `006d186d` 构建于 2026-09-02 15:26:25 +08。

**不要宣称金路径已绿。** `e2e:chain-gold` [26205](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26205) 红，**不挡本叶**，留给 E1/CHAIN。

## 范围与实现

- 只核 `lumen-ui-topic` `origin/dev` 自动 CI + K8s 镜像。未改前端业务代码。
- 未改 Java/Python helm、未改 `values` JDBC。现网仍 `demo_gkxlumenx_*`。
- Java/Python 探活仍绿（`degraded=false`），故未重滚。

## 偏离说明

- 无。CI 已因 `006d186` 自动滚，未手工 `kubectl set image`、未点名 retry。
- `e2e:chain-gold` 红按派单不修、不记本叶失败。

## 产物清单

- 现网前端：`lumen-ui-topic` `006d186d` @ `http://192.168.88.50:30892`
- 本文 handoff（编排仓；无业务仓 diff）

## 验收证据

```text
kubectl -n dev get deploy gkx-lumen-topic
IMAGE=harbor.htmisoft.net/gkx/gkx-lumen-topic:006d186d  READY=1/1

GET http://192.168.88.50:30892/
HTTP 200

GET http://192.168.88.50:30899/policy/topic/v1/policy/health
HTTP 200
java.status=up  service=gkxlumen-topic-policy-biz
python.name=lumen-algo-py  pathPrefix=/internal/policy
python.baseUrl=http://gkxlumen-platform-entan-py:8000
degraded=false
```

Pod：`gkx-lumen-topic-666bbc7bb7-sjhkx` 1/1 Running @ htsvr077。  
JDBC 未动。无正式前缀数据面变更。

## 修改内容

| 路径 | 动作 |
|------|------|
| 业务仓 / helm / JDBC | 无 |
| 本文 handoff | 新增 |

## 测试结果

- `kubectl -n dev`：`gkx-lumen-topic` 1/1，镜像 `006d186d`（≥ 目标 SHA `006d186dc3ef26671328b7ed54e637b10c261d50`）。
- 30892 HTTP 200。
- 政策 health 200，python 仍打 `gkxlumen-platform-entan-py`，Java/Python 镜像仍为 E0 的 `7d12b8dd` / `ea3acc39`。
- `e2e:chain-gold` 26205 红，不挡本叶。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`（禁止 force）
- commit：`006d186dc3ef26671328b7ed54e637b10c261d50`（一并含 `2659503` SCOPE、`d5ea3f7` DETAIL）
- pipeline jobs：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26201 · [26202](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26202) · [26204](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26204)（project=231）
- namespace：`dev`
- 镜像：`gkx-lumen-topic:006d186d`（已换掉 `97963375`）
- K8s rollout：`gkx-lumen-topic` **成功**（rev 由 E0 的 209 进到 ReplicaSet `666bbc7bb7`）
- dev URL：http://192.168.88.50:30892 HTTP **200**

## 可观测性

- 前端静态站，无新 OTEL_SERVICE_NAME。
- 政策门面 OTEL 仍 `gkxlumen-topic-policy-biz`（本叶未改）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改 Java 算法 |
| 前端→Java→Python `/internal/*` | ✅ health python.pathPrefix=`/internal/policy` |
| 图谱 Nebula | ✅ 未写 nGQL |
| 可观测 | ✅ 未拆平台 Collector |
| CI/CD | ✅ `origin/dev` 自动绿；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ JDBC 未改 |
| D8 / D10 | N/A 本叶无 UI 改动 |
| D9 8 件套 | N/A |
| D12 lumen 不调 demo **服务** | ✅ 探活仍打 `gkxlumen-platform-entan-py` |
| 禁止改工厂拓扑 | ✅ |
| 禁止 helm JDBC 改正式前缀 | ✅ 未改 helm |

## 遗留风险

- `e2e:chain-gold` [26205](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26205) 红。**不是**本叶点名，不修；分类留给 E1/CHAIN。
- 本叶不宣称政策金路径已绿。E1 冒烟另派。

## 回滚命令

```text
# 回滚前端到本叶前（E0 POL-04 / C1 TS 修，无 C1-FP / SCOPE / DETAIL）
kubectl -n dev set image deploy/gkx-lumen-topic nginx=harbor.htmisoft.net/gkx/gkx-lumen-topic:97963375
```

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.35 |
| cost_warn | green |
