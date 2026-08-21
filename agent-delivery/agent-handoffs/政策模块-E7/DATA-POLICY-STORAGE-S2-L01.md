# DATA-POLICY-STORAGE-S2-L01 · 政策维存储 S2 指针

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 无拓扑变更；补 sources/etl 指针与会签图同构 |
| 会签态 | `approved`（不翻签） |

## 修改内容

- `storage/POLICY/sources/inventory.md`
- `etl/pipeline-demo-mock.md`、`etl/pipeline-to-minio.md`
- `seeds/README.md`

## 验收证据

- 未灌数、未改业务仓。

## 架构合规自检

算法 Python ✅ · 图谱 Nebula 一张 G ✅ · 禁 PG/Neo4j ✅ · Demo 只写 `demo_*`（本叶零写入）✅ · D12 虚线 ✅

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 0 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0 |
| cost_warn | green |
