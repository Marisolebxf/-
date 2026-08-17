# ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01 · 服务机构存储端到端数据流图会签

> 日期：2026-08-14  
> Task：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01`  
> 会签主件：`agent-delivery/data/data-design/storage/SVC/01-data-flow.md`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:侯佳伟` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 协作 | `architect-agent` 起草骨架与流图；**签字权 = human:侯佳伟** |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | definition / 架构会签，不以缩代码为目标；未用 YAGNI 跳过调用链 / ADS / Nebula / 会签 / 开放项 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 headroom MCP；task-registry 走 `scripts/task-mcp-cli.mjs` 应急通道 |

## 范围与实现

- **范围**：新建 `storage/SVC` 同构骨架；`01-data-flow` 三图 + Demo ODS 真源锁定；`00-context` 写清与 ENT 主数据边界；更新 `storage/README` 登记 SVC。
- **对照**：`storage/ENT/*` + `storage/CHAIN/00-context.md` + `01-data-flow.md`；`architecture-baseline` D3/D6/D7；派单 `SVC-STORAGE-S1-S4-DISPATCH-2026-08-14.md`。
- **硬要求**：ODS 权威 = `doc/` xlsx；优先读 `md-extract` **国内机构要素库**；落库 `demo_gkxlumenx_ods`；**不复制** `dwd_org_base_info`；禁正式 ODS / raw as-built / L01 实查当建表真源。
- **开放项**：`OPEN-SVC-FLOW-10` = **Q-SVC-010**（阻断级，不伪闭合）；`OPEN-SVC-FLOW-08` = **Q-SVC-009**（industry 承诺 vs 文档；建表仍认 md-extract）。
- **非范围**：DDL 建表（S2）；stores 细表 approved（S3）；业务代码；改 E7 五件套；替甲方拍板准入口径。

## 偏离说明

无架构偏离。调度 cron/DAG、MinIO 现网参数登记为开放项（不阻塞拓扑会签）。  
**Q-SVC-010 保持阻断**：圈定层在图中明示，Demo 临时规则须标待核验，正式契约不得标 live。

## 产物清单

| 产物 | 路径 |
|---|---|
| 会签主件（approved） | `agent-delivery/data/data-design/storage/SVC/01-data-flow.md` |
| SVC 入口 / 上下文 | `…/storage/SVC/{README,00-context,CHANGELOG}.md` |
| sources / etl / seeds / stores 占位 | `…/storage/SVC/**` |
| Demo 口径 | `…/storage/SVC/etl/pipeline-demo-mock.md` |
| 体系规范更新 | `…/storage/README.md` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01.md` |

## 验收证据

- [x] 三图与基线一致（批处理 / 在线读 / 对象产物）；每图含 生产者\|消费者\|触发\|失败语义\|禁止事项
- [x] 无空白「待填」无说明
- [x] ODS 真源写死：`doc/` xlsx + 优先 `md-extract` 国内机构要素库；Demo = `demo_gkxlumenx_ods`
- [x] `00-context`：不复制 `dwd_org_base_info`；机构主体权威 = ENT
- [x] `OPEN-SVC-FLOW-*` 含 Q-SVC-010（FLOW-10，阻断级）与 Q-SVC-009（FLOW-08）
- [x] `storage/README.md` 已登记 SVC
- [x] 下游放行条款已写：**S2 必须按在线文档建表**；人签前不得开工
- [x] **人签** `signoff_by=human:侯佳伟` / `signoff_status=approved`（2026-08-14 · 本地未 push）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链 前端→Java→Python | ✅ |
| 3 | 图谱 NebulaGraph | ✅ |
| 4 | 可观测性 | ✅ N/A（文档会签） |
| 5 | CI/CD | ✅ skip（definition · `cicd: skip_design_only`） |
| 6 | demo 不污染 lumen | ✅ 仅 orchestration 文档 |
| 7 | 方案 A | ✅ Java 只读 ADS + Feign |
| 8 | 数据走 ADS（D3/D7） | ✅ |
| 9 | D8 | ✅ N/A |
| 10 | D9/D10 | ✅ N/A（存储流图；指标口径另轨 METRIC-OPEN） |

## 决议

**通过（`signoff_status: approved`）**

- `signoff_by: human:侯佳伟`
- `signoff_at: 2026-08-14`
- 主件 `status: approved`
- 本地会签；**git 未 push**（监管人择机提交）

## 下游放行说明

| 阶段 | 结论 |
|---|---|
| **S2** `DATA-SVC-STORAGE-S2-L01` | **放行开工**：按 md-extract「国内机构要素库」在 `demo_gkxlumenx_ods` **核对/补齐**（含 `industry*`）；复用 ENT 同实例；禁止只写清单；禁止写正式 `gkxlumenx_ods`；**禁止**再建一套 `dwd_org_base_info` |
| **S3** stores | 流图会签 ≠ 细表 approved；Q-SVC-010 未决策前圈定表不标 live |
| 旧稿 | 冲突以 `storage/SVC` 为准；L01 / v1 域设计非 ODS 真源 |

## CI/CD

- 分支：编排仓文档（`cicd: skip_design_only`）
- commit / pipeline：待监管人提交
- K8s：skip（definition）

## cost（完工回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | TBD（会话估算后回填） |
| model_used | Cursor Grok 4.6 |
| actual_cost | TBD |
| cost_warn | false |
