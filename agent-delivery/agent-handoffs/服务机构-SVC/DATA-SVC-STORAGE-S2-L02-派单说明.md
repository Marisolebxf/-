# DATA-SVC-STORAGE-S2-L02 · 派单说明（阶段 F · 源/ETL 指针）

> **日期**：2026-08-19  
> **Task ID**：`DATA-SVC-STORAGE-S2-L02`  
> **总控**：[`DEMO-SVC-REOPEN-长任务总控.md`](./DEMO-SVC-REOPEN-长任务总控.md)（已授权 · 范围仅阶段 F）  
> **前置**：`ARCH-SVC-STORAGE-S1-L02` · [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) **`signoff_status=approved`** · `human:淮政玮` · 2026-08-19  
> **淮总会签口径**：只放行 **S2 拓扑写作**（sources/etl/seeds 指针）；细表不得标 approved；**仍禁止 F-SEED / 50100 灌数**（须 S 契约表，S3）  
> **派单**：`agent:coordinator-agent` · `claim_type=coordinator_dispatch`  
> **监管 / 模块负责**：`human:侯佳伟`  
> **看板签收**：`human:淮政玮`  
> **执行**：`data-agent`  
> **task_type**：`definition` · 强度：**ponytail lite**（文档指针；禁止借 S2 灌数）  
> **锁**：24h  

旧叶 `DATA-SVC-STORAGE-S2-L01` = **废作**，禁止当 `depends_on`、禁止复活。可对照其 inventory 写法，不可抄停机前库状态当本轮真源。

---

## 1. 这张单是什么 / 不是什么

**是**：按已会签流图，把 SVC 读哪些 ODS 表、怎么模拟 GDF、圈定规则、seeds 骨架写进 `storage/SVC/sources|etl|seeds`。

**不是**：S3 细表 approved、DDL 新 ODS 实例、DROP 33 表、平行 `svc_org_base`、50100 灌数、F-SEED、改 lumen 四仓、改 CHAIN。

---

## 2. 必读（按序）

| 序 | 路径 | 用途 |
|---:|------|------|
| 1 | `storage/SVC/01-data-flow.md` | 已会签；§6 放行范围；§7 Demo 主路径 |
| 2 | `storage/SVC/00-context.md` | 边界；hang ENT；F 写库方 |
| 3 | `DEMO-SVC-REOPEN-长任务总控.md` §1 | 拍板项 |
| 4 | `storage/ENT/sources/inventory.md` + `etl/pipeline-demo-mock.md` | 同构样例 |
| 5 | `doc/md-extract/` 国内机构要素库 | ODS 表名/字段权威读取 |

---

## 3. 交付

在 `agent-delivery/data/data-design/storage/SVC/`：

- `sources/inventory.md`：本域依赖的 ODS **表级清单**（从已有 33 表圈选；标与 ENT 共用 / 本域独有）；真源入口；**禁止 DROP、禁止新建 ODS 实例**
- `etl/pipeline-demo-mock.md`：约定 ODS → 模拟 GDF → SVC DWD；圈定 `svc_rule_demo_kw_v1`；hang `org_id`；灌数真源仍写 50100 按钮（本单不按按钮）
- `seeds/README.md`：覆盖矩阵骨架；fixture 24 家标旁路；不伪闭合 Q-SVC-010
- 回填 `SVC/README.md` 读序（仍不得标「建设完成」；S4 才标绿）
- handoff：`agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S2-L02.md`

允许：对 `demo_gkxlumenx_ods` **核对/补列**（`ALTER ADD`，禁 DROP 重建），证据写入 handoff。不允许：把核对当成灌数完成、不允许开 F-SEED。

---

## 4. DoD

- [ ] `sources/inventory.md` + `etl/pipeline-demo-mock.md` + `seeds/README.md` 落盘 `origin/dev`
- [ ] 表名来自 md-extract；零写入正式 `gkxlumenx_ods`
- [ ] 无 `svc_org_base`；无复制 `dwd_org_base_info` 全列；无 `SELECT enterprise_*` 主路径
- [ ] 细表仍 draft；未宣称 stores approved
- [ ] **未** 50100 灌数、未建 F-SEED 叶
- [ ] 未改 lumen 四仓 / CHAIN
- [ ] handoff 含架构合规 + cost 四字段

---

## 5. `/goal`（贴 data-agent 会话）

```
任务：DATA-SVC-STORAGE-S2-L02
监管：human:侯佳伟
认领：coordinator_dispatch · 24h
总控：agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md
厚包：agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S2-L02-派单说明.md
强度：ponytail lite
上下文：headroom 推荐；禁止 compress 代替精读已会签 01-data-flow §6/§7 与总控 §1

做：storage/SVC sources/etl/seeds 指针。共用 demo_gkxlumenx_ods，不新建 ODS、不 DROP 33 表。
不做：细表 approved、F-SEED、50100 灌数、lumen 四仓、CHAIN、平行 svc_org_base。

会签口径：human:淮政玮 2026-08-19 只放行 S2 拓扑写作。禁止 force。commit [agent:data-agent]。
```
