# 重点企业全景图（M_ENT_KEYPANO_ENTERPRISE_LIST）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_KEYPANO_ENTERPRISE_LIST`
- **指标名称**：重点企业全景图
- **一级模块**：企业分析
- **二级模块**：企业发展
- **三级模块**：重点企业全景图
- **更新频率**：产业链标签更新后
- **对齐状态**：部分对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q038

## 口径定义

按目标产业链环节（上游/中游/下游）归集重点企业清单，展示每个链位下的重点企业及其基础信息（名称、注册区县、企业类型、链位、资质标签）。重点企业判定基于产业链关联表与企业规模/资质筛选。

## 计算逻辑说明

```
1.链位归集：dwd_org_industry_tags关联dwd_industry_chain_info按level（上游/中游/下游）分组企业；2.重点企业筛选：结合dwd_org_tech_tag（高新/专精特新/小巨人）、dwd_org_base_info（上市状态、企业类型）筛选；3.企业清单组装：关联dwd_org_base_info获取企业名称、注册区县、企业类型等，关联dwd_org_tech_tag获取资质标签；4.按链位分页展示。
```

**计算公式文件**：`M_ENT_KEYPANO_ENTERPRISE_LIST.md`

## 源表字段

```
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联（链位归集）
gkx.dwd_industry_chain_info(industry_code, industry_link_code, level, chain_name) — 产业链节点层级与链位名称
gkx.dwd_org_base_info(org_id, name_cn, external_id, area, org_type, listing_status, lerep) — 企业基础信息（名称、区县、类型、上市状态、法人）
gkx.dwd_org_tech_tag(org_id, org_tag) — 企业资质标签（高新/专精特新/小巨人）
```

## 待建表字段

```
ads.enterprise_keypano_node_enterprise_list(industry_code, link_level, org_id, org_name, area, org_type, qualifications, chain_node) — 重点企业按链位归集的ADS视图（未建）；产业链映射表（待建）
```

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
