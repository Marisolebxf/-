---
metric_id: M_CHAIN_SZ_KEY_NODE_COVERAGE
metric_name_zh: 深圳关键环节覆盖率
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 公式结构已定；:key_node_enum 值集待 GAP-CHAIN-IMPORTANCE-ENUM
---

# M_CHAIN_SZ_KEY_NODE_COVERAGE 深圳关键环节覆盖率 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：**B 方案归一 L1**。「环节」= `industry_chain_node` 行（链下节点）；「关键」= 供应方 `importance_level` 标记命中关键值集。两侧统一 `COALESCE(parent_node_id, node_id)` 折 L1——与 REG_ECOSYSTEM / SZ_COMPLETENESS 家族同构；在标注层级未知时对供应方标注**稳健**（若关键性标在 L2 而上链记在 L1，精确匹配会系统性失配）。

## 1. 业务定义

深圳关键环节覆盖率 = 深圳企业覆盖的关键 L1 环节数 / 该链关键 L1 环节总数 × 100。

## 2. 数据源与缺口

| 表/字段 | 状态 |
|---|---|
| `demo_gkxlumenx_dwd.industry_chain_node.importance_level`（varchar20） | **DDL 实核存在；live 114 行全 NULL；值集未知** |
| `demo_gkxlumenx_dwd.enterprise_industry_chain` | 上链桥 |
| `demo_gkxlumenx_ods.dwd_org_base_info` | 深圳判定（`city='深圳市'`） |

**缺口**：`GAP-CHAIN-IMPORTANCE-ENUM` —— 找供应方要 `importance_level` 值域字典 + 标注层级（一次问清，与 `M_CHAIN_HIGH_VALUE_RATIO` 共用，两指标解锁）。

## 3. SQL（锁定待值集）

```sql
SELECT ROUND(100 * cov.covered / denom.total, 1) AS key_node_coverage_pct
FROM (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, n.node_id)) AS total
      FROM demo_gkxlumenx_dwd.industry_chain_node n
      WHERE n.chain_id = :chain_code AND n.is_deleted = 0
        AND n.importance_level IN (:key_node_enum)) denom,
     (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, e.node_id)) AS covered
      FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
      JOIN demo_gkxlumenx_ods.dwd_org_base_info b
        ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = '深圳市'
      LEFT JOIN demo_gkxlumenx_dwd.industry_chain_node n
        ON n.node_id = e.node_id AND n.is_deleted = 0
      WHERE e.chain_code = :chain_code
        AND n.importance_level IN (:key_node_enum)) cov;
```

`:key_node_enum` 为枚举占位，待 GAP 答复后填入实际值集（如 `('关键','核心')`）。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |
| `:key_node_enum` | 关键环节值集 | **待 GAP-CHAIN-IMPORTANCE-ENUM** |

## 5. 边界语义

- `importance_level` 全 NULL → 分母 0 → NULL（无数据），如实展示，不伪造。
- 分母 0 或数据未灌不产生伪覆盖率。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：QC02 待确认，is_key_node 字段不存在 | — |
| 0.2.0 | 2026-10-14 | B 方案折 L1 + importance_level 判定 + 值集 GAP | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
