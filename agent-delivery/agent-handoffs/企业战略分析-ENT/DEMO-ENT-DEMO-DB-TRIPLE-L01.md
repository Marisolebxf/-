# DEMO-ENT-DEMO-DB-TRIPLE-L01 · 执行记录（库已建）

> **日期**：2026-08-13  
> **执行**：`human:淮政玮`（超管建库）  
> **监管**：`human:徐滕强`（后续灌数默认与 UI 切换签收）  
> **ponytail**：full  

## 已完成

1. `CREATE` + `GRANT`：`demo_gkxlumenx_ods` / `_dwd` / `_ads` → `gkxlumenx@%`  
2. DWD/ADS：**仅结构**自正式库 enterprise_* / tag_* 克隆（无生产行拷贝）  
3. ODS：按 `md-extract` **国内机构要素库 CSV** `load_schema_from_csv()` 重建 **33** 张表；字段与约定一致（`_demo_id` 为 Demo 技术主键）  
4. 离线样例写入 P0 子集（base/executive/news/financial/shareholder/stock_*）  
5. `conf/settings.yaml` + K8s `ENTAN_MYSQL_*_DB` 默认改为 `demo_*`；`innov/analysis` 去硬编码库名  

## 探测摘要

| 库 | 表数（约） |
|---|---|
| demo_gkxlumenx_ods | 33（md-extract） |
| demo_gkxlumenx_dwd | 48 |
| demo_gkxlumenx_ads | 7 |

应用默认：`ods/dwd/ads` = 三件套 demo_*。

## 未做（可交腾强）

- system-test「灌数据」主路径切到 demo_*（`DEMO-ENT-UI-SEED-ODS-L01`）  
- Nebula / MinIO demo 前缀  
- 密码：**未**写入 git；日常用 `gkxlumenx`
