# DEVOPS-DEMO-HELM-CHART-PIN-PY-L01 · demo helm:chart 钉回现网 Python 镜像

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | `/goal` 派单；默认监管 `dispatch-rules=human:徐滕强`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在 `HELM_CHART_ONLY` 读现网再 `--set`；不改 `helm:deploy`、不把 `values.yaml` tag 写死 SHA；未用 YAGNI 跳过 CI 门禁 / OTel（本叶不改探针与 collector）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CI/helm 脚本叶，无长上下文压缩需求。 |

## 问题清单

- `helm:chart`（`HELM_CHART_ONLY=true`）已不 `--set global.imageTag`，Java 不被打成当前 SHA。
- Python `values.yaml` 仍是 `image.tag: latest`；算法仓 `kubectl set image` 热更不写回 Helm values。随后 chart-only `--reuse-values` 把现网 SHA 收成 `:latest`（政策 sync-ods 404 即此因）。
- 本叶补 Python 钉回；禁止 `helm:deploy` 验收。

## 修改内容

- `scripts/k8s-deploy.sh`：`HELM_CHART_ONLY` 在 `helm upgrade` 前读取 6 个高风险 Deployment（+ 可选 `demoPy`）现网 `containers[0].image`，解析 tag 后 `--set {key}.image.tag=$tag`。Deployment 不存在或 digest/`@` 解析失败则 skip，不 `--set latest`。
- `helm:deploy` 路径仍只 `--set global.imageTag=$TAG`，行为未改。
- `.gitlab-ci.yml`：`helm:chart` 注释说明 Python 热更镜像不被 chart-only 盖回 latest。
- `values.yaml` 的 `tag: latest` **未改**（不写死 SHA）。
- 自检：`scripts/k8s-deploy.sh --selftest-pin-tag`（Git Bash 绿）。

## 测试结果

- 升级前现网（ns=`dev`，2026-08-31）：
  - `demo-platform-entan-py` → `gkx-entan-py-api:6e322240`
  - `demo-platform-entan-py-worker` → `gkx-entan-py-worker:6e322240`
  - `demo-platform-innov-py` → `gkx-innov-py:f006e9b1`
  - `search-py` / `ai-py` / `worker-py` / `demo-py` → 当时已是 `:latest`（钉回 latest，不是把 SHA 收成 latest）
- `helm:chart` job 24956 **success**（11s，未点 `helm:deploy`）。日志打印 6 组 + demoPy `--set`：
  - `entanPy.image.tag=6e322240`
  - `entanPyWorker.image.tag=6e322240`
  - `innovPy.image.tag=f006e9b1`
  - `searchPy` / `aiPy` / `workerPy` / `demoPy` = 当时现网 `latest`
- 升级后 `kubectl` 镜像与升级前一致：entan/innov 仍是 SHA，不是被收成旧 `:latest`。

## 遗留风险

- `rollme: {{ randAlphaNum 5 }}` 仍会让 Python Pod 重启；目标只保证镜像 tag 不回 latest。
- search/ai/worker 现网若本就是 `:latest`，chart-only 只能钉 latest；要 SHA 须算法仓再跑 `deploy:*` 热更。
- digest 镜像（`@sha256:`）chart helper 只渲染 `:tag`，脚本 skip 并打日志，避免拼出非法 `repo:sha256:…`。
- Java 仍走 `global.imageTag`；chart-only 不钉 Java（前序 `DEVOPS-DEMO-HELM-CHART-ONLY-L01`）。

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`
- commit：`f4a76ca`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/demo-svc-platform/-/pipelines/5750
- 部署 namespace：`dev`（仅 `helm:chart` job 24956，**未跑** `helm:deploy`）
- K8s：`helm status demo-platform -n dev` → `STATUS=deployed` `REVISION=32`（`LAST DEPLOYED: 2026-08-31 19:12:33`）
- job：https://gitlab.htmisoft.net/gkx-lumen/demo-svc-platform/-/jobs/24956
- 脚本打印：见 job trace「pin live Python image tags」6 组 `--set`

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（chart 仍注入 `gkx.commonOtelEnv`）
- Tempo / Loki：无（本叶不改 collector）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 / 算法只在 Python | ✅ 未改业务代码 |
| Nebula | ✅ 未改 |
| OTel | ✅ 未拆注入 |
| CI/CD | ✅ push `origin/dev`；只验收 `helm:chart` |
| D12 | N/A（demo Helm 操作面） |
| 禁止 helm:deploy 验收 | ✅ |
| values.yaml 不写死 SHA | ✅ |

## 涉及文件

- `${GKX_ROOT}/repos/demo-svc-platform/scripts/k8s-deploy.sh`
- `${GKX_ROOT}/repos/demo-svc-platform/.gitlab-ci.yml`
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/DEVOPS-DEMO-HELM-CHART-PIN-PY-L01.md`

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | grok-4 |
| actual_cost | 0.22 |
| cost_warn | green |
