# 三方源 live dwd 企业维齐套复核（2026-08-03）

> **探测时间**：2026-08-03 约 20:46（UTC+8）  
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）  
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）  
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）  
> **脚本产物**：`_live_dwd_enterprise_probe_2026-08-03.json`  
> **相对 08-02**：**重大变化** — 有数据表 13→**22**；多张此前为空的治理/风险/招投标/港澳台表已灌样例；但此前有数的财务/上市/标签/产业链路径**清零**。

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **结构基本齐，数据仍未齐备**（有数据面扩大，但财务/上市/标签路径回退） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以，但烟测路径需切换**：主表仍 2 万；优先走股东/高管/港澳台/招投标/风险；**勿再依赖** stock/financial/tags |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（P0 有数据仍 9/17；4 表缺失；量级远低于口头 711 万） |
| 相对 08-02 是否有进展？ | **有，且需供应方确认是否为轮换样例灌数**：结构仍 36/40；有数据 +9；但 8 张此前有数表今日为 0 |

**齐备定义（本报告）**

1. 承诺表名在源库存在  
2. COUNT(*) > 0（可查询到业务行）  
3. P0 核心路径（主数据 + 关键卫星）可支撑贴源与 Mapping 试点  

当前：(1) 大部 + (2) 扩大但路径轮换 + (3) 仍弱试点。

---

## 2. 汇总分数（四日对比）

| 维度 | 2026-07-31 | 2026-08-01 | 2026-08-02 | **2026-08-03** |
|------|------------|------------|------------|----------------|
| 库内活跃 dwd 表数 | — | — | 272 | **277**（+5） |
| 承诺表存在 | 36/40 | 36/40 | 36/40 | **36/40**（同） |
| 表缺失 | 4 | 4 | 4 | **4**（同，均为国外机构 P1） |
| 有数据（>0） | 12/40 | 13/40 | 13/40 | **22/40**（+9） |
| P0 表存在 | 17/17 | 17/17 | 17/17 | **17/17** |
| P0 有数据 | 8/17 | 9/17 | 9/17 | **9/17**（数量同，**集合已换**） |
| 主表 base_info | 0 | 20,000 | 20,000 | **20,000**（同） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（22）

| 优先级 | 表 | 行数 | 相对 08-02 |
|--------|-----|------|------------|
| P0 | **dwd_org_base_info** | **20,000** | 持平 |
| P0 | dwd_org_shareholder_info | 19,024 | **新有数**（昨=0） |
| P0 | dwd_org_executive_info | 20,000 | **新有数**（昨=0） |
| P0 | dwd_org_heis_info | 20,000 | **新有数**（昨=0） |
| P0 | dwd_research_institute_base_info | 2,075 | **新有数**（昨=0） |
| P0 | dwd_special_hongkong_company | 20,000 | **新有数**（昨=0） |
| P0 | dwd_special_taiwan_company | 20,000 | **新有数**（昨=0） |
| P0 | dwd_special_aomen_company | 396 | **新有数**（昨=0） |
| P0 | dwd_bid_base_out | 20,000 | **新有数**（昨=0） |
| P1 | dwd_org_changerecord_info | 10,901 | **新有数**（昨=0；旁路 `change_record_info` 仍有 1,676） |
| P1 | dwd_bid_win_candidate_out | 20,000 | **新有数** |
| P1 | dwd_bid_purchase_agency_out | 20,000 | **新有数** |
| P1 | dwd_bid_target_item_out | 20,000 | **新有数** |
| P1 | dwd_org_company_abnormal | 3,515 | **新有数** |
| P1 | dwd_org_company_punish | 19,992 | **新有数** |
| P1 | dwd_org_company_illegal | 887 | **新有数** |
| P1 | dwd_org_risk_tax_punish | 10,959 | **新有数** |
| P1 | dwd_org_opt_judicial_case | 19,877 | **新有数** |
| P1 | dwd_org_risk_shixin | 19,958 | **新有数** |
| P1 | dwd_org_risk_zhixing | 20,000 | **新有数** |
| P1 | dwd_org_bankruptcy_public_cases | 20,000 | **新有数** |
| P1 | dwd_org_bankruptcy_public_cases_list | 20,000 | **新有数** |

### 3.2 表在但空（14）— 含昨日有数、今日清零

#### 今日清零（昨有数 → 今 0）⚠️

| 优先级 | 表 | 08-02 行数 | 08-03 |
|--------|-----|------------|-------|
| P0 | dwd_org_stock_base | 5,845 | **0** |
| P0 | dwd_org_annual_financial_info | 5,352 | **0** |
| P0 | dwd_org_stock_finance_info | 5,352 | **0** |
| P0 | dwd_org_industry_product_tags | 5,000 | **0** |
| P0 | dwd_org_industry_tags | 4,912 | **0** |
| P0 | dwd_org_org_product_info | 1,084 | **0** |
| P0 | dwd_org_important_news_info | 913 | **0** |
| P0 | dwd_industry_chain_info | 527 | **0** |
| P1 | dwd_industry_chain_news_info | 5,000 | **0** |
| P1 | dwd_org_recruit_info | 2,000 | **0** |
| P1 | dwd_forg_executive_info | 4,811 | **0** |
| P1 | dwd_forg_base_info | 1,000 | **0** |

#### 持续为空

- P1：`dwd_forg_shareholder_info`、`dwd_forg_product_info`

### 3.3 表缺失（4）— P1 国外（连续四日同）

- dwd_forg_college_org_info
- dwd_forg_university_org_info
- dwd_forg_research_org_info
- dwd_foreign_org_annual_financial_info

---

## 4. 命名旁路（非承诺名但有数）

| live 表 | 行数 | 说明 |
|---------|------|------|
| **dwd_org_annual_report_base** | **770,000** | 仍为企业域最大体量；口头 711 万口径待澄清 |
| dwd_forg_shareholder | 21,097 | 承诺名 `dwd_forg_shareholder_info`=0 |
| dwd_forg_investment | 12,199 | |
| dwd_forg_industry | 7,569 | |
| dwd_forg_beneficiary_info | 6,276 | |
| dwd_forg_agg_identifier | 3,195 | |
| dwd_org_change_record_info | 1,676 | 承诺名 `dwd_org_changerecord_info` 今日已有 **10,901**（命名双轨并存） |
| dwd_org_innovation_carrier | 1,449 | |
| dwd_forg_ultimate_control | 1,027 | |
| dwd_forg_contact / dwd_forg_profile | 999 | |
| dwd_org_industry_chain_pat_dtl | 888 | |

---

## 5. 库内 dwd 全域分布（approx，277 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| other | 53 | 7,736,028 | 20,153.1 |
| **enterprise_org** | **100** | **611,318** | **534.0** |
| talent_paper_patent_project | 62 | 3,575 | 2.0 |
| finance_market | 8 | 0 | 970.6 |
| industry_topic | 48 | 0 | 1.0 |
| industry_chain | 3 | 0 | 0.1 |
| policy | 3 | 0 | 0.1 |

---

## 6. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | **改路径继续做**：base + 股东/高管/港澳台/招投标/风险；**暂停**依赖 stock/financial/tags 的用例 |
| Wave A P0 关单 | **仍不可** — P0 有数据仍仅 9/17；财务/上市/标签/产业链空；量级仍样例级 |
| Mapping enterprise_base | **可小样试点**（2 万 org）；勿按 711 万排产 |
| 异常升级 | **当日知会**：疑似供应方轮换样例批次，导致既有烟测路径断裂 |

---

## 7. 与供应方口头进度 / 待确认

口头「国内机构 711 万 / 2500 万」：主表仍 **2 万**；`dwd_org_annual_report_base` 仍 **77 万**。

**请供应方当日确认**：

1. 08-03 是否做了样例表轮换（清空财务/上市/标签，灌入股东/高管/风险/招投标）？旧样例是否还会回灌？  
2. 711 万口径是否含 `dwd_org_annual_report_base`？主表是否还会扩至百万级？  
3. `dwd_org_changerecord_info`（今 10,901）与 `dwd_org_change_record_info`（1,676）以哪个为正式映射名？  
4. 国外机构承诺名空表 vs 旁路有数表（如 `dwd_forg_shareholder`）正式目标是哪个？

---

## 8. 一句话给监管人

**今日有明显灌数轮换：有数据表 13→22，股东/高管/港澳台/招投标/风险已就绪样例；但财务/上市/标签/产业链等昨日有数路径全部清零。主表仍 2 万，未齐备，烟测路径需切换并请供应方确认是否为批次轮换。**
