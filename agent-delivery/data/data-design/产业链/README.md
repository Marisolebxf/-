# 产业链 data-design（legacy 目录）

> **现行存储 / 数据工程入口（唯一导航）**：  
> [`../storage/CHAIN/README.md`](../storage/CHAIN/README.md)  
> 规范：[`../storage/README.md`](../storage/README.md)  
> **S4**：`DATA-CHAIN-STORAGE-S4-L01`（2026-08-13）— 本目录**全部 md 已加文首横幅**；旧稿正文保留，**冲突时以 `storage/CHAIN` 为准**。

## 本目录文件角色

| 类别 | 文件 | 说明 |
|---|---|---|
| **DWD 细表真源**（stores 外链） | `产业链-DWD表设计-业务需求驱动(v5).md` | 入口先读 `storage/CHAIN/stores/mysql/dwd-chain.md` |
| **ADS 细表真源（现行）** | `产业链-ADS表设计-原型与Handoff驱动(v2).md` | 入口先读 `storage/CHAIN/stores/mysql/ads.md` |
| **ADS 对照稿** | `产业链-ADS表设计-业务需求驱动(v1).md` | **非**现行真源 |
| **旧域设计对照** | `产业链域数据库设计(v1).md` | 含历史 PG 叙述；**勿当真源** |
| **映射 / Step 分析** | `产业链-ODS到DWD*` · `ODS-DWD-字段对照*` · Step1 · `国内机构库-*` | 过程稿；导航走 storage |
| **Mapping 施工真源** | `产业链域-ETL-Mapping明细-源表到DWD.md` | GDF Wave B 字段全文；派单包 `GDF-CHAIN-WORKPACK-v1` |
| **决议 / 任务纪要** | `DEC-CHAIN-*` · `CHAIN-INST-*` | 产品/编码决议；不进 storage 树 |

> 另：handoff 旧稿 [`DATA-CHAIN-db-design.md`](../../agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md)（PG/`chain_*`）已同样加 S4 横幅，**勿当真源**。

## 三方 ODS

权威：`agent-delivery/data/third-party-source/doc/`（**优先读** `md-extract/` 产业链要素库）。  
Demo 落库：`demo_gkxlumenx_ods`（见 `storage/CHAIN` S2）。  
**不是**本目录，也不是 `gkx-mysql-raw` live as-built。
