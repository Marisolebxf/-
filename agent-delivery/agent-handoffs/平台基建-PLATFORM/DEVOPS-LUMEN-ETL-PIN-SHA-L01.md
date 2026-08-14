# DEVOPS-LUMEN-ETL-PIN-SHA-L01 · 钉死 gkxlumen-platform-etl-es-py 镜像 SHA

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 长任务总控已授权不必再问。现网已是 SHA；债在 helm 仍写 `latest`+`Always`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改 ETL 镜像 tag / pullPolicy 与 helm:deploy 保活现网 SHA。未点 `helm:deploy`（会滚全部 Java）。未用 YAGNI 跳过 D12。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶 helm 值 + 现网 patch，无 MCP 检索需求。 |

## 问题清单

- 现网 Deployment 已是 `lumen-etl-es-py:2ac38573`，但 `values-lumen.yaml` 仍 `tag: latest` + `pullPolicy: Always`。
- `gkxlumen.image` 用 `default .global.imageTag .image.tag`：只要 `etlEsPy.image.tag` 非空就盖过 Java 的 `global.imageTag`。下次 `helm:deploy` 会把 ETL **打回 latest**。
- 热更新仍应走 `lumen-etl-es-py` 的 `deploy:etl-es-py`（`kubectl set image` 为该次 commit SHA）。禁止 `kubectl apply` 抢建。

## 修改内容

- `helm/gkxlumen-platform/values-lumen.yaml`：`etlEsPy.image.tag=2ac38573`，`pullPolicy=IfNotPresent`
- `helm/gkxlumen-platform/values.yaml`：默认 tag 同步钉 SHA（`enabled` 仍 false）
- `scripts/k8s-deploy.sh`：`helm:deploy` 读取现网 ETL tag，`--set etlEsPy.image.tag=<live>`；若现网已是非 latest SHA，则保留该 SHA，不打回 `latest`
- 现网：`kubectl patch` 仅改 `imagePullPolicy=IfNotPresent`（镜像未改）

## 测试结果

- 现网镜像：`harbor.htmisoft.net/gkx/lumen-etl-es-py:2ac38573`
- `imagePullPolicy=IfNotPresent`
- rollout 成功；Pod `gkxlumen-platform-etl-es-py-5fff687f56-xk9h2` 1/1 Ready
- `/healthz`：`status=ok`，ES 可达，企业索引别名已绑定
- **未**跑 lumen `helm:deploy`（避免全量滚动 Java）

## 遗留风险

- lumen 仍无 `helm:chart`。只改 chart 时请勿点全量 `helm:deploy`。本叶脚本已保活 ETL SHA，但 Java 仍会被 `--set global.imageTag` 滚动。
- `deploy:etl-es-py` 热更新后，现网 SHA 会变；下次 `helm:deploy` 会跟现网 SHA，不必先改 values。values-lumen 里的 `2ac38573` 是安装默认值。
- 不要再 `kubectl apply` 抢建 ETL。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`852c93d`
- pipeline：push 后 lint/chart 即可；**不要点 `helm:deploy`**
- 部署 namespace：`dev`
- 镜像 tag：`2ac38573`
- K8s rollout：成功（仅 pullPolicy patch）
- 验证：`kubectl -n dev get deploy gkxlumen-platform-etl-es-py -o jsonpath='{.spec.template.spec.containers[0].image}{" "}{.spec.template.spec.containers[0].imagePullPolicy}'`

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改
- Tempo / Loki：无本叶增量

## 涉及文件

- `lumen-svc-platform/helm/gkxlumen-platform/values-lumen.yaml`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
- `lumen-svc-platform/scripts/k8s-deploy.sh`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未把 ETL 逻辑迁 Java |
| 调用链 FE→Java→Python | ✅ 未改调用链 |
| 图谱 Nebula | N/A |
| 可观测 | N/A（未改埋点） |
| CI/CD | ✅ 不点全量 helm:deploy；现网 patch 对齐 chart |
| D12 正式不挂 demo | ✅ 仍是 `lumen-etl-es-py` / `gkxlumen-platform-etl-es-py` |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 28000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.22 |
| cost_warn | green |
