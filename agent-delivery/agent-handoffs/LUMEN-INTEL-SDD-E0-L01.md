# Handoff — LUMEN-INTEL-SDD-E0-L01（E8 段 E：dev 发布验证）

- **执行**：agent:devops-agent（本会话）
- **监管人**：human:徐滕强
- **时间**：2026-11-05 23:43–23:59（UTC+8）
- **性质**：只核对与触发，未改任何业务代码；无 commit / 无 push
- **ponytail**: off（devops 核对单，无代码产出）

## 1. 范围与实现

对 2026-11-05 晚 E8-综合智能分析 8 张 coding 单执行 C1 发布门验证：GitLab CI 点名 deploy 绿 → K8s dev rollout + 镜像 tag → 发布 URL 核验。工具路径：GitLab MCP（project_id：algo-py=8 / svc=23 / ui-topic=17）+ 跳板机 zphz-jump kubectl（kubeconfig 副本 /tmp 用后即删，未带出）。

## 2. CI pipeline 状态（commit → 结果）

### lumen-algo-py（分支 dev，deploy 阶段 job = deploy:api / deploy:worker / deploy:entan-api）

| commit | pipeline | py:test | image:* | deploy:* | e2e:chain-gold |
|---|---|---|---|---|---|
| e8565a9（ELEM DDL+seed） | 3931 | ✅ | ✅×6 | ✅ api/worker/entan-api（innov、entan-worker=manual 设计态） | ❌ |
| 6bab0ed（ELEM 装包） | 3949 | ✅ | ✅×6 | ✅×3 | ❌ |
| b778c07（COLLAB DDL） | 3955 | ✅ | ✅×6 | ✅×3 | ❌ |
| 429f516（COLLAB 装包） | 3966 | ✅ | ✅×6 | ✅×3 | ❌ |
| 13906c3d / 828315a4（他人后续单） | 3969 等 | ✅ | ✅ | ✅ | ❌ |

**结论**：本轮 4 单 deploy 全绿；dev 头部已被推进到 828315a4（22:42 他人 commit），K8s 当前跑的即 828315a4 镜像。

### lumen-svc-platform

| commit | pipeline | build/lint/image | deploy（点名） |
|---|---|---|---|
| 0fdc245（VIT-FP） | 3947 | ✅ | ✅ topic-chain / topic-async-service / 其余 7 个 deploy 全绿 |
| 14e3fd2（ELEM-BE） | 3964 | ✅ | ✅ topic-chain / topic-async-service；**❌ deploy:display（非本单部署物）** |
| 084b2d1（COLLAB-GRAPH） | 3968 | ✅ | ✅ topic-chain / topic-async-service / deploy:element 等，**无红项** |
| 9dfeba0d（23:06 他人 display 修复） | 3972 | display image ✅（其余 image 被 newer pipeline cancel，正常） | ✅ deploy:display；其余 deploy:skipped（only-changes 设计） |

**deploy:display 红项闭环**：3964 时段红，根因 = 同仓他人 `cbd6f10e`（科学技术全景读图）双构造器致 Spring 找无参构造、gkxlumen-display 新镜像起不来、流量留旧 Pod；23:06 `9dfeba0d` 指定注入构造器修复，deploy:display 绿（3972），display pod 23:10 起 Running 1/1。**与本轮 3 单无因果关系。**

### lumen-ui-topic（deploy 阶段 job = deploy:k8s）

| commit | pipeline | build | image | deploy:k8s |
|---|---|---|---|---|
| efaee24（ELEM-FE） | 3971 | ✅ | ✅ | ✅ |
| 4d0a24d（COLLAB-FE） | 3978 | ✅ | ✅ | ✅ |

## 3. K8s dev rollout + 镜像版本（ns=zhipu-tts，全部 successfully rolled out）

| 点名 deployment | pod 状态 | 镜像 tag | 与本轮对应 |
|---|---|---|---|
| lumen-platform-algo-py（api） | 1/1 Running（22:44 起） | `gkx-lumen-algo-py-api:828315a4` | 含本轮 4 commit ✅ |
| lumen-platform-algo-py-worker | 1/1 Running | `gkx-lumen-algo-py-worker:828315a4` | 含本轮 4 commit ✅ |
| gkxlumen-platform-entan-py | 1/1 Running | `gkxlumen-entan-py-api:828315a4` | 同上 ✅ |
| gkxlumen-platform-entan-py-worker | 1/1 Running | `gkxlumen-entan-py-worker:13906c3d` | 22:26 修订单 ✅ |
| gkxlumen-platform-topic-chain | 1/1 Running（22:43 起） | `gkxlumen-topic:…`（image job tag 本轮 0fdc245/14e3fd2/084b2d1） | 含本轮 3 commit ✅ |
| gkxlumen-platform-topic-async-service | 1/1 Running（22:45 起） | `gkxlumen-topic-async-service:084b2d15` | = COLLAB-GRAPH commit ✅ |
| gkx-lumen-topic（前端静态） | 1/1 Running（23:54 起，pod 5m13s） | `gkx-lumen-topic:4d0a24db` | = COLLAB-FE commit ✅ |
| gkxlumen-platform-display（非点名，关联核验） | 1/1 Running（23:10 起） | 修复版 9dfeba0d | 红项已闭环 ✅ |

**说明**：`gkxlumen-platform-topic` deployment spec 镜像 tag 为 `latest`、pod 已 5 天未滚动；该 deployment 不在本轮 CI 的 deploy job 清单内（本轮 Java deploy 只含 topic-chain / topic-async-service / topic-enterprise / topic-svc / topic-policy / innov / display / element / cms），属存量部署方式，不计入本轮红项，仅记录供 coordinator 知悉。

## 4. 发布 URL 核验

| 目标 | 结果 |
|---|---|
| 前端 dev `http://10.50.69.111:30892/`（gkx-lumen-topic NodePort） | **200** ✅ |
| Java 网关 `http://10.50.69.111:30895/actuator/health`（gkxlumen-platform-gateway） | **200** ✅（`/` 404、`/admin/gateway/routes` 401 属网关设计行为，非故障） |
| Python lumen-algo-py in-cluster `/healthz`（svc 10.96.3.147:8000） | **200** ✅（`/health` 404 为路径命名差异，`/docs` 200 佐证 FastAPI 正常） |
| Python entan-py in-cluster `/healthz`（svc 10.96.3.124:8000） | **200** ✅ |

## 5. 红/黄项与分类

| # | 红黄项 | 分类 | 说明 |
|---|---|---|---|
| 1 | lumen-algo-py `e2e:chain-gold` 每条 pipeline 红（3931/3949/3955/3966/3969 连续 5 条，单条时长 ~0.2s 秒败） | **存量红，非本轮改动**（本仓本轮第一个 commit e8565a9 之前即已红） | 修单建议交 coordinator 派 qa-agent 抄 trace；job log 因 GitLab MCP 无日志工具、跳板机无 token（匿名 404）未取得，需有凭证方补抓 |
| 2 | lumen-svc-platform `deploy:display` 在 14e3fd2 pipeline（3964）红 | **他人单引入、当晚已闭环**：cbd6f10e 构造器问题 → 9dfeba0d 23:06 修复后绿 | 与本轮 3 单无关；无需派单 |
| 3 | lumen-ui-topic selfcheck 存量 intelL1b 红 | **存量**（4d0a24d commit message 自述与本单无关，前端自检非 CI 门） | 不影响本轮发布 |

## 6. 验收证据

- CI：GitLab pipelines 3931 / 3949 / 3955 / 3966（algo-py）、3947 / 3964 / 3968 / 3972（svc）、3971 / 3978（ui-topic）逐 job 状态见 §2；web_url 前缀 `https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/{repo}/-/pipelines/{id}`
- K8s：`kubectl rollout status` 7 个点名 deployment 全 `successfully rolled out`；镜像 tag 含今晚 commit（828315a4 / 084b2d15 / 4d0a24db）
- URL：§4 四项探测结果
- 收工：跳板机 `/tmp/admin-kc.yaml` 等副本已删（ls 确认不存在）

## 7. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 只核对不写业务代码 | ✅ 无代码改动 |
| kubectl 只在跳板机、kubeconfig 不带出 | ✅ 全程 SSH MCP，副本用后即删 |
| SSH 熔断规约 | ✅ 无探活；sudo 超时后改 nohup 短命令重试 1 次即过；GitLab 日志匿名 404 后即停未连试 |
| 长任务段 E（点名 deploy 绿 → e2e:chain-gold 复测） | ⚠️ deploy 全绿；e2e:chain-gold 存量红已登记分类（§5.1），按规约失败分类交 coordinator 派修 |
| commit 标注 | ✅ 不适用（本单无 commit） |

## 8. 待办移交

1. `e2e:chain-gold` 存量红 → coordinator 派 qa-agent 取 job log + trace 分诊（需 GitLab 凭证或 runner 侧排查）
2. `gkxlumen-platform-topic`（latest tag / 5 天未滚动）是否需纳入 CI deploy 体系 → 请 coordinator/architect 知悉裁决
