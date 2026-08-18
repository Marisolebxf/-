# 利润率（M_ENT_PROFIT_MARGIN）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PROFIT_MARGIN`
- **指标名称**：利润率
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

企业最新完整年度利润总额占营业收入的百分比。

## 计算逻辑说明

```
利润率 = pure_profit / operating_revenue * 100%。从dwd_org_stock_finance_info取值。
```

**计算公式文件**：`M_ENT_PROFIT_MARGIN.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id, pure_profit, operating_revenue, year）— 年报净利润与营业收入
计算公式：利润率 = pure_profit / operating_revenue x 100%
```

## 备注

1.1.1.2.4.2.3.4；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
