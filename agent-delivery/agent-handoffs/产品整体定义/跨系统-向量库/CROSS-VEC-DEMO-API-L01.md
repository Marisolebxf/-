# CROSS-VEC-DEMO-API-L01 · demo-svc 联调门面（按钮抽槽 / Job A 限 100）

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md)；上游 [`CROSS-VEC-POLICY-SEARCH-L01.md`](./CROSS-VEC-POLICY-SEARCH-L01.md) · [`CROSS-VEC-JOB-A-L01.md`](./CROSS-VEC-JOB-A-L01.md)。联调台例外：demo → lumen Python，不是 D12 违规。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 接单时已 claimed + in_progress；lock 24h |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只加独立 Feign + 两门面；复用 Policy 包络 / lumen API-FEIGN honesty；零新 Maven 依赖。未把 enrich 接到旧 `PolicyAlgoClient` / polan。未用 YAGNI 跳过 501 honesty / limit 100 / handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §3.1（按钮）/ §3.2（Job A） |
| 图 diff | 加 demo 联调边：`demo-ui-system-test` → `demo-platform-gateway` `/policy/v1/**` → `gkx-innov` → Feign `lumen-algo-py` `/internal/*`。政策图谱边仍走 entan-py。不直连 19530 / TEI。 |
| 会签态 | `v0.3-draft`（抄 02 frontmatter，未自填绿） |

## 范围与实现

**做**：demo 联调台两条 REST 门面，只 Feign 转发 lumen-algo-py 已交契约。本波跑批硬顶 100。

### 对外路径全文（网关 → 本服务 → Python）

| 用途 | 网关（联调台打这条） | gkx-innov | Feign → lumen-algo-py |
|------|----------------------|-----------|------------------------|
| 按钮抽槽 | `POST /policy/v1/policy/industry/enrich` | `POST /v1/policy/industry/enrich` | `POST /internal/policy/industry/enrich` |
| Job A 跑批 | `POST /policy/v1/industry/jobs/enrich` | `POST /v1/industry/jobs/enrich` | `POST /internal/industry/jobs/enrich` |

网关全局剥第一段 `/policy`，故本服务路径无 `/policy` 前缀。

**兼容（不必改网关 Path）**：`POST /innov/v1/policy/industry/enrich` · `POST /innov/v1/industry/jobs/enrich`（`/innov/**` 已 StripPrefix 到本服务）。Nacos 未同步本叶 Path 扩写时，联调台可先打 `/innov/...`。

未新增 gateway route id：只扩已有 `gkx-policy-graph` 的 Path，避免 `/policy/**` catch-all 直连 `demo-platform-entan-py`。

### Feign 目标

| 项 | 值 |
|---|---|
| Client | `com.topcomm.gkx.innov.policy.LumenAlgoClient` |
| Feign `name` / `contextId` | `lumen-algo` / `lumenAlgoClient` |
| base-url 键 | `gkx.innov.lumen-algo.algo-base-url` |
| env | `INNOV_LUMEN_ALGO_BASE_URL` |
| K8s 值 | `http://lumen-platform-algo-py:8000` |
| 禁止 | `INNOV_POLICY_ALGO_BASE_URL` / `demo-platform-entan-py` / `PolicyAlgoClient` |

仓内原先无指向 `lumen-platform-algo-py` / `gkxlumen-platform-entan-py` 的 innov 配置，本叶新增独立键，不复用 polan。

### 给 UI 的请求体

按钮：

```json
{"policy_id":"P001"}
```

或 `{"policy_ids":["P001","P002"]}`，或筛选 + 小 `limit`（Python 封顶 20）。**不要**带 `cursor` / `mode=incremental|full`（那是 Job A → 400）。

跑批：

```json
{"mode":"incremental","force":false,"cursor":"","limit":100}
```

续跑带 `job_id` + `next_cursor`。`limit` 缺省 100；`limit>100` Java 与 Python 都 400。

成功包络与 Python 一致：`{code,msg,data}`。`data` 含 `items`（按钮）或 `job_id` / `processed` / `skipped` / `coded` / `failed` / `status` / `index_version` / `next_cursor` / `degraded` / `limit_cap`（跑批）。Java **不**把 `score` 加工成 `chain:` 码。

### 501 / 400 / 409 映射

| 条件 | HTTP | 体 |
|------|------|-----|
| Python 200 且 `code=0` 且非 degraded | 200 | 原样包络 |
| `limit>100`（Java 先拦） | 400 | `{code:1,msg:本波验证闸…,data:{limit_cap:100}}` |
| Python 400（按钮 cursor/full、坏 mode） | 400 | Python 原样 |
| Python 409（第二份 full 单飞） | 409 | Python 原样（**不是** 501） |
| Python 422（collection guard） | 422 | Python 原样 |
| Python 503 / `degraded=true` / `code≠0` / 不可达 / 空体 | **501** | honesty：`engine=not_ready:python_503` 等；`items=[]`；`fabricated=false`。不漏 search hit / score |

对照 lumen `IndustryFacadeController` API-FEIGN：未就绪禁止 200 假码。

**不做**：改前端；改 Python；直连 19530 / TEI；万级放开。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 本机无 JDK / Maven / Docker，未跑 `mvn test` | 验收走 GitLab CI `backend:build`（镜像 `maven:3.9.6-eclipse-temurin-17`） |
| 2 | 未对现网 DWD 实打 search 写槽 | 与 SEARCH / JOB-A 同：人机验证在联调台；本叶单测锁死映射 |
| 3 | 扩已有网关 Path，不是「零 yaml」 | 否则建议的 `/policy/v1/policy/industry/**` 会进 entan-py catch-all。未新增 route id |

## 产物清单

- `gkx-innov/.../policy/LumenAlgoClient.java`
- `gkx-innov/.../policy/PolicyIndustryEnrichService.java`
- `gkx-innov/.../policy/PolicyIndustryEnrichController.java`
- `gkx-innov/.../policy/PolicyIndustryEnrichServiceTest.java`
- `gkx-innov/src/main/resources/application.yml`（`gkx.innov.lumen-algo`）
- `helm/gkx-platform/values.yaml`（`INNOV_LUMEN_ALGO_BASE_URL`）
- `helm/gkx-platform/configs/gkx-innov-dev.yml`
- `helm/gkx-platform/configs/gkx-gateway-dev.yml`（扩 `gkx-policy-graph` Path）
- 本 handoff

## 验收证据

### 1. 对外路径

见上表。Service = `gkx-innov`；Feign Service/键 = `lumen-algo` / `gkx.innov.lumen-algo.algo-base-url`。

### 2. 单测（本机待 CI）

`PolicyIndustryEnrichServiceTest`：`limit>100` 不调 Python；409 保持冲突；400 不升 501；503 → 501 且 items 空、无 `chain:`；成功路径不改写已有 `industry_link_code`。

### 3. 编译

push `origin/dev` 后 GitLab CI `backend:build`。

## 问题清单 / 开放项

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | 联调台按钮 / 跑批页 | `CROSS-VEC-DEMO-UI-L01` | 不改前端 |
| B | 现网 Nacos `gkx-gateway-dev.yml` 同步本叶 Path | devops / 本仓 deploy | 未同步时用 `/innov/v1/...` |
| C | 万级放开 100 封顶 | 另叶 | 本波验证闸 |

## 修改内容

| 文件 | 行为 |
|------|------|
| `LumenAlgoClient` | 两条 `/internal/*`，打 lumen-algo-py |
| `PolicyIndustryEnrichService` | 转发 + 400/409/501 映射；不写链码 |
| `PolicyIndustryEnrichController` | 两 POST |
| helm / application.yml | 新 base-url；扩网关 Path |

## 测试结果

- 单测 5 例（逻辑已写；本机无 mvn，CI 跑）
- 未直连 Milvus / TEI；未新依赖

## 遗留风险

- Nacos 网关未同步则 `/policy/v1/policy/industry/**` 仍进 entan-py（404/错进程）
- `lumen-platform-algo-py` 须与 demo 同集群可解析（`demo-svc-topic-py` 已用此 DNS）
- Job A 进程内单飞，多副本各记各的

## CI/CD（必填）

- 分支：`demo-svc-platform` `origin/dev`（先 `git pull --ff-only`）
- commit：**`e0601dbe1d567d6ba4963016465ee6be4a425e19`** `feat(policy): add industry enrich facades to lumen-algo-py` `[agent:api-agent]`
- pipeline：push 触发 GitLab CI
- K8s rollout：gkx-innov + 网关 Nacos 配置
- dev 测试：单测 + 联调台（UI 后叶）

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkx-innov`（已有）
- Feign 由 Java Agent 注 W3C traceparent
- 不写查询全文到日志

## 涉及文件

- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/LumenAlgoClient.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyIndustryEnrichService.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyIndustryEnrichController.java`
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyAlgoClient.java`（注释：enrich 勿加本接口）
- `gkx-innov/src/test/java/com/topcomm/gkx/innov/policy/PolicyIndustryEnrichServiceTest.java`
- `gkx-innov/src/main/resources/application.yml`
- `helm/gkx-platform/values.yaml`
- `helm/gkx-platform/configs/gkx-innov-dev.yml`
- `helm/gkx-platform/configs/gkx-gateway-dev.yml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python `/internal/*` | ✅ Java 只 Feign；零 NLP |
| 调用链不可越层 | ✅ 前端 → Java → Python `/internal/*` |
| 图谱仅 Nebula | ✅ 未直连图；定码仍在 Python |
| 可观测 | ✅ 沿用 gkx-innov OTel / Feign Agent |
| CI/CD | ✅ push `origin/dev`，未 force；`[agent:api-agent]` |
| D12 | ✅ 本叶是 **demo 调 lumen Python**（联调台例外，任务书点名）；lumen 前端未调 demo |
| 数据策略 | ✅ 不写 ADS；不直连 19530 |
| Java 不写算法 | ✅ 不改 score / 不拼 `chain:` |
| D8 / D9 / D10 | N/A（无 UI / 无指标卡） |
| 零新 Maven 依赖 | ✅ |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.51 |
| cost_warn | green |

口径：api 默认 80/20；B 档 `$3/$15` per 1M；`95000×0.80×3/1e6 + 95000×0.20×15/1e6 = 0.51`。
