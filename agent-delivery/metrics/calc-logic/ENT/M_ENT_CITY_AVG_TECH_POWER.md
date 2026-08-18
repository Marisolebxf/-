# 城市平均技术力（M_ENT_CITY_AVG_TECH_POWER）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CITY_AVG_TECH_POWER`
- **指标名称**：城市平均技术力
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：多城市对标排名
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014

## 口径定义

各城市该未来产业范围内企业的技术力得分均值。

## 计算逻辑说明

```
AVG(企业技术力得分) WHERE 城市=c AND 产业=i。依赖ads_ent_tech_score结果表。
```

**计算公式文件**：`M_ENT_CITY_AVG_TECH_POWER.md`

## 源表字段

```
gkx.dwd_org_industry_tags(credit_code, industry_name)
```

## 待建表字段

```
目标结果表 ads_ent_tech_score(tech_score, 待建)
```

## 备注

1.1.1.2.4.2.3.5.2；依赖M_ENT_TECH_POWER_SCORE；结果表待建

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
