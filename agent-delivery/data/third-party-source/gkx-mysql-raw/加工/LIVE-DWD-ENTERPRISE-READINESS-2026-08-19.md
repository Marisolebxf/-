# 三方源 live dwd 企业维齐套复核（2026-08-19）

> **探测时间**：2026-08-19 约 18:50（UTC+8）  
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）  
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）  
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）  
> **脚本产物**：`_live_dwd_enterprise_probe_2026-08-19.json`  
> **相对 08-17**：**样例扩量 + 双标签清零** — 主表 2 万→**4 万**；多数有数表翻倍或显著增长；失信回灌 2 万；**P0 双标签 2 万→0**，P0 有数据 17→**15**。

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **仍未齐备**（有数据 34/40；5 空；1 缺失；量级仍样例级，但主表已扩至 4 万） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以，主路径加宽**：base/股东/高管/港澳台/招投标/财务/风险多数扩量；**勿依赖** 双标签；国外股东/高管/经营仍空 |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（主表 4 万仍远低于口头 711 万；college 缺失；双标签清零） |
| 相对 08-17 是否有进展？ | **有扩量、有回退**：失信回灌；双标签清零需当日知会 |

**齐备定义（本报告）**

1. 承诺表名在源库存在  
2. COUNT(*) > 0  
3. P0 核心路径可支撑贴源与 Mapping 试点  

当前：(1) 接近齐（仅 1 缺）+ (2) 有数据面 34/40 + (3) P0 试点仍可做，但标签路径中断。

---

## 2. 汇总分数（对比）

| 维度 | 2026-08-13 | 2026-08-17 | **2026-08-19** |
|------|------------|------------|----------------|
| 库内活跃 dwd 表数 | 270 | 276 | **270**（-6） |
| 承诺表存在 | 39/40 | 39/40 | **39/40**（同） |
| 表缺失 | 1 | 1 | **1**（同，college） |
| 有数据（>0） | 35/40 | 35/40 | **34/40**（-1） |
| P0 表存在 | 17/17 | 17/17 | **17/17** |
| P0 有数据 | 17/17 | 17/17 | **15/17**（-2，双标签清零） |
| 主表 base_info | 20,000 | 20,000 | **40,000**（×2） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（34）

| 优先级 | 表 | 行数 | 相对 08-17 |
|--------|-----|------|------------|
| P0 | **dwd_org_base_info** | **40,000** | **×2** |
| P0 | dwd_org_shareholder_info | 38,629 | 19,024→ |
| P0 | dwd_org_executive_info | 40,000 | **×2** |
| P0 | dwd_org_org_product_info | 20,000 | 持平 |
| P0 | dwd_org_annual_financial_info | 20,000 | 5,352→ |
| P0 | dwd_org_important_news_info | 39,638 | 19,983→ |
| P0 | dwd_org_stock_base | 6,925 | 5,845→ |
| P0 | dwd_org_stock_finance_info | 24,335 | 5,352→ |
| P0 | dwd_org_heis_info | 2,933 | 1,819→ |
| P0 | dwd_research_institute_base_info | 4,149 | 2,075→ |
| P0 | dwd_special_hongkong_company | 40,000 | **×2** |
| P0 | dwd_special_taiwan_company | 40,000 | **×2** |
| P0 | dwd_special_aomen_company | 792 | 396→ **×2** |
| P0 | dwd_bid_base_out | 39,962 | 20,000→ |
| P0 | dwd_industry_chain_info | 1,273 | 持平 |
| P1 | dwd_org_changerecord_info | 23,313 | 3,447→ |
| P1 | dwd_org_recruit_info | 21,912 | 2,000→ |
| P1 | dwd_bid_win_candidate_out | 39,520 | 19,524→ |
| P1 | dwd_bid_purchase_agency_out | 39,975 | 19,976→ |
| P1 | dwd_bid_target_item_out | 38,646 | 20,000→ |
| P1 | dwd_org_company_abnormal | 4,836 | 3,515→ |
| P1 | dwd_org_company_punish | 39,246 | 19,992→ |
| P1 | dwd_org_company_illegal | 1,049 | 887→ |
| P1 | dwd_org_risk_tax_punish | 10,959 | 持平 |
| P1 | dwd_org_opt_judicial_case | 19,877 | 持平 |
| P1 | dwd_org_risk_shixin | 20,000 | **回灌**（昨=0） |
| P1 | dwd_org_risk_zhixing | 39,796 | 20,000→ |
| P1 | dwd_org_bankruptcy_public_cases | 33,904 | 20,000→ |
| P1 | dwd_org_bankruptcy_public_cases_list | 31,943 | 20,000→ |
| P1 | dwd_forg_base_info | 1 | 持平 |
| P1 | dwd_forg_university_org_info | 24,256 | 20,000→ |
| P1 | dwd_forg_research_org_info | 23,154 | 20,000→ |
| P1 | dwd_foreign_org_annual_financial_info | 18,193 | 持平 |
| P1 | dwd_industry_chain_news_info | 12,291 | 476→ |

### 3.2 表在但空（5）

| 优先级 | 表 | 说明 |
|--------|-----|------|
| **P0** | **dwd_org_industry_tags** | **清零**（昨 20,000）⚠️ |
| **P0** | **dwd_org_industry_product_tags** | **清零**（昨 20,000）⚠️ |
| P1 | dwd_forg_shareholder_info | 持续空（旁路 `dwd_forg_shareholder`=21,097） |
| P1 | dwd_forg_executive_info | 持续空 |
| P1 | dwd_forg_product_info | 持续空 |

### 3.3 表缺失（1）

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P1 | dwd_forg_college_org_info | 连续缺失 |

---

## 4. 命名旁路

| live 表 | 行数 | 说明 |
|---------|------|------|
| **dwd_org_annual_report_base** | **770,000** | 企业域最大体量；口头 711 万口径待澄清 |
| dwd_forg_shareholder | 21,097 | 承诺名 `*_shareholder_info`=0 |
| dwd_org_change_record_info | 1,676 | 承诺名 `changerecord_info`=23,313（双轨） |

---

## 5. 库内 dwd 全域分布（approx，270 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| other | 58 | 11,160,088 | 16,350.4 |
| talent_paper_patent_project | 46 | 2,080,999 | 2,700.0 |
| **enterprise_org** | **98** | **1,230,500** | **777.7** |
| policy | 3 | 43,748 | 343.0 |
| industry_chain | 9 | 20,582 | 55.0 |
| finance_market | 8 | 19,400 | 8.7 |
| industry_topic | 48 | 1,338 | 1.2 |

> 注：`other` / 人才专利 / 政策 / 金融 approx 相对 08-17 大幅上升，属全域灌数变化；企业承诺表结论以精确 COUNT(*) 为准。

---

## 6. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | 主路径（base/股东/高管/港澳台/招投标/财务/风险）**可按 4 万级样例继续**；**暂停** 双标签依赖 |
| Wave A P0 关单 | **仍不可** — 双标签空；college 缺失；量级仍远低于口头 711 万 |
| Mapping | 小样可扩至 4 万 org；勿按 711 万排产 |
| 异常升级 | **请监管人当日飞书知会**：双标签清零；同时告知主表扩至 4 万、失信回灌 |

---

## 7. 与供应方口头进度 / 待确认

口头「国内机构 711 万 / 2500 万」：主表现 **4 万**（仍样例级）；`dwd_org_annual_report_base` 仍 **77 万**。

**请供应方确认**：

1. 今日是否为第二批样例扩量（约翻倍）？正式冻结窗口？  
2. 双标签为何清零？是否还会回灌？  
3. `dwd_org_risk_shixin` 回灌是否稳定？  
4. `college` / 国外股东·高管·经营何时齐套？  
5. 711 万口径与年报底表关系？

---

## 8. 一句话给监管人

**今日出现明显扩量：主表 2 万→4 万，多数承诺表翻倍或显著增长，失信回灌 2 万；但 P0 双标签清零，有数据 35→34、P0 有数据 17→15。未达口头齐套——烟测可走扩量主路径，勿依赖标签；请当日知会供应方。**
