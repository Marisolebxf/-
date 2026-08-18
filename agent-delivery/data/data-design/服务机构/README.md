# 服务机构 data-design（legacy 目录）

> **历史对照，非现行存储入口。**  
> `storage/SVC/` 已于 2026-08-18 按范围 3 停机删除（`DEMO-SVC-ABORT-L01`）。  
> 规范仍见 [`../storage/README.md`](../storage/README.md)（ENT / CHAIN）。  
> 重跑 A 后的新存储入口以新总控为准，**不要**把本目录当建表真源。

## 本目录文件角色

| 类别 | 文件 | 说明 |
|---|---|---|
| **旧域设计对照** | `服务机构域数据库设计(v1).md` | 历史 DWD/ADS 稿；**勿作 ODS/stores 建表真源** |
| **legacy 分析纪要** | `SVC-DATA-ANALYSIS-L01-数据分析报告.md` | **非**建表真源；开放项仍见 `客户决策清单跟踪表.md` §2.ae（含 Q-SVC-010） |
| **功能 / 产品** | （不在本目录） | E7 五件套见 `agent-handoffs/产品整体定义/E7-产业服务链分析/` |

## 三方 ODS

权威：`agent-delivery/data/third-party-source/doc/`（**优先读** `md-extract/` · **国内机构要素库**）。  
Demo 落库：`demo_gkxlumenx_ods`（与 ENT 同实例）。  
**不是**本目录，也不是 `gkx-mysql-raw` live as-built，也不是 L01 现网实查 DDL。
