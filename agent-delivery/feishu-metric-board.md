# 飞书「指标与数据开发进度」看板使用指南

> **日期**：2026-08-01 · **任务**：ORCH-METRIC-BOARD-L01（监管 human:淮政玮）
> **真源分层**：`metrics/metric-readiness-matrix-*.yaml`（四维就绪度）+ `metrics/cfg_metric-*-seed.yaml`（8 件套）+ 各模块 `*data-gap-catalog.yaml`（缺口文案）= 唯一真源；飞书 = **只读投影**（拖拽/改列不回写 git）
> **配置**：`feishu-metric-board.yaml` · **模型**：`data-lineage-policy.md` §2.3（D9 v1.3 四维就绪度）

## 1. 看板定位

与任务看板同一个多维表格应用里的独立数据表「**指标与数据开发进度**」（table_id 见配置），一行 = 一个 metric_id。给整体开发团队回答四个问题：

| 列组 | 回答的问题 | 真源维度 |
|------|-----------|---------|
| 定义状态 / 开放项 | 这条指标口径定了没？卡在哪个甲方开放项？ | D1 |
| 结构支撑 / 结构缺口 / 结构判定 | 自研表结构（DWD/ES/图）算得出吗？ | D2 |
| 源映射 / 源缺口 | 三方源喂得饱吗？缺什么字段？ | D3 |
| 接入状态 / 接入阶段 | 现在线上跑的是什么数据？接到哪一步了？ | D4 |
| **综合就绪 / 卡点责任方** | 一句话：这条指标现在卡在谁手里？ | 四维汇总 |

「四维评估」列区分两类行：**已评估**（已入 readiness 矩阵，ENT 53 条）与**待评估**（仅有 cfg_metric 8 件套，按旧 mapping_status 降级投影；矩阵补齐后重跑脚本自动升级）。

## 2. 同步操作

```powershell
# gkx-orchestration 根目录（需 .env 有 FEISHU_APP_ID/SECRET；缺失时软失败不报错）
node scripts/sync-feishu-metric-board.mjs            # 真同步（upsert，幂等）
node scripts/sync-feishu-metric-board.mjs --dry-run  # 只看解析结果与计划
```

**何时重跑**：readiness 矩阵更新（D2 核验、D4 阶段推进）、cfg_metric 种子增删、gap catalog 文案变化后。脚本自动建表建列，按「指标ID」upsert，不会产生重复行。

## 3. 建议视图（表建好后在飞书 UI 手动配置一次）

1. **全量总览**（默认表格视图，建表自带）
2. **看板视图**：分组 = 综合就绪 —— 对齐会议主视图，直接看各泳道数量变化
3. **按模块**：表格视图分组 = 模块 —— 各模块负责人自查
4. **数据采购跟踪**：筛选 源映射 ∈ {无源, 待ODS} —— PM/甲方沟通清单
5. **甲方口径待办**：筛选 定义状态 = 草案 —— 配合 `客户决策清单跟踪表.md`

## 4. 综合就绪汇总规则（判定优先级从上到下）

未登记 → 无数据源 → 待口径确认 → 待结构设计（含待首评）→ 待数据源 → 待接入（Mock）/ 接入中 / 可上线。每档对应「卡点责任方」列（口径→王惠+甲方；结构→架构；源→GDF/甲方；接入→数据工厂），映射见配置 `blocker_owner_map`。

## 5. 首批覆盖（2026-08-01）

147 条 = cfg_metric 种子 129（ENT 49 / CHAIN 60 / POLICY 19 / TNIE 1）∪ ENT readiness 矩阵独有 18（KEYPANO 8、STAR 4、GAP-* 未注册占位等）。其中四维已评估 53 条（ENT 矩阵全量）。

## 6. 纪律

- **禁止**在飞书表里手改状态列当真源——下次同步会被矩阵值覆盖；状态变更走矩阵/种子文件提交
- 新增模块矩阵（如 CHAIN）落到 `metrics/metric-readiness-matrix-{模块}.yaml` 后重跑即可，无需改脚本
- 列名改动须同步改 `feishu-metric-board.yaml#field_names`（脚本按名匹配，改名会导致重复建列）
