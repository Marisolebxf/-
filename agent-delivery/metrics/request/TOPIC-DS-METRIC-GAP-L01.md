# TOPIC-DS-METRIC-GAP-L01 · 专题+展示 vs 算法库差集索引

> 父单索引。两子叶四件套已齐；本文件只做入口，不替代子叶 yaml/xlsx。  
> 日期：2026-08-22 · 监管 `human:淮政玮` · 截止 2026-08-24 下班前。

## 子叶

| 叶 | 状态（registry） | 主交付 missing | 四件套 |
|----|------------------|----------------|--------|
| `TOPIC-ALGO-GAP-L01` | `ready_to_sign` | **7** | `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.{yaml,xlsx,summary.md,md}` |
| `DS-ALGO-GAP-L01` | FANIN 已交，待签收 | **70**（去专题重复后） | `metrics/request/展示系统/DS-ALGO-GAP-L01.{yaml,xlsx,summary.md,md}` |

## 合计（机器真源以各叶 yaml 为准）

| 口径 | 专题 | 展示 | 说明 |
|------|------|------|------|
| 清单行 | 250 | 930 | 展示含 FANIN 数据需求 1 行 |
| **missing 主清单** | **7** | **70** | 展示已去掉 `M_POLICY_INDUSTRY_FIT`（`also_in: E7-POLICY`） |
| mapped | 171 | 204 | 只保留对应 |
| 语义欠账 | 111 | 247 | 不进主清单 |

## 共有缺口（只标一次）

| metric_id / 主项 | 专题页 | 展示页 | 处理 |
|------------------|--------|--------|------|
| `M_POLICY_INDUSTRY_FIT` 产业适配性 | E7-POLICY | DS-10-POLICY-PANORAMA | 主清单只留专题；展示 items 保留 also_in |

其余展示 70 条与专题 7 条无 ID 级重复。B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*` 两叶均未打 missing。

## 不做

- 不改 seed、不发明正式 `M_*`、不覆盖半成品 xlsx、不写业务代码。
- 教育核增 / 政策对比核增 / 抗疫核减仍 skip。
- 本索引不把父单改为 done；签收仍走两叶 spike → `ready_to_sign`，父单由 coordinator / 淮政玮推进。
