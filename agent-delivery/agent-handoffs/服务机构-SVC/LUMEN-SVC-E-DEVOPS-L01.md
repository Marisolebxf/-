# LUMEN-SVC-E-DEVOPS-L01 · 产业服务链 E0 — 点名服务发布门

> 格式参考 `templates/handoff-template.md`；内容按 2026-08-17 GitLab CI 实测。本单**只核对/触发 deploy、不改业务代码**。本机无 KUBECONFIG、SSH `192.168.88.50:22` 超时、NodePort 不可达，**K8s rollout 以 CI deploy job 日志为准**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。tech_task 绿则 `ready_to_sign`；本单 E0 **未全绿** → `blocked`，不伪绿。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D12 / 可观测核对意图；现网 kubectl 因网络不可达，D12 仅能从 CI/契约侧陈述残差。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本单为 CI/发布门核对，未挂载 compress。 |

## 结论（给 coordinator）

**FAIL（E0 门未过）→ registry `blocked`**

| 点名 | CI 结论 | 说明 |
|------|---------|------|
| lumen-ui-topic | **绿** | pipeline **5115** `deploy:k8s` success · sha `99f19bec` |
| lumen-algo-py（svcan） | **绿** | pipeline **5102** `deploy:api` + `deploy:worker` success · sha `1150bdd0` |
| lumen-topic-py（search-py / gkx_svc） | **绿（本单触发）** | pipeline **5108** 手动 play `deploy:search-py` job **22226** success · image `gkxlumen-search-service:50593548` · rollout `gkxlumen-platform-search-py` |
| gkxlumen-topic-svc | **红 / 未发** | `backend:build` 失败 → image/deploy 全 skipped |
| gkxlumen-topic-async-service | **未吃到今日 SVC 代码** | 同上 build 红；集群上次成功仍为 2026-08-14 pipe **5069** sha `7c173bdc`（CHAIN 期），**不含**今日 JAVA-JOB |

E0 状态句（诚实）：**E0 门未通过**（Java topic-svc/async 被 `ServiceFacadeControllerTest` 拦死）。**禁止**写「联调通过」冒充全绿。

## 点名服务核对（CI）

| 点名 | 仓 / 期望 deploy | 最新相关 pipeline | 关键 job | 结果 |
|------|------------------|-------------------|----------|------|
| lumen-ui-topic | `gkx-lumen-topic` / `deploy:k8s` | [5115](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5115) | [deploy:k8s 22274](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/22274) | success |
| gkxlumen-topic-svc | `gkxlumen-platform-topic-svc` / `deploy:topic-svc`（manual） | [5110](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5110) | [backend:build 22231](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/22231) | **failed**；deploy skipped |
| gkxlumen-topic-async-service | `gkxlumen-platform-topic-async-service` / `deploy:topic-async-service`（dev 自动） | 5110（今日）/ 上次绿 [5069](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5069) | 今日 deploy skipped | **未滚动今日镜像** |
| lumen-topic-py | `gkxlumen-platform-search-py` / `deploy:search-py` | [5108](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5108) | [deploy:search-py 22226](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/jobs/22226) | success（devops play） |
| lumen-algo-py | `lumen-platform-algo-py` / `deploy:api` | [5102](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5102) | deploy:api **22175** / deploy:worker **22176** | success |

已发布前端 URL（契约 / registry，本机未 curl 通）：`http://192.168.88.50:30892`（NodePort；本机连接超时，不伪造 200）。

## 阻塞根因（C1 → 派 api-agent）

`lumen-svc-platform` `backend:build`（pipe 5110 / job 22231，sha `5aa0363b`）：

- 模块：`gkxlumen-topic-svc-biz`
- 测试：`ServiceFacadeControllerTest`（3 errors）
- 根因：`@WebMvcTest` 拉起全量 `GkxlumenTopicSvcApplication` → ResourceServer / `SpringContextHolder.getBeanFactory()` **null**（`pigBearerTokenExtractor` / `PermitAllUrlProperties`）
- 连带：`backend:image:*` 与全部 `deploy:*`（含 **topic-svc**、**topic-async-service**）**skipped**

修复方向（非本单改码）：对齐 topic-chain 的 WebMvcTest 切片（`@WebMvcTest(Controller)` + 排除 Security AutoConfig / mock Feign），或 `-DskipTests` 非团队默认；修绿后：

1. 等 `backend:build` + `backend:image:topic-svc` + `backend:image:topic-async-service`
2. `deploy:topic-async-service`（dev 自动）
3. **手动 play** `deploy:topic-svc`（CI 仍 `when: manual`）
4. 若 Deployment 不存在：先 `helm:deploy` / `helm:chart` 装出 `gkxlumen-platform-topic-svc`（set image 前置）

## D12 说明

| 检查点 | 结果 |
|--------|------|
| 调用链设计 | 总控 §0：前端 → `gkxlumen-topic-svc` → `lumen-topic-py` `/internal/gkx-svc/**` →（按需）`lumen-algo-py/svcan`；禁 Feign demo-* |
| 现网 nginx / Feign env | **本机无法 kubectl/SSH**，未做 CHAIN E0 级现网 grep；待 Java 发绿后补 |
| CI 制品侧 | topic-py / algo-py 已发 lumen 制品；Java topic-svc **未发**，不得用 demo-svc-topic-py 冒充 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 2 调用链 | 设计合规；现网 topic-svc 未上线 → E0 红 |
| 5 CI/CD | 部分绿（ui / algo / search-py）；Java 红 |
| 12 D12 | 设计合规；现网未验 → 残差 |

## 修改内容

- 无业务仓改动。触发：`lumen-topic-py` `deploy:search-py` play。
- 本 handoff + registry evidence/cost/`blocked`。

## 测试结果

- GitLab API 核对五仓 `dev` pipeline / jobs（token=`GKX_GITLAB_TOKEN`）
- play `deploy:search-py` → rollout success（job 日志）
- 本机：`kubectl` 无 kubeconfig；SSH/NodePort `192.168.88.50` **timeout**

## 遗留风险

1. **P0**：修 `ServiceFacadeControllerTest` 否则 SVC Java 永无法进镜像。
2. `deploy:topic-svc` 默认 manual；且首次可能缺 Deployment（需 helm）。
3. async 仍停在 8/14 CHAIN 镜像，今日 SVC Job 代码未进集群。
4. 本机不在 88 网段时，E0 只能信 CI job，不能信本机 curl。

## CI/CD

| 项 | 值 |
|----|-----|
| 分支 | 未改业务仓；编排 `origin/dev` |
| pipeline URLs | ui [5115](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5115) · platform [5110](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5110) · topic-py [5108](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5108) · algo [5102](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5102) |
| K8s ns | `dev`（CI） |
| E0 门 | **未通过** |

## cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | 72000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 3.60 |
| cost_warn | green |

## 涉及文件

- `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-E-DEVOPS-L01.md`（本文件）
