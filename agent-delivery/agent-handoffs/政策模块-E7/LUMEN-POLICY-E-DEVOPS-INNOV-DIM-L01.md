# LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01 · 政策专题 E0 · 滚 gkxlumen-innov 至 demo DIM

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01-派单包.md`](./LUMEN-POLICY-E-DEVOPS-INNOV-DIM-L01-派单包.md)  
> C1 改绑：[`LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01.md`](./LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01.md)（`300ad30`）  
> **本叶不标 done**：tech_task 走 AV → `ready_to_sign`。禁止宣称金路径已绿。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；tech_task。本轮只点名 `gkxlumen-innov` 镜像 + Helm `INNOV_DIM_SCHEMA`。禁止改业务代码 / DDL 正式库 / 改正式 JDBC / 重滚 UI / 重滚政策 Python HTTP。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短发布边：origin/dev 已自动 `backend:image:innov`；点名 manual `helm:chart` + `deploy:innov`。未改业务代码、未 DDL、未改正式 JDBC、未重滚 `gkx-lumen-topic` / 政策 Python 镜像。未用 YAGNI 跳过 handoff / 探活。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 发布核验，无大日志需压缩。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `CHAIN-STORE-DIM-INDUSTRY-CLUSTER` |
| 图 diff | 无。本叶只滚运行时：镜像 `7d12b8dd` → `300ad303`，注入 `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`。不翻签存储图。 |
| 会签态 | `draft`（源文件 frontmatter；本叶不翻签） |

## 结论：innov 已滚到 300ad30 + demo DIM（clusters 非 500）

`origin/dev` HEAD = `300ad3036fa052f386051ed0ce7148bd8e27f554`。push 后 `backend:image:innov` **已自动绿**；`deploy:innov` / `helm:chart` 在 origin/dev 为 **manual**，本叶已点名。

| 点名 | K8s | ready | 镜像 / env | CI |
|------|-----|-------|------------|-----|
| `gkxlumen-innov` | `gkxlumen-platform-innov` | **1/1** | `gkxlumen-innov:300ad303`；Pod env **`INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`**、`INNOV_MYSQL_DB=demo_gkxlumenx_ads` | [backend:image:innov 26216](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26216) 绿 · [helm:chart 26226](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26226) 绿 · [deploy:innov 26233](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26233) 绿 |
| `gkx-lumen-topic` | 本轮**不重滚** | **1/1** | `gkx-lumen-topic:006d186d` | 保持 C1ROLL |
| 政策 Java `topic-policy` | 本轮不点名 | **1/1** | `gkxlumen-topic-policy:7d12b8dd` | 未点 |
| 政策 HTTP | 本轮**不重滚镜像** | **1/1** | `gkxlumen-entan-py-api:ea3acc39` | helm:chart 触发了同 tag 滚动（见偏离） |

helm release `gkxlumen-platform` **rev 34 deployed**（16:11:55 +08，`helm:chart`）。innov Deployment revision **39**。

**不要宣称金路径已绿。** 本叶只保证 clusters **非 500**。`e2e:chain-gold` 红/在跑 **不挡本叶**。

## 范围与实现

- 未改 `lumen-svc-platform` 业务代码（C1 `300ad30` 已在 origin/dev）。
- 未 DDL 正式库、未改正式 JDBC 前缀；数仓仍 `demo_gkxlumenx_*`。
- 未重滚前端 `006d186d`。未换政策 Python 镜像 tag。
- 顺序：先 `helm:chart`（`FORCE_NACOS_REPUBLISH=false`，`--reuse-values` 注入 env，不改 `global.imageTag`）→ 再 `deploy:innov` set-image `300ad303`。避免 helm 把镜像打回上一 release tag。

## 偏离说明

- `deploy:innov` **不会自动跑**（`.gitlab-ci.yml` 仅 `FULL_PIPELINE=true` 或 manual）。本叶点名 [26233](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26233)。
- `helm:chart` `--reuse-values` 仍滚动了若干同 release 工作负载（gateway / innov / auth / entan-py 等同 SHA 新 RS）。**镜像 tag 未变**：entan-py 仍 `ea3acc39`，前端仍 `006d186d`。未点 `helm:deploy`、未 `FULL_PIPELINE`。
- `e2e:chain-gold` 因同 pipeline 自动 `deploy:topic-chain` / `deploy:topic-async-service` 可能红或在跑。**按派单不修、不记本叶失败。**

## 产物清单

- 现网 innov：`gkxlumen-innov:300ad303` @ ns=`dev`
- 本文 handoff（编排仓；无业务仓 diff）

## 验收证据

```text
kubectl -n dev get deploy gkxlumen-platform-innov
IMAGE=harbor.htmisoft.net/gkx/gkxlumen-innov:300ad303  READY=1/1
INNOV_DIM_SCHEMA=demo_gkxlumenx_dim
INNOV_MYSQL_DB=demo_gkxlumenx_ads
Pod=gkxlumen-platform-innov-57c9b77566-scrlx

GET http://10.50.69.111:30899/topic/v1/meta/industry-clusters?include_l0=true
HTTP 200  code=0  items=15  mapped=9  pending_vendor=6  with_l0=9
policy_version=sz-10+5-2026  q068=pending_client
X-Trace-Id=d37b6beb5cee5fc3f7fe11481a451fa4

GET http://10.50.69.111:30899/innov/v1/meta/industry-clusters?include_l0=true
HTTP 200  X-Trace-Id=b6c89cf35e61d6de3b49cbdc77de49f2

GET http://10.50.69.111:30892/api/topic/v1/meta/industry-clusters?include_l0=true
HTTP 200  （前端代理，镜像仍 006d186d）

GET http://10.50.69.111:30892/
HTTP 200
```

映射例：`CL-SEI-01` 新一代信息技术 `mapped` L0=`INB1303` 等 5 条。`CL-SEI-03` 新能源 `pending_vendor` L0 空（诚实空，不造假）。

## 修改内容

| 路径 | 动作 |
|------|------|
| 业务仓 / JDBC / DDL | 无 |
| 本文 handoff | 新增 |

## 测试结果

- 点名前现网：`gkxlumen-innov:7d12b8dd`，**无** `INNOV_DIM_SCHEMA`（仍会读正式 `gkxlumenx_dim` → 500）。
- 点名后：镜像 `300ad303` + env `demo_gkxlumenx_dim`；三条 clusters 路径均 **200**，不是 500。
- 前端 `006d186d` 仍 1/1。政策 Python 镜像仍 `ea3acc39`。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`（禁止 force）
- commit：`300ad3036fa052f386051ed0ce7148bd8e27f554`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5935 （status=`manual`，因其余单服务 deploy 未点）
- jobs：[26216](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26216) image · [26226](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26226) helm:chart · [26233](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/26233) deploy:innov
- namespace：`dev`
- 镜像：`gkxlumen-innov:300ad303`
- K8s rollout：`gkxlumen-platform-innov` **成功**
- helm：`gkxlumen-platform` rev **34 deployed**
- dev 探活：网关 30899 clusters **HTTP 200**

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-innov`
- 滚后 traceId：`d37b6beb5cee5fc3f7fe11481a451fa4`（topic 前缀） / `b6c89cf35e61d6de3b49cbdc77de49f2`（innov 前缀）
- Tempo：http://10.50.69.111:30201/api/traces/d37b6beb5cee5fc3f7fe11481a451fa4
- 原 500 根因 trace：`071b34f54c36d31761617fc884567f03`（C1 已记；本叶未复用）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改 Java 算法 |
| 前端→Java→Python `/internal/*` | ✅ 未越层；未改 Feign |
| 图谱 Nebula | ✅ 未写 nGQL |
| 可观测 | ✅ innov OTel；新 trace 200 |
| CI/CD | ✅ origin/dev；点名 manual job；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 只读 ADS+DIM | ✅ 只读 `demo_gkxlumenx_dim` |
| D12 lumen 不调 demo **服务** | ✅ 未改调用链 |
| 禁止改工厂拓扑 | ✅ |
| 禁止 helm JDBC 改正式前缀 | ✅ 注入的是 demo DIM schema |
| 禁止改业务代码 / DDL 正式库 | ✅ |

## 遗留风险

- 部分集群 `pending_vendor`（无 L0）→ 页内「无相关产业数据」是诚实空，不是本叶回归。
- **不要宣称金路径已绿。** QA 复测金路径 #2～#5 另派。
- 同 pipeline 的 `e2e:chain-gold` / CHAIN 红 **不是**本叶失败。
- helm:chart 会滚动同 release 其他工作负载（同 tag）。以后若只改 innov env，仍须接受一次 chart upgrade 的连带 RS；不要用 `kubectl set env` 绕过 Helm 真源。

## 回滚命令

```text
# 回滚 innov 镜像到本叶前（无 demo DIM 绑定，clusters 会再 500）
kubectl -n dev set image deploy/gkxlumen-platform-innov app=harbor.htmisoft.net/gkx/gkxlumen-innov:7d12b8dd
# env 回滚需 helm rollback gkxlumen-platform 33 -n dev（会波及同 release，慎用）
```

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.42 |
| cost_warn | green |

## coordinator 下一步

1. 收本叶 AV → `ready_to_sign`（执行 agent 已转；**不要**标 done）。
2. 派 QA 复测 clusters 非 500 + 金路径 #2～#5。
3. 不要把 CHAIN `e2e:chain-gold` 红当政策 E0 失败。
