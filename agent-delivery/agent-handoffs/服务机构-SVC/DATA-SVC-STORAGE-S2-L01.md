# DATA-SVC-STORAGE-S2-L01 · 服务机构存储 S2 — sources/etl/seeds + Demo ODS 核对

> **日期**：2026-08-14  
> **Owner 签收**：`human:侯佳伟` · **2026-08-14** · **会签通过 · 放行 S3**  
> **本地签**：本签收仅写本地 handoff + 本地 registry；**不 commit / 不 push**（按 Owner 指示）  
> **前置**：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` · `01-data-flow` **approved**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | 文档 `lite` + 建表/核对 `full` |
| 说明 | 未用 YAGNI 跳过真源铁律 / handoff / 禁第二套主表；复用 ENT `llm_ods`，仅加核对补列 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 MCP 面板未挂载 `task-registry`；registry 状态请 coordinator 代更 |

## 问题清单

- 内网 `192.168.88.43:3306` 本机不可达 → 使用 `ENTAN_MYSQL_HOST=111.198.38.90` `PORT=34306` 完成核对（与 CHAIN/ENT S2 同入口）
- Q-SVC-010 仍阻断「圈定标 live」——seeds 仅骨架 + 待核验声明，**不伪闭合**
- 文档 `industry*` 在 Demo 已齐；三方 live 对账仍属 OPEN-SVC-FLOW-08（不挡本单）

## 修改内容

### A. 文档（orchestration · `storage/SVC`）

- `sources/inventory.md`：国内机构要素库 **33 表**清单 + 真源入口 + **与 ENT 共用 / 本域 ODS 独有=无**
- `etl/pipeline-demo-mock.md`：回填 S2 脚本入口（ENT `run_llm_ods` 主路径 + `run_svc_ods_reconcile` 核对）
- `seeds/README.md`：覆盖矩阵骨架（含待核验圈定样例声明）
- `etl/demo_gkxlumenx_ods_svc_org_show_create.sql`：焦点表 `SHOW CREATE` 摘要
- README / CHANGELOG / sources·etl 索引回填

### B. 建表核对（demo-algo-ent-analysis）

- `scripts/run_svc_ods_reconcile.py`：md-extract → `demo_gkxlumenx_ods` **核对/补列**（`ALTER ADD`；**不** DROP 重建；拒写正式 ODS）
- `entan/llm_ods/load.py`：新增 `ensure_missing_columns`
- `test_svc_ods_reconcile.py`：不连库最小自检
- **未**新建 `dwd_org_base_info` / `svc_org_base`

### C. 核对证据（2026-08-14）

| 项 | 结果 |
|---|---|
| 目标库 | `demo_gkxlumenx_ods`（`SELECT DATABASE()` 确认） |
| 文档表数 | 33 |
| missing_tables | `[]` |
| missing_columns | `{}`（含 base `industry*` 9 列） |
| `dwd_org_base_info` 行数 | 100（ENT 既有样例；本单未灌数） |
| 正式 `gkxlumenx_ods` | **零写入** |

本机旁路产物（gitignore `out/`）：

- `repos/demo-algo-ent-analysis/out/svc_s2_reconcile_report.json`
- `repos/demo-algo-ent-analysis/out/svc_demo_ods_show_create.sql`

## 测试结果

| 检查 | 结果 |
|---|---|
| `run_svc_ods_reconcile.py --self-check` | OK · 33 表 · industry* 断言 |
| `test_svc_ods_reconcile.py` | OK |
| `--check` @ `111.198.38.90:34306` | `aligned=true` |
| `--show-create` | 含 `industry` / `industry_l1_*` … `industry_l4_*` |

## 遗留风险 / 开放项

| ID | 说明 | 是否挡 S3 |
|---|---|---|
| Q-SVC-010 | 准入主路径未决策；圈定不得标 live | **挡「圈定契约 live」**；不挡 stores 草稿开写 |
| OPEN-SVC-FLOW-08 | 三方 live vs 文档 industry* | 否 |
| OPEN-SVC-FLOW-01/03/04 | 调度 / MinIO 前缀 / ES·Nebula SLA | 否（S3+） |
| seeds 具体 INSERT | 矩阵骨架已有；样例值随 S3/灌数 | 否 |

**放行 S3**：`DATA-SVC-STORAGE-S3-L01` — **已放行**（`human:侯佳伟` 本地签 · 2026-08-14）。  
六类 / Q-SVC-010 **另轨**，不挡 stores 草稿开写；圈定结果仍标 draft + 待核验。

### Owner 签收记录（本地）

| 项 | 值 |
|---|---|
| signoff_by | `human:侯佳伟` |
| signoff_at | 2026-08-14 |
| signoff_status | **approved**（本地） |
| git | **不提交**（本机签收） |
| 结论 | S2 DoD 满足；放行 S3；正式签收/push 另择时 |

## CI/CD

- 分支：`gkx-orchestration` / `demo-algo-ent-analysis`（默认工作区；**本签收轮次不 push**）
- commit：**跳过**（Owner 要求仅本地签）
- pipeline：N/A（未 push）
- 验证命令：见上表

## 可观测性

- N/A（存储定义 + Demo 核对；无新服务）

## 架构合规自检

| # | 铁律 | |
|---|---|---|
| 1 | 算法只在 Python | ✅ 核对脚本在 Python |
| 2 | 调用链 | ✅ 未越层 |
| 3 | Nebula | ✅ 未引入 Neo4j |
| 4 | 可观测 | N/A 本单 |
| 5 | CI/CD | ⏸ 本地签收轮次不 push |
| 6 | demo→lumen | ✅ 仅 demo ODS |
| 7 | 共享核心 | N/A |
| 8 | ADS 先行 | ✅ S3 再灌 stores |
| 9–11 | D8/D9/D10 | N/A 无 UI |
| D12 | 不写正式 ODS | ✅ |

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/sources/inventory.md`
- `agent-delivery/data/data-design/storage/SVC/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/SVC/etl/demo_gkxlumenx_ods_svc_org_show_create.sql`
- `agent-delivery/data/data-design/storage/SVC/seeds/README.md`
- `agent-delivery/data/data-design/storage/SVC/{README,CHANGELOG,sources/README,etl/README}.md`
- `repos/demo-algo-ent-analysis/scripts/run_svc_ods_reconcile.py`
- `repos/demo-algo-ent-analysis/entan/llm_ods/load.py`
- `repos/demo-algo-ent-analysis/test_svc_ods_reconcile.py`
- 本 handoff

## Cost（估）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~6–10 万 |
| actual_cost | 估 <$5 |
| cost_warn | false |
