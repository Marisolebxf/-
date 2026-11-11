# CI/CD 与 K8s 发布规范（Agent 强制执行）

> **铁律**：每个 leaf 任务完成 = 代码已 **push GitLab** + **Pipeline 绿** + **K8s dev 部署成功** + **冒烟/接口测试通过**。
> 仅本地改完不 push 视为 **未完成**。

---

## 1. 标准闭环（每个 Agent 必须走）

```mermaid
flowchart LR
  A[本地修改+自测] --> B[git commit]
  B --> C[git push 远程分支]
  C --> D[GitLab CI Pipeline]
  D --> E[Harbor 镜像]
  E --> F[K8s dev 滚动发布]
  F --> G[qa 冒烟/接口/E2E]
  G --> H[handoff + 更新 task-registry]
```

| 步骤 | 要求 |
|------|------|
| 分支 | 功能在 `dev` 或 `feat/{task-id}`；合并目标 `dev` → `main` |
| Commit | 消息含 task-id，如 `feat(E-INNOV-M1-L03): 移植 gkxlumen-innov` |
| Push | `git push -u origin <branch>`，禁止只留本地 |
| Pipeline | 等待 GitLab CI 全部 required job 通过（可用 `glab`/`curl` API 轮询） |
| Deploy | `main` 推 dev 命名空间；`release/*` → uat（manual）；tag → prod（manual） |
| 测试 | 对 **K8s 上运行的服务** 测，不只 localhost |

---

## 2. 基础设施（已存在）

| 项 | 值 |
|----|-----|
| GitLab | https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen |
| Harbor | harbor.test.com/zp-tts |
| Runner | tag=`gkx`，shell executor（10.50.69.111） |
| SonarQube | http://10.50.180.228:9005（源码质量；**不替代** Trivy 镜像扫） |
| K8s 集群 | 节点 `10.50.69.111`（`node01`）。API `https://apiserver.cluster.local:6443`（该机 hosts 指向 `10.103.97.2`，v1.28.15）。组变量 `KUBECONFIG_B64` 仍指向旧集群 `https://10.50.192.46:6443`，待 `L03-VARS` 更换 |
| dev 命名空间 | `zhipu-tts` |
| 前端 dev 访问 | http://10.50.69.111:30891（pc）、http://10.50.69.111:30892（topic）；原型 http://10.50.69.111:30887（demo-ui-science）、http://10.50.69.111:30888（demo-ui-topic） |

组级 CI 变量（sz-gkx/gkx-lumen，组 id 74）：`HARBOR_PROJECT`=`zp-tts`、`HARBOR_USERNAME`、`HARBOR_PASSWORD`、`KUBECONFIG_B64`、`SONAR_HOST_URL`、`SONAR_TOKEN`（**Masked + Protected**）。仓内默认与切换目标 `HARBOR_REGISTRY`=`harbor.test.com`；GitLab 上的组变量仍是 `10.50.62.9:30303`，要等 `E-PLATFORM-P0-ENV-CUTOVER-L03-VARS` 再改。口令 / Token 只在 GitLab，不进 git。

**Sonar 接入（DEVOPS-SONARQUBE-CI-L01）**：组内有 CI 的业务仓（全部 `lumen-*` / `demo-*` + `spring-boot-bridge`）在 `scan` stage 有 `sonar:scan`（`allow_failure: true`，与 trivy 同软门禁）。项目 key：lumen/bridge=`gkxlumen-*`，demo=`gkxdemo-*`。首版 Quality Gate=`GKX-Soft`（无条件软门，避免 coverage / new_violations 首版必挂）；首版用 Runner `$HOME/.cache/sonar-scanner` 缓存的 sonar-scanner-cli（linux-x64 自带 JRE）；相关仓 `dev` 已设为 protected branch，以便 Protected 变量注入。不含编排仓与 deletion_scheduled / gdzk 归档。

---

## 3. 各仓 CI/CD 现状

| 仓库 | .gitlab-ci.yml | 镜像名 | K8s 部署方式 | main→dev |
|------|----------------|--------|-------------|----------|
| `demo-algo-science` | ✅ | gkx-innov-py | helm innov-py 热更新 | manual deploy job |
| `demo-ui-system-test` / `demo-ui-system-test` | ✅ | gkx-demo-ui | 独立 Deployment NodePort 30889（`k8s/demo-ui.yaml`） | **自动** deploy:k8s |
| `demo-ui-science` | ✅ | gkx-demo-ui-science | 独立 Deployment NodePort 30887，http://10.50.69.111:30887 | **自动** deploy:k8s |
| `demo-ui-topic` | ✅ | gkx-demo-ui-topic | 独立 Deployment NodePort 30888，http://10.50.69.111:30888 | **自动** deploy:k8s |
| `lumen-ui-science-pc` | ✅ | gkx-lumen-pc | 独立 Deployment NodePort 30891，http://10.50.69.111:30891 | **自动** deploy:k8s |
| `lumen-ui-topic` / `lumen-ui-science-topic` | ✅ | gkx-lumen-topic | 独立 Deployment NodePort 30892，http://10.50.69.111:30892 | **自动** deploy:k8s |
| `lumen-algo-py` | ✅ | gkx-lumen-algo-py-api / -worker；innov/entan 独立制品 | k8s yaml + helm 热更新 | **api+worker+entan-api 路径命中时自动**（2026-08-14 / D12）；innov/entan-worker 仍 manual（`FULL_PIPELINE=true` 才自动）；**路径增量**见下「增量规则」 |
| `lumen-svc-platform` | ✅ | gkxlumen-*（含 topic-chain / topic-async-service） | helm gkxlumen-platform + 单服务 `set image` | **topic-chain + topic-async-service 自动**（2026-08-14）；`helm:deploy` / gateway / innov / topic 仍 manual |
| `demo-svc-platform` | ✅ | gkx-* 多服务 | helm gkx-platform（**不含前端**） | manual helm:deploy |
| `demo-algo-ent-analysis` / `demo-algo-ent-analysis` | ✅ | gkx-entan-py | helm entan-py 热更新 | manual deploy |
| `demo-svc-topic-py` | ✅ | gkx-search-service | helm searchPy + bootstrap `k8s/dev-search-py.yaml`；NodePort **30805** | manual `deploy:search-py`（FULL_PIPELINE 自动） |
| `lumen-etl-es-py` | ✅ | lumen-etl-es-py | helm etlEsPy + bootstrap `k8s/dev-etl-es-py.yaml`；NodePort **30806** | manual `deploy:etl-es-py`（FULL_PIPELINE 自动） |

**缺口**：`helm:deploy` 全平台仍 manual（有意）；topic-py 的 ai/analytics/graph 服务未实现，无 CI。

---

## 4. Pipeline 阶段（对齐 demo 仓）

### Java（lumen-svc-platform · CHAIN）

```
backend:build (mvn verify **仅 affected**；脚本 scripts/ci-affected-modules.sh)
  → package (backend:image:* **按路径增量**；未改服务 skip)
  → deploy:* 与 image 同门控（skip = 保持现网 digest，不伪标新 SHA）
  → deploy:topic-chain + deploy:topic-async-service  （改到才自动；tag=短 SHA + rollout = E0）
  → e2e:chain-gold（仅 chain/async 或共享扇出时；needs optional）
  → helm:deploy / gateway / …                     （dev 默认 manual；FULL_PIPELINE 自动）
```

#### 增量规则（DEVOPS-LUMEN-SVC-CI-SPEED-L01 · Phase A）

| 变更范围 | `backend:build` | 日常 image+deploy | 说明 |
|---------|-----------------|-------------------|------|
| 单服务目录（如 `gkxlumen-display/**`） | 只 `-pl` 该模块 `-am` | 仅该服务 | 其余服务 **skip**，现网镜像不动 |
| 共享扇出：`pom.xml` / `gkxlumen-common/**` / `.gitlab-ci.yml` / `scripts/ci-affected-modules.sh` / `scripts/download-otel-agent.sh` | 全量模块列表 | 全部日常常发 | 与 Nx affected / Maven reactor 扇出同语义 |
| 仅 helm/文档等非 Java | skip verify（空 `-pl`） | 日常 image 全 skip | 改 chart 仍点 `helm:chart` |
| `REBUILD_ALL=true` | 全量 verify | 全部日常常发 image+deploy | **逃生口**；不强制冷门 gateway/auth/… |
| `FULL_PIPELINE=true` | 全量 verify | 日常 + 冷门全开 | 完整发布；含 graph/datacatalog 等 |

**安全边界**：跳过 package 的服务禁止 deploy；deploy 仍校验本次 jar 的 `git.commit.id == CI_COMMIT_SHA`（仅对实际跑了 image 的服务）。topic-chain / topic-async-service 在 **自身或共享路径变更** 时仍 origin/dev 自动 deploy（长任务 C1 不变）。

**Phase B/C（未本单落地）**：api 模块细粒度扇出表；Maven Build Cache / BuildKit / 跨 job 传 class（注意 artifact 413）。

### Python（lumen-algo-py · CHAIN）

```
test (py:test 全量，保正确性)
  → package (image:* **按路径增量**；未改制品 skip)
  → deploy:* 与 image 同门控（skip = 保持现网 digest，不伪标新 SHA）
  → deploy:api + deploy:worker + deploy:entan-api  （改到才自动；tag=短 SHA + rollout + healthz = E0 / D12）
  → deploy:innov / entan-worker                   （路径命中 manual；FULL_PIPELINE 自动）
  → e2e:chain-gold / smoke:synth-routes           （仅上游 deploy 会跑时；needs optional）
```

#### 增量规则（DEVOPS-LUMEN-ALGO-CI-SPEED-L01 · Phase A）

| 变更范围 | image+deploy | 说明 |
|---------|--------------|------|
| `lumen_algo_service/**` / `docker/Dockerfile.api`（+ api 烘焙的 `vendor/innov-py/chainan`、`vendor/entan-py/polan`） | 仅 **api** | 其余 skip |
| `lumen_algo_worker/**` / `docker/Dockerfile.worker`（+ worker 烘焙的 polan） | 仅 **worker** | 其余 skip |
| `vendor/innov-py/**` / `docker/Dockerfile.innov` | **innov**（deploy 仍 manual，除非 `FULL_PIPELINE`） | |
| `vendor/entan-py/**` / entan Dockerfile | **entan-api** 自动 + **entan-worker** 镜像（deploy manual） | polan 变更另扇出 api+worker（Dockerfile 交叉 COPY） |
| 共享扇出：`lumen_common/**` / `requirements.txt` / `conf/**` / `.gitlab-ci.yml` / `scripts/ci-affected-paths.sh` | 日常自动 **api+worker+entan-api**（innov/entan-worker 镜像亦会因共享路径重建，deploy 仍 manual） | 与 Nx affected 同语义 |
| 仅文档/无关脚本 | 全部 image/deploy skip | `py:test` / `sonar:scan` 仍跑 |
| `REBUILD_ALL=true` | 日常自动三件套全开 | **逃生口**；不强制 innov/entan-worker |
| `FULL_PIPELINE=true` | 全部 image + innov/entan-worker 亦自动 deploy | 完整发布 |

本地对照：`bash scripts/ci-affected-paths.sh --self-check` / `--images` / `--daily`。

**安全边界**：跳过 package 的制品禁止 deploy；origin/dev 上 api+worker（及 D12 灌输的 entan-api）在 **自身或共享路径变更** 时仍自动 deploy（长任务 E0 不变）。`e2e:chain-gold` / `smoke:synth-routes` 用 `needs:optional` + 同 changes，避免 skip deploy 拖红整条 pipeline。

长任务 C1 循环：deploy job 绿后 **自动** `e2e:chain-gold`（只点已发布的前端；地址 `http://10.50.69.111:30892`）。`CHAIN_GOLD_ONLY=true` 跳过前端 build；`CHAIN_GOLD_GREP` 只复测失败故事。Python `deploy:api+worker`、Java `deploy:topic-chain+async-service` 绿后 **trigger** `sz-gkx/gkx-lumen/lumen-ui-topic`。目标仓须放行 inbound job token。禁止把全量 USM / 视觉回归塞进本 job。见 `长任务执行规约.md` §11.5.2。

### 前端（lumen-ui-science-pc）

```
build (npm run build) → package (frontend:image) → deploy (deploy:k8s → dev 自动)
```

---

## 5. Agent 派单附加指令（写入每个 /goal）

```
完成代码后必须：
1. git add / commit / push 到对应仓库远程分支
2. 等待 GitLab Pipeline 成功（附 pipeline URL 到 handoff）
3. 确认 K8s dev 滚动完成（kubectl rollout status 或 CI deploy job 绿）
4. 对 dev 环境执行本任务 DoD 中的测试项
5. handoff 填写：commit SHA、pipeline ID、部署 namespace、测试 URL/命令
```

---

## 6. K8s 测试入口（E-INNOV-M1）

| 被测服务 | dev 验证方式 |
|---------|-------------|
| Python innov-py | `/internal/status`；**Tempo** 中 `service.name` 对应 OTEL_SERVICE_NAME |
| Java gkxlumen-innov | 网关 `/innov/v1/*`；响应头 **traceparent** / **X-Trace-Id** |
| 前端 lumen-pc | :30891；错误拦截器输出 traceId + Grafana 深链（若已配 VITE_GRAFANA_*） |
| 前端 lumen-topic | :30892；占位首页 + observability 冒烟 |

可观测性规范见 `observability.md`。

---

## 7. 失败处理

| 情况 | 动作 |
|------|------|
| Pipeline 红 | agent 读 job log，修复后新 commit push，直到绿 |
| deploy job manual 未点 | **不适用于** `lumen-algo-py` api+worker+entan-api（路径命中时）、`lumen-svc-platform` topic-chain / topic-async-service（dev 已自动）。其它仍 manual 的 job：coordinator 在 GitLab 触发，或修单仓开 `FULL_PIPELINE` |
| K8s rollout 失败 | `kubectl describe pod` + 修镜像/配置 + 重跑 pipeline |
| 测试失败 | 开新 commit 修复，禁止标记 task done |

---

## 8. 禁止事项

- 禁止 `--no-verify` 跳过 hook（除非 hook 明确阻塞且 handoff 说明）
- 禁止 force push `main`/`dev`
- 禁止把 Harbor 密码、kubeconfig 写入代码库
- 禁止「本地验证通过」但不 push 就关 task

---

## 9. 环境、发布注意事项、Secret

流水线阶段以本文为准。环境地址、发布时怎么改密钥、集群 Secret 写在 [工程过程/部署.md](工程过程/部署.md)，不在本文再抄一份。
