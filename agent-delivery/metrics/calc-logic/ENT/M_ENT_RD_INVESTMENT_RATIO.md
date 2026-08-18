# 研发投入强度（M_ENT_RD_INVESTMENT_RATIO）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_RD_INVESTMENT_RATIO`
- **指标名称**：研发投入强度
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：年度
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

报告期内企业R&D经费支出占营业收入的比例。

## 计算逻辑说明

```
研发投入强度 = `arch development am` / operating_revenue * 100%。
```

**计算公式文件**：`M_ENT_RD_INVESTMENT_RATIO.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id, year, `arch development am`, operating_revenue）— 研发投入金额与营业收入（优先年报）
计算公式：研发投入强度 = `arch development am` / operating_revenue x 100%
```

## 备注

1.1.1.2.4.2.3.3；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
