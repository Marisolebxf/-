# LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01 · 政策专题 E · C1 集群接口绑 demo_gkxlumenx_dim

> 格式参考 `templates/handoff-template.md`。段 E 缺陷包测试驱动；只改运行时 schema 绑定。  
> 派单包：[`LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01-派单包.md`](./LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01-派单包.md)  
> 缺陷包：[`LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md`](./LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。bugfix。不要自行 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短工作 diff：只改 Java 默认 schema + Helm Java `innov.env`。未 DDL、未写正式 `gkxlumenx_dim`、未改 `lumen-ui-topic`、未翻签 `CHAIN-STORE-DIM-INDUSTRY-CLUSTER`。未用 YAGNI 跳过手off / 架构铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 compress。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `CHAIN-STORE-DIM-INDUSTRY-CLUSTER` |
| 图 diff | 无。本叶只改运行时 schema 绑定，不翻签存储图。 |
| 会签态 | `draft`（源文件 frontmatter；本叶不翻签） |

## 问题清单

- Tempo `071b34f54c36d31761617fc884567f03`：`gkxlumen-innov` 读 `gkxlumenx_dim.industry_cluster_map` 表不存在 → clusters HTTP 500。
- 根因 = C1 配错（Java `@Value` 默认正式前缀 + Helm Java `innov.env` 未注入 DIM schema），不是缺表。
- 改绑后现网 `demo_gkxlumenx_dim.industry_cluster_map` **存在**（15 行 map / 15 行 cluster），**未** blocked、**未** DDL。

## 修改内容

| 路径 | 动作 |
|------|------|
| `gkxlumen-innov/.../IndustryClusterService.java` | 默认 schema = `demo_gkxlumenx_dim`；嵌套读取 `INNOV_DIM_SCHEMA` → `INNOV_MYSQL_DIM_DB`；注释不再写「只读正式 dim」 |
| `helm/gkxlumen-platform/values.yaml` | Java `innov.env` 注入 `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim` |
| `helm/gkxlumen-platform/values-lumen.yaml` | Java `innov.env` 整表列出（Helm list 覆盖）并注入同一键；JDBC 仍 `demo_gkxlumenx_ads` |
| `IndustryClusterSchemaBindTest.java` | 断言默认占位符是 demo 前缀、不再是 `:gkxlumenx_dim}` |

未改：`lumen-ui-topic`（李伟占 `LUMEN-CHAIN-INDUSTRY-CLUSTER-L01`）；正式库；JDBC 主机。

## 测试结果

- 现网 MySQL `192.168.88.43`：`demo_gkxlumenx_dim.industry_cluster` = 15；`industry_cluster_map` = 15。`gkxlumenx_dim` 无这两张表（故旧默认必然 500）。
- 映射 L0 例：`INB1303` / `INB1309` / `INB1204` 等（长度 7，满足 `INB`≥6）；空集群保持 map 0 条诚实空。
- Helm YAML：`python yaml.safe_load` 两文件通过。
- 本机无 `mvn` / `JAVA_HOME`，未跑 Maven；CI 应跑 `IndustryClusterSchemaBindTest`。
- **现网 clusters 仍 500，直到 E0 滚 `gkxlumen-innov`（新镜像 + Helm env）。** 代码层联调通过：改绑目标表存在且有可挂图 L0。

## 遗留风险

- 必须 **E0 滚 `gkxlumen-innov`**：Java 默认值在镜像里，Helm env 也要进 Deployment。只滚前端不够。
- 滚完后 QA 复测 `GET /topic/v1/meta/industry-clusters?include_l0=true` 不得 500；页内集群→L0 金路径 #2～#5 才能再跑。Create / SHA-256 本叶未复测。
- 部分集群仍 `pending_vendor`（无 L0）→ 诚实「无相关产业数据」，不造假。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：`300ad3036fa052f386051ed0ce7148bd8e27f554`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines （push 触发；本会话未等绿）
- 部署 namespace：`dev` / 镜像：待 CI 出 `gkxlumen-innov` 新 tag
- K8s rollout：**需要 E0 滚 `gkxlumen-innov`**（本叶未自行 helm upgrade）
- 探活：滚完后 `GET http://192.168.88.50:30899/innov/v1/meta/industry-clusters?include_l0=true`（前端现网为 `/api/topic/v1/meta/industry-clusters`）不得 500

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-innov`
- 根因 traceId：`071b34f54c36d31761617fc884567f03`
- Tempo：http://192.168.88.50:30201/api/traces/071b34f54c36d31761617fc884567f03
- 滚后应用新 X-Trace-Id 验 200

## 涉及文件

- `gkxlumen-innov/src/main/java/com/topcomm/gkxlumen/innov/cluster/IndustryClusterService.java`
- `gkxlumen-innov/src/test/java/com/topcomm/gkxlumen/innov/cluster/IndustryClusterSchemaBindTest.java`
- `helm/gkxlumen-platform/values.yaml`
- `helm/gkxlumen-platform/values-lumen.yaml`

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 本叶只读 JDBC DIM，无 NLP |
| 2 | 调用链 前端→Java→Python `/internal/*` | ✅ 未越层；未改 Feign |
| 3 | 图谱 NebulaGraph | ✅ 未写 nGQL |
| 4 | 可观测 | ✅ 沿用 innov OTel；原 500 有 Tempo |
| 5 | CI/CD | ✅ push `origin/dev`；需 E0 滚 innov |
| 6 | D12 不调 demo-* 服务 | ✅ 只改 lumen Java/Helm；数仓仍 `demo_gkxlumenx_*` |
| 7 | 方案 A / 只读 ADS+DIM | ✅ 只读 DIM 映射表，不写正式库 |

## 成本

- actual_tokens: 98000（会话估算：厚包 + Java/Helm + 现网验表；source: session_estimate）
- model_used: cursor-grok-4.6
- actual_cost: 0.57
- cost_warn: green

## coordinator 下一步

1. **E0 点名滚 `gkxlumen-innov`**（镜像 + `INNOV_DIM_SCHEMA`）。
2. 滚绿后派 QA 复测 clusters 非 500 + 金路径 #2～#5。
3. 不要把本叶标 done。
