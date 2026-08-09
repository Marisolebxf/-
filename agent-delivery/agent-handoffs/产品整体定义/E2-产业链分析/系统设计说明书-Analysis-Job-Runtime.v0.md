# 系统设计说明书 · 产业链「生成分析」Analysis Job Runtime

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.9-draft |
| 日期 | 2026-08-09 |
| 状态 | 讨论定稿草案（非正式架构基线冻结）；实现前须架构师/PM 会签 |
| 样板键 | `chain:diagnosis:key_link`（关键环节） |
| 扩展 | 周期 / 瓶颈 / 区域 / 深圳（同构，见 ISOMORPH） |
| 会话产物真源目录 | `CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/` |
| 工程范式 | Harness × Graph（外）+ Prompt/Context/Loop（仅 LLM 节点内） |

---

## 1. 文档目的与读者

本文把「生成分析」从产品交互落到**可实现的系统**：谁存什么、谁调谁、状态怎么走、算法图怎么跑、前端怎么轮询、按何顺序交付。

| 读者 | 读哪些章 |
| --- | --- |
| 架构 / Tech Lead | §2～§6、§9、§11（**必读 §3、§5.3 端到端、§11**） |
| Java（api-agent） | §3.3、§5、**§5.3**、§6、§7、§10.1、§11.3～11.4 |
| Python（algorithm-agent） | §3.2～§3.6、§5、**§5.3**、§8、§9、§10.2、§11.2～11.5 |
| 前端（frontend-agent） | §4、**§5.3**、§6、§7.1、§10.3、§11.1 / §11.4 B5 |
| QA / 验收 | §3.1、§4、**§5.3**、§10 DoD、§11.5、附录 A |

**不是**：Cursor 团队编排智能体说明书；不是招标 PDF 替代品。业务范围仍以 Bid + 产品五件套为准。

---

## 2. 背景与问题

### 2.1 业务问题

用户在「产业运行诊断 / 区域产业评价 / 深圳产业决策」等页点击 **生成分析** 后，需要：

1. 创建可恢复的长耗时任务（离开页面不丢）  
2. 看见 Bid 规定的过程阶段文案  
3. 得到**不可变**结构化结果，再显式查看、再可选生成报告  

### 2.2 工程问题

- 现有 `GET /v1/chain/**` 是**同步 ADS 查询**，不是带快照的 Job。  
- 若只堆 Prompt，没有 Job/校验/快照，无法审计、无法与 SYS-JOBS 对齐。  
- 须遵守调用链：**前端 → Java REST → Python `/internal/*`**；算法只在 Python。

### 2.3 设计目标

| 目标 | 说明 |
| --- | --- |
| 可恢复 | 刷新/重登恢复同一 `task_id` |
| 可审计 | Input/Result Snapshot 冻结；指标带 honesty/gap |
| 可扩展 | 新 analysis_key = 新 Graph + draft/result shape，不换厨房 |
| 可降级 | 检索/LLM 可空叙述，禁止假「实时全网检索完成」 |
| 体验一致 | `succeeded_wait_view`：算完不停自动进结果 |

### 2.4 非目标（v0）

- 给业务用户可视化拖拽改流程（n8n 式编辑器）  
- 开放式 ReAct Agent 自行规划调库  
- 报告任务内重跑分析  
- 前端直连大模型  

---

## 3. 概念模型（入门）

```text
用户点「生成分析」
    → Job（订单）
    → Input Snapshot（下单冻住的原料）
    → Harness 托管一次 Graph 运行（护栏 + 阶段上报 + 终态）
    → Analysis Graph（预先声明的固定菜谱节点）
    → Stage Events（过程 Steps）
    → Result Snapshot（不可变成品）
    → 用户显式「查看分析结果」
    → （可选）报告 Job 只读 Result
```

| 名词 | 定义 |
| --- | --- |
| **Analysis Job Runtime** | 生产侧整套「厨房」：Java 状态机/快照/互斥/回调门禁 + Python Graph Runner + 契约。**不是** Cursor 编排 agent，也不是开放式 ReAct |
| **Harness（护栏层）** | 让 Graph **可托管、可审计、可失败、可降级** 的控制面：超时、幂等、Stage/Complete、Schema 门禁、`limits`、Worker 锁、LLM 小环上限。详见 §3.1 |
| **Graph（菜谱层）** | 某一 `analysis_key` 的**预先声明**线性节点流水线（如 `key_link.graph.v1`）；节点读写 **Artifact**，对外映射 Bid `stage_code`。详见 §3.2 |
| Job | 一次分析运行；大状态机真源在 Java |
| `task_type` | `chain:{module}:{analysis_key}`，互斥键，不含业务参数 |
| Input Snapshot | Create 时冻结的对象/参数/规则/版本 |
| Result Snapshot | Complete 成功后 Java 签发的不可变结果 |
| Artifact | 节点间结构化中间产物（托盘）；不把 LLM 原文当隐式状态 |
| Context / Prompt Pack | **仅** LLM 子节点使用的事实托盘与提示版本（Context / Prompt engineering） |
| Loop（小环） | **仅** LLM 节点内：校验失败 → 有限重试 → 降级；受 Harness `llm_retry_max` 约束 |

### 3.1 一句话纠偏（不要说成「Python 跑固定 Graph」）

更准确的说法是：

> **Runtime 用 Harness 托管一次 Graph 执行**；Graph 是固定菜谱，Harness 是托管与护栏。  
> Python 实现 **Graph Runner + 节点内局部 Harness**；Java 实现 **Job 级外层 Harness**（生命周期与快照权威）。  
> Prompt / Context / Loop **不是**整条流水线的主体，只出现在允许 LLM 的节点（关键样板 = N4c）。

对比常见误解：

| 易误解说法 | 本设计实际含义 |
| --- | --- |
| 「做成 n8n/Coze 那种可视化 Agent」 | **形态像流水线**（阶段可见），**实现是代码内声明的 Graph**；v0 不给业务用户拖拽改图 |
| 「大模型自己规划怎么分析」 | **禁止**开放规划；节点顺序写死在 `graph_version` |
| 「Python 跑固定 Graph」 | 对一半：Python **执行** Graph，但稳定性靠 **双侧 Harness**，不是裸跑脚本 |
| 「全程 Prompt engineering」 | 多数节点是查库/规则/打分；Prompt 只服务叙述类子步 |

### 3.2 五层工程范式如何落在 Runtime 上

会话起点的五类工程，在本系统里**分层嵌套**，不是五个并列微服务：

```text
┌─────────────────────────────────────────────────────────────┐
│ Analysis Job Runtime（整厨房）                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Harness engineering（护栏 / 托管）                      │  │
│  │  Java：Create·互斥·入队·超时·Stage落库·Complete门禁     │  │
│  │  Python：Worker锁·按节点 ReportStage·limits·降级策略     │  │
│  │    ┌─────────────────────────────────────────────┐    │  │
│  │    │ Graph engineering（固定菜谱）                 │    │  │
│  │    │  N1→N2→N3→N4→N5 · Artifact · stage_code     │    │  │
│  │    │    ┌───────────────────────────────────┐    │    │  │
│  │    │    │ 仅 LLM 子节点（如 N4c）            │    │    │  │
│  │    │    │  Context eng. → Prompt eng.       │    │    │  │
│  │    │    │  → Loop eng.（≤ llm_retry_max）     │    │    │  │
│  │    │    └───────────────────────────────────┘    │    │  │
│  │    └─────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

| 范式 | 本 Runtime 里「做什么」 | 「不做什么」 | 真源产物 |
| --- | --- | --- | --- |
| **Harness** | 超时/重投幂等；Stage/Complete 契约；Schema 双检；`limits`；失败码；叙述可降级；禁止假检索完成 | 替业务决定「谁是关键」；开放 tool 自规划 | CONTRACT + OpenAPI `limits` + Complete 门禁 |
| **Graph** | 声明节点序、读/写 Artifact、映射 Bid 五句 stage | 运行时改拓扑；并行开放分支（v1） | `GRAPH-key_link.v0.md` + `graph_version` |
| **Context** | 给 LLM 装**已算定事实**托盘（五环节、关键依据、企业短名单…） | 塞整库、可改权重暗示 | `n4c_context_pack` schema |
| **Prompt** | 系统/用户模板版本化；输出契约；禁止项 | 让模型改分数/改关键布尔 | `PROMPT-PACK-key_link-n4c.v0.md` |
| **Loop** | Schema/事实冲突 → 有限重试 → 降级空叙述 | 无限 ReAct；整 Job 回滚重跑 Graph | Prompt Pack 内 Loop 规则 + `llm_retry_max` |

### 3.3 Harness 实践清单（实现时对照）

把 Harness 拆成**外层（Java）**与**内层（Python）**，避免「护栏全塞进算法进程」或「算法自签结果」。

| 层级 | 实践项 | 行为 |
| --- | --- | --- |
| 外·Java | Job 状态机 | `queued→running→succeeded\|failed`；`withdrawn` 仅排队 |
| 外·Java | 快照权威 | 签发 `input_snapshot_id` / `result_snapshot_id`；Python 不得自造 result id |
| 外·Java | 互斥与幂等 | 同用户同 `task_type`；`client_request_id` / `event_id` / `complete_event_id` |
| 外·Java | 调度护栏 | Execute 超时 → `JOB_TIMEOUT`；重投不双开 Completes |
| 外·Java | Complete 门禁 | 校验 `result_payload` schema + 跨字段不变量 → 才 `succeeded` |
| 内·Python | Graph Runner | 严格按 `graph_version` 线性推进；节点失败 → `Complete(failed)` |
| 内·Python | Stage 上报 | 每节点 `ReportStage(started→succeeded\|failed)`；对外不暴露 4a/4b/4c |
| 内·Python | `limits` | 消费 Execute 下发的超时/重试上限（如 `llm_retry_max`） |
| 内·Python | 降级策略 | LLM 用尽重试 → 空叙述 + `degraded`；**不**伪造「实时全网检索完成」 |
| 内·Python | Worker 锁 | 同一 `task_id` 禁止双 Worker 并行跑图 |

**Harness 与 Graph 的边界口诀**：Graph 回答「下一步算什么」；Harness 回答「算失败了怎么办、算到哪了告诉谁、什么叫算完、谁有权盖章」。

### 3.4 Graph 实践清单（实现时对照）

| 实践项 | 关键样板做法 |
| --- | --- |
| 版本钉死 | Execute 带 `graph_version=key_link.graph.v1`；改拓扑必须升版本 |
| 线性拓扑 | N1→N2→N3→N4→N5；v1 无开放边、无模型选下一跳 |
| 节点契约 | 每节点：读 Artifact+Input → 做事 → ReportStage → 写 Artifact |
| 确定性优先 | N3 打分、N4a 关键判定 = 规则/计算；禁止 LLM 改数字与布尔 |
| LLM 收口 | 仅 N4c；先 Context Pack，再 Prompt，再 Loop，再写入 `art.narrative` |
| 终局组装 | N5 校验不变量后交 `result_payload`；不改 Input、不算第二遍指数 |
| 与同步 API | 节点内可复用现有 ADS 查询函数；**对外交付只经 Job Complete** |

节点 ↔ stage 映射与 Artifact 表见 `GRAPH-key_link.v0.md`；切片 S1–S5 见 `SLICE-PLAN-key_link-S1-S5.v0.md`。

### 3.5 一次运行的时序（Harness 包着 Graph）

```text
FE ──Create──► Java Harness：冻 Input、互斥、queued
Java ──Execute(input, graph_version, limits, callbacks)──► Python
Python Harness：加锁 → 选 Graph Runner(graph_version)
  loop 节点 in Graph:
      ReportStage(started)
      执行节点（确定性 / 或 N4c: Context→Prompt→Loop）
      ReportStage(succeeded|failed)
      失败且不可恢复 → Complete(failed) → 结束
  N5 组装 result_payload
  Complete(succeeded, result_payload)  ──► Java Harness：Schema 门禁 → 签发 result_snapshot_id
FE 轮询 GetJob → succeeded_wait_view（不自动跳结果）
```

### 3.6 Python 执行 Graph 时，如何与「算法服务」交互？

先消歧：**架构铁律里的「算法服务」= Python `/internal/*` 能力面**；对本 Job 而言，**Java 只调一次** `Execute`，不会再为每个 Graph 节点单独调一遍「算法 REST」。

```text
┌─ Java（外层 Harness）─────────────────────────────────────┐
│  只认识一个算法入口：POST /internal/.../jobs/execute       │
│  只回收：ReportStage / Complete（回调）                    │
└────────────────────────────┬──────────────────────────────┘
                             │ 一次 Execute（带 Input + limits）
                             ▼
┌─ Python Worker（内层 Harness × Graph Runner）──────────────┐
│  Graph 节点 N1…N5 不「再扮演 Java」去调算法；               │
│  节点通过 **能力适配层** 使用算法/数据能力：                 │
│                                                            │
│   Node ──(1) 进程内函数/包──► 规则 / 打分 / 装配            │
│        ──(2) ADS/仓库读 ──► 环节、企业、指标事实            │
│        ──(3) 可选：同层 /internal 兄弟能力 ──► 已有重计算   │
│        ──(4) 仅 N4c：LLM Client ──► 模型网关               │
│                                                            │
│  节点产出只进 Artifact；对外成品只经 Complete → Java        │
└────────────────────────────────────────────────────────────┘
```

| 交互方式 | 何时用 | 关键样板 | 约束 |
| --- | --- | --- | --- |
| **(1) 进程内调用（默认）** | 规则、装配、校验、轻量计算 | N1 freeze、N4a 关键判定、N5 组装、N3 加权公式 | `import` 领域模块；**不**经 Java；结果写 Artifact |
| **(2) 读 ADS / 只读仓** | 事实数据 | N2 五环节骨架、N3 因子原始值、N4b 企业名单 | 只读；失败 → `ADS_UNAVAILABLE` 或图内降级策略 |
| **(3) 同层 Python 能力 HTTP（可选）** | 已有独立 `/internal` 重服务、不宜再拷逻辑 | 复用「关键节点查询」等底层实现 | **Python→Python**；超时计入节点；仍写 Artifact；**禁止**绕回 Java 再 Feign |
| **(4) LLM Client（例外）** | 叙述类子步 | 仅 N4c | Context Pack → Prompt → Loop≤`llm_retry_max`；校验失败可降级空叙述 |

**与「现有同步 `GET /v1/chain/**`」的关系**：

- 那是 **Java 对外的只读查询门面**，不是 Graph 节点该调的路径。  
- Graph 应复用其 **底层查询/计算函数**（同仓 Python 模块或同层 `/internal`），把结果升格为 Job Artifact / Result，而不是让 Worker 去打用户侧 REST。

**禁止的交互**：

| 禁止 | 原因 |
| --- | --- |
| 节点回调 Java「请帮我算关键」 | 调用链倒挂；Java 不写算法 |
| 节点直打前端可见 API | 鉴权/契约混乱；破坏 Snapshot 封闭 |
| 每个节点让 Java 再 Execute 一次 | Job 碎片化；互斥与 stage 语义崩溃 |
| LLM 节点改分数 / 改 `is_key_node` | 确定性被破坏 |

**实现口诀**：Java 调的是 **Job 级算法入口**；Graph 调的是 **节点级能力函数**。二者都是「算法」，但 **不是同一跳 HTTP**。

---

## 4. 与产品体验的对齐

产品包：`CHAIN-TOPIC-DIAGNOSIS` / `REGIONAL` / `SHENZHEN` + `SYS-ANALYSIS-JOBS`。

### 4.1 页面主模式

| 模式 | 路由意图 | 对应 Job |
| --- | --- | --- |
| Config | 默认配置 | 无 Job 或已撤回 |
| Process | `demo_state=processing` | queued / running / succeeded(wait) / failed |
| Result | `demo_state=result` | succeeded 且用户显式进入 |
| Records | `tab=records` | 历史多行 |

### 4.2 Job.status → UI（摘要）

| status | 页面 | 备注 |
| --- | --- | --- |
| queued | Process | 可撤回 |
| running | Process | 不可取消；Steps 跟 Events |
| succeeded | Process 默认 wait_view | **禁止自动跳 Result** |
| failed | Process 失败态 | 新 task_id 重试 |
| withdrawn | Config | 释放互斥 |

细节见会话结论 A；OpenAPI `page_mode_hint` / `allow_*` 字段。

---

## 5. 逻辑架构

> 分层语义见 **§3**：本图中的 Java = Job 级外层 Harness；Python = Graph Runner + 节点内局部 Harness。

```text
┌──────────────┐     Create/Get/Events/Withdraw      ┌─────────────────────┐
│  专题前端     │ ──────────────────────────────────► │  Java Analysis Runtime│
│ industry-center│ ◄──────────────────────────────── │  = 外层 Harness       │
└──────────────┘     Job 投影 / result_snapshot_id   │  + Snapshot Store     │
                                                      └──────────┬──────────┘
                                                                 │ Execute
                                                                 │ (input_snapshot_id
                                                                 │  + graph_version
                                                                 │  + limits
                                                                 │  + callback URLs)
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │ Python Worker       │
                                                      │ = 内层 Harness      │
                                                      │   × Graph Runner    │
                                                      │ (key_link.graph.v1) │
                                                      │ ADS / Rules / LLM*  │
                                                      └──────────┬──────────┘
                                                                 │ ReportStage ×N
                                                                 │ Complete(result_payload)
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │ Java Complete 门禁  │
                                                      │ 校验 Schema         │
                                                      │ 签发 result_snapshot│
                                                      │ status=succeeded    │
                                                      └─────────────────────┘
* LLM 仅出现在 Graph 允许的节点（关键 = N4c），且套在 Context→Prompt→Loop 小环内。
```

**已决策**：Python → Java **回调**（非 Java 轮询 Python）。  
前端只轮询 Java GetJob（+ ListEvents）。

### 5.1 模块职责

| 模块 | 职责 | 不职责 |
| --- | --- | --- |
| 前端 | 配置校验展示、建单、过程壳、显式看结果、报告触发 | 假推进 stage、直连 Python/LLM、充当 Harness |
| Java Runtime | **外层 Harness**：互斥/队列/状态机、Snapshot、回调鉴权、Complete Schema 门禁、SYS-JOBS | 算高端化指数、写 nGQL 算法、执行 Graph 节点 |
| Python Worker | **内层 Harness × Graph Runner**：按 `graph_version` 跑节点、ReportStage、交 result_payload；LLM 节点内 Context/Prompt/Loop | 签发 result_snapshot_id、管用户互斥 |
| ADS/指标 | 事实与口径 | — |
| 报告服务 | 只读 Result 出文件 | 重跑分析 |

### 5.2 Snapshot ID 所有权

| ID | 签发 | 持久化 |
| --- | --- | --- |
| `task_id` | Java | Java |
| `input_snapshot_id` | Java（Create） | Java |
| `result_snapshot_id` | Java（Complete 校验后） | Java |
| Python | 只带回 `input_snapshot_id` + payload | 不自造 result id |

### 5.3 端到端运行时完整例子（关键 `key_link`）

> 场景：用户在「产业运行诊断 → 关键环节」点 **生成分析**，跑到成功，停在 wait_view，再显式查看结果。  
> 路径以 OpenAPI 草稿为准；载荷可裁剪，字段名对齐 `openapi-analysis-job.v0.yaml`。  
> **通知前端的方式**：无 WebSocket 推送要求；前端 **轮询** `GetAnalysisJob`（+ 可选 `ListEvents`）。Python **不**直连前端。

#### 0) 总时序

```text
FE                         Java                              Python Worker
│ ① POST Create            │                                   │
│─────────────────────────►│ 冻 Input、互斥、queued             │
│◄── task_id, process_route│                                   │
│ 跳转过程页，开始轮询      │                                   │
│                          │ ② POST Execute (graph_version…)   │
│                          │──────────────────────────────────►│ 202 Accepted
│                          │ status→running                    │ ③ get_graph(v1)
│                          │                                   │    for NODES…
│ ④ GET Job / Events       │◄──── ⑤ ReportStage ×10（5×起止）──│
│◄── stage 推进 UI Steps   │ 落 event、更新 current_stage_*    │
│                          │◄──── ⑥ Complete(succeeded) ───────│
│                          │ 校 schema、签发 res_kl_001        │
│                          │ status→succeeded                  │
│ ⑦ GET Job                │                                   │
│◄── page_mode_hint=       │                                   │
│    process_succeeded_    │                                   │
│    wait_view             │  ← 停在此，不自动跳结果            │
│ 用户点「查看分析结果」    │                                   │
│ ⑧ GET Result Snapshot    │                                   │
│◄── sections…             │                                   │
```

#### 1) 前端发起 Create

`POST /topic/v1/analysis-jobs`

```json
{
  "task_type": "chain:diagnosis:key_link",
  "analysis_key": "key_link",
  "client_request_id": "idem_fe_20260809_001",
  "retry_from_task_id": null,
  "draft": {
    "object": {
      "type": "industry_chain",
      "chain_id": "chain_semiconductor_lighting",
      "parent_industry_id": "ind_semiconductor_lighting"
    },
    "factors": {
      "pack_id": "diag_key_link_factors",
      "pack_version": "2026.08.01",
      "user_confirmed": true
    },
    "ui": {
      "route_path": "/industry-center/diagnosis",
      "tab": "key-link"
    }
  }
}
```

Java 动作（外层 Harness）：

1. 校验 draft / 因子只读确认  
2. 同用户同 `task_type` 互斥（若已有非终态 → `reused: true` 返回旧 task）  
3. 签发 `input_snapshot_id=ins_kl_001`，落 Input Snapshot  
4. 建 Job：`task_id=tsk_kl_001`，`status=queued`，记下 `graph_version=key_link.graph.v1`  
5. 入队调度 Execute  

响应示例：

```json
{
  "task_id": "tsk_kl_001",
  "task_type": "chain:diagnosis:key_link",
  "status": "queued",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": null,
  "reused": false,
  "process_route": "/industry-center/diagnosis?tab=key-link&demo_state=processing&task_id=tsk_kl_001",
  "result_route": "/industry-center/diagnosis?tab=key-link&demo_state=result&task_id=tsk_kl_001",
  "trace_id": "tr_abc"
}
```

前端动作：

- `navigate(process_route)`  
- 启动轮询：每 2～3s `GET .../analysis-jobs/tsk_kl_001`；可选 `GET .../events`  
- **禁止**本地 `setTimeout` 假推进 Steps  

#### 2) Java → Python Execute（加载图的入口）

`POST /internal/v1/chain/jobs/execute`（服务身份）

```json
{
  "task_id": "tsk_kl_001",
  "task_type": "chain:diagnosis:key_link",
  "analysis_key": "key_link",
  "graph_version": "key_link.graph.v1",
  "input_snapshot_id": "ins_kl_001",
  "input_payload": {
    "object": {
      "type": "industry_chain",
      "chain_id": "chain_semiconductor_lighting",
      "parent_industry_id": "ind_semiconductor_lighting",
      "display_name": "半导体照明产业链"
    },
    "factors": {
      "pack_id": "diag_key_link_factors",
      "pack_version": "2026.08.01",
      "user_confirmed": true,
      "items": [
        { "factor_key": "value_added_rate", "status": "ready" },
        { "factor_key": "tech_barrier", "status": "ready" },
        { "factor_key": "market_concentration", "status": "ready" }
      ]
    },
    "rules": {
      "key_node_criterion": { "source": "temp_default", "qc_ref": "QC02", "top_pct_by_enterprise_count": 0.2 }
    },
    "honesty": { "pending": ["QC02"], "mock_metrics": ["GAP-CHAIN-DIAG-METRICS"] }
  },
  "limits": {
    "job_timeout_sec": 900,
    "llm_retry_max": 2
  },
  "callbacks": {
    "stage_url": "https://java-internal/internal/v1/analysis-jobs/tsk_kl_001/stages",
    "complete_url": "https://java-internal/internal/v1/analysis-jobs/tsk_kl_001/complete"
  },
  "trace_id": "tr_abc"
}
```

Python 立即 `202 Accepted`；Worker 异步开跑。Java 将 Job 标为 `running`。

#### 3) Python「加载」Graph 并执行（代码即图）

```python
# Worker 伪代码（与 §11.3.1 一致）
nodes = GRAPH_REGISTRY[body["graph_version"]]
# → [("freeze", freeze.run), ("structure", ...), ... ("validate_assemble", ...)]

arts = {"input": body["input_payload"]}
for stage_code, node_fn in nodes:
    await report_stage(started)
    arts = await node_fn(arts, limits=body["limits"])  # 内调 ADS/规则/LLM
    await report_stage(succeeded)
await complete(succeeded, arts["result_payload"])
```

节点与 Bid 文案对应：

| # | stage_code | stage_label（上报用） |
| --- | --- | --- |
| 1 | `freeze` | 任务提交与产业链对象冻结 |
| 2 | `structure` | 全链路环节结构化拆解（研发/设计/制造/销售/服务） |
| 3 | `score_high_end` | 基于附加值率、技术壁垒、市场集中度计算高端化指数 |
| 4 | `annotate` | 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 |
| 5 | `validate_assemble` | 结果可信性校验与分析报告组装 |

#### 4) 前端轮询「通知」自己（进行中）

`GET /topic/v1/analysis-jobs/tsk_kl_001` → 例如跑到第 3 步时：

```json
{
  "task_id": "tsk_kl_001",
  "status": "running",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": null,
  "object_summary": "半导体照明产业链",
  "current_stage_code": "score_high_end",
  "current_stage_label": "基于附加值率、技术壁垒、市场集中度计算高端化指数",
  "stage_index": 3,
  "stage_total": 5,
  "elapsed_sec": 84,
  "allow_withdraw": false,
  "allow_view_result": false,
  "page_mode_hint": "process_running",
  "process_route": "/industry-center/diagnosis?tab=key-link&demo_state=processing&task_id=tsk_kl_001",
  "result_route": "/industry-center/diagnosis?tab=key-link&demo_state=result&task_id=tsk_kl_001",
  "trace_id": "tr_abc"
}
```

前端：用 `current_stage_*` / `stage_index` 点亮 Steps；`page_mode_hint=process_running` 保持过程壳。

可选 `GET .../events?after_event_id=`：

```json
{
  "items": [
    {
      "event_id": "evt_01",
      "stage_code": "freeze",
      "stage_label": "任务提交与产业链对象冻结",
      "status": "started",
      "at": "2026-08-09T22:40:31+08:00"
    },
    {
      "event_id": "evt_02",
      "stage_code": "freeze",
      "stage_label": "任务提交与产业链对象冻结",
      "status": "succeeded",
      "at": "2026-08-09T22:40:32+08:00"
    }
  ]
}
```

#### 5) Python → Java ReportStage（内网回调）

每节点至少一对 `started` / `succeeded`。示例（`structure` 开始）：

`POST /internal/v1/analysis-jobs/tsk_kl_001/stages`

```json
{
  "event_id": "evt_03",
  "stage_code": "structure",
  "stage_label": "全链路环节结构化拆解（研发/设计/制造/销售/服务）",
  "status": "started",
  "at": "2026-08-09T22:40:33+08:00",
  "message": null,
  "degraded": false,
  "trace_id": "tr_abc"
}
```

Java：幂等写 `analysis_job_event`；更新 Job 的 `current_stage_*` / `stage_index`。  
**前端下一轮 GetJob 即可看见推进——这就是「通知前端」的路径。**

#### 6) Python → Java Complete（成功收口）

`POST /internal/v1/analysis-jobs/tsk_kl_001/complete`

```json
{
  "complete_event_id": "cmp_01",
  "outcome": "succeeded",
  "result_schema_version": "chain.key_link.result.v1",
  "result_payload": {
    "result_title": "半导体照明产业链 · 关键环节识别",
    "summary": {
      "key_node_count": 2,
      "headline": "制造与研发环节被标为关键（规则 QC02 临时默认）"
    },
    "sections": {
      "chain_structure": { "stages": ["…五环节…"], "edges": ["…"] },
      "annotations": { "items": ["…"] },
      "competition": { "items": [], "degraded": true },
      "representative_enterprises": { "items": ["…"] },
      "tech_trends": { "items": [], "degraded": true }
    },
    "metrics_used": ["…"],
    "evidence_refs": ["…"],
    "honesty": { "pending": ["QC02"], "degraded_narrative": true }
  },
  "error_code": null,
  "failed_stage_code": null,
  "trace_id": "tr_abc"
}
```

注意：payload **不含** `result_snapshot_id`。

Java Complete 门禁：

1. 校验 `result_payload` schema + 不变量（如 `key_node_count` 一致）  
2. 签发 `result_snapshot_id=res_kl_001`，落 Result Snapshot  
3. Job → `status=succeeded`，`finished_at` 赋值  
4. **不**要求前端自动跳转  

#### 7) 前端轮询到终态（「算完了」的通知）

`GET /topic/v1/analysis-jobs/tsk_kl_001`

```json
{
  "task_id": "tsk_kl_001",
  "status": "succeeded",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": "res_kl_001",
  "current_stage_code": "validate_assemble",
  "current_stage_label": "结果可信性校验与分析报告组装",
  "stage_index": 5,
  "stage_total": 5,
  "elapsed_sec": 210,
  "finished_at": "2026-08-09T22:55:00+08:00",
  "allow_withdraw": false,
  "allow_view_result": true,
  "page_mode_hint": "process_succeeded_wait_view",
  "process_route": "/industry-center/diagnosis?tab=key-link&demo_state=processing&task_id=tsk_kl_001",
  "result_route": "/industry-center/diagnosis?tab=key-link&demo_state=result&task_id=tsk_kl_001",
  "trace_id": "tr_abc"
}
```

前端动作：

1. **停止轮询**（或降为极低频心跳）  
2. 按 `page_mode_hint` 展示 **succeeded_wait_view**（大按钮「查看分析结果」）  
3. **禁止**因 `status=succeeded` 自动 `navigate(result_route)`  

#### 8) 用户显式查看结果

用户点击后：`navigate(result_route)` 或等价打开结果模式。

`GET /topic/v1/analysis-results/res_kl_001`  
→ 返回冻结的 `result_payload`（sections 绑结果页）。

报告若需要：另开报告 Job，**只读** `res_kl_001`，不重跑 Graph。

#### 9) 失败时如何「通知」前端（对照）

Python `Complete(outcome=failed, error_code=ADS_UNAVAILABLE, failed_stage_code=structure)`  
→ Java `status=failed`  
→ 前端 GetJob 见 `page_mode_hint=process_failed`，展示重试（新 `task_id`，可带 `retry_from_task_id`）。

#### 10) 本例子里「加载」发生了几次？

| 时刻 | 加载的是什么 | 读方 |
| --- | --- | --- |
| Create | 用户 draft → Input Snapshot | Java |
| Execute | `graph_version` → `GRAPH_REGISTRY` → `NODES` | Python |
| 每节点 | Artifact + ADS/规则/（可选）LLM | Python 节点函数 |
| GetJob 轮询 | Job 行 + 当前 stage | 前端 ← Java |
| Complete | `result_payload` → Result Snapshot | Java 校验并签发 |
| 查看结果 | `result_snapshot_id` → 不可变结果 | 前端 ← Java |

**没有**：前端加载 Graph；Python 解析 `GRAPH-*.md`；Python 推 WebSocket 给浏览器。

---

## 6. 状态机与生命周期

### 6.1 Job 大状态

```text
(无) → Create → queued → running → succeeded
                      ↘ withdrawn（仅排队撤回）
                 running → failed
                 * → terminated（运维）
```

`running` 内靠 **stage_code** 细分，不新增 Job。

### 6.2 关键 `stage_code`（样板）

| code | Bid 文案 |
| --- | --- |
| freeze | 任务提交与产业链对象冻结 |
| structure | 全链路环节结构化拆解… |
| score_high_end | 基于三因子计算高端化指数 |
| annotate | 关键标注与格局/企业/趋势 |
| validate_assemble | 结果可信性校验与报告组装 |

其它键的 stage 枚举见 `ISOMORPH-chain-analysis-jobs.v0.md`。

### 6.3 前端轮询

- queued/running：GetJob 每 2～3s；ListEvents 可增量  
- 终态：停轮询  
- 权威在服务端，禁止本地 setTimeout 假 Steps  

---

## 7. 接口设计（摘要）

完整定义：`schemas/openapi-analysis-job.v0.yaml`（0.3.0-draft）。  
字段/错误码叙述：`CONTRACT-Java-Python-Analysis-Job-v0.md`。

### 7.1 对外（前端 → Java，`/topic/v1`）

| operationId | 方法路径 | 作用 |
| --- | --- | --- |
| createAnalysisJob | POST `/analysis-jobs` | 生成分析 |
| getAnalysisJob | GET `/analysis-jobs/{task_id}` | 过程页真源 |
| listAnalysisJobEvents | GET `.../events` | Steps 事件 |
| withdrawAnalysisJob | POST `.../withdraw` | 仅 queued |

另需（可同迭代或紧随）：`GET /analysis-results/{result_snapshot_id}` 供结果页。

### 7.2 对内投递（Java → Python）

| executeAnalysisJob | POST `/internal/v1/chain/jobs/execute` | 202 异步；带 callback |

### 7.3 对内回调（Python → Java）

| reportAnalysisJobStage | POST `.../stages` | 阶段进度 |
| completeAnalysisJob | POST `.../complete` | 成功交 payload / 失败交 error |

鉴权：用户 JWT vs 服务身份分离；回调禁止浏览器持有。

### 7.4 幂等

- Create：`client_request_id`  
- 互斥：同用户同 `task_type` 非终态 → `reused: true`  
- Stage：`event_id`  
- Complete：`complete_event_id`  

---

## 8. 数据设计（逻辑）

### 8.1 建议表（逻辑名，物理名实现时定）

| 实体 | 关键字段 |
| --- | --- |
| analysis_job | task_id, user_id, task_type, analysis_key, status, input_snapshot_id, result_snapshot_id, stage_*, error_*, timestamps, retry_from_task_id, graph_version, trace_id |
| analysis_snapshot | snapshot_id, kind(input\|result), schema_version, task_id, payload_json, created_at |
| analysis_job_event | event_id, task_id, stage_code, stage_label, status, at, message, degraded |

互斥索引：`(user_id, task_type) WHERE status IN (queued, running)` 唯一。

### 8.2 Input Snapshot（关键要点）

- object：`industry_chain`  
- factors：三因子只读确认  
- rules：含 QC02 临时默认  
- versions / honesty / ui  

### 8.3 Result Payload（关键）

Schema 总装：`chain.key_link.result_payload.v1.schema.json`

```text
result_title, summary, sections{
  chain_structure, annotations, competition,
  representative_enterprises, tech_trends
}, metrics_used, evidence_refs, honesty
```

跨字段不变量（N5/Java 双检）：关键数一致、每关键有依据、五环节齐全等。

---

## 9. 算法图设计（关键样板）

真源：`GRAPH-key_link.v0.md`。范式落位见 **§3.2～§3.4**（本节只列菜谱，不重复护栏定义）。

```text
N1 freeze → N2 structure → N3 score_high_end
         → N4 annotate(4a 规则关键 → 4b 企业 → 4c Context→Prompt→Loop)
         → N5 validate_assemble → Complete
```

| 原则 | 说明 |
| --- | --- |
| Graph = 固定菜谱 | `graph_version` 钉死线性序；v1 无开放规划 |
| Harness 包执行 | 每节点 ReportStage；失败 Complete(failed)；LLM 仅小环重试 |
| 数字确定性 | 高端化指数、是否关键由规则/计算产出 |
| LLM 边界 | 仅 N4c 格局/趋势；可降级空 |
| Prompt/Context | `PROMPT-PACK-key_link-n4c.v0.md` + Context/Output Schema |

与同步 API：Worker **可调用**现有查询函数，但对外只经 Job Complete 交付。

### 9.1 节点内并行 vs 图级并行（高端化指数能否拆成并行任务？）

可以并行，但要分清层级——**推荐只做节点内并行**，不要把 Bid 的一步拆成多条对外 Job/多条可见 stage。

#### 两种并行

| 类型 | 含义 | 对前端 / Job | 本设计态度 |
| --- | --- | --- | --- |
| **节点内并行** | 某一个 Graph 节点（如 N3 `score_high_end`）**内部**用 `asyncio.gather` / 线程池 / 进程池，并行拉三因子或按环节并算 | 仍是**一个** `stage_code`；一对 `ReportStage(started→succeeded)` | ✅ **鼓励**（性能优化） |
| **图级并行** | Graph 上分叉多条边、或多个子 Job 并行，再 join | 多 stage 或多次互斥语义；Steps/事件模型要重做 | ⚠️ v1 **不做**；不等于「工作流引擎」，但已踩到其复杂度 |

```text
✅ 推荐（节点内）：

  ReportStage(score_high_end, started)
       ┌─ 拉/算 附加值率 ─┐
       ├─ 拉/算 技术壁垒 ─┼─ gather ──► 加权合成 high_end_index（每环节）
       └─ 拉/算 市场集中度─┘
  ReportStage(score_high_end, succeeded)
  写出 art.stage_scores

❌ 不推荐（为三因子开三个对外 stage / 三个 Job）：

  score_factor_a ║ score_factor_b ║ score_factor_c → join
  → Bid 只有一句「计算高端化指数」，前端 Steps 对不齐
  → 失败重试、幂等、互斥、wait_view 语义变复杂
```

#### 以 N3「高端化指数」为例怎么拆

| 拆法 | 做法 | 是否改 `graph_version` 拓扑 |
| --- | --- | --- |
| A. 三因子并行取数/算子 | `score_high_end.run` 内 `gather(factor_value_added, factor_tech, factor_concentration)`，再按环节加权 | 否（仍一节点） |
| B. 五环节并行打分 | 三因子齐了之后 `gather(*[score(stage) for stage in stages])` | 否 |
| C. 子步骤日志（可选） | 节点内打结构化 log / span（OTel）；**不要**默认打成 Bid Steps | 否 |
| D. 拆成三个 Graph 节点对外可见 | 新增 stage_code，改过程五句 | **要**升 `graph_version` + 改产品文案（通常不值得） |
| E. 三个独立 Analysis Job | 各 Create 再汇总 | ❌ 互斥与 Snapshot 模型错误 |

示意（节点内，非仓内已落地代码）：

```python
# nodes/score_high_end.py
async def run(arts: dict, limits: dict) -> dict:
    ctx, skeleton = arts["context"], arts["chain_skeleton"]

    # 三因子并行（I/O 或轻量计算）
    value_added, tech, concentration = await asyncio.gather(
        load_factor(ctx, "value_added_rate"),
        load_factor(ctx, "tech_barrier"),
        load_factor(ctx, "market_concentration"),
    )

    # 五环节也可再并行合成指数
    async def score_one(stage):
        return weighted_high_end(stage, value_added, tech, concentration, ctx["factors"])

    scored = await asyncio.gather(*[score_one(s) for s in skeleton["stages"]])
    arts["stage_scores"] = {"stages": scored}
    return arts
```

对外仍只报：`stage_code=score_high_end`，文案仍是 Bid 那一句。

#### 失败与降级怎么定（节点内并行时）

| 策略 | 适用 |
| --- | --- |
| **一因子失败 → 整节点失败** → `Complete(failed)` / 或本 stage failed | 缺因子无法合成指数（默认更诚实） |
| 单因子 `status=missing` + 指数 `status=mock/partial` + honesty/gap | 产品允许部分因子缺口时展示（须产品点头） |
| 并行超时 | 计入节点超时；受 Execute `limits` / Job 超时约束 |

不建议：三因子各报一个成功 Stage，让前端以为「已经算完高端化」其实只做完 1/3。

#### 和「滑向工作流引擎」的关系

- **节点内并行** = 实现细节，Harness/Graph 对外契约不变 → **不是**工作流引擎。  
- **图级 fan-out/fan-in、可视化分支、子流程实例** = 才开始像工作流引擎；v1 无产品要求就不要做。  
- 已有先例：N4 的 4a/4b/4c 是**同一 `annotate` stage 内的子步骤**（可串行；4b/部分取数也可并行），前端只看见一句「关键标注…」。

**口诀**：并行用在**厨房里炒菜的双手**，不要把**菜单上的一道菜**拆成三道给客人点。

#### 图级并行长什么样？（例子）

下面用「关键」故意画成**图级 fan-out / fan-in**——这就是图级并行（v1 **不采用**，仅作对照）。

```text
                    ┌─► N3a score_value_added ────────┐
N1 freeze → N2 ─────┼─► N3b score_tech_barrier ───────┼─► N3join merge_scores
   structure        └─► N3c score_concentration ──────┘         │
                                                                ▼
                                                         N4 annotate → N5 → Complete
```

相对「节点内并行」的差别：

| | 节点内并行（✅） | 上图图级并行（⚠️） |
| --- | --- | --- |
| Graph 拓扑 | 仍是 `… → score_high_end → …` 一条线 | 出现**多条边、汇合节点** |
| `stage_code` | 对外 1 个 `score_high_end` | 至少 3～4 个 stage（或子图实例） |
| ReportStage | 一对 started/succeeded | 多路并发上报；顺序、重复、部分失败要定义 |
| 前端 Steps | Bid 一句，进度条好做 | 「三句同时亮」还是「等 join」？产品未定义 |
| 失败 | 节点失败即本 stage 失败 | N3a 成功、N3b 失败时：重试谁？join 是否降级？ |
| Job 模型 | 一个 `task_id` 线性推进 | 常要引入「子运行 / 分支状态」≈ 小工作流引擎 |

再举一个更「像引擎」的图级例子（区域评价想象态，非本设计）：

```text
N1 freeze
    ├─► branch_index（指数子图：权重×底分…）──┐
    └─► branch_radar（竞争力子图：三维打分…）──┼─► join_dashboard → Complete
```

这里是**两条业务子流水线**在 Graph 上并行，而不只是一个函数里的 `gather`。要回答：两条是否共用 Input Snapshot、谁先谁后展示、一条失败整单是否失败、join 产物 Schema——这些都是工作流引擎才好好回答的问题；我们的 Job 大状态机（queued/running/succeeded）表达起来会别扭。

**如何一眼判断自己在做图级并行？**

- 配置/代码里出现「从同一节点连出 ≥2 条后继，再在下游汇合」；或  
- 需要为分支单独存状态 / 子 `run_id`；或  
- 前端/OpenAPI 要为分支增加多个并行 `stage_code`。  

若只是 `score_high_end.py` 里 `asyncio.gather(...)`，**不是**图级并行。

---

## 10. 如何实现（分角色路线图）

与 `SLICE-PLAN-key_link-S1-S5.v0.md` 一致，此处给系统级视图。

### 10.0 总序

> 跨场景用法与「是否先定 Graph」见 **§11**。本节聚焦首键落地角色清单。

```text
并行：Java Runtime 竖切  ‖  前端过程壳（Mock Job）
        ↓
     Python S1（N1+N2+N5）
        ↓
     S2 → S3 → S4 → S5(LLM 可最后)
        ↓
     按 §11.4 / ISOMORPH 扩 bottleneck → regional → …
```

### 10.1 Java 实现清单

1. Job / Snapshot / Event 表与仓储  
2. Create：校验 draft、冻 Input、互斥、入队  
3. 调度器：调 Python Execute（超时、重投幂等）  
4. 回调控制器：Stage 落库；Complete 校 Schema → 签发 Result → 更新 status  
5. GetJob / Events / Withdraw  
6. 投影 SYS-JOBS 浮层（task_type、阶段文案、路由）  
7. OTel：task_id、stage、error_code、耗时  

**竖切 DoD**：Create→Execute→≥1 Stage→Complete→GetJob 终态；succeeded 不自动跳结果。

### 10.2 Python 实现清单

1. Execute 入口（202）+ Worker 锁防双开  
2. Graph Runner：按 stage ReportStage  
3. S1：结构五节点过 `chain_structure` schema  
4. S2～S4：打分、QC02 关键、企业卡  
5. S5：装 Context Pack → Prompt → 校验 LLM output → 映射 section 或降级  
6. Complete 只交 payload，不发明 result id  

### 10.3 前端实现清单

1. 关键 Tab 配置（对象/因子只读/生成禁用规则）  
2. 过程双 SectionPanel + Steps（文案固定）  
3. 轮询 GetJob；succeeded_wait_view 大按钮  
4. 结果页绑 result sections；报告走 ENT-EXPORT  
5. 记录 Tab：查看结果 / 复制配置  

先 Mock Job 不堵算法；再切真 API。

### 10.4 数据 / 口径

- QC02 等保持 honesty，不前端改绿  
- 指标 8 件套走既有 metric 体系  
- 正式公式闭合前允许 mock + gap_ref  

### 10.5 验收要点（样板）

- AC：过程五句必现；结果非仅关键列表；因子不可伪编辑  
- 互斥复用；排队可撤、运行不可撤  
- LLM 降级诚实；无「实时全网检索完成」  
- 架构铁律自检：调用链 / 算法在 Python / 可观测  

---

## 11. 多场景怎么用 · 开发步骤（先定 Graph 吗？）

> 真源差量：`ISOMORPH-chain-analysis-jobs.v0.md`。  
> 样板切片：`SLICE-PLAN-key_link-S1-S5.v0.md`。  
> 本节回答两件事：**换分析场景时改什么**；**开发按什么顺序（是否先画 Graph）**。

### 11.1 多场景使用模型：换菜谱，不换厨房

七个「生成分析」共用同一套 **Analysis Job Runtime（厨房）**，差异只在 **analysis_key 菜谱包**：

| 工作空间 | 场景（Tab） | `analysis_key` | `task_type` |
| --- | --- | --- | --- |
| 产业运行诊断 | 产业周期 | `cycle` | `chain:diagnosis:cycle` |
| 产业运行诊断 | 关键环节 ✅样板 | `key_link` | `chain:diagnosis:key_link` |
| 产业运行诊断 | 瓶颈堵点 | `bottleneck` | `chain:diagnosis:bottleneck` |
| 区域产业评价 | 指数 | `regional_index` | `chain:regional:index` |
| 区域产业评价 | 竞争力 | `regional_competitiveness` | `chain:regional:competitiveness` |
| 深圳产业决策 | 情况对比 | `shenzhen_comparison` | `chain:shenzhen:shenzhen_comparison` |
| 深圳产业决策 | 发展分析 | `shenzhen_development` | `chain:shenzhen:shenzhen_development` |

**运行时行为（所有场景相同）**：

1. 前端在对应 Tab 提交 Create（带该键的 `draft`）  
2. Java 按 `task_type` 互斥、冻 Input、Enqueue → Execute（带 `graph_version`）  
3. Python 按 `analysis_key` **选对应 Graph** 执行 → Stage/Complete  
4. 前端过程壳只换 **stage 文案表**；结果页只换 **sections 绑定**  
5. 用户仍走 `succeeded_wait_view` 再显式看结果  

**每场景必须特化的「菜谱包」**：

| 资产 | 说明 |
| --- | --- |
| Create `draft` shape | 对象类型、参数、规则确认包（如周期四参数、区域权重） |
| `stage_code` + Bid 过程文案 | 过程 Steps 真源 |
| Graph（`*.graph.vN`） | 节点序、Artifact、确定性/LLM 边界 |
| Result `sections` Schema | 结果页区块 |
| Prompt/Context Pack | **仅**该图含 LLM 节点时需要 |
| 前端配置区 + 结果区组件 | Tab 内 UI，壳可复用 |

**永远不要为新场景做的事**：新开一套 Job 状态机、新发明一套回调协议、让前端直连 Python、开放式 Agent 自规划拓扑。

### 11.2 先定义 Graph 吗？——结论

| 问题 | 答案 |
| --- | --- |
| 编码 Graph Runner 之前，要不要先有 Graph 设计稿？ | **要。** 没有节点/Artifact/stage 映射，S1 无法开工。 |
| Graph 是不是整个项目的**第一步**？ | **不是。** 更前面是产品过程文案 + 对象/结果形状；**首键**还要并行竖切 Runtime 厨房。 |
| 新场景是否从零再造 Runtime？ | **否。** 厨房复用；只交付该键菜谱包。 |
| 是否先写 Prompt / 先接 LLM？ | **否。** Graph 里确定性节点与 Job 壳先通；LLM 最后（或可降级占位）。 |

推荐心智顺序（设计侧）：

```text
产品五件套（过程文案 / 配置 / 结果区块）
    → 注册 analysis_key + task_type
    → 草拟 Create draft + Result sections（契约面）
    → 定义 Graph（节点 ↔ stage、Artifact、LLM 边界）   ←「先定图」指这一步
    →（若厨房未就绪）Runtime 竖切并行
    → 按 S1→S2→… 实现图；有 LLM 再补 Prompt Pack
```

一句话：**先定「这道菜要几步、每步产出什么」（Graph + 契约），再进厨房炒；首道菜还要先把灶台（Runtime）搭好。**

### 11.3 开发步骤 A · 首键（样板 `key_link`）——搭厨房 + 第一道菜

适用于：**Analysis Job Runtime 尚未竖切**，或本键作为样板定契约。

| 阶段 | 做什么 | 产出 / DoD | 谁 |
| --- | --- | --- | --- |
| **A0 产品对齐** | 核对 Wireframe 过程句、配置禁用规则、结果非「仅关键列表」 | 文案表 + AC 清单 | product / ux |
| **A1 注册键** | 写入 `analysis_key` / `task_type` / 互斥粒度 | ISOMORPH §1 行 | architect / api |
| **A2 契约草拟** | OpenAPI Job 面（若尚无）+ Input draft + Result 总装 schema 骨架 | `openapi-*.yaml`、`*.schema.json` | api + algorithm |
| **A3 定义 Graph** | 线性节点、stage_code、Artifact、确定性 vs LLM、失败/降级 | **设计稿** `GRAPH-*.md` + **`graph_version` 字符串**；运行时由 A5 落成 Python 注册表（见 §11.3.1） | algorithm（主）+ architect |
| **A4 并行竖切** | Java：Create/Get/Events/Withdraw/Execute/Stage/Complete；FE：过程壳+Mock | Runtime 竖切 DoD | api ‖ frontend |
| **A5 实现 S1** | 把 A3 设计稿**翻译成代码**：节点函数 + Graph 注册；N1+结构+N5；Complete 过 schema；FE 接真轮询 | 过程五步 + 可演示 Result | algorithm → 联调 |
| **A6 加肉 S2…** | 打分→规则关键→企业→（最后）LLM | 切片 DoD 逐档 | algorithm + frontend |
| **A7 冻结样板** | 厨房 API 讨论冻结；后续键只加菜谱 | 会签备注 | architect |

**A3 与 A4 可并行**：Graph 设计稿不阻塞 Java 表结构；但 **A5 编码前 A3 必须可执行级清晰**（至少 S1 节点读/写定义清楚）。

### 11.3.1 A3 产出到底是什么？Python 运行时怎么「读图」？

**短答**：A3 的 `GRAPH-key_link.v0.md` 是给人评审的**设计契约**，**运行时 Python 不解析这份 Markdown**。  
真正被读的是：**Execute 请求里的 `graph_version` 字符串 → 进程内 Graph 注册表 → 有序节点函数列表**。

```text
A3 设计时                         A5 实现后（运行时）
─────────                         ─────────────────
GRAPH-*.md（人读）          →     graphs/key_link_v1.py（代码即图）
  节点表 / Artifact / LLM 边界      NODES = [(stage, fn), ...]
graph_version 建议名         →     GRAPH_REGISTRY["key_link.graph.v1"] = NODES
（无单独「图引擎配置文件」强制）     Runner 按列表 for 循环执行
```

| 产物类型 | 文件/形态 | 谁读 | 何时 |
| --- | --- | --- | --- |
| 设计稿 | `GRAPH-key_link.v0.md` | 人 / 评审 / 对照实现 | A3；**不进生产解释器** |
| 版本钉 | `graph_version`（如 `key_link.graph.v1`） | Java 写入 Job；Execute 传给 Python | Create / Execute |
| 可执行图 | Python 模块：注册表 + 节点函数 | Graph Runner | Worker 跑 Job 时 |
| （可选）文案表 | 小 dict / YAML：`stage_code → stage_label` | ReportStage 填 Bid 文案 | 可与代码同文件；**仍不是**解析整份 GRAPH.md |

**v0 推荐：「代码即图」（code-as-graph）**——少一层 YAML 图 DSL，避免再维护一套解释器。若日后要非开发改序，再抽薄 YAML 只描述顺序与 stage，节点实现仍是 Python 函数。

#### 运行时读取示意（关键，示意代码，非仓内已落地文件）

**① Java → Python Execute**（Runner 的入口参数）

```json
{
  "task_id": "tsk_kl_001",
  "analysis_key": "key_link",
  "graph_version": "key_link.graph.v1",
  "input_snapshot_id": "snap_in_001",
  "input_payload": { "...": "..." },
  "limits": { "llm_retry_max": 2 },
  "callbacks": {
    "stage_url": "https://java-internal/.../stages",
    "complete_url": "https://java-internal/.../complete"
  }
}
```

**② 注册表：用 `graph_version` 取节点列表（Python 读的是这里，不是 md）**

```python
# 示意：graphs/registry.py
from graphs.key_link_v1 import NODES as KEY_LINK_V1

GRAPH_REGISTRY = {
    "key_link.graph.v1": KEY_LINK_V1,
    # "bottleneck.graph.v1": BOTTLENECK_V1,
}

def get_graph(graph_version: str):
    nodes = GRAPH_REGISTRY.get(graph_version)
    if not nodes:
        raise ValueError(f"unknown graph_version={graph_version}")
    return nodes
```

**③ 图定义：有序 (stage_code, 节点函数)——这就是 A3 表格的代码形态**

```python
# 示意：graphs/key_link_v1.py
from nodes import freeze, structure, score_high_end, annotate, validate_assemble

# 与 GRAPH-key_link.v0.md 节点表一一对应；改序 = 改本列表 + 升 graph_version
NODES = [
    ("freeze", freeze.run),
    ("structure", structure.run),
    ("score_high_end", score_high_end.run),
    ("annotate", annotate.run),           # 内部再调 4a/4b/4c
    ("validate_assemble", validate_assemble.run),
]

STAGE_LABELS = {
    "freeze": "任务提交与产业链对象冻结",
    "structure": "全链路环节结构化拆解（研发/设计/制造/销售/服务）",
    "score_high_end": "基于附加值率、技术壁垒、市场集中度计算高端化指数",
    "annotate": "关键环节智能标注与竞争格局/代表企业/技术趋势归纳",
    "validate_assemble": "结果可信性校验与分析报告组装",
}
```

**④ Runner：读注册表 → for 循环；每节点 ReportStage；末节点交 Complete**

```python
# 示意：runtime/graph_runner.py
async def run_job(execute_body: dict, harness: HarnessClient):
    graph_version = execute_body["graph_version"]
    nodes = get_graph(graph_version)          # ← 运行时「读图」仅此一步
    arts = {"input": execute_body["input_payload"]}

    for stage_code, node_fn in nodes:
        await harness.report_stage(stage_code, "started", STAGE_LABELS[stage_code])
        try:
            arts = await node_fn(arts, limits=execute_body["limits"])
            await harness.report_stage(stage_code, "succeeded", STAGE_LABELS[stage_code])
        except NodeFailed as e:
            await harness.report_stage(stage_code, "failed", STAGE_LABELS[stage_code], message=str(e))
            await harness.complete_failed(e.error_code, failed_stage_code=stage_code)
            return

    await harness.complete_succeeded(result_payload=arts["result_payload"])
```

**⑤ 单个节点（算法能力在这里被调用，见 §3.6）**

```python
# 示意：nodes/structure.py
async def run(arts: dict, limits: dict) -> dict:
    ctx = arts["context"]                     # 来自 N1 Artifact
    skeleton = await chain_ads.load_five_stages(ctx["chain_id"])  # 进程内/ADS
    arts["chain_skeleton"] = skeleton
    return arts
```

#### A3 完成时 Checklist（设计稿 → 可翻译成上面代码）

A3 结束时，下列项应能**直接抄进** `NODES` / 节点模块，而无需再开会猜：

1. `graph_version` 字符串已定  
2. 有序列表：每行 `stage_code` + Bid `stage_label` + 读哪些 Artifact + 写哪些 Artifact  
3. 标清：确定性 / 查询 / LLM（及 LLM 子步是否共用同一 stage）  
4. 失败码与降级策略（尤其 LLM）  
5. **明确写一句**：运行时以 Python 注册表为准；`GRAPH-*.md` 不参与解释执行  

**不要**：写解析 `GRAPH-*.md` 的 Markdown 解释器；不要用 LLM 在运行时「根据 md 规划下一节点」。

#### `graph_version` 版本怎么「保存」？

`key_link.graph.v1` **不是**单独一份要入库的二进制图文件，而是三处一起钉死的**版本钉**：

```text
① 字符串 ID（契约名）
   key_link.graph.v1

② Python 代码模块（可执行定义，跟 Git 走）
   GRAPH_REGISTRY["key_link.graph.v1"] = NODES   # 或 graphs/key_link_v1.py

③ Job / Snapshot 落库字段（这次运行用的是哪一版）
   analysis_job.graph_version = "key_link.graph.v1"
   （建议同时写入 Input Snapshot.versions.graph_version）
```

| 存哪里 | 存什么 | 为什么 |
| --- | --- | --- |
| **Git / Python 仓** | `key_link_v1.py`（或同文件内 `NODES_V1`）+ 注册表键 | 图的**真实内容**（节点序、函数）随代码发版；审计靠 commit |
| **Java Job 表** | 列 `graph_version`（Create/入队时写入） | 这条任务**当时**跑的是哪版；GetJob/排障可见 |
| **Input Snapshot**（建议） | `versions.graph_version` | 与规则包、schema 版本一起冻结，结果可追溯 |
| **Execute body** | 回传同一字符串给 Python | Worker `get_graph(version)` 选注册表项 |
| **不存** | 整份 `GRAPH-*.md` 进 DB | md 是设计稿；运行时不解析 |

**谁决定写入哪一版？**

- Create 时由 **Java**（或配置中心）按 `analysis_key` 选**当前默认**版本，例如配置表 / 枚举：`key_link → key_link.graph.v1`。  
- 前端**一般不传** `graph_version`（避免客户端锁旧图或乱升版）；若开放传参须白名单校验。  
- Execute 把 Job 上已钉死的字符串传给 Python；Python **只查注册表，不自行改版**。

**升版怎么做（改节点序 / 增删节点 / 改 Artifact 契约时）？**

```text
1. 新增模块或常量：key_link.graph.v2 → NODES_V2
2. GRAPH_REGISTRY 同时挂上 v1 与 v2（过渡期）
3. Java 默认指针改为 v2（仅影响新 Create）
4. 已跑完的 Job 仍带着当时的 graph_version=v1；重放/审计仍解析 v1
5. 确认无 in-flight 任务依赖 v1 后，再从注册表下线 v1（可选）
```

```python
# 示意：升版时注册表并存，而不是原地改 v1
from graphs.key_link_v1 import NODES as KEY_LINK_V1
from graphs.key_link_v2 import NODES as KEY_LINK_V2

GRAPH_REGISTRY = {
    "key_link.graph.v1": KEY_LINK_V1,  # 保留：旧 Job / 重放
    "key_link.graph.v2": KEY_LINK_V2,  # 新 Create 默认
}

# Java 侧默认（配置或代码常量）
DEFAULT_GRAPH_VERSION = {
    "key_link": "key_link.graph.v2",
}
```

**什么算「必须升 version」vs「可仍叫 v1」？**

| 变更 | 是否升 `graph_version` |
| --- | --- |
| 改节点顺序、增删 stage、改 Artifact 形状 | **必须**升（v1→v2） |
| 同节点内修 bug、换 ADS SQL、调权重实现（契约不变） | 可仍 `v1`；靠 **Git commit / 服务镜像版本** 追溯实现细节 |
| 只改正文案 `stage_label` | 通常不升图版本；文案表可独立小版本 |
| Prompt 文案迭代 | 升 **prompt_pack_version**，不必升 graph（除非节点边界变了） |

**和 Result schema 版本的关系**：`graph_version`（怎么算）与 `result_schema_version`（结果长什么样）分开钉；Complete 时两者都可记在 Snapshot / Job 上，便于「同图不同结果壳」或「同壳换图」的演进。

**口诀**：版本名是钥匙；Python 模块是锁芯；Job 行是「这把锁开过哪扇门」的档案。不是把整段代码序列化进数据库。

#### 薄配置（可选演进）：是什么、优缺点、何时上

相对 **代码即图**（`NODES = [(stage, fn), ...]` 写死在 `.py`）与 **可视化拖拽**，**薄配置**指：

> 用 YAML/JSON **只描述**「顺序 + stage_code/label + handler 白名单引用」；  
> **节点实现仍是 Python 函数**；Runner 加载配置后按序调用 handler。  
> **禁止**：配置里写任意代码、任意 URL、任意新 handler、开放分支/循环（v1 仍线性）。

```yaml
# 示意：graphs/key_link.graph.v2.yaml（随 Python 仓 Git，或只读挂载）
graph_version: key_link.graph.v2
analysis_key: key_link
nodes:
  - stage_code: freeze
    stage_label: 任务提交与产业链对象冻结
    handler: key_link.freeze          # 必须 ∈ HANDLER_WHITELIST
  - stage_code: structure
    stage_label: 全链路环节结构化拆解（研发/设计/制造/销售/服务）
    handler: key_link.structure
  - stage_code: score_high_end
    stage_label: 基于附加值率、技术壁垒、市场集中度计算高端化指数
    handler: key_link.score_high_end
  - stage_code: annotate
    stage_label: 关键环节智能标注与竞争格局/代表企业/技术趋势归纳
    handler: key_link.annotate
  - stage_code: validate_assemble
    stage_label: 结果可信性校验与分析报告组装
    handler: key_link.validate_assemble
```

```python
# Runner 示意
spec = load_graph_yaml(graph_version)          # 读薄配置
for step in spec["nodes"]:
    fn = HANDLER_WHITELIST[step["handler"]]    # 白名单解析，禁止动态 import 用户串
    await report_stage(step["stage_code"], "started", step["stage_label"])
    arts = await fn(arts, limits=limits)
    await report_stage(step["stage_code"], "succeeded", step["stage_label"])
```

**优点**

| 点 | 说明 |
| --- | --- |
| 改序/改文案成本低 | 调 YAML 节点顺序或 `stage_label`，不必改 Runner 代码结构 |
| 多键外形一致 | 七个 `analysis_key` 都是「一份 spec + 若干 handler」，审图更容易 |
| 仍守住确定性 | 业务逻辑在 handler 代码里；配置变不了「谁是关键」的算法 |
| 比可视化便宜一个数量级 | 无画布、无任意连线、无运营自助发明节点 |
| 版本仍清晰 | 文件名/字段 `graph_version` + Git；Job 落库方式与代码即图相同 |
| 可演进 | 以后若真要可视化，UI **只编辑这份 YAML**，不必重做 Runner |

**缺点 / 风险**

| 点 | 说明 |
| --- | --- |
| 多一层间接 | 排障要看「配置 + handler 代码」两处；新手比纯 `.py` 列表略绕 |
| 假安全感 | 若白名单不严（`importlib` 加载任意路径），薄配置会滑向远程代码执行面 |
| 契约双源 | OpenAPI/`stage_code` 枚举、前端文案表、YAML label 可能漂移，需 CI 对齐检查 |
| 改拓扑仍要发版 | YAML 若在 Git 里，改序仍走发布；**并不能**热更新绕过评审（除非另做配置中心——那又引入一致性风险） |
| Artifact 契约仍在代码 | 薄配置**解决不了**「N2 写出什么结构」；Schema/不变量仍要人写测试 |
| 过早引入不值 | 只有 1～2 个键时，YAML 收益 < 解释器与校验成本 |
| 易被要求「再加一点」 | 分支、并行、条件边一开口，就滑向工作流引擎；必须书面冻结能力边界 |

**与另外两种形态对比**

| | 代码即图（v0 推荐） | 薄配置 | 可视化拖拽 |
| --- | --- | --- | --- |
| 改顺序 | 改 Python 列表 | 改 YAML | 拖线 |
| 实现逻辑 | 同文件/同模块 | handler 代码 | 常诱导向「配置里写逻辑」 |
| 安全面 | 最小 | 中（靠白名单） | 大 |
| 适合阶段 | 首键～前几键 | 多键稳定后、改序频繁 | 平台级、有治理后再说 |

**若做薄配置，建议硬规矩（写进 DoD）**

1. handler **仅**白名单字典；禁止按字符串动态 `import` 非名单模块  
2. 仅支持 **线性** `nodes[]`；无条件边、无子图、无用户自定义 LLM URL  
3. 配置文件进 **Git**（或带版本号的只读对象存储），Create 时把 `graph_version` 钉进 Job——与现在相同  
4. CI：YAML 的 `stage_code` ⊆ OpenAPI 枚举；`handler` ⊆ 白名单；与前端过程文案表 diff  
5. **首键 `key_link` 仍用代码即图竖切**；薄配置作为 `graph.v2` 或第二键起的可选形态，不阻塞厨房  

**结论**：薄配置是「通用化」的合理下一台阶，**优点在治理与多键一致性，不在让业务同学随便改分析**；缺点是间接层与纪律成本。在 Runtime + 至少一键菜谱跑稳之前，**优先代码即图**；多键重复「改一下顺序/文案」成为痛点时再抽 YAML。

---

### 11.4 开发步骤 B · 后续键（换场景）——只做菜谱包

适用于：厨房已通（Create→…→Complete 已联调过至少一键）。

| 阶段 | 做什么 | 产出 | 注意 |
| --- | --- | --- | --- |
| **B0** | 读 ISOMORPH 该键差量：对象、stage、LLM 轻重、开放项 | 差量勾选表 | 对照产品叶子 |
| **B1** | 定 Create `draft` + Result `sections` schema（🆕/🔧） | schema + example | 信封字段复用 |
| **B2** | **定义该键 Graph**（🆕 设计稿） | `GRAPH-{key}.v0.md` + `graph_version` | 运行时仍按 §11.3.1 落成注册表，不解析 md |
| **B3** | 若有 LLM：Context/Prompt/Output Pack；若无：跳过 | Prompt Pack 或「本键无 LLM」声明 | cycle/发展分析偏重 |
| **B4** | OpenAPI：扩 `analysis_key` 枚举 / draft oneOf / stage 枚举 | 小版本契约 | **不**新建路径前缀 |
| **B5** | FE：本 Tab 配置+过程文案表+结果区块；仍走同一 Job API | 页面 | 过程壳组件复用 |
| **B6** | Python：`GRAPH_REGISTRY[graph_version]=NODES` + 节点函数；按 S1→… 切片 | Worker 分支 | 同 §11.3.1 |
| **B7** | 联调：互斥、wait_view、honesty/QC、降级 | AC | 深圳发展强制 `source_result_id` |

**建议扩键序**（风险从低到高，见 ISOMORPH）：

```text
key_link（已样板）
  → bottleneck（同链对象，易复用骨架）
  → regional_index → regional_competitiveness
  → shenzhen_comparison
  → cycle（LLM/检索重）
  → shenzhen_development（依赖对比 Result）
```

### 11.5 每个新场景的「最小菜谱检查单」

开工编码前勾完再写代码：

- [ ] `analysis_key` / `task_type` 已注册，互斥粒度确认  
- [ ] Bid/Wireframe **过程文案** ↔ `stage_code` 一一映射  
- [ ] Create `draft`：对象类型、只读规则/权重、禁用「生成」条件  
- [ ] Graph：线性节点表 + Artifact + **哪些节点禁止 LLM**  
- [ ] Result：sections 列表 + 跨字段不变量（计数一致等）  
- [ ] LLM：需要？→ Prompt/Context/Output + `llm_retry_max`/降级；不需要？→ 文档写明  
- [ ] 开放项：QC/GAP → honesty / temp_default / ⚠️，不伪闭合  
- [ ] 前端：配置 / 过程文案表 / 结果绑定 / 记录入口  
- [ ] **不**改 Job 状态机与回调语义  

### 11.6 反模式（多场景时尤其容易犯）

| 反模式 | 后果 |
| --- | --- |
| 新场景复制一整套 Java Job 服务 | 互斥/SYS-JOBS/审计分裂 |
| 未定 Graph 先堆 Prompt | 模型无处挂、关键/分数被「提示词」偷换 |
| 未定 Result schema 先写前端结果页 | 三端对不齐，返工 |
| 周期/深圳一上来就接「实时检索+长文」 | 无 Stage/降级壳，体验与审计双空 |
| 把同步 `GET /v1/chain/**` 当生成分析 | 无 Snapshot，离开即丢 |

### 11.7 与 §10 的关系

- **§10**：首键落地时的**角色分工与竖切清单**（搭厨房）。  
- **§11**：跨场景的**用法模型 + 是否先 Graph + A/B 两套步骤**。  
- 首键跟 §10 + §11.3；第二键起主要跟 §11.4～§11.5。

---

## 12. 风险与开放项

| 风险/开放项 | 缓解 |
| --- | --- |
| QC02/03/04/05… 未甲方确认 | rules.source=temp_default + UI ⚠️/honesty |
| LLM 不稳定 | 默认叙述可降级；关键/分数不靠模型 |
| 与同步 `/v1/chain` 并存混淆 | 文档与网关路径分离；Job 用 analysis-jobs |
| Schema `$ref` 校验器差异 | CI 固定 Ajv 或打包内联 |
| 本文未正式会签 | 实现启动前架构师确认 v0→v1 |

---

## 13. 附录 A · 本会话产物索引

| 产物 | 路径（相对 `E2-产业链分析/`） |
| --- | --- |
| 本说明书 | `系统设计说明书-Analysis-Job-Runtime.v0.md`（本文件） |
| 同构差量 | `ISOMORPH-chain-analysis-jobs.v0.md` |
| Job 契约 | `CHAIN-TOPIC-DIAGNOSIS-…/schemas/CONTRACT-Java-Python-Analysis-Job-v0.md` |
| OpenAPI | `…/schemas/openapi-analysis-job.v0.yaml` |
| Graph | `…/schemas/GRAPH-key_link.v0.md` |
| 切片排期 | `…/schemas/SLICE-PLAN-key_link-S1-S5.v0.md` |
| Prompt Pack | `…/schemas/PROMPT-PACK-key_link-n4c.v0.md` |
| Result/Context Schemas | `…/schemas/chain.key_link.*.schema.json` |
| schemas 索引 | `…/schemas/README.md` |

产品交互真源仍在各叶子五件套（USM/UX/Wireframe）与 `SYS-ANALYSIS-JOBS`。

---

## 14. 附录 B · 一页实现口诀

1. **厨房 = Runtime**：外层 Java Harness + 内层 Python Harness×Graph Runner  
2. **Graph 是菜谱**：换 `analysis_key` 换图，不换厨房  
3. **Harness 是托管**：超时、幂等、Stage/Complete、Schema 盖章、降级  
4. **Prompt/Context/Loop 收口**：只进允许 LLM 的节点；关键 = N4c  
5. **多场景步骤**：产品文案→契约→**定 Graph**→（首键并行竖切 Runtime）→S1…；新键只做菜谱包  
6. **前端先壳 / 算法先 S1**：Mock Job 也能 wait_view；先结构再 LLM  

---

## 15. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-08-09 | 汇总本会话 Runtime/契约/Graph/Schema/扩展/实现路线为系统设计说明书 |
| v0.2 | 2026-08-09 | 增补 §3 Harness×Graph 实践：纠偏「Python 跑固定 Graph」、五层范式落位、双侧 Harness 清单与时序 |
| v0.3 | 2026-08-09 | 增补 §3.6：Graph 执行时与算法能力的四种交互（进程内/ADS/同层 internal/LLM）及禁止项 |
| v0.4 | 2026-08-09 | 重写 §11：多场景用法、是否先定 Graph、首键 A 步 / 后续键 B 步、菜谱检查单 |
| v0.5 | 2026-08-09 | 增补 §11.3.1：A3 设计稿 vs 运行时代码即图；`graph_version`→注册表→节点函数示例 |
| v0.6 | 2026-08-09 | 增补 §5.3：从前端 Create 到 wait_view/查看结果的完整运行时载荷与轮询「通知」路径 |
| v0.7 | 2026-08-10 | §11.3.1 增补：`graph_version` 三位一体保存（字符串 ID / Python 模块+Git / Job·Snapshot 落库）与升版规则 |
| v0.8 | 2026-08-10 | §11.3.1 增补：薄配置形态定义、优缺点、与代码即图/可视化对比及硬规矩 |
| v0.9 | 2026-08-10 | 增补 §9.1：节点内并行 vs 图级并行（高端化指数三因子/五环节并行） |
