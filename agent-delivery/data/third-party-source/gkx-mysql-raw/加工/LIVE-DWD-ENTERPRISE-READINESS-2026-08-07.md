# 三方源 live dwd 企业维齐套复核（2026-08-07）

> **探测时间**：2026-08-07 约 11:07（UTC+8）  
> **库**：MySQL gkx @ 183.240.141.251:3318（只读 gkx_reader_zp；实测 `VERSION()` = `9.7.0-commercial`）  
> **对照**：Wave A 承诺 40 表（GDF-ENT-WORKPACK-v1 / 02-WaveA-贴源表清单.yaml）  
> **方法**：表存在性 + COUNT(*)（不以 Navicat「行」/ TABLE_ROWS 为准）  
> **脚本产物**：`_live_dwd_enterprise_probe_2026-08-07.json`  
> **相对 08-04**：**结构抖动 + 标签回灌** — 双标签空→各 2 万；产业链 180→1,273；国外 3 表新建（空）；但 **2 张 P0 表从库中消失**（经营/要闻），失信表清零。⚠️

---

## 1. 总判定

| 问题 | 判定 |
|------|------|
| 承诺表是否「齐备」？ | **仍未齐备**；且出现 **P0 表删表级回退**（经营/要闻 MISSING） |
| 能否开 Wave A 烟测 / 主体 Mapping 试点？ | **可以，但避开缺失/清零路径**：主表仍 2 万；股东/高管/港澳台/招投标/财务/上市/双标签可用；**勿依赖** 要闻/经营产品/失信 |
| 能否按承诺口径宣称企业维齐套 / P0 关单？ | **否**（P0 存在仅 15/17；有数据 15/17；缺失含 2×P0；量级仍样例级） |
| 相对 08-04 是否有进展？ | **喜忧参半**：标签/产业链进展；国外建表；但 P0 删表 + 失信清零需当日升级供应方 |

**齐备定义（本报告）**

1. 承诺表名在源库存在  
2. COUNT(*) > 0  
3. P0 核心路径可支撑贴源与 Mapping 试点  

当前：(1) 回退（P0 缺 2）+ (2) 有数据面仍 30/40（集合变化）+ (3) 试点可用但勿踩缺失表。

---

## 2. 汇总分数（对比）

| 维度 | 2026-08-03 | 2026-08-04 | **2026-08-07** |
|------|------------|------------|----------------|
| 库内活跃 dwd 表数 | 277 | 277 | **283**（+6） |
| 承诺表存在 | 36/40 | 36/40 | **37/40**（+1） |
| 表缺失 | 4 | 4 | **3**（集合已换，含 **2×P0**） |
| 有数据（>0） | 22/40 | 30/40 | **30/40**（数量同，集合变） |
| P0 表存在 | 17/17 | 17/17 | **15/17**（⚠️ -2） |
| P0 有数据 | 9/17 | 14/17 | **15/17**（+1；靠标签回灌） |
| 主表 base_info | 20,000 | 20,000 | **20,000**（同） |

---

## 3. 承诺 40 表明细（精确行数）

### 3.1 有数据（30）

| 优先级 | 表 | 行数 | 相对 08-04 |
|--------|-----|------|------------|
| P0 | **dwd_org_base_info** | **20,000** | 持平 |
| P0 | dwd_org_shareholder_info | 19,024 | 持平 |
| P0 | dwd_org_executive_info | 20,000 | 持平 |
| P0 | dwd_org_annual_financial_info | 5,352 | 持平 |
| P0 | dwd_org_stock_base | 5,845 | 持平 |
| P0 | dwd_org_stock_finance_info | 5,352 | 持平 |
| P0 | dwd_org_heis_info | 20,000 | 持平 |
| P0 | dwd_research_institute_base_info | 2,075 | 持平 |
| P0 | dwd_special_hongkong_company | 20,000 | 持平 |
| P0 | dwd_special_taiwan_company | 20,000 | 持平 |
| P0 | dwd_special_aomen_company | 396 | 持平 |
| P0 | dwd_bid_base_out | 20,000 | 持平 |
| P0 | dwd_industry_chain_info | 1,273 | **+1,093**（昨 180） |
| P0 | dwd_org_industry_tags | 20,000 | **新有数**（昨=0） |
| P0 | dwd_org_industry_product_tags | 20,000 | **新有数**（昨=0） |
| P1 | dwd_org_changerecord_info | 10,901 | 持平 |
| P1 | dwd_org_recruit_info | 2,000 | 持平 |
| P1 | dwd_bid_win_candidate_out | 20,000 | 持平 |
| P1 | dwd_bid_purchase_agency_out | 20,000 | 持平 |
| P1 | dwd_bid_target_item_out | 20,000 | 持平 |
| P1 | dwd_org_company_abnormal | 3,515 | 持平 |
| P1 | dwd_org_company_punish | 19,992 | 持平 |
| P1 | dwd_org_company_illegal | 887 | 持平 |
| P1 | dwd_org_risk_tax_punish | 10,959 | 持平 |
| P1 | dwd_org_opt_judicial_case | 19,877 | 持平 |
| P1 | dwd_org_risk_zhixing | 20,000 | 持平 |
| P1 | dwd_org_bankruptcy_public_cases | 20,000 | 持平 |
| P1 | dwd_org_bankruptcy_public_cases_list | 20,000 | 持平 |
| P1 | dwd_forg_base_info | 1,000 | 持平 |
| P1 | dwd_industry_chain_news_info | 1 | 持平 |

### 3.2 表在但空（7）

| 优先级 | 表 | 说明 |
|--------|-----|------|
| P1 | dwd_org_risk_shixin | **清零**（08-04=19,958 → 0）⚠️ |
| P1 | dwd_forg_shareholder_info | 持续空（旁路 `dwd_forg_shareholder`=21,097） |
| P1 | dwd_forg_executive_info | 持续空 |
| P1 | dwd_forg_product_info | 持续空 |
| P1 | dwd_forg_university_org_info | **新建空表**（08-04 缺失） |
| P1 | dwd_forg_research_org_info | **新建空表**（08-04 缺失） |
| P1 | dwd_foreign_org_annual_financial_info | **新建空表**（08-04 缺失） |

### 3.3 表缺失（3）⚠️ 含 2×P0

| 优先级 | 表 | 相对 08-04 |
|--------|-----|------------|
| **P0** | **dwd_org_org_product_info** | 昨 PRESENT/0 → **今日库中不存在** |
| **P0** | **dwd_org_important_news_info** | 昨 PRESENT/**913** → **今日库中不存在** |
| P1 | dwd_forg_college_org_info | 连续缺失（国外高校） |

---

## 4. 命名旁路（非承诺名但有数）

| live 表 | 行数 | 说明 |
|---------|------|------|
| **dwd_org_annual_report_base** | **770,000** | 企业域最大体量；口头 711 万口径待澄清 |
| dwd_forg_shareholder | 21,097 | 承诺名 `dwd_forg_shareholder_info`=0 |
| dwd_forg_investment | 12,199 | |
| dwd_forg_industry | 7,569 | |
| dwd_forg_beneficiary_info | 6,276 | |
| dwd_org_change_record_info | 1,676 | 承诺名 `changerecord_info` 仍有 10,901 |

---

## 5. 库内 dwd 全域分布（approx，283 表）

| 域 | 表数 | approx_rows | data_mb |
|----|------|-------------|---------|
| other | 57 | 7,736,028 | 20,153.2 |
| **enterprise_org** | **102** | **968,506** | **729.9** |
| talent_paper_patent_project | 62 | 27,017 | 8.0 |
| industry_chain | 3 | 1,273 | 0.2 |
| finance_market | 8 | 0 | 970.6 |
| industry_topic | 48 | 0 | 1.0 |
| policy | 3 | 0 | 0.1 |

---

## 6. 对 Wave A / Mapping 的含义

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | 继续：base + 股东/高管/港澳台/招投标/财务/上市/**双标签**；产业链可试（1,273）；**暂停** 要闻/经营产品/失信 |
| Wave A P0 关单 | **仍不可** — 2×P0 表缺失；量级样例级 |
| Mapping | 小样可做；勿按 711 万排产 |
| 异常升级 | **当日飞书知会供应方 / GDF / 数据 Lead**：P0 删表 + 失信清零 |

---

## 7. 与供应方口头进度 / 待确认

口头「国内机构 711 万 / 2500 万」：主表仍 **2 万**；`dwd_org_annual_report_base` 仍 **77 万**。

**请供应方当日确认**：

1. 为何 `dwd_org_org_product_info`、`dwd_org_important_news_info` 从库中删除？是否误删/改名/迁库？何时恢复？  
2. `dwd_org_risk_shixin` 为何从约 2 万清零？  
3. 双标签今日回灌是否为正式样例冻结批次？  
4. `dwd_forg_college_org_info` 何时建表？其余国外新建空表何时灌数？  
5. 711 万口径与年报底表关系？

---

## 8. 一句话给监管人

**标签与产业链有进展（双标签各 2 万、产业链 1,273），国外 3 表已建空壳；但出现严重回退：2 张 P0（经营/要闻）从表清单消失、失信表清零。有数据仍 30/40，主表 2 万，未齐备——请当日知会供应方查删表原因。**
