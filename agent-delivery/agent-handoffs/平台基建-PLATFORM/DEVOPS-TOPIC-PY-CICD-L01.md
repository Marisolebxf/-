# DEVOPS-TOPIC-PY-CICD-L01

> **文档性质**：coordinator → devops-agent **派单包**  
> **任务 ID**：`DEVOPS-TOPIC-PY-CICD-L01`  
> **执行角色**：devops-agent  
> **监管人（认领时必填）**：`supervised_by: human:{真名}`（建议：`human:淮政玮` 或平台运维负责人）  
> **性质**：工程交付（CI + 镜像 + K8s dev 热更新）  
> **状态**：`review`（devops 已交付；见 `DEVOPS-TOPIC-PY-CICD-L01-handoff.md`；待 coordinator 验收）  
> **日期**：2026-07-17  
> **作者**：`[agent:coordinator]`

---

## 0. 派单话术（粘贴新开会话）

```markdown
/goal devops-agent
身份：你是资深 DevOps/SRE，精通 GitLab CI、Docker、Helm/K8s、OTel 注入。
任务 ID：DEVOPS-TOPIC-PY-CICD-L01
性质：CI/CD + K8s 发布（非设计类）
仓库：
  - 主仓：repos/demo-svc-topic-py（dev）
  - 配套：repos/demo-svc-platform（helm/gkx-platform，创建 Deployment 供热更新）
  - 对照：repos/demo-algo-ent-analysis（.gitlab-ci.yml + docker/Dockerfile + deploy:entan-py）
目标：
  为 demo-svc-topic-py 已实现的 gkx-search-service 打通
  push → Pipeline 绿 → Harbor 镜像 → K8s dev rollout（热更新）。
范围（本 L01 冻结）：
  - ✅ 仅 gkx-search-service（docker/Dockerfile.search 已实现；/healthz 可用）
  - ❌ 不构建 Dockerfile.ai / analytics / graph（源码未实现，标预留；另开后续 task）
必读（P0）：
  - 本文件
  - agent-delivery/cicd-pipeline.md
  - agent-delivery/observability.md
  - demo-algo-ent-analysis/.gitlab-ci.yml（模板真源）
  - demo-algo-ent-analysis/docker/Dockerfile（python-algo-base + opentelemetry-instrument）
  - demo-svc-platform/helm/gkx-platform/templates/entan-py.yaml + values.yaml#entanPy
  - demo-svc-topic-py/docker/Dockerfile.search、gkx_search_service/main.py
架构铁律：
  1. 算法只在 Python；本仓为 Python 内部服务
  2. 调用链：前端 → Java REST → Python /internal/*（本服务前缀 /internal/gkx-search/**）
  3. 图谱：NebulaGraph（若本服务用到）
  4. 可观测性：Python opentelemetry-instrument + OTEL_*；禁止无 OTel 裸跑上线
  5. CI/CD：dev 分支触发；镜像 tag=commit SHA（可附 latest 仅推送，部署禁用 latest 作为唯一依据）
  6. demo 仓允许 main/dev 直推策略以该仓约定为准；本任务在 demo-svc-topic-py 的 dev 交付
  7. Java 不直连 nGQL；本仓可按既有实现访问 ES/Nebula
  8. secret 不入 git（PG/ES 密码走 CI 变量或既有 K8s secret 模式，对齐 entanPy）
DoD：
  1. demo-svc-topic-py 新增 .gitlab-ci.yml：stages test→package→deploy；对照 ent-analysis
  2. Dockerfile.search 对齐对照仓：优先 python-algo-base:3.11 + ENTRYPOINT opentelemetry-instrument（若依赖冲突则文档说明并保留 slim，但须注入 OTEL env）
  3. 镜像 Harbor：harbor.htmisoft.net/gkx/gkx-search-service:{sha}
  4. demo-svc-platform helm 新增 search 服务 Deployment/Service（镜像 demo-platform-*-search 命名对齐 innov-py/entan-py）；values 可开关；探针 /healthz；resources 必填
  5. deploy job：kubectl set image 热更新；dev 默认 manual，FULL_PIPELINE=true 自动
  6. push dev → Pipeline 绿；handoff 附 pipeline URL + rollout 证据 + curl /healthz
  7. 更新 repo-registry / cicd-pipeline.md 现状表一行（可选同 PR 或 orchestration 回填）
  8. cost 四字段回填；handoff → review
不要问调度者实现细节；阻塞（无 KUBECONFIG / Harbor / Deployment 未建）立即 blocked 并写明。
```

---

## 1. 背景

| 项 | 现状 |
|----|------|
| 仓 | `demo-svc-topic-py`（已 clone，`dev` @ 本地最新） |
| 已实现服务 | **仅** `gkx_search_service`（FastAPI，`/healthz`，路由 `/internal/gkx-search/**`） |
| Dockerfile | `Dockerfile.search` 可用；`ai/analytics/graph` 注释写明「预留，服务未实现」 |
| CI | **无** `.gitlab-ci.yml` |
| K8s | `demo-svc-platform` helm **尚无** search 对应 Deployment（有 `innov-py` / `entan-py` 模板可抄） |

对照模式（`demo-algo-ent-analysis`）：

1. 本仓 CI：smoke → 构建推 Harbor → `kubectl set image` 热更新  
2. Deployment 由 `demo-svc-platform` helm 预先创建（`demo-platform-entan-py`）

---

## 2. 建议命名（派单冻结草案，devops 可微调但须 handoff 记录）

| 项 | 建议值 |
|----|--------|
| Harbor 镜像 | `harbor.htmisoft.net/gkx/gkx-search-service` |
| Helm component / SVC_KEY | `search-py`（或 `topic-search-py`） |
| K8s Deployment | `demo-platform-search-py`（随 `PLATFORM_K8S_PREFIX`） |
| 容器端口 | `8080`（与现 Dockerfile 一致） |
| NodePort（若暴露） | 建议 `30805`（避开 30800 entan / 30889+ 前端）；最终以集群未占用为准 |
| OTEL_SERVICE_NAME | `gkx-search-service` |

---

## 3. 依赖与风险

| 风险 | 缓解 |
|------|------|
| helm 未建 Deployment 则 deploy job 失败 | 本任务 DoD **包含** platform helm 模板；先 helm upgrade/apply 再 set image |
| 4 服务全做会红 | L01 **只做 search**；ai/analytics/graph 另开 `DEVOPS-TOPIC-PY-CICD-L02+` |
| Dockerfile 用官方 slim 无 OTel instrument | 对齐 entan：改 base 镜像或文档豁免 + env 注入 |
| ES/PG secret | 对齐 entanPy values 模式；禁止把新密钥写入 git |

`depends_on: []`（可独立开工；与 DATA-ENT-CMS 分区无代码依赖）。

---

## 4. coordinator 验收清单

- [ ] `.gitlab-ci.yml` 存在且 dev Pipeline 绿  
- [ ] Harbor 可见 `gkx-search-service:{sha}`  
- [ ] K8s `dev` ns 存在 Deployment 且 rollout 成功  
- [ ] `curl` `/healthz` 通过（ClusterIP 或 NodePort）  
- [ ] 未误构建未实现的 ai/analytics/graph  
- [ ] handoff + cost 四字段  

---

## 5. 修订记录

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v0.1 | 2026-07-17 | coordinator-agent | 建任务 + 派单包；范围锁定 search |
