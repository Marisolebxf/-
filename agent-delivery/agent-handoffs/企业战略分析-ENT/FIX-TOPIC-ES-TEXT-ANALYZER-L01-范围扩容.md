# FIX-TOPIC-ES-TEXT-ANALYZER-L01 · 范围扩容（2026-08-11）

> 原任务仍在；本文件为 **mapping 冻结 + country_code + city_code** 扩容说明。  
> 决策人：human:徐滕强  
> 关联：`PY-ENT-REGION-SCOPE-G20-COUNTRY-L01`（含 L05 城市复活）/ KEYANALYSIS / RECOMMEND  
> 城市码口径：`agent-delivery/data/ddl/CITY-CODE-G20.md`

## 1. 扩容范围（与原 DoD 叠加）

| # | 项 | 说明 |
|---|-----|------|
| A | 原 analyzer | `main_prod` / `main_activities` / `description` 禁单字分词 + match_phrase（不变） |
| B | **新增 `country_code`** | 顶层 `keyword`，ISO 3166-1 **alpha-3**；禁止写入 `region_id` |
| B2 | **新增 `city_code`** | 顶层 `keyword`，海外 **UN/LOCODE** 五位（如 `JPTYO`）；国内空；禁止写入 `region_id` |
| C | **双字段策略冻结** | 见 §2；改 `gkx_enterprise_mappings.json` + 设计文档 **v3.7** 一次定稿 |
| D | 非范围 | 高筛 `enterprise_region` / `/meta/regions` **不动** |

## 2. 双字段策略（结构冻结）

| 现状 | 目标 | 典型字段 |
|------|------|----------|
| 仅 `keyword`，但又要分词检索 | `text` + `fields.keyword` | 视审计清单：如中文地址类需检索的字段 |
| 仅 `text`，但又要精确过滤/聚合/排序 | `text` + `fields.keyword` | `main_prod` / `main_activities` / `description` / `address` 等 |
| 仅精确过滤、无需全文 | 保持纯 `keyword` | `region_id`、`country_code`、`city_code`、`social_credit_code`、`tags_flat` 等 |

执行要求：
1. 以现网 `conf/es/gkx_enterprise_mappings.json` 为底稿出 **差集清单** 写入 handoff  
2. 与 `企业搜索-ES索引设计.md` **v3.7** 对齐后一次性改 mapping  
3. 重建 playbook 仍遵循：现网不强制 recreate；下次 init/recreate 生效  

## 3. 灌数口径

| 字段 | 企业来源 | 值 |
|------|----------|-----|
| `country_code` | 国内主库 | 可空（推荐）或统一 `CHN` |
| `country_code` | forg | alpha-2 → `code_country.alpha2` → alpha-3 |
| `city_code` | 国内主库 | **空**（用 `region_id`） |
| `city_code` | forg | 城市名 → `dim.city.city_code`（UN/LOCODE）；未映射则空 |

DWD/设计：
- `企业搜索-ES索引设计.md` v3.7  
- `DWD表结构设计-企业模块-MySQL-v3.0.md` §4.13  
- DIM：`CITY-CODE-G20.md` + L04/L05

## 4. 解锁下游

本单 mapping +（至少）索引模板/下次 recreate 就绪后：
- `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01`（应同时支持 `city_codes` OR）
- `PY-ENT-RECOMMEND-GEO-COUNTRY-L01`（geographicSources 可含 UN/LOCODE）
