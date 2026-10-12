# 核心供应商数（M_ENT_CORE_SUPPLIER_COUNT）

> 口径真源：算法 2026-09 拉回 Q017 ②（供应集合内投资金额 TOP5）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 丢掉 `risk_level=高`。禁止读 `is_core_supplier`。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖

| 顺序 | 表 | 用它做什么 |
|------|-----|------------|
| 1 | `enterprise_supply_chain` | 直接一级供应商（`relation_type='supplier'`） |
| 2 | `enterprise_invest` | 本企→该供应商的 `invest_amount` |
| 3 | 本条 | TOP5 后 COUNT。目标 `enterprise_supply_summary.core_supplier_count`，**当前无此表** |

## 元数据

- 指标ID：`M_ENT_CORE_SUPPLIER_COUNT`
- 名称：核心供应商数
- 更新频率：周
- 关联Q：Q017（团队默认 🟢）
- 对齐：D1 aligned

## 口径定义

每个企业一条：

```
供应集合 S = DISTINCT related_org_id
  FROM enterprise_supply_chain
  WHERE org_id = :id AND relation_type = 'supplier'

核心 = S 中与 enterprise_invest 配上的行
  投资方 = :id AND 被投 = 该供应商
  ORDER BY invest_amount DESC
  取 TOP5（金额空不进；并列都进）

core_supplier_count = COUNT(DISTINCT 核心供应商)
```

- 一级 = 边自身，不筛 `relation_level`。
- 不足 5 个有金额：有几个算几个（0～5；并列可能 >5）。
- **禁止** `risk_level`、`is_core_supplier`、`chain_score`、股东表。
- 只国内。不挂产业。

## 两点分开

### ① 口径

供应边 + 投资金额列在就能算。

### ② 有没有数

灌数 / mock 边另写，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_supply_chain` + `enterprise_invest` | 有表 |
| 目标 | `enterprise_supply_summary.core_supplier_count` | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。

## 分场景 / 实现方案

### 场景 A · 单企画像

入参 `:org_id`。有目标表读计数。没有则按口径现算，结果不写 live。

### 场景 B · 列表

按 `org_id` 读目标表。禁止请求路径全表现算 TOP5。

### demo / 生产

生产周 ETL 写目标表。查询带 `org_id`。

## 源表字段

```
enterprise_supply_chain
enterprise_invest <- ods: dwd_org_invest_info
```

来源系统：国内机构要素库。

## 待建 / 缺口

1. **无独立目标表**（只有这一条挡落库）。
2. D3/D4 本波不升。`is_mock: true`。

---
*2026-09-07 COVER-STAT-L01：0.3.1 拉回投资 TOP5；能算；只缺目标表；D1 aligned*
