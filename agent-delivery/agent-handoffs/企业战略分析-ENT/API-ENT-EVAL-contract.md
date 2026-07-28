# API 契约：gkx-ai-service 企业评估接口（供 Java Feign 对接）

- **整理人**：data-agent（2026-07-28 as-built 纠偏：api-agent / 监管 human:侯佳伟）
- **时间**：2026-07-28（**v5 as-built** — D-30 body-only、`sub_type` 取代 `mode`、对外任务生命周期归 CORE）；2026-07-25（v4）；2026-07-21（v3）
- **任务**：ENT-PY-EVAL-TASK（Python）+ ENT-JAVA-EVAL / ENT-JAVA-ANALYSIS-CORE（Java as-built）
- **服务**：gkx-ai-service（`demo-svc-topic-py` 仓 `gkx_ai_service/` 子项目）
- **端口**：8081（dev）
- **路由前缀**：`/internal/gkx-ai/evaluation`
- **当前模式**：Mock 优先（`GKX_MOCK_ENABLED=true`），评分结果为确定性 Mock；算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `false` 走真实 entan
- **响应包络**：统一 `{code, msg, data}`，`code=0` 成功，`code!=0` 业务错误
- **前端对外总表**：以 `API-ENT-full-catalog.md` #102–121 为准（本文件侧重 Python `/internal` + Feign）

> **v5 as-built（2026-07-28，对齐 Python v3.4 + Java CORE/EVAL）**：
> 1. **D-30**：`status` / `result` / `compare` / `cancel` 为 `POST /tasks/status|result|compare|cancel`，`task_id` 放 **body**；**禁止** `/tasks/{task_id}/...` 路径参数。
> 2. **命名**：分析小类权威字段为 **`sub_type` / `subType`**；旧字段 `mode` 仅作 Python 入参兼容别名，**新对接禁止再写 mode**。
> 3. **Java 落仓**：`gkxlumen-topic-async-service`；Feign 实类 `RemoteTopicAsyncAiPythonClient`；配置键 `python-ai-base-url` / `python-ai-service-name`（Nacos 可发现 `gkx-ai-service`）。
> 4. **对外分工**：任务 create/status/result/cancel/list/SSE → CORE `/topicAsync/topic/v1/analysis/tasks*`；四辅助 + templates → EVAL `/topicAsync/topic/v1/evaluation/**`。**禁止**第二套 `/evaluation/tasks` 生命周期。
> 5. 模板管理纯 Java（`evaluation_template`），Python 不提供 `/templates`。

> **v4 变更要点（仍有效）**：taskId 由 Java 传入；pending 不回传 Java；结果三套 sub_type schema；`created_by` 由 Java 透传。

> **Java 对接要点**：使用 `RemoteTopicAsyncAiPythonClient`（async-service），**不要**复用 `RemoteEnterprisePythonClient`（gkx-search）。

---

## 0. 三小类说明（`sub_type`）

评估支持三种小类（对齐 Wireframe-ENT-EVAL §2.2 + ARCH-ANALYSIS-TASK v3.2 §9；**废弃对外字段名 `mode`**）：

| sub_type | 中文名 | 最少企业数 | 结果结构 |
|---|---|---|---|
| `technology` | 技术力评估 | 2 | 五维雷达（技术创新/技术人才/技术投入/技术合作/技术转化）+ 排名 + 技术诊断 |
| `business` | 商业力评估 | 2 | 经营指标对比 + 排名 + 经营诊断/营收趋势/行业对标 |
| `competitiveness` | 综合竞争力评估 | 1 | 三维雷达（创新能力/经营能力/成长能力）+ 排名 + 综合诊断 + 参照均值/龙头 |

> **结果结构以 v3.2 §9 三套 sub_type schema 为最终契约**。下方的"维度键名固定4个"是旧四维评分计算模型的描述，仅用于 Python 内部评分计算阶段，**不等于结果展示结构**。

**评分计算维度键名**（Python 内部评分计算用，4 个）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

> ⚠️ 以上 4 个维度键仅用于 Python 评分计算；**结果展示结构**（雷达/排名/诊断）按 sub_type 不同，见 v3.2 §9。Java 侧用 `JsonNode`/`Map` 原样透传，不依赖这 4 个键。

---

## 1. 接口清单（Python `/internal`，9 端点含 cancel）

| # | 方法 | 路径（相对 `/internal/gkx-ai/evaluation`） | 作用 | 异步 |
|---|---|---|---|---|
| 1 | POST | `/industries` | 行业列表 | 否 |
| 2 | POST | `/indicators` | 指标注册表（按 `sub_type`+`industry`） | 否 |
| 3 | POST | `/precheck` | 数据预检 | 否 |
| 4 | POST | `/tasks` | 创建评估任务（**接受 Java 传入的 task_id**） | 是 |
| 5 | POST | `/tasks/status` | 查状态（body.`task_id`；D-30） | 否 |
| 6 | POST | `/tasks/result` | 查结果（body.`task_id`；三套 sub_type schema） | 否 |
| 7 | POST | `/tasks/compare` | 双企对比（body.`task_id`/`enterprise_a`/`enterprise_b`） | 否 |
| 8 | POST | `/tasks/history` | 历史（仅 svc 自测；正式历史查 Java `analysis_task`） | 否 |
| 9 | POST | `/tasks/cancel` | 取消（body.`task_id`；D-30 / D-31） | 否 |

> **模板管理已移交 Java 侧**：Python 不提供 `/templates`。  
> **禁止**再使用 `/tasks/{task_id}/status|result|compare|cancel` 路径参数写法。

---

## 2. 逐接口契约

### 2.0 行业列表

`POST /internal/gkx-ai/evaluation/industries`

无请求体。返回预置行业列表（商业力/综合竞争力配置页"评价行业"下拉用）。

**响应**：

```json
{
  "code": 0,
  "data": {
    "is_preview": true,
    "items": [
      {"industry_code": "ICT", "industry_name": "信息通信技术", "note": "侧重研发投入与专利产出"},
      {"industry_code": "SEMICON", "industry_name": "集成电路", "note": "侧重核心技术覆盖与专利引用"},
      {"industry_code": "BIO", "industry_name": "生物医药", "note": "侧重研发周期与创新指数"},
      {"industry_code": "NEV", "industry_name": "新能源", "note": "侧重成长性与市场表现"},
      {"industry_code": "GENERAL", "industry_name": "通用制造", "note": "均衡指标，无特殊侧重"}
    ]
  }
}
```

> `is_preview=true` 表示当前为模拟预览（正式行业映射受 Q014 阻断）。

---

### 2.1 指标注册表

`POST /internal/gkx-ai/evaluation/indicators`

**请求体**：

```json
{"sub_type": "business", "industry": "ICT"}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| sub_type | string | 否 | `technology`/`business`/`competitiveness`；缺省返回三小类全部。旧别名 `mode` 仅兼容 |
| industry | string | 否 | 行业码（常配合 business）；按行业过滤适用指标 + 返回整数权重 |

**响应（sub_type + industry，行业过滤）**：

```json
{
  "code": 0,
  "data": {
    "sub_type": "business",
    "sub_type_name": "商业力评估",
    "industry": "ICT",
    "min_enterprises": 2,
    "default_weights": {"innovation": 0.2, "operation": 0.5, "growth": 0.2, "risk": 0.1},
    "industry_weights": {"innovation": 35, "operation": 25, "growth": 25, "risk": 15},
    "dimensions": ["innovation", "operation", "growth", "risk"],
    "groups": [ ... 按行业过滤后的指标树 ... ],
    "is_preview": true,
    "preview_note": "行业模拟预览、非正式行业评价标准"
  }
}
```

| 新增字段 | 说明 |
|---|---|
| industry_weights | 行业整数权重（合计100，对齐 Wireframe "整数默认权重保持合计100%"） |
| is_preview | 是否模拟预览（Q014 未闭合均为 true） |
| preview_note | 预览免责声明 |

| indicator 字段 | 说明 |
|---|---|
| key | 指标键 |
| name | 指标中文名 |
| metric_id | D9 血缘指标 ID（`GAP-*` 表示未登记） |
| data_status | `available`(可用) / `pending`(待Q014) / `gap`(未登记/无来源) |
| unit | 单位 |
| direction | `positive`(越高越好) / `negative`(越低越好) |
| source | 数据来源 |
| default_weight | 默认权重（整数，0-100） |

---

### 2.2 数据预检（增强）

`POST /internal/gkx-ai/evaluation/precheck`

**请求体**：

```json
{
  "enterprise_codes": ["6bc50eca...", "6eeabc49..."],
  "sub_type": "technology"
}
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "total": 3,
    "found": 3,
    "missing_codes": [],
    "sub_type": "technology",
    "sub_type_name": "技术力评估",
    "min_enterprises": 2,
    "per_enterprise": [
      {
        "enterprise_code": "6bc50eca...",
        "enterprise_name": "深圳科技有限公司",
        "coverage_rate": 0.84,
        "confidence": "high",
        "critical_missing": 0,
        "available_indicators": 5
      }
    ],
    "overall_confidence": "high",
    "ready": true,
    "block_reason": null,
    "data_source": "mock"
  }
}
```

| 字段 | 说明 |
|---|---|
| per_enterprise[].coverage_rate | 该企业指标覆盖率（0-1） |
| per_enterprise[].confidence | `high`(≥80%) / `medium`(≥50%) / `low`(<50%) |
| per_enterprise[].critical_missing | 关键指标缺失数 |
| overall_confidence | 整体可信度（取最低） |
| ready | 是否可生成 |
| block_reason | 不可生成原因（missing/低覆盖/关键指标全缺） |

**生成规则**：覆盖率 <50% 或关键指标全缺 → `ready=false`；低可信可确认继续。

---

### 2.3 创建评估任务（三模式）

`POST /internal/gkx-ai/evaluation/tasks`

> **taskId 规则（v4）**：`task_id` **由 Java 唯一生成并传入**，Python 必须接受并复用，不自生成。格式 `{PREFIX}-YYYYMMDD-NNN`（如 `EVAL-20260724-001`）。status/result/compare 均使用该 taskId。

**请求体**：

```json
{
  "task_id": "EVAL-20260725-001",
  "enterprise_codes": ["6bc50eca...", "6eeabc49..."],
  "mode": "technology",
  "weights": {"innovation": 0.5, "operation": 0.2, "growth": 0.2, "risk": 0.1},
  "template_id": "TPL-TECH-INNOVATION",
  "indicators": ["tech_power_score", "patent_grant_count", "rd_investment_ratio"],
  "task_name": "2026Q3技术力评估",
  "created_by": "user001"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| task_id | string | **是** | Java 生成的全局唯一 taskId，Python 复用，不自生成 |
| enterprise_codes | string[] | 是 | 企业 org_id 列表 |
| mode | string | 否 | 缺省 `competitiveness` |
| weights | object | 否 | 自定义维度权重；缺省用模板或 mode 默认 |
| template_id | string | 否 | 模板 ID（需同 mode） |
| indicators | string[] | 否 | 选中的指标 key 列表 |
| task_name | string | 否 | 缺省自动生成 `{模式名}-{6位}` |
| created_by | string | 否 | 创建人（由 Java 登录态透传，前端传值忽略） |

**权重优先级**：显式 `weights` > `template_id`(同 mode) > mode 默认

**响应**：

```json
{"code": 0, "data": {"task_id": "EVAL-20260725-001", "status": "running"}}
```

> **status 说明（v4）**：Python 创建后立即返回 `running`（算法内部可能排队 pending，但对 Java 透明，不回传 pending）。

---

### 2.4 查任务状态

`POST /internal/gkx-ai/evaluation/tasks/status`（D-30：body 传 `task_id`，**禁止** path `{task_id}`）

**请求体**：

```json
{"task_id": "EVAL-20260725-001"}
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "task_id": "EVAL-20260725-001",
    "status": "success",
    "progress": 100,
    "stage": "assembled",
    "error": null,
    "sub_type": "technology",
    "sub_type_name": "技术力评估",
    "created_at": "...",
    "updated_at": "..."
  }
}
```

**六阶段 stage**（对齐 Wireframe F-EVAL-06）：

| stage | progress | 说明 |
|---|---|---|
| submitted | 10 | 任务提交 |
| validating | 25 | 权限与配置校验 |
| data_gathering | 45 | 企业数据汇聚 |
| computing | 65 | 指标计算 |
| confidence_check | 85 | 可信度校验 |
| assembled | 100 | 结果组装 |

**状态流转（v4）**：`running` → `success` / `failed`

> **pending 边界**：`pending` 只在算法侧内部存在（排队待跑），**不回传 Java**。Python status 接口返回值取 `running`/`success`/`failed`；算法内部 pending 对 Java 透明，Adapter 收到时映射为 Java `running`。Java MySQL 永不保存 pending。

---

### 2.5 查评估结果

`POST /internal/gkx-ai/evaluation/tasks/result`（D-30：body 传 `task_id`）

> **结果结构（v5）**：以 `ARCH-ANALYSIS-TASK-设计方案.md` v3.2 §9 三套 **sub_type** 结构为最终契约。下方旧四维统一结构**已废弃**，仅作历史参考。

> **权威契约位置**：`agent-handoffs/企业战略分析-ENT/ARCH-ANALYSIS-TASK-设计方案.md` §9。Java 侧用 `JsonNode`/`Map<String,Object>` 原样透传。

**请求体**：

```json
{"task_id": "EVAL-20260725-001"}
```

**响应（旧四维结构，已废弃，待按 v3.2 §9 理解）**：

```json
{
  "code": 0,
  "data": {
    "scores": [
      {
        "enterprise_code": "68dd51ce...",
        "total_score": 76.68,
        "rank": 1,
        "dimensions": {"innovation": 88.31, "operation": 50.98, "growth": 85.04, "risk": 53.18},
        "weights": {"innovation": 0.5, "operation": 0.2, "growth": 0.2, "risk": 0.1},
        "radar": [
          {"axis": "innovation", "value": 88.31, "normalized": 88.31},
          {"axis": "operation", "value": 50.98, "normalized": 50.98},
          {"axis": "growth", "value": 85.04, "normalized": 85.04},
          {"axis": "risk", "value": 53.18, "normalized": 53.18}
        ],
        "indicator_scores": [
          {
            "key": "patent_grant_count",
            "name": "专利授权量",
            "metric_id": "M_ENT_PATENT_GRANT_COUNT",
            "data_status": "available",
            "dimension": "innovation",
            "group_key": "tech_patent",
            "group_name": "创新产出",
            "value": 72.45,
            "raw_value": null,
            "unit": "件",
            "direction": "positive",
            "weight": 20,
            "normalized_score": 72.45
          },
          {
            "key": "patent_citation",
            "name": "专利引用",
            "metric_id": "GAP-METRIC-BID-01",
            "data_status": "gap",
            "dimension": "innovation",
            "group_key": "tech_patent",
            "group_name": "创新产出",
            "value": null,
            "raw_value": null,
            "unit": "次",
            "direction": "positive",
            "weight": 0,
            "normalized_score": null
          }
        ],
        "diagnosis": {
          "level": "risk",
          "advantages": ["innovation", "growth"],
          "weaknesses": ["operation", "risk"],
          "suggestions": ["建议加强operation维度投入", "建议加强risk维度投入"]
        },
        "confidence": "medium",
        "coverage_rate": 0.74,
        "data_source": "mock",
        "model_version": "mock-v0.1"
      }
    ],
    "data_source": "mock",
    "model_version": "mock-v0.1",
    "mode": "technology",
    "mode_name": "技术力评估"
  }
}
```

| scores[] 字段 | 说明 |
|---|---|
| total_score | 综合得分（加权汇总，0-100） |
| rank | 排名（1 起） |
| dimensions | 各维度得分（0-100） |
| radar | 雷达轴数据（axis/value/normalized） |
| indicator_scores | 指标级得分明细（维度折叠面板用，见下表） |
| diagnosis.level | `healthy` / `warn` / `risk` |
| diagnosis.advantages | 优势维度（≥75） |
| diagnosis.weaknesses | 短板维度（<55） |
| diagnosis.suggestions | 改进建议 |
| confidence | `high` / `medium` / `low` |
| coverage_rate | 该企业覆盖率 |

| indicator_scores[] 字段 | 说明 |
|---|---|
| key | 指标键 |
| name | 指标中文名 |
| metric_id | D9 血缘指标 ID |
| data_status | `available`/`pending`/`gap`；gap 时 value=null |
| dimension | 所属维度（innovation/operation/growth/risk） |
| group_key / group_name | 所属分组 |
| value | 归一化得分（0-100）；gap 时为 null |
| raw_value | 原始指标值（如 120件、3.5%），算法侧填充 |
| unit | 单位 |
| direction | `positive`/`negative` |
| weight | 权重（整数 0-100） |
| normalized_score | 归一化得分（同 value，算法侧可能不同） |

---

### 2.6 双企对比

`POST /internal/gkx-ai/evaluation/tasks/compare`（D-30：`task_id` 在 body，**禁止** path）

**请求体**：

```json
{
  "task_id": "EVAL-20260725-001",
  "enterprise_a": "6bc50eca...",
  "enterprise_b": "68dd51ce..."
}
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "enterprise_a": { ... },
    "enterprise_b": { ... },
    "dimension_diff": [
      {"dimension": "innovation", "value_a": 57.56, "value_b": 88.31, "diff": -30.75, "advantage": "b"},
      {"dimension": "operation", "value_a": 95.23, "value_b": 50.98, "diff": 44.25, "advantage": "a"}
    ],
    "total_diff": -12.01
  }
}
```

| dimension_diff 字段 | 说明 |
|---|---|
| diff | A - B（正数 A 优势，负数 B 优势） |
| advantage | `a` / `b` / `tie` |

---

### 2.7 历史任务列表

`POST /internal/gkx-ai/evaluation/tasks/history`

> 仅 svc 自测 / Mock；**正式历史只查 Java `analysis_task`**，前端不走本端点。

**请求体**：

```json
{"page": 1, "size": 20, "status": "success", "sub_type": "technology"}
```

**响应 items[] 字段**：`task_id` / `task_name` / `status` / `sub_type` / `sub_type_name` / `enterprise_count` / `created_by` / `created_at` / `updated_at`

---

## 3. Java Feign / 对外路径（as-built）

### 3.1 FeignClient（实类）

> 落仓：`gkxlumen-topic-async-service`  
> 实类：`RemoteTopicAsyncAiPythonClient`  
> 配置：`TopicAsyncAiPythonFeignConfig`；寻址 `python-ai-base-url` / `python-ai-service-name`（可发现 `gkx-ai-service`）  
> 模板管理由 Java 侧自行实现，不调 Python。

```java
@FeignClient(contextId = "remoteTopicAsyncAiPythonClient",
    name = "gkx-ai-service",
    configuration = TopicAsyncAiPythonFeignConfig.class)
public interface RemoteTopicAsyncAiPythonClient {

    @PostMapping("/internal/gkx-ai/evaluation/industries")
    R<Map<String, Object>> evalIndustries(@RequestBody Map<String, Object> req);

    @PostMapping("/internal/gkx-ai/evaluation/indicators")
    R<Map<String, Object>> evalIndicators(@RequestBody Map<String, Object> req);

    @PostMapping("/internal/gkx-ai/evaluation/precheck")
    R<Map<String, Object>> evalPrecheck(@RequestBody Map<String, Object> req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks")
    R<Map<String, Object>> evalCreateTask(@RequestBody Map<String, Object> req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/status")
    R<Map<String, Object>> evalStatus(@RequestBody Map<String, Object> req); // body.task_id

    @PostMapping("/internal/gkx-ai/evaluation/tasks/result")
    R<Map<String, Object>> evalResult(@RequestBody Map<String, Object> req); // body.task_id

    @PostMapping("/internal/gkx-ai/evaluation/tasks/compare")
    R<Map<String, Object>> evalCompare(@RequestBody Map<String, Object> req); // task_id/enterprise_a/enterprise_b

    @PostMapping("/internal/gkx-ai/evaluation/tasks/history")
    R<Map<String, Object>> evalHistory(@RequestBody Map<String, Object> req);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/cancel")
    R<Map<String, Object>> evalCancel(@RequestBody Map<String, Object> req); // body.task_id
}
```

### 3.2 对外 REST 路径（前端真源）

网关前缀：`/topicAsync`（StripPrefix=1）。完整路径见 `API-ENT-full-catalog.md`。

| 对外路径（经网关） | 归属 | 下游 |
|---|---|---|
| `POST /topicAsync/topic/v1/evaluation/industries` | EVAL | gkx-ai industries |
| `POST /topicAsync/topic/v1/evaluation/indicators` | EVAL | gkx-ai indicators |
| `POST /topicAsync/topic/v1/evaluation/precheck` | EVAL | gkx-ai precheck |
| `POST /topicAsync/topic/v1/evaluation/tasks/compare` | EVAL | gkx-ai compare（body.`task_id`） |
| `GET/POST/PUT/DELETE /topicAsync/topic/v1/evaluation/templates*` | EVAL | Java MySQL（不转发 Python） |
| `POST /topicAsync/topic/v1/analysis/tasks` | CORE | 按 analysisType 路由；`enterprise_eval` → gkx-ai `/tasks` |
| `GET /topicAsync/topic/v1/analysis/tasks/{taskId}` | CORE | Java MySQL（非 Python path） |
| `GET /topicAsync/topic/v1/analysis/tasks/{taskId}/result` | CORE | Java MySQL 指针 |
| `POST /topicAsync/topic/v1/analysis/tasks/{taskId}/cancel` | CORE | 本地取消 + Feign `…/tasks/cancel` body |

> **已删除（禁止再实现）**：`/topic/v1/evaluation/tasks` create/status/result/history 第二任务中心。

---

## 4. 联调验证

### Mock 模式（当前可用）

可用 Mock org_id：
```
6bc50eca3435d4b53fb7bf661d058a47
6eeabc4997a7838e86d559ac0c9bc93e
68dd51ce03544ad958d3533729d954b6
```

验证流程：
1. `industries` → 取预置行业列表
2. `indicators` → `sub_type=business` + `industry=ICT` → 行业过滤指标 + 整数权重
3. `precheck` → 3 家企业 + technology → ready/confidence
4. CORE `analysis/tasks` → `analysisType=enterprise_eval` → taskId
5. CORE `analysis/tasks/{id}` / SSE → 至 success
6. CORE `analysis/tasks/{id}/result` → 结果指针；大结果从 MinIO
7. EVAL `evaluation/tasks/compare` → body.taskId + A/B

### 冒烟测试结果（2026-07-25 v4，路径已按 v5 理解）

```
industries: 5 industries (ICT/SEMICON/BIO/NEV/GENERAL), is_preview=true ✓
indicators(business+ICT): 7 indicators, industry_weights={35,25,25,15}, is_preview=true ✓
templates: 404 on Python（已移交 Java）✓
create task: Java 传入 task_id，Python 复用 ✓
result: 按 v3.2 §9 三套 sub_type 结构 ✓（Python 侧已落地）
```

---

## 5. 已知限制

| 项 | 现状 | 后续 |
|---|---|---|
| 评分来源 | Mock（md5 种子） | entan 真实算法（ENT-ALGO-EVAL-INTERACTIVE） |
| 覆盖率 | Mock 确定性生成 | 接 search 真实字段覆盖率 |
| 指标值 | Mock 归一化得分 | 算法侧按指标树计算 + raw_value 原始值 |
| 行业映射 | 模拟预览（5 行业） | Q014 闭合后接正式行业映射 |
| 任务持久化 | Python 内存态（仅自测/Mock） | 正式任务真源为 Java MySQL `analysis_task`；Python 不新建任务表 |
| 模板管理 | 已移交 Java async-service | `evaluation_template` CRUD + seed |
| D9 血缘 | 指标树含 metric_id，结果含 data_source | 补 calc_process 8 件套 |
| Q014 阻断指标 | data_status=gap 不进评分 | 待甲方确认后升 available |
| 旧字段 `mode` | Python 入参仍兼容 | 新对接一律 `sub_type`/`subType` |
| compare `_raw_scores` | Mock 创建任务可写；联调回调需确认回填 | 否则 compare 可能 404 |
