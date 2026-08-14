# DEVOPS-LUMEN-TOPIC-PY-L01 · lumen-topic-py 建仓 + CI/K8s 名隔离

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控授权，lock 24h） |
| 说明 | D12-DEBT-TOPIC-PY 第 1 叶。本叶不改 Java URL。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照复制后只改名隔离；未新加依赖；未把 Java 切流塞进本叶。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未走 Headroom 压缩；建仓/CI 改名不依赖检索。 |

## 问题清单

- 无。仓名 `lumen-topic-py`（禁止 `lumen-svc-topic-py`）已按总控落地。

## 修改内容

对照 `demo-svc-topic-py` **复制树**（禁止 git merge）到 `${GKX_ROOT}/repos/lumen-topic-py`，独立 git，默认分支 `dev`。

| 项 | 值 |
|----|-----|
| GitLab | https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py （project id **275**） |
| 本地 | `E:\gkx-lumen\repos\lumen-topic-py` |
| 检索 K8s | `gkxlumen-platform-search-py` ClusterIP `:8080` |
| AI K8s | `gkxlumen-platform-ai-py` ClusterIP `:8081` |
| Worker K8s | `gkxlumen-platform-ai-worker` |
| 镜像 | `gkxlumen-search-service` / `gkxlumen-ai-service` / `gkxlumen-ai-worker`（**不**覆盖 demo 的 `gkx-*` tag） |
| OTel | `http://gkxlumen-platform-otel-collector:4318` |
| 算法厨房 | `http://lumen-platform-algo-py:8000` |
| NodePort | **无**（避开 demo 30805/30807） |

未改 `repos/demo-svc-topic-py` 任何文件。未改 Java `python-base-url`。

登记：`repo-registry.yaml` `topic_py.lumen.planned: false`；`paths.yaml` 去掉「待建」。

## 测试结果

- 本地仓 `git log -1`：`5d20411`
- GitLab `origin/dev` 已推送
- Pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026 **全绿**（含 manual deploy）
- 本叶不部署 Java、不切流量
- **补记**：`deploy:search-py` / `deploy:ai-py` / `deploy:ai-worker` **success**（job 21527/21528/21529）

## 遗留风险

- 新项目 CI 变量依赖组级 `HARBOR_*` / `KUBECONFIG_B64`；若组未继承，image/deploy 会红。
- DWD 暂留 `demo_gkxlumenx_dwd`（切服务 ≠ 切库）。
- Worker K8s 名按 registry 用 `gkxlumen-platform-ai-worker`（CI `SVC_KEY=ai-worker`），不是 `*-worker-py`。
- Java 仍打 `demo-platform-search-py`，直到 CUTOVER。

## CI/CD（必填）

- 分支：`dev`
- commit：`5d20411`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026
- 部署 namespace / 镜像 tag：`dev` / `${CI_COMMIT_SHORT_SHA}`；deploy 已手动触发
- K8s rollout：`deploy:search-py` / `ai-py` / `ai-worker` **success**（pipeline 5026）
- dev 测试 URL：ClusterIP，无 NodePort；探活 `http://gkxlumen-platform-search-py:8080/healthz`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-search-service` / `gkxlumen-ai-service` / `gkxlumen-ai-worker`
- Tempo / Loki：随 collector `gkxlumen-platform-otel-collector:4318`

## 涉及文件

- `repos/lumen-topic-py/.gitlab-ci.yml`
- `repos/lumen-topic-py/k8s/dev-search-py.yaml`
- `repos/lumen-topic-py/k8s/dev-ai-py.yaml`
- `repos/lumen-topic-py/k8s/dev-ai-worker.yaml`
- `repos/lumen-topic-py/docs/DEPLOY-K8S.md`
- `agent-delivery/repo-registry.yaml`
- `agent-delivery/paths.yaml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 前端→Java→Python `/internal` | ✅ 本仓仅 `/internal` |
| 3 NebulaGraph | ✅ 未引入 Neo4j |
| 4 可观测 | ✅ OTel env |
| 5 CI/CD push→Pipeline | ✅ `origin/dev` |
| 6 demo 不 merge 进 lumen | ✅ 复制树，无 merge |
| 7 共享聚合 / Java 不写算法 | ✅ |
| 8 ADS/Mock 策略 | ✅ 切服务未切库，handoff 已注 |
| 9 D8 前端 | N/A |
| 10 D9 血缘 | N/A |
| 11 D10 交互 | N/A |
| 12 D12 lumen 不打 demo 服务 | ✅ 本仓 K8s/镜像已隔离；Java 回落留 CUTOVER |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.40 |
| cost_warn | green |
