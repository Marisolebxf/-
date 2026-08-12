# 企业域 ODS→项目 DWD Mapping 基线（表级对照 / 辅助）

> **正式字段级施工请用**：[09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md)  
> 本文保留表级总览，供启动会对齐；细节与 ETL 以 `09` v4 为准。  
> **ODS 表名真源**：`third-party-source/doc/`  
> **DWD 目标（建表）**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)（MySQL `gkxlumenx_dwd`）  
> **作废**：旧 PG `企业模块.md`、三方参考 9 表清单、宽表 `enterprise`

---

## 1. 相对历史口径的变更

| 项 | 旧口径 | 本包（v1.2+） |
|----|--------|---------------|
| 表名真源 | live 推断 / Mapping v2 | **doc 承诺表** |
| 企业主表 | `dwd_org_reg_info` | **`dwd_org_base_info`** |
| 高校 | `dwd_org_hels_info` | **`dwd_org_heis_info`** |
| 招投标 | `dwd_org_bid_info` | **`dwd_bid_*_out` 四表** |
| 量子工商 | `dwd_company*` | **本波不贴源** → 相关字段 ❌ |
| 司法 | live 全套 | **承诺子集**（见下） |

---

## 2. 表级对照（承诺 ODS → 项目 DWD）

### 2.1 主数据 / 画像

| 项目 DWD | 承诺 ODS（gkxlumenx_ods） | 类型 | 备注 |
|----------|---------------------------|------|------|
| enterprise_base | dwd_org_base_info | direct | 字段级见 `09` §2 |
| enterprise_extra | dwd_org_base_info, org_product, stock_base | merge | `09` §3 |
| enterprise_history_name | — | gap | 本波不做 |
| enterprise_tag / tag_dict | — / 自建 | gap/later | |
| enterprise_finance_history | annual_financial, stock_finance | merge | `09` §4.1 |
| enterprise_executive | dwd_org_executive_info | direct | |
| enterprise_news | dwd_org_important_news_info | direct | |
| enterprise_bid | dwd_bid_*_out 四表 | merge | |
| enterprise_industry_chain | industry_tags + chain_info (+ product_tags) | merge | |
| enterprise_financing / invest / innovation_carrier | — | gap | |
| enterprise_patent_* | — | later | 另波 |

### 2.2 港澳台 / 科研 / 海外

见 `09` §6。

### 2.3 司法风险（承诺子集）

见 `09` §5。

---

## 3. 开放项（贴源后关闭）

| 项 | 状态 |
|----|------|
| 源库承诺表名可达 | 启动会核验 |
| company_* 不贴导致的缺口 | 🟡 catalog |
| bid / industry_tags 实际列名 vs `09` | 贴源 DDL 回写 |

**字段级与 ETL 交付以 `09` + `06` 为准。**
