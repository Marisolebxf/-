# 三方源 live dwd 企业维齐套复核（2026-08-01）

> **探测时间**：2026-08-01 约 18:14（UTC+8）
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）
> **相对 07-31**：主表 dwd_org_base_info 由 0 → 20,000

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **结构基本齐，数据未齐备** |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以**（主表已有 2 万样例） |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（多张 P0/P1 仍空；4 表缺失；量级远低于口头 711 万） |

**齐备定义（本报告）**

1. 承诺表名在源库存在
2. COUNT(*) > 0（可查询到业务行）
3. P0 核心路径（主数据 + 关键卫星）可支撑贴源与 Mapping 试点

当前仅满足 (1) 大部 + (2) 部分 + (3) 弱试点。

---

## 2. 汇总分数

| 维度 | 2026-07-31 | **2026-08-01** |
|------|------------|----------------|
| 承诺表存在 | 36/40 | **36/40**（同） |
| 表缺失 | 4 | **4**（同，均为国外机构 P1） |
| 有数据（>0） | 12/40 | **13/40** |
| P0 表存在 | 17/17 | **17/17** |
| P0 有数据 | 8/17 | **9/17** |
| 主表 base_info | **0** | **20,000**（distinct org_id=20,000） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（13）

| 优先级 | 表 | 行数 | 备注 |
|--------|-----|------|------|
| P0 | **dwd_org_base_info** | **20,000** | 主数据已灌样例；样例含信用代码/省市区 |
| P0 | dwd_org_stock_base | 5,845 | 与 base 交集仅约 **2** 个 org_id（键覆盖极低） |
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

### 3.2 表在但空（23）— 结构就绪、数据未齐

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

- dwd_org_changerecord_info（承诺名；旁路见下）

#### P1 国外

- dwd_forg_shareholder_info
- dwd_forg_product_info

### 3.3 表缺失（4）— P1 国外

- dwd_forg_college_org_info
- dwd_forg_university_org_info
- dwd_forg_research_org_info
- dwd_foreign_org_annual_financial_info

### 3.4 命名旁路（非承诺名但有数）

| live 表 | 行数 | 说明 |
|---------|------|------|
| dwd_org_change_record_info | 1,676 | 承诺名为 dwd_org_changerecord_info（无下划线分段）= 0 |
| dwd_org_annual_report_base | 770,000 | 非 Wave A 40；企业相关大体量 |
| dwd_org_reg_info / dwd_org_hels_info | 0 | 旧名仍空；主路径已是 dwd_org_base_info |

---

## 4. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | **建议立刻做**：dwd_org_base_info + stock/financial/tags |
| Wave A P0 关单 | **仍不可** — 高管/股东/高校/科研/港澳台/招投标仍空 |
| Mapping enterprise_base | **可小样试点**（2 万 org）；勿按 711 万排产 |
| 卫星表 JOIN | stock↔base 覆盖极低，ETL 需容忍「有财务无主体」/「有主体无上市」 |

---

## 5. 与供应方口头进度

口头「国内机构 711 万 / 2500 万」：live 承诺主表目前 **2 万**，仍差两个数量级。请供应方确认灌数批次与目标表是否即为 dwd_org_base_info。

---

## 6. 一句话给监管人

**承诺相关表：结构 36/40 齐、数据 13/40 有行；主表已从空变为 2 万，企业维「未齐备但可启动烟测与 Mapping 小样」。**
