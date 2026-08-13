# DEMO-CHAIN-PY-REPORT-L01 · 产业链 Python — 分析报告只读 Result 导出 MinIO

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-REPORT-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §6 REPORT  
> 契约：[`系统设计说明书-Analysis-Job-Runtime.v0.md`](../产品整体定义/E2-产业链分析/系统设计说明书-Analysis-Job-Runtime.v0.md)（报告 Job 只读 Result，不重跑 Graph）· [`DEMO-CHAIN-JAVA-C-总派单.md`](./DEMO-CHAIN-JAVA-C-总派单.md)（Java 已挡 `rerun_analysis`）  
> 依赖：[`DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md`](./DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md)

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock | 24h（coordinator 开工写入） |
| 说明 | 已 claimed + in_progress 后本会话落地；feature 完工进 `integration`，不标 done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过「禁止重跑」、handoff、pytest。未改七键 Graph 节点、未改 Java、未做 NER、未上排版引擎。报告路径不调 metric_engine、不 Execute 七键/全景分析菜谱、不写 ADS 业务表。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 Runtime 报告章节禁止 compress 代替精读；本单对 Runtime.v0（含 §2.4 非目标 / §5.1 报告服务 / §5.3 例 8 只读 Result）、PY-B §6 REPORT、JAVA-C 挡重跑 均精读，未 compress。 |

## 范围与实现

只读已有 Result Snapshot / `result_payload` 生成最小报告字节（JSON 或 HTML），写入 **Demo 桶** 对象存储；对象键含 `task_id` + `result_snapshot_id`。

| 入口 | 行为 |
|---|---|
| `POST /internal/v1/chain/reports/export` | 主路径：只读导出，返回 uri/size/content_type |
| 厨房 `chain:report:export` → `report.export.v1` | 两节点 `freeze` / `render_export`；**禁止**挂七键/全景分析 Graph |
| Execute 入参 `rerun_analysis` / `source_report_task_id` / `rerun_from_report` | `REPORT_RERUN_FORBIDDEN`（与 Java 同文案语义） |
| 报告任务带 `graph_version=key_link.graph.v1` 等分析图 | 同样拒绝，避免借报告重跑分析 |

对象键：`chain/{task_id}/{result_snapshot_id}/report.{json\|html}`  
默认桶：`demo-gkx-analysis-results`（非 `demo-`/`demo_` 前缀直接拒绝）。

### 禁止（已测）

- 报告任务内 Execute 七键 / 全景分析节点
- 调 `run_metric_engine` 重算
- `connect_chain_write` / `INSERT` ADS/DWD 业务表
- 用对象元数据替代业务表（响应标明 `persisted_to=object_store_only`）
- 自签 `result_snapshot_id`

Demo MySQL 闸门仍拒绝非 `demo_`。

## 偏离

| 项 | 说明 |
|---|---|
| MinIO 实写 | **本机/pytest 走 mock store**（`chain.minio.use_mock: true`，endpoint 空）。现网 Endpoint 未填（`platform/minio.md` OPEN）；**未假写入正式桶** `gkx-analysis-results` |
| 无新 pip 包 | 未加 minio/boto3；HttpMinioStore 用已装 `httpx` + stdlib HMAC SigV4，仅当 endpoint 配齐且桶为 demo-* |
| 报告形态 | 结构化 JSON / 最小 HTML，无 PDF 排版引擎 |
| Execute 仍同步 202 | 与 RUNTIME 厨房一致；报告厨房两节点同样同步跑完再 202 |
| Java 白名单 | 段 C 尚未注册 `chain:report:export`；联调可先打 `/reports/export`，厨房路径已就绪 |

## 产物清单

- 代码：`lumen-algo-py` `dcf67273cde0dd7fb5c22eba010dab2bb34e10c8`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / 七键菜谱节点函数 / NER

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**243 passed**, 1 skipped, 1 warning（Starlette TestClient deprecation，与本单无关；SHENZHEN 时 225 绿）
- 只读 payload 能出 JSON/HTML 字节；对象键含 `task_id`/`result_snapshot_id`
- `rerun_analysis` / `source_report_task_id` / `rerun_from_report` → `REPORT_RERUN_FORBIDDEN`；Execute 七键带 rerun 在跑图前拒绝（无 Stage 回调）
- 报告导出 monkeypatch 七键 freeze / `run_metric_engine` / panorama publish 均未触发
- 报告厨房带 `key_link.graph.v1` 被拒
- MinIO/store PUT 失败 → HTTP 502 `OBJECT_STORE_FAILED`，`status=failed`，不假成功
- 正式桶名拒绝；非 `demo_` MySQL 422

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| 现网 MinIO | Endpoint/凭证仍 OPEN；配 `LUMEN_ALGO_CHAIN_MINIO_ENDPOINT` + demo 桶后才实写 |
| Java Feign | 报告 Create 需段 C 增 `chain:report:export` 或 Feign `/reports/export` |
| 前端阅读器 | D WORKSPACE 弱壳；本单不做 |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py；不重跑分析算法 |
| 2 | 前端 → Java → Python `/internal/*` | ✅ `/internal/v1/chain/reports/export`；无前端直连 |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 未引入 Neo4j；报告不投影图 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev`（见下） |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 闸门 demo_*；对象元数据不落业务表 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 | ✅ 不改指标、不改绿；只读既有 Result honesty |

## CI/CD

- 分支：`lumen-algo-py` `dev`（禁止 main、禁止 force）
- commit：`dcf67273cde0dd7fb5c22eba010dab2bb34e10c8`（`feat(chain): export read-only analysis reports to demo object store [agent:algorithm-agent]`）
- pipeline：push `origin/dev` 触发 `py:test`
- 部署：ns=`dev`；镜像 `lumen-platform-algo-py`
- 本机 pytest：243 passed

## 可观测性

- `OTEL_SERVICE_NAME`：沿用 `lumen-platform-algo-py`
- 响应带 `trace_id`

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/report_export.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`（仅增报告菜谱绑定 + 重跑拒绝；**未改七键节点函数**）
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/conf/settings.yaml`（`chain.minio`）
- `repos/lumen-algo-py/tests/test_chain_report.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 175000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.05 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`175000 × (0.75×3 + 0.25×15) / 1e6 = 1.05`。

## 联调确认

**联调通过 / 联调确认**：pytest 243 绿；只读 Result 出字节；rerun 拒绝；不调用 Execute 七键；MinIO 失败诚实 failed；mock 对象键 `chain/{task_id}/{result_snapshot_id}/report.json`。本 agent **不**把任务标 `done`（feature → `integration`）。
