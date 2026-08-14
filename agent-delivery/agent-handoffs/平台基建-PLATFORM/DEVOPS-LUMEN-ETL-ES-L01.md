# DEVOPS-LUMEN-ETL-ES-L01 · lumen-etl-es-py 进 gkxlumen-platform helm

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（用户「继续解决其他债」） |
| 说明 | D12 余项：正式 ETL 仍挂在 `demo-platform-etl-es-py`。本叶不切 30806 流量。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照复制 demo `etl-es-py.yaml` 到 lumen chart；CI 只改前缀。不关 demo、不双写作业。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | helm/CI 前缀，不依赖检索。 |

## 问题清单

- 现网 `demo-platform-etl-es-py` 读正式 `gkxlumenx_dwd`，NodePort 30806；CI `PLATFORM_K8S_PREFIX=demo-platform`。
- lumen chart 原先没有 `etlEsPy`。Java 仓无 Feign 直连 ETL；无 CronJob。
- **demo `08f6ca9` helm**：GitLab 若显示绿，**集群仍是 failed rev 24**，innov 镜像 `6f73df72`。与本叶无关，但 demo 再点 helm 前先把 hook 那枪落到 rev 25。
- lumen innov **2B-SQL** `e1fdff4` 也未上：现网仍 `INNOV_MYSQL_DB=innov` / `LEGACY=1`。

## 修改内容

- `lumen-svc-platform` helm：`templates/etl-es-py.yaml` + `values.yaml` 默认关 + `values-lumen.yaml` 启用 ClusterIP。
- `lumen-etl-es-py` CI 前缀 `gkxlumen-platform`；bootstrap 改名、ClusterIP、OTel 打 `gkxlumen-platform-otel-collector`。
- 基线 v2.2.7 登记 `D12-DEBT-ETL-ES-PY`。

## 测试结果

- 模板 `gkxlumen.resourceName` → `gkxlumen-platform-etl-es-py`。
- CI 无 `PLATFORM_K8S_PREFIX: "demo-platform"`。
- bootstrap Service `type: ClusterIP`，无 `nodePort: 30806`。

## 遗留风险

- **先点 lumen-svc-platform `helm:deploy`**（本叶 chart + 顺带把 `e1fdff4` 2B-SQL 一起带上）。
- 再点 **lumen-etl-es-py `deploy:etl-es-py`**（set image 到新 Deployment）。
- demo `demo-platform-etl-es-py` / 30806 **本叶仍留**。下一叶 CUTOVER：关 demo `etlEsPy`、文档/作业改 in-cluster DNS。
- 两副本都读同一 DWD、同一 ES 别名；本叶不要对两边同时打全量 sync。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev` `44db5ca`；`lumen-etl-es-py` `origin/dev` `9f6f98e`
- pipeline：先点 **lumen-svc-platform `helm:deploy`**（顺带带上 2B-SQL `e1fdff4`），再点 **lumen-etl-es-py `deploy:etl-es-py`**
- 部署 ns=`dev`；Service `gkxlumen-platform-etl-es-py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 lumen 不回落 demo 运行时 | ✅ CI 不再 set image `demo-platform-etl-es-py` |
| demo 副本暂留 | ✅ 本叶不关 30806 |
| 算法只在 Python | ✅ 未改 ETL 算法 |
| D8/D9/D10 | N/A |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 40000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.35 |
| cost_warn | green |
