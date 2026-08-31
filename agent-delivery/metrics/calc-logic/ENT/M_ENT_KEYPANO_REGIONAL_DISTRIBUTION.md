# 区域分布（M_ENT_KEYPANO_REGIONAL_DISTRIBUTION）

> 口径真源：整链重点名单按区域键 COUNT → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 KEY_TOTAL + 上链 + `region_id` + 复合成员。无类型维。  
> **① DWD 能数**：`region_id` 在就能出各区域家数。  
> **② ODS→DWD**：绑码灌数另写。  
> **选链/选区不进口径**：ETL 全量；API 按键查。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点名单 |
| 2 | `enterprise_industry_chain` | 上了哪条链 |
| 3 | `enterprise_base.region_id` + `region_scope_member` | 区域键 |
| 4 | 本条 | `(chain_code, region_key)` 一格 COUNT |

不是覆盖区域数（有几个区域 ≥1）。不是资质交叉（带类型）。

## 元数据

- 指标ID：`M_ENT_KEYPANO_REGIONAL_DISTRIBUTION`
- 名称：区域分布
- 模块：E-33 重点企业概览
- 更新频率：周
- 关联Q：Q012；Q056🟢；名单 Q038

## 口径定义

整链重点名单，按区域键数有多少家。

区域键：`nation:CN` + 省 2 + 市 4 + 县 6 + `scope:gba|yrd|jjj`。热门城市并入市。

```
COUNT(DISTINCT org_id)
WHERE org_id ∈ 该链重点名单
  AND 该企点亮 :region_key
GROUP BY chain_code, region_key
```

嵌套不可加。大湾区与广东可重叠，不可加。只国内。主粒度 = 整链。

选链 / 选区是 API 过滤。

## 两步分开

① `region_id` + 成员表 + 名单 + 上链在即可数。  
② ODS 绑码另写，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 名单 + 上链 + `region_id` + DIM 成员 | 表在 |
| 目标 | `enterprise_keypano_chain_region_detail`（`chain_code + region_key + ent_count`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级

ETL 全量链 × 区域键。API 只读。禁止请求路径现算。

**计算公式文件**：`M_ENT_KEYPANO_REGIONAL_DISTRIBUTION.md`

## 源表字段

```
enterprise_industry_chain
enterprise_base.region_id
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

维表不进 `source_systems`。来源系统：国内机构要素库、产业链要素库。

## 待建 / 缺口

无独立目标表。D3/D4 本波不升。`is_mock: true`。

---
*2026-08-30 COVER-STAT-L01：整链按区域键 COUNT；含县与复合区域*
