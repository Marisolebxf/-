# Wave A 验收检查表（回签）— v1.2

> **承诺表真源**：`third-party-source/doc/`（md-extract）  
> **表清单**：`02-WaveA-贴源表清单.yaml` v1.2（共 40 张：P0=17 / P1=23）  
> **用法**：GDF 每完成一张表填写一行；本侧数据 Lead 抽检后签字。  
> **阈值（启动会共定，下列为建议默认）**：  
> - 行数：目标有效行与源相对偏差 ≤ **1%**，或绝对差 ≤ 100（取较宽者）  
> - 抽样：≥ **20** 条主键在源侧命中率 **100%**  
> - DDL：列名/类型与源一致（允许目标侧额外审计列，需备注）

**工作包版本**：GDF-ENT-WORKPACK-v1.2  
**产线名称**：________________  
**调度周期**：________________  
**GDF 负责人签字**：________ 日期：________  
**本侧验收签字**：________ 日期：________  

## 列说明

| 列 | 含义 |
|----|------|
| src_rows | 源库有效行数 |
| tgt_rows | 目标库有效行数 |
| ddl_ok | DDL 已对齐（Y/N） |
| sample_ok | 抽样主键比对通过（Y/N） |
| batch_ts | 最近成功批次时间 |
| done | 完成（Y/N） |
| sign | 双方简签 |

---

## P0 表（关单必填，17）

| # | table_name | cn | src_rows | tgt_rows | ddl_ok | sample_ok | batch_ts | done | sign | note |
|---|------------|-----|----------|----------|--------|-----------|----------|------|------|------|
| 1 | dwd_org_base_info | 国内机构信息 | | | | | | | | 主数据；非 reg_info |
| 2 | dwd_org_shareholder_info | 股东信息 | | | | | | | | |
| 3 | dwd_org_executive_info | 高管信息 | | | | | | | | |
| 4 | dwd_org_org_product_info | 经营信息 | | | | | | | | |
| 5 | dwd_org_annual_financial_info | 年报财务信息 | | | | | | | | |
| 6 | dwd_org_important_news_info | 重点资讯 | | | | | | | | |
| 7 | dwd_org_stock_base | 上市企业基本信息 | | | | | | | | |
| 8 | dwd_org_stock_finance_info | 上市企业主要财务指标 | | | | | | | | |
| 9 | dwd_org_heis_info | 高校机构信息 | | | | | | | | 承诺 heis |
| 10 | dwd_research_institute_base_info | 科研机构基本信息 | | | | | | | | |
| 11 | dwd_special_hongkong_company | 香港企业 | | | | | | | | |
| 12 | dwd_special_taiwan_company | 台湾企业 | | | | | | | | |
| 13 | dwd_special_aomen_company | 澳门企业 | | | | | | | | |
| 14 | dwd_bid_base_out | 招投标公告基本表 | | | | | | | | |
| 15 | dwd_industry_chain_info | 产业链图谱表 | | | | | | | | |
| 16 | dwd_org_industry_tags | 产业链关联企业信息 | | | | | | | | |
| 17 | dwd_org_industry_product_tags | 产业链关联产品信息 | | | | | | | | |

---

## P1 表（双周进度，23）

| # | table_name | cn | src_rows | tgt_rows | ddl_ok | sample_ok | batch_ts | done | sign | note |
|---|------------|-----|----------|----------|--------|-----------|----------|------|------|------|
| 1 | dwd_org_changerecord_info | 工商变更信息 | | | | | | | | |
| 2 | dwd_org_recruit_info | 招聘信息 | | | | | | | | |
| 3 | dwd_bid_win_candidate_out | 招投标中标候选人表 | | | | | | | | |
| 4 | dwd_bid_purchase_agency_out | 招投标采购代理表 | | | | | | | | |
| 5 | dwd_bid_target_item_out | 招投标标的表 | | | | | | | | |
| 6 | dwd_org_company_abnormal | 经营异常 | | | | | | | | |
| 7 | dwd_org_company_punish | 行政处罚 | | | | | | | | |
| 8 | dwd_org_company_illegal | 严重违法 | | | | | | | | |
| 9 | dwd_org_risk_tax_punish | 税收违法 | | | | | | | | |
| 10 | dwd_org_opt_judicial_case | 司法案件信息 | | | | | | | | |
| 11 | dwd_org_risk_shixin | 失信被执行人 | | | | | | | | |
| 12 | dwd_org_risk_zhixing | 被执行人 | | | | | | | | |
| 13 | dwd_org_bankruptcy_public_cases | 破产案件 | | | | | | | | |
| 14 | dwd_org_bankruptcy_public_cases_list | 破产案件关联人 | | | | | | | | |
| 15 | dwd_forg_base_info | 国外机构基本信息 | | | | | | | | |
| 16 | dwd_forg_shareholder_info | 国外机构股东股权穿透信息 | | | | | | | | |
| 17 | dwd_forg_executive_info | 国外机构高管信息 | | | | | | | | |
| 18 | dwd_forg_product_info | 国外机构公司经营信息 | | | | | | | | |
| 19 | dwd_forg_college_org_info | 国外高校机构信息 | | | | | | | | |
| 20 | dwd_forg_university_org_info | 国外高校机构信息 | | | | | | | | |
| 21 | dwd_forg_research_org_info | 国外科研机构基本信息 | | | | | | | | |
| 22 | dwd_foreign_org_annual_financial_info | 国外机构年报财务 | | | | | | | | |
| 23 | dwd_industry_chain_news_info | 产业动态资讯 | | | | | | | | |

---

## 不在本包（勿验收）

- `dwd_company*` / 量子 `company_*`
- 海洋 `hycy_*`、承诺表中的 `ods_*`
- 专利/论文工作簿表（另波）
- live 旧名：`dwd_org_reg_info`、`dwd_org_hels_info`、`dwd_org_bid_info` 等（见 `02` naming_delta）

---

## 抽检 SQL 示例

```sql
-- 源（gkx）— 表名以承诺为准
SELECT COUNT(*) FROM dwd_org_base_info WHERE is_deleted = 0;

-- 目标（gkxlumenx_ods）
SELECT COUNT(*) FROM dwd_org_base_info WHERE is_deleted = 0;
```

若源库查无承诺表名 → 登记供应方核验（勿自行改用旧名关单）。

---

## 关单勾选

- [ ] P0 全部 `done=Y` 且本侧抽检通过  
- [ ] 产线调度与失败告警已演示  
- [ ] 结构变更重跑流程已文档化  
- [ ] 回签存档路径：________________  
