# 派单包：ENT-PY-EVAL-TASK

- **派单方**：coordinator（architect-agent 起草）
- **时间**：2026-07-21
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强
- **Sprint**：2026-W30
- **Epic**：E-ENT-SCRUM-PDR
- **仓**：`demo-svc-topic-py`（数据侧 monorepo，**非**算法侧 `demo-algo-ent-analysis`）
- **子项目**：**新建 `gkx_ai_service/`**（与 `gkx_search_service/` 平级，共用 `gkx_common/`）—— 对应架构预设计 gkx-ai-service
- **上游依赖**：`ENT-ALGO-EVAL-INTERACTIVE`（algorithm-agent，entan 扩展交互式评估接口）—— **硬依赖联调**；Mock 模式可先行
- **架构分析真源**：`agent-handoffs/企业战略分析-ENT/ENT-ARCH-COMPARE-EVAL-分析.md`

---

## 0. 铁律前置（违反必拒）

1. **本任务只在 `demo-svc-topic-py` 仓**。**禁止**修改 `demo-algo-ent-analysis`（算法组项目，归 algorithm-agent）
2. **评估归 gkx-ai-service，不归 gkx-search-service**。评估 = 调基础数据 + 模型计算 + 任务编排，按架构预设计 §8 属 ai-service（推理+推荐+推演）。**新建 `gkx_ai_service/` 子项目**，与 `gkx_search_service/` 平级，共用 `gkx_common/`。**禁止**把评估代码塞进 `gkx_search_service/`
3. **gkx_ai_service 是算法服务的屏蔽层**。Java 只调 gkx_ai_service `/internal/gkx-ai/*`；gkx_ai_service 内部 HTTP 调 entan `/v1/*`；需要基础数据时 HTTP 调 gkx_search_service `/internal/gkx-search/*`
4. **算法只在 Python**。本任务是数据编排层，不做算法计算（评分/排名/诊断由 entan 提供）
5. **Mock 优先**。ENT-ALGO-EVAL-INTERACTIVE 未就绪前，用 Mock 评估结果；切换 entan 时仅改内部 HTTP 客户端，`/internal/gkx-ai/*` 契约不变
6. **数据血缘 D9**。评估结果中每个统计指标须可追溯 metric_id 或标 🟡 GAP（Q014/K-O7 阻断项）

---

## 1. 目标

在 `demo-svc-topic-py` 仓**新建 `gkx_ai_service/` 子项目**（gkx-ai-service 落地），实现企业评估任务编排层，支撑 Wireframe-ENT-EVAL v1.6 的配置→生成→结果→历史全流程。Java 经 Feign 调本服务，本服务屏蔽 entan 算法服务并调 gkx_search_service 获取基础数据。

---

## 2. 必读（按优先级）

| 优先级 | 文件 | 用途 |
|---|---|---|
| P0 | `agent-handoffs/企业战略分析-ENT/ENT-ARCH-COMPARE-EVAL-分析.md` | 架构分析真源（调用链/三层拆解/依赖/服务归属） |
| P0 | `agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/Wireframe-ENT-EVAL.md` | **UI 契约真源**（F-EVAL-01~08 字段表/交互/状态矩阵） |
| P0 | `agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/IA-ENT-EVAL.md` | IA/路由/权限 |
| P0 | `agent-delivery/企业维度-Python微服务架构预设计.md` §8 | **gkx-ai-service 定位**（推理+推荐+推演，调①②③+模型） |
| P0 | `agent-delivery/data-lineage-policy.md` | D9 八件套 |
| P1 | `repos/demo-svc-topic-py/gkx_search_service/main.py` | **子项目骨架参考**（FastAPI 入口/router 注册/中间件/OTel） |
| P1 | `repos/demo-svc-topic-py/gkx_search_service/deps.py` | deps 模式参考（should_use_mock / get_es_or_none / get_mock_store） |
| P1 | `repos/demo-svc-topic-py/gkx_common/` | 公共库（config/response/observability/mock/db/es）—— 直接复用 |
| P1 | `repos/demo-algo-ent-analysis/api/entan_analysis_routes.py` | entan 现有 `/v1/score` `/v1/ranking` `/v1/diagnosis`（仅参考，**不改**） |

---

## 3. 范围

### 3.1 新建子项目骨架（与 gkx_search_service 平级）

```
demo-svc-topic-py/
├── gkx_common/              # 已有公共库（复用，不改）
├── gkx_search_service/      # 已有 search 服务（不改）
└── gkx_ai_service/          # ← 本任务新建
    ├── __init__.py
    ├── main.py              # FastAPI 入口（uvicorn gkx_ai_service.main:app --port 8081）
    ├── deps.py              # 依赖注入（mock 开关 / entan client / search client）
    ├── entan_client.py      # entan HTTP 客户端（Mock 模式不调；联调模式 HTTP 调 entan /v1/*）
    ├── search_client.py     # gkx_search_service HTTP 客户端（调 /internal/gkx-search/* 取基础数据/预检）
    ├── views/
    │   ├── __init__.py
    │   └── evaluation.py    # 评估任务编排层（本任务核心，7 端点）
    └── sql/
        ├── eval_task.sql
        ├── eval_task_result.sql
        └── eval_template.sql
```

> `main.py` 参照 `gkx_search_service/main.py` 骨架：FastAPI + CORSMiddleware + TraceHeaderMiddleware + lifespan + router include。端口 **8081**（search 用 8080，避免冲突）。

### 3.2 新增端点（7 个，prefix=`/internal/gkx-ai/evaluation`）

| # | 端点 | 方法 | 功能 | 对应 Wireframe Frame |
|---|---|---|---|---|
| 1 | `/internal/gkx-ai/evaluation/precheck` | POST | 数据覆盖与可信度预检（输入企业集合+模式+指标，返回每家覆盖度/可信度/可生成性） | F-EVAL-01 ④ |
| 2 | `/internal/gkx-ai/evaluation/tasks` | POST | 创建评估任务（企业集合+模式+指标+权重+模板快照 → 返回 task_id，后台异步计算） | F-EVAL-01 生成评估 / F-EVAL-06 |
| 3 | `/internal/gkx-ai/evaluation/tasks/{task_id}/status` | GET | 查询任务状态（六阶段：提交→校验→数据汇聚→指标计算→可信校验→结果组装） | F-EVAL-06 |
| 4 | `/internal/gkx-ai/evaluation/tasks/{task_id}/result` | GET | 查询评估结果（KPI+雷达+排名+诊断+可信度+单企/双企视角） | F-EVAL-02 |
| 5 | `/internal/gkx-ai/evaluation/tasks` | GET | 最近评估列表（分页+模式筛选+企业搜索） | F-EVAL-03 |
| 6 | `/internal/gkx-ai/evaluation/templates` | GET | 个人模板列表（按模式分组，含指标数/保存时间） | F-EVAL-01 ② |
| 7 | `/internal/gkx-ai/evaluation/templates` | POST | 保存个人模板（名称+模式+指标+权重，不存企业对象） | F-EVAL-01 保存个人模板 |

### 3.3 数据模型（gkx_ai_service 自管 PG 表，demo_gdf_data 库）

| 表 | 用途 | 关键字段 |
|---|---|---|
| `eval_task` | 评估任务 | task_id, mode(technology/business/competitiveness), enterprise_codes[], indicators_snapshot, weights_snapshot, template_id, template_version, status, confidence_level, created_at, finished_at |
| `eval_task_result` | 评估结果快照 | task_id, kpi_json, radar_json, ranking_json, diagnosis_json, confidence_json, metric_ids[] |
| `eval_template` | 个人模板 | template_id, user_id, mode, name, indicators, weights, created_at |

> DDL 放 `gkx_ai_service/sql/`；Mock 模式不需要建表（内存 dict）。

### 3.4 评估计算策略（分阶段）

| 阶段 | 计算来源 | 说明 |
|---|---|---|
| **Mock 模式**（本任务交付） | gkx_ai_service 自造 Mock 结果 | 固定种子生成评分/排名/诊断/雷达数据；标注 🧪 MockBadge；指标受 Q014/K-O7 阻断的标 ⚠️ |
| **联调模式**（ENT-ALGO-EVAL-INTERACTIVE 就绪后） | HTTP 调 entan `/v1/evaluation/*` | `entan_client.py` 转发企业集合+权重，entan 返回计算结果；本层只做编排+组装 |

> **切换时只改 `entan_client.py` 内部实现**，`/internal/gkx-ai/evaluation/*` 对 Java 契约不变。

### 3.5 数据预检逻辑（端点 1）

输入：`{enterprise_codes[], mode, indicators[]}`
输出：`{items: [{enterprise_code, coverage_rate, confidence_level, missing_fields[], data_status}], generatable: bool, block_reason?}`

- 覆盖率 = 已有数据字段数 / 指标所需字段数
- 可信度 = high(≥80%) / medium(≥50%) / low(<50%)
- 可生成 = 覆盖率 ≥50% 且关键指标非全缺
- 数据来源：`search_client.py` 调 gkx_search_service `/internal/gkx-search/enterprises/compare`（ES mget 企业文档）+ `/internal/gkx-search/profile/*`（画像字段）

### 3.6 服务间调用（gkx_ai_service → gkx_search_service）

评估编排需要的基础数据（企业摘要、画像字段、财务/专利历史）由 gkx_search_service 提供：
- `search_client.py` 封装 HTTP 调用 gkx_search_service 的 `/internal/gkx-search/*` 端点
- Mock 模式下 gkx_search_service 本身也返回 Mock，链路自洽
- 这是架构预设计 §8 定义的"ai-service 调 search/graph/analytics 获取基础数据"模式

---

## 4. 响应契约要点（与 Wireframe 对齐）

### 4.1 任务状态（端点 3）

```json
{
  "task_id": "EVAL-20260721-001",
  "status": "running",
  "current_stage": "indicator_calc",
  "stages": [
    {"name": "task_submit", "status": "done", "elapsed_ms": 120},
    {"name": "permission_check", "status": "done", "elapsed_ms": 80},
    {"name": "data_aggregation", "status": "done", "elapsed_ms": 320},
    {"name": "indicator_calc", "status": "running", "elapsed_ms": 1800},
    {"name": "confidence_check", "status": "pending"},
    {"name": "result_assembly", "status": "pending"}
  ],
  "elapsed_ms": 2320
}
```

> 不伪造百分比；只展示当前阶段、已完成阶段和已用时间（Wireframe §2.4）。

### 4.2 评估结果（端点 4，按模式适配）

- **KPI 卡**：≤4 个模式关键指标（技术力=综合得分/排名/专利/研发投入；商业力=得分/营收/增长率/利润率；综合=得分/排名/短板数/创新指数）
- **雷达**：技术力双企雷达（维度轴由后端返回，未登记标 DEMO）；商业力不用雷达；综合竞争力单企/双企
- **排名**：全对象综合得分排序（任务快照）
- **诊断**：综合得分/原始指标/可信度/差距/优势/短板
- **可信度**：per_enterprise_confidence
- **metric_ids**：每个统计指标附 metric_id 或 GAP-METRIC-BID-*

### 4.3 血缘（D9）

结果中每个统计数字附：
```json
{"metric_id": "M_ENT_TECH_POWER_SCORE", "calc_process": {...}, "source_tables": [...], "pending_ref": "Q014", "mapping_status": "🟡"}
```

---

## 5. 禁止

- 修改 `demo-algo-ent-analysis` 仓任何文件（算法组项目）
- 把评估代码写进 `gkx_search_service/`（违反服务边界，评估归 ai-service）
- 在 gkx_ai_service 写评估算法（评分公式/排名算法/诊断规则）——这些归 entan
- 替甲方拍板 Q014 权重 / K-O7 数据源（标 🟡 + 临时默认 + ⚠️）
- 对 Java 暴露 entan 的 `/v1/*` 原始路径（必须经 gkx_ai_service 屏蔽）
- 伪造数据批次值 `mock_20260618`（Wireframe §3.5）
- 修改 `gkx_common/`（公共库共享，本任务只复用不改；如需扩展另起任务）

---

## 6. Definition of Done

1. `gkx_ai_service/` 子项目骨架齐备（main.py/deps.py/entan_client.py/search_client.py/views/），与 gkx_search_service 平级，共用 gkx_common
2. `views/evaluation.py` 7 端点三层齐全（router→逻辑→Mock/entan 策略）
3. Mock 模式全链路可跑通（创建任务→轮询状态→取结果→历史列表）
4. `entan_client.py` 占位（Mock 模式不调；联调模式 HTTP 调 entan），切换仅改内部
5. `search_client.py` 调 gkx_search_service `/internal/gkx-search/*` 取基础数据
6. 3 张表 DDL（`gkx_ai_service/sql/eval_*.sql`）；Mock 模式内存 dict 不依赖建表
7. 数据预检端点返回覆盖率/可信度/可生成性
8. 结果响应含 metric_id / calc_process / pending_ref（D9 血缘）
9. `main.py` 注册新 router；本地 `uvicorn gkx_ai_service.main:app --port 8081` 启动无报错；7 端点 curl 冒烟通过
10. `.gitlab-ci.yml` / `docker/` / `k8s/` 如需为 ai-service 独立部署配置，参照 search 服务模板补充（同一 monorepo，可共用 CI）
11. handoff：`agent-handoffs/企业战略分析-ENT/ENT-PY-EVAL-TASK.md` + 架构合规自检 7 条 + cost 四字段
12. API 契约文档更新（`docs/API-接口文档.md` 追加评估章节，prefix `/internal/gkx-ai/evaluation/*`）

---

## 7. Convoy 风险

| 风险 | 缓解 |
|---|---|
| 新建子项目，与 gkx_search_service 共用 gkx_common | 只读引用 gkx_common，不改其代码 |
| .gitlab-ci.yml / docker 可能需为 ai-service 加部署目标 | 参照 search 服务现有配置，加 ai-service 的 build/deploy stage；同 monorepo |
| 与 gkx_search_service 端口冲突 | ai-service 用 8081，search 用 8080 |

---

## 8. 认领话术

```text
/goal ENT-PY-EVAL-TASK
监管：human:徐滕强
data-agent：demo-svc-topic-py 新建 gkx_ai_service 子项目（与 gkx_search_service 平级，共用 gkx_common），实现企业评估任务编排层 7 端点（/internal/gkx-ai/evaluation/*），Mock 优先，屏蔽 entan。
先读：ENT-ARCH-COMPARE-EVAL-分析.md、Wireframe-ENT-EVAL.md、企业维度-Python微服务架构预设计.md §8、gkx_search_service/main.py（骨架参考）。
铁律：评估归 ai-service 不归 search；新建 gkx_ai_service 子项目；只改 demo-svc-topic-py；不碰 demo-algo-ent-analysis；不做算法计算；Mock 优先；D9 血缘。
```
