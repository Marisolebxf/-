# API-DEMO-INNOV-ADS-ISOLATE-L01 · demo Java 离开正式 ADS

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12 全拆：demo 不读写正式 `gkxlumenx_ads`。cfg 仍共享。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有 DataPlane 改写，不改控制器 SQL；缺表一次性 snapshot，不走 GDF。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 改写规则短，不依赖检索。 |

## 问题清单

- 产品页无 `X-GKX-PLANE-INNOV` 时，DataPlane **保持正式库 SQL** → EventMap 打 `gkxlumenx_ads.innovation_event`（230 行）。
- `demo_gkxlumenx_ads` **无** `innovation_event`（1146）；dim 字典已在；dwd 图/成果表空壳。
- demo innov-py 已通过 `CHAINAN_MYSQL_*` 指向 `demo_*`，但未产出创新 ADS 表。
- JDBC `INNOV_MYSQL_DATABASE` 仍是 `gkxlumenx_ads`（SQL 全限定名，catalog 本身不是根因）。

## 修改内容

| 项 | 做法 |
|----|------|
| `DataPlane.qualifyInnovSql` | 一律把 `gkxlumenx_{ads,dwd,dim,ods}.` 改写为 `demo_*`；已是 `demo_` 不二次改写；`gkxlumenx_gkx_cfg` 不动 |
| helm JDBC | `INNOV_MYSQL_DATABASE=demo_gkxlumenx_ads` |
| snapshot | `CREATE TABLE LIKE` + `INSERT SELECT`：ADS 9 张（含 `innovation_event=230`）；DWD 空壳 `FILL` graph_node=472 / graph_edge=620 / org_achievement_year=1312 |
| 基线 | `architecture-baseline.md` v2.2.5 |

## 测试结果

- 同款正则自检：`gkxlumenx_ads.x` → `demo_gkxlumenx_ads.x`；`demo_` 幂等；cfg 不改。**ok**
- JUnit `DataPlaneQualifyTest` 已加（本机无 `mvn`，交 CI）
- MySQL COUNT：`demo_gkxlumenx_ads.innovation_event=230`

## 遗留风险

- 现网要等 **demo-svc-platform** 新镜像 + helm。只点 `deploy:innov` 也能让 SQL 改写生效（jar）；`helm:deploy` 才改 JDBC catalog。
- snapshot 是一次性拷贝，之后 demo Python / 正式库会分叉。
- 联调台 `X-GKX-PLANE-INNOV=live` **不再**让创新 SQL 打回正式 ADS（全拆）。Feign 头仍透传。
- lumen Java 仍读 `innov` M1 表，本叶未动。

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`
- commit：`6f73df7`
- 部署：ns=`dev` release `demo-platform`；点 **`helm:deploy`**（或 image:innov 绿后先点 `deploy:innov` 滚 jar）
- K8s rollout：待 pipeline
- 验收：新 Pod 后 `INNOV_MYSQL_DATABASE=demo_gkxlumenx_ads`；事件列表仍有数据且 SQL 不再扫正式 ADS

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkx-innov`
- Tempo / Loki：有（未抽本叶 trace）

## 涉及文件

- `demo-svc-platform/gkx-innov/src/main/java/com/topcomm/gkx/innov/support/DataPlane.java`
- `demo-svc-platform/gkx-innov/src/test/java/com/topcomm/gkx/innov/support/DataPlaneQualifyTest.java`
- `demo-svc-platform/gkx-innov/src/main/resources/application.yml`
- `demo-svc-platform/gkx-innov/pom.xml`
- `demo-svc-platform/helm/gkx-platform/values.yaml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 demo 不读正式 ADS | ✅ DataPlane 默认改写 + JDBC catalog |
| lumen 不写 demo 库 | ✅ 未改 lumen |
| Java 不写算法 | ✅ 只读查询改写 |
| 不走 GDF 全量迁数 | ✅ 9+3 张表一次性 LIKE/INSERT |
| D8/D9/D10 | N/A 无 UI |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 55000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.5 |
| cost_warn | green |
