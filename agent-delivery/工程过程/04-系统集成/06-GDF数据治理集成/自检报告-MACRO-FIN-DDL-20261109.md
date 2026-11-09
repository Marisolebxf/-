# GDF 新派单包 DDL 签收自检报告（MACRO / FIN）

> **日期**：2026-11-09  
> **命令**：`python .cursor/skills/gkx-gdf-ddl-signoff/scripts/check_gdf_ddl.py --task GDF-MACRO-WORKPACK-L01` / `GDF-FIN-WORKPACK-L01`  
> **脚本**：已扩展维度 `macro` / `fin`（同日）  
> **结果**：**不通过**（exit 1）——符合预期缺口，非脚本误报  

## 1. MACRO（`GDF-MACRO-WORKPACK-v1`）

| 项 | 结果 |
|----|------|
| 派单包 | 识别到 7 张表 DDL（6×DWD `macro_*` + ADS `macro_city_section`） |
| `storage/MACRO/stores/mysql` | **不存在** → 全部「包有 md 无」 |
| 库核对 | 本机 `.env` **无** `GKX_LUMEN_MYSQL_PASSWORD` → 未连 demo/lumen |

表名：`macro_index_data` / `macro_index_attribute` / `macro_admin_area` / `macro_index_cal` / `macro_index_dur` / `macro_source_code` / `macro_city_section`。

**续作进度（同日）**：`GDF-MACRO-STORAGE-DDL-L01` 已入仓 `storage/MACRO/stores/mysql/`（7 表）；复检 **文件一致 7/7 绿**，仅「未设口令 / 库未核对」仍红。**不豁免 demo**：规约 §8 默认补建 `demo_gkxlumenx_*` + `gkxlumenx_*` 后再复检。

## 2. FIN（`GDF-FIN-WORKPACK-v1`）

| 项 | 结果 |
|----|------|
| 派单包 | 至少识别 ADS/DWD 草稿中的 CREATE（样例：`fin_corp_basic`、`ads_fin_industrial_fund_summary` 等） |
| `storage/FIN/stores/mysql` | **不存在** → 「包有 md 无」 |
| 库核对 | 同上，口令未设 |

**续作**：`GDF-FIN-STORAGE-DDL-L01`。

## 3. 与「成包已签收」关系

成包叶 `done` = **文档可投递**；DDL 签收自检绿 = **结构真源 + 现网一致**。二者分层：自检红不回滚成包签收，但 **GDF 建表 / SYSINT 跑通前必须先绿文件一致，再建表核库**。

## 4. CDC 预填（并行进度，非本自检范围）

- MACRO：`预填作业/` 已出，`SYSINT-06-05` in_progress  
- FIN：`预填作业/` 已出，`SYSINT-06-04` in_progress  
