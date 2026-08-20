# CHAIN-INST-DATA-ANALYSIS-L01 — 产业链和国内机构库数据源分析（收口索引）

> **现行存储入口（S4）**：[`../storage/CHAIN/README.md`](../storage/CHAIN/README.md)  
> 本稿是 **本任务 evidence 索引**，不是 stores 真源。ODS/DWD/ADS 导航与冲突裁决以 `storage/CHAIN` 为准。  
> 收口 handoff：[`../../../agent-handoffs/产业链分析-CHAIN/CHAIN-INST-DATA-ANALYSIS-L01.md`](../../../agent-handoffs/产业链分析-CHAIN/CHAIN-INST-DATA-ANALYSIS-L01.md)

> 任务 ID: CHAIN-INST-DATA-ANALYSIS-L01  
> Epic: E-CHAIN-PROTOTYPE  
> 责任人: [human:李伟]  
> 状态: **收口**（spike；待 `ready_to_sign`）  
> 初版: 2026-07-29 · 收口: 2026-08-20

---

## 1. 任务范围

只读分析产业链与国内机构库 ODS，输出映射报告，把目标 DWD 收到 v5，冻结 Q053=INB。不含接口实施与灌数验证。

## 2. 产出文件清单

### 2.1 产业链数据源分析（DoD-1）✅

| 文件 | 说明 |
|------|------|
| `产业链-ODS到DWD字段映射分析报告(v3).md` | 07-29 首轮；按当时 7 表 mock，作过程稿 |
| `ODS-DWD-字段对照与缺失明细.md` | 同期字段对照 |
| `产业链-ODS到DWD字段映射复核报告(Step2).md` | 08-06～08-11 按 v5 四主源复检 |

### 2.2 国内机构库数据源分析（DoD-2）✅

| 文件 | 说明 |
|------|------|
| `国内机构库-ODS到DWD字段映射分析报告.md` | 13 张机构 ODS；主体表空；创新载体可灌基础字段 |

### 2.3 数据模型与映射（DoD-3）✅

| 文件 | 说明 |
|------|------|
| `产业链-DWD表业务需求符合性分析(Step1).md` | 业务需求 → v5 十四表 |
| `产业链-DWD表设计-业务需求驱动(v5).md` | **DWD 目标结构真源**（stores 外链） |
| `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md` | INB 升格平台主键，已冻结 |

> `产业链域数据库设计(v1).md` 不再当目标结构。S4 后一律走 `storage/CHAIN`。

### 2.4 接口 / 验证（DoD-4 / DoD-5）⏭

本 spike 不做。接口与灌数验证转后续实现单 / `DEMO-CHAIN-SIM-PROCESS-L01`。

### 2.5 Handoff

| 文件 | 说明 |
|------|------|
| `agent-handoffs/产业链分析-CHAIN/CHAIN-INST-DATA-ANALYSIS-L01.md` | **2026-08-20 收口稿**（替代 07-29 阶段性稿） |

---

## 3. 收口后仍有效的结论

### 3.1 四主源（灌数分析范围）

`dwd_industry_chain_info` / `dwd_org_industry_tags` / `dwd_org_industry_product_tags` / `dwd_industry_chain_news_info`

目标 DWD 是 **v5 `industry_chain_*` 十四表**，不是 07-29 稿里的 7 张 `chain_*` mock。

### 3.2 编码

**Q053 🟢**：`chain_id` / `node_id` / L0 `industry_id` = INB 原文。国标只做对照表，不回写主键。

### 3.3 仍打开的数据缺口（不等本单）

| ID | 内容 | 状态 |
|----|------|------|
| Q054 | 投融资正式源 | 🔴 |
| Q055 | 机构主体表空 | 🔴 |

登记处：`客户决策清单跟踪表.md` §2.y。

### 3.4 不要在本单继续做的

- `CHAIN-DATA-L01` 三方会签  
- `CHAIN-DATA-L02` DWD vs demo  
- 生产 DDL approved、Java `/internal/*`、正式 ETL  

---

*evidence 索引 · [human:李伟] · 2026-08-20 收口*
