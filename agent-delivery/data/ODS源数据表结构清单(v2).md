# ODS 源数据表结构清单（v2）

> 生成时间: 2026-06-02 ｜ 版本: v2（基于三方数据源「要素库」重构）

---

## 1. 版本说明

本清单为 **v2 版本**，相较 v1 的根本变化在于 **ODS 层数据源的来源发生变更**：

- **v1**：ODS 层来自 PostgreSQL `demo_gdf_data.ods`（`poc_tb_*` 共 70 张示例表）。
- **v2**：ODS 层来自三方采购数据源「要素库」，即 `2-概要设计/2-1需求分析/数据需求分析/db/要素库建表语句.sql` 中定义的全部 **186 张表**（建表语句以 `dwd_` 前缀命名，但其业务定位为**三方数据源 = 本系统 ODS 层**，不要与本项目自建的 DWD 标准表混淆）。

> 命名澄清：要素库 SQL 中的 `dwd_xxx` 是数据供应方的表命名习惯，在本系统数据分层中**统一归入 ODS（贴源层）**；本项目自建的标准明细层 DWD 见 `DWD标准表结构清单.md`。

- **字符集**: utf8mb4 ｜ **引擎**: InnoDB ｜ **建表脚本**: `db/要素库建表语句.sql`

## 2. 数据域分布总览

| 数据域 | 表数量 | 字段总数 | 来源 Sheet |
|--------|--------|----------|------------|
| 金融/宏观 | 3 | 26 | 宏观行业要素库、金融要素库 |
| 行业研究 | 1 | 21 | 行业分析要素库 |
| 产业链 | 5 | 60 | 产业链要素库 |
| 企业/机构(国内) | 41 | 696 | 国内机构要素库 |
| 企业/机构(国外) | 8 | 76 | 国外机构要素库 |
| 人才 | 2 | 38 | 人才要素库 |
| 政策(国内) | 1 | 20 | 国内政策要素库 |
| 政策(国外) | 1 | 16 | 国外政策要素库 |
| 行业专题(医药) | 19 | 96 | 医药专题要素库 |
| 行业专题(化学) | 7 | 61 | 化学专题要素库 |
| 行业专题(海洋) | 35 | 296 | 海洋专题要素库 |
| 行业专题(量子)/企业工商 | 25 | 283 | 量子专题要素库 |
| 论文(中文) | 9 | 128 | 中文论文要素库 |
| 论文(外文) | 10 | 130 | 外文论文要素库 |
| 专利 | 7 | 150 | 全球专利要素库 |
| 科研项目(国内) | 5 | 60 | 国内项目要素库 |
| 科研项目(国外) | 2 | 47 | 国外项目要素库 |
| 科技报告(中文) | 4 | 34 | 中文报告要素库 |
| 科技报告(外文) | 1 | 15 | 外文报告要素库 |
| **合计** | **186** | **2253** | **20 个 Sheet** |

## 3. 全量表目录（按数据域）

### 金融/宏观（3 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_series_metadata` | 序列元数据 | 15 | - |
| 2 | `dwd_series_timepoints` | 序列时间点 | 2 | - |
| 3 | `dwd_macro_index_data` | 数据表 | 9 | rid |

### 行业研究（1 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_document_metadata` | 文档元数据 | 21 | id |

### 产业链（5 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_industry_chain_info` | 产业链图谱 | 16 | - |
| 2 | `dwd_org_industry_chain_dtl` | 产业关联企业信息 | 10 | - |
| 3 | `dwd_org_industry_chain_prod_dtl` | 产业链企业关联产品信息 | 10 | - |
| 4 | `dwd_org_industry_chain_pat_dtl` | 产业链关联专利信息 | 14 | - |
| 5 | `dwd_industry_chain_news_info` | 产业动态资讯 | 10 | - |

### 企业/机构(国内)（41 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_org_reg_info` | 机构基本信息 | 25 | - |
| 2 | `dwd_org_shareholder_info` | 股东信息 | 10 | - |
| 3 | `dwd_org_executive_info` | 高管信息 | 8 | - |
| 4 | `dwd_org_org_product_info` | 经营信息 | 10 | - |
| 5 | `dwd_org_annual_financial_info` | 年报财务信息 | 16 | - |
| 6 | `dwd_org_important_news_info` | 重点资讯 | 10 | - |
| 7 | `dwd_org_changerecord_info` | 工商变更信息 | 10 | - |
| 8 | `dwd_org_merger_acquisition_info` | 并购事件 | 6 | - |
| 9 | `dwd_org_financing_info` | 融资事件 | 12 | - |
| 10 | `dwd_org_invest_info` | 投资事件 | 11 | - |
| 11 | `dwd_org_bid_info` | 招投标事件 | 11 | - |
| 12 | `dwd_org_recruit_info` | 招聘信息 | 11 | - |
| 13 | `dwd_org_hels_info` | 高校/科研机构信息 | 21 | - |
| 14 | `dwd_org_rd_achiev_info` | 研发成果产出 | 34 | - |
| 15 | `dwd_org_tag_info` | 机构标签表 | 8 | - |
| 16 | `dwd_org_stock_base` | 上市企业基本信息 | 11 | - |
| 17 | `dwd_org_stock_finance_info` | 上市企业主要财务指标 | 20 | - |
| 18 | `dwd_org_company_abnormal` | 经营异常 | 15 | - |
| 19 | `dwd_org_company_punish` | 行政处罚 | 24 | - |
| 20 | `dwd_org_company_illegal` | 严重违法 | 16 | - |
| 21 | `dwd_org_risk_tax_punish` | 税收违法 | 30 | - |
| 22 | `dwd_org_opt_judicial_case` | 司法案件 | 16 | - |
| 23 | `dwd_org_risk_shixin` | 失信被执行人 | 32 | - |
| 24 | `dwd_org_risk_zhixing` | 被执行人 | 20 | - |
| 25 | `dwd_org_risk_xianxiao` | 限制高消费 | 16 | - |
| 26 | `dwd_org_risk_lawsuit` | 裁判文书 | 26 | - |
| 27 | `dwd_org_risk_court_filed_case` | 法院立案 | 20 | - |
| 28 | `dwd_org_risk_lawsuit_list` | 裁判文书当事人 | 15 | - |
| 29 | `dwd_org_risk_court_filed_case_litigant` | 法院立案当事人 | 12 | - |
| 30 | `dwd_org_risk_court_notice` | 开庭公告 | 23 | - |
| 31 | `dwd_org_risk_court_notice_list` | 开庭公告当事人 | 16 | - |
| 32 | `dwd_org_risk_court_announcement` | 法院公告 | 29 | - |
| 33 | `dwd_org_risk_court_announcement_list` | 法院公告当事人 | 14 | - |
| 34 | `dwd_org_company_justice` | 股权冻结 | 16 | - |
| 35 | `dwd_org_company_pledge` | 股权出质 | 31 | - |
| 36 | `dwd_org_risk_zhongben` | 终本案件 | 21 | - |
| 37 | `dwd_org_company_chattel` | 动产抵押 | 20 | - |
| 38 | `dwd_org_tb_judicial_sale` | 司法拍卖 | 13 | - |
| 39 | `dwd_org_tb_judicial_sale_info_company` | 司法拍卖当事人 | 9 | - |
| 40 | `dwd_org_bankruptcy_public_cases` | 破产案件 | 15 | - |
| 41 | `dwd_org_bankruptcy_public_cases_list` | 破产案件当事人 | 13 | - |

### 企业/机构(国外)（8 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_forg_base_info` | 海外机构基本信息 | 20 | - |
| 2 | `dwd_forg_shareholder_info` | 海外机构股东股权关联信息 | 5 | - |
| 3 | `dwd_forg_subsidiary_info` | 海外机构子公司股权关联信息 | 6 | - |
| 4 | `dwd_forg_executive_info` | 海外机构高管信息 | 6 | - |
| 5 | `dwd_forg_product_info` | 海外机构公司经营信息 | 3 | - |
| 6 | `dwd_forg_beneficiary_info` | 海外机构受益人信息（新增表） | 10 | - |
| 7 | `dwd_forg_act_contro_info` | 海外机构实控人信息（新增表） | 11 | - |
| 8 | `dwd_forg_stock_fin_info` | 海外上市企业财务信息 | 15 | - |

### 人才（2 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_scholar` | 学者 | 25 | - |
| 2 | `dwd_scholar_papers` | 论文信息 | 13 | - |

### 政策(国内)（1 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_zck_policy` | 国内政策信息 | 20 | id |

### 政策(国外)（1 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_zck_intl_policy` | 国际政策信息 | 16 | id |

### 行业专题(医药)（19 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_drug` | 药品信息表 | 10 | id |
| 2 | `dwd_medical_device` | 医疗器械表 | 6 | id |
| 3 | `dwd_clinical` | 临床信息表 | 9 | id |
| 4 | `dwd_market` | 药品市场表 | 3 | id |
| 5 | `dwd_company` | 药品企业表 | 4 | id |
| 6 | `dwd_protein` | 蛋白质表 | 6 | id |
| 7 | `dwd_multi_omics` | 多组学表 | 5 | id |
| 8 | `dwd_drug_profile` | 药物档案表 | 9 | id |
| 9 | `dwd_safety` | 药物安全表 | 3 | id |
| 10 | `dwd_clinical_trial` | 临床试验信息表 | 3 | id |
| 11 | `dwd_deal` | 药物交易 | 4 | id |
| 12 | `dwd_drug_substance` | 化合物性质与信息 | 6 | id |
| 13 | `dwd_crystal_structure` | 晶体结构与性质 | 3 | id |
| 14 | `dwd_calculation` | 分子理论计算 | 3 | id |
| 15 | `dwd_material_virtual_structure` | 材料虚拟结构 | 3 | id |
| 16 | `dwd_small_molecule_screening` | 小分子活性与筛选 | 3 | id |
| 17 | `dwd_information` | 医疗资讯 | 5 | id |
| 18 | `dwd_job` | 招聘 | 5 | id |
| 19 | `dwd_event` | 会展 | 6 | id |

### 行业专题(化学)（7 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_substance` | 物质信息表 | 23 | id |
| 2 | `dwd_react_detail` | 化学反应信息表 | 8 | id |
| 3 | `dwd_rel_reaction_substance` | 反应-物质关联表 | 6 | id |
| 4 | `dwd_molecular_spectrum` | 分子谱图 | 12 | id |
| 5 | `dwd_similar_substance` | 结构相近的其他分子 | 6 | - |
| 6 | `dwd_rel_substance_paper` | 物质-论文关联表 | 3 | id |
| 7 | `dwd_ods_substance_patent` | 物质-专利关联表 | 3 | id |

### 行业专题(海洋)（35 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_hycy_index` | 海洋产业_指标库 | 12 | logic_id |
| 2 | `dwd_hycy_aquatic_new_species` | 海洋产业_水产新品种认定情况及育种单位统计表 | 5 | logic_id |
| 3 | `dwd_hycy_marine_energy_industry_carrier` | 海洋产业_海洋能源创新平台载体名单 | 8 | logic_id |
| 4 | `dwd_hycy_offshore_fishing_company_evaluation` | 海洋产业_全国远洋渔业企业履约评估表 | 7 | logic_id |
| 5 | `dwd_hycy_sz_maritime_law_attorneys` | 海洋产业_深圳海事海商律所及执业律师 | 8 | logic_id |
| 6 | `dwd_hycy_port_operation_license_form` | 海洋产业_港口经营许可表 | 18 | logic_id |
| 7 | `dwd_hycy_international_shipping_certificate_effective_enterprise` | 海洋产业_国际班轮运输经营资格登记证有效企业 | 7 | logic_id |
| 8 | `dwd_hycy_shanghai_domestic_water_transportation_trading_director` | 海洋产业_上海市国内水路运输经营名录 | 6 | logic_id |
| 9 | `dwd_hycy_international_shipping_agency_enterprises_registration` | 海洋产业_国际船舶代理企业备案表 | 6 | logic_id |
| 10 | `dwd_hycy_pelagic_fishery_enterprises_performance_evaluation_resu` | 海洋产业_远洋渔业企业履约评估结果 | 4 | logic_id |
| 11 | `dwd_hycy_aquaculture_veterinary_drugs_enterprise_list` | 海洋产业_水产养殖用兽药名录 | 10 | logic_id |
| 12 | `dwd_hycy_nvocc_operator_list` | 海洋产业_无船承运业务经营者名录 | 4 | logic_id |
| 13 | `dwd_hycy_china_classification_society_marine_product_list` | 海洋产业_中国船级社船用产品目录 | 6 | logic_id |
| 14 | `dwd_hycy_csad_ship` | 海洋产业_CSAD船舶 | 8 | logic_id |
| 15 | `dwd_hycy_enterprise_indicators` | 海洋产业_企业指标表 | 7 | logic_id |
| 16 | `dwd_hycy_global_cruise_capacity_distribution` | 海洋产业_全球邮轮运力分布 | 8 | logic_id |
| 17 | `dwd_hycy_china_offshore_field` | 海洋产业_中国海上油气田信息 | 8 | logic_id |
| 18 | `dwd_hycy_china_major_city_lng_receiving_capacity` | 海洋产业_中国主要城市LNG接收能力 | 8 | logic_id |
| 19 | `dwd_hycy_china_offshore_production_growth` | 海洋产业_中国海洋油气产量增长情况 | 7 | logic_id |
| 20 | `dwd_hycy_china_offshore_production` | 海洋产业_中国海洋油气田产量情况 | 6 | logic_id |
| 21 | `dwd_hycy_leading_maritime_capitals` | 海洋产业_世界领先海事之都报告城市数据 | 7 | logic_id |
| 22 | `dwd_hycy_submarine_cable_distribution` | 海洋产业_海底光缆分布 | 5 | logic_id |
| 23 | `dwd_hycy_china_ocean_large_model` | 海洋产业_国内海洋大模型情况 | 6 | logic_id |
| 24 | `dwd_hycy_china_mainland_submarine_cable` | 海洋产业_中国大陆地区海底光缆情况 | 9 | logic_id |
| 25 | `dwd_hycy_methanol_production_cost_trend_prediction` | 海洋产业_甲醇生产成本及趋势预测 | 5 | logic_id |
| 26 | `dwd_hycy_ship_management_enterprise_trustee_ship` | 海洋产业_船舶管理企业代管船舶表 | 13 | logic_id |
| 27 | `dwd_hycy_gas_supply` | 海洋产业_天然气供应信息表 | 14 | logic_id |
| 28 | `dwd_hycy_green_fuel_enterprise` | 海洋产业_绿色燃料加注产业信息表 | 8 | logic_id |
| 29 | `dwd_hycy_shipping_capacity` | 海洋产业_航运运力表 | 21 | logic_id |
| 30 | `dwd_hycy_marine_alternative_fuel_cost` | 海洋产业_船用替代燃料生产成本对比表 | 7 | logic_id |
| 31 | `dwd_hycy_global_alternative_marine_fuel_market_demand_scale` | 海洋产业_船用替代燃料全球市场需求及规模预测 | 5 | logic_id |
| 32 | `dwd_hai_yang_shi_ce_shu_ju` | 海洋实测数据 | 15 | zhu_jian |
| 33 | `dwd_hai_yang_fen_xi_yu_bao_shu_ju` | 海洋分析预报数据 | 9 | zhu_jian |
| 34 | `dwd_hai_yang_di_li_yao_gan_shu_ju` | 海洋地理遥感数据 | 9 | zhu_jian |
| 35 | `dwd_shang_lian_jie_guo_biao` | 上链结果表 | 10 | zhu_jian |

### 行业专题(量子)/企业工商（25 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_industry_code` | 产业链 | 9 | id |
| 2 | `dwd_company_base` | 基础信息 | 36 | id |
| 3 | `dwd_company_branch` | 分支机构 | 13 | id |
| 4 | `dwd_company_change` | 工商变更 | 11 | id |
| 5 | `dwd_company_history_name` | 曾用名 | 8 | id |
| 6 | `dwd_company_license` | 行政许可 | 12 | id |
| 7 | `dwd_company_nei_code` | 国民行业经济分类 | 14 | id |
| 8 | `dwd_company_reg_cap_change` | 注册资本变更 | 10 | id |
| 9 | `dwd_company_shareholder` | 股东信息 | 21 | id |
| 10 | `dwd_company_staff` | 任职人员 | 12 | id |
| 11 | `dwd_company_transition_clean` | 注册地址变更 | 10 | id |
| 12 | `dwd_company_basic_tags` | 基础属性标签 | 7 | id |
| 13 | `dwd_company_brief_tags` | 企业简介 | 5 | id |
| 14 | `dwd_company_location_tags` | 所在行政区 | 8 | id |
| 15 | `dwd_company_contact_tags` | 企业联系方式 | 5 | id |
| 16 | `dwd_company_recruit` | 招聘 | 24 | id |
| 17 | `dwd_company_industry_tags` | 产业标签 | 5 | id |
| 18 | `dwd_company_diy_tags` | 特色资质标签 | 5 | id |
| 19 | `dwd_company_honor_tags` | 企业荣誉标签 | 15 | id |
| 20 | `dwd_liang_zi_qian_yan_ren_cai` | 量子前沿人才 | 7 | zhu_jian |
| 21 | `dwd_liang_zi_chan_pin_xin_xi` | 量子产品信息 | 9 | zhu_jian |
| 22 | `dwd_liang_zi_yan_fa_jin_zhan` | 量子研发进展 | 10 | zhu_jian |
| 23 | `dwd_liang_zi_shi_chang_gui_mo` | 量子市场规模 | 8 | zhu_jian |
| 24 | `dwd_liang_zi_ji_shu_qu_shi` | 量子技术趋势 | 9 | zhu_jian |
| 25 | `dwd_shang_lian_jie_guo_biao_2` | 上链结果表 | 10 | zhu_jian |

### 论文(中文)（9 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_zh_paper` | 中文论文详情信息 | 22 | id |
| 2 | `dwd_zh_paper_title` | 中文论文标题信息 | 11 | logic_id, id |
| 3 | `dwd_zh_paper_abstract` | 中文论文摘要信息 | 10 | logic_id, id |
| 4 | `dwd_zh_author` | 中文文献作者详情信息 | 13 | logic_id |
| 5 | `dwd_zh_journal` | 中文期刊详情信息 | 33 | logic_id |
| 6 | `dwd_zh_paper_reference` | 中文论文参考文献信息 | 14 | logic_id, id |
| 7 | `dwd_zh_paper_citation` | 中文论文引用文献信息 | 9 | logic_id, id |
| 8 | `dwd_zh_paper_classification` | 中文论文分类信息 | 8 | logic_id, id |
| 9 | `dwd_zh_paper_related` | 中文论文关联文献信息 | 8 | logic_id, id |

### 论文(外文)（10 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_en_paper` | 英文论文详情信息 | 23 | id |
| 2 | `dwd_en_paper_title` | 英文论文标题信息 | 11 | logic_id, id |
| 3 | `dwd_en_paper_abstract` | 英文论文摘要信息 | 10 | logic_id, id |
| 4 | `dwd_en_author` | 英文文献作者详情信息 | 13 | logic_id |
| 5 | `dwd_en_journal` | 英文期刊详情信息 | 28 | logic_id |
| 6 | `dwd_en_paper_reference` | 英文论文参考文献信息 | 14 | logic_id, id |
| 7 | `dwd_en_paper_citation` | 英文论文引用文献信息 | 9 | logic_id, id |
| 8 | `dwd_en_paper_funding` | 英文论文基金信息 | 6 | logic_id, id |
| 9 | `dwd_en_paper_classification` | 英文论文分类信息 | 8 | logic_id, id |
| 10 | `dwd_en_paper_related` | 英文论文关联文献信息 | 8 | logic_id, id |

### 专利（7 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_patent` | 专利信息表 | 76 | id |
| 2 | `dwd_patent_cited` | 专利引用关系表 | 17 | id |
| 3 | `dwd_patent_title` | 专利标题信息表 | 8 | id |
| 4 | `dwd_patent_abstract` | 专利摘要信息表 | 8 | id |
| 5 | `dwd_patent_legal` | 法律状态信息表 | 16 | id |
| 6 | `dwd_patent_transfer` | 专利转移信息表 | 11 | id |
| 7 | `dwd_patent_family` | 专利家族信息表 | 14 | id |

### 科研项目(国内)（5 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_zh_project` | 国内项目信息表 | 22 | id |
| 2 | `dwd_zh_project_output` | 国内项目-产出信息 | 25 | id |
| 3 | `dwd_rel_project_scholar` | 项目-人才关联表 | 4 | id |
| 4 | `dwd_rel_project_paper` | 项目-论文关联表 | 5 | id |
| 5 | `dwd_rel_project_patent` | 项目-专利关联表 | 4 | id |

### 科研项目(国外)（2 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_en_project` | 国外项目信息表 | 22 | - |
| 2 | `dwd_en_project_output` | 国外项目-产出信息 | 25 | id |

### 科技报告(中文)（4 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_zh_report` | 中文科技报告信息表 | 20 | - |
| 2 | `dwd_rel_report_scholar` | 报告-人才关联表 | 4 | id |
| 3 | `dwd_rel_report_paper` | 报告-论文关联表 | 5 | id |
| 4 | `dwd_rel_report_project` | 报告-项目关联表 | 5 | id |

### 科技报告(外文)（1 张表）

| # | 表名 | 中文名 | 字段数 | 主键 |
|---|------|--------|--------|------|
| 1 | `dwd_en_report` | 外文科技报告信息表 | 15 | - |

## 4. 企业/政策相关表字段明细

> 本节聚焦本次 POC 重点分析的**企业相关**与**政策相关** ODS 表的完整字段，供映射报告引用。其余领域（论文/专利/项目/报告/行业专题等）表结构详见 `db/要素库建表语句.sql`。

### 4.1 企业相关 — 国内机构（41 张表）

#### `dwd_org_reg_info` — 机构基本信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 25

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | province | VARCHAR(255) | 是 | 所在省份 |
| 5 | city | VARCHAR(255) | 是 | 所在城市 |
| 6 | address | TEXT | 是 | 公司地址 |
| 7 | addr_lng | VARCHAR(255) | 是 | 地址对应经度 |
| 8 | addr_lat | VARCHAR(255) | 是 | 地址对应维度 |
| 9 | postal_code | VARCHAR(255) | 是 | 邮政编码 |
| 10 | phone | VARCHAR(255) | 是 | 联系电话 |
| 11 | email | TEXT | 是 | 电子邮箱 |
| 12 | lerep | VARCHAR(255) | 是 | 法人名字 |
| 13 | org_size | VARCHAR(255) | 是 | 企业规模 |
| 14 | registration_org | VARCHAR(255) | 是 | 登记机关 |
| 15 | incorporation_year | DOUBLE | 是 | 成立年份 |
| 16 | incorporation_date | DATE | 是 | 成立日期 |
| 17 | start_date | VARCHAR(255) | 是 | 经营期限自 |
| 18 | end_date | VARCHAR(255) | 是 | 经营期限至 |
| 19 | listing_status | VARCHAR(255) | 是 | 上市状态 |
| 20 | listing_date | DATE | 是 | 上市日期 |
| 21 | registered_capital_value | DOUBLE | 是 | 注册资本(本币元) |
| 22 | capital_currency_code | VARCHAR(255) | 是 | 资本货币代码；值域: qhdata_standard.dim_currency_code；货币代码映射对应的货币名称。 |
| 23 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 24 | created_time | DATETIME | 否 | 创建时间 |
| 25 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_shareholder_info` — 股东信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | inv_org_id | VARCHAR(255) | 是 | 股东id；机构身份唯一id，用于关联其它表。 |
| 5 | owners_name | VARCHAR(255) | 否 | 股东名称 |
| 6 | owners_type | VARCHAR(255) | 是 | 股东类型 |
| 7 | ownership_percentage | DOUBLE | 是 | 所有权占比(%) |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_executive_info` — 高管信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 8

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | executives_name | VARCHAR(255) | 否 | 高管姓名 |
| 5 | executives_position | VARCHAR(255) | 是 | 职位名称 |
| 6 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 7 | created_time | DATETIME | 否 | 创建时间 |
| 8 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_org_product_info` — 经营信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | industry_class | VARCHAR(255) | 否 | 公司行业分类；值域: qhdata_standard.map_industry_code_2017；行业代码映射行业门类名称、大类名称、中类名称、小类名称。 |
| 5 | main_activities | TEXT | 是 | 公司经营范围 |
| 6 | description | TEXT | 是 | 业务描述 |
| 7 | main_prod | VARCHAR(255) | 是 | 主要产品 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_annual_financial_info` — 年报财务信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | year | DOUBLE | 否 | 年报年度 |
| 5 | total_assets | VARCHAR(255) | 是 | 资产总额 |
| 6 | total_liabilities | VARCHAR(255) | 是 | 负债总额 |
| 7 | operating_revenue | VARCHAR(255) | 是 | 营业收入 |
| 8 | main_business_revenue | VARCHAR(255) | 是 | 主营业务收入 |
| 9 | total_profit | VARCHAR(255) | 是 | 利润总额 |
| 10 | pure_profit | VARCHAR(255) | 是 | 净利润 |
| 11 | total_tax_paid | VARCHAR(255) | 是 | 纳税总额 |
| 12 | owners_equity | VARCHAR(255) | 是 | 所有者权益合计 |
| 13 | employees_number | VARCHAR(255) | 是 | 从业人数 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_important_news_info` — 重点资讯

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | news_title | TEXT | 是 | 资讯标题 |
| 5 | news_date | DATE | 是 | 资讯日期 |
| 6 | news_content | TEXT | 是 | 资讯内容 |
| 7 | original_textlink | TEXT | 是 | 咨询原文链接 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_changerecord_info` — 工商变更信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | update_content | VARCHAR(255) | 否 | 变更类型 |
| 5 | current_name | TEXT | 是 | 变更前内容 |
| 6 | update_name | TEXT | 是 | 变更后内容 |
| 7 | update_date | DATE | 否 | 变更日期 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_merger_acquisition_info` — 并购事件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 6

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | acquiring_org_id | VARCHAR(255) | 否 | 发起收购企业id；机构身份唯一id，用于关联其它表。 |
| 2 | acquiring_name | VARCHAR(255) | 否 | 发起收购企业名称 |
| 3 | acquired_org_id | VARCHAR(255) | 否 | 被收购企业id；机构身份唯一id，用于关联其它表。 |
| 4 | acquired_name | VARCHAR(255) | 否 | 被收购企业名称 |
| 5 | ma_amount | DOUBLE | 是 | 并购金额(元) |
| 6 | currency_code | VARCHAR(255) | 是 | 并购金额币种；值域: qhdata_standard.dim_currency_code；货币代码映射对应的货币名称。 |

#### `dwd_org_financing_info` — 融资事件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 12

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | funding_round | VARCHAR(255) | 是 | 融资轮次 |
| 5 | funding_amount | DOUBLE | 是 | 获投金额(元) |
| 6 | funding_currency_code | VARCHAR(255) | 是 | 金额币种 |
| 7 | post_valuation | DOUBLE | 是 | 投后估值 |
| 8 | completion_date | DATE | 是 | 融资完成时间 |
| 9 | investors_name | TEXT | 否 | 投资方列表 |
| 10 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 11 | created_time | DATETIME | 否 | 创建时间 |
| 12 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_invest_info` — 投资事件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | inv_org_id | VARCHAR(255) | 否 | 被投企业id；机构身份唯一id，用于关联其它表。 |
| 5 | inv_name | VARCHAR(255) | 否 | 被投资企业名称 |
| 6 | inv_external_id | VARCHAR(255) | 是 | 被投资企业统一社会信用代码 |
| 7 | investment_amount | DOUBLE | 是 | 投资金额(元) |
| 8 | investment_ratio | DOUBLE | 是 | 股权占比(%) |
| 9 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 10 | created_time | DATETIME | 否 | 创建时间 |
| 11 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_bid_info` — 招投标事件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | tender_org_id | VARCHAR(255) | 否 | 采购单位id；机构身份唯一id，用于关联其它表。 |
| 2 | tender_name_cn | VARCHAR(255) | 否 | 采购单位名称 |
| 3 | tender_external_id | VARCHAR(255) | 是 | 采购单位统一社会信用代码 |
| 4 | winner_org_id | VARCHAR(255) | 否 | 中标单位id；机构身份唯一id，用于关联其它表。 |
| 5 | winner_name_cn | VARCHAR(255) | 否 | 中标单位名称 |
| 6 | winner_external_id | VARCHAR(255) | 是 | 中标单位统一社会信用代码 |
| 7 | announcement_title | TEXT | 是 | 公告标题 |
| 8 | announcement_content | TEXT | 是 | 中标成交信息 |
| 9 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 10 | created_time | DATETIME | 否 | 创建时间 |
| 11 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_recruit_info` — 招聘信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | job_title | VARCHAR(255) | 是 | 岗位 |
| 5 | job_description | TEXT | 是 | 工作描述 |
| 6 | work_place | TEXT | 是 | 工作地点 |
| 7 | release_date | DATE | 是 | 发布日期 |
| 8 | hiring_number | DOUBLE | 是 | 招聘人数 |
| 9 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 10 | created_time | DATETIME | 否 | 创建时间 |
| 11 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_hels_info` — 高校/科研机构信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 21

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 高校id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | org_name | VARCHAR(255) | 否 | 高校/科研机构名称(中文) |
| 5 | org_name_en | VARCHAR(255) | 是 | 高校/科研机构名称(英文) |
| 6 | org_desc | TEXT | 是 | 高校/科研机构描述 |
| 7 | est_year | DATE | 是 | 建立时间 |
| 8 | address | TEXT | 是 | 地址(国家、区域、城市) |
| 9 | addr_lng | VARCHAR(255) | 是 | 地址对应经度 |
| 10 | addr_lat | VARCHAR(255) | 是 | 地址对应维度 |
| 11 | province | VARCHAR(255) | 是 | 地址所在省 |
| 12 | city | VARCHAR(255) | 是 | 地址所在市 |
| 13 | univ_type | VARCHAR(255) | 是 | 高校类型 |
| 14 | web_link | TEXT | 是 | 官方网址 |
| 15 | postal_code | VARCHAR(255) | 是 | 邮政编码 |
| 16 | email | TEXT | 是 | 电子邮箱 |
| 17 | contact_number | VARCHAR(255) | 是 | 联系电话 |
| 18 | fax_number | VARCHAR(255) | 是 | 传真号码 |
| 19 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 20 | created_time | DATETIME | 否 | 创建时间 |
| 21 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_rd_achiev_info` — 研发成果产出

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 34

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | inv_pat_auth_num | DOUBLE | 是 | 发明专利授权数 |
| 5 | util_pat_auth_num | DOUBLE | 是 | 实用新型专利授权数 |
| 6 | des_pat_auth_num | DOUBLE | 是 | 外观设计专利授权数 |
| 7 | soft_copyright_num | DOUBLE | 是 | 软件著作权数 |
| 8 | publis_papers_sum | DOUBLE | 是 | 发表论文数（论文） |
| 9 | nat_ip_num | DOUBLE | 是 | 认定国家级平台载体数 |
| 10 | province_ip_num | DOUBLE | 是 | 认定省级平台载体数 |
| 11 | city_ip_num | DOUBLE | 是 | 认定市级平台载体数（无法提供） |
| 12 | form_intl_std_num | DOUBLE | 是 | 制定国际标准数（无法提供） |
| 13 | form_nat_std_num | DOUBLE | 是 | 制定国家标准数（无法提供） |
| 14 | form_ind_std_num | DOUBLE | 是 | 制定行业标准数（无法提供） |
| 15 | nat_tech_award_sum | DOUBLE | 是 | 获得国家级科技奖项数（无法提供） |
| 16 | province_tech_award_sum | DOUBLE | 是 | 获得省科技奖项数（无法提供） |
| 17 | city_tech_award_sum | DOUBLE | 是 | 获得市科技奖项数（无法提供） |
| 18 | pct_pat_num | DOUBLE | 是 | PCT专利数 |
| 19 | ei_thesis_sum | DOUBLE | 是 | EI论文数量（论文） |
| 20 | sci_thesis_sum | DOUBLE | 是 | SCI论文数量（论文） |
| 21 | cn_sum | DOUBLE | 是 | 中文专著数量（论文） |
| 22 | fm_sum | DOUBLE | 是 | 外文专著数量（论文） |
| 23 | nat_eng_center | DOUBLE | 是 | 国家级工程中心 |
| 24 | province_eng_center | DOUBLE | 是 | 省级工程中心 |
| 25 | city_eng_center | DOUBLE | 是 | 市级工程中心（无法提供） |
| 26 | nat_key_lab | DOUBLE | 是 | 国家级重点实验室 |
| 27 | province_key_lab | DOUBLE | 是 | 省级重点实验室 |
| 28 | city_key_lab | DOUBLE | 是 | 市级重点实验室（无法提供） |
| 29 | new_variety_sum | DOUBLE | 是 | 新品种数（无法提供） |
| 30 | new_drug_cert_sum | DOUBLE | 是 | 新药证书数（无法提供） |
| 31 | ic_layout_copyright_sum | DOUBLE | 是 | IC布图版权数（无法提供） |
| 32 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 33 | created_time | DATETIME | 否 | 创建时间 |
| 34 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_tag_info` — 机构标签表

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 8

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | org_tag | VARCHAR(255) | 否 | 企业标签 |
| 5 | tag_level | VARCHAR(255) | 否 | 级别 |
| 6 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 7 | created_time | DATETIME | 否 | 创建时间 |
| 8 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_stock_base` — 上市企业基本信息

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | stock_code | VARCHAR(255) | 否 | 股票代码 |
| 2 | stock_noun | VARCHAR(255) | 是 | 股票简称 |
| 3 | stock_type | VARCHAR(255) | 是 | 上市板块 |
| 4 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 5 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 6 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 7 | listed_date | DATE | 是 | 上市日期 |
| 8 | listed_status | VARCHAR(255) | 是 | 上市状态 |
| 9 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 10 | created_time | DATETIME | 否 | 创建时间 |
| 11 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_stock_finance_info` — 上市企业主要财务指标

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id；机构身份唯一id，用于关联其它表。 |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | stock_code | VARCHAR(255) | 否 | 股票代码 |
| 4 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 5 | occur_period | VARCHAR(255) | 否 | 数据期 |
| 6 | total_assets | DOUBLE | 是 | 资产总额(元) |
| 7 | fixed_assets | DOUBLE | 是 | 固定资产总额(元) |
| 8 | total_liabilities | DOUBLE | 是 | 负债总额(元) |
| 9 | operating_revenue | DOUBLE | 是 | 营业收入(元) |
| 10 | main_business_revenue | DOUBLE | 是 | 主营业务收入(元) |
| 11 | total_profit | DOUBLE | 是 | 利润总额(元) |
| 12 | pure_profit | DOUBLE | 是 | 净利润(元) |
| 13 | total_tax_paid | DOUBLE | 是 | 纳税总额(元) |
| 14 | oper_cash_flow | DOUBLE | 是 | 经营活动现金流(元) |
| 15 | owners_equity | DOUBLE | 是 | 所有者权益合计(元) |
| 16 | employees_number | DOUBLE | 是 | 从业人数 |
| 17 | research_development_amount | DOUBLE | 是 | 研发投入金额(元) |
| 18 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 19 | created_time | DATETIME | 否 | 创建时间 |
| 20 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_company_abnormal` — 经营异常

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 15

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | abnormal_id | VARCHAR(255) | 否 | 经营异常记录id；经营异常记录唯一标识id。 |
| 5 | abn_reason | TEXT | 是 | 列入原因 |
| 6 | abn_date | DATE | 是 | 列入时间 |
| 7 | abn_org | VARCHAR(255) | 是 | 列入机关 |
| 8 | remove_reason | TEXT | 是 | 移除原因 |
| 9 | remove_date | DATE | 是 | 移除时间 |
| 10 | remove_org | VARCHAR(255) | 是 | 移除机关 |
| 11 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 12 | status | VARCHAR(255) | 是 | 状态 |
| 13 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 14 | created_time | DATETIME | 否 | 创建时间；值域: 否 |
| 15 | updated_time | DATETIME | 否 | 更新时间；值域: 否 |

#### `dwd_org_company_punish` — 行政处罚

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 24

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | penalty_id | VARCHAR(255) | 否 | 行政处罚记录id；行政处罚记录唯一标识id。 |
| 5 | decision_no | VARCHAR(255) | 是 | 决定书文号 |
| 6 | violation_type | TEXT | 是 | 违法行为类型 |
| 7 | penalty_content | TEXT | 是 | 行政处罚内容 |
| 8 | decision_org | VARCHAR(255) | 是 | 决定机关 |
| 9 | penalty_date | DATE | 是 | 处罚决定日期 |
| 10 | public_date | DATE | 是 | 公示日期 |
| 11 | penalty_basis | TEXT | 是 | 处罚依据 |
| 12 | violation_fact | TEXT | 是 | 主要违法事实 |
| 13 | penalty_type | VARCHAR(255) | 是 | 处罚种类 |
| 14 | fine_amount | DOUBLE | 是 | 罚款金额 |
| 15 | confiscate_amount | DOUBLE | 是 | 没收金额 |
| 16 | license_info | TEXT | 是 | 暂扣或吊销证照名称及编号 |
| 17 | validity_period | VARCHAR(255) | 是 | 处罚有效期 |
| 18 | public_deadline | DATE | 是 | 公示截止日期 |
| 19 | remark | TEXT | 是 | 备注 |
| 20 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 21 | status | VARCHAR(255) | 是 | 状态 |
| 22 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 23 | created_time | DATETIME | 否 | 创建时间 |
| 24 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_company_illegal` — 严重违法

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | sv_id | VARCHAR(255) | 否 | 严重违法记录id；严重违法记录唯一标识id。 |
| 5 | category | VARCHAR(255) | 是 | 类别 |
| 6 | abn_reason | TEXT | 是 | 列入原因 |
| 7 | abn_date | DATE | 是 | 列入时间 |
| 8 | abn_org | VARCHAR(255) | 是 | 列入机关 |
| 9 | remove_reason | TEXT | 是 | 移除原因 |
| 10 | remove_date | DATE | 是 | 移除时间 |
| 11 | remove_org | VARCHAR(255) | 是 | 移除机关 |
| 12 | status | VARCHAR(255) | 是 | 状态 |
| 13 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_tax_punish` — 税收违法

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 30

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | taxpayer_name | VARCHAR(255) | 否 | 纳税人名称；纳税人登记名称。 |
| 2 | tax_vio_id | VARCHAR(255) | 否 | 唯一索引id；税收违法记录唯一标识id。 |
| 3 | report_period | VARCHAR(255) | 是 | 案件上报期 |
| 4 | taxpayer_id | VARCHAR(255) | 是 | 纳税人识别码 |
| 5 | org_code | VARCHAR(255) | 是 | 组织机构代码 |
| 6 | reg_address | TEXT | 是 | 注册地址 |
| 7 | publish_date | DATE | 是 | 发布日期 |
| 8 | legal_name | VARCHAR(255) | 是 | 法定代表人或者负责人姓名 |
| 9 | legal_gender | VARCHAR(255) | 是 | 法定代表人或者负责人性别 |
| 10 | legal_id_type | VARCHAR(255) | 是 | 法定代表人或者负责人证件类型 |
| 11 | legal_id_no | VARCHAR(255) | 是 | 法定代表人或者负责人证件号码 |
| 12 | finance_name | VARCHAR(255) | 是 | 负有直接责任的财务负责人姓名 |
| 13 | finance_gender | VARCHAR(255) | 是 | 负有直接责任的财务负责人性别 |
| 14 | finance_id_type | VARCHAR(255) | 是 | 负有直接责任的财务负责人证件类型 |
| 15 | finance_id_no | VARCHAR(255) | 是 | 负有直接责任的财务负责人证件号码 |
| 16 | agency_info | TEXT | 是 | 负有直接责任的中介机构信息及其从业人员信息 |
| 17 | case_type | VARCHAR(255) | 是 | 案件性质 |
| 18 | illegal_fact | TEXT | 是 | 主要违法事实 |
| 19 | punish_basis | TEXT | 是 | 相关法律依据及税务处理处罚情况 |
| 20 | tax_authority | VARCHAR(255) | 是 | 所属税务机关 |
| 21 | original_link | TEXT | 是 | 数据原始连接 |
| 22 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 23 | original_source | VARCHAR(255) | 是 | 原始数据来源 |
| 24 | org_id | VARCHAR(255) | 是 | 机构id |
| 25 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 26 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 27 | is_history | VARCHAR(255) | 是 | 是否历史；是否历史记录，0正常；1历史。 |
| 28 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 29 | created_time | DATETIME | 否 | 创建时间 |
| 30 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_opt_judicial_case` — 司法案件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | company_name | VARCHAR(255) | 否 | 企业名称；企业登记名称。 |
| 2 | reg_no | VARCHAR(255) | 是 | 注册号 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | org_id | VARCHAR(255) | 是 | 机构id |
| 5 | case_id | VARCHAR(255) | 否 | 司法案件唯一标识；司法案件记录唯一标识id。 |
| 6 | case_title | TEXT | 是 | 案件标题 |
| 7 | case_type_tag | VARCHAR(255) | 是 | 案件类型标签 |
| 8 | case_no | VARCHAR(255) | 是 | 案号 |
| 9 | case_cause | VARCHAR(255) | 是 | 案由 |
| 10 | case_role | VARCHAR(255) | 是 | 案件身份 |
| 11 | current_procedure | VARCHAR(255) | 是 | 当前审理程序 |
| 12 | procedure_date | DATE | 是 | 当前审理程序日期 |
| 13 | data_use_flag | VARCHAR(255) | 是 | 数据使用标识 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_shixin` — 失信被执行人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 32

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | dishonest_id | VARCHAR(255) | 是 | 失信被执行人id；失信被执行人记录唯一标识id。 |
| 2 | org_id | VARCHAR(255) | 是 | 机构id |
| 3 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 4 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 5 | official_id | VARCHAR(255) | 是 | 官网id |
| 6 | case_no | VARCHAR(255) | 否 | 案号 |
| 7 | dishonest_name | VARCHAR(255) | 是 | 失信人名称 |
| 8 | gender | VARCHAR(255) | 是 | 性别 |
| 9 | age | VARCHAR(255) | 是 | 年龄 |
| 10 | credit_code | VARCHAR(255) | 是 | 统一信用代码 |
| 11 | reg_no | VARCHAR(255) | 是 | 企业注册号 |
| 12 | display_id_no | VARCHAR(255) | 是 | 展示用证件号码 |
| 13 | legal_person | VARCHAR(255) | 是 | 法定代表人或负责人 |
| 14 | exec_court | VARCHAR(255) | 是 | 执行法院 |
| 15 | province_id | VARCHAR(255) | 是 | 省份id；省份id。 |
| 16 | province | VARCHAR(255) | 是 | 省份 |
| 17 | dishonest_type | VARCHAR(255) | 是 | 失信人类型 |
| 18 | exec_basis_no | VARCHAR(255) | 是 | 执行依据文号 |
| 19 | exec_basis_org | VARCHAR(255) | 是 | 做出执行依据单位 |
| 20 | legal_obligation | TEXT | 是 | 生效法律文书确定的义务 |
| 21 | fulfillment_status | TEXT | 是 | 被执行人的履行情况 |
| 22 | dishonest_behavior | TEXT | 是 | 失信被执行人行为具体情形 |
| 23 | publish_date | DATE | 是 | 发布时间 |
| 24 | filing_date | DATE | 是 | 立案时间 |
| 25 | exec_part | VARCHAR(255) | 是 | 执行部分 |
| 26 | unexec_part | VARCHAR(255) | 是 | 未执行部分 |
| 27 | is_history | VARCHAR(255) | 是 | 是否历史数据 |
| 28 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 29 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 30 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 31 | created_time | DATETIME | 否 | 创建时间 |
| 32 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_zhixing` — 被执行人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | exec_person_id | VARCHAR(255) | 否 | 唯一索引id；被执行人记录唯一标识id。 |
| 2 | exec_person_type | VARCHAR(255) | 是 | 被执行人类型 |
| 3 | exec_person_name | VARCHAR(255) | 是 | 被执行人名称 |
| 4 | gender | VARCHAR(255) | 是 | 性别 |
| 5 | id_no | VARCHAR(255) | 是 | 证件号码 |
| 6 | exec_court | VARCHAR(255) | 是 | 执行法院 |
| 7 | case_no | VARCHAR(255) | 是 | 案号 |
| 8 | exec_basis_no | VARCHAR(255) | 是 | 执行依据文号 |
| 9 | exec_status | VARCHAR(255) | 是 | 执行状态 |
| 10 | exec_target | VARCHAR(255) | 是 | 执行标的 |
| 11 | web_id | VARCHAR(255) | 是 | 执行信息公开网id |
| 12 | filing_date | DATE | 是 | 立案时间 |
| 13 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 14 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 15 | org_id | VARCHAR(255) | 是 | 机构id |
| 16 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 17 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 18 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 19 | created_time | DATETIME | 否 | 创建时间 |
| 20 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_xianxiao` — 限制高消费

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | xhfgk_id | VARCHAR(255) | 是 | 限制高消费官网id；限制高消费官网/平台原始id。 |
| 2 | rhc_person_name | VARCHAR(255) | 否 | 限制高消费人员名称 |
| 3 | filing_date | DATE | 是 | 立案时间 |
| 4 | case_no | VARCHAR(255) | 否 | 案号 |
| 5 | gender | VARCHAR(255) | 是 | 性别 |
| 6 | company_info | TEXT | 是 | 企业信息 |
| 7 | org_id | VARCHAR(255) | 是 | 机构id |
| 8 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 9 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 10 | company_cert_no | VARCHAR(255) | 是 | 企业证件号 |
| 11 | xhfgk_doc_url | TEXT | 是 | 限制高消费令文件url |
| 12 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 13 | is_history | VARCHAR(255) | 是 | 是否是历史限制高消费 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_lawsuit` — 裁判文书

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 26

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | judgment_doc_id | VARCHAR(255) | 否 | 裁判文书网文书id；裁判文书网文书唯一标识id。 |
| 2 | defendant | VARCHAR(255) | 是 | 被告 |
| 3 | case_no | VARCHAR(255) | 是 | 案号 |
| 4 | case_type_code | VARCHAR(255) | 是 | 案件类型编码 |
| 5 | case_type | VARCHAR(255) | 是 | 案件类型 |
| 6 | doc_type_code | VARCHAR(255) | 是 | 文书类型编码 |
| 7 | doc_type | VARCHAR(255) | 是 | 文书类型 |
| 8 | province | VARCHAR(255) | 是 | 省份 |
| 9 | city | VARCHAR(255) | 是 | 地市 |
| 10 | district | VARCHAR(255) | 是 | 区县 |
| 11 | main_doc_id | VARCHAR(255) | 是 | 主表docid |
| 12 | court_name | VARCHAR(255) | 是 | 法院名称 |
| 13 | trial_procedure | VARCHAR(255) | 是 | 审理程序名称 |
| 14 | judgment_year | DOUBLE | 是 | 裁判年份 |
| 15 | judgment_date | DATE | 是 | 裁判日期 |
| 16 | case_cause | VARCHAR(255) | 是 | 案由 |
| 17 | doc_title | TEXT | 是 | 文书标题 |
| 18 | doc_full_text | TEXT | 是 | 文书全文 |
| 19 | publish_date | DATE | 是 | 公布日期 |
| 20 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 21 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 22 | original_url | TEXT | 是 | 原始连接URL |
| 23 | plaintiff | VARCHAR(255) | 是 | 原告 |
| 24 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 25 | created_time | DATETIME | 否 | 创建时间 |
| 26 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_filed_case` — 法院立案

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | case_unique_id | VARCHAR(255) | 否 | 案件唯一id；案件唯一标识id。 |
| 2 | case_no | VARCHAR(255) | 是 | 案号 |
| 3 | norm_case_no | VARCHAR(255) | 是 | 归一化案号 |
| 4 | case_cause | VARCHAR(255) | 是 | 案由 |
| 5 | trial_procedure | VARCHAR(255) | 是 | 审理程序 |
| 6 | case_status | VARCHAR(255) | 是 | 案件状态 |
| 7 | norm_case_status | VARCHAR(255) | 是 | 归一化后案件状态 |
| 8 | filing_date | DATE | 是 | 立案日期 |
| 9 | closing_date | DATE | 是 | 结案日期 |
| 10 | hearing_date | DATE | 是 | 开庭日期 |
| 11 | court_name | VARCHAR(255) | 是 | 法院 |
| 12 | undertaking_dept | VARCHAR(255) | 是 | 承办部门 |
| 13 | judge | VARCHAR(255) | 是 | 法官 |
| 14 | assistant_judge | VARCHAR(255) | 是 | 助理法官 |
| 15 | party_info | TEXT | 是 | 当事人信息 |
| 16 | court_province | VARCHAR(255) | 是 | 法院所在省 |
| 17 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 18 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 19 | created_time | DATETIME | 否 | 创建时间 |
| 20 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_lawsuit_list` — 裁判文书当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 15

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | main_doc_id | VARCHAR(255) | 否 | 主表docid；主表docid，关联裁判文书表。 |
| 2 | party_identity | VARCHAR(255) | 是 | 当事人身份 |
| 3 | party_role_type | VARCHAR(255) | 是 | 当事人角色类型 |
| 4 | party_type | VARCHAR(255) | 是 | 当事人类型 |
| 5 | related_person_name | VARCHAR(255) | 是 | 相关人名称 |
| 6 | doc_publish_date | DATE | 是 | 文书公布日期 |
| 7 | case_cause | VARCHAR(255) | 是 | 案由 |
| 8 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 9 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 10 | org_id | VARCHAR(255) | 是 | 机构id |
| 11 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 12 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 13 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 14 | created_time | DATETIME | 否 | 创建时间 |
| 15 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_filed_case_litigant` — 法院立案当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 12

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | case_unique_id | VARCHAR(255) | 否 | 案件唯一id；案件唯一标识id，关联法院立案表。 |
| 2 | filing_date | DATE | 是 | 立案日期 |
| 3 | party_name | VARCHAR(255) | 是 | 当事人名称 |
| 4 | party_role | VARCHAR(255) | 是 | 当事人角色 |
| 5 | classified_org_type | VARCHAR(255) | 是 | 归类后企业类型 |
| 6 | org_id | VARCHAR(255) | 是 | 机构id |
| 7 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 8 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 9 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 10 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 11 | created_time | DATETIME | 否 | 创建时间 |
| 12 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_notice` — 开庭公告

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 23

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_id | VARCHAR(255) | 否 | 公告id；开庭公告唯一标识id。 |
| 2 | court_name | VARCHAR(255) | 是 | 法院 |
| 3 | courtroom | VARCHAR(255) | 是 | 法庭 |
| 4 | undertaking_dept | VARCHAR(255) | 是 | 承办部门 |
| 5 | hearing_date | DATE | 是 | 开庭日期 |
| 6 | scheduling_date | DATE | 是 | 排期日期 |
| 7 | case_no | VARCHAR(255) | 是 | 案号 |
| 8 | case_cause | VARCHAR(255) | 是 | 案由 |
| 9 | case_type | VARCHAR(255) | 是 | 案件类型 |
| 10 | jurisdiction_area | VARCHAR(255) | 是 | 案件管辖区域 |
| 11 | plaintiff_appellant | VARCHAR(255) | 是 | 原告上诉人 |
| 12 | defendant_appellee | VARCHAR(255) | 是 | 被告被上诉人 |
| 13 | party | VARCHAR(255) | 是 | 当事人 |
| 14 | presiding_judge | VARCHAR(255) | 是 | 审判长主审人 |
| 15 | title | TEXT | 是 | 标题 |
| 16 | notice_content | TEXT | 是 | 公告内容 |
| 17 | province | VARCHAR(255) | 是 | 省份 |
| 18 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 19 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 20 | original_url | TEXT | 是 | 原始连接URL |
| 21 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 22 | created_time | DATETIME | 否 | 创建时间 |
| 23 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_notice_list` — 开庭公告当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_id | VARCHAR(255) | 否 | 公告id；开庭公告唯一标识id，关联开庭公告表。 |
| 2 | party_role | VARCHAR(255) | 是 | 当事人角色 |
| 3 | party_role_type | VARCHAR(255) | 是 | 当事人角色类型 |
| 4 | party_type | VARCHAR(255) | 是 | 当事人类型 |
| 5 | org_id | VARCHAR(255) | 是 | 机构id |
| 6 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 7 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 8 | related_person_name | VARCHAR(255) | 是 | 相关人名称 |
| 9 | hearing_date | DATE | 是 | 开庭日期 |
| 10 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 11 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 12 | case_cause | VARCHAR(255) | 是 | 案由 |
| 13 | reserve_field | VARCHAR(255) | 是 | 预留字段 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_announcement` — 法院公告

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 29

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_id | VARCHAR(255) | 否 | 公告id；法院公告唯一标识id。 |
| 2 | notice_no | VARCHAR(255) | 是 | 公告号 |
| 3 | notice_name | VARCHAR(255) | 是 | 公告名称 |
| 4 | notice_type | VARCHAR(255) | 是 | 公告类型 |
| 5 | notice_type_name | VARCHAR(255) | 是 | 公告类型名称 |
| 6 | notice_date | DATE | 是 | 公告日期 |
| 7 | case_no | VARCHAR(255) | 是 | 案号 |
| 8 | title | TEXT | 是 | 标题 |
| 9 | notice_content | TEXT | 是 | 公告内容 |
| 10 | court_name | VARCHAR(255) | 是 | 法院名称 |
| 11 | handle_level | VARCHAR(255) | 是 | 处理等级 |
| 12 | handle_level_name | VARCHAR(255) | 是 | 处理等级名称 |
| 13 | judge | VARCHAR(255) | 是 | 法官 |
| 14 | judge_phone | VARCHAR(255) | 是 | 法官电话 |
| 15 | mobile_phone | VARCHAR(255) | 是 | 手机号 |
| 16 | plaintiff | VARCHAR(255) | 是 | 原告 |
| 17 | party | VARCHAR(255) | 是 | 当事人 |
| 18 | province | VARCHAR(255) | 是 | 省份 |
| 19 | case_cause | VARCHAR(255) | 是 | 案由 |
| 20 | notice_year | DOUBLE | 是 | 公告年份 |
| 21 | publish_date | DATE | 是 | 公告刊登日期 |
| 22 | publish_page_no | VARCHAR(255) | 是 | 公告刊登版面页码 |
| 23 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 24 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 25 | original_url | TEXT | 是 | 原始连接URL |
| 26 | content_md5 | VARCHAR(255) | 是 | 公告内容的md5值 |
| 27 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 28 | created_time | DATETIME | 否 | 创建时间 |
| 29 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_court_announcement_list` — 法院公告当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 14

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_id | VARCHAR(255) | 否 | 公告id；法院公告唯一标识id，关联法院公告表。 |
| 2 | party_identity | VARCHAR(255) | 是 | 当事人身份 |
| 3 | party_type | VARCHAR(255) | 是 | 当事人类型 |
| 4 | party_role_type | VARCHAR(255) | 是 | 当事人角色类型 |
| 5 | related_person_name | VARCHAR(255) | 是 | 相关人名称 |
| 6 | publish_date | DATE | 是 | 公告刊登日期 |
| 7 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 8 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 9 | org_id | VARCHAR(255) | 是 | 机构id |
| 10 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 11 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 12 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 13 | created_time | DATETIME | 否 | 创建时间 |
| 14 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_company_justice` — 股权冻结

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | judicial_assist_id | VARCHAR(255) | 否 | 司法协助记录id；司法协助记录唯一标识id。 |
| 3 | executed_person | VARCHAR(255) | 是 | 被执行人 |
| 4 | equity_amount | VARCHAR(255) | 是 | 股权数额 |
| 5 | exec_court | VARCHAR(255) | 是 | 执行法院 |
| 6 | exec_notice_no | VARCHAR(255) | 是 | 执行通知书文号 |
| 7 | type_status | VARCHAR(255) | 是 | 类型｜状态 |
| 8 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 9 | status | VARCHAR(255) | 是 | 状态 |
| 10 | executed_person_type | VARCHAR(255) | 是 | 被执行人类型 |
| 11 | executed_company_id | VARCHAR(255) | 是 | 被执行人的company_id |
| 12 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 13 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_company_pledge` — 股权出质

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 31

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | pledge_id | VARCHAR(255) | 否 | 股权出质记录id；股权出质记录唯一标识id。 |
| 5 | reg_no | VARCHAR(255) | 是 | 登记编号 |
| 6 | pledgor | VARCHAR(255) | 是 | 出质人 |
| 7 | pledgor_id_no | VARCHAR(255) | 是 | 出质人证件号码 |
| 8 | pledgee | VARCHAR(255) | 是 | 质权人 |
| 9 | pledgee_id_no | VARCHAR(255) | 是 | 质权人证件号码 |
| 10 | equity_amount | VARCHAR(255) | 是 | 出质股权数额 |
| 11 | pledge_reg_date | DATE | 是 | 股权出质设立登记日期 |
| 12 | status | VARCHAR(255) | 是 | 状态 |
| 13 | public_date | DATE | 是 | 公示日期 |
| 14 | cancel_date | DATE | 是 | 注销日期 |
| 15 | cancel_reason | TEXT | 是 | 注销原因 |
| 16 | invalid_date | DATE | 是 | 失效时间 |
| 17 | invalid_reason | TEXT | 是 | 失效原因 |
| 18 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 19 | status_code | VARCHAR(255) | 是 | 状态代码 |
| 20 | province_abbr | VARCHAR(255) | 是 | 省份简称 |
| 21 | pledgor_company_id | VARCHAR(255) | 是 | 机构出质人的company_id |
| 22 | pledgor_company_name | VARCHAR(255) | 是 | 机构出质人名称 |
| 23 | pledgor_credit_code | VARCHAR(255) | 是 | 机构出质人统一社会信用代码 |
| 24 | pledgor_type | VARCHAR(255) | 是 | 出质人类型 |
| 25 | pledgee_company_id | VARCHAR(255) | 是 | 机构质权人的company_id |
| 26 | pledgee_company_name | VARCHAR(255) | 是 | 机构质权人名称 |
| 27 | pledgee_credit_code | VARCHAR(255) | 是 | 机构质权人统一社会信用代码 |
| 28 | pledgee_type | VARCHAR(255) | 是 | 质权人类型 |
| 29 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 30 | created_time | DATETIME | 否 | 创建时间 |
| 31 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_risk_zhongben` — 终本案件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 21

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | official_id | VARCHAR(255) | 是 | 官网id |
| 2 | executed_person_name | VARCHAR(255) | 是 | 被执行人姓名名称 |
| 3 | gender | VARCHAR(255) | 是 | 性别 |
| 4 | case_no | VARCHAR(255) | 否 | 案号 |
| 5 | executed_person_type | VARCHAR(255) | 是 | 被执行人类型 |
| 6 | id_no | VARCHAR(255) | 是 | 证件号码 |
| 7 | exec_court | VARCHAR(255) | 是 | 执行法院 |
| 8 | filing_date | DATE | 是 | 立案日期 |
| 9 | termination_date | DATE | 是 | 终本日期 |
| 10 | address | TEXT | 是 | 地址 |
| 11 | exec_target_amount | DOUBLE | 是 | 执行标的金额 |
| 12 | unfulfilled_amount | DOUBLE | 是 | 未履行标的金额 |
| 13 | org_id | VARCHAR(255) | 是 | 机构id |
| 14 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 15 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 16 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 17 | data_use_flag | VARCHAR(255) | 是 | 数据使用标记 |
| 18 | is_history | VARCHAR(255) | 是 | 是否是历史数据 |
| 19 | is_hidden | VARCHAR(255) | 是 | 是否不展示 |
| 20 | created_time | DATETIME | 否 | 创建时间 |
| 21 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_company_chattel` — 动产抵押

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 是 | 机构id |
| 2 | name_cn | VARCHAR(255) | 否 | 机构名称 |
| 3 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 4 | reg_no | VARCHAR(255) | 是 | 登记编号 |
| 5 | reg_date | DATE | 是 | 登记日期 |
| 6 | reg_org | VARCHAR(255) | 是 | 登记机关 |
| 7 | guarantee_type | VARCHAR(255) | 是 | 被担保债权种类 |
| 8 | guarantee_amount | DOUBLE | 是 | 被担保债权数额 |
| 9 | guarantee_scope | TEXT | 是 | 担保范围 |
| 10 | public_date | DATE | 是 | 公示日期 |
| 11 | debt_term | VARCHAR(255) | 是 | 债务人履行债务的期限 |
| 12 | debt_remark | TEXT | 是 | 主债权信息备注 |
| 13 | status | VARCHAR(255) | 是 | 状态 |
| 14 | cancel_date | DATE | 是 | 注销日期 |
| 15 | cancel_reason | TEXT | 是 | 注销原因 |
| 16 | status_code | VARCHAR(255) | 是 | 状态代码 |
| 17 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 18 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 19 | created_time | DATETIME | 否 | 创建时间 |
| 20 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_tb_judicial_sale` — 司法拍卖

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 13

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_name | TEXT | 是 | 公告名 |
| 2 | asset_disposal_unit | VARCHAR(255) | 是 | 资产处置单位 |
| 3 | notice_time | DATETIME | 是 | 公告时间 |
| 4 | notice_id | VARCHAR(255) | 否 | 公告id；司法拍卖公告唯一标识id。 |
| 5 | source_website | VARCHAR(255) | 是 | 来源网站 |
| 6 | notice_content_path | TEXT | 是 | 公告内容存储路径 |
| 7 | auction_start_date | DATE | 是 | 拍卖开始日期 |
| 8 | auction_end_date | DATE | 是 | 拍卖截止日期 |
| 9 | original_link | TEXT | 是 | 原始链接 |
| 10 | use_flag | VARCHAR(255) | 是 | 使用标志 |
| 11 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 12 | created_time | DATETIME | 否 | 创建时间 |
| 13 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_tb_judicial_sale_info_company` — 司法拍卖当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 9

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | notice_id | VARCHAR(255) | 否 | 公告id；司法拍卖公告唯一标识id，关联司法拍卖表。 |
| 2 | related_company | VARCHAR(255) | 是 | 相关公司 |
| 3 | org_id | VARCHAR(255) | 是 | 机构id |
| 4 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 5 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 6 | use_flag | VARCHAR(255) | 是 | 使用标记 |
| 7 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 8 | created_time | DATETIME | 否 | 创建时间 |
| 9 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_bankruptcy_public_cases` — 破产案件

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 15

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | case_no | VARCHAR(255) | 否 | 案号 |
| 2 | case_type | VARCHAR(255) | 是 | 案件类型 |
| 3 | handling_court | VARCHAR(255) | 是 | 经办法院 |
| 4 | applicant_info | TEXT | 是 | 申请人信息 |
| 5 | respondent_info | TEXT | 是 | 被申请人信息 |
| 6 | admin_org | VARCHAR(255) | 是 | 管理人机构 |
| 7 | admin_org_id | VARCHAR(255) | 是 | 管理人机构id |
| 8 | admin_principal | VARCHAR(255) | 是 | 管理人主要负责人 |
| 9 | public_date | DATE | 是 | 公开时间 |
| 10 | link | TEXT | 是 | 链接 |
| 11 | is_deleted | VARCHAR(255) | 是 | 是否删除 |
| 12 | history_status | VARCHAR(255) | 是 | 历史状态 |
| 13 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 14 | created_time | DATETIME | 否 | 创建时间 |
| 15 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_bankruptcy_public_cases_list` — 破产案件当事人

来源 Sheet: 国内机构要素库 ｜ 主键: - ｜ 字段数: 13

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | bankruptcy_party_id | VARCHAR(255) | 否 | 唯一索引id；破产案件当事人记录唯一标识id。 |
| 2 | case_no | VARCHAR(255) | 是 | 案号 |
| 3 | related_person_name | VARCHAR(255) | 是 | 相关人名称 |
| 4 | party_role_type | VARCHAR(255) | 是 | 当事人角色类型 |
| 5 | party_type | VARCHAR(255) | 是 | 当事人类型 |
| 6 | org_id | VARCHAR(255) | 是 | 机构id |
| 7 | name_cn | VARCHAR(255) | 是 | 机构名称 |
| 8 | external_id | VARCHAR(255) | 是 | 统一社会信用代码 |
| 9 | public_date | DATE | 是 | 公开时间 |
| 10 | is_deleted | VARCHAR(255) | 是 | 是否删除 |
| 11 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 12 | created_time | DATETIME | 否 | 创建时间 |
| 13 | updated_time | DATETIME | 否 | 更新时间 |

### 4.2 企业相关 — 国外机构（8 张表）

#### `dwd_forg_base_info` — 海外机构基本信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | name_en | VARCHAR(255) | 否 | 机构名称 |
| 3 | name_alias | VARCHAR(255) | 是 | 机构本地名称 |
| 4 | country_code | VARCHAR(255) | 是 | 国家代码 |
| 5 | country | VARCHAR(255) | 是 | 国家 |
| 6 | external_id | VARCHAR(255) | 是 | 当地官方唯一注册码 |
| 7 | city | VARCHAR(255) | 是 | 所在城市 |
| 8 | address | TEXT | 是 | 公司地址 |
| 9 | postal_code | VARCHAR(255) | 是 | 邮政编码（无数据） |
| 10 | phone | VARCHAR(255) | 是 | 联系电话 |
| 11 | email | VARCHAR(255) | 是 | 电子邮箱 |
| 12 | company_type | VARCHAR(255) | 是 | 企业类型 |
| 13 | registration_org | VARCHAR(255) | 是 | 注册机构（无数据） |
| 14 | incorporation_year | DOUBLE | 是 | 成立年份 |
| 15 | incorporation_date | DATE | 是 | 成立日期/注册日期/核准日期 |
| 16 | listing_status | VARCHAR(255) | 是 | 上市状态 |
| 17 | registered_capital_value | DOUBLE | 是 | 注册资本 |
| 18 | registered_capital_currency_code | VARCHAR(255) | 是 | 注册资本货币代码 |
| 19 | industry_class | VARCHAR(255) | 是 | 公司行业分类 |
| 20 | industry_type | VARCHAR(255) | 是 | 行业分类标准（新增字段） |

#### `dwd_forg_shareholder_info` — 海外机构股东股权关联信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 5

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | owners_name | VARCHAR(255) | 是 | 股东名称 |
| 3 | ownership_percentage | DOUBLE | 是 | 股权占比(%) |
| 4 | owners_country_code | VARCHAR(255) | 是 | 股东所在国家代码 |
| 5 | owners_country | VARCHAR(255) | 是 | 股东所在国家 |

#### `dwd_forg_subsidiary_info` — 海外机构子公司股权关联信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 6

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | affiliate | VARCHAR(255) | 是 | 子公司id |
| 3 | affiliates_name | VARCHAR(255) | 是 | 子公司名称 |
| 4 | affiliates_country_code | VARCHAR(255) | 是 | 子公司国家代码 |
| 5 | affiliates_country | VARCHAR(255) | 是 | 子公司国家 |
| 6 | affiliates_company_id | VARCHAR(255) | 是 | 子公司唯一注册码 |

#### `dwd_forg_executive_info` — 海外机构高管信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 6

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | executives_name | VARCHAR(255) | 是 | 高管姓名 |
| 3 | executives_position | VARCHAR(255) | 是 | 职位名称 |
| 4 | dm_birthdate | DATE | 是 | 高管出生日期(新增字段) |
| 5 | dm_nationalities | VARCHAR(255) | 是 | 高管国籍(新增字段) |
| 6 | dm_biography | VARCHAR(255) | 是 | 高管履历(新增字段) |

#### `dwd_forg_product_info` — 海外机构公司经营信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 3

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | description | VARCHAR(255) | 是 | 业务描述 |
| 3 | main_products | VARCHAR(255) | 是 | 主要产品 |

#### `dwd_forg_beneficiary_info` — 海外机构受益人信息（新增表）

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | bo_name | VARCHAR(255) | 是 | 受益人名称 |
| 3 | bo_gender | VARCHAR(255) | 是 | 受益人性别 |
| 4 | bo_birthdate | DATE | 是 | 受益人出生日期 |
| 5 | bo_country_code | VARCHAR(255) | 是 | 受益人所在国家代码 |
| 6 | path | VARCHAR(255) | 是 | 受益人关系路径 |
| 7 | bo_manager | VARCHAR(255) | 是 | 受益人是否同时是管理层 |
| 8 | total_percent | DOUBLE | 是 | 总持股比例 |
| 9 | direct_percent | DOUBLE | 是 | 直接持股比例 |
| 10 | indirect_percent | DOUBLE | 是 | 间接持股比例 |

#### `dwd_forg_act_contro_info` — 海外机构实控人信息（新增表）

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | country_code | VARCHAR(255) | 是 | 企业国家代码 |
| 3 | entity_eid | VARCHAR(255) | 是 | 实控人ID |
| 4 | entity_name | VARCHAR(255) | 是 | 实控人名称 |
| 5 | entity_type | VARCHAR(255) | 是 | 实控人类型 |
| 6 | entity_country_code | VARCHAR(255) | 是 | 实控人国家代码 |
| 7 | direct_pct | VARCHAR(255) | 是 | 直接持股比例 |
| 8 | total_pct | VARCHAR(255) | 是 | 总持股比例 |
| 9 | direct_pct_num | DOUBLE | 是 | 直接持股比例数值 |
| 10 | total_pct_num | DOUBLE | 是 | 总持股比例数值 |
| 11 | path | VARCHAR(255) | 是 | 路径 |

#### `dwd_forg_stock_fin_info` — 海外上市企业财务信息

来源 Sheet: 国外机构要素库 ｜ 主键: - ｜ 字段数: 15

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | org_id | VARCHAR(255) | 否 | 机构id |
| 2 | occur_period | DATE | 是 | 报告期 |
| 3 | total_assets | DOUBLE | 是 | 资产总额 |
| 4 | fixed_assets | DOUBLE | 是 | 固定资产总额 |
| 5 | total_liabilities | DOUBLE | 是 | 负债总额 |
| 6 | operating_revenue | DOUBLE | 是 | 营业收入 |
| 7 | main_business_revenue | DOUBLE | 是 | 主营业务收入 |
| 8 | total_profit | DOUBLE | 是 | 利润总额 |
| 9 | pure_profit | DOUBLE | 是 | 净利润 |
| 10 | total_tax_paid | DOUBLE | 是 | 企业所得税 |
| 11 | oper_cash_flow | DOUBLE | 是 | 经营活动现金流 |
| 12 | owners_equity | DOUBLE | 是 | 所有者权益合计 |
| 13 | employees_number | DOUBLE | 是 | 从业人数 |
| 14 | research_development_amount | DOUBLE | 是 | 研发投入金额 |
| 15 | research_development_employees_number | DOUBLE | 是 | 研发人员数（无数据） |

### 4.3 企业相关 — 产业链（5 张表）

#### `dwd_industry_chain_info` — 产业链图谱

来源 Sheet: 产业链要素库 ｜ 主键: - ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | chain_code | VARCHAR(255) | 否 | 产业链代码；产业链唯一id，用于关联其它表。 |
| 2 | chain_name | VARCHAR(255) | 否 | 产业链名称 |
| 3 | node_id | VARCHAR(255) | 否 | 节点代码；产业链节点唯一id，用于关联其它表。 |
| 4 | node_name | VARCHAR(255) | 否 | 节点名称 |
| 5 | node_type | DOUBLE | 否 | 节点类型；1-大类节点：为构建图谱结构设置的虚拟节点，不直接关联企业，可通过其下属业务节点间接关联企业。 2-业务节点：具备实际业务含义的节点，在数据处理环节直接关联企业。 3 展示节点：与产业链相关性极弱，仅做图谱关系展示，不关联企业。；值域: 1,2，3 |
| 6 | level | DOUBLE | 否 | 节点层级；产业链节点分类层级中，节点所处层级。；值域: 1,2,3,4,5 |
| 7 | node_seq | DOUBLE | 是 | 节点序号；同一父级节点下的子节点排序参考值。；值域: 1至20 |
| 8 | parent_id | VARCHAR(255) | 是 | 父级节点代码；产业链节点唯一id，用于关联其它表。 |
| 9 | parent_name | VARCHAR(255) | 是 | 父级节点名称 |
| 10 | node_imp_level | DOUBLE | 是 | 节点重要性等级；产业链节点在整个产业链体系中重要性。1为重要性最高，5为重要性最低。仅适用于节点类型为2的业务节点。；值域: 1,2,3,4,5 |
| 11 | downstream_link_code | VARCHAR(255) | 是 | 下游节点代码；产业链节点唯一id，用于关联其它表。 |
| 12 | node_stage | DOUBLE | 是 | 节点环节；适用于上中下游型产业链，1-上游，2-中游，3-下游。；值域: 1,2,3 |
| 13 | node_path | TEXT | 是 | 节点路径 |
| 14 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 15 | created_time | DATETIME | 否 | 创建时间 |
| 16 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_industry_chain_dtl` — 产业关联企业信息

来源 Sheet: 产业链要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | chain_code | VARCHAR(255) | 否 | 产业链代码；产业链唯一id，用于关联其它表。 |
| 2 | chain_name | VARCHAR(255) | 否 | 产业链名称 |
| 3 | node_id | VARCHAR(255) | 否 | 节点代码；产业链节点唯一id，用于关联其它表。 |
| 4 | node_name | VARCHAR(255) | 否 | 节点名称 |
| 5 | antitypic | VARCHAR(255) | 否 | 企业id；企业身份唯一id，用于关联其它表。 |
| 6 | credit_code | VARCHAR(255) | 是 | 统一社会信用代码 |
| 7 | chain_score | DOUBLE | 是 | 产业链评分 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_industry_chain_prod_dtl` — 产业链企业关联产品信息

来源 Sheet: 产业链要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | chain_code | VARCHAR(255) | 否 | 产业链代码；产业链唯一id，用于关联其它表。 |
| 2 | chain_name | VARCHAR(255) | 否 | 产业链名称 |
| 3 | antitypic | VARCHAR(255) | 否 | 企业id；企业身份唯一id，用于关联其它表。 |
| 4 | company_name | VARCHAR(500) | 是 | 企业名称 |
| 5 | credit_code | VARCHAR(255) | 是 | 统一社会信用代码 |
| 6 | tech_product | VARCHAR(255) | 否 | 主营产品名称 |
| 7 | tech_product_seq | DOUBLE | 是 | 主营产品排序 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_org_industry_chain_pat_dtl` — 产业链关联专利信息

来源 Sheet: 产业链要素库 ｜ 主键: - ｜ 字段数: 14

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | chain_code | VARCHAR(255) | 否 | 产业链代码；产业链唯一id，用于关联其它表。 |
| 2 | chain_name | VARCHAR(255) | 否 | 产业链名称 |
| 3 | node_id | VARCHAR(255) | 否 | 节点代码；产业链节点唯一id，用于关联其它表。 |
| 4 | node_name | VARCHAR(255) | 否 | 节点名称 |
| 5 | apno | VARCHAR(255) | 否 | 申请号；专利唯一id，用于关联专利对应企业信息。 |
| 6 | apdt | DATE | 是 | 申请日 |
| 7 | pat_name | VARCHAR(500) | 是 | 专利名称 |
| 8 | pn | VARCHAR(255) | 是 | 公布(公告)号 |
| 9 | pbdt | DATE | 是 | 公布(公告)日 |
| 10 | current_assignee | TEXT | 是 | 申请(专利权)人 |
| 11 | inventors | TEXT | 是 | 发明(设计)人 |
| 12 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 13 | created_time | DATETIME | 否 | 创建时间 |
| 14 | updated_time | DATETIME | 否 | 更新时间 |

#### `dwd_industry_chain_news_info` — 产业动态资讯

来源 Sheet: 产业链要素库 ｜ 主键: - ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | chain_code | VARCHAR(255) | 否 | 产业链代码；产业链唯一id，用于关联其它表。 |
| 2 | chain_name | VARCHAR(255) | 否 | 产业链名称 |
| 3 | news_id | VARCHAR(255) | 否 | 资讯id；资讯唯一id |
| 4 | title | VARCHAR(255) | 是 | 标题 |
| 5 | relaese_date | DATE | 是 | 发布时间 |
| 6 | summary | TEXT | 是 | 摘要 |
| 7 | source | VARCHAR(255) | 是 | 来源 |
| 8 | data_source | VARCHAR(255) | 否 | 数据来源 |
| 9 | created_time | DATETIME | 否 | 创建时间 |
| 10 | updated_time | DATETIME | 否 | 更新时间 |

### 4.4 企业相关 — 企业工商通用（量子专题 company_*，20 张表）

#### `dwd_industry_code` — 产业链

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 9

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | id |
| 2 | code | VARCHAR(255) | 是 | 环节编码 |
| 3 | name | VARCHAR(255) | 是 | 环节名称 |
| 4 | parent_code | VARCHAR(255) | 是 | 父级编码 |
| 5 | industry_code | VARCHAR(255) | 是 | 产业编码 |
| 6 | industry_name | VARCHAR(255) | 是 | 产业名称 |
| 7 | level | DOUBLE | 是 | 级别 |
| 8 | definition | VARCHAR(255) | 是 | 定义 |
| 9 | is_key_link | DOUBLE | 是 | 是否为关键环节 |

#### `dwd_company_base` — 基础信息

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 36

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | name | VARCHAR(255) | 是 | 企业名称 |
| 3 | source_id | VARCHAR(255) | 是 | 来源编码 |
| 4 | english_name | VARCHAR(255) | 是 | 企业英文名称 |
| 5 | registration_code | VARCHAR(255) | 是 | 注册号 |
| 6 | organization_code | VARCHAR(255) | 是 | 组织机构号 |
| 7 | credit_code | VARCHAR(255) | 是 | 统一信用代码 |
| 8 | first_type | VARCHAR(255) | 是 | 标准化后的企业类型 |
| 9 | second_type | VARCHAR(255) | 是 | 标准化后的企业类型 |
| 10 | detail_type | VARCHAR(255) | 是 | 标准化后的企业类型 |
| 11 | registered_capital | VARCHAR(255) | 是 | 注册资本 |
| 12 | registered_add | VARCHAR(255) | 是 | 注册地址 |
| 13 | scope | VARCHAR(255) | 是 | 经营范围 |
| 14 | start_date | VARCHAR(255) | 是 | 营业期限开始日期 |
| 15 | end_date | VARCHAR(255) | 是 | 营业期限终止日期 |
| 16 | reg_organization | VARCHAR(255) | 是 | 登记机关 |
| 17 | legal_representative | VARCHAR(255) | 是 | 法人姓名 |
| 18 | legal_rep_type | DOUBLE | 是 | 法人类型 |
| 19 | approval_date | VARCHAR(255) | 是 | 核准日期 |
| 20 | establish_date | VARCHAR(255) | 是 | 成立日期 |
| 21 | cancel_date | VARCHAR(255) | 是 | 注销日期 |
| 22 | status_std | VARCHAR(255) | 是 | 企业状态 |
| 23 | display | DOUBLE | 是 | 企业状态 |
| 24 | reg_capital_std | DOUBLE | 是 | 注册资本金额 |
| 25 | unit | VARCHAR(255) | 是 | 注册资本单位 |
| 26 | currency | VARCHAR(255) | 是 | 注册资本币种 |
| 27 | real_capital | VARCHAR(255) | 是 | 实缴资本 |
| 28 | real_capital_std | DOUBLE | 是 | 实缴资本金额 |
| 29 | cancel_reason | VARCHAR(255) | 是 | 注销原因 |
| 30 | ori_reg_city | VARCHAR(255) | 是 | 注册地所在市 |
| 31 | ori_reg_district | VARCHAR(255) | 是 | 注册的所在区 |
| 32 | ori_reg_province | VARCHAR(255) | 是 | 注册地所在省 |
| 33 | reg_xy | VARCHAR(255) | 是 | 经度 |
| 34 | is_deleted | DOUBLE | 是 | 使用标记 |
| 35 | create_time | DATE | 是 | 创建时间 |
| 36 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_branch` — 分支机构

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 13

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | branch_id | DOUBLE | 是 | 分支机构的主体唯一键 |
| 4 | branch_name | VARCHAR(255) | 是 | 分支机构名称 |
| 5 | branch_reg_code | VARCHAR(255) | 是 | 分支机构注册号 |
| 6 | branch_credit_code | VARCHAR(255) | 是 | 分支机构统一信用代码 |
| 7 | branch_establish_date | VARCHAR(255) | 是 | 分支机构成立日期 |
| 8 | branch_company_status | VARCHAR(255) | 是 | 登记状态 |
| 9 | branch_cancel_date | VARCHAR(255) | 是 | 注销日期 |
| 10 | is_history | DOUBLE | 是 | 使用标记 |
| 11 | is_deleted | DOUBLE | 是 | 使用标记 |
| 12 | create_time | DATE | 是 | 入库时间 |
| 13 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_change` — 工商变更

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 11

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | before | VARCHAR(255) | 是 | 变更前内容 |
| 4 | after | VARCHAR(255) | 是 | 变更后内容 |
| 5 | date | VARCHAR(255) | 是 | 变更日期 |
| 6 | change_type | VARCHAR(255) | 是 | 变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更, address, business, lp) |
| 7 | change_type_std | VARCHAR(255) | 是 | 变更类型(法定代表人变更, 主要人员变更, 经营范围变更, 注册资本变更, 股东信息变更) |
| 8 | change_type_detail | VARCHAR(255) | 是 | 变更类型详情 |
| 9 | is_deleted | DOUBLE | 是 | 使用标记 |
| 10 | create_time | DATE | 是 | 入库时间 |
| 11 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_history_name` — 曾用名

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 8

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | history_name | VARCHAR(255) | 是 | 曾用名 |
| 4 | start_date | VARCHAR(255) | 是 | 名称开始使用日期 |
| 5 | end_date | VARCHAR(255) | 是 | 名称结束使用日期 |
| 6 | is_deleted | DOUBLE | 是 | 使用标记 |
| 7 | create_time | DATE | 是 | 创建时间 |
| 8 | update_time | DATE | 是 | 更新时间 |

#### `dwd_company_license` — 行政许可

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 12

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | name | VARCHAR(255) | 是 | 许可证名称 |
| 4 | license_code | VARCHAR(255) | 是 | 许可文件编号 |
| 5 | scope | VARCHAR(255) | 是 | 许可内容 |
| 6 | start_date | VARCHAR(255) | 是 | 有效期自 |
| 7 | end_date | VARCHAR(255) | 是 | 有效期至 |
| 8 | organization | VARCHAR(255) | 是 | 许可机关 |
| 9 | is_history | DOUBLE | 是 | 状态 |
| 10 | is_deleted | DOUBLE | 是 | 使用标记 |
| 11 | create_time | DATE | 是 | 入库时间 |
| 12 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_nei_code` — 国民行业经济分类

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 14

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | industry | VARCHAR(255) | 是 | 最深一级的行业名称 |
| 4 | industry_l1_code | VARCHAR(255) | 是 | 一级行业编码 |
| 5 | industry_l1_name | VARCHAR(255) | 是 | 一级行业名称 |
| 6 | industry_l2_code | VARCHAR(255) | 是 | 二级行业编码 |
| 7 | industry_l2_name | VARCHAR(255) | 是 | 二级行业名称 |
| 8 | industry_l3_code | VARCHAR(255) | 是 | 三级行业编码 |
| 9 | industry_l3_name | VARCHAR(255) | 是 | 三级行业名称 |
| 10 | industry_l4_code | VARCHAR(255) | 是 | 四级行业编码 |
| 11 | industry_l4_name | VARCHAR(255) | 是 | 四级行业名称 |
| 12 | is_deleted | DOUBLE | 是 | 使用标记 |
| 13 | create_time | DATE | 是 | 入库时间 |
| 14 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_reg_cap_change` — 注册资本变更

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | type | VARCHAR(255) | 是 | 变更类型 |
| 4 | date | VARCHAR(255) | 是 | 变更日期 |
| 5 | before | DOUBLE | 是 | 变更前注册资本 |
| 6 | after | DOUBLE | 是 | 变更后注册资本 |
| 7 | unit | VARCHAR(255) | 是 | 单位 |
| 8 | is_deleted | DOUBLE | 是 | 是否删除 |
| 9 | create_time | DATE | 是 | 创建时间 |
| 10 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_shareholder` — 股东信息

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 21

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | investor_id | DOUBLE | 是 | 股东id |
| 4 | investor_name | VARCHAR(255) | 是 | 股东名称 |
| 5 | investor_type | DOUBLE | 是 | 股东类型 |
| 6 | investor_detail_type | VARCHAR(255) | 是 | 股东类型 |
| 7 | amount | VARCHAR(255) | 是 | 投资金额 |
| 8 | amount_std | DOUBLE | 是 | 投资金额标准化（万元人民币） |
| 9 | share_ratio | DOUBLE | 是 | 持股比例 |
| 10 | subscribed | VARCHAR(255) | 是 | 认缴资金,认缴日期,认缴形式 |
| 11 | contributed | VARCHAR(255) | 是 | 实缴金额,实缴日期,实缴形式 |
| 12 | stock_realcapital | VARCHAR(255) | 是 | 实缴出资额 |
| 13 | country | VARCHAR(255) | 是 | 股东国别 |
| 14 | include_date | VARCHAR(255) | 是 | 股东进入日期 |
| 15 | remove_date | VARCHAR(255) | 是 | 股东退出日期 |
| 16 | is_history | DOUBLE | 是 | 是否历史股东 |
| 17 | name_source | DOUBLE | 是 | 股东来源 |
| 18 | stock_type | VARCHAR(255) | 是 | 股东类型 |
| 19 | is_deleted | DOUBLE | 是 | 使用标记 |
| 20 | create_time | DATE | 是 | 创建时间 |
| 21 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_staff` — 任职人员

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 12

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 唯一键 |
| 3 | staff_id | DOUBLE | 是 | 主要人员是机构时，该机构的company_id |
| 4 | staff_name | VARCHAR(255) | 是 | 清洗后主要人员名称 |
| 5 | staff_type | VARCHAR(255) | 是 | 职位 |
| 6 | person_type | DOUBLE | 是 | employee_name类型 |
| 7 | start_date | VARCHAR(255) | 是 | 主要人员任职开始日期 |
| 8 | end_date | VARCHAR(255) | 是 | 主要人员任职截止日期 |
| 9 | is_history | DOUBLE | 是 | 是否历史主要人员 |
| 10 | is_deleted | DOUBLE | 是 | 使用标记 |
| 11 | create_time | DATE | 是 | 入库时间 |
| 12 | update_time | DATE | 是 | 更新时间 |

#### `dwd_company_transition_clean` — 注册地址变更

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 10

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 |  |
| 3 | name | VARCHAR(255) | 是 | 企业名称 |
| 4 | before | VARCHAR(255) | 是 | 清洗后变更前地址 |
| 5 | after | VARCHAR(255) | 是 | 清洗后变更后地址 |
| 6 | date | VARCHAR(255) | 是 | 变更日期 |
| 7 | type | VARCHAR(255) | 是 | 变更类型 |
| 8 | is_deleted | DOUBLE | 是 | 是否删除 |
| 9 | create_time | DATE | 是 | 创建时间 |
| 10 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_basic_tags` — 基础属性标签

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 7

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | business_type | VARCHAR(255) | 是 | 业务类型 |
| 3 | capital_type | VARCHAR(255) | 是 | 企业性质 |
| 4 | scale_tag | VARCHAR(255) | 是 | 企业规模标签 |
| 5 | is_deleted | DOUBLE | 是 | 使用标记 |
| 6 | create_time | DATE | 是 | 创建时间 |
| 7 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_brief_tags` — 企业简介

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 5

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | brief | VARCHAR(255) | 是 | 公司简介摘要 |
| 3 | is_deleted | DOUBLE | 是 | 使用标记 |
| 4 | create_time | DATE | 是 | 创建时间 |
| 5 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_location_tags` — 所在行政区

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 8

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | reg_province | VARCHAR(255) | 是 | 省 |
| 3 | reg_city | VARCHAR(255) | 是 | 市 |
| 4 | reg_district | VARCHAR(255) | 是 | 区 |
| 5 | reg_xy | VARCHAR(255) | 是 | 坐标 |
| 6 | is_deleted | DOUBLE | 是 | 是否删除 |
| 7 | create_time | DATE | 是 | 入库时间 |
| 8 | update_time | DATE | 是 | 数据更新时间 |

#### `dwd_company_contact_tags` — 企业联系方式

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 5

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | contact | VARCHAR(255) | 是 | 联系人信息（联系人姓名，联系方式，类型，信息来源，更新日期，原始链接） |
| 3 | is_deleted | DOUBLE | 是 | 是否删除 |
| 4 | create_time | DATE | 是 | 创建时间 |
| 5 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_recruit` — 招聘

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 24

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | source_id | VARCHAR(255) | 是 | 招聘事件ID |
| 3 | company_name | VARCHAR(255) | 是 | 公司名称 |
| 4 | city | VARCHAR(255) | 是 | 所在城市 |
| 5 | district | VARCHAR(255) | 是 | 所在区 |
| 6 | title | VARCHAR(255) | 是 | 招聘职称 |
| 7 | salary | VARCHAR(255) | 是 | 工资 |
| 8 | first_class | VARCHAR(255) | 是 | 一级分类 |
| 9 | second_class | VARCHAR(255) | 是 | 二级分类 |
| 10 | third_class | VARCHAR(255) | 是 | 三级分类 |
| 11 | address | VARCHAR(255) | 是 | 工作地址 |
| 12 | start_date | DATE | 是 | 招聘开始日期 |
| 13 | end_date | VARCHAR(255) | 是 | 招聘截止日期 |
| 14 | education | VARCHAR(255) | 是 | 教育 |
| 15 | recruit_number | VARCHAR(255) | 是 | 招聘人数 |
| 16 | description | VARCHAR(255) | 是 | 职位描述 |
| 17 | experience | VARCHAR(255) | 是 | 经验 |
| 18 | type | VARCHAR(255) | 是 | 招聘类别 |
| 19 | company_address | VARCHAR(255) | 是 | 公司地址 |
| 20 | url_Path | VARCHAR(255) | 是 | 外网链接 |
| 21 | source | VARCHAR(255) | 是 | 来源 |
| 22 | is_deleted | DOUBLE | 是 | 使用标记 |
| 23 | create_time | DATE | 是 | 创建时间 |
| 24 | update_time | DATE | 是 | 更改时间 |

#### `dwd_company_industry_tags` — 产业标签

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 5

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | industry_tag | VARCHAR(255) | 是 | 产业标签（产业编码，产业名称，置信度，环节[环节编码，环节名称，级别，置信度]） |
| 3 | is_deleted | DOUBLE | 是 | 是否删除 |
| 4 | create_time | DATE | 是 | 创建时间 |
| 5 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_diy_tags` — 特色资质标签

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 5

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | diy_tag | VARCHAR(255) | 是 | 特色资质标签 |
| 3 | is_deleted | DOUBLE | 是 | 使用标记 |
| 4 | create_time | DATE | 是 | 创建时间 |
| 5 | update_time | DATE | 是 | 最后更新时间 |

#### `dwd_company_honor_tags` — 企业荣誉标签

来源 Sheet: 量子专题要素库 ｜ 主键: id ｜ 字段数: 15

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | DOUBLE | 否 | 企业id |
| 2 | association_tag | VARCHAR(255) | 是 | 协会标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 3 | award_tag | VARCHAR(255) | 是 | 荣誉奖项标签（奖项编码，奖项类型，奖项等级，级别，获奖日期，颁发单位，奖项全称，获奖年份） |
| 4 | certification | VARCHAR(255) | 是 | 资质认证（证书名称，证书编号，资质编码，获证年份，级别，状态，有效期起，有效期止，发证日期，发证机构） |
| 5 | city_tag | VARCHAR(255) | 是 | 市级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 6 | district_tag | VARCHAR(255) | 是 | 区县级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 7 | national_tag | VARCHAR(255) | 是 | 国家级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 8 | nonpublic_tags | VARCHAR(255) | 是 |  |
| 9 | park_tag | VARCHAR(255) | 是 | 园区级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 10 | permission | VARCHAR(255) | 是 | 备案许可（许可事项名称，许可证号，许可类型编码，许可年份，管理层级，状态，有效期起，有效期止，发证日期，审批机关，许可生产范围） |
| 11 | province_tag | VARCHAR(255) | 是 | 省级标签（标签名称，标签编码，入选年份，级别，入选日期，发布机构） |
| 12 | rank_tag | VARCHAR(255) | 是 | 榜单标签（标签名称，标签编码，年份，级别，具体名次，发布日期，发布机构） |
| 13 | is_deleted | DOUBLE | 是 | 是否删除 |
| 14 | create_time | DATE | 是 | 创建时间 |
| 15 | update_time | DATE | 是 | 最后更新时间 |

### 4.5 政策相关（2 张表）

#### `dwd_zck_policy` — 国内政策信息

来源 Sheet: 国内政策要素库 ｜ 主键: id ｜ 字段数: 20

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | VARCHAR(255) | 否 | 唯一id |
| 2 | title | VARCHAR(1000) | 否 | 政策标题 |
| 3 | issued_number | VARCHAR(255) | 否 | 政策文号 |
| 4 | publish_department_name | VARCHAR(255) | 否 | 发布机构 |
| 5 | create_time | DATE | 否 | 成文日期；值域: 格式：2023-11-09 |
| 6 | publish_time | DATE | 否 | 发文日期（发布日期）；值域: 格式：2023-11-09 |
| 7 | status | VARCHAR(10) | 否 | 时效状态；值域: 已发布、已撤销 |
| 8 | publish_year | VARCHAR(4) | 否 | 发布年 |
| 9 | policy_level | VARCHAR(32) | 否 | 政策层级；值域: 国家级、省级、市级、区县级 |
| 10 | region | VARCHAR(255) | 否 | 政策地区 |
| 11 | abstract | TEXT | 否 | 摘要 |
| 12 | keywords | VARCHAR(1000) | 否 | 关键词 |
| 13 | content | TEXT | 否 | 正文内容 |
| 14 | url | VARCHAR(1000) | 否 | 原文链接 |
| 15 | pedigree | TEXT | 否 | 政策谱系/引用政策 |
| 16 | elements | TEXT | 否 | 政策主旨要素 |
| 17 | keypoints | TEXT | 否 | 政策要点 |
| 18 | allfactors | TEXT | 否 | 政策扶持要素 |
| 19 | platform | VARCHAR(255) | 否 | 数据来源 |
| 20 | attachment | TEXT | 否 | 附件 |

#### `dwd_zck_intl_policy` — 国际政策信息

来源 Sheet: 国外政策要素库 ｜ 主键: id ｜ 字段数: 16

| # | 字段名 | 类型 | 可空 | 说明 |
|---|--------|------|------|------|
| 1 | id | VARCHAR(255) | 否 | 唯一id |
| 2 | title | VARCHAR(1000) | 否 | 标题原文 |
| 3 | translate_title | VARCHAR(1000) | 否 | 标题译文 |
| 4 | abstract | VARCHAR(2000) | 否 | 摘要原文 |
| 5 | content | TEXT | 否 | 正文原文 |
| 6 | translate_content | TEXT | 否 | 正文译文 |
| 7 | media_product_name | VARCHAR(255) | 否 | 媒体名称 |
| 8 | media_type | VARCHAR(255) | 否 | 媒体类型 |
| 9 | release_year | VARCHAR(255) | 否 | 年份 |
| 10 | release_date | VARCHAR(255) | 否 | 发布日期 |
| 11 | media_area | VARCHAR(255) | 否 | 所属区域 |
| 12 | url_link | VARCHAR(1000) | 否 | url链接 |
| 13 | language | VARCHAR(255) | 否 | 语种 |
| 14 | class | VARCHAR(255) | 否 | 内容分类 |
| 15 | class_no | VARCHAR(255) | 否 | 分类号 |
| 16 | source | VARCHAR(255) | 否 | 数据来源 |

---

*清单生成时间: 2026-06-02 ｜ 数据源: db/要素库建表语句.sql（186 张表）*
