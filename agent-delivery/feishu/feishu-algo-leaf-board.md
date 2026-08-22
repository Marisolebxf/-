# 飞书「算法库叶子」看板使用指南

> **日期**：2026-08-22 · **三张投影之二**（A1）
> **真源**：`metrics/algo-results/*-requirements.yaml`（97 叶）+ `*-metrics.yaml`（ODS）  
> **配置**：[`feishu-algo-leaf-board.yaml`](./feishu-algo-leaf-board.yaml)  
> **Schema**：[`../metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`](../metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md)

## 1. 定位

一行 = 算法库 SRS **一条叶子**（表1 `requirement_id`）。给人看：97 叶覆盖了没、ODS 最差落到哪、该派哪一维 Owner。

**不投影**：xlsx 四个 sheet、给人说明全文、calc-logic。xlsx 给人审，yaml 上板。

A1 双表未交时脚本仍可跑：建空表 + 0 行。按维增量交 yaml 后重跑即 upsert，不必等 97 叶一次齐。

## 2. 同步

```powershell
node scripts/sync-feishu-algo-leaf-board.mjs
node scripts/sync-feishu-algo-leaf-board.mjs --dry-run
```

K8s Cron 随 `feishu-bitable-cron-sync.mjs` 出站。无凭据软失败。

## 3. 建议视图

1. 全量总览
2. 看板：分组 = 八维
3. 看板：分组 = ODS最差
4. 筛选：ODS最差 ∈ {无源, 部分, 待ODS} —— 8/25 采购/入站
5. 筛选：覆盖状态 = 缺失（给 A2）
6. 筛选：第三方（不伪展开公式）

## 4. ODS 最差

按表2 `dependency_rollup.ods_mapping_status`，缺则取 `inputs[].ods_mapping_status` 最差：

`none` > `pending_ods` > `partial` > `full` > `n/a`。无表2 = 未评估。

## 5. 纪律

- 飞书只读；改覆盖/ODS 走 algo-results yaml
- 禁止把 xlsx 当第二真源同步进本表
- 展示系统不套专题维度 Owner；本表是算法库叶子，维 Owner 按八维名
