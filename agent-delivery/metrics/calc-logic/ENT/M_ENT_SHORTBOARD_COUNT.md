# 短板指标数（M_ENT_SHORTBOARD_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_SHORTBOARD_COUNT`
- **指标名称**：短板指标数
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：综合竞争力评估
- **更新频率**：年度/基准更新时
- **对齐状态**：未对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014

## 口径定义

指在企业综合竞争力评价指标体系中，企业表现低于预设基准的指标个数。

## 计算逻辑说明

```
将各指标实际值与预设基准值（同行业平均值）逐一比较，低于基准的指标计为短板并统计总数。
```

**计算公式文件**：`M_ENT_SHORTBOARD_COUNT.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, total_assets, total_liabilities, development_employee, employees_number, year) — 企业规模（资产总额、从业人员数）、财务状况（营业收入利润率、资产负债率、总资产周转率）、人力资源（研发人员占比）、市场表现（市场占有率、销售收入），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 各维度同行业均值基准计算的行业归属
```

## 待建表字段

```
同业基准结果集(各指标同行业平均值/目标值) — 各指标基准阈值（现库无此表，待建）
```

## 备注

1.1.1.2.4.2.3.10；需求文档未明确构建方法，参考V3/权威机构方案

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
