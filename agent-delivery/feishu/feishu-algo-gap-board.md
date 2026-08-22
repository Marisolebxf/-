# 飞书「页面指标差集」看板使用指南

> **日期**：2026-08-22 · **三张投影之三**（A2）
> **真源**：`metrics/request/{专题系统,展示系统}/pages/*.yaml` 的 `items[]`（`row_id`）  
> **配置**：[`feishu-algo-gap-board.yaml`](./feishu-algo-gap-board.yaml)  
> **Schema**：[`../metrics/request/A2-GAP-schema.md`](../metrics/request/A2-GAP-schema.md)

## 1. 定位

一行 = 页面指标释义 **一条**。给人看：功能要了、库有没有（`差集判定`）。主交付数字 = `missing` 条数。

**不上板**：

- `semantic_debt`（专题 111 + 展示 247）—— 不是 A2 missing，走 METRIC-OPEN / 原叶补条目
- `_work/` 底稿、fan-in 索引 yaml（与 pages 重复）
- 九新目录（yaml 未交）
- xlsx（给人审，不投影）

OPEN 覆盖仍看 **任务看板**，不在本表。

## 2. 同步

```powershell
node scripts/sync-feishu-algo-gap-board.mjs
node scripts/sync-feishu-algo-gap-board.mjs --dry-run
```

K8s Cron 随 `feishu-bitable-cron-sync.mjs` 出站。无凭据软失败。

## 3. 建议视图

1. 全量总览
2. 看板：分组 = 差集判定
3. 筛选：`missing`（主清单）
4. 按系统 / 按模块
5. 处置桶：T0-X 会后 yaml 有值再筛；现网全是「未分拣」，列先建着

## 4. 处置桶

T0-X（淮政玮主持）四桶：①STAT ②已有模型 ③新 MODEL ④DEMO。会前脚本写「未分拣」，禁止在飞书手填当真源。

## 5. 纪律

- 飞书只读；改判定走 pages yaml
- 禁止为 missing 编造 `M_*`
- 展示不重列专题已记的 missing
