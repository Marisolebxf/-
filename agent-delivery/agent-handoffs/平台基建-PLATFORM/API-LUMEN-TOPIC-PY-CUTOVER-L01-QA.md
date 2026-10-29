# API-LUMEN-TOPIC-PY-CUTOVER-L01-QA · Java Feign/helm 切到 lumen-topic-py 验收

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控已授权；父会话已认领并推进 `testing`，本叶未再 claim） |
| 说明 | D12-DEBT-TOPIC-PY 第 3 叶 QA。测 Java 切流/隔离，不改 `lumen-svc-platform` 源码。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 写测 / 段 E 冒烟；对照 helm 与现网 env，未跳过 D12。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom。 |

## 问题清单

- 无 P0 缺陷。未开缺陷包。
- **WARN（不挡切流）**：`POST /topicAsync/topic/v1/analysis/tasks` 返回 200/`code=1`（`subType` 校验：只允许 technology/business/competitiveness），未下发厨房。`POST …/tasks/list` 200/`code=0`。厨房失败本就不挡切流。
- git 中 `demo-platform-search-py` / `demo-platform-ai-py` 仅出现在 **禁止回落注释**，values/env 实际 URL 为 `gkxlumen-platform-*-py`。

## 修改内容

- 无代码变更，仅验收。

## 测试结果

测试时间：2026-08-14 14:51–14:55 +08。网关 `http://10.50.69.111:30899`；前端 `http://10.50.69.111:30892` HTTP 200。

| # | 用例 | 证据 | 结果 |
|---|------|------|------|
| 1 | filters 金路径 | `POST /enterprise/topic/v1/search/meta/filters` HTTP **200** `code=0`，含 `listing_statuses`/`operating_statuses`；**202ms**；`X-Trace-Id=338e664a81c06d9c0fd48d21f2df67a1` | **PASS** |
| 2 | 检索/画像一条 | `POST /search/hot` **200** `code=0` 有热词；`X-Trace-Id=cf4ff92c186140870b15c0be9ae9ae48`。suggest/query 诚实空态 200。`profile/card` 200/`code=1` 企业不存在（诚实失败，未 5xx） | **PASS** |
| 3 | 隔离 | 网关响应与 Tempo 均无 `30805` / `demo-platform-search-py` / `demo-platform-ai-py` | **PASS** |
| 4 | demo 仍活 | `GET :30805/healthz` **200** `gkx-search-service`；demo Pod 1/1 | **PASS** |
| 5 | 三件套 Ready + `gkxlumen-*` 镜像 | 与 PY-PORT-QA 同表；tag `5d204114` | **PASS** |
| 6 | Java 配置未回落 demo | 现网 env + git helm 见下 | **PASS** |
| 7 | 分析任务（可选） | list 200；create 校验拒绝，未打厨房 | **WARN**（不挡） |
| 8 | CI | Java pipeline **5027** helm/enterprise/async success | **PASS** |

### Java 现网 env（`kubectl -n dev get deploy -o yaml`）

| Deployment | 环境变量 | 值 |
|------------|----------|-----|
| `gkxlumen-platform-topic-enterprise` | `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL` | `http://gkxlumen-platform-search-py:8080` |
| `gkxlumen-platform-topic-async-service` | `GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL` | `http://gkxlumen-platform-ai-py:8081` |

两 Java Pod 均为 1/1 Running（约 35min）。enterprise 日志可见 `Refresh keys changed: [gkxlumen.topic.enterprise.python-base-url]`。

### git 只读对照（`lumen-svc-platform`）

| 文件 | 结论 |
|------|------|
| `helm/gkxlumen-platform/values.yaml` | enterprise/async env 直连 `gkxlumen-platform-search-py:8080` / `gkxlumen-platform-ai-py:8081` |
| `helm/.../gkxlumen-topic-enterprise-biz-dev.yml` | `python-base-url: "http://gkxlumen-platform-search-py:8080"` |
| `helm/.../gkxlumen-topic-async-service-biz-dev.yml` | `python-ai-base-url: "http://gkxlumen-platform-ai-py:8081"`；`python-ai-service-name: gkxlumen-ai-service` |

### Tempo（证明 Java 打的是 lumen Python）

- TraceID `338e664a81c06d9c0fd48d21f2df67a1`
- `service.name`：`gkxlumen-gateway` → `gkxlumen-topic-enterprise-biz` → **`gkxlumen-search-service`**
- 属性含 `gkxlumen-platform-search-py`；**0** 次 `demo-platform-*` / `30805` / `gkx-search-service`

## 遗留风险

- D12-DEBT-INNOV-PY / D12-DEBT-ENTAN-PY 仍开。
- DWD 未切库。
- 关闭 **D12-DEBT-TOPIC-PY** 条件（helm 绿 + 企业检索 filters 200 + 现网 URL 指向 lumen-topic-py）：**QA 复测满足**，待 `human:淮政玮` 签收两叶。

## CI/CD（必填）

- 分支：`dev`
- commit：`1ceb8e3`（`lumen-svc-platform`）
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5027  
  `helm:deploy` [#21542](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21542)、`deploy:topic-enterprise` [#21544](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21544)、`deploy:topic-async-service` [#21545](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21545) **success**（本 QA **不重跑**）
- 部署 namespace：`dev`
- K8s rollout：topic-enterprise / topic-async-service 1/1 Running
- dev 测试 URL：`POST http://10.50.69.111:30899/enterprise/topic/v1/search/meta/filters` → 200 `code=0`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-enterprise-biz` / `gkxlumen-topic-async-service-biz`
- 下游 Python：`gkxlumen-search-service`（Tempo 已见）
- traceId：`338e664a81c06d9c0fd48d21f2df67a1`
- Tempo / Loki：Tempo **有**

## 涉及文件

- 无业务仓改动。
- 本 handoff：`agent-delivery/agent-handoffs/平台基建-PLATFORM/API-LUMEN-TOPIC-PY-CUTOVER-L01-QA.md`
- 开发 handoff：`…/API-LUMEN-TOPIC-PY-CUTOVER-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ Java 只转发 |
| 2 调用链 | ✅ 网关 → Java → lumen-topic-py `/internal` |
| 3 Nebula | ✅ 未改 |
| 4 可观测 | ✅ Tempo 跨 gateway/Java/Python |
| 5 CI/CD | ✅ 5027 证据 |
| 6 禁止 merge demo | ✅ |
| 7 共享聚合 | ✅ |
| 8 数据 | ✅ 未切库 |
| 9–11 D8/D9/D10 | N/A |
| 12 D12 | ✅ 现网 env 无 demo 回落；流量未打 30805 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 0.45 |
| cost_warn | green |
