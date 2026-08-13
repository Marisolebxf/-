# 企业维 ODS → 项目 DWD Mapping — 导读（v2.1）

> **版本**：v2.1（2026-08-13）  
> **读者**：GDF 产线  
> **字段级施工真源（唯一）**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)  
> （仓内同源：`data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md` v1.2）  
> **建表 DDL**：[`10-DWD-MySQL-DDL/`](10-DWD-MySQL-DDL/)  
> **作废**：本文件旧版短字段表（v4 及以前）、WORKPACK-v1、PG `demo_gdf_data`、宽表 `enterprise`

本文**不是**字段矩阵全文，只作开工导读。配置 Mapping / ETL 时以 **`09-企业域-ETL-Mapping明细…`** 为准。

---

## 1. 相对 WORKPACK-v2.0 短版 `09` 的关键纠偏

| 项 | 旧短版 v4 | **以 Mapping 明细 v1.2 为准** |
|----|-----------|-------------------------------|
| 施工真源 | 短字段表 | **明细全文**（直接/关联/指标/国外） |
| 融资 / 投资 / 标签 / 母子公司 | ❌/另波 | **直接映射**（§2.1） |
| 招聘 | 缺口 | **`enterprise_recruit`**（§3.16） |
| 曾用名 | ❌ 量子缺口 | **`changerecord` 含「名称」行** → `enterprise_history_name` |
| 招投标 | base+win+agency+target | **win_candidate + base_out**；agency/target **暂不映射**（§2.4） |
| 专利 | 另波 | **`dwd_patent` → patent_detail / history / chain_patent`** |
| 国外机构 | 先贴源不洗 | **`enterprise_forg_*` 六表**（§2.5 / §3.15） |
| 高校 / 科研 / 港澳台 | 可扩展 | **本期暂不映射**（§2.4；Wave A 仍可贴源镜像） |
| 产业链 org_id | tags+chain_info | **`dwd_org_industry_chain_dtl.enterprise_code` → base**；现网 credit 空为已知阻塞（§5 #6） |
| industry_category | industry 或 l1 | **优先 `industry_l4_name` / `industry_l4_code`** |
| org_id | 复用 | **源 org_id 直接复用，不重新生成**（§1.1） |

DDL 差集（相对旧 PG）仍有效：只认 `10/`；主表 `enterprise_base`；禁宽表 `enterprise`；禁自造 org_id；`enterprise_financing` 字段契约；风险 `org_id` collation。

---

## 2. 建议 ETL 顺序（摘自明细总览）

1. `enterprise_base` + `enterprise_extra` ← `dwd_org_base_info`（+ product / stock）  
2. `enterprise_executive` / `enterprise_news` / `enterprise_finance_history`  
3. `enterprise_financing` / `enterprise_invest` / `enterprise_tag` / `enterprise_parent_subsidiary`  
4. `enterprise_history_name` ← changerecord（名称变更）  
5. `enterprise_supply_chain` ← shareholder（投资方部分）  
6. `enterprise_bid` ← win_candidate + base_out  
7. `enterprise_recruit` ← recruit_info  
8. `risk_*` / `risk_bankruptcy_party`（明细 §3.13）  
9. 专利三表 ← `dwd_patent`（名称关联 org_id）  
10. `enterprise_forg_*` ← 国外源表  
11. 指标：`enterprise_risk_summary` / `region_summary` / `industry_summary` 等（§4）

**过滤**：源侧默认 `is_deleted = 0`（有该列时）。

---

## 3. 交付物（与 `06` 一致）

1. 字段级 Mapping 可追溯到 **明细 §3 / §4** 行  
2. DDL 对照 `10/`（含 `enterprise_recruit`、`enterprise_forg_*`）  
3. 抽样对账 ≥20 条 / 表；缺口登记，禁止假值  
4. 已知阻塞（credit 空 → industry_chain.org_id）书面说明，勿静默造 id  

## 4. 参考

| 材料 | 路径 |
|------|------|
| Mapping 明细（本包） | `09-企业域-ETL-Mapping明细-源表到DWD.md` |
| DDL | `10-DWD-MySQL-DDL/` |
| 作废对照 | `11-作废与误源对照.md` |
| Wave A | `02-WaveA-贴源表清单.yaml` |
