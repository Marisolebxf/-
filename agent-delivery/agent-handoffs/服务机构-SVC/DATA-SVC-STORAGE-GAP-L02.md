# DATA-SVC-STORAGE-GAP-L02 · SVC 存储 S1–S4 文档缺口补齐（不灌数）

> 日期：2026-08-19  
> Task：`DATA-SVC-STORAGE-GAP-L02`  
> 总控：`DEMO-SVC-REOPEN-长任务总控.md`（阶段 F）  
> **本单未灌数、未开 F-SEED、细表未标 approved、未执行 DDL。**

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
| 说明 | 只补 S4 列出的文档缺口；未用 YAGNI 跳过 D9 矩阵改指、词表、列对照、MinIO 指针 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI；未挂载 headroom MCP |

## 范围与实现

侯佳伟 2026-08-19：先不开灌数，补 S1–S4 不足与遗漏。

1. A1–A6 ODS→ADS 列对照：`storage/SVC/etl/ods-to-ads-mapping.md`（人口=圈定 hang JOIN ODS；不拷 DWD 主体）。  
2. A3 融资/投资列名钉死：`ods-to-dwd-mapping.md` §3（`funding_amount`/`completion_date`；投资无业务日则 `event_date` 空）。  
3. 六类临时词表：`seeds/svc_rule_demo_kw_v1.md`（Q-SVC-010 待核验；不关闭 008/010）。  
4. MinIO：`etl/pipeline-to-minio.md` 前缀 `svc/{task_id}/`；OPEN-03 写作关。  
5. 指标矩阵血缘改指 `svc_metric_*` / `svc_region_dist` / `svc_org_finance_event` / `demo_gkx_chain`；D1/D2/D4 **不改绿**。  
6. 入口 README「F-SEED 前必补」改为「缺口已补文档」。

## 偏离说明

- 词表是 Demo 临时配置，不是 algorithm-agent 正式 `svc_rule_v2.2`。  
- A2 无国家列，对照写死 `geo_level=province`。  
- 流图 `approved` 未改拓扑；仅 OPEN 表写作状态与 amendment_note。

## 产物清单

| 产物 | 路径 |
|---|---|
| A1–A6 列对照 | `data-design/storage/SVC/etl/ods-to-ads-mapping.md` |
| ETL 索引 | `…/SVC/etl/README.md` |
| MinIO 指针 | `…/SVC/etl/pipeline-to-minio.md` |
| 六类词表 | `…/SVC/seeds/svc_rule_demo_kw_v1.md` |
| 矩阵血缘 | `metrics/metric-readiness-matrix-SVC.yaml` |
| 域入口 | `data-design/storage/SVC/README.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-GAP-L02.md` |

## 验收证据

- [x] 列对照带 `demo_gkxlumenx_ods` 库名；不拷主体  
- [x] 词表标 pending_client / Q-SVC-010  
- [x] MinIO 不写现网凭证  
- [x] 矩阵不再以 `gkx_dwd.service_org` / `gkx_service` 当现行；D4 仍 mock  
- [x] 未 50100、未建 F-SEED、细表仍 draft、未改 CHAIN / lumen 四仓  
- [x] 联调完成（文档缺口对 S1–S4 入口；灌数仍另开）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A（文档）；写库方仍 = `demo-algo-ent-analysis` |
| 2 | 调用链 | ✅ F 联调台；P 虚线不施工 |
| 3 | NebulaGraph | ✅ 矩阵改指 hang `demo_gkx_chain`；禁 `gkx_service` |
| 4 | 可观测 | ✅ N/A（文档） |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / D12 | ✅ 50892 不动 |
| 8 | ADS | ✅ 对照指向现行 `svc_*`；细表 draft |
| 9 | D8 | ✅ N/A |
| 10 | D9 | ✅ 矩阵不改绿；Q-SVC-010 不伪闭合 |

## 决议

S1–S4 **文档缺口已补**。**F-SEED / 50100 仍另开**；引擎须读列对照 + 词表，禁止猜列。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 部署：N/A
- 连库 CREATE / 灌数：未执行

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 60000 |
| actual_tokens | 88000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.43 |
| cost_warn | green |
