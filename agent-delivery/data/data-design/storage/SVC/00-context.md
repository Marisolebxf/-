# 服务机构维存储 · 上下文与铁律

```yaml
---
doc_id: SVC-STORAGE-CONTEXT
element: SVC
role: context
status: draft
version: "2026-08-14"
updated: 2026-08-14
signoff_owner: human:侯佳伟
---
```

## 1. Data Product 边界

- **域**：服务机构维（SVC / 科技专题 · 产业服务链分析相关存储；产品输入 = E7 五件套，**本树不重跑产品定义**）
- **内**：
  - 本域对三方 ODS 的**依赖清单**（查阅入口，不复制机构主表）
  - 服务机构**圈定规则**及其结果表（项目 DWD；规则本身待 Q-SVC-010）
  - 服务机构**关系**（服务链环节、机构↔环节、机构↔机构等；落本域 DWD / Nebula 切片）
  - 本域 ADS / ES / 图谱切片、本域 MinIO 对象前缀
- **外**（禁止写入本树正文）：
  - 功能设计、UI、USM / IA / Wireframe（见 `agent-handoffs/产品整体定义/E7-产业服务链分析/`）
  - 指标口径正文（见 `metrics/` + `data-lineage-policy.md`；流图只声明缺口）
  - **机构主体完整属性**：权威在 **ENT**（`dwd_org_base_info` 及国内机构要素库主表）

## 2. 与 ENT 的主数据边界（硬约束）

| 项 | 约定 |
|---|---|
| 机构主体权威 | **ENT**。供应方命名常带 `dwd_*` 前缀，落库角色仍是 **约定 ODS**；项目 DWD 由 ENT 映射为 `enterprise_*` 等 |
| **禁止** | 本域 **复制** `dwd_org_base_info`（或平行 `svc_org_base` / 第二套工商主表） |
| 稳定业务键 | `org_id`（要素库）+ 统一社会信用代码 `external_id`；本域圈定/关系表只存键与本域属性 |
| 本域只保留 | 圈定规则与结果、关系、本域 ADS / ES / 图谱切片 |
| Demo 实例 | 与 ENT **共用** `demo_gkxlumenx_ods`；S2 **复用** ENT 已按 md-extract 所建国内机构要素库表，核对字段（含 `industry*`），**禁止**再 CREATE 一套主表 |

旧稿 `data-design/服务机构/服务机构域数据库设计(v1).md` 已写「禁止复制 ENT 全量工商」——与本条一致；**S4 stub**，冲突以本树为准。  
`SVC-DATA-ANALYSIS-L01-数据分析报告.md` = **legacy 分析纪要**，仅作开放项备忘，**不是** ODS / stores 建表真源。

## 3. 铁律（摘自架构基线，存储视角）

1. 调用链：前端 → Java → Python `/internal/*`；前端/Java **不**直连 DB / Nebula / MinIO（下载经门面）
2. Java **只读 ADS**；不扫 ODS/DWD；不写 ADS；不直连 nGQL
3. 算法与 ETL 在 Python / 数据工厂；写 ADS / Nebula / ES / MinIO（按管道）
4. 图谱引擎 = **NebulaGraph**；禁止 Neo4j；禁复制 CHAIN 数据模型（E7 `CT-SVC-ECO-01`）
5. 关系库 = **MySQL**；本文禁止 PostgreSQL / `dwd.` PG schema 叙述
6. 三方源变更不传导 ADS 契约面（D7）

## 4. 存储角色一览

见上级 [`../README.md`](../README.md) §5 矩阵（ENT / CHAIN / SVC 同构；实例前缀/对象前缀按域区分）。

## 5. ODS / DWD 分层（勿混淆）

| 层 | 本域约定 | 说明 |
|---|---|---|
| **约定贴源（ODS）** | 表名/字段 = `doc/` xlsx；日常读 `md-extract/`「国内机构要素库」 | 权威在文档，**不是** live as-built。供应方表名常带 `dwd_*`，**落库角色仍是 ODS** |
| **Demo ODS 实例** | `demo_gkxlumenx_ods`（与 ENT 同库） | **S2 核对/补齐目标**；禁止默认写 `gkxlumenx_ods` |
| **机构主表** | **不在本域建**；读 ENT 已对齐文档的同一套表 | 见 §2 |
| **项目 DWD（本域）** | 圈定结果、关系、本域明细切片 | 经 GDF/模拟 GDF；**不是**把要素库原样当项目 DWD |
| **冲突** | L01 现网实查、`gkx-mysql-raw`、v1 域设计稿 | **以本树会签流图为准**；旧稿仅历史输入 |

## 6. Demo / Mock

- **主路径**：按 **`third-party-source/doc/`**（优先 `md-extract/`）约定表结构写入 → `demo_*` ODS → **ETL 调度模拟 GDF** → 下游。见 [`etl/pipeline-demo-mock.md`](./etl/pipeline-demo-mock.md) · 流图 [`01-data-flow.md`](./01-data-flow.md) §7。
- **结构**与正式共用 [`stores/`](./stores/)；**ODS 口径**不以 `gkx-mysql-raw` as-built 为准。
- **样本**：[`seeds/`](./seeds/) 少量覆盖；先闭环后性能。圈定样例必须标 **待核验**（Q-SVC-010 未决策）。
- **旁路**：直写 ADS（D7）不替代全链路验收；细则 S2 补 `etl/pipeline-mock-to-ads.md`。

## 7. 圈定层（不伪闭合）

服务机构池 **不是** ODS 里的独立 Sheet。圈定发生在 ENT 机构主体之上，规则待甲方+供方决策（**Q-SVC-010**，阻断级）。

- Demo 可用团队临时默认（`business_scope` / `main_activities` 尽力而为），**必须**标待核验，**不得**写入正式 ADS 契约为 live。
- 本流图会签 **不**等于准入口径已批准。

## 8. 下一步

1. [`01-data-flow.md`](./01-data-flow.md) 拓扑已起草（2026-08-14）；**人签 `approved` 后**放行 S2  
2. **S2** `DATA-SVC-STORAGE-S2-L01`：按国内机构要素库在 `demo_gkxlumenx_ods` **核对/补齐**（含文档承诺的 `industry*` 列）；禁止只写清单；禁止写正式 ODS；禁止复制机构主表  
