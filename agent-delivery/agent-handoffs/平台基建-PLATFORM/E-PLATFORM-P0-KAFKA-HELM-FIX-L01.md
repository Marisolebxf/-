# E-PLATFORM-P0-KAFKA-HELM-FIX-L01 · demo ai-py 交由算法 CI 单一部署，helm release 去掉旧 RabbitMQ env

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 状态由监管人改，本叶未调用 task-registry MCP。本文件未提交编排仓，由监管人提交。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。只改 `values-demo.yaml` 的一个开关和两行注释；没改 `k8s-deploy.sh` / `.gitlab-ci.yml`，没加模板或脚本。可观测、D12、D13、handoff 没有用 YAGNI 跳过。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本次会话未挂载。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。按基线 §1.1 施工：`demo-platform-ai-py` → `gkx.demo.analysis.result` 这条边的部署方从「helm + 算法 CI 双方」收敛为算法 CI 一方（`k8s/dev-ai-py.yaml` 里本就是 `KAFKA_*`）。禁止事项不变。 |
| 会签态 | `draft`（抄基线 §1.1 frontmatter，未改） |
| 说明 | 没有另画图。 |

## 问题清单

- helm release `demo-platform`（ns `zhipu-tts`）rev 15（job 12158，sha 940baf67）的 `aiPy.env` 仍含 `GKX_RABBITMQ_URL`，并且管理 `demo-platform-ai-py`；同一个 Deployment 又被 demo-svc-topic-py CI 用 `kubectl apply k8s/dev-ai-py.yaml` 管理，形成双部署方。
- `helm:chart` 走 `--reuse-values`，沿用上一版合成值，`values.yaml` 里改成 Kafka 的 env 不生效（48d025a 的改动因此到不了集群）；`helm:deploy` 依赖长期失败的 `backend:image:*`，也走不通。

## 范围与实现

1. **影响面核查**（`demo-svc-platform` dev，`git pull --rebase` 后为 48d025a）：
   - 整个 chart 只有 `templates/ai-service-py.yaml` 引用 `aiPy`，且整文件包在 `{{- if and .Values.aiPy .Values.aiPy.enabled -}}` 里；关闭后只少 `demo-platform-ai-py` 的 Service + Deployment。
   - chart 内没有 nginx / ingress / configmap 按 `aiPy.enabled` 或 `ai-py` 名字引用它，其他服务不受影响。
   - 算法仓 `origin/dev:k8s/dev-ai-py.yaml` 的资源名同为 `demo-platform-ai-py`（Deployment + NodePort 30807 Service），env 为 `KAFKA_BOOTSTRAP_SERVERS` / `KAFKA_TOPIC`，无 RabbitMQ。
   - 算法 CI `deploy:*` 每次都会 `apply` bootstrap YAML，再 `set image`，因此以后由它单方持有 env。
2. **改动**：`helm/gkx-platform/values-demo.yaml` 中 `aiPy.enabled: true → false`，加注释说明由算法 CI 单一部署（含本任务 ID）。`workerPy` 保持 false，其他服务未动。
3. **发布**：push 后等 pipeline 2551 的 `helm:lint` 成功，只 play `helm:chart`；helm 删除 `demo-platform-ai-py` 之后，在项目 15 重试 `deploy:ai-py`，由 bootstrap YAML 重新创建。

## 偏离

- 无方案偏离。
- **集群只读核对未完成**：通过 ssh-executor 连接 10.50.69.111，但该主机上的 kubectl / helm 没有可用的集群凭据（API 返回 Authentication required）。因此 Java 镜像 tag 和 release manifest 只能依据 CI trace 与 chart 源码推断，推断依据见下文。

## 修改内容

- `repos/demo-svc-platform/helm/gkx-platform/values-demo.yaml`（+3 / −1）

## 测试结果 / 验收证据

| 项 | 证据 |
|----|------|
| commit | `4c0aa0d`（demo-svc-platform `origin/dev`，48d025a..4c0aa0d） |
| helm:lint | pipeline 2551 / job 13356 success（`helm lint` + `helm template` 带 values-demo） |
| helm:chart | job 13367 success：`Release "demo-platform" has been upgraded`，**REVISION 15 → 16**，STATUS deployed，LAST DEPLOYED 2026-10-18 01:07:43 |
| Python tag 钉住 | `entanPy=97a36a73`、`entanPyWorker=97a36a73`、`innovPy=9e1aca7d`、`searchPy=a7f27922`、`aiPy=bb9bab05`（模板已不渲染，无效果）、`workerPy=bb9bab05`（workerPy=false，无效果）；`demoPy` skip（无 Deployment） |
| Java 未改 tag | trace 显示 `HELM_CHART_ONLY: --reuse-values, do not --set global.imageTag`，`global.imageTag` 沿用 rev 15。rev 15（12158）之后项目 21 没有任何成功的 Java `deploy:*`（set image）作业，因此不存在热更 tag 被 helm 改回的情况。本次 Java pod 全部滚动，原因是 `microservices.yaml` 等模板含 `rollme: randAlphaNum`，每次 helm upgrade 都会重启 pod，并非 tag 变化。 |
| ai-py 被 helm 删除 | 13367 rollout summary：`pod/demo-platform-ai-py-… Terminating`，Service 列表里已无 `demo-platform-ai-py` |
| ai-py 由算法 CI 重建 | 项目 15 pipeline 2548（sha bb9bab05），`deploy:ai-py` 由 13302 重试为 **job 13374 success**：`service/demo-platform-ai-py created`、`deployment.apps/demo-platform-ai-py created`、`deployment "demo-platform-ai-py" successfully rolled out`，镜像 `harbor.test.com/zp-tts/gkx-ai-service:bb9bab05` |
| healthz | 本机 `GET http://10.50.69.111:30807/healthz` → **200**，`{"status":"ok","service":"gkx-ai-service","mock_enabled":false,...}` |
| release manifest 无 `GKX_RABBITMQ_URL` | trace 不输出 manifest，这里是推断：rev 15 所用的 940baf6 版 chart 里，`GKX_RABBITMQ_URL` 只出现在 `aiPy.env` 与 `workerPy.env`；rev 16 两者都关闭，对应模板不渲染；当前 chart `git grep -i rabbit helm/` 无结果。因此 rev 16 渲染出的 manifest 不含该变量。注意：release 的**合成值**（`helm get values --all`）里 `aiPy.env` 可能仍带旧条目，但不会被渲染。 |

## 遗留风险

- **Java pod 滚动后的就绪未核实**：13367 结束时（无 `--wait`），gateway / auth / upms / demo-a / demo-b-biz / innov 的新 pod 还在 `Init`。镜像不变，预期能 Ready，但本次没有集群凭据去确认，建议 coordinator 或 QA 抽查 `kubectl -n zhipu-tts get pods`。
- 以后再点 `helm:chart` 仍会因为 `rollme` 重启全部 Java / Python pod，这是 chart 既有行为，本叶未改。
- helm 合成值里可能残留旧的 `aiPy.env`（含 RabbitMQ 地址）；只要 `aiPy.enabled=false` 就不会渲染。如果以后有人重新打开 aiPy，需要先确认会不会带回旧 env，或改走不带 `--reuse-values` 的完整发布。
- `CHART_ONLY_PY_PIN_SPECS` 仍会对 aiPy / workerPy `--set image.tag`，无害但会写进 release 值；没改脚本（属于红线）。
- `demo-platform-worker-py` 同样由算法 CI 部署（pipeline 2548 / 13303 success），不归 helm 管（rev 15 时 workerPy 即为 false）。

## CI/CD（必填）

- 分支：`dev`
- commit：`4c0aa0d`（demo-svc-platform）
- pipeline / job：项目 21 pipeline 2551（helm:lint 13356、helm:chart 13367）；项目 15 pipeline 2548（deploy:ai-py 13374，重试自 13302）
- 部署 namespace / 镜像 tag：`zhipu-tts`；`gkx-ai-service:bb9bab05`
- K8s rollout：成功（`demo-platform-ai-py successfully rolled out`）
- dev 测试：`http://10.50.69.111:30807/healthz` → 200
- 未点击：`helm:deploy`、任何 Java `deploy:*` / `backend:image:*`

## 可观测性（建议）

- OTEL_SERVICE_NAME：由 `k8s/dev-ai-py.yaml` 注入（本叶未改，env 名单见该文件 `OTEL_*`）
- traceId：本叶不涉及业务请求，未抽样
- Tempo / Loki：有（`demo-platform-tempo` / `demo-platform-loki` 在 rev 16 rollout summary 中 Running）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D1 算法只在 Python | ✅ 未触及 |
| D2 调用链 前端→Java→Python `/internal/*` | ✅ 未改路由；ai-py Service 名与 NodePort 不变 |
| D3 Nebula | ✅ 未触及 |
| D4 可观测 | ✅ ai-py 的 OTEL env 由 bootstrap YAML 保留；Tempo / Loki 未动 |
| D5 CI/CD | ✅ push → helm:lint 绿 → helm:chart → 算法 CI deploy 绿 |
| D6 demo 只读 merge | ✅ 只改 demo 仓，未向 lumen merge |
| D12 demo / lumen 隔离 | ✅ 只动 `demo-svc-platform` 与 `demo-svc-topic-py` CI，未让 lumen 引用 demo 服务 |
| D13 消息总线 Kafka | ✅ helm 不再渲染含 `GKX_RABBITMQ_URL` 的 ai-py；现网 ai-py 为 `KAFKA_*` 版（bb9bab05）。未向 Kafka 生产消息 |
| 红线 | ✅ 未改 `k8s-deploy.sh` / `.gitlab-ci.yml` / MySQL 口令行；未 force push；未碰 `E:\gkx-lumen\`；token 只在内存中使用，未打印、未落盘 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 220k（输入为主） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈ $3.5 |
| cost_warn | false |
| source | `session_estimate` |

## 涉及文件

- `repos/demo-svc-platform/helm/gkx-platform/values-demo.yaml`
- 本 handoff
