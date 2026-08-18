# 企业科研人数（M_ENT_RESEARCHER_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_RESEARCHER_COUNT`
- **指标名称**：企业科研人数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：年度
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E32-01

## 口径定义

选定未来产业范围内的企业科研人员总数。

## 计算逻辑说明

```
先从dwd_org_industry_tags筛选目标未来产业企业，关联dwd_org_annual_financial_info取development_employee，SUM求和。
```

**计算公式文件**：`M_ENT_RESEARCHER_COUNT.md`

## 源表字段

```
gkx.dwd_org_industry_tags（credit_code, industry_name）— 未来产业筛选
gkx.dwd_org_annual_financial_info(org_id,development_employee)
gkx.dwd_foreign_org_annual_financial_info(org_id,rd_staff)
**研发人员来源说明**：国内企业优先取 dwd_org_annual_financial_info.development_employee；海外企业补充取 dwd_foreign_org_annual_financial_info.rd_staff；不得用 employees_number 替代研发人员口径。
**关联说明**：dwd_org_industry_tags.credit_code与
gkx.dwd_org_base_info(org_id,external_id)对齐
gkx.dwd_forg_base_info(org_id,external_id)对齐
```

## 备注

1.1.1.2.4.2.3；研发人员优先取年报development_employee

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
