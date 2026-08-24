# TOPIC-DS-METRIC-GAP-L01 · 专题+展示 vs 算法库差集索引（L02 收口）

> 父单索引。不替代子叶 yaml/xlsx。  
> 日期：2026-08-24 · 监管 `human:淮政玮`  
> **对照真源改为 L02**（A1 成品表回填）。L01 冻结为 OPEN 指针快照，不作 A1 对照签收。

## 子叶

| 叶 | 角色 | 状态 | 主交付 missing | 四件套 |
|----|------|------|----------------|--------|
| `TOPIC-ALGO-GAP-L01` | Round 17 指针快照 | 冻结 `in_progress`（不作对照签收） | 7 | `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.*` |
| `DS-ALGO-GAP-L01` | Round 18 指针快照 | 冻结 `in_progress`（不作对照签收） | 70 | `metrics/request/展示系统/DS-ALGO-GAP-L01.*` |
| `TOPIC-ALGO-GAP-L02` | A1 回填 · 专题 | **done**（human:淮政玮 签收） | **7→7** | `metrics/request/专题系统/TOPIC-ALGO-GAP-L02.*` |
| `DS-ALGO-GAP-L02` | A1 回填 · 展示 | **done**（human:淮政玮 签收） | **70→70** | `metrics/request/展示系统/DS-ALGO-GAP-L02.*` |

## 合计（机器真源 = L02 yaml）

| 口径 | 专题 L02 | 展示 L02 | 说明 |
|------|----------|----------|------|
| 清单行 | 250 | 930 | 展示含 FANIN 数据需求 1 行 |
| **missing 主清单** | **7** | **70** | 展示已去掉 `M_POLICY_INDUSTRY_FIT`（also_in E7-POLICY） |
| mapped（已填 A1 ID） | 171/171 | 204/204 | `TEMP_ALGO_*` 只进列 13 |
| third_party | 10（9 填 A1） | 16（14 填 A1） | 专题 `TOPIC-RORG-012`、展示投融资两行无对应叶 |
| 语义欠账 | 111 | 247 | 不进主清单 |

改判定行：专题 **0**，展示 **0**。禁止把 missing 改 mapped 充数。

## 共有缺口（只标一次）

| metric_id / 主项 | 专题页 | 展示页 | 处理 |
|------------------|--------|--------|------|
| `M_POLICY_INDUSTRY_FIT` 产业适配性 | E7-POLICY | DS-10-POLICY-PANORAMA | 主清单只留专题；展示 items 保留 also_in |

其余展示 70 条与专题 7 条无 ID 级重复。B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*` 两叶均未打 missing。

## 拆单（已建，本父单不重做分析）

| ID | 用途 |
|----|------|
| `TOPIC-ALGO-GAP-L01` / `DS-ALGO-GAP-L01` | OPEN 指针返工（冻结） |
| `TOPIC-ALGO-GAP-L02` / `DS-ALGO-GAP-L02` | A1 成品表回填（本索引消费） |
| `ALGO-LIB-SEED-TYPE-L01` | 已签类型写入 seed（并行，不挡本索引） |
| `ALGO-LIB-T0X-L01` | T0-X 四桶会（ready · pull）；输入 = 本索引 + A1 双表；SEED-TYPE 不作硬依赖 |

## 不做

- 不改 seed、不发明正式 `M_*`、不覆盖半成品 xlsx、不写业务代码。
- 教育核增 / 政策对比核增 / 抗疫核减仍 skip。
- 不开 OPEN 贴源 / GDF（右框等 T0-X 会后按桶拆）。T0-X 已开 `ALGO-LIB-T0X-L01`。
- 不把 L01 签成 A1 对照。
