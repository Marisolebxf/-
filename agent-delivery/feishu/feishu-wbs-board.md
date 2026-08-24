# 飞书「指标算法WBS」看板使用指南

> **日期**：2026-08-22 · 给人说明 §5 / §8 的 **任务投影**（不是把全文再贴一张表）
> **真源**：[`../agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md`](../agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md) §5 + §8.0  
> **状态**：`task-registry.yaml` 现网（脚本只读 join；agent 日常仍走 MCP）  
> **配置**：[`feishu-wbs-board.yaml`](./feishu-wbs-board.yaml)

## 1. 定位

一行 = **一个 WBS 工作包**（`WBS-1.1`）或 **一条点名 registry 叶**（`WBS-2.2/CHAIN-METRIC-OPEN-L01`）。

给人看：指标/算法这条线现在排到哪、**最晚必须哪天完成**、8/25 硬路径是哪一叶、哪些还没建单、哪些是废作。

「截止日期」= 给人说明 §8.1 / §8.2 的硬窗口（当天 23:59 +08）。registry `deadline` 或备注「截止 YYYY-MM-DD」只在计划没有窗口时补空。无硬截止的行留空，不编造门 1 日期。

**不投影**：给人说明全文、calc-logic、PACK 全量爆炸、xlsx、王惠表。611 行任务看板仍是 [`feishu-bitable.yaml`](./feishu-bitable.yaml) 那张，本表只 join 点名 ID。

**不建单**：应补登 OPEN、企业/综合/政策迁页叶只标「未建单」。确认后再走 MCP `task-create`。T0-X 已建 `ALGO-LIB-T0X-L01`。

## 2. 同步

```powershell
node scripts/sync-feishu-wbs-board.mjs
node scripts/sync-feishu-wbs-board.mjs --dry-run
```

K8s Cron 随 `feishu-bitable-cron-sync.mjs` 出站。无凭据软失败。

## 3. 建议视图

1. 全量总览
2. 看板：分组 = 阶段
3. 看板：分组 = 任务状态
4. 筛选：路径 = 8/25硬路径（只有 `ALGO-LIB-METRIC-DEPS-L01` 及其维内步骤）
5. 筛选：截止日期 ≤ 今天（逾期）
6. 筛选：类型 = 未建单
7. 筛选：类型 = 废作（勿再派）

## 4. 行从哪来

| 类型 | 来源 |
|------|------|
| 工作包 / 维内步骤 / 未建单（§5 表） | 给人说明 §5 各 WBS 表 |
| 任务叶 · A2 / 九新 / A1 | §5 表内反引号 ID；多 ID 工作包拆子行 |
| 任务叶 · B 轨 / 联调台 / 设计卡 | §8.0 点名且 §5 未写反引号的 |
| 任务叶 · METRIC-OPEN | 现网全部 `*-METRIC-OPEN-L01`（排除 `READINESS`） |
| 未建单 · 应补登 OPEN | §8.4 甲建议 ID，且 registry 没有 |
| 废作 | `TOPIC/DS-METRIC-INVENTORY/CLASSIFY-L01` |

`WBS-1.1.1`～`1.1.8` / `1.1.9` **不另建单**，状态跟 `ALGO-LIB-METRIC-DEPS-L01`。

`{MODULE}-PACK-L01` / `{MODULE}-FDS-L01` 只留工作包行，不按模块爆炸。

## 5. 纪律

- 飞书只读；改 WBS 结构改给人说明，改状态改 registry
- 废作四叶展示现网状态，但类型=废作，禁止当待办再派
- 本表不是第二套任务看板，禁止把 611 行全量灌进来
