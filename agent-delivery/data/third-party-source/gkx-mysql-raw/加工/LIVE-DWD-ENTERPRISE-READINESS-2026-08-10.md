# 三方源 live dwd 企业维齐套复核（2026-08-10）

> **探测时间**：2026-08-10 约 11:19（UTC+8）  
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）  
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）  
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）  
> **脚本产物**：`_live_dwd_enterprise_probe_2026-08-10.json`  
> **相对 08-07**：**P0 删表已恢复，但样例继续轮换** — 经营/要闻回库有数；国外高校/科研/财务新灌；高校/澳门/变更/招聘/部分招投标与破产明细等清零。⚠️

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **仍未齐备**（有数据 27/40；12 空；1 缺失） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以，路径再换**：主表仍 2 万；经营/要闻/双标签/港台/招投标主表/财务上市可用；**勿依赖** 高校/澳门/变更/招聘/中标候选/采购代理/失信/破产明细/国外主体 |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（P0 有数据 15/17；高校与澳门空；量级样例级） |
| 相对 08-07 是否有进展？ | **结构好转、数据面收缩**：缺失 3→1；P0 全在；但有数据 30→27，多张风险/招投标卫星清零 |

**齐备定义（本报告）**

1. 承诺表名在源库存在  
2. COUNT(*) > 0  
3. P0 核心路径可支撑贴源与 Mapping 试点  

当前：(1) 接近齐（仅 1 缺）+ (2) 面收缩 + (3) 试点可用但路径继续抖动。

---

## 2. 汇总分数（对比）

| 维度 | 2026-08-04 | 2026-08-07 | **2026-08-10** |
|------|------------|------------|----------------|
| 库内活跃 dwd 表数 | 277 | 283 | **285**（+2） |
| 承诺表存在 | 36/40 | 37/40 | **39/40**（+2） |
| 表缺失 | 4 | 3（含 2×P0） | **1**（仅国外 college） |
| 有数据（>0） | 30/40 | 30/40 | **27/40**（-3） |
| P0 表存在 | 17/17 | 15/17 | **17/17**（恢复） |
| P0 有数据 | 14/17 | 15/17 | **15/17**（同；集合变） |
| 主表 base_info | 20,000 | 20,000 | **20,000**（同） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（27）

| 优先级 | 表 | 行数 | 相对 08-07 |
|--------|-----|------|------------|
| P0 | **dwd_org_base_info** | **20,000** | 持平 |
| P0 | dwd_org_shareholder_info | 19,024 | 持平 |
| P0 | dwd_org_executive_info | 20,000 | 持平 |
| P0 | dwd_org_org_product_info | 20,000 | **恢复**（昨 MISSING） |
| P0 | dwd_org_annual_financial_info | 5,352 | 持平 |
| P0 | dwd_org_important_news_info | 19,983 | **恢复**（昨 MISSING；且 > 昔 913） |
| P0 | dwd_org_stock_base | 5,845 | 持平 |
| P0 | dwd_org_stock_finance_info | 5,352 | 持平 |
| P0 | dwd_research_institute_base_info | 2,075 | 持平 |
| P0 | dwd_special_hongkong_company | 20,000 | 持平 |
| P0 | dwd_special_taiwan_company | 20,000 | 持平 |
| P0 | dwd_bid_base_out | 20,000 | 持平 |
| P0 | dwd_industry_chain_info | 1,273 | 持平 |
| P0 | dwd_org_industry_tags | 20,000 | 持平 |
| P0 | dwd_org_industry_product_tags | 20,000 | 持平 |
| P1 | dwd_bid_target_item_out | 20,000 | 持平 |
| P1 | dwd_org_company_abnormal | 3,515 | 持平 |
| P1 | dwd_org_company_punish | 19,992 | 持平 |
| P1 | dwd_org_company_illegal | 887 | 持平 |
| P1 | dwd_org_risk_tax_punish | 10,959 | 持平 |
| P1 | dwd_org_opt_judicial_case | 19,877 | 持平 |
| P1 | dwd_org_risk_zhixing | 20,000 | 持平 |
| P1 | dwd_org_bankruptcy_public_cases | 20,000 | 持平 |
| P1 | dwd_forg_university_org_info | 20,000 | **新有数**（昨空） |
| P1 | dwd_forg_research_org_info | 20,000 | **新有数**（昨空） |
| P1 | dwd_foreign_org_annual_financial_info | 18,193 | **新有数**（昨空） |
| P1 | dwd_industry_chain_news_info | 1 | 持平 |

### 3.2 表在但空（12）— 含今日清零

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P0 | dwd_org_heis_info | **清零**（昨 20,000）⚠️ |
| P0 | dwd_special_aomen_company | **清零**（昨 396）⚠️ |
| P1 | dwd_org_changerecord_info | **清零**（昨 10,901）⚠️ |
| P1 | dwd_org_recruit_info | **清零**（昨 2,000）⚠️ |
| P1 | dwd_bid_win_candidate_out | **清零**（昨 20,000）⚠️ |
| P1 | dwd_bid_purchase_agency_out | **清零**（昨 20,000）⚠️ |
| P1 | dwd_org_bankruptcy_public_cases_list | **清零**（昨 20,000）⚠️ |
| P1 | dwd_forg_base_info | **清零**（昨 1,000）⚠️ |
| P1 | dwd_org_risk_shixin | 连续空（08-07 起） |
| P1 | dwd_forg_shareholder_info | 持续空（旁路 `dwd_forg_shareholder`=21,097） |
| P1 | dwd_forg_executive_info | 持续空 |
| P1 | dwd_forg_product_info | 持续空 |

### 3.3 表缺失（1）

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P1 | dwd_forg_college_org_info | 连续缺失（国外高校 college 名） |

---

## 4. 命名旁路（非承诺名但有数）

| live 表 | 行数 | 说明 |
|---------|------|------|
| **dwd_org_annual_report_base** | **770,000** | 企业域最大体量；口头 711 万口径待澄清 |
| dwd_forg_shareholder | 21,097 | 承诺名 `*_shareholder_info`=0 |
| dwd_forg_investment | 12,199 | |
| dwd_forg_industry | 7,569 | |
| dwd_forg_beneficiary_info | 6,276 | |
| dwd_org_change_record_info | 1,676 | 承诺名 `changerecord_info` 今日为 0（旁路仍有数） |

---

## 5. 库内 dwd 全域分布（approx，285 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| **enterprise_org** | **104** | **975,923** | **750.9** |
| other | 57 | 617,820 | 17,514.7 |
| talent_paper_patent_project | 62 | 27,017 | 8.0 |
| industry_chain | 3 | 1,273 | 0.2 |
| finance_market | 8 | 0 | 0.2 |
| industry_topic | 48 | 0 | 1.0 |
| policy | 3 | 0 | 0.1 |

> 注：`other` approx 相对 08-07 大幅下降属 `TABLE_ROWS` 估算抖动/非企业域变化，企业承诺表结论以精确 COUNT(*) 为准。

---

## 6. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | 走：base + 股东/高管/**经营**/财务/要闻/港台/招投标主表+标的/双标签/风险主路径；**暂停** 高校/澳门/变更/招聘/中标候选/采购代理/失信/破产明细 |
| Wave A P0 关单 | **仍不可** — 高校/澳门空；量级样例级；路径仍轮换 |
| Mapping | 小样可做；勿按 711 万排产 |
| 异常升级 | **当日知会供应方**：08-07 删表已恢复，但今日又清零 8 张有数表，样例批次仍不稳 |

---

## 7. 与供应方口头进度 / 待确认

口头「国内机构 711 万 / 2500 万」：主表仍 **2 万**；`dwd_org_annual_report_base` 仍 **77 万**。

**请供应方确认**：

1. 08-07 删除的经营/要闻为何今日恢复？正式冻结窗口是什么？  
2. 高校 / 澳门 / 变更 / 招聘 / 中标候选 / 采购代理 / 破产明细 / 国外主体 今日清零原因？  
3. 国外 university/research/年报财务新灌是否替代 college 缺失名？  
4. 711 万口径与年报底表关系？

---

## 8. 一句话给监管人

**结构好转：P0 全在、缺失仅 1、经营/要闻恢复且国外三表新灌；但有数据面 30→27，高校/澳门及多张卫星清零，样例批次仍在轮换。主表仍 2 万，未齐备。**
