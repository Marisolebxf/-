# 类型占比（M_ENT_TYPE_RATIO）

> 口径真源：派生自 COUNT / MATCH → 2026-08-27 COVER-STAT-L01；**2026-08-30 随 TYPE_COUNT：六类含小微均可算，判定走 tag_code**。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TYPE_RATIO`
- **指标名称**：类型占比
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：日
- **对齐状态**：六类分子随 COUNT；不再「小微无法计算」
- **关联Q编号**：Q010（随 COUNT）

## 口径定义

六类各自：`M_ENT_TYPE_COUNT[类型] / M_ENT_TYPE_MATCH_COUNT * 100`。

- 类型名单同 COUNT：外资 / 高新 / 小微 / 上市 / 专精特新 / 小巨人（`tag_code` 见 COUNT）。
- 分母是 MATCH（所选产业下匹配企业去重），不是企业总数。
- 一企可进多类，**占比合计可以超过 100%**。
- MATCH=0 时该类占比无法计算（除零）。小微分子现可算。
- 只国内。选产业已含在分子分母里，本条不再另写 JOIN。

本条不重写六类落地；落地见 `M_ENT_TYPE_COUNT.md`。①/② 随 COUNT：DWD 能数，ODS 灌数另写。

## 计算逻辑说明

```
对每一类 t ∈ {foreign, high_tech, sme, listed, little_giant, little_giant_pro}:
  RATIO[t] = TYPE_COUNT[t] / TYPE_MATCH_COUNT * 100

MATCH = 0: 该类无法计算
```

**计算公式文件**：`M_ENT_TYPE_RATIO.md`

## 源表字段

与 COUNT 同链（派生不另找表）：

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

不写 `is_listed`。来源系统：国内机构要素库、产业链要素库。

## 落表

派生。目标建议随 COUNT 同批写 `type_ratio` 列，或查询时相除。无独立事实表不算缺口。

## 待建 / 缺口

- D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.1`；STAT。

---
*2026-08-27 派生占比；2026-08-30 小微可算，判定随 tag_code*
