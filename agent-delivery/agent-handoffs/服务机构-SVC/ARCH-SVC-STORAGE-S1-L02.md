# ARCH-SVC-STORAGE-S1-L02 · 服务机构存储端到端数据流图会签（起草）

> 日期：2026-08-19  
> Task：`ARCH-SVC-STORAGE-S1-L02`  
> 总控：[`DEMO-SVC-REOPEN-长任务总控.md`](./DEMO-SVC-REOPEN-长任务总控.md)  
> 会签主件：`agent-delivery/data/data-design/storage/SVC/01-data-flow.md`  
> **人签状态**：`signoff_status=approved` · **`human:淮政玮`** · 2026-08-19（**放行 S2 拓扑；未放行 F-SEED 灌数**）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 协作 | Agent 起草骨架与流图；**签字权 = human:淮政玮**；结构歧义升级 `human:侯佳伟` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | definition / 架构会签，不以缩代码为目标；未用 YAGNI 跳过调用链 / ADS / Nebula / 会签 / 开放项 / D9 口径挂起项 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 headroom MCP；task-registry 走 `scripts/task-mcp-cli.mjs` 应急通道 |

## 范围与实现

- **范围**：重建 `storage/SVC` 骨架（`00-context` + `01-data-flow` + 入口 README）；三图同构 ENT/CHAIN；阶段 F 在线路径以 50100 实线、50892/Java 虚线画出。
- **对照**：总控已拍板 §1；`storage/ENT/01-data-flow.md` + `storage/CHAIN/01-data-flow.md`；`architecture-baseline` D3/D6/D7/D12；派单 `ARCH-SVC-STORAGE-S1-L02-派单说明.md`。
- **写死口径**：共用 `demo_gkxlumenx_ods`（不新建、不 DROP 33 表）；圈定 `svc_rule_demo_kw_v1`；hang ENT `org_id`；禁平行 `svc_org_base` / 禁复制 `dwd_org_base_info` 全列 / 禁 `enterprise_*` 主路径；一张 `demo_gkx_chain`；F 写库方=`demo-algo-ent-analysis`（50100）；F 不碰 lumen 四仓；短板 **Q-SVCCHAIN-03**，Q061 对照列；CHAIN / `industry-center` 冻结。
- **非范围**：DDL / 建表 / 灌数 / `stores/*` 细表 / 50100 改页 / F-SEED / 阶段 P。

## 偏离说明

无架构偏离。阶段 F 算法台直连 Python 是 ENT 联调台惯例，已在 §2 与产品链（虚线）拆开，避免冒充 D12 产品调用链。  
调度 cron/DAG、MinIO 现网参数、细表名登记为开放项（不阻塞拓扑会签，**人签前仍不放行 S2**）。  
Q-SVC-010 / Q-SVCCHAIN-03 保持 🟡，不伪闭合 live。

Registry DoD 文案仍残留「李伟 approved 前不得开 S2」——**会签 Owner 真源 = `human:淮政玮`**；**结构歧义 = `human:侯佳伟`**（服务机构模块负责）。未改 registry DoD 正文（MCP `task-update-fields` 无该字段）。

## 产物清单

| 产物 | 路径 |
|---|---|
| 会签主件（**approved · 2026-08-19**） | `agent-delivery/data/data-design/storage/SVC/01-data-flow.md` |
| 上下文 / 入口 / CHANGELOG | `…/storage/SVC/{00-context,README,CHANGELOG}.md` |
| 体系规范一句 | `…/storage/README.md`（SVC **流图已会签**，未标建设完成） |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-S1-L02.md` |

**未写**：`stores/mysql/*.md`、`etl/pipeline-demo-mock.md`、S2 叶、F-SEED。

## 验收证据

- [x] 三图与基线同构（批处理 / 在线读 / 对象产物）；每图含 生产者\|消费者\|触发\|失败语义\|禁止事项
- [x] 总控 §1 拍板项写入流图（含 Q-SVCCHAIN-03、一张图、F 不碰 lumen 四仓、50100 写库方）
- [x] 正文写明：本单不建表、不灌数
- [x] `signoff_owner=human:淮政玮` · `signoff_status=approved` · `signoff_by=human:淮政玮` · `signoff_at=2026-08-19`
- [x] **人签** `human:淮政玮` `approved`（放行 S2 拓扑；**未放行** F-SEED / 50100 灌数当退出门）
- [x] 未改 `lumen-*` 四仓、未改 CHAIN、未写正式库 / Demo 库

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 阶段 F 写库方 = `demo-algo-ent-analysis` |
| 2 | 调用链 前端→Java→Python | ✅ 阶段 P 虚线保留；阶段 F 标明联调台直连，不冒充产品链 |
| 3 | 图谱 NebulaGraph | ✅ 仅 `demo_gkx_chain`；禁 Neo4j / 平行 `gkx_service` |
| 4 | 可观测性 | ✅ N/A（文档会签） |
| 5 | CI/CD | ✅ skip（definition · `cicd: skip_design_only`） |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档；F 明确不碰 lumen 四仓 |
| 7 | 方案 A / D12 | ✅ Java 只读 ADS 为 P 目标；本总控不施工 50892 |
| 8 | 数据走 ADS（D3/D7） | ✅ |
| 9 | D8 | ✅ N/A |
| 10 | D9/D10 | ✅ 口径挂 Q-SVC-010 / Q-SVCCHAIN-03 / Q061 对照，不伪闭合 |

## 决议

**`human:淮政玮` 会签通过（2026-08-19）。**  
coordinator 可建 `DATA-SVC-STORAGE-S2-L02`。仍禁止无 S 契约表就开 F-SEED / 50100 灌数当底座退出门。阶段 P 不自动续。

## CI/CD

- 分支：`origin/dev`（gkx-orchestration）
- commit：本 handoff 同批 push（见 git log）
- pipeline：`cicd: skip_design_only`
- 部署 / K8s / 测试 URL：N/A（不改运行时）

## 可观测性

N/A（文档会签，无运行时服务）

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80000 |
| actual_tokens | 88000 |
| model_used | `cursor-grok-4.5`（本会话 Cursor Grok 4.6；按已用 enum 回填） |
| actual_cost | 0.44 |
| cost_warn | green |
| source | session_estimate |

## 遗留风险

- 淮政玮未签期间若有人按旧废作 S1 `approved` 开灌数 → 以本 handoff + 总控为准，拦截（本轮已签拓扑，灌数仍须 S 契约）。
- S2 表级清单仍开放（OPEN-SVC-FLOW-05/06/12）；人签只放行**拓扑**，不放行细表 approved。
