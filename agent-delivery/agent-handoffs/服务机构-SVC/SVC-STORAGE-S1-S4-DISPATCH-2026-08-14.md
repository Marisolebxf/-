# 服务机构存储链路 · S1–S4 派单汇总

> **日期**：2026-08-14  
> **派单人**：`human:淮政玮`  
> **拆法**：与 ENT / CHAIN 对齐的 **4 单串行**  
> **状态**：四单 **本地闭环** · S1 流图 approved · S2/S3 本地签收 · **S4 stub 已交（2026-08-17 · 未 push）** · 远端 registry 拉码后可能无本串任务（需另挂）  
> **会签 / 建表 Owner**：`human:侯佳伟`  
> **产品输入**：E7 五件套已交付，**本链路不重跑产品定义**  
> **旧稿**：`SVC-DATA-ANALYSIS-L01` = legacy 分析纪要，**非** ODS / stores 真源

---

## 核心要求

服务机构补 `storage/SVC/`，同构企业维 / 产业链维。表名 / 字段名必须与三方**在线约定文档**对齐：

| 项 | 值 |
|---|---|
| 权威 | `agent-delivery/data/third-party-source/doc/`（xlsx） |
| **优先读** | `doc/md-extract/`（**国内机构要素库**） |
| 日常建表 CSV | `doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内机构要素库.csv` |
| 禁止 | 以 `gkx-mysql-raw` as-built、L01 现网实查、或未对齐 doc 的草稿当建表真源 |
| 落库实例 | Demo：`demo_gkxlumenx_ods`（及后续 DWD/ADS 按流图）；**不要**写正式 `gkxlumenx_*` |
| 与 ENT 边界 | **不复制** `dwd_org_base_info`；机构主体权威在 ENT；本域只保留圈定规则、关系、本域 ADS/ES/图谱切片 |
| 准入 | **Q-SVC-010**（阻断级）写入 `OPEN-SVC-FLOW-*`，S1 **不伪闭合**；Demo 临时规则须标待核验 |

S1 定拓扑与会签；**S2 起必须按 md-extract 在 `demo_gkxlumenx_ods` 核对/补齐**（复用 ENT 已建国内机构表，禁止再建一套主表；缺 `industry*` 等文档列则按文档补列）；S3 再灌项目 stores 清单。

---

## 任务一览

| 序 | Task ID | 状态 | 角色 | 标题 |
|---|---|---|---|---|
| S1 | `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` | **ready_to_sign**（流图 approved · 待淮政玮签收） | architect-agent | 骨架 + 流图会签 |
| S2 | `DATA-SVC-STORAGE-S2-L01` | **本地签收 approved**（侯佳伟 · 未 push） | data-agent | sources/etl/seeds + Demo ODS 核对差集 0 |
| S3 | `DATA-SVC-STORAGE-S3-L01` | **本地签收**（放行 S4） | data-agent | stores 清单（draft） |
| S4 | `DATA-SVC-STORAGE-S4-L01` | **本地 stub 已交**（2026-08-17） | data-agent | 旧路径 stub |

分册：同目录 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01-派单说明.md` · `DATA-SVC-STORAGE-S2-L01-派单说明.md` · `DATA-SVC-STORAGE-S3-L01-派单说明.md` · `DATA-SVC-STORAGE-S4-L01-派单说明.md`。

---

## 顺序

```text
S1 流图会签 → S2 在线文档核对/补齐 Demo ODS（复用 ENT，禁止第二套主表）→ S3 stores 清单 → S4 stub
```

参照：`storage/ENT/**` · `storage/CHAIN/**`。  
S1 通过前 S2 不得开工。METRIC-OPEN 可与 S2 后并行，不挡 S1。

---

## 本链路不做

- 重写 E7 USM / IA / Wireframe / TRACE
- 续写或把 L01 升为现行真源
- 替甲方拍板「谁算服务机构」（Q-SVC-010）
- S1 写 DDL；未会签把 `stores/*` 标 approved
- api / frontend 接线（等 S1 会签 + S3 契约面）

---

## 开放项（S1 必须带上，不得吞掉）

| ID | 来源 | S1 处理 |
|---|---|---|
| Q-SVC-010 | 客户决策清单 §2.ae · L01 v2.2 | `OPEN-SVC-FLOW-*` 阻断级；圈定层标待决策 |
| Q-SVC-009 | industry 承诺 vs 文档 | 对账备注；建表仍认 md-extract |
| Q-SVC-001 / 008 | 边界与六类标签 | 临时规则可 Demo，不进正式契约 |
| Q-SVCCHAIN-01～06 | E7 README | 指标/算法口径；METRIC-OPEN 另轨，流图只声明缺口 |

---

## 建单后

1. ~~S1 升 `ready`；S2–S4 `backlog`~~ **已建**  
2. ~~指定会签人并认领 S1~~ **`human:侯佳伟`**  
3. ~~开 architect 会话起草~~ **已起草**（`storage/SVC/` + handoff；`signoff_status=pending_human`）  
4. **下一步**：侯佳伟在 `01-data-flow.md` 签 `approved` 后，S2 升 ready 再认领  

对照产业链汇总：[`../产业链分析-CHAIN/CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md`](../产业链分析-CHAIN/CHAIN-STORAGE-S1-S4-DISPATCH-2026-08-12.md)
