# 宏观行业域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v1.0（2026-11-09）。  
> **范围**：GDF 三方宏观行业要素库六表 → 项目 DWD（`gkxlumenx_dwd` 六张 `macro_*`）字段级映射  
> **配套**：三方源行数报告 `GKX数据源表及行数报告-20261109-1026.MD`（宏观行业要素库）· 本包 `10/`（目标列）· 本包 `04`（区划反解 / 过滤）  
> **目标库**：`gkxlumenx_dwd`（MySQL）  
> **交付对象**：GDF 三方 ETL 团队  
> **GDF 派单包**：`data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/`  
> **来源**：本文件新写。无 `storage/MACRO/etl/` 草稿可升格；**施工只认本文件**。

---

## 0. 本期边界

| 需要的项目 DWD | 本包是否洗 | 说明 |
|---|---|---|
| `macro_index_data` | **洗** | 事实；加区划反解派生列 |
| `macro_index_attribute` / `macro_admin_area` / `macro_index_cal` / `macro_index_dur` / `macro_source_code` | **洗** | 五张维度，直接映射 |
| `gkxlumenx_ads.macro_city_section` | **不在 Wave B** | ②a，见 `12`。Wave B 不写 ADS |
| 行业分析六表、金融表 | **不洗** | 不在本包 |
| ES / Nebula / Milvus | **不洗** | 本包不做 |

禁止：指标 SQL 读供应方 `gkx.dwd_*`；把 Demo as-built 列当产线全文；用 Excel 的 `t_id` 建列；用供应方 `ods_*` 当源。

---

## 1. 映射分类

| 类型 | 说明 |
|---|---|
| **直接** | 源列写入目标列（可改名、做类型转换；禁止丢值、禁止改精度） |
| **派生** | 由规则生成，不另找源列（`area_resolve` 等） |
| **不映射** | 技术字段或源无列；目标不建列或留 NULL |

### 1.1 主键 / 唯一键

| 目标表 | UK |
|---|---|
| `macro_index_data` | `(index_code, occur_period, area_code, area_code_type, dim_cal, dim_dur)` |
| `macro_admin_area` | `cur_code` |
| `macro_index_attribute` | `index_code` |
| `macro_index_cal` | `dim_cal` |
| `macro_index_dur` | `dim_dur` |
| `macro_source_code` | `source_code` |

UK 冲突：后写覆盖并**计数**，计数回传。禁止改键。事实表业务键任一列为空 → 丢弃并计数（实测 2026-11-09 为 0 行）。

### 1.2 过滤

读 ODS：**无行过滤**。不要加 `is_deleted = 0`。  
写 DWD：`is_deleted` 取源列原值，禁止写成常量 `0`。应用读 DWD 时自行加 `is_deleted = 0`。

### 1.3 公共治理列（按作业生成，下表不重复）

| DWD 列 | 来源 |
|---|---|
| `etl_batch_id` | 作业批次号 |
| `ods_updated_time` | ODS `updated_time`（供应方技术字段，增量水位） |
| `created_time` / `updated_time` | DWD 自己的写入 / 更新时间，作业生成 |

### 1.4 不映射的供应方技术字段（六表一致）

`dwd_id`（供应方物理主键）、`creater`、`updater`、`table_data_source`、`operator_remarks`、`insert_remark`、ODS 的 `created_time`：只留在 ODS，不进 DWD。`dwd_id` 不进 DWD 是因为它是供应方内部自增键、不是业务键。

### 1.5 类型

按 live（`SHOW CREATE TABLE`）取，不按 Excel：`index_value` 保持 `decimal(38,8)`；`occur_period` 保持 `int`（YYYYMM）；`occur_period_t` 保持 `varchar(20)` 原文（实测形如 `2018-06-01`，不做日期换算）；区划类列 `varchar`，禁止转 `int`（前导零 `0086` 会丢）。

---

## 2. 源表 → 目标表总览

### 2.1 直接映射

| # | 源表 | 目标表 | 说明 |
|---|---|---|---|
| 1 | `dwd_dim_index_cal` | `macro_index_cal` | 维度；3 行 |
| 2 | `dwd_dim_index_dur` | `macro_index_dur` | 维度；7 行 |
| 3 | `dwd_dim_source_code` | `macro_source_code` | 维度；4 行 |
| 4 | `dwd_dim_index_attribute` | `macro_index_attribute` | 维度；867 行 |
| 5 | `dwd_dim_admin_area` | `macro_admin_area` | 维度；20,000 行 |
| 6 | `dwd_macro_index_data` | `macro_index_data` | 事实；20,000 行；**加区划反解派生列** |

### 2.2 关联映射

仅一处：Wave B 事实表派生列 `area_resolve` / `city_code` / `city_name` / `province_code` 要查区划维度（`macro_admin_area`，所以**区划维度必须先洗完**）。其余维度表与事实表之间**不做物理 JOIN 写入**，事实表保留代码，由使用方按代码 join。不 JOIN 企业 / 产业链 / 政策表。

### 2.3 指标表

无。Wave B 不写 ADS / 汇总表。城市截面见 `12`。

### 2.4 暂不映射

本期没有「只贴不洗」的宏观源表。行业分析六表、金融表不属于本包。

---

## 3. 逐表字段

### 3.1 `dwd_macro_index_data` → `macro_index_data`

**行过滤**：无。  
**源列（live 24 列，无 `t_id`）**：`dwd_id`、`index_code`、`occur_period`、`area_code`、`dim_cal`、`dim_dur`、`rid`、`occur_period_t`、`occur_period_year`、`occur_period_month`、`index_value`、`unit_use`、`label`、`update_time`、`source_code`、`area_code_type`、`created_time`、`updated_time`、`creater`、`updater`、`table_data_source`、`operator_remarks`、`is_deleted`、`insert_remark`。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `index_code` | `index_code` | 直接 | `varchar(50)`；空行丢弃并计数 |
| `occur_period` | `occur_period` | 直接 | `int`，YYYYMM |
| `area_code` | `area_code` | 直接 | `varchar(32)` 原文；禁止补零 / 截断 / 转 int |
| `area_code_type` | `area_code_type` | 直接 | `1` 行政区；实测另有 `3`、`4`（含义待澄清）。原样，不过滤 |
| `dim_cal` | `dim_cal` | 直接 | 代码（`TB` / `JDZ` / `HB`），不是名称 |
| `dim_dur` | `dim_dur` | 直接 | 代码（`DNLJ` / `QM` / `DY` / `DJ` …） |
| `index_value` | `index_value` | 直接 | `decimal(38,8)` 原样；NULL 原样 |
| `unit_use` | `unit_use` | 直接 | **该行真实单位**（`元` / `%` …）。不要用属性表 `unit_use` 覆盖 |
| `rid` | `src_rid` | 直接 | 供应方行 ID，追溯用 |
| `occur_period_t` | `occur_period_t` | 直接 | 原文 `varchar(20)` |
| `occur_period_year` | `occur_period_year` | 直接 | |
| `occur_period_month` | `occur_period_month` | 直接 | |
| `label` | `label` | 直接 | 1 宏观 / 2 中观；实测全为 1，原样 |
| `source_code` | `source_code` | 直接 | 来源代码（`LBS` / `NATIONALSTAT` / `GACC` / `worldbank`） |
| `update_time` | `src_update_time` | 直接 | 供应方业务「数据更新时间」 |
| `is_deleted` | `is_deleted` | 直接 | 原样，取数不过滤 |
| `updated_time` | `ods_updated_time` | 直接 | 增量水位 |
| — | `area_resolve` | **派生** | 见 §3.1.1；取值 `city_by_city_code` / `municipality_by_province_code` / `district_by_area_code` / `unresolved` |
| — | `city_code` | **派生** | 见 §3.1.1；`unresolved` 时 NULL |
| — | `city_name` | **派生** | 同上 |
| — | `province_code` | **派生** | 同上 |
| `dwd_id` / `creater` / `updater` / `table_data_source` / `operator_remarks` / `insert_remark` / ODS `created_time` | — | 不映射 | 见 §1.4 |

#### 3.1.1 区划反解派生（规则真源 `04` §3.2；本节给 SQL 形态）

前置：`macro_admin_area` 已洗完。查表只用 `is_deleted = 0` 的行。

```sql
-- 目标库 gkxlumenx_dwd；对 macro_index_data 每行（含已删除行）补 4 个派生列
WITH
city AS (SELECT city_code AS k, MIN(city_name) AS city_name, MIN(province_code) AS province_code
         FROM macro_admin_area WHERE is_deleted = 0 AND city_code IS NOT NULL GROUP BY city_code),
muni AS (SELECT province_code AS k, MIN(city_code) AS city_code, MIN(city_name) AS city_name
         FROM macro_admin_area WHERE is_deleted = 0 AND province_code IN ('11','12','31','50') GROUP BY province_code),
dist AS (SELECT area_code AS k, MIN(city_code) AS city_code, MIN(city_name) AS city_name, MIN(province_code) AS province_code
         FROM macro_admin_area WHERE is_deleted = 0 AND area_code IS NOT NULL GROUP BY area_code)
SELECT f.*,
  CASE WHEN CHAR_LENGTH(f.area_code)=12 AND c.k IS NOT NULL THEN 'city_by_city_code'
       WHEN f.area_code IN ('11','12','31','50') AND m.k IS NOT NULL THEN 'municipality_by_province_code'
       WHEN CHAR_LENGTH(f.area_code)=12 AND d.k IS NOT NULL THEN 'district_by_area_code'
       ELSE 'unresolved' END                                                   AS area_resolve,
  CASE WHEN CHAR_LENGTH(f.area_code)=12 AND c.k IS NOT NULL THEN c.k
       WHEN f.area_code IN ('11','12','31','50') AND m.k IS NOT NULL THEN m.city_code
       WHEN CHAR_LENGTH(f.area_code)=12 AND d.k IS NOT NULL THEN d.city_code END AS city_code,
  CASE WHEN CHAR_LENGTH(f.area_code)=12 AND c.k IS NOT NULL THEN c.city_name
       WHEN f.area_code IN ('11','12','31','50') AND m.k IS NOT NULL THEN m.city_name
       WHEN CHAR_LENGTH(f.area_code)=12 AND d.k IS NOT NULL THEN d.city_name END AS city_name,
  CASE WHEN CHAR_LENGTH(f.area_code)=12 AND c.k IS NOT NULL THEN c.province_code
       WHEN f.area_code IN ('11','12','31','50') AND m.k IS NOT NULL THEN f.area_code
       WHEN CHAR_LENGTH(f.area_code)=12 AND d.k IS NOT NULL THEN d.province_code END AS province_code
FROM <ODS 事实表行集合 f>
LEFT JOIN city c ON c.k = f.area_code
LEFT JOIN muni m ON m.k = f.area_code
LEFT JOIN dist d ON d.k = f.area_code;
```

GDF 可用任何等价实现（映射节点 + 查找表、SQL 节点均可），**行为必须等价**：规则顺序、`is_deleted=0` 查表、不改 `area_code`、不依赖 `area_code_type`。区划维度重灌后，事实表派生列要重算（事实表体量小，直接全量重算）。回传需附 `04` §3.5 同口径的分布表。

### 3.2 `dwd_dim_admin_area` → `macro_admin_area`

**行过滤**：无。  
**源列（live 29 列）**。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `cur_code` | `cur_code` | 直接 | UK；`varchar(50)`；空行丢弃并计数 |
| `cur_name` | `cur_name` | 直接 | |
| `parent_code` | `parent_code` | 直接 | |
| `country_code` | `country_code` | 直接 | `varchar`，禁止转 int（`0086`） |
| `country_name` | `country_name` | 直接 | |
| `province_code` | `province_code` | 直接 | |
| `province_name` | `province_name` | 直接 | |
| `city_code` | `city_code` | 直接 | 12 位国标码；允许 NULL |
| `city_name` | `city_name` | 直接 | |
| `area_code` | `area_code` | 直接 | **区县编码**（不是事实表 `area_code` 的同义列，见 `01` §3） |
| `area_name` | `area_name` | 直接 | |
| `street_code` | `street_code` | 直接 | |
| `street_name` | `street_name` | 直接 | |
| `community_code` | `community_code` | 直接 | |
| `community_name` | `community_name` | 直接 | |
| `cur_level` | `cur_level` | 直接 | 1 国家 / 2 省 / 3 市 / 4 区县 / 5 街道 / 6 社区 |
| `rid` | `src_rid` | 直接 | |
| `qh_base_id` | `qh_base_id` | 直接 | 供应方基础区域 ID |
| `source_code` | `source_code` | 直接 | |
| `update_time` | `src_update_time` | 直接 | |
| `is_deleted` | `is_deleted` | 直接 | 原样 |
| `updated_time` | `ods_updated_time` | 直接 | |
| `dwd_id` / 技术字段 | — | 不映射 | 见 §1.4 |

### 3.3 `dwd_dim_index_attribute` → `macro_index_attribute`

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `index_code` | `index_code` | 直接 | UK；空行丢弃并计数 |
| `index_name` | `index_name` | 直接 | |
| `unit_show` | `unit_show` | 直接 | 推荐展示单位，如 `元,千元,万元,亿元` |
| `unit_use` | `unit_use` | 直接 | **库存单位，恒为「元」。不是行单位**。目标列 COMMENT 必须写明 |
| `data_freq` | `data_freq` | 直接 | 月度 / 季度 / 年度 |
| `time_attr_tag` | `time_attr_tag` | 直接 | 允许 NULL |
| `create_time` | `src_create_time` | 直接 | 指标创建时间 |
| `rid` | `src_rid` | 直接 | |
| `is_deleted` | `is_deleted` | 直接 | 原样 |
| `updated_time` | `ods_updated_time` | 直接 | |
| `uid` | — | 不映射 | 编辑者 ID，单人运维恒为 NULL |
| `dwd_id` / 技术字段 | — | 不映射 | 见 §1.4 |

### 3.4 `dwd_dim_index_cal` → `macro_index_cal`

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `dim_cal` | `dim_cal` | 直接 | UK；代码（`HB` / `TB` / `JDZ`） |
| `dim_cal_name` | `dim_cal_name` | 直接 | |
| `dim_cal_desc` | `dim_cal_desc` | 直接 | |
| `create_time` | `src_create_time` | 直接 | |
| `rid` | `src_rid` | 直接 | |
| `is_deleted` | `is_deleted` | 直接 | 原样 |
| `updated_time` | `ods_updated_time` | 直接 | |

### 3.5 `dwd_dim_index_dur` → `macro_index_dur`

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `dim_dur` | `dim_dur` | 直接 | UK；代码（`QM` / `DJ` / `DNLJ` / `DY` / `ZC` / `LSLJ` / `NC`） |
| `dim_dur_name` | `dim_dur_name` | 直接 | |
| `dim_dur_desc` | `dim_dur_desc` | 直接 | |
| `create_time` | `src_create_time` | 直接 | |
| `rid` | `src_rid` | 直接 | |
| `is_deleted` | `is_deleted` | 直接 | 原样 |
| `updated_time` | `ods_updated_time` | 直接 | |

### 3.6 `dwd_dim_source_code` → `macro_source_code`

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `source_code` | `source_code` | 直接 | UK；代码（`GACC` / `worldbank` / `LBS` / `NATIONALSTAT`） |
| `source_name` | `source_name` | 直接 | |
| `create_time` | `src_create_time` | 直接 | |
| `rid` | `src_rid` | 直接 | |
| `is_deleted` | `is_deleted` | 直接 | 原样 |
| `updated_time` | `ods_updated_time` | 直接 | |

---

## 4. 顺序与重跑

1. 五张维度表（任意顺序）全量。  
2. 事实表：先落 §3.1 直接列，再按 §3.1.1 补派生列；或一步 SQL 写入。  
3. 区划维度任何一次重灌后，事实表派生列全量重算。  
4. 事实表首次全量；之后按 `ods_updated_time` 增量 upsert（UK 同 §1.1）。供应方补数后若出现新 `area_code`，增量写入时同样要走反解。  
5. 删除：`is_deleted=1` 的行**原样写入**（不物理删除），应用侧过滤。  
6. 重跑：幂等（UK upsert）。

## 5. 校验（Wave B 回传须附）

| # | 校验 | 期望 |
|---|---|---|
| 1 | 每表 ODS 行数 = DWD 行数（扣除空键丢弃数、UK 冲突覆盖数后，计数须对得上） | 小维度表精确相等 |
| 2 | 事实表 UK 冲突计数 | 实测基线 0 |
| 3 | 事实表空业务键丢弃数 | 实测基线 0 |
| 4 | 事实表 `area_resolve` × `area_code_type` 分布 | 与 `04` §3.5 基线同结构：`city_by_city_code` / `municipality_by_province_code` / `district_by_area_code` / `unresolved` 都出现；四城命中预期类。行数不要求等于基线 |
| 5 | 四个政策城市 `area_code_type=1` 事实行数 > 0（深圳 / 广州 / 北京 / 上海） | `04` §3.4 |
| 6 | 事实表 `dim_cal` / `dim_dur` / `index_code` / `source_code` 孤儿数 | 0 |
| 7 | 抽样 ≥20 行事实 + 小维度表全量：`index_value` 无精度损失、`area_code` 原文一致 | 100% |
