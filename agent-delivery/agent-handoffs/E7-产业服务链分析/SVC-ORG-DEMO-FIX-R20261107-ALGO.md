# SVC-ORG-DEMO-FIX-R20261107-ALGO · 服务机构技术力快照展示序与版本自报修复（handoff）

- 任务：`SVC-ORG-DEMO-FIX-R20261107-ALGO`（Epic E7-产业服务链分析；agent=algorithm-agent；监管人=human:徐滕强；强度=ponytail full）
- 仓：`lumen-algo-py`（dev 直推；commit **`0084025`**，rebase 远端 a25e7ce 后推送成功）
- 验收轮真源：`agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-ORG-DEMO-ACCEPT-LOOP.md` 步③ 7.3.1/7.3.2 缺口键

## 1. 缺口 → 修法对照

| 缺口键 | 现况 | 修法 | 落点 |
|---|---|---|---|
| 1（ALGO/rank） | 快照 `result_payload.tech_power.rows` rank_no=26/50（库侧全池 300 行序，由旧 `vendor/entan-py/entan/svcmodels.py` 生成批次时写入 `ext.rank_no`） | 读面装配层按**选定集合**重排：score 降序稳定排序，顶层 `rank_no` 从 1 递增（同分并列 1/2）；库侧旧序只保留在 `ext` 不篡改 | `lumen_common/algorithms/svcan/engine.py` `fetch_models` tech 分支 |
| 2（ALGO/版本自报） | `result_payload.model_version=svc_proxy_v1.2`（模块常量硬编码），源表批次行实为 v1.3 | SELECT 增取 `t.model_version` 列；`out.model_version` 从源表批次行取值，取不到回落模块常量；`leaf_tech_power` 顶层 `model_version` 同步随源表批次行走 | 同上 tech 分支 + `lumen_common/algorithms/svcan/assembly/leaves.py` `leaf_tech_power` |

**为什么改装配层而不是生成层**：库内 `ext.rank_no` 全池序与 `model_version=v1.3` 是真值不改（禁改 `svc_tech_power_score`）；消费链 `leaf_tech_power`（analysis_task 快照）与 `/internal/v1/svcan/models/tech`（直读面）都走 `fetch_models`，一处修复两链同时生效；快照重跑（签发新任务）后自然携带新展示序。

## 2. 改动清单（diff 摘要，4 文件 +67/-2）

- `lumen_common/algorithms/svcan/engine.py`
  - tech 分支 SELECT 增 `t.model_version` 列（:583）
  - 按选定集合 score 降序稳定排序 → 顶层 `rank_no=1..N`（:593-598，含注释指向本单 ID）
  - `out["model_version"]` 取首个非空源表批次行值（:599-603）
- `lumen_common/algorithms/svcan/assembly/leaves.py`
  - `leaf_tech_power` 的 `envelope(...)` 增 `model_version=models.get("model_version") or MODEL_VERSION`（:132-133）——`envelope()` 基底原写死常量，`**extra` 覆盖后叶子顶层随源表走
- `tests/test_svcan_engine.py`：新增 `test_tech_rank_no_within_selected_set_and_model_version_from_source`（两行同分 40.0 + `ext.rank_no` 26/50 + 批次行 v1.3 的 FakeDB 桩，断言顶层 `[1,2]`、`ext` 不篡改、`model_version=v1.3≠常量`）
- `tests/test_svcan_assembly.py`：新增 `test_tech_power_rows_ranked_and_version_from_source`（叶子级：rows 顶层 rank_no=1、顶层/engine_meta model_version 一致）

## 3. 最小自检（结果全绿）

- 新增 2 条 pytest（仓内 pytest，CI 同款可跑）：
  - `tests/test_svcan_engine.py::test_tech_rank_no_within_selected_set_and_model_version_from_source` ✅
  - `tests/test_svcan_assembly.py::test_tech_power_rows_ranked_and_version_from_source` ✅
- 回归：`test_svcan_engine + test_svcan_assembly + test_svcan_narrate_tech_trend + test_mock_guard` = **70 passed**；全量 `pytest -q` = **816 passed / 7 skipped**（rebase 后 svcan 面复跑仍 70 passed）
- 消费端契约已核：lumen-ui-topic `svcCapabilityModel.ts` `rankOf` 顶层 `rank`/`rank_no` 优先、`ext.rank_no` 兜底（:184-187）；`ServiceOrgAnalysisWorkspace.vue`/`svcAnalysisWorkspace.ts`/报告层均消费 `svcCapabilityModel`，零前端改动即生效

## 4. pending_verification（重跑快照证据，本单不做）

DoD 第 6 条「重跑后 rank_no=1/2 与 model_version=v1.3 证据」**记 pending**：重跑需监管人徐滕强说「签发」新分析任务（与 QUERY 单 `SVC-ORG-DEMO-FIX-R20261107-QUERY` 同一签发口令；DATA 单修篮为其前置）。签发后第 2 轮验收从新快照 `result_payload.tech_power.rows` 取证：君智容/星诚优威 rank_no=1/2、payload `model_version=svc_proxy_v1.3`。装配层修法已保证新快照必然携带新展示序与源表版本。

## 5. 架构合规自检

| 铁律 | 自检 |
|---|---|
| D1 算法只在 Python | ✅ 改动全在 lumen-algo-py；未触碰 Java |
| D2 调用链（前端→Java→Python /internal/*） | ✅ 只改 Python 装配读面；Java 透传契约（`{tech_power:{rows}}`）未变 |
| D9 指标血缘 | ✅ 未新增 metric_id、未改口径分值（40/20 恒分保留，Q-SVCCHAIN-01+Q060 演示态声明不动） |
| D12 demo/lumen 隔离 | ✅ 未读改 demo 仓代码；vendor 参考只读 |
| D14 对象存储 | ✅ 不涉及 |
| D16/D18 缺项 | ✅ 不涉及（无 gapfill 表、无 mock 注入；读真值 + 展示序重排） |
| 可观测 | ✅ envelope/trace 链路未动；`fetch_models` 日志语义不变 |
| 禁区 | ✅ 未改 lumen-svc-platform、未改前端、未改用例期望、未动库内分值、未 push main |
| cost | 实际 tokens ≈ 100k（glm-5.3-Flash），实际成本 < $1（远低于 $10 告警线），cost_warn=green |

## 6. 交付

- commit：`0084025`（`origin/dev`，含 `[agent:algorithm-agent]` 标记；push 经 `git pull --rebase` 一次）
- 证据路径：本文件；测试可复现命令 `PYTHONPATH=. pytest tests/test_svcan_engine.py tests/test_svcan_assembly.py -q`
- token/口令：全程未接触、不入档

ponytail: full——只改读面装配两处 + 最小自检两条，无新依赖、无新抽象；`ext` 兜底保留旧序是为兼容未重跑的历史快照消费方，真源统一后可删。

## 续修 2026-11-07（监管人「继续」口令授权；签发取证 SVC-20261107-049 发现修复半生效）

### 根因（取证代理代码实读 + 本轮实读复核）

上轮 0084025 排序在 algo 装配层生效，但 `fetch_models` tech 读面无 `org_ids` 形参：industry 为空时排序对象=全池 300 行，rank_no=26/150 是全池序；「同分并列 1/2」仅在行集被过滤到 ≤2 时才成立。

### 改动（仅 lumen-algo-py，commit `c084e7c`，rebase 后推 `origin/dev` 成功）

1. `lumen_common/algorithms/svcan/engine.py` `fetch_models` tech 分支：新增 `org_ids`（可选）切片——有值时按选定机构集合过滤行集后再做集合内 score 降序稳定排序（顶层 rank_no 从 1 递增）；无值保持全池现行为。排序点与 0084025 协同（切片在排序之前，不重复排序）。
2. `lumen_common/algorithms/svcan/assembly/leaves.py` `leaf_tech_power`：`params.org_ids` 透传 tech 读面（与 org_coverage 透传模式一致）。
3. `tests/test_svcan_assembly.py`：`MultiTechDB` 多行桩 + 新增 2 用例（`org_ids=[两机构]` → rank_no=[1,2]+v1.3+集合外最高分被丢弃；无 `org_ids` → 全池序回归）。

### 测试

- svcan 域回归（assembly/engine/shortboard/sz_drill）：47 passed。
- 全量 pytest：**818 passed, 7 skipped, 1 deselected**（816 基线 + 2 新增）。deselected = `test_portal_svc_metrics.py::test_tech_rows_share_one_metric_id`（遗留挂点：全量跑必挂死该文件，单跑 10.7s 可过、断言本身绿；与本改动无关，stash 对照验证过改动前后行为一致）。
- CI pipeline [4288](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4288)（c084e7c）：`py:test` ✅ 238s、5 镜像 ✅、`deploy:api`/`deploy:worker`/`deploy:entan-api` ✅、e2e smoke ✅；`deploy:entan-worker`/`deploy:innov` 为 manual 闸门未跑（entan/innov 服务常态手动门，与本改动服务无关，未越权代点）。

### 重签发取证（SVC-20261108-002，不带 force，参数=用例 7.3.1 行）

- 旧网关 `10.50.69.111:30892` 连接超时（2 次，curl 28），改前端等价网关 `edu.itic-sci.com/tts/lumen/api` 一次成功。
- POST 创建 → `SVC-20261108-002`（reused=false，两机构参数正确）→ 轮询至 **success**。
- **取证结果：`model_version=svc_proxy_v1.3` ✅；rank_no ❌** —— `target_params.result_payload.tech_power.rows` = **300 行全池**，顶层 rank_no=1..300 连续（0084025 的重排生效），选定两机构（君智容 `004671cd…` / 星诚优威 `007d0adc…`）散布全池中，非 1/2。

### 续修后仍不对的根因（本轮代码实读，未第 3 次重试，按令报告并停）

svc 分析任务执行链不在 lumen-algo-py 直达：Java `RemoteSvcAnalysisPythonClient`（Feign name=**lumen-topic-py**）→ `lumen-topic-py/gkx_svc_service/views/task.py` `_call_svcan()`（:285-298）→ algo `/internal/v1/svcan/analysis/tech_power`。**`_call_svcan` 只对 `org_coverage` 拼 `org_ids` 查询参数；`tech_power` 发裸 GET，org_ids 在 topic-py 被截断**，algo 侧 leaf 收到空 params → 走全池分支。algo GET handler 本身已支持 org_ids（`svcan_analysis_get` :90-99）。**修复落点 = `lumen-topic-py` `_call_svcan` 给 tech_power（建议连同泛化到全部叶子）透传 org_ids**——超出本单「仅 lumen-algo-py」授权范围，未动，等监管人指派。

### cost

tokens ≈ 180k（glm-5.3-Flash），实际成本 < $2，cost_warn=green。token/口令全程未读取内容、未打印、未入档。
