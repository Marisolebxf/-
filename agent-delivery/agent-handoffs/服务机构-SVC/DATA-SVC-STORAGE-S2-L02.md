# DATA-SVC-STORAGE-S2-L02 · 服务机构存储 S2 — sources/etl/seeds 指针

> 日期：2026-08-19  
> Task：`DATA-SVC-STORAGE-S2-L02`  
> 流图：`storage/SVC/01-data-flow.md` **approved** · `human:淮政玮` · 2026-08-19  
> **本单未灌数、未开 F-SEED、未标细表 approved。**

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
| 说明 | 文档指针；未用 YAGNI 跳过真源 / hang `org_id` / 禁平行表 / 会签放行范围 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI；未挂载 headroom MCP |

## 范围与实现

- **范围**：重建 `storage/SVC/{sources,etl,seeds}` 指针；33 表从 md-extract 国内机构要素库圈选；全部与 ENT 共用。
- **对照**：已会签 `01-data-flow` §6/§7；总控 §1；ENT inventory / pipeline-demo-mock。
- **非范围**：S3 stores 细表、50100 灌数、F-SEED、lumen 四仓、CHAIN、DROP/新建 ODS、现场 MySQL ALTER（本单未连库核对）。

## 偏离说明

未做 Demo ODS 现场 `SHOW CREATE` / `ALTER ADD`：淮总会签本叶为「拓扑写作」；旧 `run_svc_ods_reconcile.py` 已随停机删除，不在本单复活灌数脚本。结构以 md-extract 为准。

## 产物清单

| 产物 | 路径 |
|---|---|
| ODS 清单 | `data-design/storage/SVC/sources/inventory.md` |
| ETL 指针 | `…/SVC/etl/pipeline-demo-mock.md` |
| seeds 骨架 | `…/SVC/seeds/README.md` |
| 入口回填 | `…/SVC/README.md` · `CHANGELOG.md` · `storage/README.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S2-L02.md` |

## 验收证据

- [x] 三份指针落盘；表名来自 md-extract（33 张，本域独有=无）
- [x] 圈定主读 `dwd_org_base_info`；禁 `svc_org_base` / 全列复制 / `enterprise_*` 主路径
- [x] 细表仍 draft；未 50100 灌数；未建 F-SEED
- [x] 未改 lumen 四仓 / CHAIN / 正式库

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 写库方指针 = `demo-algo-ent-analysis`（本单不跑） |
| 2 | 调用链 | ✅ F 联调台已在流图标明；P 虚线不施工 |
| 3 | NebulaGraph | ✅ hang `demo_gkx_chain` |
| 4 | 可观测 | ✅ N/A（文档） |
| 5 | CI/CD | ✅ skip_design_only |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A / D12 | ✅ 50892 不动 |
| 8 | ADS | ✅ 契约面 S3 细表 |
| 9 | D8 | ✅ N/A |
| 10 | D9 | ✅ Q-SVC-010 / Q-SVCCHAIN-03 不伪闭合 |

## 决议

S2 拓扑写作完成。**放行 S3 细表清单（仍 draft）**；**仍禁止 F-SEED / 50100 灌数**。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 部署：N/A

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80000 |
| actual_tokens | 42000 |
| model_used | `cursor-grok-4.5` |
| actual_cost | 0.22 |
| cost_warn | green |
