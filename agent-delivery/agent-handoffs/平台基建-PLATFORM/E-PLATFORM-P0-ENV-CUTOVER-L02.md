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
- 前端 `environment.url` 仍指向 `192.168.88.50`。
- 作业 11554 是旧提交，不能重试。

## 修改内容

- 组 `sz-gkx/gkx-lumen`（id 74）已有 `HARBOR_USERNAME`、`HARBOR_PASSWORD`、`KUBECONFIG_B64`。本次补了非密钥变量 `HARBOR_REGISTRY=10.50.62.9:30303`、`HARBOR_PROJECT=zp-tts`。kubeconfig 的 server 是 `https://10.50.192.46:6443`，不含 `192.168.88.50`。口令只在 GitLab。
- Harbor 上 `library` 已有 python 3.11、nginx 1.27-alpine、maven 3.9.6-eclipse-temurin-17、python-algo-base 3.11、trivy 0.50.0、helm-kubectl 3.15.4、trivy-db 2。`library/node` 不存在。`zp-tts/node:22.12.0-alpine` 清单 HTTP 200，digest `sha256:5352667a8ab72b3000ce0f1cd622741e996506d0076a16d18e2d3b6aac4bf6da`。脚本改成与飞书 CI 同一侧，不把 node 再送进 library。
- 前端仓 `.gitlab-ci.yml` 的发布地址改为新节点 NodePort。kubeconfig 注释改为 API `10.50.192.46`。`paths.yaml` 的 `pc_frontend` / `topic_frontend` 与 `cicd-pipeline.md` §2、§3 已回写。`demo-ui-science`、`demo-ui-topic` 仍是 SSH 到 `192.168.88.63`，不是这条 NodePort 入口，未改。
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
- 本次集群清单里没有 `lumen-pc` / `lumen-topic` Service。`30891` / `30892` 来自各自 `k8s/*.yaml` 的固定 nodePort，页面要等对应 `deploy:k8s`。

## 遗留风险

- Kafka 资源还在协调。`values-demo.yaml` 里 workerPy 已关，RabbitMQ 地址仍留在 values，本单不改。
- 组变量 `GKX_GITLAB_TOKEN` 长度为 0。飞书同步镜像已在跑；下次要重新发布飞书同步时，须先在 GitLab 填这个变量，不要写进仓库。
- 前端 NodePort 页面尚未在新集群拉起。

## CI/CD（必填）

- 分支：`dev`
- commit：编排仓 `ed615050`；前端见下表
- pipeline URL / ID：`2395` / job `11574`（`4aa1b007` 的 `helm:deploy`，tag `gkx`）
- 部署 namespace / 镜像 tag：`zhipu-tts`；tempo `library/tempo:2.7.1`，upms `gkx-upms:4aa1b007`
- K8s rollout：成功（上述 Deployment ready 1/1）
- dev 测试 URL / 命令与结果：Tempo 查询见测试结果；Verdaccio HTTP 200

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
