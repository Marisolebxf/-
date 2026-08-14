# 产业链存储链路 · S1–S4 派单汇总



> **日期**：2026-08-12（**2026-08-13：明确李伟负责按在线文档建表**；**2026-08-14：淮政玮签收闭环**）  

> **派单人 / 签收人**：`human:淮政玮`  

> **监管 / 会签 / 建表 Owner**：`human:李伟`  

> **拆法**：与 ENT 对齐的 **4 单串行**  

> **状态**：**S1–S4 全部 `done`**



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

| S1 | `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01` | **done** | 骨架 + 流图会签 | ODS 真源=在线文档；流图 approved |

| S2 | `DATA-CHAIN-STORAGE-S2-L01` | **done** | sources/etl/seeds + 按 md-extract 建 ODS | 主建表单 · Owner 李伟 |

| S3 | `DATA-CHAIN-STORAGE-S3-L01` | **done** | stores 清单（draft） | DWD=v5 · ADS=v2；细表仍 draft |

| S4 | `DATA-CHAIN-STORAGE-S4-L01` | **done** | 旧路径 stub | 导航至 storage/CHAIN |



分册：同目录 `*-派单说明.md` / 各 task handoff。



---



## 顺序（已完成）



```text

S1 流图会签 → S2 在线文档对齐建 ODS 表（demo_*）→ S3 stores 清单 → S4 stub

```



参照：`storage/ENT/**` 同构；产业链 CSV：`md-extract/_csv/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表__产业链要素库.csv`

---

## 下一步（存储设计已闭环 → Demo 灌数）

| Task ID | 监管 | 说明 |
|---|---|---|
| `DEMO-CHAIN-UI-SEED-ODS-L01` | `human:淮政玮` | LLM/离线 → demo ODS → 模拟 GDF → DWD v5 → ADS v2；system-test 产业链灌数据。派单：[`DEMO-CHAIN-UI-SEED-ODS-L01-派单说明.md`](./DEMO-CHAIN-UI-SEED-ODS-L01-派单说明.md) |

