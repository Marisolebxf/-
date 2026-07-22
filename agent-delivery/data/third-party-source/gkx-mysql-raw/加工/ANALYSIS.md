# gkx MySQL 原始库 — 结构对照摘要

> **位置**：`gkx-mysql-raw/加工/`（加工侧）。入站源表清单见 [`../SOURCE-TABLES.md`](../SOURCE-TABLES.md)。


对照基线：`agent-delivery/data/third-party-source/gkx-mysql-raw/gkx_schema_ddl.sql（旧要素库SQL已删；现用三方DDL沙箱）`（约 192 张 CREATE）。  
本批沙箱：`gkx_schema_ddl.sql`（421 张，活跃 364）。

## 1. 规模

| 集合 | 表数 |
|------|------|
| 旧要素库 SQL（CREATE 去重） | 192 |
| 本批全量（含 bak） | 421 |
| 本批活跃（排除 `*_bak_*`） | 364 |
| 仅本批有、旧 SQL 无 | ~200 |
| 仅旧 SQL 有、本批无 | ~28 |

结论：三方当前交付显著大于旧「186/192 要素库」文档基线；后续映射应以**本批 DDL**为贴源真源，旧 SQL 作差异清单。

## 2. 域分布（活跃表，关键词命中，可重叠）

| 关键词 | 约计 |
|--------|------|
| `hycy`（海洋） | 70 |
| `org_`（机构） | 80 |
| `company` | 47 |
| `paper` | 44 |
| `patent` | 21 |
| `author` / `scholar` | 17 / 15 |
| `quantum` | 12 |
| `forg`（国外企业） | 10 |
| `drug` | 8 |
| `zck`（政策库） | 6 |
| `industry` | 15 |

另：医药/化学（clinical、substance、drug*）、金融序列（series_*）、关联表（`dwd_rel_*` / `ods_rel_*`）等。

## 3. 相对旧基线的典型增量（节选）

- 人才关联：`dwd_author_*_rel`、`dwd_author_info`、Scopus/爱思唯尔 `dwd_en_paper_info` / `dwd_en_paper_cited_by`
- 国外企业：`dwd_forg_*` 一批（命名与旧 `dwd_forg_*_info` 有差异）
- 海洋：观测/预报/遥感等（旧拼音长表名 → 本批多为 `dwd_hycy_marine_*`）
- 机构关联：`dwd_org_base_info_*_rel`
- 大量 `ods_*` 贴源镜像（旧 SQL 以 `dwd_*` 为主）

## 4. 仅旧基线有、本批未见（节选，需供应方确认是否更名/下线）

- `dwd_en_project` / `dwd_en_project_output` / `dwd_en_report`（本批多在 `ods_en_*`）
- `dwd_document_metadata`、`dwd_innovation_carrier`
- 旧拼音海洋/量子表名（如 `dwd_hai_yang_*`、`dwd_liang_zi_*`）→ 疑似已英文化改名
- 部分 `dwd_forg_*` 旧名（如 `act_contro_info`、`stock_fin_info`）

## 5. 命名风险（分析时注意）

1. **供应方 `dwd_*` ≠ 项目自建 DWD**：映射文档里应标 `source_layer: vendor_gkx_dwd` / 目标层为项目自建 DWD/ADS。入站正式工作面 = **`dwd_*`**；`ods_*` 不对项目正式暴露（见 `SUPPLIER-WORK-CONSTRAINTS.md`，2026-07-17）。
2. **同名异构**：`dwd_company`（药企）vs `dwd_company_base`（工商）；`dwd_job` vs `dwd_company_recruit`。
3. **bak 表**：`*_bak_20260710` 勿进映射主路径。
4. **重复语义**：如 `dwd_org_base_info_financing_meta_rel` 与 `..._metadata_rel` 并存，需字段级确认。
5. **六技术字段**（2026-07-17）：`created_time` / `updated_time` / `creater` / `updater` / `table_data_source` / `is_deleted` — 非业务口径；取数默认 `is_deleted=0`。旧基线 SQL 可能缺失这些列。
6. **业务字段未定稿**：映射状态保留 🟡；缺表交供应方核验，勿自行认定下线。

## 6. 对任务 `E-PLATFORM-P1-L01` 的含义

- `blocked_by`「三方原始表结构未确定」→ **结构 DDL 已落盘本沙箱**，可解阻塞「有没有表结构」这一环。
- 仍未完成：字段映射（**仅 `dwd_*`**）、写入数据工厂、缺表核验回写。  
- **未改** `task-registry.yaml`（认领门禁需监管人确认后再动）。
- 连接：可公网直连，见 `CONNECTION.md` + `.env.local`。