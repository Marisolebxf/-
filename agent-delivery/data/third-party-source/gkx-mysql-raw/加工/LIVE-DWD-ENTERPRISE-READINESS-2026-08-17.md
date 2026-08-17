# 三方源 live dwd 企业维齐套复核（2026-08-17）

> **探测时间**：2026-08-17 约 17:31（UTC+8）  
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）  
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）  
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）  
> **脚本产物**：`_live_dwd_enterprise_probe_2026-08-17.json`  
> **相对 08-13**：**承诺 40 表行数/状态完全持平** — 有数据仍 35/40；P0 仍全有数 17/17；无清零、无新增。库内活跃 dwd 270→**276**（+6，均为非承诺 `dwd_industry_analysis_*` 旁路）。

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **仍未齐备**（有数据 35/40；4 空；1 缺失；量级仍样例级） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以，路径与 08-12/08-13 同宽**：P0 全路径可烟测；失信与国外股东/高管/经营仍空 |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（主表仍 2 万；远低于口头 711 万；college 缺失；失信等空） |
| 相对 08-13 是否有进展？ | **承诺面持平（连续稳定）**；库内新增 6 张产业分析旁路表，未改变 Wave A 承诺集 |

**齐备定义（本报告）**

1. 承诺表名在源库存在  
2. COUNT(*) > 0  
3. P0 核心路径可支撑贴源与 Mapping 试点  

当前：(1) 接近齐（仅 1 缺）+ (2) 持平 + (3) P0 试点路径齐，全量齐套仍否。

---

## 2. 汇总分数（对比）

| 维度 | 2026-08-12 | 2026-08-13 | **2026-08-17** |
|------|------------|------------|----------------|
| 库内活跃 dwd 表数 | 286 | 270 | **276**（+6） |
| 承诺表存在 | 39/40 | 39/40 | **39/40**（同） |
| 表缺失 | 1 | 1 | **1**（同，college） |
| 有数据（>0） | 35/40 | 35/40 | **35/40**（同） |
| P0 表存在 | 17/17 | 17/17 | **17/17** |
| P0 有数据 | 17/17 | 17/17 | **17/17**（持平） |
| 主表 base_info | 20,000 | 20,000 | **20,000**（同） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（35）— 与 08-13 逐表一致

| 优先级 | 表 | 行数 | 相对 08-13 |
|--------|-----|------|------------|
| P0 | **dwd_org_base_info** | **20,000** | 持平 |
| P0 | dwd_org_shareholder_info | 19,024 | 持平 |
| P0 | dwd_org_executive_info | 20,000 | 持平 |
| P0 | dwd_org_org_product_info | 20,000 | 持平 |
| P0 | dwd_org_annual_financial_info | 5,352 | 持平 |
| P0 | dwd_org_important_news_info | 19,983 | 持平 |
| P0 | dwd_org_stock_base | 5,845 | 持平 |
| P0 | dwd_org_stock_finance_info | 5,352 | 持平 |
| P0 | dwd_org_heis_info | 1,819 | 持平 |
| P0 | dwd_research_institute_base_info | 2,075 | 持平 |
| P0 | dwd_special_hongkong_company | 20,000 | 持平 |
| P0 | dwd_special_taiwan_company | 20,000 | 持平 |
| P0 | dwd_special_aomen_company | 396 | 持平 |
| P0 | dwd_bid_base_out | 20,000 | 持平 |
| P0 | dwd_industry_chain_info | 1,273 | 持平 |
| P0 | dwd_org_industry_tags | 20,000 | 持平 |
| P0 | dwd_org_industry_product_tags | 20,000 | 持平 |
| P1 | dwd_org_changerecord_info | 3,447 | 持平 |
| P1 | dwd_org_recruit_info | 2,000 | 持平 |
| P1 | dwd_bid_win_candidate_out | 19,524 | 持平 |
| P1 | dwd_bid_purchase_agency_out | 19,976 | 持平 |
| P1 | dwd_bid_target_item_out | 20,000 | 持平 |
| P1 | dwd_org_company_abnormal | 3,515 | 持平 |
| P1 | dwd_org_company_punish | 19,992 | 持平 |
| P1 | dwd_org_company_illegal | 887 | 持平 |
| P1 | dwd_org_risk_tax_punish | 10,959 | 持平 |
| P1 | dwd_org_opt_judicial_case | 19,877 | 持平 |
| P1 | dwd_org_risk_zhixing | 20,000 | 持平 |
| P1 | dwd_org_bankruptcy_public_cases | 20,000 | 持平 |
| P1 | dwd_org_bankruptcy_public_cases_list | 20,000 | 持平 |
| P1 | dwd_forg_base_info | 1 | 持平 |
| P1 | dwd_forg_university_org_info | 20,000 | 持平 |
| P1 | dwd_forg_research_org_info | 20,000 | 持平 |
| P1 | dwd_foreign_org_annual_financial_info | 18,193 | 持平 |
| P1 | dwd_industry_chain_news_info | 476 | 持平 |

### 3.2 表在但空（4）— 同 08-13

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P1 | dwd_org_risk_shixin | 连续空（08-07 起） |
| P1 | dwd_forg_shareholder_info | 持续空（旁路 `dwd_forg_shareholder`=21,097） |
| P1 | dwd_forg_executive_info | 持续空 |
| P1 | dwd_forg_product_info | 持续空 |

**今日无清零、无新增有数。**

### 3.3 表缺失（1）

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P1 | dwd_forg_college_org_info | 连续缺失 |

---

## 4. 命名旁路 / 库内变化

| live 表 | 行数 | 说明 |
|---------|------|------|
| **dwd_org_annual_report_base** | **770,000** | 企业域最大体量；口头 711 万口径待澄清 |
| dwd_forg_shareholder | 21,097 | 承诺名 `*_shareholder_info`=0 |
| dwd_org_change_record_info | 1,676 | 承诺名 `changerecord_info`=3,447（双轨） |

**新增旁路（非承诺 40）**：`dwd_industry_analysis_companies` / `content_types` / `countries` / `documents` / `industries` / `topics`（产业分析簇，共 6 张）。

---

## 5. 库内 dwd 全域分布（approx，276 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| **enterprise_org** | **99** | **1,039,902** | **787.2** |
| other | 57 | 617,820 | 17,514.7 |
| talent_paper_patent_project | 52 | 25,398 | 7.4 |
| industry_chain | 9 | 8,827 | 40.8 |
| finance_market | 8 | 0 | 0.2 |
| industry_topic | 48 | 0 | 1.0 |
| policy | 3 | 0 | 0.1 |

---

## 6. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | **维持宽路径**：全 P0 + 招投标全套 + 风险主路径；勿依赖失信与国外股东/高管/经营 |
| Wave A P0 关单 | **仍不可** — 量级样例级；缺口未变 |
| Mapping | 小样可做；勿按 711 万排产 |
| 异常升级 | 承诺面连续稳定，**无需升级**；继续跟进失信/college/国外子表与冻结窗口；产业分析旁路可登记观察，不并入 Wave A |

---

## 7. 与供应方口头进度 / 待确认

口头「国内机构 711 万 / 2500 万」：主表仍 **2 万**；`dwd_org_annual_report_base` 仍 **77 万**。

**请供应方确认**（与前几日同，仍开放）：

1. 当前样例是否已进入正式冻结批次？  
2. `dwd_org_risk_shixin` / 国外股东·高管·经营 / `college` 何时齐套？  
3. 711 万口径与年报底表关系？  
4. 新增 `dwd_industry_analysis_*` 是否正式对外、是否纳入后续企业工作包？

---

## 8. 一句话给监管人

**承诺 40 表相对 08-13 完全持平：有数据 35/40、P0 全有数 17/17、无清零。库内 +6 张产业分析旁路，未伤 Wave A。主表仍 2 万，未达口头齐套——可继续宽路径烟测，仍不可 P0 关单。**
