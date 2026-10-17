---
metric_id: M_CHAIN_SZ_ADVANTAGE_RANK
metric_name_zh: 深圳优势排名
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 读表版口径已定（结构先定，无数据不挡口径）
---

# M_CHAIN_SZ_ADVANTAGE_RANK 深圳优势排名 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：MODEL 类指标已有目标表存储 → **基于表结构先定一版，无数据是另一回事**。排名算法本体（优势评分怎么算）归 MODEL 父指标 `M_CHAIN_SZ_ADVANTAGE_SCORE` 与算法侧；本条只定**读表口径**。

## 1. 业务定义

深圳优势排名 = MODEL 产出的深圳在指定产业链对标城市中的排名（`rank_no` 直读）。

## 2. 数据源（DDL 实核）

| 表 | 关键字段 | 现状 |
|---|---|---|
| `demo_gkxlumenx_dwd.industry_chain_model_result_detail`（42 字段） | `rank_no`（int）、`result_value`、`benchmark_id`、`region_code`、`metric_id`、`chain_id` | **0 行**（模型未跑） |
| `demo_gkxlumenx_dwd.industry_chain_model_run` | `run_id`、`created_time`（最新 run 判定） | run 主表 |

## 3. SQL

```sql
SELECT d.rank_no, d.result_value, d.benchmark_id
FROM demo_gkxlumenx_dwd.industry_chain_model_result_detail d
JOIN demo_gkxlumenx_dwd.industry_chain_model_run r
  ON r.run_id = d.run_id AND r.is_deleted = 0
WHERE d.is_deleted = 0
  AND d.chain_id = :chain_code
  AND d.metric_id = 'M_CHAIN_SZ_ADVANTAGE_SCORE'
  AND d.region_code = '440300'   -- 深圳
ORDER BY r.created_time DESC, d.rank_no ASC
LIMIT 1;   -- 取最新一次 run
```

- 表 0 行 / 无匹配 → NULL，UI 显「无数据」，不伪造排名。
- 多次 run 并存时取 `created_time` 最新，防止读到历史快照。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |

## 5. 未决项（不挡读表口径）

- **QC08 对标城市集合**：继续挂 🟡 客户决策清单——影响模型怎么算（评分与对比范围），不影响本读表 SQL。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：QC08 待确认，RANK() OVER 草案 | — |
| 0.2.0 | 2026-10-14 | 读表版 rank_no 直读 + 最新 run；QC08 转 🟡 决策清单跟踪 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
