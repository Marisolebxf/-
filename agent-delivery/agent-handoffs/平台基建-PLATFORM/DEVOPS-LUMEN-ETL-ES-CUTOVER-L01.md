# DEVOPS-LUMEN-ETL-ES-CUTOVER-L01 · 关掉 demo ETL 副本

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | L01 helm 已绿（gkxlumen-platform rev 20）。关 demo 副本避免双写 ES。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只关 `etlEsPy.enabled`，不改 NodePort 到 lumen、不删模板。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 开关。 |

## 问题清单

- lumen `gkxlumen-platform-etl-es-py` 已 Helm 托管且 `/healthz` ok。
- `demo-platform-etl-es-py` 仍在，同一 `gkx_enterprise`。
- 无 CronJob / Java Feign；外网 30806 随 demo 开关释放。

## 修改内容

- `demo-svc-platform` `values.yaml` / `values-demo.yaml`：`etlEsPy.enabled=false`
- `paths.yaml` 改为 in-cluster `http://gkxlumen-platform-etl-es-py:8000`

## 测试结果

- 待 demo `helm:deploy` 后 `demo-platform-etl-es-py` 消失；lumen ETL 仍 Running。

## 遗留风险

- **请点 demo-svc-platform `helm:deploy`**（Nacos hook 已绿，应比 21724 快）。
- 另点 **lumen-etl-es-py `deploy:etl-es-py`** 把 helm 的 `latest` 钉成 SHA。
- 外网 `http://192.168.88.50:30806` 将失效，改打 in-cluster DNS。

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`
- commit：`71a032a`
- 部署：点 `helm:deploy`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 正式 ETL 不挂 demo | ✅ 关 demo etlEsPy |
| 算法只在 Python | ✅ 未改 ETL 代码 |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 18000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.16 |
| cost_warn | green |
