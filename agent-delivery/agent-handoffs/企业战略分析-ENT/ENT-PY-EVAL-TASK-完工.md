# ENT-PY-EVAL-TASK — 完工 handoff

- **任务 ID**：ENT-PY-EVAL-TASK
- **角色**：data-agent
- **监管**：human:徐滕强
- **状态**：开发完成（Mock 优先），待 Java 联调 + entan 算法就位后切真实
- **完工时间**：2026-07-21

## 1. 范围与实现

在 `demo-svc-topic-py` monorepo 内新建 `gkx_ai_service/` 子项目（与 `gkx_search_service/` 平级，共用 `gkx_common`），实现企业评估任务编排层，屏蔽 `entan` 算法服务。

### 产物清单

| 文件 | 作用 |
|---|---|
| `gkx_ai_service/__init__.py` | 子项目包标识 |
| `gkx_ai_service/main.py` | FastAPI 入口（端口 8081，路由前缀 `/internal/gkx-ai/**`） |
| `gkx_ai_service/deps.py` | 配置扩展（entan/search base_url、eval_max_enterprises） |
| `gkx_ai_service/entan_client.py` | entan 算法客户端（Mock 优先 + 联调占位 + 失败降级） |
| `gkx_ai_service/search_client.py` | gkx_search_service 客户端（by-codes 取基础数据） |
| `gkx_ai_service/views/__init__.py` | 视图包 |
| `gkx_ai_service/views/evaluation.py` | 7 端点核心实现 |
| `gkx_ai_service/sql/evaluation.sql` | 3 张表 DDL（eval_template/eval_task/eval_task_result） |

### API 端点（7 个，统一 POST + JSON Body）

| # | 路径 | 作用 |
|---|---|---|
| 1 | `POST /internal/gkx-ai/evaluation/precheck` | 数据预检（调 search 确认企业存在 + 数量上限） |
| 2 | `POST /internal/gkx-ai/evaluation/tasks` | 创建评估任务（异步执行，立即返回 task_id） |
| 3 | `POST /internal/gkx-ai/evaluation/tasks/{task_id}/status` | 查任务状态（pending/running/success/failed + progress） |
| 4 | `POST /internal/gkx-ai/evaluation/tasks/{task_id}/result` | 查评估结果（评分 + 排名 + 4 维度 + 权重） |
| 5 | `POST /internal/gkx-ai/evaluation/tasks/history` | 历史任务列表（分页 + 状态过滤） |
| 6 | `POST /internal/gkx-ai/evaluation/templates` | 评估模板列表（预置 2 个：创新驱动型/综合均衡型） |
| 7 | `POST /internal/gkx-ai/evaluation/templates/create` | 创建评估模板 |

### 评估维度（对齐 UI Wireframe）

`innovation`（创新能力）/ `operation`（经营能力）/ `growth`（成长性）/ `risk`（风险水平）

### 任务执行流

```
create_task → 立即返回 task_id(pending)
            → 后台 _run_evaluation:
               1. fetch_by_codes (search) 预检 → missing 则 failed
               2. 权重合并（template_id 默认 + 显式 weights 覆盖）
               3. entan_evaluate 评分（Mock 或 HTTP /v1/score）
               4. 落 result → success
```

## 2. Mock 优先策略

- `entan_client`：Mock 模式返回确定性评分（基于 md5 种子，50-100 分），不实际 HTTP 调用；联调模式 POST `{entan_base_url}/v1/score`，失败自动降级 Mock
- `search_client`：Mock 模式从 `gkx_common.mock.MockDataStore` 取企业；联调模式调 `/internal/gkx-search/enterprises/by-codes`，失败降级 Mock
- 任务/模板存储：当前用进程内 dict（`_tasks`/`_templates`），DDL 已就绪，后续接 PG 时替换

## 3. 偏离说明

| 项 | 派单包约定 | 实际实现 | 原因 |
|---|---|---|---|
| 请求体模型 | pydantic BaseModel | dict + Body | 环境为 pydantic v1.8.2，`X \| None` 语法不支持；与 `gkx_search_service` 风格保持一致 |
| 任务持久化 | PG 表 | 进程内 dict | Mock 阶段先跑通链路，DDL 已备好待接 PG |
| 端点数 | 7 | 7 | 一致 |

## 4. 验收证据

### 冒烟测试（2026-07-21，Mock 模式）

```
启动：GKX_MOCK_ENABLED=true uvicorn gkx_ai_service.main:app --port 8081 → startup complete

0. GET /healthz → {"status":"ok","service":"gkx-ai-service","mock_enabled":true}
1. precheck (3 真实 org_id) → ready=true, found=3, missing=[]
2. create task (template_id=TPL-BALANCED) → task_id=EVAL-dcc4b5a2bd1d
3. status (2s 后) → status=success, progress=100
4. result → 3 家企业评分排名（rank1=73.91 / rank2=68.63 / rank3=62.46，4 维度 + 权重 + data_source=mock）
5. history → total=1, 含冒烟任务
6. templates → 2 个预置模板
7. create template (风险规避型) → TPL-e6bff562，templates total=3
```

7 端点全部 200 + code=0，评分排名逻辑正确。

## 5. 架构合规自检（§2 十条）

1. ✅ 算法只在 Python：entan_client 用 Python 调算法 / Mock 评分
2. ✅ 调用链：前端 → Java REST → Python `/internal/gkx-ai/*`（本服务即 Python 层）
3. ✅ 图谱：本任务不涉及 NebulaGraph
4. ✅ 可观测性：复用 gkx_common.observability（JSON 日志 + TraceHeaderMiddleware）
5. ✅ CI/CD：代码在 demo-svc-topic-py（POC 阶段 main 直推），后续接 CI
6. ✅ demo2 只读 merge：本服务在 demo 仓，不涉及 lumen merge
7. ✅ 共享聚合核心：本服务是 Python 微服务，供 Java gkxlumen-topic Feign 调用
8. ✅ 数据策略：Mock 数据先行，DDL 待 PG 落地
9. ✅ 前端规范：本任务不涉及前端
10. ✅ 数据血缘：评分结果含 `data_source`（mock/entan）+ `model_version`，后续接 PG 后补 metric_id 8 件套

## 6. 后续 TODO（非本任务范围）

- [ ] 接 PG：用 `sql/evaluation.sql` 建表，`_tasks`/`_templates` 替换为 PG 查询
- [ ] entan 联调：`ENT-ALGO-EVAL-INTERACTIVE` 完成后，切 `GKX_MOCK_ENABLED=false` 联调 `/v1/score`
- [ ] Java 对接：api-agent 在 gkxlumen-topic 建 Feign Client 调 `/internal/gkx-ai/evaluation/**`
- [ ] 配置：`conf/settings.yaml` 增加 `ai_service` 段（entan/search base_url）

## 7. cost 回填

- actual_tokens: ~（本会话内，未单独计量）
- model_used: zs-glm-5.2
- actual_cost: <$5
- cost_warn: N

## 8. v3.0 范围变更附录（2026-07-24）

后续正式验收以修订后的 `ENT-PY-EVAL-TASK-派单包.md` 与 `API-ENT-EVAL-contract.md` v3 为准。本 handoff 记录的 2026-07-21 Mock 7 端点成果保留为阶段性证据，但以下要求已作废：

1. Python 作为正式任务编排真源
2. Python `/templates` 模板管理
3. Python 生产任务三表（含 PostgreSQL）
4. 对前端形成独立 tasks/history 真源

收口后 Python 仅保留 8 个评估适配端点；通用回调由 `ENT-PY-ANALYSIS-CALLBACK` 承接；Java `analysis_task` 为唯一任务真源。

## 9. 2026-08-21 正式门面 INT

`EVAL-20260821-001` 在 `50199` 建单成功（`analysis_fp` 64 位 SHA-256），随即 `failed`：`DWD enterprise_base 未找到企业`（检索 ES org，算法 DWD 没有）。现网 `lumen-topic-py` `mock_enabled=False`，2026-07 Mock 冒烟不能当正式证据。不进入下一步。

记录：`qa/test-records/KJZTFWXT/R0/INT-分析任务中心联调-记录-20260821.md`
