# 服务机构 data-design（legacy 目录）

> **现行存储 / 数据工程入口（唯一导航）**：  
> [`../storage/SVC/README.md`](../storage/SVC/README.md)  
> 规范：[`../storage/README.md`](../storage/README.md)  
> **S4**：`DATA-SVC-STORAGE-S4-L01`（2026-08-17 · **本地**）— 本目录旧稿保留，**冲突时以 `storage/SVC` 为准**；**不 commit / 不 push**（Owner 指示）。

## 本目录文件角色

| 类别 | 文件 | 说明 |
|---|---|---|
| **旧域设计对照** | `服务机构域数据库设计(v1).md` | 历史 DWD/ADS 稿；**勿作 ODS/stores 建表真源**；入口先读 `storage/SVC/stores/` |
| **legacy 分析纪要** | `SVC-DATA-ANALYSIS-L01-数据分析报告.md` | **非**建表真源；开放项仍见 `客户决策清单跟踪表.md` §2.ae（含 Q-SVC-010） |
| **功能 / 产品** | （不在本目录） | E7 五件套见 `agent-handoffs/产品整体定义/E7-产业服务链分析/` |

## 三方 ODS

权威：`agent-delivery/data/third-party-source/doc/`（**优先读** `md-extract/` · **国内机构要素库**）。  
Demo 落库：`demo_gkxlumenx_ods`（与 ENT 同实例；见 `storage/SVC` S2）。  
**不是**本目录，也不是 `gkx-mysql-raw` live as-built，也不是 L01 现网实查 DDL。

## 读序（强制）

1. [`../storage/SVC/00-context.md`](../storage/SVC/00-context.md)  
2. [`../storage/SVC/01-data-flow.md`](../storage/SVC/01-data-flow.md)（approved）  
3. [`../storage/SVC/sources/inventory.md`](../storage/SVC/sources/inventory.md)  
4. [`../storage/SVC/stores/`](../storage/SVC/stores/)（S3 draft 清单）  
5. 本目录旧稿仅对照 / 开放项备忘  
