# 企业集聚指数（M_ENT_CLUSTER_INDEX）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CLUSTER_INDEX`
- **指标名称**：企业集聚指数
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：年度
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q012

## 口径定义

用区位熵衡量某区域在目标产业上的相对集聚程度，LQ>1表示相对集聚。

## 计算逻辑说明

```
LQ = (区域r产业i企业数/区域r企业总数) / (全样本产业i企业数/全样本企业总数)。
```

**计算公式文件**：`M_ENT_CLUSTER_INDEX.md`

## 源表字段

```
gkx.dwd_org_industry_tags（credit_code, company_name, industry_code）
gkx.dwd_org_base_info（name_cn, province, city）
```

## 备注

1.1.1.2.4.2.3.1；需求文档未明确构建方法，参考V3/权威机构方案

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
