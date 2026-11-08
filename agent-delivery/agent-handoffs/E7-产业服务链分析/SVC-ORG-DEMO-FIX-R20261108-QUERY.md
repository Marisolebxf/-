# SVC-ORG-DEMO-FIX-R20261108-QUERY · 技术力快照 org_ids 透传修复（handoff）

- 任务：`SVC-ORG-DEMO-FIX-R20261108-QUERY`（Epic E7-产业服务链分析；agent=algorithm-agent；监管人=human:徐滕强；强度=ponytail full；task_type=bugfix）
- 诊断真源：`SVC-ORG-DEMO-ACCEPT-LOOP.md` 第 2 轮（2026-11-08，缺口键 `analysis_task.svc:analysis:tech_power.result_payload.tech_power.rows.rank_no`，两轮停交监管人后派本单）
- ponytail: full —— 一行级条件修复 + 1 个单测，无新增抽象/依赖/文件；评分、榜行装配、受理链路其余部分零改动

## 范围与实现

真因：`lumen-topic-py/gkx_svc_service/views/task.py::_call_svcan` 的 org_ids 拼接条件只认 `leaf == "org_coverage"`，tech_power 分支不存在 → 前端冻结进 targetParams 的 org_ids 到 Python 受理层被静默丢弃，algo 侧 `c084e7c`（org_ids 切片，已上线）收不到参数回退全池 300 行排序，rank_no=126/150 而非选定集合 1/2。

修复（commit `aa5a612`，origin/dev）：

```python
# gkx_svc_service/views/task.py::_call_svcan
if leaf in ("org_coverage", "tech_power") and isinstance(params, dict):   # 原: leaf == "org_coverage"
    ...
if leaf in ("org_coverage", "tech_power") and ids:                        # 原: leaf == "org_coverage"
    url = f"{url}?org_ids={quote(ids, safe=',')}"
```

- 其他 leaf（org_trend / shortboard / graph / shenzhen / attract / cultivate）零改动
- 产业参数（industry）对 tech_power 仍不下推（保持 2026-11-02 需求回归 `2cc3d4e` 口径，既有单测断言未动）
- 不改 lumen-algo-py / Java 门面 / 前端 / 用例期望；未新增 metric_id

## 自检证据

- 新增 `tests/test_gkx_svc_task.py::test_tech_power_pushes_org_ids_to_algo`：tech_power + org_ids 参数 → 断言转发 URL 带 `?org_ids=004671cd…,007d0adc…` 且不含 industry（单跑 PASSED）
- 邻域回归：`pytest tests/test_gkx_svc_task.py tests/test_analysis_tasks.py tests/test_analysis_callback.py tests/test_rank_no_ext.py tests/test_tech_rank_determinism.py tests/test_eval_callback_defaults.py -q` → **45 passed, 1 skipped**
- CI `py:smoke` job success

## CI / 部署证据

- Pipeline：[#4290](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/4290)（sha `aa5a612`，dev，2026-11-08 10:42）→ **success**，全 9 job 绿：`py:smoke` + 4 镜像打包（search/ai/worker/show）+ 4 个 deploy（`deploy:search-py` / `deploy:ai-py` / `deploy:ai-worker` / `deploy:show-py`）全部 success（本仓发布门即此 4 部署单元，`gkx_svc_service` 由其承载）

## 线上快验（deploy 绿后，用例 7.3.1 请求体，不带 force）

- `POST /tts/svcz/api/topicAsync/topic/v1/analysis/tasks`（analysisType=`svc:analysis:tech_power`，君智容 `004671cd…` + 星诚优威 `007d0adc…`，`cap_w="25,25,20,20,10"`）→ HTTP 200、`reused=false` 新建 **`SVC-20261108-003`**，09 秒转 `success`（`total_cost_ms=5991`，4 节点走满）

| 取证项 | 期望 | 实测 | 判定 |
|---|---|---|---|
| `tech_power.rows` 行集 | 按选定集合切片 | **2 行**（修复前两轮均 300 行全池） | ✅ |
| rank_no（君智容 / 星诚优威） | 选定集合内并列 1 / 2 | **1 / 2**（修复前 126/150） | ✅ |
| score / dimension_scores / weights | 40.0 / 0-1 型 / 五维各 20 | 同 | ✅ |
| model_version（顶层 + engine_meta + 行级） | `svc_proxy_v1.3` | 全部 `svc_proxy_v1.3` | ✅ |
| calc_batch_id | `svcmodels_20261107_155402` | 行级同值（与第 1 轮库侧实查一致，无重灌） | ✅ |
| yellow_gaps / pending_client_confirm | `["Q060"]` / 1 | 同 | ✅ |
| 机构名 | 君智容物联 / 星诚优威智能 | `name_cn` 逐字一致 | ✅ |

- 取证字段路径：result 端点任务壳（`resultData=null`）→ `targetParams.result_payload`（驼峰键；LOOP 第 2 轮同型）——与第 2 轮 `SVC-20261108-001` 同 fp 跨任务新建（`reused=false`），旧快照未复用，无需 force
- 脱敏：token 全程未打印、未入档；临时响应文件（/tmp/svc_*.json）已清理

## 架构合规自检（公约 §2 铁律逐条）

| 铁律 | 判定 | 说明 |
|---|---|---|
| D1 算法只在 Python | ✅ | 改的是 lumen-topic-py Python 受理层，Java 零改动 |
| D2 调用链 前端→Java→Python `/internal/*` | ✅ | 只修 Python 层内参数转发，未越层 |
| D3 图谱 NebulaGraph | ✅ | 不涉及图谱 |
| D4 可观测性 | ✅ | 埋点零改动；载荷 trace_id 链路在 |
| D5 CI/CD push→Pipeline 绿→K8s dev | ✅ | pipeline 4290 全绿，4 deploy success |
| D6 demo2 只读 merge 铁律 | ✅ | 未碰 demo-* 仓 |
| D7 共享聚合核心 / 前端只调 Java | ✅ | 前端、Java 门面零改动 |
| D8 数据策略 ADS 先行 | ✅ | 读 `demo_gkxlumenx_ads.svc_tech_power_score`，无 mock 写 |
| D9 数据血缘 8 件套 | ✅ | 未新增 metric_id、未改口径 |
| D12 demo/lumen 隔离 | ✅ | 仅 lumen-topic-py，无 demo 下游调用 |
| D14 对象存储桶 | ✅ | 不涉及 |
| D16/D17/D18 | ✅ | 不涉及 gapfill / 锁定算法闭包 / 写死 mock（真参真算） |

## 偏离说明

无。派单范围逐条执行；「deploy:api/worker success」按本仓现行发布门对应 `deploy:ai-py` / `deploy:ai-worker`（deploy:api 为派单笔误，实际 job 名 ai-py，见 pipeline 4290 job 清单）。

## cost

- actual_tokens ≈ 70,000
- model_used = `glm-5.3-Flash`
- actual_cost ≈ $0.35
- cost_warn = `green`

## 开放项

- LOOP 第 3 轮复验 7.3.1 / 7.3.2 时直接读 `SVC-20261108-003` 快照即可闭合（rank_no 1/2 已证）；qa-agent 可复核本 handoff 取证。
- `svc_compare_basket_item` guest 4 行库侧复核仍欠（第 2 轮 database MCP 受阻顺延项，属 DATA 单范围，不在本单）。
