# CDC 预填生成报告

- 工作包: `f:\gkx-lumen\gkx-orchestration\agent-delivery\data\GDF\派单包\企业\GDF-ENT-WORKPACK-v2`
- Wave A 表: 47（P0=17）
- Wave B 目标表: 34
- 产出: `1、贴源_预填-DRAFT.xlsx` / `2、明细数据_预填-DRAFT.xlsx`

## 这是 DRAFT
不是 GDF 执行结果。导入、跑批、`05` 回签仍由 GDF 完成。作业频率未填。

## warnings
- workpack 暂缓投递 — DRAFT only if user explicitly asked
- dwd_forg_college_org_info: 02 mirror_only
- dwd_forg_university_org_info: 02 mirror_only
- dwd_forg_research_org_info: 02 mirror_only
- dwd_org_industry_product_tags: 02 mirror_only
- dwd_industry_chain_news_info: 02 mirror_only
- enterprise_finance_history.revenue: 单位待三方确认，未自动 /10000
- enterprise_finance_history.main_business_revenue: 单位待三方确认，未自动 /10000
- enterprise_finance_history.total_profit: 单位待三方确认，未自动 /10000
- enterprise_finance_history.total_fixed_assets: 单位待三方确认，未自动 /10000
- enterprise_risk_summary: 预聚合后 MainOutput 为长表 org_id+risk_type；current/history 未按 remove_date 细拆
- enterprise_forg_base.registered_capital: 已强制 /10000.0（H2）

## mirror_only（只贴源不洗）
- `dwd_org_heis_info`
- `dwd_research_institute_base_info`
- `dwd_special_hongkong_company`
- `dwd_special_taiwan_company`
- `dwd_special_aomen_company`
- `dwd_bid_purchase_agency_out`
- `dwd_bid_target_item_out`
- `dwd_forg_college_org_info`
- `dwd_forg_university_org_info`
- `dwd_forg_research_org_info`
- `dwd_org_industry_product_tags`
- `dwd_industry_chain_news_info`
