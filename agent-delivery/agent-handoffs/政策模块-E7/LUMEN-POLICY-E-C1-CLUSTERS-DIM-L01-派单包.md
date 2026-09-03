# `/goal` · LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01

```
/goal LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01
角色：api-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-svc-platform · origin/dev
强度：ponytail full
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
禁止：DDL / 写正式 gkxlumenx_*；猜建表；问用户选仓；改无关仓；lumen 调 demo-* 服务（D12）。
数仓：只认 demo_gkxlumenx_*。禁止为「上 lumen」把 JDBC 改成正式前缀。
X-Trace-Id：071b34f54c36d31761617fc884567f03
图：CHAIN-STORE-DIM-INDUSTRY-CLUSTER 不翻签；本叶只改运行时 schema 绑定。
```

## coordinator 确认分类（覆盖 QA 建议 C5）

QA 建议 C5（表不存在）。Tempo：`Table 'gkxlumenx_dim.industry_cluster_map' doesn't exist`，服务 `gkxlumen-innov`。

**确认类 = C1 配错**，不是新表：

- 存储真源 `dim-industry-cluster.md`：库 = `gkxlumenx_dim`（**Demo：`demo_gkxlumenx_dim`**）。现网 lumen 数仓 = demo 源（政策总控 §0 #6）。
- Java `IndustryClusterService`：`@Value("${INNOV_DIM_SCHEMA:gkxlumenx_dim}")` **默认正式前缀**。
- Helm Java `innov.env` 有 `INNOV_MYSQL_DB=demo_gkxlumenx_ads`，**没有** `INNOV_DIM_SCHEMA`。Python `innovPy` 才有 `INNOV_MYSQL_DIM_DB=demo_gkxlumenx_dim`，Java 没读这个键。
- **禁止**在正式 `gkxlumenx_dim` CREATE 该表（那才是 C5，升级李伟）。本叶只把运行时绑到 `demo_gkxlumenx_dim`。

若改绑后 `demo_gkxlumenx_dim.industry_cluster_map` 仍不存在 → **立刻 blocked**，升级 `human:李伟`，**不要** DDL 正式库。

## 必读

1. `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-C1RETEST-L01-defect-pack.md`
2. `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-ABCDE-长任务总控.md` §0 #6/#9
3. `agent-delivery/data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md`
4. Tempo：http://192.168.88.50:30201/api/traces/071b34f54c36d31761617fc884567f03

## 必须改

1. `gkxlumen-innov/.../IndustryClusterService.java`：默认 schema = `demo_gkxlumenx_dim`。优先读已有 helm 键（`INNOV_DIM_SCHEMA` 或 `INNOV_MYSQL_DIM_DB`），禁止再默认 `gkxlumenx_dim`。
2. Helm Java `innov.env`（`values.yaml` + `values-lumen.yaml` 若覆盖）：注入 `INNOV_DIM_SCHEMA=demo_gkxlumenx_dim`。
3. GET `/topic/v1/meta/industry-clusters?include_l0=true` 不得 500。L0 须能形成 `chain:INB…`（`INB`≥6）。无映射诚实空，不造假。
4. 注释「只读正式 dim」与现网冲突，改为 demo 前缀。CHAIN 叶 `LUMEN-CHAIN-INDUSTRY-CLUSTER-L01` DoD「只读正式 dim」对本运行时作废，以总控 §0 #6 为准。本叶**不要**改 `lumen-ui-topic`（李伟占用）。

## 验收

- 本地/dev 探活：clusters 非 500。
- push `origin/dev`；commit `[agent:api-agent]`；禁止 force。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-C1-CLUSTERS-DIM-L01.md` + ponytail: full + cost + 是否需 E0 滚 `gkxlumen-innov`。
- 不要自行 done。

## Convoy

`LUMEN-SVC-P-JAVA-API-SEARCH-ORGS-L01` lock 已于 2026-08-22 过期。`LUMEN-CHAIN-INDUSTRY-CLUSTER-L01` 占 FE+集群契约；本叶只改 schema 绑定，不改级联 UI。
