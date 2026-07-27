# 派单包：ENT-PY-RECOMMEND-TASK（v3.2）

- **派单方**：coordinator（architect-agent 起草）
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强
- **仓**：`demo-svc-topic-py`
- **子项目**：`gkx_ai_service/`（与 EVAL 同子项目，复用已有骨架）
- **依赖**：`ENT-ARCH-ANALYSIS-TASK-DOC`、`ENT-MOD-RECRUIT-PDR-G1`、`ENT-PY-ANALYSIS-CALLBACK`、`ENT-ALGO-SCIENCE-ASYNC-FRAME`
- **状态**：`backlog`
- **架构真源**：`ARCH-ANALYSIS-TASK-设计方案.md` **v3.2** §11

---

## 0. 铁律前置（违反必拒）

1. **本任务只在 `demo-svc-topic-py` 仓**，复用 `gkx_ai_service/` 子项目。**禁止**修改 `demo-algo-science`
2. **gkx_ai_service 是算法服务的屏蔽层**。Java 只调 gkx_ai_service `/internal/gkx-ai/recommend/*`；gkx_ai_service 内部 HTTP 调 science 算法
3. **算法只在 Python**。本任务是数据编排层，不做推荐评分/筛选算法
4. **Mock 优先**。science 未就绪前用 Mock 结果；切换时仅改内部 HTTP 客户端，契约不变
5. **数据血缘 D9**。结果中每个统计指标须可追溯 metric_id 或标 🟡 GAP
6. **taskId 由 Java 唯一生成**，Python 复用，不自生成
7. **pending 只在算法侧**，Python status 不返回 pending，映射为 running

---

## 1. 目标

在 `gkx_ai_service` 新增 `/internal/gkx-ai/recommend/tasks` 场景适配，屏蔽 science 算法接口差异。
招引与培育共用一套推荐任务接口，用 `subType` 与 `selectionMode` 区分。
Python 不作为正式历史、状态和结果真源——正式真源为 Java MySQL `analysis_task`。

---

## 2. 端点（4 个，prefix=`/internal/gkx-ai/recommend`）

| # | 端点 | 方法 | 功能 |
|---|---|---|---|
| 1 | `/tasks` | POST | 接收 Java taskId，适配并转发算法任务 |
| 2 | `/tasks/{task_id}/status` | POST | 算法任务状态适配，供 Java 修正器调用 |
| 3 | `/tasks/{task_id}/result` | POST | 按 subType 返回引育推荐结果 |
| 4 | `/tasks/{task_id}/cancel` | POST | 逻辑取消 |

> Python **不提供** `/tasks/history`（历史只查 Java MySQL）。
> Python **不提供** 同步辅助接口（引育推荐无 industries/indicators/precheck/compare）。
> Python **不管对比篮候选池 CRUD**（候选池由 Java 管理或既有 compare-basket 任务承接）。

---

## 3. 请求/响应契约

### 3.1 创建任务 `POST /tasks`

**招引 · 条件筛选**：

```json
{
  "task_id": "REC-20260725-001",
  "analysisType": "talent_recommend",
  "callbackUrl": "http://gkx-ai-service:8081/internal/gkx-ai/analysis/callback",
  "params": {
    "subType": "attraction",
    "selectionMode": "filter",
    "filters": {
      "enterpriseTags": [],
      "industryDomains": [],
      "geographicSources": []
    },
    "weights": {
      "technologyMatch": 34,
      "growth": 33,
      "regionalFit": 33
    }
  }
}
```

**培育 · 条件筛选**：

```json
{
  "task_id": "REC-20260725-002",
  "analysisType": "talent_recommend",
  "callbackUrl": "...",
  "params": {
    "subType": "cultivation",
    "selectionMode": "filter",
    "filters": {
      "industryCategories": [],
      "policyOrientations": [],
      "enterpriseScales": []
    },
    "weights": {
      "technologyBarrier": 34,
      "marketGrowth": 33,
      "teamBackground": 33
    }
  }
}
```

**候选工作台指定企业**（招引/培育通用）：

```json
{
  "task_id": "REC-20260725-003",
  "analysisType": "talent_recommend",
  "callbackUrl": "...",
  "params": {
    "subType": "attraction",
    "selectionMode": "candidate_workbench",
    "enterpriseCodes": ["9132...", "9144..."],
    "weights": {
      "technologyMatch": 34,
      "growth": 33,
      "regionalFit": 33
    }
  }
}
```

**响应**（立即返回 running）：

```json
{
  "code": 0,
  "data": {
    "task_id": "REC-20260725-001",
    "status": "running"
  }
}
```

### 3.2 查询状态 `POST /tasks/{task_id}/status`

**状态枚举**：
- Python 返回 `running` / `success` / `failed`
- **不返回 `pending`**：算法侧 pending 映射为 `running`
- cancelled 由 Java 逻辑取消触发

**响应**：

```json
{
  "code": 0,
  "data": {
    "task_id": "REC-20260725-001",
    "status": "running",
    "current_stage": "compute",
    "stages": [
      {"name": "task_submit", "status": "done", "elapsed_ms": 100},
      {"name": "data_gather", "status": "done", "elapsed_ms": 300},
      {"name": "compute", "status": "running", "elapsed_ms": 1500},
      {"name": "result_assembly", "status": "pending"}
    ],
    "elapsed_ms": 1900
  }
}
```

### 3.3 查询结果 `POST /tasks/{task_id}/result`

**结果契约**：以 `ARCH-ANALYSIS-TASK-设计方案.md` v3.2 §11.3 / §11.4 为最终契约。

统一外层：

```json
{
  "taskId": "REC-20260725-001",
  "analysisType": "talent_recommend",
  "subType": "attraction",
  "selectionMode": "filter",
  "generatedAt": "2026-07-25T16:30:00+08:00",
  "candidateCount": 48,
  "weights": {},
  "rankings": [],
  "details": {},
  "reportStatus": "not_created"
}
```

- **attraction**：排名列表（rank/enterpriseCode/enterpriseName/industryDomain/geographicSource/targetTraits[]/recommendationScore）+ 企业评价详情（判定维度+依据+核心优势+目标特征+关键指标+风险信用+合作价值）
- **cultivation**：排名列表（rank/enterpriseCode/enterpriseName/industryCategory/enterpriseScale/developmentBottleneck/recommendationScore）+ 企业评价详情（判定维度+依据+核心优势+发展瓶颈+培育建议+关键指标+风险信用+所需支持）

**空态**：条件无匹配企业时任务正常完成，`candidateCount=0`，前端展示空态，不标记算法失败。
**证据不足**：保留企业结果，将对应维度 `evidenceStatus` 标为 `partial` 或 `unavailable`，不得伪造证据。

### 3.4 取消 `POST /tasks/{task_id}/cancel`

逻辑取消（见 ARCH §4.6 / D-31）：
- Python 标记内存 `cancelled` + **同步透传**给算法 `POST /gdf/tasks/{task_id}/cancel`
- 算法收到后设 `cancel_flag`，**每个节点开始时检查**，命中则终止
- 算法取消后发 `task_cancelled` Webhook（**不是 `task_failed`**）
- Python 收到 `task_cancelled` 回调后转发 Java
- 响应 `{code: 0, data: {task_id, status: "cancelled"}}`

---

## 4. 子类型与选择模式枚举

| subType | selectionMode | 名称 | 必填参数 | 权重键 |
|---|---|---|---|---|
| `attraction` | `filter` | 招引·条件筛选 | `filters`（enterpriseTags/industryDomains/geographicSources） | technologyMatch/growth/regionalFit |
| `attraction` | `candidate_workbench` | 招引·候选工作台 | `enterpriseCodes[]` | technologyMatch/growth/regionalFit |
| `cultivation` | `filter` | 培育·条件筛选 | `filters`（industryCategories/policyOrientations/enterpriseScales） | technologyBarrier/marketGrowth/teamBackground |
| `cultivation` | `candidate_workbench` | 培育·候选工作台 | `enterpriseCodes[]` | technologyBarrier/marketGrowth/teamBackground |

**约束**：
- 三项权重合计必须为 100
- `candidate_workbench` 至少选择 1 家企业
- `selectionMode` 只决定企业集合如何形成，不新增 analysisType、不新增 subType、不拆任务 API

---

## 5. Mock 策略

- science 异步框架未就绪前，gkx_ai_service 自造 Mock 结果
- attraction Mock：5 家候选企业排名 + 1 家企业评价详情（含 3 维判定+证据状态）
- cultivation Mock：5 家候选企业排名 + 1 家企业评价详情（含 3 维判定+发展瓶颈+培育建议）
- 部分维度 `evidenceStatus` 标为 `partial` 模拟证据不足场景
- 标注 🧪 MockBadge
- 切换 science 时仅改 `science_client.py` 内部实现，契约不变

---

## 6. 服务间调用

```
Java → gkx_ai_service /internal/gkx-ai/recommend/tasks
  → science_client.py HTTP 调 science /gdf/tasks（create-and-start）
  → 需要基础数据时调 gkx_search_service /internal/gkx-search/*
  → 算法完成后回调 gkx_ai_service /internal/gkx-ai/analysis/callback
  → Python 转发 Java /topic/v1/analysis/callback/recommend
```

---

## 6.5 JSON 字段命名风格（D-30）

> **Python ↔ 算法侧统一 `snake_case`**；Java 侧用 `camelCase`。常规字段 Java 用 `@JsonProperty` 对接 snake_case；**分析结果 `result` 例外**：Python 转 camelCase 后转发 Java（v3.2 D-30 修订）。Python 转 camelCase 后统一写 MinIO，转发 resultUrl 给 Java。Java 不存 result JSON、不碰分析结果 MinIO。

Python 侧所有 JSON 请求/响应字段一律 `snake_case`：`task_id` / `analysis_type` / `sub_type` / `enterprise_codes` / `callback_url` / `event` / `node_code` / `node_name` / `status` 等。result JSON 例外：Python 转 camelCase 后转发 Java。

---

## 7. 禁止

- 修改 `demo-algo-science` 仓任何文件
- 把推荐代码写进 `gkx_search_service/`
- 在 gkx_ai_service 写推荐评分/筛选算法——这些归 science
- 对 Java 暴露 science 原始路径
- 自生成 taskId（必须复用 Java 传入的）
- 返回 `pending` 状态给 Java
- 维护正式任务历史（历史只查 Java MySQL）
- 提供 `/tasks/history` 端点
- 管对比篮候选池 CRUD（由 Java 或既有任务承接）
- 伪造证据（证据不足时标 `evidenceStatus=partial/unavailable`）

---

## 8. DoD

1. `gkx_ai_service/views/recommend.py` 4 端点齐全（tasks/status/result/cancel）
2. 两种 subType × 两种 selectionMode 契约测试通过（4 种组合）
3. 空态（candidateCount=0）和证据不足（evidenceStatus=partial）场景覆盖
4. taskId 复用 Java 传入值，不自生成
5. status 不返回 pending，映射为 running
6. Mock 模式跑通创建→状态→结果→取消全链路
7. science_client.py 对接 science `/gdf/tasks`，Mock/真实切换不改变 Java 契约
8. 权重合计=100 校验
9. D9 血缘字段（metric_id/calc_process/source_tables/pending_ref）齐全
10. `/internal/*` 路径、OTel、CI、handoff 与 cost 四字段齐全
