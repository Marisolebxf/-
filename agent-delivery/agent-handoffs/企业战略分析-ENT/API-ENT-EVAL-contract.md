# API 契约：gkx-ai-service 企业评估接口（供 Java Feign 对接）

- **整理人**：data-agent
- **时间**：2026-07-21（v3 — 删模板管理移交Java / 加行业指标 / 加指标级明细）
- **任务**：ENT-PY-EVAL-TASK
- **服务**：gkx-ai-service（`demo-svc-topic-py` 仓 `gkx_ai_service/` 子项目）
- **端口**：8081（dev）
- **路由前缀**：`/internal/gkx-ai/evaluation`
- **当前模式**：Mock 优先（`GKX_MOCK_ENABLED=true`），评分结果为确定性 Mock；算法侧 `ENT-ALGO-EVAL-INTERACTIVE` 就绪后切 `false` 走真实 entan
- **响应包络**：统一 `{code, msg, data}`，`code=0` 成功，`code!=0` 业务错误

> **Java 对接要点**：新建独立 FeignClient（`RemoteEnterpriseAiPythonClient`），不要复用 `RemoteEnterprisePythonClient`（那个指向 gkx-search-service:8080）。下游寻址配置项：`gkxlumen.topic.enterprise.python-ai-base-url`（或 Nacos 服务发现 `gkx-ai-service`）。

---

## 0. 三模式说明

评估支持三种模式（对齐 Wireframe-ENT-EVAL §2.2）：

| mode | 中文名 | 最少企业数 | 默认维度权重 |
|---|---|---|---|
| `technology` | 技术力评估 | 2 | innovation:0.5 / operation:0.2 / growth:0.2 / risk:0.1 |
| `business` | 商业力评估 | 2 | innovation:0.2 / operation:0.5 / growth:0.2 / risk:0.1 |
| `competitiveness` | 综合竞争力评估 | 1 | 四维各 0.25 |

**维度键名**（固定 4 个，评分计算用）：

| 键 | 含义 |
|---|---|
| innovation | 创新能力 |
| operation | 经营能力 |
| growth | 成长性 |
| risk | 风险水平 |

---

## 1. 接口清单（8 端点）

| # | 方法 | 路径 | 作用 | 异步 |
|---|---|---|---|---|
| 1 | POST | `/industries` | 行业列表（商业力/综合竞争力配置页用） | 否 |
| 2 | POST | `/indicators` | 指标注册表（按 mode+industry 返回指标树+权重） | 否 |
| 3 | POST | `/precheck` | 数据预检（企业存在性 + 覆盖率 + 可信度） | 否 |
| 4 | POST | `/tasks` | 创建评估任务（三模式） | 是（立即返回 task_id） |
| 5 | POST | `/tasks/{task_id}/status` | 查任务状态（含六阶段 stage） | 否 |
| 6 | POST | `/tasks/{task_id}/result` | 查评估结果（评分+排名+雷达+诊断+指标明细+可信度） | 否 |
| 7 | POST | `/tasks/{task_id}/compare` | 双企对比（维度差值） | 否 |
| 8 | POST | `/tasks/history` | 历史任务列表（支持 mode 过滤） | 否 |

> **模板管理已移交 Java 侧**：系统模板（预定义，按模式分几类）+ 个人模板 CRUD 均由 Java 维护，Python 不提供 `/templates` 端点。

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
{"mode": "business", "industry": "ICT"}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| mode | string | 否 | `technology`/`business`/`competitiveness`；缺省返回三模式全部 |
| industry | string | 否 | 行业码（需配合 mode）；按行业过滤适用指标 + 返回整数权重 |

**响应（mode + industry，行业过滤）**：

```json
{
  "code": 0,
  "data": {
    "mode": "business",
    "mode_name": "商业力评估",
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
  "mode": "technology"
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
    "mode": "technology",
    "mode_name": "技术力评估",
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

**请求体**：

```json
{
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
| enterprise_codes | string[] | 是 | 企业 org_id 列表 |
| mode | string | 否 | 缺省 `competitiveness` |
| weights | object | 否 | 自定义维度权重；缺省用模板或 mode 默认 |
| template_id | string | 否 | 模板 ID（需同 mode） |
| indicators | string[] | 否 | 选中的指标 key 列表 |
| task_name | string | 否 | 缺省自动生成 `{模式名}-{6位}` |
| created_by | string | 否 | 创建人 |

**权重优先级**：显式 `weights` > `template_id`(同 mode) > mode 默认

**响应**：

```json
{"code": 0, "data": {"task_id": "EVAL-7155519912bf", "status": "pending"}}
```

---

### 2.4 查任务状态

`POST /internal/gkx-ai/evaluation/tasks/{task_id}/status`

**响应**：

```json
{
  "code": 0,
  "data": {
    "task_id": "EVAL-7155519912bf",
    "status": "success",
    "progress": 100,
    "stage": "assembled",
    "error": null,
    "mode": "technology",
    "mode_name": "技术力评估",
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

**状态流转**：`pending` → `running` → `success` / `failed`

---

### 2.5 查评估结果

`POST /internal/gkx-ai/evaluation/tasks/{task_id}/result`

**响应**：

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

`POST /internal/gkx-ai/evaluation/tasks/{task_id}/compare`

**请求体**：

```json
{
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

**请求体**：

```json
{"page": 1, "size": 20, "status": "success", "mode": "technology"}
```

**响应 items[] 字段**：`task_id` / `task_name` / `status` / `mode` / `mode_name` / `enterprise_count` / `created_by` / `created_at` / `updated_at`

---

## 3. Java Feign 对接建议

### 3.1 FeignClient（8 方法）

> **模板管理由 Java 侧自行实现**（系统模板预定义 + 个人模板 CRUD），不调 Python。

```java
@FeignClient(contextId = "remoteEnterpriseAiPythonClient",
    name = "topic-enterprise-ai-python",
    configuration = EnterpriseAiPythonFeignConfig.class)
public interface RemoteEnterpriseAiPythonClient {

    @PostMapping("/internal/gkx-ai/evaluation/industries")
    R<EvalIndustriesResponse> industries();

    @PostMapping("/internal/gkx-ai/evaluation/indicators")
    R<EvalIndicatorsResponse> indicators(@RequestBody EvalIndicatorsRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/precheck")
    R<EvalPrecheckResponse> precheck(@RequestBody EvalPrecheckRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/tasks")
    R<EvalTaskCreateResponse> createTask(@RequestBody EvalTaskCreateRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/status")
    R<EvalTaskStatusResponse> taskStatus(@PathVariable("taskId") String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/result")
    R<EvalTaskResultResponse> taskResult(@PathVariable("taskId") String taskId);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/{taskId}/compare")
    R<EvalCompareResponse> taskCompare(@PathVariable("taskId") String taskId, @RequestBody EvalCompareRequest request);

    @PostMapping("/internal/gkx-ai/evaluation/tasks/history")
    R<EvalTaskHistoryResponse> taskHistory(@RequestBody EvalTaskHistoryRequest request);
}
```

### 3.2 对外 REST 路径建议

| 对外路径 | 转发到 |
|---|---|
| `POST /topic/v1/evaluation/industries` | gkx-ai industries |
| `POST /topic/v1/evaluation/indicators` | gkx-ai indicators |
| `POST /topic/v1/evaluation/precheck` | gkx-ai precheck |
| `POST /topic/v1/evaluation/tasks` | gkx-ai tasks |
| `POST /topic/v1/evaluation/tasks/{taskId}/status` | gkx-ai status |
| `POST /topic/v1/evaluation/tasks/{taskId}/result` | gkx-ai result |
| `POST /topic/v1/evaluation/tasks/{taskId}/compare` | gkx-ai compare |
| `POST /topic/v1/evaluation/tasks/history` | gkx-ai history |

> 模板相关 REST（系统模板列表/个人模板 CRUD）由 Java 侧自行实现，不转发 Python。

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
2. `indicators` → mode=business + industry=ICT → 行业过滤指标 + 整数权重
3. `precheck` → 3 家企业 + technology 模式 → ready=true, confidence=high
4. `tasks` → 创建 business 任务 → task_id
5. `tasks/{id}/status` → 轮询至 success/stage=assembled
6. `tasks/{id}/result` → 排名 + 雷达 + 诊断 + **指标级明细** + 可信度
7. `tasks/{id}/compare` → A vs B 维度差值

### 冒烟测试结果（2026-07-21 v3，全部通过）

```
industries: 5 industries (ICT/SEMICON/BIO/NEV/GENERAL), is_preview=true ✓
indicators(business+ICT): 7 indicators, industry_weights={35,25,25,15}, is_preview=true ✓
templates: 404 Not Found（已移交 Java）✓
create task(business+ICT): EVAL-ce474de6a81f ✓
result: 2 scores, indicator_scores 7个/企业（gap指标value=null, available有分）✓
```

---

## 5. 已知限制

| 项 | 现状 | 后续 |
|---|---|---|
| 评分来源 | Mock（md5 种子） | entan 真实算法（ENT-ALGO-EVAL-INTERACTIVE） |
| 覆盖率 | Mock 确定性生成 | 接 search 真实字段覆盖率 |
| 指标值 | Mock 归一化得分 | 算法侧按指标树计算 + raw_value 原始值 |
| 行业映射 | 模拟预览（5 行业） | Q014 闭合后接正式行业映射 |
| 任务持久化 | 进程内 dict | 接 MySQL eval_task/eval_task_result（DDL 需按 MySQL 定稿） |
| 模板管理 | 已移交 Java | Java 侧实现系统模板 + 个人模板 CRUD |
| D9 血缘 | 指标树含 metric_id，结果含 data_source | 补 calc_process 8 件套 |
| Q014 阻断指标 | data_status=gap 不进评分 | 待甲方确认后升 available |
