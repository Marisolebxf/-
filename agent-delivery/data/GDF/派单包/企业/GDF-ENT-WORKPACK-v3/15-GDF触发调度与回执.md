# 15 — GDF 触发调度与回执（ES / 图谱）

> **读者**：GDF 产线调度 + 本侧 Java / Python。  
> **GDF 在这两块的角色**：**触发 + 调度 + 收终态**，不写 ES、不写 Nebula。  
> **调用链铁律**：GDF → **Java REST** → Python `/internal/*`。禁止 GDF 直连 Python、直连 ES、直连 graphd。  
> **现网诚实**：Python ETL **已有**「默认异步 + 轮询 status」；**没有**对外 Java、**没有**完成回调 GDF、**没有**跨进程 `job_id`。下面分「目标契约 / 现网能用什么 / 缺口」。

---

## 0. 一句话

GDF 某张 DWD 表（或同一 ES 模块的一组表）**当天洗数成功之后**，按**模块 / 图谱 op_id** 触发一次；任务可能跑很久；跑完再关单。GDF 作业**禁止**同步卡住等 ES/图谱跑完。

**当前投递态 = §6.1**（飞书值班 + 本侧转发 + 轮询 status）。下面时序图是 §4 目标，**不要**配进今日 DAG。

```text
gkx → ODS → DWD（GDF 洗数，本包 Wave A/B）
        │
        │ 表作业 success
        ▼
GDF 调度 ──POST Java──► 受理 202 + task_id
        │                    │
        │                    ▼
        │              Python 异步跑（小时级）
        │                    │
        │                    ▼
        ◄── 回执 success/failed ── 我们 POST GDF callback
        │
        └── 也可轮询 GET 状态（回执丢了时兜底）
```

---

## 1. 谁干什么

| 角色 | 做 | 不做 |
|------|----|------|
| GDF | 贴源/洗 DWD；**按表成功后触发**对应 ES 模块或图谱 op；收 callback / 轮询关单 | 写 ES；写 nGQL；`sync=true` 堵自己的调度线程；表失败还去触发下游 |
| Java | 对外 REST：受理、查状态、转 Feign；完成后调 GDF callback | 自己算 NLP / 自己写 ES / 自己写 nGQL |
| `lumen-etl-es-py` | 按模块水位 + Painless 写物理索引 | 被 GDF 直连；当 cron 真源 |
| 图谱 Python | 按 `op_id` 投影 Nebula | 灌数顺带建图；被 GDF 直连 |

前端菜单点图（`14`）仍然保留，给人用。**日批**以本卷 GDF 触发为准，不要两套日批抢同一模块。

---

## 2. 何时触发（表级 → 模块级）

触发粒度 = **ES 模块** 或 **图谱 op_id**，不是「全库洗完再 sync-all」。

| 条件 | 动作 |
|------|------|
| 该模块对应的 **全部** DWD 源表当日作业 `success` | 触发该模块 **增量**（`full=false`） |
| 模块有两张源表（如 `enterprise_base` + `enterprise_extra`） | **两张都成功**再触发一次 `reg_info`，不要表各打一次把水位打乱 |
| 源表作业 `failed` / 未跑 | **不触发**；GDF 关单为阻塞，飞书报表名 |
| 仅 ODS 贴源完成、Wave B 未洗 | **不触发** ES/图谱 |
| 首次建索引 / 空索引 | 先 `reg_info` / `forg_reg_info` **full**（人工或单独作业），再允许其他模块日批 |
| 想重灌某模块 | 显式 `full=true`；默认禁止日常 full |
| `statistics` | 依赖多表聚合：当日相关明细模块都回执 success 后再触发；或日终单独一条。禁止当第一枪 |

表 → 模块对照见 `12` §3（必须按行分开触发）。表 → 图谱 op 见 `14` §2.1。

---

## 3. 异步（长任务，必须）

ES 单模块增量可能数十分钟到数小时（专利/招投标/statistics 更长）。图谱 `scope=batch` 同样长。

| 规则 | 说明 |
|------|------|
| GDF **必须**异步触发 | HTTP 超时建议 10–15s；只等「受理」 |
| 禁止 `sync=true` | 同步会堵到网关/GDF 超时，任务可能还在跑 |
| 受理成功 ≠ 更新成功 | 受理只表示入队/开跑；终态看 callback 或 GET status |
| 重入 | 同一模块已在跑：返回「忙 / started=false」，GDF **排队或隔 15min 再触发**，不要并行打同一模块 |
| 不同模块 | **目标**可并行；**现网** Python `TaskManager` 进程内 **单飞**（全局一把锁），第二枪 `started=false`。未改代码前 GDF **必须串行**触发 |

### 3.1 现网 Python（已实现，仅内部）

| 项 | 值 |
|----|-----|
| 触发 | `POST /internal/etl/modules/{module}/sync?full=false&sync=false` |
| 立刻返回 | `{ started, module, running }`；`started=false` = 已有任务在跑 |
| 查询 | `GET /internal/etl/status` → `running` / `current_job` / `last_job` / `last_result` / `last_error` / `last_cost_s` |
| 状态存哪 | **单进程内存**，重启丢失；不是给 GDF 的正式 job 库 |
| 回执 | **无** webhook |

图谱现网写入入口仍是菜单/同步 HTTP，**没有**与 ETL 同构的异步 job + callback。日批要走本卷，须 Java 补一层受理/回执（见 §6）。

---

## 4. 目标对外契约（给 GDF，尚未落地）

Java 对外（经网关，路径待 API 叶落号；**未落号前禁止写进 GDF crontab 当已上线**）。语义先钉死：

### 4.1 触发 ES 模块

```http
POST /ent/v1/etl/modules/{module}/sync
Content-Type: application/json

{
  "full": false,
  "gdf_job_id": "GDF-DWD-enterprise_base-20260902",
  "callback_url": "https://gdf.example/api/callbacks/gkx-ent",
  "source_tables": ["enterprise_base", "enterprise_extra"],
  "dwd_success_at": "2026-09-02T03:10:00+08:00"
}
```

立刻：`202` + `{ "task_id", "module", "accepted": true }`  
忙：`409` + `{ "accepted": false, "reason": "module_busy" }`

`{module}` 只允许 `12` §3 列出的 17 个名字，禁止 `sync-all` 当日常。

### 4.2 触发图谱 op

```http
POST /ent/v1/graph/ops/{op_id}/sync
{
  "scope": "batch",
  "filter": { "all": false },
  "mode": "rule",
  "gdf_job_id": "GDF-DWD-enterprise_invest-20260902",
  "callback_url": "https://gdf.example/api/callbacks/gkx-ent"
}
```

立刻 `202`。禁止空过滤扫全库，除非显式 `filter.all=true`（须书面批准）。`op_id` 只允许 `14` 清单。

### 4.3 查询

`GET /ent/v1/etl/tasks/{task_id}`  
`GET /ent/v1/graph/tasks/{task_id}`

状态：`accepted` / `running` / `success` / `failed` / `rejected`。

### 4.4 回执（我们 → GDF）

任务结束（无论成败）`POST {callback_url}` **至少一次**。GDF 须幂等收。

```json
{
  "gdf_job_id": "GDF-DWD-enterprise_base-20260902",
  "task_id": "etl-reg_info-20260902T031500",
  "kind": "es_module",
  "name": "reg_info",
  "status": "success",
  "started_at": "2026-09-02T03:15:00+08:00",
  "finished_at": "2026-09-02T04:02:11+08:00",
  "cost_s": 2831.4,
  "rows": 120340,
  "error": null
}
```

`kind=graph_op` 时 `name` = `op_id`，另可带 `written_nodes` / `written_edges` / `skipped` 计数。`status=failed` 必须带 `error`，水位/图均按现网规则不假成功。

回执失败：我们重试 3 次（1m / 5m / 15m）；仍失败则 GDF 凭 `GET …/tasks/{id}` 关单，并告警本侧。

---

## 5. GDF 调度怎么配

**今日按 §6.1 配。** 下面 1–6 是 §4 Java 上线后的目标配法，现在写进 DAG 会空打。

1. Wave B 作业 DAG **叶子后置**：表 success → 触发对应模块/op（对照 `12`/`14`）。  
2. HTTP 成功码只认 `202` / `accepted=true`。`409` 入重试队列，不要标 DWD 失败。  
3. 关下游单只认 callback `success` 或查询到 `success`。  
4. 同一 `gdf_job_id` 重发：我们按幂等（已 success 则回已完成，不重跑；running 则 409）。  
5. **不要**给 17 个模块配死 crontab 当正式调度（`OPEN-ENT-FLOW-01` 未关）。日批时钟以 GDF 表作业结束时间为准。  
6. 密钥 / callback URL 线下给，不进本包。

---

## 6. 缺口（点名，不假装已通）

| ID | 缺口 | 现网 | 谁补 |
|----|------|------|------|
| `OPEN-ENT-GDF-TRIGGER` | Java 对外触发 / 查任务 | 无 Feign、无 `/ent/v1/etl/*` | api-agent + Java |
| `OPEN-ENT-GDF-CALLBACK` | 完成回调 GDF | Python 无 webhook | Java 出站 + GDF 收口 URL |
| `OPEN-ENT-ETL-JOBID` | 持久 `task_id`、多模块并行 | 内存单飞 `TaskManager` | `lumen-etl-es-py` |
| `OPEN-ENT-FLOW-01/04` | 正式 DAG 名 / SLA | 未关 | 不并入本叶 |
| 图谱日批异步 | 与 ETL 同构的 job | 仅菜单 HTTP | 图谱叶 + Java |

### 6.1 当前投递态（启动会就按这个配，不要配 §4 目标路径）

对外 `/ent/v1/*` **还没有**。GDF **禁止**把 §4 写进产线 DAG。

**现在能跑的日批：**

1. GDF 表作业 success → 飞书/工单打给本侧值班（`human:辜少彬`），带：`module` 或 `op_id`、源表名、`gdf_job_id`、完成时间。  
2. 本侧经 **Java 内网转发**（没有则本侧运维代发，仍禁止把 Python 地址给 GDF）调用  
   `POST /internal/etl/modules/{module}/sync?full=false&sync=false`  
3. 立刻看返回：`started=true` 才算入队；`started=false` = 忙，15 分钟后再发。现网单飞，**一次只跑一个模块**。  
4. GDF/本侧轮询 `GET /internal/etl/status`：`running=false` 且 `last_job` 对上且 `last_error` 空 → 关 ES 单成功；有 `last_error` → 失败，水位未推进。  
5. 图谱日批现网无同构 job：表 success 后本侧按 `14` §2.1 **人工/菜单 batch** 跑对应 op，结果回飞书。不要假装已有 graph callback。  
6. §4 Java + webhook 落地后，用同一套 `gdf_job_id` 切过去，不改 Wave A/B。

启动会必须口头确认：「今日起用 6.1；§4 是目标，未上线。」

---

## 7. 禁止

- GDF 直连 `lumen-etl-es-py` / 图谱 Python / ES / Nebula。  
- 一张表失败仍触发对应模块。  
- 日常 `sync-all` 或 `sync=true`。  
- 把「触发已受理」写成「ES/图谱已更新」。  
- 灌数流水线里顺带触发图谱。  
- 为触发另开第二套 ES 索引或第二张图。
