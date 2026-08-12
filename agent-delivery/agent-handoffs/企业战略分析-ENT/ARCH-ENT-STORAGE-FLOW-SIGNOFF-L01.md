# ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01 · 企业维存储端到端数据流图会签

> 日期：2026-08-12  
> Task：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01`  
> 会签主件：`agent-delivery/data/data-design/storage/ENT/01-data-flow.md`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（负责人亲自认领执行） |
| 协作 | `architect-agent` 辅助改稿与基线对照；**签字权 = human:淮政玮** |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | definition / 架构会签，不以缩代码为目标；未跳过架构铁律交付 |

## 范围与实现

- **范围**：`storage/ENT` S1 流图会签（三图 + 触发/失败语义 + §4 清单 + frontmatter）。
- **对照**：`storage/README.md` 体系规范；`architecture-baseline` D3/D6/D7 与调用链。
- **实现**：审定并更新 `01-data-flow.md` → `signoff_status=approved`；登记 OPEN-ENT-FLOW-01~04；结论放行 S2/S3。
- **非范围**：旧 `data-design/企业/*`、stores as-built 灌入、业务代码、功能设计评审。

## 偏离说明

无架构偏离。调度 cron/DAG、MinIO 现网参数未在流图层写死，显式登记为开放项（不阻塞拓扑会签）。

## 产物清单

| 产物 | 路径 |
|---|---|
| 会签主件（approved） | `agent-delivery/data/data-design/storage/ENT/01-data-flow.md` |
| ENT 入口状态刷新 | `…/storage/ENT/README.md` |
| 上下文下一步刷新 | `…/storage/ENT/00-context.md` |
| CHANGELOG | `…/storage/ENT/CHANGELOG.md` |
| 本 handoff | `agent-delivery/agent-handoffs/企业战略分析-ENT/ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md` |

## 验收证据

- [x] 三图与基线一致（批处理 / 在线读 / 对象产物）
- [x] 触发与失败语义表已填；无空白「待填」
- [x] §4 会签清单全部勾选
- [x] frontmatter：`signoff_status=approved`，`signoff_by=human:淮政玮`，`signoff_at=2026-08-12`
- [x] 下游放行结论已写（S2/S3 放行；stores 细表不得仅凭流图标 approved）
- [x] **会签通过**（definition）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 流图：Python 写 ADS/ES/Nebula/MinIO；Java 无算法 |
| 2 | 调用链 前端→Java→Python | ✅ 图 2；禁越层 |
| 3 | 图谱 NebulaGraph | ✅；禁 Neo4j |
| 4 | 可观测性 | ✅ N/A（文档会签；在线路径保留统一错误体+trace 约定） |
| 5 | CI/CD | ✅ skip（definition / 设计类） |
| 6 | demo 不污染 lumen | ✅ 仅改 orchestration 文档 |
| 7 | 方案 A 共享聚合 | ✅ Java 聚合只读 ADS + Feign |
| 8 | 数据走 ADS（D3/D7） | ✅ ADS 契约面；工厂 ODS→DWD→ADS；Mock→ADS |
| 9 | D8 前端规范 | ✅ N/A（无 UI） |
| 10 | D9/D10 | ✅ N/A（存储流图；指标真源仍 metrics/policy） |

## 决议

**通过（`signoff_status: approved`）**

- `signoff_by: human:淮政玮`
- `signoff_at: 2026-08-12`
- 主件 `status: approved`

改稿要点（相对会签前 draft）：

1. 三张 Mermaid 补全角色标注。
2. 「触发 / 失败语义」写满；具体 cron/bucket → 开放项。
3. §4 勾选；§5 开放项；§6 下游放行。

## 与 architecture-baseline 对照

| 基线条目 | 结论 |
|---|---|
| 调用链 | ✅ |
| D3 Java 只读 ADS | ✅ |
| D6 NebulaGraph | ✅ |
| D7 工厂 + Mock | ✅ |
| 仅 MySQL / 无 PG | ✅ |
| MinIO 对象面 + 元数据 MySQL | ✅ |

## 开放项

| ID | 摘要 | 关闭阶段 |
|---|---|---|
| OPEN-ENT-FLOW-01 | GDF 调度 cron/DAG/门禁路径（含 Demo 模拟调度对齐） | S2 etl |
| OPEN-ENT-FLOW-02 | MinIO 现网 Endpoint/bucket/TTL | platform/minio.md |
| OPEN-ENT-FLOW-03 | ENT 对象前缀与任务表对照 | S2 pipeline-to-minio |
| OPEN-ENT-FLOW-04 | ES/Nebula 同步失败 SLA | S2/S3 |
| OPEN-ENT-FLOW-05 | 三方 ODS **在线约定文档**入口（Demo ODS 真源） | S2 sources |
| OPEN-ENT-FLOW-06 | `demo_*` 库/桶/Nebula 命名 + LLM Mock 入口 | S2 |
| OPEN-ENT-FLOW-07 | seeds 覆盖矩阵（场景 × 数据特点） | S2 seeds |

## 补记（2026-08-12 · 会签人确认 Demo/Mock 口径）

**决议**：Demo 灌数主路径正式定为：

1. **ETL 工程调度模拟 GDF**（与正式同构，不另造加工拓扑）。
2. **LLM** 向 `demo_***` 库、MinIO `demo_**` 桶、Nebula `demo_**` 写入 Mock。
3. Mock **完整依靠模型**写入 **ODS**；ODS 表结构以 **与三方约定的在线文档**为准，**不以**现网三方库 as-built 为准——屏蔽三方进度导致的结构不一致，稳定内部全链路研发。
4. 样本量：按数据特点与场景的**少量覆盖集**；**先不考虑性能**，完成全链路开发/测试闭环。

真源文档：

- `storage/ENT/01-data-flow.md` §7  
- `storage/ENT/etl/pipeline-demo-mock.md`（`status: approved`）  
- `storage/README.md` §5.1  
- `storage/ENT/seeds/README.md`  

直写 ADS 仅为旁路，**不得**冒充全链路验收。

## 下游放行结论

| 阶段 | 结论 |
|---|---|
| S2 sources + etl | **放行** |
| S3 stores as-built 灌入 | **放行灌入**；细表 `approved` 须另评 |
| S4 legacy stub | 暂缓至 S3 有实质内容 |
| 旧 `data-design/企业/*` | 本单**未改** |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 38000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.45 |
| cost_warn | green |

（已同步写入 task-registry）

## CI/CD

- 仓：`gkx-orchestration`（文档-only）
- cicd：skip（definition）
- 部署：N/A

## 明确未做

- 未写业务代码；未灌 stores as-built；未评审功能设计；未改 `data-design/企业/*`

## 签字

- 会签：`human:淮政玮` · 2026-08-12 · **approved** · **会签通过**
- 协作改稿对照：`architect-agent`
