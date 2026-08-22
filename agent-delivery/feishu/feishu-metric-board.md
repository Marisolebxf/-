# 飞书「指标与数据开发进度」看板使用指南

> **日期**：2026-08-22 · **任务**：ORCH-METRIC-BOARD-L01（监管 human:淮政玮）
> **三张投影之一**（指标对象 / A1 算法库叶子 / A2 页面差集）。不要把 WBS、给人说明、xlsx、王惠表再投影成第四张。
> **真源分层**：`metrics/registry/metric-readiness-matrix-*.yaml`（四维就绪度）+ `metrics/registry/cfg_metric-*-seed.yaml`（8 件套）+ 各模块 `*data-gap-catalog.yaml`（缺口文案）= 唯一真源；飞书 = **只读投影**
> **配置**：[`feishu-metric-board.yaml`](./feishu-metric-board.yaml) · **模型**：[`../data-lineage-policy.md`](../data-lineage-policy.md) §2 / §2.3（D9 v1.5）

## 1. 看板定位

与任务看板同一个多维表格应用里的独立数据表「**指标与数据开发进度**」，一行 = 一个 `metric_id`。

| 列组 | 回答的问题 | 真源 |
|------|-----------|------|
| 算法类型 | STAT 还是 MODEL？未填 = `UNKNOWN`（禁止派实现单） | seed `algorithm_type` |
| 专题维度Owner | 这个专题功能谁推进；STAT 的 Java 就是此人 | 梳理 §2.3（前缀推断） |
| 合同集合 | F∩L / F−L / L−F / 未分拣 | A2 `mapped`→F∩L；其余未分拣（L−F 等 T0-X 手标） |
| 填齐阶段 | 定义/公式/源填到哪一关 | 矩阵 `lifecycle_stage`（未填 = 未标） |
| 定义状态 / 开放项 | 口径定了没？ | D1 |
| 结构 / 源 / 接入 | 算不算得出、喂不喂得饱、线上什么数 | D2 / D3 / D4 |
| **综合就绪 / 卡点责任方** | 现在卡在谁手里？ | 四维汇总；口径卡点 = **淮政玮 + 甲方** |

「四维评估」列：**已评估**（已入 readiness 矩阵）与**待评估**（仅 8 件套，按旧 `mapping_status` 降级）。

## 2. 同步操作

```powershell
node scripts/sync-feishu-metric-board.mjs            # 真同步（upsert，幂等）
node scripts/sync-feishu-metric-board.mjs --dry-run  # 只看解析结果与计划
```

K8s Cron 经 `scripts/feishu-bitable-cron-sync.mjs` 出站。无 `FEISHU_*` 凭据时软失败。

**何时重跑**：registry 矩阵/种子更新、gap catalog 变化、A2 pages 差集判定变化（影响合同集合）。

## 3. 建议视图（飞书 UI 手动配一次）

1. **全量总览**（默认表格）
2. **看板**：分组 = 综合就绪 —— **STAT 不得出现在「待算法实现」**
3. **按模块** / **按专题维度Owner**
4. **数据采购**：源映射 ∈ {无源, 待ODS}
5. **甲方口径待办**：定义状态 = 草案
6. **类型未定**：算法类型 = UNKNOWN
7. **未分拣**：合同集合 = 未分拣（T0-X 会前主视图）

## 4. 综合就绪（优先级从上到下）

未登记 → 无数据源 → 待口径确认 → 待结构设计 → 待数据源 → 待接入（Mock）/ 接入中 / 可上线。

**「待算法实现」只给 MODEL / GRAPH / COMPUTE / MIXED。** STAT / API 的 `🔧` 走「待结构设计」，卡点写成 `STAT Java（{Owner}）+ GDF ADS`。`UNKNOWN` + `🔧` 走「待口径确认」（先定类型，不派唐绍祖）。

卡点：口径 → **淮政玮 + 甲方**；模型算法 → 唐绍祖；结构 → 架构 / STAT 则模块负责人；源 → GDF/甲方；接入 → 数据工厂。

## 5. 纪律

- **禁止**在飞书手改当真源——下次同步覆盖；状态走 registry YAML
- **禁止**改已有列的中文名（脚本按名匹配，改名会重复建列）；新列由脚本补建
- 新增模块矩阵落到 `metrics/registry/` 后重跑即可
- 王惠进度表已停更，不要把口径卡点写回王惠
