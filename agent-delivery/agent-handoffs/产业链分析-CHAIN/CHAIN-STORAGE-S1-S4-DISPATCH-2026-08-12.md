# 产业链存储链路 · S1–S4 派单汇总

> **日期**：2026-08-12（**2026-08-13：明确李伟负责按在线文档建表**）  
> **派单人**：`human:淮政玮`  
> **监管 / 会签 / 建表 Owner**：`human:李伟`  
> **拆法**：与 ENT 对齐的 **4 单串行**  
> **状态**：S1 **ready_to_sign**（流图已会签）· S2 **claimed**（建表主单 · `human:李伟`）· S3–S4 **backlog**

---

## 核心要求（2026-08-13）

**李伟负责在 Demo 库中建表**，表名 / 字段名必须与三方**在线约定文档**对齐：

| 项 | 值 |
|---|---|
| 权威 | `agent-delivery/data/third-party-source/doc/`（xlsx） |
| **优先读** | `doc/md-extract/`（含 **产业链要素库** CSV/MD） |
| 禁止 | 以 `gkx-mysql-raw` as-built、或未对齐 doc 的草稿当建表真源 |
| 落库实例 | 开发用已有 **`demo_gkxlumenx_ods`**（及后续 DWD/ADS 按流图）；**不要**写正式 `gkxlumenx_*` |
| 授权账号 | `gkxlumenx`（四件套 demo 已授权） |

S1 定拓扑与会签；**S2 起必须交出可跑的 DDL/建表结果**（ODS 约定表优先）；S3 再灌项目 stores 清单。

---

## 任务一览

| 序 | Task ID | 状态 | 标题 | 建表相关 |
|---|---|---|---|---|
| S1 | `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` | **ready_to_sign** | 骨架 + 流图会签 | 在流图中写明 ODS 真源=在线文档；放行 S2 建表 |
| S2 | `DATA-CHAIN-STORAGE-S2-L01` | **claimed** | sources/etl/seeds + **按 md-extract 建 ODS 表** | **主建表单** · Owner 李伟 |
| S3 | `DATA-CHAIN-STORAGE-S3-L01` | backlog | stores 清单（draft） | 项目 DWD/ADS 等结构清单；可补 demo_dwd/ads 缺表 |
| S4 | `DATA-CHAIN-STORAGE-S4-L01` | backlog | 旧路径 stub | 不建表 |

分册：同目录 `*-派单说明.md`。

---

## 顺序

```text
S1 流图会签 → S2 在线文档对齐建 ODS 表（demo_*）→ S3 stores 清单 → S4 stub
```

参照：`storage/ENT/**` 同构；ENT 已示范 `entan/llm_ods` 从 md-extract CSV 建表。  
产业链 CSV：`md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__产业链要素库.csv`

---

## 微信知会要点

先认领 S1；S2 起你本人（或你监管的 agent）**按 md-extract 在 demo_gkxlumenx_ods 建产业链相关表**。
