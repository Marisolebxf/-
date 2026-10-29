# E-PLATFORM-P0-ENV-CUTOVER-L02 · 新集群发布入口收口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 派单原写监管人辜少彬，执行中改为淮政玮。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改发布入口、组变量和运维说明里的地址。没有重装可观测，没有改 `nebula_graphd`，没有做 TRSGraph。 |

## 问题清单

- 新 GitLab 组变量原先缺 `HARBOR_REGISTRY` / `HARBOR_PROJECT`；`KUBECONFIG_B64` 已在，但文档仍写「须重配」。
- 飞书 CI 的 node 基础镜像在 `zp-tts/node`，搬运脚本清单只覆盖 `library`。
- 前端 `environment.url` 仍指向 `10.50.69.111`。
- 作业 11554 是旧提交，不能重试。

## 修改内容

- 组 `sz-gkx/gkx-lumen`（id 74）已有 `HARBOR_USERNAME`、`HARBOR_PASSWORD`、`KUBECONFIG_B64`。本次补了非密钥变量 `HARBOR_REGISTRY=10.50.62.9:30303`、`HARBOR_PROJECT=zp-tts`。kubeconfig 的 server 是 `https://10.50.192.46:6443`，不含 `10.50.69.111`。口令只在 GitLab。
- Harbor 上 `library` 已有 python 3.11、nginx 1.27-alpine、maven 3.9.6-eclipse-temurin-17、python-algo-base 3.11、trivy 0.50.0、helm-kubectl 3.15.4、trivy-db 2。`library/node` 不存在。`zp-tts/node:22.12.0-alpine` 清单 HTTP 200，digest `sha256:5352667a8ab72b3000ce0f1cd622741e996506d0076a16d18e2d3b6aac4bf6da`。脚本改成与飞书 CI 同一侧，不把 node 再送进 library。
- 前端仓 `.gitlab-ci.yml` 的发布地址改为新节点 NodePort。kubeconfig 注释改为 API `10.50.192.46`。`paths.yaml` 的 `pc_frontend` / `topic_frontend` 与 `cicd-pipeline.md` §2、§3 已回写。
- 收口之后按同一方式把前端拉起来，见下文「前端 NodePort」。`demo-ui-science`、`demo-ui-topic` 已去掉 SSH 到 `192.168.88.63`，改成镜像加 NodePort。
- rustfs：集群内 `http://rustfs.zhipu-tts.svc.cluster.local:9000`，集群外 API `http://10.50.62.9:31390`，控制台 `http://10.50.62.9:31391/rustfs/console/`。账号在集群 Secret，不进 git。`demo-platform-tempo` / `demo-platform-loki` 的 `MINIO_ENDPOINT` 已是集群内地址。
- 合并保留清单拆成独立任务 `E-PLATFORM-P0-GITLAB-MERGE-FREEZE-L01`（backlog），本单未做。

## 测试结果

- Verdaccio `http://192.168.88.35:4873` 返回 HTTP 200，可达，不阻塞。
- 流水线：`demo-svc-platform` pipeline `2395`，提交 `4aa1b007`，job `helm:deploy` `11574` 成功。Runner tag `gkx`（runner `gkx-lumen`，id 1）。没有重试作业 11554。
  - https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-svc-platform/-/pipelines/2395
  - https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-svc-platform/-/jobs/11574
- 命名空间 `zhipu-tts` 就绪副本：
  - `demo-platform-tempo` `10.50.62.9:30303/library/tempo:2.7.1` 1/1
  - `demo-platform-loki` `10.50.62.9:30303/library/loki:3.5.0` 1/1
  - `demo-platform-upms` `10.50.62.9:30303/zp-tts/gkx-upms:4aa1b007` 1/1
  - `gkx-feishu-sync` `10.50.62.9:30303/zp-tts/gkx-feishu-sync:ba01d766` 1/1
- 可观测冒烟（未重装）：向 `gkx-otel-collector:4318/v1/traces` 打入 traceId `5b8aa5a2d2c872e8321cf37308d69df2`，Collector 返回 `{"partialSuccess":{}}`。Tempo `http://10.50.62.9:30201/api/traces/5b8aa5a2d2c872e8321cf37308d69df2` 返回 `service.name=ops-smoke`、span 名 `ops-smoke`。临时 Pod `ops-smoke-l02` 已删除。
- 前端页面实测见「前端 NodePort」。当时流水线里的 `deploy:k8s` 在 `docker run` 内容器里访问 `10.50.192.46:6443` 报 `network is unreachable`，所以已有镜像的前端是直接 apply 到 `zhipu-tts` 的。`demo-ui-science` / `demo-ui-topic` 的 deploy 作业已加上 `--network host`，这两次部署成功。

## 遗留风险

- Kafka 资源还在协调。`values-demo.yaml` 里 workerPy 已关，RabbitMQ 地址仍留在 values，本单不改。
- 组变量 `GKX_GITLAB_TOKEN` 长度为 0。飞书同步镜像已在跑；下次要重新发布飞书同步时，须先在 GitLab 填这个变量，不要写进仓库。
- 正式前端 nginx 里的 `gkxlumen-platform-gateway` 在 `zhipu-tts` 不存在。集群里正在跑的 pc / topic / science-mobile ConfigMap 已改成运行时再解析，页面能开，`/api` 要等这个网关出现。对应 `k8s/*.yaml` 的同样改动还在本地，未提交；下次用 git 里的旧 yaml 重新 apply，nginx 会再次起不来。
- `lumen-ui-admin`、`demo-admin-ui` 的 vite 构建在 `@swc/core` 反序列化 `BlockStatement` 处失败，Harbor 没有镜像，没有 NodePort。
- `lumen-ui-topic-mobile` 类型检查已在 `ce861b8` 修好并推到 `origin/dev`。清单里的 NodePort `30900` 已被 `gpustack-system/rustfs-svc` 占用，`30890` 已被 `zhipu-portal/sso-bridge` 占用，这两个端口不能再分给前端。

## CI/CD（必填）

- 分支：`dev`
- commit：编排仓 `ed615050`；前端见下表
- pipeline URL / ID：`2395` / job `11574`（`4aa1b007` 的 `helm:deploy`，tag `gkx`）
- 部署 namespace / 镜像 tag：`zhipu-tts`；tempo `library/tempo:2.7.1`，upms `gkx-upms:4aa1b007`
- K8s rollout：成功（上述 Deployment ready 1/1）
- dev 测试 URL / 命令与结果：Tempo 查询见测试结果；Verdaccio HTTP 200。前端页面见下表，均为 `http://10.50.62.9:<nodePort>/` 返回 HTTP 200。

### 前端 NodePort（2026-10-16 补充）

从集群外打开。标题是当时首页 `<title>`。

| 项目 | 地址 | 标题 | 结果 |
|------|------|------|------|
| demo-ui-science | http://10.50.62.9:30887 | 科技发展态势 | 200。流水线 `2405`，`deploy:k8s` 成功，trivy 失败但不挡部署 |
| demo-ui-topic | http://10.50.62.9:30888 | 科技专题服务系统 | 200。流水线 `2406`，`deploy:k8s` 成功，trivy 失败但不挡部署。`/topic`、`/ops` 转到 `demo-platform-gateway:9999` |
| demo-ui-system-test | http://10.50.62.9:30889 | GKX 系统和算法 | 200 |
| lumen-ui-science-pc | http://10.50.62.9:30891 | 深圳国际科技信息展示系统 | 200 |
| lumen-ui-topic | http://10.50.62.9:30892 | 深圳国际科技专题服务系统 | 200 |
| lumen-ui-algo-apiview | http://10.50.62.9:30897 | 科技专题服务算法库 | 200 |
| lumen-ui-science-mobile | http://10.50.62.9:30898 | 科技信息展示系统 | 200 |

`demo-ui-science` 流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-ui-science/-/pipelines/2405  
`demo-ui-topic` 流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-ui-topic/-/pipelines/2406

| 仓 | 补充 commit |
|----|-------------|
| gkx-orchestration | `93abe04c`（`cicd-pipeline.md` 记下 30887 / 30888） |
| demo-ui-science | `be33a81` |
| demo-ui-topic | `e43617e` |
| lumen-ui-topic-mobile | `ce861b8`（类型检查；NodePort 30900 不能用，见遗留风险） |

发布入口改地址时的 commit：

| 仓 | commit |
|----|--------|
| gkx-orchestration | `ed615050` |
| lumen-ui-science-pc | `2957aed` |
| lumen-ui-topic | `1bb56a6` |
| lumen-ui-science-mobile | `ffe6b2e` |
| lumen-ui-admin | `7f601a0` |
| lumen-ui-topic-mobile | `3a1d3c8` |
| demo-admin-ui | `465b046` |
| lumen-ui-algo-apiview | `6704818` |
| demo-ui-system-test | `1e0ec2e` |

## 可观测性（建议）

- OTEL_SERVICE_NAME：`ops-smoke`
- traceId（dev 抽样）：`5b8aa5a2d2c872e8321cf37308d69df2`
- Tempo / Loki：Tempo 有这条 span。Loki 未按这条冒烟检索。

## 涉及文件

- `agent-delivery/cicd-pipeline.md`
- `agent-delivery/paths.yaml`
- `agent-delivery/repo-registry.yaml`（仅 `dev_url`）
- `scripts/mirror-library-images.sh`
- `可观测环境-运维说明.md`
- 上表前端仓 `.gitlab-ci.yml`
- `demo-ui-science`、`demo-ui-topic` 的 `docker/Dockerfile`、`k8s/*.yaml`、`.gitlab-ci.yml`（SSH 部署改为 NodePort）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 前端 → Java REST → Python `/internal/*` | ✅ 未改调用链 |
| 算法只在 Python | ✅ 未在 Java 写算法 |
| 图谱 Nebula，不改 `nebula_graphd` | ✅ 运行时地址未改，未做 TRSGraph |
| 可观测走已有 Collector，OTLP HTTP `:4318` | ✅ 只打了一条冒烟，未重装 |
| 不切 MySQL / ES，不接 Jenkins，不改历史 pipeline URL | ✅ |
| 口令不进 git | ✅ rustfs / Harbor / kubeconfig 均未入库 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000 |
| model_used | grok-4.7 |
| actual_cost | 0.86 |
| cost_warn | green |

口径：无 Console 精确 in/out，按会话估算 160000，用预算表 B 档（输入 $3/M、输出 $15/M）和 80/20 比例计算。`source: session_estimate`。

## 2026-10-16 现网地址与登录（补充）

任务仍是 `ready_to_sign`。下面是当天排障已经推到 `origin/dev` 的关键事实，口令不写入本文。

### 登录

trace `a4281f358b9cceb932d9d9a48ba5d6c9`：网关全局过滤器已经去掉第一段路径，`gkx-auth` 路由上再配 `StripPrefix=1`，`/auth/oauth2/token` 变成 `/token`，认证返回 404。线上 Nacos 两个租户都已去掉这条 `StripPrefix`，网关已滚动。chart 提交 `demo-svc-platform` `8220c61`。登录已由人验证通过。`nacosConfigInit.runOnUpgrade=false`，之后的 helm 升级不会重写这份线上配置，除非设置 `FORCE_NACOS_REPUBLISH=true`。

### 现网地址（chart / bootstrap）

| 项 | 地址 |
|----|------|
| MySQL | `10.50.11.76:3306` |
| Redis | `10.50.62.9:31379`（demo 库 6，lumen 库 7） |
| Elasticsearch | `http://10.50.11.76:9200`，用户 `elastic` |
| 对象存储 | 集群内 `rustfs-svc.gpustack-system.svc.cluster.local:9000`；节点端口 `10.50.69.111:30900` |
| Grafana | `http://10.50.69.111:31300` |
| Milvus | `http://10.50.75.136:31594`，用户 `chatbi`；Python 只读 `MILVUS_URI` 与 `MILVUS_TOKEN`（`用户名:密码`） |

Kafka 仍不接线。

### 已推送提交

| 仓 | commit | 内容 |
|----|--------|------|
| demo-svc-platform | `8220c61` | 去掉 `gkx-auth` 多余的 `StripPrefix` |
| demo-svc-topic-py | `ec1bd22` | search 的 ES / MySQL 改到 `10.50.11.76` |
| demo-svc-topic-py | `a7f2792` | ai / worker 的 MySQL 与 rustfs；密钥走 `gkx-platform-minio` |
| lumen-svc-platform | `4fdbdab` | 去掉旧机房地址；MySQL / Redis / ES 改到现网；helm status 不再被 SIGPIPE 打断 |
| lumen-svc-platform | `14a204a` | `grafanaUrl` 与 entan 的 Milvus |

### 不要重试的作业

- `demo-svc-topic-py` job `12260`（检出的是改地址之前的提交）
- `lumen-svc-platform` job `12173`（`helm:deploy`，提交 `c16a75b`，等待超时，release 记为 failed）、job `12261`（`helm:chart`，exit 141）

下一轮要用新流水线，不要点这些旧作业的 Retry。

### 仍未收口

- node02（`10.50.179.112`）的 22 端口拒绝，Harbor 证书没拷过去；调度到该节点的 Python 镜像会因证书校验失败拉不下来。
- demo 的 ai / worker 以及 `.env.example`、`conf/settings.yaml` 里，RabbitMQ 仍是旧地址 `10.50.11.76:5672`。CI 实际 apply 的 bootstrap 已不含这条旧 MySQL / ES。
- lumen 异步服务的对象存储端点在 Nacos 配置里。默认升级不重发配置，要让 rustfs 端点进线上 Nacos，须 `FORCE_NACOS_REPUBLISH=true`。`MYSQL_HOST` 由 Pod 环境变量覆盖，不依赖重发。
- lumen release 在 `12173` 失败后状态是 failed，要等 `14a204a` 的新 `helm:deploy` 才会再装。

## 2026-10-17 迁移改动文件

任务仍是 `ready_to_sign`。下面是迁移里改过、并已在各仓 `origin/dev` 的文件。口令不写入本文。编排仓与前端发布入口仍以上文「涉及文件」和前端 commit 表为准，这里补后端、算法和 demo 服务。

`lumen-svc-platform` `81c9a09` 起，连 `10.50.11.76` 的业务账号是 `gkxlumenx`，root 口令未改。Nacos 与 upms 已由作业 [13072](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/jobs/13072) 落到 `zhipu-tts`，upms 为 1/1 Running。

### lumen-svc-platform

范围 `a6aab7a..81c9a09`。

| 用途 | 文件 |
|------|------|
| 流水线、发布脚本 | `.gitlab-ci.yml`、`scripts/k8s-deploy.sh`、`scripts/download-otel-agent.sh` |
| 现网地址、镜像 tag、业务库账号 | `helm/gkxlumen-platform/values.yaml`、`helm/gkxlumen-platform/values-lumen.yaml`、`helm/gkxlumen-platform/DEPLOY-LUMEN.md` |
| 数据源与 Nacos 启动 | `helm/gkxlumen-platform/templates/_helpers.tpl`、`templates/nacos.yaml`、`templates/mysql.yaml`、`templates/redis.yaml`、`templates/microservices.yaml`、`templates/etl-es-py.yaml` |
| 配置库默认用户 | `helm/gkxlumen-platform/configs/gkxlumen-upms-biz-dev.yml`、`gkxlumen-topic-async-service-biz-dev.yml`、`gkxlumen-topic-chain-biz-dev.yml`、`gkxlumen-topic-enterprise-biz-dev.yml`、`gkxlumen-topic-policy-biz-dev.yml`、`gkxlumen-topic-svc-biz-dev.yml` |
| 源码里的默认用户 | `gkxlumen-innov/src/main/resources/application.yml`、`gkxlumen-metrics/src/main/resources/application.yml`、`gkxlumen-register/src/main/resources/application.properties`、`gkxlumen-visual/gkxlumen-xxl-job-admin/src/main/resources/application.yml` |
| Nacos 配置说明 | `ENT-JAVA-ANALYSIS-ARTIFACT-Nacos配置.md` |

`templates/` 路径均在 `helm/gkxlumen-platform/` 下。

### lumen-etl-es-py

范围 `d79e21f..303a30b`（Harbor、`zhipu-tts`、镜像 `:latest` 与 node01 导入）。

- `.gitlab-ci.yml`
- `docker/Dockerfile`

### lumen-algo-py

范围 `155a280..2c7382e`。

| 用途 | 文件 |
|------|------|
| 流水线与镜像 | `.gitlab-ci.yml`、`docker/Dockerfile.api`、`docker/Dockerfile.innov`、`docker/Dockerfile.worker`、`docker/Dockerfile.entan-api`、`docker/Dockerfile.entan-worker` |
| 图谱默认地址 | `conf/settings.yaml`、`lumen_common/algorithms/chain/graph_project.py`、`vendor/entan-py/conf/settings.yaml`、`vendor/entan-py/conf/settings_policy.yaml`、`vendor/entan-py/entan/common/nebula.py`、`vendor/entan-py/polan/common/config.py`、`vendor/entan-py/polan/common/nebula.py` |

### demo 服务

| 仓 | commit | 文件 |
|----|--------|------|
| demo-svc-platform | `8220c61` | `helm/gkx-platform/configs/gkx-gateway-dev.yml` |
| demo-svc-topic-py | `ec1bd22` | `k8s/dev-search-py.yaml` |
| demo-svc-topic-py | `a7f2792` | `k8s/dev-ai-py.yaml`、`k8s/dev-worker-py.yaml` |
