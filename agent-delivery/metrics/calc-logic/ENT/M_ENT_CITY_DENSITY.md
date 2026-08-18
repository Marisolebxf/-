# 城市企业密度（M_ENT_CITY_DENSITY）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CITY_DENSITY`
- **指标名称**：城市企业密度
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：多城市对标排名
- **更新频率**：年度
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q016

## 口径定义

各城市该未来产业范围内去重企业数 / 城市辖区面积(百km2)。

## 计算逻辑说明

```
COUNT(DISTINCT credit_code) / 城市辖区面积(百km2)。
```

**计算公式文件**：`M_ENT_CITY_DENSITY.md`

## 源表字段

```
gkx.dwd_org_industry_tags(credit_code, industry_name)
gkx.dwd_org_base_info(org_id, city)
```

## 备注

1.1.1.2.4.2.3.5.2；城市辖区面积需外部数据

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
