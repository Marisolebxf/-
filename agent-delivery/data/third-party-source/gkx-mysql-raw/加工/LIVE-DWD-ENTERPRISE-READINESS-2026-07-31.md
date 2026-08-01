# 三方源 live `dwd_*` 实况分析（企业维齐套）

> **探测时间**：2026-07-31 约 20:10–20:20（UTC+8）  
> **库**：MySQL `gkx` @ `183.240.141.251:3318`（`VERSION()` = 9.7.0-commercial）  
> **范围**：仅 `dwd_*` 活跃表（排除 `*_bak*`）；`ods_*` 不分析  
> **方法**：`information_schema` + 企业相关表 `COUNT(*)` 精确计数  
> **对照清单**：`GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml`（承诺 40 表）  
> **原始 JSON**：`_live_dwd_enterprise_probe_2026-07-31.json`  
> **脚本**：`_probe_live_dwd_enterprise.py`（只读）

---

## 1. 总览（全库 `dwd_*`）

| 指标 | 值 |
|------|-----|
| 活跃 `dwd_*` 表数 | **272** |
| `TABLE_ROWS` 合计（不可靠） | ~891 万 |
| 数据+索引体积合计 | ~21.7 GB |

**注意**：InnoDB `TABLE_ROWS` 与真实 `COUNT(*)` 严重偏离（见 §4）。齐套判断必须以精确计数为准。

### 体积最大的 `dwd_*`（精确行数抽样）

| 表 | 体积约 | 精确行数 | 备注 |
|----|--------|----------|------|
| dwd_opt_judicial_case_detail | 16.1 GB | **11,660,061** | 司法明细；**不在**企业 Wave A 承诺 40 表 |
| dwd_option_daily_quotation | 1.9 GB | **8,043,445** | 期权行情；金融类 |
| dwd_news_base | 1.3 GB | **0** | 有体积、无行（空壳/未提交？） |
| dwd_ls_stock_daily_quotation | 0.97 GB | **0** | 同上 |
| dwd_hk_sec_daily_quotation | 0.76 GB | **0** | 同上 |
| dwd_org_annual_report_base | 0.49 GB | **770,000** | 年报基础；**不在**承诺 40，但企业相关 |
| dwd_org_base_info | 13.5 MB | **0** | 承诺主表，**空** |

与供应方今日「九类落库进度」对照：库内可见大体量主要在**司法明细 / 期权行情 / 年报基础**，**不是**承诺主表 `dwd_org_base_info` 的 711 万机构主体。

---

## 2. 企业维结论（相对承诺 40 表）

### 2.1 一句话

**表结构大体齐（36/40 存在），数据不齐——尤其主体主数据为空；企业维尚未达到可贴源关单 / 可洗 Mapping 的齐套状态。**

### 2.2 齐套评分

| 维度 | 结果 | 说明 |
|------|------|------|
| 承诺表名存在 | **36 / 40** | 4 张国外机构相关缺失 |
| P0 表名存在 | **17 / 17** | 承诺 P0 表均已建 |
| 承诺表有数据（>0 行） | **12 / 40** | 精确计数 |
| P0 有数据 | **8 / 17** | 主数据/港澳台/招投标/高校/科研均为 0 |
| 主体主数据 | ❌ | `dwd_org_base_info` = **0**；旧名 `dwd_org_reg_info` = **0**；`dwd_company*` = **0** |
| Mapping `enterprise_base` | ❌ 阻塞 | 无 org 主体行可映射 |

### 2.3 承诺 40 表逐表（精确行数）

#### 有数据（12）— 可烟测贴源

| 优先级 | 表 | 精确行数 |
|--------|-----|----------|
| P0 | dwd_org_stock_base | 5,845 |
| P0 | dwd_org_annual_financial_info | 5,352 |
| P0 | dwd_org_stock_finance_info | 5,352 |
| P0 | dwd_org_industry_product_tags | 5,000 |
| P0 | dwd_org_industry_tags | 4,912 |
| P1 | dwd_industry_chain_news_info | 5,000 |
| P0 | dwd_org_org_product_info | 1,084 |
| P0 | dwd_org_important_news_info | 913 |
| P0 | dwd_industry_chain_info | 527 |
| P1 | dwd_org_recruit_info | 2,000 |
| P1 | dwd_forg_base_info | 1,000 |
| P1 | dwd_forg_executive_info | 4,811 |

上市/财务/产业链标签约 **千～五千** 级样例，**远低于**供应方口头「国内机构 711 万」。

#### 表在但 0 行（24）— 结构就绪、数据未灌

含全部关键主路径：

- **主数据**：`dwd_org_base_info` / `shareholder_info` / `executive_info`
- **机构扩展**：`dwd_org_heis_info` / `dwd_research_institute_base_info`
- **港澳台**：`dwd_special_*_company` ×3
- **招投标出库**：`dwd_bid_*_out` ×4
- **风险子集**：abnormal / punish / illegal / tax / judicial / shixin / zhixing / bankruptcy* ×9
- **国外**：`dwd_forg_shareholder_info` / `product_info` 等
- **变更**：承诺名 `dwd_org_changerecord_info` = 0（见下命名差）

#### 表缺失（4）— P1 国外机构

| 承诺表 | 状态 |
|--------|------|
| dwd_forg_college_org_info | 不存在 |
| dwd_forg_university_org_info | 不存在 |
| dwd_forg_research_org_info | 不存在 |
| dwd_foreign_org_annual_financial_info | 不存在 |

### 2.4 命名 / 旁路发现（影响齐套判断）

| 承诺 / 预期 | live 实况 | 精确行数 |
|-------------|-----------|----------|
| dwd_org_base_info | 存在但空；旧名 `dwd_org_reg_info` 亦空 | 0 / 0 |
| dwd_org_heis_info | 存在空；旧名 `hels` 亦空 | 0 / 0 |
| dwd_org_changerecord_info | **空**；旁路 `dwd_org_change_record_info` | 0 / **1,676** |
| dwd_bid_*_out | 表在、全空；旧 `dwd_org_bid_info` 亦空 | 0 |
| （非承诺）dwd_org_annual_report_base | 有 **77 万**行 | 770,000 |
| （非承诺/排除）dwd_company* | 表在、全空 | 0 |
| （非承诺）dwd_forg_shareholder（无 `_info`） | 有数据 | 21,097 |

结论：供应方「711 万国内机构」**未落到**承诺主表或旧 `reg_info` / `company_base`；最接近的大体量企业相关表是 **`dwd_org_annual_report_base`（77 万）**，且不在 Wave A 40 清单内。

---

## 3. 对 Wave A / Mapping 的直接影响

| 动作 | 建议 |
|------|------|
| Wave A 烟测 | 可对 **有行** 的 P0（stock / financial / industry_tags / product / news / chain_info）先跑镜像 |
| Wave A P0 关单 | **不可** — 主表 `dwd_org_base_info` 仍为 0 |
| Wave B Mapping（`09`） | **暂缓 enterprise_base / extra 全量**；产业链与上市财务可小样试点，但缺主体键对齐 |
| 供应方核验清单 | 见 §5 |

`stock_base` 约 5,525 个 distinct `org_id`，`annual_financial` 约 5,352 — 有卫星数据，但 **无法挂到空的 base_info**。

---

## 4. 统计口径陷阱（给后续探测）

- **Navicat 表列表「行」列 = InnoDB 估算（`TABLE_ROWS` / `SHOW TABLE STATUS`），不是实时 `COUNT(*)`。**  
  例：`dwd_org_base_info` 列表显示 **11,954**，与 `information_schema.TABLE_ROWS` 一致；但只读账号 `gkx_reader_zp` 执行 `COUNT(*)` / `SELECT … LIMIT 3` 均为 **0**（2026-07-31 复核）。  
  对照：`dwd_org_stock_base` 估算 ~5561，精确 **5845**，且能查出样例行。  
- 多张表 **data_length > 0 且 COUNT=0**（如 `dwd_news_base`、港股/陆股日行情）— 勿用体积/列表「行」推断有业务行。  
- 齐套汇报请固定输出：**表是否存在 + `COUNT(*)` +（若有）`is_deleted=0` 子集**；Navicat 请**打开表浏览**或跑 `SELECT COUNT(*)` 再判。

---

## 5. 建议立刻向供应方确认的问题

1. 「国内机构 711 万 / 2500 万」落在哪些 **物理表名**？为何 `dwd_org_base_info` / `dwd_org_reg_info` / `dwd_company_base` 均为 0？  
2. `dwd_org_annual_report_base`（77 万）是否算机构落库进度的一部分？与 base_info 计划关系？  
3. 招投标是否应读 `dwd_bid_*_out`，还是尚未灌数？  
4. 变更表正式名是 `changerecord` 还是 `change_record`？  
5. 4 张缺失国外机构表的交付 ETA？  
6. `TABLE_ROWS` 与真实行数长期偏离，是否正在大批量 load / 未 analyze？

---

## 6. 判定摘要

| 问题 | 判定 |
|------|------|
| `dwd_*` 工作面是否已有大量数据？ | **部分有**（司法明细千万级、期权八百万、年报 77 万等），但分布不均 |
| 企业维承诺 40 表是否齐全？ | **结构基本齐，数据不齐**；主数据空；4 表缺失 |
| 可否按工作包 v1.3 推进贴源+Mapping？ | **可贴源烟测卫星表；不可宣称企业维齐套；Mapping 主体路径阻塞** |
