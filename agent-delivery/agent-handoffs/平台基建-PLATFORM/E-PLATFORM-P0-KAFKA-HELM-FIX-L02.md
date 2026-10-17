# E-PLATFORM-P0-KAFKA-HELM-FIX-L02 · 清空 aiPy/workerPy env，去掉 helm release 存储值里的旧 AMQP

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
| 说明 | 与派单强度一致。只在 `values-demo.yaml` 加两行 `env: []` 及注释；另一仓只改三行注释。没改模板、`k8s-deploy.sh`、`.gitlab-ci.yml` 可执行行。可观测、D12、D13、handoff 没有用 YAGNI 跳过。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本次会话未挂载。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无变化。只清理 helm release 存储值中已不渲染的旧 env，消息总线边与禁止事项不变。 |
| 会签态 | `draft`（沿用 L01 所抄基线 §1.1 frontmatter，未改） |
| 说明 | 没有另画图。 |

## 问题清单

- release `demo-platform`（ns `zhipu-tts`）rev 16 由 `helm:chart`（`HELM_CHART_ONLY` → `--reuse-values`）发布，沿用了 rev 15 的合成值。rev 15 的 chart（940baf67）中 `aiPy.env`、`workerPy.env` 含带口令的 AMQP 连接串，因此 rev 16 的存储值仍带着它，虽然两服务 `enabled: false` 不渲染。
- `demo-svc-topic-py/.gitlab-ci.yml` 三处历史注释仍提到 RabbitMQ。

## 范围与实现

1. **demo-svc-platform**（dev，`git pull --rebase` 后为 4c0aa0d）：`helm/gkx-platform/values-demo.yaml` 的 `aiPy`、`workerPy` 下各加一行注释 + `env: []`，保留 `enabled: false` 与原注释。
   - 模板核查：`templates/ai-service-py.yaml`、`ai-worker-py.yaml` 整文件包在 `{{- if and .Values.X .Values.X.enabled -}}` 内；env 段用 `{{- with .Values.X.env }}`，空列表为假值，直接跳过，不报错。CI `helm:lint`（含 `helm template` + values-demo）通过即为实证。
   - 合并语义：Helm 合并 `--reuse-values` 旧值与 `-f` 新值时，列表整体替换（不逐项合并），故旧 `env` 列表被 `[]` 覆盖。
2. **demo-svc-topic-py**（dev，pull 后为 bb9bab0）：`.gitlab-ci.yml` 第 14、97、119 行注释去掉 RabbitMQ 字样（改写为「残留旧 env」）。`git diff -U0` 确认三处变化行去掉前导空白后均以 `#` 开头，无可执行行变化（第 119 行是 `script: - |` 块内的 shell 注释）。
3. **发布**：项目 21 pipeline 2559 的 `helm:lint` 成功后，只 play `helm:chart`（job 13452）。未点 `helm:deploy`、任何 Java 作业；项目 15 pipeline 2560 的 `deploy:*` 为 manual，未点。

## 偏离

- 无方案偏离。
- **release 存储值未直接读取**：本机无集群凭据（同 L01），无法 `helm get values`。「rev 17 存储值的 aiPy/workerPy env 为空」依据 Helm 列表替换语义 + 本次 values 推断；job 13452 trace 中搜索 `amqp` / `RABBIT` 无命中（trace 不打印 values，仅作旁证）。建议有集群凭据者执行 `helm get values demo-platform -n zhipu-tts --all` 抽查 `aiPy.env` / `workerPy.env` 为 `[]`（输出勿外传）。

## 修改内容

- `repos/demo-svc-platform/helm/gkx-platform/values-demo.yaml`（+4）
- `repos/demo-svc-topic-py/.gitlab-ci.yml`（3 行注释改写）

## 测试结果 / 验收证据

| 项 | 证据 |
|----|------|
| commit（平台） | `4eb9e520f686e2cc63f15b082ca4a354b53ad434`（demo-svc-platform `origin/dev`，4c0aa0d..4eb9e52） |
| commit（算法） | `0ed526038b2c12142e68578baa3655c8e42d2fa0`（demo-svc-topic-py `origin/dev`，bb9bab0..0ed5260） |
| helm:lint | 项目 21 pipeline 2559 / job 13441 success |
| helm:chart | job 13452 success：`STATUS: deployed`，**REVISION: 17**，LAST DEPLOYED 2026-10-18 03:05:59 |
| 未 set imageTag | trace：`HELM_CHART_ONLY: --reuse-values, do not --set global.imageTag, no --wait` |
| Python tag 钉住 | `entanPy=97a36a73`、`entanPyWorker=97a36a73`、`innovPy=9e1aca7d`、`searchPy=a7f27922`、`aiPy=bb9bab05`、`workerPy=bb9bab05`（后两者不渲染，无效果）；`demoPy` skip（无 Deployment） |
| 算法仓 pipeline | 项目 15 pipeline 2560：`py:smoke` / `py:image:*` success；`deploy:ai-py` / `deploy:worker-py` / `deploy:search-py` manual，未点 |
| Java 探测（rev 17 后约 6.5 分钟，经 `http://10.50.69.111:30887/api`，只读 GET，首轮即全部命中） | gateway `/__no_such_path_l02` → **404** ✅；auth `/auth/token/check_token` → **401** ✅；upms `/admin/tenant/list` → **200** ✅；demo-a `/demo-a/probe-l02` → **424** ✅；innov `/innov/v1/comp/graph/metrics` → **200** ✅ |
| demo-b-biz | **未验证**。demo-a 仅 `DemoController` `POST /run` 经 `RemoteDemoBService`（Feign）调 demo-b，该接口需登录、非只读，且第一步先调已下线的 demo-py，不满足「匿名或只读」旁证条件。 |

## 遗留风险

- **旧口令仍存在于历史中**：helm release 历史 revision（≤16 的旧版本 secret，`sh.helm.release.v1.demo-platform.v*`，至少 rev 15/16 的值里含该 AMQP 连接串；保留数受 `--history-max` 限制）与两仓 git 历史仍含旧口令。本叶只保证 rev 17 起的存储值不再携带。**彻底消除要靠运维改 RabbitMQ 口令或下线旧 RabbitMQ**；删除旧 release secret 会丢失回滚能力，需监管人决定。
- demo-b-biz 就绪未经外部探测确认（见上表），建议有集群凭据者 `kubectl -n zhipu-tts get pods` 抽查。
- 项目 21 pipeline 2559 的 `backend:image:{gateway,register,auth,demo-a,demo-b,innov}` 失败（`ADD failed: ... target/*.jar: file does not exist`），属既有问题（L01 已记为长期失败），与本次 values 改动无关；因此 pipeline 整体非绿，`helm:deploy` 仍走不通。
- 每次 `helm:chart` 都会因 `rollme: randAlphaNum` 重启全部 Java / Python pod，chart 既有行为，本叶未改。
- `CHART_ONLY_PY_PIN_SPECS` 仍会对 aiPy / workerPy `--set image.tag` 写入 release 值，无害；未改脚本（红线）。

## CI/CD（必填）

- 分支：`dev`（两仓）
- commit：`4eb9e52`（demo-svc-platform）、`0ed5260`（demo-svc-topic-py）
- pipeline / job：项目 21 pipeline 2559（helm:lint 13441、helm:chart 13452）；项目 15 pipeline 2560（deploy 作业 manual 未点）
- 部署 namespace / 镜像 tag：`zhipu-tts`；Java `global.imageTag` 沿用旧值，Python 钉住见上
- K8s rollout：helm upgrade 成功（REVISION 17，无 `--wait`）；Java 外部探测全部符合预期
- dev 测试：见「Java 探测」行
- 未点击：`helm:deploy`、任何 Java `deploy:*` / `backend:image:*`、项目 15 `deploy:*`

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改
- traceId：本叶不涉及业务请求，未抽样
- Tempo / Loki：未动

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D1 算法只在 Python | ✅ 未触及 |
| D2 调用链 前端→Java→Python `/internal/*` | ✅ 未改路由 |
| D3 Nebula | ✅ 未触及 |
| D4 可观测 | ✅ 未改 OTEL 配置 |
| D5 CI/CD | ✅ push → helm:lint 绿 → helm:chart 成功 |
| D6 demo 只读 merge | ✅ 只改 demo 仓，未向 lumen merge |
| D12 demo / lumen 隔离 | ✅ 只动 `demo-svc-platform` values 与 `demo-svc-topic-py` 注释，未让 lumen 引用 demo 服务 |
| D13 消息总线 Kafka | ✅ release 存储值清除旧 AMQP env，仓内 CI 注释不再提 RabbitMQ；未向 Kafka 生产消息 |
| 红线 | ✅ 未改 `k8s-deploy.sh` / demo-svc-platform `.gitlab-ci.yml` / MySQL 口令行；未 force push；未碰 `E:\gkx-lumen\`；未调 task-registry MCP；未提交编排仓；token 只在进程内存/环境变量使用，未打印、未落盘；本文与 commit 未写口令或连接串原文 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 150k（输入为主） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈ $2.5 |
| cost_warn | false |
| source | `session_estimate` |

## 涉及文件

- `repos/demo-svc-platform/helm/gkx-platform/values-demo.yaml`
- `repos/demo-svc-topic-py/.gitlab-ci.yml`
- 本 handoff
