# CDC 预填生成报告

- 工作包: `E:\zhipu\gkx-lumen\gkx-orchestration\agent-delivery\data\GDF\派单包\金融数据\GDF-FIN-WORKPACK-v1`
- Wave A 表: 28（P0=9）
- Wave B 目标表: 11
- 产出: `1、贴源_预填-DRAFT.xlsx` / `2、明细数据_预填-DRAFT.xlsx`

## 这是 DRAFT
不是 GDF 执行结果。导入、跑批、`05` 回签仍由 GDF 完成。作业频率未填。

## warnings
- fin_industrial_fund_lp.sub_capital: 单位待确认（OPEN-FIN-03），原样不换算
- fin_industrial_fund_lp.lp_real_capital: 单位待确认（OPEN-FIN-03），原样不换算
- fin_industrial_fund_inv_summary.cum_inv_amount: 单位待确认（OPEN-FIN-03），原样不换算
- dwd_org_financing_info: owner=ENT-v4，贴源/洗数归他包，本包 CDC 不含
- dwd_org_invest_info: owner=ENT-v4，贴源/洗数归他包，本包 CDC 不含
- dwd_org_merger_acquisition_info: owner=ENT-v4，贴源/洗数归他包，本包 CDC 不含

## mirror_only（只贴源不洗）
- `dwd_ls_stock_daily_quotation`
- `dwd_hk_sec_daily_quotation`
- `dwd_us_sec_daily_quotation`
- `dwd_option_daily_quotation`
- `dwd_option_basic_info`
- `dwd_foreign_exchange_info`
- `dwd_fund_basic_info`
- `dwd_fund_equity_sector_allocation`
- `dwd_fund_bond_allocation`

## 金融包补充说明（本次手工追加，重生成需重加）

- 模板壳：金融包无 	emplates/，借 企业/GDF-ENT-WORKPACK-v1/执行结果/ 两张模板的布局壳，内容全部清空重写。
- Wave A：28 张（FIN 自有；P0=9，P1=10，P2/0 行 mirror_only=9）。ENT-v4 三表（dwd_org_financing_info / dwd_org_invest_info / dwd_org_merger_acquisition_info）不在本 CDC。「没找到的表」无登记。
- Wave B：11 张 in_*（19 张源表）。7 张单源直出；in_bond / in_industry_class_his / in_main_biz_composition / in_valuation_daily 为 UNION ALL（每源 IVn → IVU → MainOutput）。P2 / 0 行表不进 Wave B。
- etl_time 不映射（DDL 默认 CURRENT_TIMESTAMP）；eg_capital_wan 为 09 §3.3 的 SQL 实现（MySQL 8 REGEXP_REPLACE），外币/空// → NULL，不写 0。
- 类型列按 09 目标列类型填；以 10-DWD-MySQL-DDL/ 预建表为准（草稿未签收）。
- 待 GDF 确认：SRC_ENT（沿用 ENT 数据源名，金融域字典值）、业务主题 FIN、作业频率/运行区间（未填）、大表增量策略（04 §3，回签前不得宣称 CDC 闭环）。
- 未在 GDF 导入验证；这是预填草稿，不是执行结果，也不是跑通。
