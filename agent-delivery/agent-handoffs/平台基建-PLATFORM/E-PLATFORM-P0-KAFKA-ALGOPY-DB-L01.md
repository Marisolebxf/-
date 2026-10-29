# E-PLATFORM-P0-KAFKA-ALGOPY-DB-L01 · lumen-algo-py 集群 MySQL 地址纠正

> 起因：dev 异步企业评估 `EVAL-20261018-003` 失败 `(2003) Can't connect to MySQL server on '10.50.11.76'`；`lumen-algo-py` 的 api / worker 清单把库指到集群内不可达的 10.50.11.76。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent`（协作 algorithm-agent 视角） |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 两份清单各改 1 个值 + 1 行注释，README 示例同步 1 处；未改代码逻辑、未动口令行、OTel env 未动；未用 YAGNI 跳过可观测 / 架构铁律 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 改动量极小，未启用 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无边变更：仅 `lumen-algo-py`（api/worker）→ MySQL 的物理地址由 10.50.11.76 改为 10.50.11.76，与图中同库节点一致；Kafka 边、topic 未动 |
| 会签态 | `draft`（抄 `architecture-baseline.md` §ARCH-MSG-KAFKA `signoff_status`） |

## 问题清单

- `k8s/api.yaml`、`k8s/worker.yaml` 的 `LUMEN_ALGO_MYSQL_HOST="10.50.11.76"` 在集群内不可达，worker 在 `validate/data_gather` 前即连库失败 → 任务 failed。
- 同账号 `gkxlumenx` 已在 `10.50.11.76:3306` 被 `lumen-topic-py` search/ai 使用（`k8s/dev-search-py.yaml` / `dev-ai-py.yaml`）。

## 修改内容

| 文件 | 改动 |
|------|------|
| `k8s/api.yaml` | `LUMEN_ALGO_MYSQL_HOST` → `"10.50.11.76"`，加注释「与 lumen-topic-py search/ai 对齐，勿写回旧内网地址（集群内不可达）」 |
| `k8s/worker.yaml` | 同上 |
| `k8s/README.md` | Secret 示例中的 `LUMEN_ALGO_MYSQL_HOST` 同步为 10.50.11.76 |

未改：口令行、DB 名、`MILVUS_URI`、Kafka / OTel / embed 配置、任何 Python 代码（`lumen_common/db.py` 等代码内默认值 10.50.11.76 仍在，见遗留风险）。

偏离说明：无（MILVUS_URI 按派单第 3 步结论「不改」）。

## 测试结果

### 三库 / 关键表只读核对（本机 pymysql，口令只在内存，SELECT 只读，未写库）

MySQL 8.0.39 @ 10.50.11.76:3306，账号 `gkxlumenx` 对三库均有 `ALL PRIVILEGES`（worker 需写 cfg 任务表与 ADS 评分表，权限满足）。

| 库 | 存在 | 表数 | 关键表（来自 `tasks/executor.py`、`algorithms/real_data.py`、`evaluation/*`、`science/*`、`tasks/repository.py`） |
|----|----|----|----|
| `demo_gkxlumenx_dwd` | ✅ | 139 | `enterprise_base`(50) `enterprise_industry_chain`(50) `enterprise_tag`(70) `enterprise_patent_history`(286) `enterprise_supply_chain`(19) `enterprise_risk_summary`(**0**) `enterprise_bid`(16) `enterprise_cooperation`(90) `enterprise_executive`(165) `enterprise_financing`(11) `enterprise_innovation_carrier`(13) `enterprise_invest`(12) `enterprise_news`(90) — 全部存在且可 SELECT |
| `demo_gkxlumenx_ads` | ✅ | 101 | `tech_power`(50) `biz_power`(50) — 存在且可 SELECT |
| `gkxlumenx_cfg` | ✅ | 8 | `lumen_analysis_task`(89) `lumen_analysis_task_node`(479) `lumen_analysis_task_retry`(19) — 存在且可 SELECT |

缺库：无；缺表：无。注意 `enterprise_risk_summary` 为空表（风险洞察路径可能出空结果，非连接问题）。
另：10.50 的 `lumen_analysis_task` 中查不到 `EVAL-20261018*` 行——该失败任务记录应在旧库 10.50.11.76，新库上需重新发起评估才能复测。

### Milvus 结论

- 企业评估（technology/business/competitiveness）、风险洞察（supply_chain/pain_points）、引育推荐（attraction/cultivation）三条异步路径的节点代码均**不导入** `industry_embed`；只有产业锚点 `/industry/embed/*`、政策产业 enrich、chain `graph_project` 用 Milvus。
- `open_store()` 在调用时才建连（模块 import 不连），启动不强依赖；`/healthz` 不探 Milvus。
- grep `repo-registry.yaml`、`lumen-topic-py`、`demo-svc-topic-py`、`demo-svc-platform`（含 helm values）、`lumen-svc-platform` 与编排仓 `agent-delivery`：只出现 `10.50.69.111:19530` / `192.168.88.48:19530`，**无 10.50.* Milvus 地址**。本机 TCP：`10.50.11.76:19530` 不通，`10.50.69.111:19530` 通（本机结果仅参考）。
- 结论：无可信新地址且三条路径不强依赖 → **`MILVUS_URI` 不改**，风险见下。

## 遗留风险

1. **Milvus 集群内不可达**：`MILVUS_URI=http://10.50.69.111:19530` 在集群内大概率同样不通，影响产业锚点 rebuild/search、政策产业 enrich；需 devops 确认 10.50 网段 Milvus 实例或打通网络后另起叶。
2. **代码内默认值仍为 10.50.11.76**：`lumen_common/db.py`、`algorithms/svcan/db.py`、`algorithms/chain/demo_guard.py`、`scripts/seed_chain_bottleneck_demo.py` 默认 host 仍为 `10.50.11.76`；清单 env 覆盖后无影响，但脱离清单运行会再踩坑（本叶红线禁改代码逻辑）。
3. **Secret 覆盖语义**：`envFrom: lumen-algo-mysql`（optional）在 K8s 中优先级低于 `env`，即使 Secret 里写了旧 host 也会被清单值覆盖；反之若将来要用 Secret 改 host，须先删清单里的 env 行。
4. **明文口令入 git**（既有债，与 D13「口令不进 git」冲突）：本叶红线不动口令行。
5. `enterprise_risk_summary` 空表，风险洞察可能出空态。
6. e2e:chain-gold 下游红（见 CI/CD），失败点与本改动无关且此前已持续红。

## CI/CD（必填）

- 分支：`dev`（`git pull --rebase` 后 Already up to date，直推，无 force）
- commit：`ee939a81` — `fix(k8s): 算法服务数据库地址改为 10.50.11.76 [agent:devops-agent]`（正文含任务 ID，无口令）
- pipeline：GitLab project 8 `sz-gkx/gkx-lumen/lumen-algo-py` pipeline **2557**（source=push）
  - `py:test` 13427 ✅；`image:api` 13428 ✅；`image:worker` 13429 ✅（另 image:innov/entan-* 同绿）
  - `deploy:api` **13433** ✅（自动触发，非 manual）：`deployment "lumen-platform-algo-py" successfully rolled out`
  - `deploy:worker` **13434** ✅（自动触发）：`deployment "lumen-platform-algo-py-worker" successfully rolled out`
  - `deploy:innov` / `deploy:entan-api` / `deploy:entan-worker` 为 manual，未点（非本叶）
- 镜像 tag：deploy 作业按 CI 设计用 `:latest`（`.gitlab-ci.yml` L98），image 作业同时推 `:ee939a81` 与 `:latest`，digest 一致——api `sha256:5054c242…3fcd`、worker `sha256:96a0b4e7…a258`，可证明 rollout 的就是新提交镜像。trace 中未出现 MySQL / Milvus 连接报错（deploy 作业不打 pod 日志）。
- 自动触发 `e2e:chain-gold`：bridge 13438 → lumen-ui-topic pipeline **2558** job **13439** ❌（5 failed / 1 passed）。失败为 `500 /api/enterprise/topic/v1/search/by-codes` 及页面 20s 超时；D12 demo 命中断言为空（通过）；无 MySQL/2003/Milvus 字样。此前下游 2554 / 2555 / 1326–1331 同样 failed，属既有红，需 qa-agent 另行分类。
- dev 复测：需在新库上重新发起一次企业评估异步任务确认（本叶不生产 Kafka 消息、不写库，未发起）。

## 可观测性

- OTEL_SERVICE_NAME：`lumen-platform-algo-py` / `lumen-platform-algo-py-worker`（未改）
- traceId（dev 抽样）：无（未发起业务请求）
- Tempo / Loki：无

## 架构合规自检

| 铁律 | 结果 | 说明 |
|----|----|----|
| D1 算法只在 Python | ✅ | 仅改 Python 服务部署清单 |
| D2 调用链 | ✅ | 未变 |
| D3 NebulaGraph | ✅ | 未涉及 |
| D4 可观测 | ✅ | OTel env 未动 |
| D5 CI/CD | ✅ | push → pipeline 2557 绿 → K8s dev rollout 成功 |
| D6/D12 demo 隔离 | ✅ | 新库为 lumen 共用库，未引入任何 `demo-*` 服务地址；e2e D12 断言通过（库名 `demo_gkxlumenx_*` 为既有 schema 命名，非 demo 服务） |
| D7 共享聚合核心 | ✅ | 未涉及 |
| D8/D9/D10 | N/A | 无前端 / 指标改动 |
| D13 Kafka | ✅ | 未改 bootstrap / topic；未生产消息；未动 MySQL root / 口令行；未写库 |

## 涉及文件

- `${GKX_ROOT}/repos/lumen-algo-py/k8s/api.yaml`
- `${GKX_ROOT}/repos/lumen-algo-py/k8s/worker.yaml`
- `${GKX_ROOT}/repos/lumen-algo-py/k8s/README.md`

## Cost

- Cost source: session_estimate
- actual_tokens ≈ 120k（in+out）；model_used: claude-opus（Cursor agent）；actual_cost ≈ $2.5；cost_warn: false
