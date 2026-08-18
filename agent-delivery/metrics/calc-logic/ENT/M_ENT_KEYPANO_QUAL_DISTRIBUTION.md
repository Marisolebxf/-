# 重点企业全景图（M_ENT_KEYPANO_QUAL_DISTRIBUTION）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_KEYPANO_QUAL_DISTRIBUTION`
- **指标名称**：重点企业全景图
- **一级模块**：企业分析
- **二级模块**：企业发展
- **三级模块**：重点企业全景图
- **更新频率**：月度/年度
- **对齐状态**：部分对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q010

## 口径定义

按企业类型（外企/国高企/小微/上市）×行政层级（国家/省/市）进行交叉分组统计企业数量，呈现整链重点企业的资质结构分布。国家、省、市为嵌套统计范围，各层级数量不可相加；同一企业可命中多个资质标签，各资质数量不可相加为企业总数。

## 计算逻辑说明

```
1.企业类型分组：外企(dwd_org_base_info.org_type含外商/外资/中外合资/港澳台)、国高企(dwd_org_tech_tag.org_tag=国家级高新技术企业)、小微(company_basic_tags.scale_tag in 小型/微型)、上市(dwd_org_base_info.listing_status=是)；2.行政层级分组：按province(省级)、city(市级)筛选，全国为全量；3.交叉统计：对每个(类型,层级)组合做COUNT(DISTINCT org_id)；4.产业链范围限定：通过dwd_org_industry_tags关联目标产业链。
```

**计算公式文件**：`M_ENT_KEYPANO_QUAL_DISTRIBUTION.md`

## 源表字段

```
gkx.dwd_org_base_info(org_id, name_cn, org_type, listing_status, province, city) — 企业类型（外企/上市）、行政层级（省/市）
gkx.dwd_org_tech_tag(org_id, org_tag) — 企业资质标签（国高企）
gkx.company_basic_tags(id, scale_tag) — 企业规模标签（小微）
gkx.dwd_org_industry_tags(credit_code, industry_code) — 产业链范围限定
gkx.dwd_org_stock_base(org_id) — 上市企业辅助判定
```

## 待建表字段

```
ads.enterprise_keypano_qual_distribution(industry_code, qual_type, admin_level, enterprise_count) — 整链资质分布预聚合表（未建）；资质有效期与认定层级口径待Q010闭合
```

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
