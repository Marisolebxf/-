# 营收（M_ENT_REVENUE_LATEST）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_REVENUE_LATEST`
- **指标名称**：营收
- **一级模块**：企业分析
- **二级模块**：企业查询
- **三级模块**：企业画像
- **更新频率**：年度
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E23

## 口径定义

企业最新年度营业收入。

## 计算逻辑说明

```
从dwd_org_annual_financial_info取最新year的operating_revenue。
```

**计算公式文件**：`M_ENT_REVENUE_LATEST.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id,operating_revenue,year）
```

## 备注

1.1.1.2.4.2.3.3

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
