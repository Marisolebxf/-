# LUMEN-POLICY-C-TASK-L01 · analysis/tasks 政策 Job + 签发 snapshot

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-JAVA-C-总派单.md`](./LUMEN-POLICY-JAVA-C-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1  
> 前序：[`LUMEN-POLICY-PY-HARNESS-L01.md`](./LUMEN-POLICY-PY-HARNESS-L01.md) · [`LUMEN-POLICY-PY-JOB-L01.md`](./LUMEN-POLICY-PY-JOB-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；Job 真源在 async-service，不复制第二套任务中心；C-PORTAL 本叶不做 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照产业链/SVC Adapter：同一 `AnalysisAdapterRegistry` + 已有 `POST/GET /topic/v1/analysis/tasks`；只加政策白名单与 Feign execute；复用指纹门与 Java 签发 snapshot；未新建任务表/队列/helm |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Adapter + 单测，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | §2.2 补分析 Job 实线：`gkxlumen-topic-async-service` `POST/GET /topic/v1/analysis/tasks` → Feign `POST /internal/policy/jobs/execute`（只调 harness.dispatch）→ Java 签发 `result_snapshot_id`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- **对外**：已有 `POST/GET /topic/v1/analysis/tasks` + `GET .../result`（网关 `/topicAsync` StripPrefix=1）。政策 types 进同一任务中心。
- **task_type / sub_type**：`policy_timeseries` / `policy_regional` / `policy_shenzhen` / `policy_focus`；别名 `timeseries` / `regional` / `focus` / `policy:*`。裸键 `shenzhen` 归 SVC，政策用 `policy_shenzhen`。不注册 worker 内部 `policy_shard`。
- **Feign**：`lumen-algo-py` `POST /internal/policy/jobs/execute`（url 默认 `http://lumen-platform-algo-py:8000`，与产业链 Job 同基址）。万级仍走 Python 已有 `/gdf/tasks` worker，同一套 `dispatch`。
- **Snapshot**：Python 不自签；Adapter 剥离 `result_snapshot_id`；成功后 Java 写 `res-{taskId}`。
- **挂接 VID**：仅 `chain:` / `segment:`（例 `chain:INB170101`）；拒绝 `INB1303` / 中文名。时序/区域/深圳要求 1 产业 XOR ≥1 技术领域。禁止一次 items 4 万+。
- **禁止**：Feign `demo-*`；Java nGQL/NLP；直调 `eval.*.run()`；暴露 hang；C-PORTAL。

## I2-12 / 附录 E

| 条 | Java 实现 | 前端（D 叶） |
|----|-----------|--------------|
| E0-1 切条件不自动 create | 仅 `POST /topic/v1/analysis/tasks` 落库；GET list/detail 无副作用 | 条件栏「开始分析」才 POST；本叶 N/A |
| E0-3 同用户同条件单飞 | `analysis_fp`（64 位 SHA-256）+ Redis 创建锁；已有 `running` 复用 | 指纹须含产业/技术领域 |
| E0-4 当天成功打开结果 | 上海自然日 `success` 复用；`force=true`（「重新分析」）才新建；running 仍单飞 | 须提供「重新分析」入口 |
| wait_view | 成功 `page_mode_hint=process_succeeded_wait_view`，`viewed=false`；result 不把 viewed 改 true | D-WAITVIEW |

## 偏离说明

- 裸键 `shenzhen` 已属 SVC 白名单，政策不注册该别名，避免 Adapter 重复键。
- Feign 复用 `gkxlumen.topic.async.chain.algo-base-url`，不另加 helm 键。
- `gkxlumen-topic-policy` 的 `executeJob` 仍只声明，不在 policy 模块再开任务 API。

## 产物清单

- 代码：`lumen-svc-platform` `6b91104df4554ac545f63ef5436861793f122a24` → `origin/dev`
- 流图：`storage/POLICY/01-data-flow.md` §2.2 Job 边
- 本文 handoff

## 验收证据

- 单测 42 passed：`PolicyAnalysisTypesTest` 4 · `PolicyAnalysisAdapterImplTest` 6 · `AnalysisTaskServiceImplPolicyJobTest` 6 · `AnalysisAdapterRegistryChainTest` 3 · `AnalysisTaskServiceImplFingerprintGateTest` 8 · `AnalysisTaskServiceImplSvcJobTest` 15
- create 成功签发 `res-POLICY-1`，响应/落库不含 Python `py-stolen`
- Feign `@PostMapping("/internal/policy/jobs/execute")` · `name=lumen-algo-py` · url 不含 `demo-`
- 缺 `analysis_fp` 拒绝；running / 当天 success 复用；`force=true` 新建

## 修改内容

| 路径 | 动作 |
|------|------|
| `PolicyAnalysisTypes` | 政策白名单 + VID 规则 |
| `PolicyAnalysisAdapterImpl` + Feign | executeJob；剥离 snapshot；XOR/4万+ 校验 |
| `AnalysisTaskServiceImpl` | 政策走指纹门 + 同步签发 |
| `AnalysisTaskIdGenerator` | 前缀 `POLICY` |
| `RemotePolicyPythonClient` | 注释：C-TASK 真源在 async-service |
| `01-data-flow.md` | §2.2 Job 实线；不改工厂拓扑 |

## 测试结果

```text
mvn -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am test
  -Dtest=PolicyAnalysisTypesTest,PolicyAnalysisAdapterImplTest,AnalysisTaskServiceImplPolicyJobTest,AnalysisAdapterRegistryChainTest,AnalysisTaskServiceImplFingerprintGateTest,AnalysisTaskServiceImplSvcJobTest
# 42 passed
```

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`6b91104df4554ac545f63ef5436861793f122a24`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：不改 helm；async-service 随 `origin/dev` CI
- JDBC：未改；任务表仍跟现网 async（demo 前缀）

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-async-service`（已有）
- Job 计算 span 仍在 Python harness `gkx.polan.policy.harness`
- Tempo / Loki：本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 只校验/签发/Feign |
| 前端→Java→Python `/internal/*` | ✅ `/internal/policy/jobs/execute` |
| 图谱 Nebula | ✅ 未写 nGQL；VID 只用图上链码 |
| 可观测 | ✅ 复用 async-service + harness span |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ 未改正式 JDBC |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改口径 |
| D12 lumen 不调 demo **服务** | ✅ Feign `lumen-algo-py`；url 不含 `demo-` |
| I2-12 不自签 snapshot | ✅ Java `res-{taskId}` |
| 禁止一次 load 4 万+ | ✅ `FULL_SCAN_FORBIDDEN` |
| 禁止改算子方法 | ✅ 只调 harness |

## 遗留风险

- 现网 Job 依赖 Demo ADS/DWD 有行；空结果仍签发 snapshot（Python accepted），前端按空态+角标渲染。
- 万级须 FE/调用方走 worker `harness_mode`/fan-in；本叶 HTTP Execute 拒 ≥40000。
- D 叶须自己算 `analysis_fp` 并带「开始分析」/「重新分析」；切条件自动 create 由前端守。
- 裸键 `shenzhen` 仍是 SVC；政策请用 `policy_shenzhen`。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 115000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.76 |
| cost_warn | green |
