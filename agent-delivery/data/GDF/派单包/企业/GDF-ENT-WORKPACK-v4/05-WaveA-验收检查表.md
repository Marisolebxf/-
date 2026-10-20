# Wave A 验收检查表（回签）— v4.0

> **任务**：`GDF-ENT-WORKPACK-V4-L01`  
> **清单真源**：`02-WaveA-贴源表清单.yaml` **v4.0（62 张：P0=15 / P1=33 / P2=14）**，基线 = 10-19 三方承诺清单 + live 实证  
> **tgt**：`gkxlumenx_ods` 同名表。贴源不连、不改、不验收 `demo_gkxlumenx_*`。  
> **v4.0 变更（相对 v3 表单）**：`dwd_org_stock_base` 移出；`dwd_forg_subsidiary_info`（从未存在）换源 `dwd_agg_subsidiary_info`；专利侧表 +5 张（P2 mirror_only）；司法明细/年报 base+asset/利润表（v3.1.6 扩入）入列；融资/投资/并购归属金融要素库（施工不变）。  
> **2026-10-19**：预填行数一律不作验收线；回签时 src/tgt 用 `COUNT(*)` 现算。`dwd_forg_college_org_info` 源库无表，本期不贴不洗，不计入完成数。  
> **阈值**：有效行偏差 ≤1% 或绝对差 ≤100（取较宽者）；抽样 ≥20 条且主键命中 100%；DDL 同构（额外审计列须备注；10-19 Excel 纪要中 t_id 等列 live 不存在，不要求）。  
> **财务单位**：目标统一万元；GDF 须填 `unit_evidence`，不能从值域判断时停止并报阻塞。

**产线名称**：________________  
**调度周期 / DAG**：________________（`OPEN-ENT-FLOW-01` 未关前不得伪填）  
**GDF 负责人签字**：________ 日期：________  
**本侧验收签字**：________ 日期：________

列：`src/tgt`=有效行数；`ddl/sample`=Y/N；`batch`=最近成功批次；`unit_evidence`=财务单位证据；`done/sign`=回签。

## P0（关单必填，15）

| # | table_name | cn | src | tgt | ddl | sample | batch | unit_evidence | done | sign | note |
|---:|---|---|---:|---:|---|---|---|---|---|---|---|
| 1 | dwd_org_base_info | 国内机构信息 | | | | | | | | | 主数据；非 reg_info |
| 2 | dwd_org_shareholder_info | 股东信息 | | | | | | | | | |
| 3 | dwd_org_executive_info | 高管信息 | | | | | | | | | |
| 4 | dwd_org_org_product_info | 经营信息 | | | | | | | | | |
| 5 | dwd_org_annual_financial_info | 年报财务 | | | | | | 必填 | | | 目标万元 |
| 6 | dwd_org_important_news_info | 重点资讯 | | | | | | | | | |
| 7 | dwd_org_stock_finance_info | 上市财务指标 | | | | | | 必填 | | | v4.0：is_listed/listed_code 改源之一；源明确元→目标万元 |
| 8 | dwd_org_financing_info | 融资信息 | | | | | | 金额字段需留证 | | | v4.0 归属金融要素库；live 23,662 行 |
| 9 | dwd_org_invest_info | 对外投资 | | | | | | 金额字段需留证 | | | v4.0 归属金融要素库；live 53,758 行 |
| 10 | dwd_org_tech_tag | 科技型标签 | | | | | | | | | 改口表；`org_tag` 中文名；旧名 tag_info 不贴 |
| 11 | dwd_org_subsidiary_info | 子公司 | | | | | | | | | |
| 12 | dwd_bid_base_out | 招投标公告 | | | | | | | | | |
| 13 | dwd_bid_win_candidate_out | 中标候选人 | | | | | | | | | |
| 14 | dwd_industry_chain_info | 产业链图谱 | | | | | | | | | |
| 15 | dwd_org_industry_tags | 产业链企业标签 | | | | | | | | | live 估 2,197,216；先洗可覆盖字段 |

**v4.0 移出说明**：`dwd_org_stock_base`（原 P0#7）10-19 清单不再收录，本表不贴不洗、不计完成数；上市字段承接见 09 §3.1/§3.1.2 v4 注。

## P1（双周进度，33）

| # | table_name | cn | src | tgt | ddl | sample | batch | unit_evidence | done | sign | note |
|---:|---|---|---:|---:|---|---|---|---|---|---|---|
| 1 | dwd_org_changerecord_info | 工商变更 | | | | | | | | | |
| 2 | dwd_org_recruit_info | 招聘 | | | | | | | | | |
| 3 | dwd_org_heis_info | 高校机构 | | | | | | | | | mirror_only |
| 4 | dwd_research_institute_base_info | 科研机构 | | | | | | | | | mirror_only |
| 5 | dwd_special_hongkong_company | 香港企业 | | | | | | | | | → enterprise_base；region_id=810000 |
| 6 | dwd_special_taiwan_company | 台湾企业 | | | | | | | | | → enterprise_base；region_id=710000 |
| 7 | dwd_special_aomen_company | 澳门企业 | | | | | | | | | region_id=820000；仅 396 行有 org_id，其余只留 ODS |
| 8 | dwd_org_company_abnormal | 经营异常 | | | | | | | | | |
| 9 | dwd_org_company_punish | 行政处罚 | | | | | | | | | |
| 10 | dwd_org_company_illegal | 严重违法 | | | | | | | | | |
| 11 | dwd_org_risk_tax_punish | 税收违法 | | | | | | | | | |
| 12 | dwd_org_opt_judicial_case | 司法案件 | | | | | | | | | |
| 13 | dwd_org_risk_shixin | 失信被执行人 | | | | | | | | | |
| 14 | dwd_org_risk_zhixing | 被执行人 | | | | | | | | | |
| 15 | dwd_org_bankruptcy_public_cases | 破产案件 | | | | | | | | | |
| 16 | dwd_org_bankruptcy_public_cases_list | 破产关联人 | | | | | | | | | |
| 17 | dwd_forg_base_info | 国外机构基本信息 | | | | | | | | | |
| 18 | dwd_forg_product_info | 国外经营 | | | | | | | | | |
| 19 | dwd_forg_executive_info | 国外高管 | | | | | | | | | |
| 20 | dwd_forg_shareholder_info | 国外股东穿透 | | | | | | | | | |
| 21 | dwd_foreign_org_annual_financial_info | 国外年报财务 | | | | | | | 必填 | | | 目标万元 |
| 22 | dwd_agg_subsidiary_info | 机构子公司（国外母子） | | | | | | | | | **v4.0 换源**（替 forg_subsidiary，live 19,810 行）；eid 命中率 6.3% 为已知现状，未命中进治理清单 |
| 23 | dwd_org_industry_product_tags | 产业链产品标签 | | | | | | | | | wash → enterprise_industry_product |
| 24 | dwd_patent | 专利主表 | | | | | | | | | 名称精确匹配；联合申请人/权利人写 patent_org_rel |
| 25 | dwd_patent_applicants | 专利申请人 | | | | | | | | | 名称精确匹配；写 patent_org_rel |
| 26 | dwd_patent_assignees | 当前专利权人 | | | | | | | | | 名称精确匹配；写 patent_org_rel |
| 27 | dwd_patent_title | 专利标题分表 | | | | | | | | | → title_zh 宽列 |
| 28 | dwd_patent_abstract | 专利摘要分表 | | | | | | | | | → abstract_zh 宽列 |
| 29 | dwd_patent_legal | 专利法律状态分表 | | | | | | | | | → legal_status |
| 30 | dwd_patent_cited | 专利引用分表 | | | | | | | | | → citation_count / cited_by_count |
| 31 | dwd_opt_judicial_case_detail | 司法案件明细 | | | | | | | | | v3.1.6 扩入；回补 risk_judicial_case（09 §3.13.5-补） |
| 32 | dwd_org_annual_report_base | 年报基本信息 | | | | | | | | | v3.1.6 扩入；mirror_only 备查 |
| 33 | dwd_org_annual_report_asset | 年报资产信息 | | | | | | | | | v3.1.6 扩入；wash 补财务历史（09 §3.20）；金额 varchar 源态 |

**v4.0 换源说明**：原 P1#22 `dwd_forg_subsidiary_info`（书面阻塞、live 从未存在）由 `dwd_agg_subsidiary_info` 替代——**母子段阻塞解除**，但低命中率（6.3%）为已知现状，未命中进治理清单、不造 ID。

## P2（本包不洗，贴源备查，14）

| # | table_name | cn | note |
|---:|---|---|---|
| 1 | dwd_bid_purchase_agency_out | 采购代理 | mirror_only |
| 2 | dwd_bid_target_item_out | 标的物 | mirror_only |
| 3 | dwd_org_income_statement | 利润表 | v3.1.6 扩入；106 列上市利润表备查 |
| 4 | dwd_org_merger_acquisition_info | 并购事件 | Q-WP3-21 只贴不洗；v4.0 归属金融要素库 |
| 5 | dwd_forg_university_org_info | 国外高校 | mirror_only |
| 6 | dwd_forg_research_org_info | 国外科研 | mirror_only |
| 7 | dwd_industry_chain_news_info | 产业资讯 | 合规表不洗 |
| 8 | dwd_patent_inventors | 专利发明人 | v3.1.6 扩入；图谱备查 |
| 9 | dwd_patent_priority_filings | 专利优先权 | **v4.0 扩入**；无承接列 |
| 10 | dwd_patent_claim | 专利权利要求 | **v4.0 扩入**；全文无承接列 |
| 11 | dwd_patent_description | 专利说明书 | **v4.0 扩入**；全文无承接列 |
| 12 | dwd_patent_transfer | 专利转移 | **v4.0 扩入**；轨迹走 detail_json 另拍板 |
| 13 | dwd_patent_family | 专利同族 | **v4.0 扩入**；无承接列 |
| 14 | ~~dwd_forg_college_org_info~~ | ~~国外高校~~ | **源库无表，不贴**；列此仅作对照，不计任何数 |

## 供应方待核实（不计入 Wave A 完成数）

`dwd_org_industry_chain_dtl`：live 不存在；继续索取或核实名。到表前不得将 `chain_score` / `segment_key` 标完成。  
`dwd_org_industry_chain_pat_dtl`：Q-WP3-19；到表前不洗 `enterprise_chain_patent`。

## 抽检 SQL

```sql
SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkxlumenx_ods.dwd_org_base_info WHERE is_deleted = 0;
-- v4.0 新增换源表抽检
SELECT COUNT(*) FROM gkx.dwd_agg_subsidiary_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkxlumenx_ods.dwd_agg_subsidiary_info WHERE is_deleted = 0;
```

源库无承诺表 → 记阻塞，禁止换旧名或造表关单。

## 关单

- [ ] P0 除书面裁掉项外全部 `done=Y`（标签按 `dwd_org_tech_tag`）；P1 本期纳入项回签（`dwd_forg_college_org_info` 无表不计入）  
- [ ] 财务 `unit_evidence` 齐全，目标均为万元  
- [ ] `enterprise_base.region_id` / 可空 `enterprise_code` 与 `enterprise_patent_org_rel` DDL 已验收  
- [ ] 港澳台/专利/国外母子（agg_subsidiary）未匹配记录均有拒绝 / 待治理清单，未生成伪 ID  
- [ ] 调度 / 失败告警有真实证据；OPEN 未关不得填完成  
- [ ] 结构变更重跑流程已文档化  
- [ ] 回签存档路径：________________
