# DEVOPS-LUMEN-INNOV-ENTAN-PIN-SHA-L01 · 钉死 innov/entan Python 镜像 SHA

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 对照 ETL `DEVOPS-LUMEN-ETL-PIN-SHA-L01`。长任务不必再问。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改三套 Python tag / pullPolicy 与 helm:deploy 保活。未点 `helm:deploy`。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | helm 值 + 现网 set image。 |

## 问题清单

- 现网 `gkxlumen-innov-py` / `entan-py-api` / `entan-py-worker` 均为 `:latest` + `Always`。
- Harbor 上该 digest 同时挂着 `9a1889a4` / `4c6a6a53` / `a3c3c123` / `41ce60de` / `latest`（9a1889a 之后 vendor 未变，后续 chain CI 只是同层打新 tag）。
- `values-lumen.yaml` 仍写 `latest`，下次 `helm:deploy` 会打回浮动 tag。

## 修改内容

- `values-lumen.yaml` / `values.yaml`：三套 tag=`9a1889a4`，`pullPolicy=IfNotPresent`
- `k8s-deploy.sh`：innov/entan/etl 一律保活现网非 latest SHA
- 现网 `kubectl set image` + patch pullPolicy（digest 未变）

## 测试结果

- 现网：
  - `gkxlumen-innov-py:9a1889a4` `IfNotPresent` Ready 1；digest 仍 `sha256:db41551e…`
  - `gkxlumen-entan-py-api:9a1889a4` `IfNotPresent` Ready 1；digest 仍 `sha256:8276f657…`
  - `gkxlumen-entan-py-worker:9a1889a4` `IfNotPresent` Ready 1；digest 仍 `sha256:ea2ced12…`
- `/healthz` 均为 ok
- **未**点 `helm:deploy`

## 遗留风险

- 热更新仍走 `lumen-algo-py` 的 `deploy:innov` / `deploy:entan-*`（会 set 成该次 commit SHA）。
- 只改 chart 请点 `helm:chart`，不要点 `helm:deploy`。
- demo 的 `gkx-innov-py:latest` / `gkx-entan-py-*:latest` 未动（原型仓，本叶不钉）。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`7c173bd`
- pipeline：push 后 **不要点 `helm:deploy`**；可选点 `helm:chart` 把 helm values 写入 release
- namespace：`dev`
- 镜像 tag：`9a1889a4`
- K8s rollout：成功（仅改 tag 字符串，digest 相同）

## 可观测性（建议）

- 未改 OTel

## 涉及文件

- `lumen-svc-platform/helm/gkxlumen-platform/values-lumen.yaml`
- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
- `lumen-svc-platform/scripts/k8s-deploy.sh`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未迁 Java |
| D12 正式不挂 demo | ✅ 仍是 `gkxlumen-*`，未动 demo 镜像 |
| 调用链 FE→Java→Python | ✅ 未改 |
| 禁止把口令写入新文档 | ✅ |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 26000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.22 |
| cost_warn | green |
