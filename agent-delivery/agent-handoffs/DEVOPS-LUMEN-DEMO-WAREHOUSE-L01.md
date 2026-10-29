# DEVOPS-LUMEN-DEMO-WAREHOUSE-L01 · lumen 数仓切到 demo_gkxlumenx_*（平台库不动）

> 内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 人确认：只改数仓、平台库不动，并推进 dev 部署。先建单后执行。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改数仓 env / InnovSql 限定名；未动 UPMS/Nacos/topic-enterprise；未加新依赖。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为 helm/k8s 库名切换，未走 Headroom 压缩。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链图；只改同一 MySQL 实例上的数仓库名。 |
| 会签态 | N/A |

## 问题清单

- Java `gkxlumen-innov` 镜像内 `InnovSql` 硬编码已改仓，但现网 jar 仍是旧镜像；`INNOV_MYSQL_DB` 已切到 `demo_gkxlumenx_ads`（JDBC 默认库）。需 GitLab 手动 `deploy:innov` 后 SQL 限定名才进现网。
- 下次 `helm:deploy` 会按已 push 的 `values-lumen.yaml` 重放 env，与本次 `kubectl set env` 一致。

## 修改内容

- helm `values.yaml` / `values-lumen.yaml`：innov / innov-py / entan-py / entan-py-worker / etl-es-py 的 ODS/DWD/ADS/DIM → `demo_gkxlumenx_*`；`gkxlumenx_cfg` 不动。
- `InnovSql` 将 ads/dwd/dim 限定名改为 `demo_gkxlumenx_*`；cfg 仍 `gkxlumenx_cfg`。
- `lumen-algo-py` `k8s/api.yaml` + `worker.yaml`：`LUMEN_ALGO_MYSQL_{DWD,ADS}_DB` → demo 库。
- 未改：`MYSQL_DB=gkxlumenx`（UPMS/Auth）、`gkxlumenx_config`、`gkxlumenx_topic_enterprise`。search-py 原本已是 `demo_gkxlumenx_dwd`。

## 测试结果

- `kubectl -n dev set env` 后 7 个 Deployment READY=1/1。
- 现网 env 抽检（2026-09-02）：
  - innov-py：`INNOV_MYSQL_{ODS,DWD,ADS,DIM}_DB=demo_gkxlumenx_*`，`CFG=gkxlumenx_cfg`
  - entan-py / worker：`ENTAN_MYSQL_{DWD,ADS}_DB=demo_gkxlumenx_*`
  - etl-es-py：`MYSQL_DWD_DB=demo_gkxlumenx_dwd`
  - lumen-platform-algo-py / worker：`LUMEN_ALGO_MYSQL_{DWD,ADS}_DB=demo_gkxlumenx_*`
  - innov Java：`INNOV_MYSQL_DB=demo_gkxlumenx_ads`，平台 `MYSQL_DB=gkxlumenx`（未动）
  - upms：`MYSQL_DB=gkxlumenx`（未动）
  - topic-enterprise：`MYSQL_DB=gkxlumenx_topic_enterprise`（未动）

## 遗留风险

- innov Java SQL 限定名要等新镜像；旧 jar 仍 qualify 到 `gkxlumenx_{ads,dwd,dim}`。
- Python 批处理若 `INNOV_RUN_ON_START=1` / `ENTAN_RUN_ON_START=1`，会向 demo 数仓写结果（与 demo-platform 同源，注意并发）。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：
  - `lumen-svc-platform` `47bed29` fix(helm): point lumen warehouse at demo_gkxlumenx_* [agent:devops-agent]
  - `lumen-algo-py` `bc30dc6` fix(k8s): point algo-py warehouse at demo_gkxlumenx_* [agent:devops-agent]
- pipeline URL / ID：push 已触发各仓 CI；Python/helm env 由 10.50.69.111 `kubectl set env` 即时生效，未等 manual `helm:deploy`
- 部署 namespace / 镜像 tag：`dev`；镜像 tag 未换（仅 env）
- K8s rollout：成功（7 deploy READY=1）
- dev 测试 URL / 命令与结果：见上方 env 抽检

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改
- Tempo / Loki：无本叶新采样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未把算法搬进 Java |
| 调用链前端→Java→Python `/internal/*` | ✅ 未改调用链 |
| 图谱 NebulaGraph | ✅ 未改 |
| 可观测性 | ✅ 未删 OTel env |
| CI/CD push → Pipeline | ✅ 已 push `origin/dev` |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不写算法 | ✅ |
| 数据策略 ADS | ✅ 切到已有 demo ADS/DWD |
| D8 / D9 / D10 | N/A 无 UI |
| D12 lumen 不调 demo 服务 | ✅ 只改同实例数仓库名，未指向 demo-* Service；未连 `gkxx` |

## 涉及文件

- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
- `lumen-svc-platform/helm/gkxlumen-platform/values-lumen.yaml`
- `lumen-svc-platform/helm/gkxlumen-platform/DEPLOY-LUMEN.md`
- `lumen-svc-platform/gkxlumen-innov/.../InnovSql.java` + 单测
- `lumen-algo-py/k8s/api.yaml`
- `lumen-algo-py/k8s/worker.yaml`
- `lumen-algo-py/k8s/README.md`
