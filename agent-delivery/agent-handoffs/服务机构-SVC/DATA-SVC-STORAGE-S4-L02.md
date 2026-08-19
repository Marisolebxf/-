# DATA-SVC-STORAGE-S4-L02 · 服务机构存储 S4 — README 入口 / 文档闭环

> 日期：2026-08-19  
> Task：`DATA-SVC-STORAGE-S4-L02`  
> 流图：`storage/SVC/01-data-flow.md` **approved** · `human:淮政玮` · 2026-08-19  
> **本单未灌数、未开 F-SEED、细表未标 approved。**

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
| 说明 | 文档 stub / 入口；未用 YAGNI 跳过 OPEN-13、inventory 本波读法、F-SEED 前必补清单 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI；未挂载 headroom MCP |

## 范围与实现

- **范围**：`storage/README.md` + `storage/SVC/README.md` 标 **S1–S4 文档闭环**（≠灌数完成）；`data-design/服务机构/` stub 指向本树；OPEN-SVC-FLOW-13 写作关闭；inventory 本波读法（圈定主表 / A3 融资投资 / 招投标旁路 / 其余不聚合）。
- **F-SEED 前必补**（写在 `SVC/README.md`，本单不补正文）：A1–A6 列对照、六类词表、MinIO 管道、指标矩阵旧 `service_org`。
- **对照**：已会签流图 §6；总控 S4 = README 入口；ENT/CHAIN S4 stub 同构。
- **非范围**：50100 灌数、F-SEED 叶、细表 approved、连库 DDL、改 lumen 四仓 / CHAIN。

## 偏离说明

- 流图原文「把 SVC 标成建设完成」落地为 **文档闭环** 用语，避免与灌数完成混淆。
- 旧 `DATA-SVC-STORAGE-S4-L01` 仅对照，不 `depends_on`。

## 产物清单

| 产物 | 路径 |
|---|---|
| 规范入口 | `data-design/storage/README.md` |
| 域入口 | `data-design/storage/SVC/README.md` |
| inventory 本波读法 | `…/SVC/sources/inventory.md` |
| 旧路径 stub | `data-design/服务机构/README.md` + v1 / L01 横幅 |
| 派单说明 | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S4-L02-派单说明.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S4-L02.md` |

## 验收证据

- [x] `storage/README.md` SVC 行 = S1–S4 文档闭环；域入口不再写「会签 pending」
- [x] `服务机构/README.md` 强制导航 `storage/SVC`
- [x] inventory 标明圈定 / A3 / 招投标旁路 / 其余不聚合
- [x] `SVC/README.md` 列出 F-SEED 前必补四项
- [x] 细表仍 draft；未 50100 灌数；未建 F-SEED
- [x] 未改 lumen 四仓 / CHAIN / 正式库

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A（文档）；写库方仍 = `demo-algo-ent-analysis` |
| 2 | 调用链 | ✅ F 联调台；P 虚线不施工 |
| 3 | NebulaGraph | ✅ 未改 hang `demo_gkx_chain` |
| 4 | 可观测 | ✅ N/A（文档） |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / D12 | ✅ 50892 不动 |
| 8 | ADS | ✅ 未改契约表；入口指向 S3 draft |
| 9 | D8 | ✅ N/A |
| 10 | D9 | ✅ Q-SVC-010 不伪闭合；矩阵改指留给 METRIC |

## 决议

S4 入口完成。**F-SEED 可另开叶**（须补列对照 + 词表）；**本单不灌数**。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 部署：N/A
- 连库 CREATE：仍未执行（F-SEED 首刀跑 S3 `ddl-demo-empty.sql`）

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 38000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.19 |
| cost_warn | green |
