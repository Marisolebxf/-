# 旧 GitLab `dev` 同步方案

- 日期：2026-10-17
- 状态：方案已定，尚未执行（不 fetch、不合并、不推送）
- 对应键：origin 的**项目路径**（仓库名）。目录名只是检出位置，两边碰巧与路径一致

## 1. 做法

新组已用 GitLab 群组导入落过一版快照，导入之后两侧都有新提交。再导一次会盖掉新侧已经记在任务和 handoff 里的改动，也不能增量补旧站后来的提交。

同步用两份本地检出对 `dev`：

| | 旧站 | 新站 |
|---|---|---|
| 主机 | `https://gitlab.htmisoft.net/` | `https://aminer-edu-gitlab.jyzhang.cn/` |
| 组 | `gkx-lumen/<项目路径>.git` | `sz-gkx/gkx-lumen/<项目路径>.git` |
| 工作根 | `F:\gkx-lumen` | `E:\zhipu\gkx-lumen` |

在**新仓**把旧目录加成本地远程 `legacy`（指本地路径，不抄旧 origin URL），`fetch` 后对比 `origin/dev` 与 `legacy/dev`。只同步 `dev`。推送前先出对照表，人确认后再推 `origin/dev`。

`F:` 上单次 git 大约 1–2 分钟。20 个仓用一段脚本循环，把 ahead/behind 写成一张表。

旧仓作为来源之前，先确认它的 `dev` 等于旧站 `origin/dev`，且工作区干净。未提交的本地改动单独列出，不进这次合并。旧站若在截止点之后又有推送，先在 `F:` 上 `fetch`，再把新的 `dev` 当作截止点。

## 2. 合并清单（20）

新侧检出都在 `E:\zhipu\gkx-lumen\repos\<项目路径>`，编排仓在 `E:\zhipu\gkx-lumen\gkx-orchestration`。旧侧除编排仓外都在 `F:\gkx-lumen\repos\<项目路径>`。

| 项目路径 | 旧目录 |
|---|---|
| `gkx-orchestration` | `F:\gkx-lumen\gkx-orchestration` |
| `demo-admin-ui` | `F:\gkx-lumen\repos\demo-admin-ui` |
| `demo-algo-ent-analysis` | `F:\gkx-lumen\repos\demo-algo-ent-analysis` |
| `demo-algo-science` | `F:\gkx-lumen\repos\demo-algo-science` |
| `demo-svc-platform` | `F:\gkx-lumen\repos\demo-svc-platform` |
| `demo-svc-topic-py` | `F:\gkx-lumen\repos\demo-svc-topic-py` |
| `demo-ui-gaoduanzhiku-view` | `F:\gkx-lumen\repos\demo-ui-gaoduanzhiku-view` |
| `demo-ui-gdzk` | `F:\gkx-lumen\repos\demo-ui-gdzk` |
| `demo-ui-science` | `F:\gkx-lumen\repos\demo-ui-science` |
| `demo-ui-system-test` | `F:\gkx-lumen\repos\demo-ui-system-test` |
| `demo-ui-topic` | `F:\gkx-lumen\repos\demo-ui-topic` |
| `lumen-algo-py` | `F:\gkx-lumen\repos\lumen-algo-py` |
| `lumen-etl-es-py` | `F:\gkx-lumen\repos\lumen-etl-es-py` |
| `lumen-svc-platform` | `F:\gkx-lumen\repos\lumen-svc-platform` |
| `lumen-topic-py` | `F:\gkx-lumen\repos\lumen-topic-py` |
| `lumen-ui-algo-apiview` | `F:\gkx-lumen\repos\lumen-ui-algo-apiview` |
| `lumen-ui-science-mobile` | `F:\gkx-lumen\repos\lumen-ui-science-mobile` |
| `lumen-ui-science-pc` | `F:\gkx-lumen\repos\lumen-ui-science-pc` |
| `lumen-ui-topic` | `F:\gkx-lumen\repos\lumen-ui-topic` |
| `lumen-ui-topic-mobile` | `F:\gkx-lumen\repos\lumen-ui-topic-mobile` |

`demo-svc-topic-py`、`lumen-etl-es-py`、`lumen-topic-py` 于 2026-10-17 在旧目录重新拉取，origin 项目路径与新侧一致，分支均为 `dev`。

`repo-registry.yaml` 里 `migration_map` 的 `status: empty` 等字段是导入前的登记，不作为这次对仓依据。

## 3. 不合并

| 路径 | 原因 |
|---|---|
| `jx-tech-topic/iticsci-tech-topic-backend` | 新侧单独范围，不从旧站并 |
| `jx-tech-topic/iticsci-tech-topic-frontend` | 同上 |
| `lumen-ui-admin` | 明确不合并 |
| `lumen-ui-gdzk` | 明确不合并 |

旧侧有 origin、这次不拉的：`dataease`、`lumen-algo-platform`、`lumen-ui-science-topic`。临时目录 `demo-algo-ent-analysis-tmp`（`SZCGKX/ent-analysis-demo`）、`_tmp_lumen_fronted_pc`（`SZCGKX/gkx_lumen_fronted_pc`）指向别的组，不在范围内。扫描时两边 `worktrees` 为空。

## 4. 编排仓已核实的分叉

写方案时编排仓两侧都对着各自的 `origin/dev`，旧侧工作区干净：

| | 提交 | 说明 |
|---|---|---|
| 旧 `F:\gkx-lumen\gkx-orchestration` | `5faacd78` | `chore(registry): sync from Feishu board watch`。这个对象不在新仓里 |
| 新 `E:\zhipu\gkx-lumen\gkx-orchestration` | `37662b5a` | 导入之后还有现网地址、Harbor、久新专题等提交 |

编排仓不能快进，作为第一个试点。新仓工作区里还有未提交的 Kafka 基线（`agent-delivery/architecture-baseline.md`）和 handoff（`E-PLATFORM-P0-KAFKA-RMQ-L01.md`）。同步前先 `stash` 或单独提交，避免和旧站合并混成一次提交。

## 5. 执行步骤

脚本：`scripts/sync-legacy-dev.ps1`（实现本节和第 6、10 节）。

```powershell
# 只对照，不改分支、不提交、不推送
powershell -File scripts/sync-legacy-dev.ps1

# 合并并锁回新侧文件，提交在 sync/legacy-20261017，不推送
powershell -File scripts/sync-legacy-dev.ps1 -Apply

# 结果表确认后，校验锁定路径再推到新站 dev
powershell -File scripts/sync-legacy-dev.ps1 -Push
```

`-Apply` 与 `-Push` 不能同一次执行。工作区不干净的仓会停止，避免把未提交文件带进合并。下面是脚本对每个仓做的事。`legacy` 已存在则核对它指向旧目录本地路径，不改成带令牌的 URL。

```powershell
git remote add legacy "F:\gkx-lumen\repos\<项目路径>"
git fetch legacy
git rev-list --left-right --count origin/dev...legacy/dev
git log --oneline origin/dev..legacy/dev
```

编排仓的旧路径是 `F:\gkx-lumen\gkx-orchestration`。

三种结果：

| `origin/dev...legacy/dev` | 处理 |
|---|---|
| 右侧为 0 | 旧 `dev` 没有新提交，跳过 |
| 左侧为 0，右侧大于 0 | 新 `dev` 是旧 `dev` 的祖先，快进合并 |
| 两侧都大于 0 | 从当前 `dev` 开 `sync/legacy-20261017`，按第 6 节合并并锁回新侧文件 |
| 没有共同祖先 | 停止。这个仓的历史对不上导入快照，不自动合并 |

没有共同祖先时不要加 `--allow-unrelated-histories`。全部仓的表确认之后，才把结果推到新站 `origin/dev`。

## 6. 新侧提交不被旧文件覆盖

`git merge-base origin/dev legacy/dev` 是导入快照。普通合并里，导入之后只有新侧改过的文件会保持新侧版本，Git 不会用旧文件整份替换它。

CI/CD 文件的风险在另一处：同一个文件两边都改过时，Git 按行块自动合并。`.gitlab-ci.yml`、Helm、`k8s` 经常合得上、不产生冲突标记，旧站的镜像名、变量和部署段会混进新站已经改过的文件。

因此分叉合并用下面的顺序，锁的是整文件，不做按行混合。

1. `git switch -c sync/legacy-20261017`
2. `git merge --no-commit --no-ff legacy/dev`（有冲突也继续，先不要提交）
3. 算出导入之后新 `dev` 改过的路径：`git diff --name-only <merge-base> origin/dev`
4. 这些路径从 `origin/dev` 整文件放回暂存区和工作区。新侧已删除的路径在合并后又出现时，从暂存区删掉
5. CI/CD 路径再整树放回一次，即使第 3 步没有列出它们：`.gitlab-ci.yml`、`k8s/`、`helm/`、`docker/`、名为 `Dockerfile` 或以 `Dockerfile` 开头的文件。目录以新 `dev` 的树为准，旧站在这些目录里新增的文件也删掉
6. 检查锁定路径相对 `origin/dev` 的 diff 为空。不为空则不提交
7. 提交说明写明：业务文件来自旧 `dev`；锁定路径与新 `origin/dev` 字节一致

第 3 步盖住导入之后的全部新提交（基线、handoff、Harbor 的 `d5543025`、现网地址等）。第 5 步盖住大量 CI/CD：新侧没改过的流水线文件也不接收旧站后续修改。旧站只改过 CI/CD 的提交会在结果表里记成「旧侧 CI 改动已按新侧整文件丢弃」，需要的话由人另开提交捡回，不进这次自动合并。

业务文件里、导入之后新侧没改过、且不在第 5 步目录中的，仍按旧 `dev` 合入。

## 7. 结果表（执行时填）

| 项目路径 | 旧 HEAD | 新 HEAD | 新侧领先 | 旧侧领先 | 处理 | 锁定路径 diff 是否为空 | 旧侧 CI 被整文件丢弃 |
|---|---|---|---|---|---|---|---|---|
| | | | | | 跳过 / 快进 / 合并 / 停止 | | |

## 8. 凭据

部分旧仓的 origin 把访问令牌写在 URL 里。`legacy` 只用本地目录，不把带令牌的 URL 写进新仓。令牌已出现在本机命令输出中，在旧 GitLab 上作废并更换。本文不记录令牌原文。

## 9. 新侧自导入快照以来改过的文件

2026-10-17 只读对比：`git fetch` 旧目录的 `dev`，`git diff --name-status <merge-base> origin/dev`。未合并、未推送。`ahead/behind` 是 `origin/dev...旧dev` 的左/右提交数（左=新侧独有，右=旧侧独有）。右为 0 的仓没有旧提交可合入。

`demo-admin-ui` 旧目录本地只有 `main`，对比用的是该目录的 `origin/dev`。其余仓用旧目录本地 `dev`。

工作区未提交、不在下表里：`E-PLATFORM-P0-KAFKA-RMQ-L01.md`、本方案文件。`architecture-baseline.md` 的已提交版本在编排仓清单中，未提交增量未计入。

| 项目路径 | 新侧独有提交 | 旧侧独有提交 | 新侧改动文件数 |
|---|---:|---:|---:|
| `gkx-orchestration` | 18 | 107 | 56 |
| `demo-admin-ui` | 7 | 0 | 3 |
| `demo-algo-ent-analysis` | 5 | 19 | 13 |
| `demo-algo-science` | 4 | 3 | 7 |
| `demo-svc-platform` | 21 | 0 | 31 |
| `demo-svc-topic-py` | 7 | 3 | 12 |
| `demo-ui-gaoduanzhiku-view` | 6 | 0 | 3 |
| `demo-ui-gdzk` | 5 | 0 | 4 |
| `demo-ui-science` | 7 | 0 | 4 |
| `demo-ui-system-test` | 7 | 1 | 3 |
| `demo-ui-topic` | 7 | 0 | 4 |
| `lumen-algo-py` | 6 | 17 | 13 |
| `lumen-etl-es-py` | 8 | 8 | 2 |
| `lumen-svc-platform` | 33 | 40 | 36 |
| `lumen-topic-py` | 6 | 13 | 12 |
| `lumen-ui-algo-apiview` | 7 | 24 | 3 |
| `lumen-ui-science-mobile` | 8 | 0 | 3 |
| `lumen-ui-science-pc` | 8 | 8 | 3 |
| `lumen-ui-topic` | 8 | 17 | 3 |
| `lumen-ui-topic-mobile` | 12 | 0 | 7 |

状态：`M` 修改，`A` 新增。

### gkx-orchestration

`M .gitlab-ci.yml`，以及：

- `M .cursor/rules/00-team-constitution.mdc`
- `M .cursor/rules/data.mdc`
- `M .env.example`
- `M CODEOWNERS`
- `M README.md`
- `A agent-delivery/agent-handoffs/thirdpart/JX-TOPIC-ARCH-ASBUILT-L01.md`
- `A agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-ENV-CUTOVER-L02.md`
- `A agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-TRSGRAPH-L01.md`
- `M agent-delivery/architecture-baseline.md`
- `M agent-delivery/cicd-pipeline.md`
- `M agent-delivery/data/GDF/GDF协作指南.md`
- `M agent-delivery/data/data-design/storage/CHAIN/stores/nebula/graph-chain.md`
- `M agent-delivery/data/data-design/storage/ENT/stores/nebula/graph-enterprise.md`
- `M agent-delivery/feishu/feishu-bitable.yaml`
- `M agent-delivery/feishu/feishu-user-story-board.yaml`
- `M agent-delivery/formal-docs-registry.yaml`
- `M agent-delivery/graph-engine.md`
- `M agent-delivery/paths.yaml`
- `M agent-delivery/repo-registry.yaml`
- `M agent-delivery/task-registry.yaml`
- `M agent-delivery/team-members.md`
- `M agent-delivery/team-onboarding.md`
- `M agent-delivery/team-roster.yaml`
- `M agent-delivery/智能体编排与派单手册.md`
- `M deploy/feishu-sync/Dockerfile`
- `M deploy/feishu-sync/README.md`
- `M deploy/feishu-sync/k8s/cronjob-coordinator-loop.yaml`
- `M deploy/feishu-sync/k8s/cronjob.yaml`
- `M deploy/feishu-sync/k8s/deployment.yaml`
- `M deploy/feishu-sync/k8s/ingress-path.yaml`
- `M deploy/feishu-sync/k8s/secret.example.yaml`
- `M deploy/feishu-sync/k8s/service.yaml`
- `M deploy/feishu-sync/setup-git-credentials.sh`
- `A deploy/observability/k8s/grafana.yaml`
- `A deploy/observability/k8s/loki.yaml`
- `A deploy/observability/k8s/otel-collector.yaml`
- `A deploy/observability/k8s/prometheus.yaml`
- `A deploy/observability/k8s/rustfs-buckets-job.yaml`
- `A deploy/observability/k8s/secret.example.yaml`
- `A deploy/observability/k8s/tempo.yaml`
- `M gkx-lumen.code-workspace`
- `M scripts/bootstrap.ps1`
- `M scripts/bootstrap.sh`
- `M scripts/gdf-author-path-guard.mjs`
- `M scripts/k8s-apply-feishu-sync-secret.sh`
- `M scripts/k8s-deploy-feishu-sync.sh`
- `M scripts/lib/board-task-status.mjs`
- `M scripts/lib/feishu-bitable-api.ps1`
- `M scripts/lib/load-env.ps1`
- `M scripts/lib/load-env.sh`
- `A scripts/mirror-library-images.sh`
- `M scripts/set-gitlab-default-branch-dev.ps1`
- `M workspaces/README.md`
- `M workspaces/fe-topic.code-workspace`
- `A 可观测环境-运维说明.md`

### 只有 CI / 镜像 / 部署清单

这些仓的新侧差异全部落在 `.gitlab-ci.yml`、`docker/`、`k8s/`、`Dockerfile`：

- `demo-admin-ui`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/admin-ui.yaml`
- `demo-ui-gaoduanzhiku-view`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/zhiku-view.yaml`
- `demo-ui-science`：`A .dockerignore`，`.gitlab-ci.yml`，`A docker/Dockerfile`，`A k8s/demo-ui-science.yaml`
- `demo-ui-system-test`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/demo-ui.yaml`
- `demo-ui-topic`：`A .dockerignore`，`.gitlab-ci.yml`，`A docker/Dockerfile`，`A k8s/demo-ui-topic.yaml`
- `lumen-etl-es-py`：`.gitlab-ci.yml`，`docker/Dockerfile`
- `lumen-ui-algo-apiview`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/lumen-algo-apiview.yaml`
- `lumen-ui-science-mobile`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/lumen-science-mobile.yaml`
- `lumen-ui-science-pc`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/lumen-pc.yaml`
- `lumen-ui-topic`：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/lumen-topic.yaml`

`demo-ui-gdzk` 多一个业务文件：`.gitlab-ci.yml`，`docker/Dockerfile`，`k8s/zhiku-view.yaml`，`M src/router/menu.ts`。

### demo-algo-ent-analysis

- `M .gitlab-ci.yml`
- `M conf/deploy/k8s/entan-api.yaml`
- `M conf/deploy/k8s/entan-worker.yaml`
- `M conf/settings.yaml`
- `M conf/settings_policy.yaml`
- `M deploy/k8s/entan-api.yaml`
- `M deploy/k8s/entan-worker.yaml`
- `M docker/Dockerfile`
- `M docker/Dockerfile.api`
- `M docker/Dockerfile.worker`
- `M entan/common/nebula.py`
- `M polan/common/config.py`
- `M polan/common/nebula.py`

### demo-algo-science

- `M .gitlab-ci.yml`
- `M chainan/graph/nebula_schema.py`
- `M conf/settings.yaml`
- `M deploy/k8s/innov-api.yaml`
- `M deploy/k8s/innov-worker.yaml`
- `M docker/Dockerfile`
- `M docker/Dockerfile.base`

### demo-svc-platform

`.gitlab-ci.yml`，`scripts/download-otel-agent.sh`，`scripts/k8s-deploy.sh`，`CLAUDE.md`，以及：

- `gkx-app-server/gkx-app-server-biz/Dockerfile`
- `gkx-auth/Dockerfile`
- `gkx-boot/Dockerfile`
- `gkx-demo-a/Dockerfile`
- `gkx-demo-b/gkx-demo-b-biz/Dockerfile`
- `gkx-flow/gkx-flow-biz/Dockerfile`
- `gkx-gateway/Dockerfile`
- `gkx-innov/Dockerfile`
- `gkx-register/Dockerfile`
- `gkx-upms/gkx-upms-biz/Dockerfile`
- `gkx-visual/gkx-codegen/Dockerfile`
- `gkx-visual/gkx-daemon-elastic-job/Dockerfile`
- `gkx-visual/gkx-daemon-quartz/Dockerfile`
- `gkx-visual/gkx-jimu-platform/Dockerfile`
- `gkx-visual/gkx-monitor/Dockerfile`
- `gkx-visual/gkx-mp-platform/Dockerfile`
- `gkx-visual/gkx-pay-platform/Dockerfile`
- `gkx-visual/gkx-report-platform/Dockerfile`
- `gkx-visual/gkx-xxl-job-admin/Dockerfile`
- `helm/gkx-platform/configs/gkx-gateway-dev.yml`
- `helm/gkx-platform/configs/gkx-upms-biz-dev.yml`
- `helm/gkx-platform/templates/_helpers.tpl`
- `helm/gkx-platform/templates/etl-es-py.yaml`
- `helm/gkx-platform/templates/microservices.yaml`
- `helm/gkx-platform/templates/nacos.yaml`
- `helm/gkx-platform/values-demo.yaml`
- `helm/gkx-platform/values.yaml`

### demo-svc-topic-py

- `M .env.example`
- `M .gitlab-ci.yml`
- `M conf/settings.yaml`
- `M docker/Dockerfile.ai`
- `M docker/Dockerfile.analytics`
- `M docker/Dockerfile.graph`
- `M docker/Dockerfile.search`
- `M docker/Dockerfile.worker`
- `M gkx_common/nebula.py`
- `M k8s/dev-ai-py.yaml`
- `M k8s/dev-search-py.yaml`
- `M k8s/dev-worker-py.yaml`

### lumen-algo-py

- `M .gitlab-ci.yml`
- `M conf/settings.yaml`
- `M docker/Dockerfile.api`
- `M docker/Dockerfile.entan-api`
- `M docker/Dockerfile.entan-worker`
- `M docker/Dockerfile.innov`
- `M docker/Dockerfile.worker`
- `M lumen_common/algorithms/chain/graph_project.py`
- `M vendor/entan-py/conf/settings.yaml`
- `M vendor/entan-py/conf/settings_policy.yaml`
- `M vendor/entan-py/entan/common/nebula.py`
- `M vendor/entan-py/polan/common/config.py`
- `M vendor/entan-py/polan/common/nebula.py`

### lumen-svc-platform

`.gitlab-ci.yml`，`CLAUDE.md`，`ENT-JAVA-ANALYSIS-ARTIFACT-Nacos配置.md`，`scripts/download-otel-agent.sh`，`scripts/k8s-deploy.sh`，以及：

- `gkxlumen-auth/Dockerfile`
- `gkxlumen-gateway/Dockerfile`
- `gkxlumen-innov/Dockerfile`
- `gkxlumen-innov/src/main/resources/application.yml`
- `gkxlumen-metrics/Dockerfile`
- `gkxlumen-metrics/src/main/resources/application.yml`
- `gkxlumen-register/src/main/resources/application.properties`
- `gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/Dockerfile`
- `gkxlumen-topic-chain/gkxlumen-topic-chain-biz/Dockerfile`
- `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/Dockerfile`
- `gkxlumen-topic-policy/gkxlumen-topic-policy-biz/Dockerfile`
- `gkxlumen-topic-svc/gkxlumen-topic-svc-biz/Dockerfile`
- `gkxlumen-topic/Dockerfile`
- `gkxlumen-upms/gkxlumen-upms-biz/Dockerfile`
- `gkxlumen-visual/gkxlumen-xxl-job-admin/src/main/resources/application.yml`
- `helm/gkxlumen-platform/DEPLOY-LUMEN.md`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-async-service-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-chain-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-enterprise-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-policy-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-svc-biz-dev.yml`
- `helm/gkxlumen-platform/configs/gkxlumen-upms-biz-dev.yml`
- `helm/gkxlumen-platform/templates/_helpers.tpl`
- `helm/gkxlumen-platform/templates/etl-es-py.yaml`
- `helm/gkxlumen-platform/templates/microservices.yaml`
- `helm/gkxlumen-platform/templates/mysql.yaml`
- `helm/gkxlumen-platform/templates/nacos.yaml`
- `helm/gkxlumen-platform/templates/redis.yaml`
- `helm/gkxlumen-platform/values-demo.yaml`
- `helm/gkxlumen-platform/values-lumen.yaml`
- `helm/gkxlumen-platform/values.yaml`

### lumen-topic-py

- `M .env.example`
- `M .gitlab-ci.yml`
- `M conf/settings.yaml`
- `M docker/Dockerfile.ai`
- `M docker/Dockerfile.analytics`
- `M docker/Dockerfile.graph`
- `M docker/Dockerfile.search`
- `M docker/Dockerfile.worker`
- `M gkx_common/nebula.py`
- `M k8s/dev-ai-py.yaml`
- `M k8s/dev-ai-worker.yaml`
- `M k8s/dev-search-py.yaml`

### lumen-ui-topic-mobile

- `M .gitlab-ci.yml`
- `M README.md`
- `M docker/Dockerfile`
- `M k8s/lumen-topic-mobile.yaml`
- `M scripts/breakpoints.test.mjs`
- `M src/utils/analysisFingerprint.ts`
- `M src/utils/evalResultMap.ts`

## 10. 验收标准

同步完成以本节为准。任一款不满足，该仓不推 `origin/dev`。锁定路径的对照提交是 2026-10-17 只读对比时的新侧 `origin/dev`（下表）。同步前若该分支又有新提交，先重跑第 9 节的 diff，用新的 SHA 替换下表后再验收。

| 项目路径 | 锁定对照 SHA |
|---|---|
| `gkx-orchestration` | `37662b5a8133ff836fa0dcc6b00fc52c075a3677` |
| `demo-admin-ui` | `c7415988fe4d8513787666a578a97c3cb909b9d2` |
| `demo-algo-ent-analysis` | `97a36a7343fab586dbed4097fbe4d958d65bcb93` |
| `demo-algo-science` | `9e1aca7d5be91c1ae465b871a0d1b172d35f1e2d` |
| `demo-svc-platform` | `d835c4cdb6b4898e8c79f4f31b459a04b381d1c2` |
| `demo-svc-topic-py` | `a7f279226cb770050ac5ab3bf920518208da5b1b` |
| `demo-ui-gaoduanzhiku-view` | `e54edd8980fbcca543fa72d0ccb72e8b728486b8` |
| `demo-ui-gdzk` | `ce4943f02159bd28a789a8d0771a43bd633fd80d` |
| `demo-ui-science` | `165bf45d4396d322e4a395db180ba0b957b38413` |
| `demo-ui-system-test` | `fef7e6c31bbf2aeb57c2bef3ba29b5e6a2413ffb` |
| `demo-ui-topic` | `9e4cb04f3a3ffd55a30a673c5cfaecacf7e5ee0e` |
| `lumen-algo-py` | `2c7382e9365e4e4f8d48434eae49ec0288161b09` |
| `lumen-etl-es-py` | `303a30bf66a0ebd5a2dab5d6b1c9368aeb6b51d4` |
| `lumen-svc-platform` | `81c9a093be72505b360925297b6a41b09761dadc` |
| `lumen-topic-py` | `0b1309fa6a5b2282c606a5baad96912c4f550077` |
| `lumen-ui-algo-apiview` | `d47f81a143f3311269a7ee1aa450618554d2c954` |
| `lumen-ui-science-mobile` | `7c4aa72250052518c6022c9ed1addf57ec4a4689` |
| `lumen-ui-science-pc` | `bd87526a7bdb769eae7b1dd6550cacdcecde054d` |
| `lumen-ui-topic` | `dfb23e6fa0dc69f554de0d9a66fcbb32fc8f89c7` |
| `lumen-ui-topic-mobile` | `63e192b31af375e7714a73fcc58a2dc9271d369e` |

### 10.1 范围

- 第 2 节 20 个仓都有第 7 节结果表的一行，处理取值为「跳过」「快进」「合并」「停止」之一。
- `lumen-ui-admin`、`lumen-ui-gdzk`、`jx-tech-topic/iticsci-tech-topic-backend`、`jx-tech-topic/iticsci-tech-topic-frontend` 的 `origin/dev` 与同步前一致，没有 `sync/legacy-20261017`，没有从旧目录取过来的合并提交。
- 旧侧的 `dataease`、`lumen-algo-platform`、`lumen-ui-science-topic`、`demo-algo-ent-analysis-tmp`、`_tmp_lumen_fronted_pc` 不进入新仓合并。
- 没有使用 `--allow-unrelated-histories`。没有共同祖先的仓处理为「停止」，`dev` 停在对照 SHA。

### 10.2 新侧文件不被覆盖

对每一个处理为「合并」或「快进」的仓，用锁定对照 SHA（下称 `$base`）核对。CI/CD 整树这条必须无输出且退出码为 0：

```powershell
git diff --exit-code $base HEAD -- .gitlab-ci.yml k8s helm docker
git diff --exit-code $base HEAD -- $(git ls-files '*Dockerfile*')
```

第 9 节（或重跑后的新清单）里的每个路径再比 blob。两个命令输出的 SHA 必须相同：

```powershell
git rev-parse "${base}:<路径>"
git rev-parse "HEAD:<路径>"
```

对照 SHA 中已删除的路径，`git cat-file -e "HEAD:<路径>"` 必须失败。

同时满足：
- `.gitlab-ci.yml`、`k8s/`、`helm/`、`docker/`、`Dockerfile` 与 `Dockerfile*` 的整树与对照 SHA 一致。这四类目录中，旧站多出来的文件不在 `HEAD` 里。
- 编排仓至少包括：`.gitlab-ci.yml`、`agent-delivery/architecture-baseline.md`、`agent-delivery/cicd-pipeline.md`、`deploy/feishu-sync/`、`deploy/observability/k8s/`、`scripts/mirror-library-images.sh`、`可观测环境-运维说明.md`，blob 与 `37662b5a` 相同。
- 旧站只改过上述锁定路径的内容记在第 7 节「旧侧 CI 被整文件丢弃」，不出现在合并结果里。

处理为「跳过」的仓（2026-10-17 对比里旧侧独有提交为 0）：`origin/dev` 仍等于锁定对照 SHA。

### 10.3 旧侧业务提交进得来

处理为「合并」的仓，`git merge-base --is-ancestor <旧 dev SHA> HEAD` 退出码为 0。旧 `dev` 相对对照 SHA 改过、且不在第 10.2 锁定集合里的文件，内容与旧 `dev` 一致。

处理为「快进」的仓，`HEAD` 等于旧 `dev`，同时仍满足第 10.2。若快进后锁定路径不再等于对照 SHA，改为第 6 节的分叉合并，不保留这次快进。

### 10.4 提交与工作区

- 合并提交在 `sync/legacy-20261017` 上，提交说明写明业务文件来自旧 `dev`，锁定路径与新侧对照 SHA 字节一致。
- 该提交不包含同步前的未提交文件：`E-PLATFORM-P0-KAFKA-RMQ-L01.md`、本方案、以及 `architecture-baseline.md` 相对 `37662b5a` 的未提交增量。
- 新仓 `.git/config` 的远程 URL 不包含访问令牌。`legacy` 指向 `F:\gkx-lumen\...` 本地目录。

### 10.5 推送

- 第 7 节 20 行填满，且每一行「锁定路径 diff 是否为空」为「是」（「停止」行除外，该行 `dev` 未移动）。
- 人确认结果表之后，只推 `sync/legacy-20261017` 到新站对应仓的 `dev`。
- 推送后新站 `origin/dev` 等于本地 `HEAD`，再跑一次第 10.2 的 blob 对照，结果与推送前相同。

## 11. 迁移完成后仍要做的事

第 10 节通过并推到新站 `dev`，只表示旧 `dev` 的业务提交已进入新仓，且第 9 节的新侧文件仍在。下面这些不在本次同步的完成定义里，状态以 2026-10-17 登记为准。

### 11.1 同步提交之外的本地文件

这些文件不进 `sync/legacy-20261017`。推送完成后在新 `dev` 上另开提交：

- `agent-delivery/architecture-baseline.md` 相对 `37662b5a` 的未提交增量（Kafka / D13）
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-KAFKA-RMQ-L01.md`
- 本方案 `GITLAB-HTMISOFT-DEV-SYNC.md`

### 11.2 旧站收口

- 作废写在旧 origin URL 里的访问令牌并更换。新仓远程 URL 里不出现该令牌（第 10.4）。
- 这 20 个仓的旧 `dev` 停止再推。截止点之后若旧站又有提交，按第 1 节重新 fetch，再走第 6 节，不在已推送的同步提交上改历史。
- `dataease`、`lumen-algo-platform`、`lumen-ui-science-topic` 和两个临时目录本次不迁。是否归档沿用既有 M6 条件，不在本次同步里做。

### 11.3 流水线

推送后在新 GitLab 上看这 12 个旧侧有独有提交的仓：`gkx-orchestration`、`demo-algo-ent-analysis`、`demo-algo-science`、`demo-svc-topic-py`、`demo-ui-system-test`、`lumen-algo-py`、`lumen-etl-es-py`、`lumen-svc-platform`、`lumen-topic-py`、`lumen-ui-algo-apiview`、`lumen-ui-science-pc`、`lumen-ui-topic`。`dev` 流水线按新侧已锁定的 `.gitlab-ci.yml` 跑。第 10.2 只证明文件字节还在，不代替流水线结果。

第 7 节「旧侧 CI 被整文件丢弃」非空时，由人决定要不要把旧站流水线改动重新做成新侧提交。不自动捡回。

旧侧独有提交为 0、处理为「跳过」的 8 个仓（`demo-admin-ui`、`demo-svc-platform`、`demo-ui-gaoduanzhiku-view`、`demo-ui-gdzk`、`demo-ui-science`、`demo-ui-topic`、`lumen-ui-science-mobile`、`lumen-ui-topic-mobile`）同步后 `dev` 不动，不必为这次同步再跑流水线。

### 11.4 仍开着、且本次同步不改状态的任务

| 任务 | 状态 | 同步完成后仍要做的事 |
|---|---|---|
| `E-PLATFORM-P0-KAFKA-RMQ-L01` | integration | 架构记录已在基线。图 `ARCH-MSG-KAFKA` 仍是 draft。运行时仍是 RabbitMQ |
| `E-PLATFORM-P0-KAFKA-ALGO-L01` | ready | AI 与 Worker 改 Kafka 客户端。尚未开工 |
| `E-PLATFORM-P0-KAFKA-API-L01` | ready | 确认 Java 不接消息总线。尚未开工 |
| `E-PLATFORM-P0-KAFKA-DEVOPS-L01` | backlog | 等 ALGO 之后改 Helm / topic，去掉 RabbitMQ |
| `E-PLATFORM-P0-TRSGRAPH-L01` | in_progress | graphd 切到新库，只重灌 `demo_gkx_chain`。与这次 git 同步分开 |

`lumen-ui-admin`、`lumen-ui-gdzk`、`jx-tech-topic` 两个仓不在本次合并里，它们自己的后续开发不由本方案推进。
