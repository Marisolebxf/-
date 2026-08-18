# 成长潜力（M_ENT_GROWTH_POTENTIAL）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 本指标含 4 行子指标（L1+L2+L3），已合并为单文件。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## L1 指标元数据

- **指标ID**：`M_ENT_GROWTH_POTENTIAL`
- **指标名称（一级）**：成长潜力
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引推荐
- **更新频率**：年度/季度
- **对齐状态**：未对齐
- **是否在数据库（L1）**：是
- **关联Q编号**：Q015

## L1 口径定义

从企业市场扩张、盈利提升、资产积累反映企业内生增长动能和可持续发展能力。

## L1 计算逻辑说明

```
各维度与行业均值进行比较，数据取自企业最近两个完整自然年度。三个维度采用等权重加权汇总，得出成长潜力综合得分。
```

**计算公式文件**：`M_ENT_GROWTH_POTENTIAL.md`

## L1 源表字段

```
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, total_profit, total_assets, total_liabilities, year) — 营收/利润/净资产同比计算（净资产=资产总额-负债总额）
gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标
```

## L1 备注

1.1.1.2.4.2.3.6；

## 子指标详情（L2 / L3）

### L2：市场扩张

#### L2 详情：市场扩张

- **口径定义**：从企业市场扩张、盈利提升、资产积累反映企业内生增长动能和可持续发展能力。
- **计算逻辑**：`营业收入增长率超出行业均值情况`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 营收同比计算<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标`
- **更新频率**：年度/季度
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.6；

### L2：盈利提升

#### L2 详情：盈利提升

- **口径定义**：从企业市场扩张、盈利提升、资产积累反映企业内生增长动能和可持续发展能力。
- **计算逻辑**：`利润增长率超出行业均值情况`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, total_profit, year) — 利润同比计算<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标`
- **更新频率**：年度/季度
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.6；

### L2：资产积累

#### L2 详情：资产积累

- **口径定义**：从企业市场扩张、盈利提升、资产积累反映企业内生增长动能和可持续发展能力。
- **计算逻辑**：`净资产增长率超出行业均值情况`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, total_assets, total_liabilities, year) — 净资产同比计算（净资产=资产总额-负债总额）<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业均值对标`
- **更新频率**：年度/季度
- **对齐状态**：未对齐
- **关联Q编号**：Q015
- **是否在数据库**：是
- **备注**：1.1.1.2.4.2.3.6；

---
*生成自王惠 20260816 Excel 底稿（4 行），data-agent 正式化 2026-08-18*
