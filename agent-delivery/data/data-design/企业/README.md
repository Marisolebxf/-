# 企业 data-design（legacy 目录）

> **现行存储 / 数据工程入口（唯一导航）**：  
> [`../storage/ENT/README.md`](../storage/ENT/README.md)  
> 规范：[`../storage/README.md`](../storage/README.md)  
> **S4**：`DATA-ENT-STORAGE-S4-L01`（2026-08-12）— 本目录旧链接保留，冲突时以 `storage/ENT` 为准。

## 本目录还留什么

| 类别 | 文件 | 说明 |
|---|---|---|
| **as-built DDL 细表**（stores 外链真源） | `DWD表结构设计-企业*-MySQL-v3.*.md` | 正文保留；入口先读 `storage/ENT/stores/mysql/*` |
| **ES 设计细表** | `企业搜索-ES*.md` · `sample-enterprise-doc.json` | 入口先读 `storage/ENT/stores/elasticsearch/*` |
| **功能设计**（不进 storage） | `重点企业分析-功能设计.md` · `深圳企业现状分析-功能设计.md` | 产品侧；不迁入 storage 树 |
| **血缘 / 字典专项** | `dwd_enterprise_master.md` · `ENT-DICT-CATALOG-L01.md` | 另轨任务产物；存储导航仍走 storage |
| **已归档 stub** | PG 大稿 / 域设计 v1 / vs-demo / 详细设计 | 见 `_archive/2026-08/data-design-企业-legacy/` |

## 三方 ODS

权威：`agent-delivery/data/third-party-source/doc/`（**优先读** `md-extract/`）。  
**不是**本目录，也不是 `gkx-mysql-raw` live。
