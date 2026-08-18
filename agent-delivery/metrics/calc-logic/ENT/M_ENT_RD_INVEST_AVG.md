# 平均研发投入（M_ENT_RD_INVEST_AVG）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_RD_INVEST_AVG`
- **指标名称**：平均研发投入
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：年度
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

选定产业内全部企业法人单位，最近一个完整自然年度R&D经费内部支出金额的算术平均值。

## 计算逻辑说明

```
AVG(各企业R&D经费)。研发投入优先从dwd_org_annual_financial_info取`arch development am`。
```

**计算公式文件**：`M_ENT_RD_INVEST_AVG.md`

## 源表字段

```
gkx.dwd_org_annual_financial_info（org_id, year, `arch development am`）— 研发投入金额（优先年报）
```

## 备注

1.1.1.2.4.2.3.3；简单统计类；研发投入优先取年报`arch development am`

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
