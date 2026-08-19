# ARCH-SVC-STORAGE-S1-L02 · 派单说明（阶段 F · 流图会签）

> **日期**：2026-08-19  
> **Task ID**：`ARCH-SVC-STORAGE-S1-L02`  
> **总控**：[`DEMO-SVC-REOPEN-长任务总控.md`](./DEMO-SVC-REOPEN-长任务总控.md)（已授权 · 范围仅阶段 F）  
> **派单**：`agent:coordinator-agent` · `claim_type=coordinator_dispatch`  
> **监管**：`human:侯佳伟`  
> **会签 Owner**：`human:淮政玮`（流图签字后才允许 S2/S3 / F-SEED）  
> **结构歧义**：`human:李伟`（不是本单会签人）  
> **看板签收**：`human:淮政玮`（`ready_to_sign → done`）  
> **执行**：`architect-agent`  
> **task_type**：`definition` · 强度：**ponytail off**（会签文档，不写业务代码）  
> **锁**：24h  

旧叶 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` = **废作**，禁止当依赖、禁止复活。

---

## 1. 这张单是什么 / 不是什么

**是**：把服务机构数据 **怎么流、谁写谁读、禁止什么** 画死，写入 `storage/SVC/01-data-flow.md`，交 **淮政玮** 会签。

**不是**：建表、灌数、写 DDL、改 50100 页面、碰 lumen 四仓、开 F-SEED。

会签通过后，才允许 S2/S3 写细表，才允许 50100 灌数。淮政玮在等这份流图，别着急灌数。

### 文件在哪（现在就能打开 vs 还没写）

| 文件 | 路径 | 现在有没有 |
|------|------|------------|
| 本叶厚包 | `gkx-orchestration/agent-delivery/agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-S1-L02-派单说明.md` | **有** |
| 阶段 F 总控 | 同目录 `DEMO-SVC-REOPEN-长任务总控.md` | **有** |
| 会签主产物 | `gkx-orchestration/agent-delivery/data/data-design/storage/SVC/01-data-flow.md` | **已起草**（`signoff_status=pending` · 等淮政玮） |
| 对照样例 | `…/storage/ENT/01-data-flow.md`、`…/storage/CHAIN/01-data-flow.md` | 有 |
| 完工 handoff | 同 SVC 目录 `ARCH-SVC-STORAGE-S1-L02.md` | **有**（待淮政玮会签，未放行 S2） |

---

## 2. 必读（按序）

| 序 | 路径 | 用途 |
|---:|------|------|
| 1 | `agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md` | 已拍板 §1（含短板 Q-SVCCHAIN-03、一张图、F 不碰 lumen） |
| 2 | `data/data-design/storage/README.md` | 体系规范；决策 #7 一张 `demo_gkx_chain` |
| 3 | `storage/ENT/01-data-flow.md` + `storage/CHAIN/01-data-flow.md` | 同构三图 + frontmatter 会签字段 |
| 4 | `architecture-baseline.md` | D3 ADS / D6 Nebula / D7 工厂 / D12 |
| 5 | `storage/platform/minio.md` | 只引用 |
| 6 | `客户决策清单跟踪表.md` | Q-SVC-010、Q-SVCCHAIN-03、Q061 对照 |

不要当会签真源：已删的旧 `storage/SVC/`、`gkx-mysql-raw` as-built、废作 S1–S4 handoff 正文（可对照，不可当 `depends_on`）。

---

## 3. 交付

### 3.1 骨架（允许，仍不算建表）

新建 `agent-delivery/data/data-design/storage/SVC/`：

- `00-context.md`（元素边界、与 ENT/CHAIN hang、阶段 F 读写方）
- `01-data-flow.md`（本单主产物）

**本单不要**写 `stores/mysql/*.md` 细表、不要改 Demo 库、不要把 `storage/README.md` 的 SVC 行标成已建设完成（S4 再加回入口；S1 可在 README 加「SVC 流图会签中」一句，可选）。

### 3.2 `01-data-flow.md` 必须写死

同构 ENT/CHAIN：批处理主链 / 在线读路径（**阶段 F 以 50100 为准**）/ 对象产物。frontmatter 含 `signoff_owner: human:淮政玮`、`signoff_status`（起草=`pending`，淮政玮签后=`approved`）。对照 ENT 流图也是淮政玮会签。

拓扑要点（总控已拍板，不得改口径）：

1. ODS 共用 `demo_gkxlumenx_ods`，不新建 ODS，不 DROP 33 表。  
2. Demo 主路径：约定 ODS → 模拟 GDF → SVC DWD → ADS；圈定 `svc_rule_demo_kw_v1`。  
3. 禁 `SELECT enterprise_*`；禁复制 `dwd_org_base_info` 全列；禁平行 `svc_org_base`；主体 hang ENT `org_id`。  
4. 图谱 hang **一张** Demo `demo_gkx_chain`，不新建 `gkx_service` space。  
5. **阶段 F 写库方**：`demo-algo-ent-analysis`（50100 按钮触发）。**阶段 F 不写**：`lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic`。50892 只读留给 P 总控，本流图可画「未来 Java 只读 ADS」虚线，但标注 **不在本总控施工**。  
6. 短板 Demo 运行时口径 = **Q-SVCCHAIN-03**；Q061 对照列。  
7. CHAIN 路径 / `industry-center` 算法 **不动**。

### 3.3 会签

- 起草完成：handoff + `signoff_status: pending`，请 **`human:淮政玮`** 会签。  
- 淮政玮 `approved` 之前：**禁止**建 `DATA-SVC-STORAGE-S2-L02`、禁止 F-SEED。  
- 流图结构吵起来才升级 `human:李伟`，不挡把稿交给淮政玮。

---

## 4. DoD

- [x] `storage/SVC/00-context.md` + `01-data-flow.md` 落盘 `origin/dev`  
- [x] 三图 + 生产者/消费者/禁止事项表齐全  
- [x] 总控 §1 拍板项写入流图（含 Q-SVCCHAIN-03、一张图、F 不碰 lumen 四仓）  
- [x] 正文写明：本单不建表、不灌数  
- [ ] `human:淮政玮` 会签（handoff 已写「待淮政玮签、未放行 S2」——未签不得解锁 S2）  
- [x] handoff：`agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-S1-L02.md`（架构合规 + cost 四字段；definition 无 ponytail 缩文档）  
- [x] 未改 `lumen-*` 四仓、未改 CHAIN、未写正式库  

---

## 5. `/goal`（贴 architect 会话）

```
任务：ARCH-SVC-STORAGE-S1-L02
监管：human:侯佳伟
认领：coordinator_dispatch · 24h
总控：agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md
厚包：agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-S1-L02-派单说明.md
强度：ponytail off
上下文：headroom 推荐；禁止 compress 代替精读 ENT/CHAIN 流图与总控已拍板表

做：storage/SVC 骨架 + 01-data-flow 会签稿。同构 ENT/CHAIN 三图。
不做：建表、灌数、DDL、50100 改页、lumen 四仓、CHAIN、F-SEED。

会签 Owner：human:淮政玮。未 approved 不得宣称放行 S2。
结构歧义才升级 human:李伟。看板签收仍 human:淮政玮。禁止 force。commit [agent:architect-agent]。
```
