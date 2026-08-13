# DEMO-CHAIN-PY-JOB-KEY-LINK-L01 · 产业链 Python — 样板键 chain:diagnosis:key_link

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-JOB-KEY-LINK-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §1 / §6 KEY-LINK  
> 契约：[`DESIGN-LANDING-key_link.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/DESIGN-LANDING-key_link.v0.md) · [`GRAPH-key_link.v0.md`](../产品整体定义/E2-产业链分析/CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/schemas/GRAPH-key_link.v0.md)  
> 依赖：[`DEMO-CHAIN-PY-JOB-RUNTIME-L01.md`](./DEMO-CHAIN-PY-JOB-RUNTIME-L01.md) · [`DEMO-CHAIN-PY-METRIC-L01.md`](./DEMO-CHAIN-PY-METRIC-L01.md)

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
| 说明 | 未用 YAGNI 跳过五段 Graph、诚实空、LLM 边界、handoff、pytest。未另开第二套 GRAPH_REGISTRY。未实现 BOTTLENECK/CYCLE/REGIONAL/SHENZHEN/PANORAMA/Nebula。厨房 SEARCH/SYNC/RUNTIME 骨架未改行为。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 DESIGN-LANDING / GRAPH / schema / Demo 页禁止 compress 代替精读；本单未对必读做 headroom compress。 |

## 范围与实现

把 RUNTIME 的 `GRAPH_STUB_PENDING_KEY_LINK` **替换**为 `key_link.graph.v1` 五段真节点。仍走现有 `GRAPH_REGISTRY` + `execute_chain_job`；菜谱在 `lumen_common.algorithms.chain.key_link`。

| 段 | stage_code | 本单 |
|---|---|---|
| N1 | `freeze` | 校验 `object.type/object_type=industry_chain`、三因子 `user_confirmed`+`ready`；不查 ADS、不算分、不调 LLM |
| N2 | `structure` | **完整五环节** rd/design/manufacturing/sales/service；Demo DWD 能映射则填边界/企业数，否则目录默认文案 + 字段诚实空；禁止只返回关键节点 |
| N3 | `score_high_end` | 确定性加权（0.34/0.33/0.33）；缺因子 → `status=missing`；有值 → `status=mock` + `gap_ref=GAP-CHAIN-DIAG-METRICS`；**不用** Q056/QC07 |
| N4 | `annotate` | **规则** QC02 Top20% 企业数标 `is_key_node`；LLM **只叙述**；无密钥/URL 则跳过叙述，规则仍跑 |
| N5 | `validate_assemble` | `result_payload` 对齐 `chain.key_link.result_payload.v1`；不自签 `result_snapshot_id` |

**复用（禁止第二套注册表）**

```python
from lumen_common.algorithms.chain.job_runtime import GRAPH_REGISTRY, execute_chain_job
from lumen_common.algorithms.chain.key_link import node_freeze, node_structure, node_score_high_end, node_annotate, node_validate_assemble
```

硬约束落地：

- LLM 输出即使带 `is_key_node` / 分数字段也不写回骨架
- Complete 成功只交 `result_payload`；厨房仍剥离 `result_snapshot_id`
- 不写 `industry_chain_graph_snapshot`
- Execute 入口仍 `assert_demo_mysql_targets`
- 结构歧义（DWD 有节点但映不上五环节）记 `GAP-CHAIN-DIAG-STAGE-MAP` + `STRUCT_AMBIGUITY_ESCALATE:human:李伟`，其余诚实降级继续；**未**新建表、**未**改主键

### result_payload 要点（成功路径）

- `sections.chain_structure.stages` 长度 5，stage_key 固定集合
- `summary.key_node_count.value === count(is_key_node)`
- 每个关键环节有 `annotations`（`enterprise_count_top_pct` / `temp.qc02.top20.v1`）
- 无 LLM：`competition`/`tech_trends` 空 + `degraded=true` + `honesty.degrade_reasons=["llm_unavailable"]`
- 高端化缺因子：`high_end_index.status=missing`、`value=null`、`display=—`

## 偏离

| 项 | 说明 |
|---|---|
| 五环节 vs DWD 上中下游 | DWD `stage_code` 是 upstream/mid/down，不是诊断五码。不新建映射表；按 `node_type/node_name` 能认则认，否则目录骨架 + gap。升级点记给 `human:李伟`，本单不 blocked 整任务 |
| 公式未闭合 | 有因子值也只出 `mock`+`GAP-CHAIN-DIAG-METRICS`，不标 `ok` |
| QC02 | 临时 Top20% 企业数；无企业数则 0 个关键（诚实），不抄 Demo 页 设计/制造 假分 |
| Execute 仍同步跑完再 202 | 与 RUNTIME 厨房一致；未改 BackgroundTasks |
| 无 jsonschema 依赖 | 不变量用 Python 断言；未新增 pip 包 |

## 产物清单

- 代码：`lumen-algo-py` `bba8220a3eabd5aa21d9678e8074d0d0be099344`（`origin/dev`）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC 语义；未写 ADS graph_snapshot；未做其它诊断键

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**168 passed**, 1 warning in 2.32s（Starlette TestClient deprecation，与本单无关；RUNTIME 时 161 绿）
- 成功路径：五环节 + 规则关键标记（制造）
- LLM 关闭：仍有 QC02 关键；格局/趋势诚实降级
- 故意缺数据：五环节骨架、分数 missing、关键数 0
- 错误对象：Complete(`failed`) `INPUT_OBJECT_INVALID` / `failed_stage_code=freeze`
- 厨房仍禁止 `result_snapshot_id`；stub 文案 `GRAPH_STUB_PENDING_KEY_LINK` 已移除

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| QC02 / GAP-CHAIN-DIAG-METRICS | 口径未甲方确认；UI 须带 🟡 |
| 五环节映射表 | 若要正式 `gkx_cfg` 枚举，升级 `human:李伟` 后再建，禁止本单改 DWD PK |
| 真 LLM | 需 `LUMEN_ALGO_CHAIN_LLM_API_KEY` + `LUMEN_ALGO_CHAIN_LLM_URL`；默认跳过 |
| BOTTLENECK 等六键 | 可复用 `node_freeze` 等函数；本单未实现 |
| 段 C Java | Snapshot 签发 / wait_view / Complete schema 门禁 |

## CI/CD

- 分支：`lumen-algo-py` `dev` → `origin/dev`（禁止 force / 禁止 main）
- commit：`bba8220a3eabd5aa21d9678e8074d0d0be099344`
- pipeline：push 后由 GitLab `py:test` 接管
- K8s rollout：本会话未等镜像；Execute 路径仍挂在原 API
- 本地：pytest 168 绿

## 可观测性

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py`
- `trace_id`：Execute body 或 `current_trace_id()` 写入 Stage/Complete
- 未第二套中间件

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 仅 lumen-algo-py |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 只经已有 Execute；回调 Java；无前端直连 |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；本单不做投影 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev` `bba8220a3eabd5aa21d9678e8074d0d0be099344` |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 只读 demo_*；不写 graph_snapshot |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 + honesty/gap | ✅ `M_CHAIN_KEY_NODE_COUNT` + QC02/METRICS gap；禁止假市场/投融资分 |

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/key_link.py`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_job_runtime.py`
- `repos/lumen-algo-py/tests/test_chain_key_link.py`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 205000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.23 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`205000 × (0.75×3 + 0.25×15) / 1e6 = 1.23`。

## 联调确认

**联调通过 / 联调确认**：pytest 168 绿；五段 ReportStage 实跑；LLM 无密钥时跳过叙述但规则关键仍在；`result_payload` 含完整五环节；Complete 无自造 `result_snapshot_id`；缺数据诚实空；错误对象 Complete(failed)；SEARCH/SYNC 路由仍在。本 agent **不**把任务标 `done`（feature → `integration`）。
