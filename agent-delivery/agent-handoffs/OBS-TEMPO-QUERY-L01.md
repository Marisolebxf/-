# OBS-TEMPO-QUERY-L01 · 修复 lumen/demo Tempo，使两条 trace 能查

- 时间：2026-11-16
- 监管人：human:淮政玮
- 仓库：lumen-svc-platform、demo-svc-platform（helm 探针）；线上 ns `zhipu-tts` 已 patch。未改业务 Java，未改政策治理代码。
- ponytail: full — 只加已有 Deployment 上的探针，不新 chart、不改 Tempo 配置、不改业务代码。线上先重启恢复查询，再把同一探针写进模板，避免下次 helm 发布冲掉。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | task-claim 后 task-update-status 到 in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 可观测探针按现场故障补上，没有另起一套 Tempo。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无（未改架构图） |
| 图 diff | 无 |
| 会签态 | 不适用 |
| 说明 | 本次只修 Tempo 进程不退出导致查不到 trace。 |

## 问题清单

- lumen Tempo `30202` 连接拒绝。
- demo Tempo `30200` `GET /api/traces/<id>` 500：`error querying ingesters ... empty ring`。
- 要查的 trace：`20daac09da4ea189342c0f0863f09678`（执行溯源）、`838aad41ac2aa40ffd53ccf689b5dee2`（执行指标库）。业务写入失败的直接原因是 element 日志里的 `Connection is read-only`，本次未改。

## 根因

两套都是 Tempo 2.7.1 单进程。进程还在，ingester 模块已经不在。

- `GET /ready` 正文：`Some services are not Running:` / `Terminated: 1` / `Running: 17`，HTTP 503。
- `tempo_ring_members{name="ingester"}` 全部为 0。goroutine 里有 distributor / querier / frontend / compactor / storage，没有 `modules/ingester`。
- 日志被刷成 `pusher failed to consume trace data` / `DoBatch: InstancesCount <= 0`。`tempo_distributor_ingester_clients` = 0。容器日志只留了最近约一小时，模块当初为何 Terminated 的那一行已经不在。
- 块列表轮询 `metas=0`。配置里 `block_retention: 72h`，lumen 探针失败已持续约 3d17h，超过保留期，对象存储里看不到块。
- lumen 只有 readiness、没有 liveness（`restarts=0`，已 4d11h）。Pod `0/1`，Endpoints 为空，NodePort `30202` 连接拒绝。
- demo 没有探针（旧容器 `restarts=9`，5d 前那次之后不再涨）。Pod 仍是 `1/1`，`30200` 把查询打到空 ring，返回 500。

重启后 ingester 会自己回到 ring（`ACTIVE=1`，`/ready` 200）。所以查询失败是模块死后进程不退出，不是现在这份 `tempo.yaml` 起不来。

## 修改内容

1. 滚动重启 `deploy/gkxlumen-platform-tempo`、`deploy/demo-platform-tempo`。
2. 线上 patch（随后探针变更再次滚动，验收在第二次滚动之后）：
   - 两套都加 `livenessProbe`：`/ready`，`initialDelaySeconds=60`，`periodSeconds=20`，`failureThreshold=6`（约 2 分钟持续 503 才重启；启动后约 15s 的 ingester ready 等待被 initialDelay 盖住）。
   - demo 补上与 lumen 相同的 `readinessProbe`（`/ready`，delay 10s，period 10s），避免半死进程继续回 empty ring。
3. 模板与线上对齐：
   - `lumen-svc-platform` `helm/gkxlumen-platform/templates/tempo.yaml` commit `a8167c504f636e85466a1bda4dad95d182d3b4c0`
   - `demo-svc-platform` `helm/gkx-platform/templates/tempo.yaml` commit `b9062419453aee527622034134d3cd50ab860947`
4. 用完删除跳板机 `/tmp/admin-kc.yaml`。未执行 helm upgrade，未碰 Nacos。

## 测试结果

命名空间 `zhipu-tts`。探针 patch 滚动完成后：

| 检查 | 结果 |
|------|------|
| Pod | `gkxlumen-platform-tempo-69cb6c5746-5kklw` 1/1；`demo-platform-tempo-774b74bf84-6jv8j` 1/1 |
| 探针 | 两套 deploy 均为 `ready=/ready`、`live=/ready`、liveness delay=60 |
| `http://10.50.69.111:30202/ready` | 200，body `ready` |
| `http://10.50.69.111:30200/ready` | 200，body `ready` |
| ingester ring ACTIVE | lumen、demo 均为 1 |

两条 trace，两个端口，均为 HTTP 404、body 0 字节（trace 已不在，不是连接失败，也不是 empty ring）：

```
curl -sS -o NUL -w "%{http_code} %{size_download}\n" http://10.50.69.111:30202/api/traces/20daac09da4ea189342c0f0863f09678
curl -sS -o NUL -w "%{http_code} %{size_download}\n" http://10.50.69.111:30202/api/traces/838aad41ac2aa40ffd53ccf689b5dee2
curl -sS -o NUL -w "%{http_code} %{size_download}\n" http://10.50.69.111:30200/api/traces/20daac09da4ea189342c0f0863f09678
curl -sS -o NUL -w "%{http_code} %{size_download}\n" http://10.50.69.111:30200/api/traces/838aad41ac2aa40ffd53ccf689b5dee2
```

实测四次都是 `404 0`。

## 遗留风险

- 这两条 trace 查不到原文。ingester 已死超过 72h 保留期，块列表为 0。重启不能把它们找回来。
- 模块当初为何 Terminated，保留日志里没有。liveness 只能在再次发生时把 Pod 拉起来，不能阻止那一次退出。
- 下次 `helm:chart` 若用旧模板会冲掉探针；本次模板已推 `origin/dev`。本次没有跑 helm upgrade。

## CI/CD（必填）

- 分支：`dev`
- commit：lumen `a8167c504f636e85466a1bda4dad95d182d3b4c0`；demo `b9062419453aee527622034134d3cd50ab860947`；本 handoff 在 gkx-orchestration 同一次提交
- pipeline：未为这次探针单独盯 CI。线上已用 kubectl patch 生效，不依赖本次 pipeline。
- 部署：ns `zhipu-tts`，镜像仍是 Tempo v2.7.1，未换镜像
- K8s rollout：两次滚动都到 1/1；最终 Pod 见上表
- 复查命令与结果：见「测试结果」

## 可观测性

- 上述两个 traceId 在 lumen `30202` 与 demo `30200` 均为 404 空 body
- 新进程 `/ready` 200，ingester ring ACTIVE=1

## 涉及文件

- `repos/lumen-svc-platform/helm/gkxlumen-platform/templates/tempo.yaml`
- `repos/demo-svc-platform/helm/gkx-platform/templates/tempo.yaml`
- `agent-delivery/agent-handoffs/OBS-TEMPO-QUERY-L01.md`

## 架构合规自检

- 未改 Java 业务、未改政策治理代码
- 未改调用链 / 图谱 / Nacos
- kubeconfig 未进 git，跳板机副本已删
- 未 force push
