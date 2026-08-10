# ARCH-ENT-PY-LUMEN-ALGO-ADAPT-L01 Handoff

- 时间：2026-08-06
- 状态：本地实现与专项验证完成；待人工 review、commit/push、CI/K8s 联调
- 执行：agent:algorithm-agent
- 监管：human:徐滕强
- 仓：`repos/demo-svc-topic-py`

## 1. 范围与实现

本任务不新增招标功能点，只调整企业评估、风险洞察、引育推荐的内部算法调用架构：

- Java → Python 的 `/internal/gkx-ai/**` 路径、方法和响应包络保持不变。
- Python → 算法统一收敛至 `lumen-algo-py`：
  - `POST /gdf/tasks/create-and-start`
  - `GET /gdf/tasks/{task_id}`
  - `GET /gdf/tasks/{task_id}/result`
  - `POST /gdf/tasks/{task_id}/cancel`
  - `POST /v1/evaluation/precheck`
- 配置收敛为 `GKX_ALGO_BASE_URL=http://lumen-platform-algo-py:8000`，删除 entan/science 双基址。
- 算法 HTTP 200 但 `code != 0` 统一按业务失败处理。
- 创建任务同步等待算法受理结果；重复 `task_id` 直接向 Java 返回算法的“task_id 已存在”，不再由 Python 内存软幂等。
- status/result/cancel 直接查询算法任务 API；Python `_tasks` 仅保留 history/展示元信息，不再作为正式状态或结果真源。
- status 轮询不抢先向 Java 暴露算法 `success`：算法完成后仍返回 `running`，由 callback 在 MQ/MinIO 结果指针就绪后推进 Java 成功终态，避免“success 但无 resultUrl”。
- 风险/引育 `params` 展平到算法请求顶层。
- 预检内部转发算法，并严格映射回既有 Java 契约：`coverage_rate` 保持 0–1、`critical_missing` 保持整数，覆盖率低于 50% 时 `ready=false`。
- industries/indicators 保持 Python 本地注册表。
- compare 保持 Python 本地计算，但输入改为算法 `/result`；兼容 `scores` 及当前综合竞争力 `dimension_rows`。

## 2. 产物清单

- `gkx_ai_service/algo_client.py`
- `gkx_ai_service/deps.py`
- `gkx_ai_service/entan_client.py`
- `gkx_ai_service/science_client.py`
- `gkx_ai_service/views/evaluation.py`
- `gkx_ai_service/views/risk.py`
- `gkx_ai_service/views/recommend.py`
- `gkx_ai_service/views/callback.py`
- `gkx_ai_service/main.py`
- `conf/settings.yaml`
- `k8s/dev-ai-py.yaml`
- `tests/test_lumen_algo_adaptation.py`
- `tests/test_no_mock_runtime.py`
- `tests/test_eval_callback_defaults.py`

## 3. 偏离与开放项

- 未改 Java、前端、lumen-algo-py，符合任务边界。
- 未执行 commit/push、CI、K8s rollout；需人工 review 后继续。
- 全量测试结果为 `111 passed, 2 skipped, 28 failed`。28 个失败全部位于未修改的 `tests/test_dwd_v3_compatibility.py`，原因是其尝试 monkeypatch 已不存在的 `enterprise_risk.query`；与本次算法适配无调用关系。
- 当前异步算法结果只有综合竞争力 `dimension_rows` 可还原旧四维 compare 输入；technology/business 若需同一 `dimension_diff` 语义，后续需补充明确的维度映射契约，不能在 Python 侧臆造业务口径。

## 4. 验收证据

- 专项回归：
  - 命令：`.venv/bin/pytest -q tests/test_lumen_algo_adaptation.py tests/test_no_mock_runtime.py tests/test_eval_callback_defaults.py tests/test_analysis_callback.py`
  - 结果：`39 passed, 1 warning`
- 编译：`.venv/bin/python -m compileall -q gkx_ai_service` 通过。
- 补丁检查：`git diff --check` 通过。
- warning：FastAPI TestClient 的 Starlette/httpx2 弃用提示，不影响本次行为。

## 5. 架构合规自检

1. 算法只在 Python：✅
2. 前端 → Java → Python → 算法，Java 不越层：✅
3. 图谱仍为 NebulaGraph，本任务未改图谱：✅
4. 保留 `gkx_common.observability` 日志链路：✅
5. CI/CD：⏳ 待 commit/push 后验证
6. demo/lumen 只读 merge 边界：✅ 未做 merge
7. 共享聚合核心与 Java REST 边界：✅
8. ADS 标准表策略：✅ 预检/计算由 lumen-algo 读取 ADS/DWD
9. D8 前端规范：N/A，无前端改动
10. D9 数据血缘：✅ 不改指标注册表与结果血缘字段

## 6. Cost

- `actual_tokens`：待会话结束后由 registry 工具回填
- `model_used`：Auto
- `actual_cost`：待平台账单回填
- `cost_warn`：green（未触发 $10 暂停线）
