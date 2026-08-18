# 市场份额（M_ENT_MARKET_SHARE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_MARKET_SHARE`
- **指标名称**：市场份额
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：季度/年度
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

企业营业收入占所属行业总营业收入的比重。

## 计算逻辑说明

```
市场份额 = 企业营收 / 同行业所有企业营收合计 * 100%。行业总营收按industry_l1_code分组聚合。
```

**计算公式文件**：`M_ENT_MARKET_SHARE.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id, operating_revenue, year）— 年报营业收入（分子）
gkx.dwd_org_base_info（org_id, industry, industry_l1_code）— 企业所属行业分类（分母筛选）
```

## 备注

1.1.1.2.4.2.3.4；需求文档未明确构建方法，参考V3方案；需郭经理与数据采购方沟通

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
