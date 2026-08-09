# CONTRACT · Java ↔ Python Analysis Job（v0 草稿）

> **范围**：产业链「生成分析」长耗时 Job（先以 `chain:diagnosis:key_link` 为样例，其它 `analysis_key` 同构）。  
> **不在范围**：现有同步只读 `GET /v1/chain/{id}/key-nodes`（ADS 查询门面，不是本 Job 协议）。  
> **架构铁律**：前端 → Java REST → Python `/internal/*`；Java 不写算法；快照与任务真源在 **Java（SYS-JOBS）**。  
> **状态**：讨论草稿，不代表已实现。  
> **已决策（2026-08-09）**：进度与收口采用 **Python → Java 回调**（`ReportStage` / `CompleteJob`），不采用 Java 轮询 Python。  
> **OpenAPI 片段**：同目录 `openapi-analysis-job.v0.yaml`（Create / GetJob / ListEvents / Withdraw / Execute / ReportStage / Complete）。  
> **关键 Graph**：同目录 `GRAPH-key_link.v0.md`。

---

## 0. 入门：谁干什么

| 角色 | 职责 | 不管什么 |
| --- | --- | --- |
| **前端** | CreateJob、订阅进度、显式看结果 | 不直连 Python、不自造 stage |
| **Java Runtime** | 互斥/队列/Job 状态机、**持久化 Input/Result Snapshot**、投影 SYS-JOBS | 不算高端化指数、不调 LLM |
| **Python Graph Worker** | 按 `graph_version` 跑节点、上报 stage、提交结果载荷 | 不改 Job 互斥、不直接对前端推送 |

**Snapshot ID 所有权（重要）**：

| ID | 谁生成 | 谁持久化 | 谁只读消费 |
| --- | --- | --- | --- |
| `task_id` | Java | Java | 前端 / Python |
| `input_snapshot_id` | Java（Create 时） | Java | Python（执行入参） |
| `result_snapshot_id` | Java（Complete 成功落库时） | Java | 前端 / 报告任务 |
| `trace_id` | Java（或网关） | 随请求传递 | 全链路日志 |

Python **不要**自己发明 `result_snapshot_id` 写进库；它提交 `result_payload`，由 Java 校验 schema 后签发 `result_snapshot_id`。

---

## 1. 调用总序（关键环节）

```text
FE                Java                         Python
│                   │                            │
│ POST CreateJob    │                            │
│──────────────────►│ 校验·互斥·冻 Input Snapshot │
│◄──── task_id ─────│ status=queued|running      │
│                   │                            │
│                   │ POST /internal/.../execute │
│                   │───────────────────────────►│
│                   │   body: task_id            │
│                   │         input_snapshot_id  │
│                   │         input_payload      │
│                   │         graph_version      │
│                   │                            │
│                   │◄──── ReportStage (×N) ─────│
│ GET Job/events    │ 更新 stage / 投影过程页    │
│◄──────────────────│                            │
│                   │◄──── Complete(success) ────│
│                   │ 校验 result_payload        │
│                   │ 写 Result Snapshot         │
│                   │ status=succeeded           │
│                   │                            │
│ 仍停 succeeded_wait_view，等用户点查看结果      │
```

失败时 Python 调 `Complete(failed)` 或 Java 因超时自己 `failed`；前端走 `error_retry`。

---

## 2. 接口清单（逻辑名 → 建议路径）

> 路径名为建议；落地时以 OpenAPI 为准。前缀示意：Java 对外 `/topic/v1/analysis-jobs`；Java→Python `/internal/v1/chain/jobs`。

### 2.1 前端 → Java

| 逻辑名 | 方法 / 路径（建议） | 作用 |
| --- | --- | --- |
| `CreateAnalysisJob` | `POST /topic/v1/analysis-jobs` | 点「生成分析」 |
| `GetAnalysisJob` | `GET /topic/v1/analysis-jobs/{task_id}` | 过程页轮询 |
| `ListJobEvents` | `GET /topic/v1/analysis-jobs/{task_id}/events` | stage 事件列表 |
| `GetResultSnapshot` | `GET /topic/v1/analysis-results/{result_snapshot_id}` | 查看结果 |
| `WithdrawQueuedJob` | `POST .../{task_id}/withdraw` | 仅 queued |

### 2.2 Java → Python

| 逻辑名 | 方法 / 路径（建议） | 作用 |
| --- | --- | --- |
| `ExecuteJob` | `POST /internal/v1/chain/jobs/execute` | 开始跑图（可异步立即 202） |

### 2.3 Python → Java（回调；内网）

| 逻辑名 | 方法 / 路径（建议） | 作用 |
| --- | --- | --- |
| `ReportStage` | `POST /internal/v1/analysis-jobs/{task_id}/stages` | 上报阶段 |
| `CompleteJob` | `POST /internal/v1/analysis-jobs/{task_id}/complete` | 成功/失败收口 |

**鉴权**：Python 回调须服务身份（mTLS / 内部 token）；禁止浏览器可调。

**进度回传选型（已决策）**：采用 **Python 回调 Java**（`ReportStage` + `CompleteJob`）。不采用 Java 轮询 Python 拉状态。Execute 仍由 Java → Python 发起；回调 URL 可在 Execute body 的 `callback` 中下发。

---

## 3. CreateAnalysisJob（前端 → Java）

### 3.1 Request（关键环节）

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

说明：

- 前端传 **草稿**；Java 补齐展示名、规则包版本、`honesty`、签发 `input_snapshot_id`。  
- `client_request_id`：幂等键，防双击重复建单。  
- 同用户同 `task_type` 已有非终态 → **不新建**，返回已有 `task_id` + `reused: true`。

### 3.2 Response 200

```json
{
  "task_id": "tsk_kl_001",
  "task_type": "chain:diagnosis:key_link",
  "status": "queued",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": null,
  "reused": false,
  "process_route": "/industry-center/diagnosis?tab=key-link&demo_state=processing&task_id=tsk_kl_001",
  "trace_id": "tr_..."
}
```

### 3.3 Create 错误码（Java → 前端）

| `error_code` | HTTP 建议 | 含义 | 前端态 |
| --- | --- | --- | --- |
| `VALIDATION_OBJECT_REQUIRED` | 400 | 无对象 | `empty_object` |
| `VALIDATION_OBJECT_TYPE` | 400 | 关键须 `industry_chain` | `config_invalid` |
| `VALIDATION_FACTORS_UNAVAILABLE` | 400 | 因子包不可用 | `config_invalid` |
| `VALIDATION_FACTORS_NOT_CONFIRMED` | 400 | 未确认只读因子 | `config_invalid` |
| `VALIDATION_WEIGHT_EDIT_REJECTED` | 400 | 企图改正式权重 | `config_invalid` |
| `PERMISSION_LOCKED` | 403 | 无权限 | `permission_locked` |
| `OBJECT_UNAVAILABLE` | 409 | 对象暂不可用 | `unavailable` |
| `QUOTA_EXCEEDED` | 429 | 日权益不足 | 来源模块提示 |
| `CAPACITY_QUEUED_FULL` | 503 | 队列满（策略可改为仍入队） | 可解释稍后 |
| `INTERNAL_ERROR` | 500 | 未知 | `error_retry` |

互斥「恢复原单」**不是错误**：HTTP 200 + `reused: true`。

---

## 4. ExecuteJob（Java → Python）

Java 在 Job 进入可执行后调用。建议 **body 带齐 Input**，避免 Python 再调 Java 拉快照（降耦合）；仍传 id 便于日志关联。

### 4.1 Request

```json
{
  "task_id": "tsk_kl_001",
  "task_type": "chain:diagnosis:key_link",
  "analysis_key": "key_link",
  "input_snapshot_id": "ins_kl_001",
  "input_payload": { "...": "完整 Input Snapshot.payload + honesty + versions" },
  "schema_version": "chain.key_link.input.v1",
  "graph_version": "key_link.graph.v1",
  "prompt_pack_version": "key_link.prompts.v1",
  "trace_id": "tr_...",
  "callback": {
    "stage_url": "https://java-internal/.../stages",
    "complete_url": "https://java-internal/.../complete"
  },
  "limits": {
    "timeout_sec": 600,
    "llm_retry_max": 2
  }
}
```

### 4.2 Response

| 码 | 含义 |
| --- | --- |
| 202 Accepted | 已接收，异步执行 |
| 409 `JOB_ALREADY_RUNNING` | 同 task 重复投递（幂等忽略或拒绝） |
| 400 `INPUT_SCHEMA_INVALID` | input 对不上声明 schema |
| 503 `WORKER_BUSY` | 可让 Java 稍后再投 |

Python **不得**在 Execute 响应里返回最终业务结果（结果走 Complete）。

---

## 5. ReportStage（Python → Java）

每进入/完成一个过程阶段调用一次（或 `started` + `succeeded` 成对）。

### 5.1 Request

```json
{
  "task_id": "tsk_kl_001",
  "input_snapshot_id": "ins_kl_001",
  "event_id": "evt_stage_003",
  "stage_code": "score_high_end",
  "stage_label": "基于附加值率、技术壁垒、市场集中度计算高端化指数",
  "stage_index": 3,
  "stage_total": 5,
  "status": "succeeded",
  "message": null,
  "degraded": false,
  "degrade_reasons": [],
  "at": "2026-08-09T22:51:00+08:00",
  "trace_id": "tr_..."
}
```

字段约定：

| 字段 | 规则 |
| --- | --- |
| `event_id` | Python 生成，Java 幂等去重 |
| `stage_label` | **必须**用产品 Bid 过程文案（关键五段见下表） |
| `stage_code` | 机器码，稳定枚举 |
| `input_snapshot_id` | 冗余校验：须与 Job 上冻结的一致，否则拒绝 |
| 不传 `result_snapshot_id` | 阶段上报阶段不涉及结果 ID |

### 5.2 关键环节 `stage_code` 枚举（v0）

| index | stage_code | stage_label（验收必现） |
| --- | --- | --- |
| 1 | `freeze` | 任务提交与产业链对象冻结 |
| 2 | `structure` | 全链路环节结构化拆解（研发/设计/制造/销售/服务） |
| 3 | `score_high_end` | 基于附加值率、技术壁垒、市场集中度计算高端化指数 |
| 4 | `annotate` | 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 |
| 5 | `validate_assemble` | 结果可信性校验与分析报告组装 |

> `stage_label` 可与 Wireframe 全文对齐微调；**禁止**改成「调用 GPT」等技术黑话（业务态）。

### 5.3 ReportStage 错误码（Java → Python）

| `error_code` | 含义 | Python 应 |
| --- | --- | --- |
| `JOB_NOT_FOUND` | 无此 task | 停止 |
| `JOB_NOT_RUNNING` | 已终态仍上报 | 停止 |
| `SNAPSHOT_MISMATCH` | input_snapshot_id 不符 | 停止并 Complete(failed) |
| `STAGE_ORDER_INVALID` | 阶段乱序/跳号（若启用严格序） | 按策略重试或失败 |
| `DUPLICATE_EVENT` | event_id 重复 | 视为成功（幂等） |

Java 收到合法 Stage 后：`status` 保持 `running`（或仍 `queued` 直到第一阶段），更新 `current_stage_*`，供前端过程页。

---

## 6. CompleteJob（Python → Java）

### 6.1 成功 Request

```json
{
  "task_id": "tsk_kl_001",
  "input_snapshot_id": "ins_kl_001",
  "outcome": "succeeded",
  "complete_event_id": "evt_complete_001",
  "graph_version": "key_link.graph.v1",
  "prompt_pack_version": "key_link.prompts.v1",
  "result_schema_version": "chain.key_link.result.v1",
  "result_payload": {
    "result_title": "半导体照明产业链 · 产业关键环节识别结果",
    "summary": {},
    "sections": {
      "chain_structure": {
        "schema_version": "chain.key_link.chain_structure.v1",
        "stages": [],
        "edges": []
      }
    },
    "metrics_used": ["M_CHAIN_KEY_NODE_COUNT"],
    "evidence_refs": [],
    "honesty": {
      "data_mode": "mock",
      "pending_decisions": ["QC02"],
      "gaps": ["GAP-CHAIN-DIAG-METRICS"],
      "degraded": false,
      "degrade_reasons": []
    }
  },
  "artifact_refs": [],
  "at": "2026-08-09T22:55:00+08:00",
  "trace_id": "tr_..."
}
```

**snapshot id 传递规则（成功）**：

1. Python 提交时 **只带** `input_snapshot_id`（证明跑的是哪份输入）。  
2. **不带**自造 `result_snapshot_id`。  
3. Java 校验 `result_payload`（含 `chain_structure` schema）通过后：  
   - 生成 `result_snapshot_id`  
   - 持久化 Result（写入 `payload.input_snapshot_id`）  
   - Job：`status=succeeded`，`result_snapshot_id=...`  
4. Complete 响应把签发的 id 回给 Python（仅日志/审计用）：

```json
{
  "accepted": true,
  "task_id": "tsk_kl_001",
  "status": "succeeded",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": "res_kl_001"
}
```

### 6.2 失败 Request

```json
{
  "task_id": "tsk_kl_001",
  "input_snapshot_id": "ins_kl_001",
  "outcome": "failed",
  "complete_event_id": "evt_complete_fail_001",
  "error_code": "SCHEMA_VALIDATION_FAILED",
  "error_message": "chain_structure.stages length != 5",
  "failed_stage_code": "validate_assemble",
  "failed_stage_label": "结果可信性校验与分析报告组装",
  "details": { "schema": "chain.key_link.chain_structure.v1" },
  "at": "2026-08-09T22:55:00+08:00",
  "trace_id": "tr_..."
}
```

失败时：`result_snapshot_id` 保持 `null`；Job → `failed`；释放互斥。

### 6.3 Complete 错误码（Java 拒收回调时 → Python）

| `error_code` | 含义 |
| --- | --- |
| `JOB_NOT_FOUND` | |
| `JOB_NOT_RUNNING` | 重复 Complete / 已终态 |
| `SNAPSHOT_MISMATCH` | input id 不符 |
| `RESULT_SCHEMA_INVALID` | result_payload 未过 schema（含 chain_structure） |
| `RESULT_INVARIANT_FAILED` | 如 key_node_count ≠ 标注数（跨字段） |
| `DUPLICATE_COMPLETE` | complete_event_id 重复 → 幂等返回已有结果 |

### 6.4 Python 业务失败 `error_code`（写入 Job，给前端）

| `error_code` | 含义 | 用户侧 |
| --- | --- | --- |
| `INPUT_OBJECT_INVALID` | 执行期发现对象不可用 | 失败 + 可复制配置 |
| `ADS_UNAVAILABLE` | 数仓/ADS 不可用 | 诚实失败或降级策略由图决定 |
| `RULE_PACK_UNAVAILABLE` | 规则包缺失 | |
| `RETRIEVAL_UNAVAILABLE` | 检索未接通 | 可 `degraded` 继续或失败（按 analysis_key 策略） |
| `LLM_SCHEMA_FAILED` | LLM 输出多次不过 Schema | |
| `LLM_FACT_CONFLICT` | 叙述数字不在 Context | |
| `SCHEMA_VALIDATION_FAILED` | 组装结果不过 schema | |
| `GRAPH_TIMEOUT` | 节点超时 | |
| `INTERNAL_WORKER_ERROR` | 未分类 | |

Java 自身也可不经 Python 置失败：

| `error_code` | 来源 |
| --- | --- |
| `JOB_TIMEOUT` | Java 看门狗 |
| `OPS_TERMINATED` | 运维终止 |
| `WORKER_LOST` | 心跳丢失 |

---

## 7. 前端读接口与过程页轮询（Get / Events / Withdraw）

> OpenAPI：`openapi-analysis-job.v0.yaml` 中 `getAnalysisJob` / `listAnalysisJobEvents` / `withdrawAnalysisJob`。

### 7.1 谁轮询谁

| 角色 | 行为 |
| --- | --- |
| Python → Java | **回调** ReportStage / Complete（已决策） |
| 前端 → Java | **轮询** GetJob（权威）；可选 ListEvents 画 Steps |
| 前端 | **禁止**直连 Python；禁止用本地 setTimeout 假推进阶段 |

### 7.2 轮询策略（建议）

1. 进入 `demo_state=processing` 后立即 `GET .../analysis-jobs/{task_id}` 一次。  
2. `status ∈ {queued, running}`：每 **2～3s** 轮询 GetJob；可用 `ListEvents?since_event_id=` 增量补 Steps。  
3. `status` 进入终态（`succeeded` / `failed` / `withdrawn` / `terminated`）：**停止轮询**。  
4. 实时通道（SSE/WS）未接通时：降级轮询即可（对齐 SYS-JOBS「不断言本地真源」）。  
5. 页面隐藏（切 Tab）可降频或暂停；回到过程页再拉一次全量。

### 7.3 GetJob 与页面态

| `status` | `allow_withdraw` | `allow_view_result` | 默认 `page_mode_hint` | 前端主模式 |
| --- | --- | --- | --- | --- |
| `queued` | true（发起人） | false | `process_queued` | Process：队列位 + 撤回 |
| `running` | false | false | `process_running` | Process：Steps + 已用时间 |
| `succeeded` | false | true | `process_succeeded_wait_view` | Process 停住；点查看 → Result |
| `failed` | false | false | `process_failed` | Process 失败 + 按配置新建 |
| `withdrawn` | false | false | `config` / `process_withdrawn` | 回 Config |
| `terminated` | false | false | `process_failed` 类 | 运维终止说明 |

**铁律**：`succeeded` ≠ 自动进 Result。须用户点「查看分析结果」或显式带 `demo_state=result`。

### 7.4 ListEvents

- 事件来源 = Python `ReportStage` 落库。  
- Steps 勾选态以事件为准，不靠 GetJob 的单个 `current_stage_*` 反推历史。  
- `since_event_id` 增量；刷新后无 since 则全量升序。

### 7.5 Withdraw

- 仅 `queued`；`running` 返回 `WITHDRAW_NOT_ALLOWED`（409）。  
- 成功 → `withdrawn`，释放互斥，返回 `config_route`。

### 7.6 GetJob 响应示例（字段以 OpenAPI 为准）

```json
{
  "task_id": "tsk_kl_001",
  "task_type": "chain:diagnosis:key_link",
  "analysis_key": "key_link",
  "status": "running",
  "input_snapshot_id": "ins_kl_001",
  "result_snapshot_id": null,
  "current_stage_code": "score_high_end",
  "current_stage_label": "基于附加值率、技术壁垒、市场集中度计算高端化指数",
  "stage_index": 3,
  "stage_total": 5,
  "elapsed_sec": 84,
  "queue_position": null,
  "allow_withdraw": false,
  "allow_view_result": false,
  "page_mode_hint": "process_running",
  "process_route": "...",
  "result_route": "..."
}
```

---

## 8. ID 传递速查表

| 时机 | 携带的 ID | 不携带 |
| --- | --- | --- |
| FE → Java Create | `client_request_id`；可选 `retry_from_task_id` | snapshot（尚未有） |
| Java → FE Create 响应 | `task_id`, `input_snapshot_id` | `result_snapshot_id` |
| Java → Python Execute | `task_id`, `input_snapshot_id`, 完整 input | `result_snapshot_id` |
| Python → Java ReportStage | `task_id`, `input_snapshot_id`, `event_id` | `result_snapshot_id` |
| Python → Java Complete(success) | `task_id`, `input_snapshot_id`, `result_payload` | 自造 result id |
| Java → Python Complete 响应 | 新签发 `result_snapshot_id` | |
| FE → Java GetJob / Events | `task_id` | |
| FE → Java Withdraw | `task_id`（仅 queued） | |
| FE → Java GetResult | `result_snapshot_id` 或经由 `task_id` 解析 | |

---

## 9. 幂等与并发（最小集）

1. Create：`user_id + client_request_id` 幂等。  
2. 互斥：`user_id + task_type` 非终态唯一。  
3. ReportStage：`event_id` 幂等。  
4. Complete：`complete_event_id` 幂等；第二次返回同一 `result_snapshot_id`。  
5. Execute：同一 `task_id` 重复投递不双开图（worker 锁）。

---

## 10. 与现有同步 API 的边界

| | 同步 `GET /v1/chain/{id}/key-nodes` | 本 Job 协议 |
| --- | --- | --- |
| 场景 | 联调/ADS 即时读 | 「生成分析」配置→过程→不可变结果 |
| 快照 | 无 | Input/Result 必有 |
| SYS-JOBS | 不进 | 必进 |
| LLM/多阶段 | 无 | 有 Graph + Stage |

Graph 内部**可以**调用现有查询函数复用 ADS 逻辑，但对外仍只通过 Job Complete 交付 Result。

---

## 11. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0 | 2026-08-09 | 讨论稿：Create / Execute / ReportStage / Complete + 错误码 + snapshot id 传递；样例 key_link |
| v0.1 | 2026-08-09 | 锁定 Python 回调；补充 OpenAPI Create+Complete 片段 |
| v0.2 | 2026-08-09 | OpenAPI 并入 Execute + ReportStage → `openapi-analysis-job.v0.yaml` |
| v0.3 | 2026-08-09 | 对外读接口：GetJob / ListEvents / Withdraw + 过程页轮询约定 |
| v0.4 | 2026-08-09 | 关键 Graph 五节点：`GRAPH-key_link.v0.md` |
| v0.5 | 2026-08-09 | 同构扩展差量见 `../ISOMORPH-chain-analysis-jobs.v0.md` |
