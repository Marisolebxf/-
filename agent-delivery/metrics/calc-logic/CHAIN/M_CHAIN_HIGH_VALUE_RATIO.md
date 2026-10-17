---
metric_id: M_CHAIN_HIGH_VALUE_RATIO
metric_name_zh: 高价值环节占比
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 公式结构已定；:high_value_enum 值集待 GAP-CHAIN-IMPORTANCE-ENUM
---

# M_CHAIN_HIGH_VALUE_RATIO 高价值环节占比 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：**B 方案归一 L1**。与 `M_CHAIN_SZ_KEY_NODE_COVERAGE` 共用 `importance_level` 字段、共用同一缺口 `GAP-CHAIN-IMPORTANCE-ENUM`（一次问清值域字典 + 标注层级，两指标解锁）。

## 1. 业务定义

高价值环节占比 = 该链高价值 L1 环节数 / 该链全部 L1 环节数 × 100。

- 分母与 `M_CHAIN_REG_ECOSYSTEM` 分母完全相同（全链 L1）；
- 分子 = `importance_level` 命中高价值值集的节点折 L1 去重。

## 2. 数据源与缺口

| 表/字段 | 状态 |
|---|---|
| `demo_gkxlumenx_dwd.industry_chain_node.importance_level`（varchar20） | **DDL 实核存在；live 114 行全 NULL；值集未知** |
| `demo_gkxlumenx_dwd.industry_chain_node`（node_level/parent_node_id） | 分母 + 折 L1 映射 |

**缺口**：`GAP-CHAIN-IMPORTANCE-ENUM`（与 SZ_KEY_NODE_COVERAGE 共用）。

## 3. SQL（锁定待值集）

```sql
SELECT ROUND(100 * hv.hv_cnt / denom.total, 1) AS high_value_ratio_pct
FROM (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, n.node_id)) AS total
      FROM demo_gkxlumenx_dwd.industry_chain_node n
      WHERE n.chain_id = :chain_code AND n.node_level = 1 AND is_deleted = 0) denom,
     (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, n.node_id)) AS hv_cnt
      FROM demo_gkxlumenx_dwd.industry_chain_node n
      WHERE n.chain_id = :chain_code AND n.is_deleted = 0
        AND n.importance_level IN (:high_value_enum)) hv;
```

`:high_value_enum` 为枚举占位，待 GAP 答复后填入实际值集。

注：分子不限 `node_level=1`（供应方可能标在 L2），靠 `COALESCE` 折 L1；分母显式 L1，两侧同为 L1 维度。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |
| `:high_value_enum` | 高价值值集 | **待 GAP-CHAIN-IMPORTANCE-ENUM** |

## 5. 边界语义

- `importance_level` 全 NULL → 分子 0 → 0%？**否**：值集未定前整条指标不出数（NULL，无数据），避免把「未标注」误读为「无高价值环节」。
- 值集定 + 数据灌齐后正常出数。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：QC02 待确认 | — |
| 0.2.0 | 2026-10-14 | B 方案折 L1 + L1 分母同 REG_ECOSYSTEM + 值集 GAP 共用 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
