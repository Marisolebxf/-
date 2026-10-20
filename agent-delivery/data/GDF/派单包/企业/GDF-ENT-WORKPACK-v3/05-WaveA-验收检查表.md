# Wave A 验收检查表（回签）— v3.0

> **任务**：`GDF-ENT-WORKPACK-V3-L01`  
> **清单真源**：`02-WaveA-贴源表清单.yaml`（49 张：P0=16 / P1=26 / P2=7；另有 2 张供应方待核实表）  
> **tgt**：`gkxlumenx_ods` 同名表。贴源不连、不改、不验收 `demo_gkxlumenx_*`。  
> **重出日期**：2026-09-02（不沿用 v1.2 的 40 表旧表）  
> **2026-10-19**：表内预填的 src 行数（专利 86028、申请人 59018、权利人 70000、产业链标签 18818、港澳台 40000）不作验收线。回签时 src/tgt 用 `COUNT(*)` 现算。`dwd_forg_college_org_info` 源库无表，本期不洗，不计入完成数。  
> **阈值**：有效行偏差 ≤1% 或绝对差 ≤100（取较宽者）；抽样 ≥20 条且主键命中 100%；DDL 同构（额外审计列须备注）。  
> **财务单位**：目标统一万元；GDF 须填 `unit_evidence`，不能从值域判断时停止并报阻塞。

**产线名称**：________________  
**调度周期 / DAG**：________________（`OPEN-ENT-FLOW-01` 未关前不得伪填）  
**GDF 负责人签字**：________ 日期：________  
**本侧验收签字**：________ 日期：________

列：`src/tgt`=有效行数；`ddl/sample`=Y/N；`batch`=最近成功批次；`unit_evidence`=财务单位证据；`done/sign`=回签。

## P0（关单必填，16）

| # | table_name | cn | src | tgt | ddl | sample | batch | unit_evidence | done | sign | note |
|---:|---|---|---:|---:|---|---|---|---|---|---|---|
| 1 | dwd_org_base_info | 国内机构信息 | | | | | | | | | 主数据；非 reg_info |
| 2 | dwd_org_shareholder_info | 股东信息 | | | | | | | | | |
| 3 | dwd_org_executive_info | 高管信息 | | | | | | | | | |
| 4 | dwd_org_org_product_info | 经营信息 | | | | | | | | | |
| 5 | dwd_org_annual_financial_info | 年报财务 | | | | | | 必填 | | | 目标万元 |
| 6 | dwd_org_important_news_info | 重点资讯 | | | | | | | | | |
| 7 | dwd_org_stock_base | 上市基本信息 | | | | | | | | | |
| 8 | dwd_org_stock_finance_info | 上市财务指标 | | | | | | 必填 | | | 源明确元→目标万元 |
| 9 | dwd_org_financing_info | 融资信息 | | | | | | 金额字段需留证 | | | live gkx 已见 42104 行 |
| 10 | dwd_org_invest_info | 对外投资 | | | | | | 金额字段需留证 | | | |
| 11 | dwd_org_tech_tag | 科技型标签 | | | | | | | | | 2026-09-02 改口贴此表；`org_tag` 中文名；旧名 tag_info 不贴 |
| 12 | dwd_org_subsidiary_info | 子公司 | | | | | | | | | |
| 13 | dwd_bid_base_out | 招投标公告 | | | | | | | | | |
| 14 | dwd_bid_win_candidate_out | 中标候选人 | | | | | | | | | |
| 15 | dwd_industry_chain_info | 产业链图谱 | | | | | | | | | |
| 16 | dwd_org_industry_tags | 产业链企业标签 | | | | | | | | | live 已见 18818 行；先洗可覆盖字段 |

## P1（双周进度，26）

| # | table_name | cn | src | tgt | ddl | sample | batch | unit_evidence | done | sign | note |
|---:|---|---|---:|---:|---|---|---|---|---|---|---|
| 1 | dwd_org_changerecord_info | 工商变更 | | | | | | | | | |
| 2 | dwd_org_recruit_info | 招聘 | | | | | | | | | |
| 3 | dwd_org_heis_info | 高校机构 | | | | | | | | | mirror_only |
| 4 | dwd_research_institute_base_info | 科研机构 | | | | | | | | | mirror_only |
| 5 | dwd_special_hongkong_company | 香港企业 | 40000 | | | | | | | | → enterprise_base；region_id=810000 |
| 6 | dwd_special_taiwan_company | 台湾企业 | 40000 | | | | | | | | → enterprise_base；region_id=710000 |
| 7 | dwd_special_aomen_company | 澳门企业 | 792 | | | | | | | | region_id=820000；仅396行有 org_id，其余只留 ODS |
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
| 21 | dwd_foreign_org_annual_financial_info | 国外年报财务 | | | | | | 必填 | | | 目标万元 |
| 22 | dwd_forg_subsidiary_info | 国外子公司 | | | | | | | | | **书面阻塞**：live 无此表；母子段等源到位再洗 |
| 23 | dwd_org_industry_product_tags | 产业链产品标签 | | | | | | | | | wash → enterprise_industry_product |
| 24 | dwd_patent | 专利主表 | 86028 | | | | | | | | 联合各名称源精确匹配覆盖3161件 |
| 25 | dwd_patent_applicants | 专利申请人 | 59018 | | | | | | | | 名称精确匹配；写 patent_org_rel |
| 26 | dwd_patent_assignees | 当前专利权人 | 70000 | | | | | | | | 名称精确匹配；写 patent_org_rel |

## P2（本包不洗，贴源按启动会决定，7）

`dwd_bid_purchase_agency_out`、`dwd_bid_target_item_out`、`dwd_forg_college_org_info`、`dwd_forg_university_org_info`、`dwd_forg_research_org_info`、`dwd_industry_chain_news_info`、`dwd_org_merger_acquisition_info`（Q-WP3-21 可贴源不洗）。

## 供应方待核实（不计入 Wave A 完成数）

`dwd_org_industry_chain_dtl`：live 不存在；继续索取或核实名。到表前不得将 `chain_score` / `segment_key` 标完成。  
`dwd_org_industry_chain_pat_dtl`：Q-WP3-19；到表前不洗 `enterprise_chain_patent`。

## 抽检 SQL

```sql
SELECT COUNT(*) FROM gkx.dwd_org_base_info WHERE is_deleted = 0;
SELECT COUNT(*) FROM gkxlumenx_ods.dwd_org_base_info WHERE is_deleted = 0;
```

源库无承诺表 → 记阻塞，禁止换旧名或造表关单。

## 关单

- [ ] P0 除书面裁掉项外全部 `done=Y`（标签按 `dwd_org_tech_tag`）；P1 本期纳入项回签（`forg_subsidiary` 书面阻塞不计入完成）  
- [ ] 财务 `unit_evidence` 齐全，目标均为万元  
- [ ] `enterprise_base.region_id` / 可空 `enterprise_code` 与 `enterprise_patent_org_rel` DDL 已验收  
- [ ] 港澳台和专利未匹配记录均有拒绝 / 待治理清单，未生成伪 ID  
- [ ] 调度 / 失败告警有真实证据；OPEN 未关不得填完成  
- [ ] 结构变更重跑流程已文档化  
- [ ] 回签存档路径：________________
