# 营业收入增长率（M_ENT_REVENUE_GROWTH_RATE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_REVENUE_GROWTH_RATE`
- **指标名称**：营业收入增长率
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：年度
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

企业本年营业收入总额同上年营业收入总额差值的比率。

## 计算逻辑说明

```
营收增长率 = (本期 - 上期) / 上期 * 100%。从dwd_org_stock_finance_info取连续两期数据。
```

**计算公式文件**：`M_ENT_REVENUE_GROWTH_RATE.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id, operating_revenue, year）— 年报营业收入（按年报年度）
计算公式：营收增长率 = (本期 operating_revenue - 上期 operating_revenue) / 上期 operating_revenue x 100%
```

## 备注

1.1.1.2.4.2.3.4；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
