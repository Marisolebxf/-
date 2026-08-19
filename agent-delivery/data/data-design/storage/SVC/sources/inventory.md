# 服务机构维 ODS 表级清单

```yaml
---
doc_id: SVC-SOURCE-INVENTORY
element: SVC
role: source
status: draft
version: "2026-08-19"
updated: 2026-08-19
task_id: DATA-SVC-STORAGE-S2-L02
---
```

> **真源**：权威 `third-party-source/doc/` xlsx；日常读 `doc/md-extract/`。  
> Sheet：`版权人才、企业机构、政策数据汇总表` → **国内机构要素库**。  
> CSV：`doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv`  
> **禁止**：以 `gkx-mysql-raw` as-built 改写本清单；DROP 约定 33 表；新建平行 ODS 实例；默认写正式 `gkxlumenx_ods`。  
> **本域独有 ODS 表 = 无**。33 张全部与 ENT **共用** `demo_gkxlumenx_ods`。

## 目标库

| 层 | 库名 | 说明 |
|---|---|---|
| Demo ODS | `demo_gkxlumenx_ods` | 共用 ENT 已建实例；**不新建、不 DROP** |
| 正式 ODS | `gkxlumenx_ods` | **本单零写入** |

## 圈定主读（P0）

SVC Demo 临时规则 `svc_rule_demo_kw_v1` **只读**机构主表字段，不复制全列到 `svc_org_base`。

| 约定表名 | 中文 | 与 ENT | 本域用途 | 圈定用字段（md-extract） |
|---|---|---|---|---|
| `dwd_org_base_info` | 机构基本信息 | **共用** | 圈定服务机构池；hang `org_id` | `org_id`、`name_cn`、`industry`、`industry_l1_name`…`industry_l4_name`；有则加 `business_scope`（该表文档**无**此列，见 Q-SVC-010） |

Q-SVC-010：Demo 该表无可靠 `business_scope`；`org_type` 不可作服务机构语义。规则版一律 `pending_client_confirm`，不伪闭合 live。

## 其余 32 表（共用 · 本波不作为圈定主路径）

供应方命名带 `dwd_`，角色仍是约定 ODS。SVC **不**平行再建、**不** DROP。

| 约定表名 | 中文 | 与 ENT |
|---|---|---|
| `dwd_org_shareholder_info` | 股东信息 | 共用 |
| `dwd_org_executive_info` | 高管信息 | 共用 |
| `dwd_org_org_product_info` | 经营信息 | 共用 |
| `dwd_org_annual_financial_info` | 年报财务信息 | 共用 |
| `dwd_org_important_news_info` | 重点资讯 | 共用 |
| `dwd_org_changerecord_info` | 工商变更信息 | 共用 |
| `dwd_org_recruit_info` | 招聘信息 | 共用 |
| `dwd_org_heis_info` | 高校基本信息 | 共用 |
| `dwd_org_stock_base` | 上市企业基本信息 | 共用 |
| `dwd_org_stock_finance_info` | 上市企业主要财务指标 | 共用 |
| `dwd_org_company_abnormal` | 经营异常 | 共用 |
| `dwd_org_company_punish` | 行政处罚 | 共用 |
| `dwd_org_company_illegal` | 严重违法 | 共用 |
| `dwd_org_risk_tax_punish` | 税收违法 | 共用 |
| `dwd_org_opt_judicial_case` | 司法案件信息 | 共用 |
| `dwd_org_risk_shixin` | 失信被执行人 | 共用 |
| `dwd_org_risk_zhixing` | 被执行人 | 共用 |
| `dwd_org_bankruptcy_public_cases` | 破产案件 | 共用 |
| `dwd_org_bankruptcy_public_cases_list` | 破产案件当事人 | 共用 |
| `dwd_special_hongkong_company` | 香港企业 | 共用 |
| `dwd_special_taiwan_company` | 台湾企业 | 共用 |
| `dwd_special_aomen_company` | 澳门企业 | 共用 |
| `dwd_bid_base_out` | 招投标公告基础表 | 共用 |
| `dwd_bid_win_candidate_out` | 招投标中标候选人表 | 共用 |
| `dwd_bid_purchase_agency_out` | 招投标采购代理表 | 共用 |
| `dwd_bid_target_item_out` | 招投标标的物表 | 共用 |
| `dwd_research_institute_base_info` | 科研机构基本信息 | 共用 |
| `dwd_org_subsidiary_info` | 子公司信息 | 共用 |
| `dwd_org_merger_acquisition_info` | 并购事件 | 共用 |
| `dwd_org_financing_info` | 融资事件 | 共用 |
| `dwd_org_invest_info` | 投资事件 | 共用 |
| `dwd_org_tech_tag` | 科技型标签 | 共用 |

**本域 ODS 独有 = 无。** 禁止 `svc_org_base`。产业链 `dwd_org_industry_tags` 等属 `storage/CHAIN`，本清单不收入、本轮不改。

## 禁止

- `SELECT enterprise_*` 当服务机构主路径  
- 复制 `dwd_org_base_info` 全列成 SVC 主体表  
- 以现网 as-built 删文档列（OPEN-SVC-FLOW-08）
