# DATA-SVC-STORAGE-CARD-L02 · SVC ADS 名单卡面 + 表级血缘图（选 B · 不灌数）

> 日期：2026-08-20  
> Task：`DATA-SVC-STORAGE-CARD-L02`  
> 总控：`DEMO-SVC-REOPEN-长任务总控.md`（阶段 F）  
> 拍板：`human:淮政玮` 选 B（名单走 ADS 投影/卡面；线上不联 ODS）  
> **本单未执行 DDL、未灌数、未开 F-SEED、细表未标 approved、未改 §1 工厂拓扑边。**

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 只补一张 ADS 卡面 + §1.1 血缘图；未整树返工；未用 YAGNI 跳过 D9 展示列 / 图即契约 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI；未挂载 headroom MCP |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（增补）；`SVC-STORAGE-FLOW` **未改边** |
| 图 diff | §1 工厂 `flowchart LR` 边未动。新增 §1.1：ODS 户口本 → DWD hang → Nebula 一张图 → ADS 卡面/十模型/A1–A6 → 线上只读 ADS。灌数虚线 = JOIN 一次投影，不是在线联 ODS。 |
| 会签态 | `SVC-STORAGE-FLOW` frontmatter 仍 `signoff_status=approved`（2026-08-19）；血缘图为 2026-08-20 增补，细表仍 draft |
| 说明 | 真源 = `01-data-flow.md` §1.1 Mermaid；PNG 不是源头 |

## 范围与实现

淮政玮 2026-08-20：**选 B**。名单走 ADS 投影/卡面，灌数写一次；线上名单不联 ODS。

1. ADS 卡面 `demo_gkxlumenx_ads.svc_org_card`：仅展示列（`org_id`、名称、省市、区、行业、六类候选、待核验）。**不是**平行 `svc_org_base`，**不是**全列复制。DWD 仍只 hang `org_id`。  
2. 空表 SQL 写入 `ddl-demo-empty.sql`；**本单不 CREATE、不灌数**。  
3. `01-data-flow.md` §1.1 表级血缘图（人主看图）；§7 灌数时序一句：ODS 圈定 → 写 circle → 同一批投影 card + 聚合指标 → 再跑模型写回；名称 JOIN `svc_org_card`，不回 ODS。  
4. S1 会签态维持；S2–S4 / GAP / 卡面 **draft**，不升细表 approved。  
5. **A 不做**：50100 现拼 ODS。

## 偏离说明

- 无。未整树返工 mapping / inventory / 矩阵。  
- `diagram-as-contract.md` 图目录加一行 `SVC-STORAGE-LINEAGE`（指针，不是新拓扑）。

## 产物清单

| 产物 | 路径 |
|---|---|
| 卡面列对照 | `data-design/storage/SVC/stores/mysql/ads.md` §1.1 |
| 空表 SQL | `…/stores/mysql/ddl-demo-empty.sql`（`svc_org_card`） |
| 血缘图 | `data-design/storage/SVC/01-data-flow.md` §1.1 |
| 图目录 | `diagram-as-contract.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-CARD-L02.md` |

## 验收证据

- [x] 卡面仅展示列；标明禁 `svc_org_base` / 全列复制  
- [x] DDL 已写空表 CREATE；未连库执行  
- [x] §1.1 Mermaid `diagram_id=SVC-STORAGE-LINEAGE`；§1 工厂边未改  
- [x] 细表仍 draft；未 50100；未建 F-SEED  
- [x] 未改 lumen 四仓 / CHAIN / 正式库  
- [x] 联调完成（卡面+血缘文档对淮总看一眼；灌数仍另开）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A（文档）；写库方仍 = `demo-algo-ent-analysis` |
| 2 | 调用链 | ✅ 线上只读 ADS；不联 ODS |
| 3 | NebulaGraph | ✅ 血缘 hang `demo_gkx_chain` |
| 4 | 可观测 | ✅ N/A（文档） |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / D12 | ✅ 50892 不施工；名单不另造 ODS 拼法 |
| 8 | ADS | ✅ 卡面在 ADS；DWD 不升主表 |
| 9 | D8 | ✅ N/A |
| 10 | D9 | ✅ Q-SVC-010 待核验列在卡面；不伪闭合 |

## 决议

卡面 + 血缘图已落盘，**请淮总看一眼后再开 F-SEED**。本单不灌数。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 部署：N/A
- 连库 CREATE / 灌数：未执行

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 92000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.48 |
| cost_warn | green |
