# 政策域 ETL Mapping 明细 — 源表到 DWD

> **版本**：v1.0  
> **日期**：2026-09-01  
> **范围**：GDF 三方政策表 → 项目 DWD（`gkxlumenx_dwd.policy_base_info`）字段级映射  
> **配套**：`storage/POLICY/sources/ods-ddl.md`（贴源结构）· 本包 `10/`（产线目标列）  
> **目标库**：`gkxlumenx_dwd`（MySQL）  
> **交付对象**：GDF 三方 ETL 团队  
> **GDF 派单包**：`data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/`  
> **升格自**：`storage/POLICY/etl/ods-to-dwd-mapping.md`（仍 draft；**施工只认本文件**）

---

## 0. 本期边界

| 需要的项目 DWD | 本包是否洗 | 说明 |
|---|---|---|
| `policy_base_info` | **洗** | 国内 + 国际同表 |
| ADS `policy_*` | **不洗** | 本包不做 |
| ES 政策索引 | **不洗** | 本包不做 |
| Nebula `policy` 点/边 | **不洗** | 本包不做 |

禁止：指标 SQL 读供应方 `gkx.dwd_*`；把 Demo `demo_gkxlumenx_dwd.policy_base_info` as-built 列当产线全文；用 `dwd_zck_*` 或旧 v1 37 列当源。

---

## 1. 映射分类

| 类型 | 说明 |
|---|---|
| **直接** | 源列写入目标列（可截断/类型转换，禁止丢正文） |
| **派生** | 由平面/常量规则生成，不另找源列 |
| **不映射** | 源无列或禁止伪造；目标留 NULL |

### 1.1 主键

`policy_id` = ODS `id` **原文**。禁止哈希、禁止 `pol:` 前缀（那是图 VID）。`id` 空行丢弃。

### 1.2 平面与碰撞

| 源表 | `source_plane` |
|---|---|
| `dwd_policy_base` | `domestic` |
| `dwd_global_policy_base` | `global` |

生产 UK：**永远** `(source_plane, policy_id)`。  
同一平面内 `policy_id` 重复 → 后写覆盖并计数。  
跨平面 `id` 字符串相同 → **允许共存**（靠 `source_plane` 区分），**不是**同一条政策。  
`human:淮政玮` 2026-09-01 拍板方案 A：**永远分 UK**。禁止加 `gbl:` 或任何前缀改 `policy_id`。`OPEN-POLICY-MAP-01` **已关**。

### 1.3 过滤

读 ODS：`is_deleted = 0 AND IFNULL(is_history, 0) = 0`。  
写 DWD：`is_deleted = 0`。

### 1.4 年份 / 状态 / 级别

- `publish_year` / 国际 `year`：**varchar/text 直拷**，禁止 `CAST AS SIGNED` 失败丢行。  
- 国内 `status`：只认源文案 **有效/失效**，禁止再映射 docstatus 20/30。  
- 国内 `rank`：国家级/省级/市级/区县级 **原文** 写入 `rank`；禁止压成 smallint `level`。

### 1.5 不再从 ODS 取（禁止假填）

旧 v1 / Demo as-built 有、新贴源无：`gis_location`、`sci_tech_attribute`、整型 `level`。需要则算法派生并标 OPEN，**禁止**用假坐标或假科技属性填。

---

## 2. 源表 → 目标表总览

### 2.1 直接映射

| # | 源表 | 目标表 | 说明 |
|---|---|---|---|
| 1 | `dwd_policy_base` | `policy_base_info` | 国内；`source_plane=domestic` |
| 2 | `dwd_global_policy_base` | `policy_base_info` | 国际；同表；`source_plane=global` |

### 2.2 关联映射

无。本期不 JOIN 企业/产业链表。

### 2.3 指标表

无。本包不写 ADS / 汇总表。

### 2.4 暂不映射

本期没有「只贴不洗」的政策源表。旧名 `dwd_zck_*` 已作废，不进 Wave A/B。禁止另建第二张政策主表。

---

## 3. 逐表字段

公共治理列（`etl_batch_id` / `ods_updated_time` / `is_deleted` / `created_time` / `updated_time`）按作业生成，下表不重复。过滤见 §1.3。

### 3.1 `dwd_policy_base` → `policy_base_info`

**行过滤**：`is_deleted = 0 AND IFNULL(is_history, 0) = 0`。  
**派生**：`source_plane` = `domestic`。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `id` | `policy_id` | 直接 | 原文；空行丢弃 |
| `title` | `title` | 直接 | 源 varchar(500) |
| `publish_code` | `issued_number` | 直接 | |
| `ministry` | `publish_organization` | 直接 | |
| `publish_date` | `publish_date` | 直接 | |
| `publish_year` | `publish_year` | 直接 | varchar(4) 原文，禁止 INT 硬转丢行 |
| `implementation_date` | `implementation_date` | 直接 | |
| `expire_date` | `expire_date` | 直接 | |
| `status` | `status` | 直接 | 有效/失效原文 |
| `rank` | `rank` | 直接 | 国家级/省级/市级/区县级原文 |
| `type` | `policy_type` | 直接 | 展示类别原文；QPOL-01 码化留给 ADS |
| `province` | `province` | 直接 | 禁止丢区/市 |
| `city` | `city` | 直接 | |
| `district` | `district` | 直接 | |
| `abstract` | `abstract` | 直接 | |
| `keywords` | `keywords` | 直接 | text，勿截断 |
| `content` | `content` | 直接 | longtext，禁止截断 |
| `link` | `url` | 直接 | |
| `quote_policy` | `pedigree` | 直接 | 引用原文 |
| `theme` | `theme` | 直接 | |
| `keypoints` | `keypoints` | 直接 | 源 varchar(1000) |
| `policy_support` | `policy_support` | 直接 | JSON 原样 |
| `source` | `source` | 直接 | |
| `appendix_name` | `appendix_name` | 直接 | 勿与 link 合成单 TEXT |
| `appendix_link` | `appendix_link` | 直接 | |
| — | `source_plane` | 派生 | 常量 `domestic` |
| — | `gis_location` | 不映射 | 源无；禁止假坐标 |
| — | `sci_tech_attribute` | 不映射 | 源无 |

**UK**：`(source_plane, policy_id)` Upsert。

国内行国际专有列（`disclosure_date` / `country` / `geo_region` / `language` / `doc_type` 等）保持 NULL。

### 3.2 `dwd_global_policy_base` → `policy_base_info`

**行过滤**：`is_deleted = 0 AND IFNULL(is_history, 0) = 0`。  
**派生**：`source_plane` = `global`。  
国际源无 `rank` / `type` / `status` / `expire_date` / `province|city|district`：对应列 NULL，禁止用国内码回填。

| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |
|---|---|---|---|
| `id` | `policy_id` | 直接 | 与国内同一字符串空间；靠 source_plane 区分 |
| `title` | `title` | 直接 | 源为 text |
| `abstract` | `abstract` | 直接 | |
| `organ` | `publish_organization` | 直接 | 必填；空则 drop 并计数 |
| `year` | `publish_year` | 直接 | text 原文，勿当年 INT |
| `publish_date` | `publish_date` | 直接 | 必填；空则 drop 并计数 |
| `disclosure_date` | `disclosure_date` | 直接 | 国际专有 |
| `category` | `policy_type` | 直接 | 领域原文；禁止混进国内 type 码表 |
| `topic` | `topic` | 直接 | 专题；与 category 分列 |
| `content` | `content` | 直接 | 禁止截断 |
| `region` | `region` | 直接 | 海外实施区域 |
| `country` | `country` | 直接 | |
| `geo_region` | `geo_region` | 直接 | |
| `link` | `url` | 直接 | |
| `language` | `language` | 直接 | |
| `source` | `source` | 直接 | |
| `theme` | `theme` | 直接 | |
| `appendix_name` | `appendix_name` | 直接 | |
| `appendix_link` | `appendix_link` | 直接 | |
| `report_number` | `report_number` | 直接 | |
| `project_id` | `project_id` | 直接 | |
| `security_class` | `security_class` | 直接 | |
| `version_type` | `version_type` | 直接 | |
| `volume_no` | `volume_no` | 直接 | |
| `doc_type` | `doc_type` | 直接 | |
| — | `source_plane` | 派生 | 常量 `global` |
| — | `rank` | 不映射 | 国际源无此列 |
| — | `status` | 不映射 | 国际源无此列 |
| — | `expire_date` | 不映射 | 国际源无此列 |
| — | `province` | 不映射 | 用 country/region |
| — | `city` | 不映射 | |
| — | `district` | 不映射 | |

**UK**：`(source_plane, policy_id)` Upsert。

---

## 4. ETL 顺序

```text
1. Wave A 贴源（两张 P0 wash）
2. 按 10 建/改 policy_base_info
3. POLICY-B1-DOMESTIC
4. POLICY-B2-GLOBAL（可与 B1 并行，须共用 UK）
5. 禁止写 ADS / ES / Nebula
```

增量建议：源 `updated_time`（空则 `created_time`）水位；删除跟 `is_deleted=1` 或历史翻转为软删 DWD。具体 CDC 参数由产线回签。

---

## 5. 抽样与诚实

每平面 ≥20 条：`policy_id`、`source_plane`、`title`、`publish_organization`、`content` 长度与源一致。  
输出 drop 计数：空 `id`、国际空 `organ`/`publish_date`。

---

## 6. 开放项

| ID | 项 | 状态 |
|---|---|---|
| OPEN-POLICY-MAP-01 | 跨平面 `id` 是否永远分 UK | **已关**（2026-09-01 `human:淮政玮`：方案 A 永远分 UK；禁止 `gbl:` 改键） |
| OPEN-POLICY-MAP-02 | QPOL-01 类别码表 | 本包 `policy_type` 原文；码化留给 ADS |
| OPEN-POLICY-FLOW-01 | 正式 DAG 名 | 产线回写 |
| OPEN-POLICY-DIM-01 | `dim.region` 维表 | 本包写 `province/city/district` 原文，不建维表 |

Demo as-built 用 `ext1` 承载类型、`region` 拼串：产线 **不**再写这两列当正名。
