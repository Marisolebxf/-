---
metric_id: M_CHAIN_SZ_COMPLETENESS
metric_name_zh: 深圳产业链完整度
algorithm_type: STAT
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 口径已定（复用 REG_ECOSYSTEM 深圳特例）
---

# M_CHAIN_SZ_COMPLETENESS 深圳产业链完整度 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板：本指标 = `M_CHAIN_REG_ECOSYSTEM`（区域环节完整度）在 `region_city='深圳市'` 的**特例**，口径完全复用不另立。细稿引用 REG_ECOSYSTEM 文档（`M_CHAIN_REG_ECOSYSTEM.md`）不复制逻辑，避免两处漂移。旧稿 QC01「按节点数/按企业覆盖/按产值覆盖」三选一废弃，统一落 L1 节点覆盖版。

## 1. 业务定义

深圳产业链完整度 = 深圳企业覆盖的 L1 环节数 / 该链全部 L1 环节数 × 100。

- **L1 口径**沿用此前「用L1先」拍板，与 REG_ECOSYSTEM 同构（同页家族指标口径一致）。

## 2. 数据源

| 表 | 用途 |
|---|---|
| `demo_gkxlumenx_dwd.industry_chain_node` | 分母：该链 L1 环节（`node_level=1 AND is_deleted=0`） |
| `demo_gkxlumenx_dwd.enterprise_industry_chain` | 上链桥（`chain_code=:chain_code`） |
| `demo_gkxlumenx_ods.dwd_org_base_info` | 深圳判定（`city='深圳市' AND is_deleted=0`） |

## 3. SQL

```sql
SELECT ROUND(100 * cov.covered / denom.total, 1) AS sz_completeness_pct
FROM (SELECT COUNT(*) AS total
      FROM demo_gkxlumenx_dwd.industry_chain_node
      WHERE chain_id = :chain_code AND node_level = 1 AND is_deleted = 0) denom,
     (SELECT COUNT(DISTINCT COALESCE(n.parent_node_id, e.node_id)) AS covered
      FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
      JOIN demo_gkxlumenx_ods.dwd_org_base_info b
        ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = '深圳市'
      LEFT JOIN demo_gkxlumenx_dwd.industry_chain_node n
        ON n.node_id = e.node_id AND n.is_deleted = 0
      WHERE e.chain_code = :chain_code) cov;
```

与 REG_ECOSYSTEM 唯一差异：`:region_city` 绑定常量 `'深圳市'`。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码 | 必填 |

## 5. 边界语义

- 分母 0（链无 L1 节点）→ NULL，UI 显「无数据」，不伪造 0%。
- 上链桥当前 0 行 → 真数 0%，如实展示（数据事，不挡口径）。

## 6. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：QC01 三选一待确认 | — |
| 0.2.0 | 2026-10-14 | 复用 REG_ECOSYSTEM 深圳特例，L1 口径定版 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
