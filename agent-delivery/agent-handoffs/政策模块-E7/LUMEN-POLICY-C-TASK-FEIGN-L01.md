# LUMEN-POLICY-C-TASK-FEIGN-L01 · 政策 Job Feign 基址改打 gkxlumen-platform-entan-py

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 前序：[`LUMEN-POLICY-C-TASK-L01.md`](./LUMEN-POLICY-C-TASK-L01.md) · [`LUMEN-POLICY-C-BOOT-L01.md`](./LUMEN-POLICY-C-BOOT-L01.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h；bugfix：只拆 Job Feign 基址，不重做 Adapter / I2-12 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：独立配置键 + helm/Nacos + 单测断言；未改 Adapter / 指纹门 / chain Feign / 工厂拓扑 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | Feign 基址三文件，无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | Job Feign 基址对齐 §2.2 PY3：`gkxlumen-platform-entan-py`。路径仍 `POST /internal/policy/jobs/execute`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

- 政策 Job 独立键 `gkxlumen.topic.async.policy.algo-base-url`，默认 `http://gkxlumen-platform-entan-py:8000`。
- `RemotePolicyJobPythonClient` 改用该键。`name=lumen-algo-py`。路径仍 `POST /internal/policy/jobs/execute`。
- helm/Nacos `gkxlumen-topic-async-service-biz-dev.yml` 增加政策 URL；`values.yaml` 注入 `GKXLUMEN_TOPIC_ASYNC_POLICY_ALGO_BASE_URL`。
- **未改** `chain.algo-base-url` / `RemoteChainJobPythonClient`（仍 `http://lumen-platform-algo-py:8000`）。
- 禁止 `demo-platform-entan-py`。未重做 Adapter / I2-12。

## 偏离说明

- C-TASK-L01 曾写「Feign 复用 `gkxlumen.topic.async.chain.algo-base-url`」。现网 `/internal/policy` 挂 entan-api，产业链厨房无该路由，金路径 3–5 会 404。本叶纠正为独立键，与 C-BOOT `gkxlumen-topic-policy` 同基址。
- 未改 `gkxlumen-topic-policy` 的 `gkxlumen.topic.policy.algo-base-url`（查询门面已打 entan-py）。

## 产物清单

- 代码：`lumen-svc-platform` `2ef1c7907e5cfdcfaf6fbe4a8b59f779bd28dbfc` → `origin/dev`
- 流图：`storage/POLICY/01-data-flow.md` amendment（不改工厂拓扑、不翻签）
- 本文 handoff

## 验收证据

- 单测 `PolicyAnalysisAdapterImplTest.feignClientPointsAtLumenAlgoInternalExecuteNotDemo`：`url` 含 `gkxlumen-platform-entan-py`、不含 `demo-`、不含 `chain.algo-base-url`；`name=lumen-algo-py`；path=`/internal/policy/jobs/execute`
- helm `chain.algo-base-url` 仍 `http://lumen-platform-algo-py:8000`
- helm `policy.algo-base-url` = `http://gkxlumen-platform-entan-py:8000`；yml 不含 `demo-platform-entan-py:8000`
- `RemoteChainJobPythonClient` 未改
- 本机 Windows 无 mvn/JDK；源码契约用 node 核对；CI `backend:build` / `deploy:topic-async-service` 随 `origin/dev`

## 修改内容

| 路径 | 动作 |
|------|------|
| `RemotePolicyJobPythonClient` | url 键改为 `gkxlumen.topic.async.policy.algo-base-url`，默认 entan-py |
| `gkxlumen-topic-async-service-biz-dev.yml` | 增加 `async.policy.algo-base-url`；不改 chain |
| `helm/.../values.yaml` | 增加 env `GKXLUMEN_TOPIC_ASYNC_POLICY_ALGO_BASE_URL` |
| `PolicyAnalysisAdapterImplTest` | 断言 entan-py、禁 demo-、path 不变 |

## 测试结果

```text
# 本机无 JDK；契约检查（与单测同断言）
feign name=lumen-algo-py PASS
independent policy key PASS
policy not using chain key PASS
default entan-py PASS
feign url has no demo- PASS
path /internal/policy/jobs/execute PASS
chain url unchanged PASS
```

联调通过：政策 Job Feign 与 topic-policy 同打 `gkxlumen-platform-entan-py:8000`；产业链 Job 仍打 `lumen-platform-algo-py:8000`。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`2ef1c7907e5cfdcfaf6fbe4a8b59f779bd28dbfc`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines?ref=dev
- 部署：Nacos DataId 随 helm 配置；`deploy:topic-async-service` 随 `origin/dev` CI；需 `FORCE_NACOS_REPUBLISH` 才会把新键灌进现网 Nacos
- JDBC：未改

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-topic-async-service-biz`（已有）
- Tempo / Loki：本叶未抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 只改 Feign 基址 |
| 前端→Java→Python `/internal/*` | ✅ `POST /internal/policy/jobs/execute` |
| 图谱 Nebula | ✅ 未写 nGQL |
| 可观测 | ✅ 复用 async-service |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 ADS `demo_gkxlumenx_*` | ✅ 未改 JDBC |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改口径 |
| D12 lumen 不调 demo **服务** | ✅ url 默认 `gkxlumen-platform-entan-py`；禁止 `demo-platform-entan-py` |
| I2-12 不自签 snapshot | ✅ 本叶未改 Adapter / 签发 |
| 禁止改 chain Feign | ✅ `RemoteChainJobPythonClient` 未动 |
| 禁止改工厂拓扑 | ✅ `POLICY-STORAGE-FLOW` §1 未改 |

## 遗留风险

- 现网 Nacos 若未 republish，仍可能读到旧 DataId（无 `async.policy`）；Feign 占位符默认仍是 entan-py，滚动后即可打中。
- 金路径 3–5 仍依赖 entan-api 已挂 `/internal/policy/jobs/execute`（PY-JOB as-built）。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.32 |
| cost_warn | green |
