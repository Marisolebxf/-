# 管道 · DWD → ADS（政策）

```yaml
---
doc_id: POLICY-ETL-DWD-TO-ADS
element: POLICY
role: etl
status: as-built
version: "2026-08-31"
updated: 2026-08-31
engine: mysql
task_id: DATA-POLICY-STORAGE-ETL-FILL-L01
---
```

> ADS 表结构真源 [`../stores/mysql/ads.md`](../stores/mysql/ads.md)（S3 draft）。本文件写**谁写了哪张表、按什么顺序、怎么幂等**。
> Java **只读**本层，不参与本管道。

## 意图

从 DWD 单表 `policy_base_info` 算出全部政策 ADS 面。政策域**没有** DWD 宽表中间层——每个算法模块直接读 DWD 明细，各自产出自己的 ADS 表。

## 写入图（as-built · `polan`）

| 步 | 模块 | 产出 ADS 表 |
|---|---|---|
| A | `basic/indicators.py` | `policy_level_dist` · `policy_type_dist` · `policy_timeseries` · `policy_national_dist` · `policy_sz_dist` |
| B | `graph/entity.py` | `policy_entity` · `policy_graph_node` · `policy_graph_edge` |
| B+ | `graph/nebula_loader.py` | 不写 ADS，**读** 上面两张图表投影 Nebula（见 [`pipeline-to-nebula.md`](./pipeline-to-nebula.md)） |
| C1 | `eval/focus.py` | `policy_focus` |
| C2 | `eval/intensity.py` | `policy_intensity` · `policy_metric_timeseries` |
| C3 | `eval/effect.py` | `policy_effect` · `policy_metric_timeseries` |
| C4 | `eval/gap.py` | `policy_effect`（短板列） |
| C5 | `eval/opportunity.py` | `policy_focus`（机遇列） |
| C6 | `eval/layout.py` | `policy_effect`（布局列） |
| D1 | `text/parse.py` | `policy_text_parse` |
| D2 | `text/match.py` | `policy_match` |
| D3 | `text/simulate.py` | `policy_simulate` |

> ⚠️ **S3 未登记四张表**：`policy_entity` / `policy_text_parse` / `policy_match` / `policy_simulate` 实际已被写入，但 [`../stores/mysql/ads.md`](../stores/mysql/ads.md) 只登记了九张指标表 + 两张图镜像。补登属 S3 细表变更，走 `OPEN-POLICY-GRAPH-03` 同批升级 `human:淮政玮`，**不在本叶静默改 S3**。

## 顺序约束（不可随意打乱）

多个模型共写同一张表，靠**步序**而非表锁保证正确：

1. `policy_focus`：C1 先建基线，C5 再补机遇列。
2. `policy_effect`：C3 先建基线，C4 补短板列，C6 补布局列。
3. **C6 `layout` 必须在 C5 `opportunity` 与 C4 `gap` 之后**（`eval/layout.py` 显式声明该依赖，`run_all_policy` 已保证）。
4. `policy_metric_timeseries`：C2 与 C3 各写自己的维度行，互不覆盖。

单独重跑某个模型是安全的（各模型写前只删自己拥有的 rowset）；但**跳过前置直接跑 C6 会读到空基线**。

## 幂等

| 模块 | 策略 |
|---|---|
| `basic` / `eval` / `text` | 写前删除**自己拥有的 rowset**，可单独重跑 |
| `graph/entity.py` | 先 `TRUNCATE` 三张表再整体重写 |
| 批次标识 | `calc_batch_id`；Mock 批次前缀 `mock_`，用于区分非 live 数据 |

## 调度

| 项 | 值 |
|---|---|
| 编排 | `python scripts/run_all_policy.py` → `build_steps()` 第 4–15 步 |
| 增量语义 | ODS/DWD 走差集增量，**ADS 一律按当前 DWD 全量重算**，不做 ADS 增量 |
| 查询期降级 | `polan/metrics/metrics.py`：ADS 表空或不可用时返回 mock 并标注口径，**不回写 ADS** |

## 禁止

Java 写 ADS 或直连 nGQL；把查询期 mock 降级结果回写 ADS 冒充 live；跳过顺序约束重跑；把 fixture 计数写进指标表（`OPEN-POLICY-DISP-*` 缺表项一律诚实空 + 角标）。
