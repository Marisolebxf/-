# 断链风险等级（M_ENT_SUPPLY_CHAIN_RISK）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_SUPPLY_CHAIN_RISK`
- **指标名称**：断链风险等级
- **一级模块**：企业分析
- **二级模块**：风险洞察
- **三级模块**：供应链关系
- **更新频率**：月度/事件触发
- **对齐状态**：未对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014

## 口径定义

对企业供应链因内外部因素导致中断的可能性及其影响程度的综合评价等级。依照需求文档提供的构建方法。

## 计算逻辑说明

```
供应链韧性指数 = 加权汇总（资金关系/供需稳固/产品流动/绩效波动），映射断链风险等级（低/中/高）。
```

**计算公式文件**：`M_ENT_SUPPLY_CHAIN_RISK.md`

## 源表字段

```
gkx.dwd_org_stock_finance_info(org_id, operating_revenue, total_profit, occur_period) — 营收与利润波动性计算（绩效波动维度）
gkx.dwd_org_company_abnormal(org_id, abn_reason, abn_date) — 经营异常（供应链关联企业风险信号）
gkx.dwd_org_company_illegal(org_id, category, abn_date) — 严重违法（供应链关联企业风险信号）
gkx.dwd_org_company_punish(org_id, penalty_date, penalty_type, violation_type) — 行政处罚（供应链关联企业风险信号）
```

## 待建表字段

```
供应链边表(source_org_id, target_org_id, relation_type) — 供应链上下游关系边表（现库无此表，待建）
```

## 备注

1.1.1.2.4.2.3.8 + 算法库5.4；依照需求文档提供的构建方法；供应链边表待建

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
