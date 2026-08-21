# POLICY · ODS → 项目 DWD 字段对照（draft）

```yaml
---
doc_id: POLICY-ETL-ODS-TO-DWD
element: POLICY
role: etl
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: mysql
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> ODS DDL 真源：[`../sources/ods-ddl.md`](../sources/ods-ddl.md)。  
> 项目 DWD：`demo_gkxlumenx_dwd.policy_base_info`。旧 v1 37 列 **不得**当贴源。本叶不 APPLY。

读过滤：`is_deleted=0`；`is_history=0`（当前）。`id` 长度 ≤100，上图 VID `pol:{id}` 仍受 `vid_length=80` 约束——超长须截断策略另开（禁止静默碰撞）。

## 1. 国内 `dwd_policy_base` → `policy_base_info`

| ODS | 项目 DWD 建议列 | 规则 |
|---|---|---|
| `id` | `policy_id` | 主键；勿另造哈希 |
| `title` | `title` | 直拷；源 500 |
| `publish_code` | `issued_number` | 直拷 |
| `ministry` | `publish_organization` | 直拷 |
| `publish_date` | `publish_date` | 直拷 |
| `publish_year` | `publish_year` | **varchar(4)**，禁止当 INT 硬转失败丢行 |
| `implementation_date` | `implementation_date` | 直拷 |
| `expire_date` | `expire_date` | 直拷 |
| `status` | `status` | **有效/失效** 字符串；禁止再映射 docstatus 20/30 |
| `rank` | `level` 或 `rank` | **国家级/省级/市级/区县级** 原文；ADS 分层再码化 |
| `type` | `policy_type` | 展示类别/QPOL-01 主读此列 |
| `province` `city` `district` | 同名三列（推荐）或拼 `region` | 全景筛省市区；禁止丢区 |
| `abstract` `keywords` `content` | 同名 | `keywords` 源为 text |
| `link` | `url` | 直拷 |
| `quote_policy` | `pedigree` / 引用原文 | 图谱 `cite` 候选 |
| `theme` | `theme` | 拆解背景/指导思想 |
| `keypoints` | `keypoints` | 源 varchar(1000) |
| `policy_support` | `policy_support` **JSON** | 扶持对象/行为/方式/申报条件；图谱 `support`/`apply_to` |
| `source` | `source` | 直拷 |
| `appendix_name` `appendix_link` | 同名 | 勿合成单 TEXT 丢链接 |
| 技术列 | 同名保留或 ETL 审计 | `created_time` 等；`insert_remark` 不进业务口径 |

**不再从 ODS 取**（旧 v1 有、新表无）：`gis_location`、`sci_tech_attribute`、整型 `level`。需要则算法派生，标 OPEN，禁止用假坐标填。

## 2. 国际 `dwd_global_policy_base` → 同一张 `policy_base_info`

建议 `source_plane=global`（或等价列）区分国内行。无 `rank`/`type`/`status`/`expire_date`。

| ODS | 项目 DWD | 规则 |
|---|---|---|
| `id` | `policy_id` | 与国内同一键空间，碰撞则加前缀 `gbl:` 须书面定（OPEN） |
| `title` `abstract` `content` `link` `theme` | 同名 / `url` | `title` 源为 text |
| `organ` | `publish_organization` | 必填 |
| `year` | `publish_year` | text，勿当 year INT |
| `publish_date` | `publish_date` | 必填 |
| `disclosure_date` | `disclosure_date` | 国际专有 |
| `category` `topic` | `policy_type` / `topic` | 领域 vs 专题，禁止混进国内 `type` 码 |
| `region` `country` `geo_region` | 同名 | 海外全景筛 |
| `language` `report_number` `project_id` `security_class` `version_type` `volume_no` `doc_type` | 同名或 JSON `ext` | 不丢列 |
| `appendix_*` `source` | 同名 | |

## 3. 展示筛选用列（DS-10）

国内：`type` `ministry` `province/city/district` `rank` `status` `keywords` `title`。  
海外：`category` `country` `region` `organ` `year`。
