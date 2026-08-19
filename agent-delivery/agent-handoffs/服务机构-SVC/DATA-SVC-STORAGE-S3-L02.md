# DATA-SVC-STORAGE-S3-L02 · 服务机构存储 S3 — 细表 draft + 映射 + Demo 空表 CREATE

> 日期：2026-08-19  
> Task：`DATA-SVC-STORAGE-S3-L02`  
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
| 说明 | 文档细表 + DDL；未用 YAGNI 跳过 OPEN-06 映射、A1–A6、十模型回写、Demo 空表 CREATE、hang `demo_gkx_chain` |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI；未挂载 headroom MCP |

## 范围与实现

- **范围**：`storage/SVC/stores/*` 细表 draft；`etl/ods-to-dwd-mapping.md`（源 = **`demo_gkxlumenx_ods.dwd_org_base_info`**，ODS 贴源）；`ddl-demo-empty.sql` 仅 Demo DWD/ADS 空表。
- **DWD**：`svc_org_circle` / `svc_org_graph_hang` / `svc_org_finance_event`（只 hang `org_id`，无 38 列主体）。
- **ADS**：A1–A6（`svc_metric_fact|series|dist` + `svc_region_dist`）+ 十模型（`svc_chain_gap` 含 Q-SVCCHAIN-03 `runtime_flag` 与 Q061 对照列；`svc_relation_chain`；`svc_tech_power_score`×6 `model_id`；招引/培育）。
- **图**：只 hang `demo_gkx_chain`。
- **对照**：已会签流图 §6/§7；总控 §1；S2 inventory。
- **非范围**：50100 灌数、F-SEED、lumen 四仓、CHAIN、DROP/新建 ODS、细表 approved、连库执行 DDL。

## 偏离说明

- 未连 Demo MySQL 执行 CREATE：本单只落 SQL；**F-SEED 首刀跑** `stores/mysql/ddl-demo-empty.sql`。未两边空。
- ES 仅指针，不挡 F（OPEN-04 仍开放）。
- 未抄旧 `DATA-SVC-STORAGE-S3-L01` 的 `gkx_svc` / `service_org` 全列主体。

## 产物清单

| 产物 | 路径 |
|---|---|
| OPEN-06 映射 | `data-design/storage/SVC/etl/ods-to-dwd-mapping.md` |
| DWD / ADS / DIM | `…/stores/mysql/{dwd-svc,ads,dim,README}.md` |
| Demo 空表 DDL | `…/stores/mysql/ddl-demo-empty.sql`（12 表） |
| Nebula | `…/stores/nebula/graph-svc.md` |
| ES 指针 | `…/stores/elasticsearch/README.md` |
| 入口回填 | `SVC/README.md` · `CHANGELOG.md` · `storage/README.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S3-L02.md` |

## 验收证据

- [x] 映射源带库名 `demo_gkxlumenx_ods.dwd_org_base_info`；主体列标 n.a. 不复制
- [x] DDL 12 张 `CREATE TABLE IF NOT EXISTS` 仅 `demo_gkxlumenx_dwd` / `_ads`；无 DROP ODS
- [x] ADS 含 A1–A6 metric_id 与十模型表；短板 `runtime_flag` = Q-SVCCHAIN-03
- [x] 细表 draft；未 50100 灌数；未建 F-SEED
- [x] 未改 lumen 四仓 / CHAIN / 正式库

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 写库方仍 = `demo-algo-ent-analysis`（本单不跑） |
| 2 | 调用链 | ✅ F 联调台；P 虚线不施工 |
| 3 | NebulaGraph | ✅ hang `demo_gkx_chain`；禁 `gkx_service` |
| 4 | 可观测 | ✅ N/A（文档） |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / D12 | ✅ 50892 不动 |
| 8 | ADS | ✅ 契约面已列；Java 阶段 P 只读 |
| 9 | D8 | ✅ N/A |
| 10 | D9 | ✅ Q-SVC-010 / Q-SVCCHAIN-03 / Q061 对照不伪闭合 |

## 决议

S3 细表 + OPEN-06 映射 + Demo 空表 CREATE 写作完成（draft）。**放行 S4 入口**；**仍禁止 F-SEED / 50100 灌数**。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 部署：N/A
- 连库 CREATE：未执行（F-SEED 首刀）

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 120000 |
| actual_tokens | 98000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.48 |
| cost_warn | green |
