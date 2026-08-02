# 三方源 live dwd 企业维齐套复核（2026-08-02）

> **探测时间**：2026-08-02 约 23:50（UTC+8）
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）
> **相对 08-01**：企业维承诺 40 表行数与结构**完全持平**，无新增灌数；库内活跃 dwd 表总数 256 → **272**（+16），但增量集中在非企业域。

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **结构基本齐，数据仍未齐备**（与 08-01 一致） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以**（主表仍有 2 万样例） |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（多张 P0/P1 仍空；4 表缺失；量级远低于口头 711 万） |
| 相对 08-01 是否有进展？ | **承诺 40 表无进展**；库内 dwd 总表数 +16，但均非 Wave A 清单表 |

**齐备定义（本报告）**

1. 承诺表名在源库存在
2. COUNT(*) > 0（可查询到业务行）
3. P0 核心路径（主数据 + 关键卫星）可支撑贴源与 Mapping 试点

当前仅满足 (1) 大部 + (2) 部分 + (3) 弱试点，与 08-01 同。

---

## 2. 汇总分数（三日对比）

| 维度 | 2026-07-31 | 2026-08-01 | **2026-08-02** |
|------|------------|------------|----------------|
| 库内活跃 dwd 表数 | — | — | **272** |
| 承诺表存在 | 36/40 | 36/40 | **36/40**（同） |
| 表缺失 | 4 | 4 | **4**（同，均为国外机构 P1） |
| 有数据（>0） | 12/40 | 13/40 | **13/40**（同） |
| P0 表存在 | 17/17 | 17/17 | **17/17** |
| P0 有数据 | 8/17 | 9/17 | **9/17**（同） |
| 主表 base_info | 0 | 20,000 | **20,000**（同） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（13）— 与 08-01 完全一致

| 优先级 | 表 | 行数 | 备注 |
|--------|-----|------|------|
| P0 | **dwd_org_base_info** | **20,000** | 主数据样例；与 08-01 持平 |
| P0 | dwd_org_stock_base | 5,845 | 与 base 交集极低（08-01 实测约 2 个 org_id） |
| P0 | dwd_org_annual_financial_info | 5,352 | |
| P0 | dwd_org_stock_finance_info | 5,352 | |
| P0 | dwd_org_industry_product_tags | 5,000 | |
| P0 | dwd_org_industry_tags | 4,912 | |
| P0 | dwd_org_org_product_info | 1,084 | |
| P0 | dwd_org_important_news_info | 913 | |
| P0 | dwd_industry_chain_info | 527 | |
| P1 | dwd_industry_chain_news_info | 5,000 | |
| P1 | dwd_forg_executive_info | 4,811 | |
| P1 | dwd_org_recruit_info | 2,000 | |
| P1 | dwd_forg_base_info | 1,000 | |

### 3.2 表在但空（23）— 结构就绪、数据未齐（与 08-01 同）

#### P0 主/扩展

- dwd_org_shareholder_info
- dwd_org_executive_info
- dwd_org_heis_info
- dwd_research_institute_base_info

#### P0 港澳台

- dwd_special_hongkong_company
- dwd_special_taiwan_company
- dwd_special_aomen_company

#### P0 招投标

- dwd_bid_base_out

#### P1 招投标

- dwd_bid_win_candidate_out
- dwd_bid_purchase_agency_out
- dwd_bid_target_item_out

#### P1 风险

- dwd_org_company_abnormal
- dwd_org_company_punish
- dwd_org_company_illegal
- dwd_org_risk_tax_punish
- dwd_org_risk_shixin
- dwd_org_risk_zhixing
- dwd_org_opt_judicial_case
- dwd_org_bankruptcy_public_cases
- dwd_org_bankruptcy_public_cases_list

#### P1 国内其他

- dwd_org_changerecord_info（承诺名；旁路 `dwd_org_change_record_info` 有 1,676 行，见 §4）

#### P1 国外

- dwd_forg_shareholder_info
- dwd_forg_product_info

### 3.3 表缺失（4）— P1 国外（与 08-01 同）

- dwd_forg_college_org_info
- dwd_forg_university_org_info
- dwd_forg_research_org_info
- dwd_foreign_org_annual_financial_info

---

## 4. 命名旁路（非承诺名但有数）— 本次重点观察

> 这些表不在 Wave A 40 清单，但属于企业/国外机构域且**已有数据**。供应方可能已用**不同表名**灌数，或这些是更细粒度的卫星表。建议与供应方核对是否应纳入 Mapping 或替换承诺名。

| live 表 | 行数 | 域 | 说明 |
|---------|------|----|------|
| **dwd_org_annual_report_base** | **770,000** | enterprise_org | 非 Wave A 40；企业相关**最大体量表**（approx 537,092 / data 494 MB）；可能对应口头「国内机构 711 万」口径的一部分？需供应方澄清 |
| dwd_forg_shareholder | 21,097 | enterprise_org | 国外机构股东（非承诺名 `dwd_forg_shareholder_info`，后者=0） |
| dwd_forg_investment | 12,199 | enterprise_org | 国外企业投资 |
| dwd_forg_industry | 7,569 | enterprise_org | 国外企业行业分类 |
| dwd_forg_beneficiary_info | 6,276 | enterprise_org | 海外机构受益人（新增表） |
| dwd_forg_agg_identifier | 3,195 | enterprise_org | 国外企业代码 |
| dwd_forg_ultimate_control | 1,027 | enterprise_org | 国外企业实际控制人 |
| dwd_org_change_record_info | 1,676 | enterprise_org | 承诺名为 `dwd_org_changerecord_info`（无下划线分段）= 0 |
| dwd_org_innovation_carrier | 1,449 | enterprise_org | 创新载体 |
| dwd_org_financing_info | 949 | enterprise_org | 融资信息 |
| dwd_org_merger_acquisition_info | 922 | enterprise_org | 并购信息 |
| dwd_org_industry_chain_pat_dtl | 888 | enterprise_org | 产业链专利明细 |
| dwd_forg_profile | 999 | enterprise_org | 国外机构简介 |
| dwd_forg_contact | 999 | enterprise_org | 国外机构联系方式 |

**关键疑问（待供应方确认）**：

- [ ] `dwd_org_annual_report_base` 77 万行是否属于「国内机构」承诺口径？是否应作为 Wave A 主数据源替代/补充 `dwd_org_base_info`（仅 2 万）？
- [ ] `dwd_forg_shareholder`（2.1 万有数）vs 承诺名 `dwd_forg_shareholder_info`（0）—— 哪个是正式映射目标？
- [ ] `dwd_org_change_record_info`（1,676）vs 承诺名 `dwd_org_changerecord_info`（0）—— 是否承诺名笔误？

---

## 5. 库内 dwd 全域分布（approx，272 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| other | 53 | 7,736,028 | 20,153.1 |
| **enterprise_org** | **100** | **649,323** | **566.2** |
| talent_paper_patent_project | 58 | 20,130 | 7.2 |
| industry_chain | 3 | 5,205 | 5.6 |
| finance_market | 8 | 0 | 970.6 |
| industry_topic | 48 | 0 | 1.0 |
| policy | 2 | 0 | 0.0 |

> enterprise_org 域 100 张表中，承诺 40 清单仅覆盖 36（含主/卫星）；其余 60+ 张为旁路表（含 §4 所列有数表）。

---

## 6. 对 Wave A / Mapping 的含义（与 08-01 一致，无新进展）

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | **继续做**：dwd_org_base_info + stock/financial/tags 路径仍可用 |
| Wave A P0 关单 | **仍不可** — 高管/股东/高校/科研/港澳台/招投标仍空 |
| Mapping enterprise_base | **可小样试点**（2 万 org）；勿按 711 万排产 |
| 卫星表 JOIN | stock↔base 覆盖极低，ETL 需容忍「有财务无主体」/「有主体无上市」 |
| **新增建议** | 评估是否将 `dwd_org_annual_report_base`（77 万）等旁路表纳入 Mapping 基线，先与供应方澄清口径 |

---

## 7. 与供应方口头进度

口头「国内机构 711 万 / 2500 万」：live 承诺主表 `dwd_org_base_info` 仍 **2 万**，连续三日无增长；但库内 `dwd_org_annual_report_base` 有 **77 万**。**请供应方明确**：

1. 711 万口径是否包含 `dwd_org_annual_report_base`？
2. 主表 `dwd_org_base_info` 是否还会继续灌数至 711 万，还是已止于样例 2 万？

---

## 8. 一句话给监管人

**承诺相关表连续三日无进展：结构 36/40 齐、数据 13/40 有行；主表仍 2 万。但库内存在 `dwd_org_annual_report_base` 77 万行等旁路有数表，需供应方澄清是否属承诺口径。**
